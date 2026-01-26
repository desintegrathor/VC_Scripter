# Remaining Ghidra Rules - Implementation Roadmap

**Current Status**: 40/136 rules implemented (~30% coverage)
**Remaining**: 96 rules from Ghidra's transformation engine
**Last Updated**: 2026-01-26

---

## Overview

Ghidra implements 136+ transformation rules organized into thematic "ActionPool" groups. We've implemented 40 foundational rules. This document categorizes the remaining 96 rules by priority and complexity.

---

## Priority 1: High-Impact Rules (20 rules)

These rules have the biggest impact on decompilation quality and are relatively straightforward to implement.

### Arithmetic Simplification (8 rules)

| Rule | Transformation | Complexity | Impact |
|------|----------------|------------|--------|
| **RuleCollectTerms** | `a + b + c → canonical form` | Medium | High - enables CSE |
| **RuleMulDistribute** | `x*a + x*b → x*(a+b)` | Medium | High - factoring |
| **RuleFactorConstant** | Extract common factors | Medium | High |
| **RuleSubToAdd** | `x - (-y) → x + y` | Low | Medium - already partially implemented |
| **RuleDivOptimize** | Optimize signed division | Medium | Medium |
| **RuleRemainderOptimize** | Optimize remainder operations | Medium | Medium |
| **RuleNegateDistribute** | `-(x + y) → -x - y` | Low | Low - disabled by default |
| **RuleDivChain** | Simplify nested divisions | Medium | Medium |

**Already Implemented**: RuleDoubleAdd, RuleDoubleSub, RuleNegateIdentity, RuleMulByPowerOf2, RuleDivByPowerOf2, RuleModByPowerOf2

### Bitwise Operations (6 rules)

| Rule | Transformation | Complexity | Impact |
|------|----------------|------------|--------|
| **RuleBitUndistribute** | `(x&a)\|(x&b) → x&(a\|b)` | Medium | High - bit manipulation |
| **RuleHighOrderAnd** | `(x&0xff00)>>8 → (x>>8)&0xff` | Medium | High - byte extraction |
| **RuleShiftBitops** | Simplify shift + bitwise combos | High | High - optimization |
| **RuleNotDistribute** | `~(a&b) → ~a\|~b` (DeMorgan) | Low | Medium |
| **RuleAndDistribute** | `(a\|b)&c → (a&c)\|(b&c)` | Medium | Medium |
| **RuleOrCollapse** | Remove redundant ORs | Low | Medium |

**Already Implemented**: RuleAndMask, RuleOrMask, RuleXorCancel, RuleShiftByZero, RuleDoubleShift

### Comparison & Boolean (6 rules)

| Rule | Transformation | Complexity | Impact |
|------|----------------|------------|--------|
| **RuleLessEqual** | `x<=y && x>=y → x==y` | Low | High - condition simplification |
| **RuleIntLessEqual** | `x<=y → !(x>y)` | Low | Medium |
| **RuleBxor2NotEqual** | `(a^b)!=0 → a!=b` | Low | High - XOR pattern recognition |
| **RuleCompareRange** | Optimize chained comparisons | Medium | High - range checks |
| **RuleBooleanUndistribute** | `(a&&b)\|\|(a&&c) → a&&(b\|c)` | Medium | High - factoring |
| **RuleLogic2Bool** | Convert bitwise to boolean | Medium | Medium |

**Already Implemented**: RuleEqualitySelf, RuleLessEqualSelf, RuleNotEqual, RuleCompareZero, RuleBooleanAnd, RuleBooleanOr, RuleBooleanNot, RuleBooleanDedup

---

## Priority 2: Medium-Impact Rules (30 rules)

### Sign/Zero Extension Detection (8 rules)

Critical for detecting type conversions and casts properly.

