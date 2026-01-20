"""
Orchestrator for structured function formatting.

This module contains the main entry point functions that coordinate all the
structure analysis, pattern detection, and code emission modules to produce
structured C-like output from decompiled code.
"""

from __future__ import annotations

from typing import Dict, Set, List, Optional
import logging
import sys

from ..ssa import SSAFunction
from ..expr import ExpressionFormatter
from ..cfg import find_loops_in_function
from ..parenthesization import ExpressionContext, is_simple_expression
from ...disasm import opcodes
from ..type_inference import TypeInferenceEngine

logger = logging.getLogger(__name__)

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


def _find_reachable_blocks(cfg, entry_block: int) -> Set[int]:
    """
    Find all blocks reachable from entry_block using DFS.

    This function performs a depth-first search to identify all blocks
    that can be reached from the entry point, filtering out dead code
    that appears after returns or unconditional jumps.

    Args:
        cfg: Control flow graph
        entry_block: Entry block ID

    Returns:
        Set of reachable block IDs
    """
    reachable = set()
    stack = [entry_block]

    while stack:
        block_id = stack.pop()
        if block_id in reachable:
            continue

        reachable.add(block_id)

        # Add successors
        block = cfg.blocks.get(block_id)
        if block:
            for succ in block.successors:
                if succ not in reachable:
                    stack.append(succ)

    return reachable


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
    func_sig = detect_function_signature(ssa_func, entry_addr, end_addr, func_name=func_name)

    # Find the entry block for this function
    # For negative entry addresses (e.g., ScriptMain at -1098), use CFG's resolved entry_block
    if entry_addr < 0:
        entry_block = cfg.entry_block
    else:
        entry_block = start_to_block.get(entry_addr)
        if entry_block is None:
            return f"// Function {func_name} at {entry_addr} - entry block not found"

    # Find blocks in this function (MOVED UP - needed for VariableRenamer)
    func_block_ids: Set[int] = set()
    for block_id, block in cfg.blocks.items():
        if block.start >= entry_addr:
            if end_addr is None or block.start <= end_addr:
                func_block_ids.add(block_id)

    # Filter out unreachable blocks (dead code elimination)
    reachable_blocks = _find_reachable_blocks(cfg, entry_block)
    func_block_ids = func_block_ids & reachable_blocks

    import sys
    print(f"DEBUG: {func_name} entry={entry_addr} end={end_addr} blocks={len(func_block_ids)}", file=sys.stderr)

    logger.debug(f"{func_name}: {len(func_block_ids)} reachable blocks (out of {len([b for b in cfg.blocks.values() if entry_addr <= b.start <= (end_addr or float('inf'))])})")

    # FIX 2: Variable name collision resolution
    # Run variable renaming BEFORE creating formatter to detect and resolve collisions
    from ..variable_renaming import VariableRenamer
    renamer = VariableRenamer(ssa_func, func_block_ids)
    rename_map = renamer.analyze_and_rename()

    # SSA LOWERING: Collapse versioned SSA variables to unversioned C variables
    # This transforms rename_map: {"t100_0": "sideA", "t200_0": "sideB"} → {"t100_0": "side", "t200_0": "side"}
    from ..ssa_lowering import SSALowerer
    lowerer = SSALowerer(
        rename_map=rename_map,
        variable_versions=renamer.variable_versions,
        cfg=cfg,
        ssa_func=ssa_func,
        loops=[]  # Will be populated with func_loops after loop detection
    )
    lowering_result = lowerer.lower()

    # Use lowered rename_map for expression formatting
    rename_map = lowering_result.lowered_rename_map

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
    print(f"DEBUG ORCHESTRATOR: _detect_switch_patterns returned {len(switch_patterns)} switches", file=sys.stderr)
    for i, sw in enumerate(switch_patterns):
        print(f"DEBUG ORCHESTRATOR: Switch {i}: {sw.test_var} with {len(sw.cases)} cases, header_block={sw.header_block}", file=sys.stderr)

    # Build map: block_id -> switch pattern (for quick lookup)
    block_to_switch: Dict[int, SwitchPattern] = {}
    for switch in switch_patterns:
        print(f"DEBUG ORCHESTRATOR: Adding switch {switch.test_var} to map, all_blocks={switch.all_blocks}", file=sys.stderr)
        for block_id in switch.all_blocks:
            block_to_switch[block_id] = switch
    print(f"DEBUG ORCHESTRATOR: block_to_switch contains {len(block_to_switch)} entries", file=sys.stderr)

    # FÁZE 2A: Removed if/else pre-detection - now done during rendering
    # This allows detection to work correctly after switch emission modifies CFG structure
    block_to_if: Dict[int, IfElsePattern] = {}  # Will be populated during rendering
    visited_ifs: Set[int] = set()               # Track visited if patterns

    # Track which loop headers we've seen
    emitted_loop_headers: Set[int] = set()

    # FIX (07-02): Run type inference BEFORE variable collection and signature generation
    # This refines SSA value.value_type fields with dataflow analysis, enabling
    # accurate type declarations (float/int/struct) instead of generic "dword"
    # ENHANCEMENT (07-06a): Also used for parameter type inference in function signatures
    type_engine = None
    try:
        type_engine = TypeInferenceEngine(ssa_func, aggressive=True)
        type_engine.integrate_with_ssa_values()
        logger.info(f"Type inference completed for {func_name}")
    except Exception as e:
        logger.warning(f"Type inference failed for {func_name}: {e}. Continuing with SSA initial types.")

    # Determine function signature using bytecode analysis and type inference
    from ..function_signature import get_function_signature_string
    scr = ssa_func.scr

    # Get complete signature (handles both entry points and internal functions)
    # BUGFIX (07-ERROR6): Disable type_engine for signatures when using build_ssa_all_blocks()
    # TypeInferenceEngine.infer_parameter_types() assumes entry_block=0, which is wrong
    # when SSAFunction contains multiple functions. Use bytecode-based detection instead.
    signature = get_function_signature_string(
        ssa_func,
        func_name,
        entry_addr,
        end_addr,
        scr_header_enter_size=scr.header.enter_size,
        type_engine=None  # Disable type inference for signatures - use bytecode detection
    )

    lines.append(f"{signature} {{")

    # Use SSA lowering variable declarations
    # These are already de-duplicated and properly typed
    local_vars = []
    lowered_var_names = set()
    for var_type, var_name in lowering_result.variable_declarations:
        # FIX: Handle array types correctly (e.g., "s_SC_MP_EnumPlayers[64]")
        # Array syntax should be after variable name: "s_SC_MP_EnumPlayers local_296[64]"
        if "[" in var_type:
            base_type = var_type[:var_type.index("[")]
            array_part = var_type[var_type.index("["):]
            local_vars.append(f"{base_type} {var_name}{array_part}")
        else:
            local_vars.append(f"{var_type} {var_name}")
        lowered_var_names.add(var_name)

    # Also collect array declarations and struct types from old system
    # (TODO: Merge this logic into SSA lowering)
    # FIX (06-05): Pattern 5 - Remove overly restrictive filter that excluded simple struct types
    # The old filter only kept arrays ([) and "complex types" (multiple spaces), which excluded
    # single-word struct types like "c_Vector3 vec" (only one space).
    # This caused declarations generated by _collect_local_variables to be lost during emission.
    old_vars = _collect_local_variables(ssa_func, func_block_ids, formatter)
    for var_decl in old_vars:
        # Extract variable name from declaration for duplicate check
        parts = var_decl.split()
        if len(parts) >= 2:
            # Get last part (variable name), strip array brackets if present
            var_name = parts[-1].split('[')[0]

            # BUGFIX: If this variable was already declared by lowering, but the old system
            # has better type info (struct types, arrays, pointers), REPLACE the lowering declaration
            if var_name in lowered_var_names:
                # Check if this declaration has better type info than the lowered one
                # Better = has struct type (s_SC_), array syntax ([), pointer type (*), or dword (handle type)
                # Also check for specific SDK types like ushort* from SC_Wtxt
                # FIX (01-20): Added "void*" and "dword" as better types - used for pointer/handle types in Vietcong scripting
                has_better_type = (var_decl.startswith("s_SC_") or
                                   var_decl.startswith("c_") or
                                   var_decl.startswith("dword ") or
                                   var_decl.startswith("void* ") or
                                   var_decl.startswith("void *") or
                                   "[" in var_decl or
                                   "*" in var_decl)
                if has_better_type:
                    # Remove the lowered declaration and add this better one
                    lowered_decl = None
                    for i, decl in enumerate(local_vars):
                        # Extract variable name from existing declaration for precise matching
                        decl_parts = decl.split()
                        if len(decl_parts) >= 2:
                            decl_var = decl_parts[-1].split('[')[0]  # Handle arrays
                            if decl_var == var_name:
                                lowered_decl = decl
                                local_vars[i] = var_decl
                                break
                    if lowered_decl:
                        continue
                else:
                    # Keep the lowered declaration, skip this one
                    continue

        local_vars.append(var_decl)

    if local_vars:
        for var_decl in sorted(set(local_vars)):  # De-duplicate
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
    goto_targets: Set[int] = set()      # Track blocks referenced by goto statements (Pattern 1 fix)

    for idx, (addr, block_id, block) in enumerate(func_blocks):
        # Skip blocks that have already been rendered (unless they're goto targets - Pattern 1 fix)
        # If a block is a goto target, we need to emit its label even if it was "emitted" by pattern detection
        if block_id in emitted_blocks and block_id not in goto_targets:
            continue

        # ORPHANED BLOCK VALIDATION: Check if block is unreachable (no predecessors)
        # This prevents rendering unreachable code after return statements
        if block_id != entry_block:
            # Get predecessors that are in the current function
            predecessors = [p for p in cfg.blocks[block_id].predecessors if p in func_block_ids]
            if not predecessors:
                logger.debug(
                    f"Skipping orphaned block {block_id} at address {addr} "
                    f"in function {func_name} - no predecessors (unreachable code)"
                )
                continue

        # Skip blocks that are part of a switch pattern (except header)
        if block_id in block_to_switch:
            switch = block_to_switch[block_id]
            # Only skip non-header blocks if the switch has already been emitted
            if block_id != switch.header_block and switch.header_block in emitted_switches:
                continue
            # CHANGED: Allow if/else detection inside switch case bodies
            # Only skip if this is the switch header itself (which will be rendered as switch/case)
            if block_id == switch.header_block:
                # Skip if/else detection for switch headers (they're rendered as switch statements)
                pass  # Will be handled by switch rendering below
            # For non-header blocks (case bodies), allow if/else detection

        # FÁZE 2B: Runtime if/else detection (moved from pre-processing)
        # Try to detect if/else pattern if not already known
        # NEW: Pass ssa_func and formatter for compound condition detection
        # CHANGED: Removed "and block_id not in block_to_switch" to allow nested if/else inside cases
        is_switch_header = block_id in block_to_switch and block_to_switch[block_id].header_block == block_id
        if block_id not in block_to_if and not is_switch_header:
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
        if block_id in block_to_switch:
            sw = block_to_switch[block_id]
            print(f"DEBUG ORCHESTRATOR: Block {block_id} is in block_to_switch, header_block={sw.header_block}, is_header={block_id == sw.header_block}", file=sys.stderr)
        if block_id in block_to_switch and block_id == block_to_switch[block_id].header_block:
            switch = block_to_switch[block_id]
            base_indent = "    " + "    " * len(active_loops)

            # Pattern 1 fix: Emit label for goto targets before switch rendering
            if block_id in goto_targets:
                # Category 6 fix: Remove meaningless goto if previous line jumps to this label
                if lines and lines[-1].strip().startswith(f"goto block_{block_id};"):
                    lines.pop()  # Remove the meaningless goto
                lines.append(f"{base_indent}block_{block_id}:")

            # Render switch statement
            print(f"DEBUG ORCHESTRATOR: Rendering switch for {switch.test_var} with {len(switch.cases)} cases at block {block_id}", file=sys.stderr)
            switch_line = f"{base_indent}switch ({switch.test_var}) {{"
            lines.append(switch_line)
            print(f"DEBUG ORCHESTRATOR: Appended to lines: '{switch_line}'", file=sys.stderr)
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
                # FIX: Ensure default case has at least a break statement if body is empty
                # An empty default: case is a C syntax error
                if not default_lines or all(line.strip() == "" for line in default_lines):
                    lines.append(f"{base_indent}    break;")
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

            # Pattern 1 fix: Emit label for goto targets before if/else rendering
            if block_id in goto_targets:
                # Category 6 fix: Remove meaningless goto if previous line jumps to this label
                if lines and lines[-1].strip().startswith(f"goto block_{block_id};"):
                    lines.pop()  # Remove the meaningless goto
                lines.append(f"{base_indent}block_{block_id}:")

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
            found_return_in_if = False  # Track if we hit a return in if-body
            for body_block_id in true_body_sorted:
                # Skip blocks after return (unreachable code across blocks)
                if found_return_in_if:
                    continue

                body_block = cfg.blocks.get(body_block_id)
                if body_block:
                    # FIX 3C: Only add comment if block has actual statements
                    ssa_block = ssa_blocks.get(body_block_id, [])
                    if not _is_control_flow_only(ssa_block, resolver):
                        if SHOW_BLOCK_COMMENTS: lines.append(f"{base_indent}    // Block {body_block_id} @{body_block.start}")
                    # FIX 3B: Pass recursive params for nested if/else detection
                    block_lines = _format_block_lines(
                        ssa_func, body_block_id, base_indent + "    ", formatter,
                        block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver
                    )
                    lines.extend(block_lines)

                    # Check if this block ended with a return
                    if block_lines and any("return" in line for line in block_lines):
                        found_return_in_if = True

            # Check if false branch is non-empty
            if if_pattern.false_body:
                lines.append(f"{base_indent}}} else {{")

                # Render false branch
                false_body_sorted = sorted(if_pattern.false_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
                found_return_in_else = False  # Track if we hit a return in else-body
                for body_block_id in false_body_sorted:
                    # Skip blocks after return (unreachable code across blocks)
                    if found_return_in_else:
                        continue

                    body_block = cfg.blocks.get(body_block_id)
                    if body_block:
                        # FIX 3C: Only add comment if block has actual statements
                        ssa_block = ssa_blocks.get(body_block_id, [])
                        if not _is_control_flow_only(ssa_block, resolver):
                            if SHOW_BLOCK_COMMENTS: lines.append(f"{base_indent}    // Block {body_block_id} @{body_block.start}")
                        # FIX 3B: Pass recursive params for nested if/else detection
                        block_lines = _format_block_lines(
                            ssa_func, body_block_id, base_indent + "    ", formatter,
                            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver
                        )
                        lines.extend(block_lines)

                        # Check if this block ended with a return
                        if block_lines and any("return" in line for line in block_lines):
                            found_return_in_else = True

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
                lines.append(f"{indent}while (TRUE) {{  // loop body: blocks {sorted(header_loop.body)}")

        # Calculate current indentation based on active loops
        base_indent = "    " + "    " * len(active_loops)

        # Pattern 1 fix: Emit label for goto targets
        if block_id in goto_targets:
            # Category 6 fix: Remove meaningless goto if previous line jumps to this label
            if lines and lines[-1].strip().startswith(f"goto block_{block_id};"):
                lines.pop()  # Remove the meaningless goto
            lines.append(f"{base_indent}block_{block_id}:")

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
                    # FIX (Pattern 1 - 06-02): Skip goto to orphaned blocks (unreachable blocks with no predecessors)
                    # Check if target block exists and is reachable

                    is_orphaned_target = False
                    # Check if target_block is valid (>= 0) and exists in CFG
                    if target_block < 0 or target_block not in cfg.blocks:
                        # Target block doesn't exist - skip goto
                        is_orphaned_target = True
                    elif target_block not in func_block_ids:
                        # Target block is outside this function's scope - skip goto
                        is_orphaned_target = True
                    elif target_block != entry_block:
                        # Check if target block has predecessors (excluding entry block)
                        target_cfg_block = cfg.blocks[target_block]
                        predecessors = [p for p in target_cfg_block.predecessors if p in func_block_ids]
                        if not predecessors:
                            is_orphaned_target = True

                    if not is_switch_header_jump and not is_orphaned_target:
                        if is_back_edge:
                            lines.append(f"{base_indent}if ({cond_text}) continue;  // back to loop header @{target}")
                        elif is_loop_exit:
                            lines.append(f"{base_indent}if ({cond_text}) break;  // exit loop @{target}")
                        else:
                            # Pattern 1 fix: Track this block as a goto target
                            goto_targets.add(target_block)
                            lines.append(f"{base_indent}if ({cond_text}) goto block_{target_block}; // @{target}")
                else:
                    # Unconditional jump
                    # FIX 1B: Skip rendering if jumping to switch header
                    # FIX (Pattern 1 - 06-02): Skip goto to orphaned blocks
                    # Check if target block exists and is reachable

                    is_orphaned_target = False
                    # Check if target_block is valid (>= 0) and exists in CFG
                    if target_block < 0 or target_block not in cfg.blocks:
                        # Target block doesn't exist - skip goto
                        is_orphaned_target = True
                    elif target_block not in func_block_ids:
                        # Target block is outside this function's scope - skip goto
                        is_orphaned_target = True
                    elif target_block != entry_block:
                        # Check if target block has predecessors (excluding entry block)
                        target_cfg_block = cfg.blocks[target_block]
                        predecessors = [p for p in target_cfg_block.predecessors if p in func_block_ids]
                        if not predecessors:
                            is_orphaned_target = True

                    if not is_switch_header_jump and not is_orphaned_target:
                        # FIX 3C: Skip goto if target is already emitted (unreachable code)
                        if target_block not in emitted_blocks:
                            # Check if target is the next block (meaningless goto)
                            is_next_block = False
                            if idx + 1 < len(func_blocks):
                                next_block_id = func_blocks[idx + 1][1]
                                if target_block == next_block_id:
                                    is_next_block = True

                            if is_back_edge:
                                lines.append(f"{base_indent}continue;  // back to loop header @{target}")
                            elif is_loop_exit:
                                lines.append(f"{base_indent}break;  // exit loop @{target}")
                            elif is_next_block:
                                # Skip meaningless goto to next block (Category 6 fix)
                                pass
                            else:
                                # Pattern 1 fix: Track this block as a goto target
                                goto_targets.add(target_block)
                                lines.append(f"{base_indent}goto block_{target_block}; // @{target}")

    # Close any remaining active loops
    while active_loops:
        active_loops.pop()
        indent = "    " + "    " * len(active_loops)
        lines.append(f"{indent}}}")

    # FIX #4: Add return statement if function ends without one
    # Check if there are any RET instructions in exit blocks that weren't emitted
    needs_return = False
    return_value = None

    # Find blocks that end with RET but weren't emitted (e.g., after switch)
    for block_id, block in cfg.blocks.items():
        if block_id in emitted_blocks:
            continue  # Skip already emitted blocks

        if block.instructions:
            last_instr = block.instructions[-1]
            if resolver.is_return(last_instr.opcode):
                needs_return = True

                # Try to extract return value from SSA
                ssa_block = ssa_func.instructions.get(block_id, [])
                for ssa_instr in reversed(ssa_block):
                    if ssa_instr.mnemonic == "RET":
                        # Check if RET has input (return value)
                        if ssa_instr.inputs:
                            return_value = formatter.render_value(ssa_instr.inputs[0])
                        break
                break  # Use first found RET

    # Alternative: Check if last emitted line already has a return
    last_line_has_return = False
    for line in reversed(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("//"):
            if stripped.startswith("return"):
                last_line_has_return = True
            break

    # Add return statement if needed and not already present
    # FIX (06-05): Pattern 3 - Synthesize return values for non-void functions
    # Functions with non-void return type ending with bare "return;" crash SCMP.exe
    if needs_return and not last_line_has_return:
        if return_value:
            lines.append(f"    return {return_value};")
        else:
            # Extract return type from function signature to determine if void
            # Signature format: "returntype funcname(params)"
            return_type = "void"  # Default assumption
            sig_parts = signature.split('(')[0].strip().split()
            if len(sig_parts) >= 2:
                # First part is return type, second is function name
                return_type = sig_parts[0]

            # Synthesize appropriate return value based on type
            if return_type.lower() == 'void':
                lines.append(f"    return;")
            elif 'float' in return_type.lower():
                lines.append(f"    return 0.0f;  // FIX (06-05): Synthesized return value")
            elif 'double' in return_type.lower():
                lines.append(f"    return 0.0;  // FIX (06-05): Synthesized return value")
            elif 'char' in return_type.lower():
                lines.append(f"    return 0;  // FIX (06-05): Synthesized return value")
            else:
                # Default: int or pointer types
                lines.append(f"    return 0;  // FIX (06-05): Synthesized return value")

    # FIX (06-05): Pattern 3 - Post-process to fix bare returns in non-void functions
    # The expr.py module emits "return;" for RET 0 instructions, but doesn't know function signature
    # This post-processing step fixes bare returns based on actual function return type
    return_type_from_sig = "void"  # Extract from signature
    sig_parts = signature.split('(')[0].strip().split()
    if len(sig_parts) >= 2:
        return_type_from_sig = sig_parts[0]

    # Only fix if function is non-void
    if return_type_from_sig.lower() != 'void':
        # Scan all lines and fix bare returns
        for i in range(len(lines)):
            stripped = lines[i].strip()
            if stripped == 'return;':
                # Determine appropriate return value based on type
                if 'float' in return_type_from_sig.lower():
                    lines[i] = lines[i].replace('return;', 'return 0.0f;  // FIX (06-05): Synthesized return value')
                elif 'double' in return_type_from_sig.lower():
                    lines[i] = lines[i].replace('return;', 'return 0.0;  // FIX (06-05): Synthesized return value')
                elif 'char' in return_type_from_sig.lower():
                    lines[i] = lines[i].replace('return;', 'return 0;  // FIX (06-05): Synthesized return value')
                else:
                    # Default: int or pointer types
                    lines[i] = lines[i].replace('return;', 'return 0;  // FIX (06-05): Synthesized return value')

    lines.append("}")

    # PRIORITY 2 FIX: Enhanced undefined variable detection and declaration with type inference
    # This catches edge cases where SSA lowering missed declarations (e.g., undefined temporaries, struct variables)
    import re
    from typing import Set, Dict, Optional, List as ListType, Tuple

    # Helper function to scan all variables used in code
    def _scan_all_variables(lines: ListType[str]) -> Set[str]:
        """Extract ALL variable names used in code."""
        used_vars = set()
        identifier_pattern = re.compile(r'\b([a-zA-Z_]\w*)\b')

        for line in lines:
            # Skip comments and string literals
            code_part = line.split('//')[0]  # Remove line comments
            code_part = re.sub(r'/\*.*?\*/', '', code_part)  # Remove block comments
            # TODO: Could also skip string literals, but less critical

            for match in identifier_pattern.finditer(code_part):
                var_name = match.group(1)
                used_vars.add(var_name)

        return used_vars

    # Helper function to infer struct type from field access patterns
    def _infer_struct_type_from_fields(var_name: str, lines: ListType[str]) -> Optional[str]:
        """Try to determine struct type from field access patterns."""
        # Extract field names accessed on this variable
        field_pattern = re.compile(rf'{re.escape(var_name)}[.-]>?(\w+)')
        fields_accessed = set()

        for line in lines:
            matches = field_pattern.findall(line)
            fields_accessed.update(matches)

        # Match against known struct types based on field names
        # Quick heuristics for common cases
        if 'watchfulness' in fields_accessed or 'zerodist' in fields_accessed or 'watchfulness_zerodist' in fields_accessed:
            return "s_SC_P_AI_props"
        if 'side' in fields_accessed and 'master_nod' in fields_accessed:
            return "s_SC_P_info"
        if fields_accessed and any(f.startswith('field') for f in fields_accessed):
            # Generic struct with fieldN members
            return "dword"

        return None

    # Helper function to infer variable type from usage patterns
    def _infer_type_from_usage(var_name: str, lines: ListType[str]) -> str:
        """Infer variable type from how it's used in code."""

        # Check for struct member access: var.field* or var->field*
        struct_access_pattern = re.compile(rf'\b{re.escape(var_name)}[.-]>?\w+')
        for line in lines:
            if struct_access_pattern.search(line):
                # It's a struct - try to find which one
                struct_type = _infer_struct_type_from_fields(var_name, lines)
                return struct_type if struct_type else "dword"  # Fallback to generic

        # Check for pointer dereference: (*var) or *var
        pointer_deref_pattern = re.compile(rf'\(\*{re.escape(var_name)}\)|\*{re.escape(var_name)}\b')
        for line in lines:
            if pointer_deref_pattern.search(line):
                return "int*"

        # Check for array access: var[index]
        array_access_pattern = re.compile(rf'{re.escape(var_name)}\[')
        for line in lines:
            if array_access_pattern.search(line):
                return "int"  # Array element access implies int type

        # Check for float operations
        float_keywords = ['frnd', 'fabs', 'sqrt', 'sin', 'cos']
        for line in lines:
            if var_name in line:
                for keyword in float_keywords:
                    if keyword in line:
                        return "float"

        # Check for function calls with &var (address-of)
        # Pattern: FunctionName(&var_name) suggests var should be the param type
        address_of_pattern = re.compile(rf'(\w+)\(&{re.escape(var_name)}\b')
        for line in lines:
            match = address_of_pattern.search(line)
            if match:
                func_name = match.group(1)

                # Try to infer type from common SDK function patterns
                if "GetAtgSettings" in func_name:
                    return "s_SC_MP_SRV_AtgSettings"
                elif "GetInfo" in func_name or "P_info" in func_name:
                    return "s_SC_P_info"
                elif "GetSettings" in func_name:
                    return "s_SC_MP_SRV_settings"
                elif "SC_MP_EnumPlayers" in func_name:
                    # First parameter is s_SC_MP_EnumPlayers *list
                    # ASP 256 allocates 256 dwords, struct is 4 dwords each → 64 elements
                    return "s_SC_MP_EnumPlayers[64]"
                # Add more common patterns as needed

        # Default to int
        return "int"

    # Define C keywords and built-in identifiers to skip
    c_keywords = {
        'if', 'else', 'while', 'for', 'return', 'break', 'continue', 'switch', 'case', 'default',
        'int', 'float', 'double', 'void', 'char', 'short', 'long', 'unsigned', 'signed',
        'struct', 'union', 'enum', 'typedef', 'sizeof', 'const', 'static', 'extern',
        'true', 'false', 'TRUE', 'FALSE', 'NULL',
        'dword', 'BOOL', 'byte'
    }

    # Built-in type names that might appear in code
    builtin_types = {
        'c_Vector3', 's_SC_P_info', 's_SC_P_AI_props', 's_SC_OBJ_info', 's_SC_MP_hud',
        's_SC_MP_SRV_settings', 's_SC_L_info', 's_SC_P_Create'
    }

    # 1. Collect already declared variables
    declared_vars = set()

    # Add parameters from function signature
    # Extract parameter names from signature string (e.g., "int func(int param0, float param1)")
    # The signature was already generated earlier, so we parse it from the first line
    if lines and '(' in lines[0]:
        sig_line = lines[0]
        # Extract params between ( and {
        params_start = sig_line.find('(')
        params_end = sig_line.find(')')
        if params_start > 0 and params_end > params_start:
            params_str = sig_line[params_start+1:params_end].strip()
            if params_str and params_str != 'void':
                # Parse "int param0, float param1" or "s_SC_OBJ_info *info"
                param_parts = params_str.split(',')
                for param_part in param_parts:
                    # Each part is "type name", take the last word as name
                    # Handle pointers: "s_SC_OBJ_info *info" -> "info"
                    words = param_part.strip().split()
                    if words:
                        param_name = words[-1]
                        # Strip pointer prefix if present
                        param_name = param_name.lstrip('*')
                        # Handle array params like "int arr[]" - strip brackets
                        param_name = param_name.split('[')[0]
                        declared_vars.add(param_name)

    # Add variables from SSA lowering
    for var_type, var_name in lowering_result.variable_declarations:
        clean_name = var_name.lstrip('&')  # Remove & prefix if present
        declared_vars.add(clean_name)

    # Scan lines for existing declarations (type keyword followed by identifier)
    type_keywords = {'int', 'float', 'double', 'void', 'char', 'short', 'long', 'dword', 'BOOL', 'byte', 'ushort'}
    for line in lines:
        # Match patterns like "int foo;", "c_Vector3 bar;", or "ushort* ptr;"
        # BUGFIX: Added \*?\s* to handle pointer types like "ushort* t2881_ret;"
        decl_match = re.search(r'\b(\w+)\*?\s+\*?([a-zA-Z_]\w*)\s*[;=\[]', line)
        if decl_match:
            type_name = decl_match.group(1)
            var_name = decl_match.group(2)
            if type_name in type_keywords or type_name.startswith('s_') or type_name.startswith('c_'):
                declared_vars.add(var_name)

    # 2. Scan for all used variables
    used_vars = _scan_all_variables(lines)

    # 3. Filter to find undefined variables
    undefined_vars = set()
    for var_name in used_vars:
        # Skip if already declared
        if var_name in declared_vars:
            continue

        # Skip C keywords and built-in types
        if var_name in c_keywords or var_name in builtin_types:
            continue

        # Skip function names (SC_*, func_*)
        if var_name.startswith('SC_') or var_name.startswith('func_'):
            continue

        # Skip constants and macros (all caps, optionally with underscores)
        if var_name.isupper():
            continue

        # Skip type names (s_*, c_*)
        if var_name.startswith('s_') or var_name.startswith('c_'):
            continue

        # Skip global variables (gVarname pattern - 'g' followed by uppercase letter)
        # These are already declared at file scope, don't shadow them locally
        if len(var_name) >= 2 and var_name[0] == 'g' and var_name[1].isupper():
            continue

        # Now check if this variable SHOULD be declared
        # Include all remaining identifiers that aren't obviously constants/types
        needs_declaration = False

        # Pattern 1: local_X (stack variables)
        if var_name.startswith('local_'):
            needs_declaration = True

        # Pattern 2: tXXX_X (SSA temporaries)
        elif var_name.startswith('t') and '_' in var_name and var_name[1:].split('_')[0].isdigit():
            needs_declaration = True

        # Pattern 3: Single letter variables (i, j, k, tmp, etc.)
        elif len(var_name) == 1 and var_name in 'ijklmnxyz':
            needs_declaration = True

        # Pattern 4: Common variable names (tmp, retval, props, etc.)
        elif var_name in {'tmp', 'tmp1', 'tmp2', 'retval', 'result', 'idx', 'index'}:
            needs_declaration = True

        # Pattern 5: Variables with struct field access (detected by _infer_type_from_usage)
        elif any(f'{var_name}.' in line or f'{var_name}->' in line for line in lines):
            needs_declaration = True

        # Pattern 6: Pointer dereferences
        elif any(f'(*{var_name})' in line or f'*{var_name}' in line for line in lines):
            needs_declaration = True

        # Pattern 7: Variables that look like semantic names from variable renaming
        elif var_name in {'ai_props', 'player_info', 'obj_info', 'srv_settings', 'hudinfo',
                          'side', 'sideA', 'sideB', 'master', 'nod', 'enemy'}:
            needs_declaration = True

        # Pattern 8: Variables used with array indexing (var[index])
        # BUGFIX: Global arrays like abl_list need to be declared
        elif any(f'{var_name}[' in line for line in lines):
            needs_declaration = True

        if needs_declaration:
            undefined_vars.add(var_name)

    # 4. Infer types for undefined variables
    var_declarations_to_add: ListType[Tuple[str, str]] = []
    for var_name in sorted(undefined_vars):
        var_type = _infer_type_from_usage(var_name, lines)
        var_declarations_to_add.append((var_type, var_name))

    # 5. Insert declarations after function signature
    if var_declarations_to_add:
        # Find the insertion point (after opening brace, before first code)
        insert_pos = 1
        for i, line in enumerate(lines):
            if line.strip().endswith('{'):
                insert_pos = i + 1
                break

        # Add declarations
        for var_type, var_name in var_declarations_to_add:
            lines.insert(insert_pos, f"    {var_type} {var_name};  // Auto-generated")
            insert_pos += 1

        # Add blank line after auto-generated declarations
        if var_declarations_to_add:
            lines.insert(insert_pos, "")

    # BUGFIX: Fix &array_var references - arrays decay to pointers, don't need &
    # For any variable declared as an array (contains '['), replace &varname with varname
    import re
    array_vars = set()
    for line in lines:
        # Match variable declarations like "Type varname[size];"
        match = re.match(r'\s+\w+\s+(\w+)\[', line)
        if match:
            array_vars.add(match.group(1))

    if array_vars:
        # Replace &array_var with array_var in function calls
        for i, line in enumerate(lines):
            for arr_var in array_vars:
                # Match &array_var in function calls (not in declarations)
                # Pattern: &varname followed by , or ) (function argument context)
                lines[i] = re.sub(rf'&({arr_var})([,)])', r'\1\2', lines[i])

    # DEBUG: Check if lines contain switches
    switch_count = sum(1 for line in lines if "switch (" in line)
    print(f"DEBUG ORCHESTRATOR FINAL: Returning {len(lines)} lines, {switch_count} contain 'switch ('", file=sys.stderr)
    return "\n".join(lines)
