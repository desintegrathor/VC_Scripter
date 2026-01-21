"""
Code rendering and emission for structured output.

This module contains functions for recursively rendering if/else structures,
loops, and other control flow patterns into structured C-like code.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Any

from ...ssa import SSAFunction
from ...expr import ExpressionFormatter
from ...cfg import CFG, NaturalLoop
from ...parenthesization import ExpressionContext, is_simple_expression
from ....disasm import opcodes
from ..patterns.models import IfElsePattern, CompoundCondition
from ..patterns.loops import _detect_for_loop
from ..analysis.condition import _combine_conditions
from ..utils.helpers import SHOW_BLOCK_COMMENTS, _is_control_flow_only
from .block_formatter import _format_block_lines, _format_block_lines_filtered


def _render_if_else_recursive(
    if_pattern: IfElsePattern,
    indent: str,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    block_to_if: Dict[int, IfElsePattern],
    visited_ifs: Set[int],
    emitted_blocks: Set[int],
    cfg: CFG,
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver,
    # FÁZE 1.3: Early return/break pattern detection
    early_returns: Optional[Dict[int, tuple]] = None
) -> List[str]:
    """
    Recursively render if/else with nested structures.

    This allows if/else patterns to be properly nested inside other structures
    like switch cases.

    Args:
        if_pattern: The if/else pattern to render
        indent: Current indentation
        ssa_func: SSA function data
        formatter: Expression formatter
        block_to_if: Map of block IDs to if/else patterns
        visited_ifs: Set to track rendered if/else headers
        emitted_blocks: Set to track rendered blocks
        cfg: Control flow graph
        start_to_block: Address to block ID map
        resolver: Opcode resolver

    Returns:
        List of rendered lines
    """
    lines = []
    ssa_blocks = ssa_func.instructions

    # Mark this if/else as visited
    visited_ifs.add(if_pattern.header_block)

    # Get header block
    header_block = cfg.blocks[if_pattern.header_block]

    # NEW: Check if this is a compound condition pattern
    compound = getattr(if_pattern, 'compound', None)
    if compound is not None:
        # VALIDATION: Check if compound has calculated bodies
        if hasattr(compound, 'true_body') and compound.true_body:
            # Use calculated bodies from detection phase
            true_body = compound.true_body
        else:
            # Fallback to old behavior (single target)
            true_body = {compound.true_target}

        # CRITICAL VALIDATION: Empty body means bad detection - skip rendering
        if not true_body or (len(true_body) == 1 and compound.true_target in compound.involved_blocks):
            import sys
            print(f"WARNING: Empty body for compound at block {if_pattern.header_block}, skipping",
                  file=sys.stderr)
            return []  # Don't render empty if blocks

        # This is a compound condition (AND/OR chain)
        # Render using _combine_conditions helper
        cond_text = _combine_conditions(
            compound.conditions,
            compound.operator,
            preserve_style=True  # Match original formatting
        )

        # FIX #8: Extract header code from the first block in the compound chain
        # The header block (if_pattern.header_block) may have code BEFORE the compound condition
        # We need to emit that code first
        header_block_id = if_pattern.header_block
        header_code_lines = []

        # Only emit header code if this is the actual header block (not a nested involved block)
        if header_block_id not in emitted_blocks:
            # Get all expressions from the header block
            from ...expr import format_block_expressions
            header_exprs = format_block_expressions(ssa_func, header_block_id, formatter=formatter)

            # Filter out comparison/jump expressions that are part of the compound condition
            # These typically include EQU, JZ/JNZ instructions
            # We want to keep XCALL, ASGN, and other "real" code
            for expr in header_exprs:
                expr_text = expr.text.strip()
                # Skip if it's a goto or empty
                if expr_text.startswith("goto ") or not expr_text:
                    continue
                # Skip if it's a simple comparison assignment (part of condition chain)
                # Pattern: "tmp = value == constant;"
                if " == " in expr_text and expr_text.endswith(";") and expr_text.count("=") == 2:
                    continue
                # Keep everything else (function calls, assignments, etc.)
                header_code_lines.append(f"{indent}{expr_text}")

        # Emit header code before the if statement
        lines.extend(header_code_lines)

        # Mark all involved blocks (condition testing blocks) as emitted and visited
        # This prevents them from being re-processed as separate if/else patterns
        for involved_block in compound.involved_blocks:
            emitted_blocks.add(involved_block)
            visited_ifs.add(involved_block)

        # Render the if statement with compound condition
        lines.append(f"{indent}if ({cond_text}) {{")

        # Render true body - iterate over ALL body blocks, not just target
        for body_block_id in sorted(true_body, key=lambda b: cfg.blocks[b].start if b in cfg.blocks else b):
            if body_block_id not in emitted_blocks:
                true_block_lines = _format_block_lines(
                    ssa_func, body_block_id, indent + "    ", formatter,
                    block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                    early_returns
                )
                lines.extend(true_block_lines)
                # Mark this body block as emitted
                emitted_blocks.add(body_block_id)

        lines.append(f"{indent}}}")

        return lines

    # Extract condition from SSA (simple if/else case)
    cond_text = None
    ssa_block = ssa_blocks.get(if_pattern.header_block, [])

    # FÁZE 1.6: Check if there's CALL/XCALL + LLD immediately before JZ/JNZ
    func_call_cond = None
    if header_block.instructions:
        last_instr = header_block.instructions[-1]
        jz_index = None
        for idx, inst in enumerate(ssa_block):
            if inst.address == last_instr.address:
                jz_index = idx
                break

        if jz_index is not None and jz_index >= 2:
            # Check if pattern is: CALL/XCALL, LLD, (SSP), JZ/JNZ
            for check_idx in range(jz_index - 1, max(0, jz_index - 3), -1):
                check_inst = ssa_block[check_idx]
                if check_inst.mnemonic == "LLD":
                    # Found LLD, now check if there's CALL/XCALL before it
                    for call_idx in range(check_idx - 1, max(0, check_idx - 3), -1):
                        call_inst = ssa_block[call_idx]
                        if call_inst.mnemonic in {"CALL", "XCALL"}:
                            # Found CALL + LLD pattern! Use this as condition
                            try:
                                call_expr = formatter._format_call(call_inst)
                                if call_expr.endswith(";"):
                                    call_expr = call_expr[:-1].strip()
                                func_call_cond = call_expr
                            except Exception:
                                pass
                            break
                    break

    if header_block.instructions:
        last_instr = header_block.instructions[-1]
        mnemonic = resolver.get_mnemonic(last_instr.opcode)
        for ssa_inst in ssa_block:
            if ssa_inst.address == last_instr.address and ssa_inst.inputs:
                cond_value = ssa_inst.inputs[0]

                # FÁZE 1.6: Use function call if detected
                if func_call_cond:
                    cond_expr = func_call_cond
                else:
                    # FIX 3: Pass IN_CONDITION context
                    cond_expr = formatter.render_value(cond_value, context=ExpressionContext.IN_CONDITION)
                    # Only use SSA name if rendered as pure number
                    if cond_expr.lstrip('-').isdigit():
                        alias = cond_value.alias or cond_value.name
                        if alias and not alias.startswith("data_"):
                            cond_expr = alias
                # FÁZE 3 FIX: NO negation needed - we already swapped true/false branches
                # in _detect_if_else_pattern based on JZ vs JNZ semantics
                # FIX 3: No hardcoded parens - expression already has them if needed
                cond_text = cond_expr
                break
    if cond_text is None:
        cond_text = f"cond_{if_pattern.header_block}"

    # Render header block statements (excluding conditional jump)
    # Only add comment if block has actual statements
    if SHOW_BLOCK_COMMENTS and not _is_control_flow_only(ssa_block, resolver):
        lines.append(f"{indent}// Block {if_pattern.header_block} @{header_block.start}")

    # Get header statements (excluding the conditional jump)
    header_lines = _format_block_lines(
        ssa_func, if_pattern.header_block, indent, formatter,
        None, None, None, None, None, None,  # Disable recursion for header itself
        early_returns
    )

    # Remove last line if it's the conditional jump
    if header_lines and ("goto" in header_lines[-1] or "if (" in header_lines[-1]):
        header_lines = header_lines[:-1]

    # FÁZE 1.6: If we detected a function call as condition, remove the call statement
    # from header_lines to avoid duplication
    if func_call_cond and header_lines:
        # The last statement might be the function call - check and remove if so
        for i in range(len(header_lines) - 1, -1, -1):
            line = header_lines[i].strip()
            # Check if line contains XCALL or CALL by looking for known patterns
            if (line.startswith("SC_") or line.startswith("func_")) and line.endswith(";"):
                # This is likely the function call statement
                header_lines = header_lines[:i] + header_lines[i+1:]
                break

    lines.extend(header_lines)

    # Render if statement
    lines.append(f"{indent}if ({cond_text}) {{")

    # Render true branch (recursively)
    true_body_sorted = sorted(if_pattern.true_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
    for body_block_id in true_body_sorted:
        # FÁZE 1.1: Skip already emitted blocks
        if body_block_id in emitted_blocks:
            continue
        body_block = cfg.blocks.get(body_block_id)
        if body_block:
            # Recursive call - will detect nested if/else
            ssa_block = ssa_blocks.get(body_block_id, [])
            if not _is_control_flow_only(ssa_block, resolver):
                if SHOW_BLOCK_COMMENTS: lines.append(f"{indent}    // Block {body_block_id} @{body_block.start}")
            lines.extend(_format_block_lines(
                ssa_func, body_block_id, indent + "    ", formatter,
                block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                early_returns
            ))

            # DEAD CODE ELIMINATION: Stop if block ends with return
            if body_block.instructions:
                last_instr = body_block.instructions[-1]
                if resolver.is_return(last_instr.opcode):
                    break  # Remaining blocks are unreachable

    # Render false branch if exists
    if if_pattern.false_body:
        lines.append(f"{indent}}} else {{")

        # Render false branch (recursively)
        false_body_sorted = sorted(if_pattern.false_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
        for body_block_id in false_body_sorted:
            # FÁZE 1.1: Skip already emitted blocks
            if body_block_id in emitted_blocks:
                continue
            body_block = cfg.blocks.get(body_block_id)
            if body_block:
                # Recursive call - will detect nested if/else
                ssa_block = ssa_blocks.get(body_block_id, [])
                if not _is_control_flow_only(ssa_block, resolver):
                    if SHOW_BLOCK_COMMENTS: lines.append(f"{indent}    // Block {body_block_id} @{body_block.start}")
                lines.extend(_format_block_lines(
                    ssa_func, body_block_id, indent + "    ", formatter,
                    block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                    early_returns
                ))

                # DEAD CODE ELIMINATION: Stop if block ends with return
                if body_block.instructions:
                    last_instr = body_block.instructions[-1]
                    if resolver.is_return(last_instr.opcode):
                        break  # Remaining blocks are unreachable

    lines.append(f"{indent}}}")

    # Mark all blocks as emitted
    emitted_blocks.add(if_pattern.header_block)
    emitted_blocks.update(if_pattern.true_body)
    emitted_blocks.update(if_pattern.false_body)

    return lines


def _render_blocks_with_loops(
    block_ids: List[int],
    indent: str,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    cfg: CFG,
    func_loops: List,
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver,
    block_to_if: Dict[int, Any],
    visited_ifs: Set[int],
    emitted_blocks: Set[int],
    global_map: Optional[Dict[int, str]] = None,
    # FÁZE 1.3: Early return/break pattern detection
    early_returns: Optional[Dict[int, tuple]] = None
) -> List[str]:
    """
    Render a sequence of blocks with loop detection support.

    Used for rendering switch case bodies where loops may be present.
    """
    lines: List[str] = []
    processed_in_loop: Set[int] = set()

    # Track which blocks have for-loops as successors and what variable to skip
    skip_last_assignment: Dict[int, str] = {}  # block_id -> variable_name to skip

    # Pre-scan to identify blocks that need initialization skipped
    for body_block_id in block_ids:
        # Check if this block is a loop header
        for loop in func_loops:
            if loop.header == body_block_id:
                # Try to detect for-loop pattern
                for_info = _detect_for_loop(loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map)
                if for_info:
                    # Mark predecessor blocks to skip initialization
                    header_block = cfg.blocks.get(loop.header)
                    if header_block:
                        for pred_id in header_block.predecessors:
                            if pred_id not in loop.body and pred_id in block_ids:
                                # This predecessor should skip assignment to loop variable
                                skip_last_assignment[pred_id] = for_info.init_var
                break

    for body_block_id in block_ids:
        # Skip if already processed as part of a loop
        if body_block_id in processed_in_loop:
            continue

        body_block = cfg.blocks.get(body_block_id)
        if not body_block:
            continue

        # Check if this block is a loop header
        header_loop = None
        for loop in func_loops:
            if loop.header == body_block_id:
                header_loop = loop
                break

        # FÁZE 3.2 FIX: Loop headers take precedence over emitted_blocks
        # Even if a loop header was marked as emitted (e.g., as part of if/else body),
        # we should render it as a loop instead
        if not header_loop:
            # Not a loop header - check if already emitted as part of if/else
            if body_block_id in emitted_blocks:
                continue

        if header_loop:
            # Render loop
            lines.append(f"{indent}// Loop header - Block {body_block_id} @{body_block.start}")

            # Try to detect for-loop pattern
            for_info = _detect_for_loop(header_loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map)
            if for_info:
                lines.append(f"{indent}for ({for_info.var} = {for_info.init}; {for_info.condition}; {for_info.increment}) {{")
            else:
                lines.append(f"{indent}while (TRUE) {{  // loop body: blocks {sorted(header_loop.body)}")

            # Render loop body blocks
            loop_body_sorted = sorted(header_loop.body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
            for loop_body_id in loop_body_sorted:
                loop_body_block = cfg.blocks.get(loop_body_id)
                if loop_body_block:
                    ssa_block = ssa_func.instructions.get(loop_body_id, [])
                    if not _is_control_flow_only(ssa_block, resolver):
                        if SHOW_BLOCK_COMMENTS: lines.append(f"{indent}    // Block {loop_body_id} @{loop_body_block.start}")

                    # FÁZE 3.2 FIX: For for-loops, skip increment in back edge block
                    # Back edge block contains the increment and jumps back to header
                    # Identify back edge block: has loop header as successor
                    skip_var = None
                    if for_info:
                        # Check if this block jumps back to header (back edge)
                        if header_loop.header in loop_body_block.successors:
                            skip_var = for_info.var  # Skip increment for loop variable

                    if skip_var:
                        # Filter out increment assignment
                        block_lines = _format_block_lines_filtered(
                            ssa_func, loop_body_id, indent + "    ", formatter, skip_var,
                            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                            early_returns
                        )
                        lines.extend(block_lines)
                    else:
                        lines.extend(_format_block_lines(
                            ssa_func, loop_body_id, indent + "    ", formatter,
                            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                            early_returns
                        ))

            lines.append(f"{indent}}}")

            # Mark all loop body blocks as processed
            processed_in_loop.update(header_loop.body)
        else:
            # Regular block - render normally
            ssa_block = ssa_func.instructions.get(body_block_id, [])
            if not _is_control_flow_only(ssa_block, resolver):
                if SHOW_BLOCK_COMMENTS: lines.append(f"{indent}// Block {body_block_id} @{body_block.start}")

            # Check if we need to skip last assignment in this block
            if body_block_id in skip_last_assignment:
                skip_var = skip_last_assignment[body_block_id]
                # Render expressions but filter out the last assignment to skip_var
                block_lines = _format_block_lines_filtered(
                    ssa_func, body_block_id, indent, formatter, skip_var,
                    block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                    early_returns
                )
                lines.extend(block_lines)
            else:
                lines.extend(_format_block_lines(
                    ssa_func, body_block_id, indent, formatter,
                    block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                    early_returns
                ))

            # DEAD CODE ELIMINATION: Check if block terminates execution
            # If block ends with return, stop rendering remaining blocks (they're unreachable)
            if body_block and body_block.instructions:
                last_instr = body_block.instructions[-1]
                if resolver.is_return(last_instr.opcode):
                    # Stop iteration - all following blocks are unreachable
                    break

    return lines
