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
        # Block must have exactly two successors
        if len(block.out_edges) != 2:
            return False

        succ1 = block.out_edges[0].target
        succ2 = block.out_edges[1].target

        if succ1.is_collapsed or succ2.is_collapsed:
            return False

        # One branch should be the body, other should be merge point
        # Body has single successor which is the merge point
        # Check if succ1 is body and succ2 is merge
        if (succ1.has_single_successor() and
            succ1.get_single_successor() == succ2 and
            succ1.has_single_predecessor()):
            return True

        # Check if succ2 is body and succ1 is merge
        if (succ2.has_single_successor() and
            succ2.get_single_successor() == succ1 and
            succ2.has_single_predecessor()):
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
            # True branch is body (index 0)
            negate_condition = False
        else:
            body = succ2
            merge = succ1
            # True branch is merge, so we need to negate condition
            negate_condition = True

        # Create if block
        if_block = BlockIf(
            block_type=BlockType.IF,
            block_id=graph._allocate_block_id(),
            condition_block=block,
            true_block=body,
            false_block=None,  # No else
        )

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

        true_branch = block.out_edges[0].target
        false_branch = block.out_edges[1].target

        if true_branch.is_collapsed or false_branch.is_collapsed:
            return False

        # Both must have single successor and single predecessor
        if not true_branch.has_single_successor() or not true_branch.has_single_predecessor():
            return False
        if not false_branch.has_single_successor() or not false_branch.has_single_predecessor():
            return False

        # Both must go to the same merge point
        true_merge = true_branch.get_single_successor()
        false_merge = false_branch.get_single_successor()

        if true_merge != false_merge:
            return False

        # Don't match if branches are same block (would be proper if)
        if true_branch == false_branch:
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
        # Header must have exactly two successors
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

        # Find the exit block (successor that's not body or self)
        for edge in block.out_edges:
            if edge.target != body_block and edge.target != block:
                exit_block = edge.target
                break

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

        for edge in block.in_edges:
            if edge.edge_type == EdgeType.BACK_EDGE:
                body_block = edge.source
                break

        for edge in block.out_edges:
            if edge.target != body_block and edge.target != block:
                exit_block = edge.target
                break

        if body_block is None or exit_block is None:
            return None

        # Create while block
        while_block = BlockWhileDo(
            block_type=BlockType.WHILE_DO,
            block_id=graph._allocate_block_id(),
            condition_block=block,
            body_block=body_block,
        )

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

        # Find exit block
        exit_block = None
        for edge in cond.out_edges:
            if edge.target != block:
                exit_block = edge.target
                break

        if exit_block is None:
            return None

        # Create do-while block
        dowhile_block = BlockDoWhile(
            block_type=BlockType.DO_WHILE,
            block_id=graph._allocate_block_id(),
            body_block=block,
            condition_block=cond,
        )

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


class RuleBlockSwitch(CollapseRule):
    """
    Collapse switch/case pattern.

    This rule uses pre-detected switch patterns from the pattern analysis.
    It creates a BlockSwitch from the detected pattern.
    """

    def __init__(self):
        super().__init__("BlockSwitch")
        self.switch_patterns = []  # Set externally

    def set_patterns(self, patterns):
        """Set the detected switch patterns."""
        self.switch_patterns = patterns

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # Check if this block is a switch header
        if not isinstance(block, BlockBasic):
            return False

        for pattern in self.switch_patterns:
            if pattern.header_block == block.original_block_id:
                return True

        return False

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        # Find the matching pattern
        pattern = None
        for p in self.switch_patterns:
            if p.header_block == block.original_block_id:
                pattern = p
                break

        if pattern is None:
            return None

        # Create cases
        cases = []
        for case_info in pattern.cases:
            case_block = None
            # CaseInfo has block_id (entry point) and body_blocks (all blocks in case)
            if case_info.block_id in graph.cfg_to_struct:
                case_block = graph.cfg_to_struct[case_info.block_id]

            cases.append(SwitchCase(
                value=case_info.value,
                body_block=case_block,
                is_default=False,
                has_break=case_info.has_break,
            ))

        # Create default case
        default_case = None
        if pattern.default_body_blocks:
            default_block_id = min(pattern.default_body_blocks)
            if default_block_id in graph.cfg_to_struct:
                default_case = SwitchCase(
                    value=-1,
                    body_block=graph.cfg_to_struct[default_block_id],
                    is_default=True,
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

        # Add switch_block
        graph.blocks[switch_block.block_id] = switch_block
        if graph.entry_block == block:
            graph.entry_block = switch_block

        # Mark all switch blocks as collapsed
        for cfg_block_id in pattern.all_blocks:
            if cfg_block_id in graph.cfg_to_struct:
                struct_block = graph.cfg_to_struct[cfg_block_id]
                if struct_block != block:  # Don't remove header twice
                    graph.remove_block(struct_block)

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


# Default rule ordering (most specific to least specific)
DEFAULT_RULES: List[CollapseRule] = [
    RuleBlockSwitch(),   # Switch/case (uses pre-detected patterns)
    RuleBlockWhileDo(),  # While loops
    RuleBlockDoWhile(),  # Do-while loops
    RuleBlockIfElse(),   # Full if-else
    RuleBlockProperIf(), # If without else
    RuleBlockCat(),      # Sequential blocks (most common, run last)
    RuleBlockGoto(),     # Fallback for unstructured
]
