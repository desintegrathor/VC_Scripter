"""
Basic collapse rule for sequential block merging.

This module contains RuleBlockCat, the simplest collapse rule that merges
fall-through blocks into a BlockList.
"""

from __future__ import annotations

from typing import Optional

from .base import CollapseRule
from ...blocks.hierarchy import EdgeType, BlockGraph, StructuredBlock


class RuleBlockCat(CollapseRule):
    """
    Collapse sequential blocks into a BlockList.

    Pattern:
        A -> B  (A has single successor B, B has single predecessor A)

    Result:
        BlockList([A, B])

    This is the most basic collapse - combining fall-through blocks.
    """

    def __init__(self):
        super().__init__("BlockCat")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # Block must have exactly one successor
        if not block.has_single_successor():
            return False

        successor = block.get_single_successor()
        if successor is None or successor.is_collapsed:
            return False

        # Successor must have exactly one predecessor (this block)
        if not successor.has_single_predecessor():
            return False

        # Don't collapse self-loops
        if successor == block:
            return False

        # Don't collapse across back edges
        for edge in block.out_edges:
            if edge.target == successor and edge.edge_type == EdgeType.BACK_EDGE:
                return False

        return True

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        successor = block.get_single_successor()
        if successor is None:
            return None

        # Merge the blocks
        return graph.merge_blocks(block, successor)
