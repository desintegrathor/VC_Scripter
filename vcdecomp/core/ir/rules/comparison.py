"""
Comparison operation simplification rules.

This module implements rules for simplifying comparison operations:
- RuleEqualitySelf: x == x → true, x != x → false
- RuleLessEqualSimplify: x <= x → true, x < x → false
- RuleCompareConstants: Fold constant comparisons
- RuleLessGreaterContradict: x < y && x > y → false (contradictions)
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


class RuleEqualitySelf(SimplificationRule):
    """
    Simplify comparisons of value with itself.

    Examples:
        x == x → true (1)
        x != x → false (0)
    """

    def __init__(self):
        super().__init__("RuleEqualitySelf")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("EQU", "NEQ", "FEQU", "FNEQ", "DEQU", "DNEQ"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs
        return left.name == right.name

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # x == x → 1, x != x → 0
        result = 1 if inst.mnemonic in ("EQU", "FEQU", "DEQU") else 0

        const_result = create_constant_value(
            result, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="CONST",
            address=inst.address,
            inputs=[const_result],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleEqualitySelf: {inst.mnemonic}(x, x) → {result}")
        return new_inst


class RuleLessEqualSelf(SimplificationRule):
    """
    Simplify less-than/greater-than comparisons of value with itself.

    Examples:
        x <= x → true (1)
        x >= x → true (1)
        x < x → false (0)
        x > x → false (0)
    """

    def __init__(self):
        super().__init__("RuleLessEqualSelf")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in (
            "LES",
            "LEQ",
            "GRE",
            "GEQ",
            "FLES",
            "FLEQ",
            "FGRE",
            "FGEQ",
            "DLES",
            "DLEQ",
            "DGRE",
            "DGEQ",
        ):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs
        return left.name == right.name

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # x <= x → 1, x >= x → 1
        # x < x → 0, x > x → 0
        result = 1 if "EQ" in inst.mnemonic else 0

        const_result = create_constant_value(
            result, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="CONST",
            address=inst.address,
            inputs=[const_result],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleLessEqualSelf: {inst.mnemonic}(x, x) → {result}")
        return new_inst


class RuleCompareConstants(SimplificationRule):
    """
    Fold comparisons of two constants.

    Examples:
        5 == 5 → true
        3 < 10 → true
        7 > 20 → false
    """

    def __init__(self):
        super().__init__("RuleCompareConstants")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check if it's a comparison
        if inst.mnemonic not in (
            "EQU",
            "NEQ",
            "LES",
            "LEQ",
            "GRE",
            "GEQ",
            "FEQU",
            "FNEQ",
            "FLES",
            "FLEQ",
            "FGRE",
            "FGEQ",
            "DEQU",
            "DNEQ",
            "DLES",
            "DLEQ",
            "DGRE",
            "DGEQ",
        ):
            return False

        if len(inst.inputs) != 2:
            return False

        # Both inputs must be constants
        return all(is_constant(inp) for inp in inst.inputs)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        left_val = get_constant_value(left, ssa_func)
        right_val = get_constant_value(right, ssa_func)

        if left_val is None or right_val is None:
            return None

        # Evaluate comparison
        result = self._evaluate_comparison(inst.mnemonic, left_val, right_val)
        if result is None:
            return None

        const_result = create_constant_value(
            result, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="CONST",
            address=inst.address,
            inputs=[const_result],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(
            f"RuleCompareConstants: {left_val} {inst.mnemonic} {right_val} → {result}"
        )
        return new_inst

    def _evaluate_comparison(self, mnemonic: str, left: int, right: int) -> Optional[int]:
        """Evaluate comparison and return 1 (true) or 0 (false)."""
        # Integer comparisons
        if mnemonic == "EQU":
            return 1 if left == right else 0
        elif mnemonic == "NEQ":
            return 1 if left != right else 0
        elif mnemonic == "LES":
            return 1 if left < right else 0
        elif mnemonic == "LEQ":
            return 1 if left <= right else 0
        elif mnemonic == "GRE":
            return 1 if left > right else 0
        elif mnemonic == "GEQ":
            return 1 if left >= right else 0

        # Float/double comparisons (treat as integers for now)
        # TODO: Proper float comparison handling
        elif mnemonic in ("FEQU", "DEQU"):
            return 1 if left == right else 0
        elif mnemonic in ("FNEQ", "DNEQ"):
            return 1 if left != right else 0
        elif mnemonic in ("FLES", "DLES"):
            return 1 if left < right else 0
        elif mnemonic in ("FLEQ", "DLEQ"):
            return 1 if left <= right else 0
        elif mnemonic in ("FGRE", "DGRE"):
            return 1 if left > right else 0
        elif mnemonic in ("FGEQ", "DGEQ"):
            return 1 if left >= right else 0

        return None
