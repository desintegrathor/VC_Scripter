// Structured decompilation of decompiler_source_tests/test3/LEVEL.SCR
// Functions: 11

#include <inc\sc_global.h>
#include <inc\sc_def.h>

void func_0292(void) {
    int j;
    int k;
    dword local_1;
    c_Vector3 vec;

    SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0);
    SC_ZeroMem(&vec, 12);
    vec.z = -20000.0f;
    local_0 = 0;
    for (i = 0; i < 16; i++) {
        local_1 = SC_P_GetBySideGroupMember(1, 9, 9);
        if (! local_1) {
            SC_P_SetActive(local_1, FALSE);
            SC_P_SetPos(local_1, &vec);
        } else {
            local_0 = i + 1;
        }
    }
    if (i >= 16) {
        return;
    }
    if (! local_1 || ! SC_P_IsReady(local_1)) {
    }
}

void func_0355(void) {
    dword i;
    int j;
    int k;
    dword local_2;

    local_1 = 0;
    local_0 = 0;
    local_2 = SC_P_GetBySideGroupMember(1, i, i);
    SC_P_SetActive(local_2, TRUE);
    local_0 = idx + 1;
    local_1 = i + 1;
    local_2 = SC_P_GetBySideGroupMember(3, 0, i);
    SC_P_SetActive(local_2, TRUE);
    local_1 = i + 1;
    return;
}

int func_0448(void) {
    return SC_P_GetBySideGroupMember(2, 0, 1);
}

int func_0458(int param_0, int param_1, int param_2) {
    int j;
    int k;
    int local_2;

    local_1 = 0;
    local_0 = 0;
    for (i = 0; i < param_1; i++) {
        local_2 = SC_P_GetBySideGroupMember(1, param_0, param_0);
        if (! SC_P_IsReady(local_2)) {
            local_1++;
        } else {
            local_0 = i + 1;
        }
    }
    if (i >= param_1) {
        return local_1;
    }
    if (SC_P_IsReady(local_2)) {
    }
}

void func_0511(int param_0, int param_1) {
    dword local_3[2];
    int g_will_pos;
    int k;
    float local_5;
    c_Vector3 vec;

    SC_P_GetPos(param_0, &vec);
    SC_ZeroMem(&local_3, 8);
    local_6 = 0;
    for (i = 0; i < 4; i++) {
        local_5 = SC_2VectorsDist(&vec, &g_will_pos[i]);
        if (local_5 <= tmp5) {
            (&local_3) + 4 = tmp8;
            param_1[1] = param_1[0];
            local_3 = local_5;
            param_1[0] = i;
            local_6 = i + 1;
        } else {
            (&local_3) + 4 = local_5;
            param_1[1] = i;
        }
    }
    if (i >= 4) {
        return;
    }
    if (local_5 <= tmp5) {
        if (local_5 > tmp20) {
        }
    } else {
    }
}

void func_0612(float param_0) {
    int g_vill_visited;
    int g_will_pos;
    int j;
    int k;
    float local_10;
    int local_11;
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
        if (g_pilot_timer > 0.0f) break;
        g_pilot_phase = 2;
        func_0511(SC_PC_Get(), &local_2);
        g_pilot_vill_nr = tmp31;
        t780_ret = func_0448();
        SC_P_ScriptMessage(t780_ret, 0, g_pilot_vill_nr);
        g_pilot_timer = 210.0f + frnd(30.0f);
        SC_SpeechRadio2(3463 + 2 * g_pilot_vill_nr + rand() % 2, 0);
        t814_ret = func_0448();
        SC_HUD_RadarShowPlayer(t814_ret, -16711936);
        break;
    case 2:
        g_pilot_timer -= param_0;
        if (g_pilot_timer < 0.0f) {
            g_pilot_phase = 1;
            g_pilot_timer = 30.0f + frnd(10.0f);
            g_pilot_vill_nr = 255;
            t856_ret = func_0448();
            SC_P_ScriptMessage(t856_ret, 0, g_pilot_vill_nr);
            SC_HUD_RadarShowPlayer(0, 0);
        } else {
            t870_ret = SC_PC_GetPos(&vec);
            t876_ret = func_0448(SC_PC_GetPos(&vec));
            SC_P_GetPos(t876_ret, &vec2);
            if (! (SC_IsNear2D( & vec, & vec2, 50.0f))) break;
        }
        g_pilot_phase = 4;
        g_pilot_timer = 0;
        SC_SetSideAlly(1, 2, -1.0f);
        SC_sgi(SGI_LEVELPHASE, 2);
        break;
    case 4:
        if (SC_ggi(SGI_LEVELPHASE) > 5) break;
        if (g_pilot_timer > 0.0f) break;
        g_pilot_timer = 1.5f;
        t940_ret = func_0448();
        t944_ret = SC_PC_Get();
        local_10 = SC_P_GetDistance(t940_ret, t944_ret);
        if (local_10 > 15.0f) {
            t960_ret = SC_PC_GetPos(&vec2);
            t966_ret = func_0448(SC_PC_GetPos(&vec2));
            SC_P_Ai_Go(t966_ret, &vec2);
        } else {
            if (local_10 >= 8.0f) break;
        }
        t978_ret = func_0448();
        SC_P_Ai_Stop(t978_ret);
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
    t654_ret = SC_IsNear2D((&g_will_pos) + (&g_will_pos) * 12, &vec, 80.0f);
    (&g_vill_visited) + (&g_vill_visited) * 4 = 1;
    local_0 = t625_ret + 1;
    local_1++;
    local_0 = t625_ret + 1;
    return;
}

