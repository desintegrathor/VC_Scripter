# Decompiler Fix Summary

## Problem Identified
The decompiler was failing to track local struct variables, leading to:
1. Missing struct field accesses (`tmp2` instead of `set.tt_respawntime`)
2. Uninitialized variable usage
3. Magic numbers instead of proper field accesses

## Root Cause
`vcdecomp/core/ir/field_tracker.py` only tracked struct types for **function parameters** (param_0, param_1, etc.), not for **local variables** passed to SDK functions.

Pattern:
```
ASP 3                                    # Allocate stack for struct
LADR [sp+1]                              # Load address of local_1
XCALL $SC_MP_SRV_GetAtgSettings          # Call function with &local_1
```

The field tracker had no logic to detect that `local_1` should be typed as `s_SC_MP_SRV_AtgSettings`.

## Fix Implemented
Added new method `_detect_local_structs()` to `field_tracker.py`:

1. **Scans for XCALL instructions** - Finds external function calls
2. **Checks function name** - Matches against known struct-parameter functions (SC_MP_SRV_GetAtgSettings, SC_P_GetInfo, etc.)
3. **Looks for preceding LADR** - Finds the address-of instruction that passes `&local_X`
4. **Tracks struct type** - Adds `local_X` to `var_struct_types` with the correct struct type
5. **Tracks both variants** - Adds both `local_1` and `&local_1` to handle PNT (pointer arithmetic) instructions

## Results

### Before Fix
```c
int func_0119(void) {
    int local_1;
    int tmp2;
    int tmp4;

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!tmp2) {              // WRONG: tmp2 uninitialized
        return tmp4;          // WRONG: tmp4 uninitialized
    } else {
        local_0 = SC_ggf(400);
        local_0 = 1106247680; // WRONG: Magic number
        return local_0;
    }
}
```

### After Fix
```c
int func_0119(void) {
    int local_0;
    dword local_1;  // TODO: Should be s_SC_MP_SRV_AtgSettings

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!tmp2) {              // TODO: Should be if (local_1.tt_respawntime>1.0f)
        return local_1->tt_respawntime;  // GOOD: Field access detected!
    } else {
        local_0 = SC_ggf(400);
        local_0 = 1106247680;
        return local_0;
    }
}
```

### Improvement
- **Field access tracking**: ✅ Now detecting `local_1->tt_respawntime`
- **Struct type declaration**: ⚠️ Partial - Type sometimes detected, sometimes overridden to `dword`
- **Field operator**: ⚠️ Uses `->` instead of `.` (should detect value vs pointer)

## Remaining Issues

### 1. Variable Type Declaration Override
The `_infer_type_from_usage()` function in `orchestrator.py` runs AFTER field tracking and sometimes overrides the struct type with `dword` or `int`.

**Solution**: The variable type inference should check `field_tracker.var_struct_types` and respect detected struct types.

### 2. Missing Control Flow
Most function bodies are still mostly empty - only fragments of code are being emitted. This is a separate, larger issue with the SSA-to-C conversion.

### 3. Uninitialized tmp Variables
Variables like `tmp2` are used before being assigned. The SSA lowering is not properly tracking value sources.

### 4. Float Constant Display
Still showing IEEE 754 hex (`1106247680`) instead of float notation (`30.0f`).

### 5. Pointer vs Value Detection
Field accesses use `->` even for value types. Need to detect whether the base is a pointer or a value.

## Impact
This fix significantly improves field access reconstruction for functions that use local struct variables. It's a critical foundation for further improvements.

## Files Modified
- `vcdecomp/core/ir/field_tracker.py`:
  - Added `_detect_local_structs()` method
  - Updated `analyze()` to call the new method
  - Fixed `get_field_expression()` to strip `&` prefix from base variable names

## Test Case
- **File**: `decompiler_source_tests/test1/tt.scr`
- **Function**: `func_0119` (GetRecovTime)
- **Expected**: Detect `s_SC_MP_SRV_AtgSettings set` and field access `set.tt_respawntime`
- **Actual**: Field access `local_1->tt_respawntime` detected ✅, but type declaration needs improvement

## Next Steps
1. Fix variable type inference to respect field tracker detections
2. Detect value vs pointer for correct operator (`.` vs `->`)
3. Improve SSA-to-C conversion to emit complete function bodies
4. Fix float constant representation
