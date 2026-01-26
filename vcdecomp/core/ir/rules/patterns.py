"""
Advanced pattern detection and optimization rules.

This module implements high-level pattern recognition rules inspired by Ghidra's
advanced simplification passes:

Phase 4 rules (10 rules):
- RuleConditionInvert: Invert conditions to reduce negations
- RuleSelectPattern: Detect ternary/select patterns (x ? a : b)
- RuleDemorganLaws: Apply De Morgan's laws to complex conditions
- RuleAbsoluteValue: Detect abs() patterns
- RuleMinMaxPatterns: Detect min/max patterns
- RuleBitfieldExtract: Detect bitfield extraction patterns
- RuleSignMagnitude: Optimize sign-magnitude conversions
- RuleRangeCheck: Optimize range checking patterns
- RuleBoolNormalize: Normalize boolean expressions
- RuleConditionMerge: Merge redundant conditions
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


class RuleConditionInvert(SimplificationRule):
    """
    Invert conditions to reduce double negation.

    Examples:
        !(a < b) → a >= b
        !(a == b) → a != b
        !(a <= b) → a > b

    This applies boolean algebra to simplify negated comparisons.
    """

    def __init__(self):
        super().__init__("RuleConditionInvert")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Look for NOT applied to comparison
        if inst.mnemonic != "NOT":
            return False
        if len(inst.inputs) != 1:
            return False

        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        # Check if input is a comparison operation
        comp_op = input_val.producer_inst.mnemonic
        return comp_op in ("EQU", "NEQ", "LES", "LEQ", "GRE", "GEQ")

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """Invert the comparison instead of negating the result."""
        comp_inst = inst.inputs[0].producer_inst
        comp_op = comp_inst.mnemonic

        # Map to inverted operation
        invert_map = {
            "EQU": "NEQ",  # !(a == b) → a != b
            "NEQ": "EQU",  # !(a != b) → a == b
            "LES": "GEQ",  # !(a < b) → a >= b
            "LEQ": "GRE",  # !(a <= b) → a > b
            "GRE": "LEQ",  # !(a > b) → a <= b
            "GEQ": "LES",  # !(a >= b) → a < b
        }

        inverted_op = invert_map.get(comp_op)
        if not inverted_op:
            return None

        # Create new comparison with inverted operation
        return SSAInstruction(
            id=inst.id,
            mnemonic=inverted_op,
            inputs=comp_inst.inputs,
            output=inst.output,
        )


class RuleDemorganLaws(SimplificationRule):
    """
    Apply De Morgan's laws to simplify boolean expressions.

    Examples:
        !(a && b) → !a || !b
        !(a || b) → !a && !b

    This can expose further optimization opportunities.
    """

    def __init__(self):
        super().__init__("RuleDemorganLaws")
        self.is_disabled = True  # Complex: requires boolean expression tree

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Look for NOT of AND/OR
        if inst.mnemonic != "NOT":
            return False
        if len(inst.inputs) != 1:
            return False

        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        return input_val.producer_inst.mnemonic in ("AND", "OR", "BA", "BO")

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Apply De Morgan's laws.
        Note: This is disabled because it requires creating new NOT instructions
        for each operand, which is complex in SSA form.
        """
        return None


