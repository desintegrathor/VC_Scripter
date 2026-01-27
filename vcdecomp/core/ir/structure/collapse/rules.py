"""
Collapse rules for control flow structuring.

This module provides pattern-matching rules that detect and collapse
control flow patterns into hierarchical block structures.

Modeled after Ghidra's blockaction.hh rules:
- RuleBlockCat: Collapse sequential blocks
- RuleBlockProperIf: Collapse if-then (no else)
- RuleBlockIfElse: Collapse if-then-else
- RuleBlockWhileDo: Collapse while loops
- RuleBlockDoWhile: Collapse do-while loops
- RuleBlockSwitch: Collapse switch/case
- RuleBlockGoto: Mark unstructured edges as goto
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING

from ..blocks.hierarchy import (
    BlockType,
    EdgeType,
    StructuredBlock,
    BlockBasic,
    BlockList,
    BlockIf,
    BlockWhileDo,
    BlockDoWhile,
    BlockInfLoop,
    BlockCondition,
    BlockSwitch,
    BlockGoto,
    BlockGraph,
    BlockEdge,
    SwitchCase,
)

if TYPE_CHECKING:
    pass


class CollapseRule(ABC):
    """
    Abstract base class for collapse rules.

    Each rule detects a specific control flow pattern and collapses
    it into a higher-level structured block.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        """
        Check if this rule matches at the given block.

        Args:
            graph: The block graph
            block: Block to check for pattern match

        Returns:
            True if the pattern matches
        """
        pass

    @abstractmethod
    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        """
        Apply the rule, collapsing the pattern into a new block.

        Args:
            graph: The block graph
            block: Block where pattern was matched

        Returns:
            The new collapsed block, or None if collapse failed
        """
        pass


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
                    # OR: cond1 --true--> target, cond1 --false--> cond2
                    #     So if outer_target is reached on true branch of block, it's OR
                    # AND: cond1 --false--> other, cond1 --true--> cond2
                    #     So if outer_target is reached on false branch of block, it's AND
                    is_or = (i == 1)  # inner_block on false branch means OR pattern
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
                    return True

        # Check if succ2 is body and succ1 is merge
        if (succ2.has_single_predecessor() and
            succ2.has_single_successor() and
            block.is_decision_out(1)):
            if succ2.get_single_successor() == succ1:
                # Clause must not have unstructured gotos out
                if not succ2.is_goto_out(0):
                    return True

        return False

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        succ1 = block.out_edges[0].target
        succ2 = block.out_edges[1].target

        # Determine which is body and which is merge
        if (succ1.has_single_successor() and
            succ1.get_single_successor() == succ2 and
            succ1.has_single_predecessor()):
            body = succ1
            merge = succ2
            # True branch is body (index 0) - no negation needed
            negate_condition = False
        else:
            body = succ2
            merge = succ1
            # True branch is merge, so we need to negate condition
            # In Ghidra terms: the "false" branch (index 1) goes to body
            negate_condition = True

        # Create if block
        if_block = BlockIf(
            block_type=BlockType.IF,
            block_id=graph._allocate_block_id(),
            condition_block=block,
            true_block=body,
            false_block=None,  # No else
        )

        # Apply condition negation if needed (Ghidra-style)
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


