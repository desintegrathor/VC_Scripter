# Root Cause Analysis: Pilot Script Switch Detection Failure

## Problem Summary

The Pilot script decompilation produces completely wrong control flow:
- **Expected**: `switch(info->message)` with cases for `SC_LEV_MES_TIME`, `SC_LEV_MES_RADIOUSED`, etc.
- **Actual**: `switch(g_showinfo_timer)` with wrong case structure

## Investigation Findings

### Assembly Analysis

**Lines 1081-1089 in LEVEL.asm (ScriptMain function):**
```assembly
1081: LADR     [sp-4]               ; Load address of 'info' parameter
1082: DADR     0                    ; Add offset 0 (info->message)
1083: DCP      4                    ; Dereference: load info->message value
1084: JMP      label_1086           ; ⚠️ Unconditional jump - loaded value NOT USED!
1085: JMP      label_1090           ; ⚠️ Dead code?
label_1086:
1086: LCP      [sp+87]              ; Load local variable (g_showinfo_timer)
1087: GCP      data[396]             ; Load constant 0.0f
1088: EQU                           ; Compare (float comparison!)
1089: JZ       label_2739           ; Jump if not equal
```

**Key Observations:**

1. **info->message IS loaded** (lines 1081-1083) but immediately **discarded** by unconditional JMP (line 1084)
2. The next comparison (lines 1086-1089) switches to a **different variable** `[sp+87]`
3. This is a **FLOAT comparison** (`data[396] = 0.0f`) not integer
4. Variable `[sp+87]` is `g_showinfo_timer` (a local float), not `info->message`

### Why This Happens

The switch pattern detector in `switch_case.py` looks for:
1. Multiple blocks with **EQU comparisons** on the **same variable**
2. Each comparison to a **constant value**
3. Conditional jumps to case bodies

**The problem:**
- The detector finds the EQU comparison at line 1088
- It identifies `[sp+87]` (g_showinfo_timer) as the switch variable
- It treats this as the main switch statement
- The actual `info->message` load is **ignored** because it's followed by an unconditional jump

### Compiler Optimization Theory

The compiler may have:
1. **Inlined or optimized** the switch statement in a non-standard way
2. Used a **jump table** that the decompiler doesn't recognize
3. **Reordered code** so that different message handlers appear as separate switches

### Original Source Structure

```c
int ScriptMain(s_SC_L_info *info) {
    // ...
    switch(info->message) {
        case SC_LEV_MES_TIME:      // 0
            // ... nested switch(gphase) ...
            switch(gphase) {
                case 0: // init
                case 1: // gameplay
                    // ... nested switch(SC_ggi(SGI_LEVELPHASE)) ...
                    switch(SC_ggi(SGI_LEVELPHASE)) {
                        case 0: // in heli
                            // ... nested switch(g_dialog) ...
                        case 1: // searching
                        case 2: // pilot found
                        // ...
                    }
            }
            break;
        case SC_LEV_MES_RADIOUSED:  // 1
            // ...
            break;
        case SC_LEV_MES_SPEACHDONE: // 2
            break;
        case SC_LEV_MES_EVENT:      // 4
            break;
        case SC_LEV_MES_INITSCENE:  // 7
            break;
        case SC_LEV_MES_JUSTLOADED: // 11
            break;
        case SC_LEV_MES_GETMUSIC:   // 15
            break;
    }
}
```

**The original has 4 levels of nesting:**
1. `switch(info->message)` - main message handler
2. `switch(gphase)` - game phase (inside TIME message)
3. `switch(SC_ggi(SGI_LEVELPHASE))` - level phase (inside gphase 1)
4. `switch(g_dialog)` - dialog state (inside level phase 0)

### What the Decompiler Sees

The decompiler is detecting:
- A switch on `g_showinfo_timer` (WRONG - this is a float timer, not a message enum)
- Multiple duplicate switches on the same variable (artifact of failed pattern detection)
- Cases with mostly empty bodies (because the real code is misattributed)

## Root Causes Identified

### 1. Dead Code / Optimization Detection ❌

**File**: `vcdecomp/core/ir/cfg.py` (CFG construction)

**Problem**: The decompiler doesn't recognize that lines 1081-1083 load a value that's immediately discarded.

**Impact**: The loaded `info->message` value is lost, never used in switch detection.

### 2. Switch Variable Tracing ❌

**File**: `vcdecomp/core/ir/structure/patterns/switch_case.py` (lines 298-316)

**Problem**: The switch detector traces back from EQU comparisons to find the switch variable. It finds `[sp+87]` but doesn't realize this is a LOCAL variable, not a PARAMETER FIELD.

