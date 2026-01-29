"""
Code rendering and emission for structured output.

This module contains functions for recursively rendering if/else structures,
loops, and other control flow patterns into structured C-like code.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Any, Tuple

from ...ssa import SSAFunction
from ...expr import ExpressionFormatter, format_block_expressions
from ...cfg import CFG, NaturalLoop
from ....disasm import opcodes
from ..patterns.models import IfElsePattern, CompoundCondition, SwitchPattern, CaseInfo, TernaryInfo
from ..patterns.loops import _detect_for_loop, _detect_while_loop, _detect_do_while_loop
from ..patterns.if_else import _detect_ternary_pattern
from ..patterns.models import WhileLoopInfo, DoWhileLoopInfo
from ..analysis.condition import _combine_conditions, render_condition
from ..utils.helpers import SHOW_BLOCK_COMMENTS, _is_control_flow_only
from .block_formatter import _format_block_lines, _format_block_lines_filtered


def _render_block_statements(
    ssa_func: SSAFunction,
    block_id: int,
    formatter: ExpressionFormatter,
    resolver: "opcodes.OpcodeResolver",
    global_map: Optional[Dict[int, str]] = None,
) -> List[str]:
    """
    Render statements for a basic block.

    This is a simple helper function that formats expressions for a single block
    without recursive if/else handling. Used by the hierarchical emitter.

    Args:
        ssa_func: SSA function data
        block_id: Block ID to format
        formatter: ExpressionFormatter to use
        resolver: Opcode resolver
        global_map: Optional global variable name map

    Returns:
        List of statement strings (without indentation)
    """
    expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)

    lines = []
    found_return = False

    for expr in expressions:
        expr_text = expr.text.strip()

        # Skip unreachable code after returns
        if found_return:
            continue

        lines.append(expr_text)

        # Check if this is an unconditional return
        if expr_text.startswith("return"):
            found_return = True

    return lines


def _partition_blocks_for_nested_switch(
    block_ids: List[int],
    nested_switch: SwitchPattern,
    cfg: CFG
) -> Tuple[List[int], List[int]]:
    """
    Partition blocks into pre-nested and post-nested groups.

    Nested switch blocks are excluded entirely (rendered separately via callback).
    This ensures correct structural order regardless of bytecode address interleaving.

    Args:
        block_ids: List of block IDs to partition
        nested_switch: The nested switch pattern to partition around
        cfg: Control flow graph for address lookups

    Returns:
        Tuple of (pre_nested_blocks, post_nested_blocks) both sorted by address.
    """
    nested_header_addr = cfg.blocks[nested_switch.header_block].start if nested_switch.header_block in cfg.blocks else 0
    nested_blocks = nested_switch.all_blocks

    pre: List[int] = []
    post: List[int] = []

    for bid in block_ids:
        if bid in nested_blocks:
            continue  # Skip - rendered with nested switch
        block_addr = cfg.blocks[bid].start if bid in cfg.blocks else 0
        if block_addr < nested_header_addr:
            pre.append(bid)
        else:
            post.append(bid)

    pre.sort(key=lambda b: cfg.blocks[b].start if b in cfg.blocks else 0)
    post.sort(key=lambda b: cfg.blocks[b].start if b in cfg.blocks else 0)
    return pre, post


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
    early_returns: Optional[Dict[int, tuple]] = None,
    func_loops: Optional[List] = None,
    global_map: Optional[Dict[int, str]] = None,
    switch_exit_ids: Optional[Set[int]] = None,
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

            for expr in header_exprs:
                expr_text = expr.text.strip()
                # Skip if it's a goto or empty
                if expr_text.startswith("goto ") or not expr_text:
                    continue
                if expr.address in compound.condition_addrs:
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
        if func_loops:
            lines.extend(_render_blocks_with_loops(
                sorted(true_body, key=lambda b: cfg.blocks[b].start if b in cfg.blocks else b),
                indent + "    ",
                ssa_func,
                formatter,
                cfg,
                func_loops,
                start_to_block,
                resolver,
                block_to_if,
                visited_ifs,
                emitted_blocks,
                global_map,
                early_returns
            ))
        else:
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
    condition_render = render_condition(
        ssa_func,
        if_pattern.header_block,
        formatter,
        cfg,
        resolver,
        negate=False
    )
    cond_text = condition_render.text or f"cond_{if_pattern.header_block}"

    # NEW: Try to detect ternary pattern before rendering full if/else
    ternary_info = _detect_ternary_pattern(
        if_pattern, ssa_func, formatter, cfg, resolver, cond_text
    )

    if ternary_info:
        # Render as ternary operator instead of if/else
        # First, render any header statements (excluding the conditional jump)
        ssa_block = ssa_blocks.get(if_pattern.header_block, [])

        header_lines = _format_block_lines(
            ssa_func, if_pattern.header_block, indent, formatter,
            None, None, None, None, None, None,  # Disable recursion for header itself
            early_returns
        )

        # Remove last line if it's the conditional jump
        if header_lines and ("goto" in header_lines[-1] or "if (" in header_lines[-1]):
            header_lines = header_lines[:-1]

        # Remove condition statement if it duplicates the rendered condition
        if header_lines and condition_render.text:
            header_lines = [
                line for line in header_lines
                if line.strip().rstrip(";") != condition_render.text
            ]

        lines.extend(header_lines)

        # Render the ternary expression
        lines.append(f"{indent}{ternary_info.variable} = ({ternary_info.condition}) ? {ternary_info.true_value} : {ternary_info.false_value};")

        # Mark all blocks as emitted
        emitted_blocks.add(if_pattern.header_block)
        emitted_blocks.update(if_pattern.true_body)
        emitted_blocks.update(if_pattern.false_body)

        return lines

    # Render header block statements (excluding conditional jump)
    # Only add comment if block has actual statements
    ssa_block = ssa_blocks.get(if_pattern.header_block, [])
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

    if condition_render.call_is_condition_only and condition_render.call_statement_text:
        header_lines = [
            line for line in header_lines
            if line.strip() != condition_render.call_statement_text
        ]

    # Remove condition statement if it duplicates the rendered condition
    if header_lines and condition_render.text:
        header_lines = [
            line for line in header_lines
            if line.strip().rstrip(";") != condition_render.text
        ]

    lines.extend(header_lines)

    # Normalize inverted conditions for more natural code.
    # Case 1: `if (!expr)` with both branches → swap branches, remove negation
    # Case 2: `if (cond) { /* empty */ } else { code }` → `if (!cond) { code }`
    render_true_body = if_pattern.true_body
    render_false_body = if_pattern.false_body
    render_cond_text = cond_text

    def _negate_condition(cond: str) -> str:
        """Negate a condition expression, simplifying where possible."""
        # Simple negation removal
        if cond.startswith("!(") and cond.endswith(")"):
            return cond[2:-1]
        if cond.startswith("! "):
            return cond[2:]
        if cond.startswith("!"):
            return cond[1:]
        # Flip comparison operators
        flip_ops = {
            " < ": " >= ", " > ": " <= ",
            " <= ": " > ", " >= ": " < ",
            " == ": " != ", " != ": " == ",
        }
        for op, flipped in flip_ops.items():
            if op in cond:
                return cond.replace(op, flipped, 1)
        # Fallback: wrap in !()
        if ' ' in cond or '(' in cond:
            return f"!({cond})"
        return f"!{cond}"

    def _true_body_is_empty() -> bool:
        """Check if the true body has no real statements (only control flow)."""
        if not if_pattern.true_body:
            return True
        for bid in if_pattern.true_body:
            ssa_block_check = ssa_func.instructions.get(bid, [])
            if not _is_control_flow_only(ssa_block_check, resolver):
                return False
        return True

    should_swap = False
    if if_pattern.false_body:
        if cond_text.startswith("!"):
            # Case 1: negated condition with both branches
            should_swap = True
        elif _true_body_is_empty():
            # Case 2: empty true body with non-empty else → negate and swap
            should_swap = True

    if should_swap:
        render_cond_text = _negate_condition(cond_text)
        render_true_body = if_pattern.false_body
        render_false_body = if_pattern.true_body

    # Detect conditional break pattern: if one branch ends with JMP to switch exit,
    # render as `if (cond) { body; break; }` + sequential code instead of if/else.
    def _branch_ends_with_switch_exit(body: Set[int]) -> bool:
        """Check if the last block in a branch ends with JMP to a switch exit block."""
        if not body or not switch_exit_ids:
            return False
        # Find the last block by address
        last_bid = max(body, key=lambda b: cfg.blocks[b].start if b in cfg.blocks else 0)
        blk = cfg.blocks.get(last_bid)
        if not blk or not blk.instructions:
            return False
        last_instr = blk.instructions[-1]
        mnem = resolver.get_mnemonic(last_instr.opcode)
        if mnem == "JMP":
            jmp_target = start_to_block.get(last_instr.arg1)
            return jmp_target in switch_exit_ids
        return False

    # Check if one branch ends with a break (JMP to switch exit)
    true_has_break = _branch_ends_with_switch_exit(render_true_body)
    false_has_break = _branch_ends_with_switch_exit(render_false_body)

    if true_has_break and render_false_body and not false_has_break:
        # True branch ends with break → emit as: if (cond) { body; break; }
        # The false body will be emitted as sequential code after the if block.
        lines.append(f"{indent}if ({render_cond_text}) {{")

        true_body_sorted = sorted(render_true_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
        if func_loops:
            lines.extend(_render_blocks_with_loops(
                true_body_sorted, indent + "    ", ssa_func, formatter, cfg,
                func_loops, start_to_block, resolver, block_to_if, visited_ifs,
                emitted_blocks, global_map, early_returns
            ))
        else:
            for body_block_id in true_body_sorted:
                if body_block_id in emitted_blocks:
                    continue
                body_block = cfg.blocks.get(body_block_id)
                if body_block:
                    ssa_block = ssa_blocks.get(body_block_id, [])
                    if not _is_control_flow_only(ssa_block, resolver):
                        if SHOW_BLOCK_COMMENTS: lines.append(f"{indent}    // Block {body_block_id} @{body_block.start}")
                    lines.extend(_format_block_lines(
                        ssa_func, body_block_id, indent + "    ", formatter,
                        block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                        early_returns
                    ))

        lines.append(f"{indent}    break;")
        lines.append(f"{indent}}}")

        # Mark header and true body as emitted, but NOT false body
        emitted_blocks.add(if_pattern.header_block)
        emitted_blocks.update(if_pattern.true_body)
        emitted_blocks.update(if_pattern.false_body - render_false_body)
        # Mark JMP-to-exit blocks in true body as emitted (they're control flow only)
        for bid in render_true_body:
            blk = cfg.blocks.get(bid)
            if blk and blk.instructions:
                last = blk.instructions[-1]
                if resolver.get_mnemonic(last.opcode) == "JMP":
                    jt = start_to_block.get(last.arg1)
                    if jt in switch_exit_ids:
                        emitted_blocks.add(bid)

        return lines

    elif false_has_break and render_true_body and not true_has_break:
        # False branch ends with break → negate condition and swap
        negated_cond = _negate_condition(render_cond_text)
        lines.append(f"{indent}if ({negated_cond}) {{")

        false_body_sorted = sorted(render_false_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
        if func_loops:
            lines.extend(_render_blocks_with_loops(
                false_body_sorted, indent + "    ", ssa_func, formatter, cfg,
                func_loops, start_to_block, resolver, block_to_if, visited_ifs,
                emitted_blocks, global_map, early_returns
            ))
        else:
            for body_block_id in false_body_sorted:
                if body_block_id in emitted_blocks:
                    continue
                body_block = cfg.blocks.get(body_block_id)
                if body_block:
                    ssa_block = ssa_blocks.get(body_block_id, [])
                    if not _is_control_flow_only(ssa_block, resolver):
                        if SHOW_BLOCK_COMMENTS: lines.append(f"{indent}    // Block {body_block_id} @{body_block.start}")
                    lines.extend(_format_block_lines(
                        ssa_func, body_block_id, indent + "    ", formatter,
                        block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                        early_returns
                    ))

        lines.append(f"{indent}    break;")
        lines.append(f"{indent}}}")

        # Mark header and false body as emitted, but NOT true body
        emitted_blocks.add(if_pattern.header_block)
        emitted_blocks.update(if_pattern.false_body)
        emitted_blocks.update(if_pattern.true_body - render_true_body)
        for bid in render_false_body:
            blk = cfg.blocks.get(bid)
            if blk and blk.instructions:
                last = blk.instructions[-1]
                if resolver.get_mnemonic(last.opcode) == "JMP":
                    jt = start_to_block.get(last.arg1)
                    if jt in switch_exit_ids:
                        emitted_blocks.add(bid)

        return lines

    # Standard if/else rendering (no conditional break)
    # Render if statement
    lines.append(f"{indent}if ({render_cond_text}) {{")

    # Render true branch (recursively)
    true_body_sorted = sorted(render_true_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
    if func_loops:
        lines.extend(_render_blocks_with_loops(
            true_body_sorted,
            indent + "    ",
            ssa_func,
            formatter,
            cfg,
            func_loops,
            start_to_block,
            resolver,
            block_to_if,
            visited_ifs,
            emitted_blocks,
            global_map,
            early_returns
        ))
    else:
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

    # Render false branch if exists (skip if all blocks are control-flow-only)
    def _body_has_content(body_set):
        """Check if any block in body has real statements."""
        if not body_set:
            return False
        for bid in body_set:
            ssa_blk = ssa_func.instructions.get(bid, [])
            if not _is_control_flow_only(ssa_blk, resolver):
                return True
        return False

    if render_false_body and _body_has_content(render_false_body):
        lines.append(f"{indent}}} else {{")

        # Render false branch (recursively)
        false_body_sorted = sorted(render_false_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
        if func_loops:
            lines.extend(_render_blocks_with_loops(
                false_body_sorted,
                indent + "    ",
                ssa_func,
                formatter,
                cfg,
                func_loops,
                start_to_block,
                resolver,
                block_to_if,
                visited_ifs,
                emitted_blocks,
                global_map,
                early_returns
            ))
        else:
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
    early_returns: Optional[Dict[int, tuple]] = None,
    # FIX (01-24): Nested switch support
    block_to_switch: Optional[Dict[int, SwitchPattern]] = None,
    render_switch_callback: Optional[Any] = None,  # Callback to render nested switches
    switch_exit_ids: Optional[Set[int]] = None,
) -> List[str]:
    """
    Render a sequence of blocks with loop detection support.

    Used for rendering switch case bodies where loops may be present.
    Also supports nested switch/case patterns via block_to_switch parameter.

    FIX (01-25): Uses hierarchical block partitioning for nested switches.
    Instead of iterating all case body blocks linearly by address, partitions them into:
    - Pre-nested blocks: Blocks before the nested switch header
    - Nested switch blocks: Delegated entirely to recursive rendering
    - Post-nested blocks: Blocks after the nested switch
    This ensures correct structural order regardless of bytecode address interleaving.
    """
    lines: List[str] = []
    processed_in_loop: Set[int] = set()

    # FIX (01-25): Hierarchical block partitioning for nested switches
    # If there are nested switches, use partitioning to ensure correct rendering order
    if block_to_switch and render_switch_callback:
        # Find ALL nested switch headers in this block set
        block_ids_set = set(block_ids)
        nested_headers_in_scope = [
            bid for bid in block_ids
            if bid in block_to_switch and bid == block_to_switch[bid].header_block
        ]

        if nested_headers_in_scope:
            # Get the first nested switch (by address order)
            first_nested_header = min(nested_headers_in_scope,
                                      key=lambda b: cfg.blocks[b].start if b in cfg.blocks else 0)
            nested_switch = block_to_switch[first_nested_header]

            # Partition blocks around this nested switch
            pre_blocks, post_blocks = _partition_blocks_for_nested_switch(
                block_ids, nested_switch, cfg
            )

            # Build a filtered block_to_switch map excluding this nested switch's blocks
            filtered_block_to_switch = {
                k: v for k, v in block_to_switch.items()
                if k not in nested_switch.all_blocks
            }

            # Render pre-nested blocks (recursive call without this switch)
            if pre_blocks:
                lines.extend(_render_blocks_with_loops(
                    pre_blocks, indent, ssa_func, formatter, cfg, func_loops,
                    start_to_block, resolver, block_to_if, visited_ifs,
                    emitted_blocks, global_map, early_returns,
                    filtered_block_to_switch, render_switch_callback
                ))

            # Render nested switch using the callback
            switch_lines = render_switch_callback(
                nested_switch, indent, block_to_if, visited_ifs, emitted_blocks
            )
            lines.extend(switch_lines)

            # Mark all nested switch blocks as processed
            processed_in_loop.update(nested_switch.all_blocks)

            # Render post-nested blocks (recursive call)
            if post_blocks:
                lines.extend(_render_blocks_with_loops(
                    post_blocks, indent, ssa_func, formatter, cfg, func_loops,
                    start_to_block, resolver, block_to_if, visited_ifs,
                    emitted_blocks, global_map, early_returns,
                    filtered_block_to_switch, render_switch_callback
                ))

            return lines  # Early return - handled via partitioning

    # Track which blocks have for-loops as successors and what variable to skip
    skip_last_assignment: Dict[int, str] = {}  # block_id -> variable_name to skip
    guard_blocks: Set[int] = set()

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
                    if for_info.guard_block is not None:
                        guard_blocks.add(for_info.guard_block)
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

        # FIX (01-24): Check if this block is a nested switch header
        if block_to_switch and body_block_id in block_to_switch:
            nested_switch = block_to_switch[body_block_id]
            if body_block_id == nested_switch.header_block:
                # This is a nested switch header - render it using the callback
                if render_switch_callback:
                    switch_lines = render_switch_callback(
                        nested_switch, indent, block_to_if, visited_ifs, emitted_blocks
                    )
                    lines.extend(switch_lines)
                    # Mark all switch blocks as processed
                    processed_in_loop.update(nested_switch.all_blocks)
                continue  # Skip normal block rendering

        if header_loop:
            # Render loop
            lines.append(f"{indent}// Loop header - Block {body_block_id} @{body_block.start}")

            # Try to detect for-loop pattern (most specific)
            for_info = _detect_for_loop(header_loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map)
            while_info = None
            do_while_info = None

            if for_info:
                lines.append(f"{indent}for ({for_info.var} = {for_info.init}; {for_info.condition}; {for_info.increment}) {{")
                if for_info.guard_block is not None:
                    guard_blocks.add(for_info.guard_block)
            else:
                # Try while-loop pattern
                while_info = _detect_while_loop(header_loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map)
                if while_info:
                    lines.append(f"{indent}while ({while_info.condition}) {{")
                else:
                    # Try do-while pattern
                    do_while_info = _detect_do_while_loop(header_loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map)
                    if do_while_info:
                        lines.append(f"{indent}do {{")
                    else:
                        # Fallback: unrecognized loop pattern
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
                        if any(edge.source == loop_body_id for edge in header_loop.back_edges):
                            skip_var = for_info.var  # Skip increment for loop variable

                    if skip_var:
                        # Filter out increment assignment
                        block_lines = _format_block_lines_filtered(
                            ssa_func, loop_body_id, indent + "    ", formatter, skip_var,
                            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                            early_returns, guard_blocks
                        )
                        lines.extend(block_lines)
                    else:
                        lines.extend(_format_block_lines(
                            ssa_func, loop_body_id, indent + "    ", formatter,
                            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                            early_returns, guard_blocks,
                            func_loops=func_loops, global_map=global_map,
                            switch_exit_ids=switch_exit_ids
                        ))

            # Close loop with appropriate syntax
            if do_while_info:
                lines.append(f"{indent}}} while ({do_while_info.condition});")
            else:
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
                    early_returns, guard_blocks
                )
                lines.extend(block_lines)
            else:
                lines.extend(_format_block_lines(
                    ssa_func, body_block_id, indent, formatter,
                    block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                    early_returns, guard_blocks,
                    func_loops=func_loops, global_map=global_map,
                    switch_exit_ids=switch_exit_ids
                ))

            # DEAD CODE ELIMINATION: Check if block terminates execution
            # If block ends with return, stop rendering remaining blocks (they're unreachable)
            if body_block and body_block.instructions:
                last_instr = body_block.instructions[-1]
                if resolver.is_return(last_instr.opcode):
                    # Stop iteration - all following blocks are unreachable
                    break

    return lines
