"""
Pointer arithmetic simplification rules.

This module implements rules for simplifying pointer arithmetic patterns:
- RulePointerAdd: (ptr + a) + b → ptr + (a + b)
- RulePointerOffsetFold: Fold constant offsets in pointer arithmetic
- RuleIndexScale: Optimize array index scaling

Phase 3 additions (10 new rules):
- RulePtrIndex: Convert pointer arithmetic to array indexing
- RuleArrayBase: Simplify array base address (&arr[0] → arr)
- RulePtrAddChain: Properly chain pointer additions
- RulePtrSubNormalize: Normalize pointer subtraction (ptr - (-4) → ptr + 4)
- RuleStructOffset: Detect struct field access patterns
- RuleArrayBounds: Array index constant folding
- RulePtrCompare: Pointer comparison normalization
- RulePtrDiff: Detect element count from pointer difference
- RulePtrNullCheck: Optimize null pointer checks
- RulePtrArithIdentity: Pointer arithmetic identity (ptr + 0 → ptr)
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


class RulePointerAdd(SimplificationRule):
    """
    Combine consecutive pointer additions.

    Examples:
        (ptr + 4) + 8 → ptr + 12
        (ptr + offset1) + offset2 → ptr + (offset1 + offset2)

    This is the same as RuleDoubleAdd but specifically for pointer context.
    """

    def __init__(self):
        super().__init__("RulePointerAdd")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # This is essentially the same as RuleDoubleAdd
        # but we keep it separate for clarity in pointer arithmetic context
        if inst.mnemonic != "ADD":
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant (offset)
        if not is_constant(right):
            return False

        # Left must be result of another ADD
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic != "ADD":
            return False
        if len(left.producer_inst.inputs) != 2:
            return False

        # Inner ADD's right operand must be constant
        inner_right = left.producer_inst.inputs[1]
        return is_constant(inner_right)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # This is handled by RuleDoubleAdd, but we keep this rule
        # for semantic clarity in logs
        return None  # Let RuleDoubleAdd handle it


class RuleIndexOptimize(SimplificationRule):
    """
    Optimize array indexing patterns.

    Examples:
        (i * 4) + (base + offset) → base + (i * 4 + offset)
        base + (i * elem_size) → optimize when elem_size is power of 2
    """

    def __init__(self):
        super().__init__("RuleIndexOptimize")
        self.is_disabled = True  # Complex rule, disabled by default

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # This is a complex pattern that requires sophisticated matching
        # Disabled for now
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleOffsetCanonical(SimplificationRule):
    """
    Canonicalize struct/array offset expressions.

    Examples:
        ptr + (offset + field) → ptr + (field + offset)
        Ensure offsets are in canonical order for CSE
    """

    def __init__(self):
        super().__init__("RuleOffsetCanonical")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "ADD":
            return False
        if len(inst.inputs) != 2:
            return False

        # This is really a specialization of term ordering
        # We rely on RuleTermOrder to handle this
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None  # Handled by RuleTermOrder


# ============================================================================
# Phase 3: Pointer & Array Rules (10 new rules)
# ============================================================================


class RulePtrAddChain(SimplificationRule):
    """
    Properly implement pointer addition chaining.

    Examples:
        (ptr + 4) + 8 → ptr + 12
        (ptr + offset1) + offset2 → ptr + (offset1 + offset2)

    This replaces the stub RulePointerAdd with a real implementation.
    """

    def __init__(self):
        super().__init__("RulePtrAddChain")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "ADD":
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant (offset)
        if not is_constant(right):
            return False

        # Left must be result of another ADD
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic != "ADD":
            return False
        if len(left.producer_inst.inputs) != 2:
            return False

        # Inner ADD's right operand must be constant
        inner_right = left.producer_inst.inputs[1]
        return is_constant(inner_right)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """Combine the two constant offsets."""
        left, right = inst.inputs
        inner_left = left.producer_inst.inputs[0]
        inner_right = left.producer_inst.inputs[1]

        # Get constant values
        offset1 = get_constant_value(inner_right, ssa_func)
        offset2 = get_constant_value(right, ssa_func)

        # Create new combined offset
        combined_offset = offset1 + offset2
        new_const = create_constant_value(combined_offset, ssa_func)

        # Create new ADD: base + combined_offset
        return SSAInstruction(
            id=inst.id,
            mnemonic="ADD",
            inputs=[inner_left, new_const],
            output=inst.output,
        )


class RulePtrSubNormalize(SimplificationRule):
    """
    Normalize pointer subtraction with negative constants.

    Examples:
        ptr - (-4) → ptr + 4
        ptr - (-offset) → ptr + offset

    This converts subtraction of negative values to addition.
    """

    def __init__(self):
        super().__init__("RulePtrSubNormalize")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "SUB":
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant
        if not is_constant(right):
            return False

        # Check if constant is negative
        val = get_constant_value(right, ssa_func)
        return val < 0

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """Convert ptr - (-X) to ptr + X."""
        left, right = inst.inputs
        val = get_constant_value(right, ssa_func)

        # Create positive constant
        new_const = create_constant_value(-val, ssa_func)

        # Create ADD instead of SUB
        return SSAInstruction(
            id=inst.id,
            mnemonic="ADD",
            inputs=[left, new_const],
            output=inst.output,
        )


class RulePtrArithIdentity(SimplificationRule):
    """
    Eliminate identity operations in pointer arithmetic.

    Examples:
        ptr + 0 → ptr
        ptr - 0 → ptr

    This is similar to RuleAddIdentity but specifically for pointers.
    """

    def __init__(self):
        super().__init__("RulePtrArithIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("ADD", "SUB"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant zero
        if not is_constant(right):
            return False

        val = get_constant_value(right, ssa_func)
        return val == 0

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """Return just the pointer (left operand)."""
        left, right = inst.inputs

        # Create COPY instruction
        return SSAInstruction(
            id=inst.id,
            mnemonic="COPY",
            inputs=[left],
            output=inst.output,
        )


class RulePtrNullCheck(SimplificationRule):
    """
    Optimize null pointer checks.

    Examples:
        ptr == 0 → !ptr
        ptr != 0 → ptr (in boolean context)
        0 == ptr → !ptr

    This converts explicit null checks to implicit boolean conversion.
    """

    def __init__(self):
        super().__init__("RulePtrNullCheck")
        self.is_disabled = True  # Conservative: disabled until we have type info

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("EQU", "NEQ"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # One operand must be constant zero
        left_is_zero = is_constant(left) and get_constant_value(left, ssa_func) == 0
        right_is_zero = is_constant(right) and get_constant_value(right, ssa_func) == 0

        return left_is_zero or right_is_zero

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Convert to boolean operation.
        Note: This is disabled by default because we need type information
        to know if this is actually a pointer check or just integer comparison.
        """
        return None


