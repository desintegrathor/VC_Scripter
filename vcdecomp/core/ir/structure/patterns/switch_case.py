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

logger = logging.getLogger(__name__)

# Environment-controlled debug logging for switch detection
SWITCH_DEBUG = os.environ.get('VCDECOMP_SWITCH_DEBUG', '0') == '1'

def _switch_debug(msg: str):
    """
    Output debug messages for switch detection when enabled.
    Enable with: VCDECOMP_SWITCH_DEBUG=1
    """
    if SWITCH_DEBUG:
        print(f"[SWITCH] {msg}", file=sys.stderr)


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
    """
    import sys

    # Search through SSA instructions (which have correct mnemonics)
    ssa_blocks = ssa_func.instructions  # Dict[block_id, List[SSAInstruction]]

    # Find the FIRST (earliest) GCP/GLD instruction in the entire function
    # that loads a global variable - this is likely the switch variable
    gcp_candidates = []

    # Collect all GCP/GLD from all SSA blocks in function
    for block_id in func_block_ids:
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

    # If we found any GCP, use the FIRST one (earliest in function)
    if gcp_candidates:
        # Sort by instruction address (earliest first)
        gcp_candidates.sort(key=lambda x: x[0])
        # Return the first global variable name
        return gcp_candidates[0][1]

    return None


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
    print(f"DEBUG SWITCH: ScriptMain area blocks (1090-1200): {sorted(scriptmain_blocks)}", file=sys.stderr)
    print(f"DEBUG SWITCH: ScriptMain blocks in func_block_ids: {sorted(scriptmain_in_func)}", file=sys.stderr)
    if scriptmain_missing:
        print(f"DEBUG SWITCH: ScriptMain blocks MISSING from func_block_ids: {sorted(scriptmain_missing)}", file=sys.stderr)
        for bid in sorted(scriptmain_missing):
            if bid in cfg.blocks:
                block = cfg.blocks[bid]
                print(f"DEBUG SWITCH:   Block {bid}: start={block.start}, end={block.end}, preds={len(block.predecessors)}", file=sys.stderr)

    # Iterate through blocks looking for switch headers
    for block_id in func_block_ids:
        if block_id in processed_blocks:
            continue

        block = cfg.blocks.get(block_id)
        if not block or not block.instructions:
            continue

        logger.debug(f"Checking block {block_id} for switch pattern (start addr: {block.start})")
        print(f"DEBUG SWITCH: Checking block {block_id} for switch pattern (start addr: {block.start})", file=sys.stderr)

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

        # Chain tracking state for debug
        chain_debug = {
            'blocks_processed': [],
            'break_reasons': [],
            'variables_seen': [],
            'ssa_values_seen': []
        }

        # BFS state: blocks to visit with their depth
        visited_blocks = set()
        to_visit = [(block_id, 0)]  # (block_id, depth)
        max_bfs_depth = 15  # Reasonable limit to avoid exploring too far

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
                                base_name = _trace_value_to_global(base_var, formatter)
                            if not base_name:
                                # Phase 8B.1: Use multi-block SSA tracing for complex cases
                                producer = _follow_ssa_value_across_blocks(base_var, ssa_func, max_depth=10)
                                if producer:
                                    if producer.mnemonic == 'LCP':
                                        # Parameter load - try to resolve again with producer context
                                        base_name = _trace_value_to_parameter(base_var, formatter, ssa_func)
                                    elif producer.mnemonic in {'GCP', 'GLD'}:
                                        # Global load - try to resolve again with producer context
                                        base_name = _trace_value_to_global(base_var, formatter)
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
                    var_name = _trace_value_to_global(var_value, formatter)
                    if var_name:
                        _switch_debug(f"  -> Found global: {var_name}")

                if not var_name:
                    var_name = _trace_value_to_function_call(ssa_func, var_value, formatter)
                    if var_name:
                        _switch_debug(f"  -> Found function call result: {var_name}")

                # CRITICAL FIX for Switch Variable Tracking:
                # If normal tracing failed, use heuristic to find switch variable
                # from nearby GCP instructions. This is needed because compiler generates
                # code where global is loaded once at function entry but not properly
                # propagated through CFG to switch comparison blocks.
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

                # Track this variable's frequency and priority
                variable_frequency[var_name] = variable_frequency.get(var_name, 0) + 1
                variable_priority[var_name] = max(variable_priority.get(var_name, 0), var_priority)
                variable_to_ssa[var_name] = var_value

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
                    print(f"DEBUG SWITCH: First case - variable: {test_var}, SSA: {var_value.name if hasattr(var_value, 'name') else var_value}", file=sys.stderr)
                elif test_var != var_name:
                    # NESTED SWITCH FIX: Different variable = likely nested switch
                    # Skip this block - it will be processed when we analyze the case body
                    _switch_debug(f"Different variable seen: {test_var} -> {var_name} (skipping - likely nested switch)")
                    chain_debug['variables_seen'].append(var_name)
                    chain_debug['ssa_values_seen'].append(var_value.name if hasattr(var_value, 'name') else str(var_value))
                    print(f"DEBUG SWITCH: Variable mismatch - test_var: {test_var}, new var_name: {var_name} (skipping - nested switch)", file=sys.stderr)
                    # Don't add successors for nested switch blocks - let them be detected later
                    continue

                # Same variable (or first case), try to extract constant value using ConstantPropagator
                _switch_debug(f"About to extract constant from: {const_value.name if hasattr(const_value, 'name') else const_value}")
                print(f"DEBUG SWITCH: About to extract constant from: {const_value.name if hasattr(const_value, 'name') else const_value}", file=sys.stderr)
                case_val = None
                const_info = formatter._constant_propagator.get_constant(const_value)
                if const_info is not None:
                    case_val = const_info.value
                    _switch_debug(f"  Successfully extracted case value: {case_val}")
                    print(f"DEBUG SWITCH: Successfully extracted case value: {case_val}", file=sys.stderr)
                else:
                    _switch_debug(f"  Failed to extract constant - const_value alias={const_value.alias if hasattr(const_value, 'alias') else 'None'}, producer={const_value.producer_inst.mnemonic if const_value.producer_inst else 'None'}")
                    print(f"DEBUG SWITCH: Failed to extract constant for SSA value: {const_value.name}", file=sys.stderr)

                if case_val is not None:
                        # This is a valid case!
                        print(f"DEBUG SWITCH: case_val is not None: {case_val}", file=sys.stderr)
                        # Determine which successor is the case body
                        # JZ means jump if zero (condition false), so arg1 is NOT the case
                        # JNZ means jump if not zero (condition true), so arg1 IS the case
                        mnemonic = resolver.get_mnemonic(opcode)
                        print(f"DEBUG SWITCH: mnemonic={mnemonic}, opcode={opcode}", file=sys.stderr)
                        if mnemonic == "JNZ":
                            case_block = last_instr.arg1
                        else:  # JZ
                            # Fall-through is the case body
                            case_block = last_instr.address + 1

                        print(f"DEBUG SWITCH: case_block address={case_block}", file=sys.stderr)

                        # Convert address to block ID
                        case_block_id = None
                        for bid, b in cfg.blocks.items():
                            if b.start == case_block:
                                case_block_id = bid
                                break

                        print(f"DEBUG SWITCH: case_block_id={case_block_id}", file=sys.stderr)
                        if case_block_id is not None:
                            # PHASE 3 FIX: Store all potential cases with their variable info
                            # Don't filter yet - we'll do that after BFS completes
                            case_info = CaseInfo(value=case_val, block_id=case_block_id)
                            all_potential_cases.append((var_name, var_priority, var_value, case_info, current_block))

                            # TEMPORARY: Also add to old structure for compatibility
                            cases.append(case_info)
                            chain_blocks.append(current_block)
                            found_equ = True
                            print(f"DEBUG SWITCH: Added case: value={case_val}, block={case_block_id}, var={var_name}, priority={var_priority}", file=sys.stderr)

                            # BFS: Add ALL successors of this comparison block to the queue
                            # This allows us to find comparison blocks even if they're not directly chained
                            for succ in curr_block_obj.successors:
                                if succ not in visited_blocks and succ in func_block_ids:
                                    to_visit.append((succ, depth + 1))
                                    _switch_debug(f"Added successor {succ} to BFS queue")
                        else:
                            _switch_debug(f"Case block ID not found for address {case_block}")

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

        # If we found at least 3 cases, it's a switch
        # (1-2 cases are just regular if/else statements, not switch)
        print(f"DEBUG SWITCH: BFS loop complete for block {block_id}: {len(cases)} unique cases collected (duplicates removed)", file=sys.stderr)
        if len(cases) >= 3:
            print(f"DEBUG SWITCH: Creating switch with {len(cases)} cases on variable '{test_var}'", file=sys.stderr)
            logger.debug(f"Found switch with {len(cases)} cases on variable '{test_var}'")

            # HEURISTIC FIX: For ScriptMain with network message cases, use info->message
            # Network message constants typically include SC_NET_MES_* values (0-20)
            case_values = [case.value for case in cases if case.value is not None]
            print(f"DEBUG SWITCH: Heuristic check - test_var={test_var}, case_values={case_values[:5] if case_values else None}", file=sys.stderr)
            # Check if test_var is a generic parameter AND we're in ScriptMain
            if test_var and test_var.startswith('param_'):
                # Get function name from formatter if available
                func_name = getattr(formatter, 'func_name', None) if formatter else None
                print(f"DEBUG SWITCH: func_name from formatter = {func_name}", file=sys.stderr)
                # For ScriptMain, assume first parameter field (param_0, param_1, param_2) is info->message
                if func_name == "ScriptMain" and case_values and all(isinstance(v, int) and 0 <= v <= 20 for v in case_values):
                    test_var = "info->message"
                    print(f"DEBUG SWITCH: ScriptMain heuristic applied: {test_var}", file=sys.stderr)

            # Find the exit block - common successor of all case blocks
            # For now, we'll use a simple heuristic: find the most common successor
            # that is not part of the switch itself
            all_case_blocks = {case.block_id for case in cases}
            exit_candidates: Dict[int, int] = {}  # block_id -> count

            for case in cases:
                # Find successors of the case block
                case_block = cfg.blocks.get(case.block_id)
                if case_block:
                    for succ in case_block.successors:
                        if succ not in all_case_blocks and succ not in chain_blocks:
                            exit_candidates[succ] = exit_candidates.get(succ, 0) + 1

            # The exit block is the one referenced by most cases
            exit_block = None
            if exit_candidates:
                exit_block = max(exit_candidates.items(), key=lambda x: x[1])[0]

                # FÁZE 1.3 FIX: If exit block is just a JMP, follow it to find the real exit
                exit_blk = cfg.blocks.get(exit_block)
                if exit_blk and exit_blk.instructions and len(exit_blk.instructions) == 1:
                    instr = exit_blk.instructions[0]
                    mnem = resolver.get_mnemonic(instr.opcode)
                    if mnem == "JMP":
                        # Follow the JMP to find real exit
                        real_exit = start_to_block.get(instr.arg1)
                        if real_exit is not None:
                            exit_block = real_exit

            # Collect all blocks belonging to the switch (initially just chain and case entries)
            print(f"DEBUG SWITCH: Building all_blocks for {test_var}, chain_blocks={chain_blocks}, header_block={block_id}", file=sys.stderr)
            all_blocks = set(chain_blocks)
            all_blocks.add(block_id)  # CRITICAL FIX: Always include header block
            all_blocks.update(all_case_blocks)
            print(f"DEBUG SWITCH: all_blocks after adding chain and cases: {all_blocks}", file=sys.stderr)
            if current_block is not None:
                all_blocks.add(current_block)  # default block

            # Find body blocks for each case using graph traversal
            # Build stop blocks: all case entries + exit + default
            stop_blocks = all_case_blocks.copy()
            # BUG FIX: Add chain blocks (test blocks) to prevent BFS from crossing into next case test
            stop_blocks.update(chain_blocks)
            if exit_block is not None:
                stop_blocks.add(exit_block)
            if current_block is not None:
                stop_blocks.add(current_block)

                # FIX #1 PART 2: Find the actual default entry block
                # current_block is the last test block (e.g., block 18 at 091)
                # The default entry is typically the fall-through or jump target
                default_entry = None
                curr_blk = cfg.blocks.get(current_block)
                if curr_blk and curr_blk.instructions:
                    last_test_instr = curr_blk.instructions[-1]
                    test_mnem = resolver.get_mnemonic(last_test_instr.opcode)

                    # If it's a conditional jump (JZ), default is either target or fall-through
                    if resolver.is_conditional_jump(last_test_instr.opcode):
                        # JZ jumps on false (zero), so target is next test or default
                        target_addr = last_test_instr.arg1
                        fall_through_addr = last_test_instr.address + 1

                        # Find which one is the default (not in chain_blocks)
                        for bid, b in cfg.blocks.items():
                            if b.start == target_addr and bid not in chain_blocks:
                                default_entry = bid
                                break
                            elif b.start == fall_through_addr and bid not in chain_blocks:
                                default_entry = bid
                                break
                    elif test_mnem == "JMP":
                        # Direct JMP to default
                        target_addr = last_test_instr.arg1
                        for bid, b in cfg.blocks.items():
                            if b.start == target_addr:
                                default_entry = bid
                                break

                # Add default entry to stop blocks so cases don't leak into default
                if default_entry is not None:
                    stop_blocks.add(default_entry)

            # For each case, find all blocks in its body
            for case in cases:
                case.body_blocks = _find_case_body_blocks(
                    cfg, case.block_id, stop_blocks, resolver
                )
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

                default_body = _find_case_body_blocks(
                    cfg, default_body_entry, stop_blocks, resolver
                )
                all_blocks.update(default_body)

            # FIX #1: Detect break statements in each case
            # Analyze each case's exit behavior to determine if it has break
            for case in cases:
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
                _internal_type=switch_type,
            )
            print(f"DEBUG SWITCH: Appending switch to switches list: {test_var} with {len(cases)} cases", file=sys.stderr)
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
