"""
Conditional statement collapse rules.

This module contains rules for collapsing if-then and if-then-else patterns,
including special cases like non-exiting bodies.
"""

from __future__ import annotations

from typing import Optional

from .base import CollapseRule
from ...blocks.hierarchy import (
    BlockType,
    EdgeType,
    BlockGraph,
    StructuredBlock,
    BlockIf,
    BlockEdge,
)
from ....expr import ExpressionFormatter, format_block_expressions

_SIDE_EFFECT_MNEMONICS = {"CALL", "XCALL", "STORE", "DCP", "ASGN"}


def _get_expression_formatter(graph: BlockGraph) -> Optional[ExpressionFormatter]:
    if graph.ssa_func is None:
        return None
    formatter = getattr(graph, "_expr_formatter", None)
    if formatter is None:
        formatter = ExpressionFormatter(graph.ssa_func)
        setattr(graph, "_expr_formatter", formatter)
    return formatter


def _block_has_side_effect_expressions(graph: BlockGraph, block: Optional[StructuredBlock]) -> bool:
    if graph.ssa_func is None or block is None:
        return False
    formatter = _get_expression_formatter(graph)
    if formatter is None:
        return False
    for block_id in block.covered_blocks:
        expressions = format_block_expressions(graph.ssa_func, block_id, formatter=formatter)
        for expr in expressions:
            if expr.mnemonic in _SIDE_EFFECT_MNEMONICS:
                return True
    return False


def _if_has_side_effect_expressions(graph: BlockGraph, *blocks: Optional[StructuredBlock]) -> bool:
    return any(_block_has_side_effect_expressions(graph, block) for block in blocks)


