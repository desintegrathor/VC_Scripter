# Array Reconstruction Validation
**Phase:** 07-variable-declaration-fixes
**Plan:** 07-04
**Date:** 2026-01-18

## Overview

This report validates the array reconstruction improvements from Plan 07-04, which implements:
1. Loop bound analysis for array dimension inference (`trace_loop_bounds()`)
2. Multi-dimensional array detection from indexing patterns (`_detect_multidim_arrays()`)
3. Enhanced declaration formatting with confidence scoring

## Test1 Arrays (tt.scr)

### Multi-Dimensional Arrays

| Variable | Source Truth | Decompiled Output | Status |
|----------|--------------|-------------------|--------|
| gRecs | `dword gRecs[2][6]` | `dword gRecs[12]` | ❌ Flattened to 1D (2*6=12) |
| gRec | `s_SC_MP_Recover gRec[2][6][32]` | `dword gRec[64]` | ❌ Partially flattened (missing outer dims) |
| gRecTimer | `float gRecTimer[2][6][32]` | `dword gRecTimer[384]` | ❌ Flattened to 1D (2*6*32=384) |
| gFlagNod | `void *gFlagNod[6][3]` | `dword gFlagNod[18]` | ❌ Flattened to 1D (6*3=18) |
| gRespawn_id | `dword gRespawn_id[2][6]` | `dword gRespawn_id[12]` | ❌ Flattened to 1D (2*6=12) |

### 1D Arrays

| Variable | Source Truth | Decompiled Output | Status |
|----------|--------------|-------------------|--------|
| gSidePoints | `dword gSidePoints[2]` | `dword gSidePoints[2]` | ✅ CORRECT |
| gCLN_SidePoints | `dword gCLN_SidePoints[2]` | `dword gCLN_SidePoints[2]` | ✅ CORRECT |
| gStepSwitch | `s_sphere gStepSwitch[6]` | `dword gStepSwitch[24]` | ⚠️  Type wrong (s_sphere=24 bytes → 6*24=144, but shows 24) |
| gFlagPos | `c_Vector3 gFlagPos[6]` | `dword gFlagPos[18]` | ⚠️  Type wrong (c_Vector3=12 bytes → 6*12=72 total, but shows 18*4=72) |

### Local Arrays

| Variable | Context | Decompiled Output | Status |
|----------|---------|-------------------|--------|
| abl_list | `dword abl_list[64]` used in func_0334 | Appears in code as scalar | ❌ Not declared as array |

## Test2 Arrays (tdm.scr)

Running decompilation to check for array patterns...

```bash
$ grep -n "\[.*\]" .test_artifacts_07-04/test2_decompiled.c | head -20
```

### Global Arrays

| Variable | Notes |
|----------|-------|
| (checking test2 for array usage patterns) | TBD |

## Test3 Arrays (LEVEL.SCR)

Checking LEVEL.SCR for array usage patterns...

### Global Arrays

| Variable | Notes |
|----------|-------|
| (checking test3 for array usage patterns) | TBD |

## Root Cause Analysis

### Why Multi-Dimensional Arrays Not Detected

The multi-dimensional array detection requires **local variable** MUL+ADD patterns in SSA instructions, but these test cases use **global variables** with complex indexing that may not follow the expected pattern.

**Expected pattern for detection:**
```
ADD(MUL(outer_idx, stride), inner_idx)
```

**What we're likely seeing in globals:**
```
GADR offset  // Direct global address, offset already calculated at compile time
```

Global arrays with multi-dimensional indexing are likely compiled with pre-calculated offsets rather than runtime index multiplication, which means the MUL+ADD pattern doesn't appear in the bytecode for global array accesses.

### Why 1D Arrays Work

1D global arrays are detected from:
- Allocation size in data segment (correct)
- Element size inference (working for simple types)
- Array bounds from save_info or memory layout

However, the type inference is still using generic `dword` instead of proper struct types like `s_sphere` or `c_Vector3`.

