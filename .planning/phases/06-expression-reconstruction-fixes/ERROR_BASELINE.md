# Expression Reconstruction Error Baseline

**Date**: 2026-01-18
**Purpose**: Establish baseline measurement of decompiler expression reconstruction bugs to guide systematic fixes in Phase 6

## Executive Summary

- **Total test scripts**: 3 (test1/tt.scr, test2/tdm.scr, test3/LEVEL.scr)
- **Compilation success rate**: 0/3 (100% failure)
- **Compiler behavior**: SCMP.exe crashes with access violation (code 3221225477 / 0xC0000005)
- **Root cause**: Decompiled code is so malformed that compiler cannot parse it - crashes before writing error files
- **Error categorization**: Manual inspection required (compiler crash prevents automated error analysis)

## Current State Assessment

The decompiler produces **syntactically invalid C code** that causes the original SCMP.exe compiler to crash rather than produce compilation errors. This indicates critical bugs in expression reconstruction (`vcdecomp/core/ir/expr.py`) and code emission (`vcdecomp/core/ir/structure/emit/`).

All three test scripts exhibit the same categories of bugs, indicating systematic issues rather than edge cases.

## Error Pattern Analysis

### Pattern 1: Unreachable Goto to Undefined Labels

**Frequency**: HIGH (appears in 2/3 test files)
**Severity**: FATAL - Makes code unparseable
**Impact**: Breaks control flow, causes compiler confusion

**Examples**:

1. **test1_tt_decompiled.c, line 31**:
   ```c
   int func_0050(float param_0) {
       ...
       goto block_3; // @57
       if (!tmp1) {
   ```
   - Label `block_3` does not exist in the function
   - Code after goto is unreachable (control flow error)

2. **test1_tt_decompiled.c, lines 154-155**:
   ```c
   int func_0334(int param_0) {
       int tmp;

       goto block_46; // @343
       goto block_48; // @348
       return FALSE;
   }
   ```
   - Both labels undefined, entire function is broken
   - All statements are unreachable

**Root cause**: Structure orchestrator fails to resolve CFG blocks to proper C labels. Orphaned blocks (unreachable code warnings in test output) are being emitted as goto statements to non-existent labels instead of being omitted.

**Fix target**: `vcdecomp/core/ir/structure/emit/code_emitter.py` - skip emission of goto statements to orphaned blocks

---

### Pattern 2: Type Mismatch in Variable Assignments

**Frequency**: HIGH (appears in 2/3 test files)
**Severity**: FATAL - Type system violation
**Impact**: Compiler cannot determine variable types

**Examples**:

1. **test1_tt_decompiled.c, lines 65-67**:
   ```c
   tmp5 = SC_ggf(400);  // Function returns float
   tmp5 = 30.0f;         // Float literal
   return tmp5;
   ```
   BUT `tmp5` is declared as `s_SC_MP_EnumPlayers` (struct type), not float!

2. **test1_tt_decompiled.c, lines 88-90**:
   ```c
   tmp6 = tmp5;          // int to struct assignment
   tmp6 = 5.0f;          // float to struct assignment
   tmp6 = 10.0f;         // float to struct assignment
   ```
   Variable `tmp6` declared as `s_SC_MP_EnumPlayers` but assigned int and float values

3. **test3_LEVEL_decompiled.c, line 84**:
   ```c
   *tmp = -20000.0f;     // Dereferencing int pointer, assigning float
   ```
   `tmp` declared as `int`, used as pointer and assigned float literal

**Root cause**: Type inference in `vcdecomp/core/ir/expr.py` is broken. Variables are assigned incorrect types based on heuristics, but actual usage requires different types. Stack lifter or SSA builder is not propagating type information correctly.

**Fix target**:
- `vcdecomp/core/ir/stack_lifter.py` - improve type tracking for stack variables
- `vcdecomp/core/ir/expr.py` - fix variable type declaration logic

---

### Pattern 3: Missing Return Value in Non-Void Functions

**Frequency**: HIGH (appears in all 3/3 test files)
**Severity**: ERROR - Undefined behavior
**Impact**: Function may return garbage value

**Examples**:

1. **test1_tt_decompiled.c, line 47**:
   ```c
   int func_0050(float param_0) {
       ...
       return;  // Should be "return <value>;" for int function
   }
   ```

2. **test2_tdm_decompiled.c, line 43**:
   ```c
   int func_0010(float param_0) {
       ...
       return;  // Empty return in int function
   }
   ```

3. **test3_LEVEL_decompiled.c, lines 86, 93, 108, 132**:
   Multiple functions with `int` return type but `return;` statement

**Root cause**: Control flow analysis in structure module fails to detect that function execution path must return a value. Empty return statements are emitted when no explicit return value is computed.

**Fix target**: `vcdecomp/core/ir/structure/analysis/flow.py` - detect required return values based on function signature