void func_0985(int param_0) {
    SC_P_Ai_SetMoveMode(param_0, SC_P_AI_MOVEMODE_RUN);
    SC_P_Ai_SetMovePos(param_0, SC_P_AI_MOVEPOS_STAND);
    return;
}

void func_0994(int param_0) {
    int k;
    void* local_0;

    g_trashes_enabled = param_0;
    local_0 = SC_NOD_Get(0, "maj_uh-1d_vreck");
    if (local_0) {
        if (! param_0) {
        } else {
        }
        SC_DUMMY_Set_DoNotRenHier2(local_0, 1);
    }
    return;
}

void func_1021(void) {
    s_SC_MP_EnumPlayers enum_pl;
    int local_256;

    local_256 = 64;
    SC_sgi(SGI_DEBR_01, 0);
    SC_sgi(SGI_REWARD_PILOT, 1);
    t1040_ret = SC_MP_EnumPlayers(&enum_pl, &local_256, 1);
    if ((SC_MP_EnumPlayers( & enum_pl, & local_256, 1)) || local_256 > 0) {
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
    dword i;
    s_SC_initgroup idx;
    int j;
    float k;
    int local_0;
    float local_1;
    float local_2;
    dword local_22;
    dword local_23;
    dword local_24;
    dword local_25;
    dword local_26;
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
        local_23 = t1092_ret;
        if (local_23 && tmp4 <= 0.0f) {
            SC_MissionFailed();
        }
        info->next_exe_time = 0.2f;
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
        for (i = 0; i < 12; i++) {
            idx.SideId = 1;
            idx.GroupId = i;
            idx.MaxPlayers = 16;
            idx.NoHoldFireDistance = 100.0f;
            SC_InitSideGroup(&idx);
            local_20 = i + 1;
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
        for (i = 0; i < 4; i++) {
            SC_ZeroMem(t1464_, 12);
            local_43[i] = 1.5f;
            local_43[i].y = 5.0f;
            (&local_63) + i * 4 = i;
            local_20 = i + 1;
        }
        local_20 = 0;
        for (i = 0; i < 10; i++) {
            SC_Ai_SetPlFollow(1, i, 0, &local_43, &local_63, &local_63, 4);
            local_20 = i + 1;
        }
        local_20 = 0;
        for (i = 0; i < 4; i++) {
            t1544_ret = sprintf(&local_67, "WP_will%d", i + 1);
            t1556_ret = SC_GetWp(&local_67, &g_will_pos[i]);
            local_20 = i + 1;
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
            local_0 = i + 0.3f;
            SC_SpeechRadio2(3401, &local_0);
            local_0 = tmp114 + 0.3f;
            SC_SpeechRadio2(3402, &local_0);
            local_0 += 0.5f;
            SC_SpeechRadio2(3403, &local_0);
            local_0 += 0.3f;
            SC_SpeechRadio2(3404, &local_0);
            local_0 += 0.5f;
            g_dialog = 1;
            break;
        case 1:
            if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK) < 1) break;
            local_24 = SC_P_GetBySideGroupMember(0, 0, 2);
            local_25 = SC_P_GetBySideGroupMember(0, 0, 5);
            local_27 = SC_P_GetBySideGroupMember(0, 0, 4);
            local_0 = 3.0f;
            SC_P_Speech2(local_24, 3420, &local_0);
            local_0 = 3.2f;
            SC_P_Speech2(local_25, 3421, &local_0);
            g_dialog = 2;
            break;
        case 2:
            if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK) < 2) break;
            local_26 = SC_P_GetBySideGroupMember(0, 2, 1);
            local_0 = 1.0f;
            SC_P_Speech2(local_26, 3422, &local_0);
            local_0 = tmp114 + 0.3f;
            t1894_ret = SC_P_GetBySideGroupMember(0, 0, 0);
            SC_P_Speech2(t1894_ret, 3423, &local_0);
            local_0 += 0.4f;
            SC_P_Speech2(local_26, 3422, &local_0);
            local_0 += 0.3f;
            SC_SpeechRadio2(3416, &local_0);
            local_0 += 0.5f;
            SC_SpeechRadio2(3417, &local_0);
            local_0 += 0.5f;
            SC_SpeechRadio2(3418, &local_0);
            local_0 += 0.5f;
            SC_P_Speech2(local_26, 3419, &local_0);
            local_0 += 2.0f;
            local_2 = local_0 - 1.2f;
            t1970_ret = SC_P_GetBySideGroupMember(0, 0, 0);
            SC_P_Speech2(t1970_ret, 3430, &local_2);
            local_2 = tmp141 + 1.5f;
            SC_P_Speech2(local_25, 3431, &local_0);
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
            break;
        case 3:
            if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK) < 3) break;
            local_0 = 0;
            SC_SpeechRadio2(3440, &local_0);
            local_0 = i + 0.5f;
            SC_SpeechRadio2(3441, &local_0);
            local_0 = tmp114 + 0.5f;
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
            break;
        case 4:
            if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK) < 4) break;
            g_dialog = 5;
            local_26 = SC_P_GetBySideGroupMember(0, 2, 1);
            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
            local_0 = 0;
            SC_P_Speech2(local_26, 3447, &local_0);
            local_0 += 0.3f;
            SC_P_Speech2(local_22, 3448, &local_0);
            local_0 += 0.6f;
            SC_P_Speech2(local_26, 3449, &local_0);
            local_0 += 0.3f;
            info->next_exe_time = local_0 - 1.0f;
            SC_P_Speech2(local_22, 3450, &local_0);
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
                if (!g_save[1]) {
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
            if (! local_23) break;
            if (! local_22) break;
            if (! SC_P_GetActive(local_23)) break;
            if (! SC_P_IsReady(local_23)) break;
            if (! SC_P_IsReady(local_22)) break;
            if (local_1 >= 10.0f) break;
            SC_sgi(SGI_LEVELPHASE, 3);
            local_0 = 0;
            SC_P_Speech2(local_22, 3451, &local_0);
            local_0 += 1.6f;
            SC_P_Speech2(local_23, 3452, &local_0);
            local_0 += 0.5f;
            SC_P_Speech2(local_22, 3453, &local_0);
            local_0 = tmp192;
            local_83.text_id = 3471;
            local_83.status = 2;
            SC_SetObjectives(1, &local_83, 0.0f);  // 3471: "Find the pilot"
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
                break;
            }
            func_0612(info->elapsed_time);
            SC_P_GetPos(local_23, &vec);
            // Loop header - Block 199 @2472
            for (local_20 = i; local_20 < 4; local_20++) {
                if ((SC_2VectorsDist( & vec, & g_will_pos[idx6])) < 40.0f) {
                    SC_sgi(SGI_LEVELPHASE, 6);
                    SC_sgi(SGI_LEVPILOT_EVACVILLID, idx6);
                    vec.z += 1.5f;
                    vec2.x = tmp216 - tmp217;
                    vec2.y = tmp221 - vec.y;
                    vec2.z = 0.0f;
                    t2542_ret = SC_VectorLen(&vec2);
                    local_0 = (SC_VectorLen(&vec2)) / 10.0f;
                    vec2.x /= t2551_;
                    vec2.y /= vec2.y;
                    vec2.z = 7.0f;
                    t2576_ret = SC_Item_Create2(147, &vec, &vec2);
                } else {
                    local_20 = idx6 + 1;
                }
            }
            break;
        case 6:
            func_0612(info->elapsed_time);
            break;
        case 7:
            local_20 = 2;
            g_final_enter_timer += info->elapsed_time;
            if (SC_P_IsInHeli(local_23)) {
                local_20 = idx6 - 1;
            } else {
                if (g_final_enter_timer > 30.0f) {
                    SC_P_SetToHeli(local_23, "heli2", 3);
                } else {
                    func_0985(local_23);
                    SC_P_Ai_EnterHeli(local_23, "heli2", 4);
                    info->next_exe_time = 4.0f;
                }
            }
            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
            if (SC_P_IsInHeli(local_22)) {
                local_20 = idx6 - 1;
            }
            if (idx6 != 0) break;
            SC_sgi(SGI_LEVELPHASE, 8);
            t2696_ret = SC_AGS_Set(1);
            info->next_exe_time = 0.1f;
            gEndTimer = 15.0f;
            break;
        case 8:
            if (gEndTimer >= 0.0f) break;
            func_1021();
            SC_TheEnd();
            SC_sgi(SGI_LEVELPHASE, 9);
            break;
        }
        break;
    case 1:
        if (local_88 == 20) {
            SC_sgi(SGI_LEVELPHASE, 5);
            SC_RadioBatch_Begin();
            local_0 = 0;
            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
            SC_P_Speech2(local_22, 3454, &local_0);
            local_0 += 1.3f;
            SC_SpeechRadio2(3455, &local_0);
            local_0 += 0.5f;
            SC_P_Speech2(local_22, 3456, &local_0);
            local_0 += 0.7f;
            SC_SpeechRadio2(3461, &local_0);
            local_0 += 0.5f;
            SC_P_SpeechMes2(local_22, 3457, &local_0, 11);
            gPilotCommTime = local_0 + 3.0f;
            info->next_exe_time = 0.1f;
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
        if (param_1->field_4 >= 20) {
            info->param3 = 0;
        } else {
            param_1->field_8 = tmp300;
            info->param3 = 1;
        }
        break;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

