// Structured decompilation of decompilation/TUNNELS01/SCRIPTS/LEVEL.SCR
// Functions: 28

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword gVar;
BOOL gVar1;
BOOL gVar2;
dword gVar3;
dword gVar20;
dword gVar19;
dword gVar17;
dword gVar4;
BOOL gVar5;
dword gVar6;
dword gVar7;
dword gVar8;
int gVar9;
dword gVar10;
dword gVar11;
int gVar12;
dword gVar13;
dword gVar14;
int gVar15;
dword gVar16;
dword gData;
dword gphase;
dword gVar18;

int _init(s_SC_L_info *info) {
    int side;
    int side2;
    int side3;
    int sideB;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp14;
    int tmp15;
    int tmp16;
    int tmp17;
    int tmp18;
    int tmp19;
    int tmp2;
    int tmp20;
    int tmp21;
    int tmp22;
    int tmp23;
    int tmp24;
    int tmp25;
    int tmp26;
    int tmp27;
    int tmp28;
    int tmp29;
    int tmp3;
    int tmp30;
    int tmp31;
    int tmp32;
    int tmp33;
    int tmp34;
    int tmp35;
    int tmp36;
    int tmp37;
    int tmp38;
    int tmp39;
    int tmp4;
    int tmp40;
    int tmp41;
    int tmp42;
    int tmp43;
    int tmp44;
    int tmp45;
    int tmp46;
    int tmp47;
    int tmp48;
    int tmp49;
    int tmp5;
    int tmp50;
    int tmp51;
    int tmp52;
    int tmp53;
    int tmp54;
    int tmp55;
    int tmp56;
    int tmp57;
    int tmp58;
    int tmp59;
    int tmp6;
    int tmp60;
    int tmp61;
    int tmp62;
    int tmp63;
    int tmp64;
    int tmp65;
    int tmp7;
    int tmp8;
    int tmp9;

    return FALSE;
}

float func_0291(float param_0) {
    float result = frnd(param_0);
    if (result < 0.0f) {
        result = -result;
    }
    return result;
}

void func_0354(int message_type, int param_1, int player_id) {
    if (!player_id) {
        SC_Log(3, "Message %d %d to unexisted player!", message_type, message_type);
    } else {
        SC_P_ScriptMessage(player_id, message_type, param_1);
    }
}

int func_0371(int group_id, int member_id) {
    int player = SC_P_GetBySideGroupMember(1, group_id, member_id);
    int enemies = SC_P_Ai_GetSureEnemies(player);
    if (enemies) {
        return 1;
    }

    player = SC_P_GetBySideGroupMember(1, group_id, member_id);
    float danger = SC_P_Ai_GetDanger(player);
    if (danger > 0.5f) {
        return 1;
    }

    return 0;
}

void func_0883(void) {
    s_SC_P_Create weapons;
    int player = SC_PC_Get();
    SC_P_GetWeapons(player, &weapons);

    // Store weapon slots 1-10 in global variables 101-110
    // If weapon exists, store its ID, otherwise store 255 (empty)
    if (weapons.weapon[0]) {
        SC_sgi(101, weapons.weapon[0]);
    } else {
        SC_sgi(101, 255);
    }

    if (weapons.weapon[1]) {
        SC_sgi(102, weapons.weapon[1]);
    } else {
        SC_sgi(102, 255);
    }

    if (weapons.weapon[2]) {
        SC_sgi(103, weapons.weapon[2]);
    } else {
        SC_sgi(103, 255);
    }

    if (weapons.weapon[3]) {
        SC_sgi(104, weapons.weapon[3]);
    } else {
        SC_sgi(104, 255);
    }

    if (weapons.weapon[4]) {
        SC_sgi(105, weapons.weapon[4]);
    } else {
        SC_sgi(105, 255);
    }

    if (weapons.weapon[5]) {
        SC_sgi(106, weapons.weapon[5]);
    } else {
        SC_sgi(106, 255);
    }

    if (weapons.weapon[6]) {
        SC_sgi(107, weapons.weapon[6]);
    } else {
        SC_sgi(107, 255);
    }

    if (weapons.weapon[7]) {
        SC_sgi(108, weapons.weapon[7]);
    } else {
        SC_sgi(108, 255);
    }

    if (weapons.weapon[8]) {
        SC_sgi(109, weapons.weapon[8]);
    } else {
        SC_sgi(109, 255);
    }

    if (weapons.weapon[9]) {
        SC_sgi(110, weapons.weapon[9]);
    } else {
        SC_sgi(110, 255);
    }
}

