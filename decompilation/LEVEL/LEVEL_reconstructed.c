/*
 * LEVEL.c - Level Script (Reconstructed)
 * Decompiled from LEVEL.SCR using vcdecomp
 *
 * Mission: LIK_Tunnels (Tunnels mission - Vietnamese tunnels exploration)
 * Level folder: levels\LIK_Tunnels\data\Tunnels01\
 *
 * This is a single-player mission level script containing:
 * - AI control for VC (Vietcong) units
 * - Alarm and detection systems
 * - Traps (grenade cans, claymores)
 * - Mission objectives and save points
 * - Waypoint system for AI navigation
 * - Radio communication with command
 * - Interactive objects (crates, hatches/poklop)
 * - Save/load functionality with state preservation
 *
 * Statistics:
 * - Instructions: 10,051
 * - Basic blocks: 1,061
 * - Functions: 26
 * - External functions: 97
 *
 * Key objects:
 * - "grenadebedna" - Grenade crate (interactable)
 * - "n_poklop_01" - Hatch/trapdoor
 * - "granat_v_plechovce2#3" - Grenade in tin can (trap)
 * - "Plechovka" - Tin can (trap trigger)
 * - "Konec dratu" - End of wire (trap)
 *
 * External scripts referenced:
 * - levels\LIK_Tunnels\data\Tunnels01\scripts\openablecrate.c
 * - levels\LIK_Tunnels\data\Tunnels01\scripts\poklop.c
 * - levels\LIK_Tunnels\data\Tunnels01\scripts\past.c
 */

#include "inc\sc_global.h"
#include "inc\sc_def.h"

// ============================================================================
// GLOBAL VARIABLES (mapped from data segment via save info)
// ============================================================================

// Save info structure - for SC_MissionSave() function calls
// NOTE: s_SC_MissionSave is only 12 bytes (savename_id, description_id, disable_info)
// The actual game state is stored in separate global variables below
s_SC_MissionSave sav_info;                    // offset 0 (12 bytes)

// Mission state machine
int gphase;                                    // offset 128 - Current mission phase
int lastorder;                                 // offset 160 - Last order given
int pointstatus;                               // offset 192 - Point/checkpoint status
int alarmtype;                                 // offset 224 - Type of alarm triggered
int alarmer;                                   // offset 256 - Who triggered alarm
int enemydangertext;                           // offset 288 - Enemy danger text ID
int reportedcontact;                           // offset 320 - Contact reported flag
int trapfound;                                 // offset 352 - Trap found flag
int alarms;                                    // offset 384 - Alarm counter/state

// Objectives system
s_SC_Objective Objectives[4];                  // offset 416 - Mission objectives array
int objcount;                                  // offset 544 - Number of objectives
int music;                                     // offset 576 - Music state

// Active places (array of waypoints/checkpoints)
c_Vector3 AP[100];                             // Active places array
int save_crateuse;                             // Crate use state
int save_doorsuse;                             // Doors use state
int vcrunpoint;                                // VC run point
int vcrunpoint2;                               // VC run point 2
int vc1stat;                                   // VC1 status
int vcdiggers;                                 // VC diggers state
int diggertarget;                              // Digger target
int vc1timer;                                  // VC1 timer
int vcdiggertimer;                             // VC digger timer
int vcgroup1;                                  // VC group 1 state
int vcgroup2;                                  // VC group 2 state
int diggerstart;                               // Digger start flag
int vc1digtimer;                               // VC1 dig timer
int vc2digtimer;                               // VC2 dig timer

// Player/team arrays
dword players[16];                             // Player handles
c_Vector3 playerpos[16];                       // Player positions

// ============================================================================
// CONSTANTS
// ============================================================================

#define MAX_TRAPS           10
#define MAX_OBJECTIVES      4
#define MAX_PLAYERS         16
#define ALARM_NONE          0
#define ALARM_SPOTTED       1
#define ALARM_HEARD         2

// AI mode constants from sc_global.h:
// SC_P_AI_MODE_SCRIPT = 0  (peace/script-controlled mode)
// SC_P_AI_MODE_BATTLE = 1  (battle mode)
// Note: Original code uses "PEACE" but sc_global.h defines it as "SCRIPT"
#ifndef SC_P_AI_MODE_SCRIPT
#define SC_P_AI_MODE_SCRIPT 0
#endif
#ifndef SC_P_AI_MODE_BATTLE
#define SC_P_AI_MODE_BATTLE 1
#endif
// Alias for compatibility with reconstructed code
#define SC_P_AI_MODE_PEACE SC_P_AI_MODE_SCRIPT

// ============================================================================
// FORWARD DECLARATIONS
// ============================================================================

// Helper functions
float AbsRand(float range);                    // func_0291 - Absolute random
void SendMessage(int msg, int param, dword player); // func_0354
int CheckDanger(dword player, int side, int group); // func_0371
void SaveWeapons(void);                        // func_0883
void LoadWeapons(void);                        // func_1054
void SaveAmmoState(void);                      // func_1111 - Save ammo to global vars
void SaveIntelState(void);                     // func_1146 - Save intel to global vars
void LoadIntelState(void);                     // func_1180 - Load intel from global vars
void InitLevel(void);                          // func_1223