| Rule | Transformation | Complexity | Impact |
|------|----------------|------------|--------|
| **RulePiece2Zext** | `PIECE(0,x) → ZEXT(x)` | Medium | High - type recovery |
| **RulePiece2Sext** | Detect sign extension via PIECE | High | High - signed types |
| **RuleZextEliminate** | Remove unnecessary zero extensions | Medium | High - cleanup |
| **RuleSextChain** | Collapse sign extension chains | Low | Medium |
| **RuleTruncateZext** | `trunc(zext(x)) → x` | Low | Medium |
| **RuleBoolZext** | Boolean to int conversions | Medium | Medium |
| **RulePromoteTypes** | Apply C integer promotion | High | High - type correctness |
| **RuleCastPropagation** | Propagate casts through expressions | High | Medium |

**Already Implemented**: RuleCastChain, RuleCastIdentity, RuleCastConstant

### Pointer Arithmetic (7 rules)

Important for array indexing and struct field access.

| Rule | Transformation | Complexity | Impact |
|------|----------------|------------|--------|
| **RulePointerSub** | Simplify pointer differences | Medium | High - pointer math |
| **RuleArrayIndex** | Optimize array indexing | High | High - arrays |
| **RuleAddressSimplify** | Simplify complex addresses | High | High |
| **RuleOffsetCanonical** | Canonicalize struct offsets | Medium | High - structs |
| **RuleLoadStore** | Optimize load/store chains | High | Medium |
| **RuleSegmentOp** | Handle segmented addressing | High | Low - x86 specific |
| **RulePtrArith** | General pointer arithmetic | Medium | Medium |

**Already Implemented**: RulePointerAdd (disabled), RuleIndexOptimize (disabled)

### Subvariable Flow (5 rules)

Advanced bit-field and partial register detection.

| Rule | Transformation | Complexity | Impact |
|------|----------------|------------|--------|
| **RuleSubvarAnd** | Detect bit extraction patterns | High | High - bitfields |
| **RuleSubvarShift** | Logical shifts of extracted bits | High | High |
| **RuleSplitFlow** | Split data flow for partial values | Very High | High |
| **RulePieceUnion** | Detect union patterns | Very High | Medium |
| **RulePullsubMulti** | Pull SUBPIECE through phi nodes | High | Medium |

### Control Flow Simplification (5 rules)

| Rule | Transformation | Complexity | Impact |
|------|----------------|------------|--------|
| **RuleIndirectCollapse** | Collapse indirect operations | High | High - indirect calls |
| **RuleSwitchSingle** | Optimize single-case switches | Low | Low |
| **RuleConditionalMove** | Detect conditional moves | Medium | Medium - ternary |
| **RuleBranchReduce** | Simplify branch conditions | Medium | Medium |
| **RuleCollapseConstant** | Fold constants in branches | Low | Low |

### Value Set Analysis (5 rules)

Range tracking and value propagation.

| Rule | Transformation | Complexity | Impact |
|------|----------------|------------|--------|
| **RuleRangeMeld** | Merge value ranges | High | High - bounds checking |
| **RuleFloatRange** | Track float precision | High | Medium |
| **RuleValueTrack** | Propagate known values | Medium | High |
| **RuleMultiCollapse** | Simplify phi nodes | High | Medium |
| **RuleConstTrackBack** | Back-propagate constants | Medium | Medium |

---

## Priority 3: Low-Priority / Specialized Rules (46 rules)

These are either highly specialized, architecture-specific, or provide marginal benefits.

### Floating-Point Operations (10 rules)

| Category | Count | Examples |
|----------|-------|----------|
| Float comparisons | 3 | RuleFloatCast, RuleFloatRange, RuleNan2Undef |
| Float arithmetic | 4 | RuleFloatAdd, RuleFloatMul, RuleFloatNeg |
| Float conversions | 3 | RuleFloat2Float, RuleInt2Float, RuleFloat2Int |

### Architecture-Specific (12 rules)

| Category | Count | Examples |
|----------|-------|----------|
| x86 segment ops | 3 | RuleSegment, RuleSegmentOp |
| Carry/borrow flags | 4 | RuleCarryElim, RuleBorrowSub |
| Special registers | 5 | RulePcodeOp, RuleHumptyDumpty |

### Advanced Dead Code (8 rules)

