// Structured decompilation of decompilation\pilot\LEVEL.SCR
// Functions: 10

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\mplevel.inc>

// Global variables
dword gVar1;
dword gVar4;
dword gVar2;
dword gVar;
dword gphase;
dword g_dialog;
dword g_will_group;
dword g_dochange;
float g_final_enter_timer;
dword g_will_pos;
dword g_vill_visited;
dword g_pilot_phase;
float g_pilot_timer;
dword g_pilot_vill_nr;
float g_showinfo_timer;
dword g_trashes_enabled;
dword gShot_pos;
float gEndTimer;
float gPilotCommTime;
dword g_save[64];
dword g_music;
float gStartMusicTime;
dword gVar7;
dword gVar8;
dword gVar9;
dword gVar10;
dword gVar11;
dword gVar13;
dword gVar3;
dword gVar12;
dword gVar6;
dword gVar5;

int _init(s_SC_L_info *info) {
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    return FALSE;
}

int func_0292(void) {
    int i;
    int local_;
    int local_2;

    SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0);
    SC_ZeroMem(&local_2, 12);
    local_2.field2 = -20000.0f;
    i = 0;
    // Loop header - Block 2 @312
    for (i = 0; (i < 16); i = i + 1) {
        if (!(i < 16)) break;  // exit loop @354
        local_ = SC_P_GetBySideGroupMember(1, 9, i);
        if (!local_) {
            SC_P_SetActive(local_, FALSE);
            SC_P_SetPos(local_, &local_2);
        } else {
            i++;
        }
        SC_P_IsReady(local_);
        if (!local_5) goto block_7; // @345
    }
    return i;
}

int func_0355(void) {
    int i;
    int idx;
    int local_;

    i = 0;
    // Loop header - Block 10 @362
    for (i = 0; (i < 12); i = i + 1) {
        if (!(i < 12)) break;  // exit loop @413
        if (!(i != 9)) {
            idx = 0;
        } else {
            i++;
        }
        // Loop header - Block 13 @374
        for (idx = 0; (idx < 16); idx = idx + 1) {
            if (!(idx < 16)) break;  // exit loop @404
            local_ = SC_P_GetBySideGroupMember(1, i, idx);
            if (!local_) {
                SC_P_SetActive(local_, TRUE);
            } else {
                idx++;
            }
        }
    }
    i = 0;
    // Loop header - Block 19 @417
    for (i = 0; (i < 16); i = i + 1) {
        if (!(i < 16)) break;  // exit loop @447
        local_ = SC_P_GetBySideGroupMember(3, 0, i);
        if (!local_) {
            SC_P_SetActive(local_, TRUE);
        } else {
            i++;
        }
    }
    return i;
}

int func_0448(int param, int param) {
    int i;
    int tmp;
    int tmp1;

    SC_P_GetBySideGroupMember(2, 0, 1);
    return FALSE;
    tmp = 0;
    i = 0;
    if (!(i < param)) {
        tmp1 = SC_P_GetBySideGroupMember(1, param_0, i);
        SC_P_IsReady(tmp1);
        tmp++;
        i++;
    }
    return tmp;
}

int func_0511(int param, int param) {
    dword local_3[16];
    int i;
    int local_;
    int tmp;

    SC_P_GetPos(param, &tmp);
    SC_ZeroMem(&local_3, 8);
    i = 0;
    // Loop header - Block 32 @527
    for (i = 0; (i < 4); i = i + 1) {
        if (!(i < 4)) break;  // exit loop @611
        local_ = SC_2VectorsDist(&tmp, &g_will_pos[i]);
        if (!(local_ > local_3)) {
            local_3.field1 = local_3;
            retval + 4 = (*retval);
            local_3 = local_;
            retval = i;
        } else {
        }
        local_3.field1 = local_;
        retval + 4 = i;
        i++;
        continue;  // back to loop header @527
    }
    return i;
}

