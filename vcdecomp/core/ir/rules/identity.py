"""
Algebraic identity simplification rules.

This module implements rules for simplifying operations with identity values:
- RuleTermOrder: Canonical term ordering (3 + x → x + 3)
- RuleAndIdentity: x & -1 → x, x & 0 → 0, x & x → x
- RuleOrIdentity: x | 0 → x, x | -1 → -1, x | x → x
- RuleAddIdentity: x + 0 → x
- RuleMulIdentity: x * 1 → x, x * 0 → 0
"""

import logging
from typing import Optional

from .base import (
    SimplificationRule,
    is_constant,
    get_constant_value,
    create_constant_value,
    is_commutative,
)
from ..ssa import SSAFunction, SSAInstruction

logger = logging.getLogger(__name__)


class RuleTermOrder(SimplificationRule):
    """
    Canonicalize commutative operations for CSE.

    Transform: 3 + x → x + 3
              const + var → var + const

    This enables common subexpression elimination by ensuring
    equivalent expressions have identical form.
    """

    def __init__(self):
        super().__init__("RuleTermOrder")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Must be commutative
        if not is_commutative(inst.mnemonic):
            return False

        # Must have exactly 2 inputs
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Constants should be on the right
        left_is_const = is_constant(left)
        right_is_const = is_constant(right)

        if left_is_const and not right_is_const:
            return True  # Need to swap

        # If both non-constant, order by name for determinism
        if not left_is_const and not right_is_const:
            return left.name > right.name

        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Swap operands
        inst.inputs[0], inst.inputs[1] = inst.inputs[1], inst.inputs[0]

        self.apply_count += 1
        logger.debug(f"RuleTermOrder: Swapped operands of {inst.mnemonic}")
        return inst


class RuleAndIdentity(SimplificationRule):
    """
    Simplify bitwise AND with identity values.

    Examples:
        x & -1 → x   (AND with all 1s)
        x & 0 → 0    (AND with 0)
        x & x → x    (AND with self)
    """

    def __init__(self):
        super().__init__("RuleAndIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BA":  # Bitwise AND
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x & 0 → 0
        right_val = get_constant_value(right, ssa_func)
        if right_val == 0:
            # Replace with constant 0
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
            logger.debug(f"RuleAndIdentity: x & 0 → 0")
            return new_inst

        # Check for x & -1 (0xFFFFFFFF) → x
        if right_val == 0xFFFFFFFF or right_val == -1:
            # Replace with left operand
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleAndIdentity: x & -1 → x")
            return new_inst

        # Check for x & x → x
        if left.name == right.name:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleAndIdentity: x & x → x")
            return new_inst

        return None


class RuleOrIdentity(SimplificationRule):
    """
    Simplify bitwise OR with identity values.

    Examples:
        x | 0 → x    (OR with 0)
        x | -1 → -1  (OR with all 1s)
        x | x → x    (OR with self)
    """

    def __init__(self):
        super().__init__("RuleOrIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BO":  # Bitwise OR
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x | 0 → x
        right_val = get_constant_value(right, ssa_func)
        if right_val == 0:
            # Replace with left operand
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleOrIdentity: x | 0 → x")
            return new_inst

        # Check for x | -1 → -1
        if right_val == 0xFFFFFFFF or right_val == -1:
            # Replace with constant -1
            const_all_ones = create_constant_value(
                0xFFFFFFFF, inst.outputs[0].value_type, ssa_func
            )
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="CONST",
                address=inst.address,
                inputs=[const_all_ones],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleOrIdentity: x | -1 → -1")
            return new_inst

        # Check for x | x → x
        if left.name == right.name:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleOrIdentity: x | x → x")
            return new_inst

        return None


class RuleAddIdentity(SimplificationRule):
    """
    Simplify addition with identity values.

    Examples:
        x + 0 → x
        0 + x → x
    """

    def __init__(self):
        super().__init__("RuleAddIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("ADD", "FADD", "DADD"):
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x + 0 → x
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
            logger.debug(f"RuleAddIdentity: x + 0 → x")
            return new_inst

        # Check for 0 + x → x (after term ordering, this shouldn't happen, but be safe)
        left_val = get_constant_value(left, ssa_func)
        if left_val == 0:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[right],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleAddIdentity: 0 + x → x")
            return new_inst

        return None


class RuleMulIdentity(SimplificationRule):
    """
    Simplify multiplication with identity values.

    Examples:
        x * 1 → x
        x * 0 → 0
    """

    def __init__(self):
        super().__init__("RuleMulIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("MUL", "FMUL", "DMUL"):
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x * 1 → x
        right_val = get_constant_value(right, ssa_func)
        if right_val == 1:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleMulIdentity: x * 1 → x")
            return new_inst

        # Check for x * 0 → 0
        if right_val == 0:
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
            logger.debug(f"RuleMulIdentity: x * 0 → 0")
            return new_inst

        return None