// Trap/Node helper functions
void GetNodePosition(char *nodename, c_Vector3 *pos); // func_3368
float GetNodeRotation(char *nodename);         // func_3388
void InitTraps(void);                          // trap init (uses helpers)
void AddTrap(int index, c_Vector3 *pos);       // func_4180
void RemoveTrap(int index);                    // func_4376
float GetDistanceToPlayer(dword player, c_Vector3 *targetpos); // func_4575
void SetPlayerSpecAnims(dword player);         // func_4594

// AI functions
void SetupVCUnit(dword player);                // func_4948
void UpdateVCGroup(int group);                 // func_5197
int GetEventValue(int eventtype, int param);   // func_6196 - Event type mapper
void UpdateObjectives(void);                   // func_6259

// Waypoint functions
void InitWaypoints(void);                      // func_6804
void UpdateWaypoints(void);                    // func_6873
void GetMyGroup(dword player, int *group);     // func_6984
void SetCheckpoint(int index, c_Vector3 *pos); // func_7043

// Main functions
void MainLoop(void);                           // func_7697
void ProcessPhase(int phase);                  // func_7807
void OnObjectUse(void *node);                  // func_8934 - Object interaction
void ScriptMain(int eventtype, int phase, int param2); // Entry point @9054

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/*
 * AbsRand - Returns absolute value of random number
 * func_0291 @291-312
 *
 * Disassembly:
 *   291: ASP 1
 *   292: ASP 1
 *   293: LCP [sp-4]           ; param
 *   294: ASP 1
 *   295: XCALL $frnd          ; frnd(param)
 *   296: LLD [sp+1]
 *   297: SSP 1
 *   298: LADR [sp+0]
 *   299: ASGN
 *   300: SSP 1
 *   301: LCP [sp+0]           ; local_0
 *   302: GCP data[0]          ; 0
 *   303: FLES                 ; local_0 < 0
 *   304: JZ label_0310
 *   305: LCP [sp+0]
 *   306: FNEG
 *   307: LADR [sp+0]
 *   308: ASGN                 ; local_0 = -local_0
 *   309: SSP 1
 *   310: RET
 */
float AbsRand(float range) {
    float result;

    result = frnd(range);
    if (result < 0.0f) {
        result = -result;
    }
    return result;
}

/*
 * SetBattleMode - Put player into battle mode
 * Block 4 @313-331 (part of func_0291 continuation)
 */
void SetBattleMode(dword player) {
    SC_P_Ai_SetMode(player, SC_P_AI_MODE_BATTLE);
    SC_P_Ai_EnableShooting(player, TRUE);
    SC_P_Ai_EnableSituationUpdate(player, 1);
    SC_Log(3, "Player %d enabled", player);  // Log level 3
}

/*
 * SetPeaceMode - Put player into peace mode
 * Block 5 @332-353
 */
void SetPeaceMode(dword player) {
    SC_P_Ai_SetMode(player, SC_P_AI_MODE_PEACE);
    SC_P_Ai_EnableShooting(player, FALSE);
    SC_P_Ai_EnableSituationUpdate(player, 0);
    SC_P_Ai_Stop(player);
    SC_Log(3, "Player %d disabled", player);  // Log level 3
}

/*
 * SendMessage - Send script message to player
 * func_0354 @354-370
 *
 * If player is valid, sends message. Otherwise logs error.
 */
void SendMessage(int msg, int param, dword player) {
    if (player) {
        SC_P_ScriptMessage(player, param, msg);
    } else {
        SC_Log(4, "Message %d %d to unexisted player!", param, msg);  // Log level 4 (warning)
    }
}

/*
 * CheckGroupDanger - Check if group has enemies or danger
 * func_0371 @371-434
 *
 * Returns 1 if danger detected, 0 otherwise
 */
int CheckGroupDanger(int side, int group, dword *member) {
    dword pl;
    float danger;
    int enemies;

    // Get first member of group
    pl = SC_P_GetBySideGroupMember(side, group, 0);
    *member = pl;

    // Check for sure enemies
    enemies = SC_P_Ai_GetSureEnemies(pl);
    if (enemies) {
        return 1;
    }

    // Check danger level
    danger = SC_P_Ai_GetDanger(pl);
    if (danger > 0.5f) {
        return 1;
    }

    return 0;
}

/*
 * CheckPlayerDanger - Check if specific player has danger
 * Block 15-19 @410-434
 */
int CheckPlayerDanger(dword player) {
    float danger;
    int enemies;

    enemies = SC_P_Ai_GetSureEnemies(player);
    if (enemies) {
        return 1;
    }

    danger = SC_P_Ai_GetDanger(player);
    if (danger > 0.5f) {
        return 1;
    }

    return 0;
}

/*
 * SetAiDisablePeaceCrouch - Set AI property disable_peace_crouch
 * Block 20 @435-453
 */
