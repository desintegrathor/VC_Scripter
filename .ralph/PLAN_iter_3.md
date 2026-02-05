## Summary

Here is the implementation plan for Iteration 3:

---

# Implementation Plan - Iteration 3

## Selected Root-Cause Invariant

**SDK struct array fields store total byte size in `field.size` instead of element size, causing `get_verified_field_name()` to always compute array index 0 for every element access.**

The SDK parser (`sdk_parser.py:302`) stores `field_size = base_size * array_size` (total bytes), but `get_verified_field_name()` (`structures.py:599`) divides offset by `field.size` as if it were the element size:

```python
index = (offset - field.offset) // field.size  # BUG: divides by total, always 0
```

For `sort_by` (offset=40, size=20, array_size=5):
- offset 44 → (44-40)//20 = **0** (should be 1)
- offset 48 → (48-40)//20 = **0** (should be 2)

## Evidence

All three tests affected. In **tt.scr** and **tdm.scr**, the `s_SC_MP_hud` struct initialization shows:
- `sort_by[0]` repeated for what should be `sort_by[0]`, `sort_by[1]`, `sort_by[2]`, `sort_by[3]`
- `side_name[0]` for what should be `side_name[1]` (offset 20, index=(20-16)//8=0 instead of (20-16)//4=1)
- `side_color` indices similarly wrong

ASM confirms PNT+ADD patterns produce correct total offsets (40+0, 40+4, 40+8, etc.) but the final index lookup in structures.py divides by total array size instead of element size.

## Proposed Fix

- **File:** `vcdecomp/core/structures.py`, function `get_verified_field_name()` (lines 596-600)
- Compute `element_size = field.size // field.array_size`
- Fix `field_end = field.offset + field.size` (total size is already field.size)
- Fix `index = (offset - field.offset) // element_size`

## Expected Impact

- **tt:** IMPROVED (~11 wrong field references fixed)
- **tdm:** IMPROVED (~11 wrong field references fixed)
- **LEVEL:** IMPROVED (array field indices in s_SC_Ai_PlFollow and others corrected)

No regressions expected — only corrects array index from always-0 to the mathematically correct value.

## Implementation Steps

1. Fix `get_verified_field_name()` SDK path (lines 596-600)
2. Verify built-in struct path (lines 43-56) is already correct (it uses element size)
3. Run all 3 test decompilations
4. Run pytest

The full plan with ASM evidence is in `.ralph/PLAN_iter_3.md`.
 offset 24
hudinfo.side_name[1] = 1011;                            // offset 20
hudinfo.side_color[1] = 0x44ff0000;                     // offset 28
```

**ASM (ground truth):**
```
PNT 40, GCP 0, ADD -> offset 40 (sort_by[0])
PNT 40, GCP 4, ADD -> offset 44 (sort_by[1])
PNT 40, GCP 8, ADD -> offset 48 (sort_by[2])
PNT 40, GCP 12, ADD -> offset 52 (sort_by[3])
PNT 32, ASGN -> offset 32 (pl_mask)
PNT 16, GCP 0, ADD -> offset 16 (side_name[0])
PNT 24, GCP 0, ADD -> offset 24 (side_color[0])
PNT 16, GCP 4, ADD -> offset 20 (side_name[1])
PNT 24, GCP 4, ADD -> offset 28 (side_color[1])
```

### Test 2 (tdm.scr) - identical hudinfo bug

Same pattern as Test 1. All sort_by, side_name, side_color array indices are wrong.

### Test 3 (LEVEL.SCR) - s_SC_Ai_PlFollow follow_change

The `follow_change` field (offset 24, size=44, array_size=11) would similarly have wrong indices, though the visible impact is through the ZeroMem call pattern.

## Proposed Fix

### Primary Fix
- **File:** `vcdecomp/core/structures.py`
- **Function:** `get_verified_field_name()` (line 597-600)
- **Change:** Compute element size as `field.size // field.array_size` instead of using `field.size` directly for both `field_end` and index calculation.

```python
# BEFORE (buggy):
field_end = field.offset + (field.size * field.array_size)  # total * count = way too big
index = (offset - field.offset) // field.size               # divides by total, always 0

# AFTER (fixed):
element_size = field.size // field.array_size if field.array_size > 0 else field.size
field_end = field.offset + field.size  # field.size IS total size already
index = (offset - field.offset) // element_size  # divides by element size
```

### Secondary Fix (same bug, different code path)
- **File:** `vcdecomp/core/structures.py`
- **Functions:** `get_field_at_offset()` (line 44) and `get_field_name_at_offset()` (line 55)
- **Change:** These use built-in `StructField` where `size` IS element size and `array_count` IS count, so `field.size * field.array_count` is correct. No change needed here.

### Alternative approach (NOT recommended): Fix the parser
- **File:** `vcdecomp/sdk/sdk_parser.py`
- **Line 302:** Could change to store element size: `field_size = base_size`
- **Risk:** This changes the JSON format semantics; all downstream code depending on field.size would need audit. Riskier than fixing the consumer.

## Expected Impact

- **tt:** IMPROVED - All hudinfo struct field assignments will have correct indices (sort_by[0..3], side_name[0..1], side_color[0..1]). Approximately 11 wrong field references fixed.
- **tdm:** IMPROVED - Same hudinfo fix. Approximately 11 wrong field references fixed.
- **LEVEL:** IMPROVED - Any SDK array field accesses will have correct indices. The s_SC_Ai_PlFollow.follow_change and similar array fields will render correctly.

No regressions expected since this only changes the array index computation from always-0 to the correct value.

## Implementation Steps

1. **Read and understand the existing code** at `structures.py` lines 37-57 (built-in path) and lines 581-609 (SDK path) to confirm which `size` semantics each uses.

2. **Fix `get_verified_field_name()` in `structures.py`** (SDK path, lines 596-600):
   - Compute `element_size = field.size // field.array_size` when `field.array_size > 0`
   - Fix `field_end = field.offset + field.size` (since field.size is already total size)
   - Fix `index = (offset - field.offset) // element_size`

3. **Verify built-in struct path** at lines 43-46 and 54-56:
   - The built-in `StructField` uses element size in `size` and element count in `array_count`
   - Confirm the formulas are correct for this different convention
   - No change needed if already correct

4. **Run all three test decompilations** and verify:
   - sort_by[0], sort_by[1], sort_by[2], sort_by[3] have correct indices
   - side_name[0], side_name[1] have correct indices
   - side_color[0], side_color[1] have correct indices
   - No regressions in other struct field accesses

5. **Run pytest** to check for test regressions.
