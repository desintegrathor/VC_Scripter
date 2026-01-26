"""
Expression simplification engine for SSA-level optimizations.

This module re-exports the new modular simplification system for
backward compatibility. The actual implementation is now split across:

- rules/ package: Individual simplification rules
- simplify_engine.py: Fixed-point transformation engine

This module provides:
- SimplificationRule base class
- All individual rules
- SimplificationEngine class
- simplify_expressions() function (backward compatible API)
"""

# Re-export everything from the new modular structure
from .rules import (
    # Base classes and utilities
    SimplificationRule,
    is_constant,
    get_constant_value,
    create_constant_value,
    is_commutative,
    # All rules
    RuleTermOrder,
    RuleConstantFold,
    RuleCompareConstants,
    RuleAndIdentity,
    RuleOrIdentity,
    RuleAddIdentity,
    RuleMulIdentity,
    RuleSubIdentity,
    RuleDivIdentity,
    RuleAndMask,
    RuleOrMask,
    RuleXorCancel,
    RuleShiftByZero,
    RuleDoubleShift,
    RuleDoubleAdd,
    RuleDoubleSub,
    RuleNegateIdentity,
    RuleMulByPowerOf2,
    RuleDivByPowerOf2,
    RuleModByPowerOf2,
    RuleEqualitySelf,
    RuleLessEqualSelf,
    RuleBooleanAnd,
    RuleBooleanOr,
    RuleBooleanNot,
    RuleBooleanDedup,
    # Registry
    ALL_RULES,
    RULE_GROUPS,
)

from .simplify_engine import (
    SimplificationEngine,
    SimplificationStats,
    simplify_expressions,
)

# For backward compatibility, also export DEFAULT_RULES
DEFAULT_RULES = ALL_RULES

__all__ = [
    # Base classes
    "SimplificationRule",
    "is_constant",
    "get_constant_value",
    "create_constant_value",
    "is_commutative",
    # Engine
    "SimplificationEngine",
    "SimplificationStats",
    "simplify_expressions",
    # Rules
    "RuleTermOrder",
    "RuleConstantFold",
    "RuleCompareConstants",
    "RuleAndIdentity",
    "RuleOrIdentity",
    "RuleAddIdentity",
    "RuleMulIdentity",
    "RuleSubIdentity",
    "RuleDivIdentity",
    "RuleAndMask",
    "RuleOrMask",
    "RuleXorCancel",
    "RuleShiftByZero",
    "RuleDoubleShift",
    "RuleDoubleAdd",
    "RuleDoubleSub",
    "RuleNegateIdentity",
    "RuleMulByPowerOf2",
    "RuleDivByPowerOf2",
    "RuleModByPowerOf2",
    "RuleEqualitySelf",
    "RuleLessEqualSelf",
    "RuleBooleanAnd",
    "RuleBooleanOr",
    "RuleBooleanNot",
    "RuleBooleanDedup",
    # Registry
    "ALL_RULES",
    "DEFAULT_RULES",
    "RULE_GROUPS",
]
