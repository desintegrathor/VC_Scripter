"""
Condition expression extraction and combination utilities.

This module contains functions for extracting condition expressions from
conditional jump blocks and combining multiple conditions with logical operators.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Set, Dict, Tuple

from ...ssa import SSAFunction, SSAValue
from ...expr import ExpressionFormatter, COMPARISON_OPS
from ....disasm import opcodes
from ...parenthesization import ExpressionContext, is_simple_expression
from ...cfg import CFG
from ..patterns.models import CompoundCondition
from .value_trace import (
    _trace_value_to_function_call,
    _find_xcall_with_lld_in_predecessors,
    call_is_condition_only,
    _build_condition_value_map,
)


@dataclass(frozen=True)
class ConditionRender:
    text: str
    values: List[SSAValue]
    addresses: List[int]
    call_is_condition_only: bool = False
    call_statement_text: Optional[str] = None


def _find_condition_jump(block, resolver: opcodes.OpcodeResolver):
    for instr in reversed(block.instructions):
        if resolver.is_conditional_jump(instr.opcode):
            return instr
    return None


def _find_ssa_condition_value(ssa_block, instr_address: int):
    for ssa_inst in ssa_block:
        if ssa_inst.address == instr_address and ssa_inst.inputs:
            return ssa_inst.inputs[0]
    return None


def _find_call_inst_for_condition(
    ssa_func: SSAFunction,
    value,
    max_depth: int = 8,
    visited: Optional[Set[int]] = None
):
    if not value or max_depth <= 0:
        return None
    if visited is None:
        visited = set()
    if id(value) in visited:
        return None
    visited.add(id(value))

    producer = value.producer_inst
    if not producer:
        return None

    if producer.mnemonic in {"CALL", "XCALL"}:
        return producer

    if producer.mnemonic == "LLD":
        block_instructions = ssa_func.instructions.get(producer.block_id, [])
        lld_index = None
        for idx, inst in enumerate(block_instructions):
            if inst.address == producer.address:
                lld_index = idx
                break
        if lld_index is not None:
            for idx in range(lld_index - 1, max(0, lld_index - 5), -1):
                prev_inst = block_instructions[idx]
                if prev_inst.mnemonic in {"CALL", "XCALL"}:
                    return prev_inst

    if producer.mnemonic == "LCP":
        stack_offset = None
        if producer.instruction and producer.instruction.instruction:
            stack_offset = producer.instruction.instruction.arg1
        xcall_lld = _find_xcall_with_lld_in_predecessors(
            block_id=producer.block_id,
            stack_offset=stack_offset,
            ssa_func=ssa_func,
            max_depth=4,
        )
        if xcall_lld:
            return xcall_lld[0]

    if producer.mnemonic == "PHI":
        for phi_input in producer.inputs:
            call_inst = _find_call_inst_for_condition(
                ssa_func, phi_input, max_depth - 1, visited
            )
            if call_inst:
                return call_inst

    for input_value in producer.inputs:
        call_inst = _find_call_inst_for_condition(
            ssa_func, input_value, max_depth - 1, visited
        )
        if call_inst:
            return call_inst

    return None


def _collect_condition_values(
    value,
    max_depth: int = 8,
    values: Optional[List[SSAValue]] = None,
    addresses: Optional[Set[int]] = None,
    visited: Optional[Set[int]] = None
) -> Tuple[List[SSAValue], Set[int]]:
    if values is None:
        values = []
    if addresses is None:
        addresses = set()
    if visited is None:
        visited = set()
    if not value or max_depth < 0 or id(value) in visited:
        return values, addresses

    visited.add(id(value))
    values.append(value)

    producer = value.producer_inst
    if producer:
        addresses.add(producer.address)
        for input_value in producer.inputs:
            _collect_condition_values(
                input_value,
                max_depth - 1,
                values=values,
                addresses=addresses,
                visited=visited
            )

    return values, addresses


def render_condition(
    ssa_func: SSAFunction,
    block_id: int,
    formatter: ExpressionFormatter,
    cfg: CFG,
    resolver: opcodes.OpcodeResolver,
    negate: Optional[bool] = None
) -> ConditionRender:
    """
    Render a condition for a block's conditional jump.

    Returns a ConditionRender containing the rendered text, SSA values used in the
    condition, and instruction addresses that contribute to the condition.
    """
    block = cfg.blocks.get(block_id)
    if not block or not block.instructions:
        return ConditionRender(text=f"cond_{block_id}", values=[], addresses=[])

    jump_instr = _find_condition_jump(block, resolver)
    if not jump_instr:
        return ConditionRender(text=f"cond_{block_id}", values=[], addresses=[])

    ssa_block = ssa_func.instructions.get(block_id, [])
    cond_value = _find_ssa_condition_value(ssa_block, jump_instr.address)
    if not cond_value:
        return ConditionRender(text=f"cond_{block_id}", values=[], addresses=[])

    values: List[SSAValue] = []
    addresses: Set[int] = set()
    visited: Set[int] = set()
    _collect_condition_values(
        cond_value,
        values=values,
        addresses=addresses,
        visited=visited
    )
    addresses.add(jump_instr.address)

    call_inst = _find_call_inst_for_condition(ssa_func, cond_value)
    call_statement_text = None
    call_only = False
    rename_map_backup = None
    condition_value_map = _build_condition_value_map(
        ssa_func,
        block_id,
        jump_instr.address,
        values,
        formatter,
    )
    if condition_value_map and hasattr(formatter, "_rename_map"):
        rename_map_backup = formatter._rename_map
        merged_map = dict(formatter._rename_map)
        for key, value in condition_value_map.items():
            merged_map.setdefault(key, value)
        formatter._rename_map = merged_map

    try:
        if call_inst:
            call_statement_text = formatter._format_call(call_inst).strip()
            call_only = call_is_condition_only(ssa_func, call_inst, addresses)
            if call_only:
                addresses.add(call_inst.address)
                for input_value in call_inst.inputs:
                    _collect_condition_values(
                        input_value,
                        values=values,
                        addresses=addresses,
                        visited=visited
                    )

        cond_expr = None
        call_expr = _trace_value_to_function_call(ssa_func, cond_value, formatter)
        if call_expr and call_only:
            cond_expr = call_expr
        else:
            if cond_value.producer_inst and cond_value.producer_inst.mnemonic in COMPARISON_OPS:
                cond_expr = formatter._inline_expression(
                    cond_value,
                    context=ExpressionContext.IN_CONDITION
                )
            elif cond_value.producer_inst and cond_value.producer_inst.mnemonic == "PHI":
                for phi_input in cond_value.producer_inst.inputs:
                    if phi_input.producer_inst and phi_input.producer_inst.mnemonic in COMPARISON_OPS:
                        cond_expr = formatter._inline_expression(
                            phi_input,
                            context=ExpressionContext.IN_CONDITION
                        )
                        break

        if cond_expr is None:
            cond_expr = formatter.render_value(
                cond_value,
                context=ExpressionContext.IN_CONDITION
            )
            if cond_expr.lstrip('-').isdigit():
                alias = cond_value.alias or cond_value.name
                if alias and not alias.startswith("data_"):
                    cond_expr = alias
    finally:
        if rename_map_backup is not None:
            formatter._rename_map = rename_map_backup

    if negate is None:
        mnemonic = resolver.get_mnemonic(jump_instr.opcode)
        if mnemonic == "JZ":
            negate = True
        elif mnemonic == "JNZ":
            negate = False
        else:
            negate = False

    if negate:
        if is_simple_expression(cond_expr):
            cond_expr = f"!{cond_expr}"
        else:
            cond_expr = f"!({cond_expr})"

    return ConditionRender(
        text=cond_expr,
        values=values,
        addresses=sorted(addresses),
        call_is_condition_only=call_only,
        call_statement_text=call_statement_text,
    )


def _extract_condition_from_block(
    block_id: int,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    cfg: CFG,
    resolver: opcodes.OpcodeResolver
) -> Optional[str]:
    """
    Extract condition expression from a block ending with conditional jump.

    Finds the JZ/JNZ instruction in the block and extracts its condition
    from the corresponding SSA instruction.

    Args:
        block_id: Block ID to extract condition from
        ssa_func: SSA function containing the block
        formatter: Expression formatter for rendering
        cfg: Control flow graph
        resolver: Opcode resolver

    Returns:
        Rendered condition expression, or None if not found/not applicable
    """
    render = render_condition(
        ssa_func,
        block_id,
        formatter,
        cfg,
        resolver,
        negate=False
    )
    return render.text if render.text else None


def _extract_condition_expr(
    ssa_func: SSAFunction,
    block_id: int,
    instr_address: int,
    formatter: ExpressionFormatter,
    resolver: opcodes.OpcodeResolver
) -> Optional[str]:
    """
    Legacy wrapper for extracting condition expressions.

    This function provides backward compatibility for code that doesn't have
    access to the CFG. It directly searches SSA instructions for the condition.

    Args:
        ssa_func: SSA function containing the block
        block_id: Block ID to extract condition from
        instr_address: Address of the conditional jump instruction
        formatter: Expression formatter for rendering
        resolver: Opcode resolver

    Returns:
        Rendered condition expression, or None if not found
    """
    ssa_block = ssa_func.instructions.get(block_id, [])

    for ssa_inst in ssa_block:
        if ssa_inst.address == instr_address and ssa_inst.inputs:
            cond_value = ssa_inst.inputs[0]

            # If condition comes from comparison operation, inline it
            if cond_value.producer_inst and cond_value.producer_inst.mnemonic in COMPARISON_OPS:
                cond_expr = formatter._inline_expression(
                    cond_value,
                    context=ExpressionContext.IN_CONDITION
                )
                return cond_expr

            # If condition is PHI, check if any input is a comparison
            if cond_value.producer_inst and cond_value.producer_inst.mnemonic == "PHI":
                for phi_input in cond_value.producer_inst.inputs:
                    if phi_input.producer_inst and phi_input.producer_inst.mnemonic in COMPARISON_OPS:
                        cond_expr = formatter._inline_expression(
                            phi_input,
                            context=ExpressionContext.IN_CONDITION
                        )
                        return cond_expr

            # Fallback: use render_value
            cond_expr = formatter.render_value(
                cond_value,
                context=ExpressionContext.IN_CONDITION
            )

            # If renders as just a number, use SSA name/alias instead
            if cond_expr.lstrip('-').isdigit():
                alias = cond_value.alias or cond_value.name
                if alias and not alias.startswith("data_"):
                    cond_expr = alias

            return cond_expr

    return None


def _combine_conditions(
    conditions: List,  # List[Union[str, CompoundCondition]]
    operator: str,
    preserve_style: bool = True
) -> str:
    """
    Combine multiple conditions with && or || operators.

    Applies proper parenthesization to match original code style.

    Args:
        conditions: List of condition strings or CompoundCondition objects
        operator: "&&" or "||"
        preserve_style: If True, add extra parentheses to match original style

    Returns:
        Combined condition expression
    """
    if len(conditions) == 0:
        return "true"
    if len(conditions) == 1:
        cond = conditions[0]
        if isinstance(cond, CompoundCondition):
            return _combine_conditions(cond.conditions, cond.operator, preserve_style)
        return str(cond)

    # Render each condition
    rendered = []
    for cond in conditions:
        if isinstance(cond, CompoundCondition):
            # Recursively render compound conditions
            sub_expr = _combine_conditions(cond.conditions, cond.operator, preserve_style)
            # Wrap in parentheses for clarity (matches original style)
            rendered.append(f"({sub_expr})")
        else:
            rendered.append(str(cond))

    # Combine with operator
    if operator == "||":
        # OR style: (A && B) || (C && D)
        # CompoundConditions already wrapped above
        combined = f" {operator} ".join(rendered)
    else:
        # AND style: A && B && C
        # Don't add extra parentheses for simple AND
        combined = f" {operator} ".join(rendered)

    return combined


def _collect_and_chain(
    start_block_id: int,
    cfg: CFG,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    visited: Set[int]
) -> Tuple[List[int], Optional[int], Optional[int]]:
    """
    Collect blocks forming an AND chain by following fallthrough paths.

    An AND chain is a sequence of blocks where:
    1. Each block ends with JZ jumping to the same FALSE target
    2. Blocks are connected via fallthrough (sequential addresses)
    3. Final block in chain has a fallthrough to JMP block (TRUE target)

    Example CFG structure:
        Block A: cond1; JZ false_target  → fallthrough to B
        Block B: cond2; JZ false_target  → fallthrough to C
        Block C: JMP true_target

    This represents: if (cond1 && cond2) goto true_target else goto false_target

    Args:
        start_block_id: Block ID to start from
        cfg: Control flow graph
        resolver: Opcode resolver
        start_to_block: Address to block ID mapping
        visited: Set of already visited blocks (to prevent infinite loops)

    Returns:
        Tuple of (chain_blocks, true_target, false_target):
        - chain_blocks: List of block IDs in the AND chain
        - true_target: Block ID to jump to when all conditions are TRUE
        - false_target: Block ID to jump to when any condition is FALSE
        Returns ([], None, None) if no AND chain detected
    """
    if start_block_id in visited:
        return ([], None, None)

    visited.add(start_block_id)

    block = cfg.blocks.get(start_block_id)
    if not block or not block.instructions:
        return ([], None, None)

    last_instr = block.instructions[-1]
    conditional_instr = None
    explicit_true_target = None

    # Block must contain a conditional jump (JZ/JNZ) to be part of a chain.
    if resolver.is_conditional_jump(last_instr.opcode):
        conditional_instr = last_instr
    elif len(block.instructions) >= 2:
        second_last = block.instructions[-2]
        if (resolver.is_conditional_jump(second_last.opcode) and
                resolver.get_mnemonic(last_instr.opcode) == "JMP"):
            conditional_instr = second_last
            explicit_true_target = start_to_block.get(last_instr.arg1)

    if conditional_instr is None:
        return ([], None, None)

    # This is the first block in potential AND chain
    chain_blocks = [start_block_id]
    false_target_addr = conditional_instr.arg1  # Where to go if condition fails
    false_target = start_to_block.get(false_target_addr)

    if explicit_true_target is not None:
        return (chain_blocks, explicit_true_target, false_target)

    # Follow fallthrough path to find more conditions or TRUE target
    fallthrough_addr = last_instr.address + 1
    fallthrough_block_id = start_to_block.get(fallthrough_addr)

    if not fallthrough_block_id:
        return (chain_blocks, None, false_target)

    fallthrough_block = cfg.blocks.get(fallthrough_block_id)
    if not fallthrough_block or not fallthrough_block.instructions:
        return (chain_blocks, None, false_target)

    # Check if fallthrough block is just a JMP (end of AND chain, this is TRUE target)
    if len(fallthrough_block.instructions) == 1:
        ft_last = fallthrough_block.instructions[-1]
        if resolver.get_mnemonic(ft_last.opcode) == "JMP":
            # This JMP is where we go if all conditions pass
            true_target = start_to_block.get(ft_last.arg1)
            return (chain_blocks, true_target, false_target)

    # Check if fallthrough block is another condition in the AND chain
    ft_last_instr = fallthrough_block.instructions[-1]
    ft_conditional = None
    if resolver.is_conditional_jump(ft_last_instr.opcode):
        ft_conditional = ft_last_instr
    elif len(fallthrough_block.instructions) >= 2:
        ft_second_last = fallthrough_block.instructions[-2]
        if (resolver.is_conditional_jump(ft_second_last.opcode) and
                resolver.get_mnemonic(ft_last_instr.opcode) == "JMP"):
            ft_conditional = ft_second_last

    if ft_conditional:
        # Check if it jumps to the SAME false target
        if ft_conditional.arg1 == false_target_addr:
            # It's part of the AND chain! Recursively collect the rest
            rest_chain, true_target, _ = _collect_and_chain(
                fallthrough_block_id, cfg, resolver, start_to_block, visited
            )
            if rest_chain:
                chain_blocks.extend(rest_chain)
                # CRITICAL FIX: If recursive call returned true_target=None,
                # use the fallthrough block of the last condition as the true target
                if true_target is None:
                    # Find the last block's fallthrough
                    last_block = cfg.blocks.get(chain_blocks[-1])
                    if last_block and last_block.instructions:
                        last_addr = last_block.instructions[-1].address
                        last_fallthrough_addr = last_addr + 1
                        true_target = start_to_block.get(last_fallthrough_addr)

                return (chain_blocks, true_target, false_target)
        else:
            # Fallthrough is a conditional jump but to DIFFERENT target (not AND chain)
            # This could be OR pattern or something else - return None for true_target
            return (chain_blocks, None, false_target)

    # Fallthrough doesn't continue the AND chain and is not a conditional jump
    # The fallthrough block itself is the TRUE target (when all conditions pass)
    # This is the common case for AND chains ending with normal code
    return (chain_blocks, fallthrough_block_id, false_target)


def _collect_or_chain(
    start_block_id: int,
    cfg: CFG,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    visited: Set[int]
) -> Tuple[List[int], Optional[int], Optional[int]]:
    """
    Collect blocks forming an OR chain by following fallthrough paths.

    An OR chain is a sequence of blocks where:
    1. Each block ends with JNZ jumping to the same TRUE target
    2. Blocks are connected via fallthrough (sequential addresses)
    3. Final block in chain has a fallthrough to JMP block (FALSE target)

    Example CFG structure:
        Block A: cond1; JNZ true_target  → fallthrough to B
        Block B: cond2; JNZ true_target  → fallthrough to C
        Block C: JMP false_target

    This represents: if (cond1 || cond2) goto true_target else goto false_target

    Args:
        start_block_id: Block ID to start from
        cfg: Control flow graph
        resolver: Opcode resolver
        start_to_block: Address to block ID mapping
        visited: Set of already visited blocks (to prevent infinite loops)

    Returns:
        Tuple of (chain_blocks, true_target, false_target):
        - chain_blocks: List of block IDs in the OR chain
        - true_target: Block ID to jump to when any condition is TRUE
        - false_target: Block ID to jump to when all conditions are FALSE
        Returns ([], None, None) if no OR chain detected
    """
    if start_block_id in visited:
        return ([], None, None)

    visited.add(start_block_id)

    block = cfg.blocks.get(start_block_id)
    if not block or not block.instructions:
        return ([], None, None)

    last_instr = block.instructions[-1]
    conditional_instr = None
    explicit_false_target = None

    # Block must contain a conditional jump (JNZ specifically) to be part of OR chain
    if resolver.is_conditional_jump(last_instr.opcode):
        mnemonic = resolver.get_mnemonic(last_instr.opcode)
        if mnemonic == "JNZ":
            conditional_instr = last_instr
    elif len(block.instructions) >= 2:
        second_last = block.instructions[-2]
        mnemonic = resolver.get_mnemonic(second_last.opcode)
        if (mnemonic == "JNZ" and
                resolver.get_mnemonic(last_instr.opcode) == "JMP"):
            conditional_instr = second_last
            explicit_false_target = start_to_block.get(last_instr.arg1)

    if conditional_instr is None:
        return ([], None, None)

    # This is the first block in potential OR chain
    chain_blocks = [start_block_id]
    true_target_addr = conditional_instr.arg1  # Where to go if condition is true
    true_target = start_to_block.get(true_target_addr)

    if explicit_false_target is not None:
        return (chain_blocks, true_target, explicit_false_target)

    # Follow fallthrough path to find more conditions or FALSE target
    fallthrough_addr = last_instr.address + 1
    fallthrough_block_id = start_to_block.get(fallthrough_addr)

    if not fallthrough_block_id:
        return (chain_blocks, true_target, None)

    fallthrough_block = cfg.blocks.get(fallthrough_block_id)
    if not fallthrough_block or not fallthrough_block.instructions:
        return (chain_blocks, true_target, None)

    # Check if fallthrough block is just a JMP (end of OR chain, this is FALSE target)
    if len(fallthrough_block.instructions) == 1:
        ft_last = fallthrough_block.instructions[-1]
        if resolver.get_mnemonic(ft_last.opcode) == "JMP":
            # This JMP is where we go if all conditions fail
            false_target = start_to_block.get(ft_last.arg1)
            return (chain_blocks, true_target, false_target)

    # Check if fallthrough block is another condition in the OR chain
    ft_last_instr = fallthrough_block.instructions[-1]
    ft_conditional = None
    if resolver.is_conditional_jump(ft_last_instr.opcode):
        if resolver.get_mnemonic(ft_last_instr.opcode) == "JNZ":
            ft_conditional = ft_last_instr
    elif len(fallthrough_block.instructions) >= 2:
        ft_second_last = fallthrough_block.instructions[-2]
        if (resolver.is_conditional_jump(ft_second_last.opcode) and
                resolver.get_mnemonic(ft_second_last.opcode) == "JNZ" and
                resolver.get_mnemonic(ft_last_instr.opcode) == "JMP"):
            ft_conditional = ft_second_last

    if ft_conditional:
        # Check if it jumps to the SAME true target
        if ft_conditional.arg1 == true_target_addr:
            # It's part of the OR chain! Recursively collect the rest
            rest_chain, _, false_target = _collect_or_chain(
                fallthrough_block_id, cfg, resolver, start_to_block, visited
            )
            if rest_chain:
                chain_blocks.extend(rest_chain)
                # CRITICAL FIX: If recursive call returned false_target=None,
                # use the fallthrough block of the last condition as the false target
                if false_target is None:
                    # Find the last block's fallthrough
                    last_block = cfg.blocks.get(chain_blocks[-1])
                    if last_block and last_block.instructions:
                        last_addr = last_block.instructions[-1].address
                        last_fallthrough_addr = last_addr + 1
                        false_target = start_to_block.get(last_fallthrough_addr)

                return (chain_blocks, true_target, false_target)
        else:
            # Fallthrough is a conditional jump but to DIFFERENT target (not OR chain)
            return (chain_blocks, true_target, None)

    # Fallthrough doesn't continue the OR chain and is not a JNZ
    # The fallthrough block itself is the FALSE target (when all conditions fail)
    return (chain_blocks, true_target, fallthrough_block_id)
