// Structured decompilation of decompiler_source_tests/test3/LEVEL.SCR
// Functions: 10

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword gVar = 0;
dword gVar1 = 0;
int gphase = 0;
int g_dialog = 0;
dword g_will_group[4] = {0};
int g_dochange = 1;
float g_final_enter_timer = 0.0f;
c_Vector3 g_will_pos[4] = {0};
dword g_vill_visited[4] = {0};
int g_pilot_phase = 0;
float g_pilot_timer = 0.0f;
int g_pilot_vill_nr = 255;
float g_showinfo_timer = 0.0f;
int g_trashes_enabled = 0;
dword gShot_pos[3] = {0};
float gEndTimer = 0.0f;
float gPilotCommTime = 0.0f;
dword g_save[2] = {0};
dword g_music[2] = {0};
float gStartMusicTime = 0.0f;

void _init(s_SC_L_info *info) {
    int j;
    int side;
    int side2;
    int side3;
    int side4;
    int side5;
    int sideB;

    return;
}

void func_0292(void) {
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated
    int t321_ret;  // Auto-generated
    int t332_ret;  // Auto-generated
    int z;  // Auto-generated

    c_Vector3 vec;
    dword i;
    int j;
    int k;
    int ptr;
    int ptr1;

    SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0);
    SC_ZeroMem(&vec, 12);
    vec.z = -20000.0f;
    local_0 = 0;
    // Loop header - Block 2 @312
    for (i = 0; i < 16; i = i + 1) {
        t321_ret = SC_P_GetBySideGroupMember(1, 9, i);
        local_1 = SC_P_GetBySideGroupMember(1, 9, i);
        if (ptr && t332_ret = SC_P_IsReady(ptr)) {
            SC_P_SetActive(ptr, FALSE);
            SC_P_SetPos(ptr, &vec);
        }
    }
    return;
}

void func_0355(void) {
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated
    int t383_ret;  // Auto-generated
    int t426_ret;  // Auto-generated

    dword i;
    int j;
    int k;
    int local_2;
    int obj;
    int ptr;
    int ptr1;

    local_1 = 0;
    // Loop header - Block 10 @362
    for (ptr = 0; ptr < 12; ptr = ptr + 1) {
        if (ptr != 9) {
            local_0 = 0;
        } else {
            local_1 = ptr + 1;
        }
        // Loop header - Block 13 @374
        for (i = 0; i < 16; i = i + 1) {
            t383_ret = SC_P_GetBySideGroupMember(1, ptr, i);
            local_2 = SC_P_GetBySideGroupMember(1, ptr, i);
            if (obj) {
                SC_P_SetActive(obj, TRUE);
            } else {
                local_0 = i + 1;
            }
        }
    }
    local_1 = 0;
    // Loop header - Block 19 @417
    for (ptr1 = 0; ptr1 < 16; ptr1 = ptr1 + 1) {
        t426_ret = SC_P_GetBySideGroupMember(3, 0, ptr1);
        local_2 = SC_P_GetBySideGroupMember(3, 0, ptr1);
        if (obj) {
            SC_P_SetActive(obj, TRUE);
        } else {
            local_1 = ptr1 + 1;
        }
    }
    return;
}

dword func_0448(int param_0) {
    int t453_ret;  // Auto-generated

    t453_ret = SC_P_GetBySideGroupMember(2, 0, 1);
    return SC_P_GetBySideGroupMember(2, 0, 1);
}

void func_0511(int param_0, int param_1) {
    int local_6;  // Auto-generated

    c_Vector3 vec;
    dword local_3[2];
    float local_5;
    float ptr2;
    float t539_ret;
    int g_will_pos;
    int k;
    int local_0;
    int ptr;
    int tmp5;
    int tmp8;

    SC_P_GetPos(param_1, &vec);
    SC_ZeroMem(local_3, 8);
    local_6 = 0;
    // Loop header - Block 32 @527
    for (ptr = 0; ptr < 4; ptr = ptr + 1) {
        t539_ret = SC_2VectorsDist(&vec, &g_will_pos[ptr]);
        local_5 = SC_2VectorsDist(&vec, &g_will_pos[ptr]);
        if (ptr2 > tmp5) {
            local_3[0].status = tmp8;
            param_0[1] = param_0[0];
            local_3 = ptr2;
            param_0[0] = ptr;
        } else {
            if (ptr2 > local_3[0].status) {
                local_3[0].status = ptr2;
                param_0[1] = ptr;
            } else {
                local_6 = ptr + 1;
            }
        }
    }
    return;
}