void SetAiDisablePeaceCrouch(dword player, int value) {
    s_SC_P_AI_props aiprops;

    SC_ZeroMem(&aiprops, sizeof(s_SC_P_AI_props));
    SC_P_Ai_GetProps(player, &aiprops);
    aiprops.disable_peace_crouch = value;
    SC_P_Ai_SetProps(player, &aiprops);
}

/*
 * SetAiHearDistance - Set AI property hear_distance_mult
 * Block 21 @454-472
 */
void SetAiHearDistance(dword player, float mult) {
    s_SC_P_AI_props aiprops;

    SC_ZeroMem(&aiprops, sizeof(s_SC_P_AI_props));
    SC_P_Ai_GetProps(player, &aiprops);
    aiprops.hear_distance_mult = mult;
    SC_P_Ai_SetProps(player, &aiprops);
}

/*
 * SetAiShootImprecision - Set AI property shoot_imprecision (multiplied)
 * Block 22 @473-495
 */
void SetAiShootImprecision(dword player, float mult) {
    s_SC_P_AI_props aiprops;

    SC_ZeroMem(&aiprops, sizeof(s_SC_P_AI_props));
    SC_P_Ai_GetProps(player, &aiprops);
    aiprops.shoot_imprecision = aiprops.shoot_imprecision * mult;
    SC_P_Ai_SetProps(player, &aiprops);
}

/*
 * SetAiShootDamage - Set AI property shoot_damage_mult (multiplied)
 * Block 23 @496-518
 */
void SetAiShootDamage(dword player, float mult) {
    s_SC_P_AI_props aiprops;

    SC_ZeroMem(&aiprops, sizeof(s_SC_P_AI_props));
    SC_P_Ai_GetProps(player, &aiprops);
    aiprops.shoot_damage_mult = aiprops.shoot_damage_mult * mult;
    SC_P_Ai_SetProps(player, &aiprops);
}

/*
 * SetAiGrenadeEnabled - Enable/disable grenade throwing
 * Block 24-27 @519-545
 */
void SetAiGrenadeEnabled(dword player, int enabled) {
    s_SC_P_AI_props aiprops;

    SC_ZeroMem(&aiprops, sizeof(s_SC_P_AI_props));
    SC_P_Ai_GetProps(player, &aiprops);

    if (enabled) {
        aiprops.grenade_sure_time = 5.0f;
    } else {
        aiprops.grenade_sure_time = 1000.0f;
    }

    SC_P_Ai_SetProps(player, &aiprops);
}

/*
 * SetAiBerserk - Set AI berserk mode
 * Block 28 @546-564
 */
void SetAiBerserk(dword player, int berserk) {
    s_SC_P_AI_props aiprops;

    SC_ZeroMem(&aiprops, sizeof(s_SC_P_AI_props));
    SC_P_Ai_GetProps(player, &aiprops);
    aiprops.berserk = berserk;
    SC_P_Ai_SetProps(player, &aiprops);
}

/*
 * GetCurrentMission - Get current mission number
 * Block 29 @565-572
 */
int GetCurrentMission(void) {
    return SC_ggi(SGI_CURRENTMISSION);
}

/*
 * GetChopper - Get chopper state
 * Block 30 @573-580
 */
int GetChopper(void) {
    return SC_ggi(SGI_CHOPPER);
}

/*
 * GetPlayerInfo - Get player info
 * Block 31 @581-589
 */
void GetPlayerInfo(dword player, s_SC_P_getinfo *info) {
    SC_P_GetInfo(player, info);
}

// ============================================================================
// SAVE/LOAD FUNCTIONS
// ============================================================================

/*
 * SaveWeapons - Save current player weapons to global vars
 * func_0883 @883-1053
 *
 * This function reads weapon slots from current player and saves them
 * to global variables (101-109) for later restoration.
 */
void SaveWeapons(void) {
    dword pc;
    s_SC_P_Create pinfo;
    int slot;

    pc = SC_PC_Get();

    if (SC_P_GetWeapons(pc, &pinfo)) {
        // Save weapon slot 1
        if (pinfo.weap_slot1 != 0 && pinfo.weap_slot1 != 255) {
            SC_sgi(101, pinfo.weap_slot1);
        } else {
            SC_sgi(101, 255);
        }

        // Save weapon slot 2
        if (pinfo.weap_slot2 != 0 && pinfo.weap_slot2 != 255) {
            SC_sgi(102, pinfo.weap_slot2);
        } else {
            SC_sgi(102, 255);
        }

        // Save weapon slot 3
        if (pinfo.weap_slot3 != 0 && pinfo.weap_slot3 != 255) {
            SC_sgi(103, pinfo.weap_slot3);
        } else {
            SC_sgi(103, 255);
        }

        // TODO: Implement slots 4-9 (similar pattern to slots 1-3)
        // Original disassembly shows complete weapon slot saving logic
    }
}

/*
 * LoadWeapons - Load saved weapons back to player
 * func_1054 @1054-1110
 */
