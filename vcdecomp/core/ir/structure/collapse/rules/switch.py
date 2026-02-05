"""
Switch/case collapse rules.

This module contains rules for collapsing switch/case patterns and handling
fall-through cases.
"""

from __future__ import annotations

from typing import Optional, Iterable
import os
import sys

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
from ....expr import ExpressionFormatter, format_block_expressions
from .....disasm import opcodes

SWITCH_EMPTY_DEBUG = os.environ.get("VCDECOMP_SWITCH_EMPTY_DEBUG", "0") == "1"


def _switch_empty_debug(msg: str) -> None:
    if SWITCH_EMPTY_DEBUG:
        print(f"DEBUG SWITCH EMPTY: {msg}", file=sys.stderr)


def _get_expression_formatter(graph: BlockGraph) -> Optional[ExpressionFormatter]:
    if graph.ssa_func is None:
        return None
    formatter = getattr(graph, "_expr_formatter", None)
    if formatter is None:
        formatter = ExpressionFormatter(graph.ssa_func)
        setattr(graph, "_expr_formatter", formatter)
    return formatter


def _block_ids_have_emitted_expressions(
    graph: BlockGraph,
    block_ids: Iterable[int],
    formatter: Optional[ExpressionFormatter],
    context: str,
) -> bool:
    if graph.ssa_func is None:
        _switch_empty_debug(f"{context}: no SSA function available")
        return False
    if formatter is None:
        _switch_empty_debug(f"{context}: no expression formatter available")
        return False
    ids = list(block_ids)
    if not ids:
        _switch_empty_debug(f"{context}: no block IDs to inspect")
        return False
    for block_id in ids:
        expressions = format_block_expressions(graph.ssa_func, block_id, formatter=formatter)
        for expr in expressions:
            if expr.text.strip() and not expr.text.strip().startswith("goto "):
                _switch_empty_debug(
                    f"{context}: emitted expression found in block {block_id} ({expr.mnemonic})"
                )
                return True
    _switch_empty_debug(f"{context}: no emitted expressions found")
    return False


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
        covers the case's entry CFG block ID. This handles cases where:
        1. The block is still a basic uncollapsed block
        2. The block was collapsed into a larger structure (BlockIf, BlockList, etc.)
        3. The block is inside another structure's covered_blocks

        Args:
            graph: The current block graph
            case_info: Case information containing block_id

        Returns:
            The structured block for the case entry, or None if not found
        """
        entry_cfg_id = case_info.block_id

        # First try direct lookup in cfg_to_struct mapping
        if entry_cfg_id in graph.cfg_to_struct:
            block = graph.cfg_to_struct[entry_cfg_id]
            if not block.is_collapsed:
                return block

        # Search through ALL uncollapsed blocks for one that covers this CFG block
        # This handles the case where the entry block was collapsed into a larger
        # structure (e.g., BlockIf, BlockList, BlockWhileDo) that covers multiple CFG blocks
        for struct_block in graph.get_uncollapsed_blocks():
            if entry_cfg_id in struct_block.covered_blocks:
                return struct_block

        # If the entry block was collapsed, find the outermost uncollapsed container.
        # Walk up the parent chain from the collapsed block to find its uncollapsed ancestor.
        if entry_cfg_id in graph.cfg_to_struct:
            block = graph.cfg_to_struct[entry_cfg_id]
            if block.is_collapsed:
                current = block
                while current and current.is_collapsed and current.parent:
                    current = current.parent
                if current and not current.is_collapsed:
                    return current

        # Last resort: search ALL blocks (including collapsed) and walk up parents
        for struct_block in graph.blocks.values():
            if entry_cfg_id in struct_block.covered_blocks:
                if not struct_block.is_collapsed:
                    return struct_block
                # Walk up parent chain
                current = struct_block
                while current and current.is_collapsed and current.parent:
                    current = current.parent
                if current and not current.is_collapsed:
                    return current

        return None

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        """
        Check if switch pattern matches.

        Simplified approach: Just check that this is a detected switch header.
        The switch rule runs LAST in the order, so other patterns have already
        had a chance to collapse. We accept the switch as-is.

        Important: inner (nested) switches must be collapsed before outer switches.
        If this switch's case body contains an uncollapsed inner switch header,
        we defer matching until the inner switch has been processed.
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

        # Check if any uncollapsed inner switch headers exist in this switch's blocks.
        # If so, defer collapsing this outer switch until inner switches are processed.
        for inner_pattern in self.switch_patterns:
            if inner_pattern is pattern:
                continue
            if inner_pattern.header_block in pattern.all_blocks:
                # Inner switch header is inside this switch's blocks
                # Check if the inner header is still an uncollapsed BlockBasic
                inner_block = graph.cfg_to_struct.get(inner_pattern.header_block)
                if inner_block and isinstance(inner_block, BlockBasic) and not inner_block.is_collapsed:
                    # Inner switch hasn't been processed yet - defer
                    return False

        return True

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        """
        Apply switch collapse using already-structured case bodies from graph.
        """
        formatter = _get_expression_formatter(graph)
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
                # Case entry block not found as uncollapsed block in the graph.
                # This happens when inner blocks weren't properly collapsed.
                # Instead of refusing the entire switch, create the case with
                # body_block=None and use body_block_ids for flat emission.
                # The emitter's _emit_switch_case_body_flat handles this path.
                if _block_ids_have_emitted_expressions(
                    graph,
                    [case_info.block_id],
                    formatter,
                    f"case {case_info.value}",
                ):
                    _switch_empty_debug(
                        f"case {case_info.value}: body has emitted expressions but entry block "
                        f"not found; using body_block_ids fallback for flat emission"
                    )
                case_body = None
                has_break = case_info.has_break

            cases.append(SwitchCase(
                value=case_info.value,
                body_block=case_body,  # Already structured (BlockIf, BlockList, etc.)
                is_default=False,
                has_break=has_break,
                fall_through_to=case_info.falls_through_to,  # Preserve fall-through relationship
                body_block_ids=set(case_info.body_blocks),  # CFG block IDs as fallback
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

            if default_body is None and _block_ids_have_emitted_expressions(
                graph,
                pattern.default_body_blocks,
                formatter,
                "default case",
            ):
                _switch_empty_debug("default case: body has emitted expressions; refusing to discard")
                return None

            default_case = SwitchCase(
                value=-1,
                body_block=default_body,
                is_default=True,
                has_break=True,
                body_block_ids=set(pattern.default_body_blocks),  # CFG block IDs as fallback
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

        # Collect all covered blocks (exclude switch exit so it can be emitted after switch)
        switch_block.covered_blocks = set(pattern.all_blocks)
        if pattern.exit_block is not None:
            switch_block.covered_blocks.discard(pattern.exit_block)

        # If exit_block wasn't detected, avoid covering return-only blocks
        # that are outside any case body (common switch epilogue).
        case_bodies: list[set] = []
        for case_info in pattern.cases:
            if case_info.body_blocks:
                case_bodies.append(set(case_info.body_blocks))
        if pattern.default_body_blocks:
            case_bodies.append(set(pattern.default_body_blocks))

        cfg = getattr(graph, "ssa_func", None).cfg if getattr(graph, "ssa_func", None) else None
        resolver = None
        if getattr(graph, "ssa_func", None) is not None:
            resolver = getattr(graph.ssa_func.scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
        if cfg and resolver:
            case_body_ids = set().union(*case_bodies) if case_bodies else set()
            for bid in list(switch_block.covered_blocks):
                if bid in case_body_ids:
                    continue
                cfg_block = cfg.blocks.get(bid)
                if not (cfg_block and cfg_block.instructions):
                    continue
                last_instr = cfg_block.instructions[-1]
                if resolver.is_return(last_instr.opcode):
                    switch_block.covered_blocks.discard(bid)

        # Register in structured_map so the emitter can find this switch
        # even after it's been removed from the graph by an outer switch.
        # Don't overwrite existing entries - inner switches register first
        # (due to innermost-first processing order) and should be preserved.
        if hasattr(graph, 'structured_map'):
            for cfg_id in switch_block.covered_blocks:
                if cfg_id not in graph.structured_map:
                    graph.structured_map[cfg_id] = switch_block

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

                # Update exit block's in_edges - preserve edges from switch body blocks
                # that are being removed (they're part of the switch structure)
                switch_body_blocks = set(block_ids_to_remove)
                exit_block.in_edges = [
                    e for e in exit_block.in_edges
                    if e.source.is_collapsed
                    or e.source == switch_block
                    or getattr(e.source, 'original_block_id', None) in switch_body_blocks
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