void func_0612(int param_0, float param_1) {
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated
    int t625_ret;  // Auto-generated
    int t654_ret;  // Auto-generated
    float t729_ret;  // Auto-generated
    int t759_ret;  // Auto-generated
    int t767_ret;  // Auto-generated
    float t790_ret;  // Auto-generated
    int t804_ret;  // Auto-generated
    float t843_ret;  // Auto-generated
    int t870_ret;  // Auto-generated
    int t886_ret;  // Auto-generated
    int t916_ret;  // Auto-generated
    int t944_ret;  // Auto-generated
    int t960_ret;  // Auto-generated

    c_Vector3 vec;
    dword local_12;
    float local_10;
    float ptr4;
    float t947_ret;
    int data_;
    int data_257;
    int data_257_v1;
    int data_258;
    int g_will_pos;
    int i;
    int j;
    int k;
    int local_11;
    int local_13;
    int local_2;
    int local_4;
    int obj;
    int ptr;
    int ptr1;
    int ptr2;
    int ptr5;
    int tmp17;
    int tmp22;
    int tmp35;
    int tmp6;
    int tmp70;

    switch (g_pilot_phase) {
    case 0:
        t625_ret = SC_PC_GetPos(&local_4);
        // Loop header - Block 41 @633
        for (i = 0; i < 4; i = i + 1) {
            if (tmp6) {
            } else {
                if (t654_ret = SC_IsNear2D(&g_will_pos[i], &local_4, 80.0f)) {
                    g_vill_visited[i] = 1;
                } else {
                    local_0 = i + 1;
                }
            }
            local_0 = i + 1;
        }
        local_1 = 0;
        // Loop header - Block 48 @683
        for (j = 0; j < 3; j = j + 1) {
            if (tmp17) {
                local_1 = ptr1 + 1;
            } else {
                local_0 = j + 1;
            }
            local_0 = j + 1;
        }
        if (ptr2 > 1 && tmp22) {
            g_pilot_phase = 1;
            t729_ret = frnd(10.0f);
            g_pilot_timer = 10.0f + frnd(10.0f);
        }
        break;
    case 1:
        if (!g_pilot_timer <= 0.0f) break;
        g_pilot_phase = 2;
        t759_ret = SC_PC_Get();
        func_0511(SC_PC_Get(), &local_2);
        t767_ret = rand();
        g_pilot_vill_nr = tmp35;
        func_0448();
        SC_P_ScriptMessage(local_12, 0, g_pilot_vill_nr);
        t790_ret = frnd(30.0f);
        g_pilot_timer = 30.0f + frnd(30.0f);
        t804_ret = rand();
        SC_SpeechRadio2(3463 + 2 * g_pilot_vill_nr + rand() % 2, 0);
        func_0448();
        SC_HUD_RadarShowPlayer(local_12, -16711936);
        break;
    case 2:
        g_pilot_timer -= param_0;
        if (g_pilot_timer < 0.0f) {
            g_pilot_phase = 1;
            t843_ret = frnd(10.0f);
            g_pilot_timer = 10.0f + frnd(10.0f);
            g_pilot_vill_nr = 255;
            func_0448();
            SC_P_ScriptMessage(local_12, 0, g_pilot_vill_nr);
            SC_HUD_RadarShowPlayer(0, 0);
        } else {
            t870_ret = SC_PC_GetPos(&local_4);
            func_0448(SC_PC_GetPos(&local_4));
            SC_P_GetPos(local_12, &vec);
            if (!t886_ret = SC_IsNear2D(&local_4, &vec, 50.0f)) break;
            g_pilot_phase = 4;
            g_pilot_timer = 0;
            SC_SetSideAlly(1, 2, -1.0f);
            SC_sgi(SGI_LEVELPHASE, 2);
        }
        break;
    default:
        break;
        break;
    }
    if (local_11 == 4) {
        if (t916_ret = SC_ggi(SGI_LEVELPHASE)) {
        } else {
            g_pilot_timer -= param_0;
            if (g_pilot_timer <= 0.0f) {
                g_pilot_timer = 1.5f;
                func_0448();
                t944_ret = SC_PC_Get();
                t947_ret = SC_P_GetDistance(tmp70, SC_PC_Get());
                local_10 = SC_P_GetDistance(tmp70, SC_PC_Get());
                if (ptr4 > 15.0f) {
                    t960_ret = SC_PC_GetPos(&vec);
                    func_0448(SC_PC_GetPos(&vec));
                    SC_P_Ai_Go(local_12, &vec);
                } else {
                    if (ptr4 < 8.0f) {
                        func_0448();
                        SC_P_Ai_Stop(local_12);
                    }
                }
            }
        }
    }
    return;
}

