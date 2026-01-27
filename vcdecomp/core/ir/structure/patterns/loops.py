"""
Loop pattern detection for control flow analysis.

This module contains functions for detecting for-loop patterns in natural loops,
identifying initialization, condition, and increment components.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Iterable, Set

from ...cfg import CFG, NaturalLoop
from ....disasm import opcodes
from ...ssa import SSAFunction
from ...expr import ExpressionFormatter
from ..analysis.condition import render_condition
from ..analysis.value_trace import _check_ssa_value_equivalence
from .if_else import _detect_early_return_pattern

from .models import ForLoopInfo, WhileLoopInfo, DoWhileLoopInfo


def _condition_mentions_loop_var(
    condition_text: str,
    init_var: str | Iterable[str],
    values: Optional[List] = None
) -> bool:
    if not condition_text:
        return False
    if isinstance(init_var, str):
        loop_vars = {init_var} if init_var else set()
    else:
        loop_vars = {v for v in init_var if v}
    if loop_vars and any(loop_var in condition_text for loop_var in loop_vars):
        return True
    if values:
        for value in values:
            value_name = value.alias or value.name
            if value_name and value_name.startswith("&"):
                value_name = value_name[1:]
            if value_name in loop_vars:
                return True
    return False


def _normalize_loop_var_name(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    if name.startswith("&"):
        name = name[1:]
    return name


def _score_loop_var_name(name: Optional[str], preferred: Optional[Set[str]] = None) -> int:
    if not name:
        return -100
    score = 0
    if preferred and name in preferred:
        score += 6
    if name.startswith("local_"):
        score += 4
    if name.startswith("param_"):
        score += 2
    if name.startswith("ptr"):
        score -= 3
    if name.startswith("tmp"):
        score -= 2
    if name.startswith("t") and name[1:].isdigit():
        score -= 1
    if name.startswith("data_"):
        score -= 6
    return score


def _extract_condition_vars(condition_text: str, values: Optional[List]) -> Set[str]:
    vars_found: Set[str] = set()
    if values:
        for value in values:
            value_name = _normalize_loop_var_name(value.alias or value.name)
            if value_name:
                vars_found.add(value_name)
    if condition_text:
        import re
        match = re.match(r'!?\(?\s*([A-Za-z_]\w*)\s*[<>=!]+', condition_text)
        if match:
            vars_found.add(match.group(1))
    return vars_found


def _invert_condition_text(condition_text: str) -> str:
    stripped = condition_text.strip()
    if stripped.startswith("!"):
        if stripped.startswith("!(") and stripped.endswith(")"):
            return stripped[2:-1].strip()
        return stripped[1:].strip()
    import re
    match = re.match(r'^\(?\s*(.+?)\s*(<=|>=|<|>|==|!=)\s*(.+?)\s*\)?$', stripped)
    if match:
        left, op, right = match.groups()
        inverse = {
            "<": ">=",
            "<=": ">",
            ">": "<=",
            ">=": "<",
            "==": "!=",
            "!=": "==",
        }.get(op, op)
        return f"{left.strip()} {inverse} {right.strip()}"
    return f"!({condition_text})"


def _find_guard_condition(
    loop: NaturalLoop,
    cfg: CFG,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    init_var: str | Iterable[str]
) -> Optional[Tuple[str, int]]:
    sorted_body = sorted(loop.body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
    for block_id in sorted_body:
        if block_id == loop.header:
            continue
        block = cfg.blocks.get(block_id)
        if block and block.instructions:
            last_instr = block.instructions[-1]
            if resolver.is_conditional_jump(last_instr.opcode):
                target_block = start_to_block.get(last_instr.arg1)
                if target_block is not None and target_block not in loop.body:
                    condition_render = render_condition(
                        ssa_func,
                        block_id,
                        formatter,
                        cfg,
                        resolver,
                        negate=None
                    )
                    break_condition = condition_render.text or ""
                    if break_condition:
                        continue_condition = _invert_condition_text(break_condition)
                        if _condition_mentions_loop_var(continue_condition, init_var, condition_render.values):
                            return continue_condition, block_id
        early_ret = _detect_early_return_pattern(cfg, block_id, start_to_block, resolver)
        if not early_ret:
            continue
        guard_block_id, exit_block_id, continue_block_id, is_negated = early_ret
        if continue_block_id not in loop.body:
            continue
        if exit_block_id in loop.body:
            continue
        exit_block = cfg.blocks.get(exit_block_id)
        if not exit_block or not exit_block.instructions:
            continue
        exit_instr = exit_block.instructions[-1]
        if resolver.get_mnemonic(exit_instr.opcode) != "JMP":
            continue
        exit_target_block = start_to_block.get(exit_instr.arg1)
        if exit_target_block is not None and exit_target_block in loop.body:
            continue

        condition_render = render_condition(
            ssa_func,
            block_id,
            formatter,
            cfg,
            resolver,
            negate=not is_negated
        )
        condition_text = condition_render.text or ""
        if not condition_text:
            continue
        if not _condition_mentions_loop_var(condition_text, init_var, condition_render.values):
            continue
        return condition_text, guard_block_id
    return None


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
    init_candidates: List[Tuple[str, str, Optional[object]]] = []

    def _maybe_store_init(var_name: Optional[str], value_text: str, ssa_value) -> None:
        if not var_name:
            return
        init_candidates.append((var_name, value_text, ssa_value))

    condition_candidates: Set[str] = set()

    # Check predecessors for initialization pattern
    # Pattern 1: Direct assignment (inst has outputs)
    # Pattern 2: ASGN instruction (inputs=[value, &target])
    for pred_id in predecessors:
        pred_ssa_block = ssa_func.instructions.get(pred_id, [])
        # Look for assignments like: local_2 = 0, i = 0
        for inst in reversed(pred_ssa_block):  # Check from end backwards
            # Pattern 1: Direct output (e.g., local_2 = 0)
            if inst.outputs and len(inst.outputs) == 1:
                var_name = _normalize_loop_var_name(inst.outputs[0].alias or inst.outputs[0].name)
                if var_name and not var_name.startswith("data_"):
                    # Found potential init variable
                    # Get initialization value from instruction
                    if inst.inputs and len(inst.inputs) > 0:
                        init_value = formatter.render_value(inst.inputs[0])
                    else:
                        init_value = "0"  # Default
                    _maybe_store_init(var_name, init_value, inst.outputs[0])
            # Pattern 2: ASGN instruction (inputs=[value, &target])
            elif inst.mnemonic == "ASGN" and len(inst.inputs) >= 2:
                target = inst.inputs[1]
                target_name = _normalize_loop_var_name(target.alias or target.name)
                if target_name and not target_name.startswith("data_"):
                    init_value = formatter.render_value(inst.inputs[0])
                    _maybe_store_init(target_name, init_value, target)

    # Step 2: Extract condition from header's conditional jump
    condition_text = None
    guard_block: Optional[int] = None
    condition_render = None
    last_instr = header_block.instructions[-1]
    if resolver.is_conditional_jump(last_instr.opcode):
        target_block = start_to_block.get(last_instr.arg1)
        if target_block is not None and target_block not in loop.body:
            condition_render = render_condition(
                ssa_func,
                loop.header,
                formatter,
                cfg,
                resolver,
                negate=None
            )
            break_condition = condition_render.text or ""
            if break_condition:
                inverted_condition = _invert_condition_text(break_condition)
                condition_candidates = _extract_condition_vars(inverted_condition, condition_render.values)
                if _condition_mentions_loop_var(inverted_condition, condition_candidates, condition_render.values):
                    condition_text = inverted_condition
                    guard_block = loop.header

        if condition_text is None:
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

                                condition_candidates = _extract_condition_vars(cond_expr, compare_inst.inputs)
                                if _condition_mentions_loop_var(cond_expr, condition_candidates, compare_inst.inputs):
                                    condition_text = cond_expr
                            break
                    break

    # If we didn't find a candidate in predecessors, try header block for init
    if not init_candidates:
        header_ssa_block = ssa_func.instructions.get(loop.header, [])
        for inst in reversed(header_ssa_block):
            if inst.outputs and len(inst.outputs) == 1:
                var_name = _normalize_loop_var_name(inst.outputs[0].alias or inst.outputs[0].name)
                if var_name and not var_name.startswith("data_"):
                    init_value = formatter.render_value(inst.inputs[0]) if inst.inputs else "0"
                    _maybe_store_init(var_name, init_value, inst.outputs[0])
            elif inst.mnemonic == "ASGN" and len(inst.inputs) >= 2:
                target_name = _normalize_loop_var_name(inst.inputs[1].alias or inst.inputs[1].name)
                if target_name and not target_name.startswith("data_"):
                    init_value = formatter.render_value(inst.inputs[0])
                    _maybe_store_init(target_name, init_value, inst.inputs[1])

    init_ssa_map: Dict[str, Optional[object]] = {}
    if init_candidates:
        def _init_candidate_score(item: Tuple[str, str, Optional[object]]) -> int:
            name, _, ssa_val = item
            score = _score_loop_var_name(name, condition_candidates)
            if ssa_val and condition_render and condition_render.values:
                for cond_val in condition_render.values:
                    if _check_ssa_value_equivalence(ssa_val, cond_val, ssa_func):
                        score += 5
                        break
            return score

        init_candidates.sort(key=_init_candidate_score, reverse=True)
        init_var, init_value, _ = init_candidates[0]
        init_ssa_map = {name: ssa_val for name, _, ssa_val in init_candidates}

    if not init_var:
        return None

    # Step 3: Find increment at end of loop body
    # Look in blocks that jump back to header (back edges)
    # Pattern 1: Direct increment (inst has outputs with init_var name)
    # Pattern 2: ASGN instruction (inputs=[value, &init_var])
    increment_text = None
    increment_var = init_var
    increment_ssa_val = None
    loop_vars = {init_var} | condition_candidates
    for back_edge in loop.back_edges:
        source_id = back_edge.source
        target_id = back_edge.target
        if target_id == loop.header:
            # This block jumps back to header - check for increment
            source_ssa_block = ssa_func.instructions.get(source_id, [])
            for inst in reversed(source_ssa_block):
                # Pattern 1: Direct output (e.g., i = i + 1)
                if inst.outputs and len(inst.outputs) == 1:
                    var_name = _normalize_loop_var_name(inst.outputs[0].alias or inst.outputs[0].name)
                    matches_loop_var = var_name in loop_vars
                    if not matches_loop_var and condition_render and condition_render.values:
                        for cond_val in condition_render.values:
                            if _check_ssa_value_equivalence(inst.outputs[0], cond_val, ssa_func):
                                matches_loop_var = True
                                break
                    if matches_loop_var:
                        # Found assignment to loop variable
                        increment_var = var_name
                        increment_ssa_val = inst.outputs[0]
                        # Check if it's increment pattern: i = i + 1
                        if inst.mnemonic in {"IADD", "CADD", "SADD"}:
                            # Simple increment
                            increment_text = f"{increment_var}++"
                        elif inst.inputs:
                            # Generic assignment - render it
                            inc_expr = formatter.render_value(inst.inputs[0]) if inst.inputs else "?"
                            if f"{increment_var} + 1" in inc_expr or f"({increment_var} + 1)" == inc_expr:
                                increment_text = f"{increment_var}++"
                            else:
                                inc_value = inst.inputs[0]
                                if inc_value and inc_value.producer_inst:
                                    prod_inst = inc_value.producer_inst
                                    if prod_inst.mnemonic in {"IADD", "CADD", "SADD"} and len(prod_inst.inputs) >= 2:
                                        left, right = prod_inst.inputs[0], prod_inst.inputs[1]
                                        other = None
                                        if _check_ssa_value_equivalence(left, inst.outputs[0], ssa_func):
                                            other = right
                                        elif _check_ssa_value_equivalence(right, inst.outputs[0], ssa_func):
                                            other = left
                                        if other:
                                            other_text = formatter.render_value(other)
                                            if other_text in {"1", "1.0", "1.0f"}:
                                                increment_text = f"{increment_var}++"
                                                break
                                increment_text = f"{increment_var} = {inc_expr}"
                        break
                # Pattern 2: ASGN instruction (inputs=[value, &target])
                elif inst.mnemonic == "ASGN" and len(inst.inputs) >= 2:
                    target = inst.inputs[1]
                    target_name = _normalize_loop_var_name(target.alias or target.name)
                    matches_loop_var = target_name in loop_vars
                    if not matches_loop_var and condition_render and condition_render.values:
                        for cond_val in condition_render.values:
                            if _check_ssa_value_equivalence(target, cond_val, ssa_func):
                                matches_loop_var = True
                                break
                    if matches_loop_var:
                        increment_var = target_name
                        increment_ssa_val = target
                        # Found assignment to loop variable
                        # Render the increment expression
                        inc_expr = formatter.render_value(inst.inputs[0])
                        # Check for i+1 pattern
                        if f"{increment_var} + 1" in inc_expr or f"({increment_var} + 1)" == inc_expr:
                            increment_text = f"{increment_var}++"
                        else:
                            inc_value = inst.inputs[0]
                            if inc_value and inc_value.producer_inst:
                                prod_inst = inc_value.producer_inst
                                if prod_inst.mnemonic in {"IADD", "CADD", "SADD"} and len(prod_inst.inputs) >= 2:
                                    left, right = prod_inst.inputs[0], prod_inst.inputs[1]
                                    other = None
                                    if _check_ssa_value_equivalence(left, target, ssa_func):
                                        other = right
                                    elif _check_ssa_value_equivalence(right, target, ssa_func):
                                        other = left
                                    if other:
                                        other_text = formatter.render_value(other)
                                        if other_text in {"1", "1.0", "1.0f"}:
                                            increment_text = f"{increment_var}++"
                                            break
                            increment_text = f"{increment_var} = {inc_expr}"
                        break
            if increment_text:
                break

    if not increment_text:
        return None

    if increment_var != init_var:
        init_ssa = init_ssa_map.get(init_var)
        if init_ssa and increment_ssa_val and _check_ssa_value_equivalence(init_ssa, increment_ssa_val, ssa_func):
            increment_text = increment_text.replace(increment_var, init_var)
            increment_var = init_var
        for candidate_var, candidate_value, _ in init_candidates:
            if candidate_var == increment_var:
                init_var = candidate_var
                init_value = candidate_value
                break

    guard_info = _find_guard_condition(
        loop,
        cfg,
        ssa_func,
        formatter,
        resolver,
        start_to_block,
        loop_vars
    )
    if guard_info:
        condition_text, guard_block = guard_info

    if not condition_text:
        return None

    # Successfully detected for-loop pattern
    # Extract the actual variable name from condition if it's different from init_var
    # Condition is like "(i <= gData28)" - extract the left operand
    import re
    display_var = init_var
    match = re.match(r'!?\(?(\w+)\s*[<>=!]+', condition_text)
    if match:
        cond_var = match.group(1)
        if cond_var != init_var:
            preferred = _score_loop_var_name(cond_var, condition_candidates)
            current = _score_loop_var_name(init_var, condition_candidates)
            if preferred >= current:
                # Use the variable name from condition (it's the aliased form)
                display_var = cond_var
                # Also update increment to use display_var
                increment_text = increment_text.replace(init_var, display_var)
                condition_text = condition_text.replace(init_var, display_var)
            else:
                condition_text = condition_text.replace(cond_var, init_var)

    return ForLoopInfo(
        var=display_var,
        init=init_value,
        condition=condition_text,
        increment=increment_text,
        init_var=init_var,
        guard_block=guard_block
    )


def _detect_while_loop(
    loop: NaturalLoop,
    cfg: CFG,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    global_map: Optional[Dict[int, str]] = None
) -> Optional[WhileLoopInfo]:
    """
    Detect while-loop pattern in a natural loop (Ghidra-style).

    Pattern:
    - Header block has conditional jump (the loop condition)
    - One branch goes to loop body
    - Other branch goes to exit (outside loop)
    - Body eventually jumps back to header (back edge)

    CFG structure:
        [header/condition] --false--> [exit]
               |
               v (true)
           [body blocks]
               |
               v (back edge)
        [header/condition]

    This differs from for-loop:
    - No clear initialization in predecessor
    - No clear increment at back edge
    - Just condition test at header

    Args:
        loop: Natural loop to analyze
        cfg: Control flow graph
        ssa_func: SSA function data
        formatter: Expression formatter
        resolver: Opcode resolver
        start_to_block: Address to block ID mapping
        global_map: Global variable name resolution

    Returns:
        WhileLoopInfo if pattern matches, None otherwise
    """
    header_block = cfg.blocks.get(loop.header)
    if not header_block or not header_block.instructions:
        return None

    # Check if header ends with conditional jump
    last_instr = header_block.instructions[-1]
    if not resolver.is_conditional_jump(last_instr.opcode):
        return None

    # Get successors
    if len(header_block.successors) != 2:
        return None

    # Determine which successor is exit (outside loop) and which is body (inside loop)
    exit_block = None
    body_entry = None

    for succ in header_block.successors:
        if succ not in loop.body:
            exit_block = succ
        else:
            if succ != loop.header:  # Don't count self-loop
                body_entry = succ

    # If no clear exit block found, not a while pattern
    if exit_block is None:
        return None

    # If no body entry (e.g., all successors outside loop), not a while pattern
    if body_entry is None:
        # Could be a do-while instead (body comes before condition)
        return None

    # Extract condition from header
    condition_render = render_condition(
        ssa_func,
        loop.header,
        formatter,
        cfg,
        resolver,
        negate=None  # We'll determine proper polarity
    )

    condition_text = condition_render.text or ""
    if not condition_text:
        return None

    # Determine condition polarity
    # JZ: jump if zero (false) -> jump target is exit when condition is false
    # JNZ: jump if not zero (true) -> jump target is exit when condition is true
    mnemonic = resolver.get_mnemonic(last_instr.opcode)
    jump_target = start_to_block.get(last_instr.arg1)

    if jump_target == exit_block:
        # Jump goes to exit
        if mnemonic == "JZ":
            # JZ to exit: continue when condition is TRUE
            # Condition text is the "break" condition, so invert for "continue" condition
            condition_text = _invert_condition_text(condition_text)
        # JNZ to exit: continue when condition is FALSE - already correct
    else:
        # Jump goes to body (exit is fallthrough)
        if mnemonic == "JNZ":
            # JNZ to body: continue when condition is TRUE - already correct
            pass
        else:
            # JZ to body: continue when condition is FALSE, invert
            condition_text = _invert_condition_text(condition_text)

    # Get all body blocks (all blocks in loop except header if it's just condition)
    body_blocks = set(loop.body)
    body_blocks.discard(loop.header)  # Header is condition, not body

    return WhileLoopInfo(
        condition=condition_text,
        header_block=loop.header,
        body_blocks=body_blocks,
        exit_block=exit_block
    )


def _detect_do_while_loop(
    loop: NaturalLoop,
    cfg: CFG,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    global_map: Optional[Dict[int, str]] = None
) -> Optional[DoWhileLoopInfo]:
    """
    Detect do-while loop pattern in a natural loop (Ghidra-style).

    Pattern:
    - Body executes at least once before condition check
    - Condition block at the END of the loop (has the back edge)
    - Condition jumps back to body start on true, exits on false

    CFG structure:
        [body_start] <-- entry from outside loop
            |
            v
        [body blocks]
            |
            v
        [condition] --true--> [body_start] (back edge)
            |
            v (false)
        [exit]

    Key difference from while loop:
    - Loop header is NOT the condition block
    - Condition is at the back edge source, not header

    Args:
        loop: Natural loop to analyze
        cfg: Control flow graph
        ssa_func: SSA function data
        formatter: Expression formatter
        resolver: Opcode resolver
        start_to_block: Address to block ID mapping
        global_map: Global variable name resolution

    Returns:
        DoWhileLoopInfo if pattern matches, None otherwise
    """
    header_block = cfg.blocks.get(loop.header)
    if not header_block or not header_block.instructions:
        return None

    # For do-while, header should NOT have conditional jump
    # (or if it does, it's not the loop condition - it's inner control flow)
    last_header_instr = header_block.instructions[-1]

    # Find the back edge - the condition is at the source of the back edge
    condition_block_id = None
    for back_edge in loop.back_edges:
        if back_edge.target == loop.header:
            condition_block_id = back_edge.source
            break

    if condition_block_id is None:
        return None

    # Condition block must end with conditional jump
    condition_block = cfg.blocks.get(condition_block_id)
    if not condition_block or not condition_block.instructions:
        return None

    last_cond_instr = condition_block.instructions[-1]
    if not resolver.is_conditional_jump(last_cond_instr.opcode):
        # Not a conditional back edge - could be unconditional loop
        return None

    # Determine exit block (the false target of the condition)
    exit_block = None
    for succ in condition_block.successors:
        if succ not in loop.body:
            exit_block = succ
            break

    if exit_block is None:
        # All successors are in loop body - unusual, might be nested loop
        return None

    # Verify the conditional jump structure
    # One branch should go to header (back edge), other to exit
    mnemonic = resolver.get_mnemonic(last_cond_instr.opcode)
    jump_target = start_to_block.get(last_cond_instr.arg1)

    # Extract condition
    condition_render = render_condition(
        ssa_func,
        condition_block_id,
        formatter,
        cfg,
        resolver,
        negate=None
    )

    condition_text = condition_render.text or ""
    if not condition_text:
        return None

    # Determine condition polarity for do-while
    # We want: "do { body } while (condition)" where condition is TRUE to continue
    if jump_target == loop.header:
        # Jump goes back to header (continue loop)
        if mnemonic == "JNZ":
            # JNZ back to header: continue when TRUE - correct
            pass
        else:
            # JZ back to header: continue when FALSE, invert
            condition_text = _invert_condition_text(condition_text)
    else:
        # Jump goes to exit
        if mnemonic == "JZ":
            # JZ to exit: exit when FALSE, so continue when TRUE - correct
            pass
        else:
            # JNZ to exit: exit when TRUE, so continue when FALSE - invert
            condition_text = _invert_condition_text(condition_text)

    # Body blocks are all loop blocks
    body_blocks = set(loop.body)

    return DoWhileLoopInfo(
        condition=condition_text,
        body_start_block=loop.header,
        condition_block=condition_block_id,
        body_blocks=body_blocks,
        exit_block=exit_block
    )


def _detect_loop_type(
    loop: NaturalLoop,
    cfg: CFG,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    global_map: Optional[Dict[int, str]] = None
) -> Optional[object]:
    """
    Detect the type of loop pattern and return the appropriate info object.

    Priority order (most specific to least specific):
    1. For-loop: has init, condition at header, increment at back edge
    2. While-loop: condition at header, no clear init/increment
    3. Do-while loop: condition at back edge, body executes first

    Args:
        loop: Natural loop to analyze
        cfg: Control flow graph
        ssa_func: SSA function data
        formatter: Expression formatter
        resolver: Opcode resolver
        start_to_block: Address to block ID mapping
        global_map: Global variable name resolution

    Returns:
        ForLoopInfo, WhileLoopInfo, or DoWhileLoopInfo if a pattern matches,
        None if no loop pattern detected
    """
    # Try for-loop first (most specific pattern)
    for_loop = _detect_for_loop(
        loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map
    )
    if for_loop:
        return for_loop

    # Try while-loop (condition at header)
    while_loop = _detect_while_loop(
        loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map
    )
    if while_loop:
        return while_loop

    # Try do-while loop (condition at back edge)
    do_while_loop = _detect_do_while_loop(
        loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map
    )
    if do_while_loop:
        return do_while_loop

    return None
