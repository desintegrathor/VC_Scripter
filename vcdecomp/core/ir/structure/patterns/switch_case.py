"""
Switch/case pattern detection for control flow analysis.

This module contains functions for detecting switch/case patterns in the CFG,
including the main switch pattern detection and helper functions for finding
switch variables from nearby global variable loads.
"""

from __future__ import annotations

from typing import Dict, Set, List, Optional
import logging
import sys
import os

from ...cfg import CFG
from ....disasm import opcodes
from ...ssa import SSAFunction
from ...expr import ExpressionFormatter

from .models import CaseInfo, SwitchPattern
from ..analysis.flow import _find_case_body_blocks
from ..analysis.value_trace import (
    _trace_value_to_parameter,
    _trace_value_to_parameter_field,
    _trace_value_to_global,
    _trace_value_to_function_call,
    _follow_ssa_value_across_blocks,
    _check_ssa_value_equivalence
)
from .jump_table import _detect_binary_search_switch
from ..utils.helpers import debug_print

logger = logging.getLogger(__name__)

# Environment-controlled debug logging for switch detection
SWITCH_DEBUG = os.environ.get('VCDECOMP_SWITCH_DEBUG', '0') == '1'

def _switch_debug(msg: str):
    """
    Output debug messages for switch detection when enabled.
    Enable with: VCDECOMP_SWITCH_DEBUG=1
    """
    if SWITCH_DEBUG:
        debug_print(f"[SWITCH] {msg}")


def _detect_case_fallthrough(
    cfg: CFG,
    cases: List[CaseInfo],
    resolver: opcodes.OpcodeResolver
) -> Dict[int, int]:
    """
    Detect which cases fall through to other cases.

    A case falls through when its entry block is a single-instruction JMP
    that targets another case's entry block.

    Pattern example (GetAttackingSide):
        case 0 entry (block 343): JMP 348  -> falls through to case 3
        case 3 entry (block 348): return 0

    This detects the bytecode pattern where the compiler generates a JMP
    from one case's entry point directly to another case's entry point,
    indicating fall-through semantics in the original source.

    Args:
        cfg: Control flow graph
        cases: List of detected case info objects
        resolver: Opcode resolver for mnemonic lookup

    Returns:
        Dict mapping case_value -> target_case_value for fall-through cases
    """
    fallthrough_map: Dict[int, int] = {}

    # Build map: entry block_id -> case value
    block_to_case: Dict[int, int] = {case.block_id: case.value for case in cases}

    for case in cases:
        case_block = cfg.blocks.get(case.block_id)
        if not case_block or not case_block.instructions:
            continue

        # Check if single-instruction JMP block
        if len(case_block.instructions) != 1:
            continue

        instr = case_block.instructions[0]
        mnem = resolver.get_mnemonic(instr.opcode)

        if mnem != "JMP":
            continue

        # Find JMP target block
        target_addr = instr.arg1
        target_block_id = None
        for bid, b in cfg.blocks.items():
            if b.start == target_addr:
                target_block_id = bid
                break

        if target_block_id is None:
            continue

        # Check if target is another case's entry
        if target_block_id in block_to_case:
            target_case_value = block_to_case[target_block_id]
            fallthrough_map[case.value] = target_case_value
            _switch_debug(f"Fall-through detected: case {case.value} -> case {target_case_value}")

    return fallthrough_map


def _resolve_conditional_targets(
    block: "BasicBlock",
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver
) -> tuple[Optional[int], Optional[int]]:
    """
    Resolve conditional jump targets using disassembler addresses.

    Returns (jump_target_block_id, fallthrough_block_id).
    """
    if not block or not block.instructions:
        return (None, None)

    last_instr = block.instructions[-1]
    if not resolver.is_conditional_jump(last_instr.opcode):
        return (None, None)

    jump_target = start_to_block.get(last_instr.arg1)
    fallthrough_addr = last_instr.address + 1
    fallthrough = start_to_block.get(fallthrough_addr)
    if fallthrough is None:
        for succ in block.successors:
            if succ != jump_target:
                fallthrough = succ
                break

    return (jump_target, fallthrough)


def _validate_switch_integrity(
    cases: List[CaseInfo],
    case_sources: Dict[tuple[int, int], int],
    cfg: CFG,
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver
) -> bool:
    """
    Validate that switch cases align with CFG conditional branches.

    Ensures each comparison block maps to exactly one case and that the
    case block matches the disassembler jump target semantics.
    """
    if not cases:
        return False

    comparison_blocks = set(case_sources.values())
    if len(comparison_blocks) != len(cases):
        _switch_debug(
            f"Integrity check failed: {len(cases)} cases but {len(comparison_blocks)} comparison blocks"
        )
        return False

    for case in cases:
        key = (case.value, case.block_id)
        compare_block_id = case_sources.get(key)
        if compare_block_id is None:
            _switch_debug(f"Integrity check failed: missing source for case {key}")
            return False

        compare_block = cfg.blocks.get(compare_block_id)
        if not compare_block or not compare_block.instructions:
            _switch_debug(f"Integrity check failed: missing comparison block {compare_block_id}")
            return False

        last_instr = compare_block.instructions[-1]
        if not resolver.is_conditional_jump(last_instr.opcode):
            _switch_debug(f"Integrity check failed: non-conditional block {compare_block_id}")
            return False

        jump_target, fallthrough = _resolve_conditional_targets(compare_block, start_to_block, resolver)
        if jump_target is None or fallthrough is None:
            _switch_debug(f"Integrity check failed: unresolved targets for block {compare_block_id}")
            return False

        mnemonic = resolver.get_mnemonic(last_instr.opcode)
        expected_case = jump_target if mnemonic == "JNZ" else fallthrough
        if expected_case != case.block_id:
            _switch_debug(
                f"Integrity check failed: case {case.value} block {case.block_id} "
                f"does not match expected {expected_case} from block {compare_block_id}"
            )
            return False

    return True


def _find_mod_in_predecessors(block_id: int, ssa_func: SSAFunction, max_depth: int = 2, visited: Optional[Set[int]] = None) -> Optional[any]:
    """
    Search for a MOD instruction in the current block or predecessor blocks.

    This handles the pattern where MOD leaves its result on the stack, and a subsequent
    LCP instruction loads it for comparison.

    Args:
        block_id: Current block ID
        ssa_func: SSA function
        max_depth: Maximum depth to search (default: 2)
        visited: Set of visited block IDs to prevent cycles

    Returns:
        MOD SSA instruction if found, None otherwise
    """
    if max_depth <= 0:
        return None

    if visited is None:
        visited = set()

    if block_id in visited:
        return None
    visited.add(block_id)

    # Check current block for MOD
    ssa_block = ssa_func.instructions.get(block_id)
    if ssa_block:
        for ssa_inst in ssa_block:
            if ssa_inst.mnemonic == 'MOD':
                return ssa_inst

    # Search predecessors
    cfg = ssa_func.cfg
    block = cfg.get_block(block_id)
    if block and block.predecessors:
        for pred_id in block.predecessors:
            result = _find_mod_in_predecessors(pred_id, ssa_func, max_depth - 1, visited)
            if result:
                return result

    return None


def _case_has_break(
    cfg: CFG,
    case: CaseInfo,
    exit_block: Optional[int],
    resolver: opcodes.OpcodeResolver
) -> bool:
    """
    Determine if a case ends with a break statement.

    Returns:
        True if case ends with JMP to switch exit (has break)
        False if case ends with RET (has return, no break needed)
        False if case falls through to next case (rare, no break)
    """
    if not case.body_blocks or exit_block is None:
        return True  # Default to True if we can't determine

    # Find the last block(s) in the case body
    # A case can have multiple exit points (e.g., if/else branches)
    # We need to check all of them
    last_blocks = []
    for block_id in case.body_blocks:
        block = cfg.blocks.get(block_id)
        if not block or not block.instructions:
            continue

        # A block is a "last block" if it jumps outside the case body
        last_instr = block.instructions[-1]
        mnem = resolver.get_mnemonic(last_instr.opcode)

        # Check if this block exits the case
        if mnem == "JMP":
            target = last_instr.arg1
            # Find target block ID
            target_block_id = None
            for bid, b in cfg.blocks.items():
                if b.start == target:
                    target_block_id = bid
                    break

            # If JMP goes outside case body, this is a last block
            if target_block_id is not None and target_block_id not in case.body_blocks:
                last_blocks.append((block_id, mnem, target_block_id))

        elif mnem == "RET":
            # RET is always a last block
            last_blocks.append((block_id, mnem, None))

        elif resolver.is_conditional_jump(last_instr.opcode):
            # Conditional jump might exit the case
            target = last_instr.arg1
            fall_through = last_instr.address + 1

            target_block_id = None
            fall_through_block_id = None

            for bid, b in cfg.blocks.items():
                if b.start == target:
                    target_block_id = bid
                if b.start == fall_through:
                    fall_through_block_id = bid

            # If either branch goes outside case body, this could be a last block
            exits_case = False
            if target_block_id is not None and target_block_id not in case.body_blocks:
                exits_case = True
            if fall_through_block_id is not None and fall_through_block_id not in case.body_blocks:
                exits_case = True

            if exits_case:
                last_blocks.append((block_id, "JZ/JNZ", target_block_id or fall_through_block_id))

    # CRITICAL FIX: Check if there are "break blocks" immediately after case body
    # These are single-instruction JMP blocks that jump to exit, representing "break;"
    # They're not included in case.body_blocks but follow the last block
    for block_id, mnem, target in list(last_blocks):
        if mnem == "RET":
            continue  # Skip RET blocks

        # Check if target is a simple JMP block (break block)
        if target is not None and target not in case.body_blocks:
            target_block = cfg.blocks.get(target)
            if target_block and len(target_block.instructions) == 1:
                target_instr = target_block.instructions[0]
                target_mnem = resolver.get_mnemonic(target_instr.opcode)
                if target_mnem == "JMP":
                    # This is a break block! Follow it to see where it goes
                    break_target = target_instr.arg1
                    break_target_id = None
                    for bid, b in cfg.blocks.items():
                        if b.start == break_target:
                            break_target_id = bid
                            break
                    # Update the target to point to the actual destination
                    last_blocks.append((target, "JMP (break)", break_target_id))

    # Now check what these last blocks do:
    # - If ALL last blocks RET → no break needed (return False)
    # - If ANY last block JMPs to exit_block → has break (return True)
    # - Otherwise → fall-through or complex control flow (return True as default)

    if not last_blocks:
        return True  # No clear exit found, assume break

    all_ret = True
    any_jmp_to_exit = False

    for block_id, mnem, target in last_blocks:
        if mnem == "RET":
            # This path returns, no break needed on this path
            pass
        else:
            all_ret = False
            # Check if this jumps to switch exit
            if target == exit_block:
                any_jmp_to_exit = True

    # If all paths return, no break needed
    if all_ret:
        return False

    # If any path jumps to exit, we have a break
    if any_jmp_to_exit:
        return True

    # Otherwise, assume break (safe default)
    return True


