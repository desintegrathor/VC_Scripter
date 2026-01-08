"""
Loop pattern detection for control flow analysis.

This module contains functions for detecting for-loop patterns in natural loops,
identifying initialization, condition, and increment components.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from ...cfg import CFG, NaturalLoop
from ....disasm import opcodes
from ...ssa import SSAFunction
from ...expr import ExpressionFormatter

from .models import ForLoopInfo


def _detect_for_loop(
    loop: NaturalLoop,
    cfg: CFG,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    global_map: Optional[Dict[int, str]] = None
) -> Optional[ForLoopInfo]:
    """
    Detect for-loop pattern in a natural loop.

    Pattern:
    1. Predecessor of header has initialization (i = 0)
    2. Header has conditional jump testing loop variable (i < N)
    3. Last block in body has increment (i++)

    Returns:
        ForLoopInfo if pattern matches, None otherwise
    """
    # Get header block
    header_block = cfg.blocks.get(loop.header)
    if not header_block or not header_block.instructions:
        return None

    # Step 1: Find initialization in predecessor blocks
    # Look for assignments immediately before loop entry
    predecessors = [p for p in header_block.predecessors if p not in loop.body]
    if not predecessors:
        return None

    init_var = None
    init_value = None

    # Check predecessors for initialization pattern
    # Pattern 1: Direct assignment (inst has outputs)
    # Pattern 2: ASGN instruction (inputs=[value, &target])
    for pred_id in predecessors:
        pred_ssa_block = ssa_func.instructions.get(pred_id, [])
        # Look for assignments like: local_2 = 0, i = 0
        for inst in reversed(pred_ssa_block):  # Check from end backwards
            # Pattern 1: Direct output (e.g., local_2 = 0)
            if inst.outputs and len(inst.outputs) == 1:
                var_name = inst.outputs[0].alias or inst.outputs[0].name
                if var_name and not var_name.startswith("data_") and not var_name.startswith("&"):
                    # Found potential init variable
                    init_var = var_name
                    # Get initialization value from instruction
                    if inst.inputs and len(inst.inputs) > 0:
                        init_value = formatter.render_value(inst.inputs[0])
                    else:
                        init_value = "0"  # Default
                    break
            # Pattern 2: ASGN instruction (inputs=[value, &target])
            elif inst.mnemonic == "ASGN" and len(inst.inputs) >= 2:
                target = inst.inputs[1]
                target_name = target.alias or target.name
                # Extract variable name from &local_2 → local_2
                if target_name and target_name.startswith("&"):
                    var_name = target_name[1:]  # Strip & prefix
                    if var_name and not var_name.startswith("data_"):
                        # Found potential init variable
                        init_var = var_name
                        # Get initialization value from first input
                        init_value = formatter.render_value(inst.inputs[0])
                        break
        if init_var:
            break

    if not init_var:
        return None

    # Step 2: Extract condition from header's conditional jump
    last_instr = header_block.instructions[-1]
    if not resolver.is_conditional_jump(last_instr.opcode):
        return None

    # Get condition from SSA
    condition_text = None
    header_ssa_block = ssa_func.instructions.get(loop.header, [])

    # Find the comparison instruction (the one that produces the condition value)
    for ssa_inst in header_ssa_block:
        if ssa_inst.address == last_instr.address and ssa_inst.inputs:
            cond_value = ssa_inst.inputs[0]

            # Find the instruction that produced this value
            for compare_inst in header_ssa_block:
                if compare_inst.outputs and any(out.name == cond_value.name for out in compare_inst.outputs):
                    # This is the comparison instruction - manually render it
                    if compare_inst.inputs and len(compare_inst.inputs) >= 2:
                        left = formatter.render_value(compare_inst.inputs[0])
                        right_val = compare_inst.inputs[1]

                        # FIX: If right operand is a data segment reference, resolve to global name or constant
                        right_alias = right_val.alias or right_val.name
                        if right_alias and right_alias.startswith("data_"):
                            # This is a data segment reference
                            offset = int(right_alias[5:])  # Extract offset from "data_123"
                            if global_map and offset in global_map:
                                # Known global variable name
                                right = global_map[offset]
                            else:
                                # FÁZE 2.1: Try to resolve as constant from data segment
                                scr = getattr(ssa_func, 'scr', None)
                                if scr and hasattr(scr, 'data_segment'):
                                    try:
                                        # Read 4-byte integer from data segment
                                        import struct
                                        data_seg = scr.data_segment
                                        # CRITICAL FIX: offset is in DWORD units, not bytes!
                                        # data_383 means 383rd DWORD (4-byte word)
                                        byte_offset = offset * 4
                                        if byte_offset < len(data_seg.raw_data):
                                            bytes_data = data_seg.raw_data[byte_offset:byte_offset+4]
                                            if len(bytes_data) == 4:
                                                const_value = struct.unpack('<I', bytes_data)[0]
                                                # Use constant value if it looks reasonable for loop bound
                                                if 0 <= const_value < 10000:
                                                    right = str(const_value)
                                                else:
                                                    right = right_alias
                                            else:
                                                right = right_alias
                                        else:
                                            right = right_alias
                                    except:
                                        # Fallback to data_X if resolution fails
                                        right = right_alias
                                else:
                                    # Fallback to data_X if no data segment available
                                    right = right_alias
                        else:
                            right = formatter.render_value(right_val)

                        # Map mnemonic to operator
                        op_map = {
                            "ULES": "<=", "UGTS": ">", "UGES": ">=", "ULSS": "<",
                            "IEQS": "==", "INES": "!=",
                            "CESS": "<", "CGTS": ">", "CGES": ">=", "CLES": "<=",
                            "CEQS": "==", "CNES": "!=",
                            "SESS": "<", "SGTS": ">", "SGES": ">=", "SLES": "<=",
                            "SEQS": "==", "SNES": "!=",
                            "IESS": "<", "IGTS": ">", "IGES": ">=", "ILES": "<=",
                        }
                        op = op_map.get(compare_inst.mnemonic, "?")

                        # P0.2 FIX: Analyze jump direction to correct loop conditions
                        # Problem: Compiler generates <= for < in some cases (off-by-one bug)
                        # Solution: Check if jump exits loop (forward) or continues (backward)
                        jump_instr = ssa_inst  # The JZ/JNZ instruction
                        jump_target = last_instr.arg1  # Target address of jump

                        # Determine if jump exits loop or continues loop
                        # If jump goes FORWARD (to higher address) → likely exit condition
                        # If jump goes BACKWARD (to lower address) → likely loop continuation
                        is_forward_jump = jump_target > last_instr.address

                        # For-loops typically have pattern: JZ forward (exit when condition false)
                        # So if bytecode has ULES (<=) and JZ forward, we need to normalize:
                        # - ULES + JZ forward = exit when (i <= limit) is FALSE = continue when (i > limit)
                        # - But wait, that's inverted! Let's check the jump mnemonic

                        # Actually, the condition in bytecode represents when to EXIT the loop
                        # For standard for-loops: continue while (i < N), exit when NOT (i < N)
                        # Compiler generates: compare i vs N, JZ exit_label (jump if i >= N)
                        # So bytecode comparison is "i >= N" (exit condition)
                        # We want to display: "i < N" (continue condition)

                        # Heuristic for for-loops:
                        # If operator is <= and it looks like a standard loop bound check,
                        # convert to < (the original source likely used <)
                        if op in ["<=", ">="]:
                            # Check if this is a standard loop pattern (counter vs constant/variable)
                            # Pattern: local_X <= N where local_X starts at 0
                            if init_value in ["0", "0x0", "0x00000000"]:
                                # Loop starts at 0, likely should be < not <=
                                if op == "<=":
                                    op = "<"
                                    # Note: We're making an educated guess that the original
                                    # source used < and the compiler generated <=
                                    # This is a common pattern in VC Script compiler
                                elif op == ">=":
                                    op = ">"

                        cond_expr = f"({left} {op} {right})"

                        # Check if condition involves our loop variable (check both name and any aliases)
                        # For example, local_2 might be rendered as "i" due to aliasing
                        involves_loop_var = init_var in cond_expr
                        # Also check if any of the inputs have the init_var as their base
                        if not involves_loop_var:
                            for inp in compare_inst.inputs:
                                inp_name = inp.alias or inp.name
                                # Strip & prefix if present
                                if inp_name and inp_name.startswith("&"):
                                    inp_name = inp_name[1:]
                                if inp_name == init_var:
                                    involves_loop_var = True
                                    break
                        if involves_loop_var:
                            condition_text = cond_expr
                    break
            break

    if not condition_text:
        return None

    # Step 3: Find increment at end of loop body
    # Look in blocks that jump back to header (back edges)
    # Pattern 1: Direct increment (inst has outputs with init_var name)
    # Pattern 2: ASGN instruction (inputs=[value, &init_var])
    increment_text = None
    for back_edge in loop.back_edges:
        source_id = back_edge.source
        target_id = back_edge.target
        if target_id == loop.header:
            # This block jumps back to header - check for increment
            source_ssa_block = ssa_func.instructions.get(source_id, [])
            for inst in reversed(source_ssa_block):
                # Pattern 1: Direct output (e.g., i = i + 1)
                if inst.outputs and len(inst.outputs) == 1:
                    var_name = inst.outputs[0].alias or inst.outputs[0].name
                    if var_name == init_var:
                        # Found assignment to loop variable
                        # Check if it's increment pattern: i = i + 1
                        if inst.mnemonic in {"IADD", "CADD", "SADD"}:
                            # Simple increment
                            increment_text = f"{init_var}++"
                        elif inst.inputs:
                            # Generic assignment - render it
                            inc_expr = formatter.render_value(inst.inputs[0]) if inst.inputs else "?"
                            if f"{init_var} + 1" in inc_expr or f"({init_var} + 1)" == inc_expr:
                                increment_text = f"{init_var}++"
                            else:
                                increment_text = f"{init_var} = {inc_expr}"
                        break
                # Pattern 2: ASGN instruction (inputs=[value, &target])
                elif inst.mnemonic == "ASGN" and len(inst.inputs) >= 2:
                    target = inst.inputs[1]
                    target_name = target.alias or target.name
                    # Extract variable name from &local_2 → local_2
                    if target_name and target_name.startswith("&"):
                        var_name = target_name[1:]  # Strip & prefix
                        if var_name == init_var:
                            # Found assignment to loop variable
                            # Render the increment expression
                            inc_expr = formatter.render_value(inst.inputs[0])
                            # Check for i+1 pattern
                            if f"{init_var} + 1" in inc_expr or f"({init_var} + 1)" == inc_expr:
                                increment_text = f"{init_var}++"
                            else:
                                increment_text = f"{init_var} = {inc_expr}"
                            break
            if increment_text:
                break

    if not increment_text:
        return None

    # Successfully detected for-loop pattern
    # Extract the actual variable name from condition if it's different from init_var
    # Condition is like "(i <= gData28)" - extract the left operand
    import re
    display_var = init_var
    match = re.match(r'\((\w+)\s*[<>=!]+', condition_text)
    if match:
        cond_var = match.group(1)
        if cond_var != init_var:
            # Use the variable name from condition (it's the aliased form)
            display_var = cond_var
            # Also update increment to use display_var
            increment_text = increment_text.replace(init_var, display_var)

    return ForLoopInfo(
        var=display_var,
        init=init_value,
        condition=condition_text,
        increment=increment_text,
        init_var=init_var
    )
