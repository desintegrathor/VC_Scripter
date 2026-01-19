# Pilot Mission Decompilation Comparison

## Summary

Comparison of original source (`LEVEL.C`) vs decompiled output (`LEVEL_decompiled.c`) for the Pilot mission script.

**Script**: `decompilation\pilot\LEVEL.SCR`
**Original Source**: 966 lines
**Decompiled Output**: 853 lines

---

## Key Issues Found

### 1. Control Flow Structure - CRITICAL ❌

**Problem**: The entire control flow is completely broken. The decompiler produced multiple nested switch statements where there should be a simple message handler switch.

**Original Structure**:
```c
int ScriptMain(s_SC_L_info *info) {
    switch(info->message) {
        case SC_LEV_MES_TIME:
            // ... handle time tick
            switch(gphase) {
                case 0: // init
                case 1: // gameplay
            }
            break;
        case SC_LEV_MES_RADIOUSED:
            // ... handle radio
            break;
        case SC_LEV_MES_EVENT:
            // ... handle events
            break;
    }
}
```

**Decompiled Structure**:
```c
int ScriptMain(s_SC_L_info *info) {
    switch (g_showinfo_timer) {  // ❌ WRONG! Should be info->message
        case 0:
            // ... all initialization code in case 0
            // ... all gameplay code in case 0
            // ... nested switches everywhere
            break;
        case 1:
            // ... some radio code
            break;
    }
    // Then THREE MORE identical switch statements on g_showinfo_timer
    // With empty cases and duplicated loop headers
}
```

**Impact**: The decompiled code is completely non-functional. It switches on a float timer variable instead of the message enum.

---

### 2. Variable Naming - PARTIAL SUCCESS ✅/⚠️

**Loop Counters** ✅: Phase 2 improvements working correctly
```c
// Original:
for (i=0; i<16; i++)
for (j=0; j<12; j++)

// Decompiled:
for (i = 0; (i < 16); i = i + 1)  // ✅ Correct naming!
for (i = 0; (i < 12); i = i + 1)  // ⚠️ Should be 'j'
```

**Struct Variables** ✅: Phase 2 working for some structs
```c
// Original:
s_SC_P_getinfo plinfo;
s_SC_initside initside;
s_SC_initgroup initgroup;
s_SC_Ai_PlFollow fol[4];
s_SC_MissionSave savinfo;
s_SC_Objective objective[2];

// Decompiled:
int plinfo;       // ✅ Good name, wrong type
int initside;     // ✅ Good name, wrong type
int initgroup;    // ✅ Good name, wrong type
int plfollow;     // ⚠️ Close (fol → plfollow)
int missionsave;  // ⚠️ Close (savinfo → missionsave)
int objective;    // ✅ Good name!
```

**Other Variables** ❌: Still many issues
```c
// Original:
dword pc, pilot, crocker, hornster, pilot_h1, defort;
float fl, fl2, dist;
c_Vector3 vec, plpos, movdir;

// Decompiled:
int local_, local_0, local_2, local_11, local_17, etc.  // ❌ Generic names
int tmp, tmp1, tmp2, tmp3;                               // ❌ Generic temps
```

---

### 3. Global Variable Detection - CRITICAL ❌

**Problem**: Many global variables detected with wrong types or as simple scalars instead of arrays.

**Original Globals**:
```c
dword gphase = 0;
dword g_dialog = 0;
dword g_will_group[4] = {3,2,1,4};           // ❌ Scalar in decompiled
BOOL g_dochange = TRUE;
float g_final_enter_timer = 0.0f;
c_Vector3 g_will_pos[4];                     // ❌ Scalar in decompiled
BOOL g_vill_visited[4] = {FALSE,FALSE,FALSE,FALSE};  // ❌ Scalar
dword g_pilot_phase = PILOT_PH_DISABLED;
float g_pilot_timer = 0.0f;
dword g_pilot_vill_nr = 0xff;
float g_showinfo_timer = 0.0f;
BOOL g_trashes_enabled = FALSE;
c_Vector3 gShot_pos;                         // ❌ Scalar
float gEndTimer;
float gPilotCommTime = 0.0f;
BOOL g_save[2];                              // ❌ Array[64] in decompiled!
BOOL g_music[2];                             // ❌ Scalar in decompiled
float gStartMusicTime = 0.0f;
```

