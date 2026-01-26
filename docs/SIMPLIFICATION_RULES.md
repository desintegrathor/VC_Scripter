# Simplification Rules Summary

This document provides an overview of all 70 SSA-level transformation rules implemented in the decompiler.

## Overview

- **Total Rules**: 70 (Phase 3 target: 70) ✅
- **Ghidra Reference**: 136 rules
- **Coverage**: ~51% of Ghidra's rule set
- **Organization**: 10 rule categories
- **Enabled**: 57 rules (13 disabled by default)

## Rule Categories

### 1. Canonical Form (1 rule)
Rules that establish canonical form for better CSE (Common Subexpression Elimination).

| Rule | Transformation | Description |
|------|----------------|-------------|
| RuleTermOrder | `3 + x → x + 3` | Order terms for commutative operations |

### 2. Constant Folding (3 rules)
Rules that evaluate operations on constants at compile time.

| Rule | Transformation | Description |
|------|----------------|-------------|
| RuleConstantFold | `2 + 3 → 5` | Fold arithmetic/bitwise operations |
| RuleCompareConstants | `5 == 5 → true` | Fold comparison operations |
| RuleCastConstant | `int(5.7) → 5` | Fold type conversions on constants |

### 3. Identity Rules (6 rules)
Rules that simplify operations with identity elements.

| Rule | Transformation | Description |
|------|----------------|-------------|
| RuleAndIdentity | `x & 0xFFFFFFFF → x` | AND with all bits set |
| RuleOrIdentity | `x \| 0 → x` | OR with zero |
| RuleAddIdentity | `x + 0 → x` | Addition with zero |
| RuleMulIdentity | `x * 1 → x` | Multiplication with one |
| RuleSubIdentity | `x - 0 → x`, `x - x → 0` | Subtraction identities |
| RuleDivIdentity | `x / 1 → x` | Division by one |

### 4. Bitwise Operations (12 rules)
Rules for simplifying bitwise operations.

| Rule | Transformation | Description |
|------|----------------|-------------|
| RuleAndMask | `(x & 0xff) & 0x0f → x & 0x0f` | Combine AND masks |
| RuleOrMask | `(x \| 0x0f) \| 0xff → x \| 0xff` | Combine OR masks |
| RuleXorCancel | `x ^ x → 0`, `x ^ 0 → x` | XOR cancellation |
| RuleShiftByZero | `x << 0 → x`, `x >> 0 → x` | Shifts by zero |
| RuleDoubleShift | `(x << 2) << 3 → x << 5` | Combine consecutive shifts |
| RuleAndWithOr | `(x \| y) & x → x` | Absorption law (AND/OR) |
| RuleOrWithAnd | `(x & y) \| x → x` | Absorption law (OR/AND) |
| RuleAndZero | `x & 0 → 0` | AND with zero |
| RuleOrAllOnes | `x \| 0xFFFFFFFF → 0xFFFFFFFF` | OR with all bits set |
| RuleNotDistribute | `~(a&b) → ~a\|~b` | DeMorgan's laws (disabled) |
| RuleHighOrderAnd | `(x&0xff00)>>8 → (x>>8)&0xff` | Byte extraction pattern |
| RuleBitUndistribute | `(x&a)\|(x&b) → x&(a\|b)` | Factor common terms |

### 5. Arithmetic Operations (13 rules)
Rules for simplifying arithmetic operations.

| Rule | Transformation | Description |
|------|----------------|-------------|
| RuleDoubleAdd | `(x + 2) + 3 → x + 5` | Combine consecutive additions |
| RuleDoubleSub | `(x - 2) - 3 → x - 5` | Combine consecutive subtractions |
| RuleNegateIdentity | `-(-x) → x` | Double negation |
| RuleMulByPowerOf2 | `x * 4 → x << 2` | Multiply by power of 2 → shift |
| RuleDivByPowerOf2 | `x / 4 → x >> 2` | Divide by power of 2 → shift |
| RuleModByPowerOf2 | `x % 8 → x & 7` | Modulo by power of 2 → AND |
| RuleMulZero | `x * 0 → 0` | Multiplication by zero |
| RuleModOne | `x % 1 → 0` | Modulo by one |
| RuleCancelAddSub | `(x + y) - y → x` | Addition/subtraction cancellation |
| RuleAbsorbNegation | `x - (-y) → x + y` | Absorb negation into operation |
| RuleStrengthReduction | `x / x → 1` | Replace expensive ops with cheaper ones |
| RuleMulDistribute | `x*a + x*b → x*(a+b)` | Factor common multipliers |
| RuleCollectTerms | `a+b+c → canonical` | Reorganize addition trees (disabled) |