void LoadWeapons(void) {
    dword pc;
    int slot;

    pc = SC_PC_Get();

    // Restore each weapon slot from global vars
    slot = SC_ggi(101);
    if (slot != 255) {
        SC_P_SetAmmoInWeap(pc, 0, slot);
    }

    // TODO: Implement loading for slots 2-9 (similar pattern)
    // See SaveWeapons() for the corresponding save logic
}

/*
 * SaveAmmoState - Save player ammo state to global variables
 * func_1111 @1111-1145
 *
 * Saves current weapon ammo counts to global game variables using SC_sgi
 * and SC_P_WriteAmmoToGlobalVar for persistence across save/load.
 */
void SaveAmmoState(void) {
    dword pc;
    int ammo;

    pc = SC_PC_Get();

    // Write ammo for weapon slot 1 to global var 0x01000000
    SC_P_WriteAmmoToGlobalVar(pc, 1, 0x01000000);

    // Save ammo count from weapon slot 256 (0x100) to global var 0x10000
    ammo = SC_P_GetAmmoInWeap(pc, 256);
    SC_sgi(0x10000, ammo);

    // Save ammo count from weapon slot 0 to global var 1
    ammo = SC_P_GetAmmoInWeap(pc, 0);
    SC_sgi(1, ammo);
}

/*
 * SaveIntelState - Save player intel to global variables
 * func_1146 @1146-1179
 *
 * Gets player intel structure and saves each field to global vars
 * using SC_sgi for persistence. Used before mission completion.
 */
void SaveIntelState(void) {
    s_SC_P_intel intel;
    int i;
    int *intel_ptr;

    // Get current player intel
    SC_PC_GetIntel(&intel);

    // Save intel fields to global variables
    // Base address 0x3F000000 with stride 0x13F0000
    intel_ptr = (int*)&intel;
    for (i = 0; i < 10; i++) {
        SC_sgi(0x3F000000 + i, intel_ptr[i * 5]);  // Approximate - needs verification
    }
}

/*
 * LoadIntelState - Load player intel from global variables
 * func_1180 @1180-1217 (unlabeled in disassembly, after func_1146)
 *
 * Reads intel values from global vars and applies to player.
 */
void LoadIntelState(void) {
    s_SC_P_intel intel;
    int i;
    int *intel_ptr;

    // Initialize intel structure
    intel_ptr = (int*)&intel;

    // Load intel fields from global variables
    // Starts from index 319 and decrements (based on data[143] = 319)
    for (i = 319; i >= 0; i--) {
        intel_ptr[i] = SC_ggi(i);  // Approximate - needs verification
    }

    // Apply intel to player
    SC_PC_SetIntel(&intel);
}

// ============================================================================
// INITIALIZATION
// ============================================================================

/*
 * InitLevel - Initialize level script
 * func_1223 @1223-3367
 *
 * This is a large initialization function that sets up:
 * - Player teams
 * - VC unit configurations
 * - Initial AI states
 * - Objectives
 * - Waypoints
 */
void InitLevel(void) {
    s_SC_initside initside;
    s_SC_initgroup initgroup;
    c_Vector3 pos;
    int i;
    int difficulty;

    // Get difficulty level
    difficulty = SC_ggi(SGI_DIFFICULTY);
    SC_message("Level difficulty is %d", difficulty);

    // Initialize sides
    SC_ZeroMem(&initside, sizeof(s_SC_initside));
    initside.side = SC_P_SIDE_VC;
    // ... setup initside fields
    SC_InitSide(SC_P_SIDE_VC, &initside);

    // Initialize groups
    SC_ZeroMem(&initgroup, sizeof(s_SC_initgroup));
    initgroup.side = SC_P_SIDE_VC;
    initgroup.group = 0;
    // ... setup initgroup fields
    SC_InitSideGroup(&initgroup);

    // Setup AI behavior
    SC_Ai_SetShootOnHeardEnemyColTest(1);
    SC_Ai_SetGroupEnemyUpdate(SC_P_SIDE_VC, 0, 1);

    // Setup command menu
    SC_SetCommandMenu(1);

    // Enable player controls
    SC_PC_EnableMovement(1);
    SC_PC_EnableRadioBreak(1);

    // Initialize objectives
    objcount = 0;
    SC_ZeroMem(&Objectives, sizeof(Objectives));

    // Initialize waypoints
    InitWaypoints();

    // Initialize traps
    InitTraps();

    // Set initial phase
    gphase = 1;
}

// ============================================================================
// TRAP FUNCTIONS
// ============================================================================

/*
 * GetNodePosition - Get world position of a named node
 * func_3368 @3368-3387
 *
 * Helper function to get node position by name.
 * Returns position via pointer parameter.
 */
void GetNodePosition(char *nodename, c_Vector3 *pos) {
    void *node;

    node = SC_NOD_Get(0, nodename);
    if (node != 0) {
        SC_NOD_GetWorldPos(node, pos);
    }
}

/*
 * GetNodeRotation - Get world rotation Z of a named node
 * func_3388 @3388-3413
 */
float GetNodeRotation(char *nodename) {
    void *node;

    node = SC_NOD_Get(0, nodename);
    if (node != 0) {
        return SC_NOD_GetWorldRotZ(node);
    }
    return 0.0f;
}

