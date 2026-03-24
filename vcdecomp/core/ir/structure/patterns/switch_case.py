"""
Switch/case pattern detection for control flow analysis.

This module contains functions for detecting switch/case patterns in the CFG,
including the main switch pattern detection and helper functions for finding
switch variables from nearby global variable loads.
"""

from __future__ import annotations

from typing import Dict, Set, List, Optional
from dataclasses import dataclass
import logging
import sys
import os

from ...cfg import CFG, NaturalLoop, find_all_loops
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
    _check_ssa_value_equivalence,
    _has_dcp_producer_in_phi,
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


@dataclass
class SwitchVariableCandidate:
    """A candidate switch variable with confidence score from a specific tracer."""
    name: str           # e.g., "gphase", "info->message", "param_0%4"
    confidence: int     # 0-100
    source: str         # tracer tag for debug logging
    is_expression: bool = False  # True for "param_0%4" etc.


def _compute_frame_def_has_dcp(var_value, ssa_func) -> Optional[bool]:
    """Check if the reaching definition for var_value's frame slot involves DCP.

    Returns:
        True  = DCP in reaching def (value likely from parameter field access)
        False = no DCP (value from global, function call, etc.)
        None  = unknown (no metadata or SSA info available)
    """
    if not ssa_func or not var_value or not hasattr(var_value, 'metadata'):
        return None
    frame_version = var_value.metadata.get('frame_def_version')
    if not frame_version:
        return None
    if not hasattr(ssa_func, 'values') or frame_version not in ssa_func.values:
        return None
    def_value = ssa_func.values[frame_version]
    return _has_dcp_producer_in_phi(def_value, ssa_func, max_depth=5)


def _try_resolve_mod_expression(
    var_value, current_block, ssa_func, formatter
) -> Optional[str]:
    """Try to resolve a MOD (modulo) expression for the switch variable.

    Extracts the 'base_var % constant' pattern from bytecode. Handles three
    strategies for matching MOD output to LCP input:
    1. Alias matching (MOD output alias == LCP alias)
    2. Dead header pattern (MOD last in predecessor, LCP first in current)
    3. ASGN store pattern (MOD result stored via ASGN to same location)

    Returns the expression string (e.g., "param_0%4") or None.
    """
    actual_producer = var_value.producer_inst
    if not actual_producer:
        return None

    # If producer is LCP, search predecessor blocks for MOD
    if actual_producer.mnemonic == 'LCP':
        lcp_alias = var_value.alias

        # Extract stack offset from LCP instruction
        lcp_offset = None
        if (actual_producer.instruction and
            actual_producer.instruction.instruction):
            raw_offset = actual_producer.instruction.instruction.arg1
            lcp_offset = raw_offset - 0x100000000 if raw_offset >= 0x80000000 else raw_offset
            _switch_debug(f"  LCP stack offset: {lcp_offset}")

        # Search current block and predecessors for MOD instruction
        mod_inst = _find_mod_in_predecessors(current_block, ssa_func, max_depth=2)
        if mod_inst:
            mod_matches = False

            # Strategy 1: Check if MOD has output with matching alias
            if mod_inst.outputs:
                for out in mod_inst.outputs:
                    if out.alias == lcp_alias:
                        mod_matches = True
                        _switch_debug(f"  -> MOD matched via alias: {lcp_alias}")
                        break

            # Strategy 2: Dead header pattern
            if not mod_matches and lcp_offset is not None:
                mod_block_id = _get_instruction_block(mod_inst, ssa_func)
                if mod_block_id is not None:
                    cfg = ssa_func.cfg
                    mod_block = cfg.get_block(mod_block_id)
                    if mod_block:
                        if (current_block == mod_block_id or
                            current_block in mod_block.successors):
                            mod_is_last_op = False
                            mod_ssa_block = ssa_func.instructions.get(mod_block_id, [])
                            real_ops = [i for i in mod_ssa_block if i.address >= 0]
                            for idx_m, inst_m in enumerate(real_ops):
                                if inst_m is mod_inst:
                                    remaining = real_ops[idx_m+1:]
                                    mod_is_last_op = all(
                                        r.mnemonic == 'JMP' for r in remaining
                                    ) if remaining else True
                                    break

                            lcp_is_first = False
                            cmp_ssa_block = ssa_func.instructions.get(current_block, [])
                            cmp_real = [i for i in cmp_ssa_block if i.address >= 0]
                            if cmp_real and cmp_real[0].mnemonic == 'LCP':
                                lcp_is_first = True

                            if mod_is_last_op and lcp_is_first:
                                mod_matches = True
                                _switch_debug(f"  -> MOD matched via dead header pattern (MOD in block {mod_block_id}, LCP [sp+{lcp_offset}] first in block {current_block})")

                    # Strategy 3: ASGN store pattern
                    if not mod_matches and mod_inst.address is not None:
                        mod_block_insts = ssa_func.instructions.get(current_block, [])
                        for check_inst in mod_block_insts:
                            if (check_inst.mnemonic == 'ASGN' and
                                len(check_inst.inputs) >= 2 and
                                check_inst.inputs[1].alias and
                                check_inst.inputs[1].alias.startswith('&') and
                                check_inst.inputs[1].alias[1:] == lcp_alias):
                                mod_matches = True
                                _switch_debug(f"  -> MOD matched via ASGN pattern")
                                break

            if mod_matches:
                actual_producer = mod_inst
                _switch_debug(f"  -> Found MOD in predecessor block (same variable {lcp_alias})")
            else:
                _switch_debug(f"  -> Found MOD in predecessor block but for different variable")

    if actual_producer and actual_producer.mnemonic == "MOD":
        if len(actual_producer.inputs) >= 2:
            base_var = actual_producer.inputs[0]
            mod_value = actual_producer.inputs[1]

            # Try to get base variable name
            base_name = _trace_value_to_parameter(base_var, formatter, ssa_func)
            if not base_name:
                base_name = _trace_value_to_global(base_var, formatter, ssa_func)
            if not base_name:
                producer = _follow_ssa_value_across_blocks(base_var, ssa_func, max_depth=10)
                if producer:
                    if producer.mnemonic == 'LCP':
                        base_name = _trace_value_to_parameter(base_var, formatter, ssa_func)
                    elif producer.mnemonic in {'GCP', 'GLD'}:
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
                result = f"{base_name}%{mod_const}"
                _switch_debug(f"  -> Detected modulo switch: {result}")
                return result

    return None