def _block_ends_with_return(
    cfg: CFG,
    block_id: int,
    resolver: opcodes.OpcodeResolver
) -> bool:
    """
    Check if a block ends with a return instruction.

    Args:
        cfg: Control flow graph
        block_id: Block to check
        resolver: Opcode resolver

    Returns:
        True if block ends with RET, False otherwise
    """
    block = cfg.blocks.get(block_id)
    if not block or not block.instructions:
        return False

    last_instr = block.instructions[-1]
    return resolver.is_return(last_instr.opcode)


def _block_is_returnish(
    cfg: CFG,
    block_id: int,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int]
) -> bool:
    """
    Check if a block either returns directly or jumps to a return block.

    Args:
        cfg: Control flow graph
        block_id: Block to check
        resolver: Opcode resolver
        start_to_block: Mapping from instruction address to block ID

    Returns:
        True if block ends with RET or JMP to a RET block
    """
    block = cfg.blocks.get(block_id)
    if not block or not block.instructions:
        return False

    last_instr = block.instructions[-1]
    if resolver.is_return(last_instr.opcode):
        return True

    if resolver.get_mnemonic(last_instr.opcode) == "JMP":
        target_block_id = start_to_block.get(last_instr.arg1)
        if target_block_id is not None:
            return _block_ends_with_return(cfg, target_block_id, resolver)

    return False


def _is_simple_return_switch(
    cases: List[CaseInfo],
    cfg: CFG,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int]
) -> bool:
    """
    Heuristic for small switch-return functions where integrity checks fail.

    This accepts a switch if every case entry block immediately returns
    (or jumps to a return), which matches patterns like:
        case 0: return 0;
        case 3: return 0;
        default: return 1;
    """
    if len(cases) < 2:
        return False

    return all(
        _block_is_returnish(cfg, case.block_id, resolver, start_to_block)
        for case in cases
    )


def _find_param_field_in_predecessors(
    ssa_func: SSAFunction,
    current_block_id: int,
    var_value,
    formatter: ExpressionFormatter
) -> Optional[str]:
    """
    Search predecessor blocks for parameter field access pattern.

    Pattern: When switch var is loaded via LCP in current block,
    look in predecessor blocks for:
        LADR [sp-N]   ; Load param address (negative offset = parameter)
        DADR offset   ; Add field offset
        DCP           ; Dereference

    This handles the common Vietcong compiler pattern where:
        Block N:   LADR [sp-4] → DADR 0 → DCP → JMP Block N+1
        Block N+1: LCP [sp+418] → EQU → JZ

    The DCP result is stored on stack, then LCP reloads it. We need to
    trace through this pattern to find the actual parameter field access.

    Args:
        ssa_func: SSA function containing the blocks
        current_block_id: Block where the switch comparison is happening
        var_value: The SSA value being tested (typically from LCP)
        formatter: Expression formatter

    Returns:
        Parameter field access string (e.g., "info->message") if found, None otherwise
    """
    cfg = ssa_func.cfg
    if not cfg:
        return None

    ssa_blocks = ssa_func.instructions

    # Get predecessors using BFS traversal (up to 10 levels)
    # This is needed because the LADR→DADR→DCP pattern might be many blocks away
    # from the switch comparison block, especially in large functions like ScriptMain
    preds = set()
    to_visit = []
    if current_block_id in cfg.blocks:
        block = cfg.blocks[current_block_id]
        for pred in block.predecessors:
            to_visit.append((pred, 1))

    max_depth = 10  # Extend search depth for large functions
    while to_visit:
        pred_id, depth = to_visit.pop(0)
        if pred_id in preds:
            continue
        preds.add(pred_id)
        if depth < max_depth and pred_id in cfg.blocks:
            for pred in cfg.blocks[pred_id].predecessors:
                if pred not in preds:
                    to_visit.append((pred, depth + 1))

    _switch_debug(f"  Searching {len(preds)} predecessor blocks for LADR→DADR→DCP pattern")

    # Search each predecessor for the pattern
    for pred_id in preds:
        if pred_id not in ssa_blocks:
            continue

        instrs = ssa_blocks[pred_id]

        # Look for DCP preceded by DADR preceded by LADR
        for i, instr in enumerate(instrs):
            if instr.mnemonic != 'DCP':
                continue

            # Check if this DCP has inputs from DADR
            if not instr.inputs or len(instr.inputs) == 0:
                continue

            # Get the pointer input to DCP
            ptr_value = instr.inputs[0]
            if not ptr_value.producer_inst:
                continue

            dadr_inst = ptr_value.producer_inst

            # Check if pointer came from DADR
            if dadr_inst.mnemonic != 'DADR':
                continue

            # Get field offset from DADR instruction
            field_offset = None
            if dadr_inst.instruction and dadr_inst.instruction.instruction:
                field_offset = dadr_inst.instruction.instruction.arg1

            # Get the base address input to DADR
            if not dadr_inst.inputs or len(dadr_inst.inputs) == 0:
                continue

            base_value = dadr_inst.inputs[0]
            if not base_value.producer_inst:
                continue

            ladr_inst = base_value.producer_inst

            # Check if base came from LADR
            if ladr_inst.mnemonic != 'LADR':
                continue

            # Get stack offset from LADR instruction
            stack_offset = None
            if ladr_inst.instruction and ladr_inst.instruction.instruction:
                stack_offset = ladr_inst.instruction.instruction.arg1

            # Handle signed conversion: offsets > 0x7FFFFFFF are negative in two's complement
            signed_offset = stack_offset
            if stack_offset is not None and stack_offset > 0x7FFFFFFF:
                signed_offset = stack_offset - 0x100000000  # Convert to signed

            _switch_debug(f"    Found LADR→DADR→DCP: LADR [sp{signed_offset:+d}], DADR {field_offset}, DCP in block {pred_id}")

            # Check if LADR loads a parameter address (negative stack offset)
            if signed_offset is not None and signed_offset < 0:
                # This is a parameter! Map field offset to field name.
                # s_SC_NET_info struct layout:
                #   0: message (dword)
                #   4: param1 (dword)
                #   8: param2 (dword)
                #  12: param3 (dword)
                #  16: elapsed_time (float)
                #  20: fval1 / next_exe_time (float)
                # s_SC_L_info has similar layout

                field_map = {
                    0: "message",
                    4: "param1",
                    8: "param2",
                    12: "param3",
                    16: "elapsed_time",
                    20: "fval1",  # or next_exe_time for s_SC_L_info
                }

                field_name = field_map.get(field_offset)
                if field_name:
                    # Default parameter name
                    param_name = "info"

                    # Try to get better parameter name from function signature
                    if hasattr(formatter, '_func_signature') and formatter._func_signature:
                        func_sig = formatter._func_signature
                        if func_sig.param_types:
                            for param_type in func_sig.param_types:
                                if 's_SC_NET_info' in param_type or 's_SC_L_info' in param_type:
                                    parts = param_type.split()
                                    if parts:
                                        param_name = parts[-1].lstrip('*')
                                    break

                    result = f"{param_name}->{field_name}"
                    _switch_debug(f"    SUCCESS: Found parameter field access: {result}")
                    return result
                else:
                    _switch_debug(f"    Field offset {field_offset} not in field_map, trying generic")
                    # Return generic field access for unknown fields
                    return f"info->field_{field_offset}"

    return None