void func_1054(void) {
    int player = SC_PC_Get();
    SC_P_WriteHealthToGlobalVar(player, 95);
}

void func_1111(void) {
    int player = SC_PC_Get();
    SC_P_WriteAmmoToGlobalVar(player, 60, 89);

    player = SC_PC_Get();
    int ammo_weap2 = SC_P_GetAmmoInWeap(player, 2);
    SC_sgi(90, ammo_weap2);

    player = SC_PC_Get();
    int ammo_weap1 = SC_P_GetAmmoInWeap(player, 1);
    SC_sgi(91, ammo_weap1);
}

void func_1146(void) {
    s_SC_P_intel intel;
    SC_PC_GetIntel(&intel);

    // Loop through 10 intel items and store in global variables 50-59
    for (int i = 0; i < 10; i++) {
        SC_sgi(50 + i, intel.intel[i]);
    }
}

void func_1223(void) {
    func_1146();
    func_0883();
    func_1111();
    func_1054();
    SC_Osi("MISSION COMPLETE");
    SC_MissionDone();
}

void func_3368(char *node_name, c_Vector3 *out_pos) {
    void *node = SC_NOD_Get(0, node_name);
    if (node != 0) {
        SC_NOD_GetWorldPos(node, out_pos);
    }
}

int func_4180(c_Vector3 *target_pos, float distance, int player_id) {
    c_Vector3 player_pos;
    SC_P_GetPos(player_id, &player_pos);
    return SC_IsNear3D(&player_pos, target_pos, distance);
}

int func_4376(c_Vector3 *pos, int side, int player_id) {
    s_SC_P_getinfo player_info;
    s_sphere sphere;
    c_Vector3 player_pos;
    int players[32];
    int player_count = 32;
    int closest_player = 0;
    float min_distance = 0.0f;

    SC_P_GetInfo(player_id, &player_info);
    SC_P_GetPos(player_id, &sphere.pos);
    sphere.radius = 1000.0f;

    SC_GetPls(&sphere, &player_count, players);

    for (int i = 0; i < player_count; i++) {
        int pl = players[i];
        SC_P_GetInfo(pl, &player_info);

        if (player_info.side == side || player_info.side == 100) {
            continue;
        }

        if (!SC_P_IsReady(pl)) {
            continue;
        }

        SC_P_GetPos(pl, &player_pos);
        float dist = SC_2VectorsDist(&player_pos, pos);

        if (dist < min_distance || i == 0) {
            min_distance = dist;
            closest_player = pl;
        }
    }

    return closest_player;
}

float func_4575(c_Vector3 *pos, int player_id) {
    c_Vector3 player_pos;
    SC_P_GetPos(player_id, &player_pos);
    return SC_2VectorsDist(pos, &player_pos);
}

void func_4948(int param_0) {
    // This function appears to initialize a local variable to 0
    // but doesn't return anything or have other side effects
    int local = 0;
}

void func_5197(void) {
    SC_sgi(SGI_MISSIONDEATHCOUNT, 0);
    SC_sgi(SGI_MISSIONALARM, 0);
    SC_sgi(SGI_LEVELPHASE, 0);
    SC_sgi(SGI_ALLYDEATHCOUNT, 0);
    SC_sgi(SGI_TEAMDEATHCOUNT, 0);
    SC_sgi(SGI_TEAMWIA, 0);
    SC_sgi(SGI_INTELCOUNT, 0);
    SC_sgi(SGI_CHOPPER, 0);
    SC_sgi(SGI_GAMETYPE, 0);
    int difficulty = SC_ggi(SGI_DIFFICULTY);
    SC_Log(3, "Level difficulty is %d", difficulty);
}

