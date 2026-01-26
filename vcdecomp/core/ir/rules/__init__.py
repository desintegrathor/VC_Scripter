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

Rule count target: 40-50 rules (current: 50, Ghidra has: 136)
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
    RuleAndWithOr,
    RuleOrWithAnd,
    RuleAndZero,
    RuleOrAllOnes,
    RuleNotDistribute,
    RuleHighOrderAnd,
    RuleBitUndistribute,
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
    RuleMulZero,
    RuleModOne,
    RuleMulDistribute,
    RuleCollectTerms,
)
from .comparison import (
    RuleEqualitySelf,
    RuleLessEqualSelf,
    RuleCompareConstants,
    RuleNotEqual,
    RuleCompareZero,
    RuleLessEqual,
    RuleIntLessEqual,
    RuleBxor2NotEqual,
)
from .boolean import (
    RuleBooleanAnd,
    RuleBooleanOr,
    RuleBooleanNot,
    RuleBooleanDedup,
)
from .advanced_arithmetic import (
    RuleCancelAddSub,
    RuleAbsorbNegation,
    RuleStrengthReduction,
)
from .typeconv import (
    RuleCastChain,
    RuleCastIdentity,
    RuleCastConstant,
    RuleSextChain,
    RuleTruncateZext,
    RuleBoolZext,
    RuleZextEliminate,
    RulePromoteTypes,
    RuleCastPropagation,
    RuleIntegralPromotion,
    RuleFloatIntRoundtrip,
    RuleConstantCast,
    RuleSignExtendDetect,
    RuleNarrowingRedundant,
    RuleTypeCoercion,
)
from .pointer import (
    RulePtrAddChain,
    RulePtrSubNormalize,
    RulePtrArithIdentity,
    RulePtrNullCheck,
    RulePtrCompare,
    RulePtrDiff,
    RuleArrayBase,
    RuleStructOffset,
    RuleArrayBounds,
    RulePtrIndex,
)
from .patterns import (
    RuleConditionInvert,
    RuleDemorganLaws,
    RuleAbsoluteValue,
    RuleMinMaxPatterns,
    RuleBitfieldExtract,
    RuleSignMagnitude,
    RuleRangeCheck,
    RuleBoolNormalize,
    RuleConditionMerge,
    RuleSelectPattern,
)
from .loops import (
    RuleLoopIncrementSimplify,
    RuleLoopCounterNormalize,
    RuleLoopBoundConstant,
    RuleInductionSimplify,
    RuleLoopInvariantDetect,
    RuleLoopStrength,
    RuleLoopUnswitch,
    RuleCountedLoop,
    RuleLoopElimination,
    RuleLoopRotate,
    RuleLoopFusion,
)
from .dataflow import (
    RuleCopyPropagation,
    RuleConstantPropagation,
    RuleDeadValue,
    RuleIdentityCopy,
    RulePhiSimplify,
    RuleSingleUseInline,
    RuleRedundantCopy,
    RuleCopyChain,
    RuleValueNumbering,
    RuleUnusedResult,
    RuleTrivialPhi,
    RuleForwardSubstitution,
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
    RuleAndWithOr(),
    RuleOrWithAnd(),
    RuleAndZero(),
    RuleOrAllOnes(),
    RuleNotDistribute(),
    RuleHighOrderAnd(),
    RuleBitUndistribute(),

    # Phase 6: Arithmetic chaining and optimization
    RuleDoubleAdd(),
    RuleDoubleSub(),
    RuleNegateIdentity(),
    RuleMulByPowerOf2(),
    RuleDivByPowerOf2(),
    RuleModByPowerOf2(),
    RuleMulZero(),
    RuleModOne(),
    RuleMulDistribute(),
    RuleCollectTerms(),

    # Phase 7: Comparison simplification
    RuleEqualitySelf(),
    RuleLessEqualSelf(),
    RuleNotEqual(),
    RuleCompareZero(),
    RuleLessEqual(),
    RuleIntLessEqual(),
    RuleBxor2NotEqual(),

    # Phase 8: Boolean logic
    RuleBooleanAnd(),
    RuleBooleanOr(),
    RuleBooleanNot(),
    RuleBooleanDedup(),

    # Phase 9: Advanced arithmetic
    RuleCancelAddSub(),
    RuleAbsorbNegation(),
    RuleStrengthReduction(),

    # Phase 10: Type conversions
    RuleCastChain(),
    RuleCastIdentity(),
    RuleCastConstant(),
    RuleSextChain(),
    RuleTruncateZext(),
    RuleBoolZext(),
    RuleZextEliminate(),
    RulePromoteTypes(),
    RuleCastPropagation(),
    RuleIntegralPromotion(),
    RuleFloatIntRoundtrip(),
    RuleConstantCast(),
    RuleSignExtendDetect(),
    RuleNarrowingRedundant(),
    RuleTypeCoercion(),

    # Phase 11: Pointer & Array rules (Phase 3)
    RulePtrAddChain(),
    RulePtrSubNormalize(),
    RulePtrArithIdentity(),
    RulePtrNullCheck(),
    RulePtrCompare(),
    RulePtrDiff(),
    RuleArrayBase(),
    RuleStructOffset(),
    RuleArrayBounds(),
    RulePtrIndex(),

    # Phase 12: Advanced patterns (Phase 4)
    RuleConditionInvert(),
    RuleDemorganLaws(),
    RuleAbsoluteValue(),
    RuleMinMaxPatterns(),
    RuleBitfieldExtract(),
    RuleSignMagnitude(),
    RuleRangeCheck(),
    RuleBoolNormalize(),
    RuleConditionMerge(),
    RuleSelectPattern(),

    # Phase 13: Loop optimization (Phase 5)
    RuleLoopIncrementSimplify(),
    RuleLoopCounterNormalize(),
    RuleLoopBoundConstant(),
    RuleInductionSimplify(),
    RuleLoopInvariantDetect(),
    RuleLoopStrength(),
    RuleLoopUnswitch(),
    RuleCountedLoop(),
    RuleLoopElimination(),
    RuleLoopRotate(),
    RuleLoopFusion(),

    # Phase 14: Data flow & copy propagation (Phase 6)
    RuleCopyPropagation(),
    RuleConstantPropagation(),
    RuleDeadValue(),
    RuleIdentityCopy(),
    RulePhiSimplify(),
    RuleSingleUseInline(),
    RuleRedundantCopy(),
    RuleCopyChain(),
    RuleValueNumbering(),
    RuleUnusedResult(),
    RuleTrivialPhi(),
    RuleForwardSubstitution(),
]