class RuleBlockProperIf(CollapseRule):
    """
    Collapse if-then pattern (no else branch).

    Pattern:
        cond --true--> body --> merge
        cond --false----------> merge

    Result:
        BlockIf(cond, body, None)  # No else

    The false branch goes directly to merge (skip body).
    """

    def __init__(self):
        super().__init__("BlockProperIf")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # Block must have exactly two successors (binary condition)
        if len(block.out_edges) != 2:
            return False

        # No loops back to self
        if block.out_edges[0].target == block or block.out_edges[1].target == block:
            return False

        # Neither branch can be unstructured
        if block.is_goto_out(0) or block.is_goto_out(1):
            return False

        succ1 = block.out_edges[0].target
        succ2 = block.out_edges[1].target

        if succ1.is_collapsed or succ2.is_collapsed:
            return False

        # Check if succ1 is body and succ2 is merge
        # Body (clause) must have: single predecessor, single successor, be a decision edge
        if (succ1.has_single_predecessor() and
            succ1.has_single_successor() and
            block.is_decision_out(0)):
            if succ1.get_single_successor() == succ2:
                # Clause must not have unstructured gotos out
                if not succ1.is_goto_out(0):
                    if _if_has_side_effect_expressions(graph, block, succ1):
                        return False
                    return True

        # Check if succ2 is body and succ1 is merge
        if (succ2.has_single_predecessor() and
            succ2.has_single_successor() and
            block.is_decision_out(1)):
            if succ2.get_single_successor() == succ1:
                # Clause must not have unstructured gotos out
                if not succ2.is_goto_out(0):
                    if _if_has_side_effect_expressions(graph, block, succ2):
                        return False
                    return True

        return False

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        succ1 = block.out_edges[0].target  # Jump target (FALSE path for JZ)
        succ2 = block.out_edges[1].target  # Fallthrough (TRUE path for JZ)

        # Determine which is body and which is merge
        # Edge ordering: index 0 = jump target (FALSE for JZ), index 1 = fallthrough (TRUE for JZ)
        if (succ1.has_single_successor() and
            succ1.get_single_successor() == succ2 and
            succ1.has_single_predecessor()):
            # succ1 (jump target / FALSE path) is the body
            body = succ1
            merge = succ2
            # Body is on FALSE branch (jump target), need to negate condition
            # so that "if (!cond)" becomes the semantic equivalent of "if body on false"
            # Actually: JZ already auto-negates, so we need to CANCEL that negation
            # to get "if (cond) { body }" where body executes when original condition is FALSE
            negate_condition = True
        else:
            # succ2 (fallthrough / TRUE path) is the body
            body = succ2
            merge = succ1
            # Body is on TRUE branch (fallthrough), no additional negation needed
            # JZ auto-negates, which would give "if (!cond) { body }"
            # But we want "if (cond) { body }" - so we need to cancel JZ's auto-negation
            # Wait - if body is on TRUE path and JZ auto-negates...
            # Actually: when body is on fallthrough (TRUE path), we want "if (cond)"
            # JZ renders as "if (!cond)" by default, so we need to cancel that
            # But that seems wrong for this case...
            #
            # Let me reconsider:
            # - JZ jumps when cond == 0 (false), continues when cond != 0 (true)
            # - Fallthrough (succ2) executes when cond is TRUE
            # - Jump target (succ1) executes when cond is FALSE
            #
            # render_condition with JZ auto-adds "!" because JZ semantics are inverted
            # So render_condition gives "!cond" when cond was the value being tested
            #
            # If body is on fallthrough (TRUE path):
            # - We want: if (cond) { body }
            # - render_condition gives: !cond
            # - We need to negate that: !!cond = cond
            # - So negate_condition = True? No wait, that's confusing.
            #
            # Let me think differently:
            # - render_condition with negate=None (auto) and JZ gives "!cond"
            # - render_condition with negate=False gives "cond"
            # - render_condition with negate=True gives "!cond"
            #
            # If body is on fallthrough (TRUE), we want "if (cond) { body }"
            # - condition_negated=True means pass negate=False, giving "cond" ✓
            #
            # If body is on jump target (FALSE), we want "if (!cond) { body }"
            # - Actually no, we want the condition to evaluate to TRUE when body runs
            # - If body runs when original cond is FALSE, we want "if (!cond) { body }"
            # - condition_negated=True means pass negate=False, giving "cond"
            # - But we want "!cond"! So condition_negated should be False here.
            #
            # OK new logic:
            # - If body is on TRUE path (fallthrough/succ2): want "if (cond)", negate_condition=True (cancels JZ's !)
            # - If body is on FALSE path (jump target/succ1): want "if (!cond)", negate_condition=False (keeps JZ's !)
            negate_condition = True  # Cancel JZ's auto-negation to get "if (cond)"

        # Create if block
        if_block = BlockIf(
            block_type=BlockType.IF,
            block_id=graph._allocate_block_id(),
            condition_block=block,
            true_block=body,
            false_block=None,  # No else
        )

        # Apply condition negation if needed
        # condition_negated flag tells emitter to pass negate=False to render_condition,
        # which cancels JZ's auto-negation
        if negate_condition:
            if_block.negate_condition()

        # Update covered blocks
        if_block.covered_blocks = block.covered_blocks | body.covered_blocks

        # Set parent references
        block.parent = if_block
        body.parent = if_block

        # Redirect incoming edges to if_block
        for edge in block.in_edges:
            if not edge.source.is_collapsed:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=if_block,
                    edge_type=edge.edge_type
                )
                if_block.in_edges.append(new_edge)
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[i] = new_edge

        # Create edge from if_block to merge
        merge_edge = BlockEdge(source=if_block, target=merge, edge_type=EdgeType.NORMAL)
        if_block.out_edges.append(merge_edge)

        # Update merge's in_edges
        merge.in_edges = [e for e in merge.in_edges if e.source not in (block, body)]
        merge.in_edges.append(merge_edge)

        # Add if_block, remove old blocks
        graph.blocks[if_block.block_id] = if_block
        if graph.entry_block == block:
            graph.entry_block = if_block

        graph.remove_block(block)
        graph.remove_block(body)

        return if_block


class RuleBlockIfElse(CollapseRule):
    """
    Collapse if-then-else pattern.

    Pattern:
        cond --true--> true_body --> merge
        cond --false-> false_body --> merge

    Result:
        BlockIf(cond, true_body, false_body)
    """

    def __init__(self):
        super().__init__("BlockIfElse")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # Block must have exactly two successors
        if len(block.out_edges) != 2:
            return False

        # No loops back to self
        if block.out_edges[0].target == block or block.out_edges[1].target == block:
            return False

        # Neither branch can be unstructured
        if block.is_goto_out(0) or block.is_goto_out(1):
            return False

        true_branch = block.out_edges[0].target
        false_branch = block.out_edges[1].target

        if true_branch.is_collapsed or false_branch.is_collapsed:
            return False

        # Don't match if branches are same block (would be proper if)
        if true_branch == false_branch:
            return False

        # Both must have single successor and single predecessor
        if not true_branch.has_single_successor() or not true_branch.has_single_predecessor():
            return False
        if not false_branch.has_single_successor() or not false_branch.has_single_predecessor():
            return False

        # Neither branch should have unstructured gotos out
        if true_branch.is_goto_out(0) or false_branch.is_goto_out(0):
            return False

        # Both must go to the same merge point
        true_merge = true_branch.get_single_successor()
        false_merge = false_branch.get_single_successor()

        if true_merge != false_merge:
            return False

        if _if_has_side_effect_expressions(graph, block, true_branch, false_branch):
            return False

        return True

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        true_body = block.out_edges[0].target
        false_body = block.out_edges[1].target
        merge = true_body.get_single_successor()

        # Create if block
        if_block = BlockIf(
            block_type=BlockType.IF,
            block_id=graph._allocate_block_id(),
            condition_block=block,
            true_block=true_body,
            false_block=false_body,
        )

        # Update covered blocks
        if_block.covered_blocks = (
            block.covered_blocks |
            true_body.covered_blocks |
            false_body.covered_blocks
        )

        # Set parent references
        block.parent = if_block
        true_body.parent = if_block
        false_body.parent = if_block

        # Redirect incoming edges to if_block
        for edge in block.in_edges:
            if not edge.source.is_collapsed:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=if_block,
                    edge_type=edge.edge_type
                )
                if_block.in_edges.append(new_edge)
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[i] = new_edge

        # Create edge from if_block to merge
        merge_edge = BlockEdge(source=if_block, target=merge, edge_type=EdgeType.NORMAL)
        if_block.out_edges.append(merge_edge)

        # Update merge's in_edges
        merge.in_edges = [e for e in merge.in_edges if e.source not in (block, true_body, false_body)]
        merge.in_edges.append(merge_edge)

        # Add if_block, remove old blocks
        graph.blocks[if_block.block_id] = if_block
        if graph.entry_block == block:
            graph.entry_block = if_block

        graph.remove_block(block)
        graph.remove_block(true_body)
        graph.remove_block(false_body)

        return if_block