int func_6196(int param_0) {
    // Simple switch/case that always returns 1
    // Original has unreachable code paths
    if (param_0 == 0 || param_0 == 1) {
        return 1;
    }
    return 1;
}

void func_6259(void) {
    int player = SC_P_GetBySideGroupMember(0, 0, 1);
    int peace_mode = SC_P_Ai_GetPeaceMode(player);
    if (peace_mode == 2) {
        SC_Ai_SetPeaceMode(0, 0, 0);
        SC_Ai_PointStopDanger(0, 0);
    }
}

int func_6804(void) {
    for (int i = 1; i < 6; i++) {
        int player = SC_P_GetBySideGroupMember(0, 0, i);
        int is_ready = SC_P_IsReady(player);
        if (is_ready) {
            player = SC_P_GetBySideGroupMember(0, 0, i);
            int peace_mode = SC_P_Ai_GetPeaceMode(player);
            if (peace_mode != 0) {
                return peace_mode;
            }
        }
    }
    return 0;
}

void func_6873(void) {
    // Initialize array of 14 active place structures
    // Each structure has: name (24 bytes), position (12 bytes), radius (4), state (4), distance (4)
    char name_buffer[16];

    for (int i = 0; i < 14; i++) {
        // Set initial state to 0
        gData[i].state = 0;

        // Generate waypoint name "ACTIVEPLACE#%d"
        sprintf(name_buffer, "ACTIVEPLACE#%d", i);

        // Get waypoint position
        func_3368(name_buffer, &gData[i].position);

        // Initialize radius, state, and distance
        gData[i].radius = 2.0f;
        gData[i].state = 0;
        gData[i].distance = -1.0f;
    }

    // Set special values for entries 0 and 1
    gData[0].distance = 30.0f;
    gData[1].distance = 15.0f;
    gData[7].state = -100;

    // Get specific waypoints
    c_Vector3 wp_pos;
    SC_GetWp("WayPoint113", &wp_pos);
    SC_GetWp("WayPoint#33", &wp_pos);
}

void func_6984(int index) {
    // Manages active place state based on index
    // Sets state values in gData array
    if (index < 0 || index >= 14) {
        return;
    }

    switch (gData[index].state) {
        case 0:
        case 1:
            gData[index].state = 0;
            gData[index].field_24 = 1;
            break;

        case 2:
        case 3:
        case 4:
        case 5:
        case 6:
            // Other state transitions
            break;

        default:
            break;
    }
}

