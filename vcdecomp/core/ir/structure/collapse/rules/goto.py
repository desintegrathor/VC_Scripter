"""
Goto collapse rule for unstructured control flow.

This module contains the fallback rule for marking unstructured edges as goto.
"""

from __future__ import annotations

from typing import Optional

from .base import CollapseRule
from ...blocks.hierarchy import (
    BlockType,
    EdgeType,
    BlockGraph,
    StructuredBlock,
    BlockGoto,
    BlockEdge,
)


class RuleBlockGoto(CollapseRule):
    """
    Mark unstructured edges as goto.

    This is the fallback rule when no structured pattern matches.
    It wraps a block with unstructured outgoing edges in a BlockGoto.
    """

    def __init__(self):
        super().__init__("BlockGoto")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # Only match if block has outgoing edges that haven't been structured
        if block.is_collapsed:
            return False

        # Check if any outgoing edge is marked as irreducible or goto
        for edge in block.out_edges:
            if edge.edge_type in (EdgeType.IRREDUCIBLE, EdgeType.GOTO_EDGE):
                return True

        return False

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        # Find the unstructured target
        goto_target = None
        for edge in block.out_edges:
            if edge.edge_type in (EdgeType.IRREDUCIBLE, EdgeType.GOTO_EDGE):
                goto_target = edge.target
                break

        if goto_target is None:
            return None

        # Create goto block
        goto_block = BlockGoto(
            block_type=BlockType.GOTO,
            block_id=graph._allocate_block_id(),
            wrapped_block=block,
            goto_target=goto_target,
        )

        goto_block.covered_blocks = block.covered_blocks

        # Set parent
        block.parent = goto_block

        # Redirect edges
        for edge in block.in_edges:
            if not edge.source.is_collapsed:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=goto_block,
                    edge_type=edge.edge_type
                )
                goto_block.in_edges.append(new_edge)
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[i] = new_edge

        # Copy non-goto outgoing edges
        for edge in block.out_edges:
            if edge.edge_type not in (EdgeType.IRREDUCIBLE, EdgeType.GOTO_EDGE):
                new_edge = BlockEdge(
                    source=goto_block,
                    target=edge.target,
                    edge_type=edge.edge_type
                )
                goto_block.out_edges.append(new_edge)

        # Add goto_block
        graph.blocks[goto_block.block_id] = goto_block
        if graph.entry_block == block:
            graph.entry_block = goto_block

        graph.remove_block(block)

        return goto_block
