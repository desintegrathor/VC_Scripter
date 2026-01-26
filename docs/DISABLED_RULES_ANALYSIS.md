# Disabled Rules Analysis

**Date**: 2026-01-26
**Total Rules**: 103
**Enabled**: 66 (64%)
**Disabled**: 37 (36%)

This document analyzes all 37 disabled rules to identify which can be enabled and what infrastructure is needed.

---

## Executive Summary

### Infrastructure Categories

| Infrastructure Required | Count | Priority |
|------------------------|-------|----------|
| **CFG Integration** | 13 rules | 🔴 High |
| **Use-Def Chains** | 7 rules | 🔴 High |
| **Type Information** | 7 rules | 🟡 Medium |
| **Simple/Quick Wins** | 6 rules | 🟢 **Quick wins!** |
| **Advanced Analysis** | 4 rules | 🔴 High |

### Quick Wins (1 rule - can enable immediately)

1. **RuleCompareZero** - `x == 0 → !x` optimization (fully implemented)

### Near-Term Wins (5 rules - need intermediate value creation infrastructure)

2. **RuleNotDistribute** - De Morgan's laws (bitwise) - needs to create NOT instructions
3. **RuleIntLessEqual** - Normalize comparisons - needs to wrap in NOT
4. **RuleDemorganLaws** - De Morgan's laws (boolean) - needs to create NOT instructions
5. **RuleCopyChain** - Simplify copy chains - just enable delegation (trivial)
6. **RulePtrIndex** - Array notation - better handled at code emission (not IR level)

---

## Category 1: Bitwise Operations (1 rule)

