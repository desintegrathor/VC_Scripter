Now let me output the plan summary to the user:

# Implementation Plan - Iteration 4

## Selected Root-Cause Invariant

**When a CALL/XCALL return value has zero real uses (no instruction reads the returned value), the call must be emitted as a bare statement (`func(args);`) without a return-value assignment (`t###_ret = func(args);`).**

The current decompiler always emits `t###_ret = func(args);` when `inst.outputs` is non-empty, regardless of whether any subsequent code actually reads the return value. This produces 24+ spurious `t###_ret` assignments across all 3 tests.

## Evidence

| Test | Affected Lines | Examples |
|------|---------------|----------|
| tt.scr | 16 | `t2286_ret = sprintf(...)` should be `sprintf(...)` |
| tdm.scr | 2 | `t504_ret = sprintf(...)` should be `sprintf(...)` |
| LEVEL.SCR | 6 | `t625_ret = SC_PC_GetPos(...)` should be `SC_PC_GetPos(...)` |

The original source uses bare calls: `sprintf(txt, "TT_flag_%d", i);` — the return value is never captured.

Functions affected: `sprintf`, `swprintf`, `SC_AnsiToUni`, `SC_PC_GetPos`, `SC_GetWp`, `SC_P_GetPos`, `SC_Item_Create2`, `SC_VectorLen`

## Proposed Fix

- **File:** `vcdecomp/core/ir/expr.py`
- **Function:** `_format_call()` (both CALL and XCALL branches)
- **Change:** Check `real_uses = sum(1 for addr, _ in output.uses if addr >= 0)`. If zero, emit bare `func(args);` without the `dest = ` prefix.

## Expected Impact
- **tt:** IMPROVED (16 fewer `t###_ret` assignments)
- **tdm:** IMPROVED (2 fewer)
- **LEVEL:** IMPROVED (6 fewer, plus eliminates downstream confusion like `func_0448(t870_ret)`)

## Next Priority (do NOT fix yet)
- Nested for-loop destruction: the triple-nested `for(i) for(j) for(k)` pattern in tt.scr's gRecTimer update is completely collapsed into one flat loop. Requires loop nesting hierarchy in the collapse engine.
(&local_67, &g_will_pos[i]);
```

**Original (CORRECT):**
```c
// LEVEL.C line 164: bare call
SC_PC_GetPos(&pl_pos);
// LEVEL.C line 499: bare call
sprintf(txt,"WP_will%d",i+1);
// LEVEL.C line 500: bare call
SC_GetWp(txt,&g_will_pos[i]);
```

## Proposed Fix

- **File:** `vcdecomp/core/ir/expr.py`
- **Function:** `_format_call()` (lines 4031-4213)
- **Change:** Before emitting `dest = func(args);`, check if the return value has zero real uses. If so, emit `func(args);` instead.

The check: count `real_uses = sum(1 for addr, _ in output.uses if addr >= 0)`. If `real_uses == 0`, omit the assignment prefix.

This is the **same metric** already used at line 1506 in `_render_value_impl()` but applied at the emit-as-statement level instead of the inline-as-expression level.

## Expected Impact

- **tt:** IMPROVED - 16 `t###_ret = func(...)` become bare `func(...)` calls. This removes 16 undeclared variable references and makes the output match the original source structure.
- **tdm:** IMPROVED - 2 instances fixed.
- **LEVEL:** IMPROVED - 6 instances fixed. Additionally, fixes like `t625_ret = SC_PC_GetPos(&vec)` -> `SC_PC_GetPos(&vec)` also eliminate downstream confusion where `t625_ret` is incorrectly passed as an argument (e.g., `func_0448(t870_ret)` becomes `func_0448()` because `SC_PC_GetPos` return is not an argument to GetPilot).

**Regression risk:** LOW. This only changes the rendering of calls whose return value is demonstrably unused. It does NOT affect calls where the return IS used (like `SC_MP_EnumPlayers` where the return is checked in `if()`).

## Implementation Steps

1. **In `_format_call()` (CALL branch, around line 4058):** Before the `if inst.outputs:` check, count real uses of the output. If zero real uses, treat as no output.

2. **In `_format_call()` (XCALL branch, around line 4198):** Same change - check real uses before emitting assignment.

3. **Define "real uses":** `real_uses = sum(1 for addr, _ in output.uses if addr >= 0)` - this counts only actual code references, not SSA construction artifacts (PHI markers have negative addresses).

4. **Run all three test decompilations** and verify:
   - `t###_ret = sprintf(...)` -> `sprintf(...)`
   - `t###_ret = SC_AnsiToUni(...)` -> `SC_AnsiToUni(...)`
   - `t###_ret = SC_PC_GetPos(...)` -> `SC_PC_GetPos(...)`
   - Return values that ARE used (like `SC_MP_EnumPlayers` in conditions) remain unchanged.

5. **Run `py -3 -m pytest vcdecomp/tests/test_structure_patterns.py -v`** to check for regressions.
