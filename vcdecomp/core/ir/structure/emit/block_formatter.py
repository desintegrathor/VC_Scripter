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
from ...parenthesization import ExpressionContext, is_simple_expression
from ....disasm import opcodes
from ..patterns.models import IfElsePattern
from ..analysis.value_trace import _trace_value_to_function_call

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
    early_returns: Optional[Dict[int, tuple]] = None
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
    early_returns: Optional[Dict[int, tuple]] = None
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
        header_block, exit_block, continue_block, is_negated = early_returns[block_id]

        # Extract condition from SSA
        ssa_block = ssa_func.instructions.get(block_id, [])
        block = cfg.blocks[block_id]
        cond_text = None

        if block.instructions:
            last_instr = block.instructions[-1]

            # FÁZE 1.6: Special check - if there's CALL/XCALL + LLD immediately before JZ,
            # use the function call as the condition instead of the input value
            func_call_cond = None
            jz_index = None
            for idx, inst in enumerate(ssa_block):
                if inst.address == last_instr.address:
                    jz_index = idx
                    break

            if jz_index is not None and jz_index >= 2:
                # Check if pattern is: CALL/XCALL, LLD, (SSP), JZ
                # LLD should be 1-2 instructions before JZ
                import sys
                # print(f"DEBUG early_return block {block_id}: jz_index={jz_index}, checking for CALL+LLD", file=sys.stderr)
                for check_idx in range(jz_index - 1, max(0, jz_index - 3), -1):
                    check_inst = ssa_block[check_idx]
                    # print(f"  check_idx={check_idx}: {check_inst.mnemonic}@{check_inst.address}", file=sys.stderr)
                    if check_inst.mnemonic == "LLD":
                        # print(f"  Found LLD at {check_idx}", file=sys.stderr)
                        # Found LLD, now check if there's CALL/XCALL before it
                        for call_idx in range(check_idx - 1, max(0, check_idx - 3), -1):
                            call_inst = ssa_block[call_idx]
                            # print(f"    call_idx={call_idx}: {call_inst.mnemonic}@{call_inst.address}", file=sys.stderr)
                            if call_inst.mnemonic in {"CALL", "XCALL"}:
                                # Found CALL + LLD pattern! Use this as condition
                                # print(f"  Found CALL/XCALL at {call_idx}! Formatting...", file=sys.stderr)
                                # print(f"  CALL inputs: {[inp.name for inp in call_inst.inputs]}", file=sys.stderr)
                                try:
                                    call_expr = formatter._format_call(call_inst)
                                    # print(f"  Formatted: {call_expr}", file=sys.stderr)
                                    if call_expr.endswith(";"):
                                        call_expr = call_expr[:-1].strip()
                                    func_call_cond = call_expr
                                    # print(f"  func_call_cond set to: {func_call_cond}", file=sys.stderr)
                                except Exception as e:
                                    # print(f"  Exception formatting: {e}", file=sys.stderr)
                                    import traceback
                                    traceback.print_exc(file=sys.stderr)
                                break
                        break

            # Extract condition from SSA
            for ssa_inst in ssa_block:
                if ssa_inst.address == last_instr.address and ssa_inst.inputs:
                    cond_value = ssa_inst.inputs[0]

                    if func_call_cond:
                        # Use function call as condition
                        cond_expr = func_call_cond
                    else:
                        # FÁZE 1.6: Check if condition value comes from function call
                        func_call = _trace_value_to_function_call(ssa_func, cond_value, formatter)
                        if func_call:
                            cond_expr = func_call
                        else:
                            # FIX 3: Pass IN_CONDITION context
                            cond_expr = formatter.render_value(cond_value, context=ExpressionContext.IN_CONDITION)
                            # Only use SSA name if rendered as pure number
                            if cond_expr.lstrip('-').isdigit():
                                alias = cond_value.alias or cond_value.name
                                if alias and not alias.startswith("data_"):
                                    cond_expr = alias

                    # FIX 3: Smart negation - only add parens if needed
                    if is_negated:
                        if is_simple_expression(cond_expr):
                            cond_text = f"!{cond_expr}"
                        else:
                            cond_text = f"!({cond_expr})"
                    else:
                        cond_text = cond_expr
                    break

        if cond_text is None:
            cond_text = f"cond_{block_id}"

        lines = []
        # Render header statements (excluding the conditional jump)
        expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)
        if expressions:
            # Filter out the last expression (conditional jump)
            for expr in expressions[:-1]:
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
        # _render_if_else_recursive will be defined in code_emitter.py (subtask 5.2)
        from .code_emitter import _render_if_else_recursive
        return _render_if_else_recursive(
            block_to_if[block_id], indent, ssa_func, formatter,
            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
            early_returns
        )

    # Regular block formatting
    expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)
    return [f"{indent}{expr.text}" for expr in expressions]
