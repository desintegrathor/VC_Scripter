The plan is written to `.ralph/PLAN_iter_3.md`. Here's the summary:

## Iteration 3 Plan Summary

**Root-Cause Invariant**: Post-processing dead code elimination in `emit_function()` (hierarchical_emitter.py:505-521) truncates structurally required closing braces `}` when the last `return` statement is inside a nested block (if/else, switch/case).

**The bug**: The DCE finds the **last** `return` in the emitted lines and truncates everything after it. But when a return is inside `if (...) { return; } else { return; }` or `switch { case: return; default: return; }`, the closing braces of those blocks appear after the return and get deleted.

**Evidence**: 5 missing closing braces in tt.scr (func_0119, func_0155, func_0213, func_0334 + one more). tdm.scr and LEVEL.SCR are unaffected (balanced braces).

**Fix**: Replace naive "truncate after last return" with brace-depth-aware truncation — only truncate after returns at brace depth 0 (function body level). Returns inside nested blocks (depth > 0) are preserved with their enclosing closing braces.

**Expected Impact**:
- tt.scr: **IMPROVED** (5 syntax errors fixed)
- tdm.scr: **UNCHANGED** (no regression)
- LEVEL.SCR: **UNCHANGED** (no regression)

**Next Priority**: Compound AND/OR condition extraction (`/* condition */` placeholders for short-circuit `(a < 3) && (a > -3)` patterns).
 is gone

Original (lines 139-154):
    if (set.tt_respawntime>1.0f){
        return set.tt_respawntime;
    }
    val = SC_ggf(400);
    if (val==0) val = 30;
    return val;
```

**Function func_0155 (GetRecovLimitTime) — same pattern, lines 99-114**
**Function func_0213 (GetTimeLimit) — same pattern, lines 123-131**

**Function func_0334 (GetAttackingSide):**
```
Decompiled (lines 163-170):
    switch (param_0%4) {
    case 0:
    case 3:
        return FALSE;
    default:
        return TRUE;   ← last return, DCE truncates here
}                       ← function }, but switch } is gone

Original (lines 230-240):
    switch(main_phase%4){
        case 0:
        case 3:return 0;
    }
    return 1;
```

### Non-Affected Tests: tdm.scr (0 issues), LEVEL.SCR (0 issues)
These tests have balanced braces ({=}, }=}). Their functions don't end with returns inside nested blocks, so the DCE doesn't trigger the bug.

## Proposed Fix

- **File**: `vcdecomp/core/ir/structure/emit/hierarchical_emitter.py`
- **Function**: `emit_function()`, lines 505-521
- **Change**: Replace the naive "truncate after last return" with a brace-depth-aware truncation

### Current Code (buggy):
```python
last_return_idx = -1
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == "return;" or stripped.startswith("return "):
        last_return_idx = i
if last_return_idx >= 0 and last_return_idx < len(lines) - 1:
    has_labeled = any(...)
    if not has_labeled:
        lines = lines[:last_return_idx + 1]
```

### Fixed Code:
Only truncate after a return that is at **brace depth 0** (top-level function body). A return inside a nested block (depth > 0) should not trigger truncation of the enclosing block's closing braces.

```python
# Post-processing: Dead code elimination
# Find the last return statement at brace depth 0 (function body level).
# Returns inside nested blocks (if/else, switch, while) must NOT trigger
# truncation — their enclosing closing braces are syntactically required.
last_toplevel_return_idx = -1
brace_depth = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    brace_depth += stripped.count('{') - stripped.count('}')
    if (stripped == "return;" or stripped.startswith("return ")) and brace_depth == 0:
        last_toplevel_return_idx = i

if last_toplevel_return_idx >= 0 and last_toplevel_return_idx < len(lines) - 1:
    # Check if anything after the return is a labeled block (goto target)
    has_labeled = any(
        lines[j].strip().endswith(":")
        for j in range(last_toplevel_return_idx + 1, len(lines))
        if lines[j].strip()
    )
    if not has_labeled:
        lines = lines[:last_toplevel_return_idx + 1]
```

The key change: track `brace_depth` and only consider returns where `brace_depth == 0`. Returns inside `if { ... return; }` have depth >= 1 and are skipped.

## Expected Impact

- **tt.scr**: **IMPROVED** — 5 missing closing braces restored, all functions syntactically valid
- **tdm.scr**: **UNCHANGED** — no functions trigger this pattern (brace-balanced already)
- **LEVEL.SCR**: **UNCHANGED** — no functions trigger this pattern (brace-balanced already)

## Implementation Steps

1. Read `hierarchical_emitter.py` lines 505-521 to confirm the exact code
2. Replace the dead code elimination block with the brace-depth-aware version
3. Run all three test decompilations and verify:
   - tt.scr: brace count balanced (currently { = 179, } = 174, should be equal)
   - tdm.scr: no regressions (currently balanced)
   - LEVEL.SCR: no regressions (currently balanced)
4. Visually compare affected functions (func_0119, func_0155, func_0213, func_0334) to verify correct closing braces

## Risk Assessment

**Very low risk**:
- The change makes the DCE more conservative (only truncates at depth 0), which can only ADD lines (closing braces) to the output, never remove correct lines
- If no top-level return exists, `last_toplevel_return_idx` stays -1 and no truncation occurs (same as current behavior when no return exists)
- The brace counting is a well-understood technique

## Next Priority (DO NOT FIX YET)

**Compound AND/OR condition extraction**: `if (/* condition */)` placeholders appear when the bytecode has sequential `JZ` jumps to the same target forming `(a < 3) && (a > -3)` short-circuit AND patterns. The condition extraction code doesn't recognize multi-predicate short-circuit chains. This affects 2 functions in tt.scr.
