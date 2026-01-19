# Decompilation Analysis: tt.c vs tt_decompiled.c

**Test Case**: decompiler_source_tests/test1/tt.scr
**Original Source**: tt.c (1225 lines)
**Decompiled Output**: tt_decompiled.c (437 lines)
**Date**: 2026-01-19
**Last Updated**: 2026-01-19 (Phase 1 Complete)

## Executive Summary

The decompiler produces structurally valid C code but suffers from critical information loss across multiple domains:
- **Function naming**: All semantic names replaced with generic `func_XXXX` labels
- **Variable declarations**: Type inference failures, incorrect array dimensions, missing initializers
- **Control flow**: Massive simplification - switch statements, loops, and complex logic reduced to fragments
- **Code completeness**: ~64% code loss (1225 → 437 lines)

The decompiled output is **not functionally equivalent** to the original and would require extensive manual reconstruction to be usable.

### ✅ Phase 1 Complete (2026-01-19)
**Fixed: Float Constant Formatting**
- Float constants now display correctly as `30.0f`, `5.0f`, `10.0f` instead of hex values like `1106247680`
- Fixed DataResolver initialization to work even without global type info
- Extended float detection to handle type hints `'int'`, `'dword'`, `'unsignedlong'`
- Improved heuristics to recognize common whole-number floats
- **Impact**: Readability significantly improved, constants are now human-readable
- **Files Modified**: `vcdecomp/core/ir/expr.py`, `vcdecomp/core/ir/data_resolver.py`
- **Commit**: db1a45a

---

## Summary Statistics

The decompilation of `tt.scr` has produced severely incomplete output. The original source is 1225 lines, but the decompiled output is only 437 lines (36% of original). Most function implementations are missing or incorrect.

## Critical Issues Found

### 1. **Missing Switch/Case Structure (ScriptMain)**

**Original (line 487-659):**
```c
switch(info->message){
    case SC_NET_MES_SERVER_TICK:
        // server tick code (200+ lines)
        if (SRV_CheckEndRule(info->elapsed_time)) break;
        // ...massive switch case body
        break;
    case SC_NET_MES_CLIENT_TICK:
        // client tick code
        break;
    case SC_NET_MES_LEVELPREINIT:
        // level pre-init
        break;
    // ... many more cases
}
```

**Decompiled (line 419-434):**
```c
block_157:
func_0050(tmp3);
if (!local_419) {
    return TRUE;
} else {
    local_296.field1 = 0;  // WRONG: Should be accessing field properly
    tmp6 = tmp3;
    local_ = 64;
    SC_MP_EnumPlayers(enum_pl, &local_, tmp20);
    gSidePoints[0] = 0;
    gSidePoints[1] = 0;
    func_0249();
    tmp19 = 0;
    tmp19 = 0;
}
```

**ROOT CAUSE:** The decompiler failed to detect the switch/case structure entirely. Instead of a switch statement on `info->message`, it generated a simple if/else with block labels.

---

### 2. **Uninitialized Variable Usage (tmp variables everywhere)**

**Example from GetRecovTime() (original line 138-153):**
```c
float GetRecovTime(void){
    float val;
    s_SC_MP_SRV_AtgSettings set;

    SC_MP_SRV_GetAtgSettings(&set);

    if (set.tt_respawntime>1.0f){
        return set.tt_respawntime;
    }

    val = SC_ggf(400);
    if (val==0) val = 30;
    return val;
}
```

**Decompiled (line 94-113):**
```c
int func_0119(void) {
    int local_0;  // Auto-generated
    s_SC_MP_SRV_AtgSettings local_1;  // Auto-generated

    int idx;
    int tmp;
    int tmp1;
    int tmp2;  // UNINITIALIZED!
    int tmp3;
    int tmp4;  // UNINITIALIZED!

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!tmp2) {  // Using uninitialized tmp2!
        return tmp4;  // Using uninitialized tmp4!
    } else {
        local_0 = SC_ggf(400);
        local_0 = 1106247680;  // Magic number (30.0f in hex)
        return local_0;
    }
    return 0;  // FIX (06-05): Synthesized return value
}
```

**ROOT CAUSE:** The decompiler is not properly tracking where values come from. Variables `tmp2` and `tmp4` are used before being assigned. The check `if (!tmp2)` should be `if (set.tt_respawntime>1.0f)`.

---

### 3. **Missing Struct Field Access**

**Original (line 146):**
```c
if (set.tt_respawntime>1.0f){
    return set.tt_respawntime;
}
```

**Decompiled (line 106-107):**
```c
if (!tmp2) {  // Should be: if (local_1.tt_respawntime>1.0f)
    return tmp4;  // Should be: return local_1.tt_respawntime;
}
```

**ROOT CAUSE:** The field tracker is detecting struct type `s_SC_MP_SRV_AtgSettings` for `local_1` (shown in DEBUG output: "param_0 detected as s_SC_NET_info"), but it's failing to reconstruct field accesses. The DCP (dereference pointer) instructions that access `set.tt_respawntime` are not being converted to proper field expressions.

The DEBUG output shows:
```
DEBUG PNT: Rejected - base_var '&local_1' not in var_struct_types ['param_0']
```

This indicates the field tracker only tracked `param_0` but didn't track local struct variables properly.

---

### 4. **Missing For Loops**