def _find_switch_variable_from_nearby_gcp(
    ssa_func: SSAFunction,
    current_block_id: int,
    var_value,
    formatter: ExpressionFormatter,
    func_block_ids: Set[int]
) -> Optional[str]:
    """
    Heuristic to find switch variable when normal tracing fails.

    Pattern: Compiler generates code like:
        Block 1: GCP data[X]  # Load global variable
                 JMP Block 2
        Block 2: LCP [sp+0]   # Load from stack (but value didn't propagate through CFG)
                 ...
                 EQU          # Compare in switch

    We look for GCP instructions in SSA blocks (which preserve correct mnemonics)
    to find the first global variable load - this is likely the switch variable.

    IMPORTANT: This is a LAST RESORT heuristic. Prefer using:
    1. _trace_value_to_parameter_field() for parameter field access
    2. _find_param_field_in_predecessors() for cross-block parameter field patterns

    To avoid picking wrong variables, we now limit search to predecessor blocks only.
    """
    import sys

    cfg = ssa_func.cfg

    # CRITICAL FIX: Only search in predecessor blocks, not entire function!
    # This prevents picking up unrelated global variables from other parts of the function.
    search_blocks = set()
    search_blocks.add(current_block_id)

    if cfg and current_block_id in cfg.blocks:
        block = cfg.blocks[current_block_id]
        search_blocks.update(block.predecessors)
        # Also search predecessors of predecessors (2 levels)
        for pred_id in list(search_blocks):
            if pred_id in cfg.blocks:
                search_blocks.update(cfg.blocks[pred_id].predecessors)

    _switch_debug(f"  GCP heuristic: searching {len(search_blocks)} predecessor blocks (was: entire function)")

    # Search through SSA instructions (which have correct mnemonics)
    ssa_blocks = ssa_func.instructions  # Dict[block_id, List[SSAInstruction]]

    # Find GCP/GLD instructions in predecessor blocks only
    gcp_candidates = []

    # Collect all GCP/GLD from predecessor blocks
    for block_id in search_blocks:
        if block_id not in ssa_blocks:
            continue

        ssa_instrs = ssa_blocks[block_id]
        for ssa_instr in ssa_instrs:
            if ssa_instr.mnemonic in {'GCP', 'GLD'}:
                # Found a global load!
                # Get the dword offset from instruction
                if hasattr(ssa_instr, 'instruction') and hasattr(ssa_instr.instruction, 'instruction'):
                    dword_offset = ssa_instr.instruction.instruction.arg1

                    if hasattr(formatter, '_global_names'):
                        global_name = formatter._global_names.get(dword_offset)
                        if global_name:
                            # Record this as candidate with instruction address
                            gcp_candidates.append((ssa_instr.address, global_name, dword_offset))
                            _switch_debug(f"    GCP candidate: {global_name} at addr {ssa_instr.address} in block {block_id}")

    # If we found any GCP, use the FIRST one (earliest in predecessor blocks)
    if gcp_candidates:
        # Sort by instruction address (earliest first)
        gcp_candidates.sort(key=lambda x: x[0])
        result = gcp_candidates[0][1]
        _switch_debug(f"  GCP heuristic result: {result}")
        return result

    return None


def _extract_comparison_variable(
    block_id: int,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter
) -> Optional[str]:
    """
    Extract the variable being tested in a comparison block.

    This is used during pre-scanning to identify nested switch headers.
    A nested switch header tests a DIFFERENT variable than the outer switch.

    Args:
        block_id: Block ID to check
        ssa_func: SSA function context
        formatter: Expression formatter

    Returns:
        Variable name being tested if found, None otherwise
    """
    ssa_block = ssa_func.instructions.get(block_id)
    if not ssa_block:
        return None

    for ssa_inst in ssa_block:
        if ssa_inst.mnemonic == 'EQU':
            if len(ssa_inst.inputs) >= 2:
                var_value = ssa_inst.inputs[0]
                # Use existing variable tracing logic
                var_name = _trace_value_to_parameter_field(var_value, formatter, ssa_func)
                if not var_name:
                    var_name = _trace_value_to_parameter(var_value, formatter, ssa_func)
                if not var_name:
                    var_name = _trace_value_to_global(var_value, formatter, ssa_func)
                if not var_name and hasattr(var_value, 'alias'):
                    var_name = var_value.alias
                return var_name
    return None


def _pre_scan_for_nested_headers(
    cfg: CFG,
    case_entry: int,
    case_entries: Set[int],
    chain_blocks: List[int],
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver,
    outer_switch_var: str,
    max_depth: int = 15
) -> Set[int]:
    """
    Pre-scan from a case entry to find blocks that start nested switches.

    A nested switch header is a block that:
    1. Has a conditional jump (JZ/JNZ)
    2. Tests a DIFFERENT variable than the outer switch
    3. Is reachable from the case entry

    This function is called BEFORE preliminary body detection to ensure
    that nested switch headers are included in stop_blocks, preventing
    the BFS from traversing INTO nested switch structures.

    Args:
        cfg: Control flow graph
        case_entry: Entry block of the case being scanned
        case_entries: Set of all case entry blocks
        chain_blocks: List of comparison chain blocks
        ssa_func: SSA function context
        formatter: Expression formatter
        start_to_block: Map from instruction address to block ID
        resolver: Opcode resolver
        outer_switch_var: Variable being tested in the outer switch
        max_depth: Maximum BFS depth to search

    Returns:
        Set of block IDs that are nested switch headers
    """
    nested_headers = set()
    visited = set()
    stop_blocks = set(case_entries)
    stop_blocks.update(chain_blocks)

    worklist = [(case_entry, 0)]  # (block_id, depth)

    while worklist:
        block_id, depth = worklist.pop(0)

        if block_id in visited or depth > max_depth:
            continue
        if block_id in stop_blocks and block_id != case_entry:
            continue

        visited.add(block_id)
        block = cfg.blocks.get(block_id)
        if not block:
            continue

        # Check if this block has a conditional jump testing a different variable
        if block.instructions:
            last_instr = block.instructions[-1]
            if resolver.is_conditional_jump(last_instr.opcode):
                # Try to extract the test variable
                var_name = _extract_comparison_variable(block_id, ssa_func, formatter)
                if var_name and var_name != outer_switch_var:
                    # This block tests a different variable - it's a nested switch header
                    nested_headers.add(block_id)
                    debug_print(f"DEBUG SWITCH: Pre-scan found nested header at {block_id}: tests '{var_name}' vs outer '{outer_switch_var}'")
                    # Don't traverse into nested switch - it will be detected separately
                    continue

        # Add successors to worklist
        for succ in block.successors:
            if succ not in visited:
                worklist.append((succ, depth + 1))

    return nested_headers


def _find_equ_for_comparison(
    current_block_id: int,
    jump_ssa,
    ssa_blocks: Dict[int, List],
    cfg,
    max_pred_search: int = 3
):
    """
    Find EQU instruction producing jump condition.
    Searches current block and up to max_pred_search predecessor levels.

    Args:
        current_block_id: Block ID to start search from
        jump_ssa: The JZ/JNZ SSA instruction
        ssa_blocks: Dictionary of block IDs to SSA instruction lists
        cfg: Control flow graph
        max_pred_search: Maximum predecessor depth to search (default: 3)

    Returns:
        Tuple of (equ_inst, var_value, const_value) or None
    """
    if not jump_ssa or not jump_ssa.inputs:
        return None

    condition_value = jump_ssa.inputs[0]

    # Search current block for EQU
    for ssa_inst in ssa_blocks.get(current_block_id, []):
        if any(out.name == condition_value.name for out in ssa_inst.outputs):
            if ssa_inst.mnemonic == "EQU" and len(ssa_inst.inputs) >= 2:
                _switch_debug(f"Found EQU in current block {current_block_id}")
                return (ssa_inst, ssa_inst.inputs[0], ssa_inst.inputs[1])

    # Search predecessors if not found in current block
    if max_pred_search > 0:
        current_block = cfg.blocks.get(current_block_id)
        if current_block:
            for pred_id in current_block.predecessors:
                _switch_debug(f"Searching for EQU in predecessor block {pred_id}")
                # Search this predecessor
                for ssa_inst in ssa_blocks.get(pred_id, []):
                    if any(out.name == condition_value.name for out in ssa_inst.outputs):
                        if ssa_inst.mnemonic == "EQU" and len(ssa_inst.inputs) >= 2:
                            _switch_debug(f"Found EQU in predecessor block {pred_id}")
                            return (ssa_inst, ssa_inst.inputs[0], ssa_inst.inputs[1])

                # Recurse to predecessor's predecessors
                result = _find_equ_for_comparison(
                    pred_id, jump_ssa, ssa_blocks, cfg, max_pred_search - 1
                )
                if result:
                    return result

    return None


