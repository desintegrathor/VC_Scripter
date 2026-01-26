# Rule Enablement Roadmap

**Date**: 2026-01-26
**Current Status**: 67/103 rules enabled (65% - up from 66 previously)
**Goal**: Enable remaining 36 disabled rules through infrastructure investments

---

## Progress Today

### ✅ Phase 1A Complete: Enabled 1 Quick Win Rule

**Rule enabled**: RuleCompareZero
- Pattern: `x == 0 → !x`, `x != 0 → x`
- Status: Fully implemented, now enabled
- Impact: Simplifies zero comparisons in boolean contexts
- File: `vcdecomp/core/ir/rules/comparison.py:334`

**Current totals**:
- Total rules: 103
- Enabled: 67 (65%)
- Disabled: 36 (35%)

---

## Infrastructure Investment Plan

The remaining 36 disabled rules require three major infrastructure investments:

### Priority 1: Use-Def Chains (🔴 High Impact - 3-5 days)

**What it unlocks**: 7 high-impact data flow optimization rules

**Rules enabled**:
1. **RuleCopyPropagation** - Replace uses of copies with originals
2. **RuleConstantPropagation** - Propagate constants through assignments
3. **RuleDeadValue** - Remove unused SSA values
4. **RuleUnusedResult** - Eliminate operations with unused results
5. **RuleForwardSubstitution** - Forward substitute simple expressions
6. **RuleSingleUseInline** - Inline single-use temporary values
7. **RuleValueNumbering** - Common subexpression elimination (partial)

**Implementation**:
```python
class UseDefChain:
    """Track definitions and uses of SSA values."""

    def __init__(self, ssa_func: SSAFunction):
        self.uses: Dict[SSAValue, List[SSAInstruction]] = {}
        self.defs: Dict[SSAValue, SSAInstruction] = {}
        self._build_chains(ssa_func)

    def get_uses(self, value: SSAValue) -> List[SSAInstruction]:
        """Return all instructions that use this value."""
        return self.uses.get(value, [])

    def get_def(self, value: SSAValue) -> Optional[SSAInstruction]:
        """Return instruction that defines this value."""
        return self.defs.get(value)

    def use_count(self, value: SSAValue) -> int:
        """Count number of uses of this value."""
        return len(self.get_uses(value))

    def is_single_use(self, value: SSAValue) -> bool:
        """Check if value is used exactly once."""
        return self.use_count(value) == 1
```

**Integration points**:
1. Build use-def chains in SimplificationEngine before applying rules
2. Pass chains to rules via context parameter or ssa_func attribute
3. Update chains after each transformation

**Files to modify**:
- `vcdecomp/core/ir/use_def.py` (NEW) - Use-def chain implementation
- `vcdecomp/core/ir/simplify_engine.py` - Integrate chains into engine
- `vcdecomp/core/ir/rules/dataflow.py` - Enable and implement 7 rules

**Estimated effort**: 3-5 days
**Impact**: HIGH - Enables most powerful data flow optimizations

---

### Priority 2: Intermediate Value Creation (🟡 Medium Impact - 4-6 hours)

**What it unlocks**: 4 rules that need to create new SSA values/instructions

**Rules enabled**:
1. **RuleNotDistribute** - De Morgan's laws for bitwise (`~(a&b) → ~a|~b`)
2. **RuleDemorganLaws** - De Morgan's laws for boolean (`!(a&&b) → !a||!b`)
3. **RuleIntLessEqual** - Normalize comparisons (`x<=y → !(x>y)`)
4. **RuleCollectTerms** - Canonicalize addition trees (partial)

**Current limitation**:
- Rules can only return ONE replacement instruction
- Some rules need to create intermediate instructions (e.g., NOT operations)
- Current architecture: `apply() -> Optional[SSAInstruction]`

**Solution options**:

**Option A: Multi-instruction return** (Recommended)
```python
def apply(self, inst: SSAInstruction, ssa_func: SSAFunction
         ) -> Union[SSAInstruction, List[SSAInstruction], None]:
    """
    Return single instruction, list of instructions, or None.

    When returning list:
    - First N-1 instructions are inserted before target
    - Last instruction replaces target
    """
    pass
```

**Option B: Instruction builder**
```python
class InstructionBuilder:
    def create_value(self, mnemonic: str, inputs: List[SSAValue]) -> SSAValue:
        """Create intermediate SSA value with instruction."""
        pass

def apply(self, inst: SSAInstruction, ssa_func: SSAFunction,
         builder: InstructionBuilder) -> Optional[SSAInstruction]:
    # Use builder to create intermediates
    pass
```

**Implementation steps**:
1. Modify SimplificationEngine._apply_rule_exhaustive() to handle list returns
2. Insert intermediate instructions into block before target
3. Update SSAValue producer links for new instructions
4. Test thoroughly to ensure SSA form is maintained