# Rule groups for selective application
RULE_GROUPS = {
    "canonical": [RuleTermOrder],
    "fold": [RuleConstantFold, RuleCompareConstants, RuleCastConstant],
    "identity": [RuleAndIdentity, RuleOrIdentity, RuleAddIdentity, RuleMulIdentity, RuleSubIdentity, RuleDivIdentity],
    "bitwise": [RuleAndMask, RuleOrMask, RuleXorCancel, RuleShiftByZero, RuleDoubleShift, RuleAndWithOr, RuleOrWithAnd, RuleAndZero, RuleOrAllOnes, RuleNotDistribute, RuleHighOrderAnd, RuleBitUndistribute],
    "arithmetic": [RuleDoubleAdd, RuleDoubleSub, RuleNegateIdentity, RuleMulByPowerOf2, RuleDivByPowerOf2, RuleModByPowerOf2, RuleMulZero, RuleModOne, RuleCancelAddSub, RuleAbsorbNegation, RuleStrengthReduction, RuleMulDistribute, RuleCollectTerms],
    "comparison": [RuleEqualitySelf, RuleLessEqualSelf, RuleNotEqual, RuleCompareZero, RuleLessEqual, RuleIntLessEqual, RuleBxor2NotEqual],
    "boolean": [RuleBooleanAnd, RuleBooleanOr, RuleBooleanNot, RuleBooleanDedup],
    "typeconv": [RuleCastChain, RuleCastIdentity, RuleCastConstant, RuleSextChain, RuleTruncateZext, RuleBoolZext, RuleZextEliminate, RulePromoteTypes, RuleCastPropagation, RuleIntegralPromotion, RuleFloatIntRoundtrip, RuleConstantCast, RuleSignExtendDetect, RuleNarrowingRedundant, RuleTypeCoercion],
    "pointer": [RulePtrAddChain, RulePtrSubNormalize, RulePtrArithIdentity, RulePtrNullCheck, RulePtrCompare, RulePtrDiff, RuleArrayBase, RuleStructOffset, RuleArrayBounds, RulePtrIndex],
    "patterns": [RuleConditionInvert, RuleDemorganLaws, RuleAbsoluteValue, RuleMinMaxPatterns, RuleBitfieldExtract, RuleSignMagnitude, RuleRangeCheck, RuleBoolNormalize, RuleConditionMerge, RuleSelectPattern],
    "loops": [RuleLoopIncrementSimplify, RuleLoopCounterNormalize, RuleLoopBoundConstant, RuleInductionSimplify, RuleLoopInvariantDetect, RuleLoopStrength, RuleLoopUnswitch, RuleCountedLoop, RuleLoopElimination, RuleLoopRotate, RuleLoopFusion],
    "dataflow": [RuleCopyPropagation, RuleConstantPropagation, RuleDeadValue, RuleIdentityCopy, RulePhiSimplify, RuleSingleUseInline, RuleRedundantCopy, RuleCopyChain, RuleValueNumbering, RuleUnusedResult, RuleTrivialPhi, RuleForwardSubstitution],
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
    "RuleAndWithOr",
    "RuleOrWithAnd",
    "RuleAndZero",
    "RuleOrAllOnes",
    "RuleNotDistribute",
    "RuleHighOrderAnd",
    "RuleBitUndistribute",

    # Arithmetic rules
    "RuleDoubleAdd",
    "RuleDoubleSub",
    "RuleNegateIdentity",
    "RuleMulByPowerOf2",
    "RuleDivByPowerOf2",
    "RuleModByPowerOf2",
    "RuleMulZero",
    "RuleModOne",
    "RuleMulDistribute",
    "RuleCollectTerms",

    # Comparison rules
    "RuleEqualitySelf",
    "RuleLessEqualSelf",
    "RuleNotEqual",
    "RuleCompareZero",
    "RuleLessEqual",
    "RuleIntLessEqual",
    "RuleBxor2NotEqual",

    # Boolean rules
    "RuleBooleanAnd",
    "RuleBooleanOr",
    "RuleBooleanNot",
    "RuleBooleanDedup",

    # Advanced arithmetic rules
    "RuleCancelAddSub",
    "RuleAbsorbNegation",
    "RuleStrengthReduction",

    # Type conversion rules
    "RuleCastChain",
    "RuleCastIdentity",
    "RuleCastConstant",
    "RuleSextChain",
    "RuleTruncateZext",
    "RuleBoolZext",
    "RuleZextEliminate",
    "RulePromoteTypes",
    "RuleCastPropagation",
    "RuleIntegralPromotion",
    "RuleFloatIntRoundtrip",
    "RuleConstantCast",
    "RuleSignExtendDetect",
    "RuleNarrowingRedundant",
    "RuleTypeCoercion",

    # Pointer & Array rules
    "RulePtrAddChain",
    "RulePtrSubNormalize",
    "RulePtrArithIdentity",
    "RulePtrNullCheck",
    "RulePtrCompare",
    "RulePtrDiff",
    "RuleArrayBase",
    "RuleStructOffset",
    "RuleArrayBounds",
    "RulePtrIndex",

    # Advanced pattern rules
    "RuleConditionInvert",
    "RuleDemorganLaws",
    "RuleAbsoluteValue",
    "RuleMinMaxPatterns",
    "RuleBitfieldExtract",
    "RuleSignMagnitude",
    "RuleRangeCheck",
    "RuleBoolNormalize",
    "RuleConditionMerge",
    "RuleSelectPattern",

    # Loop optimization rules
    "RuleLoopIncrementSimplify",
    "RuleLoopCounterNormalize",
    "RuleLoopBoundConstant",
    "RuleInductionSimplify",
    "RuleLoopInvariantDetect",
    "RuleLoopStrength",
    "RuleLoopUnswitch",
    "RuleCountedLoop",
    "RuleLoopElimination",
    "RuleLoopRotate",
    "RuleLoopFusion",

    # Data flow optimization rules
    "RuleCopyPropagation",
    "RuleConstantPropagation",
    "RuleDeadValue",
    "RuleIdentityCopy",
    "RulePhiSimplify",
    "RuleSingleUseInline",
    "RuleRedundantCopy",
    "RuleCopyChain",
    "RuleValueNumbering",
    "RuleUnusedResult",
    "RuleTrivialPhi",
    "RuleForwardSubstitution",

    # Registry
    "ALL_RULES",
    "RULE_GROUPS",
]
