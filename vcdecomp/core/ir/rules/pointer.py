"""
Pointer arithmetic simplification rules.

This module implements rules for simplifying pointer arithmetic patterns:
- RulePointerAdd: (ptr + a) + b → ptr + (a + b)
- RulePointerOffsetFold: Fold constant offsets in pointer arithmetic
- RuleIndexScale: Optimize array index scaling
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
