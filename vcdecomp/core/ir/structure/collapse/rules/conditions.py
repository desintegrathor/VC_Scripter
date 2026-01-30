"""
Boolean condition collapse rules.

This module contains rules for collapsing AND/OR boolean condition patterns
(short-circuit evaluation).
"""

from __future__ import annotations

from typing import Optional

from .base import CollapseRule
from ...blocks.hierarchy import (
    BlockType,
    EdgeType,
    BlockGraph,
    StructuredBlock,
    BlockCondition,
    BlockEdge,
)


class RuleBlockOr(CollapseRule):
    """
    Collapse AND/OR boolean conditions (short-circuit evaluation).

    Pattern (OR - ||):
        cond1 --true--> target
        cond1 --false--> cond2 --true--> target
                         cond2 --false--> other

    Pattern (AND - &&):
        cond1 --false--> other
        cond1 --true--> cond2 --false--> other
                        cond2 --true--> target

    Result:
        BlockCondition(cond1, cond2, is_or=True/False)

    Ghidra preconditions from ruleBlockOr():
    - bl->sizeOut() == 2 (binary condition)
    - One branch leads to another condition block
    - Both conditions share a common target (short-circuit)
    """

    def __init__(self):
        super().__init__("BlockOr")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # Block must have exactly two outgoing edges (binary condition)
        if len(block.out_edges) != 2:
            return False

        # Neither branch can be a goto
        if block.is_goto_out(0) or block.is_goto_out(1):
            return False

        # Check each branch for nested condition pattern
        for i in range(2):
            inner_block = block.out_edges[i].target

            if inner_block == block or inner_block.is_collapsed:
                continue

            # Inner block must have single predecessor (this block)
            if not inner_block.has_single_predecessor():
                continue

            # Inner block must also be a binary condition
            if len(inner_block.out_edges) != 2:
                continue

            # Don't match if inner_block has unstructured gotos coming into it
            if inner_block.is_interior_goto_target():
                continue

            # Don't use loop back edge to get to inner_block
            if block.is_back_edge_out(i):
                continue

            # Check if one of inner_block's targets == other branch of block
            other_branch = block.out_edges[1-i].target

            # Skip if other_branch is same as block (no looping)
            if other_branch == block:
                continue

            for j in range(2):
                if inner_block.out_edges[j].target == other_branch:
                    # Found short-circuit pattern!
                    # Also check that the loop-back doesn't go to block
                    if inner_block.out_edges[1-j].target == block:
                        continue
                    return True

        return False

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        # Find the nested condition pattern
        inner_block = None
        inner_idx = -1
        outer_target = None
        is_or = False

        for i in range(2):
            candidate = block.out_edges[i].target

            if candidate == block or candidate.is_collapsed:
                continue

            if not candidate.has_single_predecessor():
                continue

            if len(candidate.out_edges) != 2:
                continue

            other_branch = block.out_edges[1-i].target

            for j in range(2):
                if candidate.out_edges[j].target == other_branch:
                    inner_block = candidate
                    inner_idx = i
                    outer_target = other_branch

                    # Determine if OR or AND:
                    # Edge convention: index 0 = jump target (FALSE for JZ),
                    #                  index 1 = fallthrough (TRUE for JZ)
                    # OR: cond1 --true--> target, cond1 --false--> cond2
                    #     inner_block on FALSE branch (i==0), target on TRUE branch
                    # AND: cond1 --false--> target, cond1 --true--> cond2
                    #     inner_block on TRUE branch (i==1), target on FALSE branch
                    is_or = (i == 0)  # inner_block on FALSE branch means OR
                    break

            if inner_block is not None:
                break

        if inner_block is None:
            return None

        # Create combined condition block
        cond_block = BlockCondition(
            block_type=BlockType.CONDITION,
            block_id=graph._allocate_block_id(),
            first_condition=block,
            second_condition=inner_block,
            is_or=is_or,
        )

        # Update covered blocks
        cond_block.covered_blocks = block.covered_blocks | inner_block.covered_blocks

        # Set parent references
        block.parent = cond_block
        inner_block.parent = cond_block

        # Redirect incoming edges to cond_block
        for edge in block.in_edges:
            if not edge.source.is_collapsed:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=cond_block,
                    edge_type=edge.edge_type
                )
                cond_block.in_edges.append(new_edge)
                for k, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[k] = new_edge

        # Set outgoing edges - cond_block inherits inner_block's exits
        # (except the one going to outer_target which is now part of the condition)
        for edge in inner_block.out_edges:
            if edge.target != outer_target:
                new_edge = BlockEdge(
                    source=cond_block,
                    target=edge.target,
                    edge_type=edge.edge_type
                )
                cond_block.out_edges.append(new_edge)
                # Update target's in_edges
                for k, in_edge in enumerate(edge.target.in_edges):
                    if in_edge.source == inner_block:
                        edge.target.in_edges[k] = new_edge

        # Also add edge to outer_target (the shared target)
        outer_edge = BlockEdge(source=cond_block, target=outer_target, edge_type=EdgeType.NORMAL)
        cond_block.out_edges.append(outer_edge)

        # Update outer_target's in_edges
        outer_target.in_edges = [e for e in outer_target.in_edges if e.source not in (block, inner_block)]
        outer_target.in_edges.append(outer_edge)

        # Add to graph
        graph.blocks[cond_block.block_id] = cond_block
        if graph.entry_block == block:
            graph.entry_block = cond_block

        # Remove old blocks
        graph.remove_block(block)
        graph.remove_block(inner_block)

        return cond_block