/*
 * InitTraps - Initialize trap system
 * (actual initialization happens in InitLevel, these are helper funcs)
 */
void InitTraps(void) {
    int i;
    c_Vector3 pos;

    // Trap initialization uses GetNodePosition to find trap objects
    // like "Plechovka" (tin can) and "Konec dratu" (wire end)
    for (i = 0; i < MAX_TRAPS; i++) {
        // Each trap consists of a can and wire trigger
        // GetNodePosition(trapname, &pos);
    }
}

/*
 * AddTrap - Add a trap at position
 * func_4180 @4180-4375
 */
void AddTrap(int index, c_Vector3 *pos) {
    void *node;
    char nodename[64];

    sprintf(nodename, "trap_%d", index);
    SC_message("adding trap on pos %d", index);

    // Get the can object (Plechovka = tin can in Czech)
    node = SC_NOD_Get(0, "Plechovka");
    if (!node) {
        SC_message("trap not found!!!");
        return;
    }

    // Get wire end object
    node = SC_NOD_Get(0, "Konec dratu");  // "End of wire"

    // TODO: Setup trap collision/trigger
}

/*
 * RemoveTrap - Remove a trap
 * func_4376 @4376-4574
 */
void RemoveTrap(int index) {
    SC_message("removing trap %d", index);

    // TODO: Implement trap removal logic from func_4376
}

/*
 * GetDistanceToPlayer - Calculate distance from player to a position
 * func_4575 @4575-4593
 *
 * Takes player ID and target position, returns distance.
 */
float GetDistanceToPlayer(dword player, c_Vector3 *targetpos) {
    c_Vector3 playerpos;
    float dist;

    // Get player position
    SC_P_GetPos(player, &playerpos);

    // Calculate distance
    dist = SC_2VectorsDist(&playerpos, targetpos);

    return dist;
}

/*
 * SetPlayerSpecAnims - Set special animations for player
 * func_4594 @4594-4633
 *
 * s_SC_P_SpecAnims has array sa[5] with indexes:
 *   SC_PL_SA_STATIV=0, SC_PL_SA_ENEMYSPOTTED=1, SC_PL_SA_WALK=2,
 *   SC_PL_SA_RUN=3, SC_PL_SA_DEATH=4
 */
void SetPlayerSpecAnims(dword player) {
    s_SC_P_SpecAnims anims;

    SC_ZeroMem(&anims, sizeof(s_SC_P_SpecAnims));

    // Setup animation filenames (relative to G\CHARACTERS\Anims\specmove\)
    // Based on disassembly data values - these are string pointers
    // The actual values need verification from string data section

    SC_P_SetSpecAnims(player, &anims);
}

// ============================================================================
// AI FUNCTIONS
// ============================================================================

/*
 * SetupVCUnit - Setup a VC (Vietcong) AI unit
 * func_4948 @4948-5196
 */
void SetupVCUnit(dword player) {
    s_SC_P_AI_props aiprops;
    int difficulty;

    // Get difficulty
    difficulty = SC_ggi(SGI_DIFFICULTY);

    // Setup AI properties based on difficulty
    SC_ZeroMem(&aiprops, sizeof(s_SC_P_AI_props));
    SC_P_Ai_GetProps(player, &aiprops);

    // Adjust based on difficulty
    if (difficulty == 0) {
        // Easy
        aiprops.shoot_imprecision = aiprops.shoot_imprecision * 1.5f;
        aiprops.shoot_damage_mult = aiprops.shoot_damage_mult * 0.5f;
    } else if (difficulty == 1) {
        // Medium
        // Default settings
    } else {
        // Hard
        aiprops.shoot_imprecision = aiprops.shoot_imprecision * 0.8f;
        aiprops.shoot_damage_mult = aiprops.shoot_damage_mult * 1.2f;
    }

    SC_P_Ai_SetProps(player, &aiprops);

    // Set battle mode
    SC_P_Ai_SetMode(player, SC_P_AI_MODE_PEACE);
    SC_P_Ai_EnableShooting(player, FALSE);
}

/*
 * UpdateVCGroup - Update VC group behavior
 * func_5197 @5197-6195
 */
void UpdateVCGroup(int group) {
    dword leader;
    dword member;
    c_Vector3 leaderpos;
    int i;
    int membercount;

    // Get group leader
    leader = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, group, 0);
    if (!leader) return;

    // Get leader position
    SC_P_GetPos(leader, &leaderpos);

    // Count members
    membercount = SC_GetGroupPlayers(SC_P_SIDE_VC, group);

    if (membercount > 5) {
        SC_message("GetMyGroup: TOO much players in group around!");
    }

    // Update each member
    for (i = 1; i < membercount; i++) {
        member = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, group, i);

        // TODO: Check if member should follow leader
        // TODO: Implement formation/follow logic
    }
}

/*
 * GetEventValue - Map event type to return value
 * func_6196 @6196-6258
 *
 * Switch/case function that maps event types to specific return values.
 * Used for event handling logic in ScriptMain.
 */