**Files to modify**:
- `vcdecomp/core/ir/simplify_engine.py` - Handle multi-instruction returns
- `vcdecomp/core/ir/rules/bitwise.py` - Implement RuleNotDistribute
- `vcdecomp/core/ir/rules/patterns.py` - Implement RuleDemorganLaws
- `vcdecomp/core/ir/rules/comparison.py` - Implement RuleIntLessEqual
- `vcdecomp/core/ir/rules/arithmetic.py` - Implement RuleCollectTerms

**Estimated effort**: 4-6 hours
**Impact**: MEDIUM - Improves boolean/comparison optimization

---

### Priority 3: CFG Integration (🔴 High Impact - 3-5 days)

**What it unlocks**: 13 rules requiring control flow analysis

**Rules enabled (8 loop rules)**:
1. **RuleInductionSimplify** - Simplify induction variables
2. **RuleLoopInvariantDetect** - Detect loop-invariant expressions
3. **RuleLoopStrength** - Strength reduction in loops
4. **RuleLoopUnswitch** - Hoist invariant conditions
5. **RuleCountedLoop** - Detect loop trip counts
6. **RuleLoopElimination** - Dead loop removal
7. **RuleLoopRotate** - Normalize loop forms
8. **RuleLoopFusion** - Merge adjacent loops

**Rules enabled (5 pattern rules)**:
9. **RuleAbsoluteValue** - Detect `(x<0)?-x:x → abs(x)`
10. **RuleMinMaxPatterns** - Detect `(a<b)?a:b → min(a,b)`
11. **RuleSignMagnitude** - Sign/magnitude conversions
12. **RuleSelectPattern** - Simplify `cond?a:a → a`
13. **RulePhiSimplify** - Simplify `phi(y,y) → y`
14. **RuleTrivialPhi** - Eliminate `phi(y) → y`

**Current situation**:
- CFG already exists in `vcdecomp/core/ir/cfg.py`
- SSA instructions not linked to CFG basic blocks
- Need loop detection and phi node handling

**Implementation**:
```python
class CFGIntegration:
    """Link SSA instructions with CFG basic blocks."""

    def __init__(self, cfg: CFG, ssa_func: SSAFunction):
        self.cfg = cfg
        self.ssa_func = ssa_func
        self._link_instructions_to_blocks()

    def get_block_for_inst(self, inst: SSAInstruction) -> BasicBlock:
        """Get CFG block containing instruction."""
        pass

    def get_phi_nodes(self, block: BasicBlock) -> List[SSAInstruction]:
        """Get phi nodes at start of block."""
        pass

    def is_loop_header(self, block: BasicBlock) -> bool:
        """Check if block is a natural loop header."""
        pass

    def get_loop_body(self, header: BasicBlock) -> Set[BasicBlock]:
        """Get all blocks in loop rooted at header."""
        pass
```

**Files to modify**:
- `vcdecomp/core/ir/cfg_integration.py` (NEW) - Link CFG with SSA
- `vcdecomp/core/ir/simplify_engine.py` - Pass CFG to rules
- `vcdecomp/core/ir/rules/loops.py` - Implement 8 loop rules
- `vcdecomp/core/ir/rules/patterns.py` - Implement 5 pattern rules
- `vcdecomp/core/ir/rules/dataflow.py` - Implement 2 phi rules

**Estimated effort**: 3-5 days
**Impact**: HIGH - Enables loop optimization and advanced patterns

---

### Priority 4: Type System (🟡 Medium Impact - 2-3 days)

**What it unlocks**: 7 rules requiring type information

**Rules enabled (4 type conversion rules)**:
1. **RulePromoteTypes** - C integer promotion detection
2. **RuleIntegralPromotion** - Optimize promoted arithmetic
3. **RuleSignExtendDetect** - Sign vs zero extension
4. **RuleTypeCoercion** - Mixed-type expression optimization

**Rules enabled (3 pointer rules)**:
5. **RulePtrNullCheck** - Optimize `ptr==0 → !ptr`
6. **RulePtrDiff** - Detect `(ptr1-ptr2)/4 → count`
7. **RuleStructOffset** - Detect `ptr+12 → ptr->field`

**Implementation**:
```python
class TypeInference:
    """Infer and track types for SSA values."""

    def __init__(self, ssa_func: SSAFunction):
        self.types: Dict[SSAValue, Type] = {}
        self._infer_types(ssa_func)

    def get_type(self, value: SSAValue) -> Optional[Type]:
        """Get inferred type for value."""
        return self.types.get(value)

    def is_pointer(self, value: SSAValue) -> bool:
        """Check if value is a pointer."""
        t = self.get_type(value)
        return t and isinstance(t, PointerType)

    def get_pointee_size(self, value: SSAValue) -> Optional[int]:
        """Get size of type pointed to."""
        pass

class Type:
    """Base type class."""
    pass

class IntType(Type):
    def __init__(self, size: int, signed: bool):
        self.size = size
        self.signed = signed

class PointerType(Type):
    def __init__(self, pointee: Type):
        self.pointee = pointee
```