void func_7043(int index) {
    // Complex speech and AI management function
    // This function handles various phases of NPC interactions and commands
    // Based on assembly analysis: manages gData[index] state and orchestrates
    // speech sequences, AI commands, and mission objectives

    float will_talk_timer;
    c_Vector3 pos;
    c_Vector3 waypoint_pos;
    int player;
    int npc;
    int sound_id;

    // Get player and will talk timer
    player = SC_PC_Get();
    will_talk_timer = SC_P_GetWillTalk(player);
    will_talk_timer += 0.2f;

    // Check current state from gData[index]
    if (gData[index].field_24 == 0) {
        // State 0: Initial speech selection
        if (gData[index].field_24 == 0) {
            // Play speech 903 or 904 based on condition
            if (gData[index].field_24 == 0) {
                player = SC_PC_Get();
                SC_P_Speech2(player, 903, &will_talk_timer);
                will_talk_timer += 0.1f;
            } else {
                player = SC_PC_Get();
                SC_P_Speech2(player, 904, &will_talk_timer);
                will_talk_timer += 0.1f;
            }

            // Set state to -100
            gData[index].field_24 = -100;
            gData[index].state = gData[index].state;
        }
    }
    else if (gData[index].field_24 == 1) {
        // State 1: Random speech and distance check
        if (gData[index].field_24 == 0) {
            // Random speech selection
            if (rand() % 2 == 0) {
                player = SC_PC_Get();
                SC_P_Speech2(player, 905, &will_talk_timer);
                will_talk_timer += 0.1f;
            } else {
                player = SC_PC_Get();
                SC_P_Speech2(player, 911, &will_talk_timer);
                will_talk_timer += 0.1f;
            }
        } else {
            // Distance check and speech
            float dist1 = func_4575(SC_PC_Get(), &gData[index]);
            float dist2 = func_4575(SC_PC_Get(), &gData[7]);  // gData + 196 bytes = index 7

            if (dist1 <= dist2) {
                player = SC_PC_Get();
                int speech_id = 908 + (rand() % 3);
                SC_P_Speech2(player, speech_id, &will_talk_timer);
                will_talk_timer += 0.1f;
            }
        }

        gData[index].field_24 = -100;
        gData[index].state = gData[index].state;
    }
    else if (gData[index].field_24 == 2) {
        // State 2: Speech sequence
        player = SC_PC_Get();
        SC_P_Speech2(player, 912, &will_talk_timer);  // Placeholder speech ID
        will_talk_timer += 0.1f;
        gData[index].field_24 = -100;
    }
    else if (gData[index].field_24 == 3) {
        // State 3: Speech with message
        player = SC_PC_Get();
        SC_P_SpeechMes2(player, 913, &will_talk_timer, 10);  // Placeholder
        will_talk_timer += 0.1f;
        gData[index].field_24 = -100;
    }
    else if (gData[index].field_24 == 4) {
        // State 4: NPC interaction with sound
        npc = SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(npc, &pos);
        SC_SND_PlaySound3D(100, &pos);  // Placeholder sound
        will_talk_timer += 0.1f;

        player = SC_PC_Get();
        SC_P_SpeechMes2(player, 914, &will_talk_timer, 11);
        will_talk_timer += 0.1f;
        will_talk_timer = 0.5f;
    }
    else if (gData[index].field_24 == 5) {
        // State 5: Multiple NPC speech sequence
        npc = SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Speech2(npc, 915, &will_talk_timer);
        will_talk_timer += 0.1f;

        npc = SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_Speech2(npc, 916, &will_talk_timer);
        will_talk_timer += 0.1f;

        npc = SC_P_GetBySideGroupMember(1, 0, 2);
        SC_P_SpeechMes2(npc, 917, &will_talk_timer, 12);
        will_talk_timer += 0.1f;

        gData[index].field_24 = -100;
    }
    else if (gData[index].field_24 == 6) {
        // State 6: More speech
        player = SC_PC_Get();
        SC_P_Speech2(player, 918, &will_talk_timer);
        will_talk_timer += 0.1f;
        gData[index].field_24 = -100;
    }
    else if (gData[index].field_24 == 7) {
        // State 7: Another speech
        player = SC_PC_Get();
        SC_P_Speech2(player, 919, &will_talk_timer);
        will_talk_timer += 0.1f;
        gData[index].field_24 = -100;
    }
    else if (gData[index].field_24 == 8) {
        // State 8: NPC speech with message
        npc = SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SpeechMes2(npc, 920, &will_talk_timer, 13);
        will_talk_timer += 0.1f;
        gData[index].field_24 = -100;
        gData[index].field_24 = -100;
    }
    else if (gData[index].field_24 == 9) {
        // State 9: AI mode and waypoint
        npc = SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(npc, 1);

        SC_GetWp(0, &waypoint_pos);
        npc = SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_Go(npc, &waypoint_pos);

        player = SC_PC_Get();
        SC_P_SpeechMes2(player, 932, &will_talk_timer, 15);
        will_talk_timer += 0.1f;
        gData[index].field_24 = -100;
    }
    else if (gData[index].field_24 == 10) {
        // State 10: Sound effects
        npc = SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(npc, &pos);
        SC_SND_PlaySound3D(101, &pos);

        npc = SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_GetPos(npc, &pos);
        SC_SND_PlaySound3D(102, &pos);

        player = SC_PC_Get();
        SC_P_Speech2(player, 933, &will_talk_timer);
        will_talk_timer += 0.1f;
        gData[index].state = 1;
        gData[index].field_24 = -100;
        SC_AGS_Set(0);
        gData[index].field_24 = -100;
        func_1223();
        gData[index].field_24 = -100;
    }
}