| Rule | Purpose |
|------|---------|
| RuleEarlyRemoval | Remove dead ops early |
| RuleDeadCode | Standard DCE |
| RuleUnreachable | Remove unreachable code |
| RuleSideEffect | Preserve side effects |
| RuleVolatile | Handle volatile accesses |
| RulePureFunction | Mark pure functions |
| RuleLoadCollapse | Collapse redundant loads |
| RuleStoreCollapse | Collapse redundant stores |

### Esoteric Patterns (16 rules)

Rare patterns that might not apply to VC-Script bytecode:

- RuleThreeWayCompare - Detect <=> operator
- RuleRotate - Detect rotate operations
- RuleBitReverse - Detect bit reversal
- RulePopCount - Detect population count
- RuleLeadingZeros - Detect clz/ctz
- RuleSaturation - Detect saturating arithmetic
- RuleAbsValue - Detect absolute value
- RuleMinMax - Detect min/max operations
- RuleSignum - Detect sign function
- RuleSwapBytes - Detect byte swapping
- RuleCopyProp - Copy propagation
- RuleConstProp - Constant propagation
- RuleRedundant - Remove redundant ops
- RuleIdentity - Identity detection
- RuleSymmetric - Symmetric operations
- RuleTransitive - Transitive relations

---

## Recommended Next Steps

### Phase 1.5: Quick Wins (10-15 rules, 1-2 weeks)

Add highest-impact rules with low implementation complexity:

1. **RuleCollectTerms** - Reorganize addition trees (enables better CSE)
2. **RuleMulDistribute** - Factor common terms: `x*a + x*b → x*(a+b)`
3. **RuleBitUndistribute** - Bitwise factoring: `(x&a)|(x&b) → x&(a|b)`
4. **RuleLessEqual** - Condition simplification: `x<=y && x>=y → x==y`
5. **RuleBxor2NotEqual** - XOR pattern: `(a^b)!=0 → a!=b`
6. **RuleNotDistribute** - DeMorgan's laws: `~(a&b) → ~a|~b`
7. **RuleHighOrderAnd** - Byte extraction: `(x&0xff00)>>8 → (x>>8)&0xff`
8. **RuleIntLessEqual** - Comparison: `x<=y → !(x>y)`
9. **RuleSextChain** - Collapse sign extensions
10. **RuleTruncateZext** - Eliminate redundant casts: `trunc(zext(x)) → x`

**Expected improvement**: 15-20% better simplification, especially for bit manipulation

### Phase 2: Type & Extension Rules (8-10 rules, 2-3 weeks)

Focus on sign/zero extension detection for better type recovery:

1. RulePiece2Zext
2. RulePiece2Sext
3. RuleZextEliminate
4. RuleBoolZext
5. RulePromoteTypes
6. RuleCastPropagation
7. RuleSextEliminate
8. RuleSignExtend

**Expected improvement**: 20-30% better type inference

### Phase 3: Pointer & Array Rules (7 rules, 2-3 weeks)

Improve array indexing and struct field detection:

1. RulePointerSub
2. RuleArrayIndex
3. RuleAddressSimplify
4. RuleOffsetCanonical
5. RuleLoadStore
6. Enable RulePointerAdd (currently disabled)
7. Enable RuleIndexOptimize (currently disabled)

**Expected improvement**: Much better array/struct detection

### Phase 4: Advanced Patterns (10-15 rules, 3-4 weeks)

Subvariable flow, value sets, advanced comparisons:

1. RuleSubvarAnd
2. RuleSubvarShift
3. RuleCompareRange
4. RuleBooleanUndistribute
5. RuleValueTrack
6. RuleMultiCollapse
7. RuleIndirectCollapse
8. RuleConditionalMove
9. RuleBranchReduce
10. RuleShiftBitops

**Expected improvement**: Handle complex bit manipulation, ranges, ternary operators

---

## Rule Dependency Graph

Some rules depend on others being implemented first:

```
RuleTermOrder (canonical form)
    ↓
RuleConstantFold
    ↓
RuleCollectTerms ← Enables CSE
    ↓
RuleMulDistribute, RuleBitUndistribute ← Factoring
    ↓
RuleZextEliminate, RuleSextChain ← Type cleanup
    ↓
RulePromoteTypes ← Type recovery
    ↓
RulePointerSub, RuleArrayIndex ← Pointer math
    ↓
RuleSubvarAnd, RuleSubvarShift ← Bitfield detection
```