class RuleBlockWhileDo(CollapseRule):
    """
    Collapse while loop pattern.

    Pattern:
        header <--back-- body
        header --exit--> after

    Where header is loop condition and body loops back.

    Result:
        BlockWhileDo(header, body)
    """

    def __init__(self):
        super().__init__("BlockWhileDo")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # Header must have exactly two successors (condition + exit)
        if len(block.out_edges) != 2:
            return False

        # One edge should be a back edge coming back to this block
        has_back_edge_in = False
        body_block = None
        exit_block = None

        for edge in block.in_edges:
            if edge.edge_type == EdgeType.BACK_EDGE:
                has_back_edge_in = True
                body_block = edge.source
                break

        if not has_back_edge_in or body_block is None:
            return False

        # Identify body vs exit in outgoing edges
        for i, edge in enumerate(block.out_edges):
            if edge.target == body_block:
                # This is the loop edge back to body
                # Check that it's not marked as unstructured
                if block.is_goto_out(i):
                    return False
            elif edge.target != block:
                exit_block = edge.target

        if exit_block is None:
            return False

        # Body should have single successor back to header
        if not body_block.has_single_successor():
            return False

        if body_block.get_single_successor() != block:
            return False

        # Body should have single predecessor (the header)
        if not body_block.has_single_predecessor():
            return False

        return True

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        # Find body and exit
        body_block = None
        exit_block = None
        body_edge_index = -1

        for edge in block.in_edges:
            if edge.edge_type == EdgeType.BACK_EDGE:
                body_block = edge.source
                break

        # Find which outgoing edge goes to body
        for i, edge in enumerate(block.out_edges):
            if edge.target == body_block:
                body_edge_index = i
            elif edge.target != block:
                exit_block = edge.target

        if body_block is None or exit_block is None:
            return None

        # Create while block
        while_block = BlockWhileDo(
            block_type=BlockType.WHILE_DO,
            block_id=graph._allocate_block_id(),
            condition_block=block,
            body_block=body_block,
        )

        # Ghidra: negate condition if body is on false branch (index 1)
        # while (cond) { body } means cond should be true to enter body
        # If bytecode has false branch going to body, we need to negate
        if body_edge_index == 1:
            while_block.negate_condition()

        # Update covered blocks
        while_block.covered_blocks = block.covered_blocks | body_block.covered_blocks

        # Set parent references
        block.parent = while_block
        body_block.parent = while_block

        # Redirect incoming edges (excluding back edge from body)
        for edge in block.in_edges:
            if edge.source != body_block and not edge.source.is_collapsed:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=while_block,
                    edge_type=edge.edge_type
                )
                while_block.in_edges.append(new_edge)
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[i] = new_edge

        # Create edge to exit
        exit_edge = BlockEdge(source=while_block, target=exit_block, edge_type=EdgeType.NORMAL)
        while_block.out_edges.append(exit_edge)

        # Update exit's in_edges
        exit_block.in_edges = [e for e in exit_block.in_edges if e.source != block]
        exit_block.in_edges.append(exit_edge)

        # Add while_block, remove old blocks
        graph.blocks[while_block.block_id] = while_block
        if graph.entry_block == block:
            graph.entry_block = while_block

        graph.remove_block(block)
        graph.remove_block(body_block)

        return while_block