void func_7697(float delta_time, c_Vector3 *player_pos) {
    // Update timers and check proximity for all active places
    int i;

    // First loop: Update timers and check for state transitions
    for (i = 0; i < 14; i++) {
        if (gData[i].state > 0.0f) {
            // Decrement timer by delta_time
            gData[i].state -= delta_time;

            // If timer expired, trigger state change
            if (gData[i].state <= 0.0f) {
                func_6984(i);
            }
        }
    }

    // Second loop: Check proximity and trigger interactions
    for (i = 0; i < 14; i++) {
        if (gData[i].field_24 != -100) {
            // Check if player is near this location
            if (SC_IsNear3D(player_pos, &gData[i].pos, gData[i].radius)) {
                func_7043(i);
                return;
            }
        }
    }
}

int func_7807(float param_0) {
    int local_5;  // Auto-generated

    c_Vector3 data_1763;
    c_Vector3 local_2;
    c_Vector3 local_6;
    c_Vector3 local_9;
    c_Vector3 tmp114;
    c_Vector3 tmp2;
    c_Vector3 tmp21;
    int data_;
    int data_1757;
    int data_1758;
    int local_;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp100;
    int tmp101;
    int tmp102;
    int tmp103;
    int tmp104;
    int tmp105;
    int tmp106;
    int tmp107;
    int tmp108;
    int tmp109;
    int tmp11;
    int tmp110;
    int tmp111;
    int tmp112;
    int tmp113;
    int tmp115;
    int tmp116;
    int tmp117;
    int tmp118;
    int tmp119;
    int tmp12;
    int tmp120;
    int tmp121;
    int tmp122;
    int tmp123;
    int tmp124;
    int tmp125;
    int tmp126;
    int tmp127;
    int tmp128;
    int tmp129;
    int tmp13;
    int tmp130;
    int tmp131;
    int tmp132;
    int tmp133;
    int tmp134;
    int tmp135;
    int tmp136;
    int tmp14;
    int tmp15;
    int tmp16;
    int tmp17;
    int tmp18;
    int tmp19;
    int tmp20;
    int tmp22;
    int tmp23;
    int tmp24;
    int tmp25;
    int tmp26;
    int tmp27;
    int tmp28;
    int tmp29;
    int tmp3;
    int tmp30;
    int tmp31;
    int tmp32;
    int tmp33;
    int tmp34;
    int tmp35;
    int tmp36;
    int tmp37;
    int tmp38;
    int tmp39;
    int tmp4;
    int tmp40;
    int tmp41;
    int tmp42;
    int tmp43;
    int tmp44;
    int tmp45;
    int tmp46;
    int tmp47;
    int tmp48;
    int tmp49;
    int tmp5;
    int tmp50;
    int tmp51;
    int tmp52;
    int tmp53;
    int tmp54;
    int tmp55;
    int tmp56;
    int tmp57;
    int tmp58;
    int tmp59;
    int tmp6;
    int tmp60;
    int tmp61;
    int tmp62;
    int tmp63;
    int tmp64;
    int tmp65;
    int tmp66;
    int tmp67;
    int tmp68;
    int tmp69;
    int tmp7;
    int tmp70;
    int tmp71;
    int tmp72;
    int tmp73;
    int tmp74;
    int tmp75;
    int tmp76;
    int tmp77;
    int tmp78;
    int tmp79;
    int tmp8;
    int tmp80;
    int tmp81;
    int tmp82;
    int tmp83;
    int tmp84;
    int tmp85;
    int tmp86;
    int tmp87;
    int tmp88;
    int tmp89;
    int tmp9;
    int tmp90;
    int tmp91;
    int tmp92;
    int tmp93;
    int tmp94;
    int tmp95;
    int tmp96;
    int tmp97;
    int tmp98;
    int tmp99;

    goto block_900; // @7817
    SC_P_GetBySideGroupMember(tmp5, tmp6, tmp7);
    SC_P_IsReady(local_);
    if (!local_6) {
        func_0371(tmp3, tmp4);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Speech2(local_6, 926, &tmp2);
        tmp2 = tmp1;
        data_ = 1;
    }
    goto block_907; // @7868
    SC_P_GetBySideGroupMember(tmp9, tmp10, tmp11);
    SC_P_IsReady(local_);
    if (!local_6) {
        SC_P_GetBySideGroupMember(tmp12, tmp13, tmp14);
        func_4180(&tmp15, tmp16);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_BATTLE);
        data_ = 2;
        SC_P_GetBySideGroupMember(tmp18, tmp19, tmp20);
        SC_P_Ai_GetShooting(local_, &tmp21);
        SC_PC_Get();
        tmp2 = SC_P_GetWillTalk(local_);
        SC_PC_Get();
        SC_P_Speech2(local_6, 929, &tmp2);
        tmp2 = tmp17;
        data_ = 3;
        SC_P_GetBySideGroupMember(tmp28, tmp29, tmp30);
        SC_P_IsReady(local_);
        SC_PC_Get();
        tmp2 = SC_P_GetWillTalk(local_);
        SC_PC_Get();
        SC_P_Speech2(local_6, 927, &tmp2);
        tmp2 = tmp22;
        data_ = 100;
        tmp24 = tmp23;
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_Go(local_6, &vcrunpoint2);
        SC_PC_Get();
        SC_P_GetWillTalk(local_);
        tmp2 = tmp26;
        SC_PC_Get();
        SC_P_Speech2(local_6, 930, &tmp2);
        tmp2 = tmp27;
        data_ = 4;
        SC_P_GetBySideGroupMember(tmp31, tmp32, tmp33);
        func_4180(&tmp15, tmp34);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_BATTLE);
        data_ = 5;
        SC_P_GetBySideGroupMember(tmp38, tmp39, tmp40);
        SC_P_IsReady(local_6);
        SC_P_GetBySideGroupMember(tmp41, tmp42, tmp43);
        SC_P_IsReady(local_6);
        tmp35 = 1;
        SC_PC_Get();
        SC_P_GetWillTalk(local_6);
        tmp2 = tmp36;
        SC_PC_Get();
        SC_P_Speech2(local_5, 928, &tmp2);
        tmp2 = tmp37;
        SC_P_GetBySideGroupMember(tmp47, tmp48, tmp49);
        SC_P_IsReady(local_6);
        SC_P_GetBySideGroupMember(tmp50, tmp51, tmp52);
        SC_P_IsReady(local_6);
        SC_P_GetBySideGroupMember(tmp53, tmp54, tmp55);
        SC_P_IsReady(local_6);
        tmp44 = 1;
        SC_PC_Get();
        SC_P_GetWillTalk(local_6);
        tmp2 = tmp45;
        SC_PC_Get();
        SC_P_Speech2(local_5, 931, &tmp2);
        tmp2 = tmp46;
        func_0371(tmp60, tmp61);
        SC_P_GetBySideGroupMember(1, 1, 0);
        rand();
        SC_P_Speech2(local_5, tmp58, &tmp2);
        tmp2 = tmp59;
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        data_1757 = 100;
        func_0371(tmp66, tmp67);
        SC_P_GetBySideGroupMember(1, 1, 1);
        rand();
        SC_P_Speech2(local_5, tmp64, &tmp2);
        tmp2 = tmp65;
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_SetMode(local_5, SGI_INTELCOUNT);
        data_1757 = 100;
        func_0371(tmp72, tmp73);
        SC_P_GetBySideGroupMember(1, 1, 2);
        rand();
        SC_P_Speech2(local_5, tmp70, &tmp2);
        tmp2 = tmp71;
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        data_1757 = 100;
        SC_P_GetBySideGroupMember(tmp77, tmp78, tmp79);
        SC_P_Ai_SetMode(local_6, tmp80);
        SC_P_GetBySideGroupMember(tmp81, tmp82, tmp83);
        SC_P_Ai_SetMode(local_6, tmp84);
        SC_P_GetBySideGroupMember(tmp85, tmp86, tmp87);
        SC_P_Ai_SetMode(local_6, tmp88);
        SC_P_GetBySideGroupMember(tmp89, tmp90, tmp91);
        SC_P_Ai_Stop(local_6);
        SC_P_GetBySideGroupMember(tmp92, tmp93, tmp94);
        SC_P_Ai_Stop(local_6);
        SC_P_GetBySideGroupMember(tmp95, tmp96, tmp97);
        SC_P_Ai_Stop(local_6);
        frnd(20.0f);
        tmp75 = tmp74;
        rand();
        data_1758 = tmp76;
        SC_P_GetBySideGroupMember(tmp99, tmp100, data_1758);
        SC_P_GetPos(local_6, &local_2);
        SC_P_GetBySideGroupMember(tmp101, tmp102, tmp103);
        SC_P_Ai_Go(local_6, &local_2);
        SC_P_GetBySideGroupMember(tmp104, tmp105, tmp106);
        SC_P_GetPos(local_6, &data_1763);
        data_1757 = 2;
        SC_P_GetBySideGroupMember(tmp111, tmp112, tmp113);
        SC_P_GetBySideGroupMember(tmp115, tmp116, data_1758);
        SC_P_GetDistance(data_1758, local_9);
        SC_P_GetBySideGroupMember(1, 1, 2);
        rand();
        SC_P_Speech2(local_, tmp109, &tmp2);
        tmp2 = tmp110;
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_Go(local_, &data_1763);
        data_1758 = 2;
        SC_P_GetBySideGroupMember(tmp118, tmp119, tmp120);
        func_4180(&data_1763, tmp121);
        rand();
        data_1758 = tmp117;
        SC_P_GetBySideGroupMember(1, 1, data_1758);
        SC_P_GetPos(local_, &local_2);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_Go(local_, &local_2);
        tmp75 = tmp122;
        frnd(20.0f);
        tmp75 = tmp124;
        tmp2 = 0;
        rand();
        SC_P_GetBySideGroupMember(1, 1, tmp125);
        rand();
        SC_P_Speech2(local_6, tmp127, &tmp2);
        tmp2 = tmp128;
        tmp130 = tmp129;
        frnd(5.0f);
        tmp130 = tmp132;
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetPos(local_6, &local_2);
        SC_SND_PlaySound3D(10419, &local_2);
        tmp134 = tmp133;
        frnd(5.0f);
        tmp134 = tmp136;
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_GetPos(local_6, &local_2);
        SC_SND_PlaySound3D(10419, &local_2);
        return tmp121;
    } else {
        SC_PC_Get();
        tmp2 = SC_P_GetWillTalk(local_);
        SC_PC_Get();
        SC_P_Speech2(local_6, 927, &tmp2);
        tmp2 = tmp8;
        data_ = 100;
    }
    return;
}

