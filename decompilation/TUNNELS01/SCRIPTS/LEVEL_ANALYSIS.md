# LEVEL.SCR Detailed Analysis

## Critical Findings from Disassembly Comparison

### 1. _init Function (IP 0-290)
**Purpose**: Initializes two large data structures in global memory

**Structure 1** (`data[1410]`): 256 bytes (64 dwords)
- Offsets 0-19: Five floats (0.0f each)
- Offsets 20-28: Three ints (100, 100, 100)
- Offsets 32-48: Five floats (0.0f each)
- Offsets 52-60: Three ints (100, 100, 100)
- Offset 64: int (-1)
- Offsets 68-80: Four floats (0.0f each)
- Offsets 84-88: Two ints (-1, -1)
- Offsets 92-100: Three ints (100, 45, 100)
- Offsets 104-108: Two floats (1.0f, 5.0f)
- Offset 112: float (0.0f)
- Offsets 116-124: Three ints (10, 10, 100)
- Offsets 128-132: Two ints (28, 90)
- Offsets 136-140: Two floats (0.0f, 10.0f)
- Offsets 144-156: Four floats (0.0f each)
- Offset 160: int (100)
- Offset 164: int (-1)
- Offsets 168-180: Four floats (0.0f each)
- Offsets 184-188: Two ints (-1, -1)
- Offset 192: int (100)
- Offset 196: int (-1)
- Offsets 200-212: Four floats (0.0f each)
- Offsets 216-220: Two ints (-1, -1)
- Offset 224: int (100)
- Offset 228: int (-1)
- Offsets 232-244: Four floats (0.0f each)
- Offsets 248-252: Two ints (-1, -1)
- Offset 256: int (100)

This appears to be an **array of structures** - likely player/AI configuration data.

**Structure 2** (`data[1732]`): 32 bytes (8 dwords)
- 8 floats all initialized to 0.0f

This is likely a **c_Vector3 array** or similar coordinate data.

### 2. Function Boundaries - CRITICAL ERROR IN DECOMPILATION

The decompiler MERGED multiple functions into `func_0291`. Looking at disassembly:

- **IP 291-312**: `AbsRandom(float)` - returns abs(frnd(param))
- **IP 313-331**: `EnablePlayer(dword)` - enables AI with combat settings
- **IP 332-353**: `DisablePlayer(dword)` - disables AI
- **IP 354-370**: `SendMessage(dword, int, int)` - sends script message

These should be **4 separate functions**, not one!

### 3. ScriptMain Entry Point (IP 9054)

**Parameters** (from `s_SC_L_info *info`):
- `info->field_20` (offset +20): Frame time multiplier (set to 0.2f or 0.5f)
- `info->param1` (offset +4 from [sp-4]): Message/event parameter
- `info->elapsed_time`: Delta time for updates

**Structure**:
```
switch (gphase) {
  case 0:  // Initialization
  case 1:  // Intro cutscene/dialog
  case 2:  // Main gameplay (missing in decompiled!)
  case 4:  // Message handler
  case 7:  // Object initialization
  case 8:  // Unknown
  case 11: // Unknown
  default: // Save handler
}
```

### 4. Phase System

**Phase 0**: Level initialization
- Sets mission ID = 9
- Initializes sides (0=US, 1=VC)
- Initializes groups:
  - Side 0, Group 0: 4 players, 30.0f radius
  - Side 1, Group 0: 9 players
  - Side 1, Group 1: 16 players
  - Side 1, Group 2: 16 players
  - Side 1, Group 3: 9 players
- Disables group enemy updates for VC groups
- Sets command menu = 2009
- **Immediately transitions to Phase 1** (no waiting!)

**Phase 1**: Intro sequence
- Plays radio dialogs (916-920, 933-937)
- Player movement disabled during intro
- Uses `SC_RadioBatch_Begin/End()` for batched radio
- Calls `func_0291()` for timing delays
- **Transitions to Phase 2**

**Phase 2**: Main gameplay loop (MISSING PROPER DECODE!)
- Calls `func_7697()` - Active place updates
- Calls `func_7807()` - VC AI updates
- This is the MAIN UPDATE LOOP that runs every frame!

**Phase 4**: Message handler
- Checks `info->param1 == 51` (message ID)
- Calls `func_8934(info)` to handle message
- Returns immediately after handling

**Phase 7**: Object scripts
- Calls `func_8919()` - sets object scripts

**Phase 8/11**: Unknown handlers
- Call `func_8932()` and `func_8933()`

**Default**: Save game handler
- Uses `save[]` array indexed by `info->param1`
- Creates save points with IDs 9110-9115

### 5. Message Handler (case 4)

The decompiled code shows:
```c
case 4:
    break;
```

But disassembly shows:
```asm
9091: LCP  [sp+20]           ; Load gphase
9092: GCP  data[2272]  ; = 4
9093: EQU
9094: JZ   label_9111
9095: LADR [sp-4]            ; Load info pointer
9096: DADR 4                 ; Add 4 (get info->param1)
9097: DCP  4                 ; Load value
9100: LCP  [sp+21]           ; Load info->param1
9101: GCP  data[2273]  ; = 51
9102: EQU                    ; Compare
9103: JZ   label_9108
9104: LCP  [sp-4]            ; Load info
9105: CALL func_8934         ; Handle message 51
```

**Correct code**:
```c
case 4: // Message handler
    if (info->param1 == 51) {
        func_8934(info);  // Handle object interaction message
    }
    break;
```

### 6. Global Variable Mapping

From disassembly analysis:

