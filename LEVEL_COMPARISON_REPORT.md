# LEVEL.SCR Decompilation Comparison Report

## Summary

The switch detection improvements have made significant progress, but there are still **critical accuracy issues** when compared to the original source code.

## Switch Detection Results

### Original LEVEL.C Structure
- **Main switch**: `switch(info->message)` with case `SC_LEV_MES_TIME` 
- **Nested switch 1**: `switch(gphase)` with cases 0, 1, 2, 3, 4, 7, 10, 11, 15, 20
- **Nested switch 2**: `switch(i)` 
- **Nested switch 3**: `switch(g_dialog)`
- **Other switches**: Multiple switches on `info->param1`, `g_pilot_phase`
- **Total**: ~10+ switch statements (some deeply nested)

### Decompiled LEVEL_decompiled.c Structure  
- **Detected**: 4 switch statements total
- **Variables**: `param_1`, `g_showinfo_timer` (appears 3 times), `local_89`
- **Cases detected**: 11, 4, 4, 1 respectively

## Critical Issues Found

### Issue 1: Wrong Switch Variable ❌
**Location**: Main switch in ScriptMain function

**Original (line 361)**:
```c
switch(info->message){
    case SC_LEV_MES_TIME:
        // ...
```

**Decompiled (line 592)**:
```c
switch (g_showinfo_timer) {
    case 0:
        // ...
```

**Problem**: The decompiler selected `g_showinfo_timer` (a global timer variable) instead of `info->message` (the actual control variable). This is a fundamental misdetection.

**Root Cause**: 
- The BFS found comparisons against both variables
- Priority scoring gave global variable (`g_showinfo_timer`) priority 50
- Should have detected parameter field access (`info->message`) with priority 100
- Parameter field tracing failed, fell back to generic `param_1`

### Issue 2: Missing Nested Switch Detection ❌
**Location**: Nested `switch(gphase)` inside `case SC_LEV_MES_TIME`

**Original (line 399)**:
```c
switch(info->message){
    case SC_LEV_MES_TIME:
        // ... some code ...
        switch(gphase){
            case 0:
                // initialization code
            case 1:
                // ...
```

**Decompiled (line 592-691)**:
```c
switch (g_showinfo_timer) {
    case 0:
        // ... some code ...
        break;
    // ... other cases ...
    default:
    }
    // Nested switch code appears HERE (outside switch!) ❌
    initside = 32;
    *tmp23 = 4;
    SC_InitSide(0.0f, &initside);
```

**Problem**: The nested `switch(gphase)` was not detected. Its code appears as linear statements after the outer switch closes.

**Impact**: Major control flow structure lost.

### Issue 3: Case Value Semantics Lost ❌
**Original**: Uses symbolic enum names like `SC_LEV_MES_TIME`
**Decompiled**: Uses raw numbers `0`, `1`, `2`, etc.

**Impact**: Lost readability, but bytecode-equivalent.

### Issue 4: Excessive Generic Variables ❌
**Examples**:
- `param_1->field_20` instead of `info->next_exe_time`
- `tmp4`, `tmp7`, `tmp10`, `tmp11`... instead of semantic names like `pilot`, `plinfo`, `fl`

**Impact**: Code is nearly unreadable compared to original.

## What's Working ✅

1. **Switch Detection Works**: 4 switches detected vs 0 before the fix
2. **Case Values Extracted**: Numeric case values are correct (0, 1, 2, 4, 7, 10, 11, 15, 20, 667)
3. **Break Statements**: Properly generated
4. **No Duplicate Cases**: Deduplication logic working
5. **Valid C Syntax**: Generated switch statements compile (modulo other issues)
6. **Code Structure**: Linear case bodies mostly correct

## Comparison Metrics

| Metric | Original | Decompiled | Match? |
|--------|----------|------------|--------|
| Total switches | ~10+ | 4 | ❌ 40% |
| Main switch variable | `info->message` | `g_showinfo_timer` | ❌ Wrong |
| Nested switches | 5+ | 0 | ❌ None |
| Case value accuracy | Symbolic | Numeric | ⚠️ Equivalent |
| Variable names | Semantic | Generic (`tmp`) | ❌ Lost |
| Code compiles | Yes | Yes (with fixes) | ✅ |
| Control flow preserved | Complex nested | Flat linear | ❌ Lost |

## Root Causes

1. **Parameter Field Detection Failure**: 
   - `_trace_value_to_parameter_field()` not finding `info->message` pattern
   - Falls back to generic `param_1` or picks wrong variable

2. **Nested Switch Not Implemented**:
   - Phase 5 from plan (nested switch support) was skipped
   - Recursive detection not implemented

3. **Variable Naming**:
   - SSA lowering and variable renaming producing generic names
   - Struct field name resolution incomplete

## Success Rate Assessment

**Switch Detection Accuracy**: ~30-40%
- Detects switches exist ✅
- Gets case values right ✅  
- Gets switch variable wrong ❌
- Misses nested switches ❌
- Loses semantic names ❌

**Overall Decompilation Quality**: ~40%
- Code compiles ✅
- Basic control flow ⚠️
- Semantic accuracy ❌

## Recommendations

### High Priority
1. Fix parameter field detection to correctly identify `info->message`
2. Implement nested switch detection (recursive pattern matching)
3. Improve variable naming (preserve struct field names)

### Medium Priority
4. Map numeric constants to enum names using debug info
5. Reduce generic tmp variable proliferation
6. Better SSA lowering for semantic names

### Low Priority
7. Detect and preserve comments
8. Format output to match original style