### 6. Comparison Operations (8 rules)
Rules for simplifying comparison operations.

| Rule | Transformation | Description |
|------|----------------|-------------|
| RuleEqualitySelf | `x == x → true`, `x != x → false` | Self-comparison |
| RuleLessEqualSelf | `x <= x → true`, `x < x → false` | Self-comparison (ordered) |
| RuleNotEqual | `!(x == y) → x != y` | Negate comparison operators |
| RuleCompareZero | `x == 0 → !x` | Compare with zero (disabled) |
| RuleCompareConstants | `5 < 10 → true` | Handled by RuleConstantFold |
| RuleLessEqual | `x<=y && x>=y → x==y` | Redundant comparison elimination |
| RuleIntLessEqual | `x<=y → !(x>y)` | Normalize comparisons (disabled) |
| RuleBxor2NotEqual | `(a^b)!=0 → a!=b` | XOR-based inequality pattern |

### 7. Boolean Logic (4 rules)
Rules for simplifying boolean operations.

| Rule | Transformation | Description |
|------|----------------|-------------|
| RuleBooleanAnd | `x && true → x`, `x && false → false` | Logical AND with constants |
| RuleBooleanOr | `x \|\| true → true`, `x \|\| false → x` | Logical OR with constants |
| RuleBooleanNot | `!(!x) → x` | Double negation |
| RuleBooleanDedup | `x && x → x`, `x \|\| x → x` | Remove duplicate operations |

### 8. Type Conversions (15 rules)
Rules for simplifying type conversions, casts, and extensions.

| Rule | Transformation | Description |
|------|----------------|-------------|
| RuleCastChain | `int→float→int → int` | Eliminate redundant cast chains |
| RuleCastIdentity | `int→int → identity` | Remove identity casts |
| RuleCastConstant | `int(5.7) → 5` | Fold type conversions on constants |
| RuleSextChain | `sext(sext(x)) → sext(x)` | Collapse sign extension chains |
| RuleTruncateZext | `zext(trunc(x)) → x` | Eliminate trunc-then-extend |
| RuleBoolZext | `int(x == y) → x == y` | Eliminate boolean→int conversions |
| RuleZextEliminate | `int(int(x)) → int(x)` | Remove unnecessary zero extensions |
| RulePromoteTypes | `char + char → int` | C integer promotion detection (disabled) |
| RuleCastPropagation | Cast info flow | Propagate cast info through expressions |
| RuleIntegralPromotion | Optimize promoted ops | Optimize promoted integral arithmetic (disabled) |
| RuleFloatIntRoundtrip | `int(float(x)) → x` | Detect float→int→float roundtrips |
| RuleConstantCast | `(int)X → info` | Propagate type info through constant casts |
| RuleSignExtendDetect | Sign vs zero | Sign extension pattern detection (disabled) |
| RuleNarrowingRedundant | `char(int(c)) → c` | Eliminate redundant narrowing |
| RuleTypeCoercion | Mixed-type expr | Optimize mixed-type expressions (disabled) |

### 9. Pointer & Array (10 rules)
Rules for simplifying pointer arithmetic and array access patterns.

| Rule | Transformation | Description |
|------|----------------|-------------|
| RulePtrAddChain | `(ptr + 4) + 8 → ptr + 12` | Chain consecutive pointer additions |
| RulePtrSubNormalize | `ptr - (-4) → ptr + 4` | Normalize negative subtraction |
| RulePtrArithIdentity | `ptr + 0 → ptr` | Eliminate identity operations |
| RuleArrayBounds | `base + (i * size)` | Constant fold array index calculation |
| RulePtrNullCheck | `ptr == 0 → !ptr` | Optimize null checks (disabled - needs type info) |
| RulePtrCompare | `(ptr+4) < (ptr+8) → 4 < 8` | Simplify pointer comparisons (disabled - needs alias analysis) |
| RulePtrDiff | `(ptr1-ptr2)/4 → count` | Detect element count patterns (disabled - needs type info) |
| RuleArrayBase | `&arr[0] → arr` | Simplify array base address (disabled - needs ADDR opcode) |
| RuleStructOffset | `ptr + 12 → ptr->field` | Detect struct field access (disabled - needs struct types) |
| RulePtrIndex | `*(ptr+4) → ptr[1]` | Convert to array notation (disabled - presentation-only) |

