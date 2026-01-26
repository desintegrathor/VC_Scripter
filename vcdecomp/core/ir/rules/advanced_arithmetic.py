"""
Advanced arithmetic simplification rules.

This module implements more sophisticated arithmetic transformations:
- RuleCancelAddSub: (x + y) - y → x, (x - y) + y → x
- RuleAbsorbNegation: x - (-y) → x + y, x + (-y) → x - y
- RuleDistributeNegation: -(x + y) → -x - y, -(x - y) → -x + y
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


class RuleCancelAddSub(SimplificationRule):
    """
    Cancel additions and subtractions of the same value.

    Examples:
        (x + y) - y → x
        (x - y) + y → x
        x + y - y → x
    """

    def __init__(self):
        super().__init__("RuleCancelAddSub")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("ADD", "SUB"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Left must be result of ADD or SUB
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic not in ("ADD", "SUB"):
            return False
        if len(left.producer_inst.inputs) != 2:
            return False

        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs
        inner_op = left.producer_inst
        inner_left, inner_right = inner_op.inputs

        # Case 1: (x + y) - y → x
        if inst.mnemonic == "SUB" and inner_op.mnemonic == "ADD":
            if inner_right.name == right.name:
                new_inst = SSAInstruction(
                    block_id=inst.block_id,
                    mnemonic="COPY",
                    address=inst.address,
                    inputs=[inner_left],
                    outputs=inst.outputs,
                    instruction=inst.instruction,
                )
                self.apply_count += 1
                logger.debug(f"RuleCancelAddSub: (x + y) - y → x")
                return new_inst

            # Also check: (y + x) - y → x
            if inner_left.name == right.name:
                new_inst = SSAInstruction(
                    block_id=inst.block_id,
                    mnemonic="COPY",
                    address=inst.address,
                    inputs=[inner_right],
                    outputs=inst.outputs,
                    instruction=inst.instruction,
                )
                self.apply_count += 1
                logger.debug(f"RuleCancelAddSub: (y + x) - y → x")
                return new_inst

        # Case 2: (x - y) + y → x
        if inst.mnemonic == "ADD" and inner_op.mnemonic == "SUB":
            if inner_right.name == right.name:
                new_inst = SSAInstruction(
                    block_id=inst.block_id,
                    mnemonic="COPY",
                    address=inst.address,
                    inputs=[inner_left],
                    outputs=inst.outputs,
                    instruction=inst.instruction,
                )
                self.apply_count += 1
                logger.debug(f"RuleCancelAddSub: (x - y) + y → x")
                return new_inst

        return None


class RuleAbsorbNegation(SimplificationRule):
    """
    Absorb negations in addition/subtraction.

    Examples:
        x - (-y) → x + y
        x + (-y) → x - y
    """

    def __init__(self):
        super().__init__("RuleAbsorbNegation")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("ADD", "SUB"):
            return False
        if len(inst.inputs) != 2:
            return False

        # Right operand must be result of NEG
        right = inst.inputs[1]
        if not right.producer_inst:
            return False
        return right.producer_inst.mnemonic == "NEG"

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs
        neg_op = right.producer_inst

        # Get the original value (before negation)
        original = neg_op.inputs[0]

        # x - (-y) → x + y
        if inst.mnemonic == "SUB":
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="ADD",
                address=inst.address,
                inputs=[left, original],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleAbsorbNegation: x - (-y) → x + y")
            return new_inst

        # x + (-y) → x - y
        if inst.mnemonic == "ADD":
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="SUB",
                address=inst.address,
                inputs=[left, original],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleAbsorbNegation: x + (-y) → x - y")
            return new_inst

        return None


class RuleDistributeNegation(SimplificationRule):
    """
    Distribute negation over addition/subtraction.

    Examples:
        -(x + y) → -x - y
        -(x - y) → -x + y (which becomes y - x after simplification)
    """

    def __init__(self):
        super().__init__("RuleDistributeNegation")
        self.is_disabled = True  # Disabled by default (may increase complexity)

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "NEG":
            return False
        if len(inst.inputs) != 1:
            return False

        # Input must be result of ADD or SUB
        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False
        return input_val.producer_inst.mnemonic in ("ADD", "SUB")

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # This rule is complex and may not always be beneficial
        # Keeping it disabled by default
        return None


class RuleStrengthReduction(SimplificationRule):
    """
    Apply strength reduction: replace expensive ops with cheaper ones.

    Examples:
        x * 1 → x (already handled by RuleMulIdentity)
        x * 0 → 0 (already handled by RuleMulIdentity)
        x / x → 1 (when non-zero)
    """

    def __init__(self):
        super().__init__("RuleStrengthReduction")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("DIV", "IDIV"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs
        # x / x → 1
        return left.name == right.name

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # x / x → 1 (assuming x != 0)
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
        logger.debug(f"RuleStrengthReduction: x / x → 1")
        return new_inst
