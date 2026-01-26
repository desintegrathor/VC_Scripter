"""
Boolean logic simplification rules.

This module implements rules for simplifying boolean operations:
- RuleBooleanAnd: x && true → x, x && false → false
- RuleBooleanOr: x || true → true, x || false → x
- RuleBooleanNot: !(!x) → x
- RuleBooleanDedup: x && x → x, x || x → x
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


class RuleBooleanAnd(SimplificationRule):
    """
    Simplify logical AND with constants.

    Examples:
        x && true → x
        x && false → false
        x && 1 → x
        x && 0 → 0
    """

    def __init__(self):
        super().__init__("RuleBooleanAnd")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Logical AND can be represented as bitwise AND in some contexts
        # or as explicit boolean AND
        if inst.mnemonic not in ("BA", "AND", "LAND"):
            return False
        if len(inst.inputs) != 2:
            return False

        # One operand must be constant
        left, right = inst.inputs
        return is_constant(left) or is_constant(right)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Ensure constant is on the right (after term ordering, should already be)
        const_val = get_constant_value(right, ssa_func)
        non_const = left

        if const_val is None:
            # Constant might be on left
            const_val = get_constant_value(left, ssa_func)
            non_const = right

        if const_val is None:
            return None

        # x && 0 → 0
        if const_val == 0:
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
            logger.debug(f"RuleBooleanAnd: x && 0 → 0")
            return new_inst

        # x && 1 → x (for boolean context)
        # x && -1 → x (for bitwise AND with all bits set)
        if const_val == 1 or const_val == 0xFFFFFFFF or const_val == -1:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[non_const],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleBooleanAnd: x && {const_val} → x")
            return new_inst

        return None


class RuleBooleanOr(SimplificationRule):
    """
    Simplify logical OR with constants.

    Examples:
        x || false → x
        x || true → true
        x || 0 → x
        x || 1 → 1 (in boolean context)
    """

    def __init__(self):
        super().__init__("RuleBooleanOr")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("BO", "OR", "LOR"):
            return False
        if len(inst.inputs) != 2:
            return False

        # One operand must be constant
        left, right = inst.inputs
        return is_constant(left) or is_constant(right)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Ensure constant is on the right
        const_val = get_constant_value(right, ssa_func)
        non_const = left

        if const_val is None:
            const_val = get_constant_value(left, ssa_func)
            non_const = right

        if const_val is None:
            return None

        # x || 0 → x
        if const_val == 0:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[non_const],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleBooleanOr: x || 0 → x")
            return new_inst

        # x || 1 → 1 (boolean), x || -1 → -1 (bitwise)
        if const_val == 1:
            const_one = create_constant_value(1, inst.outputs[0].value_type, ssa_func)
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="CONST",
                address=inst.address,
                inputs=[const_one],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleBooleanOr: x || 1 → 1")
            return new_inst

        if const_val == 0xFFFFFFFF or const_val == -1:
            const_all = create_constant_value(
                0xFFFFFFFF, inst.outputs[0].value_type, ssa_func
            )
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="CONST",
                address=inst.address,
                inputs=[const_all],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleBooleanOr: x || -1 → -1")
            return new_inst

        return None


class RuleBooleanNot(SimplificationRule):
    """
    Simplify double negation.

    Examples:
        !(!x) → x
        ~(~x) → x (bitwise NOT)
    """

    def __init__(self):
        super().__init__("RuleBooleanNot")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("BN", "NOT", "LNOT"):  # Bitwise/Logical NOT
            return False
        if len(inst.inputs) != 1:
            return False

        # Input must be result of another NOT
        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        return input_val.producer_inst.mnemonic in ("BN", "NOT", "LNOT")

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        inner_not = inst.inputs[0].producer_inst

        # Get the original value (before double negation)
        original = inner_not.inputs[0]

        # Create copy instruction
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="COPY",
            address=inst.address,
            inputs=[original],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleBooleanNot: !(!x) → x")
        return new_inst


class RuleBooleanDedup(SimplificationRule):
    """
    Remove duplicate boolean operations.

    Examples:
        x && x → x
        x || x → x
    """

    def __init__(self):
        super().__init__("RuleBooleanDedup")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("BA", "BO", "AND", "OR", "LAND", "LOR"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs
        return left.name == right.name

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # x op x → x (for idempotent operations)
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
        logger.debug(f"RuleBooleanDedup: x {inst.mnemonic} x → x")
        return new_inst