## Rule Application Strategy

### Fixed-Point Iteration
The SimplificationEngine applies rules iteratively until convergence (no more changes):

```python
engine = SimplificationEngine()
stats = engine.simplify_to_fixpoint(ssa_func)
```

### Application Phases
Rules are applied in phases to maximize effectiveness:

1. **Canonical Form** - Establish consistent ordering
2. **Constant Folding** - Evaluate constant operations
3. **Identity Rules** - Simplify with identity elements
4. **Nested Operations** - Combine nested bitwise/arithmetic ops
5. **Optimization** - Apply strength reduction and advanced patterns
6. **Comparison** - Simplify comparison operations
7. **Boolean Logic** - Simplify logical operations
8. **Type Conversions** - Eliminate unnecessary casts
9. **Pointer & Array** - Simplify pointer arithmetic and array access

### Emergent Simplification
One rule can enable another through iteration:
- `(x + 2) + 3` → `x + 5` (RuleDoubleAdd)
- `x + 5 - 5` → `x + 0` (RuleCancelAddSub)
- `x + 0` → `x` (RuleAddIdentity)

## Implementation Details

### File Organization
```
vcdecomp/core/ir/rules/
├── __init__.py          # Central registry
├── base.py              # Base class and helpers
├── identity.py          # Identity rules (6 rules)
├── bitwise.py           # Bitwise rules (9 rules)
├── arithmetic.py        # Arithmetic rules (11 rules)
├── comparison.py        # Comparison rules (5 rules)
├── boolean.py           # Boolean rules (4 rules)
├── advanced_arithmetic.py  # Advanced rules (3 rules)
├── typeconv.py          # Type conversion rules (3 rules)
└── pointer.py           # Pointer rules (placeholder)
```

### Engine Architecture
```
vcdecomp/core/ir/
├── simplify.py          # Backward compatibility wrapper
├── simplify_engine.py   # Fixed-point transformation engine
└── rules/               # Modular rule package
```

## Performance Characteristics

- **Max Iterations**: 100 (configurable)
- **Typical Convergence**: 3-10 iterations
- **Worst Case**: Early termination after max iterations
- **Rule Complexity**: O(n) per rule application
- **Total Complexity**: O(k * n * r) where:
  - k = number of iterations
  - n = number of SSA instructions
  - r = number of enabled rules

## Comparison with Ghidra

| Metric | VC-Decompiler | Ghidra |
|--------|---------------|--------|
| Total Rules | 70 | 136 |
| Coverage | ~51% | 100% |
| Rule Categories | 10 | 15+ |
| Fixed-Point Engine | ✓ | ✓ |
| Modular Organization | ✓ | ✓ |
| Power-of-2 Optimizations | ✓ | ✓ |
| Type Inference Rules | 15 | 25+ |
| Pointer/Array Rules | 10 | 15+ |

## Future Enhancements

Potential additions for Phase 3+ (70+ rules):
1. **Pointer Arithmetic** (Phase 3) - Array indexing optimizations, pointer addition chains
2. **Range Analysis** (Phase 4) - Value range-based simplifications
3. **Float Operations** (Phase 4) - Floating-point specific optimizations
4. **Bit Manipulation** (Phase 4) - Advanced bit manipulation patterns
5. **Memory Access** (Phase 5) - Load/store optimization patterns

## References

- **Ghidra Decompiler**: `docs/GHIDRA_DECOMPILER_RESEARCH.md`
- **Implementation Plan**: `docs/IMPLEMENTATION_PLAN_GHIDRA_ENHANCEMENTS.md`
- **Source Code**: `vcdecomp/core/ir/rules/`
- **Engine**: `vcdecomp/core/ir/simplify_engine.py`

---

**Last Updated**: 2026-01-26
**Rule Count**: 60 (53 enabled, 7 disabled)
**Status**: Phase 2 complete - Type & Extension Rules ✓✓✓
**Next**: Phase 3 - Pointer & Array Rules (target: 70)