def _detect_switch_patterns(
    ssa_func: SSAFunction,
    func_block_ids: Set[int],
    formatter: ExpressionFormatter,
    start_to_block: Dict[int, int]
) -> List[SwitchPattern]:
    """
    Detect switch/case patterns in the function.

    A switch pattern consists of:
    1. Multiple consecutive blocks testing the SAME variable
    2. Each test is an equality comparison (EQU) with a constant
    3. Each test jumps to different case bodies on match
    4. All tests share a common exit point

    Pattern example:
        Block A: if (var == 0) goto case_0; else goto Block B
        Block B: if (var == 1) goto case_1; else goto Block C
        Block C: if (var == 2) goto case_2; else goto default
    """
    cfg = ssa_func.cfg
    resolver = getattr(ssa_func.scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    ssa_blocks = ssa_func.instructions
    switches: List[SwitchPattern] = []
    processed_blocks: Set[int] = set()

    # DEBUG: Print blocks around ScriptMain entry (1097)
    scriptmain_blocks = [bid for bid in cfg.blocks.keys() if 1090 <= cfg.blocks[bid].start <= 1200]
    scriptmain_in_func = [bid for bid in scriptmain_blocks if bid in func_block_ids]
    scriptmain_missing = [bid for bid in scriptmain_blocks if bid not in func_block_ids]
    debug_print(f"DEBUG SWITCH: ScriptMain area blocks (1090-1200): {sorted(scriptmain_blocks)}")
    debug_print(f"DEBUG SWITCH: ScriptMain blocks in func_block_ids: {sorted(scriptmain_in_func)}")
    if scriptmain_missing:
        debug_print(f"DEBUG SWITCH: ScriptMain blocks MISSING from func_block_ids: {sorted(scriptmain_missing)}")
        for bid in sorted(scriptmain_missing):
            if bid in cfg.blocks:
                block = cfg.blocks[bid]
                debug_print(f"DEBUG SWITCH:   Block {bid}: start={block.start}, end={block.end}, preds={len(block.predecessors)}")

    # Iterate through blocks looking for switch headers
    for block_id in func_block_ids:
        if block_id in processed_blocks:
            continue

        block = cfg.blocks.get(block_id)
        if not block or not block.instructions:
            continue

        logger.debug(f"Checking block {block_id} for switch pattern (start addr: {block.start})")
        debug_print(f"DEBUG SWITCH: Checking block {block_id} for switch pattern (start addr: {block.start})")

        # PHASE 8A: Try binary search detection first (for large switches)
        binary_switch = _detect_binary_search_switch(
            cfg, block_id, ssa_func, formatter, func_block_ids
        )
        if binary_switch and len(binary_switch.cases) >= 3:
            _switch_debug(f"Detected binary search switch with {len(binary_switch.cases)} cases at block {block_id}")
            switches.append(binary_switch)
            processed_blocks.update(binary_switch.all_blocks)
            continue

        # Fall back to BFS-based detection for smaller switches
        # This handles both linear chains AND non-linear patterns where
        # case bodies are interleaved between comparison blocks
        test_var = None
        test_ssa_value = None  # Track the actual SSA value being tested (for aliasing detection)
        cases: List[CaseInfo] = []
        chain_blocks: List[int] = []

        # PHASE 2 FIX: Track ALL variables seen across ALL comparison blocks
        # This allows us to pick the most consistent variable (highest occurrence)
        # and handle cases where different blocks use different names for the same value
        variable_frequency: Dict[str, int] = {}  # var_name -> count of blocks using it
        variable_priority: Dict[str, int] = {}   # var_name -> priority score (param field=100, global=50, etc.)
        variable_to_ssa: Dict[str, any] = {}      # var_name -> SSA value

        # PHASE 3 FIX: Collect ALL potential cases first, then filter
        # Structure: List[(var_name, var_priority, ssa_value, case_info)]
        all_potential_cases: List[tuple] = []
        case_sources: Dict[tuple[int, int], int] = {}

        # FIX: Track detection order for cases (preserves bytecode order)
        next_detection_order: int = 0

        # Chain tracking state for debug
        chain_debug = {
            'blocks_processed': [],
            'break_reasons': [],
            'variables_seen': [],
            'ssa_values_seen': []
        }

        # NEW: Track blocks that are nested switch headers (different variable)
        # These should be excluded from case body detection
        nested_switch_headers: Set[int] = set()

        # BFS state: blocks to visit with their depth
        visited_blocks = set()
        to_visit = [(block_id, 0)]  # (block_id, depth)
        max_bfs_depth = 15  # Reasonable limit to avoid exploring too far
        last_chain_block: Optional[int] = None  # Track last comparison/test block in chain

        # BFS exploration to find all comparison blocks
        while to_visit:
            current_block, depth = to_visit.pop(0)

            _switch_debug(f"BFS: Visiting block {current_block} (depth={depth}, queue_size={len(to_visit)})")

            # Depth limit
            if depth > max_bfs_depth:
                _switch_debug(f"  Skipping: depth {depth} > max {max_bfs_depth}")
                continue

            # Skip if already visited
            if current_block in visited_blocks:
                _switch_debug(f"  Skipping: already visited")
                continue
            visited_blocks.add(current_block)

            # Skip if not in function scope
            if current_block not in func_block_ids:
                _switch_debug(f"  Skipping: not in function scope")
                continue

            # Skip already processed blocks (but don't break entire BFS)
            if current_block in processed_blocks:
                _switch_debug(f"Block {current_block} already processed, skipping")
                continue

            curr_block_obj = cfg.blocks.get(current_block)
            if not curr_block_obj or not curr_block_obj.instructions:
                _switch_debug(f"Block {current_block} has no instructions, skipping")
                continue

            _switch_debug(f"Checking block {current_block} (addr: {curr_block_obj.start})")
            chain_debug['blocks_processed'].append(current_block)

            last_instr = curr_block_obj.instructions[-1]
            opcode = last_instr.opcode

            # Must be conditional jump for a comparison block
            # If not, this block might be a case body - explore its successors
            if not resolver.is_conditional_jump(opcode):
                _switch_debug(f"Block {current_block} has no conditional jump, might be case body")
                # Add successors to BFS queue (this handles interleaved case bodies)
                for succ in curr_block_obj.successors:
                    if succ not in visited_blocks and succ in func_block_ids:
                        to_visit.append((succ, depth + 1))
                continue


            # Get SSA instructions for this block
            ssa_block = ssa_blocks.get(current_block, [])

            # Find the condition (should be EQU comparison)
            # JZ/JNZ takes the result of EQU as input, so we need to find the EQU that produces the condition
            found_equ = False

            # Find the JZ/JNZ instruction in SSA
            jump_ssa = None
            for ssa_inst in ssa_block:
                if ssa_inst.address == last_instr.address:
                    jump_ssa = ssa_inst
                    break

            # Use multi-block EQU finder (searches current block and predecessors)
            equ_result = _find_equ_for_comparison(
                current_block, jump_ssa, ssa_blocks, cfg, max_pred_search=3
            )

            _switch_debug(f"Block {current_block}: EQU search result: {equ_result is not None}")
            if equ_result:
                equ_inst, var_value, const_value = equ_result
                _switch_debug(f"  EQU found: var={var_value.name if hasattr(var_value, 'name') else var_value}, const={const_value.name if hasattr(const_value, 'name') else const_value}")

                # FIX #3: Improved float filtering - check if constant is a float
                # Message IDs are typically 0-1000, definitely integers
                # Only filter if we have strong evidence this is a float switch
                if const_value.alias and const_value.alias.startswith("data_"):
                    try:
                        offset = int(const_value.alias[5:])
                        if ssa_func.scr and ssa_func.scr.data_segment:
                            const_raw = ssa_func.scr.data_segment.get_dword(offset * 4)
                            logger.debug(f"  Checking constant: data[{offset}] = {const_raw} (0x{const_raw:08X})")

                            # CRITICAL FIX: Integer range check for message IDs
                            # Message IDs are typically 0-10000 (extended range for VC engine constants)
                            # If value is in this range, treat as integer, NOT float
                            if 0 <= const_raw < 10000:
                                logger.debug(f"    -> In message ID range (0-10000), treating as integer")
                                # Don't skip this case - it's likely a valid switch case
                            else:
                                # Outside message ID range - might be float
                                import struct
                                try:
                                    float_val = struct.unpack('f', struct.pack('I', const_raw & 0xFFFFFFFF))[0]
                                    logger.debug(f"    As float: {float_val}")

                                    # Check if this is definitely a float by looking for fractional part
                                    # OR if the value is very large and looks like a float bit pattern
                                    if not (float_val != float_val):  # Not NaN
                                        # Has fractional part? Definitely float
                                        if abs(float_val - round(float_val)) > 0.01:
                                            logger.debug(f"    -> Detected as float (has decimal part), skipping switch case")
                                            found_equ = False
                                            break
                                        # Large value that doesn't make sense as message ID?
                                        # Could still be integer constant, so be conservative
                                        elif const_raw > 100000:
                                            # Very large value - check if float interpretation is more sensible
                                            if -10000.0 < float_val < 10000.0:
                                                logger.debug(f"    -> Large value with reasonable float interpretation, might be float")
                                                # Be conservative - don't filter unless we're sure
                                except:
                                    pass
                    except (ValueError, AttributeError):
                        pass

                # FIX #1: Get variable name - try parameter field FIRST (highest priority)
                _switch_debug(f"Switch detection: Tracing var_value {var_value.name if hasattr(var_value, 'name') else var_value} (alias: {var_value.alias if hasattr(var_value, 'alias') else 'None'})")
                _switch_debug(f"  Producer: {var_value.producer_inst.mnemonic if var_value.producer_inst else 'None'}")
                _switch_debug(f"  Current test_var: {test_var}, test_ssa_value: {test_ssa_value.name if test_ssa_value and hasattr(test_ssa_value, 'name') else test_ssa_value}")

                var_name = None

                # Phase 8B.1 FIX: Check for MOD operation FIRST before other traces
                # This prevents parameter/global traces from hiding the modulo expression

                # First, check if var_value itself is produced by MOD
                actual_producer = var_value.producer_inst

                # If producer is LCP (load from stack), search predecessor blocks for MOD
                # This handles cases like: Block N: MOD -> Block N+1: LCP [sp+0] -> EQU
                if actual_producer and actual_producer.mnemonic == 'LCP':
                    # Search current block and predecessors for MOD instruction
                    mod_inst = _find_mod_in_predecessors(current_block, ssa_func, max_depth=2)
                    if mod_inst:
                        actual_producer = mod_inst
                        _switch_debug(f"  -> Found MOD in predecessor block")

                if actual_producer and actual_producer.mnemonic == "MOD":
                        # Extract: var % constant
                        if len(actual_producer.inputs) >= 2:
                            base_var = actual_producer.inputs[0]
                            mod_value = actual_producer.inputs[1]

                            # Try to get base variable name
                            base_name = _trace_value_to_parameter(base_var, formatter, ssa_func)
                            if not base_name:
                                base_name = _trace_value_to_global(base_var, formatter, ssa_func)
                            if not base_name:
                                # Phase 8B.1: Use multi-block SSA tracing for complex cases
                                producer = _follow_ssa_value_across_blocks(base_var, ssa_func, max_depth=10)
                                if producer:
                                    if producer.mnemonic == 'LCP':
                                        # Parameter load - try to resolve again with producer context
                                        base_name = _trace_value_to_parameter(base_var, formatter, ssa_func)
                                    elif producer.mnemonic in {'GCP', 'GLD'}:
                                        # Global load - try to resolve again with producer context
                                        base_name = _trace_value_to_global(base_var, formatter, ssa_func)
                            if not base_name:
                                base_name = formatter.render_value(base_var)

                            # Try to get modulo constant
                            mod_const = None
                            if mod_value.alias and mod_value.alias.startswith("data_"):
                                try:
                                    offset = int(mod_value.alias[5:])
                                    if ssa_func.scr and ssa_func.scr.data_segment:
                                        mod_const = ssa_func.scr.data_segment.get_dword(offset * 4)
                                except (ValueError, AttributeError):
                                    pass

                            if mod_const is not None:
                                var_name = f"{base_name}%{mod_const}"
                                _switch_debug(f"  -> Detected modulo switch: {var_name}")

                # If not MOD, try other variable resolution methods
                # PRIORITY FIX: Try global variables FIRST, before parameter fields
                # This prefers named globals like "gphase" over generic "info->param2"
                if not var_name:
                    var_name = _trace_value_to_global(var_value, formatter, ssa_func)
                    if var_name:
                        _switch_debug(f"  -> Found global: {var_name}")

                # Then try parameter field access (info->message, info->param1, etc.)
                if not var_name:
                    var_name = _trace_value_to_parameter_field(var_value, formatter, ssa_func)
                    if var_name:
                        _switch_debug(f"  -> Found parameter field: {var_name}")

                if not var_name:
                    var_name = _trace_value_to_parameter(var_value, formatter, ssa_func)
                    if var_name:
                        _switch_debug(f"  -> Found parameter: {var_name}")

                        # PHASE 8B Priority 1: If generic parameter name (param_0, param_1, etc.),
                        # try to infer semantic name from function context
                        if var_name.startswith('param_'):
                            semantic_name = _infer_parameter_semantic_name(
                                var_value, var_name, ssa_func, formatter
                            )
                            if semantic_name:
                                var_name = semantic_name
                                _switch_debug(f"  -> Inferred semantic parameter name: {var_name}")

                if not var_name:
                    var_name = _trace_value_to_function_call(ssa_func, var_value, formatter)
                    if var_name:
                        _switch_debug(f"  -> Found function call result: {var_name}")

                # CRITICAL FIX for Switch Variable Tracking:
                # Try parameter field pattern in predecessor blocks FIRST.
                # This handles the common Vietcong pattern:
                #   Block N:   LADR [sp-4] → DADR 0 → DCP → JMP Block N+1
                #   Block N+1: LCP [sp+418] → EQU → JZ (switch comparison)
                # Normal tracing fails because LCP loads from a different stack slot than DCP writes.
                if not var_name:
                    var_name = _find_param_field_in_predecessors(
                        ssa_func, current_block, var_value, formatter
                    )
                    if var_name:
                        _switch_debug(f"  -> Found via predecessor param field search: {var_name}")

                # FALLBACK: If predecessor search failed, try GCP heuristic.
                # This is needed for global variable switches where the global is loaded
                # in a predecessor block but not tracked through SSA.
                if not var_name:
                    # Look for GCP in SSA blocks - works for all iterations, not just first
                    # IMPORTANT: Pass SSA function, not CFG, to get correct mnemonics
                    var_name = _find_switch_variable_from_nearby_gcp(
                        ssa_func, current_block, var_value, formatter, func_block_ids
                    )
                    if var_name:
                        _switch_debug(f"  -> Found via GCP heuristic: {var_name}")

                if not var_name:
                    # Fall back to regular rendering if neither parameter nor global
                    var_name = formatter.render_value(var_value)
                    _switch_debug(f"  -> Fallback to rendered value: {var_name}")

                # PHASE 2 FIX: Calculate priority score for this variable
                var_priority = 0
                if "->" in var_name:
                    # Parameter field access (info->message)
                    var_priority = 100
                elif var_name.startswith("param_"):
                    var_priority = 90
                elif var_name.startswith("g") or "_g" in var_name:
                    var_priority = 50
                elif "%" in var_name:
                    # Modulo expression
                    var_priority = 80
                else:
                    var_priority = 30

                _switch_debug(f"  Variable '{var_name}' assigned priority: {var_priority}")

                # NESTED SWITCH FIX: When we see a different variable, it's likely a nested switch
                # Only collect cases for the SAME variable to preserve switch structure
                # The nested switch will be detected when we process case bodies later

                # Track for first case establishment
                if test_var is None:
                    test_var = var_name
                    test_ssa_value = var_value
                    _switch_debug(f"First case established: {test_var} (SSA: {var_value.name if hasattr(var_value, 'name') else var_value})")
                    chain_debug['variables_seen'].append(test_var)
                    chain_debug['ssa_values_seen'].append(var_value.name if hasattr(var_value, 'name') else str(var_value))
                    debug_print(f"DEBUG SWITCH: First case - variable: {test_var}, SSA: {var_value.name if hasattr(var_value, 'name') else var_value}")
                elif test_var != var_name:
                    # NESTED SWITCH FIX: Different variable = likely nested switch
                    # EXCEPTION: If test_var is a MOD expression (contains %), and var_name is local_N,
                    # this is likely the same switch - the MOD result is stored on stack and reloaded.
                    # Pattern: Block N: MOD param_0, 4 -> Block N+1: LCP [sp+0] (becomes local_0)
                    is_mod_switch = '%' in test_var
                    is_stack_load = var_name.startswith('local_') or var_name.startswith('n')

                    if is_mod_switch and is_stack_load:
                        # Same switch, different name - use the MOD-based name
                        _switch_debug(f"MOD switch continuation: {test_var} vs {var_name} (treating as same variable)")
                        chain_debug['variables_seen'].append(var_name)
                        chain_debug['ssa_values_seen'].append(var_value.name if hasattr(var_value, 'name') else str(var_value))
                        debug_print(f"DEBUG SWITCH: MOD switch continuation - keeping {test_var}")
                        # Don't update test_var - keep the MOD-based name
                    else:
                        # Skip this block - it will be processed when we analyze the case body
                        _switch_debug(f"Different variable seen: {test_var} -> {var_name} (skipping - likely nested switch)")
                        chain_debug['variables_seen'].append(var_name)
                        chain_debug['ssa_values_seen'].append(var_value.name if hasattr(var_value, 'name') else str(var_value))
                        debug_print(f"DEBUG SWITCH: Variable mismatch - test_var: {test_var}, new var_name: {var_name} (skipping - nested switch)")

                        # NEW: Record this block as a nested switch header
                        # This prevents case body BFS from traversing into nested switch structures
                        nested_switch_headers.add(current_block)
                        debug_print(f"DEBUG SWITCH: Added block {current_block} to nested_switch_headers")

                        # Don't add successors for nested switch blocks - let them be detected later
                        # CRITICAL: Do NOT track this variable in frequency/priority - it belongs
                        # to a nested switch, not the current one being detected.
                        continue

                # Track this variable's frequency and priority.
                # This is done AFTER the nested switch check so that variables
                # belonging to nested switches are excluded from best-variable selection.
                variable_frequency[var_name] = variable_frequency.get(var_name, 0) + 1
                variable_priority[var_name] = max(variable_priority.get(var_name, 0), var_priority)
                variable_to_ssa[var_name] = var_value

                # Same variable (or first case), try to extract constant value using ConstantPropagator
                _switch_debug(f"About to extract constant from: {const_value.name if hasattr(const_value, 'name') else const_value}")
                debug_print(f"DEBUG SWITCH: About to extract constant from: {const_value.name if hasattr(const_value, 'name') else const_value}")
                case_val = None
                const_info = formatter._constant_propagator.get_constant(const_value)
                if const_info is not None:
                    case_val = const_info.value
                    _switch_debug(f"  Successfully extracted case value: {case_val}")
                    debug_print(f"DEBUG SWITCH: Successfully extracted case value: {case_val}")
                else:
                    _switch_debug(f"  Failed to extract constant - const_value alias={const_value.alias if hasattr(const_value, 'alias') else 'None'}, producer={const_value.producer_inst.mnemonic if const_value.producer_inst else 'None'}")
                    debug_print(f"DEBUG SWITCH: Failed to extract constant for SSA value: {const_value.name}")

                if case_val is not None:
                        # This is a valid case!
                        debug_print(f"DEBUG SWITCH: case_val is not None: {case_val}")
                        # Determine which successor is the case body
                        # JZ means jump if zero (condition false), so arg1 is NOT the case
                        # JNZ means jump if not zero (condition true), so arg1 IS the case
                        mnemonic = resolver.get_mnemonic(opcode)
                        debug_print(f"DEBUG SWITCH: mnemonic={mnemonic}, opcode={opcode}")

                        jump_target, fallthrough = _resolve_conditional_targets(
                            curr_block_obj, start_to_block, resolver
                        )
                        if mnemonic == "JNZ":
                            case_block_id = jump_target
                        else:  # JZ
                            case_block_id = fallthrough

                        debug_print(f"DEBUG SWITCH: case_block_id={case_block_id}")
                        if case_block_id is not None:
                            # PHASE 3 FIX: Store all potential cases with their variable info
                            # Don't filter yet - we'll do that after BFS completes
                            # FIX: Assign detection_order to preserve bytecode order
                            case_info = CaseInfo(value=case_val, block_id=case_block_id, detection_order=next_detection_order)
                            next_detection_order += 1
                            all_potential_cases.append((var_name, var_priority, var_value, case_info, current_block))
                            case_sources[(case_val, case_block_id)] = current_block

                            # TEMPORARY: Also add to old structure for compatibility
                            cases.append(case_info)
                            chain_blocks.append(current_block)
                            last_chain_block = current_block  # Track last test block
                            found_equ = True
                            debug_print(f"DEBUG SWITCH: Added case: value={case_val}, block={case_block_id}, var={var_name}, priority={var_priority}, order={case_info.detection_order}")

                            # BFS: Add ALL successors of this comparison block to the queue
                            # This allows us to find comparison blocks even if they're not directly chained
                            for succ in curr_block_obj.successors:
                                if succ not in visited_blocks and succ in func_block_ids:
                                    to_visit.append((succ, depth + 1))
                                    _switch_debug(f"Added successor {succ} to BFS queue")
                        else:
                            _switch_debug(f"Case block ID not resolved for comparison block {current_block}")

            # If no EQU found, still explore successors (might be a gap in the chain)
            if not found_equ:
                _switch_debug(f"No EQU found in block {current_block}, exploring successors")
                for succ in curr_block_obj.successors:
                    if succ not in visited_blocks and succ in func_block_ids:
                        to_visit.append((succ, depth + 1))

        # Log chain completion statistics
        _switch_debug(f"Chain complete: {len(cases)} cases found")
        if len(cases) < 1:
            _switch_debug(f"Insufficient cases (need 1+), discarding")
            _switch_debug(f"Break reasons: {chain_debug['break_reasons']}")
        else:
            switch_type = "full" if len(cases) >= 2 else "single_case"
            _switch_debug(f"Switch detected: {test_var}, type={switch_type}")

        # PHASE 2 FIX: Select the BEST variable based on priority and frequency
        # If we saw multiple variables during BFS, pick the one with highest priority
        # This handles cases where different blocks use different names for the same value
        if len(cases) >= 1 and variable_frequency:
            _switch_debug(f"Variable frequency: {variable_frequency}")
            _switch_debug(f"Variable priority: {variable_priority}")

            # Find variable with best combination of priority and frequency
            best_var = None
            best_score = -1

            for var_name in variable_frequency:
                # Score = priority * 1000 + frequency
                # This heavily weights priority but uses frequency as tiebreaker
                score = variable_priority.get(var_name, 0) * 1000 + variable_frequency[var_name]
                _switch_debug(f"  {var_name}: priority={variable_priority.get(var_name, 0)}, freq={variable_frequency[var_name]}, score={score}")

                if score > best_score:
                    best_score = score
                    best_var = var_name

            if best_var and best_var != test_var:
                _switch_debug(f"Overriding test_var '{test_var}' with best variable '{best_var}' (score={best_score})")
                test_var = best_var
                test_ssa_value = variable_to_ssa.get(best_var, test_ssa_value)

        # BUGFIX: Deduplicate cases by value (BFS might find same value multiple times)
        # Keep the first occurrence of each case value
        seen_values = set()
        unique_cases = []
        for case in cases:
            if case.value not in seen_values:
                seen_values.add(case.value)
                unique_cases.append(case)
            else:
                _switch_debug(f"Removing duplicate case value={case.value}, block={case.block_id}")

        cases = unique_cases
        filtered_case_sources = {
            (case.value, case.block_id): case_sources[(case.value, case.block_id)]
            for case in cases
            if (case.value, case.block_id) in case_sources
        }

        # Detect fall-through patterns BEFORE body block analysis
        # This detects cases like: case 0: case 3: return 0;
        # where case 0's entry block is a single JMP to case 3's entry block
        fallthrough_map = _detect_case_fallthrough(cfg, cases, resolver)

        # Update cases with fall-through info
        for case in cases:
            if case.value in fallthrough_map:
                case.falls_through_to = fallthrough_map[case.value]
                case.has_break = False  # Fall-through cases don't have break
                _switch_debug(f"Marked case {case.value} as fall-through to case {case.falls_through_to}")

        # Handle shared case bodies (multiple case values mapping to the same entry block).
        # This happens in patterns like:
        #   case 0:
        #   case 3:
        #       return 0;
        # The compiler can point both case values at the same block without an explicit JMP.
        shared_body_map: Dict[int, List[CaseInfo]] = {}
        for case in cases:
            shared_body_map.setdefault(case.block_id, []).append(case)

        for shared_bid, shared_cases in shared_body_map.items():
            if len(shared_cases) <= 1:
                continue
            # Preserve detection order: earlier cases fall through to the last one
            shared_cases_sorted = sorted(shared_cases, key=lambda c: c.detection_order)
            body_case = shared_cases_sorted[-1]
            for shared_case in shared_cases_sorted[:-1]:
                if shared_case.falls_through_to is None:
                    shared_case.falls_through_to = body_case.value
                    shared_case.has_break = False
                    _switch_debug(
                        f"Marked shared-body case {shared_case.value} as fall-through to case {body_case.value} "
                        f"(shared block {shared_bid})"
                    )

        # Determine if this should be a switch statement
        # 3+ cases always becomes a switch
        # 2 cases becomes a switch only if there's a default case OR case values are non-sequential
        # (non-sequential values like 0,2 suggest intentional switch; sequential 0,1 is likely if-else)
        debug_print(f"DEBUG SWITCH: BFS loop complete for block {block_id}: {len(cases)} unique cases collected (duplicates removed)")

        # Use last_chain_block instead of current_block (which might be a body block)
        # The last chain block is the last test/comparison block in the switch chain
        current_block = last_chain_block
        has_default = current_block is not None  # current_block becomes the default block
        case_values_sorted = sorted([c.value for c in cases if c.value is not None])
        non_sequential = len(case_values_sorted) >= 2 and any(
            case_values_sorted[i+1] - case_values_sorted[i] > 1 for i in range(len(case_values_sorted)-1)
        )

        should_be_switch = len(cases) >= 3 or (len(cases) >= 2 and (has_default or non_sequential))
        debug_print(f"DEBUG SWITCH: should_be_switch={should_be_switch} (cases={len(cases)}, has_default={has_default}, non_sequential={non_sequential})")

        if should_be_switch:
            if not _validate_switch_integrity(cases, filtered_case_sources, cfg, start_to_block, resolver):
                if not _is_simple_return_switch(cases, cfg, resolver, start_to_block):
                    _switch_debug(
                        f"Switch integrity check failed for block {block_id}; "
                        "falling back to raw control flow"
                    )
                    continue
                _switch_debug(
                    f"Switch integrity check failed for block {block_id}, "
                    "but simple return-switch heuristic matched"
                )
            debug_print(f"DEBUG SWITCH: Creating switch with {len(cases)} cases on variable '{test_var}'")
            logger.debug(f"Found switch with {len(cases)} cases on variable '{test_var}'")

            # HEURISTIC FIX: For ScriptMain with network message cases, use info->message
            # Network message constants typically include SC_NET_MES_* values (0-20)
            case_values = [case.value for case in cases if case.value is not None]
            debug_print(f"DEBUG SWITCH: Heuristic check - test_var={test_var}, case_values={case_values[:5] if case_values else None}")
            # Check if test_var is a generic parameter AND we're in ScriptMain
            if test_var and test_var.startswith('param_'):
                # Get function name from formatter if available
                func_name = getattr(formatter, 'func_name', None) if formatter else None
                debug_print(f"DEBUG SWITCH: func_name from formatter = {func_name}")
                # For ScriptMain, assume first parameter field (param_0, param_1, param_2) is info->message
                if func_name == "ScriptMain" and case_values and all(isinstance(v, int) and 0 <= v <= 20 for v in case_values):
                    test_var = "info->message"
                    debug_print(f"DEBUG SWITCH: ScriptMain heuristic applied: {test_var}")

            # Find the exit block - the convergence point where all case paths meet
            #
            # BUG FIX: The old algorithm looked at immediate successors of case ENTRY blocks,
            # but those are often body blocks (e.g., if/else branches), not the exit.
            #
            # New algorithm:
            # 1. Pre-scan for nested switch headers (BEFORE body detection)
            # 2. Do preliminary body detection with nested headers as stop barriers
            # 3. Find where body blocks exit TO (successors outside body)
            # 4. The most common such successor is the real exit block
            all_case_blocks = {case.block_id for case in cases}

            # CRITICAL FIX: Pre-scan for nested switch headers BEFORE preliminary body detection
            # This prevents the BFS from traversing INTO nested switch structures
            # which was causing nested switch cases to appear outside their parent switch
            for case in cases:
                if case.falls_through_to is not None:
                    continue
                # Do limited BFS from each case entry to find nested switch headers
                pre_scan_nested = _pre_scan_for_nested_headers(
                    cfg, case.block_id, all_case_blocks, chain_blocks,
                    ssa_func, formatter, start_to_block, resolver, test_var
                )
                nested_switch_headers.update(pre_scan_nested)

            if nested_switch_headers:
                debug_print(f"DEBUG SWITCH: Pre-scan found nested_switch_headers: {sorted(nested_switch_headers)}")

            # Step 1: Find preliminary body blocks for each case
            # Use case entries and nested headers as stop barriers
            # NOTE: Do NOT add chain_blocks to stop - they can be before/after case entries
            # and adding them prevents BFS from finding complete case bodies
            preliminary_stop = all_case_blocks.copy()
            preliminary_stop.update(nested_switch_headers)  # CRITICAL: Include nested headers

            preliminary_bodies: Dict[int, Set[int]] = {}
            for case in cases:
                if case.falls_through_to is not None:
                    preliminary_bodies[case.block_id] = set()
                    continue
                preliminary_bodies[case.block_id] = _find_case_body_blocks(
                    cfg, case.block_id, preliminary_stop, resolver
                )
                # Add this body to stop blocks so next cases don't overlap
                preliminary_stop.update(preliminary_bodies[case.block_id])

            # Step 2: Find exit block - block reached by multiple cases
            # The exit block is where case bodies converge - it has predecessors from multiple cases
            #
            # We look for blocks that are successors of case body blocks and are reached
            # from bodies of different cases.

            # Collect all body blocks per case (for tracking which case reaches what)
            all_preliminary_body = set()
            for body in preliminary_bodies.values():
                all_preliminary_body.update(body)
            all_preliminary_body.update(all_case_blocks)
            all_preliminary_body.update(chain_blocks)

            # Find exit candidates: blocks that are successors of body blocks
            # Track which cases reach each successor
            exit_candidates: Dict[int, Set[int]] = {}  # block_id -> set of case entries that reach it

            for case_entry, body in preliminary_bodies.items():
                for bid in body:
                    block = cfg.blocks.get(bid)
                    if block:
                        for succ in block.successors:
                            if succ not in exit_candidates:
                                exit_candidates[succ] = set()
                            exit_candidates[succ].add(case_entry)

            debug_print(f"DEBUG SWITCH: exit_candidates with reaching cases: {exit_candidates}")

            # Exit block must be reached by ALL cases (or at least multiple)
            # Also, if a block is in a case body but reached by another case, it's an exit
            best_exit = None
            best_score = 0
            for bid, reaching_cases in exit_candidates.items():
                # Skip blocks that are part of the switch structure itself
                if bid in all_case_blocks or bid in chain_blocks:
                    continue

                # PHASE 1.3 FIX: Verify exit isn't a nested structure entry
                # Check if this block starts a nested switch (has JZ/JNZ)
                candidate_block = cfg.blocks.get(bid)
                if candidate_block and candidate_block.instructions:
                    last_instr = candidate_block.instructions[-1]
                    if resolver.is_conditional_jump(last_instr.opcode):
                        # This might be the start of a nested if/else or switch
                        # It's NOT a good exit candidate if it's only reached by one case
                        if len(reaching_cases) == 1:
                            debug_print(f"DEBUG SWITCH: Skipping potential nested structure at {bid}")
                            continue

                # Calculate score: how many DIFFERENT cases reach this block?
                score = len(reaching_cases)

                # Bonus: if this block is already in some case's body but also reached
                # by other cases, it's a strong exit candidate
                if bid in all_preliminary_body and len(reaching_cases) > 1:
                    score += 10  # Strong indicator

                # Prefer blocks reached by MORE cases
                if score > best_score:
                    best_score = score
                    best_exit = bid
                    debug_print(f"DEBUG SWITCH: New best exit: {bid} with score {score} (reached by {reaching_cases})")

            exit_candidates_simple: Dict[int, int] = {
                bid: len(cases) for bid, cases in exit_candidates.items()
                if bid not in all_case_blocks and bid not in chain_blocks
            }
            debug_print(f"DEBUG SWITCH: exit_candidates (simplified): {exit_candidates_simple}")

            # The exit block is the best candidate from our analysis
            exit_block = best_exit
            if exit_block is not None:
                debug_print(f"DEBUG SWITCH: Selected exit_block: {exit_block}")

                # FÁZE 1.3 FIX: If exit block is just a JMP, follow it to find the real exit
                exit_blk = cfg.blocks.get(exit_block)
                if exit_blk and exit_blk.instructions and len(exit_blk.instructions) == 1:
                    instr = exit_blk.instructions[0]
                    mnem = resolver.get_mnemonic(instr.opcode)
                    if mnem == "JMP":
                        # Follow the JMP to find real exit
                        real_exit = start_to_block.get(instr.arg1)
                        if real_exit is not None:
                            debug_print(f"DEBUG SWITCH: Following JMP from {exit_block} to real exit {real_exit}")
                            exit_block = real_exit

            # Collect all blocks belonging to the switch (initially just chain and case entries)
            debug_print(f"DEBUG SWITCH: Building all_blocks for {test_var}, chain_blocks={chain_blocks}, header_block={block_id}")
            all_blocks = set(chain_blocks)
            all_blocks.add(block_id)  # CRITICAL FIX: Always include header block
            all_blocks.update(all_case_blocks)
            debug_print(f"DEBUG SWITCH: all_blocks after adding chain and cases: {all_blocks}")
            if current_block is not None:
                all_blocks.add(current_block)  # default block

            # Find body blocks for each case using graph traversal
            # Build stop blocks: all case entries + exit + default
            stop_blocks = all_case_blocks.copy()
            debug_print(f"DEBUG SWITCH: Initial stop_blocks (case entries): {sorted(stop_blocks)}")
            # NOTE: Do NOT add chain_blocks to stop_blocks. When a case entry IS a chain block
            # (comparison falls through to case body), adding it to stop_blocks causes BFS to
            # stop immediately, resulting in empty case bodies. The all_case_blocks set already
            # provides sufficient boundaries between cases.
            debug_print(f"DEBUG SWITCH: chain_blocks (NOT added to stop_blocks): {sorted(chain_blocks)}")

            # FIX (01-24): Do NOT add nested_switch_headers to stop_blocks
            # Instead, let them be included in case bodies and detected as nested switches later
            # The nested_switch_headers will be stored in SwitchPattern.nested_headers for reference
            if nested_switch_headers:
                debug_print(f"DEBUG SWITCH: Found nested_switch_headers (will NOT add to stop_blocks): {sorted(nested_switch_headers)}")

            if exit_block is not None:
                debug_print(f"DEBUG SWITCH: Adding exit_block to stop_blocks: {exit_block}")
                stop_blocks.add(exit_block)
            if current_block is not None:
                # NOTE: Do NOT add current_block to stop_blocks here.
                # current_block is the last test block (part of chain_blocks), and adding it
                # would prevent BFS from finding case bodies that come after case entries
                # but before the next test block in the comparison chain.

                # FIX #1 PART 2: Find the actual default entry block
                # current_block is the last test block (e.g., block 18 at 091)
                # The default entry is typically the non-case branch of the last comparison.
                default_entry = None
                curr_blk = cfg.blocks.get(current_block)
                if curr_blk and curr_blk.instructions:
                    compare_to_case = {
                        compare_block_id: case_block_id
                        for (case_value, case_block_id), compare_block_id in filtered_case_sources.items()
                    }
                    case_block_id = compare_to_case.get(current_block)
                    default_candidates = []
                    for compare_block_id, compare_case_block_id in compare_to_case.items():
                        compare_blk = cfg.blocks.get(compare_block_id)
                        if not compare_blk:
                            continue
                        cmp_jump, cmp_fallthrough = _resolve_conditional_targets(
                            compare_blk, start_to_block, resolver
                        )
                        if cmp_jump is None or cmp_fallthrough is None:
                            continue
                        if compare_case_block_id == cmp_jump:
                            candidate = cmp_fallthrough
                        elif compare_case_block_id == cmp_fallthrough:
                            candidate = cmp_jump
                        else:
                            continue
                        if candidate in chain_blocks or candidate in all_case_blocks:
                            continue
                        default_candidates.append(candidate)
                    if default_candidates:
                        default_entry = min(
                            default_candidates,
                            key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else bid
                        )

                    jump_target, fallthrough = _resolve_conditional_targets(
                        curr_blk, start_to_block, resolver
                    )

                    if default_entry is None and jump_target is not None and fallthrough is not None:
                        if case_block_id is not None:
                            if case_block_id == jump_target:
                                default_entry = fallthrough
                            elif case_block_id == fallthrough:
                                default_entry = jump_target
                        if default_entry is None:
                            for candidate in (jump_target, fallthrough):
                                if candidate not in chain_blocks and candidate not in all_case_blocks:
                                    default_entry = candidate
                                    break
                    if default_entry is None:
                        last_test_instr = curr_blk.instructions[-1]
                        test_mnem = resolver.get_mnemonic(last_test_instr.opcode)
                        if test_mnem == "JMP":
                            # Direct JMP to default
                            target_addr = last_test_instr.arg1
                            for bid, b in cfg.blocks.items():
                                if b.start == target_addr:
                                    default_entry = bid
                                    break

                # Add default entry to stop blocks so cases don't leak into default
                if default_entry is not None:
                    stop_blocks.add(default_entry)

            # PHASE 1.2: Two-pass case body detection
            # Pass 1: Find preliminary bodies to identify break blocks
            # Pass 2: Re-run with break blocks from ALL cases as stop blocks

            # Pass 1: Preliminary body detection
            _switch_debug(f"Pass 1: Preliminary body detection for {len(cases)} cases")
            preliminary_bodies: Dict[int, Set[int]] = {}
            preliminary_stop = set(stop_blocks)

            for case in cases:
                if case.falls_through_to is not None:
                    preliminary_bodies[case.block_id] = set()
                    continue

                preliminary_bodies[case.block_id] = _find_case_body_blocks(
                    cfg, case.block_id, preliminary_stop, resolver,
                    known_exit_blocks={exit_block} if exit_block else None
                )
                # Add this case's body to stop_blocks for next cases
                preliminary_stop.update(preliminary_bodies[case.block_id])

            # Identify break blocks: single-instruction JMP blocks targeting exit
            break_blocks: Set[int] = set()
            for case in cases:
                for body_bid in preliminary_bodies.get(case.block_id, set()):
                    body_block = cfg.blocks.get(body_bid)
                    if not body_block or not body_block.instructions:
                        continue
                    if len(body_block.instructions) == 1:
                        instr = body_block.instructions[0]
                        mnem = resolver.get_mnemonic(instr.opcode)
                        if mnem == "JMP":
                            # Find target block
                            target_addr = instr.arg1
                            target_block = None
                            for bid, b in cfg.blocks.items():
                                if b.start == target_addr:
                                    target_block = bid
                                    break
                            # If target is exit block or outside all preliminary bodies, it's a break
                            if target_block == exit_block:
                                break_blocks.add(body_bid)
                            elif target_block is not None:
                                is_in_any_body = any(
                                    target_block in pb
                                    for pb in preliminary_bodies.values()
                                )
                                if not is_in_any_body and target_block not in all_case_blocks:
                                    break_blocks.add(body_bid)

            _switch_debug(f"Identified {len(break_blocks)} break blocks: {sorted(break_blocks)}")

            # Pass 2: Final body detection with break blocks from other cases as stop blocks
            _switch_debug(f"Pass 2: Final body detection with break block barriers")
            for case in cases:
                # Skip body detection for fall-through cases - they have no body, just a label
                if case.falls_through_to is not None:
                    case.body_blocks = set()  # No body - just a label that falls through
                    _switch_debug(f"Skipping body detection for fall-through case {case.value}")
                    continue

                # Build stop blocks: include break blocks from OTHER cases
                pass2_stop = set(stop_blocks)
                for other_case in cases:
                    if other_case.block_id != case.block_id:
                        # Add break blocks from other cases
                        other_body = preliminary_bodies.get(other_case.block_id, set())
                        for bb in break_blocks:
                            if bb in other_body:
                                pass2_stop.add(bb)

                debug_print(f"DEBUG SWITCH: Finding body for case {case.value}, entry={case.block_id}, stop_blocks={sorted(pass2_stop)}")
                case.body_blocks = _find_case_body_blocks(
                    cfg, case.block_id, pass2_stop, resolver,
                    known_exit_blocks={exit_block} if exit_block else None
                )
                debug_print(f"DEBUG SWITCH: Case {case.value} body_blocks: {sorted(case.body_blocks)}")
                # BUG FIX #3: Add this case's body to stop_blocks so next cases don't cross into it
                stop_blocks.update(case.body_blocks)
                # Update all_blocks to include all case body blocks
                all_blocks.update(case.body_blocks)

            # Also find body blocks for default case if present
            default_body = None
            if current_block is not None:
                # FIX #1 PART 3: Use default_entry if found, otherwise use current_block
                # Remove default_entry from stop_blocks temporarily so BFS can include it
                default_body_entry = default_entry if default_entry is not None else current_block
                if default_entry is not None and default_entry in stop_blocks:
                    stop_blocks.remove(default_entry)

                # BUG FIX: If default_entry equals exit_block, there is NO explicit default case.
                # The "default" path just falls through to the post-switch code (exit_block).
                # In this case, we should NOT create a default body, otherwise the post-switch
                # code will be incorrectly rendered inside the default case.
                debug_print(f"DEBUG SWITCH: Checking default: default_body_entry={default_body_entry}, exit_block={exit_block}, default_entry={default_entry}")
                if default_body_entry == exit_block:
                    debug_print(f"DEBUG SWITCH: No explicit default case - default_entry equals exit_block ({exit_block})")
                    default_body = None
                    current_block = None  # Clear to signal no default
                else:
                    default_body = _find_case_body_blocks(
                        cfg, default_body_entry, stop_blocks, resolver,
                        known_exit_blocks={exit_block} if exit_block else None
                    )
                    debug_print(f"DEBUG SWITCH: Found default body blocks: {default_body}")

                    # BUG FIX #2: Check if the "default body" is actually just the exit point.
                    # If the default body is a single block that starts AFTER all case bodies,
                    # it's the post-switch code (common exit), not a real default case.
                    if default_body and len(default_body) == 1:
                        potential_exit = next(iter(default_body))
                        potential_exit_blk = cfg.blocks.get(potential_exit)

                        if potential_exit_blk:
                            potential_exit_addr = potential_exit_blk.start
                            # Find the maximum address of any case body block
                            max_case_addr = 0
                            for case in cases:
                                for body_bid in case.body_blocks:
                                    body_blk = cfg.blocks.get(body_bid)
                                    if body_blk:
                                        max_case_addr = max(max_case_addr, body_blk.end)

                            debug_print(f"DEBUG SWITCH: Checking if {potential_exit} (addr {potential_exit_addr}) is after all case bodies (max addr {max_case_addr})")

                            # If the potential exit block starts after all case bodies, it's post-switch code
                            if potential_exit_addr >= max_case_addr:
                                # Special case: switch-return functions often have a single return block
                                # as the implicit default. Keep it if there's no common exit block.
                                if exit_block is None and _block_ends_with_return(cfg, potential_exit, resolver):
                                    debug_print(
                                        "DEBUG SWITCH: Keeping default body as return-only block "
                                        f"for switch-return function (default_body={default_body})"
                                    )
                                else:
                                    debug_print(
                                        f"DEBUG SWITCH: No explicit default case - default body {default_body} is post-switch code"
                                    )
                                    default_body = None
                                    current_block = None

                    if default_body:
                        all_blocks.update(default_body)

            # FIX #1: Detect break statements in each case
            # Analyze each case's exit behavior to determine if it has break
            # IMPORTANT: Skip fall-through cases - their has_break was already set to False
            for case in cases:
                if case.falls_through_to is not None:
                    # Fall-through cases don't have break - already set above
                    continue
                case.has_break = _case_has_break(cfg, case, exit_block, resolver)

            # Determine switch type for rendering
            switch_type = "full" if len(cases) >= 2 else "single_case"

            switch = SwitchPattern(
                test_var=test_var,
                header_block=block_id,
                cases=cases,
                default_block=current_block,  # Last block in chain is default
                default_body_blocks=default_body,
                exit_block=exit_block,
                all_blocks=all_blocks,
                nested_headers=nested_switch_headers.copy() if nested_switch_headers else set(),
                dispatch_blocks=set(chain_blocks),
                _internal_type=switch_type,
            )
            debug_print(f"DEBUG SWITCH: Appending switch to switches list: {test_var} with {len(cases)} cases, all_blocks={sorted(all_blocks)}")
            switches.append(switch)
            processed_blocks.update(chain_blocks)

    # FIX #2: Prioritize switches by importance
    # Parameter field switches (e.g., info->message) are most important
    # Global variable switches are medium priority
    # Local variable switches are lowest priority
    def _rank_switch_importance(sw: SwitchPattern) -> int:
        """
        Rank switch importance for prioritization.

        Returns:
            Higher number = higher priority
            100+ = Parameter field access (info->message, info->param1, etc.)
            50-99 = Global variable (gphase, g_dialog, etc.)
            0-49 = Local variable or unknown
        """
        var_name = sw.test_var

        # Parameter field access = highest priority (most likely main switch)
        if "->" in var_name:
            # Check if it's a parameter field (starts with param name like "info", "data", etc.)
            # Common parameter names: info, data, param, msg
            param_prefixes = ["info->", "data->", "param->", "msg->", "event->"]
            if any(var_name.startswith(prefix) for prefix in param_prefixes):
                return 100
            # Other struct field access
            return 90

        # Global variable = medium priority
        # Globals typically start with 'g' or have specific prefixes
        if var_name.startswith("g") or var_name.startswith("_g"):
            return 50

        # Check for common global patterns
        global_patterns = ["phase", "state", "mode", "flag", "status"]
        if any(pattern in var_name.lower() for pattern in global_patterns):
            return 45

        # Local variable or unknown = lowest priority
        # These include local_, tmp, var, etc.
        if var_name.startswith("local_") or var_name.startswith("tmp") or var_name.startswith("var"):
            return 10

        # Unknown/other = low-medium priority
        return 30

    # Sort switches by importance (highest priority first)
    if len(switches) > 1:
        switches.sort(key=_rank_switch_importance, reverse=True)

    return switches


def _infer_parameter_semantic_name(var_value, generic_name: str, ssa_func: SSAFunction, formatter: ExpressionFormatter) -> Optional[str]:
    """
    PHASE 8B Priority 1: Try to infer semantic parameter name from usage patterns.

    This is a placeholder for future enhancement. Currently returns None,
    which means the generic parameter name (param_0, param_1, etc.) will be used.

    Future enhancements could analyze:
    - Parameter usage patterns (e.g., passed to functions with known signatures)
    - Comparisons against known constants (e.g., sides: 0=VC, 1=US, 2=NE)
    - Arithmetic patterns that suggest semantic meaning

    Args:
        var_value: SSA value representing the parameter
        generic_name: Generic name like "param_0", "param_1"
        ssa_func: SSA function context
        formatter: Expression formatter

    Returns:
        Semantic name if inferred, None otherwise
    """
    # Future: Could analyze how parameter is used:
    # - Passed to functions with known signatures
    # - Compared against known constants (e.g., sides: 0=VC, 1=US, 2=NE)
    # - Used in arithmetic patterns

    # For now, keep generic name
    # The important fix is that the switch is DETECTED, even with generic name
    return None