def _resolve_switch_variable(
    var_value, current_block, ssa_func, formatter, func_block_ids
) -> SwitchVariableCandidate:
    """Run ALL variable resolution tracers and pick the best candidate by confidence.

    Replaces the old first-match-wins waterfall with a unified scoring system.
    Each tracer assigns a base confidence score. When the frame slot's reaching
    definition has no DCP (meaning it doesn't come from a parameter field access),
    parameter-based tracers are penalized to 0.
    """
    candidates = []
    frame_has_dcp = _compute_frame_def_has_dcp(var_value, ssa_func)
    _switch_debug(f"  frame_has_dcp: {frame_has_dcp}")

    # 1. MOD structural pattern (confidence 95)
    mod_name = _try_resolve_mod_expression(var_value, current_block, ssa_func, formatter)
    if mod_name:
        candidates.append(SwitchVariableCandidate(
            name=mod_name, confidence=95, source="mod_expression", is_expression=True
        ))

    # 2. Dead GCP/LCP header (confidence 90)
    dead_gcp_name = _find_dead_gcp_in_predecessor(ssa_func, current_block, formatter)
    if dead_gcp_name:
        candidates.append(SwitchVariableCandidate(
            name=dead_gcp_name, confidence=90, source="dead_gcp_header"
        ))

    # 3. Global variable trace (confidence 70, boosted to 80 when no DCP)
    global_name = _trace_value_to_global(var_value, formatter, ssa_func, skip_dcp_guard=True)
    if global_name:
        conf = 80 if frame_has_dcp is False else 70
        candidates.append(SwitchVariableCandidate(
            name=global_name, confidence=conf, source="global_trace"
        ))

    # 4. Parameter field access (confidence 75, dropped to 0 when no DCP)
    param_field_name = _trace_value_to_parameter_field(var_value, formatter, ssa_func)
    if param_field_name:
        conf = 0 if frame_has_dcp is False else 75
        candidates.append(SwitchVariableCandidate(
            name=param_field_name, confidence=conf, source="param_field"
        ))

    # 5. Parameter trace (confidence 60, dropped to 0 when no DCP)
    param_name = _trace_value_to_parameter(var_value, formatter, ssa_func)
    if param_name:
        conf = 0 if frame_has_dcp is False else 60
        # Try semantic name inference
        if param_name.startswith('param_'):
            semantic = _infer_parameter_semantic_name(var_value, param_name, ssa_func, formatter)
            if semantic:
                param_name = semantic
                conf = 0 if frame_has_dcp is False else 65
                candidates.append(SwitchVariableCandidate(
                    name=param_name, confidence=conf, source="semantic_param"
                ))
            else:
                candidates.append(SwitchVariableCandidate(
                    name=param_name, confidence=conf, source="param_trace"
                ))
        else:
            candidates.append(SwitchVariableCandidate(
                name=param_name, confidence=conf, source="param_trace"
            ))

    # 6. Function call result (confidence 55)
    func_call_name = _trace_value_to_function_call(ssa_func, var_value, formatter)
    if func_call_name:
        candidates.append(SwitchVariableCandidate(
            name=func_call_name, confidence=55, source="func_call"
        ))

    # 7. Predecessor param field search (confidence 50, dropped to 0 when no DCP)
    pred_field_name = _find_param_field_in_predecessors(
        ssa_func, current_block, var_value, formatter
    )
    if pred_field_name:
        conf = 0 if frame_has_dcp is False else 50
        candidates.append(SwitchVariableCandidate(
            name=pred_field_name, confidence=conf, source="pred_param_field"
        ))

    # 8. Nearby GCP heuristic (confidence 30)
    gcp_name = _find_switch_variable_from_nearby_gcp(
        ssa_func, current_block, var_value, formatter, func_block_ids
    )
    if gcp_name:
        candidates.append(SwitchVariableCandidate(
            name=gcp_name, confidence=30, source="nearby_gcp"
        ))

    # 9. Fallback: render_value (confidence 10)
    rendered = formatter.render_value(var_value)
    if rendered:
        candidates.append(SwitchVariableCandidate(
            name=rendered, confidence=10, source="render_fallback"
        ))

    # Filter out confidence=0 candidates
    viable = [c for c in candidates if c.confidence > 0]

    if not viable:
        # All candidates were zeroed out — use render fallback
        fallback_name = formatter.render_value(var_value)
        _switch_debug(f"  -> All candidates zeroed out, using render fallback: {fallback_name}")
        return SwitchVariableCandidate(
            name=fallback_name, confidence=10, source="render_fallback"
        )

    # Pick winner: max confidence, tiebreak by shorter name
    viable.sort(key=lambda c: (-c.confidence, len(c.name)))
    winner = viable[0]

    _switch_debug(f"  -> Candidates: {[(c.name, c.confidence, c.source) for c in viable]}")
    _switch_debug(f"  -> Winner: {winner.name} (confidence={winner.confidence}, source={winner.source})")

    return winner


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