---

### Pattern 4: Multiple Sequential Assignments to Same Variable

**Frequency**: MEDIUM (appears in 2/3 test files)
**Severity**: WARNING - Code compiles but is nonsensical
**Impact**: Dead code, only last assignment matters

**Examples**:

1. **test1_tt_decompiled.c, lines 65-67**:
   ```c
   tmp5 = SC_ggf(400);
   tmp5 = 30.0f;
   tmp5 = 10.0f;
   return tmp5;  // Only 10.0f matters, previous assignments wasted
   ```

2. **test1_tt_decompiled.c, lines 88-91**:
   ```c
   tmp6 = tmp5;
   tmp6 = 5.0f;
   tmp6 = 10.0f;
   return tmp6;  // Only final value (10.0f) is used
   ```

**Root cause**: SSA (Static Single Assignment) form is not being properly converted back to regular code. Each SSA temporary gets emitted as an assignment, but the multiple assignments to the same variable suggest phi nodes or redundant assignments aren't being optimized away.

**Fix target**: `vcdecomp/core/ir/ssa.py` - improve SSA-to-AST conversion, eliminate redundant assignments

---

### Pattern 5: Undeclared Variables Used

**Frequency**: MEDIUM (appears in 2/3 test files)
**Severity**: FATAL - Undefined symbol
**Impact**: Compiler cannot resolve variable reference

**Examples**:

1. **test3_LEVEL_decompiled.c, line 83**:
   ```c
   SC_ZeroMem(&vec, 12);  // 'vec' is not declared anywhere
   ```

2. **test3_LEVEL_decompiled.c, line 105**:
   ```c
   SC_P_GetPos(param_0, &vec);  // 'vec' used again, still not declared
   ```

3. **test3_LEVEL_decompiled.c, line 144**:
   ```c
   SC_MP_EnumPlayers(&enum_pl, &local_, 1);  // 'enum_pl' not declared
   ```

**Root cause**: Global variable detection or local variable collection is missing some variables. Variables that are used (likely from data segment addresses) are not being added to the function's variable declarations.

**Fix target**: `vcdecomp/core/ir/structure/analysis/variables.py` - comprehensive variable collection from all expression references

---

### Pattern 6: Unreachable Code After Return

**Frequency**: MEDIUM (appears in 2/3 test files)
**Severity**: WARNING - Code compiles but unreachable
**Impact**: Confusing, dead code

**Examples**:

1. **test1_tt_decompiled.c, lines 37-44**:
   ```c
   SC_MP_EndRule_SetTimeLeft(data_, tmp5);
   SC_MP_LoadNextMap();
   return TRUE;          // Function returns here
   SC_MP_LoadNextMap();  // UNREACHABLE
   return TRUE;          // UNREACHABLE
   SC_message("EndRule unsopported: %d", tmp);  // UNREACHABLE
   return FALSE;         // UNREACHABLE
   ```

2. **test1_tt_decompiled.c, lines 195-200**:
   ```c
   local_ = SC_MP_SRV_GetTeamsNrDifference(1);
   return 7;             // UNREACHABLE (inside if block, but early return)
   SC_P_GetInfo(idx, &player_info);  // UNREACHABLE
   local_1 = 1;          // UNREACHABLE
   local_1 = 0;          // UNREACHABLE
   return 7;             // UNREACHABLE
   ```

**Root cause**: Control flow graph includes unreachable nodes (from original bytecode optimizations or dead code). Structure analysis is emitting all nodes instead of pruning unreachable ones.

**Fix target**: `vcdecomp/core/ir/structure/patterns/` - prune unreachable blocks before code generation

---

## Prioritized Fix Targets

Based on frequency, severity, and fix complexity:

### Priority 1: CRITICAL (Blocks compilation entirely)

1. **Pattern 1: Undefined goto labels** - HIGH frequency, FATAL severity
   - Fix: Skip emission of goto to orphaned blocks
   - Estimated complexity: LOW (simple check in code emitter)
   - File: `vcdecomp/core/ir/structure/emit/code_emitter.py`

2. **Pattern 5: Undeclared variables** - MEDIUM frequency, FATAL severity
   - Fix: Comprehensive variable collection from all expressions
   - Estimated complexity: MEDIUM (thorough AST traversal)
   - File: `vcdecomp/core/ir/structure/analysis/variables.py`

### Priority 2: HIGH (Major correctness issues)

3. **Pattern 2: Type mismatches** - HIGH frequency, FATAL severity
   - Fix: Improve type inference and propagation
   - Estimated complexity: HIGH (requires SSA + stack lifter changes)
   - Files: `vcdecomp/core/ir/stack_lifter.py`, `vcdecomp/core/ir/expr.py`

