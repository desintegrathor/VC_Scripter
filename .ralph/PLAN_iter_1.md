=== ITERATION SUMMARY ===

**1. ROOT-CAUSE INVARIANT:**
The `is_local_var` guard in `_detect_array_indexing()` (expr.py:2829-2855) unconditionally blocks local variable array/struct field notation when no pre-existing type tracker evidence exists. This causes `ADD(LADR(base), offset)` patterns — which are inherently evidence of array or struct access — to fall through to raw pointer arithmetic rendering (`(&base) + offset`).

**2. EVIDENCE:**
- **tt.scr**: 3 instances — `(&local_296) + 4 = 0` (should be `side[1] = FALSE`), `(&local_296) + ((*tmp27)) * 4 = 1` (should be `side[enum_pl[i].side] = TRUE`), `(&local_63) + i * 4 = i` (should be `fol_ord[i] = i`)
- **tdm.scr**: 0 instances (unaffected)
- **LEVEL.SCR**: 6 instances — `(&local_3) + 4 = local_5` (should be `dist[1] = dist[0]`), `(&local_63) + 4 = 3490` (should be `fol_ord[1] = 3490`), etc.

**3. CODE CHANGES:**
Two changes in `vcdecomp/core/ir/expr.py`:
1. In `_detect_array_indexing()`: allow MUL-based indexing through the `is_local_var` guard (MUL is definitive array evidence)
2. In `_format_pointer_target()`: add handler for `ADD(LADR(base), const_offset)` to produce `base.field_N` as a fallback (mirrors existing DADR handler)

**4. REGRESSION REPORT:**
- tt: predicted IMPROVED (3 instances fixed)
- tdm: predicted UNCHANGED (0 instances of this pattern)
- LEVEL: predicted IMPROVED (6 instances fixed)

**5. NEXT PRIORITY:**
Missing function call inlining for `has_out_params` calls (`t###_ret` variables like `t1157_ret` used without being assigned from their `SC_MP_EnumPlayers` call) — affects all three tests