void func_0985(int param_0, int param_1) {
    SC_P_Ai_SetMoveMode(param_0, SC_P_AI_MOVEMODE_RUN);
    SC_P_Ai_SetMovePos(param_0, SC_P_AI_MOVEPOS_STAND);
    return;
}

void func_0994(int param_0, int param_1) {
    int j;
    void* local_0;
    void* t1003_ret;

    g_trashes_enabled = param_1;
    t1003_ret = SC_NOD_Get(0, "maj_uh-1d_vreck");
    local_0 = SC_NOD_Get(0, "maj_uh-1d_vreck");
    if (local_0) {
        if (param_0) {
        } else {
        }
        SC_DUMMY_Set_DoNotRenHier2(local_0, 1);
    }
    return;
}

void func_1021(void) {
    int t1040_ret;  // Auto-generated

    int local_256;
    int ptr;
    s_SC_MP_EnumPlayers enum_pl;

    local_256 = 64;
    SC_sgi(SGI_DEBR_01, 0);
    SC_sgi(SGI_REWARD_PILOT, 1);
    if (t1040_ret = SC_MP_EnumPlayers(&enum_pl, &local_256, 1) && ptr > 0) {
        SC_sgi(SGI_DEBR_01, -1);
        SC_sgi(SGI_REWARD_PILOT, 0);
    }
    return;
}