**Current logic:**
```python
var_name = _trace_value_to_parameter(var_value, formatter, ssa_func)
if not var_name:
    var_name = _trace_value_to_global(var_value, formatter)
if not var_name:
    var_name = _find_switch_variable_from_nearby_gcp(...)
if not var_name:
    var_name = formatter.render_value(var_value)  # Falls back to local variable name
```

**Missing**: Detection of parameter **field access** (`info->message` vs just `info`)

### 3. Type-Based Filtering ❌

**File**: `vcdecomp/core/ir/structure/patterns/switch_case.py` (line 293)

**Problem**: The detector checks for `mnemonic == "EQU"` but doesn't verify it's an **integer comparison**, not float.

**Evidence**: Line 1088 shows EQU comparing to `0.0f` (float), which shouldn't be a switch case value.

### 4. Multiple Switch Prioritization ❌

**Problem**: When multiple potential switches exist, the detector picks the first one it finds, not the most likely "main" switch.

**Impact**: It picks the `g_showinfo_timer` switch instead of the `info->message` switch.

## Required Fixes

### Fix 1: Detect Parameter Field Access

**Location**: `vcdecomp/core/ir/structure/analysis/value_trace.py`

**Add**: New function `_trace_value_to_parameter_field()` that:
1. Traces value back through DADR (field offset add)
2. Identifies the base parameter
3. Returns formatted name like `info->message`

**Example**:
```python
def _trace_value_to_parameter_field(value, formatter, ssa_func):
    # Find producer of 'value'
    for block in ssa_func.instructions.values():
        for inst in block:
            for out in inst.outputs:
                if out.name == value.name:
                    # Found producer
                    if inst.mnemonic == "DCP":  # Dereference pointer
                        # Check if input is from DADR
                        ptr_value = inst.inputs[0]
                        return _trace_dadr_to_param_field(ptr_value, formatter, ssa_func)
    return None
```

### Fix 2: Prioritize Parameter-Based Switches

**Location**: `vcdecomp/core/ir/structure/patterns/switch_case.py` (line 382+)

**Add**: After detecting all switches, rank them:
```python
def _rank_switch_importance(switch, ssa_func):
    # Parameter field access = highest priority
    if "->" in switch.switch_var and switch.switch_var.startswith("param"):
        return 100
    # Global variable = medium priority
    elif switch.switch_var.startswith("g"):
        return 50
    # Local variable = lowest priority
    else:
        return 10

switches.sort(key=lambda s: _rank_switch_importance(s, ssa_func), reverse=True)
```

### Fix 3: Filter Out Float Switches

**Location**: `vcdecomp/core/ir/structure/patterns/switch_case.py` (line 336+)

**Add**: Check constant type:
```python
if case_val is not None:
    # Check if this is a float constant (shouldn't be switch case)
    if isinstance(case_val, float) or (const_value.alias and "0.0f" in const_value.alias):
        # Skip this switch - it's comparing floats, not case values
        found_equ = False
        break
    # ... rest of logic
```

### Fix 4: Handle Jump Table Switches

**Problem**: The compiler might be using a jump table instead of sequential EQU comparisons.

**Solution**: Add jump table detection in CFG analysis.

## Testing Strategy

### After Fixes:

1. **Verify switch variable**:
   ```bash
   py -m vcdecomp structure decompilation\pilot\LEVEL.SCR > test.c
   grep "switch.*info->message" test.c  # Should find it!
   ```

2. **Check case values**:
   - Should see cases 0, 1, 2, 4, 7, 11, 15 (message enum values)
   - Should NOT see float comparisons

3. **Verify nesting**:
   - Case 0 should contain nested `switch(gphase)`
   - Inside that, nested `switch(SC_ggi(SGI_LEVELPHASE))`

4. **Regression test**:
   - TDM script should still work correctly
   - Don't break existing working switches

## Priority

🔴 **CRITICAL** - This breaks the entire decompiled output, making it non-functional.

## Files to Modify

1. `vcdecomp/core/ir/structure/analysis/value_trace.py`
   - Add `_trace_value_to_parameter_field()`
   - Add `_trace_dadr_to_param_field()`

2. `vcdecomp/core/ir/structure/patterns/switch_case.py`
   - Add switch importance ranking
   - Add float constant filtering
   - Modify switch variable tracing to prioritize parameter fields

3. `vcdecomp/core/ir/cfg.py` (optional)
   - Improve dead code detection
   - Better handling of unconditional jumps after value loads

## Next Steps

1. ✅ **Complete root cause analysis** (this document)
2. ⏭️ Implement Fix #1 (parameter field tracing)
3. ⏭️ Implement Fix #2 (switch prioritization)
4. ⏭️ Implement Fix #3 (float filtering)
5. ⏭️ Test on Pilot script
6. ⏭️ Regression test on TDM script