**Type inference sources**:
1. Opcodes: IADD→int, FADD→float, DADD→double
2. Constants: 0→int, 0.0→float
3. External functions: SDK headers provide signatures
4. Struct definitions: Parse from SDK headers

**Files to modify**:
- `vcdecomp/core/ir/type_inference.py` (NEW) - Type system
- `vcdecomp/core/ir/simplify_engine.py` - Integrate types
- `vcdecomp/core/ir/rules/typeconv.py` - Implement 4 type rules
- `vcdecomp/core/ir/rules/pointer.py` - Implement 3 pointer rules

**Estimated effort**: 2-3 days
**Impact**: MEDIUM - Better type-aware optimizations

---

### Priority 5: Remaining Rules (🟢 Low Complexity - 2-4 hours)

**Rules that can be enabled with moderate effort**:

1. **RuleRangeCheck** (2-3 hours)
   - Pattern: `(x >= a) && (x <= b)` optimization
   - Needs: Boolean expression tree traversal
   - Can enable for simple cases

2. **RulePtrNullCheck** (1-2 hours)
   - Pattern: `ptr == 0 → !ptr`
   - Needs: Heuristic to identify pointers (or wait for type system)
   - Can use simple heuristic: values compared to 0 could be pointers

3. **RuleArrayBase** (30 minutes)
   - Pattern: `&arr[0] → arr`
   - Needs: Check if ADDR opcode exists in instruction set
   - If yes, trivial to implement

4. **RuleCopyChain** (2 minutes)
   - Already delegates to RuleRedundantCopy
   - Just needs matches() to not return False immediately

5. **RulePtrIndex** (skip - code emission)
   - Better handled at code emission stage, not IR level

---

## Recommended Execution Order

### Phase 1: Foundation (1 week)
1. ✅ **Day 1**: Enable RuleCompareZero (DONE)
2. **Days 2-4**: Implement Use-Def Chains (Priority 1)
   - Unlocks 7 high-impact data flow rules
   - Immediate optimization improvements
3. **Days 5-6**: Implement Intermediate Value Creation (Priority 2)
   - Unlocks 4 boolean/comparison rules
   - Moderate complexity, good ROI

**Result after Phase 1**: 78/103 rules enabled (76%)

### Phase 2: Advanced Optimizations (1 week)
1. **Days 7-9**: Implement CFG Integration (Priority 3)
   - Unlocks 13 loop and pattern rules
   - Most complex but highest impact
2. **Days 10-11**: Implement Type System (Priority 4)
   - Unlocks 7 type-aware rules
   - Moderate complexity

**Result after Phase 2**: 98/103 rules enabled (95%)

### Phase 3: Cleanup (1 day)
1. **Day 12**: Enable remaining rules (Priority 5)
   - RuleRangeCheck, RulePtrNullCheck, RuleArrayBase, RuleCopyChain
   - Minor improvements

**Result after Phase 3**: 102/103 rules enabled (99%)

---

## Alternative: Quick Wins Only (1-2 days)

If full infrastructure is too much work, focus on highest ROI:

1. ✅ **RuleCompareZero** (DONE)
2. **Use-Def Chains** (3-5 days) - Unlocks 7 rules
3. **Skip others** - Document as future work

**Result**: 74/103 enabled (72%), but highest-impact rules enabled

---

## Current Blockers Summary

| Infrastructure | Rules Blocked | Effort | Impact | Priority |
|---------------|---------------|--------|--------|----------|
| Use-Def Chains | 7 | 3-5 days | 🔴 HIGH | 1 |
| CFG Integration | 13 | 3-5 days | 🔴 HIGH | 2 |
| Intermediate Values | 4 | 4-6 hours | 🟡 MED | 3 |
| Type System | 7 | 2-3 days | 🟡 MED | 4 |
| Simple Impl | 5 | 2-4 hours | 🟢 LOW | 5 |

---

## Next Steps

**Immediate** (this session):
1. ✅ Enable RuleCompareZero
2. ✅ Document current state
3. Commit progress
4. Create detailed use-def chain implementation plan

**Near-term** (next session):
1. Implement use-def chains (highest ROI)
2. Enable 7 data flow rules
3. Test on real scripts
4. Measure impact

**Long-term** (follow-up work):
1. CFG integration (13 rules)
2. Intermediate value creation (4 rules)
3. Type system (7 rules)
4. Remaining minor rules (5 rules)

---

**Status**: 67/103 rules enabled (65%)
**Progress today**: +1 rule (RuleCompareZero)
**Path to 95%**: Implement use-def chains + CFG integration
**Estimated total effort**: 2-3 weeks for full enablement