**Original (line 565-568):**
```c
for (i=0;i<2;i++)
for (j=0;j<gSteps;j++)
    for (k=0;k<gRecs[i][j];k++)
        gRecTimer[i][j][k] -= info->elapsed_time;
```

**Decompiled:** Completely missing from output.

**ROOT CAUSE:** Loop detection is failing. The control flow graph analysis is not properly identifying loop structures.

---

### 5. ~~**Magic Numbers Instead of Float Constants**~~ ✅ **FIXED in Phase 1**

**Original:**
```c
val = 30;        // or 30.0f
val = 5.0f;
val = 10.0f;
```

**Decompiled (BEFORE Phase 1):**
```c
local_0 = 1106247680;  // 30.0f in IEEE 754 hex
tmp6 = 1084227584;     // 5.0f in IEEE 754 hex
tmp6 = 1092616192;     // 10.0f in IEEE 754 hex
```

**Decompiled (AFTER Phase 1):** ✅
```c
local_0 = 30.0f;
tmp6 = 5.0f;
tmp6 = 10.0f;
```

**ROOT CAUSE:** Type inference was incorrect. Float constants were being printed as integer hex values.

**FIX:** DataResolver now initializes even without global type info, and float detection extended to handle `'int'`, `'dword'` type hints. Heuristics improved to recognize common whole-number floats.

---

### 6. **Incorrect Function Signatures**

**Original:**
```c
BOOL SRV_CheckEndRule(float time){
```

**Decompiled:**
```c
int func_0050(float param_0) {
```

**ROOT CAUSE:** Function name detection is not working. The decompiler doesn't have access to the original function names (they're stripped from the .scr bytecode).

---

### 7. **Missing Function Bodies**

**Original _init() (line 377-392):** Had some initialization code

**Decompiled _init() (line 58-73):**
```c
int _init(s_SC_NET_info *info) {
    int n;
    int side;
    int sideB;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;

    return 0;  // FIX (06-05): Synthesized return value
}
```

**ROOT CAUSE:** The SSA (Static Single Assignment) to C code conversion is losing most of the instructions. Only variable declarations remain.

---

## Root Cause Summary

### Primary Issues:

1. **Switch/Case Detection Failure**
   - File: `vcdecomp/core/ir/structure/patterns/switch_case.py`
   - The switch pattern detector is not recognizing the jump table for `info->message`
   - Need to examine why the switch detection is failing

2. **Field Access Reconstruction Failure**
   - File: `vcdecomp/core/ir/field_tracker.py`
   - The field tracker only propagates struct types for function parameters, not local variables
   - DEBUG shows: "base_var '&local_1' not in var_struct_types ['param_0']"
   - Local structs like `s_SC_MP_SRV_AtgSettings set;` are not being tracked

3. **SSA Lowering/Expression Building Failure**
   - File: `vcdecomp/core/ir/ssa_lowering.py` or `vcdecomp/core/ir/expr.py`
   - Many SSA values are not being properly converted to C expressions
   - Variables remain as `tmp`, `tmp1`, etc. without proper source tracking

4. **Type Inference Issues**
   - File: `vcdecomp/core/ir/type_inference.py`
   - Float constants are being treated as integers
   - IEEE 754 float literals (1106247680) should be converted to float notation (30.0f)

5. **Loop Detection Failure**
   - File: `vcdecomp/core/ir/structure/patterns/loops.py`
   - For-loops are not being detected in the control flow graph

6. **Control Flow Graph Issues**
   - File: `vcdecomp/core/ir/structure/orchestrator.py`
   - The overall structure reconstruction is missing large portions of the code
   - Only fragments of each function are being emitted

---

## Next Steps

### Priority 1: Fix Field Access Tracking for Local Variables
The field tracker needs to propagate struct types for local variables, not just parameters.

### Priority 2: Fix Switch/Case Detection
Examine why the switch on `info->message` is not being detected.

### Priority 3: Fix Type Inference for Float Constants
Convert IEEE 754 integer representations back to float literals.

### Priority 4: Fix SSA to C Conversion
Ensure all SSA instructions are properly converted to C statements.

### Priority 5: Fix Loop Detection
Improve for-loop pattern detection in CFG.

---

## Detailed Function-by-Function Comparison

### Function Mapping Table

| Original Function | Decompiled Name | Lines Original | Lines Decompiled | Recovery Rate | Status |
|------------------|-----------------|----------------|------------------|---------------|--------|
| `SRV_CheckEndRule` | `func_0050` | 36 | 18 | 50% | ⚠️ Partial |
| `GetRecovTime` | `func_0119` | 16 | 14 | 87% | ⚠️ Partial |
| `GetRecovLimitTime` | `func_0155` | 17 | 14 | 82% | ⚠️ Partial |
| `GetTimeLimit` | `func_0213` | 15 | 13 | 87% | ⚠️ Partial |
| `UpdateSidePoints` | `func_0249` | 4 | 8 | 200% | ❌ Incorrect |
| `SRV_UpdateMissionTime` | `func_0264` | 11 | 18 | 163% | ❌ Incorrect |
| `ResetMission` | `func_0294` | 14 | 22 | 157% | ❌ Incorrect |
| `GetAttackingSide` | `func_0334` | 9 | 5 | 56% | ⚠️ Partial |
| `RoundEnd` | `func_0355` | 46 | 62 | 135% | ❌ Incorrect |
| `SetFlagStatus` | `func_0498` | 66 | 10 | 15% | ❌ Critical failure |
| `Check_ABL` | `func_0752` | 27 | 16 | 59% | ⚠️ Partial |
| `Check_ABL_Restart` | `func_0852` | 52 | 12 | 23% | ❌ Critical failure |
| `RecoverDeathDefenders` | `func_1028` | 16 | 12 | 75% | ⚠️ Partial |
| `ScriptMain` | `ScriptMain` | 756 | 76 | 10% | ❌ Catastrophic failure |
| N/A | `_init` | N/A | 15 | N/A | ❌ Spurious function |