int GetEventValue(int eventtype, int param) {
    // Based on disassembly - cascading if/else for event type mapping
    // The data values are packed integers, actual event IDs need verification

    if (eventtype == 29) {
        return 29;
    }

    if (eventtype == 14) {
        if (param == 0) {
            return 14;
        }
        if (param == 14) {
            return 2;
        }
    }

    if (eventtype == 2) {
        if (param < 2) {
            return 2;
        }
    }

    if (eventtype == 11) {
        if (param != 0) {
            return 11;
        }
    }

    return 11;  // default
}

/*
 * UpdateObjectives - Update mission objectives
 * func_6259 @6259-6803
 */
void UpdateObjectives(void) {
    int i;

    for (i = 0; i < objcount; i++) {
        // TODO: Check objective completion conditions
        // TODO: Update objective status using SC_SetObjectives
    }
}

// ============================================================================
// WAYPOINT FUNCTIONS
// ============================================================================

/*
 * InitWaypoints - Initialize waypoint system
 * func_6804 @6804-6872
 */
void InitWaypoints(void) {
    int i;
    char wpname[64];
    c_Vector3 pos;

    // Load active places
    for (i = 0; i < 100; i++) {
        sprintf(wpname, "ACTIVEPLACE#%d", i);
        if (SC_GetWp(wpname, &pos)) {
            AP[i] = pos;
        }
    }
}

/*
 * UpdateWaypoints - Update waypoint-related logic
 * func_6873 @6873-6983
 */
void UpdateWaypoints(void) {
    // TODO: Update waypoint triggers
    // TODO: Check player proximity to waypoints using SC_IsNear3D
}

/*
 * GetMyGroup - Get player's group
 * func_6984 @6984-7042
 */
void GetMyGroup(dword player, int *group) {
    s_SC_P_getinfo info;

    SC_P_GetInfo(player, &info);
    *group = info.group;
}

/*
 * SetCheckpoint - Set a checkpoint position
 * func_7043 @7043-7696
 */
void SetCheckpoint(int index, c_Vector3 *pos) {
    char wpname[64];

    sprintf(wpname, "WayPoint#%d", index);
    SC_GetWp(wpname, pos);
}

// ============================================================================
// MAIN FUNCTIONS
// ============================================================================

/*
 * MainLoop - Main update loop called every frame
 * func_7697 @7697-7806
 */
void MainLoop(void) {
    dword pc;
    c_Vector3 pcpos;

    // Get player
    pc = SC_PC_Get();
    SC_PC_GetPos(&pcpos);

    // Update traps
    UpdateTraps();

    // Update objectives
    UpdateObjectives();

    // Update AI groups
    UpdateVCGroup(0);
    UpdateVCGroup(1);

    // Process current phase
    ProcessPhase(gphase);
}

/*
 * ProcessPhase - Process mission phase
 * func_7807 @7807-8918
 *
 * This is the main state machine for the mission.
 */
void ProcessPhase(int phase) {
    dword pc;
    c_Vector3 pcpos;

    pc = SC_PC_Get();
    SC_PC_GetPos(&pcpos);

    switch (phase) {
        case 0:
            // Initial state
            break;

        case 1:
            // Phase 1 - Mission start
            // Check for trigger conditions
            break;

        case 2:
            // Phase 2 - First objective
            break;

        case 3:
            // Phase 3 - Combat phase
            break;

        // ... more phases based on mission progression

        case 100:
            // Mission complete
            SC_message("MISSION COMPLETE");
            SC_MissionCompleted();
            SC_MissionDone();
            break;
    }
}

// ============================================================================
// OBJECT INTERACTION CALLBACKS
// ============================================================================

/*
 * OnObjectUse - Called when player interacts with object
 * func_8934 @8934-9053
 *
 * Handles interaction with grenade crates, hatches, and traps
 */
void OnObjectUse(void *node) {
    dword pc;
    float speechtime;
    char *nodename;

    pc = SC_PC_Get();
    speechtime = SC_P_GetWillTalk(pc);

    // Get object name
    nodename = SC_NOD_GetName(node);

    // Check for grenade crate
    if (SC_StringSame(nodename, "grenadebedna")) {
        SC_P_Speech2(pc, 923, &speechtime);
        speechtime += 0.1f;
        save_crateuse = 1;
        return;
    }

    // Check for hatch/trapdoor
    if (SC_StringSame(nodename, "n_poklop_01")) {
        SC_P_Speech2(pc, 938, &speechtime);
        speechtime += 0.1f;
        save_doorsuse = 1;
        return;
    }

    // Check for grenade in can trap
    if (SC_StringSame(nodename, "granat_v_plechovce2#3")) {
        SC_P_Speech2(pc, 925, &speechtime);
        speechtime += 0.1f;
        return;
    }
}

// ============================================================================
// ENTRY POINT AND CALLBACKS
// ============================================================================