| Data Offset | Variable Name | Type | Purpose |
|-------------|---------------|------|---------|
| data[945] | gphase | int | Current level phase |
| data[1410] | player_data | struct[4] | Player/AI configuration array |
| data[1732] | vector_data | c_Vector3[2-3] | Position/waypoint data |
| data[0] | CONST_ZERO | float | Constant 0.0f |
| data[1] | CONST_ONE | int | Constant 1 |
| data[2] | CONST_ONE | int | Constant 1 |

### 7. Function Call Analysis

**func_4948(int objectiveID)**:
- Called with IDs: 901, 902, 1475
- Likely sets objectives or triggers

**func_5197()**:
- Called during initialization (phase 0)
- No parameters
- Probably initializes level-specific data

**func_6873()**:
- Called after objectives setup
- No parameters
- Possibly spawns AI or initializes groups

**func_7697(c_Vector3 *playerPos, float deltaTime)**:
- Called every frame in phase 2
- Updates active places/trigger zones
- Returns early if player too far

**func_7807(c_Vector3 *playerPos, float deltaTime)**:
- Called every frame in phase 2
- Main VC AI state machine
- Controls VC behavior based on vc1stat

**func_8919()**:
- Sets object scripts for interactive items:
  - "grenadebedna" -> openablecrate.c
  - "n_poklop_01" -> poklop.c
  - "d_past_04_01" -> past.c

**func_8934(s_SC_L_info *info)**:
- Handles message 51 (object interaction)
- Checks object names and triggers player speech
- Sets flags: crateuse, doorsuse

### 8. AI State Machine (vc1stat)

From `func_7807()` disassembly:

**State 0**: Initial/idle
- Checks if VC group 1 member 0 is ready
- Checks for enemies
- Plays speech 926 (warning)
- Transitions to state 1

**State 1**: Warning phase
- Waits for player response
- If VC dies: speech 927, state 100
- If player near vcrunpoint (5.0f): set battle mode, state 2

**State 2**: Combat initiated
- Waits for VC to start shooting
- When shooting: speech 929, state 3

**State 3**: Active combat
- Checks if VC died: speech 927, state 100
- Timer increments with deltaTime
- After 3.0s: VC retreats to vcrunpoint2, speech 930, state 4

**State 4**: Retreating
- If player follows: re-engage battle, state 5

**State 5**: Final combat
- Checks if entire group (members 0,4,5) dead
- When all dead: vcgroup2 = 1, speech 931

**State 100**: Dead/inactive
- VC group no longer active

### 9. Digger AI System

Controlled by `vcdiggers` variable:

**vcdiggers == 0**: Initial state
- Diggers working peacefully

**vcdiggers == 100**: Combat state
- Triggered when any digger (group 1, members 0-2) detects enemy
- All 3 diggers switch to battle mode
- Play alert speech (947 or 948, random)

**vcdiggers == 2**: Working behavior
- Timer-based movement between diggers
- Every 20+ seconds, pick random digger as target
- Move digger #2 to target position
- Creates illusion of workers moving around

### 10. Critical Errors in My Reconstruction

1. **Missing Phase 2 case** - The main gameplay loop!
2. **Wrong case 4 implementation** - It's a message handler, not save handler
3. **Function separation** - Multiple functions merged in decompiler output
4. **Initialization sequence** - Phase 0 immediately goes to Phase 1, then Phase 2
5. **info->param1 usage** - Used for both messages (case 4) and save IDs (default case)
6. **Frame timing** - field_20 is frame time multiplier, not delta time
7. **Function signatures** - Many helper functions have wrong parameter counts

### 11. Correct Phase Flow

```
_init() called once at load
  ↓
ScriptMain() called repeatedly
  ↓
Phase 0 (first call):
  - Initialize level
  - Set gphase = 1
  ↓
Phase 1 (next call):
  - Play intro dialogs
  - Set gphase = 2
  ↓
Phase 2 (every frame):
  - Update active places
  - Update VC AI
  - Main gameplay
  ↓
Phase 4 (on message 51):
  - Handle object interaction
  ↓
Default (on save trigger):
  - Save game state
```

### 12. Save System

Uses `save[]` array with `info->param1` as index:
- Checks if `save[info->param1] == 0`
- If never saved: calls `SC_MissionSave()` with ID 9110-9115
- Sets `save[info->param1] = 1` to prevent re-saving

Save IDs found in code:
- 9110, 9111, 9112, 9113, 9114, 9115

Each corresponds to a different checkpoint location.

### 13. Speech/Dialog System

Radio batches for coordinated dialog:
```c
SC_RadioBatch_Begin();
  Player speech
  Radio delay
  Radio response
  Player speech
  Radio delay
  Radio response
SC_RadioBatch_End();
```

Speech IDs:
- 900-902: Initial briefing
- 916-920: First radio batch
- 923: Grenade crate found
- 925: Booby trap found
- 926: VC warning
- 927: VC defeated
- 929: VC engaging
- 930: VC retreating
- 931: All VC dead
- 933-937: Second radio batch
- 938: Hatch found
- 947-948: Digger alert (random)

### Recommendations for Reconstruction

1. **Split func_0291** into 4+ separate functions
2. **Add Phase 2 case** with proper update loop
3. **Fix case 4** to handle messages correctly
4. **Add proper comments** explaining phase transitions
5. **Document message IDs** and their meanings
6. **Fix function signatures** based on disassembly
7. **Add timing constants** (3.0f combat timer, 20.0f digger timer)
8. **Document data structures** properly (especially data[1410] array)
