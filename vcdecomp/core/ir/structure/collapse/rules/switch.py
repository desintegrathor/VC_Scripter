"""
Switch/case collapse rules.

This module contains rules for collapsing switch/case patterns and handling
fall-through cases.
"""

from __future__ import annotations

from typing import Optional

from .base import CollapseRule
from ...blocks.hierarchy import (
    BlockType,
    EdgeType,
    BlockGraph,
    StructuredBlock,
    BlockBasic,
    BlockSwitch,
    BlockEdge,
    SwitchCase,
)


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
