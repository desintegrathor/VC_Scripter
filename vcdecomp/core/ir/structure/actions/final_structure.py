"""
Final structure action for block ordering and label finalization.

Implements Ghidra's ActionFinalStructure which performs:
1. Block ordering (topological sort)
2. Printing finalization
3. Scope break insertion
4. Unstructured edge marking
5. Label bump-up fixup

Corresponds to Ghidra's ActionFinalStructure in blockaction.cc:2186.
"""

from __future__ import annotations

import logging
from typing import Set, TYPE_CHECKING

from .base import Action
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
    BlockSwitch,
    BlockGoto,
)

if TYPE_CHECKING:
    from ..blocks.hierarchy import BlockGraph

logger = logging.getLogger(__name__)


class ActionFinalStructure(Action):
    """
    Final structure transformation pass.

    This action performs the final cleanup and organization of the
    structured block tree after all collapse rules have been applied.

    Corresponds to Ghidra's ActionFinalStructure::apply() which calls:
    - graph.orderBlocks() - Order blocks for printing
    - graph.finalizePrinting() - Final formatting setup
    - graph.scopeBreak() - Insert break statements
    - graph.markUnstructured() - Mark goto edges
    - graph.markLabelBumpUp() - Fix label references
    """

    def __init__(self):
        """Initialize the final structure action."""
        super().__init__("ActionFinalStructure")

    def apply(self, graph: 'BlockGraph') -> int:
        """
        Apply final structure transformations.

        Args:
            graph: The block graph to finalize

        Returns:
            Number of changes made
        """
        self.count = 0

        # 1. Order blocks for natural printing order
        self._order_blocks(graph)

        # 2. Finalize printing (recurse into all blocks)
        if graph.root:
            self._finalize_printing(graph.root)

        # 3. Insert scope breaks (break statements in loops/switches)
        if graph.root:
            self._scope_break(graph.root, -1, -1)

        # 4. Mark unstructured edges (gotos)
        if graph.root:
            self._mark_unstructured(graph.root)

        # 5. Fix label references (bump up)
        if graph.root:
            self._mark_label_bump_up(graph.root, False)

        return self.count

    def _order_blocks(self, graph: 'BlockGraph') -> None:
        """
        Order blocks for natural printing.

        Performs a topological sort of blocks to ensure they appear
        in a natural order when printed. This is mostly handled by
        the collapse algorithm, but we can verify and adjust if needed.

        Args:
            graph: The block graph
        """
        # For now, the collapse algorithm produces blocks in the right order
        # Ghidra's orderBlocks() does a more sophisticated topological sort
        # We can implement this later if needed
        pass

    def _finalize_printing(self, block: StructuredBlock) -> None:
        """
        Finalize printing for all blocks (recursive).

        This recurses into all structured blocks to perform any
        final setup needed before code emission.

        Args:
            block: The block to finalize
        """
        # Recurse into children
        if isinstance(block, BlockList):
            for component in block.components:
                self._finalize_printing(component)

        elif isinstance(block, BlockIf):
            if block.true_block:
                self._finalize_printing(block.true_block)
            if block.false_block:
                self._finalize_printing(block.false_block)

        elif isinstance(block, (BlockWhileDo, BlockDoWhile, BlockInfLoop)):
            if block.body_block:
                self._finalize_printing(block.body_block)

        elif isinstance(block, BlockSwitch):
            for case in block.cases:
                if case.body_block:
                    self._finalize_printing(case.body_block)
            if block.default_case and block.default_case.body_block:
                self._finalize_printing(block.default_case.body_block)

        elif isinstance(block, BlockGoto):
            if block.wrapped_block:
                self._finalize_printing(block.wrapped_block)

    def _scope_break(
        self,
        block: StructuredBlock,
        cur_exit: int,
        cur_loop_exit: int
    ) -> None:
        """
        Insert break statements where needed.

        Marks edges that require explicit break statements in switch
        statements or loops. This corresponds to Ghidra's scopeBreak().

        Args:
            block: The block to process
            cur_exit: Current exit block ID (-1 if none)
            cur_loop_exit: Current loop exit block ID (-1 if none)
        """
        # Process based on block type
        if isinstance(block, BlockList):
            # For sequential blocks, propagate the exit context
            for component in block.components:
                self._scope_break(component, cur_exit, cur_loop_exit)

        elif isinstance(block, BlockIf):
            # Process both branches with same exit context
            if block.true_block:
                self._scope_break(block.true_block, cur_exit, cur_loop_exit)
            if block.false_block:
                self._scope_break(block.false_block, cur_exit, cur_loop_exit)

        elif isinstance(block, (BlockWhileDo, BlockDoWhile, BlockInfLoop)):
            # Loops: set their exit as the loop exit
            # Find the exit block (first block after the loop)
            loop_exit = self._find_loop_exit(block)
            if block.body_block:
                self._scope_break(block.body_block, loop_exit, loop_exit)

            # Mark any edges to loop_exit from within the loop as BREAK
            self._mark_break_edges(block, loop_exit)

        elif isinstance(block, BlockSwitch):
            # Switches: mark break edges to exit
            switch_exit = self._find_switch_exit(block)

            for case in block.cases:
                if case.body_block:
                    self._scope_break(case.body_block, switch_exit, cur_loop_exit)

            if block.default_case and block.default_case.body_block:
                self._scope_break(block.default_case.body_block, switch_exit, cur_loop_exit)

            # Mark edges to switch_exit as BREAK
            self._mark_break_edges(block, switch_exit)

    def _find_loop_exit(self, loop_block: StructuredBlock) -> int:
        """
        Find the exit block for a loop.

        Args:
            loop_block: The loop block

        Returns:
            Block ID of the loop exit, or -1 if none
        """
        # Look for outgoing edges from the loop that exit
        for edge in loop_block.out_edges:
            if edge.edge_type not in (EdgeType.BACK_EDGE, EdgeType.LOOP_EDGE):
                return edge.target.block_id

        return -1

    def _find_switch_exit(self, switch_block: BlockSwitch) -> int:
        """
        Find the exit block for a switch.

        Args:
            switch_block: The switch block

        Returns:
            Block ID of the switch exit, or -1 if none
        """
        # Look for outgoing edges from the switch
        for edge in switch_block.out_edges:
            if edge.edge_type == EdgeType.NORMAL:
                return edge.target.block_id

        return -1

    def _mark_break_edges(self, container_block: StructuredBlock, exit_id: int) -> None:
        """
        Mark edges that require break statements.

        Args:
            container_block: The containing block (loop or switch)
            exit_id: The exit block ID
        """
        if exit_id == -1:
            return

        # Recursively find all edges within the container that target the exit
        def mark_recursive(block: StructuredBlock):
            # Check edges from this block
            for edge in block.out_edges:
                if edge.target.block_id == exit_id:
                    if edge.edge_type == EdgeType.NORMAL:
                        edge.edge_type = EdgeType.BREAK_EDGE
                        self.count += 1

            # Recurse into children
            if isinstance(block, BlockList):
                for component in block.components:
                    mark_recursive(component)

            elif isinstance(block, BlockIf):
                if block.true_block:
                    mark_recursive(block.true_block)
                if block.false_block:
                    mark_recursive(block.false_block)

            elif isinstance(block, (BlockWhileDo, BlockDoWhile, BlockInfLoop)):
                # Don't recurse into nested loops (they have their own breaks)
                pass

            elif isinstance(block, BlockSwitch):
                # Don't recurse into nested switches
                pass

        # Start marking from the container's body
        if isinstance(container_block, (BlockWhileDo, BlockDoWhile, BlockInfLoop)):
            if container_block.body_block:
                mark_recursive(container_block.body_block)
        elif isinstance(container_block, BlockSwitch):
            for case in container_block.cases:
                if case.body_block:
                    mark_recursive(case.body_block)
            if container_block.default_case and container_block.default_case.body_block:
                mark_recursive(container_block.default_case.body_block)

    def _mark_unstructured(self, block: StructuredBlock) -> None:
        """
        Mark unstructured edges that require goto statements.

        Recursively processes all blocks and marks edges that cannot
        be represented with structured control flow.

        Args:
            block: The block to process
        """
        # Check if this block has any goto edges that need labels
        for edge in block.out_edges:
            if edge.edge_type == EdgeType.GOTO_EDGE:
                # Ensure target has a label
                if not edge.target.label:
                    edge.target.label = f"label_{edge.target.block_id}"
                    edge.target.needs_label = True
                    self.count += 1

        # Recurse into children
        if isinstance(block, BlockList):
            for component in block.components:
                self._mark_unstructured(component)

        elif isinstance(block, BlockIf):
            if block.true_block:
                self._mark_unstructured(block.true_block)
            if block.false_block:
                self._mark_unstructured(block.false_block)

        elif isinstance(block, (BlockWhileDo, BlockDoWhile, BlockInfLoop)):
            if block.body_block:
                self._mark_unstructured(block.body_block)

        elif isinstance(block, BlockSwitch):
            for case in block.cases:
                if case.body_block:
                    self._mark_unstructured(case.body_block)
            if block.default_case and block.default_case.body_block:
                self._mark_unstructured(block.default_case.body_block)

        elif isinstance(block, BlockGoto):
            # Goto blocks themselves represent unstructured flow
            if block.goto_target and not block.goto_target.label:
                block.goto_target.label = f"label_{block.goto_target.block_id}"
                block.goto_target.needs_label = True
                self.count += 1

    def _mark_label_bump_up(self, block: StructuredBlock, bump: bool) -> None:
        """
        Fix label references by bumping them up.

        This handles cases where a label needs to be moved to a parent
        block. Corresponds to Ghidra's markLabelBumpUp().

        Args:
            block: The block to process
            bump: Whether to bump labels up
        """
        # Mark this block if bump is true
        if bump and block.needs_label:
            block.label_bump_up = True

        # Recurse - only first child gets bump=True
        if isinstance(block, BlockList):
            if block.components:
                self._mark_label_bump_up(block.components[0], bump)
                for component in block.components[1:]:
                    self._mark_label_bump_up(component, False)

        elif isinstance(block, BlockIf):
            # Only bump up on first branch
            if block.true_block:
                self._mark_label_bump_up(block.true_block, bump)
            if block.false_block:
                self._mark_label_bump_up(block.false_block, False)

        elif isinstance(block, (BlockWhileDo, BlockDoWhile, BlockInfLoop)):
            if block.body_block:
                self._mark_label_bump_up(block.body_block, False)

        elif isinstance(block, BlockSwitch):
            # Pass false to all cases
            for case in block.cases:
                if case.body_block:
                    self._mark_label_bump_up(case.body_block, False)
            if block.default_case and block.default_case.body_block:
                self._mark_label_bump_up(block.default_case.body_block, False)