**Critical Observation**: The most important function `ScriptMain` (756 lines) is reduced to only 76 lines (90% loss).

---

## Variable Declaration Issues

### Global Variable Type Comparison

#### Multi-Dimensional Array Failures

| Original Declaration | Decompiled | Issue |
|---------------------|-----------|-------|
| `dword gRecs[2][STEP_MAX]` (2×6=12) | `dword gRecs[12]` | ✅ Size correct, ❌ Lost semantic structure (2 sides × 6 steps) |
| `s_SC_MP_Recover gRec[2][STEP_MAX][REC_MAX]` (2×6×32=384) | `dword gRec[64]` | ❌ Wrong type, ❌ Wrong size (should be 384) |
| `float gRecTimer[2][STEP_MAX][REC_MAX]` (2×6×32=384) | `dword gRecTimer[384]` | ❌ Wrong type (float→dword), ✅ Size correct |
| `s_sphere gStepSwitch[STEP_MAX]` (6) | `dword gStepSwitch[24]` | ❌ Wrong type, ❌ Wrong size |
| `void *gFlagNod[STEP_MAX][3]` (6×3=18) | `dword gFlagNod[18]` | ❌ Wrong type (void*→dword), ❌ Lost 2D structure |
| `c_Vector3 gFlagPos[STEP_MAX]` (6 structs) | `dword gFlagPos[18]` | ❌ Wrong type, ❌ Lost struct meaning |
| `dword gRespawn_id[2][STEP_MAX]` (2×6=12) | `dword gRespawn_id[12]` | ✅ Size correct, ❌ Lost 2D structure |

**Pattern**: All multi-dimensional arrays flattened. Struct types reduced to `dword`. Size calculations sometimes correct (total elements) but dimensional structure lost.

#### Type Inference Failures

