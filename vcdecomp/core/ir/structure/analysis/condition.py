"""
Condition expression extraction and combination utilities.

This module contains functions for extracting condition expressions from
conditional jump blocks and combining multiple conditions with logical operators.
"""

from __future__ import annotations

from typing import List, Optional, Set, Dict, Tuple

from ...ssa import SSAFunction
from ...expr import ExpressionFormatter, COMPARISON_OPS
from ....disasm import opcodes
from ...parenthesization import ExpressionContext
from ...cfg import CFG
from ..patterns.models import CompoundCondition


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
    block = cfg.blocks.get(block_id)
    if not block or not block.instructions:
        return None

    # Find the last conditional jump in the block
    for instr in reversed(block.instructions):
        if resolver.is_conditional_jump(instr.opcode):
            # Found conditional jump, now find corresponding SSA instruction
            ssa_block = ssa_func.instructions.get(block_id, [])

            for ssa_inst in ssa_block:
                if ssa_inst.address == instr.address and ssa_inst.inputs:
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
            break

    return None


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
    mnemonic = resolver.get_mnemonic(last_instr.opcode)

    # Block must end with conditional jump (JZ/JNZ) to be part of AND chain
    if not resolver.is_conditional_jump(last_instr.opcode):
        return ([], None, None)

    # This is the first block in potential AND chain
    chain_blocks = [start_block_id]
    false_target_addr = last_instr.arg1  # Where to go if condition fails
    false_target = start_to_block.get(false_target_addr)

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
    if resolver.is_conditional_jump(ft_last_instr.opcode):
        # Check if it jumps to the SAME false target
        if ft_last_instr.arg1 == false_target_addr:
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