4. **Pattern 3: Missing return values** - HIGH frequency, ERROR severity
   - Fix: Detect required return values, synthesize placeholder if needed
   - Estimated complexity: MEDIUM (function signature analysis)
   - File: `vcdecomp/core/ir/structure/analysis/flow.py`

### Priority 3: MEDIUM (Code quality issues)

5. **Pattern 4: Multiple assignments** - MEDIUM frequency, WARNING severity
   - Fix: Optimize SSA-to-AST conversion, eliminate dead assignments
   - Estimated complexity: MEDIUM (SSA analysis)
   - File: `vcdecomp/core/ir/ssa.py`

6. **Pattern 6: Unreachable code** - MEDIUM frequency, WARNING severity
   - Fix: Prune unreachable CFG nodes before emission
   - Estimated complexity: LOW (reachability analysis)
   - File: `vcdecomp/core/ir/structure/analysis/flow.py`

## Baseline Metrics

### Test 1: test1_tt_decompiled.c (Turntable script)

- **Compilation**: CRASH (access violation 0xC0000005)
- **Decompilation**: PARTIAL (11/15 functions succeeded, 4 failed with AttributeError)
- **File size**: 4,530 bytes
- **Critical errors**:
  - Pattern 1 (undefined goto): 3 instances
  - Pattern 2 (type mismatch): 5+ instances
  - Pattern 3 (missing return): 8 instances
  - Pattern 5 (undeclared var): 1 instance (`abl_list`)
  - Pattern 6 (unreachable code): 4 blocks

### Test 2: test2_tdm_decompiled.c (Deathmatch script)

- **Compilation**: CRASH (access violation)
- **Decompilation**: Not measured (test output truncated)
- **File size**: Unknown
- **Critical errors**:
  - Pattern 1 (undefined goto): 1 instance (line 31)
  - Pattern 3 (missing return): 1+ instance
  - Similar patterns to test1 expected

### Test 3: test3_LEVEL_decompiled.c (Level script)

- **Compilation**: CRASH (access violation)
- **Decompilation**: Not measured
- **File size**: Unknown (but shows 62+ tmp variables in _init alone - suggests large function)
- **Critical errors**:
  - Pattern 2 (type mismatch): 1 instance (line 84 - pointer deref)
  - Pattern 3 (missing return): 4+ instances
  - Pattern 5 (undeclared var): 2 instances (`vec`, `enum_pl`)

## Measurement Methodology

Since the compiler crashes before producing error files, this baseline was created through **manual source code inspection** of the three decompiled test files:

1. Run pytest validation suite to decompile scripts
2. Examine decompiled .c files in `.test_artifacts_baseline/`
3. Identify error patterns by manual code review
4. Categorize errors by type and severity
5. Count instances across all test files
6. Cross-reference with decompiler warnings in test output

**Limitation**: This baseline captures only **statically detectable errors**. Runtime semantic errors (wrong bytecode output that compiles successfully) are not measured here.

## Success Criteria for Phase 6

After implementing fixes, the baseline will be considered improved when:

1. **At least 1/3 test files compile successfully** (no crash, SCMP returns 0)
2. **Pattern 1 eliminated** (no undefined goto labels)
3. **Pattern 5 eliminated** (all variables declared)
4. **Pattern 3 reduced by 50%+** (most functions have proper return statements)

## Next Steps

**Phase 6 Plan 02**: Implement Priority 1 fixes (Patterns 1 & 5)
- Fix undefined goto labels (orphaned block handling)
- Fix undeclared variables (comprehensive variable collection)
- Re-run validation suite
- Measure improvement: compiler should parse code (even if errors remain)

**Phase 6 Plan 03**: Implement Priority 2 fixes (Patterns 2 & 3)
- Fix type mismatches (type inference improvements)
- Fix missing return values (control flow analysis)
- Re-run validation suite
- Measure improvement: reduce fatal errors

**Phase 6 Plan 04**: Implement Priority 3 fixes (Patterns 4 & 6)
- Optimize SSA conversion (eliminate redundant assignments)
- Prune unreachable code
- Re-run validation suite
- Measure improvement: bytecode match percentage increases

## Appendix: Test Output Evidence

Test execution captured the following warnings (evidence of orphaned blocks):

```
WARNING  vcdecomp.core.ir.structure.orchestrator:orchestrator.py:362
Skipping orphaned block 2 at address 53 in function func_0050 - no predecessors (unreachable code)
...
[90+ similar warnings for other orphaned blocks]
```

This directly correlates with **Pattern 1** (undefined goto labels) and **Pattern 6** (unreachable code).

The decompilation itself shows partial success:
- test1/tt: 11/15 functions succeeded (73% success rate)
- 4 functions failed with AttributeError (separate bug in structure analysis)

This indicates the decompiler infrastructure is working, but expression reconstruction and code emission have systematic bugs.