class RuleBlockDoWhile(CollapseRule):
    """
    Collapse do-while loop pattern.

    Pattern:
        body --> cond --back--> body
        cond --exit--> after

    Where condition is at the bottom.

    Result:
        BlockDoWhile(body, cond)
    """

    def __init__(self):
        super().__init__("BlockDoWhile")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # This block is the body - should have single successor (condition)
        if not block.has_single_successor():
            return False

        cond = block.get_single_successor()
        if cond is None or cond.is_collapsed:
            return False

        # Condition must have two successors
        if len(cond.out_edges) != 2:
            return False

        # One of condition's successors should be back to body (this block)
        has_back_to_body = False
        for edge in cond.out_edges:
            if edge.target == block and edge.edge_type == EdgeType.BACK_EDGE:
                has_back_to_body = True
                break

        if not has_back_to_body:
            return False

        # Condition should have single predecessor (body)
        if not cond.has_single_predecessor():
            return False

        return True

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        cond = block.get_single_successor()
        if cond is None:
            return None

        # Find exit block and back edge index
        exit_block = None
        back_edge_index = -1
        for i, edge in enumerate(cond.out_edges):
            if edge.target == block and edge.edge_type == EdgeType.BACK_EDGE:
                back_edge_index = i
            elif edge.target != block:
                exit_block = edge.target

        if exit_block is None:
            return None

        # Create do-while block
        dowhile_block = BlockDoWhile(
            block_type=BlockType.DO_WHILE,
            block_id=graph._allocate_block_id(),
            body_block=block,
            condition_block=cond,
        )

        # Ghidra: negate condition if back edge is on false branch (index 1)
        # do { body } while (cond) means cond should be true to loop back
        # If bytecode has false branch looping back, we need to negate
        if back_edge_index == 1:
            dowhile_block.negate_condition()

        # Update covered blocks
        dowhile_block.covered_blocks = block.covered_blocks | cond.covered_blocks

        # Set parent references
        block.parent = dowhile_block
        cond.parent = dowhile_block

        # Redirect incoming edges to body (now to dowhile)
        for edge in block.in_edges:
            if edge.source != cond and not edge.source.is_collapsed:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=dowhile_block,
                    edge_type=edge.edge_type
                )
                dowhile_block.in_edges.append(new_edge)
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[i] = new_edge

        # Create edge to exit
        exit_edge = BlockEdge(source=dowhile_block, target=exit_block, edge_type=EdgeType.NORMAL)
        dowhile_block.out_edges.append(exit_edge)

        # Update exit's in_edges
        exit_block.in_edges = [e for e in exit_block.in_edges if e.source != cond]
        exit_block.in_edges.append(exit_edge)

        # Add dowhile_block, remove old blocks
        graph.blocks[dowhile_block.block_id] = dowhile_block
        if graph.entry_block == block:
            graph.entry_block = dowhile_block

        graph.remove_block(block)
        graph.remove_block(cond)

        return dowhile_block


class RuleBlockInfLoop(CollapseRule):
    """
    Collapse infinite loop (while(1) or for(;;)).

    Pattern:
        bl --> bl  (single exit loops back to itself)

    Result:
        BlockInfLoop(bl)

    Ghidra preconditions from ruleBlockInfLoop():
    - bl->sizeOut() == 1 (single exit)
    - !bl->isGotoOut(0) (exit is not unstructured)
    - bl->getOut(0) == bl (block loops to itself)
    """

    def __init__(self):
        super().__init__("BlockInfLoop")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # Block must have exactly one successor
        if not block.has_single_successor():
            return False

        successor = block.get_single_successor()

        # Must loop back to itself
        if successor != block:
            return False

        # Edge must not be marked as goto/irreducible
        for edge in block.out_edges:
            if edge.target == block:
                if edge.edge_type in (EdgeType.GOTO_EDGE, EdgeType.IRREDUCIBLE):
                    return False

        return True

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        # Create infinite loop wrapping this block
        inf_loop = BlockInfLoop(
            block_type=BlockType.INF_LOOP,
            block_id=graph._allocate_block_id(),
            body_block=block,
        )

        # Update covered blocks
        inf_loop.covered_blocks = set(block.covered_blocks)

        # Set parent
        block.parent = inf_loop

        # Redirect incoming edges to inf_loop (skip self-loop)
        for edge in block.in_edges:
            if edge.source != block:  # Skip self-loop
                new_edge = BlockEdge(
                    source=edge.source,
                    target=inf_loop,
                    edge_type=edge.edge_type
                )
                inf_loop.in_edges.append(new_edge)
                # Update source's out_edges
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[i] = new_edge

        # InfLoop has no outgoing edges (it's infinite)
        # Break statements would need separate handling

        # Add to graph, remove old block
        graph.blocks[inf_loop.block_id] = inf_loop
        if graph.entry_block == block:
            graph.entry_block = inf_loop

        graph.remove_block(block)

        return inf_loop


