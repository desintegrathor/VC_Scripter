"""
Cover (live range) tracking for variable merging.

This module provides cover tracking for SSA values, which represents
where a value is "live" (defined but not yet consumed by all uses).

Modeled after Ghidra's cover.hh - covers are used to determine which
SSA values can be merged into the same source-level variable (those
with non-overlapping covers can share a name).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from ...ssa import SSAValue


@dataclass
class CoverPiece:
    """
    A single contiguous piece of a cover.

    Represents a range within a single basic block where a value is live.
    """
    block_id: int
    start_addr: int  # First address where value is live
    end_addr: int    # Last address where value is live

    def overlaps(self, other: "CoverPiece") -> bool:
        """Check if this piece overlaps with another."""
        if self.block_id != other.block_id:
            return False
        return not (self.end_addr < other.start_addr or other.end_addr < self.start_addr)

    def adjacent(self, other: "CoverPiece") -> bool:
        """Check if this piece is adjacent to another (can be merged)."""
        if self.block_id != other.block_id:
            return False
        return (self.end_addr + 1 >= other.start_addr or
                other.end_addr + 1 >= self.start_addr)

    def merge(self, other: "CoverPiece") -> Optional["CoverPiece"]:
        """Merge with another piece if overlapping or adjacent."""
        if self.block_id != other.block_id:
            return None
        if not self.overlaps(other) and not self.adjacent(other):
            return None

        return CoverPiece(
            block_id=self.block_id,
            start_addr=min(self.start_addr, other.start_addr),
            end_addr=max(self.end_addr, other.end_addr)
        )

    def contains(self, block_id: int, addr: int) -> bool:
        """Check if this piece contains a specific point."""
        return (self.block_id == block_id and
                self.start_addr <= addr <= self.end_addr)


@dataclass
class Cover:
    """
    Complete cover (live range) for an SSA value.

    A cover is a set of CoverPieces representing all points in the
    program where the value is live.
    """
    pieces: List[CoverPiece] = field(default_factory=list)

    def add_piece(self, piece: CoverPiece):
        """Add a piece to the cover, merging with existing if possible."""
        # Try to merge with existing pieces
        for i, existing in enumerate(self.pieces):
            merged = existing.merge(piece)
            if merged is not None:
                self.pieces[i] = merged
                self._consolidate()
                return

        self.pieces.append(piece)

    def add_def_point(self, block_id: int, addr: int):
        """Add a definition point to the cover."""
        self.add_piece(CoverPiece(block_id, addr, addr))

    def add_use_point(self, block_id: int, addr: int):
        """Add a use point to the cover."""
        # Extend existing piece in same block or add new
        for piece in self.pieces:
            if piece.block_id == block_id:
                if addr >= piece.start_addr:
                    piece.end_addr = max(piece.end_addr, addr)
                    return
                elif addr < piece.start_addr:
                    piece.start_addr = addr
                    return

        self.add_piece(CoverPiece(block_id, addr, addr))

    def add_range(self, block_id: int, start: int, end: int):
        """Add a range to the cover."""
        self.add_piece(CoverPiece(block_id, start, end))

    def intersects(self, other: "Cover") -> bool:
        """Check if this cover intersects with another."""
        for p1 in self.pieces:
            for p2 in other.pieces:
                if p1.overlaps(p2):
                    return True
        return False

    def contains(self, block_id: int, addr: int) -> bool:
        """Check if the cover contains a specific point."""
        for piece in self.pieces:
            if piece.contains(block_id, addr):
                return True
        return False

    def merge(self, other: "Cover"):
        """Merge another cover into this one."""
        for piece in other.pieces:
            self.add_piece(piece)

    def is_empty(self) -> bool:
        """Check if cover is empty."""
        return len(self.pieces) == 0

    def get_block_ids(self) -> Set[int]:
        """Get all block IDs in this cover."""
        return {p.block_id for p in self.pieces}

    def _consolidate(self):
        """Consolidate overlapping/adjacent pieces."""
        if len(self.pieces) <= 1:
            return

        # Sort by block then start address
        self.pieces.sort(key=lambda p: (p.block_id, p.start_addr))

        # Merge adjacent pieces
        consolidated = []
        current = self.pieces[0]

        for piece in self.pieces[1:]:
            merged = current.merge(piece)
            if merged is not None:
                current = merged
            else:
                consolidated.append(current)
                current = piece

        consolidated.append(current)
        self.pieces = consolidated


def compute_cover(value: "SSAValue", ssa_func) -> Cover:
    """
    Compute the cover for an SSA value.

    Args:
        value: The SSA value
        ssa_func: SSA function containing the value

    Returns:
        Cover representing where the value is live
    """
    cover = Cover()

    # Get definition point
    if hasattr(value, 'def_block') and hasattr(value, 'def_addr'):
        cover.add_def_point(value.def_block, value.def_addr)

    # Get use points
    if hasattr(value, 'uses'):
        for use in value.uses:
            if hasattr(use, 'block_id') and hasattr(use, 'addr'):
                cover.add_use_point(use.block_id, use.addr)

    return cover
