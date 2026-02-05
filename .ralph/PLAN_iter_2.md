Here's the analysis summary and plan:

---

# Implementation Plan - Iteration 2

## Selected Root-Cause Invariant

**`get_verified_field_name()` in `structures.py` fails to resolve struct fields due to (A) exact-match-only offset lookup that misses array elements, and (B) returning `None` when the header parser provides conflicting (wrong) offsets against the SDK database.**

## Evidence

**39 total `field_N` occurrences** across all 3 tests (25 in tt, 12 in tdm, 2 in LEVEL) that should all be proper field names.

Verified with direct testing:
- `get_verified_field_name('s_SC_NET_info', 4)` → `None` (should be `param1`) — SDK/header conflict
- `get_verified_field_name('s_SC_MP_hud', 44)` → `None` (should be `sort_by[1]`) — array element miss
- `get_verified_field_name('s_SC_P_getinfo', 8)` → `None` (should be `side`) — SDK/header conflict

## Proposed Fix

**File:** `vcdecomp/core/structures.py`, function `get_verified_field_name()`

Two changes:
1. Use existing `sdk_struct.get_field_name_at_offset(offset)` instead of manual exact-match loop (fixes array elements)
2. Trust SDK as authoritative — return its result directly without requiring header parser agreement (fixes conflicts)

## Expected Impact
- **tt:** IMPROVED (~25 `field_N` resolved)
- **tdm:** IMPROVED (~12 `field_N` resolved)
- **LEVEL:** IMPROVED (~2 `field_N` resolved)
- No regressions expected — only adding names where `None` was returned

The full plan is in `.ralph/PLAN_iter_2.md`.
_4;
```
**Original (line 148):**
```c
gEndRule = info->param1;
```
Same `s_SC_NET_info` offset 4 conflict as tt.

**Decompiled (line 156):**
```c
local_10 = player_info.field_8;
```
**Original (line 260):**
```c
sideA = plinfo.side;
```
Same `s_SC_P_getinfo` offset 8 conflict.

### Test 3 (LEVEL) - 2 occurrences of `field_N`

**Decompiled (line 643):**
```c
if (info->field_4 >= 20) {
```
**Original (line 928):**
```c
if (info->param1>= MAX_MUSICS){
```
Same `s_SC_L_info`/`s_SC_NET_info` offset conflict.

### Verified Test Cases

```
FAIL: get_verified_field_name('s_SC_NET_info', 0) = None  (should be 'message')
FAIL: get_verified_field_name('s_SC_NET_info', 4) = None  (should be 'param1')
FAIL: get_verified_field_name('s_SC_P_getinfo', 8) = None  (should be 'side')
FAIL: get_verified_field_name('s_SC_MP_hud', 44) = None   (should be 'sort_by[1]')
FAIL: get_verified_field_name('s_SC_MP_hud', 48) = None   (should be 'sort_by[2]')
FAIL: get_verified_field_name('s_SC_MP_hud', 20) = None   (should be 'side_name[1]')
FAIL: get_verified_field_name('s_SC_MP_hud', 28) = None   (should be 'side_color[1]')
```

Header parser produces WRONG offsets:
- `s_SC_NET_info`: Header says `elapsed_time` at 0, `fval1` at 4 (SDK says `message` at 0, `param1` at 4)
- `s_SC_P_getinfo`: Header says `side` at 0, `member_id` at 8 (SDK says `side` at 8)

## Proposed Fix

- **File:** `vcdecomp/core/structures.py`
- **Function:** `get_verified_field_name()`
- **Change:** Two-part fix:
  1. Use `StructDef.get_field_name_at_offset()` for SDK lookup (already handles arrays correctly)
  2. Trust SDK database as authoritative when it has a result - don't let header parser conflicts override it

### General Invariant

**SDK struct definitions are the authoritative source for field offset-to-name mapping. Array element offsets must be resolved through range-based matching, not exact-match only. When the authoritative source provides a result, secondary sources that conflict should not veto it.**

## Expected Impact

- **tt:** IMPROVED - ~25 `field_N` → resolved to proper names (param1, side, sort_by[1], side_name[1], etc.)
- **tdm:** IMPROVED - ~12 `field_N` → resolved to proper names
- **LEVEL:** IMPROVED - ~2 `field_N` → resolved to proper names
- **Total:** ~39 `field_N` occurrences eliminated across all tests
- **No regressions expected** - only adding field name resolution where it currently returns `None`

## Implementation Steps

1. **Read** `vcdecomp/core/structures.py` lines 581-611 (`get_verified_field_name`)
2. **Modify** SDK lookup to use `sdk_struct.get_field_name_at_offset(offset)` instead of the manual exact-match loop
   - This reuses the existing correct array-aware logic at lines 49-57
   - Handles `sort_by[1]`, `side_name[1]`, `side_color[1]` etc.
3. **Modify** conflict resolution: When SDK provides a name, return it directly without requiring header parser agreement
   - SDK is curated and authoritative
   - Header parser has known bugs with offset calculation
   - Still allow header parser to fill gaps where SDK has no entry
4. **Run** all three test decompilations
5. **Verify** reduction in `field_N` count and no regressions

### The Fix (pseudocode)

```python
def get_verified_field_name(struct_name: str, offset: int) -> Optional[str]:
    sdk_db = _get_sdk_database()
    if sdk_db:
        sdk_struct = sdk_db.get_structure(struct_name)
        if sdk_struct:
            name = sdk_struct.get_field_name_at_offset(offset)
            if name:
                return name  # SDK is authoritative, return directly

    # Fallback: try header parser
    db = get_header_database()
    header_fields = db.get_struct_fields(struct_name)
    field_info = header_fields.get(offset)
    if field_info:
        return field_info.name

    return None
```