**Decompiled Globals**:
```c
dword gphase;                    // ✅ Correct
dword g_dialog;                  // ✅ Correct
dword g_will_group;              // ❌ Should be [4]
dword g_dochange;                // ✅ Correct (wrong type but OK)
float g_final_enter_timer;       // ✅ Correct
dword g_will_pos;                // ❌ Should be c_Vector3[4]
dword g_vill_visited;            // ❌ Should be BOOL[4]
dword g_pilot_phase;             // ✅ Correct
float g_pilot_timer;             // ✅ Correct
dword g_pilot_vill_nr;           // ✅ Correct
float g_showinfo_timer;          // ✅ Correct
dword g_trashes_enabled;         // ✅ Correct
dword gShot_pos;                 // ❌ Should be c_Vector3
float gEndTimer;                 // ✅ Correct
float gPilotCommTime;            // ✅ Correct
dword g_save[64];                // ❌ Should be BOOL[2]
dword g_music;                   // ❌ Should be BOOL[2]
float gStartMusicTime;           // ✅ Correct
```

**Score**: 11/21 correct (52%) - needs improvement

---

### 4. Function Detection - MIXED ✅/❌

**Original Functions**:
1. `_init()` - Initialization
2. `DisapearAttackers()` - Remove attackers
3. `ActivatePatrolsAndSnipers()` - Enable AI
4. `GetPilot()` - Get pilot player
5. `GetGroupMembers()` - Count group members
6. `GetFarestWills()` - Find farthest villages
7. `DoTick_Willages()` - Village AI logic
8. `SetPlRun()` - Set player run mode
9. `ShowTrashes()` - Toggle crash site visibility
10. `DecideReward()` - Determine mission reward
11. `ScriptMain()` - Main entry point

**Decompiled Functions**:
1. `_init()` ✅ Detected correctly
2. `func_0292()` ⚠️ = DisapearAttackers (wrong name)
3. `func_0355()` ⚠️ = ActivatePatrolsAndSnipers
4. `func_0448()` ⚠️ = GetPilot/GetGroupMembers (merged?)
5. `func_0511()` ⚠️ = GetFarestWills
6. `func_0612()` ⚠️ = DoTick_Willages
7. `func_0985()` ⚠️ = SetPlRun
8. `func_0994()` ⚠️ = ShowTrashes
9. `func_1021()` ⚠️ = DecideReward
10. `ScriptMain()` ✅ Detected but broken

**Score**: 10/10 functions detected, but all have wrong names and some have broken logic.

---

### 5. Loop Detection - GOOD ✅

**Example 1 - Simple Loop**:
```c
// Original:
for (i=0; i<16; i++){
    pl = SC_P_GetBySideGroupMember(1,9,i);
    if ((pl)&&(SC_P_IsReady(pl))){
        SC_P_SetActive(pl,FALSE);
        SC_P_SetPos(pl,&pos);
    }
}

// Decompiled:
for (i = 0; (i < 16); i = i + 1) {
    if (!(i < 16)) break;  // ⚠️ Redundant check
    local_ = SC_P_GetBySideGroupMember(1, 9, i);
    if (!local_) {         // ⚠️ Logic inverted?
        SC_P_SetActive(local_, FALSE);
        SC_P_SetPos(local_, &local_2);
    } else {
        i++;               // ❌ Double increment!
    }
    SC_P_IsReady(local_);  // ❌ Missing if check
    if (!local_5) goto block_7; // ❌ Wrong control flow
}
```

**Status**: Loop structure detected ✅ but body has control flow errors ❌

---

### 6. Struct Field Access - NEEDS WORK ⚠️

**Original**:
```c
info->message
info->elapsed_time
info->next_exe_time
info->param1
info->param2
info->param3

initside.MaxHideOutsStatus
initside.MaxGroups
initgroup.SideId
initgroup.GroupId
```

**Decompiled**:
```c
param_0->field_20    // ❌ Should be next_exe_time
param_0->field_12    // ❌ Should be param3
local_88             // ❌ Should be info->param1

initside.field1      // ⚠️ Could map to field names
initgroup.field1
initgroup.field2
```