def _get_instruction_block(inst, ssa_func: SSAFunction) -> Optional[int]:
    """Get the block ID containing an instruction.

    Args:
        inst: SSA instruction to find
        ssa_func: SSA function

    Returns:
        Block ID if found, None otherwise
    """
    for block_id, insts in ssa_func.instructions.items():
        for i in insts:
            if i is inst or (hasattr(i, 'address') and hasattr(inst, 'address')
                            and i.address == inst.address):
                return block_id
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
    # Use dict to track depth: pred_id -> depth
    preds: Dict[int, int] = {}
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
        preds[pred_id] = depth  # Store depth for this predecessor
        if depth < max_depth and pred_id in cfg.blocks:
            for pred in cfg.blocks[pred_id].predecessors:
                if pred not in preds:
                    to_visit.append((pred, depth + 1))

    _switch_debug(f"  Searching {len(preds)} predecessor blocks for LADR→DADR→DCP pattern")

    # Search each predecessor for the pattern
    for pred_id, depth in preds.items():
        if pred_id not in ssa_blocks:
            continue

        instrs = ssa_blocks[pred_id]

        # Get the alias (stack slot) of the var_value being traced.
        # We use this to verify the DCP result connects to the same stack slot.
        var_alias = getattr(var_value, 'alias', None)

        # Look for DCP preceded by DADR preceded by LADR
        for i, instr in enumerate(instrs):
            if instr.mnemonic != 'DCP':
                continue

            # Verify the DCP output connects to the var_value being traced.
            # Check if the DCP output is in the phi_sources of the var_value,
            # or if the DCP is followed by SSP to the same stack slot as the LCP.
            if var_value and var_value.producer_inst:
                lcp_inst = var_value.producer_inst
                if lcp_inst.mnemonic == 'LCP' and lcp_inst.instruction and lcp_inst.instruction.instruction:
                    lcp_stack_offset = lcp_inst.instruction.instruction.arg1
                    # Check if there's an SSP in the same block or nearby that stores
                    # the DCP result to the same stack offset as the LCP
                    dcp_stores_to_lcp_slot = False

                    # Step 1: Search from DCP to end of block for SSP to same slot
                    # (Extended from 5-instruction window to entire block until branch)
                    for j in range(i + 1, len(instrs)):
                        check_inst = instrs[j]
                        # Stop if we hit a branch/jump - SSP won't be after that
                        if check_inst.mnemonic in ('JMP', 'JZ', 'JNZ', 'RET'):
                            break
                        if check_inst.mnemonic == 'SSP' and check_inst.instruction and check_inst.instruction.instruction:
                            ssp_offset = check_inst.instruction.instruction.arg1
                            if ssp_offset == lcp_stack_offset:
                                dcp_stores_to_lcp_slot = True
                                _switch_debug(f"    Found SSP to slot {lcp_stack_offset} at offset {j - i} from DCP in same block")
                                break

                    # Step 2: Search successor blocks for SSP to same slot
                    if not dcp_stores_to_lcp_slot:
                        dcp_block = cfg.blocks.get(pred_id)
                        if dcp_block:
                            for succ_id in dcp_block.successors:
                                if succ_id in ssa_blocks:
                                    for succ_inst in ssa_blocks[succ_id]:
                                        if succ_inst.mnemonic == 'SSP' and succ_inst.instruction and succ_inst.instruction.instruction:
                                            if succ_inst.instruction.instruction.arg1 == lcp_stack_offset:
                                                dcp_stores_to_lcp_slot = True
                                                _switch_debug(f"    Found SSP to slot {lcp_stack_offset} in successor block {succ_id}")
                                                break
                                        # Stop at branches
                                        if succ_inst.mnemonic in ('JMP', 'JZ', 'JNZ', 'RET'):
                                            break
                                    if dcp_stores_to_lcp_slot:
                                        break

                    # Step 3: Check SSA use chain - if DCP output is used by SSP
                    if not dcp_stores_to_lcp_slot:
                        if hasattr(instr, 'outputs') and instr.outputs:
                            dcp_output = instr.outputs[0]
                            # Check uses of this SSA value
                            for user in getattr(dcp_output, 'uses', []):
                                if hasattr(user, 'mnemonic') and user.mnemonic == 'SSP':
                                    if user.instruction and user.instruction.instruction:
                                        if user.instruction.instruction.arg1 == lcp_stack_offset:
                                            dcp_stores_to_lcp_slot = True
                                            _switch_debug(f"    Found SSP to slot {lcp_stack_offset} via SSA use chain")
                                            break

                    # Step 4: Also check phi_sources of var_value for the DCP output
                    if not dcp_stores_to_lcp_slot:
                        if var_value.phi_sources:
                            for _, phi_src in var_value.phi_sources:
                                if phi_src.producer_inst and phi_src.producer_inst is instr:
                                    dcp_stores_to_lcp_slot = True
                                    _switch_debug(f"    Found DCP output in phi_sources")
                                    break

                    # Step 5: DIRECT PREDECESSOR HEURISTIC
                    # If the DCP is in a direct predecessor (depth 1) of the current block,
                    # AND the LCP alias indicates a high stack offset (likely function parameter),
                    # AND the DCP accesses a parameter via LADR with negative offset,
                    # then accept this DCP as the switch variable source.
                    # This handles the common VC compiler pattern where:
                    #   Block N:   LADR [sp-4] → DADR 0 → DCP → JMP Block N+1
                    #   Block N+1: LCP [sp+418] → EQU → JZ
                    # The bytecode doesn't store the DCP result to sp+418, but the values
                    # are semantically related (both represent info->message).
                    if not dcp_stores_to_lcp_slot and depth == 1:
                        # Check if this is a parameter field access pattern
                        # Look ahead to see if this DCP is from LADR→DADR→DCP on a parameter
                        if instr.inputs and len(instr.inputs) > 0:
                            ptr_val = instr.inputs[0]
                            if ptr_val.producer_inst and ptr_val.producer_inst.mnemonic == 'DADR':
                                dadr = ptr_val.producer_inst
                                if dadr.inputs and len(dadr.inputs) > 0:
                                    base_val = dadr.inputs[0]
                                    if base_val.producer_inst and base_val.producer_inst.mnemonic == 'LADR':
                                        ladr = base_val.producer_inst
                                        if ladr.instruction and ladr.instruction.instruction:
                                            ladr_offset = ladr.instruction.instruction.arg1
                                            # Convert to signed
                                            if ladr_offset > 0x7FFFFFFF:
                                                ladr_offset = ladr_offset - 0x100000000
                                            # If LADR has negative offset, it's a parameter access
                                            if ladr_offset < 0:
                                                # Check if LCP offset is high (likely total frame size + 1)
                                                # indicating it accesses the same parameter slot
                                                if lcp_stack_offset > 100:  # High offset threshold
                                                    dcp_stores_to_lcp_slot = True
                                                    _switch_debug(f"    Direct predecessor heuristic: DCP from LADR[sp{ladr_offset:+d}] matches high LCP offset {lcp_stack_offset}")

                    if not dcp_stores_to_lcp_slot:
                        _switch_debug(f"    Skipping DCP - output doesn't connect to LCP stack slot {lcp_stack_offset}")
                        continue

            # Check if this DCP has inputs from DADR
            if not instr.inputs or len(instr.inputs) == 0:
                continue

            # Get the pointer input to DCP
            ptr_value_dcp = instr.inputs[0]
            if not ptr_value_dcp.producer_inst:
                continue

            dadr_inst = ptr_value_dcp.producer_inst

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


