"""
Switch/case pattern detection for control flow analysis.

This module contains functions for detecting switch/case patterns in the CFG,
including the main switch pattern detection and helper functions for finding
switch variables from nearby global variable loads.
"""

from __future__ import annotations

from typing import Dict, Set, List, Optional

from ...cfg import CFG
from ....disasm import opcodes
from ...ssa import SSAFunction
from ...expr import ExpressionFormatter

from .models import CaseInfo, SwitchPattern
from ..analysis.flow import _find_case_body_blocks
from ..analysis.value_trace import _trace_value_to_parameter, _trace_value_to_global


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

    # Iterate through blocks looking for switch headers
    for block_id in func_block_ids:
        if block_id in processed_blocks:
            continue

        block = cfg.blocks.get(block_id)
        if not block or not block.instructions:
            continue

        # Start collecting potential switch cases
        test_var = None
        cases: List[CaseInfo] = []
        chain_blocks: List[int] = []
        current_block = block_id

        # Follow the chain of equality tests
        while current_block is not None and current_block in func_block_ids:
            if current_block in processed_blocks:
                break

            curr_block_obj = cfg.blocks.get(current_block)
            if not curr_block_obj or not curr_block_obj.instructions:
                break

            last_instr = curr_block_obj.instructions[-1]
            opcode = last_instr.opcode

            # Must be conditional jump
            if not resolver.is_conditional_jump(opcode):
                break


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

            if jump_ssa and len(jump_ssa.inputs) > 0:
                # The condition value is the first input to JZ/JNZ
                condition_value = jump_ssa.inputs[0]

                # Find the producer of this condition (should be EQU)
                equ_inst = None
                for ssa_inst in ssa_block:
                    if any(out.name == condition_value.name for out in ssa_inst.outputs):
                        equ_inst = ssa_inst
                        break

                if equ_inst and equ_inst.mnemonic == "EQU" and len(equ_inst.inputs) >= 2:
                    var_value = equ_inst.inputs[0]
                    const_value = equ_inst.inputs[1]

                    # Get variable name - try to trace back to parameter first, then global
                    var_name = _trace_value_to_parameter(var_value, formatter, ssa_func)
                    if not var_name:
                        var_name = _trace_value_to_global(var_value, formatter)

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

                    if not var_name:
                        # Fall back to regular rendering if neither parameter nor global
                        var_name = formatter.render_value(var_value)

                    # Check if first switch or same variable
                    if test_var is None:
                        test_var = var_name
                    elif test_var != var_name:
                        # Different variable, not part of switch
                        # Don't process this block, break the loop
                        break

                    # Same variable (or first case), try to extract constant value
                    case_val = None
                    if const_value.alias and const_value.alias.startswith("data_"):
                        try:
                            offset = int(const_value.alias[5:])
                            if ssa_func.scr and ssa_func.scr.data_segment:
                                case_val = ssa_func.scr.data_segment.get_dword(offset * 4)
                        except (ValueError, AttributeError):
                            pass

                    if case_val is not None:
                            # This is a valid case!
                            # Determine which successor is the case body
                            # JZ means jump if zero (condition false), so arg1 is NOT the case
                            # JNZ means jump if not zero (condition true), so arg1 IS the case
                            mnemonic = resolver.get_mnemonic(opcode)
                            if mnemonic == "JNZ":
                                case_block = last_instr.arg1
                            else:  # JZ
                                # Fall-through is the case body
                                case_block = last_instr.address + 1

                            # Convert address to block ID
                            case_block_id = None
                            for bid, b in cfg.blocks.items():
                                if b.start == case_block:
                                    case_block_id = bid
                                    break

                            if case_block_id is not None:
                                cases.append(CaseInfo(value=case_val, block_id=case_block_id))
                                chain_blocks.append(current_block)
                                found_equ = True

                                # Find next block in chain
                                if mnemonic == "JNZ":
                                    # Fall-through is next test
                                    next_addr = last_instr.address + 1
                                else:  # JZ
                                    # Jump target is next test
                                    next_addr = last_instr.arg1

                                # Find next block
                                next_block = None
                                for bid, b in cfg.blocks.items():
                                    if b.start == next_addr:
                                        next_block = bid
                                        break
                                current_block = next_block
                            else:
                                pass  # Case block ID not found

            if not found_equ:
                break

        # If we found at least 2 cases, it's a switch
        if len(cases) >= 2:

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
            all_blocks = set(chain_blocks)
            all_blocks.update(all_case_blocks)
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
                default_body = _find_case_body_blocks(
                    cfg, current_block, stop_blocks, resolver
                )
                all_blocks.update(default_body)

            switch = SwitchPattern(
                test_var=test_var,
                header_block=block_id,
                cases=cases,
                default_block=current_block,  # Last block in chain is default
                default_body_blocks=default_body,
                exit_block=exit_block,
                all_blocks=all_blocks,
            )
            switches.append(switch)
            processed_blocks.update(chain_blocks)

    return switches
