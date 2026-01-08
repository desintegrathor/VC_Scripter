"""
Orchestrator for structured function formatting.

This module contains the main entry point functions that coordinate all the
structure analysis, pattern detection, and code emission modules to produce
structured C-like output from decompiled code.
"""

from __future__ import annotations

from typing import Dict, Set, List, Optional

from ..ssa import SSAFunction
from ..expr import ExpressionFormatter
from ..cfg import find_loops_in_function
from ..parenthesization import ExpressionContext, is_simple_expression
from ...disasm import opcodes

# Import from extracted modules
from .utils.helpers import (
    _load_symbol_db,
    _build_start_map,
    _dominates,
    _is_control_flow_only,
    SHOW_BLOCK_COMMENTS,
)
from .patterns.models import SwitchPattern, IfElsePattern
from .patterns.if_else import _detect_if_else_pattern, _detect_early_return_pattern
from .patterns.switch_case import _detect_switch_patterns
from .patterns.loops import _detect_for_loop
from .analysis.variables import _collect_local_variables
from .emit.block_formatter import _format_block_lines
from .emit.code_emitter import _render_blocks_with_loops


def format_structured_function(ssa_func: SSAFunction) -> str:
    """
    Format SSA function as structured C-like code (legacy version).

    This is a simplified legacy function likely deprecated in favor of
    format_structured_function_named. It provides basic structured output
    with simple if/else detection and loop recognition.

    Args:
        ssa_func: SSA function data

    Returns:
        Formatted C-like code as a string
    """
    cfg = ssa_func.cfg
    resolver = getattr(ssa_func.scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    start_to_block = _build_start_map(cfg)
    visited: Set[int] = set()
    lines: List[str] = []
    # Load symbol database for global variable name resolution
    symbol_db = _load_symbol_db()

    # FIX 2: Variable name collision resolution (simplified for legacy function)
    # Note: This function is likely deprecated, main function is format_structured_function_v3
    from ..variable_renaming import VariableRenamer
    all_block_ids = set(cfg.blocks.keys()) if cfg and cfg.blocks else set()
    renamer = VariableRenamer(ssa_func, all_block_ids)
    rename_map = renamer.analyze_and_rename()

    formatter = ExpressionFormatter(ssa_func, symbol_db=symbol_db, rename_map=rename_map)
    ssa_blocks = ssa_func.instructions

    def process(block_id: int, indent: str = "    ") -> None:
        if block_id in visited:
            lines.append(f"{indent}// goto block {block_id}")
            return
        block = cfg.blocks.get(block_id)
        if not block:
            lines.append(f"{indent}// missing block {block_id}")
            return

        visited.add(block_id)
        lines.append(f"{indent}// Block {block_id}")
        lines.extend(_format_block_lines(ssa_func, block_id, indent))

        if not block.instructions:
            return

        last_instr = block.instructions[-1]
        opcode = last_instr.opcode
        if resolver.is_conditional_jump(opcode):
            true_block = start_to_block.get(last_instr.arg1)
            fallthrough_addr = last_instr.address + 1
            false_block = start_to_block.get(fallthrough_addr)
            if (
                true_block is not None
                and false_block is not None
                and len(block.successors) == 2
                and cfg.blocks[true_block].predecessors == {block_id}
                and cfg.blocks[false_block].predecessors == {block_id}
            ):
                cond_text = None
                ssa_block = ssa_blocks.get(block_id, [])
                for ssa_inst in ssa_block:
                    if ssa_inst.address == last_instr.address and ssa_inst.inputs:
                        cond_value = ssa_inst.inputs[0]
                        # FIX 3: Pass IN_CONDITION context
                        cond_expr = formatter.render_value(cond_value, context=ExpressionContext.IN_CONDITION)
                        # If condition renders as just a number, use SSA name instead
                        if cond_expr.lstrip('-').isdigit():
                            cond_expr = cond_value.alias or cond_value.name
                        mnemonic = resolver.get_mnemonic(opcode)
                        # FIX 3: Smart negation
                        if mnemonic == "JZ":
                            if is_simple_expression(cond_expr):
                                cond_text = f"!{cond_expr}"
                            else:
                                cond_text = f"!({cond_expr})"
                        elif mnemonic == "JNZ":
                            cond_text = cond_expr
                        else:
                            cond_text = cond_expr
                        break
                if cond_text is None:
                    cond_text = f"cond_block_{block_id}"
                lines.append(f"{indent}if ({cond_text}) {{")
                process(true_block, indent + "    ")
                lines.append(f"{indent}}} else {{")
                process(false_block, indent + "    ")
                lines.append(f"{indent}}}")
                return

        # Default: follow successors sequentially
        for succ in sorted(block.successors):
            if succ is None:
                continue
            if _dominates(cfg, succ, block_id) and succ != block_id:
                lines.append(f"{indent}while (/* loop to block {succ} */) {{")
                if succ in visited:
                    lines.append(f"{indent}    // loop body already emitted")
                else:
                    process(succ, indent + "    ")
                lines.append(f"{indent}}}")
            else:
                process(succ, indent)

    lines.append("void function_entry(void) {")
    process(cfg.entry_block)
    lines.append("}")
    return "\n".join(lines)


def format_structured_function_named(ssa_func: SSAFunction, func_name: str, entry_addr: int, end_addr: int = None, function_bounds=None) -> str:
    """
    Format structured output for a specific function with custom name and entry point.

    Args:
        ssa_func: SSA function data
        func_name: Name of the function
        entry_addr: Entry address of the function
        end_addr: End address of the function (optional, for linear output mode)
        function_bounds: Optional dict {func_name: (start_addr, end_addr)} for CALL resolution (FÁZE 4)

    Uses per-function ExpressionFormatter with function boundaries for 100% reliable
    structure field detection. This ensures local_0 in different functions correctly
    maps to different structure types.
    """
    cfg = ssa_func.cfg
    resolver = getattr(ssa_func.scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    start_to_block = _build_start_map(cfg)
    lines: List[str] = []
    # Load symbol database for global variable name resolution
    symbol_db = _load_symbol_db()

    # FÁZE 3.3: Detect function signature to get parameter names
    from ..function_signature import detect_function_signature
    func_sig = detect_function_signature(ssa_func, entry_addr, end_addr)

    # Find the entry block for this function
    entry_block = start_to_block.get(entry_addr)
    if entry_block is None:
        return f"// Function {func_name} at {entry_addr} - entry block not found"

    # Find blocks in this function (MOVED UP - needed for VariableRenamer)
    func_block_ids: Set[int] = set()
    for block_id, block in cfg.blocks.items():
        if block.start >= entry_addr:
            if end_addr is None or block.start <= end_addr:
                func_block_ids.add(block_id)

    # FIX 2: Variable name collision resolution
    # Run variable renaming BEFORE creating formatter to detect and resolve collisions
    from ..variable_renaming import VariableRenamer
    renamer = VariableRenamer(ssa_func, func_block_ids)
    rename_map = renamer.analyze_and_rename()

    # Create per-function formatter with function boundaries for accurate structure detection
    # FÁZE 3.3: Pass parameter info for correct aliasing
    # FÁZE 4: Pass function_bounds for CALL resolution
    # FIX 2: Pass rename_map for variable collision resolution
    formatter = ExpressionFormatter(ssa_func, func_start=entry_addr, func_end=end_addr, func_name=func_name, symbol_db=symbol_db, func_signature=func_sig, function_bounds=function_bounds, rename_map=rename_map)
    ssa_blocks = ssa_func.instructions

    # Detect loops in this function using local dominator computation
    func_loops = find_loops_in_function(cfg, func_block_ids, entry_block)

    # Resolve global variables for better naming in for-loop conditions
    from ..global_resolver import resolve_globals
    global_map = resolve_globals(ssa_func)

    # Detect switch/case patterns
    switch_patterns = _detect_switch_patterns(ssa_func, func_block_ids, formatter, start_to_block)

    # Build map: block_id -> switch pattern (for quick lookup)
    block_to_switch: Dict[int, SwitchPattern] = {}
    for switch in switch_patterns:
        for block_id in switch.all_blocks:
            block_to_switch[block_id] = switch

    # FÁZE 2A: Removed if/else pre-detection - now done during rendering
    # This allows detection to work correctly after switch emission modifies CFG structure
    block_to_if: Dict[int, IfElsePattern] = {}  # Will be populated during rendering
    visited_ifs: Set[int] = set()               # Track visited if patterns

    # Track which loop headers we've seen
    emitted_loop_headers: Set[int] = set()

    # Determine function signature using bytecode analysis
    from ..function_signature import get_function_signature_string
    scr = ssa_func.scr

    # Get complete signature (handles both entry points and internal functions)
    signature = get_function_signature_string(
        ssa_func,
        func_name,
        entry_addr,
        end_addr,
        scr_header_enter_size=scr.header.enter_size
    )

    lines.append(f"{signature} {{")

    # Collect local variable declarations
    local_vars = _collect_local_variables(ssa_func, func_block_ids, formatter)
    if local_vars:
        for var_decl in sorted(local_vars):
            lines.append(f"    {var_decl};")
        lines.append("")  # Empty line after declarations

    # Linear output mode: output all blocks in address range
    func_blocks = []
    for block_id, block in cfg.blocks.items():
        if block.start >= entry_addr:
            if end_addr is None or block.start <= end_addr:
                func_blocks.append((block.start, block_id, block))

    # Sort by address
    func_blocks.sort(key=lambda x: x[0])

    # Track active loops (stack for nesting)
    active_loops = []

    # Find which loops each block belongs to (for proper scope tracking)
    block_to_loops: Dict[int, List] = {}
    for block_id in func_block_ids:
        block_to_loops[block_id] = [l for l in func_loops if block_id in l.body]
        # Sort by size (smallest/innermost first)
        block_to_loops[block_id].sort(key=lambda l: len(l.body))

    emitted_switches: Set[int] = set()  # Track which switches we've rendered
    emitted_ifs: Set[int] = set()       # Track which if/else patterns we've rendered
    emitted_blocks: Set[int] = set()    # Track all blocks we've rendered

    for idx, (addr, block_id, block) in enumerate(func_blocks):
        # Skip blocks that have already been rendered
        if block_id in emitted_blocks:
            continue

        # Skip blocks that are part of a switch pattern (except header)
        if block_id in block_to_switch:
            switch = block_to_switch[block_id]
            # If this is not the header, and we've already emitted the switch, skip it
            if block_id != switch.header_block and switch.header_block in emitted_switches:
                continue
            # If this is a switch block but not the header, skip for now
            if block_id != switch.header_block:
                continue

        # FÁZE 2B: Runtime if/else detection (moved from pre-processing)
        # Try to detect if/else pattern if not already known and not part of switch
        # NEW: Pass ssa_func and formatter for compound condition detection
        if block_id not in block_to_if and block_id not in block_to_switch:
            if_pattern = _detect_if_else_pattern(cfg, block_id, start_to_block, resolver, visited_ifs, func_loops, ssa_func=ssa_func, formatter=formatter)
            if if_pattern:
                # Register this pattern
                block_to_if[if_pattern.header_block] = if_pattern
                for body_block_id in if_pattern.true_body:
                    if body_block_id not in block_to_if:
                        block_to_if[body_block_id] = if_pattern
                for body_block_id in if_pattern.false_body:
                    if body_block_id not in block_to_if:
                        block_to_if[body_block_id] = if_pattern

        # Skip blocks that are part of an if/else pattern (except header)
        if block_id in block_to_if:
            if_pattern = block_to_if[block_id]
            # If this is not the header, and we've already emitted the if, skip it
            if block_id != if_pattern.header_block and if_pattern.header_block in emitted_ifs:
                continue
            # If this is an if body block but not the header, skip for now
            if block_id != if_pattern.header_block:
                continue

        # Check if we need to close any loops (block is not in their body)
        loops_to_close = []
        for loop in active_loops:
            if block_id not in loop.body:
                loops_to_close.append(loop)
        for loop in loops_to_close:
            active_loops.remove(loop)
            indent = "    " + "    " * len(active_loops)
            lines.append(f"{indent}}}")

        # Check if this is a switch header
        if block_id in block_to_switch and block_id == block_to_switch[block_id].header_block:
            switch = block_to_switch[block_id]
            base_indent = "    " + "    " * len(active_loops)

            # Render switch statement
            lines.append(f"{base_indent}switch ({switch.test_var}) {{")
            for case in switch.cases:
                lines.append(f"{base_indent}case {case.value}:")
                # Render all blocks in case body (sorted by address) with loop support
                case_body_sorted = sorted(case.body_blocks, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
                case_start_line = len(lines)  # Track where case body starts

                # FÁZE 3: Detect if/else patterns in case body BEFORE rendering
                # FÁZE 3.2 FIX: Pass func_loops to avoid misdetecting loop headers
                # BUG FIX #4: Build stop blocks from other cases to prevent if/else from crossing case boundaries
                case_stop_blocks = set()
                for other_case in switch.cases:
                    if other_case.value != case.value:
                        case_stop_blocks.update(other_case.body_blocks)
                if switch.default_body_blocks:
                    case_stop_blocks.update(switch.default_body_blocks)
                if switch.exit_block:
                    case_stop_blocks.add(switch.exit_block)

                # NEW FIX: Detect compound conditions FIRST (highest priority)
                # Then detect early returns, but skip blocks that are part of compound patterns
                compound_blocks = set()  # Blocks involved in compound conditions

                for body_block_id in case_body_sorted:
                    if body_block_id not in block_to_if:
                        temp_visited = set()
                        # Try compound detection first
                        if_pattern = _detect_if_else_pattern(cfg, body_block_id, start_to_block, resolver, temp_visited, func_loops, context_stop_blocks=case_stop_blocks, ssa_func=ssa_func, formatter=formatter)
                        if if_pattern and hasattr(if_pattern, 'compound'):
                            # Compound pattern detected - mark all involved blocks
                            compound_blocks.update(if_pattern.compound.involved_blocks)
                            block_to_if[body_block_id] = if_pattern

                # FÁZE 1.3: Detect early return/break patterns AFTER compound detection
                # Skip blocks that are part of compound patterns
                early_returns: Dict[int, tuple] = {}
                for body_block_id in case_body_sorted:
                    if body_block_id not in compound_blocks:
                        early_ret = _detect_early_return_pattern(cfg, body_block_id, start_to_block, resolver, switch.exit_block)
                        if early_ret:
                            early_returns[body_block_id] = early_ret

                # Now detect regular if/else patterns (not compound, not early return)
                for body_block_id in case_body_sorted:
                    if body_block_id not in block_to_if and body_block_id not in early_returns:
                        temp_visited = set()
                        # Regular if/else detection (compound already done above)
                        if_pattern = _detect_if_else_pattern(cfg, body_block_id, start_to_block, resolver, temp_visited, func_loops, context_stop_blocks=case_stop_blocks, ssa_func=ssa_func, formatter=formatter)
                        if if_pattern:
                            block_to_if[body_block_id] = if_pattern

                # FIX 3A: Use _render_blocks_with_loops to support loops in case bodies
                # FÁZE 1.3: Pass early_returns for early return/break detection
                case_lines = _render_blocks_with_loops(
                    case_body_sorted,
                    base_indent + "    ",
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
                )
                lines.extend(case_lines)

                # Check if last line is a return statement - if so, don't add break
                has_return = False
                for i in range(len(lines) - 1, case_start_line - 1, -1):
                    line = lines[i].strip()
                    if line and not line.startswith("//"):  # Skip empty lines and comments
                        if line.startswith("return"):
                            has_return = True
                        break

                if case.has_break and not has_return:
                    lines.append(f"{base_indent}    break;")
            if switch.default_block is not None and switch.default_body_blocks:
                lines.append(f"{base_indent}default:")
                # Render all blocks in default body (sorted by address) with loop support
                default_body_sorted = sorted(switch.default_body_blocks, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)

                # FÁZE 3: Detect if/else patterns in default body BEFORE rendering
                # FÁZE 3.2 FIX: Pass func_loops to avoid misdetecting loop headers
                for body_block_id in default_body_sorted:
                    if body_block_id not in block_to_if:
                        temp_visited = set()
                        # FIX: Pass ssa_func and formatter for compound condition detection
                        if_pattern = _detect_if_else_pattern(cfg, body_block_id, start_to_block, resolver, temp_visited, func_loops, ssa_func=ssa_func, formatter=formatter)
                        if if_pattern:
                            block_to_if[body_block_id] = if_pattern

                # FIX 3A: Use _render_blocks_with_loops to support loops in default body
                default_lines = _render_blocks_with_loops(
                    default_body_sorted,
                    base_indent + "    ",
                    ssa_func,
                    formatter,
                    cfg,
                    func_loops,
                    start_to_block,
                    resolver,
                    block_to_if,
                    visited_ifs,
                    emitted_blocks,
                    global_map
                )
                lines.extend(default_lines)
            lines.append(f"{base_indent}}}")
            emitted_switches.add(block_id)

            # FIX 1A: Mark all switch blocks as emitted to prevent re-rendering
            emitted_blocks.update(switch.all_blocks)
            if switch.exit_block is not None:
                emitted_blocks.add(switch.exit_block)

            # FIX 3C: Skip next block if it's unreachable connector after switch
            if idx + 1 < len(func_blocks):
                next_addr, next_block_id, next_block = func_blocks[idx + 1]
                next_block_obj = cfg.blocks.get(next_block_id)
                next_ssa_block = ssa_blocks.get(next_block_id, [])

                # If next block is just a connector (no statements, only control flow)
                if next_block_obj and _is_control_flow_only(next_ssa_block, resolver):
                    # Check if it's jumping to already-emitted block
                    if next_block_obj.instructions:
                        last = next_block_obj.instructions[-1]
                        if resolver.is_jump(last.opcode):
                            target = start_to_block.get(last.arg1, -1)
                            if target in emitted_blocks:
                                # Skip this connector block
                                emitted_blocks.add(next_block_id)

            continue

        # Check if this is an if/else header
        if block_id in block_to_if and block_id == block_to_if[block_id].header_block:
            if_pattern = block_to_if[block_id]
            base_indent = "    " + "    " * len(active_loops)

            # Get condition from SSA
            cond_text = None
            ssa_block = ssa_blocks.get(block_id, [])
            block_obj = cfg.blocks[block_id]
            if block_obj.instructions:
                last_instr = block_obj.instructions[-1]
                mnemonic = resolver.get_mnemonic(last_instr.opcode)
                for ssa_inst in ssa_block:
                    if ssa_inst.address == last_instr.address and ssa_inst.inputs:
                        cond_value = ssa_inst.inputs[0]
                        # FIX 3: Pass IN_CONDITION context to avoid redundant parentheses
                        cond_expr = formatter.render_value(cond_value, context=ExpressionContext.IN_CONDITION)
                        # Only use SSA name if rendered as pure number
                        if cond_expr.lstrip('-').isdigit():
                            alias = cond_value.alias or cond_value.name
                            if alias and not alias.startswith("data_"):
                                cond_expr = alias

                        # FIX 3: Smart negation - only add parens if needed
                        if mnemonic == "JZ":
                            # JZ means "jump if zero" = jump if false, so negate condition
                            if is_simple_expression(cond_expr):
                                cond_text = f"!{cond_expr}"
                            else:
                                cond_text = f"!({cond_expr})"
                        elif mnemonic == "JNZ":
                            # JNZ means "jump if not zero" = jump if true, use as-is
                            cond_text = cond_expr
                        else:
                            cond_text = cond_expr
                        break
            if cond_text is None:
                cond_text = f"cond_{block_id}"

            # Render header block (without the conditional jump)
            if SHOW_BLOCK_COMMENTS: lines.append(f"{base_indent}// Block {block_id} @{block_obj.start}")
            # Format block but exclude last instruction (conditional jump)
            # FIX 3B: Disable recursion for header - pass None for recursive params
            header_lines = _format_block_lines(
                ssa_func, block_id, base_indent, formatter,
                None, None, None, None, None, None
            )
            # Remove last line if it's the conditional jump
            if header_lines and ("goto" in header_lines[-1] or "if (" in header_lines[-1]):
                header_lines = header_lines[:-1]
            lines.extend(header_lines)

            # Render if statement
            lines.append(f"{base_indent}if ({cond_text}) {{")

            # Render true branch
            true_body_sorted = sorted(if_pattern.true_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
            for body_block_id in true_body_sorted:
                body_block = cfg.blocks.get(body_block_id)
                if body_block:
                    # FIX 3C: Only add comment if block has actual statements
                    ssa_block = ssa_blocks.get(body_block_id, [])
                    if not _is_control_flow_only(ssa_block, resolver):
                        if SHOW_BLOCK_COMMENTS: lines.append(f"{base_indent}    // Block {body_block_id} @{body_block.start}")
                    # FIX 3B: Pass recursive params for nested if/else detection
                    lines.extend(_format_block_lines(
                        ssa_func, body_block_id, base_indent + "    ", formatter,
                        block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver
                    ))

            # Check if false branch is non-empty
            if if_pattern.false_body:
                lines.append(f"{base_indent}}} else {{")

                # Render false branch
                false_body_sorted = sorted(if_pattern.false_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
                for body_block_id in false_body_sorted:
                    body_block = cfg.blocks.get(body_block_id)
                    if body_block:
                        # FIX 3C: Only add comment if block has actual statements
                        ssa_block = ssa_blocks.get(body_block_id, [])
                        if not _is_control_flow_only(ssa_block, resolver):
                            if SHOW_BLOCK_COMMENTS: lines.append(f"{base_indent}    // Block {body_block_id} @{body_block.start}")
                        # FIX 3B: Pass recursive params for nested if/else detection
                        lines.extend(_format_block_lines(
                            ssa_func, body_block_id, base_indent + "    ", formatter,
                            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver
                        ))

            lines.append(f"{base_indent}}}")
            emitted_ifs.add(block_id)
            # Mark all blocks as emitted
            emitted_blocks.add(block_id)  # Header
            emitted_blocks.update(if_pattern.true_body)  # True branch
            emitted_blocks.update(if_pattern.false_body)  # False branch
            continue

        # Check if this block is a loop header we haven't opened yet
        header_loop = None
        for loop in func_loops:
            if loop.header == block_id and block_id not in emitted_loop_headers:
                header_loop = loop
                break

        if header_loop:
            emitted_loop_headers.add(block_id)  # Track by header ID, not loop object
            active_loops.append(header_loop)
            indent = "    " + "    " * (len(active_loops) - 1)
            lines.append(f"{indent}// Loop header - Block {block_id} @{addr}")

            # FIX 3A: Try to detect for-loop pattern
            for_info = _detect_for_loop(header_loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map)
            if for_info:
                lines.append(f"{indent}for ({for_info.var} = {for_info.init}; {for_info.condition}; {for_info.increment}) {{")
            else:
                lines.append(f"{indent}while (true) {{  // loop body: blocks {sorted(header_loop.body)}")

        # Calculate current indentation based on active loops
        base_indent = "    " + "    " * len(active_loops)

        # FIX 3C: Only add comment if block has actual statements
        ssa_block = ssa_blocks.get(block_id, [])
        if not _is_control_flow_only(ssa_block, resolver):
            if SHOW_BLOCK_COMMENTS: lines.append(f"{base_indent}// Block {block_id} @{addr}")
        # FIX 3B: Pass recursive params for nested if/else detection
        lines.extend(_format_block_lines(
            ssa_func, block_id, base_indent, formatter,
            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver
        ))

        if block.instructions:
            last_instr = block.instructions[-1]
            opcode = last_instr.opcode
            mnemonic = resolver.get_mnemonic(opcode)

            # Show control flow
            # NOTE: RET is now handled in expr.py, so we don't add extra return here
            if False and resolver.is_return(opcode):
                lines.append(f"{base_indent}return;")
            elif resolver.is_jump(opcode):
                target = last_instr.arg1
                target_block = start_to_block.get(target, -1)

                # FIX 1B: Skip goto if jumping into a switch that will be rendered next
                # This handles both direct header jumps AND jumps to first case block
                is_switch_header_jump = False
                if target_block in block_to_switch:
                    target_switch = block_to_switch[target_block]

                    # Check if the switch header will be rendered next
                    # (target might be header itself OR a case block within the switch)
                    if idx + 1 < len(func_blocks):
                        next_addr, next_block_id, next_block = func_blocks[idx + 1]

                        # If next block is the switch header, skip goto
                        if next_block_id == target_switch.header_block:
                            is_switch_header_jump = True

                # Import flow analysis functions
                from .analysis.flow import _get_loop_for_block, _is_back_edge_target

                # Check if this is a back edge (continue) or loop exit (break)
                is_back_edge = _is_back_edge_target(cfg, block_id, target_block, func_loops)
                containing_loop = _get_loop_for_block(block_id, func_loops)
                is_loop_exit = (containing_loop and
                               target_block not in containing_loop.body and
                               target_block in containing_loop.exits)

                if resolver.is_conditional_jump(opcode):
                    # Get condition from SSA
                    cond_text = None
                    ssa_block = ssa_blocks.get(block_id, [])
                    for ssa_inst in ssa_block:
                        if ssa_inst.address == last_instr.address and ssa_inst.inputs:
                            cond_value = ssa_inst.inputs[0]
                            # FIX 3: Pass IN_CONDITION context
                            cond_expr = formatter.render_value(cond_value, context=ExpressionContext.IN_CONDITION)
                            # Only use SSA name if rendered as pure number AND has meaningful alias
                            # Skip data_ aliases as they should be resolved to actual values
                            if cond_expr.lstrip('-').isdigit():
                                alias = cond_value.alias or cond_value.name
                                # Keep numeric value for data_ references (already resolved)
                                # Use alias only for local_/param_ variables
                                if alias and not alias.startswith("data_"):
                                    cond_expr = alias
                            # FIX 3: Smart negation
                            if mnemonic == "JZ":
                                if is_simple_expression(cond_expr):
                                    cond_text = f"!{cond_expr}"
                                else:
                                    cond_text = f"!({cond_expr})"
                            elif mnemonic == "JNZ":
                                cond_text = cond_expr
                            else:
                                cond_text = cond_expr
                            break
                    if cond_text is None:
                        cond_text = f"cond_{block_id}"

                    # FIX 1B: Skip rendering if jumping to switch header
                    if not is_switch_header_jump:
                        if is_back_edge:
                            lines.append(f"{base_indent}if ({cond_text}) continue;  // back to loop header @{target}")
                        elif is_loop_exit:
                            lines.append(f"{base_indent}if ({cond_text}) break;  // exit loop @{target}")
                        else:
                            lines.append(f"{base_indent}if ({cond_text}) goto block_{target_block}; // @{target}")
                else:
                    # Unconditional jump
                    # FIX 1B: Skip rendering if jumping to switch header
                    if not is_switch_header_jump:
                        # FIX 3C: Skip goto if target is already emitted (unreachable code)
                        if target_block not in emitted_blocks:
                            if is_back_edge:
                                lines.append(f"{base_indent}continue;  // back to loop header @{target}")
                            elif is_loop_exit:
                                lines.append(f"{base_indent}break;  // exit loop @{target}")
                            else:
                                lines.append(f"{base_indent}goto block_{target_block}; // @{target}")

    # Close any remaining active loops
    while active_loops:
        active_loops.pop()
        indent = "    " + "    " * len(active_loops)
        lines.append(f"{indent}}}")

    lines.append("}")
    return "\n".join(lines)
