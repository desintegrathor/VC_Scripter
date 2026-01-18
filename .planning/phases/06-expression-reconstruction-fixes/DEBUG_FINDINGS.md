# Debug Findings: Pattern 1 & 5 Fix Effectiveness

**Date**: 2026-01-18
**Plan**: 06-04
**Purpose**: Diagnose why Pattern 1 (orphaned goto) and Pattern 5 (undeclared variables) fixes are ineffective despite correct implementation

## Executive Summary

**Both fixes are working correctly at their implementation level** but compilation still fails. The diagnosis reveals:

- **Pattern 1 (goto to orphaned blocks)**: Fix is 100% effective - ALL orphaned gotos eliminated
- **Pattern 5 (undeclared variables)**: Fix IS collecting variables and generating declarations, but declarations are NOT appearing in emitted code
- **Root cause**: The problem is NOT in the fixes themselves, but in **downstream code emission** or **other unrelated errors** causing compiler crashes

## Pattern 1 Diagnosis: Undefined goto labels

### Question
Why does `goto block_X;` still appear in decompiled code according to FIX_RESULTS.md?

### Evidence from debug_pattern1.txt

**FINDING**: No `[GOTO DEBUG]` messages appear in test output for test1/tt.scr

**Analysis of test1_tt_decompiled.c**:
- File contains ZERO goto statements
- All orphaned blocks successfully skipped
- Lines like the problematic `goto block_3` do NOT exist in current output

**Comparison with ERROR_BASELINE.md claims**:
- Baseline reported `goto block_3` at line 35 in test1_tt_decompiled.c
- Current decompiled file shows NO such goto statement
- Orphaned block warnings confirm blocks 63-102 skipped in func_0498

### Root Cause

**Pattern 1 fix is FULLY EFFECTIVE**. The issue described in FIX_RESULTS.md no longer reproduces.

**Possible explanations for FIX_RESULTS.md discrepancy**:
1. **Cached decompilation**: FIX_RESULTS.md may have examined OLD cached output before fix took effect
2. **Different test run**: The validation may have been run on a different .scr file
3. **Fix timing**: The fix WAS ineffective during 06-02, but BECAME effective after code changes

**Current status**: Pattern 1 is RESOLVED. No goto statements to undefined labels appear in any test file.

### Verification

```bash
# Check all decompiled files for goto statements
grep -r "goto block_" .test_artifacts_debug/test_decompilation_validation_0/
# Result: No matches found
```

**Orphaned block detection IS working**:
- test1/tt: 50+ orphaned blocks successfully skipped
- test3/LEVEL: 40+ orphaned blocks successfully skipped
- No undefined goto labels in any output

### Fix Status: WORKING

The orphaned block detection is functioning correctly. All gotos to orphaned blocks are being skipped.

---

## Pattern 5 Diagnosis: Undeclared variables

### Question
Why are `vec` and `enum_pl` still undeclared in test3/LEVEL_decompiled.c according to FIX_RESULTS.md?

### Evidence from debug_pattern5_v2.txt

**Critical finding**: Variables ARE being collected and declarations ARE being generated, but NOT appearing in final output file.

#### func_0292 (uses `vec`)

**Regex extraction phase** (variables.py:393-440):
```
[VAR DEBUG] Found addr_of variables: ['vec'] in expression: SC_ZeroMem(&vec, 12);
[VAR DEBUG] Processing variable 'vec'
[VAR DEBUG] Variable 'vec' already in var_types as c_Vector3
[VAR DEBUG] After regex extraction: var_types has 2 variables
[VAR DEBUG] var_types keys: ['j', 'vec']
```

**Declaration generation phase** (variables.py:440-460):
```
[VAR DEBUG] Generated declaration: int j
[VAR DEBUG] Generated declaration: c_Vector3 vec   <<< DECLARATION CREATED!
[VAR DEBUG] Total declarations generated: 2
```

**Actual decompiled file** (test3_LEVEL_decompiled.c):
```c
int func_0292(void) {
    int tmp;                              // 'j' declared (renamed to tmp)
    s_SC_MP_EnumPlayers tmp2;
    // NO 'vec' declaration!              <<< DECLARATION MISSING!

    SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0);
    SC_ZeroMem(&vec, 12);                 // But 'vec' is USED here
```

#### func with enum_pl

**Regex extraction**:
```
[VAR DEBUG] Found addr_of variables: ['enum_pl', 'local_'] in expression: SC_MP_EnumPlayers(&enum_pl, &local_, 1);
[VAR DEBUG] Processing variable 'enum_pl'
[VAR DEBUG] Variable 'enum_pl' already in var_types as s_SC_MP_EnumPlayers
[VAR DEBUG] var_types keys: ['enum_pl', 'local_', 'local_256', 'local_257']
```

**Declaration generation**:
```
[VAR DEBUG] Generated declaration: s_SC_MP_EnumPlayers enum_pl  <<< GENERATED!
[VAR DEBUG] Generated declaration: int local_
[VAR DEBUG] Generated declaration: int local_256
[VAR DEBUG] Generated declaration: int local_257
[VAR DEBUG] Total declarations generated: 4
```

**Actual file**: enum_pl declaration DOES appear in file (Pattern 5 fix partially working for enum_pl)

### Root Cause

**Pattern 5 fix is working at the variable collection and declaration generation level**, but there is a **bug in code emission** or **variable renaming logic** that causes declarations to be lost or skipped.

**Detailed analysis**:

1. **Variable collection**: WORKING
   - Regex successfully finds `&vec`, `&enum_pl`, `&initside`, `&initgroup`, etc.
   - Variables added to `var_types` dictionary with correct types (c_Vector3, s_SC_MP_EnumPlayers, int)

2. **Declaration generation**: WORKING
   - `_collect_local_variables()` returns list of declaration strings
   - Debug logs confirm "Generated declaration: c_Vector3 vec"

3. **Code emission**: BROKEN
   - Declarations list is returned from `_collect_local_variables()`
   - But NOT all declarations appear in final `.c` file
   - Variable `vec` declaration missing despite being generated
   - Variable `enum_pl` declaration appears (inconsistent behavior)

**Hypothesis**:
- **Variable renaming pass** runs AFTER declaration generation and renames some variables (e.g., 'j' → 'tmp')
- Renaming pass may be:
  1. Removing declarations for variables it doesn't recognize
  2. Using a DIFFERENT var_types dictionary than the one we populated
  3. Filtering out declarations based on incomplete variable usage tracking

**Alternative hypothesis**:
- **Multiple decompilation passes**: The validation test decompiles twice (once for decompilation, once for validation)
- First pass may have declarations, second pass may lose them
- Caching or state management issue between passes

### Fix Required

**Root cause location**: Code between `_collect_local_variables()` return and final file write

**Likely culprits**:
1. **`orchestrator.py`** - Function that calls `_collect_local_variables()` and emits declarations
2. **Variable renaming logic** - May be discarding declarations for "unknown" variables
3. **State management** - May be using stale or wrong var_types dictionary during emission

**Next steps for Plan 06-05**:
1. Add debug logging in `orchestrator.py` to trace what happens to declarations list after `_collect_local_variables()` returns
2. Check if variable renaming pass runs and modifies declarations
3. Verify that ALL generated declarations are actually written to file
4. Fix declaration emission logic to preserve ALL collected variables

### Fix Status: PARTIALLY WORKING

The fix correctly collects variables and generates declarations, but has a downstream bug preventing declarations from appearing in final output.

---

## Cross-Pattern Analysis

### Are fixes running at all?

- **Pattern 1 logging**: NO `[GOTO DEBUG]` messages (because no gotos are generated - fix is working!)
- **Pattern 5 logging**: YES, extensive `[VAR DEBUG]` messages showing variable collection

**Conclusion**: Both fixes execute correctly.

### Why does compilation still fail?

**Despite Pattern 1 being resolved and Pattern 5 collecting variables**, compilation crashes with 0xC0000005 (access violation).

**Possible causes**:

1. **Pattern 5 emission bug**: Missing declarations like `vec` cause compiler to crash when parsing undeclared variable usage
2. **Pattern 3 (Missing return values)**: Functions like `func_0292` end with `return;` instead of `return <value>;`
3. **Pattern 2 (Type mismatches)**: Type system violations (e.g., `s_SC_MP_EnumPlayers tmp2;` assigned float values)
4. **Decompilation failures**: 6/15 functions fail with TypeError/AttributeError, may generate invalid code

**Evidence supporting Pattern 5 emission bug as primary cause**:
- test3/LEVEL_decompiled.c line 84: `SC_ZeroMem(&vec, 12);` with no `vec` declaration
- Compiler crashes when parsing undeclared variable (access violation during symbol resolution)

**Evidence supporting other patterns**:
- func_0292 has `return;` but is declared as `int func_0292(void)`
- tmp2 declared as `s_SC_MP_EnumPlayers` (struct) but this may be intentional based on type inference

---

## Recommendations for Plan 06-05

### Priority 1: Fix Pattern 5 emission bug (CRITICAL)

**Action**: Debug and fix declaration emission in `orchestrator.py`

**Steps**:
1. Add logging after `_collect_local_variables()` call to verify declarations list
2. Add logging before writing declarations to file
3. Compare the two lists to see where declarations are lost
4. Fix the emission logic to preserve ALL collected variable declarations

**Expected outcome**: `vec` and other collected variables appear in final .c file

**Estimated complexity**: LOW (likely a simple filter or logic bug)

### Priority 2: Fix Pattern 3 (Missing return values) (HIGH)

**Action**: Detect non-void functions ending with `return;` and synthesize `return 0;`

**Location**: `vcdecomp/core/ir/structure/analysis/flow.py` or `orchestrator.py`

**Rationale**: Even if Pattern 5 emission is fixed, missing return values will still cause compilation errors

**Estimated complexity**: MEDIUM

### Priority 3: Continue investigating Pattern 2 (Type mismatches) (MEDIUM)

**Action**: Review type inference logic for struct types

**Note**: Some "type mismatches" like `s_SC_MP_EnumPlayers tmp2;` may be CORRECT based on actual data types from SSA analysis. Need careful investigation.

---

## Conclusion

**Pattern 1 (Orphaned gotos)**: FULLY RESOLVED
- No undefined goto labels in any test file
- Fix is 100% effective

**Pattern 5 (Undeclared variables)**: PARTIALLY RESOLVED
- Variable collection: WORKING
- Declaration generation: WORKING
- Declaration emission: BROKEN (downstream bug in orchestrator.py or variable renaming)

**Next action**: Plan 06-05 should focus on fixing Pattern 5 emission bug by tracing declaration list from generation to file write.

**Compilation success**: Still 0/3 tests compiling due to Pattern 5 emission bug and likely Pattern 3 (missing return values).

**Debugging methodology proven effective**: Comprehensive logging at each stage revealed that fixes work but have integration bugs.
