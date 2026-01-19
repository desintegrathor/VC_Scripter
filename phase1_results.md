# Phase 1 Results: Function Boundary Detection Fix

## Changes Made
Modified `vcdecomp/core/ir/function_detector.py` (lines 106-125):
- **Before**: Used first RET instruction after function start as end boundary
- **After**: Use start of next function as end boundary (similar to legacy `call_only` method)
- **Rationale**: Functions with early returns were being truncated, orphaning code blocks with switches

## Results

### Switch Detection Improvement
- **Before fix**: 3 full switches (2+ cases)
- **After fix**: 5 full switches (2+ cases)
- **Improvement**: +2 switches (+67%)

### Switch Locations (Phase 1)
Line numbers in tt_phase1_debug.c:
1. Line 110: `switch (gEndRule)` in func_0050
2. Line 297: `switch (gSteps)` in func_0213  
3. Line 323: `switch (n)` in func_0334
4. Line 382: `switch (gMission_phase)` in func_0334
5. Line 762: `switch (gCLN_ShowInfo)` in ScriptMain ← NEW!

### Original tt.c Switch Count
Total switches in original: **12 switches**
```bash
$ grep -E "^\s+switch\s*\(" tt.c | wc -l
12
```

The plan document claiming "22 switches" appears to be counting switch CASES, not switch STATEMENTS.

### Test Results
- ✅ 224 tests passing (no regressions)
- ✅ 36 tests failing (pre-existing failures, unchanged)
- ✅ Function detector unit tests: 5 passed, 3 skipped

### Analysis

**Progress**: 5/12 = **42% switch detection rate** (vs. target of 100%)

**Missing**: 7 switches still not detected

**Why the improvement was modest**:
The function boundary fix helped include more code in ScriptMain, but the main issue appears to be the SWITCH DETECTION ALGORITHM itself, not just function boundaries.

Looking at the original tt.c, ScriptMain has a large switch on `info->message` with 13 cases (lines 487-1223 in original). This switch is likely not being detected due to:
1. Complex nested structure
2. Modulo operations (e.g., `switch(main_phase%4)`)
3. Nested switches within cases
4. Jump table optimization by compiler

### Recommendation

Phase 2 (Jump Table Detection) is NECESSARY to achieve the 100% goal. The function boundary fix was helpful but insufficient.