class RuleBlockIfNoExit(CollapseRule):
    """
    Collapse if-then where body has no exit (dead end/non-returning).

    Pattern:
        cond --true--> body (no exit / sizeOut == 0)
        cond --false--> continue

    Result:
        BlockIf(cond, body, None)  # Body has no exit

    Ghidra preconditions from ruleBlockIfNoExit():
    - bl->sizeOut() == 2 (binary condition)
    - One branch has sizeOut == 0 (no exit - dead end)
    - Branch has single predecessor (condition block)
    - Edge is not marked as goto

    This is a SECONDARY rule - only tried when primary rules are stuck.
    """

    def __init__(self):
        super().__init__("BlockIfNoExit")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # Block must have exactly two successors (binary condition)
        if len(block.out_edges) != 2:
            return False

        # Check each branch for dead-end pattern
        for i in range(2):
            clause = block.out_edges[i].target

            if clause == block or clause.is_collapsed:
                continue

            # Clause has single predecessor (this block)
            if not clause.has_single_predecessor():
                continue

            # Clause has NO exits (dead end - no return)
            if len(clause.out_edges) != 0:
                continue

            # Edge to clause must not be unstructured
            if block.is_goto_out(i):
                continue

            return True

        return False

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        # Find the dead-end clause
        dead_clause = None
        dead_clause_idx = -1
        continue_block = None

        for i in range(2):
            clause = block.out_edges[i].target

            if clause == block or clause.is_collapsed:
                continue

            if clause.has_single_predecessor() and len(clause.out_edges) == 0:
                dead_clause = clause
                dead_clause_idx = i
            else:
                continue_block = clause

        if dead_clause is None:
            return None

        # Determine if we need to negate condition
        # If dead clause is on index 1 (false branch), we need to negate
        # to make it the true branch for proper if-then syntax
        negate_condition = (dead_clause_idx == 1)

        # Create if block
        if_block = BlockIf(
            block_type=BlockType.IF,
            block_id=graph._allocate_block_id(),
            condition_block=block,
            true_block=dead_clause,
            false_block=None,  # No else
        )

        # Apply condition negation if needed (Ghidra-style)
        if negate_condition:
            if_block.negate_condition()

        # Update covered blocks
        if_block.covered_blocks = block.covered_blocks | dead_clause.covered_blocks

        # Set parent references
        block.parent = if_block
        dead_clause.parent = if_block

        # Redirect incoming edges to if_block
        for edge in block.in_edges:
            if not edge.source.is_collapsed:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=if_block,
                    edge_type=edge.edge_type
                )
                if_block.in_edges.append(new_edge)
                for j, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[j] = new_edge

        # If there's a continue block, create edge to it
        if continue_block is not None:
            merge_edge = BlockEdge(source=if_block, target=continue_block, edge_type=EdgeType.NORMAL)
            if_block.out_edges.append(merge_edge)

            # Update continue_block's in_edges
            continue_block.in_edges = [e for e in continue_block.in_edges if e.source != block]
            continue_block.in_edges.append(merge_edge)

        # Add if_block, remove old blocks
        graph.blocks[if_block.block_id] = if_block
        if graph.entry_block == block:
            graph.entry_block = if_block

        graph.remove_block(block)
        graph.remove_block(dead_clause)

        return if_block
