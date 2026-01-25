"""
Variable merge engine for SSA-to-source transformation.

This module provides the merge engine that combines multiple SSA values
into source-level variables based on:
1. Forced merges (PHI inputs, globals, same stack location)
2. Speculative merges (same type, non-overlapping covers)

Modeled after Ghidra's merge.cc merge engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, TYPE_CHECKING
import logging

from .cover import Cover, compute_cover
from .high_variable import HighVariable, create_high_variable

if TYPE_CHECKING:
    from ...ssa import SSAFunction, SSAValue

logger = logging.getLogger(__name__)


@dataclass
class MergeGroup:
    """A group of SSA values that should be merged."""
    reason: str  # Why these are grouped
    values: List["SSAValue"] = field(default_factory=list)


class MergeEngine:
    """
    Engine for merging SSA values into source-level variables.

    The merge process has several phases:
    1. Build covers for all SSA values
    2. Forced merges (PHI, globals, stack)
    3. Speculative merges (compatible types, non-overlapping)
    """

    def __init__(self, ssa_func: "SSAFunction"):
        self.ssa_func = ssa_func
        self.covers: Dict[str, Cover] = {}  # value.name -> Cover
        self.high_variables: List[HighVariable] = []
        self.value_to_high: Dict[str, HighVariable] = {}  # value.name -> HighVariable

    def build_covers(self):
        """
        Build covers for all SSA values.

        Computes the live range (cover) for each value based on
        definition and use points.
        """
        if not hasattr(self.ssa_func, 'values'):
            return

        for value in self.ssa_func.values.values():
            cover = compute_cover(value, self.ssa_func)
            self.covers[value.name] = cover

    def merge_forced(self):
        """
        Perform forced merges.

        Forced merges include:
        1. PHI inputs - all inputs to a PHI must be same variable
        2. Global variables - all refs to same global
        3. Stack locations - same stack offset in same function
        """
        # Group by forced relationships
        groups = self._find_forced_groups()

        for group in groups:
            if len(group.values) <= 1:
                continue

            # Create or find HighVariable for first value
            first = group.values[0]
            hv = self._get_or_create_high(first)

            # Merge remaining values
            for value in group.values[1:]:
                if value.name in self.value_to_high:
                    # Already assigned - merge the high variables
                    other_hv = self.value_to_high[value.name]
                    if other_hv != hv:
                        hv.merge(other_hv)
                        # Update mappings
                        for inst in other_hv.instances:
                            self.value_to_high[inst.name] = hv
                        self.high_variables.remove(other_hv)
                else:
                    # Add to this HighVariable
                    cover = self.covers.get(value.name, Cover())
                    hv.add_instance(value, cover)
                    self.value_to_high[value.name] = hv

    def merge_speculative(self):
        """
        Perform speculative merges.

        Speculative merges combine variables with:
        1. Same data type
        2. Non-overlapping covers
        3. Similar naming patterns
        """
        # Get unassigned values
        unassigned = []
        for value in self.ssa_func.values.values():
            if value.name not in self.value_to_high:
                unassigned.append(value)

        # Sort by name for consistent ordering
        unassigned.sort(key=lambda v: v.name)

        # Try to merge each unassigned into existing HighVariable
        for value in unassigned:
            cover = self.covers.get(value.name, Cover())
            merged = False

            # Try existing HighVariables
            for hv in self.high_variables:
                if self._can_merge_speculative(value, cover, hv):
                    hv.add_instance(value, cover)
                    self.value_to_high[value.name] = hv
                    merged = True
                    break

            # Create new HighVariable if not merged
            if not merged:
                hv = create_high_variable(value, cover)
                self.high_variables.append(hv)
                self.value_to_high[value.name] = hv

    def get_high_variables(self) -> List[HighVariable]:
        """Get all HighVariables after merging."""
        return self.high_variables

    def get_high_for_value(self, value_name: str) -> Optional[HighVariable]:
        """Get the HighVariable for a given SSA value name."""
        return self.value_to_high.get(value_name)

    def _find_forced_groups(self) -> List[MergeGroup]:
        """Find groups of values that must be merged."""
        groups = []

        # PHI groups
        phi_groups = self._find_phi_groups()
        groups.extend(phi_groups)

        # Global variable groups
        global_groups = self._find_global_groups()
        groups.extend(global_groups)

        # Stack location groups
        stack_groups = self._find_stack_groups()
        groups.extend(stack_groups)

        return groups

    def _find_phi_groups(self) -> List[MergeGroup]:
        """Find groups based on PHI node inputs."""
        groups = []

        if not hasattr(self.ssa_func, 'phi_nodes'):
            return groups

        for phi in self.ssa_func.phi_nodes:
            group = MergeGroup(reason="phi")

            # Add PHI output
            if hasattr(phi, 'output'):
                group.values.append(phi.output)

            # Add PHI inputs
            if hasattr(phi, 'inputs'):
                for inp in phi.inputs:
                    if inp not in group.values:
                        group.values.append(inp)

            if len(group.values) > 1:
                groups.append(group)

        return groups

    def _find_global_groups(self) -> List[MergeGroup]:
        """Find groups of global variable references."""
        groups = []
        global_refs: Dict[int, List["SSAValue"]] = {}

        for value in self.ssa_func.values.values():
            if hasattr(value, 'metadata') and value.metadata.get('is_global'):
                offset = value.metadata.get('global_offset')
                if offset is not None:
                    if offset not in global_refs:
                        global_refs[offset] = []
                    global_refs[offset].append(value)

        for offset, values in global_refs.items():
            if len(values) > 1:
                groups.append(MergeGroup(reason=f"global_{offset}", values=values))

        return groups

    def _find_stack_groups(self) -> List[MergeGroup]:
        """Find groups of stack location references."""
        groups = []
        stack_refs: Dict[int, List["SSAValue"]] = {}

        for value in self.ssa_func.values.values():
            if hasattr(value, 'metadata'):
                offset = value.metadata.get('stack_offset')
                if offset is not None and not value.metadata.get('is_global'):
                    if offset not in stack_refs:
                        stack_refs[offset] = []
                    stack_refs[offset].append(value)

        for offset, values in stack_refs.items():
            if len(values) > 1:
                groups.append(MergeGroup(reason=f"stack_{offset}", values=values))

        return groups

    def _get_or_create_high(self, value: "SSAValue") -> HighVariable:
        """Get existing HighVariable for value or create new one."""
        if value.name in self.value_to_high:
            return self.value_to_high[value.name]

        cover = self.covers.get(value.name, Cover())
        hv = create_high_variable(value, cover)
        self.high_variables.append(hv)
        self.value_to_high[value.name] = hv
        return hv

    def _can_merge_speculative(
        self,
        value: "SSAValue",
        cover: Cover,
        hv: HighVariable
    ) -> bool:
        """Check if value can be speculatively merged into HighVariable."""
        # Covers must not intersect
        if hv.cover.intersects(cover):
            return False

        # Types should match (if both known)
        if hasattr(value, 'value_type') and value.value_type is not None:
            if hv.data_type is not None and hv.data_type != value.value_type:
                return False

        # Don't merge globals with locals
        is_global = False
        if hasattr(value, 'metadata'):
            is_global = value.metadata.get('is_global', False)
        if hv.is_global != is_global:
            return False

        return True


def merge_ssa_values(ssa_func: "SSAFunction") -> List[HighVariable]:
    """
    Merge SSA values into high-level variables.

    Convenience function that runs the full merge process.

    Args:
        ssa_func: SSA function to process

    Returns:
        List of merged HighVariables
    """
    engine = MergeEngine(ssa_func)
    engine.build_covers()
    engine.merge_forced()
    engine.merge_speculative()
    return engine.get_high_variables()
