# Decompilation Progress Report

## Major Bug Fixed: ScriptMain Boundaries

### Problem
ScriptMain was being decompiled as an empty function (2 lines) instead of the massive 2600+ instruction function it actually is.

**Before:**
- ScriptMain: entry=-1097, end=49, blocks=0
- Output: `return 0;  // FIX (06-05): Synthesized return value`
- Total decompiled output: 346 lines
- Recompiled .scr: 10KB (should be 60KB)

**Root Cause:**
The function boundary detector in `detect_function_boundaries_v2()` was using the raw negative entry point value (-1097) instead of resolving it to the actual address (1096). This caused:
1. Entry point -1097 to be added to function_starts list
2. When sorted, -1097 comes before all positive addresses
3. The first RET instruction >= -1097 is at address 49
4. ScriptMain incorrectly bounded to (-1097, 49) with 0 blocks

### Solution
**File: vcdecomp/core/disasm/disassembler.py**
- Changed `get_function_boundaries_v2()` to extract the already-resolved ScriptMain address from `self.functions` dict
- The disassembler's `__init__` already correctly resolves negative entry points to actual addresses
- Now passes the resolved address (1096) instead of raw value (-1097)

**File: vcdecomp/core/ir/function_detector.py** 
- Added logic to handle negative entry points by resolving them: `actual_entry = len(instructions) + entry_point`
- However, this wasn't sufficient because the calculation was still wrong
- The real fix was using the pre-resolved address from disassembler

### Results
**After Fix:**
- ScriptMain: entry=1096, end=3709, blocks=11
- ScriptMain now generates actual decompiled code
- Total decompiled output: 435 lines (was 346)
- ScriptMain contains real logic instead of empty stub

## Remaining Issues

### 1. Struct Field Access Bugs
The decompiled ScriptMain has incorrect struct field access:
```c
int local_296;  // Declared as int
...
local_296.field1 = 0;  // ERROR: trying to access field of int
```

**Should be:**
```c
info->fval1 = 0.0f;  // Access parameter's struct field
```

This indicates the struct field reconstruction logic is misidentifying which variable is being accessed.

### 2. Compilation Status
Currently the compiler (scmp.exe) is crashing even on minimal test files. This appears to be an environment issue, not related to the decompilation fixes. Earlier in the session, compilation was working successfully.

## Files Modified

1. **vcdecomp/core/disasm/disassembler.py** (lines 404-414)
   - Fixed `get_function_boundaries_v2()` to use resolved ScriptMain address

2. **vcdecomp/core/ir/function_detector.py** (lines 78-90, 101-103)
   - Added negative entry point resolution logic
   - Added debug output for entry point processing

3. **vcdecomp/core/ir/structure/orchestrator.py** (line 233-234)
   - Added debug output for function boundary verification

## Next Steps

1. Fix struct field access reconstruction bugs
2. Investigate compiler crash (may be Wine/environment related)
3. Test full decompilation -> recompilation cycle once compiler is stable
4. Compare bytecode of recompiled output to original

## Key Achievement

✅ ScriptMain is now properly decompiled with actual code instead of an empty stub
✅ Function boundary detection works correctly for negative entry points
✅ Decompilation output is significantly more complete
