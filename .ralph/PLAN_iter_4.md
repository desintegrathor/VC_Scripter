Plan written to `.ralph/PLAN_iter_4.md`. Here's the summary:

---

# Iteration 4 Plan Summary

## Root-Cause Invariant
**The for-loop body emitter treats inner loop headers as flat statement blocks instead of recursively detecting nested loops.**

`_emit_natural_for_loop()` in `hierarchical_emitter.py` pre-marks ALL body blocks as "emitted" then iterates them calling `_emit_body_block_by_id()` — a flat statement renderer. It never checks `_loop_header_map` to see if a body block is itself a loop header. Inner loops are destroyed.

## Evidence
- **tt.scr**: Triple nested `for(i) for(j) for(k)` timer update loop → flattened to single loop with orphaned `idx`, `idx29` assignments
- **tt.scr**: Triple nested respawn init `for(k) for(j) for(i)` → same flattening
- **tdm.scr**: No nested for-loops (neutral)
- **LEVEL.SCR**: Various loops inside switch cases benefit from the same emission path fix

## Fix
In `hierarchical_emitter.py:_emit_natural_for_loop()`, before emitting a body block as flat statements, check if it's a loop header and recursively call `_try_emit_natural_loop()`. Also fix the pre-marking strategy so inner loop headers remain eligible for nested detection.

## Expected Impact
- **tt**: IMPROVED (nested loops restored)
- **tdm**: UNCHANGED
- **LEVEL**: IMPROVED (indirect benefits)
undefined SSA names because their for-loop detection never fired.

**Also in tt.scr — Triple nested respawn init loop (tt.c lines 874-902):**
```c
for (k=0;k<2;k++){
    if (k) side_char = 'D'; else side_char = 'A';
    for (j=0;j<STEP_MAX;j++){
        for (i=0;i<REC_MAX;i++){
            sprintf(txt,"TT_%c%d_%d",side_char,j,i);
            if (SC_NET_FillRecover(&gRec[k][j][gRecs[k][j]],txt)) gRecs[k][j]++;
        }
        if (gRespawn_id[k][j]){ ... }
    }
}
```

Decompiled as a single flat loop with undefined `idx`, `idx29` variables.

### Test 2 (tdm.scr) — Simpler case, no deeply nested loops

tdm.scr doesn't have deeply nested for-loops. The inner loop in case 1 (`for i < 64`) is a single loop, so this fix won't change tdm output (neutral).

### Test 3 (LEVEL.SCR) — Nested village iteration

**Original (LEVEL.C lines 166-173):**
```c
for (i=0;i<4;i++)
    if (!g_vill_visited[i]){
        if (SC_IsNear2D(&g_will_pos[i],&pl_pos,80.0f)){
            g_vill_visited[i] = TRUE;
        }
    }
```

**Decompiled (LEVEL_decompiled.c lines 207-213):**
```c
for (i = 0; i < 4; i++) {
    if (! g_vill_visited[i]) {
    } else {
        t654_ret = SC_IsNear2D(&g_will_pos[i], &vec, 80.0f);
        g_vill_visited[i] = 1;
    }
}
```

The condition is inverted and the IsNear2D result is assigned to a temp instead of being used as a condition. This particular issue is more about if/else detection inside loop bodies, but the same body emission path is responsible.

## Proposed Fix

- **File:** `vcdecomp/core/ir/structure/emit/hierarchical_emitter.py`
- **Function:** `_emit_natural_for_loop()` (lines 614-668)
- **Change:** Before emitting a body block as flat statements, check if it's a loop header in `_loop_header_map`. If so, recursively call `_try_emit_natural_loop()` to emit it as a nested for/while loop instead of flat statements.

The same fix must be applied in `_try_emit_body_block_with_condition()` (line 862) which also calls `_emit_body_block_by_id()` for blocks inside if-branches within a loop body.

### Key Invariant

**General semantic invariant:** When emitting the body of a structured loop, any body block that is itself a loop header must be emitted as a nested loop structure, not as flat statements. This is the same principle Ghidra follows — inner structures are recognized before outer ones process their bodies.

## Expected Impact

- **tt:** IMPROVED — the triple-nested timer loop and respawn init loop should now emit as nested `for()` loops instead of flat code with orphaned variables. This fixes ~20 lines of broken output.
- **tdm:** UNCHANGED — no deeply nested for-loops exist in this test.
- **LEVEL:** IMPROVED — any loops nested inside other loops will be properly detected. The village iteration loop itself isn't nested inside another for-loop, so the primary benefit here is indirect (loop body emission improvements).

## Implementation Steps

1. **In `_emit_natural_for_loop()` (line 640-665):** Before calling `_emit_body_block_by_id()` at line 663, add a check: if `body_id in self._loop_header_map`, call `self._try_emit_natural_loop(self._loop_header_map[body_id], indent + "    ")` instead. If it returns lines, use those; if None (pattern detection failed), fall through to flat emission.

2. **In `_try_emit_body_block_with_condition()` (line 862):** Same check before calling `_emit_body_block_by_id()`: if the block is a loop header, try emitting as a nested loop first.

3. **Fix the pre-marking strategy:** In `_emit_natural_for_loop()` lines 620-624, the current code marks ALL body blocks as emitted before processing. This must be changed: only mark the CURRENT loop's blocks as "claimed" (to prevent other top-level emission), but inner loop headers must remain eligible for `_try_emit_natural_loop()`. Options:
   - Use a separate set (`_claimed_by_loop`) instead of `emitted_blocks` for pre-marking
   - OR: remove the body block from `emitted_blocks` before attempting nested loop detection
   - OR: pass a `force=True` equivalent to `_try_emit_natural_loop()` so it proceeds even for pre-marked blocks

4. **Handle the `_emitted_as_loop_body` set:** The `_try_emit_natural_loop()` code at line 395 skips blocks in `_emitted_as_loop_body`. Inner loop headers added by the outer loop's pre-marking will be skipped. Need to either:
   - Not add inner loop headers to `_emitted_as_loop_body` during pre-marking
   - OR: temporarily remove them when recursing

5. **Test all three:** Run decompilation on all 3 test files and verify no regressions.

## Risk Assessment

- **Low risk on tdm:** No nested loops, so output should be identical.
- **Medium risk on tt and LEVEL:** The recursive loop emission must correctly handle:
  - Shared blocks between inner and outer loops (back-edge targets)
  - Inner loop blocks being a subset of outer loop blocks
  - For-loop increment detection for inner loops (the increment block of the inner loop is also a body block of the outer loop)
