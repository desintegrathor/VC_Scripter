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


class RuleLessEqual(SimplificationRule):
    """
    Simplify redundant comparison combinations.

    Examples:
        x <= y && x >= y → x == y
        x < y || x > y || x == y → true (always)
    """

    def __init__(self):
        super().__init__("RuleLessEqual")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Look for logical AND of two comparisons
        if inst.mnemonic not in ("BA", "LAND"):  # Bitwise AND or logical AND
            return False
        if len(inst.inputs) != 2:
            return False

        # Both inputs must be comparisons
        left, right = inst.inputs
        if not left.producer_inst or not right.producer_inst:
            return False

        left_cmp = left.producer_inst
        right_cmp = right.producer_inst

        # Check if both are comparisons
        if not self._is_comparison(left_cmp.mnemonic):
            return False
        if not self._is_comparison(right_cmp.mnemonic):
            return False

        # Check if they compare the same operands
        if len(left_cmp.inputs) != 2 or len(right_cmp.inputs) != 2:
            return False

        # Same operands (a <= b && a >= b)
        if (left_cmp.inputs[0].name == right_cmp.inputs[0].name and
            left_cmp.inputs[1].name == right_cmp.inputs[1].name):
            # Check for x <= y && x >= y pattern
            if self._is_less_equal(left_cmp.mnemonic) and self._is_greater_equal(right_cmp.mnemonic):
                return True
            if self._is_greater_equal(left_cmp.mnemonic) and self._is_less_equal(right_cmp.mnemonic):
                return True

        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left_cmp = inst.inputs[0].producer_inst
        right_cmp = inst.inputs[1].producer_inst

        # x <= y && x >= y → x == y
        # Convert to equality check
        eq_op = self._get_equality_op(left_cmp.mnemonic)
        if eq_op is None:
            return None

        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic=eq_op,
            address=inst.address,
            inputs=left_cmp.inputs,  # Use operands from first comparison
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleLessEqual: x<=y && x>=y → x==y")
        return new_inst

    def _is_comparison(self, mnemonic: str) -> bool:
        return mnemonic in (
            "EQU", "NEQ", "LES", "LEQ", "GRE", "GEQ",
            "FEQU", "FNEQ", "FLES", "FLEQ", "FGRE", "FGEQ",
            "DEQU", "DNEQ", "DLES", "DLEQ", "DGRE", "DGEQ",
        )

    def _is_less_equal(self, mnemonic: str) -> bool:
        return mnemonic in ("LEQ", "FLEQ", "DLEQ")

    def _is_greater_equal(self, mnemonic: str) -> bool:
        return mnemonic in ("GEQ", "FGEQ", "DGEQ")

    def _get_equality_op(self, mnemonic: str) -> Optional[str]:
        """Get corresponding equality operator for comparison type."""
        if mnemonic in ("LEQ", "GEQ", "LES", "GRE"):
            return "EQU"
        elif mnemonic in ("FLEQ", "FGEQ", "FLES", "FGRE"):
            return "FEQU"
        elif mnemonic in ("DLEQ", "DGEQ", "DLES", "DGRE"):
            return "DEQU"
        return None


class RuleIntLessEqual(SimplificationRule):
    """
    Normalize comparison operators to reduce operator diversity.

    Examples:
        x <= y → !(x > y)
        x >= y → !(x < y)

    Note: Disabled by default as it may make code less readable.
    """

    def __init__(self):
        super().__init__("RuleIntLessEqual")
        self.is_disabled = True  # Disabled - may reduce readability

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Match <= or >= comparisons
        return inst.mnemonic in ("LEQ", "GEQ", "FLEQ", "FGEQ", "DLEQ", "DGEQ")

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Convert x <= y to !(x > y)
        # Convert x >= y to !(x < y)

        negated_op = self._get_negated_strict_op(inst.mnemonic)
        if negated_op is None:
            return None

        # Create the strict comparison
        strict_cmp = SSAInstruction(
            block_id=inst.block_id,
            mnemonic=negated_op,
            address=inst.address,
            inputs=inst.inputs,
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        # Would need to wrap in NOT - but this complicates the IR
        # For now, return None (disabled by default anyway)
        return None

    def _get_negated_strict_op(self, mnemonic: str) -> Optional[str]:
        """Get the strict comparison that, when negated, equals the input."""
        negation_map = {
            "LEQ": "GRE",  # x <= y = !(x > y)
            "GEQ": "LES",  # x >= y = !(x < y)
            "FLEQ": "FGRE",
            "FGEQ": "FLES",
            "DLEQ": "DGRE",
            "DGEQ": "DLES",
        }
        return negation_map.get(mnemonic)


class RuleBxor2NotEqual(SimplificationRule):
    """
    Detect XOR-based inequality pattern.

    Examples:
        (a ^ b) != 0 → a != b
        (a ^ b) == 0 → a == b

    This pattern is common in compiled code for inequality checks.
    """

    def __init__(self):
        super().__init__("RuleBxor2NotEqual")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Must be comparison with zero
        if inst.mnemonic not in ("EQU", "NEQ"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # One operand must be zero
        left_val = get_constant_value(left, ssa_func)
        right_val = get_constant_value(right, ssa_func)

        if left_val != 0 and right_val != 0:
            return False

        # The other operand must be result of XOR
        xor_val = right if left_val == 0 else left
        if not xor_val.producer_inst:
            return False

        return xor_val.producer_inst.mnemonic == "BX"  # Bitwise XOR

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Get the XOR instruction
        left_val = get_constant_value(left, ssa_func)
        xor_val = right if left_val == 0 else left

        xor_inst = xor_val.producer_inst
        if len(xor_inst.inputs) != 2:
            return None

        # (a ^ b) != 0 → a != b
        # (a ^ b) == 0 → a == b
        new_op = inst.mnemonic  # Keep the same comparison operator

        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic=new_op,
            address=inst.address,
            inputs=xor_inst.inputs,  # Use XOR operands directly
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleBxor2NotEqual: (a^b){inst.mnemonic}0 → a{inst.mnemonic}b")
        return new_inst