### 1.1 RuleNotDistribute
- **Pattern**: `~(a&b) → ~a|~b` (De Morgan's laws for bitwise ops)
- **Status**: Disabled
- **Reason**: Listed as "disabled" but no technical blocker
- **Can Enable**: ✅ YES - Simple pattern matching
- **Priority**: 🟢 Quick win
- **Estimated Work**: 5 minutes

---

## Category 2: Arithmetic Operations (1 rule)

### 2.1 RuleCollectTerms
- **Pattern**: `a+b+c → canonical` (reorganize addition trees)
- **Status**: Disabled
- **Reason**: Needs expression tree rewriting
- **Can Enable**: ⚠️ PARTIAL - Needs tree traversal logic
- **Priority**: 🟡 Medium
- **Estimated Work**: 2-4 hours
- **Requirements**:
  - Traverse expression tree
  - Collect all additive terms
  - Sort and canonicalize

---

## Category 3: Comparison Operations (2 rules)

### 3.1 RuleCompareZero
- **Pattern**: `x == 0 → !x`, `x != 0 → x`
- **Status**: Disabled
- **Reason**: Uncertain (no technical blocker)
- **Can Enable**: ✅ YES - Simple pattern
- **Priority**: 🟢 Quick win
- **Estimated Work**: 5 minutes

### 3.2 RuleIntLessEqual
- **Pattern**: `x<=y → !(x>y)` (normalize comparisons)
- **Status**: Disabled
- **Reason**: Uncertain (no technical blocker)
- **Can Enable**: ✅ YES - Simple transformation
- **Priority**: 🟢 Quick win
- **Estimated Work**: 5 minutes

---

## Category 4: Type Conversion (4 rules)

### 4.1 RulePromoteTypes
- **Pattern**: `char + char → int` (C integer promotion detection)
- **Status**: Disabled
- **Reason**: Needs type system integration
- **Can Enable**: ❌ NO - Requires type inference
- **Priority**: 🟡 Medium
- **Requirements**:
  - Type information for each SSA value
  - C promotion rules implementation

### 4.2 RuleIntegralPromotion
- **Pattern**: Optimize promoted integral arithmetic
- **Status**: Disabled
- **Reason**: Needs type system
- **Can Enable**: ❌ NO - Requires type inference
- **Priority**: 🟡 Medium
- **Requirements**: Same as RulePromoteTypes

### 4.3 RuleSignExtendDetect
- **Pattern**: Detect sign vs zero extension patterns
- **Status**: Disabled
- **Reason**: Needs type system
- **Can Enable**: ❌ NO - Requires type inference
- **Priority**: 🟡 Medium
- **Requirements**: Sign/unsigned type tracking

### 4.4 RuleTypeCoercion
- **Pattern**: Optimize mixed-type expressions
- **Status**: Disabled
- **Reason**: Needs type system
- **Can Enable**: ❌ NO - Requires type inference
- **Priority**: 🟡 Medium
- **Requirements**: Full type inference system

---

## Category 5: Pointer & Array (6 rules)

### 5.1 RulePtrNullCheck
- **Pattern**: `ptr == 0 → !ptr`
- **Status**: Disabled
- **Reason**: Needs type information (to identify pointers)
- **Can Enable**: ⚠️ PARTIAL - Could enable with heuristics
- **Priority**: 🟡 Medium
- **Estimated Work**: 1-2 hours
- **Requirements**:
  - Heuristic: values compared to 0 could be pointers
  - Or: type inference to identify pointer types

### 5.2 RulePtrCompare
- **Pattern**: `(ptr+4) < (ptr+8) → 4 < 8`
- **Status**: Disabled
- **Reason**: Needs alias analysis
- **Can Enable**: ❌ NO - Requires alias analysis
- **Priority**: 🔴 High (complex)
- **Requirements**:
  - Alias analysis to ensure ptr is same base
  - Pointer arithmetic tracking

### 5.3 RulePtrDiff
- **Pattern**: `(ptr1-ptr2)/4 → count` (element count)
- **Status**: Disabled
- **Reason**: Needs type information
- **Can Enable**: ❌ NO - Requires type sizes
- **Priority**: 🟡 Medium
- **Requirements**: Type system with sizeof information

### 5.4 RuleArrayBase
- **Pattern**: `&arr[0] → arr`
- **Status**: Disabled
- **Reason**: Needs ADDR opcode
- **Can Enable**: ⚠️ DEPENDS - Check if ADDR opcode exists
- **Priority**: 🟢 Quick win IF opcode exists
- **Estimated Work**: 30 minutes (if opcode exists)

### 5.5 RuleStructOffset
- **Pattern**: `ptr + 12 → ptr->field`
- **Status**: Disabled
- **Reason**: Needs struct type information
- **Can Enable**: ❌ NO - Requires struct definitions
- **Priority**: 🔴 High (but complex)
- **Requirements**: Struct type database from SDK

### 5.6 RulePtrIndex
- **Pattern**: `*(ptr+4) → ptr[1]` (presentation-only)
- **Status**: Disabled
- **Reason**: Presentation-only transformation
- **Can Enable**: ✅ YES - Cosmetic improvement
- **Priority**: 🟢 Quick win
- **Estimated Work**: 30 minutes
- **Note**: Only improves readability, doesn't affect semantics

---

## Category 6: Advanced Patterns (6 rules)

### 6.1 RuleDemorganLaws
- **Pattern**: `!(a && b) → !a || !b`
- **Status**: Disabled
- **Reason**: Listed as "needs expression tree" but actually simple
- **Can Enable**: ✅ YES - Standard boolean transformation
- **Priority**: 🟢 Quick win
- **Estimated Work**: 10 minutes

### 6.2 RuleAbsoluteValue
- **Pattern**: `(x < 0) ? -x : x → abs(x)`
- **Status**: Disabled
- **Reason**: Needs CFG analysis (ternary operator)
- **Can Enable**: ❌ NO - Requires CFG
- **Priority**: 🔴 High
- **Requirements**: Control flow analysis for ternary/if patterns

### 6.3 RuleMinMaxPatterns
- **Pattern**: `(a < b) ? a : b → min(a,b)`
- **Status**: Disabled
- **Reason**: Needs CFG analysis
- **Can Enable**: ❌ NO - Requires CFG
- **Priority**: 🔴 High
- **Requirements**: Same as RuleAbsoluteValue

### 6.4 RuleSignMagnitude
- **Pattern**: Sign/magnitude conversion optimization
- **Status**: Disabled
- **Reason**: Needs CFG
- **Can Enable**: ❌ NO - Requires CFG
- **Priority**: 🔴 High
- **Requirements**: CFG analysis

### 6.5 RuleRangeCheck
- **Pattern**: `(x >= a) && (x <= b)` optimization
- **Status**: Disabled
- **Reason**: Needs boolean expression analysis
- **Can Enable**: ⚠️ PARTIAL - Simple cases possible
- **Priority**: 🟡 Medium
- **Estimated Work**: 2-3 hours
- **Requirements**:
  - Boolean expression tree traversal
  - Pattern matching for range patterns
  - Could enable for simple cases only

### 6.6 RuleSelectPattern
- **Pattern**: `cond ? a : a → a` (simplify identical branches)
- **Status**: Disabled
- **Reason**: Needs CFG analysis
- **Can Enable**: ❌ NO - Requires CFG
- **Priority**: 🔴 High
- **Requirements**: Control flow analysis

---

## Category 7: Loop Optimization (8 rules)

All loop rules require CFG integration and loop analysis.

### 7.1 RuleInductionSimplify
- **Pattern**: `j = i * 4 + base` (induction variable simplification)
- **Status**: Disabled
- **Reason**: Needs loop analysis
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High
- **Requirements**: Loop detection, induction variable analysis

### 7.2 RuleLoopInvariantDetect
- **Pattern**: Detect loop-invariant expressions
- **Status**: Disabled
- **Reason**: Needs CFG
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High
- **Requirements**: Loop detection, dominance analysis

### 7.3 RuleLoopStrength
- **Pattern**: `j = i * 4 → j += 4` (strength reduction)
- **Status**: Disabled
- **Reason**: Needs induction analysis
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High
- **Requirements**: Induction variable analysis

### 7.4 RuleLoopUnswitch
- **Pattern**: Hoist loop-invariant conditions
- **Status**: Disabled
- **Reason**: Needs CFG
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High
- **Requirements**: Loop detection, code motion analysis

### 7.5 RuleCountedLoop
- **Pattern**: Detect loop trip counts
- **Status**: Disabled
- **Reason**: Needs CFG
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High
- **Requirements**: Loop detection, trip count analysis

### 7.6 RuleLoopElimination
- **Pattern**: Dead loop removal
- **Status**: Disabled
- **Reason**: Needs CFG
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High
- **Requirements**: Loop detection, side effect analysis

### 7.7 RuleLoopRotate
- **Pattern**: Normalize loop forms
- **Status**: Disabled
- **Reason**: Needs CFG
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High
- **Requirements**: Loop restructuring capability

### 7.8 RuleLoopFusion
- **Pattern**: Merge adjacent loops
- **Status**: Disabled
- **Reason**: Needs CFG + dependency analysis
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High (most complex)
- **Requirements**: Loop detection, dependency analysis, code motion

---

## Category 8: Data Flow Optimization (11 rules)

Most data flow rules require use-def chain infrastructure.

### 8.1 RuleCopyPropagation
- **Pattern**: `x = y; z = x + 1 → z = y + 1`
- **Status**: Disabled
- **Reason**: Needs use-def chains
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High (high impact)
- **Requirements**: Use-def chain analysis

### 8.2 RuleConstantPropagation
- **Pattern**: `x = 5; y = x + 3 → y = 8`
- **Status**: Disabled
- **Reason**: Needs reaching definitions
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High (high impact)
- **Requirements**: Reaching definitions analysis

### 8.3 RuleDeadValue
- **Pattern**: Remove unused SSA values
- **Status**: Disabled
- **Reason**: Needs use-def chains
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High (code cleanup)
- **Requirements**: Use-def chains, liveness analysis

### 8.4 RulePhiSimplify
- **Pattern**: `x = phi(y, y) → x = y`
- **Status**: Disabled
- **Reason**: Needs CFG
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High
- **Requirements**: Phi node representation, CFG

### 8.5 RuleSingleUseInline
- **Pattern**: `temp = a + b; r = temp * 2 → r = (a+b)*2`
- **Status**: Disabled
- **Reason**: Needs use count tracking
- **Can Enable**: ⚠️ PARTIAL - Simple heuristic possible
- **Priority**: 🟡 Medium
- **Estimated Work**: 4-6 hours
- **Requirements**:
  - Use count tracking (simpler than full use-def chains)
  - Could scan all instructions to count uses

### 8.6 RuleCopyChain
- **Pattern**: Simplify copy chains
- **Status**: Disabled (delegates to RuleRedundantCopy)
- **Reason**: Already handled by RuleRedundantCopy
- **Can Enable**: ✅ YES - Just a delegation wrapper
- **Priority**: 🟢 Quick win
- **Estimated Work**: 2 minutes (just enable it)

### 8.7 RuleValueNumbering
- **Pattern**: `x = a + b; y = a + b → y = x` (CSE)
- **Status**: Disabled
- **Reason**: Needs value numbering infrastructure
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High (significant optimization)
- **Requirements**: Value numbering hash table, expression canonicalization

### 8.8 RuleUnusedResult
- **Pattern**: Remove operations with unused results
- **Status**: Disabled
- **Reason**: Needs use-def chains
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High
- **Requirements**: Use-def chains

### 8.9 RuleTrivialPhi
- **Pattern**: `x = phi(y) → x = y`
- **Status**: Disabled
- **Reason**: Needs CFG
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High
- **Requirements**: Phi nodes, CFG

### 8.10 RuleForwardSubstitution
- **Pattern**: `x = 5; z = x → z = 5`
- **Status**: Disabled
- **Reason**: Needs use analysis
- **Can Enable**: ❌ NO
- **Priority**: 🔴 High (high impact)
- **Requirements**: Use-def chains or reaching definitions

### 8.11 (Missing from count - RuleCopyChain counted above)

---

## Action Plan: Revised After Code Analysis

### Phase 1A: Enable 1 True Quick Win (🟢 Immediate - 5 minutes)

Only 1 rule is truly ready (fully implemented, just needs enabling):

1. **RuleCompareZero** - `x == 0 → !x` (change `is_disabled = False`)

**Estimated Impact**: Minor - simplifies zero comparisons
**Risk**: Very low - fully implemented and tested logic
**Testing**: Run on tdm.scr and LEVEL.SCR

### Phase 1B: Implement Intermediate Value Creation (🟡 1-2 hours)

Infrastructure needed to unlock 3 more rules:

**What's needed**: Ability for rules to create intermediate SSA values/instructions

**Current limitation**: Rules like RuleNotDistribute need to create new NOT instructions for each operand, but the current `apply()` interface only returns a single replacement instruction.

**Solution options**:
1. **Multi-instruction return**: Allow `apply()` to return List[SSAInstruction]
2. **Value builder helper**: Add SSAValueBuilder to simplification context
3. **Two-pass system**: First pass creates values, second pass uses them

**Unlocks**:
- RuleNotDistribute (De Morgan bitwise)
- RuleIntLessEqual (comparison normalization)
- RuleDemorganLaws (De Morgan boolean)

### Phase 1C: Enable Near-Term Wins (🟢 After Phase 1B - 30 minutes)

Once intermediate value creation is implemented:

1. **RuleNotDistribute** - Implement De Morgan distribution
2. **RuleIntLessEqual** - Implement comparison wrapping
3. **RuleDemorganLaws** - Implement De Morgan for boolean
4. **RuleCopyChain** - Just enable (delegates to RuleRedundantCopy)

**Estimated Impact**: Moderate - better boolean/comparison optimization
**Risk**: Low - well-defined transformations
**Testing**: Comprehensive validation on all test scripts

### Phase 2: Medium Complexity (🟡 1-2 days)

Rules requiring moderate implementation work:

1. **RuleCollectTerms** - Canonicalize addition trees (2-4 hours)
2. **RuleRangeCheck** - Simple range patterns (2-3 hours)
3. **RuleSingleUseInline** - Use count heuristic (4-6 hours)
4. **RulePtrNullCheck** - Pointer heuristic (1-2 hours)
5. **RuleArrayBase** - If ADDR opcode exists (30 min check + 30 min implement)

**Estimated Impact**: Moderate to high
**Risk**: Low to medium
**Testing**: Comprehensive validation needed

### Phase 3: Infrastructure Investment (🔴 1-2 weeks)

High-value infrastructure that unlocks many rules:

1. **Use-Def Chains** - Unlocks 7 data flow rules (3-5 days)
   - RuleCopyPropagation
   - RuleConstantPropagation
   - RuleDeadValue
   - RuleUnusedResult
   - RuleForwardSubstitution

2. **Basic CFG Integration** - Unlocks 13 rules (3-5 days)
   - All 8 loop rules
   - 5 advanced pattern rules

3. **Type System** - Unlocks 7 rules (2-3 days)
   - 4 type conversion rules
   - 3 pointer rules

---

## Recommendation

**Immediate Action**: Start with Phase 1 (6 quick wins)
- Low risk, immediate benefit
- 1 hour of work
- Boosts rule count from 66 to 72 enabled rules

**Next Step**: Evaluate Phase 2 vs Phase 3
- Phase 2: Incremental improvements, 5 more rules
- Phase 3: Infrastructure investment, 20+ rules unlocked

**Strategic Goal**:
- Quick wins: 72/103 enabled (70%)
- With Phase 2: 77/103 enabled (75%)
- With Phase 3: 97+/103 enabled (94%+)

---

## Infrastructure Requirements Summary

### Critical Path: Use-Def Chains

**What it is**: Track which instructions use each SSA value

**Implementation**:
```python
class UseDefChain:
    def __init__(self, ssa_func: SSAFunction):
        self.uses: Dict[SSAValue, List[SSAInstruction]] = {}
        self.defs: Dict[SSAValue, SSAInstruction] = {}
        self._build_chains(ssa_func)

    def get_uses(self, value: SSAValue) -> List[SSAInstruction]:
        return self.uses.get(value, [])

    def get_def(self, value: SSAValue) -> Optional[SSAInstruction]:
        return self.defs.get(value)

    def use_count(self, value: SSAValue) -> int:
        return len(self.get_uses(value))
```

**Enables**: 7 high-impact data flow rules

### Critical Path: CFG Integration

**What it is**: Integrate existing CFG with SSA IR

**Implementation**:
- Already have CFG in `vcdecomp/core/ir/cfg.py`
- Need to link SSA instructions to CFG basic blocks
- Add CFG traversal methods to SSA function

**Enables**: 13 rules (8 loop + 5 pattern)

### Critical Path: Type System

**What it is**: Track type information for SSA values

**Implementation**:
- Parse SDK headers for struct definitions
- Infer types from opcodes (IADD → int, FADD → float)
- Propagate types through SSA graph

**Enables**: 7 rules (4 type + 3 pointer)

---

**End of Analysis**
