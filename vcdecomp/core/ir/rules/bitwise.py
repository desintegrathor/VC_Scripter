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


class RuleShiftByZero(SimplificationRule):
    """
    Simplify shifts by zero.

    Examples:
        x << 0 → x
        x >> 0 → x
    """

    def __init__(self):
        super().__init__("RuleShiftByZero")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("LS", "RS", "SHL", "SHR"):
            return False
        if len(inst.inputs) != 2:
            return False

        # Shift amount (right operand) must be 0
        right = inst.inputs[1]
        if not is_constant(right):
            return False

        shift_amount = get_constant_value(right, ssa_func)
        return shift_amount == 0

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left = inst.inputs[0]

        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="COPY",
            address=inst.address,
            inputs=[left],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleShiftByZero: x {inst.mnemonic} 0 → x")
        return new_inst


class RuleDoubleShift(SimplificationRule):
    """
    Combine consecutive shifts in the same direction.

    Examples:
        (x << 2) << 3 → x << 5
        (x >> 1) >> 2 → x >> 3
    """

    def __init__(self):
        super().__init__("RuleDoubleShift")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("LS", "RS", "SHL", "SHR"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant
        if not is_constant(right):
            return False

        # Left must be result of same shift operation
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic != inst.mnemonic:
            return False
        if len(left.producer_inst.inputs) != 2:
            return False

        # Inner shift's amount must also be constant
        inner_right = left.producer_inst.inputs[1]
        return is_constant(inner_right)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs
        inner_shift = left.producer_inst

        # Get shift amounts
        outer_amount = get_constant_value(right, ssa_func)
        inner_amount = get_constant_value(inner_shift.inputs[1], ssa_func)

        if outer_amount is None or inner_amount is None:
            return None

        # Combine shift amounts (mask to 5 bits for safety)
        combined_amount = (inner_amount + outer_amount) & 0x1F

        # Create new instruction: x << combined_amount
        combined_const = create_constant_value(
            combined_amount, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic=inst.mnemonic,
            address=inst.address,
            inputs=[inner_shift.inputs[0], combined_const],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(
            f"RuleDoubleShift: (x {inst.mnemonic} {inner_amount}) {inst.mnemonic} {outer_amount} → x {inst.mnemonic} {combined_amount}"
        )
        return new_inst


class RuleAndWithOr(SimplificationRule):
    """
    Simplify AND of OR operations when one term is common.

    Examples:
        (x | y) & x → x
        x & (x | y) → x

    This is absorption law: x & (x | y) = x
    """

    def __init__(self):
        super().__init__("RuleAndWithOr")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BA":  # Bitwise AND
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Check if either operand is an OR operation
        left_is_or = left.producer_inst and left.producer_inst.mnemonic == "BO"
        right_is_or = right.producer_inst and right.producer_inst.mnemonic == "BO"

        return left_is_or or right_is_or

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Case 1: (x | y) & x → x
        if left.producer_inst and left.producer_inst.mnemonic == "BO":
            or_op = left.producer_inst
            or_left, or_right = or_op.inputs

            if or_left.name == right.name or or_right.name == right.name:
                new_inst = SSAInstruction(
                    block_id=inst.block_id,
                    mnemonic="COPY",
                    address=inst.address,
                    inputs=[right],
                    outputs=inst.outputs,
                    instruction=inst.instruction,
                )
                self.apply_count += 1
                logger.debug(f"RuleAndWithOr: (x | y) & x → x")
                return new_inst

        # Case 2: x & (x | y) → x
        if right.producer_inst and right.producer_inst.mnemonic == "BO":
            or_op = right.producer_inst
            or_left, or_right = or_op.inputs

            if or_left.name == left.name or or_right.name == left.name:
                new_inst = SSAInstruction(
                    block_id=inst.block_id,
                    mnemonic="COPY",
                    address=inst.address,
                    inputs=[left],
                    outputs=inst.outputs,
                    instruction=inst.instruction,
                )
                self.apply_count += 1
                logger.debug(f"RuleAndWithOr: x & (x | y) → x")
                return new_inst

        return None


class RuleOrWithAnd(SimplificationRule):
    """
    Simplify OR of AND operations when one term is common.

    Examples:
        (x & y) | x → x
        x | (x & y) → x

    This is absorption law: x | (x & y) = x
    """

    def __init__(self):
        super().__init__("RuleOrWithAnd")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BO":  # Bitwise OR
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Check if either operand is an AND operation
        left_is_and = left.producer_inst and left.producer_inst.mnemonic == "BA"
        right_is_and = right.producer_inst and right.producer_inst.mnemonic == "BA"

        return left_is_and or right_is_and

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Case 1: (x & y) | x → x
        if left.producer_inst and left.producer_inst.mnemonic == "BA":
            and_op = left.producer_inst
            and_left, and_right = and_op.inputs

            if and_left.name == right.name or and_right.name == right.name:
                new_inst = SSAInstruction(
                    block_id=inst.block_id,
                    mnemonic="COPY",
                    address=inst.address,
                    inputs=[right],
                    outputs=inst.outputs,
                    instruction=inst.instruction,
                )
                self.apply_count += 1
                logger.debug(f"RuleOrWithAnd: (x & y) | x → x")
                return new_inst

        # Case 2: x | (x & y) → x
        if right.producer_inst and right.producer_inst.mnemonic == "BA":
            and_op = right.producer_inst
            and_left, and_right = and_op.inputs

            if and_left.name == left.name or and_right.name == left.name:
                new_inst = SSAInstruction(
                    block_id=inst.block_id,
                    mnemonic="COPY",
                    address=inst.address,
                    inputs=[left],
                    outputs=inst.outputs,
                    instruction=inst.instruction,
                )
                self.apply_count += 1
                logger.debug(f"RuleOrWithAnd: x | (x & y) → x")
                return new_inst

        return None


class RuleAndZero(SimplificationRule):
    """
    Simplify AND with zero.

    Examples:
        x & 0 → 0
        0 & x → 0
    """

    def __init__(self):
        super().__init__("RuleAndZero")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BA":  # Bitwise AND
            return False
        if len(inst.inputs) != 2:
            return False

        # Either operand can be zero
        left, right = inst.inputs
        left_val = get_constant_value(left, ssa_func)
        right_val = get_constant_value(right, ssa_func)

        return left_val == 0 or right_val == 0

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # x & 0 → 0
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
        logger.debug(f"RuleAndZero: x & 0 → 0")
        return new_inst


class RuleOrAllOnes(SimplificationRule):
    """
    Simplify OR with all bits set.

    Examples:
        x | 0xFFFFFFFF → 0xFFFFFFFF
        x | -1 → -1
    """

    def __init__(self):
        super().__init__("RuleOrAllOnes")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BO":  # Bitwise OR
            return False
        if len(inst.inputs) != 2:
            return False

        # Check if either operand is all bits set
        left, right = inst.inputs
        left_val = get_constant_value(left, ssa_func)
        right_val = get_constant_value(right, ssa_func)

        # Check for 0xFFFFFFFF or -1
        return left_val == 0xFFFFFFFF or left_val == -1 or right_val == 0xFFFFFFFF or right_val == -1

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # x | 0xFFFFFFFF → 0xFFFFFFFF
        const_all = create_constant_value(0xFFFFFFFF, inst.outputs[0].value_type, ssa_func)
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="CONST",
            address=inst.address,
            inputs=[const_all],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleOrAllOnes: x | 0xFFFFFFFF → 0xFFFFFFFF")
        return new_inst
