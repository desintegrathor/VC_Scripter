# Implementation Plan: Ghidra-Inspired Decompiler Enhancements

**Based on:** GHIDRA_DECOMPILER_RESEARCH.md
**Created:** 2026-01-26
**Timeline:** 3-6 months (phased approach)
**Priority:** High

---

## Overview

This document provides a concrete, actionable implementation plan for enhancing the VC-Script-Decompiler based on research into Ghidra's advanced techniques. The plan is divided into three phases with clear milestones and deliverables.

---

## Phase 1: Transformation Rules & Fixed-Point Engine (Weeks 1-12)

**Goal:** Expand simplification capabilities from 8 rules to 40-50 rules with iterative application

**Estimated Effort:** 60-80 hours
**Expected Impact:** 20-30% cleaner output, better expression simplification
**Priority:** ⭐⭐⭐ HIGHEST

### Week 1-2: Framework Enhancement

#### Task 1.1: Refactor Simplification Engine
**File:** `vcdecomp/core/ir/simplify.py`
**Time:** 8 hours

- [ ] Add `SimplificationEngine` class with fixed-point iteration
- [ ] Implement convergence detection (no changes = done)
- [ ] Add max iteration safety limit (default: 100)
- [ ] Add statistics tracking (iterations, rules applied, convergence time)
- [ ] Add rule enable/disable mechanism
- [ ] Write unit tests for convergence behavior

**Deliverable:** Working fixed-point engine that applies rules until convergence

#### Task 1.2: Create Rules Package Structure
**Files:** `vcdecomp/core/ir/rules/__init__.py`, submodules
**Time:** 4 hours

```
vcdecomp/core/ir/rules/
├── __init__.py         # Rule registry and exports
├── arithmetic.py       # 10 arithmetic rules
├── bitwise.py          # 8 bitwise rules
├── comparison.py       # 6 comparison rules
├── boolean.py          # 6 boolean logic rules
├── typeconv.py         # 5 type conversion rules
└── pointer.py          # 5 pointer arithmetic rules
```

- [ ] Create package structure
- [ ] Move existing 8 rules from `simplify.py` to appropriate modules
- [ ] Set up rule registry (`ALL_RULES` list)
- [ ] Update imports in main decompiler pipeline

**Deliverable:** Clean package structure with existing rules migrated

---

### Week 3-5: Arithmetic Rules (10 rules)

#### Task 1.3: Implement Basic Arithmetic Rules
**File:** `vcdecomp/core/ir/rules/arithmetic.py`
**Time:** 16 hours (1.6 hours per rule)

##### Rule 1: RuleCollectTerms
**Pattern:** `(a + b) + c` → `a + (b + c)` (right-associative canonical form)
**Purpose:** Enable better CSE and constant folding
**Test cases:** 3-4 variations

##### Rule 2: RuleDoubleAdd
**Pattern:** `(x + const1) + const2` → `x + (const1 + const2)`
**Purpose:** Fold adjacent constants
**Test cases:** 3 variations

##### Rule 3: RuleDoubleSub
**Pattern:** `(x - a) - b` → `x - (a + b)`
**Purpose:** Simplify subtraction chains
**Test cases:** 3 variations

##### Rule 4: RuleMulDistribute
**Pattern:** `x * a + x * b` → `x * (a + b)` (when profitable)
**Purpose:** Factor out common terms
**Test cases:** 4 variations (profitable vs. not)

##### Rule 5: RuleFactorConstant
**Pattern:** `2*x + 4*y` → `2*(x + 2*y)` (when profitable)
**Purpose:** Extract common factors
**Test cases:** 3 variations

##### Rule 6: RuleNegateIdentity
**Pattern:** `-(-x)` → `x`
**Purpose:** Remove double negation
**Test cases:** 2 variations

##### Rule 7: RuleDivByPowerOf2
**Pattern:** `x / 4` → `x >> 2` (when profitable based on context)
**Purpose:** Use shifts instead of division (faster, clearer for indexing)
**Test cases:** 3 variations (2, 4, 8)

##### Rule 8: RuleMulByPowerOf2
**Pattern:** `x * 8` → `x << 3` (when profitable)
**Purpose:** Use shifts instead of multiplication
**Test cases:** 3 variations

