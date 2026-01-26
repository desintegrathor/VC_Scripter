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


class RuleNotEqual(SimplificationRule):
    """
    Simplify negated equality comparisons.

    Examples:
        !(x == y) → x != y
        !(x != y) → x == y
        !(x < y) → x >= y
    """

    def __init__(self):
        super().__init__("RuleNotEqual")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check if this is a logical NOT
        if inst.mnemonic not in ("BN", "NOT", "LNOT"):
            return False
        if len(inst.inputs) != 1:
            return False

        # Input must be result of a comparison
        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        return input_val.producer_inst.mnemonic in (
            "EQU", "NEQ", "LES", "LEQ", "GRE", "GEQ",
            "FEQU", "FNEQ", "FLES", "FLEQ", "FGRE", "FGEQ",
            "DEQU", "DNEQ", "DLES", "DLEQ", "DGRE", "DGEQ",
        )

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        compare_inst = inst.inputs[0].producer_inst

        # Get negated comparison
        negated_op = self._negate_comparison(compare_inst.mnemonic)
        if negated_op is None:
            return None

        # Create new comparison with negated operator
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic=negated_op,
            address=inst.address,
            inputs=compare_inst.inputs,
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleNotEqual: !({compare_inst.mnemonic}) → {negated_op}")
        return new_inst

    def _negate_comparison(self, op: str) -> Optional[str]:
        """Return the negated comparison operator."""
        negation_map = {
            # Integer comparisons
            "EQU": "NEQ",
            "NEQ": "EQU",
            "LES": "GEQ",
            "LEQ": "GRE",
            "GRE": "LEQ",
            "GEQ": "LES",
            # Float comparisons
            "FEQU": "FNEQ",
            "FNEQ": "FEQU",
            "FLES": "FGEQ",
            "FLEQ": "FGRE",
            "FGRE": "FLEQ",
            "FGEQ": "FLES",
            # Double comparisons
            "DEQU": "DNEQ",
            "DNEQ": "DEQU",
            "DLES": "DGEQ",
            "DLEQ": "DGRE",
            "DGRE": "DLEQ",
            "DGEQ": "DLES",
        }
        return negation_map.get(op)


class RuleCompareZero(SimplificationRule):
    """
    Simplify comparisons with zero.

    Examples:
        x == 0 → !x (in boolean context)
        x != 0 → x (in boolean context)

    Note: Disabled by default as this is context-dependent.
    """

    def __init__(self):
        super().__init__("RuleCompareZero")
        self.is_disabled = True  # Context-dependent optimization

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("EQU", "NEQ"):
            return False
        if len(inst.inputs) != 2:
            return False

        # One operand must be zero
        left, right = inst.inputs
        left_val = get_constant_value(left, ssa_func)
        right_val = get_constant_value(right, ssa_func)

        return left_val == 0 or right_val == 0

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Determine which is the value and which is zero
        left_val = get_constant_value(left, ssa_func)
        value = right if left_val == 0 else left

        # x != 0 → x (in boolean context)
        if inst.mnemonic == "NEQ":
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[value],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleCompareZero: x != 0 → x")
            return new_inst

        # x == 0 → !x (in boolean context)
        if inst.mnemonic == "EQU":
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="LNOT",
                address=inst.address,
                inputs=[value],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleCompareZero: x == 0 → !x")
            return new_inst

        return None