void func_8919(void) {
    SC_SetObjectScript("grenadebedna", "levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\openablecrate.c");
    SC_SetObjectScript("n_poklop_01", "levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\poklop.c");
    SC_SetObjectScript("d_past_04_01", "levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\past.c");
}

void func_8932(void) {
}

void func_8933(void) {
}

int func_8934(s_SC_L_info *info) {
    int player = SC_PC_Get();
    float will_talk = SC_P_GetWillTalk(player);

    if (info->field_8) {
        char *obj_name = SC_NOD_GetName(info->field_8);
        int is_same = SC_StringSame(obj_name, "grenadebedna");

        if (is_same) {
            player = SC_PC_Get();
            SC_P_Speech2(player, 923, &will_talk);
            will_talk += 0.1f;
            return 1;
        }
    }
    return 0;
}

int ScriptMain(s_SC_L_info *info) {
    c_Vector3 local_;
    c_Vector3 local_9;
    s_SC_initside initside;
    static int save[32];
    static int phase = 0;

    // Set initial time multiplier
    info->field_20 = 0.2f;

    // Event dispatch based on info->field_0 (event type)
    int event = info->field_0;

    // Handle different event types
    switch (event) {
        case 7:  // Mission start / level load
            func_8919();
            return FALSE;

        case 11:  // Unknown event
            func_8933();
            return FALSE;

        case 8:  // Unknown event
            func_8932();
            return FALSE;

        case 4:  // Object interaction
            if (info->field_4 == 51) {
                return func_8934(info);
            }
            return FALSE;

        case 0:  // Main game loop / initialization
            if (phase == 0) {
                // Initial setup
                SC_sgi(200, 9);
                func_5197();
                SC_DeathCamera_Enable(0);
                SC_RadioSetDist(500.0f);

                // Initialize sides and groups
                SC_ZeroMem(&initside, sizeof(initside));
                initside.side = 0;
                initside.max_players = 8;
                initside.flags = 32;
                SC_InitSide(0, &initside);

                SC_ZeroMem(&initside, sizeof(initside));
                initside.side = 1;
                initside.max_players = 16;
                initside.flags = 64;
                SC_InitSide(1, &initside);

                // Initialize player groups
                SC_ZeroMem(&initside, sizeof(initside));
                initside.side = 0;
                initside.group = 0;
                initside.max_players = 4;
                initside.distance = 30.0f;
                SC_InitSideGroup(&initside);

                SC_ZeroMem(&initside, sizeof(initside));
                initside.side = 1;
                initside.group = 0;
                initside.max_players = 9;
                SC_InitSideGroup(&initside);

                SC_ZeroMem(&initside, sizeof(initside));
                initside.side = 1;
                initside.group = 1;
                initside.max_players = 16;
                SC_InitSideGroup(&initside);

                SC_ZeroMem(&initside, sizeof(initside));
                initside.side = 1;
                initside.group = 2;
                initside.max_players = 16;
                SC_InitSideGroup(&initside);

                SC_ZeroMem(&initside, sizeof(initside));
                initside.side = 1;
                initside.group = 3;
                initside.max_players = 9;
                SC_InitSideGroup(&initside);

                SC_Ai_SetShootOnHeardEnemyColTest(1);
                SC_Ai_SetGroupEnemyUpdate(0, 0, 1);
                SC_Ai_SetGroupEnemyUpdate(1, 0, 1);
                SC_Ai_SetGroupEnemyUpdate(1, 1, 1);
                SC_Ai_SetGroupEnemyUpdate(1, 2, 1);

                phase = 1;
                SC_sgi(SGI_LEVELPHASE, phase);
                SC_Log(3, "Levelphase changed to %d", phase);
                SC_Osi("Levelphase changed to %d", phase);
                SC_SetCommandMenu(1);
                info->field_20 = 0.5f;
            }
            else if (phase == 1) {
                // Phase 1: Mission intro
                local_ = 1.0f;
                SC_AGS_Set(1);

                int player = SC_PC_Get();
                SC_P_SpeechMes2(player, 907, &local_, 11);

                func_4948(0);
                func_4948(1);
                func_4948(2);
                func_6873();

                phase = 2;
                SC_sgi(SGI_LEVELPHASE, phase);
                SC_Log(3, "Levelphase changed to %d", phase);
                SC_Osi("Levelphase changed to %d", phase);
            }
            else if (phase == 2) {
                // Phase 2: Mission gameplay
                SC_PC_GetPos(&local_9);
                // ... mission logic would go here ...

                // Check mission completion
                player = SC_PC_Get();
                local_ = SC_P_GetWillTalk(player);
                SC_PC_EnableMovement(1);
                SC_PC_EnableRadioBreak(0);

                // Radio communications
                SC_RadioBatch_Begin();
                player = SC_PC_Get();
                SC_P_Speech2(player, 908, &local_);
                local_ += func_0291(0.3f);
                SC_SpeechRadio2(906, &local_);
                local_ += func_0291(0.2f);
                player = SC_PC_Get();
                SC_P_Speech2(player, 909, &local_);
                local_ += func_0291(0.3f);
                SC_SpeechRadio2(910, &local_);
                local_ += func_0291(0.2f);
                player = SC_PC_Get();
                SC_P_SpeechMes2(player, 911, &local_, 11);
                SC_RadioBatch_End();

                // Save game progress
                s_SC_MissionSave save_info;
                save_info.save_id = 9110;
                save_info.name_id = 9111;
                SC_MissionSave(&save_info);
                SC_Log(3, "Saving game id %d", 9110);
                SC_Osi("Saving game id %d", 9110);

                phase = 3;
            }
            else if (phase >= 3) {
                // Mission complete
                func_1223();
                info->field_12 = 1;
                return TRUE;
            }
            break;

        default:
            break;
    }

    return FALSE;
}

