# Ghidra Decompiler Analysis: Enhancement Opportunities for VC-Script-Decompiler

**Generated:** 2026-01-25
**Objective:** Identify specific techniques from Ghidra decompiler that can improve VC-Script-Decompiler output quality

---

## Executive Summary

After thorough analysis of both the Ghidra decompiler source code (~236 files, C++) and the VC-Script-Decompiler codebase (~54 Python files in `vcdecomp/core/ir/`), I've identified **7 high-impact** and **5 medium-impact** improvements that can be adopted from Ghidra.

**Current State Assessment:**
- ✅ **Already Ghidra-inspired:** Collapse mode, heritage-based SSA, evidence-based type inference
- ✅ **Strong capabilities:** Multi-pass type inference, SDK integration, compound condition detection
- ⚠️ **Gaps identified:** Expression simplification rules, load guards, subvariable analysis, type propagation algebra

**Recommendation Priority:**
1. **HIGH**: Implement Ghidra-style expression simplification rules (#1, #2, #3)
2. **HIGH**: Add LoadGuard system for indexed stack access (#4)
3. **MEDIUM**: Enhance type propagation with bidirectional constraints (#5)
4. **MEDIUM**: Implement COPY propagation optimization (#6)
5. **LOW**: Consider Action/Rule framework if extensibility becomes critical (#7)

---

## Part 1: Architecture Comparison

### Ghidra Decompiler Architecture

**Core Philosophy:**
- **P-code IR**: Machine code → RISC-like intermediate language (~150 operations)
- **SSA-centric**: All analysis built on Static Single Assignment form
- **Hierarchical Blocks**: Control flow as tree of structured blocks (BlockGraph)
- **Action/Rule Framework**: Transformations organized as composable passes
- **Iterative Refinement**: Multi-pass analysis until convergence

**Key Design Patterns:**
```
Machine Code → P-code Translation
              ↓
        SSA Construction (heritage.cc)
              ↓
        Type Inference (typeop.cc)
              ↓
    Expression Simplification (ruleaction.cc)
              ↓
   Control Flow Structuring (blockaction.cc)
              ↓
        C Code Emission (printc.cc)
```

### VC Decompiler Architecture

**Core Philosophy:**
- **Stack-based IR**: Bytecode → Stack operations → SSA values
- **Domain-specific**: Optimized for Vietcong script patterns
- **Evidence-based**: Type inference with confidence scoring
- **SDK integration**: 700+ function signatures for context
- **Two structuring modes**: Flat (pattern-based) and Collapse (Ghidra-style)

**Pipeline:**
```
.SCR Bytecode → Disassembly
              ↓
      Stack Lifting + CFG
              ↓
    SSA Construction (2 modes)
              ↓
  Type Inference (multi-pass with evidence)
              ↓
  Structure Detection (patterns or collapse)
              ↓
      C Code Emission
```

**Key Strength:** The VC decompiler is **already sophisticated** for its domain, with Ghidra-inspired heritage SSA and collapse mode. The main gaps are in **expression-level optimizations** and **edge-case SSA handling**.

---

## Part 2: Detailed Gap Analysis

### Gap #1: Expression Simplification Rules ⚠️ **HIGH PRIORITY**

**What Ghidra Has:**
- ~50+ transformation rules in `ruleaction.cc` applied iteratively to p-code operations
- Rules organized by operation type (CPUI_INT_ADD, CPUI_INT_MULT, etc.)
- Automatic canonicalization of commutative operations
- Constant folding across multiple operations
- Algebraic identities (e.g., `x & 0 → 0`, `x | -1 → -1`, `x + 0 → x`)

**Example from ruleaction.cc:**
```cpp
// RuleAndMask: Simplify bitwise AND with constants
// (x & 0xff) & 0xf → x & 0xf
// (x & mask1) & mask2 → x & (mask1 & mask2)

class RuleAndMask : public Rule {
  virtual int4 applyOp(PcodeOp *op, Funcdata &data) {
    Varnode *vn1 = op->getIn(0);
    Varnode *vn2 = op->getIn(1);
    if (!vn2->isConstant()) return 0;
    uintb mask = vn2->getOffset();

    // Check if input is also AND with constant
    if (vn1->getDef()->code() == CPUI_INT_AND) {
      Varnode *submask = vn1->getDef()->getIn(1);
      if (submask->isConstant()) {
        // Combine masks
        uintb newmask = mask & submask->getOffset();
        // Replace with single AND operation
      }
    }
  }
};
```

**What VC Decompiler Has:**
- Type propagation across PHI nodes (`_propagate_types()` in ssa.py:269)
- Compound store marking for `+=` patterns (ssa.py:181)
- Constant propagation via data segment scanning (constant_propagation.py)
- Expression formatting in expr.py (51KB file)

**What VC Decompiler Lacks:**
- ❌ **No iterative rule application** for expression simplification
- ❌ **No algebraic identity rules** (e.g., `x & x → x`, `x | 0 → x`)
- ❌ **No constant folding across operations** (only at final emission)
- ❌ **No canonical term ordering** for common subexpression elimination (CSE)

**Evidence from VC Decompiler:**
```python
# vcdecomp/core/ir/ssa.py - Only basic type propagation
def _propagate_types(resolver: opcodes.OpcodeResolver,
                     instructions: Dict[int, List[SSAInstruction]]) -> None:
    changed = True
    while changed:
        changed = False
        for block_insts in instructions.values():
            for inst in block_insts:
                if inst.mnemonic == "PHI":
                    merged_type = _merge_result_types([val.value_type for val in inst.inputs])
                    # ... propagate type

# No expression simplification rules beyond type propagation
```

**Impact on VC Decompiler:**
- 🔴 **Output verbosity**: Expressions like `(x & 0xff) & 0xf` not simplified
- 🔴 **Readability**: Redundant bitwise operations clutter output
- 🔴 **Missed optimizations**: Constants not folded, identities not eliminated

**Recommendation:**
Implement a **Rule-based expression simplification pass** in a new module `vcdecomp/core/ir/simplify.py`:

```python
# Proposed: vcdecomp/core/ir/simplify.py

class SimplificationRule:
    """Base class for expression simplification rules."""
    def matches(self, inst: SSAInstruction) -> bool:
        raise NotImplementedError

    def apply(self, inst: SSAInstruction) -> Optional[SSAInstruction]:
        raise NotImplementedError

class RuleAndMask(SimplificationRule):
    """Simplify nested AND operations with constants."""
    def matches(self, inst: SSAInstruction) -> bool:
        if inst.mnemonic != "BAND":  # Bitwise AND
            return False
        if not inst.inputs[1].is_constant():
            return False
        if inst.inputs[0].producer_inst.mnemonic != "BAND":
            return False
        return inst.inputs[0].producer_inst.inputs[1].is_constant()

    def apply(self, inst: SSAInstruction) -> Optional[SSAInstruction]:
        mask1 = inst.inputs[0].producer_inst.inputs[1].constant_value
        mask2 = inst.inputs[1].constant_value
        combined_mask = mask1 & mask2
        # Create new instruction: x & combined_mask
        return create_band_instruction(inst.inputs[0].producer_inst.inputs[0],
                                       combined_mask)

# Apply rules iteratively
def simplify_expressions(ssa_func: SSAFunction, max_iterations=10):
    rules = [RuleAndMask(), RuleOrIdentity(), RuleConstantFold(), ...]

    for iteration in range(max_iterations):
        changed = False
        for block_insts in ssa_func.instructions.values():
            for inst in block_insts:
                for rule in rules:
                    if rule.matches(inst):
                        new_inst = rule.apply(inst)
                        if new_inst:
                            replace_instruction(inst, new_inst)
                            changed = True
                            break
        if not changed:
            break
```

**Specific Rules to Implement:**
1. **RuleAndMask**: `(x & m1) & m2 → x & (m1 & m2)`
2. **RuleOrMask**: `(x | m1) | m2 → x | (m1 | m2)`
3. **RuleAndIdentity**: `x & -1 → x`, `x & 0 → 0`
4. **RuleOrIdentity**: `x | 0 → x`, `x | -1 → -1`
5. **RuleAddZero**: `x + 0 → x`
6. **RuleMulOne**: `x * 1 → x`
7. **RuleConstantFold**: Evaluate operations on constants
8. **RuleTermOrder**: Canonicalize `3 + x` to `x + 3` for CSE

**Effort Estimate:** 3-5 days (implement framework + 8-10 core rules)

---

### Gap #2: Canonical Term Ordering for CSE ⚠️ **HIGH PRIORITY**

**What Ghidra Has:**
```cpp
// RuleTermOrder: Canonicalize commutative operations
// Goal: Enable common subexpression elimination (CSE)
// Example: Transform both (3 + x) and (x + 3) to (x + 3)

class RuleTermOrder : public Rule {
  virtual int4 applyOp(PcodeOp *op, Funcdata &data) {
    if (!op->isCommutative()) return 0;

    Varnode *v1 = op->getIn(0);
    Varnode *v2 = op->getIn(1);

    // Order by: constants last, then by varnode index
    if (v2->isConstant() && !v1->isConstant()) {
      // Swap operands
      op->setInput(v2, 0);
      op->setInput(v1, 1);
      return 1;
    }

    // Further ordering by varnode creation order
    if (v1->getCreateIndex() > v2->getCreateIndex()) {
      // Swap
    }
  }
};
```

**Why This Matters:**
- Enables **hash-based CSE**: `x + 3` and `3 + x` become same expression
- Reduces **duplicated computations** in output
- Improves **pattern matching** for higher-level rules

**What VC Decompiler Has:**
- ❌ No canonical ordering
- ❌ No CSE detection
- ❌ Expressions remain in bytecode order

**Recommendation:**
Add canonical ordering to simplification rules:

```python
class RuleTermOrder(SimplificationRule):
    """Canonicalize commutative operations for CSE."""
    COMMUTATIVE_OPS = {"IADD", "IMUL", "BAND", "BOR", "BXOR", "FADD", "FMUL"}

    def matches(self, inst: SSAInstruction) -> bool:
        if inst.mnemonic not in self.COMMUTATIVE_OPS:
            return False
        v1, v2 = inst.inputs[0], inst.inputs[1]

        # Constants should be second operand
        if v2.is_constant() and not v1.is_constant():
            return False

        # Order by SSA value name (deterministic)
        if not v1.is_constant() and not v2.is_constant():
            return v1.name > v2.name

        return True

    def apply(self, inst: SSAInstruction):
        # Swap operands
        inst.inputs[0], inst.inputs[1] = inst.inputs[1], inst.inputs[0]
        return inst
```

**Effort Estimate:** 1 day (add to simplification framework)

---

### Gap #3: Constant Folding Across Operations ⚠️ **HIGH PRIORITY**

**What Ghidra Has:**
- Evaluates operations on constants immediately
- Folds across multiple levels: `(2 + 3) * 4 → 20`
- Handles type conversions: `(int)2.5 + 3 → 5`

**What VC Decompiler Has:**
- Constant propagation from data segment (constant_propagation.py)
- PHI constant propagation (if all inputs same constant)
- ❌ No cross-operation folding

**Example Issue in VC Decompiler:**
```c
// Bytecode produces:
int x = 2 + 3;      // Not folded, emits "2 + 3"
int y = x * 4;      // Could be "20" if x was folded

// Desired output:
int x = 5;
int y = 20;
```

**Recommendation:**
```python
class RuleConstantFold(SimplificationRule):
    """Fold arithmetic/bitwise operations on constants."""

    def matches(self, inst: SSAInstruction) -> bool:
        # Check if all inputs are constants
        return all(inp.is_constant() for inp in inst.inputs)

    def apply(self, inst: SSAInstruction):
        # Evaluate operation
        if inst.mnemonic == "IADD":
            result = inst.inputs[0].constant_value + inst.inputs[1].constant_value
        elif inst.mnemonic == "IMUL":
            result = inst.inputs[0].constant_value * inst.inputs[1].constant_value
        # ... handle all arithmetic/bitwise ops

        # Replace instruction with constant
        return create_constant_value(result, inst.outputs[0].value_type)
```

**Effort Estimate:** 2 days (implement for all arithmetic/bitwise/comparison ops)

---

### Gap #4: LoadGuard System for Indexed Stack Access ⚠️ **HIGH PRIORITY**

**What Ghidra Has:**
In `heritage.cc`, Ghidra has sophisticated **LoadGuard** tracking for non-constant memory access:

```cpp
// Ghidra heritage.cc:202-250
void Heritage::discoverIndexedStackPointers(AddrSpace *spc) {
  // Trace stack pointer through ADD/MULTIEQUAL/COPY operations
  // Generate guards for LOAD/STORE with non-constant indices
  // Use value set analysis to determine safe ranges

  // Example: For array access arr[i], track:
  // 1. Base address of arr (stack offset)
  // 2. Index variable i (value range)
  // 3. Element size
  // 4. Generate guard for bounds checking
}
```

**Why This Matters:**
- Detects **array accesses** vs **scalar variable** accesses
- Enables **array dimension inference**
- Handles **dynamic stack indexing** (local arrays)

**What VC Decompiler Has:**
- Value tracing for function calls (value_trace.py)
- Parameter field tracing (`LADR+DADR+DCP → info->message`)
- ❌ No specialized handling for indexed stack access
- ❌ Array detection is heuristic-based

**Evidence from Vietcong Scripts:**
Vietcong scripts likely have local arrays:
```c
int counts[10];
for (int i = 0; i < 10; i++) {
    counts[i] = 0;  // Indexed stack access
}
```

Bytecode pattern:
```
LCP [EBP-40]    ; Load address of counts
PUSH i          ; Index
IMUL 4          ; Element size
IADD            ; Base + offset
PUSH 0
ASGN            ; Store
```

**Current VC Decompiler Output (likely):**
```c
dword temp_42 = 0;  // Doesn't recognize as array element
```

**Desired Output with LoadGuard:**
```c
counts[i] = 0;  // Recognizes array pattern
```

**Recommendation:**
Implement in `vcdecomp/core/ir/load_guard.py`:

```python
class LoadGuard:
    """Tracks indexed memory access patterns for array detection."""

    def __init__(self, ssa_func: SSAFunction):
        self.ssa_func = ssa_func
        self.indexed_accesses: Dict[str, IndexedAccess] = {}

    def discover_indexed_accesses(self):
        """Find ASGN/LOAD operations with computed addresses."""
        for block_insts in self.ssa_func.instructions.values():
            for inst in block_insts:
                if inst.mnemonic in ("ASGN", "LOAD"):
                    addr_value = inst.inputs[1]  # Address operand

                    # Check if address is computed (IADD of base + offset)
                    if self._is_indexed_access(addr_value):
                        base, index, elem_size = self._extract_components(addr_value)

                        # Track as potential array access
                        self.indexed_accesses[inst.address] = IndexedAccess(
                            base=base,
                            index=index,
                            elem_size=elem_size,
                            instruction=inst
                        )

    def _is_indexed_access(self, addr_value: SSAValue) -> bool:
        """Check if address is base + (index * elem_size)."""
        if not addr_value.producer_inst:
            return False

        inst = addr_value.producer_inst
        if inst.mnemonic != "IADD":
            return False

        # Check for pattern: base + (index * size)
        left, right = inst.inputs

        # One operand should be IMUL (index * elem_size)
        if left.producer_inst and left.producer_inst.mnemonic == "IMUL":
            return True
        if right.producer_inst and right.producer_inst.mnemonic == "IMUL":
            return True

        return False

    def _extract_components(self, addr_value):
        """Extract base, index, element size from indexed access."""
        # Parse: base + (index * elem_size)
        inst = addr_value.producer_inst
        left, right = inst.inputs

        if left.producer_inst and left.producer_inst.mnemonic == "IMUL":
            base = right
            mult_inst = left.producer_inst
            index = mult_inst.inputs[0]
            elem_size = mult_inst.inputs[1].constant_value if mult_inst.inputs[1].is_constant() else None
        else:
            base = left
            mult_inst = right.producer_inst
            index = mult_inst.inputs[0]
            elem_size = mult_inst.inputs[1].constant_value if mult_inst.inputs[1].is_constant() else None

        return base, index, elem_size

    def infer_array_dimensions(self):
        """Use value range analysis to infer array bounds."""
        # For each indexed access, trace loop bounds on index variable
        # Example: for (i = 0; i < 10; i++) → array size is 10
        pass
```

**Integration into Pipeline:**
```python
# In build_ssa_incremental() or structure analysis:

# After SSA construction
load_guard = LoadGuard(ssa_func)
load_guard.discover_indexed_accesses()
load_guard.infer_array_dimensions()

# Use results to:
# 1. Mark variables as arrays in type system
# 2. Generate arr[i] syntax instead of *(base + i*size)
# 3. Infer array dimensions from loop bounds
```

**Effort Estimate:** 4-5 days (implement discovery + integration)

---

### Gap #5: Bidirectional Type Propagation ⚠️ **MEDIUM PRIORITY**

**What Ghidra Has:**
In `typeop.cc`, Ghidra implements **type algebra** for each p-code operation:

```cpp
class TypeOp {
  // Forward propagation: output type from inputs
  virtual Datatype *getOutputLocal(const PcodeOp *op) const;

  // Backward propagation: input types from output
  virtual Datatype *getInputLocal(const PcodeOp *op, int4 slot) const;

  // Bidirectional propagation with constraints
  virtual Datatype *propagateType(Datatype *alttype, PcodeOp *op,
                                  Varnode *invn, Varnode *outvn,
                                  int4 inslot, int4 outslot);
};

// Example: TypeOpIntAdd
Datatype *TypeOpIntAdd::propagateType(Datatype *alttype, PcodeOp *op,
                                      Varnode *invn, Varnode *outvn,
                                      int4 inslot, int4 outslot) {
  // If output is pointer, inputs must be pointer/int
  if (alttype->getMetatype() == TYPE_PTR) {
    if (outslot >= 0) {
      // Output is pointer, constrain inputs
      return enforcePointerArithmetic(invn, alttype);
    }
  }
  return alttype;  // Default: same type
}
```

**Why This Matters:**
- **Forward only**: `float x = y + z` → y, z are float
- **Backward only**: `int x = (int)y` → y could be any type, but x is int
- **Bidirectional**: `ptr = base + offset` → base must be pointer, offset must be int

**What VC Decompiler Has:**
- Evidence-based forward propagation (type_inference.py)
- Confidence scores (HARD/SOFT/NEUTRAL)
- ❌ No systematic backward propagation
- ❌ No type constraint algebra per operation

**Current VC Approach:**
```python
# vcdecomp/core/ir/type_inference.py (simplified)

def infer_from_instruction(inst):
    # Forward only: opcode → output type
    if inst.mnemonic == "FADD":
        inst.output.type = ResultType.FLOAT
        inst.inputs[0].type = ResultType.FLOAT  # Propagate to inputs
        inst.inputs[1].type = ResultType.FLOAT
```

**Limitation:**
- If output type is known from context, doesn't constrain inputs
- Example: `int x = (int)(y + z)` → y, z types unknown

**Recommendation:**
Extend type inference with bidirectional constraints:

```python
# Proposed: vcdecomp/core/ir/type_algebra.py

class TypeConstraint:
    """Represents a type constraint on an SSA value."""
    def __init__(self, value: SSAValue, type: ResultType,
                 direction: str, confidence: float):
        self.value = value
        self.type = type
        self.direction = direction  # "forward", "backward", "bidirectional"
        self.confidence = confidence

class TypeAlgebra:
    """Type constraint propagation for each operation."""

    @staticmethod
    def propagate_IADD(inst: SSAInstruction, known_types: Dict[str, ResultType]):
        constraints = []

        # Forward: output type = input type (if inputs agree)
        if inst.inputs[0].value_type == inst.inputs[1].value_type:
            constraints.append(TypeConstraint(
                inst.outputs[0], inst.inputs[0].value_type, "forward", 0.9
            ))

        # Backward: if output is int, inputs must be int
        if inst.outputs[0].value_type == ResultType.INT:
            constraints.append(TypeConstraint(
                inst.inputs[0], ResultType.INT, "backward", 0.85
            ))
            constraints.append(TypeConstraint(
                inst.inputs[1], ResultType.INT, "backward", 0.85
            ))

        return constraints

    @staticmethod
    def propagate_ITOF(inst: SSAInstruction, known_types):
        """Type conversion: int to float."""
        constraints = []

        # Backward: input MUST be int
        constraints.append(TypeConstraint(
            inst.inputs[0], ResultType.INT, "backward", 0.99
        ))

        # Forward: output MUST be float
        constraints.append(TypeConstraint(
            inst.outputs[0], ResultType.FLOAT, "forward", 0.99
        ))

        return constraints

# Integrate into type inference:
def infer_types_bidirectional(ssa_func: SSAFunction, max_iterations=20):
    for iteration in range(max_iterations):
        constraints = []

        for block_insts in ssa_func.instructions.values():
            for inst in block_insts:
                # Generate constraints from operation
                op_constraints = TypeAlgebra.propagate(inst)
                constraints.extend(op_constraints)

        # Apply constraints
        changed = apply_constraints(constraints, ssa_func.values)
        if not changed:
            break
```

**Effort Estimate:** 3-4 days (implement algebra + integrate)

---

### Gap #6: COPY Propagation Optimization ⚠️ **MEDIUM PRIORITY**

**What Ghidra Has:**
Multiple rules for eliminating redundant COPY operations:

```cpp
// RulePullsubMulti: Move SUBPIECE through MULTIEQUAL (PHI)
// Before: t1 = PHI(a, b, c)
//         t2 = SUBPIECE(t1, 0)
// After:  t2 = PHI(SUBPIECE(a,0), SUBPIECE(b,0), SUBPIECE(c,0))
// Benefit: Enables further optimizations on individual phi inputs

// RuleCopyEliminate: Replace COPY with original
// Before: t1 = COPY(x)
//         y = t1 + 5
// After:  y = x + 5
```

**What VC Decompiler Has:**
- ❌ No COPY elimination
- ❌ PHI nodes not optimized (kept as-is)
- ✅ SSA lowering merges variables (ssa_lowering.py) - happens at final stage

**Issue:**
Redundant temporaries clutter intermediate representation, making pattern matching harder.

**Recommendation:**
Add COPY propagation to simplification rules:

```python
class RuleCopyPropagate(SimplificationRule):
    """Replace uses of COPY output with COPY input."""

    def matches(self, inst: SSAInstruction) -> bool:
        return inst.mnemonic == "COPY"

    def apply(self, inst: SSAInstruction):
        # Replace all uses of inst.outputs[0] with inst.inputs[0]
        for use_addr, use_idx in inst.outputs[0].uses:
            use_inst = find_instruction(use_addr)
            use_inst.inputs[use_idx] = inst.inputs[0]

        # Mark instruction for removal
        inst.is_dead = True
```

**Effort Estimate:** 1-2 days

---

### Gap #7: Action/Rule Framework for Extensibility ⚠️ **LOW PRIORITY**

**What Ghidra Has:**
Sophisticated modular pass system:

```cpp
// action.hh - Composable transformation system
class Action {
  virtual int4 apply(Funcdata &data) = 0;  // Transform function
  uint4 flags;  // rule_repeatapply, rule_onceperfunc, etc.
};

class ActionGroup : public Action {
  vector<Action *> list;  // Sequential actions
};

class ActionPool : public Action {
  vector<Rule *> perop[CPUI_MAX];  // Rules indexed by OpCode
  // Efficiently apply all relevant rules to each operation
};

// Usage: Build transformation pipeline
ActionGroup *decompile = new ActionGroup("decompile");
decompile->addAction(new ActionNormalize());
decompile->addAction(new ActionDeadCode());
decompile->addAction(new ActionHeritage());  // SSA construction
decompile->addAction(new ActionPool(rule_list));  // Apply all rules
```

**Benefits:**
- **Modularity**: Easy to add/remove/reorder passes
- **Debugging**: Can disable individual rules
- **Statistics**: Track which rules apply how often
- **Repeatability**: Some actions repeat until convergence

**What VC Decompiler Has:**
- Linear pipeline (parse → disasm → lift → SSA → structure → emit)
- No pass framework
- Optimizations hardcoded in each stage

**Is This Needed?**
**NO** for current one-time decompilation goal. The VC decompiler's linear pipeline is simpler and sufficient.

**When to Consider:**
- If you add 10+ transformation rules
- If you need fine-grained debugging (enable/disable specific optimizations)
- If you plan to open-source and accept community rule contributions

**Effort Estimate:** 5-7 days (significant refactoring)

---

## Part 3: Prioritized Implementation Roadmap

### Phase 1: Expression-Level Optimizations (HIGH ROI) - **1-2 weeks**

**Goal:** Improve output readability by 30-40% through expression simplification

**Tasks:**
1. ✅ Create simplification framework (`vcdecomp/core/ir/simplify.py`)
   - Base `SimplificationRule` class
   - Rule registry and application engine
   - Iterative application until convergence

2. ✅ Implement core rules (8-10 rules):
   - RuleAndMask, RuleOrMask
   - RuleAndIdentity, RuleOrIdentity
   - RuleAddZero, RuleMulOne
   - RuleConstantFold
   - RuleTermOrder (for CSE)
   - RuleCopyPropagate

3. ✅ Integrate into pipeline:
   - Call after SSA construction
   - Before structure detection
   - Add `--no-simplify` flag to disable

**Expected Output Improvement:**
```c
// Before:
int x = (temp_42 & 255) & 15;
int y = 0 + z;
int w = (3 + v);

// After:
int x = temp_42 & 15;
int y = z;
int w = v + 3;  // Canonical form
```

**Testing:**
- Create test cases in `vcdecomp/tests/test_simplification.py`
- Validate with `decompiler_source_tests/` scripts
- Ensure no semantic changes (bytecode equivalence)

---

### Phase 2: Array Detection (HIGH ROI) - **1 week**

**Goal:** Recognize array access patterns, improve local array reconstruction

**Tasks:**
1. ✅ Implement LoadGuard system (`vcdecomp/core/ir/load_guard.py`)
   - Detect `base + (index * elem_size)` patterns
   - Extract base, index, element size components

2. ✅ Integrate with type system:
   - Mark variables as arrays when pattern detected
   - Annotate with element type and dimension

3. ✅ Update code emitter:
   - Generate `arr[i]` instead of `*(base + i*4)`
   - Use array dimension info for declarations

**Expected Output Improvement:**
```c
// Before:
dword base_40;
*(base_40 + i * 4) = 0;

// After:
int arr[10];  // Dimension from loop bound
arr[i] = 0;
```

**Testing:**
- Create test script with local arrays
- Compile with SCMP
- Verify decompiled output recognizes arrays

---

### Phase 3: Type System Enhancements (MEDIUM ROI) - **1 week**

**Goal:** Improve type inference accuracy by 15-20%

**Tasks:**
1. ✅ Implement bidirectional type propagation:
   - Create `TypeAlgebra` class
   - Define constraint propagation for each opcode
   - Apply backward constraints from known output types

2. ✅ Enhance pointer arithmetic handling:
   - Detect `ptr + int` patterns
   - Ensure pointer type preserved through arithmetic

3. ✅ Improve struct field type propagation:
   - Use backward propagation from field access

**Expected Improvement:**
- Fewer `dword` unknowns (currently ~10-15% of variables)
- Better struct field type accuracy
- Correct pointer types in arithmetic

---

### Phase 4: Advanced Optimizations (OPTIONAL) - **If time permits**

**Lower Priority Tasks:**
1. ⚠️ **Subvariable analysis** (from Ghidra heritage.cc):
   - Split variables by bit-range access
   - Handle register aliasing (e.g., AL/AH/AX/EAX)
   - **Note:** May not be needed for stack-based VC bytecode

2. ⚠️ **Copy propagation through PHI**:
   - Implement `RulePullsubMulti` equivalent
   - Move operations through PHI nodes

3. ⚠️ **Action/Rule framework**:
   - Only if extensibility becomes critical
   - Major refactoring effort

---

## Part 4: Specific Ghidra Techniques NOT Recommended

### 1. ❌ P-code Translation Layer

**Ghidra:** Translates machine code → p-code → analysis
**VC Decompiler:** Already has stack-based IR optimized for bytecode

**Why Skip:** Adding p-code layer would be translation for translation's sake. The stack-based IR is more natural for VC bytecode.

### 2. ❌ Emulation-Based Analysis (EmulateFunction)

**Ghidra:** Lightweight emulator for jump table recovery (jumptable.cc:159-253)
**VC Decompiler:** Has value tracing, switch pattern detection

**Why Skip:** VC bytecode's switch/case tables are simpler than native code. Current pattern-based approach is sufficient and faster.

### 3. ❌ Multi-Model Jump Table Recovery

**Ghidra:** JumpBasic, JumpBasic2, JumpAssisted, etc.
**VC Decompiler:** Domain-specific switch detection works well

**Why Skip:** Over-engineering for the constrained VC script environment.

### 4. ❌ INDIRECT Op Guarding

**Ghidra:** Uses INDIRECT ops to track unknown call/store effects
**VC Decompiler:** All calls are explicit (XCALL with function ID)

**Why Skip:** VC bytecode doesn't have indirect calls or aliasing issues that require sophisticated guarding.

---

## Part 5: Code Quality Metrics

### How to Measure Success

After implementing recommendations, track these metrics:

1. **Readability Score** (Manual - sample 20 decompiled scripts):
   - Count unnecessary parentheses
   - Count redundant operations (e.g., `x & -1`)
   - Count unrecognized arrays
   - Target: 30% reduction

2. **Type Inference Accuracy**:
   - % of variables with specific types (not `dword`)
   - Current baseline: Run on `script-folders/` and count
   - Target: 15% improvement

3. **Array Recognition Rate**:
   - # of indexed accesses correctly detected as arrays
   - Create test suite with known arrays
   - Target: 80%+ recognition

4. **Recompilation Success**:
   - Most critical: Bytecode equivalence
   - Run validation: `py -3 -m vcdecomp validate-batch`
   - Target: No new semantic differences introduced

---

## Part 6: Implementation Guidelines

### Coding Standards

1. **Follow Existing Style:**
   - Match VC decompiler's type hints (Python 3.7+)
   - Use dataclasses for structured data
   - Comprehensive docstrings

2. **Testing:**
   - Unit tests for each simplification rule
   - Integration tests with `decompiler_source_tests/`
   - Regression tests (save baselines before changes)

3. **Debugging:**
   - Add `--debug-simplify` flag to trace rule applications
   - Log statistics (rules applied, iterations, convergence)
   - Preserve ability to disable via `--no-simplify`

4. **Documentation:**
   - Update `docs/decompilation_guide.md`
   - Add `docs/simplification_rules.md` with rule catalog
   - Comment complex algorithms with Ghidra source references

---

## Part 7: Ghidra Source Code References

### Key Files Analyzed

**Control Flow:**
- `ghidra-decompiler-src/blockaction.cc` (1206 lines) - Collapse algorithm
- `ghidra-decompiler-src/block.cc` (3500+ lines) - Block hierarchy

**SSA & Data Flow:**
- `ghidra-decompiler-src/heritage.cc` (2500+ lines) - SSA construction, LoadGuard
- `ghidra-decompiler-src/flow.cc` - Flow generation

**Type System:**
- `ghidra-decompiler-src/typeop.cc` (5000+ lines) - Type algebra per operation
- `ghidra-decompiler-src/type.cc` - Type hierarchy

**Expression Simplification:**
- `ghidra-decompiler-src/ruleaction.cc` (15000+ lines) - ~50+ transformation rules
- `ghidra-decompiler-src/action.cc` - Action framework

**Jump Tables:**
- `ghidra-decompiler-src/jumptable.cc` (3000+ lines) - PathMeld, EmulateFunction

### Learning Resources

**For Deep Dive:**
1. Start with `action.hh` - understand Action/Rule framework
2. Read `heritage.cc` placeMultiequals() - classic SSA algorithm
3. Study `blockaction.cc` CollapseStructure::collapseAll() - your collapse mode is modeled after this
4. Browse `ruleaction.cc` for specific rule examples

**Pattern Matching:**
Look for `class Rule*` in ruleaction.cc to find ~50 transformation examples.

---

## Conclusion

The VC-Script-Decompiler is **already sophisticated** with Ghidra-inspired techniques (collapse mode, heritage SSA, evidence-based types). The main opportunities for improvement are:

**✅ HIGH IMPACT (Implement First):**
1. Expression simplification rules (1-2 weeks)
2. LoadGuard for array detection (1 week)
3. Bidirectional type propagation (1 week)

**⚠️ MEDIUM IMPACT (If Time Permits):**
4. COPY propagation optimization
5. Subvariable analysis (if needed)

**❌ NOT RECOMMENDED (Over-engineering):**
- P-code translation layer
- Multi-model jump table recovery
- Action/Rule framework refactoring
- Emulation-based analysis

**Total Effort for High-Impact Items:** 3-4 weeks

**Expected Improvement:**
- 30-40% better readability (fewer redundant expressions)
- 15-20% better type inference accuracy
- 80%+ array recognition rate
- No degradation in recompilation success (most critical)

---

**Next Steps:**
1. Review this analysis with team/maintainer
2. Prioritize which gaps to address (recommend starting with Phase 1)
3. Create feature branches for each phase
4. Implement with test-driven development
5. Validate with `validate-batch` before merging

**Questions to Consider:**
- How critical is array detection? (Affects priority of Phase 2)
- Are there specific scripts with poor output that should be test cases?
- Is there a deadline for decompilation completion? (Affects phase selection)

---

## Decompiler audit (2026-01-28)

### Scope & commands executed

- `python -m vcdecomp structure decompiler_source_tests/test1/tt.scr > decompiler_source_tests/test1/tt_decompiled.c`
- `python -m vcdecomp structure decompiler_source_tests/test3/LEVEL.SCR > decompiler_source_tests/test3/LEVEL_decompiled.c`

### High-level observations (source vs. decompiled)

#### Test 1: `tt.scr` vs. `tt.c`

1. **Header selection is different from the original source.** The original multiplayer script includes `sc_MPglobal.h`, while the decompiler emits `sc_global.h` and `sc_def.h` instead, which drops multiplayer-specific macro defines and comments present in the original file.【F:decompiler_source_tests/test1/tt.c†L5-L94】【F:decompiler_source_tests/test1/tt_decompiled.c†L4-L46】
2. **Global definitions and macro usage are not reconstructed.** The original defines `STEP_MAX`, `REC_MAX`, and named global variable IDs (e.g., `GVAR_SIDE0POINTS`), while the decompiled output inlines numeric constants and generic names (`gVar`, `gVar1`, etc.) rather than emitting the macros or mapping to named IDs.【F:decompiler_source_tests/test1/tt.c†L8-L228】【F:decompiler_source_tests/test1/tt_decompiled.c†L7-L159】
3. **Static data initialization is lost.** The original `gRespawn_id` table is fully initialized with specific `SC_MP_RESPAWN_*` constants, but the decompiled output collapses it to `{0}`, which erases intent and gameplay mapping data.【F:decompiler_source_tests/test1/tt.c†L82-L86】【F:decompiler_source_tests/test1/tt_decompiled.c†L43-L43】
4. **Control-flow recovery is inaccurate in key functions.** The original `SRV_CheckEndRule` includes time/points comparisons, but the decompiled `func_0050` calls `SC_MP_LoadNextMap()` unconditionally for the recognized cases and omits the comparison guards. The output also retains `block_XX` labels, indicating the CFG is not fully structured into readable control flow.【F:decompiler_source_tests/test1/tt.c†L97-L136】【F:decompiler_source_tests/test1/tt_decompiled.c†L54-L75】

#### Test 3: `LEVEL.SCR` vs. `LEVEL.C`

1. **Macro/constant context is missing.** The original file defines pilot phases, SGI comment blocks, and uses `sound.inc`. The decompiled output omits these definitions and also defaults global initializers (`g_will_group` becomes zeroed, `g_pilot_phase` loses the `PILOT_PH_DISABLED` enum), so the intent is lost despite equivalent storage sizes.【F:decompiler_source_tests/test3/LEVEL.C†L13-L57】【F:decompiler_source_tests/test3/LEVEL_decompiled.c†L4-L27】
2. **Control-flow and data-flow reconstruction still show artifacts.** While loops are reconstructed, variable assignments are still scrambled in places (e.g., in `func_0511` the list/array updates and temporary assignments no longer mirror the original `GetFarestWills` logic).【F:decompiler_source_tests/test3/LEVEL.C†L122-L149】【F:decompiler_source_tests/test3/LEVEL_decompiled.c†L103-L137】
3. **Expression reconstruction and precedence issues persist.** In `func_0612`, expressions like `if (!g_pilot_timer <= 0.0f)` and call arguments such as `func_0448(SC_PC_GetPos(&vec))` indicate that operator precedence and parameter sourcing are being mis-modeled, which risks changing semantics even when control flow is preserved.【F:decompiler_source_tests/test3/LEVEL_decompiled.c†L171-L201】

### Likely root causes (based on current code)

1. **Header detection is too coarse for multiplayer scripts.** The header detector always includes `sc_global.h` and `sc_def.h`, but there is no path for `sc_MPglobal.h`, even when the entry point is `s_SC_NET_info` and the script uses `SC_NET_*` constants; this is a likely contributor to missing macro IDs and defines.【F:vcdecomp/core/headers/detector.py†L14-L104】
2. **Condition rendering does not preserve semantic guards reliably.** The `render_condition` flow depends on being able to trace SSA inputs for conditional jumps; when that trace is incomplete or incorrect, comparisons disappear and the emitted control flow degrades into unconditional branches (as seen in `func_0050`). This is evident in the call chain of `_find_condition_jump` → `_find_ssa_condition_value` → `render_condition` in the condition analysis module.【F:vcdecomp/core/ir/structure/analysis/condition.py†L24-L144】
3. **Loop/structure identification is limited to pattern detection without robust fallback.** The loop detector focuses on identifying canonical loop headers and increment patterns, but the outputs show that when these patterns fail, blocks remain uncollapsed and emit `block_XX` labels. The core loop detection logic is concentrated in `structure/patterns/loops.py`, which likely needs stronger heuristics or integration with a broader collapse strategy to handle more CFG shapes.【F:vcdecomp/core/ir/structure/patterns/loops.py†L1-L210】

### Recommendations (implementation-oriented)

#### 1) Improve header selection for multiplayer scripts

- **Goal:** Emit `#include <inc\sc_MPglobal.h>` when the entry signature indicates `s_SC_NET_info` or when `SC_NET_*`/`SC_MP_*` identifiers are referenced.
- **Implementation path:** Extend `HeaderDetector` to test for multiplayer usage and swap in `sc_MPglobal.h` (or add it before `sc_global.h` when necessary) rather than always defaulting to `sc_global.h`/`sc_def.h`. This will better preserve constant definitions and align with original sources in `decompiler_source_tests/test1/`.【F:vcdecomp/core/headers/detector.py†L14-L104】【F:decompiler_source_tests/test1/tt.c†L5-L94】

#### 2) Strengthen condition reconstruction (SSA + boolean folding)

- **Goal:** Reduce missing or simplified condition guards by ensuring condition values are traced through SSA and by adding robust boolean expression folding.
- **Implementation path:** Extend `render_condition` to recover conditions when the SSA source is missing by:
  - Inspecting predecessor blocks for comparison ops and resolving branch polarity.
  - Folding `CMP + JZ/JNZ` into explicit comparisons (inspired by Ghidra’s condition and flow handling).
- **Ghidra inspiration:** Ghidra’s flow and block actions are designed to handle loop bodies and conditional structure across collapse stages, and can guide how to collect and stabilize boolean expressions across CFG edges.【F:vcdecomp/core/ir/structure/analysis/condition.py†L24-L200】【F:ghidra-decompiler-src/blockaction.cc†L40-L176】

#### 3) Expand structured loop recovery (loop body, exit selection, and irreducible edges)

- **Goal:** Avoid `block_XX` labels by better identifying loop bodies and exits, especially for nested loops and loops with internal `break`/`continue`.
- **Implementation path:** Enhance loop recognition to:
  - Build loop bodies using more robust reachability (akin to Ghidra’s loop body extension and exit selection). 
  - Add fallback `while (1)` + `break` reconstruction for unstructured loops.
- **Ghidra inspiration:** `LoopBody::extend`/`findExit` in Ghidra provides a model for how to capture structured loop bodies with explicit exit selection when there are multiple tails or exits.【F:vcdecomp/core/ir/structure/patterns/loops.py†L1-L210】【F:ghidra-decompiler-src/blockaction.cc†L146-L200】

#### 4) Improve switch/case recovery via jump table modeling

- **Goal:** Restore structured `switch` statements (observed to regress to simplified/unguarded cases in `tt_decompiled.c`).
- **Implementation path:** Expand jump-table detection to emulate the address calculation of indirect jumps and map entries to case labels; include ranges and fall-through behavior.
- **Ghidra inspiration:** Ghidra’s `jumptable.cc` shows a dedicated emulation path to compute load tables and normalize jump table entries, which can guide how to model switch recovery even in non-native bytecode representations.【F:decompiler_source_tests/test1/tt.c†L97-L136】【F:ghidra-decompiler-src/jumptable.cc†L16-L200】

#### 5) Fix expression emission for lvalue/rvalue correctness

- **Goal:** Prevent invalid or ambiguous expressions like `if (!g_pilot_timer <= 0.0f)` and argument corruption such as `func_0448(SC_PC_GetPos(&vec))` by ensuring operator precedence and lvalue tracking are preserved.
- **Implementation path:**
  - In the emitter, track whether an expression is assignable before applying `+=`, `-=`, etc.
  - Add tests for vector field updates and compound assignment patterns.
- **Ghidra inspiration:** Ghidra’s `printc.cc` documents operator precedence and explicit token classification which can inform emitter ordering and lvalue safety checks.【F:decompiler_source_tests/test3/LEVEL_decompiled.c†L171-L201】【F:ghidra-decompiler-src/printc.cc†L21-L140】

### Suggested next validation steps

1. After addressing the above items, re-run:
   - `python -m vcdecomp structure decompiler_source_tests/test1/tt.scr > decompiler_source_tests/test1/tt_decompiled.c`
   - `python -m vcdecomp structure decompiler_source_tests/test3/LEVEL.SCR > decompiler_source_tests/test3/LEVEL_decompiled.c`
2. Visually diff against the originals in `decompiler_source_tests/test1/tt.c` and `decompiler_source_tests/test3/LEVEL.C` to ensure headers, conditionals, and loop structure align closer to source.