##### Rule 9: RuleModSimplify
**Pattern:** `x % 1` → `0`, `x % power_of_2` → `x & (power_of_2 - 1)`
**Purpose:** Optimize modulo operations
**Test cases:** 3 variations

##### Rule 10: RuleSubToAdd
**Pattern:** `x - (-y)` → `x + y`
**Purpose:** Canonicalize to addition
**Test cases:** 2 variations

**Deliverable:** 10 working arithmetic rules with tests

---

### Week 6-7: Bitwise Rules (8 rules)

#### Task 1.4: Implement Bitwise Rules
**File:** `vcdecomp/core/ir/rules/bitwise.py`
**Time:** 12 hours (1.5 hours per rule)

##### Rule 1: RuleAndDistribute
**Pattern:** `(a | b) & c` → `(a & c) | (b & c)` (when beneficial)
**Test cases:** 3 variations

##### Rule 2: RuleOrConsume
**Pattern:** `(x | const1) | const2` → `x | (const1 | const2)`
**Test cases:** 2 variations

##### Rule 3: RuleOrCollapse
**Pattern:** `x | x` → `x`, `x | 0` → `x`, `x | -1` → `-1`
**Test cases:** 4 variations

##### Rule 4: RuleXorCancel
**Pattern:** `x ^ x` → `0`, `x ^ 0` → `x`
**Test cases:** 3 variations

##### Rule 5: RuleAndCommute
**Pattern:** Canonicalize AND order (constants right, variables left)
**Test cases:** 3 variations

##### Rule 6: RuleHighOrderAnd
**Pattern:** `(x & 0xff00) >> 8` → `(x >> 8) & 0xff`
**Test cases:** 3 variations

##### Rule 7: RuleShiftBitops
**Pattern:** `(x << a) & mask` → optimize based on mask
**Test cases:** 4 variations

