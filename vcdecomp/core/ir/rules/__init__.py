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
)
from .arithmetic import (
    RuleConstantFold,
    RuleDoubleAdd,
    RuleDoubleSub,
    RuleNegateIdentity,
)

# Registry of all available rules
ALL_RULES = [
    # Phase 1: Term ordering (canonical form for CSE)
    RuleTermOrder(),

    # Phase 2: Constant folding
    RuleConstantFold(),

    # Phase 3: Identity rules
    RuleAndIdentity(),
    RuleOrIdentity(),
    RuleAddIdentity(),
    RuleMulIdentity(),

    # Phase 4: Nested operation simplification
    RuleAndMask(),
    RuleOrMask(),

    # Phase 5: XOR simplification
    RuleXorCancel(),

    # Phase 6: Arithmetic chaining
    RuleDoubleAdd(),
    RuleDoubleSub(),
    RuleNegateIdentity(),
]

# Rule groups for selective application
RULE_GROUPS = {
    "canonical": [RuleTermOrder],
    "fold": [RuleConstantFold],
    "identity": [RuleAndIdentity, RuleOrIdentity, RuleAddIdentity, RuleMulIdentity],
    "bitwise": [RuleAndMask, RuleOrMask, RuleXorCancel],
    "arithmetic": [RuleDoubleAdd, RuleDoubleSub, RuleNegateIdentity],
}

__all__ = [
    # Base classes
    "SimplificationRule",
    "is_constant",
    "get_constant_value",
    "create_constant_value",
    "is_commutative",

    # Rules
    "RuleTermOrder",
    "RuleConstantFold",
    "RuleAndIdentity",
    "RuleOrIdentity",
    "RuleAddIdentity",
    "RuleMulIdentity",
    "RuleAndMask",
    "RuleOrMask",
    "RuleXorCancel",
    "RuleDoubleAdd",
    "RuleDoubleSub",
    "RuleNegateIdentity",

    # Registry
    "ALL_RULES",
    "RULE_GROUPS",
]
