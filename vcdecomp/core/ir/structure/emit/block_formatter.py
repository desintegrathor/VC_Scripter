"""
Block formatting utilities for code emission.

This module contains functions for formatting block expressions into code lines,
including filtering specific variable assignments and handling recursive structure
detection for nested control flow patterns.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, TYPE_CHECKING

from ...ssa import SSAFunction
from ...expr import format_block_expressions, ExpressionFormatter
from ...cfg import CFG
from ....disasm import opcodes
from ..patterns.models import IfElsePattern
from ..analysis.condition import render_condition

if TYPE_CHECKING:
    # Forward reference to avoid circular import with code_emitter
    # This will be resolved when code_emitter.py is created in subtask 5.2
    from typing import Callable


def _format_block_lines_filtered(
    ssa_func: SSAFunction,
    block_id: int,
    indent: str,
    formatter: ExpressionFormatter,
    skip_var: str,
    block_to_if: Optional[Dict[int, IfElsePattern]] = None,
    visited_ifs: Optional[Set[int]] = None,
    emitted_blocks: Optional[Set[int]] = None,
    cfg: Optional[CFG] = None,
    start_to_block: Optional[Dict[int, int]] = None,
    resolver: Optional[opcodes.OpcodeResolver] = None,
    # FÁZE 1.3: Early return/break pattern detection
    early_returns: Optional[Dict[int, tuple]] = None,
    skip_early_return_blocks: Optional[Set[int]] = None
) -> List[str]:
    """
    Format block expressions but skip the last assignment to a specific variable.

    Used to suppress loop initialization when it's duplicated in for-loop header.

    Args:
        ssa_func: SSA function data
        block_id: Block ID to format
        indent: Indentation string
        formatter: ExpressionFormatter to use
        skip_var: Variable name to skip the last assignment for
        block_to_if: Map of block IDs to if/else patterns (unused here, for API consistency)
        visited_ifs: Set of if/else headers already rendered (unused here, for API consistency)
        emitted_blocks: Set of blocks already rendered (unused here, for API consistency)
        cfg: Control flow graph (unused here, for API consistency)
        start_to_block: Map of instruction addresses to block IDs (unused here, for API consistency)
        resolver: Opcode resolver (unused here, for API consistency)
        early_returns: Map of block IDs to early return patterns (unused here, for API consistency)

    Returns:
        List of formatted code lines with the last assignment to skip_var removed
    """
    # Get all expressions for this block
    expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)

    # Find the last assignment to skip_var
    last_assignment_idx = -1
    for i in range(len(expressions) - 1, -1, -1):
        expr = expressions[i]
        text = expr.text.strip().rstrip(';')  # Remove trailing semicolon
        # Check if this expression assigns to skip_var
        # Pattern: "skip_var = ..." or "skip_var++" or "skip_var--" or "++skip_var" or "--skip_var"
        if (text.startswith(f"{skip_var} =") or
            text == f"{skip_var}++" or text == f"{skip_var}--" or
            text == f"++{skip_var}" or text == f"--{skip_var}"):
            last_assignment_idx = i
            break

    # Filter out the last assignment
    if last_assignment_idx >= 0:
        filtered_expressions = expressions[:last_assignment_idx] + expressions[last_assignment_idx + 1:]
    else:
        filtered_expressions = expressions

    return [f"{indent}{expr.text}" for expr in filtered_expressions]


def _format_block_lines(
    ssa_func: SSAFunction,
    block_id: int,
    indent: str,
    formatter: ExpressionFormatter = None,
    # FIX 3B: New params for recursive structure detection
    block_to_if: Optional[Dict[int, IfElsePattern]] = None,
    visited_ifs: Optional[Set[int]] = None,
    emitted_blocks: Optional[Set[int]] = None,
    cfg: Optional[CFG] = None,
    start_to_block: Optional[Dict[int, int]] = None,
    resolver: Optional[opcodes.OpcodeResolver] = None,
    # FÁZE 1.3: Early return/break pattern detection
    early_returns: Optional[Dict[int, tuple]] = None,
    skip_early_return_blocks: Optional[Set[int]] = None,
    func_loops: Optional[List] = None,
    global_map: Optional[Dict[int, str]] = None,
    switch_exit_ids: Optional[Set[int]] = None,
) -> List[str]:
    """
    Format expressions for a block, with optional recursive structure detection.

    Args:
        ssa_func: SSA function data
        block_id: Block ID to format
        indent: Indentation string
        formatter: Optional ExpressionFormatter to use. If None, creates a new one.
        block_to_if: Map of block IDs to if/else patterns (for recursive detection)
        visited_ifs: Set of if/else headers already rendered (for recursive detection)
        emitted_blocks: Set of blocks already rendered (for recursive detection)
        cfg: Control flow graph (for recursive detection)
        start_to_block: Map of instruction addresses to block IDs (for recursive detection)
        resolver: Opcode resolver (for recursive detection)
        early_returns: Map of block IDs to early return patterns (FÁZE 1.3)

    Returns:
        List of formatted code lines for the block

    Note:
        When formatter is provided, uses it for consistent per-function structure detection.
        When recursive params are provided, can detect and render nested if/else structures.
    """
    # FÁZE 1.1: Check if block already emitted - skip to prevent duplication
    if emitted_blocks is not None and block_id in emitted_blocks:
        return []  # Already rendered, don't duplicate

    # FÁZE 1.3: Check if this block is an early return/break pattern
    if early_returns and block_id in early_returns:
        if skip_early_return_blocks and block_id in skip_early_return_blocks:
            expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)
            return [f"{indent}{expr.text}" for expr in expressions]
        header_block, exit_block, continue_block, is_negated = early_returns[block_id]

        condition_render = render_condition(
            ssa_func,
            block_id,
            formatter,
            cfg,
            resolver,
            negate=is_negated
        )
        cond_text = condition_render.text or f"cond_{block_id}"

        lines = []
        # Render ALL header statements.
        # format_block_expressions() already filters out control flow ops
        # (JMP, JZ, JNZ), so all remaining expressions are real statements.
        # The branch condition is rendered separately by render_condition() above.
        expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)
        for expr in expressions:
            lines.append(f"{indent}{expr.text}")

        # Render early return/break
        lines.append(f"{indent}if ({cond_text}) break;")

        # Mark blocks as emitted
        emitted_blocks.add(block_id)
        emitted_blocks.add(exit_block)
        # Don't add continue_block - it will be rendered normally after this

        return lines

    # FIX 3B: Check if this block is an if/else header - render recursively
    if (block_to_if and visited_ifs is not None and emitted_blocks is not None and
        block_id in block_to_if and block_id == block_to_if[block_id].header_block and
        block_id not in visited_ifs and cfg and start_to_block and resolver):
        # Lazy import to avoid circular dependency
        from .code_emitter import _render_if_else_recursive
        return _render_if_else_recursive(
            block_to_if[block_id], indent, ssa_func, formatter,
            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
            early_returns, func_loops=func_loops, global_map=global_map,
            switch_exit_ids=switch_exit_ids
        )

    # Regular block formatting
    expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)

    # Mark block as emitted BEFORE rendering to prevent re-entry issues
    # This must happen here to prevent duplicate emission when blocks are processed
    # from multiple call sites (e.g., both from switch case body iteration and
    # from nested if/else rendering within the same case body).
    if emitted_blocks is not None:
        emitted_blocks.add(block_id)

    # TASK 2 (07-07): Detect and remove unreachable code after returns
    # Scan through expressions and stop emitting after an unconditional return
    filtered_lines = []
    found_return = False

    for expr in expressions:
        expr_text = expr.text.strip()

        # If we already found a return, this statement is unreachable - skip it
        if found_return:
            # Skip emitting (silently omit for clean output)
            # Alternative: emit as comment for debugging
            # filtered_lines.append(f"{indent}// UNREACHABLE: {expr.text}")
            continue

        # Emit the statement
        filtered_lines.append(f"{indent}{expr.text}")

        # Check if this is an unconditional return
        # Pattern: "return;" or "return <value>;"
        if expr_text.startswith("return"):
            # Check if it's truly unconditional (not inside a ternary or complex expression)
            # Simple heuristic: if line starts with "return", it's unconditional
            found_return = True

    return filtered_lines