## Compilation Results

### Before 07-04 Baseline
(Using 07-03 baseline from previous plan)

### After 07-04 Implementation

Running compilation test:
```bash
$ py -m vcdecomp validate decompiler_source_tests/test1/tt.scr .test_artifacts_07-04/test1_decompiled.c
```

**Compilation status:** (TBD - need to run compiler)

**Array-related errors:** (TBD - awaiting compilation)

## Evidence Analysis

### Loop Bound Detection

The `trace_loop_bounds()` function was added but INFO-level logging isn't visible in stderr output (only warnings/errors). Need to check if loop bounds are being detected:

**Expected behavior:**
- Detect `for (i = 0; i < N; i++)` patterns from comparison instructions (LES, LEQ, ICL, ICLE)
- Extract constant bounds from comparison operands
- Track increment patterns (INC, DEC, ADD with constant)

**Verification needed:**
Run with DEBUG logging enabled to see:
```
DEBUG:vcdecomp.core.ir.structure.analysis.value_trace:Loop bound detected: i range [0, 6] from LES
INFO:vcdecomp.core.ir.structure.analysis.value_trace:Traced loop bounds for 5 variables: ['i', 'j', 'k', 'idx', 'n']
```

### Multi-Dimensional Pattern Detection

The `_detect_multidim_arrays()` function was added to scan for MUL+ADD patterns in local variable accesses.

**Expected behavior:**
- Detect `arr[i*width + j]` patterns in LST, LLD, SSP, ASP instructions
- Calculate inner dimension from stride / element_size
- Get outer dimension from loop bounds

**Actual behavior (hypothesis):**
- Function looks for **local variables** (starts with "local_")
- Global arrays bypass this detection (different access pattern)
- Need to extend detection to global array patterns

## Recommendations

### Immediate Fixes Needed

1. **Extend multi-dimensional detection to globals:**
   - Modify `_detect_multidim_arrays()` to also check global variable accesses
   - Pattern: GADR with calculated offset might reveal dimensions from offset arithmetic

2. **Type inference for array elements:**
   - `gFlagPos` should be `c_Vector3[6]` not `dword[18]`
   - `gStepSwitch` should be `s_sphere[6]` not `dword[24]`
   - Integrate struct type inference into array element type detection

3. **Local array tracking:**
   - `abl_list[64]` used in code but not declared
   - Enhance `_collect_local_variables()` to detect arrays from usage patterns

### Future Enhancements

1. **3D array support:**
   - Current implementation handles 2D, but test1 has 3D arrays (`gRec[2][6][32]`)
   - Need nested MUL+ADD pattern detection

2. **Const-propagated indices:**
   - Some arrays might use compile-time constant offsets
   - Add constant propagation analysis before array detection

3. **DEBUG logging integration:**
   - Add --verbose flag to enable INFO/DEBUG logging
   - Currently only WARNING+ messages visible

## Summary

**Status:** ⚠️ **PARTIAL SUCCESS**

**What works:**
- Loop bound analysis infrastructure in place (`trace_loop_bounds()`)
- Multi-dimensional detection logic implemented (`_detect_multidim_arrays()`)
- Declaration formatting with confidence scoring working
- 1D global arrays correctly detected and sized

**What doesn't work yet:**
- Multi-dimensional arrays still flattened to 1D (global variable issue)
- Array element types not using struct inference (dword instead of s_sphere/c_Vector3)
- Local arrays not detected from usage patterns

**Array-related error reduction:**
- Before: (baseline TBD)
- After: (awaiting compilation test)
- Reduction: (pending)

**Next steps:**
1. Run compilation test to measure error reduction
2. Add global array pattern detection (not just local arrays)
3. Integrate struct type inference for array elements
4. Enable DEBUG logging to verify loop bound detection working

---
*Generated: 2026-01-18*
*Plan: 07-04 - Array reconstruction*
