"""
Bitwise operation simplification rules.

This module implements rules for simplifying bitwise operations:
- RuleAndMask: (x & m1) & m2 → x & (m1 & m2)
- RuleOrMask: (x | m1) | m2 → x | (m1 | m2)
- RuleXorCancel: x ^ x → 0, x ^ 0 → x
"""

import logging
from typing import Optional, List, Union

from .base import (
    SimplificationRule,
    is_constant,
    get_constant_value,
    create_constant_value,
    create_intermediate_value,
)
from ..ssa import SSAFunction, SSAInstruction, SSAValue

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


class RuleNotDistribute(SimplificationRule):
    """
    Apply DeMorgan's laws to distribute NOT over AND/OR (bitwise).

    Examples:
        ~(a & b) → ~a | ~b
        ~(a | b) → ~a & ~b

    This uses multi-instruction transformation to create intermediate NOT operations.

    Note: May increase expression complexity in some cases, but can enable
    further optimizations through bit manipulation analysis.
    """

    def __init__(self):
        super().__init__("RuleNotDistribute")
        self.is_disabled = False  # NOW ENABLED with multi-instruction support!

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Must be a NOT operation
        if inst.mnemonic != "BN":  # Bitwise NOT
            return False
        if len(inst.inputs) != 1:
            return False

        # Input must be AND or OR
        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        prod_inst = input_val.producer_inst
        if prod_inst.mnemonic not in ("BA", "BO"):  # Bitwise AND/OR
            return False

        # Must have exactly 2 inputs
        if len(prod_inst.inputs) != 2:
            return False

        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Union[SSAInstruction, List[SSAInstruction], None]:
        """
        Apply DeMorgan's law using multi-instruction transformation.

        Transformation:
        1. Create NOT_A = NOT(a)
        2. Create NOT_B = NOT(b)
        3. Replace NOT(a AND b) with NOT_A OR NOT_B
        """
        inner_inst = inst.inputs[0].producer_inst

        # Get operands
        a = inner_inst.inputs[0]
        b = inner_inst.inputs[1]

        # Determine new operation (flip AND ↔ OR)
        new_op = "BO" if inner_inst.mnemonic == "BA" else "BA"

        # Create intermediate values for ~a and ~b
        not_a_val = create_intermediate_value("not_a", a.value_type, ssa_func)
        not_b_val = create_intermediate_value("not_b", b.value_type, ssa_func)

        # Create intermediate instructions
        not_a_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="BN",  # Bitwise NOT
            address=inst.address - 2,  # Pseudo-address before target
            inputs=[a],
            outputs=[not_a_val],
        )

        not_b_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="BN",  # Bitwise NOT
            address=inst.address - 1,  # Pseudo-address before target
            inputs=[b],
            outputs=[not_b_val],
        )

        # Create replacement instruction: NOT_A op NOT_B
        replacement_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic=new_op,
            address=inst.address,
            inputs=[not_a_val, not_b_val],
            outputs=inst.outputs,
            instruction=inst.instruction,
            metadata=inst.metadata,
        )

        # Return list: [NOT_A, NOT_B, NOT_A op NOT_B]
        return [not_a_inst, not_b_inst, replacement_inst]


class RuleHighOrderAnd(SimplificationRule):
    """
    Optimize byte/word extraction patterns by moving shifts.

    Examples:
        (x & 0xff00) >> 8 → (x >> 8) & 0xff
        (x & 0xffff0000) >> 16 → (x >> 16) & 0xffff

    This makes byte extraction more obvious and enables further optimizations.
    """

    def __init__(self):
        super().__init__("RuleHighOrderAnd")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Must be a right shift
        if inst.mnemonic not in ("RS", "RSA"):  # Right shift (logical or arithmetic)
            return False
        if len(inst.inputs) != 2:
            return False

        # Shift amount must be constant
        shift_amount_val = inst.inputs[1]
        shift_amount = get_constant_value(shift_amount_val, ssa_func)
        if shift_amount is None or shift_amount == 0:
            return False

        # Left operand must be AND with constant mask
        and_val = inst.inputs[0]
        if not and_val.producer_inst:
            return False

        and_inst = and_val.producer_inst
        if and_inst.mnemonic != "BA":
            return False
        if len(and_inst.inputs) != 2:
            return False

        # AND mask must be constant
        mask_val = get_constant_value(and_inst.inputs[1], ssa_func)
        if mask_val is None:
            return False

        # Check if mask has high-order bits set that will be shifted out
        # For example: mask = 0xff00, shift = 8
        # After shift, we'd get: (value & 0xff00) >> 8 = (value >> 8) & 0xff
        shifted_mask = (mask_val >> shift_amount) & 0xFFFFFFFF

        # Only apply if the transformation is beneficial (mask becomes simpler)
        return shifted_mask != 0 and shifted_mask < mask_val

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        shift_amount_val = inst.inputs[1]
        shift_amount = get_constant_value(shift_amount_val, ssa_func)

        and_inst = inst.inputs[0].producer_inst
        original_value = and_inst.inputs[0]
        mask_val = get_constant_value(and_inst.inputs[1], ssa_func)

        if shift_amount is None or mask_val is None:
            return None

        # Calculate new mask after shifting
        new_mask = (mask_val >> shift_amount) & 0xFFFFFFFF

        # Build: (x >> shift) & new_mask
        # This requires creating an intermediate shift operation
        # For simplicity, we'll skip this optimization for now
        # (requires multi-instruction transformation)

        return None