int func_0612(float time) {
    int i;
    int local_;
    int local_1;
    int local_10;
    int local_11;
    int local_12;
    int local_13;
    int local_7;
    int tmp;
    int tmp1;

    if (!(g_pilot_phase == 0)) {
        SC_PC_GetPos(&local_);
        i = 0;
    }
    // Loop header - Block 41 @633
    for (i = 0; (i < 4); i = i + 1) {
        if (!(i < 4)) break;  // exit loop @675
        if (!g_vill_visited[i]) {
        } else {
            SC_IsNear2D(&g_will_pos[i], &local_, 80.0f);
        }
        g_vill_visited[i] = 1;
        i++;
        continue;  // back to loop header @633
    }
    local_1 = 0;
    i = 0;
    // Loop header - Block 48 @683
    for (i = 0; (i < 3); i = i + 1) {
        if (!(i < 3)) break;  // exit loop @711
        if (!g_vill_visited[i]) {
            local_1++;
        } else {
            i++;
        }
    }
    if (!(local_1 > 1)) {
        g_pilot_phase = 1;
        frnd(10.0f);
        g_pilot_timer = 10.0f + local_12;
    } else {
    }
    if (!g_vill_visited.field3) goto block_56; // @736
    switch (g_pilot_phase) {
    case 1:
        g_pilot_timer = g_pilot_timer - retval;
        if (g_pilot_timer <= 0) {
            g_pilot_phase = 2;
            SC_PC_Get();
            func_0511(local_12, &tmp);
            rand();
            g_pilot_vill_nr = local_2[local_13 % 2];
            func_0448();
            SC_P_ScriptMessage(local_12, 0, g_pilot_vill_nr);
            frnd(30.0f);
            g_pilot_timer = 30.0f + local_13;
            rand();
            SC_SpeechRadio2(3463 + 2 * g_pilot_vill_nr + local_13 % 2, 0.0f);
            func_0448();
            SC_HUD_RadarShowPlayer(local_12, -16711936);
        }
        break;
    case 2:
        g_pilot_timer = g_pilot_timer - retval;
        if (g_pilot_timer < 0) {
            g_pilot_phase = 1;
            frnd(10.0f);
            g_pilot_timer = 10.0f + local_13;
            g_pilot_vill_nr = 255;
            func_0448();
            SC_P_ScriptMessage(local_12, 0, g_pilot_vill_nr);
            SC_HUD_RadarShowPlayer(0, 0);
        } else {
            SC_PC_GetPos(&local_);
            func_0448();
            SC_P_GetPos(local_12, &local_7);
            if (SC_IsNear2D(&local_, &local_7, 50.0f)) {
                g_pilot_phase = 4;
                g_pilot_timer = 0;
                SC_SetSideAlly(1, 2, -1.0f);
                SC_sgi(SGI_LEVELPHASE, 2);
            }
        }
        break;
    case 4:
        SC_ggi(SGI_LEVELPHASE);
        if (local_12 > 5) {
        } else {
            g_pilot_timer = g_pilot_timer - retval;
            if (g_pilot_timer <= 0) {
                g_pilot_timer = 1.5f;
                func_0448();
                SC_PC_Get();
                local_10 = SC_P_GetDistance(local_13, tmp1);
                if (local_10 > 15.0f) {
                    SC_PC_GetPos(&local_7);
                    func_0448();
                    SC_P_Ai_Go(local_12, &local_7);
                } else {
                    if (local_10 < 8.0f) {
                        func_0448();
                        SC_P_Ai_Stop(local_12);
                    }
                }
            }
        }
        break;
    default:
        return &local_7;
    }
    return;
}

int func_0985(int param) {
    SC_P_Ai_SetMoveMode(retval, SC_P_AI_MOVEMODE_SNEAK);
    SC_P_Ai_SetMovePos(retval, SC_P_AI_MOVEPOS_STAND);
    return FALSE;
}

int func_0994(int param) {
    int local_;

    g_trashes_enabled = retval;
    local_ = SC_NOD_Get(0, "maj_uh-1d_vreck");
    if (!local_) {
        SC_DUMMY_Set_DoNotRenHier2(local_, 1);
    }
    return TRUE;
}