class RulePtrCompare(SimplificationRule):
    """
    Normalize pointer comparisons.

    Examples:
        (ptr + 4) < (ptr + 8) → 4 < 8 (if same base pointer)
        ptr1 - ptr2 < 0 → ptr1 < ptr2

    This detects when comparing pointers with known base and offsets.
    """

    def __init__(self):
        super().__init__("RulePtrCompare")
        self.is_disabled = True  # Complex analysis required

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("LES", "LEQ", "GRE", "GEQ", "EQU", "NEQ"):
            return False
        if len(inst.inputs) != 2:
            return False

        # Would need to track base pointers and offsets
        # This requires more sophisticated alias analysis
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RulePtrDiff(SimplificationRule):
    """
    Detect element count from pointer difference.

    Examples:
        (ptr1 - ptr2) / 4 → element_count (for 4-byte elements)
        (ptr1 - ptr2) >> 2 → element_count (shift by 2 = divide by 4)

    This recognizes the pattern of computing array element count from pointer difference.
    """

    def __init__(self):
        super().__init__("RulePtrDiff")
        self.is_disabled = True  # Requires type information

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check for division or right shift after SUB
        if inst.mnemonic not in ("DIV", "SHR"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant (element size)
        if not is_constant(right):
            return False

        # Left must be SUB (pointer difference)
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic != "SUB":
            return False

        # This pattern is valid, but we need type info to confirm it's pointers
        return False  # Disabled until we have pointer type tracking

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleArrayBase(SimplificationRule):
    """
    Simplify array base address patterns.

    Examples:
        &arr[0] → arr
        &(*ptr) → ptr

    This eliminates redundant address-of and dereference operations.
    """

    def __init__(self):
        super().__init__("RuleArrayBase")
        self.is_disabled = True  # Need address-of and deref opcodes

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # This requires ADDR and DEREF opcodes which may not exist in our IR
        # Pattern: ADDR(DEREF(x)) → x or ADDR(INDEX(arr, 0)) → arr
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleStructOffset(SimplificationRule):
    """
    Detect and optimize struct field access patterns.

    Examples:
        ptr + 12 → ptr->field3 (if we know offset 12 is field3)
        (ptr + 8) + 4 → ptr + 12 (combine struct offsets)

    This recognizes common struct field offset patterns.
    """

    def __init__(self):
        super().__init__("RuleStructOffset")
        self.is_disabled = True  # Requires struct type information

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "ADD":
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Look for ADD with constant offset
        if not is_constant(right):
            return False

        offset = get_constant_value(right, ssa_func)

        # Common struct field offsets (heuristic)
        # Typical: 0, 4, 8, 12, 16, 20, 24, 28, 32...
        # This is just a heuristic; real implementation needs type info
        common_offsets = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48]

        # For now, disabled until we have proper struct type tracking
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleArrayBounds(SimplificationRule):
    """
    Optimize array index bounds checking and constant folding.

    Examples:
        arr[3] when arr size is known
        Fold: base + (i * 4) when i is constant

    This performs constant folding for array indexing.
    """

    def __init__(self):
        super().__init__("RuleArrayBounds")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Pattern: base + (index * elem_size)
        if inst.mnemonic != "ADD":
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right could be MUL (index * elem_size)
        if right.producer_inst and right.producer_inst.mnemonic == "MUL":
            mul_inst = right.producer_inst
            if len(mul_inst.inputs) == 2:
                mul_left, mul_right = mul_inst.inputs
                # Both must be constants to fold
                if is_constant(mul_left) and is_constant(mul_right):
                    return True

        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """Fold constant array index calculation."""
        left, right = inst.inputs
        mul_inst = right.producer_inst
        mul_left, mul_right = mul_inst.inputs

        # Calculate index * elem_size
        index = get_constant_value(mul_left, ssa_func)
        elem_size = get_constant_value(mul_right, ssa_func)
        offset = index * elem_size

        # Create new constant
        new_const = create_constant_value(offset, ssa_func)

        # Return base + folded_offset
        return SSAInstruction(
            id=inst.id,
            mnemonic="ADD",
            inputs=[left, new_const],
            output=inst.output,
        )


class RulePtrIndex(SimplificationRule):
    """
    Convert pointer arithmetic to array indexing notation.

    Examples:
        *(ptr + 4) → ptr[1] (for 4-byte elements)
        *(ptr + (i * 4)) → ptr[i] (for 4-byte elements)

    This is primarily a presentation rule to make output more readable.
    Note: This operates at the expression level, not SSA IR level.
    """

    def __init__(self):
        super().__init__("RulePtrIndex")
        self.is_disabled = True  # Presentation-only rule, handled by code emitter

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # This is better handled at the code emission stage
        # where we have full expression context
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None