---

## Implementation Complexity Estimates

| Complexity | Count | Time per Rule | Examples |
|------------|-------|---------------|----------|
| Low | 20 | 1-2 hours | RuleNotDistribute, RuleSextChain |
| Medium | 40 | 4-8 hours | RuleCollectTerms, RuleBitUndistribute |
| High | 25 | 1-2 days | RuleSubvarAnd, RuleArrayIndex |
| Very High | 11 | 3-5 days | RuleSplitFlow, RulePromoteTypes |

**Total estimated effort**: 8-12 weeks for all 96 remaining rules

---

## Comparison: VC-Script vs Ghidra

| Category | VC-Script (40) | Ghidra (136) | Coverage |
|----------|----------------|--------------|----------|
| **Canonical** | 1 | 3 | 33% |
| **Folding** | 3 | 8 | 38% |
| **Identity** | 6 | 12 | 50% |
| **Bitwise** | 9 | 18 | 50% |
| **Arithmetic** | 11 | 25 | 44% |
| **Comparison** | 5 | 12 | 42% |
| **Boolean** | 4 | 10 | 40% |
| **Type/Cast** | 3 | 15 | 20% ⚠️ |
| **Pointer** | 0 | 12 | 0% ⚠️ |
| **Subvariable** | 0 | 8 | 0% ⚠️ |
| **Control Flow** | 0 | 5 | 0% ⚠️ |
| **Value Sets** | 0 | 5 | 0% ⚠️ |
| **Float** | 0 | 10 | 0% |
| **Arch-specific** | 0 | 12 | 0% |

**Key gaps**: Type/cast rules, pointer arithmetic, subvariable flow

---

## Recommended Prioritization

For maximum decompilation quality improvement with minimal effort:

### Immediate (Next Sprint)
- ✅ **40 rules complete** (Phase 1 foundation)
- 🎯 **10 Quick Win rules** (Phase 1.5) - 1-2 weeks

### Short Term (1-2 months)
- 🎯 **Type & Extension rules** (Phase 2) - 2-3 weeks
- 🎯 **Pointer & Array rules** (Phase 3) - 2-3 weeks

### Medium Term (3-6 months)
- 🎯 **Advanced Patterns** (Phase 4) - 3-4 weeks
- 🎯 **Subvariable Flow** - 3-4 weeks
- 🎯 **Value Set Analysis** - 2-3 weeks

### Long Term (6-12 months)
- Float operations (if needed)
- Architecture-specific rules (if needed)
- Esoteric patterns (low ROI)

---

## Success Metrics

| Metric | Current (40 rules) | Phase 1.5 (50 rules) | Phase 2 (60 rules) | Phase 3 (70 rules) | Phase 4 (85 rules) |
|--------|-------------------|---------------------|-------------------|-------------------|-------------------|
| **Rule Coverage** | 29% | 37% | 44% | 51% | 62% |
| **Quality Improvement** | Baseline | +15% | +30% | +45% | +60% |
| **Type Accuracy** | Good | Good | Excellent | Excellent | Excellent |
| **Array Detection** | Fair | Fair | Good | Excellent | Excellent |
| **Bit Manipulation** | Good | Excellent | Excellent | Excellent | Excellent |

---

## References

- **Source Analysis**: `docs/GHIDRA_DECOMPILER_RESEARCH.md`
- **Implementation Plan**: `docs/IMPLEMENTATION_PLAN_GHIDRA_ENHANCEMENTS.md`
- **Current Rules**: `docs/SIMPLIFICATION_RULES.md`
- **Ghidra Source**: `ghidra-decompiler-src/ruleaction.cc` (14,000+ lines)

---

**Last Updated**: 2026-01-26
**Status**: 40/136 rules (29% coverage) ✓
**Next Milestone**: Phase 1.5 - Quick Wins (50 rules, 37% coverage)