def _find_dead_gcp_in_predecessor(
    ssa_func: SSAFunction,
    current_block_id: int,
    formatter: ExpressionFormatter,
) -> Optional[str]:
    """
    Detect the "dead switch header" compiler pattern.

    The VC compiler emits a header block for switch statements:
        Block N:   GCP data[X]   ; declare switch variable (NEVER consumed)
                   JMP Block N+1
        Block N+1: LCP [sp+Y]    ; re-read value from frame stack
                   GCP const     ; case value
                   EQU           ; compare

    Also detects LCP dead headers (used when the switch variable is already
    in a local frame slot):
        Block N:   LCP [sp+X]    ; declare switch variable (NEVER consumed)
                   JMP Block N+1

    The output has zero real uses (only flows to PHI nodes with negative
    addresses). Combined with the block shape (only GCP/GLD/LCP + JMP), this
    is a definitive signal of the switch variable.
    """
    cfg = ssa_func.cfg
    if not cfg or current_block_id not in cfg.blocks:
        return None

    preds = cfg.blocks[current_block_id].predecessors
    ssa_blocks = ssa_func.instructions

    for pred_id in preds:
        if pred_id not in ssa_blocks:
            continue

        ssa_instrs = ssa_blocks[pred_id]

        # Filter to non-PHI instructions (address >= 0)
        real_instrs = [i for i in ssa_instrs if i.address >= 0]

        # Block shape check: exactly 2 real instructions, header + JMP
        if len(real_instrs) != 2:
            continue

        header_instr = None
        has_jmp = False
        for instr in real_instrs:
            if instr.mnemonic in {'GCP', 'GLD', 'LCP'}:
                header_instr = instr
            elif instr.mnemonic == 'JMP':
                has_jmp = True

        if not header_instr or not has_jmp:
            continue

        # Check that header output has zero real uses (all uses are PHI, addr < 0)
        if not header_instr.outputs:
            continue

        header_output = header_instr.outputs[0]
        real_uses = [addr for addr, _ in header_output.uses if addr >= 0]
        if len(real_uses) > 0:
            continue

        # Dead header confirmed — resolve variable name
        if header_instr.mnemonic in {'GCP', 'GLD'}:
            # Global load header: resolve global name from data offset
            if hasattr(header_instr, 'instruction') and hasattr(header_instr.instruction, 'instruction'):
                dword_offset = header_instr.instruction.instruction.arg1
                if hasattr(formatter, '_global_names'):
                    global_name = formatter._global_names.get(dword_offset)
                    if global_name:
                        _switch_debug(f"    Dead GCP header in block {pred_id}: {global_name} (0 real uses)")
                        return global_name

        elif header_instr.mnemonic == 'LCP':
            # LCP dead header: the loaded variable IS the switch variable.
            # Try to resolve the alias (e.g., local_20 → g_dialog if stored there).
            alias = header_output.alias
            if alias:
                # Check if this local has a global name via global resolver
                if hasattr(formatter, '_global_names'):
                    # Try resolving through the frame slot value
                    var_name = _trace_value_to_global(header_output, formatter, ssa_func)
                    if var_name:
                        _switch_debug(f"    Dead LCP header in block {pred_id}: {var_name} (from {alias})")
                        return var_name
                # If not a global, return the alias as-is (local variable name)
                _switch_debug(f"    Dead LCP header in block {pred_id}: {alias} (local)")
                return alias

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
                # Use existing variable tracing logic — same priority order
                # as _resolve_switch_variable: globals first, then param fields
                var_name = _trace_value_to_global(var_value, formatter, ssa_func)
                if not var_name:
                    var_name = _trace_value_to_parameter_field(var_value, formatter, ssa_func)
                if not var_name:
                    var_name = _trace_value_to_parameter(var_value, formatter, ssa_func)
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
                var_val, const_val = ssa_inst.inputs[0], ssa_inst.inputs[1]
                return (ssa_inst, var_val, const_val)

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
                            var_val, const_val = ssa_inst.inputs[0], ssa_inst.inputs[1]
                            return (ssa_inst, var_val, const_val)

                # Recurse to predecessor's predecessors
                result = _find_equ_for_comparison(
                    pred_id, jump_ssa, ssa_blocks, cfg, max_pred_search - 1
                )
                if result:
                    return result

    return None