int func_1021(void) {
    int local_;

    local_ = 64;
    SC_sgi(SGI_DEBR_01, 0);
    SC_sgi(SGI_REWARD_PILOT, 1);
    SC_MP_EnumPlayers(&j, &local_, 1);
    if (!local_257) {
        SC_sgi(SGI_DEBR_01, -1);
        SC_sgi(SGI_REWARD_PILOT, 0);
    } else {
        return FALSE;
    }
    if (!(local_ > 0)) goto block_88; // @1056
    return;
}

int ScriptMain(s_SC_L_info *info) {
    char local_67[32];
    int i;
    int idx;
    int initgroup;
    int initside;
    int local_;
    int local_0;
    int local_11;
    int local_17;
    int local_2;
    int local_22;
    int local_25;
    int local_26;
    int local_63;
    int local_90;
    int local_91;
    int missionsave;
    int objective;
    int plfollow;
    int plinfo;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    switch (g_showinfo_timer) {
    case 0:
        local_ = func_0448();
        if (local_ && plinfo <= 0) {
            SC_MissionFailed();
            return TRUE;
        }
        param_0->field_20 = 0.20000000298023224f;
        if (g_showinfo_timer < 11.0f) {
            local_0 = g_showinfo_timer;
            g_showinfo_timer = g_showinfo_timer + info->elapsed_time;
            if (local_0 < 4.0f && g_showinfo_timer >= 4.0f) {
                local_63 = 0;
                local_63.field1 = 3490;
                local_63.field2 = 3491;
                SC_ShowMovieInfo(&local_63);
            }
            if (local_0 < 10.5f && g_showinfo_timer >= 10.5f) {
                SC_ShowMovieInfo(0);
            }
        }
        initside = 32;
        initside.field1 = 4;
        SC_InitSide(0, &initside);
        initgroup = 0;
        initgroup.field1 = 0;
        initgroup.field2 = 16;
        initgroup.field3 = 100.0f;
        SC_InitSideGroup(&initgroup);
        initgroup = 0;
        initgroup.field1 = 1;
        initgroup.field2 = 2;
        initgroup.field3 = 100.0f;
        SC_InitSideGroup(&initgroup);
        initgroup = 0;
        initgroup.field1 = 2;
        initgroup.field2 = 16;
        initgroup.field3 = 100.0f;
        SC_InitSideGroup(&initgroup);
        initside.field1 = 12;
        SC_InitSide(1, &initside);
        i = 0;
        // Loop header - Block 106 @1272
        for (i = 0; (i < 12); i = i + 1) {
            initgroup = 1;
            initgroup.field1 = i;
            initgroup.field2 = 16;
            initgroup.field3 = 100.0f;
            SC_InitSideGroup(&initgroup);
        }
        initside = 2;
        initside.field1 = 2;
        SC_InitSide(2, &initside);
        initgroup = 2;
        initgroup.field1 = 0;
        initgroup.field2 = 1;
        initgroup.field3 = 100.0f;
        SC_InitSideGroup(&initgroup);
        initgroup = 2;
        initgroup.field1 = 1;
        initgroup.field2 = 20;
        initgroup.field3 = 0;
        SC_InitSideGroup(&initgroup);
        SC_SetSideAlly(0, 2, 1.0f);
        SC_SetSideAlly(1, 2, 1.0f);
        initside = 2;
        initside.field1 = 1;
        SC_InitSide(3, &initside);
        initgroup = 3;
        initgroup.field1 = 0;
        initgroup.field2 = 16;
        initgroup.field3 = 0;
        SC_InitSideGroup(&initgroup);
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
        i = 0;
        // Loop header - Block 109 @1455
        for (i = 0; (i < 4); i = i + 1) {
            t1464_0 = PNT(&local_43[i]);
            SC_ZeroMem(t1464_0, 12);
            local_43[i] = 1.5f;
            local_43[i].field1 = 5.0f;
            local_63[i] = i;
        }
        i = 0;
        // Loop header - Block 112 @1506
        for (i = 0; (i < 10); i = i + 1) {
            SC_Ai_SetPlFollow(1, i, 0, &plfollow, &local_63, &local_63, 4);
        }
        i = 0;
        // Loop header - Block 115 @1532
        for (i = 0; (i < 4); i = i + 1) {
            sprintf(&tmp, "WP_will%d", i + 1);
            SC_GetWp(&tmp, &g_will_pos[i]);
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
        i = SC_ggi(SGI_LEVELPHASE);
        if (g_save[0]) {
        } else {
            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
            if (local_22 && idx) {
                g_save[0] = 1;
                missionsave = 9136;
                missionsave.field1 = 9137;
                SC_MissionSave(&missionsave);
            }
        }
        if (g_music) {
        } else {
            if (gStartMusicTime > 0 && gStartMusicTime <= 0) {
                g_music = 1;
                SC_AGS_Set(0);
            }
        }
        local_0 = 0.5f;
        SC_SpeechRadio2(3400, &local_0);
        local_0 = local_0 + 0.30000001192092896f;
        SC_SpeechRadio2(3401, &local_0);
        local_0 = local_0 + 0.30000001192092896f;
        SC_SpeechRadio2(3402, &local_0);
        local_0 = local_0 + 0.5f;
        SC_SpeechRadio2(3403, &local_0);
        local_0 = local_0 + 0.30000001192092896f;
        SC_SpeechRadio2(3404, &local_0);
        local_0 = local_0 + 0.5f;
        g_dialog = 1;
        SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
        if (local_91 < 1) {
        } else {
            tmp1 = SC_P_GetBySideGroupMember(0, 0, 2);
            local_25 = SC_P_GetBySideGroupMember(0, 0, 5);
            tmp2 = SC_P_GetBySideGroupMember(0, 0, 4);
            local_0 = 3.0f;
            SC_P_Speech2(tmp1, 3420, &local_0);
            local_0 = 3.200000047683716f;
            SC_P_Speech2(local_25, 3421, &local_0);
            g_dialog = 2;
            SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
            if (local_91 < 2) {
            } else {
                local_26 = SC_P_GetBySideGroupMember(0, 2, 1);
                local_0 = 1.0f;
                SC_P_Speech2(local_26, 3422, &local_0);
                local_0 = local_0 + 0.30000001192092896f;
                SC_P_GetBySideGroupMember(0, 0, 0);
                SC_P_Speech2(local_91, 3423, &local_0);
                local_0 = local_0 + 0.4000000059604645f;
                SC_P_Speech2(local_26, 3422, &local_0);
                local_0 = local_0 + 0.30000001192092896f;
                SC_SpeechRadio2(3416, &local_0);
                local_0 = local_0 + 0.5f;
                SC_SpeechRadio2(3417, &local_0);
                local_0 = local_0 + 0.5f;
                SC_SpeechRadio2(3418, &local_0);
                local_0 = local_0 + 0.5f;
                SC_P_Speech2(local_26, 3419, &local_0);
                local_0 = local_0 + 2.0f;
                local_2 = local_0 - 1.2000000476837158f;
                SC_P_GetBySideGroupMember(0, 0, 0);
                SC_P_Speech2(local_91, 3430, &local_2);
                local_2 = local_2 + 1.5f;
                SC_P_Speech2(local_25, 3431, &local_0);
                SC_SpeechRadio2(3424, &local_0);
                local_0 = local_0 + 0.5f;
                SC_SpeechRadio2(3425, &local_0);
                local_0 = local_0 + 0.5f;
                SC_SpeechRadio2(3426, &local_0);
                local_0 = local_0 + 0.5f;
                SC_SpeechRadio2(3427, &local_0);
                local_0 = local_0 + 0.5f;
                SC_SpeechRadio2(3428, &local_0);
                local_0 = local_0 + 0.5f;
                SC_SpeechRadio2(3429, &local_0);
                local_0 = local_0 + 0.5f;
                g_dialog = 3;
                SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
                if (local_91 < 3) {
                } else {
                    local_0 = 0;
                    SC_SpeechRadio2(3440, &local_0);
                    local_0 = local_0 + 0.5f;
                    SC_SpeechRadio2(3441, &local_0);
                    local_0 = local_0 + 0.5f;
                    SC_SpeechRadio2(3442, &local_0);
                    local_0 = local_0 + 0.5f;
                    SC_SpeechRadio2(3443, &local_0);
                    local_0 = local_0 + 0.5f;
                    SC_SpeechRadio2(3444, &local_0);
                    local_0 = local_0 + 0.5f;
                    SC_SpeechRadio2(3445, &local_0);
                    local_0 = local_0 + 0.5f;
                    SC_SpeechRadio2(3446, &local_0);
                    local_0 = local_0 + 0.5f;
                    g_dialog = 4;
                    SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
                    if (local_91 < 4) {
                    } else {
                        g_dialog = 5;
                        local_26 = SC_P_GetBySideGroupMember(0, 2, 1);
                        local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
                        local_0 = 0;
                        SC_P_Speech2(local_26, 3447, &local_0);
                        local_0 = local_0 + 0.30000001192092896f;
                        SC_P_Speech2(local_22, 3448, &local_0);
                        local_0 = local_0 + 0.6000000238418579f;
                        SC_P_Speech2(local_26, 3449, &local_0);
                        local_0 = local_0 + 0.30000001192092896f;
                        local_0 - 1.0f = t2229_0;
                        SC_P_Speech2(local_22, 3450, &local_0);
                        SC_PC_EnableExit(1);
                        g_dialog = 6;
                    }
                }
            }
        }
        if (g_dochange) {
            func_0292();
            func_0355();
            g_dochange = 0;
            if (g_save[1]) {
            } else {
                g_save[1] = 1;
                missionsave = 9138;
                missionsave.field1 = 9139;
                SC_MissionSave(&missionsave);
            }
        }
        func_0612(info->elapsed_time);
        func_0612(info->elapsed_time);
        local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
        if (local_ && local_22) {
            if (SC_P_GetActive(local_)) {
                if (SC_P_IsReady(local_)) {
                    if (SC_P_IsReady(local_22)) {
                        tmp3 = SC_P_GetDistance(local_, local_22);
                        if (tmp3 < 10.0f) {
                            SC_sgi(SGI_LEVELPHASE, 3);
                            local_0 = 0;
                            SC_P_Speech2(local_22, 3451, &local_0);
                            local_0 = local_0 + 1.600000023841858f;
                            SC_P_Speech2(local_, 3452, &local_0);
                            local_0 = local_0 + 0.5f;
                            SC_P_Speech2(local_22, 3453, &local_0);
                            local_0 = t2397_0;
                            objective = 3471;
                            objective.field1 = 2;
                            SC_SetObjectives(1, &objective, 0.0f);
                        }
                    }
                }
            }
        }
        SC_Radio_Enable(20);
        SC_PC_EnableRadioBreak(1);
        SC_sgi(SGI_LEVELPHASE, 4);
        if (gPilotCommTime > 0) {
            gPilotCommTime = gPilotCommTime - info->elapsed_time;
        } else {
            func_0612(info->elapsed_time);
            SC_P_GetPos(local_, &local_11);
            i = 0;
        }
        // Loop header - Block 181 @2472
        for (i = 0; (i < 4); i = i + 1) {
            SC_2VectorsDist(&local_11, &g_will_pos[i]);
            if (local_90 < 40.0f) {
                SC_sgi(SGI_LEVELPHASE, 6);
                SC_sgi(SGI_LEVPILOT_EVACVILLID, i);
                local_11.field2 = local_11.field2 + 1.5f;
                local_17 = g_will_pos[i] - local_11;
                local_17.field1 = (*g_will_pos[i].field1) - local_11.field1;
                local_17.field2 = 0;
                SC_VectorLen(&local_17);
                local_0 = local_90 / 10.0f;
                local_17 = local_17 / local_0;
                local_17.field1 = local_17.field1 / local_0;
                local_17.field2 = 7.0f;
                SC_Item_Create2(147, &local_11, &local_17);
                func_0612(info->elapsed_time);
                i = 2;
                g_final_enter_timer = g_final_enter_timer + info->elapsed_time;
                if (SC_P_IsInHeli(local_)) {
                    i--;
                } else {
                    if (g_final_enter_timer > 30.0f) {
                        SC_P_SetToHeli(local_, "heli2", 3);
                    } else {
                        func_0985(local_);
                        SC_P_Ai_EnterHeli(local_, "heli2", 4);
                        param_0->field_20 = 4.0f;
                    }
                }
                local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
                if (SC_P_IsInHeli(local_22)) {
                    i--;
                }
                if (i == 0) {
                    SC_sgi(SGI_LEVELPHASE, 8);
                    SC_AGS_Set(1);
                    param_0->field_20 = 0.10000000149011612f;
                    gEndTimer = 15.0f;
                }
                gEndTimer = gEndTimer - info->elapsed_time;
                if (gEndTimer < 0) {
                    func_1021();
                    SC_TheEnd();
                    SC_sgi(SGI_LEVELPHASE, 9);
                }
            } else {
                i++;
            }
        }
        break;
    case 1:
        SC_sgi(SGI_LEVELPHASE, 5);
        SC_RadioBatch_Begin();
        local_0 = 0;
        local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
        SC_P_Speech2(local_22, 3454, &local_0);
        local_0 = local_0 + 1.2999999523162842f;
        SC_SpeechRadio2(3455, &local_0);
        local_0 = local_0 + 0.5f;
        SC_P_Speech2(local_22, 3456, &local_0);
        local_0 = local_0 + 0.699999988079071f;
        SC_SpeechRadio2(3461, &local_0);
        local_0 = local_0 + 0.5f;
        SC_P_SpeechMes2(local_22, 3457, &local_0, 11);
        gPilotCommTime = local_0 + 3.0f;
        param_0->field_20 = 0.10000000149011612f;
        SC_RadioBatch_End();
        break;
    case 2:
        SC_message("Break");
        if (gPilotCommTime > 3.0f) {
            gPilotCommTime = 3.0f;
        }
        break;
    case 4:
        func_0994(1);
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
        gStartMusicTime = 0.20000000298023224f;
        break;
    case 11:
        SC_ggi(SGI_LEVPILOT_JUSTLOADEDVALUE);
        SC_sgi(SGI_LEVPILOT_JUSTLOADEDVALUE, idx + 1);
        func_0994(g_trashes_enabled);
        break;
    case 15:
        if (info->param1 >= 20) {
            param_0->field_12 = 0;
        } else {
            info->param2 = music[info->param1];
            param_0->field_12 = 1;
        }
        break;
    default:
    }
    switch (g_showinfo_timer) {
    case 0:
        break;
    case 1:
        // Loop header - Block 181 @2472
        for (i = 0; (i < 4); i = i + 1) {
        }
        break;
    default:
    }
    switch (g_showinfo_timer) {
    case 0:
        break;
    case 1:
        break;
    case 2:
        break;
    case 3:
        break;
    case 4:
        break;
    case 5:
        // Loop header - Block 181 @2472
        for (i = 0; (i < 4); i = i + 1) {
        }
        break;
    case 6:
        break;
    case 7:
        break;
    case 8:
        break;
    default:
    }
    switch (g_showinfo_timer) {
    case 0:
        break;
    case 1:
        break;
    case 2:
        break;
    case 3:
        break;
    case 4:
        break;
    case 5:
        break;
    default:
        // Loop header - Block 181 @2472
        for (i = 0; (i < 4); i = i + 1) {
        }
    }
    if (!(local_88 == 20)) {
    }
    if (!(local_88 == 11)) {
    }
    switch (g_showinfo_timer) {
    case 10:
        break;
    case 667:
        break;
    default:
    }
    return;
}