/*
 * ScriptMain - Script entry point
 * Entry point at IP 9054
 *
 * Parameters:
 *   eventtype (local_5) - Type of script event
 *   phase (local_21) - Current phase/message
 *   param2 - Additional parameter
 *
 * Event types:
 *   0 = Level initialization
 *   1 = Radio communication event
 *   2 = Save point / checkpoint
 *   3 = Object interaction
 *   4 = Trigger event
 *   7, 8, 11 = Various mission triggers
 *   15 = Player position update
 */
void ScriptMain(int eventtype, int phase, int param2) {
    // Local buffers for structure initialization
    // s_SC_initside: 8 bytes (MaxHideOutsStatus, MaxGroups)
    // s_SC_initgroup: 20 bytes (SideId, GroupId, MaxPlayers, NoHoldFireDistance, follow_point_max_distance)
    int initdata[8];      // 32 bytes - enough for s_SC_initgroup (20B)
    int savedata[4];      // 16 bytes - enough for s_SC_MissionSave (12B)
    c_Vector3 pos;
    c_Vector3 playerpos;
    float speechtime;
    dword pc;
    dword member;

    speechtime = 0.0f;

    // Event type 3, 7, 11, 8, 4: Check conditions
    if (eventtype == 3 || eventtype == 7 || eventtype == 11 ||
        eventtype == 8 || eventtype == 4) {
        // Handle special events
    }

    // Event type 0: Level initialization
    if (eventtype == 0) {
        if (phase == 0) {
            // Full level initialization
            SC_sgi(SGI_CURRENTMISSION, 9);  // Set mission number

            SC_DeathCamera_Enable(0);
            SC_RadioSetDist(10.0f);

            // Initialize US side (side 0)
            // s_SC_initside layout: { MaxHideOutsStatus, MaxGroups } = 8 bytes
            SC_ZeroMem(initdata, 8);
            initdata[0] = 32;  // MaxHideOutsStatus (offset 0)
            initdata[1] = 8;   // MaxGroups (offset 4)
            SC_InitSide(0, initdata);

            // Initialize VC side (side 1)
            // s_SC_initside layout: { MaxHideOutsStatus, MaxGroups } = 8 bytes
            SC_ZeroMem(initdata, 8);
            initdata[0] = 64;  // MaxHideOutsStatus (offset 0)
            initdata[1] = 16;  // MaxGroups (offset 4)
            SC_InitSide(1, initdata);

            // Initialize group 0 for side 0 (US)
            // s_SC_initgroup layout (20 bytes):
            //   [0] SideId, [1] GroupId, [2] MaxPlayers,
            //   [3] NoHoldFireDistance (float), [4] follow_point_max_distance (float)
            SC_ZeroMem(initdata, 20);
            initdata[0] = 0;   // SideId = US (offset 0)
            initdata[1] = 0;   // GroupId (offset 4)
            initdata[2] = 4;   // MaxPlayers (offset 8)
            // initdata[3] = 0.0f; // NoHoldFireDistance (offset 12) - left as 0
            *((float*)&initdata[4]) = 30.0f;  // follow_point_max_distance (offset 16)
            SC_InitSideGroup(initdata);

            // Initialize VC groups 0-3
            // All use default NoHoldFireDistance=0.0 and follow_point_max_distance=0.0
            SC_ZeroMem(initdata, 20);
            initdata[0] = 1;   // SideId = VC (SC_P_SIDE_VC)
            initdata[1] = 0;   // GroupId
            initdata[2] = 9;   // MaxPlayers
            SC_InitSideGroup(initdata);

            SC_ZeroMem(initdata, 20);
            initdata[0] = 1;   // SideId = VC
            initdata[1] = 1;   // GroupId
            initdata[2] = 16;  // MaxPlayers
            SC_InitSideGroup(initdata);

            SC_ZeroMem(initdata, 20);
            initdata[0] = 1;   // SideId = VC
            initdata[1] = 2;   // GroupId
            initdata[2] = 16;  // MaxPlayers
            SC_InitSideGroup(initdata);

            SC_ZeroMem(initdata, 20);
            initdata[0] = 1;   // SideId = VC
            initdata[1] = 3;   // GroupId
            initdata[2] = 9;   // MaxPlayers
            SC_InitSideGroup(initdata);

            // Configure AI behavior
            SC_Ai_SetShootOnHeardEnemyColTest(1);
            SC_Ai_SetGroupEnemyUpdate(1, 0, 0);
            SC_Ai_SetGroupEnemyUpdate(1, 1, 0);
            SC_Ai_SetGroupEnemyUpdate(1, 2, 0);
            SC_Ai_SetGroupEnemyUpdate(1, 3, 0);

            // Set initial level phase
            gphase = 1;
            SC_sgi(SGI_LEVELPHASE, 1);
            SC_Log(3, "Levelphase changed to %d", 1);
            SC_Osi("Levelphase changed to %d", 1);

            // Setup command menu
            SC_SetCommandMenu(2009);
        }

        if (phase == 1) {
            // Phase 1 - Start mission speech
            speechtime = 1.0f;
            SC_AGS_Set(0);
            pc = SC_PC_Get();
            SC_P_SpeechMes2(pc, 900, &speechtime, 1);
            speechtime += 0.1f;

            // Advance to phase 2
            gphase = 2;
            SC_sgi(SGI_LEVELPHASE, 2);
            SC_Log(3, "Levelphase changed to %d", 2);
            SC_Osi("Levelphase changed to %d", 2);
        }

        if (phase == 2) {
            // Phase 2 - Get player position
            SC_PC_GetPos(&playerpos);
        }
    }

    // Event type 1: Radio communication
    if (eventtype == 1) {
        pc = SC_PC_Get();
        speechtime = SC_P_GetWillTalk(pc);

        SC_PC_EnableMovement(0);
        SC_PC_EnableRadioBreak(1);

        if (phase == 1) {
            // Radio conversation sequence 1
            SC_RadioBatch_Begin();
            SC_P_Speech2(pc, 916, &speechtime);
            speechtime += 0.4f;
            SC_SpeechRadio2(917, &speechtime);
            speechtime += 0.4f;
            SC_P_Speech2(pc, 918, &speechtime);
            speechtime += 0.4f;
            SC_SpeechRadio2(919, &speechtime);
            speechtime += 0.4f;
            SC_P_SpeechMes2(pc, 920, &speechtime, 2);
            speechtime += 0.1f;
            SC_RadioBatch_End();
        }

        if (phase == 2) {
            // Radio conversation sequence 2
            SC_RadioBatch_Begin();
            SC_P_Speech2(pc, 933, &speechtime);
            speechtime += 0.4f;
            SC_SpeechRadio2(934, &speechtime);
            speechtime += 0.4f;
            SC_P_Speech2(pc, 935, &speechtime);
            speechtime += 0.4f;
            SC_SpeechRadio2(936, &speechtime);
            speechtime += 0.4f;
            SC_P_SpeechMes2(pc, 937, &speechtime, 3);
            speechtime += 0.1f;
            SC_RadioBatch_End();
        }
    }

    // Event type 2: Save points and checkpoints
    if (eventtype == 2) {
        if (phase == 1) {
            // Save point 1
            // s_SC_MissionSave: { savename_id, description_id, disable_info } = 12 bytes
            SC_ZeroMem(savedata, 12);
            savedata[0] = 9110;  // savename_id (text ID for save name)
            savedata[1] = 9111;  // description_id (text ID for description)
            savedata[2] = 0;     // disable_info (FALSE = show screenshot)
            SC_MissionSave(savedata);
            SC_Log(3, "Saving game id %d", 9110);
            SC_Osi("Saving game id %d", 9110);
        }

        if (phase == 2) {
            // Save point 2
            SC_PC_EnableMovement(1);
            SC_ZeroMem(savedata, 12);
            savedata[0] = 9112;  // savename_id
            savedata[1] = 9113;  // description_id
            savedata[2] = 0;     // disable_info
            SC_MissionSave(savedata);
            SC_Log(3, "Saving game id %d", 9112);
            SC_Osi("Saving game id %d", 9112);
        }

        if (phase == 3) {
            // Save point 3
            SC_PC_EnableMovement(1);
            SC_ZeroMem(savedata, 12);
            savedata[0] = 9114;  // savename_id
            savedata[1] = 9115;  // description_id
            savedata[2] = 0;     // disable_info
            SC_MissionSave(savedata);
            SC_Log(3, "Saving game id %d", 9114);
            SC_Osi("Saving game id %d", 9114);
        }

        if (phase == 11) {
            // Enable radio
            SC_Radio_Enable(1);
        }

        if (phase == 12) {
            // Play sound at VC position
            member = SC_P_GetBySideGroupMember(1, 0, 0);
            SC_P_GetPos(member, &pos);
            SC_SND_PlaySound3D(2055, &pos);
        }

        if (phase == 13) {
            // Teleport VC units
            member = SC_P_GetBySideGroupMember(1, 0, 0);
            SC_P_GetPos(member, &pos);
            SC_SND_PlaySound3D(2060, &pos);

            member = SC_P_GetBySideGroupMember(1, 0, 1);
            SC_P_GetPos(member, &pos);
            SC_SND_PlaySound3D(2070, &pos);

            SC_GetWp("WayPoint53", &pos);
            member = SC_P_GetBySideGroupMember(1, 0, 0);
            SC_P_SetPos(member, &pos);

            SC_GetWp("WayPoint#9", &pos);
            member = SC_P_GetBySideGroupMember(1, 0, 1);
            SC_P_SetPos(member, &pos);
        }

        if (phase == 14) {
            // Teleport to waypoint 57
            SC_GetWp("WayPoint57", &pos);
            member = SC_P_GetBySideGroupMember(1, 0, 0);
            SC_P_SetPos(member, &pos);
        }

        if (phase == 15) {
            // Enable radio 2
            SC_Radio_Enable(2);
        }

        if (phase == 100) {
            // Mission trigger - call InitLevel
            InitLevel();
        }
    }

    // Event type 15: Position update
    if (eventtype == 15) {
        // Handle position-based events
        if (param2 >= 20) {
            param2 = 0;
        }
    }
}
