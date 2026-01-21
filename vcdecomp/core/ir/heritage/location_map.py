"""
Location tracking for heritage-based SSA construction.

This module tracks which memory locations (stack slots, parameters, globals)
have been heritaged (converted to SSA form) and in which pass. This allows
incremental SSA construction to avoid redundant work and track when new
variables are discovered.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple


class AddressSpace(Enum):
    """Memory address spaces for heritage tracking."""
    STACK = auto()      # Local stack variables (positive offsets from SP)
    PARAM = auto()      # Function parameters (negative offsets from SP)
    GLOBAL = auto()     # Global variables (data segment)
    REGISTER = auto()   # Virtual registers (internal)


@dataclass
class HeritageRange:
    """
    A range of memory that has been heritaged.

    Attributes:
        space: The address space (stack, param, global, register)
        offset: Byte offset within the address space
        size: Size in bytes
        pass_number: Pass in which this range was heritaged
        var_name: Optional variable name assigned during heritage
    """
    space: AddressSpace
    offset: int
    size: int
    pass_number: int
    var_name: Optional[str] = None

    def overlaps(self, other: "HeritageRange") -> bool:
        """Check if this range overlaps with another range."""
        if self.space != other.space:
            return False
        # Ranges overlap if neither is completely before or after the other
        return not (self.offset + self.size <= other.offset or
                    other.offset + other.size <= self.offset)

    def contains(self, space: AddressSpace, offset: int, size: int) -> bool:
        """Check if this range fully contains the specified location."""
        if self.space != space:
            return False
        return (self.offset <= offset and
                offset + size <= self.offset + self.size)


class LocationMap:
    """
    Track which memory locations have been heritaged and when.

    This is the core data structure for incremental SSA construction.
    It allows the heritage orchestrator to:
    1. Check if a location has already been heritaged
    2. Determine which pass discovered a variable
    3. Find newly discovered variables in each pass
    4. Track variable splitting when locations are reused
    """

    def __init__(self) -> None:
        """Initialize an empty location map."""
        # Ranges organized by address space for efficient lookup
        self._ranges: Dict[AddressSpace, List[HeritageRange]] = {
            space: [] for space in AddressSpace
        }
        self._current_pass: int = 0

        # Map from (space, offset) to list of ranges at that offset
        # Used for efficient overlap detection
        self._offset_index: Dict[Tuple[AddressSpace, int], List[HeritageRange]] = {}

        # Track variables discovered in each pass
        self._pass_discoveries: Dict[int, Set[str]] = {}

    @property
    def current_pass(self) -> int:
        """Current heritage pass number."""
        return self._current_pass

    def advance_pass(self) -> None:
        """Advance to the next heritage pass."""
        self._current_pass += 1
        self._pass_discoveries[self._current_pass] = set()

    def is_heritaged(
        self, space: AddressSpace, offset: int, size: int
    ) -> Tuple[bool, Optional[int]]:
        """
        Check if a memory location has been heritaged.

        Args:
            space: Address space to check
            offset: Byte offset within the space
            size: Size of the location in bytes

        Returns:
            (is_heritaged, pass_number) tuple.
            pass_number is None if not heritaged.
        """
        for range_obj in self._ranges[space]:
            if range_obj.contains(space, offset, size):
                return True, range_obj.pass_number

        return False, None

    def mark_heritaged(
        self,
        space: AddressSpace,
        offset: int,
        size: int,
        var_name: Optional[str] = None
    ) -> HeritageRange:
        """
        Mark a memory location as heritaged.

        Args:
            space: Address space
            offset: Byte offset within the space
            size: Size in bytes
            var_name: Optional variable name

        Returns:
            The HeritageRange object created
        """
        new_range = HeritageRange(
            space=space,
            offset=offset,
            size=size,
            pass_number=self._current_pass,
            var_name=var_name
        )

        self._ranges[space].append(new_range)

        # Update offset index
        key = (space, offset)
        if key not in self._offset_index:
            self._offset_index[key] = []
        self._offset_index[key].append(new_range)

        # Track discovery
        if var_name:
            if self._current_pass not in self._pass_discoveries:
                self._pass_discoveries[self._current_pass] = set()
            self._pass_discoveries[self._current_pass].add(var_name)

        return new_range

    def get_overlapping_ranges(
        self, space: AddressSpace, offset: int, size: int
    ) -> List[HeritageRange]:
        """
        Find all heritaged ranges that overlap with a location.

        This is useful for detecting variable splitting - when a single
        stack slot is used for multiple semantically different variables.

        Args:
            space: Address space
            offset: Byte offset
            size: Size in bytes

        Returns:
            List of overlapping HeritageRange objects
        """
        target = HeritageRange(space, offset, size, 0)
        return [r for r in self._ranges[space] if r.overlaps(target)]

    def get_discoveries_in_pass(self, pass_number: int) -> Set[str]:
        """Get variable names discovered in a specific pass."""
        return self._pass_discoveries.get(pass_number, set()).copy()

    def get_all_heritaged_in_space(self, space: AddressSpace) -> List[HeritageRange]:
        """Get all heritaged ranges in an address space."""
        return self._ranges[space].copy()

    def get_unheritaged_offsets(
        self,
        space: AddressSpace,
        candidate_offsets: Set[int],
        size: int = 4
    ) -> Set[int]:
        """
        Filter offsets to only those not yet heritaged.

        Args:
            space: Address space
            candidate_offsets: Set of offsets to check
            size: Size of each location (default 4 bytes / dword)

        Returns:
            Set of offsets that are not yet heritaged
        """
        result = set()
        for offset in candidate_offsets:
            is_done, _ = self.is_heritaged(space, offset, size)
            if not is_done:
                result.add(offset)
        return result

    def clear(self) -> None:
        """Clear all heritage tracking data."""
        for space in AddressSpace:
            self._ranges[space] = []
        self._offset_index.clear()
        self._pass_discoveries.clear()
        self._current_pass = 0

    def __repr__(self) -> str:
        total = sum(len(ranges) for ranges in self._ranges.values())
        return f"LocationMap(pass={self._current_pass}, ranges={total})"