class RuleAbsoluteValue(SimplificationRule):
    """
    Detect absolute value patterns.

    Examples:
        (x < 0) ? -x : x → abs(x)
        (x >= 0) ? x : -x → abs(x)

    This recognizes common abs() implementations.
    """

    def __init__(self):
        super().__init__("RuleAbsoluteValue")
        self.is_disabled = True  # Requires control flow analysis

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # This pattern requires analyzing phi nodes in CFG
        # Pattern: phi(x, -x) where condition is x < 0
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleMinMaxPatterns(SimplificationRule):
    """
    Detect min/max patterns.

    Examples:
        (a < b) ? a : b → min(a, b)
        (a > b) ? a : b → max(a, b)
        (a < b) ? b : a → max(a, b)

    This recognizes common min/max implementations.
    """

    def __init__(self):
        super().__init__("RuleMinMaxPatterns")
        self.is_disabled = True  # Requires control flow analysis

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # This pattern requires analyzing phi nodes in CFG
        # Pattern: phi(a, b) where condition is a < b or a > b
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleBitfieldExtract(SimplificationRule):
    """
    Detect bitfield extraction patterns.

    Examples:
        (x >> shift) & mask → EXTRACT(x, shift, width)
        (x & mask) >> shift → EXTRACT(x, shift, width)

    This recognizes common bitfield access patterns.
    """

    def __init__(self):
        super().__init__("RuleBitfieldExtract")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Pattern 1: (x >> shift) & mask
        if inst.mnemonic == "BA":  # Bitwise AND
            if len(inst.inputs) != 2:
                return False
            left, right = inst.inputs

            # Right must be constant mask
            if not is_constant(right):
                return False

            # Left must be shift
            if left.producer_inst and left.producer_inst.mnemonic in ("SHR", "SHL"):
                shift_inst = left.producer_inst
                if len(shift_inst.inputs) == 2:
                    # Shift amount must be constant
                    if is_constant(shift_inst.inputs[1]):
                        return True

        # Pattern 2: (x & mask) >> shift
        if inst.mnemonic in ("SHR", "SHL"):
            if len(inst.inputs) != 2:
                return False
            left, right = inst.inputs

            # Right must be constant shift
            if not is_constant(right):
                return False

            # Left must be AND with constant mask
            if left.producer_inst and left.producer_inst.mnemonic == "BA":
                and_inst = left.producer_inst
                if len(and_inst.inputs) == 2:
                    if is_constant(and_inst.inputs[1]):
                        return True

        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Simplify bitfield extraction.

        For now, we just recognize the pattern but don't transform it
        because we'd need a BITFIELD_EXTRACT opcode.
        """
        # TODO: Could compute the effective mask and shift
        # and replace with a single AND if the pattern is redundant
        return None


class RuleSignMagnitude(SimplificationRule):
    """
    Optimize sign-magnitude conversions.

    Examples:
        (x < 0) ? -x : x combined with sign extraction
        Detect two's complement sign extraction patterns

    This recognizes sign/magnitude decomposition.
    """

    def __init__(self):
        super().__init__("RuleSignMagnitude")
        self.is_disabled = True  # Requires control flow analysis

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleRangeCheck(SimplificationRule):
    """
    Optimize range checking patterns.

    Examples:
        (x >= a) && (x <= b) → IN_RANGE(x, a, b)
        (x < a) || (x > b) → OUT_RANGE(x, a, b)
        (unsigned)x < n → x in [0, n)

    This recognizes common bounds checking patterns.
    """

    def __init__(self):
        super().__init__("RuleRangeCheck")
        self.is_disabled = True  # Requires boolean expression analysis

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Look for AND/OR of two comparisons
        if inst.mnemonic not in ("AND", "OR"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Both must be comparison operations
        if not (left.producer_inst and right.producer_inst):
            return False

        left_is_comp = left.producer_inst.mnemonic in (
            "LES",
            "LEQ",
            "GRE",
            "GEQ",
            "EQU",
            "NEQ",
        )
        right_is_comp = right.producer_inst.mnemonic in (
            "LES",
            "LEQ",
            "GRE",
            "GEQ",
            "EQU",
            "NEQ",
        )

        return left_is_comp and right_is_comp

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Detect range check patterns.

        For now, we just recognize the pattern but don't simplify it
        because the pattern is already reasonably clear.
        """
        # Could potentially optimize to a single unsigned comparison
        # if we detect (x >= 0) && (x < n) → (unsigned)x < n
        # But this requires type analysis
        return None


class RuleBoolNormalize(SimplificationRule):
    """
    Normalize boolean expressions to canonical form.

    Examples:
        (x != 0) → x (in boolean context)
        (x == 0) → !x (in boolean context)
        (x == 1) → x (if x is boolean)

    This simplifies boolean comparisons.
    """

    def __init__(self):
        super().__init__("RuleBoolNormalize")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Look for comparison with 0 or 1
        if inst.mnemonic not in ("EQU", "NEQ"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # One operand must be constant 0 or 1
        if is_constant(left):
            val = get_constant_value(left, ssa_func)
            return val in (0, 1)
        elif is_constant(right):
            val = get_constant_value(right, ssa_func)
            return val in (0, 1)

        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Simplify boolean comparisons.

        x != 0 → x (assume boolean context)
        x == 0 → !x
        x == 1 → x (if x is boolean)
        """
        left, right = inst.inputs

        # Get the value and non-constant operand
        if is_constant(right):
            const_val = get_constant_value(right, ssa_func)
            var = left
        else:
            const_val = get_constant_value(left, ssa_func)
            var = right

        # x != 0 → x (in boolean context)
        if inst.mnemonic == "NEQ" and const_val == 0:
            return SSAInstruction(
                id=inst.id,
                mnemonic="COPY",
                inputs=[var],
                output=inst.output,
            )

        # x == 0 → !x
        if inst.mnemonic == "EQU" and const_val == 0:
            return SSAInstruction(
                id=inst.id,
                mnemonic="NOT",
                inputs=[var],
                output=inst.output,
            )

        # x == 1 → x (assume x is boolean)
        if inst.mnemonic == "EQU" and const_val == 1:
            # Only safe if we know x is boolean (0 or 1)
            # For now, don't apply this transformation
            return None

        return None


class RuleConditionMerge(SimplificationRule):
    """
    Merge redundant conditions.

    Examples:
        (a < b) && (a < b) → a < b
        (a == b) || (a == b) → a == b

    This eliminates duplicate comparisons in boolean expressions.
    """

    def __init__(self):
        super().__init__("RuleConditionMerge")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Look for AND/OR with duplicate inputs
        if inst.mnemonic not in ("AND", "OR"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Check if both inputs come from the same instruction
        # (same SSA value)
        return left == right

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """Replace (x OP x) with x."""
        # a && a → a
        # a || a → a
        return SSAInstruction(
            id=inst.id,
            mnemonic="COPY",
            inputs=[inst.inputs[0]],
            output=inst.output,
        )


class RuleSelectPattern(SimplificationRule):
    """
    Detect and optimize ternary select patterns.

    Examples:
        cond ? a : a → a
        cond ? true : false → cond
        cond ? false : true → !cond

    This simplifies degenerate select/ternary patterns.
    Note: This operates on phi nodes in the CFG, not SSA instructions directly.
    """

    def __init__(self):
        super().__init__("RuleSelectPattern")
        self.is_disabled = True  # Requires control flow analysis

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # This would operate on phi nodes
        # Pattern: phi(a, a) → a (both branches produce same value)
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None