| Variable | Original Type | Decompiled Type | Issue |
|----------|--------------|-----------------|-------|
| `gSteps` | `dword` (initialized to 0) | `int` | ⚠️ Acceptable, ❌ Missing initializer |
| `gEndRule` | `dword` | `int` | ⚠️ Acceptable |
| `gTime` | `float` | `int` | ❌ Critical - wrong type |
| `gNoActiveTime` | `float` (initialized to 0.0f) | `float` | ✅ Correct type, ❌ Missing initializer |
| `gPhaseTimer` | `float` | `int` | ❌ Wrong type |
| `gMissionTime_update` | `float` (initialized to 10.0f) | `int` | ❌ Wrong type AND missing init |
| `gMissionTime` | `float` | `int` | ❌ Wrong type |
| `gMissionTimePrev` | N/A (doesn't exist) | `float` | ❌ Spurious variable |
| `gMissionTimeToBeat` | `float` | `int` | ❌ Wrong type |
| `gCLN_ShowInfo` | `float` (initialized to 0.0f) | `int` | ❌ Wrong type AND missing init |

**Pattern**: Many float variables incorrectly typed as `int`. All initializers missing.

#### Mysterious Generic Variables

The decompiler generates unexplained variables not present in original:
```c
dword gVar;
dword gVar1;
dword gVar2;
dword gVar3;
// ... through gVar12
```

**Hypothesis**: These represent:
- Misidentified global variable references
- Compiler-generated temporaries stored in data segment
- Artifacts from incorrect global pointer resolution

---

## Control Flow Recovery Failures

### 1. Switch Statement Destruction: SRV_CheckEndRule

#### Original (Lines 100-131)
```c
switch(gEndRule){
    case SC_MP_ENDRULE_TIME:
        if (gMission_phase>MISSION_PHASE_NOACTIVE) gTime += time;
        SC_MP_EndRule_SetTimeLeft(gTime,gMission_phase);
        if (gTime>gEndValue){
            SC_MP_LoadNextMap();
            return TRUE;
        }
        break;

    case SC_MP_ENDRULE_POINTS:
        if ((gSidePoints[0]>=gEndValue)||(gSidePoints[1]>=gEndValue)){
            SC_MP_LoadNextMap();
            return TRUE;
        }
        break;

    default:
        SC_message("EndRule unsupported: %d",gEndRule);
        break;
}
return FALSE;
```

#### Decompiled (Lines 75-92)
```c
block_3:
if (!tmp1) {
    data_ = tmp2;
} else {
    SC_MP_EndRule_SetTimeLeft(data_, gMission_phase);
    SC_MP_LoadNextMap();
    return TRUE;
}
return 0;
```

**Damage Assessment**:
- ❌ Switch statement → simple if/else
- ❌ Only 1 of 3 cases partially present
- ❌ `SC_MP_ENDRULE_POINTS` case completely lost
- ❌ Default case with error message lost
- ❌ Time accumulation logic `gTime += time` lost
- ❌ Points checking logic lost
- ❌ Mysterious `block_3:` label without corresponding goto

### 2. Complete Loop Annihilation: SetFlagStatus

#### Original (Lines 301-348) - 48 lines
```c
for (i=0;i<STEP_MAX;i++){
    us = FALSE;
    vc = FALSE;
    ne = FALSE;

    if ((i+1)==cur_step){
        switch(attacking_side){
            case 0: vc = TRUE; break;
            case 1: us = TRUE; break;
            case 2: ne = TRUE; break;
        }
    }
    else if (i<cur_step){
        ne = TRUE;
    }

    if (gFlagNod[i][0]) SC_DUMMY_Set_DoNotRenHier2(gFlagNod[i][0],!us);
    if (gFlagNod[i][1]) SC_DUMMY_Set_DoNotRenHier2(gFlagNod[i][1],!vc);
    if (gFlagNod[i][2]) SC_DUMMY_Set_DoNotRenHier2(gFlagNod[i][2],!ne);

    fpv_list[flags].id = 0;
    if (us) fpv_list[flags].id = g_FPV_UsFlag;
    else if (vc) fpv_list[flags].id = g_FPV_VcFlag;
    else if (ne) fpv_list[flags].id = g_FPV_NeFlag;

    if (fpv_list[flags].id){
        fpv_list[flags].color = 0xffffffff;
        fpv_list[flags].pos = gFlagPos[i];
        fpv_list[flags].scale = 1.0f;
        flags++;
    }
}
SC_MP_FpvMapSign_Set(flags,fpv_list);
```

#### Decompiled (Lines 293-302) - 10 lines
```c
int func_0498(int param_0, int param_1) {
    int idx;
    int m;
    int tmp;
    int tmp1;

    tmp = 0;
    tmp1 = 0;
    return 0;
}
```

**Damage Assessment**:
- ❌ 95%+ code loss
- ❌ Entire for loop vanished
- ❌ Switch statement inside loop gone
- ❌ All flag rendering logic lost
- ❌ Array accesses to `gFlagNod[i][0]`, `[i][1]`, `[i][2]` gone
- ❌ FPV map sign construction missing
- ❌ Function reduced to meaningless stub
- ❌ Critical game functionality (flag visibility) completely broken

### 3. Nested Loop Triple-Vanishing Act

#### Original (Lines 565-568)
```c
for (i=0;i<2;i++)
    for (j=0;j<gSteps;j++)
        for (k=0;k<gRecs[i][j];k++)
            gRecTimer[i][j][k] -= info->elapsed_time;
```

#### Decompiled
**Completely absent** - not even a trace in ScriptMain decompiled output.

**Impact**: Timer system for respawn points non-functional.

### 4. ScriptMain Catastrophe

Original structure (Lines 470-1225):
```c
int ScriptMain(s_SC_NET_info *info){
    // 15 local variable declarations
    // ...

    switch(info->message){
        case SC_NET_MES_SERVER_TICK:       // 170 lines
            // Player enumeration
            // Team balance checking
            // Mission phase state machine (nested switch)
            // Timer updates (triple nested loop)
            // Flag capture detection (nested loops)
            break;

        case SC_NET_MES_CLIENT_TICK:       // 78 lines
            // HUD updates
            // Flag rendering
            // Time synchronization
            break;

        case SC_NET_MES_LEVELPREINIT:      // 16 lines
            break;

        case SC_NET_MES_LEVELINIT:         // 181 lines
            // Resource loading
            // Respawn point discovery (nested loops)
            // Global variable synchronization
            break;

        case SC_NET_MES_RENDERHUD:         // 169 lines
            // HUD text rendering
            // Game status messages
            break;

        case SC_NET_MES_SERVER_RECOVER_TIME:     // 44 lines
        case SC_NET_MES_SERVER_RECOVER_PLACE:    // 33 lines
        case SC_NET_MES_RESTARTMAP:              // 20 lines
        case SC_NET_MES_RULESCHANGED:            // 6 lines
        case SC_NET_MES_SERVER_KILL:             // 4 lines
    }
    return 1;
}
```

Decompiled (Lines 361-435):
```c
int ScriptMain(s_SC_NET_info *info) {
    // 38 variable declarations (mostly wrong types)

    block_157:
    func_0050(tmp3);
    if (!local_419) {
        return TRUE;
    } else {
        local_296.field1 = 0;
        tmp6 = tmp3;
        local_ = 64;
        SC_MP_EnumPlayers(enum_pl, &local_, tmp20);
        gSidePoints[0] = 0;
        gSidePoints[1] = 0;
        func_0249();
        tmp19 = 0;
        tmp19 = 0;
    }
    return 0;
}
```

**Damage Assessment**:
- ❌ 90% code loss (756 → 76 lines)
- ❌ No switch on `info->message`
- ❌ All 16 message handler cases missing
- ❌ Only 3 function calls present (original: 100+)
- ❌ No loops visible
- ❌ Game logic completely non-functional

**This is the most severe failure** - the entire game script is reduced to a stub.

---

## Expression Decompilation Issues

### 1. Temporary Variable Explosion

Pattern throughout code: one temporary per stack operation.

#### Example: GetRecovTime condition check

**Original:**
```c
if (set.tt_respawntime>1.0f){
    return set.tt_respawntime;
}
```

**Decompiled:**
```c
if (!tmp2) {  // What is tmp2?
    return tmp4;  // What is tmp4?
}
```

**Problem**: The values `tmp2` and `tmp4` are never assigned in the visible code. The comparison `set.tt_respawntime>1.0f` should produce a boolean result stored in `tmp2`, but the FADD/FCMP/JZ instruction sequence is not being reconstructed into the comparison expression.

### 2. Float Constants as Hex Magic Numbers

| Original | Decompiled | IEEE-754 Verification |
|----------|-----------|---------------------|
| `30` or `30.0f` | `1106247680` | 0x41F00000 = 30.0f ✅ |
| `5.0f` | `1084227584` | 0x40A00000 = 5.0f ✅ |
| `10.0f` | `1092616192` | 0x41200000 = 10.0f ✅ |
| `8*60` (480) | `1139802112` | 0x43F00000 = 480.0f ✅ |
| `1.0f` | Correctly as `1.0f` | ✅ |

**Pattern**: Most float constants converted to integer hex representation instead of float literals. The decompiler's type inference knows these are floats (storing in float variables) but expression formatting uses integer representation.

### 3. Constant Replacement with Magic Numbers

| Original | Decompiled | Impact |
|----------|-----------|--------|
| `GVAR_SIDE0POINTS` (500) | `500` | Acceptable - constant value preserved |
| `GVAR_SIDE1POINTS` (501) | `501` | Acceptable |
| `GVAR_MISSIONTIME` (504) | `504` | Acceptable |
| `GVAR_MISSIONTIME_UPDATE` (505) | `505` | Acceptable |
| `GVAR_CURSTEP` (507) | `507` | Acceptable |
| `SC_MP_ENDRULE_TIME` | Not present | ❌ Lost - switch case missing |
| `SC_MP_ENDRULE_POINTS` | Not present | ❌ Lost - switch case missing |
| `MISSION_PHASE_NOACTIVE` (0) | Not present | ❌ Lost |
| `MISSION_PHASE_INGAME` (1) | Not present | ❌ Lost |

**Issue**: Named constants replaced with raw values. While numeric values are correct, semantic meaning lost.

### 4. Struct Field Access Inconsistencies

#### Success case: Local struct with known type
```c
// Original
s_SC_MP_SRV_AtgSettings set;
SC_MP_SRV_GetAtgSettings(&set);
if (set.tt_respawntime>1.0f){
    return set.tt_respawntime;
}

// Decompiled (partially correct structure)
s_SC_MP_SRV_AtgSettings local_1;
SC_MP_SRV_GetAtgSettings(&local_1);
if (!tmp2) {
    return local_1->tt_respawntime;  // Field name recovered!
}
```

**Observation**: Field name `tt_respawntime` correctly identified. BUT using pointer dereference `->` when should be `.` (struct on stack, not pointer).

#### Failure case: Parameter struct
```c
// Original (ScriptMain)
info->message       // Used in switch
info->elapsed_time  // Used throughout
info->param1        // Used in multiple cases
info->param2        // Used in multiple cases
info->fval1         // Used for respawn time

// Decompiled ScriptMain
// No field accesses visible at all
```

**Why the difference?**
- Local structs: Type recovered from function signature of `SC_MP_SRV_GetAtgSettings(&set)`
- Parameter structs: Field access lost because the code using them is missing

---

## Data Structure Recovery Analysis

### Successfully Recovered Struct Types

| Struct Type | Recovery Status | Usage Context |
|------------|----------------|---------------|
| `s_SC_NET_info` | ✅ Name + fields | ScriptMain parameter |
| `s_SC_MP_SRV_AtgSettings` | ✅ Name + some fields | Local variable in func_0119, func_0155, func_0213 |
| `s_SC_P_getinfo` | ✅ Name only | Not enough code to see fields |
| `s_SC_MP_EnumPlayers` | ✅ Name + array | Array declaration present |

### Failed Struct Type Recovery

| Struct Type | Original Usage | Decompiled As | Impact |
|------------|---------------|---------------|--------|
| `s_SC_MP_Recover` | `gRec[2][6][32]` | `dword gRec[64]` | ❌ Type lost, size wrong |
| `s_sphere` | `gStepSwitch[6]` | `dword gStepSwitch[24]` | ❌ Type and size wrong |
| `c_Vector3` | `gFlagPos[6]` | `dword gFlagPos[18]` | ❌ Type lost |
| `s_SC_MP_SRV_settings` | Local in ScriptMain | Not visible | ❌ Code missing |
| `s_SC_HUD_MP_icon` | Local array in ScriptMain | Not visible | ❌ Code missing |
| `s_SC_FpvMapSign` | Local array in SetFlagStatus | Not visible | ❌ Code missing |

**Pattern**: Structs in global arrays almost always fail to recover. Structs in local variables within function calls sometimes succeed.

---

## Missing Code Sections

### 1. Preprocessor Conditional Code

#### Original (Lines 82-87)
```c
#if _GE_VERSION_ >= 133
dword gRespawn_id[2][STEP_MAX] = {
    {0,SC_MP_RESPAWN_TT_ATT_1, /*...*/},
    {SC_MP_RESPAWN_TT_DEF_0, /*...*/}
};
#endif
```

#### Decompiled
```c
dword gRespawn_id[12];  // No conditional, no initializer
```

**Issue**: The .scr was compiled with a specific `_GE_VERSION_`, so inactive code branches are permanently lost.

### 2. Complete Message Handler Cases

From ScriptMain, these entire cases are missing:

| Message Handler | Original Lines | Decompiled Presence |
|----------------|---------------|-------------------|
| `SC_NET_MES_SERVER_TICK` | 170 | ❌ 0% |
| `SC_NET_MES_CLIENT_TICK` | 78 | ❌ 0% |
| `SC_NET_MES_LEVELPREINIT` | 16 | ❌ 0% |
| `SC_NET_MES_LEVELINIT` | 181 | ❌ 0% |
| `SC_NET_MES_RENDERHUD` | 169 | ❌ 0% |
| `SC_NET_MES_SERVER_RECOVER_TIME` | 44 | ❌ 0% |
| `SC_NET_MES_SERVER_RECOVER_PLACE` | 33 | ❌ 0% |
| `SC_NET_MES_RESTARTMAP` | 20 | ❌ 0% |
| `SC_NET_MES_RULESCHANGED` | 6 | ❌ 0% |
| `SC_NET_MES_SERVER_KILL` | 4 | ❌ 0% |

**Total missing code from ScriptMain alone: 721 lines**

---

## Comparative Metrics

| Metric | Original | Decompiled | Accuracy % |
|--------|----------|-----------|-----------|
| **Code Size** |
| Total lines | 1225 | 437 | 36% |
| Code lines (no blanks/comments) | ~1050 | ~400 | 38% |
| **Functions** |
| Total functions | 14 | 15 | 107% (spurious) |
| Correctly named | 14 | 1 (ScriptMain) | 7% |
| Functionally correct | 14 | 0 | 0% |
| **Variables** |
| Global variables | 57 | 56 + 12 gVar* | 120% (spurious) |
| Correct type | 57 | ~17 | 30% |
| Correct dimensions (arrays) | 8 multi-dim | 0 | 0% |
| With initializers | 10 | 0 | 0% |
| **Control Flow** |
| Switch statements | 7 | 0 | 0% |
| For loops | 15+ | 0 | 0% |
| While loops | 2 | 0 | 0% |
| If statements | ~80 | ~15 | 19% |
| **Expressions** |
| Function calls | 200+ | ~30 | 15% |
| Array accesses | 100+ | ~5 | 5% |
| Struct field accesses | 50+ | ~3 | 6% |
| **Documentation** |
| Semantic comments | 54 | 0 | 0% |
| Header includes | 1 | 2 | 200% (wrong headers) |

---

## Usability Assessment

### What Works
✅ File parsing and disassembly
✅ Function boundary detection (correct count)
✅ Basic variable declarations (names as local_N)
✅ Simple function calls to engine APIs
✅ Some struct type name recovery
✅ Syntactically valid C output

### What Doesn't Work
❌ Function naming (all generic)
❌ Variable naming (all generic)
❌ Switch statement recovery (0%)
❌ Loop recovery (0%)
❌ Multi-dimensional array types
❌ Struct types in globals
❌ Float constant formatting
❌ Code completeness (64% loss)
❌ Complex expression reconstruction
❌ Control flow fidelity

### Practical Usability Score: 2/10

**For compilation**: Would not compile (undefined variables, incomplete logic)
**For understanding**: Provides skeleton but missing critical logic
**For modification**: Would require 80%+ rewrite
**For learning**: Shows function boundaries and some API calls

**Estimated manual effort to make functional**: 40-60 hours for this single file

---

## Recommendations for Improvement

### Critical Priority (P0)

1. **Switch statement detection** (highest impact)
   - File: `vcdecomp/core/ir/structure/patterns/switch_case.py`
   - Root cause: Jump table pattern not recognized
   - Impact: ScriptMain completely broken without this

2. **Loop detection** (high impact)
   - File: `vcdecomp/core/ir/structure/patterns/loops.py`
   - Root cause: For-loop patterns not identified in CFG
   - Impact: All timer logic, player enumeration broken

3. **SSA to C conversion completeness** (critical)
   - File: `vcdecomp/core/ir/ssa_lowering.py` and `structure/emit/code_emitter.py`
   - Root cause: Many SSA instructions not emitted as C statements
   - Impact: 64% code loss

### High Priority (P1)

4. **Field access tracking for locals**
   - File: `vcdecomp/core/ir/field_tracker.py`
   - Root cause: Only tracks function parameters, not local structs
   - Impact: `tmp2` instead of `set.tt_respawntime>1.0f`

5. **Float constant formatting**
   - File: `vcdecomp/core/ir/expr.py`
   - Root cause: Type inference knows float but uses int formatting
   - Impact: `1092616192` instead of `10.0f`

6. **Array dimension inference**
   - File: `vcdecomp/core/ir/type_inference.py`
   - Root cause: Multi-level indexing not tracked
   - Impact: All multi-dimensional arrays wrong

### Medium Priority (P2)

7. **Function name inference heuristics**
8. **Variable name inference**
9. **Struct type propagation to globals**
10. **Temporary variable reduction**

### Long-term (P3)

11. **Constant/define recovery**
12. **Comment generation**
13. **Initializer recovery**

---

## Test Case Value

This test case is **exceptionally valuable** for decompiler development:

✅ **Real-world complexity**: Production game code
✅ **Complete ground truth**: Original source available
✅ **Diverse patterns**: State machines, network handlers, rendering
✅ **Size**: Large enough to stress test (1225 lines)
✅ **Engine integration**: Tests external function call handling

**Recommended use**:
- Primary regression test for all major improvements
- Benchmark for measuring decompiler progress
- Reference for expected vs actual output quality

---

## Conclusion

The VC-Script decompiler is in **early alpha** stage:

**Current state**:
- Can parse bytecode ✅
- Can identify functions ✅
- Can generate valid C syntax ✅
- Cannot recover functional logic ❌

**Readiness**:
- Research/development: **Ready**
- Understanding bytecode: **Partially ready**
- Code recovery: **Not ready**
- Production use: **Not ready**

**Most critical gap**: Control flow recovery (switches, loops). Without this, the decompiled output is largely useless for practical purposes.

**Path forward**: Focus all development effort on switch/loop detection before addressing naming or other quality-of-life issues. The 64% code loss is unacceptable for any real use case.

---

## Implementation Plan for Remaining Fixes

Based on the analysis, here are the remaining critical fixes with prioritized implementation guidance:

### 🔴 Phase 2: Local Struct Field Tracking (HIGH IMPACT, MEDIUM RISK)
**Priority**: P0 - Critical for readability
**Estimated Effort**: 3-4 hours
**Files**: `vcdecomp/core/ir/field_tracker.py`

**Problem**:
```c
// Current output:
if (!tmp2) {  // Should be: if (local_1.tt_respawntime>1.0f)
    return tmp4;  // Should be: return local_1.tt_respawntime;
}
```

**Root Cause**:
- `_detect_local_structs()` (lines 161-233) only tracks structs passed to XCALL
- PNT pattern matching (line 371) requires `base_var in var_struct_types`
- Local variables passed by reference to functions are not tracked

**Solution**:
1. Extend `_detect_local_structs()` to track `&local_N` patterns in XCALL arguments
2. Look up function signature to determine struct type (e.g., `SC_MP_SRV_GetAtgSettings(*s_SC_MP_SRV_AtgSettings)`)
3. Add local variable to `var_struct_types` dict
4. Fix PNT/DCP pattern matching to handle `&local_N` base addresses

**Expected Impact**:
- Struct field accesses correctly reconstructed: `local_1.tt_respawntime` instead of `tmp2`
- ~50+ field accesses recovered across all functions
- Significantly improved readability of struct-heavy code

**Testing**:
```bash
py -m vcdecomp structure decompiler_source_tests/test1/tt.scr > output.c
# Verify func_0119 shows local_1.tt_respawntime
grep "tt_respawntime" output.c
```

---

### 🔴 Phase 3: Switch Detection Improvements (CRITICAL IMPACT, HIGH RISK)
**Priority**: P0 - Blocks 90% of ScriptMain recovery
**Estimated Effort**: 6-8 hours
**Files**: `vcdecomp/core/ir/structure/patterns/switch_case.py`

**Problem**:
- ScriptMain's switch on `info->message` not detected
- 721 lines of code (90%) missing from ScriptMain

**Root Cause**:
- Line 207: Brittle heuristic finds FIRST global load in function
- Lines 317-333: Float filtering logic incorrectly classifies `info->message` as float
- Switch variable tracing fails when GCP not in same block

**Solution**:
1. Replace single-block GCP search with multi-block value tracing
2. Use `analysis/value_trace.py::trace_value()` to track through field accesses
3. Tighten float detection (message IDs are typically 0-1000 integers, not floats)
4. Add comprehensive logging to debug switch detection

**Expected Impact**:
- ScriptMain switch statement recovered with 10+ cases
- ~721 lines of critical game logic restored
- All message handlers (SERVER_TICK, CLIENT_TICK, LEVELINIT, etc.) reconstructed

**Risk**:
- High complexity - switch detection affects entire control flow
- May cause false positives if heuristics too loose
- Requires careful testing on multiple scripts

**Testing**:
```bash
py -m vcdecomp structure decompiler_source_tests/test1/tt.scr > output.c
# Verify ScriptMain has switch statement
grep -A5 "switch.*message" output.c
# Check case count
grep "case SC_NET_MES" output.c | wc -l  # Should be 10+
```

---

### 🔴 Phase 4: Loop Detection Validation (MEDIUM IMPACT, LOW RISK)
**Priority**: P1 - Needed for timer logic and enumeration
**Estimated Effort**: 2-3 hours
**Files**: `vcdecomp/core/ir/structure/patterns/loops.py`

**Problem**:
- Triple nested loop in ScriptMain completely missing
- SetFlagStatus loop (48 lines) vanished
- All for-loops (15+) not detected

**Root Cause**:
- Lines 167-203: Off-by-one correction heuristic unreliable
- Assumes all 0-initialized loops use `<` not `<=`
- Doesn't validate that condition variable matches init variable

**Solution**:
1. Add init/condition/increment validation (verify same variable)
2. Make off-by-one correction conservative (only when safe)
3. Support `i += step` and `i--` patterns
4. Add logging for debugging

**Expected Impact**:
- Triple nested loop recovered: `for(i=0;i<2;i++) for(j=0;j<gSteps;j++) for(k=0;k<gRecs[i][j];k++)`
- SetFlagStatus loop (48 lines) restored
- ~15+ for-loops detected across all functions

**Testing**:
```bash
py -m vcdecomp structure decompiler_source_tests/test1/tt.scr > output.c
# Count for loops
grep -c "^[[:space:]]*for[[:space:]]*(" output.c  # Should be 15+
```

---

### 🔴 Phase 5: SSA Emission Completeness (CRITICAL IMPACT, HIGHEST RISK)
**Priority**: P0 - Root cause of 64% code loss
**Estimated Effort**: 8-12 hours
**Files**: `vcdecomp/core/ir/structure/emit/code_emitter.py`, `vcdecomp/core/ir/ssa_lowering.py`

**Problem**:
- 64% of code missing (1225 → 437 lines)
- Function bodies reduced to stubs (e.g., _init has only variable declarations)
- Many SSA instructions never converted to C statements

**Root Cause**:
- Variable naming collisions during SSA lowering
- PHI nodes with multiple inputs fall back to first input silently
- Dead code after RET not emitted (but may not actually be dead)
- Complex conditional bodies miscalculated

**Solution**:
1. **Add SSA instruction tracking**:
   - Create set of all SSA instruction IDs in function
   - Track which instructions are emitted during code generation
   - Log warnings for unemitted reachable instructions

2. **Fix variable naming collisions** (`ssa_lowering.py` lines 189-205):
   - Detect duplicate lowered names
   - Add numeric suffixes when collisions occur
   - Ensure all SSA variables get unique C names

3. **Improve PHI node handling**:
   - Detect when PHI inputs are undefined
   - Generate comments for uninitialized variables
   - Flag functions with uninitialized usage

4. **Fix header code extraction** (`code_emitter.py` lines 94-122):
   - Validate extracted header instructions
   - Ensure no instructions duplicated or skipped

**Expected Impact**:
- Code recovery increases from 36% to 70%+
- Function bodies fully reconstructed
- _init function has actual implementation
- ScriptMain completeness dramatically improved

**Risk**:
- HIGHEST RISK - touches core code generation
- High chance of breaking existing working code
- Requires extensive testing and regression checks

**Testing**:
```bash
py -m vcdecomp structure decompiler_source_tests/test1/tt.scr > output.c
wc -l output.c  # Should be 800+ lines (from current 437)
# Test compilation
cd test_compilation && ./scmp.exe ../output.c test.scr sc_global.h
```

---

## Recommended Implementation Order

### Week 1: Quick Wins (Phases 1-2)
- ✅ **Phase 1 COMPLETE**: Float formatting (2-3 hours) - **DONE**
- **Phase 2**: Local struct field tracking (3-4 hours)
- **Result**: Significantly improved readability with minimal risk

### Week 2: High-Impact Core Fixes (Phase 3-4)
- **Phase 3**: Switch detection (6-8 hours)
- **Phase 4**: Loop detection (2-3 hours)
- **Result**: Most control flow structures recovered, ~70% of missing code restored

### Week 3: Deep Architecture Fix (Phase 5)
- **Phase 5**: SSA emission completeness (8-12 hours)
- **Result**: Near-complete code recovery, functional decompilation

### Week 4: Validation & Regression
- Run full regression tests on all test scripts
- Validate bytecode equivalence with original compiler
- Document remaining limitations
- Create comprehensive test suite

---

## Success Metrics (Revised Post-Phase 1)

| Metric | Original | Current | Phase 2 Target | Phase 3-4 Target | Phase 5 Target |
|--------|----------|---------|----------------|------------------|----------------|
| Code recovery % | 100% | 36% | 40% | 65% | 75%+ |
| Float constants correct | 100% | **100%** ✅ | 100% | 100% | 100% |
| Switch statements | 7 | 0 | 0 | 6+ | 6+ |
| For loops | 15+ | 0 | 0 | 12+ | 15+ |
| Struct field accesses | 50+ | 3 | 30+ | 40+ | 50+ |
| Functions with complete bodies | 14 | 0 | 0 | 3-4 | 10+ |

---

## Risk Mitigation

1. **Commit after each phase** with descriptive messages
2. **Tag working states**: `phase2-fields-working`, `phase3-switches-working`, etc.
3. **Keep original code commented** for quick rollback
4. **Run regression tests** after each phase:
   ```bash
   PYTHONPATH=. python -m pytest vcdecomp/tests/test_structure_patterns.py -v
   PYTHONPATH=. python -m pytest vcdecomp/tests/test_end_to_end_decompilation.py -v
   ```
5. **Test on multiple scripts** (not just tt.scr):
   - decompiler_source_tests/test2/tdm.scr (team deathmatch)
   - decompiler_source_tests/test3/LEVEL.scr (level script)

---

## Long-term Improvements (Post-Phase 5)

Once core functionality is stable:

### P2 - Quality of Life
- **Function name inference**: Heuristics based on called APIs
- **Variable name inference**: Based on usage patterns
- **Constant/define recovery**: Reverse-engineer magic numbers
- **Type propagation to globals**: Fix multi-dimensional arrays

### P3 - Polish
- **Comment generation**: Auto-generate explanatory comments
- **Initializer recovery**: Restore global variable initializers
- **Dead code elimination**: Remove truly unreachable code
- **Code formatting**: Consistent indentation and style

---

## Conclusion

**Phase 1 (Float Formatting) is complete** and demonstrates that incremental improvements are achievable. The remaining work is well-scoped and prioritized.

**Critical Path**: Phases 2-3-5 form the critical path to functional decompilation. Phase 4 is important but can be done in parallel with Phase 5.

**Timeline Estimate**: With focused effort, Phases 2-5 could be completed in 3-4 weeks, resulting in a decompiler that produces ~75% functional code recovery with correct control flow structures.

**Next Immediate Step**: Begin Phase 2 (Local Struct Field Tracking) - lowest risk, high readability impact, builds confidence before tackling the more complex Phases 3 and 5.