class RuleBitUndistribute(SimplificationRule):
    """
    Factor out common terms in bitwise operations (reverse distribution).

    Examples:
        (x & a) | (x & b) → x & (a | b)
        (x | a) & (x | b) → x | (a & b)

    This is the reverse of distribution and can simplify complex bit manipulation.
    """

    def __init__(self):
        super().__init__("RuleBitUndistribute")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Must be OR or AND
        if inst.mnemonic not in ("BA", "BO"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Both operands must be the complementary operation
        if not left.producer_inst or not right.producer_inst:
            return False

        left_inst = left.producer_inst
        right_inst = right.producer_inst

        # Check for pattern: (x OP1 a) OP2 (x OP1 b)
        # where OP1 and OP2 are complementary (AND/OR or OR/AND)
        target_op = "BA" if inst.mnemonic == "BO" else "BO"

        if left_inst.mnemonic != target_op or right_inst.mnemonic != target_op:
            return False

        if len(left_inst.inputs) != 2 or len(right_inst.inputs) != 2:
            return False

        # Check if they share a common operand
        # Pattern: (x & a) | (x & b)
        left_ops = set([left_inst.inputs[0].name, left_inst.inputs[1].name])
        right_ops = set([right_inst.inputs[0].name, right_inst.inputs[1].name])

        common = left_ops & right_ops
        return len(common) == 1

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left_inst = inst.inputs[0].producer_inst
        right_inst = inst.inputs[1].producer_inst

        # Find the common operand and the unique ones
        left_ops = {left_inst.inputs[0].name: left_inst.inputs[0],
                    left_inst.inputs[1].name: left_inst.inputs[1]}
        right_ops = {right_inst.inputs[0].name: right_inst.inputs[0],
                     right_inst.inputs[1].name: right_inst.inputs[1]}

        common_names = set(left_ops.keys()) & set(right_ops.keys())
        if len(common_names) != 1:
            return None

        common_name = list(common_names)[0]
        common_val = left_ops[common_name]

        # Get the unique operands
        left_unique = [v for k, v in left_ops.items() if k != common_name][0]
        right_unique = [v for k, v in right_ops.items() if k != common_name][0]

        # Build: x & (a | b) or x | (a & b)
        # This requires creating an intermediate operation
        # For simplicity, we'll skip this for now (requires multi-instruction transformation)

        self.apply_count += 1
        logger.debug(f"RuleBitUndistribute: (x{left_inst.mnemonic}a){inst.mnemonic}(x{right_inst.mnemonic}b) → factored")
        return None  # Requires multi-instruction support


class RuleNotDistribute(SimplificationRule):
    """
    Apply DeMorgan's laws to distribute NOT over AND/OR.

    Examples:
        ~(a & b) → ~a | ~b
        ~(a | b) → ~a & ~b

    This is Ghidra's approach to boolean/bitwise simplification.

    Reference: Ghidra ruleaction.cc, similar to DeMorgan transformation
    """

    def __init__(self):
        super().__init__("RuleNotDistribute")
        self.is_disabled = True  # May increase code complexity

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Must be BN (bitwise NOT)
        if inst.mnemonic != "BN":
            return False
        if len(inst.inputs) != 1:
            return False

        # Input must be AND or OR
        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        inner_inst = input_val.producer_inst
        return inner_inst.mnemonic in ("BA", "BO") and len(inner_inst.inputs) == 2

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Get the inner operation: ~(a op b)
        inner_inst = inst.inputs[0].producer_inst
        a, b = inner_inst.inputs

        # Determine the new operation
        # ~(a & b) → ~a | ~b
        # ~(a | b) → ~a & ~b
        new_op = "BO" if inner_inst.mnemonic == "BA" else "BA"

        # This requires creating NOT operations for both operands
        # Requires multi-instruction transformation, which we'll skip for now

        self.apply_count += 1
        logger.debug(f"RuleNotDistribute: ~({inner_inst.mnemonic}) → {new_op} with NOTs")
        return None  # Requires multi-instruction support
