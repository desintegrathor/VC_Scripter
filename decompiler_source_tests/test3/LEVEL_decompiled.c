// Structured decompilation of decompiler_source_tests\test3\LEVEL.SCR
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

int _init(s_SC_L_info *info) {
    return;
}

int func_0292(void) {
    int j;
    int k;
    c_Vector3 vec;

    SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0);
    SC_ZeroMem(&vec, 12);
    vec.z = -20000.0f;
    local_0 = 0;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0355(void) {
    int j;
    int k;
    int local_2;

    local_1 = 0;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0448(int param_0) {
    return SC_P_GetBySideGroupMember(2, 0, 1);
}

int func_0511(int param_0, int param_1) {
    dword local_3[2];
    int g_will_pos;
    int k;
    float local_5;
    c_Vector3 vec;

    SC_P_GetPos(param_1, &vec);
    SC_ZeroMem(&local_3, 8);
    local_6 = 0;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0612(int param_0, float param_1) {
    int g_vill_visited;
    int g_will_pos;
    int j;
    int k;
    float local_10;
    int local_11;
    dword local_12;
    dword local_13;
    int local_2;
    BOOL t625_ret;
    c_Vector3 vec;
    c_Vector3 vec2;

    switch (g_pilot_phase) {
    case 0:
        t625_ret = SC_PC_GetPos(&vec);
        local_0 = 0;
        break;
    case 1:
        g_pilot_timer -= param_0;
        if (g_pilot_timer <= 0.0f) {
            g_pilot_phase = 2;
            t759_ret = SC_PC_Get();
            func_0511(t759_ret, &local_2);
            g_pilot_vill_nr = tmp30;
            func_0448();
            SC_P_ScriptMessage(local_12, 0, g_pilot_vill_nr);
            g_pilot_timer = 210.0f + frnd(30.0f);
            SC_SpeechRadio2(3463 + 2 * g_pilot_vill_nr + rand() % 2, 0);
            func_0448();
            SC_HUD_RadarShowPlayer(local_12, -16711936);
        }
        break;
    case 2:
        g_pilot_timer -= param_0;
        if (g_pilot_timer < 0.0f) {
            g_pilot_phase = 1;
            g_pilot_timer = 30.0f + frnd(10.0f);
            g_pilot_vill_nr = 255;
            func_0448();
            SC_P_ScriptMessage(local_12, 0, g_pilot_vill_nr);
            SC_HUD_RadarShowPlayer(0, 0);
        } else {
            t870_ret = SC_PC_GetPos(&vec);
            func_0448(SC_PC_GetPos(&vec));
            SC_P_GetPos(local_12, &vec2);
            if (SC_IsNear2D( & vec, & vec2, 50.0f)) {
                g_pilot_phase = 4;
                g_pilot_timer = 0;
                SC_SetSideAlly(1, 2, -1.0f);
                SC_sgi(SGI_LEVELPHASE, 2);
            }
        }
        break;
    case 4:
        if (SC_ggi(SGI_LEVELPHASE) > 5) {
        } else {
            g_pilot_timer -= param_0;
            if (g_pilot_timer <= 0.0f) {
                g_pilot_timer = 1.5f;
                func_0448();
                t944_ret = SC_PC_Get();
                local_10 = SC_P_GetDistance(local_13, t944_ret);
                if (ptr2 > 15.0f) {
                    t960_ret = SC_PC_GetPos(&vec2);
                    func_0448(SC_PC_GetPos(&vec2));
                    SC_P_Ai_Go(local_12, &vec2);
                } else {
                    if (ptr2 < 8.0f) {
                        func_0448();
                        SC_P_Ai_Stop(local_12);
                    }
                }
            }
        }
        break;
    default:
        if (local_11 == 1) {
        } else {
            if (local_11 == 2) {
            } else {
                if (local_11 == 4) {
                }
            }
        }
        break;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

void func_0985(int param_0, int param_1) {
    SC_P_Ai_SetMoveMode(param_0, SC_P_AI_MOVEMODE_RUN);
    SC_P_Ai_SetMovePos(param_0, SC_P_AI_MOVEPOS_STAND);
    return;
}

int func_0994(int param_0, int param_1) {
    int k;
    void* local_0;

    g_trashes_enabled = param_1;
    local_0 = SC_NOD_Get(0, "maj_uh-1d_vreck");
    if (local_0) {
        if (! param_0) {
        } else {
        }
        SC_DUMMY_Set_DoNotRenHier2(local_0, 1);
    }
    return;
}

int func_1021(void) {
    s_SC_MP_EnumPlayers enum_pl;
    int local_256;

    local_256 = 64;
    SC_sgi(SGI_DEBR_01, 0);
    SC_sgi(SGI_REWARD_PILOT, 1);
    t1040_ret = SC_MP_EnumPlayers(&enum_pl, &local_256, 1);
    if ((SC_MP_EnumPlayers( & enum_pl, & local_256, 1)) || ptr > 0) {
        SC_sgi(SGI_DEBR_01, -1);
        SC_sgi(SGI_REWARD_PILOT, 0);
    }
    return;
}

int ScriptMain(s_SC_L_info *info) {
    s_SC_Ai_PlFollow local_43;
    char local_67[32];
    int g_music;
    int g_save;
    int g_will_pos;
    float i;
    s_SC_initgroup idx;
    int j;
    float k;
    int local_0;
    float local_1;
    float local_2;
    int local_22;
    int local_23;
    int local_24;
    int local_25;
    int local_26;
    int local_27;
    s_SC_initside local_4;
    int local_63;
    s_SC_MissionSave local_80;
    s_SC_Objective local_83;
    int local_87;
    int local_88;
    int local_89;
    int local_90;
    s_SC_P_getinfo player_info;
    c_Vector3 vec;
    c_Vector3 vec2;

    switch (info->message) {
    case 0:
        local_23 = func_0448();
        if (ptr && tmp3 <= 0.0f) {
            SC_MissionFailed();
        }
        param_0->next_exe_time = 0.2f;
        if (g_showinfo_timer < 11.0f) {
            local_0 = g_showinfo_timer;
            g_showinfo_timer += info->elapsed_time;
            if (local_0 < 4.0f && g_showinfo_timer >= 4.0f) {
                local_63 = 0;
                (&local_63) + 4 = 3490;
                (&local_63) + 8 = 3491;
                SC_ShowMovieInfo(&local_63);
            }
            if (local_0 < 10.5f && g_showinfo_timer >= 10.5f) {
                SC_ShowMovieInfo(0);
            }
        }
        if (local_88 == 0) {
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
            local_20 = 0;
        } else {
            local_20 = SC_ggi(SGI_LEVELPHASE);
            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
            g_save[0] = 1;
            local_80.savename_id = 9136;
            local_80.description_id = 9137;
            SC_MissionSave(&local_80);  // 9137: "You are flying over the ricefields."
            gStartMusicTime -= info->elapsed_time;
            g_music = 1;
            t1700_ret = SC_AGS_Set(0);
        }
        for (local_20 = 0; local_20 < 12; local_20++) {
            idx.SideId = 1;
            idx.GroupId = obj;
            idx.MaxPlayers = 16;
            idx.NoHoldFireDistance = 100.0f;
            SC_InitSideGroup(&idx);
            local_20 = obj + 1;
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
        local_20 = 0;
        for (local_20 = 0; local_20 < 4; local_20++) {
            SC_ZeroMem(t1464_, 12);
            local_43[obj] = 1.5f;
            local_43[obj].y = 5.0f;
            (&local_63) + obj * 4 = obj;
            local_20 = obj + 1;
        }
        local_20 = 0;
        for (local_20 = 0; local_20 < 10; local_20++) {
            SC_Ai_SetPlFollow(1, obj, 0, &local_43, &local_63, &local_63, 4);
            local_20 = obj + 1;
        }
        local_20 = 0;
        for (local_20 = 0; local_20 < 4; local_20++) {
            t1544_ret = sprintf(&local_67, "WP_will%d", obj + 1);
            t1556_ret = SC_GetWp(&local_67, &g_will_pos[obj]);
            local_20 = obj + 1;
        }
        SC_sgi(SGI_LEVELPHASE, 0);
        SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0);
        SC_sgi(SGI_LEVPILOT_JUSTLOADEDVALUE, 0);
        SC_RadioSetDist(10.0f);
        SC_ZeroMem(&g_save, 8);
        SC_ZeroMem(&g_music, 8);
        SC_ArtillerySupport(0);
        SC_SetViewAnim("g\\camanims\\CAMERA\\Pilot_in.anm", 0, 350, 0);
        SC_FadeTo(1, 0.0f);
        SC_FadeTo(0, 3.0f);
        switch (g_dialog) {
        case 0:
            local_0 = 0.5f;
            SC_SpeechRadio2(3400, &local_0);
            local_0 = obj + 0.3f;
            SC_SpeechRadio2(3401, &local_0);
            local_0 = tmp113 + 0.3f;
            SC_SpeechRadio2(3402, &local_0);
            local_0 += 0.5f;
            SC_SpeechRadio2(3403, &local_0);
            local_0 += 0.3f;
            SC_SpeechRadio2(3404, &local_0);
            local_0 += 0.5f;
            g_dialog = 1;
            break;
        case 1:
            if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK) < 1) {
            } else {
                local_24 = SC_P_GetBySideGroupMember(0, 0, 2);
                local_25 = SC_P_GetBySideGroupMember(0, 0, 5);
                local_27 = SC_P_GetBySideGroupMember(0, 0, 4);
                local_0 = 3.0f;
                SC_P_Speech2(ptr21, 3420, &local_0);
                local_0 = 3.2f;
                SC_P_Speech2(ptr22, 3421, &local_0);
                g_dialog = 2;
            }
            break;
        case 2:
            if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK) < 2) {
            } else {
                local_26 = SC_P_GetBySideGroupMember(0, 2, 1);
                local_0 = 1.0f;
                SC_P_Speech2(ptr24, 3422, &local_0);
                local_0 = tmp113 + 0.3f;
                t1894_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                SC_P_Speech2(t1894_ret, 3423, &local_0);
                local_0 += 0.4f;
                SC_P_Speech2(ptr24, 3422, &local_0);
                local_0 += 0.3f;
                SC_SpeechRadio2(3416, &local_0);
                local_0 += 0.5f;
                SC_SpeechRadio2(3417, &local_0);
                local_0 += 0.5f;
                SC_SpeechRadio2(3418, &local_0);
                local_0 += 0.5f;
                SC_P_Speech2(ptr24, 3419, &local_0);
                local_0 += 2.0f;
                local_2 = local_0 - 1.2f;
                t1970_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                SC_P_Speech2(t1970_ret, 3430, &local_2);
                local_2 = ptr26 + 1.5f;
                SC_P_Speech2(ptr22, 3431, &local_0);
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
            break;
        case 3:
            if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK) < 3) {
            } else {
                local_0 = 0;
                SC_SpeechRadio2(3440, &local_0);
                local_0 = obj + 0.5f;
                SC_SpeechRadio2(3441, &local_0);
                local_0 = tmp113 + 0.5f;
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
            break;
        case 4:
            if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK) < 4) {
            } else {
                g_dialog = 5;
                local_26 = SC_P_GetBySideGroupMember(0, 2, 1);
                local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
                local_0 = 0;
                SC_P_Speech2(ptr24, 3447, &local_0);
                local_0 += 0.3f;
                SC_P_Speech2(ptr15, 3448, &local_0);
                local_0 += 0.6f;
                SC_P_Speech2(ptr24, 3449, &local_0);
                local_0 += 0.3f;
                /* invalid store: local_0 - 1.0f = tmp165; */
                SC_P_Speech2(ptr15, 3450, &local_0);
            }
            break;
        case 5:
            SC_PC_EnableExit(1);
            g_dialog = 6;
            break;
        }
        switch (local_89) {
        case 1:
            if (g_dochange) {
                func_0292();
                func_0355();
                g_dochange = 0;
                if (g_save[1]) {
                } else {
                    g_save[1] = 1;
                    local_80.savename_id = 9138;
                    local_80.description_id = 9139;
                    SC_MissionSave(&local_80);  // 9139: "There is a pilot from the crashed helicopter somewhere in the ricefields.  Captain Rosenfield wants you to find him and bring him back alive."
                }
            }
            func_0612(info->elapsed_time);
            break;
        case 2:
            func_0612(info->elapsed_time);
            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
            if (ptr && ptr15) {
                if (SC_P_GetActive(ptr)) {
                    if (SC_P_IsReady(ptr)) {
                        if (SC_P_IsReady(ptr15)) {
                            local_1 = SC_P_GetDistance(ptr, ptr15);
                            if (ptr28 < 10.0f) {
                                SC_sgi(SGI_LEVELPHASE, 3);
                                local_0 = 0;
                                SC_P_Speech2(ptr15, 3451, &local_0);
                                local_0 += 1.6f;
                                SC_P_Speech2(ptr, 3452, &local_0);
                                local_0 += 0.5f;
                                SC_P_Speech2(ptr15, 3453, &local_0);
                                local_0 = tmp187;
                                local_83.text_id = 3471;
                                local_83.status = 2;
                                SC_SetObjectives(1, &local_83, 0.0f);  // 3471: "Find the pilot"
                            }
                        }
                    }
                }
            }
            break;
        case 3:
            SC_Radio_Enable(20);
            SC_PC_EnableRadioBreak(1);
            SC_sgi(SGI_LEVELPHASE, 4);
            break;
        case 4:
            break;
        case 5:
            if (gPilotCommTime > 0.0f) {
                gPilotCommTime -= info->elapsed_time;
            } else {
                func_0612(info->elapsed_time);
                SC_P_GetPos(ptr, &vec);
                local_20 = 0;
            }
            // Loop header - Block 199 @2472
            for (local_20 = obj; local_20 < 4; local_20++) {
                if ((SC_2VectorsDist( & vec, & g_will_pos[obj])) < 40.0f) {
                    SC_sgi(SGI_LEVELPHASE, 6);
                    SC_sgi(SGI_LEVPILOT_EVACVILLID, obj);
                    vec.z += 1.5f;
                    vec2.x = tmp210 - tmp211;
                    /* invalid store: tmp215 - vec.y = tmp219; */
                    vec2.z = 0.0f;
                    t2542_ret = SC_VectorLen(&vec2);
                    local_0 = (SC_VectorLen(&vec2)) / 10.0f;
                    vec2.x /= t2551_;
                    /* invalid store: vec2.y / vec2.y = tmp228; */
                    vec2.z = 7.0f;
                    t2576_ret = SC_Item_Create2(147, &vec, &vec2);
                } else {
                    local_20 = obj + 1;
                }
            }
            break;
        case 6:
            func_0612(info->elapsed_time);
            break;
        case 7:
            local_20 = 2;
            g_final_enter_timer += info->elapsed_time;
            if (SC_P_IsInHeli(ptr)) {
                local_20 = ptr12 - 1;
            } else {
                if (g_final_enter_timer > 30.0f) {
                    SC_P_SetToHeli(ptr, "heli2", 3);
                } else {
                    func_0985(ptr);
                    SC_P_Ai_EnterHeli(ptr, "heli2", 4);
                    param_0->next_exe_time = 4.0f;
                }
            }
            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
            if (SC_P_IsInHeli(ptr15)) {
                local_20 = ptr12 - 1;
            }
            if (ptr12 == 0) {
                SC_sgi(SGI_LEVELPHASE, 8);
                t2696_ret = SC_AGS_Set(1);
                param_0->next_exe_time = 0.1f;
                gEndTimer = 15.0f;
            }
            break;
        case 8:
            gEndTimer -= info->elapsed_time;
            if (gEndTimer < 0.0f) {
                func_1021();
                SC_TheEnd();
                SC_sgi(SGI_LEVELPHASE, 9);
            }
            break;
        }
        break;
    case 1:
        if (local_88 == 20) {
            SC_sgi(SGI_LEVELPHASE, 5);
            SC_RadioBatch_Begin();
            local_0 = 0;
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
            param_0->next_exe_time = 0.1f;
            SC_RadioBatch_End();
        }
        break;
    case 2:
        if (local_88 == 11) {
            SC_message(&data_759);
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
        SC_sgi(SGI_CURRENTMISSION, MISSION_PILOT);
        SC_PreloadBES(1, "Levels\\Ricefield\\data\\Pilot\\objects\\ivq_kopac.bes");
        gStartMusicTime = 0.2f;
        break;
    case 11:
        SC_sgi(SGI_LEVPILOT_JUSTLOADEDVALUE, SC_ggi(SGI_LEVPILOT_JUSTLOADEDVALUE) + 1);
        func_0994(g_trashes_enabled);
        break;
    case 15:
        if ((param_0- > field_4) >= 20) {
            param_0->param3 = 0;
        } else {
            param_0->field_8 = tmp293;
            param_0->param3 = 1;
        }
        break;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

