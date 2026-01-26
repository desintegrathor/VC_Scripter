"""
Bitwise operation simplification rules.

This module implements rules for simplifying bitwise operations:
- RuleAndMask: (x & m1) & m2 → x & (m1 & m2)
- RuleOrMask: (x | m1) | m2 → x | (m1 | m2)
- RuleXorCancel: x ^ x → 0, x ^ 0 → x
"""

import logging
from typing import Optional

from .base import (
    SimplificationRule,
    is_constant,
    get_constant_value,
    create_constant_value,
)
from ..ssa import SSAFunction, SSAInstruction

logger = logging.getLogger(__name__)


class RuleAndMask(SimplificationRule):
    """
    Simplify nested AND operations with constants.

    Examples:
        (x & 0xff) & 0x0f → x & 0x0f
        (x & m1) & m2 → x & (m1 & m2)

    From Ghidra's ruleaction.cc.
    """

    def __init__(self):
        super().__init__("RuleAndMask")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BA":  # Bitwise AND
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant
        if not is_constant(right):
            return False

        # Left must be result of another AND with constant
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic != "BA":
            return False
        if len(left.producer_inst.inputs) != 2:
            return False

        # The inner AND's right operand must also be constant
        inner_right = left.producer_inst.inputs[1]
        return is_constant(inner_right)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs
        inner_and = left.producer_inst

        # Get mask values
        outer_mask = get_constant_value(right, ssa_func)
        inner_mask = get_constant_value(inner_and.inputs[1], ssa_func)

        if outer_mask is None or inner_mask is None:
            return None

        # Combine masks
        combined_mask = outer_mask & inner_mask

        # Create new instruction: x & combined_mask
        combined_const = create_constant_value(
            combined_mask, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="BA",
            address=inst.address,
            inputs=[inner_and.inputs[0], combined_const],  # x, combined_mask
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(
            f"RuleAndMask: (x & 0x{inner_mask:x}) & 0x{outer_mask:x} → x & 0x{combined_mask:x}"
        )
        return new_inst


class RuleOrMask(SimplificationRule):
    """
    Simplify nested OR operations with constants.

    Examples:
        (x | 0x0f) | 0xff → x | 0xff
        (x | m1) | m2 → x | (m1 | m2)
    """

    def __init__(self):
        super().__init__("RuleOrMask")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BO":  # Bitwise OR
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant
        if not is_constant(right):
            return False

        # Left must be result of another OR with constant
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic != "BO":
            return False
        if len(left.producer_inst.inputs) != 2:
            return False

        # The inner OR's right operand must also be constant
        inner_right = left.producer_inst.inputs[1]
        return is_constant(inner_right)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs
        inner_or = left.producer_inst

        # Get mask values
        outer_mask = get_constant_value(right, ssa_func)
        inner_mask = get_constant_value(inner_or.inputs[1], ssa_func)

        if outer_mask is None or inner_mask is None:
            return None

        # Combine masks
        combined_mask = outer_mask | inner_mask

        # Create new instruction: x | combined_mask
        combined_const = create_constant_value(
            combined_mask, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="BO",
            address=inst.address,
            inputs=[inner_or.inputs[0], combined_const],  # x, combined_mask
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(
            f"RuleOrMask: (x | 0x{inner_mask:x}) | 0x{outer_mask:x} → x | 0x{combined_mask:x}"
        )
        return new_inst


class RuleXorCancel(SimplificationRule):
    """
    Simplify XOR operations.

    Examples:
        x ^ x → 0
        x ^ 0 → x
    """

    def __init__(self):
        super().__init__("RuleXorCancel")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BX":  # Bitwise XOR
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x ^ x → 0
        if left.name == right.name:
            const_zero = create_constant_value(0, inst.outputs[0].value_type, ssa_func)
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="CONST",
                address=inst.address,
                inputs=[const_zero],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleXorCancel: x ^ x → 0")
            return new_inst

        # Check for x ^ 0 → x
        right_val = get_constant_value(right, ssa_func)
        if right_val == 0:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleXorCancel: x ^ 0 → x")
            return new_inst

        return None