**Status**: Need struct field resolution (Phase 2 Fix #6)

---

### 7. External Function Calls - GOOD ✅

Most external function calls are correctly identified:
```c
SC_P_GetBySideGroupMember()  ✅
SC_P_IsReady()               ✅
SC_P_SetActive()             ✅
SC_P_SetPos()                ✅
SC_InitSide()                ✅
SC_InitSideGroup()           ✅
SC_SetSideAlly()             ✅
SC_sgi()                     ✅
SC_ggi()                     ✅
SC_SpeechRadio2()            ✅
SC_P_Speech2()               ✅
```

---

## Critical Issues Summary

### 🔴 CRITICAL (Must Fix)
1. **Switch statement on wrong variable** - Uses `g_showinfo_timer` instead of `info->message`
2. **Multiple duplicate switch statements** - Structure analysis completely broken
3. **Control flow errors in loops** - Double increments, inverted conditions, missing checks
4. **Array detection broken** - Most arrays detected as scalars

### 🟡 HIGH PRIORITY
5. **Variable naming incomplete** - Many `local_`, `tmp` variables remain
6. **Struct field names missing** - All fields show as `field_N`
7. **Function naming generic** - All functions named `func_NNNN`
8. **Global array sizes wrong** - `g_save[64]` should be `[2]`

### 🟢 WORKING WELL
- ✅ Loop counter naming (`i`, `j`, `idx`)
- ✅ Basic struct variable naming (`plinfo`, `initside`, `initgroup`)
- ✅ External function call detection
- ✅ Global variable name preservation
- ✅ Basic function detection (wrong names but structure OK)

---

## Root Cause Analysis

### Issue 1: Switch Statement Mismatch

**Suspected Cause**: The switch pattern detector is likely:
1. Finding a switch on `g_showinfo_timer` (which exists in the code)
2. Treating it as the main switch instead of the `info->message` switch
3. Possibly missing the actual message switch because it's using case values that need constant resolution

**Evidence**:
- Original has: `switch(info->message)` with cases `SC_LEV_MES_TIME`, `SC_LEV_MES_RADIOUSED`, etc.
- Decompiled has: `switch(g_showinfo_timer)` with numeric cases
- The constants (`SC_LEV_MES_TIME` = 0, etc.) may be confusing the detector

**Files to Check**:
- `vcdecomp/core/ir/structure/patterns/switch_case.py` - Switch detection logic
- `vcdecomp/core/ir/expr.py` - Constant resolution

### Issue 2: Control Flow in Loops

**Suspected Cause**:
1. Condition negation is happening incorrectly
2. Loop exit conditions being added as explicit checks
3. Short-circuit evaluation breaking into separate if statements

**Evidence**:
```c
// Should be:
if ((pl)&&(SC_P_IsReady(pl)))

// Becomes:
if (!local_) {
    // ...
} else {
    i++;
}
SC_P_IsReady(local_);
if (!local_5) goto block_7;
```

**Files to Check**:
- `vcdecomp/core/ir/structure/patterns/loops.py` - Loop body extraction
- `vcdecomp/core/ir/structure/analysis/condition.py` - Condition simplification

### Issue 3: Array Detection

**Suspected Cause**: Global array detection is not analyzing indexed access patterns.

**Files to Check**:
- `vcdecomp/core/ir/global_resolver.py` - Global type inference

---

## Next Steps

### Immediate Priority
1. **Fix switch statement detection** - Ensure main message handler switch is correctly identified
2. **Fix duplicate switch statements** - Only one switch should exist in ScriptMain
3. **Debug control flow** - Fix loop body condition inversion

### Phase 2 Completion
4. **Implement Fix #6** - Struct field name resolution
5. **Implement Fix #7** - Global array detection
6. **Implement Fix #9** - Constant value resolution for switch cases

### Testing
After fixes, recompile and validate:
```bash
py -m vcdecomp structure decompilation\pilot\LEVEL.SCR > decompilation\pilot\LEVEL_fixed.c
py -m vcdecomp validate decompilation\pilot\LEVEL.SCR decompilation\pilot\LEVEL_fixed.c
```

---

## Progress vs TDM Script

**TDM Script** (after Phase 1+2):
- ✅ Switch statements correct
- ✅ Loop bodies populated
- ✅ If/else branches correct
- ✅ Function returns correct
- ✅ Variable naming good (60%+)

**Pilot Script** (current):
- ❌ Switch statements completely broken
- ⚠️ Loop bodies have errors
- ❌ Control flow issues
- ⚠️ Variable naming partial (40%?)

**Conclusion**: Phase 1 fixes may not have fully addressed all control flow issues. The Pilot script is exposing more complex cases that weren't covered by TDM testing.