class RuleBlockSwitch(CollapseRule):
    """
    Collapse switch/case pattern.

    This rule uses pre-detected switch patterns from the pattern analysis.
    It creates a BlockSwitch from the detected pattern.

    Ghidra approach: By the time this rule runs (LAST in rule order), case
    bodies are already collapsed into BlockIf, BlockList, etc. So we just
    collect the already-structured blocks from the graph - no recursive
    collapse needed.

    Preconditions (from Ghidra's ruleBlockSwitch):
    - Each case block has sizeIn == 1 (only switch goes to it)
    - Each case block has sizeOut <= 1 (at most one exit)
    - If sizeOut == 1, exit must be the switch's exit block
    """

    def __init__(self):
        super().__init__("BlockSwitch")
        self.switch_patterns = []  # Set externally

    def set_patterns(self, patterns):
        """Set the detected switch patterns."""
        self.switch_patterns = patterns

    def _get_pattern(self, cfg_block_id: int):
        """Get switch pattern for a CFG block ID."""
        for pattern in self.switch_patterns:
            if pattern.header_block == cfg_block_id:
                return pattern
        return None

    def _find_case_entry_block(self, graph: BlockGraph, case_info) -> Optional[StructuredBlock]:
        """
        Find the entry block for a case in the current graph state.

        Since blocks may have been collapsed, we look for the block that
        covers the case's entry CFG block ID.
        """
        entry_cfg_id = case_info.block_id

        # First try direct lookup
        if entry_cfg_id in graph.cfg_to_struct:
            block = graph.cfg_to_struct[entry_cfg_id]
            if not block.is_collapsed:
                return block

        # Search through uncollapsed blocks for one that covers this CFG block
        for struct_block in graph.get_uncollapsed_blocks():
            if entry_cfg_id in struct_block.covered_blocks:
                return struct_block

        return None

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        """
        Check if switch pattern matches.

        Simplified approach: Just check that this is a detected switch header.
        The switch rule runs LAST in the order, so other patterns have already
        had a chance to collapse. We accept the switch as-is.
        """
        # Don't match if this is already a BlockSwitch
        if isinstance(block, BlockSwitch):
            return False

        # Must be a switch header - only match on BlockBasic with the exact header block ID
        if not isinstance(block, BlockBasic):
            return False

        cfg_block_id = block.original_block_id
        pattern = self._get_pattern(cfg_block_id)
        if pattern is None:
            return False

        return True

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        """
        Apply switch collapse using already-structured case bodies from graph.
        """
        # Get the CFG block ID
        cfg_block_id = None
        if isinstance(block, BlockBasic):
            cfg_block_id = block.original_block_id
        elif hasattr(block, 'covered_blocks') and block.covered_blocks:
            for covered_id in block.covered_blocks:
                if self._get_pattern(covered_id):
                    cfg_block_id = covered_id
                    break

        pattern = self._get_pattern(cfg_block_id)
        if pattern is None:
            return None

        # Build cases using already-collapsed bodies from graph
        cases = []
        block_ids_to_remove = set()  # Use block_id for hashability

        for case_info in pattern.cases:
            # Find the (already collapsed) case body in the graph
            case_body = self._find_case_entry_block(graph, case_info)

            if case_body is not None and not case_body.is_collapsed and case_body != block:
                block_ids_to_remove.add(case_body.block_id)

                # Determine if case has break (exits to switch exit)
                has_break = len(case_body.out_edges) > 0

            else:
                case_body = None
                has_break = case_info.has_break

            cases.append(SwitchCase(
                value=case_info.value,
                body_block=case_body,  # Already structured (BlockIf, BlockList, etc.)
                is_default=False,
                has_break=has_break,
            ))

        # Build default case
        default_case = None
        if pattern.default_body_blocks:
            # Find default entry block
            default_entry = min(pattern.default_body_blocks)
            default_body = None

            # Look for the block covering default entry
            if default_entry in graph.cfg_to_struct:
                default_body = graph.cfg_to_struct[default_entry]
                if default_body.is_collapsed:
                    default_body = None
                elif default_body != block:
                    block_ids_to_remove.add(default_body.block_id)
            else:
                # Search through uncollapsed blocks
                for struct_block in graph.get_uncollapsed_blocks():
                    if default_entry in struct_block.covered_blocks:
                        default_body = struct_block
                        if struct_block != block:
                            block_ids_to_remove.add(struct_block.block_id)
                        break

            default_case = SwitchCase(
                value=-1,
                body_block=default_body,
                is_default=True,
                has_break=True,
            )

        # Create switch block
        switch_block = BlockSwitch(
            block_type=BlockType.SWITCH,
            block_id=graph._allocate_block_id(),
            header_block=block,
            test_var=pattern.test_var,
            cases=cases,
            default_case=default_case,
        )

        # Collect all covered blocks
        switch_block.covered_blocks = set(pattern.all_blocks)

        # Set parent for header
        block.parent = switch_block

        # Redirect incoming edges to switch_block
        for edge in block.in_edges:
            if not edge.source.is_collapsed:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=switch_block,
                    edge_type=edge.edge_type
                )
                switch_block.in_edges.append(new_edge)
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[i] = new_edge

        # Find exit block (block after switch)
        if pattern.exit_block is not None and pattern.exit_block in graph.cfg_to_struct:
            exit_block = graph.cfg_to_struct[pattern.exit_block]
            if not exit_block.is_collapsed:
                exit_edge = BlockEdge(
                    source=switch_block,
                    target=exit_block,
                    edge_type=EdgeType.NORMAL
                )
                switch_block.out_edges.append(exit_edge)

                # Update exit block's in_edges
                exit_block.in_edges = [
                    e for e in exit_block.in_edges
                    if e.source.is_collapsed or e.source == switch_block
                ]
                exit_block.in_edges.append(exit_edge)

        # Add switch_block to graph
        graph.blocks[switch_block.block_id] = switch_block
        if graph.entry_block == block:
            graph.entry_block = switch_block

        # Remove case body blocks from graph (they're now inside switch)
        for block_id in block_ids_to_remove:
            if block_id in graph.blocks:
                graph.remove_block(graph.blocks[block_id])

        # Remove header block
        graph.remove_block(block)

        return switch_block


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


