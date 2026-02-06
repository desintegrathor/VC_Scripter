The implementation plan is written to `.ralph/PLAN_iter_2.md`. Here's the summary:

---

## Iteration 2 - Planning Complete

### Root-Cause Invariant
**Every XCALL/CALL must appear exactly once in the output — either as a standalone statement or inlined at its use-site.** The `should_emit` gate at `expr.py:4658-4663` skips emission for XCALLs whose return values are "inlinable" (`_can_inline()` returns True). But actual inlining at `_render_value_impl()` only works when `real_uses == 1`. When real_uses != 1, the call is **neither emitted nor inlined**, producing undefined `t###_ret` variables.

### Impact: 38 undefined variables across all 3 tests
- **tt.scr**: 13 `t###_ret` occurrences (SC_MP_EnumPlayers, SC_IsNear3D, SC_NET_FillRecover, SC_GetScriptHelper missing)
- **tdm.scr**: 4 `t###_ret` occurrences (SC_MP_EnumPlayers, SC_NET_FillRecover missing)
- **LEVEL.SCR**: 21 `t###_ret` occurrences (SC_2VectorsDist, SC_IsNear2D, etc. missing)

### Fix Location
- **Primary**: `vcdecomp/core/ir/expr.py:4658-4663` — tighten `should_emit` to only skip XCALLs when `real_uses == 1` (guaranteeing inlining succeeds)
- **Secondary**: Same file, `_render_value_impl()` — improve inlining for condition contexts

### Expected Outcome
All 3 tests improved, no regressions expected. This is a pure correctness fix — XCALLs that were silently dropped will now appear in output.
ines 487-488):**
```c
local_12 = 64;
if (t1157_ret) {
```

**Original (lines 499-504):**
```c
pls = 64;
if (SC_MP_EnumPlayers(enum_pl, &pls, SC_MP_ENUMPLAYER_SIDE_ALL)) {
    if ((pls==0) && ...
```

**Mismatch:** Same pattern -- `SC_MP_EnumPlayers(...)` call completely missing.

---

**Decompiled (line 534):**
```c
if (t1576_ret) {
```

**Original (line 617):**
```c
if (SC_IsNear3D(&pos, &gStepSwitch[j].pos, gStepSwitch[j].rad)) {
```

**Mismatch:** `SC_IsNear3D(...)` call missing. Return value `t1576_ret` used but never defined.

---

**Decompiled (lines 740, 767):**
```c
if (t2513_ret) {        // SC_NET_FillRecover() missing
if (!t2769_ret) {       // SC_GetScriptHelper() missing
```

### LEVEL.SCR (test3)

**Decompiled (line 626):**
```c
if (t2484_ret < 40.0f) {
```

**Original (line 753):**
```c
if (SC_2VectorsDist(&vec, &g_will_pos[i]) < 40.0f) {
```

**Mismatch:** `SC_2VectorsDist(...)` call missing.

---

**Decompiled (lines 172-175):**
```c
t870_ret = SC_PC_GetPos(&vec);
SC_P_GetPos(func_0448(t870_ret), &vec2);
t886_ret = SC_IsNear2D(&vec, &vec2, 50.0f);
if (! t886_ret) break;
```

**Original (lines 231-235):**
```c
SC_PC_GetPos(&pl_pos);
SC_P_GetPos(GetPilot(), &vec);
if (SC_IsNear2D(&pl_pos, &vec, 50.0f)) {
```

**Mismatch:** `SC_IsNear2D(...)` emitted as statement but should be inlined into `if` condition. Also `SC_PC_GetPos` return (void) incorrectly used as arg to `func_0448`.

## Proposed Fix

- **File:** `vcdecomp/core/ir/expr.py`
- **Function:** `format_block_expressions()` (line 4658-4663)
- **Change:** Tighten the `should_emit` gate to only skip XCALLs when inlining is **guaranteed** to succeed (i.e., the output has exactly 1 real use AND `_can_inline()` returns True). When `real_uses > 1` or inlining would fail, always emit the XCALL as a statement with return value assignment.

### Secondary fix in same function:
- **Function:** `_render_value_impl()` (line 1500-1508)
- **Change:** Remove the `real_uses == 1` restriction for XCALL/CALL inlining in conditions. When a function call return value is used in a condition context (IN_CONDITION) and has no out params, always inline it regardless of use count. This enables `if (SC_IsNear3D(...))` instead of `t886_ret = SC_IsNear3D(...); if (!t886_ret)`.

## Expected Impact

- **tt:** Improved -- ~5 missing function calls will be emitted (SC_MP_EnumPlayers, SC_IsNear3D, SC_NET_FillRecover, SC_GetScriptHelper). t1157_ret, t1576_ret, t2513_ret, t2769_ret resolved.
- **tdm:** Improved -- 2 missing function calls will be emitted (SC_MP_EnumPlayers, SC_NET_FillRecover). t184_ret, t516_ret resolved.
- **LEVEL:** Improved -- ~4 missing function calls emitted or inlined (SC_2VectorsDist, SC_IsNear2D, etc). t2484_ret, t654_ret, t886_ret resolved.

## Implementation Steps

1. **Read and understand the current `should_emit` logic at expr.py:4658-4663**
   - Confirm the exact condition that causes XCALLs to be skipped

2. **Fix the emission gate (expr.py:4658-4663)**
   - For XCALL/CALL: only skip if ALL outputs have exactly 1 real use (meaning inlining will succeed)
   - New logic:
     ```python
     if inst.mnemonic in {"CALL", "XCALL"}:
         has_out_params = inst.metadata.get("has_out_params", False) if inst.metadata else False
         if has_out_params:
             should_emit = True  # Must emit for side effects
         else:
             # Only skip if ALL outputs will be successfully inlined (single real-use each)
             will_inline = all(
                 sum(1 for addr, _ in val.uses if addr >= 0) == 1
                 for val in inst.outputs
             ) if inst.outputs else False
             should_emit = not will_inline
     else:
         should_emit = not inst.outputs or not all(
             formatter._can_inline(val) for val in inst.outputs
         )
     if not should_emit:
         continue
     ```

3. **When emitting a non-inlined XCALL as statement, emit with return value assignment**
   - Currently, non-inlined XCALLs fall through to `_format_call()` at line 4780
   - If the XCALL has outputs that are used (real_uses > 0), emit as `t###_ret = func(...);`
   - Check if `_format_call()` already handles this or needs modification

4. **Run all three tests to verify improvements**
   - Confirm t###_ret count decreases
   - Check for regressions (no duplicate emissions)

5. **Handle edge case: ensure no double-emission**
   - When should_emit=True forces statement emission, the inlining path at _render_value_impl line 1500-1508 must NOT also inline, otherwise the call appears twice
   - The `real_uses == 1` guard already prevents this for multi-use values
   - For single-use values: the statement emission means the value is resolved, so inlining shouldn't trigger (the value is already emitted)

6. **Regression test with pytest**
   - `py -3 -m pytest vcdecomp/tests/test_structure_patterns.py -v`
