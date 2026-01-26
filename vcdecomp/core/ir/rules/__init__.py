"""
Transformation rules package for SSA-level simplification.

This package implements Ghidra-inspired transformation rules organized by category:
- base: Base classes and utilities (SimplificationRule, helpers)
- identity: Algebraic identity rules (x + 0 → x, x * 1 → x, etc.)
- bitwise: Bitwise operation simplification
- arithmetic: Arithmetic simplification and folding
- comparison: Comparison operation simplification
- boolean: Boolean logic simplification
- typeconv: Type conversion simplification
- pointer: Pointer arithmetic simplification

Rule count target: 40-50 rules (current: 8, Ghidra has: 136)
"""

from .base import SimplificationRule, is_constant, get_constant_value, create_constant_value, is_commutative
from .identity import (
    RuleTermOrder,
    RuleAndIdentity,
    RuleOrIdentity,
    RuleAddIdentity,
    RuleMulIdentity,
)
from .bitwise import (
    RuleAndMask,
    RuleOrMask,
    RuleXorCancel,
    RuleShiftByZero,
    RuleDoubleShift,
)
from .arithmetic import (
    RuleConstantFold,
    RuleDoubleAdd,
    RuleDoubleSub,
    RuleNegateIdentity,
    RuleSubIdentity,
    RuleDivIdentity,
    RuleMulByPowerOf2,
    RuleDivByPowerOf2,
    RuleModByPowerOf2,
)
from .comparison import (
    RuleEqualitySelf,
    RuleLessEqualSelf,
    RuleCompareConstants,
)
from .boolean import (
    RuleBooleanAnd,
    RuleBooleanOr,
    RuleBooleanNot,
    RuleBooleanDedup,
)

# Registry of all available rules
ALL_RULES = [
    # Phase 1: Term ordering (canonical form for CSE)
    RuleTermOrder(),

    # Phase 2: Constant folding
    RuleConstantFold(),
    RuleCompareConstants(),

    # Phase 3: Identity rules
    RuleAndIdentity(),
    RuleOrIdentity(),
    RuleAddIdentity(),
    RuleMulIdentity(),
    RuleSubIdentity(),
    RuleDivIdentity(),

    # Phase 4: Nested operation simplification
    RuleAndMask(),
    RuleOrMask(),

    # Phase 5: XOR and shift simplification
    RuleXorCancel(),
    RuleShiftByZero(),
    RuleDoubleShift(),

    # Phase 6: Arithmetic chaining and optimization
    RuleDoubleAdd(),
    RuleDoubleSub(),
    RuleNegateIdentity(),
    RuleMulByPowerOf2(),
    RuleDivByPowerOf2(),
    RuleModByPowerOf2(),

    # Phase 7: Comparison simplification
    RuleEqualitySelf(),
    RuleLessEqualSelf(),

    # Phase 8: Boolean logic
    RuleBooleanAnd(),
    RuleBooleanOr(),
    RuleBooleanNot(),
    RuleBooleanDedup(),
]

# Rule groups for selective application
RULE_GROUPS = {
    "canonical": [RuleTermOrder],
    "fold": [RuleConstantFold, RuleCompareConstants],
    "identity": [RuleAndIdentity, RuleOrIdentity, RuleAddIdentity, RuleMulIdentity, RuleSubIdentity, RuleDivIdentity],
    "bitwise": [RuleAndMask, RuleOrMask, RuleXorCancel, RuleShiftByZero, RuleDoubleShift],
    "arithmetic": [RuleDoubleAdd, RuleDoubleSub, RuleNegateIdentity, RuleMulByPowerOf2, RuleDivByPowerOf2, RuleModByPowerOf2],
    "comparison": [RuleEqualitySelf, RuleLessEqualSelf],
    "boolean": [RuleBooleanAnd, RuleBooleanOr, RuleBooleanNot, RuleBooleanDedup],
}

__all__ = [
    # Base classes
    "SimplificationRule",
    "is_constant",
    "get_constant_value",
    "create_constant_value",
    "is_commutative",

    # Identity rules
    "RuleTermOrder",
    "RuleAndIdentity",
    "RuleOrIdentity",
    "RuleAddIdentity",
    "RuleMulIdentity",
    "RuleSubIdentity",
    "RuleDivIdentity",

    # Folding rules
    "RuleConstantFold",
    "RuleCompareConstants",

    # Bitwise rules
    "RuleAndMask",
    "RuleOrMask",
    "RuleXorCancel",
    "RuleShiftByZero",
    "RuleDoubleShift",

    # Arithmetic rules
    "RuleDoubleAdd",
    "RuleDoubleSub",
    "RuleNegateIdentity",
    "RuleMulByPowerOf2",
    "RuleDivByPowerOf2",
    "RuleModByPowerOf2",

    # Comparison rules
    "RuleEqualitySelf",
    "RuleLessEqualSelf",

    # Boolean rules
    "RuleBooleanAnd",
    "RuleBooleanOr",
    "RuleBooleanNot",
    "RuleBooleanDedup",

    # Registry
    "ALL_RULES",
    "RULE_GROUPS",
]