class RuleCaseFallthru(CollapseRule):
    """
    Handle switch case fall-through patterns.

    Detects when one case falls through to another and marks it.
    This is a SECONDARY rule - only tried when primary rules are stuck.

    Pattern:
        case N: body --> case M: body  (no break, falls through)

    Result:
        Update SwitchCase to mark fall_through_to = M
    """

    def __init__(self):
        super().__init__("CaseFallthru")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # This rule operates on switch blocks, not individual blocks
        # For now, this is a placeholder - full implementation would
        # require tracking which blocks are part of a switch and
        # analyzing their flow relationships
        return False

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        # Placeholder for fall-through handling
        return None


# Primary rules (Ghidra order) - tried repeatedly until no changes
# Following Ghidra's collapseInternal() rule order
PRIMARY_RULES: List[CollapseRule] = [
    RuleBlockGoto(),      # 1. Handle unstructured first
    RuleBlockCat(),       # 2. Sequential merge
    RuleBlockOr(),        # 3. AND/OR conditions
    RuleBlockProperIf(),  # 4. If-then (no else)
    RuleBlockIfElse(),    # 5. If-then-else
    RuleBlockWhileDo(),   # 6. While loops
    RuleBlockDoWhile(),   # 7. Do-while loops
    RuleBlockInfLoop(),   # 8. Infinite loops
    RuleBlockSwitch(),    # 9. Switch/case (LAST)
]

# Secondary rules (lower priority, only when primary rules stuck)
SECONDARY_RULES: List[CollapseRule] = [
    RuleBlockIfNoExit(),  # 10. Non-exiting if bodies
    RuleCaseFallthru(),   # 11. Switch fall-through
]

# Default rule ordering - for backwards compatibility
DEFAULT_RULES: List[CollapseRule] = PRIMARY_RULES.copy()