def _is_different_stack_source(test_ssa_value, var_value) -> bool:
    """
    Check if two SSA values that resolved to the same variable name
    actually come from different stack locations (LCP aliases).

    This detects nested switch variables that falsely resolve to the same
    global name. For example, gphase is loaded to local_88 for the outer
    switch, but SC_ggi(SGI_LEVELPHASE) result stored in local_89 also
    traces back to gphase via _trace_value_to_global's GCP heuristic.

    Returns True if both values are produced by LCP but from different
    stack slots (different aliases), indicating different source variables.
    """
    if not test_ssa_value or not var_value:
        return False

    test_prod = test_ssa_value.producer_inst
    var_prod = var_value.producer_inst

    if not test_prod or not var_prod:
        return False

    # Both must be LCP (stack loads) for this check to apply
    if test_prod.mnemonic != 'LCP' or var_prod.mnemonic != 'LCP':
        return False

    test_alias = test_ssa_value.alias
    var_alias = var_value.alias

    if not test_alias or not var_alias:
        return False

    # If aliases differ, they load from different stack slots = different variables
    if test_alias != var_alias:
        _switch_debug(
            f"Different stack source detected: test={test_alias} vs new={var_alias} "
            f"(same resolved name but different stack slots → nested switch)"
        )
        return True

    return False


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

    # Compute loops once for back-edge filtering in case body detection
    # This prevents premature termination at loop headers inside case bodies
    loops: List[NaturalLoop] = find_all_loops(cfg)

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
        variable_confidence: Dict[str, int] = {}  # var_name -> confidence score from unified scoring
        variable_to_ssa: Dict[str, any] = {}      # var_name -> SSA value

        # PHASE 3 FIX: Collect ALL potential cases first, then filter
        # Structure: List[(var_name, var_confidence, ssa_value, case_info, source_block)]
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
        max_bfs_depth = 100  # Large switches (e.g., 31 cases) need depth > 60
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

                # Resolve switch variable using unified scoring system
                _switch_debug(f"Switch detection: Tracing var_value {var_value.name if hasattr(var_value, 'name') else var_value} (alias: {var_value.alias if hasattr(var_value, 'alias') else 'None'})")
                _switch_debug(f"  Producer: {var_value.producer_inst.mnemonic if var_value.producer_inst else 'None'}")
                _switch_debug(f"  Current test_var: {test_var}, test_ssa_value: {test_ssa_value.name if test_ssa_value and hasattr(test_ssa_value, 'name') else test_ssa_value}")

                winner = _resolve_switch_variable(
                    var_value, current_block, ssa_func, formatter, func_block_ids
                )
                var_name = winner.name
                var_confidence = winner.confidence

                _switch_debug(f"  Variable '{var_name}' assigned confidence: {var_confidence} (source: {winner.source})")

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
                elif test_var != var_name or _is_different_stack_source(test_ssa_value, var_value):
                    # NESTED SWITCH FIX: Different variable = likely nested switch
                    # EXCEPTION 1: If test_var is a MOD expression (contains %), and var_name is local_N,
                    # this is likely the same switch - the MOD result is stored on stack and reloaded.
                    # Pattern: Block N: MOD param_0, 4 -> Block N+1: LCP [sp+0] (becomes local_0)
                    is_mod_switch = '%' in test_var
                    is_stack_load = var_name.startswith('local_') or var_name.startswith('n')

                    # EXCEPTION 2: If both SSA values load from the same stack location,
                    # they're the same variable with different names (e.g., one traces to
                    # SC_ggi() result, the other to local_1 which stores that result).
                    same_source = False
                    if test_ssa_value and var_value:
                        def _get_lcp_alias(v):
                            """Get the LCP alias (stack location) for an SSA value."""
                            if v.producer_inst and v.producer_inst.mnemonic == 'LCP':
                                return v.alias
                            return None
                        test_alias = _get_lcp_alias(test_ssa_value)
                        var_alias = _get_lcp_alias(var_value)
                        if test_alias and var_alias and test_alias == var_alias:
                            same_source = True
                            _switch_debug(f"Same stack source: {test_var} and {var_name} both from {test_alias}")

                    if is_mod_switch and is_stack_load:
                        # Same switch, different name - use the MOD-based name
                        _switch_debug(f"MOD switch continuation: {test_var} vs {var_name} (treating as same variable)")
                        chain_debug['variables_seen'].append(var_name)
                        chain_debug['ssa_values_seen'].append(var_value.name if hasattr(var_value, 'name') else str(var_value))
                        debug_print(f"DEBUG SWITCH: MOD switch continuation - keeping {test_var}")
                        # Don't update test_var - keep the MOD-based name
                    elif same_source:
                        # Same stack variable, different traced names - keep the first (more descriptive) name
                        # Use test_var for tracking so the best_variable logic doesn't
                        # pick a different name just because a later false resolution
                        # has higher priority (e.g., info->param2 priority=100 vs gphase priority=50).
                        var_name = test_var
                        _switch_debug(f"Same-source continuation: {test_var} vs original (treating as same variable)")
                        chain_debug['variables_seen'].append(var_name)
                        chain_debug['ssa_values_seen'].append(var_value.name if hasattr(var_value, 'name') else str(var_value))
                        debug_print(f"DEBUG SWITCH: Same-source continuation - keeping {test_var}")
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

                # Track this variable's frequency and confidence.
                # This is done AFTER the nested switch check so that variables
                # belonging to nested switches are excluded from best-variable selection.
                variable_frequency[var_name] = variable_frequency.get(var_name, 0) + 1
                variable_confidence[var_name] = max(variable_confidence.get(var_name, 0), var_confidence)
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
                            all_potential_cases.append((var_name, var_confidence, var_value, case_info, current_block))
                            case_sources[(case_val, case_block_id)] = current_block

                            # TEMPORARY: Also add to old structure for compatibility
                            cases.append(case_info)
                            chain_blocks.append(current_block)
                            last_chain_block = current_block  # Track last test block
                            found_equ = True
                            debug_print(f"DEBUG SWITCH: Added case: value={case_val}, block={case_block_id}, var={var_name}, confidence={var_confidence}, order={case_info.detection_order}")

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

        # Select the BEST variable based on confidence and frequency
        # If we saw multiple variables during BFS, pick the one with highest confidence
        if len(cases) >= 1 and variable_frequency:
            _switch_debug(f"Variable frequency: {variable_frequency}")
            _switch_debug(f"Variable confidence: {variable_confidence}")

            best_var = None
            best_score = -1

            for var_name in variable_frequency:
                # Score = confidence * 1000 + frequency
                # This heavily weights confidence but uses frequency as tiebreaker
                score = variable_confidence.get(var_name, 0) * 1000 + variable_frequency[var_name]
                _switch_debug(f"  {var_name}: confidence={variable_confidence.get(var_name, 0)}, freq={variable_frequency[var_name]}, score={score}")

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

        # STRUCTURAL CONTINUITY CHECK: Split chain at structural gaps.
        # When two separate switch(X) statements on the same variable exist,
        # the BFS merges them because it doesn't detect structural boundaries.
        # Check if chain_blocks form a continuous CFG path. If not, keep only
        # the first connected segment and leave the rest for later detection.
        if len(chain_blocks) >= 2:
            first_segment_end = 0
            for ci in range(1, len(chain_blocks)):
                prev_bid = chain_blocks[ci - 1]
                curr_bid = chain_blocks[ci]
                prev_block = cfg.blocks.get(prev_bid)
                connected = False
                if prev_block:
                    # Direct successor
                    if curr_bid in prev_block.successors:
                        connected = True
                    else:
                        # Allow one intermediate block (JMP passthrough)
                        for succ_id in prev_block.successors:
                            succ_block = cfg.blocks.get(succ_id)
                            if succ_block and curr_bid in succ_block.successors:
                                # Verify it's a JMP-only block
                                if succ_block.instructions and len(succ_block.instructions) <= 2:
                                    connected = True
                                    break
                if connected:
                    first_segment_end = ci
                else:
                    break

            if first_segment_end < len(chain_blocks) - 1:
                # Gap found — split chain
                kept_chain = chain_blocks[:first_segment_end + 1]
                dropped_chain = chain_blocks[first_segment_end + 1:]
                kept_set = set(kept_chain)

                # Filter cases to only keep those from the first segment
                kept_cases = []
                for case in cases:
                    # Find the chain block that produced this case
                    case_key = (case.value, case.block_id)
                    src = filtered_case_sources.get(case_key) or case_sources.get(case_key)
                    if src in kept_set:
                        kept_cases.append(case)

                if kept_cases and len(kept_cases) < len(cases):
                    debug_print(f"DEBUG SWITCH: Split chain at structural gap: kept {len(kept_cases)} cases (chain {kept_chain}), dropped {len(cases) - len(kept_cases)} cases (chain {dropped_chain})")
                    chain_blocks = kept_chain
                    cases = kept_cases
                    # Update last_chain_block
                    last_chain_block = kept_chain[-1] if kept_chain else last_chain_block

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
                    cfg, case.block_id, preliminary_stop, resolver,
                    loops=loops
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
            best_exit_addr = -1  # Track address for tiebreaking
            for bid, reaching_cases in exit_candidates.items():
                # Skip blocks that are part of the switch structure itself
                if bid in all_case_blocks or bid in chain_blocks:
                    continue

                # Skip blocks that are inside a case body (they're internal to a case,
                # not convergence points) - unless reached by multiple cases
                if bid in all_preliminary_body and len(reaching_cases) <= 1:
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

                # Get block address for tiebreaking (prefer higher addresses = later in code)
                candidate_addr = candidate_block.start if candidate_block else 0

                # Prefer blocks reached by MORE cases; tiebreak by highest address
                # (exit blocks typically appear after all case bodies in code order)
                if score > best_score or (score == best_score and candidate_addr > best_exit_addr):
                    best_score = score
                    best_exit = bid
                    best_exit_addr = candidate_addr
                    debug_print(f"DEBUG SWITCH: New best exit: {bid} (addr={candidate_addr}) with score {score} (reached by {reaching_cases})")

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
            # Include header block (use actual_header if it was adjusted,
            # but we need to compute it first - so always include block_id for now,
            # and fix up after actual_header is determined below)
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
                    known_exit_blocks={exit_block} if exit_block else None,
                    loops=loops
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
                    known_exit_blocks={exit_block} if exit_block else None,
                    loops=loops
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
                        known_exit_blocks={exit_block} if exit_block else None,
                        loops=loops
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
                                # NEW: Check if block contains meaningful code (not just boilerplate)
                                # XCALL = function call, GADR = address of (typically string)
                                # These indicate real code, not just exit boilerplate
                                has_meaningful_code = False
                                block_to_check = potential_exit_blk

                                # If this is a JMP-only block, also check the JMP target
                                # This handles cases where the default entry is a JMP block
                                # that redirects to the actual default body
                                blocks_to_check = [potential_exit_blk]
                                if (len(potential_exit_blk.instructions) == 1 and
                                    resolver.get_mnemonic(potential_exit_blk.instructions[0].opcode) == "JMP"):
                                    jmp_target_addr = potential_exit_blk.instructions[0].arg1
                                    for bid, blk in cfg.blocks.items():
                                        if blk.start == jmp_target_addr and bid != exit_block:
                                            blocks_to_check.append(blk)
                                            debug_print(f"DEBUG SWITCH: Following JMP from default entry to block {bid} (addr {jmp_target_addr})")
                                            break

                                for blk in blocks_to_check:
                                    for instr in blk.instructions:
                                        mnem = resolver.get_mnemonic(instr.opcode)
                                        if mnem in ("XCALL", "GADR"):
                                            has_meaningful_code = True
                                            break
                                    if has_meaningful_code:
                                        break

                                if has_meaningful_code:
                                    debug_print(
                                        f"DEBUG SWITCH: Keeping default body {default_body} - "
                                        f"contains meaningful code (not just exit boilerplate)"
                                    )
                                    # Don't set default_body = None, this IS the default case
                                    # Also add the JMP target block to default_body if it was followed
                                    if len(blocks_to_check) > 1:
                                        for bid, blk in cfg.blocks.items():
                                            if blk == blocks_to_check[1]:
                                                default_body.add(bid)
                                                debug_print(f"DEBUG SWITCH: Added JMP target block {bid} to default_body")
                                                break
                                elif exit_block is None and _block_ends_with_return(cfg, potential_exit, resolver):
                                    # Special case: switch-return functions often have a single return block
                                    # as the implicit default. Keep it if there's no common exit block.
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

            # Determine the actual header block: the first comparison block in the chain.
            # When BFS starts from a non-comparison block (e.g., block 95 which contains
            # pre-switch code), we should use the first chain block (e.g., block 109)
            # as the header so the collapse engine correctly identifies the switch start.
            actual_header = block_id
            if chain_blocks:
                first_chain = chain_blocks[0]
                # Only override if block_id is not itself a comparison block
                if first_chain != block_id and first_chain in func_block_ids:
                    first_chain_block = cfg.blocks.get(first_chain)
                    if first_chain_block and first_chain_block.instructions:
                        last_instr = first_chain_block.instructions[-1]
                        if resolver.is_conditional_jump(last_instr.opcode):
                            actual_header = first_chain
                            debug_print(f"DEBUG SWITCH: Using first chain block {actual_header} as header instead of BFS start {block_id}")
                            # Remove pre-switch blocks from all_blocks - they are NOT part of the switch
                            # They'll be emitted as sequential code before the switch by the collapse engine
                            all_blocks.discard(block_id)

            # Ensure actual_header is in all_blocks
            all_blocks.add(actual_header)

            switch = SwitchPattern(
                test_var=test_var,
                header_block=actual_header,
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