int ScriptMain(s_SC_L_info *info) {
    int local_20;  // Auto-generated
    int t1544_ret;  // Auto-generated
    int t1556_ret;  // Auto-generated
    int t1618_ret;  // Auto-generated
    int t1635_ret;  // Auto-generated
    int t1646_ret;  // Auto-generated
    int t1700_ret;  // Auto-generated
    int t1785_ret;  // Auto-generated
    int t1797_ret;  // Auto-generated
    int t1808_ret;  // Auto-generated
    int t1819_ret;  // Auto-generated
    int t1856_ret;  // Auto-generated
    int t1868_ret;  // Auto-generated
    int t1894_ret;  // Auto-generated
    int t1970_ret;  // Auto-generated
    int t2061_ret;  // Auto-generated
    int t2155_ret;  // Auto-generated
    int t2171_ret;  // Auto-generated
    int t2182_ret;  // Auto-generated
    int t2311_ret;  // Auto-generated
    int t2325_ret;  // Auto-generated
    int t2333_ret;  // Auto-generated
    int t2341_ret;  // Auto-generated
    int t2576_ret;  // Auto-generated
    int t2622_ret;  // Auto-generated
    int t2664_ret;  // Auto-generated
    int t2673_ret;  // Auto-generated
    int t2696_ret;  // Auto-generated
    int t2766_ret;  // Auto-generated
    int t2941_ret;  // Auto-generated
    int x;  // Auto-generated
    int y;  // Auto-generated
    int z;  // Auto-generated

    c_Vector3 vec;
    char local_67[32];
    dword* tmp83;
    float data_;
    float data_235;
    float local_1;
    float local_2;
    float t2350_ret;
    float t2484_ret;
    float t2542_ret;
    int data_224;
    int data_225;
    int data_264;
    int data_266;
    int data_268;
    int g_music;
    int g_save;
    int g_will_pos;
    int i;
    int j;
    int k;
    int local_0;
    int local_11;
    int local_17;
    int local_22;
    int local_23;
    int local_24;
    int local_25;
    int local_26;
    int local_27;
    int local_43;
    int local_63;
    int local_80;
    int local_83;
    int local_87;
    int local_88;
    int local_89;
    int local_90;
    int obj;
    int ptr;
    int ptr1;
    int ptr13;
    int ptr14;
    int ptr15;
    int ptr16;
    int ptr17;
    int ptr18;
    int ptr19;
    int ptr2;
    int ptr20;
    int ptr22;
    int ptr25;
    int ptr26;
    int ptr27;
    int ptr4;
    int ptr5;
    int ptr9;
    int side;
    int side2;
    int sideB;
    int t1463_;
    int t1481_;
    int t2409_;
    int t2523_;
    int tmp140;
    int tmp205;
    int tmp242;
    int tmp274;
    int tmp275;
    int tmp279;
    int tmp283;
    int tmp3;
    int tmp396;
    s_SC_P_getinfo player_info;
    s_SC_initgroup idx;
    s_SC_initside local_4;
    void* tmp78;

    switch (info->message) {
    case 0:
        switch (info->param1) {
        case 0:
            local_4.MaxHideOutsStatus = 32;
            local_4.MaxGroups = 4;
            SC_InitSide(0, &local_4);
            idx.SideId = 0;
            idx.GroupId = 0;
            idx.MaxPlayers = 16;
            idx.NoHoldFireDistance = 100.0f;
            SC_InitSideGroup(&idx);
            idx.SideId = 0;
            idx.GroupId = 1;
            idx.MaxPlayers = 2;
            idx.NoHoldFireDistance = 100.0f;
            SC_InitSideGroup(&idx);
            idx.SideId = 0;
            idx.GroupId = 2;
            idx.MaxPlayers = 16;
            idx.NoHoldFireDistance = 100.0f;
            SC_InitSideGroup(&idx);
            local_4.MaxGroups = 12;
            SC_InitSide(1, &local_4);
            // Loop header - Block 111 @1272
            for (ptr5 = 0; ptr5 < 12; ptr5 = ptr5 + 1) {
                idx.SideId = 1;
                idx.GroupId = ptr5;
                idx.MaxPlayers = 16;
                idx.NoHoldFireDistance = 100.0f;
                SC_InitSideGroup(&idx);
                local_20 = ptr5 + 1;
            }
            local_4.MaxHideOutsStatus = 2;
            local_4.MaxGroups = 2;
            SC_InitSide(2, &local_4);
            idx.SideId = 2;
            idx.GroupId = 0;
            idx.MaxPlayers = 1;
            idx.NoHoldFireDistance = 100.0f;
            SC_InitSideGroup(&idx);
            idx.SideId = 2;
            idx.GroupId = 1;
            idx.MaxPlayers = 20;
            idx.NoHoldFireDistance = 0;
            SC_InitSideGroup(&idx);
            SC_SetSideAlly(0, 2, 1.0f);
            SC_SetSideAlly(1, 2, 1.0f);
            local_4.MaxHideOutsStatus = 2;
            local_4.MaxGroups = 1;
            SC_InitSide(3, &local_4);
            idx.SideId = 3;
            idx.GroupId = 0;
            idx.MaxPlayers = 16;
            idx.NoHoldFireDistance = 0;
            SC_InitSideGroup(&idx);
            SC_SetSideAlly(0, 3, 0.0f);
            SC_SetSideAlly(1, 3, 1.0f);
            SC_SetSideAlly(2, 3, 0.0f);
            func_0994(0);
            gphase = 1;
            SC_sgi(SGI_LEVPILOT_S1G0, 0);
            SC_sgi(SGI_LEVPILOT_S1G1, 0);
            SC_sgi(SGI_LEVPILOT_S1G2, 0);
            SC_sgi(SGI_LEVPILOT_S1G3, 0);
            SC_sgi(SGI_LEVPILOT_S1G4, 0);
            // Loop header - Block 114 @1455
            for (ptr5 = 0; ptr5 < 4; ptr5 = ptr5 + 1) {
                SC_ZeroMem(tmp78, 12);
                (&local_43) + ptr5 * 20 = 1.5f;
                *tmp83 = 5.0f;
                (&local_63) + ptr5 * 4 = ptr5;
                local_20 = ptr5 + 1;
            }
            // Loop header - Block 117 @1506
            for (ptr5 = 0; ptr5 < 10; ptr5 = ptr5 + 1) {
                SC_Ai_SetPlFollow(1, ptr5, 0, &local_43, &local_63, &local_63, 4);
                local_20 = ptr5 + 1;
            }
            // Loop header - Block 120 @1532
            for (ptr5 = 0; ptr5 < 4; ptr5 = ptr5 + 1) {
                t1544_ret = sprintf(local_67, "WP_will%d", ptr5 + 1);
                t1556_ret = SC_GetWp(local_67, &g_will_pos[ptr5]);
                local_20 = ptr5 + 1;
            }
            SC_sgi(SGI_LEVELPHASE, 0);
            SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0);
            SC_sgi(SGI_LEVPILOT_JUSTLOADEDVALUE, 0);
            SC_RadioSetDist(10.0f);
            SC_ZeroMem(&g_save, 8);
            SC_ZeroMem(&g_music, 8);
            SC_ArtillerySupport(0);
            SC_SetViewAnim(&tmp337, 0, 350, 0);
            SC_FadeTo(1, 0.0f);
            SC_FadeTo(0, 3.0f);
            break;
        case 1:
            t1618_ret = SC_ggi(SGI_LEVELPHASE);
            local_20 = SC_ggi(SGI_LEVELPHASE);
            if (g_save[0]) {
            } else {
                t1635_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
                if (ptr15 && t1646_ret = SC_P_IsReady(ptr15)) {
                    g_save[0] = 1;
                    local_80.text_id = 9136;
                    local_80.status = 9137;
                    SC_MissionSave(&local_80);  // 9137: "You are flying over the ricefields."
                }
            }
            if (tmp140) {
            } else {
                if (gStartMusicTime > 0.0f && gStartMusicTime <= 0.0f) {
                    g_music = 1;
                    t1700_ret = SC_AGS_Set(0);
                }
            }
            if (local_89 == 0) {
                if (local_90 == 0) {
                    local_0 = 0.5f;
                    SC_SpeechRadio2(3400, &local_0);
                    local_0 += 0.3f;
                    SC_SpeechRadio2(3401, &local_0);
                    local_0 += 0.3f;
                    SC_SpeechRadio2(3402, &local_0);
                    local_0 += 0.5f;
                    SC_SpeechRadio2(3403, &local_0);
                    local_0 += 0.3f;
                    SC_SpeechRadio2(3404, &local_0);
                    local_0 += 0.5f;
                    g_dialog = 1;
                } else {
                    if (local_90 == 1) {
                        if (t1785_ret = SC_ggi(SGI_LEVPILOT_HELI3_ATTACK)) {
                        } else {
                            t1797_ret = SC_P_GetBySideGroupMember(0, 0, 2);
                            local_24 = SC_P_GetBySideGroupMember(0, 0, 2);
                            t1808_ret = SC_P_GetBySideGroupMember(0, 0, 5);
                            local_25 = SC_P_GetBySideGroupMember(0, 0, 5);
                            t1819_ret = SC_P_GetBySideGroupMember(0, 0, 4);
                            local_27 = SC_P_GetBySideGroupMember(0, 0, 4);
                            local_0 = 3.0f;
                            SC_P_Speech2(ptr17, 3420, &local_0);
                            local_0 = 3.2f;
                            SC_P_Speech2(ptr18, 3421, &local_0);
                            g_dialog = 2;
                        }
                    } else {
                        if (local_90 == 2) {
                            if (t1856_ret = SC_ggi(SGI_LEVPILOT_HELI3_ATTACK)) {
                            } else {
                                t1868_ret = SC_P_GetBySideGroupMember(0, 2, 1);
                                local_26 = SC_P_GetBySideGroupMember(0, 2, 1);
                                local_0 = 1.0f;
                                SC_P_Speech2(ptr20, 3422, &local_0);
                                local_0 += 0.3f;
                                t1894_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                                SC_P_Speech2(SC_P_GetBySideGroupMember(0, 0, 0), 3423, &local_0);
                                local_0 += 0.4f;
                                SC_P_Speech2(ptr20, 3422, &local_0);
                                local_0 += 0.3f;
                                SC_SpeechRadio2(3416, &local_0);
                                local_0 += 0.5f;
                                SC_SpeechRadio2(3417, &local_0);
                                local_0 += 0.5f;
                                SC_SpeechRadio2(3418, &local_0);
                                local_0 += 0.5f;
                                SC_P_Speech2(ptr20, 3419, &local_0);
                                local_0 += 2.0f;
                                local_2 = local_0 - 1.2f;
                                t1970_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                                SC_P_Speech2(SC_P_GetBySideGroupMember(0, 0, 0), 3430, &local_2);
                                local_2 = ptr22 + 1.5f;
                                SC_P_Speech2(ptr18, 3431, &local_0);
                                SC_SpeechRadio2(3424, &local_0);
                                local_0 += 0.5f;
                                SC_SpeechRadio2(3425, &local_0);
                                local_0 += 0.5f;
                                SC_SpeechRadio2(3426, &local_0);
                                local_0 += 0.5f;
                                SC_SpeechRadio2(3427, &local_0);
                                local_0 += 0.5f;
                                SC_SpeechRadio2(3428, &local_0);
                                local_0 += 0.5f;
                                SC_SpeechRadio2(3429, &local_0);
                                local_0 += 0.5f;
                                g_dialog = 3;
                            }
                        } else {
                            if (local_90 == 3) {
                                if (t2061_ret = SC_ggi(SGI_LEVPILOT_HELI3_ATTACK)) {
                                } else {
                                    local_0 = 0;
                                    SC_SpeechRadio2(3440, &local_0);
                                    local_0 += 0.5f;
                                    SC_SpeechRadio2(3441, &local_0);
                                    local_0 += 0.5f;
                                    SC_SpeechRadio2(3442, &local_0);
                                    local_0 += 0.5f;
                                    SC_SpeechRadio2(3443, &local_0);
                                    local_0 += 0.5f;
                                    SC_SpeechRadio2(3444, &local_0);
                                    local_0 += 0.5f;
                                    SC_SpeechRadio2(3445, &local_0);
                                    local_0 += 0.5f;
                                    SC_SpeechRadio2(3446, &local_0);
                                    local_0 += 0.5f;
                                    g_dialog = 4;
                                }
                            } else {
                                if (local_90 == 4) {
                                    if (t2155_ret = SC_ggi(SGI_LEVPILOT_HELI3_ATTACK)) {
                                    } else {
                                        g_dialog = 5;
                                        t2171_ret = SC_P_GetBySideGroupMember(0, 2, 1);
                                        local_26 = SC_P_GetBySideGroupMember(0, 2, 1);
                                        t2182_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                                        local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
                                        local_0 = 0;
                                        SC_P_Speech2(ptr20, 3447, &local_0);
                                        local_0 += 0.3f;
                                        SC_P_Speech2(ptr15, 3448, &local_0);
                                        local_0 += 0.6f;
                                        SC_P_Speech2(ptr20, 3449, &local_0);
                                        local_0 += 0.3f;
                                        local_0 - 1.0f = tmp205;
                                        SC_P_Speech2(ptr15, 3450, &local_0);
                                    }
                                } else {
                                    if (local_90 == 5) {
                                        SC_PC_EnableExit(1);
                                        g_dialog = 6;
                                    }
                                }
                            }
                        }
                    }
                }
            } else {
                if (local_89 == 1) {
                    if (g_dochange) {
                        func_0292();
                        func_0355();
                        g_dochange = 0;
                        if (g_save[1]) {
                        } else {
                            g_save[1] = 1;
                            local_80.text_id = 9138;
                            local_80.status = 9139;
                            SC_MissionSave(&local_80);  // 9139: "There is a pilot from the crashed hel..."
                        }
                    }
                    func_0612(info->elapsed_time);
                } else {
                    if (local_89 == 2) {
                        func_0612(info->elapsed_time);
                        t2311_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                        local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
                        if (ptr && ptr15) {
                            if (t2325_ret = SC_P_GetActive(ptr)) {
                                if (t2333_ret = SC_P_IsReady(ptr)) {
                                    if (t2341_ret = SC_P_IsReady(ptr15)) {
                                        t2350_ret = SC_P_GetDistance(ptr, ptr15);
                                        local_1 = SC_P_GetDistance(ptr, ptr15);
                                        if (ptr25 < 10.0f) {
                                            SC_sgi(SGI_LEVELPHASE, 3);
                                            local_0 = 0;
                                            SC_P_Speech2(ptr15, 3451, &local_0);
                                            local_0 += 1.6f;
                                            SC_P_Speech2(ptr, 3452, &local_0);
                                            local_0 += 0.5f;
                                            SC_P_Speech2(ptr15, 3453, &local_0);
                                            local_0 = tmp242;
                                            local_83 = 3471;
                                            local_83.y = 2;
                                            SC_SetObjectives(1, &local_83, 0.0f);  // 3471: "Find the pilot"
                                        }
                                    }
                                }
                            }
                        }
                    } else {
                        if (local_89 == 3) {
                            SC_Radio_Enable(20);
                            SC_PC_EnableRadioBreak(1);
                            SC_sgi(SGI_LEVELPHASE, 4);
                        } else {
                            if (local_89 == 4) {
                            } else {
                                if (local_89 == 5) {
                                    if (gPilotCommTime > 0.0f) {
                                        gPilotCommTime -= info->elapsed_time;
                                    } else {
                                        func_0612(info->elapsed_time);
                                        SC_P_GetPos(ptr, &vec);
                                        local_20 = 0;
                                    }
                                } else {
                                    if (local_89 == 6) {
                                        func_0612(info->elapsed_time);
                                    } else {
                                        if (local_89 == 7) {
                                            local_20 = 2;
                                            g_final_enter_timer += info->elapsed_time;
                                            if (t2622_ret = SC_P_IsInHeli(ptr)) {
                                                local_20 = ptr5 - 1;
                                            } else {
                                                if (g_final_enter_timer > 30.0f) {
                                                    SC_P_SetToHeli(ptr, "heli2", 3);
                                                } else {
                                                    func_0985(ptr);
                                                    SC_P_Ai_EnterHeli(ptr, "heli2", 4);
                                                    &param_0.next_exe_time = 4.0f;
                                                }
                                            }
                                            t2664_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                                            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
                                            if (t2673_ret = SC_P_IsInHeli(ptr15)) {
                                                local_20 = ptr5 - 1;
                                            }
                                            if (ptr5 == 0) {
                                                SC_sgi(SGI_LEVELPHASE, 8);
                                                t2696_ret = SC_AGS_Set(1);
                                                &param_0.next_exe_time = 0.1f;
                                                gEndTimer = 15.0f;
                                            }
                                        } else {
                                            if (local_89 == 8) {
                                                gEndTimer -= info->elapsed_time;
                                                if (gEndTimer < 0.0f) {
                                                    func_1021();
                                                    SC_TheEnd();
                                                    SC_sgi(SGI_LEVELPHASE, 9);
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            // Loop header - Block 199 @2472
            for (ptr9 = 0; ptr9 < 4; ptr9 = ptr9 + 1) {
                if (t2484_ret = SC_2VectorsDist(&vec, &g_will_pos[ptr9])) {
                    SC_sgi(SGI_LEVELPHASE, 6);
                    SC_sgi(SGI_LEVPILOT_EVACVILLID, ptr9);
                    vec.z + 1.5f += 1.5f;
                    local_17.x = tmp274 - tmp275;
                    tmp279 - vec.y = tmp283;
                    local_17.z = 0;
                    t2542_ret = SC_VectorLen(&local_17);
                    local_0 = SC_VectorLen(&local_17) / 10.0f;
                    local_17.x /= local_0;
                    local_17.y /= local_0;
                    local_17.z = 7.0f;
                    t2576_ret = SC_Item_Create2(147, &vec, &local_17);
                } else {
                    local_20 = ptr9 + 1;
                }
                local_20 = ptr9 + 1;
            }
            break;
        }
        SC_P_GetInfo(ptr, &player_info);
        if (tmp3 <= 0.0f) {
            SC_MissionFailed();
        } else {
            &param_0.next_exe_time = 0.2f;
            if (g_showinfo_timer < 11.0f) {
                local_0 = g_showinfo_timer;
                g_showinfo_timer += info->elapsed_time;
                if (local_0 < 4.0f && g_showinfo_timer >= 4.0f) {
                    local_63 = 0;
                    local_63[0].y = 3490;
                    local_63[0].z = 3491;
                    SC_ShowMovieInfo(&local_63);  // 3490: "17.12. 1967 8:00" | 3491: "Ricefields around Khe Bana river"
                }
                if (local_0 < 10.5f && g_showinfo_timer >= 10.5f) {
                    SC_ShowMovieInfo(0);
                }
            }
        }
        break;
    case 1:
        if (local_88 == 20) {
            SC_sgi(SGI_LEVELPHASE, 5);
            SC_RadioBatch_Begin();
            local_0 = 0;
            t2766_ret = SC_P_GetBySideGroupMember(0, 0, 0);
            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
            SC_P_Speech2(ptr15, 3454, &local_0);
            local_0 += 1.3f;
            SC_SpeechRadio2(3455, &local_0);
            local_0 += 0.5f;
            SC_P_Speech2(ptr15, 3456, &local_0);
            local_0 += 0.7f;
            SC_SpeechRadio2(3461, &local_0);
            local_0 += 0.5f;
            SC_P_SpeechMes2(ptr15, 3457, &local_0, 11);
            gPilotCommTime = local_0 + 3.0f;
            &param_0.next_exe_time = 0.1f;
            SC_RadioBatch_End();
        }
        break;
    case 2:
        if (local_88 == 11) {
            SC_message(&tmp373);
            if (gPilotCommTime > 3.0f) {
                gPilotCommTime = 3.0f;
            }
        }
        break;
    case 4:
        switch (info->param1) {
        case 10:
            func_0994(1);
            break;
        case 667:
            break;
        }
        break;
    case 3:
        break;
    case 7:
        SC_SetObjectScript("heli1", "levels\\ricefield\\data\\pilot\\scripts\\heli1.c");
        SC_SetObjectScript("heli2", "levels\\ricefield\\data\\pilot\\scripts\\heli2.c");
        SC_SetObjectScript("heli3", "levels\\ricefield\\data\\pilot\\scripts\\heli3.c");
        SC_Item_Preload(147);
        SC_SetMapFpvModel("g\\weapons\\Vvh_map\\map_ricefield.bes");
        SC_sgi(SGI_CURRENTMISSION, 25);
        SC_PreloadBES(1, "Levels\\Ricefield\\data\\Pilot\\objects\\ivq_kopac.bes");
        gStartMusicTime = 0.2f;
        break;
    case 11:
        t2941_ret = SC_ggi(SGI_LEVPILOT_JUSTLOADEDVALUE);
        SC_sgi(SGI_LEVPILOT_JUSTLOADEDVALUE, SC_ggi(SGI_LEVPILOT_JUSTLOADEDVALUE) + 1);
        func_0994(g_trashes_enabled);
        break;
    case 15:
        if (param_0->field_4 >= 20) {
            &param_0.param3 = 0;
        } else {
            param_0->field_8 = tmp396;
            &param_0.param3 = 1;
        }
        break;
    }
    return TRUE;
}