##### Rule 8: RuleNotDistribute
**Pattern:** `~(a & b)` → `~a | ~b` (DeMorgan's law)
**Test cases:** 3 variations

**Deliverable:** 8 working bitwise rules with tests

---

### Week 8-9: Comparison & Boolean Rules (12 rules)

#### Task 1.5: Implement Comparison Rules
**File:** `vcdecomp/core/ir/rules/comparison.py`
**Time:** 8 hours

##### Rule 1: RuleEquality
**Pattern:** `x == x` → `true`, `x != x` → `false`
**Test cases:** 3 variations

##### Rule 2: RuleLessEqual
**Pattern:** `x <= y && x >= y` → `x == y`
**Test cases:** 2 variations

##### Rule 3: RuleIntLessEqual
**Pattern:** `x <= y` → `!(x > y)` (canonical form)
**Test cases:** 2 variations

##### Rule 4: RuleLessNotEqual
**Pattern:** Eliminate redundant conditions in chains
**Test cases:** 3 variations

##### Rule 5: RuleCompareRange
**Pattern:** `x > 0 && x < 10` → optimize
**Test cases:** 3 variations

##### Rule 6: RuleFloatRange
**Pattern:** Track floating-point comparisons
**Test cases:** 2 variations

#### Task 1.6: Implement Boolean Rules
**File:** `vcdecomp/core/ir/rules/boolean.py`
**Time:** 8 hours

##### Rule 1: RuleBooleanUndistribute
**Pattern:** `(a && b) || (a && c)` → `a && (b || c)`
**Test cases:** 3 variations

##### Rule 2: RuleBooleanDedup
**Pattern:** `a && a` → `a`, `a || a` → `a`
**Test cases:** 3 variations

##### Rule 3: RuleBooleanNegate
**Pattern:** `!(a && b)` → `!a || !b` (DeMorgan's law)
**Test cases:** 3 variations

##### Rule 4: RuleBoolZext
**Pattern:** Convert bool to int when needed
**Test cases:** 2 variations

##### Rule 5: RuleLogic2Bool
**Pattern:** Convert bitwise AND to logical AND when appropriate
**Test cases:** 2 variations

##### Rule 6: RuleTrivialBool
**Pattern:** `x && true` → `x`, `x || false` → `x`
**Test cases:** 4 variations

**Deliverable:** 12 working comparison/boolean rules with tests

---

### Week 10-11: Type Conversion & Pointer Rules (10 rules)

#### Task 1.7: Implement Type Conversion Rules
**File:** `vcdecomp/core/ir/rules/typeconv.py`
**Time:** 8 hours

##### Rule 1: RuleZextEliminate
**Pattern:** Remove unnecessary zero extensions
**Test cases:** 3 variations

##### Rule 2: RuleSextChain
**Pattern:** Collapse sign extension chains
**Test cases:** 2 variations

##### Rule 3: RuleCastChain
**Pattern:** `int→float→int` → `int`
**Test cases:** 3 variations

##### Rule 4: RuleTruncateZext
**Pattern:** `trunc(zext(x))` → `x`
**Test cases:** 2 variations

##### Rule 5: RulePromoteTypes
**Pattern:** Apply C integer promotion rules
**Test cases:** 3 variations

#### Task 1.8: Implement Pointer Arithmetic Rules
**File:** `vcdecomp/core/ir/rules/pointer.py`
**Time:** 8 hours

##### Rule 1: RulePointerAdd
**Pattern:** `(ptr + a) + b` → `ptr + (a + b)`
**Test cases:** 3 variations

##### Rule 2: RulePointerSub
**Pattern:** Simplify pointer differences
**Test cases:** 2 variations

##### Rule 3: RuleArrayIndex
**Pattern:** `base + i*4 + j*4` → `base + (i+j)*4`
**Test cases:** 3 variations

##### Rule 4: RuleAddressSimplify
**Pattern:** Simplify complex address computations
**Test cases:** 3 variations

##### Rule 5: RuleOffsetCanonical
**Pattern:** Canonicalize struct field offsets
**Test cases:** 2 variations

**Deliverable:** 10 working type/pointer rules with tests

---

### Week 12: Integration & Testing

#### Task 1.9: Integrate with Decompilation Pipeline
**File:** `vcdecomp/core/decompile.py`
**Time:** 8 hours

- [ ] Add SimplificationEngine to decompilation pipeline
- [ ] Add optimization level flag (0=none, 1=basic, 2=aggressive)
- [ ] Add command-line option `--optimize-level`
- [ ] Add statistics reporting
- [ ] Update CLI help text

```python
# New command-line option
py -3 -m vcdecomp structure --optimize-level 2 script.scr > output.c
```

#### Task 1.10: End-to-End Testing
**Files:** Test scripts in `decompiler_source_tests/`
**Time:** 8 hours

- [ ] Test all rules on `test1/tt.c`
- [ ] Test convergence on `test2/tdm.c`
- [ ] Test performance on `test3/LEVEL.C`
- [ ] Measure improvement metrics
- [ ] Generate before/after comparison report

**Metrics to measure:**
- Number of instructions before/after
- Convergence iterations
- Time taken for simplification
- Readability score (manual review)

**Deliverable:** Phase 1 complete with 40 rules, fixed-point engine, integration, and validation

---

## Phase 2: Dead Code Elimination & Enhanced SSA (Weeks 13-24)

**Goal:** Add DCE and improve SSA construction with dominator trees

**Estimated Effort:** 60-80 hours
**Expected Impact:** 10-15% better SSA form, improved type inference
**Priority:** ⭐⭐ HIGH

### Week 13-15: Dead Code Elimination

#### Task 2.1: Implement DCE Algorithm
**File:** `vcdecomp/core/ir/dce.py`
**Time:** 16 hours

- [ ] Implement liveness analysis (backward sweep)
- [ ] Mark instructions with side effects (CALL, XCALL, ASGN, RET)
- [ ] Propagate liveness to input values
- [ ] Remove dead instructions
- [ ] Remove unused SSA values
- [ ] Write comprehensive tests

**Algorithm:**
1. Seed worklist with side-effect instructions
2. Backward propagate liveness to producers
3. Remove unmarked instructions
4. Update SSA value uses

**Test cases:**
- Dead arithmetic (result unused)
- Dead assignments
- Partially dead code (some branches)
- Live code preservation

#### Task 2.2: Integrate DCE with Pipeline
**File:** `vcdecomp/core/decompile.py`
**Time:** 4 hours

- [ ] Add DCE after simplification
- [ ] Add statistics tracking
- [ ] Add command-line flag `--enable-dce`
- [ ] Test interaction with simplification

**Deliverable:** Working DCE that removes 15-20% of dead code

---

### Week 16-20: Augmented Dominator Tree

#### Task 2.3: Implement Dominator Tree Construction
**File:** `vcdecomp/core/ir/dominator.py`
**Time:** 20 hours

- [ ] Implement Lengauer-Tarjan algorithm for immediate dominators
- [ ] Build dominator tree from idom
- [ ] Compute dominator frontier
- [ ] Compute dominator depths
- [ ] Add visualization support (GraphViz)
- [ ] Write comprehensive tests

**Key data structures:**
```python
class DominatorTree:
    idom: Dict[int, int]              # Immediate dominator
    dom_tree: Dict[int, List[int]]    # Dominator tree (parent→children)
    dom_frontier: Dict[int, Set[int]]  # Dominator frontier
    depth: Dict[int, int]              # Depth in dominator tree
```

**Test cases:**
- Simple linear CFG
- Diamond CFG
- Loop CFG
- Complex nested loops
- Irreducible graphs (edge cases)

#### Task 2.4: Integrate with SSA Builder
**File:** `vcdecomp/core/ir/ssa.py`
**Time:** 12 hours

- [ ] Refactor SSA builder to use dominator tree
- [ ] Implement dominator-frontier-based phi placement
- [ ] Update renaming algorithm
- [ ] Validate against existing SSA output (should be identical or better)
- [ ] Add regression tests

**Deliverable:** Enhanced SSA construction with proper phi placement

---

### Week 21-24: Value Set Analysis Enhancement

#### Task 2.5: Enhance LoadGuard with Range Tracking
**File:** `vcdecomp/core/ir/load_guard.py`
**Time:** 16 hours

- [ ] Add value set analysis for pointer ranges
- [ ] Track min/max offsets for indexed accesses
- [ ] Detect access strides (regular patterns)
- [ ] Improve array dimension inference
- [ ] Add confidence scoring
- [ ] Write comprehensive tests

**Enhancement:**
```python
class LoadGuard:
    def analyze_pointer_range(self, ptr_value):
        """Analyze the range of addresses this pointer can access."""
        # Track through:
        # - IADD operations (offset accumulation)
        # - IMUL operations (index scaling)
        # - Phi-nodes (merge ranges)
        return (min_offset, max_offset, stride)
```

#### Task 2.6: Testing & Validation
**Time:** 8 hours

- [ ] Test on all `decompiler_source_tests/`
- [ ] Validate with recompilation
- [ ] Measure improvement in type inference
- [ ] Generate comparison report

**Deliverable:** Phase 2 complete with DCE, enhanced SSA, and improved LoadGuard

---

## Phase 3: Advanced Features (Weeks 25-28) - OPTIONAL

**Goal:** Add advanced features for completeness

**Estimated Effort:** 40-60 hours
**Expected Impact:** 5-10% improvement (diminishing returns)
**Priority:** ⭐ MEDIUM (only if time permits)

### Task 3.1: Advanced Cast Insertion
**File:** `vcdecomp/core/ir/cast_strategy.py`
**Time:** 16 hours

- [ ] Implement CastStrategy interface
- [ ] Add C-specific integer promotion rules
- [ ] Determine when casts are implicit vs. explicit
- [ ] Handle truncation vs. cast distinction

### Task 3.2: Expression Canonicalization
**File:** `vcdecomp/core/ir/canonical.py`
**Time:** 12 hours

- [ ] Implement term ordering (constants right)
- [ ] Implement operation ordering (associativity normalization)
- [ ] Enable better Common Subexpression Elimination (CSE)

### Task 3.3: Advanced Control Flow (if time permits)
**File:** `vcdecomp/core/ir/cfg_advanced.py`
**Time:** 20 hours

- [ ] Implement DAG-based CFG analysis
- [ ] Add spanning tree construction
- [ ] Add unstructured edge detection
- [ ] Likely goto inference

**Deliverable:** Phase 3 complete (optional, time permitting)

---

## Testing & Validation Strategy

### Continuous Testing (Throughout All Phases)

#### Unit Tests
**Target:** 95% code coverage for new modules

```bash
# Run tests for specific modules
py -3 -m pytest vcdecomp/tests/test_simplification_rules.py -v
py -3 -m pytest vcdecomp/tests/test_dce.py -v
py -3 -m pytest vcdecomp/tests/test_dominator_tree.py -v

# Run with coverage
py -3 -m pytest vcdecomp/tests/ --cov=vcdecomp.core.ir.rules
py -3 -m pytest vcdecomp/tests/ --cov=vcdecomp.core.ir.dce
py -3 -m pytest vcdecomp/tests/ --cov=vcdecomp.core.ir.dominator
```

#### Integration Tests
**Target:** All test scripts pass recompilation validation

```bash
# Test on known source files
for test in decompiler_source_tests/*/; do
    echo "Testing $test"
    py -3 -m vcdecomp structure --optimize-level 2 "$test"/*.scr > output.c
    py -3 -m vcdecomp validate "$test"/*.scr output.c
done
```

#### Regression Tests
**Target:** No degradation in existing functionality

```bash
# Save baseline before changes
py -3 -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --save-baseline

# After changes, check for regressions
py -3 -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --regression
```

#### Performance Tests
**Target:** No more than 10% slowdown in decompilation time

```bash
# Benchmark decompilation time
time py -3 -m vcdecomp structure test3/LEVEL.C > /dev/null

# Profile with optimization levels
py -3 -m cProfile -o profile.stats -m vcdecomp structure --optimize-level 0 script.scr
py -3 -m cProfile -o profile.stats -m vcdecomp structure --optimize-level 2 script.scr
```

---

## Success Metrics

### Quantitative Targets

| Metric | Baseline | Phase 1 Target | Phase 2 Target | Phase 3 Target |
|--------|----------|----------------|----------------|----------------|
| **Simplification rules** | 8 | 40-50 | 50 | 50+ |
| **Expression simplification** | ~60% | ~80% | ~85% | ~90% |
| **Dead code eliminated** | 0% | N/A | ~15-20% | ~20% |
| **Type inference accuracy** | ~85% | ~88% | ~92% | ~95% |
| **Phi-node quality** | Basic | Basic | Optimal | Optimal |
| **Convergence iterations** | 1 | 2-5 avg | 2-5 avg | 2-5 avg |
| **Decompilation time** | 1.0x | ≤1.2x | ≤1.3x | ≤1.4x |

### Qualitative Improvements

**Example transformation progression:**

**Original bytecode output:**
```c
int temp_0;
int temp_1;
int result;

temp_0 = x + 0;
temp_1 = temp_0 * 1;
result = temp_1;

if (result != result) {
    return 0;
}

if (result > 10) {
    temp_2 = result;
} else {
    temp_2 = result;
}

return temp_2;
```

**After Phase 1 (Rules + Fixed-Point):**
```c
int result;

result = x;  // Simplified: (x + 0) * 1 → x

// Dead comparison removed: result != result

if (result > 10) {
    return result;
} else {
    return result;
}
```

**After Phase 2 (DCE + Enhanced SSA):**
```c
return x;  // Fully simplified: no intermediate variables, dead code removed
```

---

## Risk Mitigation

### Risk 1: Complexity Explosion
**Risk:** Adding 40 rules makes the codebase hard to maintain
**Mitigation:**
- Clear modular structure (`rules/` package)
- Each rule is independent and well-tested
- Comprehensive documentation for each rule
- Rule registry for easy enable/disable

### Risk 2: Performance Regression
**Risk:** Fixed-point iteration slows down decompilation
**Mitigation:**
- Add optimization level flag (users can disable)
- Set reasonable max iteration limit (100)
- Profile and optimize hot paths
- Add early termination when no changes detected

### Risk 3: Correctness Issues
**Risk:** Rules introduce bugs or incorrect transformations
**Mitigation:**
- Extensive unit tests for each rule
- Validation with recompilation testing
- Regression test suite
- Conservative rule design (only apply when 100% safe)

### Risk 4: Integration Complexity
**Risk:** New features break existing functionality
**Mitigation:**
- Incremental integration (one phase at a time)
- Backward compatibility (optimization level 0 = old behavior)
- Extensive regression testing
- Feature flags for easy rollback

---

## Timeline & Milestones

### Milestone 1: Phase 1 Complete (Week 12)
**Deliverables:**
- ✅ 40 simplification rules implemented
- ✅ Fixed-point transformation engine working
- ✅ Integration with decompilation pipeline
- ✅ Command-line option for optimization levels
- ✅ Comprehensive tests with 95% coverage

**Success criteria:**
- All rules pass unit tests
- 20-30% improvement in expression simplification
- No regression in existing test cases
- Decompilation time ≤ 1.2x baseline

---

### Milestone 2: Phase 2 Complete (Week 24)
**Deliverables:**
- ✅ Dead code elimination implemented
- ✅ Augmented dominator tree constructed
- ✅ Enhanced SSA with proper phi placement
- ✅ Improved LoadGuard with range tracking
- ✅ Integration and validation

**Success criteria:**
- 15-20% dead code removed
- Better phi-node placement (fewer redundant phis)
- Improved type inference accuracy
- No regression in existing functionality

---

### Milestone 3: Phase 3 Complete (Week 28) - OPTIONAL
**Deliverables:**
- ✅ Advanced cast insertion
- ✅ Expression canonicalization
- ✅ Optional: DAG-based CFG analysis

**Success criteria:**
- 5-10% additional improvement
- Better cast handling
- Cleaner output

---

## Resource Requirements

### Developer Time
- **Phase 1:** 60-80 hours (1-2 developers, 6-8 weeks part-time)
- **Phase 2:** 60-80 hours (1-2 developers, 6-8 weeks part-time)
- **Phase 3:** 40-60 hours (1 developer, 4-6 weeks part-time) - OPTIONAL

**Total:** 160-220 hours (4-6 months part-time)

### Infrastructure
- ✅ Existing test scripts (`decompiler_source_tests/`)
- ✅ Existing validation system (`vcdecomp validate`)
- ✅ Existing CI/CD (if applicable)
- ⚠️ May need more test cases for edge scenarios

---

## Documentation Updates

### Required Documentation
- [ ] Update `docs/decompilation_guide.md` with new optimization levels
- [ ] Create `docs/simplification_rules.md` documenting all 40 rules
- [ ] Update `docs/structure_refactoring.md` with new architecture
- [ ] Update `CLAUDE.md` with new commands and flags
- [ ] Add examples to README showing improvements

### API Documentation
- [ ] Document SimplificationEngine API
- [ ] Document DominatorTree API
- [ ] Document DCE API
- [ ] Add usage examples for each optimization level

---

## Next Steps (Immediate Actions)

### Week 0: Preparation (Before Phase 1)

1. **Create branch for development:**
   ```bash
   git checkout -b enhancement/ghidra-inspired-improvements
   ```

2. **Set up development environment:**
   - Ensure all tests pass on baseline
   - Profile current performance
   - Generate baseline metrics

3. **Create tracking documents:**
   - Set up project board (GitHub Issues or similar)
   - Create task tracking spreadsheet
   - Set up weekly progress reports

4. **Review plan with team:**
   - Get feedback on priorities
   - Adjust timeline if needed
   - Assign responsibilities

5. **Start Week 1 tasks:**
   - Begin Task 1.1 (Framework Enhancement)
   - Begin Task 1.2 (Rules Package Structure)

---

## Conclusion

This implementation plan provides a structured, phased approach to significantly enhancing the VC-Script-Decompiler with Ghidra-inspired techniques. The focus is on **high-impact, feasible improvements** that will deliver measurable benefits to decompilation quality.

**Key principles:**
- ✅ **Incremental development** - Each phase delivers value independently
- ✅ **Extensive testing** - Unit, integration, regression, and performance tests
- ✅ **Backward compatibility** - Existing functionality preserved
- ✅ **Risk mitigation** - Clear mitigation strategies for each risk
- ✅ **Realistic timeline** - 3-6 months for meaningful improvements

The plan builds on our **existing Ghidra-inspired features** (type_algebra, load_guard) and focuses on the areas with the highest return on investment: **transformation rules and optimization passes**.

---

**Document Version:** 1.0
**Status:** ✅ Ready for Implementation
**Next Review:** After Phase 1 Milestone (Week 12)
