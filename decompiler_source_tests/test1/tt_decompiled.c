// Structured decompilation of tt.scr
// Functions: 15

#include <inc\sc_global.h>
#include <inc\sc_def.h>

int func_0050(float param_0, int param_1) {
    switch (gEndRule) {
    case SC_MP_ENDRULE_TIME:
        if (gMission_phase > 0) {
            gTime += param_0;
        }
        if (gTime <= ((float)gEndValue)) break;
        SC_MP_LoadNextMap();
        return TRUE;
        break;
    case SC_MP_ENDRULE_POINTS:
        if (gSidePoints[0] >= gEndValue || gSidePoints[1] >= gEndValue) {
            SC_MP_LoadNextMap();
            return TRUE;
        }
        break;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0119(void) {
    s_SC_MP_SRV_AtgSettings atg_settings;
    float local_0;

    SC_MP_SRV_GetAtgSettings(&atg_settings);
    if (atg_settings.tt_respawntime <= 1.0f) {
        local_0 = SC_ggf(400);
        if (local_0 == 0.0f) {
            local_0 = 30.0f;
        }
        return local_0;
    } else {
        return atg_settings.tt_respawntime;
    }
}

int func_0155(int param_0) {
    s_SC_MP_SRV_AtgSettings atg_settings;
    float local_0;

    SC_MP_SRV_GetAtgSettings(&atg_settings);
    if (atg_settings.tt_respawntime <= 1.0f) {
        local_0 = SC_ggf(401);
        if (local_0 == 0.0f) {
            local_0 = 10.0f;
        }
        return local_0;
    } else {
        local_0 = atg_settings.tt_respawntime / 3.0f;
        if (local_0 < 5.0f) {
            local_0 = 5.0f;
        }
        if (local_0 > 10.0f) {
            local_0 = 10.0f;
        }
        return local_0;
    }
}

int func_0213(void) {
    s_SC_MP_SRV_AtgSettings atg_settings;
    float local_0;

    SC_MP_SRV_GetAtgSettings(&atg_settings);
    if (atg_settings.tt_timelimit <= 59.0f) {
        local_0 = SC_ggf(402);
        if (local_0 == 0.0f) {
            local_0 = 480.0f;
        }
        return local_0;
    } else {
        return atg_settings.tt_timelimit;
    }
}

void func_0249(void) {
    SC_sgi(500, gSidePoints[0]);
    SC_sgi(501, gSidePoints[1]);
    return;
}

void func_0264(float param_0) {
    gMissionTime_update -= param_0;
    if (gMissionTime_update < 0.0f) {
        gMissionTime_update = 10.0f;
        SC_sgf(504, gMissionTime);
        SC_sgi(505, SC_ggi(505) + 1);
    }
    return;
}

void func_0294(void) {
    gCurStep = gSteps - 1;
    SC_sgi(507, gCurStep);
    if ((gMainPhase % 2) != 0) {
        gMissionTime = gMissionTimeToBeat;
    } else {
        gMissionTime = t312_ret;
        gMissionTimePrev = gMissionTime;
    }
    gMissionTime_update = -1.0f;
    func_0264(0);
    return;
}

int func_0334(int param_0, int param_1) {
    if ((param_0 % 4) != 0) {
        if ((param_0 % 4) != 3) {
            return TRUE;
        }
    } else {
    }
    return FALSE;
}

void func_0355(void) {
    switch (gMission_phase) {
    case MISSION_PHASE_WIN_DEFENDERS:
        gSidePoints[(1 - gAttackingSide)]++;
        func_0249();
        SC_sgi(506, 1 - gAttackingSide);
        SC_sgi(509, 1 - gAttackingSide);
        if (gMainPhase % 2) {
            gMainPhase++;
        } else {
            gMainPhase += 2;
        }
        break;
    case MISSION_PHASE_WIN_ATTACKERS:
        SC_sgi(509, gAttackingSide);
        if (gMainPhase % 2) {
            gSidePoints[gAttackingSide]++;
            func_0249();
            SC_sgi(506, gAttackingSide);
        } else {
            gMissionTimeToBeat = gMissionTimePrev - gMissionTime;
        }
        gMainPhase++;
        break;
    }
    return;
}

void func_0498(int param_0, int param_1) {
    s_SC_FpvMapSign local_5[4];
    int local_2;
    dword local_4;

    local_4 = 0;
    local_3 = 0;
    for (i = 0; i < 6; i++) {
        local_0 = 0;
        local_1 = 0;
        local_2 = 0;
        if ((i + 1) != param_1) {
            if (i < param_1) {
                local_2 = 1;
            }
        } else {
            switch (g_FPV_UsFlag) {
            case 0:
                local_1 = 1;
                break;
            case 1:
                local_0 = 1;
                break;
            case 2:
                local_2 = 1;
                break;
            }
        }
        if (tmp10) {
            if (! t592_) {
            } else {
            }
            SC_DUMMY_Set_DoNotRenHier2(t592_, 1);
        }
        if (tmp17) {
            if (! local_1) {
            } else {
            }
            SC_DUMMY_Set_DoNotRenHier2(t617_, 1);
        }
        if (tmp24) {
            if (! local_2) {
            } else {
            }
            SC_DUMMY_Set_DoNotRenHier2(t642_, 1);
        }
        local_5[0].id = 0;
        if (! local_0) {
            if (! local_1) {
                if (local_2) {
                    local_5[g_FPV_NeFlag].id = g_FPV_NeFlag;
                }
            } else {
                local_5[g_FPV_VcFlag].id = g_FPV_VcFlag;
            }
        } else {
            local_5[g_FPV_UsFlag].id = g_FPV_UsFlag;
        }
        if (tmp42) {
            local_5[-1].y = -1;
            local_5[t712_].field_12 = t712_;
            local_5[1065353216].z = 1.0f;
            local_4++;
        }
        local_3 = i + 1;
    }
    SC_MP_FpvMapSign_Set(local_4, &local_5);
    return;
}

void func_0752(int param_0) {
    dword local_1;
    s_SC_P_getinfo player_info;

    switch (player_info.field_8) {
    case 0:
        if (local_0 <= 0) {
        }
        local_1 = 1;
        break;
    case 1:
        if (local_0 >= 0) {
            return;
        }
        local_1 = 0;
        break;
    }
    return;
}

void func_0852(void) {
    s_SC_MP_EnumPlayers enum_pl;
    dword local_1;
    int local_2;
    int local_265;
    int local_266;

    if (! SC_MP_SRV_GetAutoTeamBalance()) {
        return;
    }
    local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
    if (/* condition */) {
        return;
    }
    if (local_0 <= 0) {
        local_1 = 1;
        local_2 = tmp7 / 2;
    } else {
        local_1 = 0;
        local_2 = local_0 / 2;
    }
    local_265 = 64;
    t921_ret = SC_MP_EnumPlayers(&enum_pl, &local_265, local_1);
    local_266 = rand() % local_265;
    local_264 = local_266;
    local_264 = j + 1;
    local_264 = 0;
    t1006_ret = SC_MP_SRV_P_SetSideClass(t994_, 1 - local_1, 1 + 20 * ((1 - local_1)));
    local_8[j].id = 0;
    local_2 = i - 1;
}

void func_1028(void) {
    s_SC_MP_EnumPlayers enum_pl;
    int input_158_unknown_158_1044_1;
    dword local_257;
    int local_258;

    local_257 = input_158_unknown_158_1044_1 - t1041_ret;
    local_258 = 64;
    t1057_ret = SC_MP_EnumPlayers(&enum_pl, &local_258, local_257);
    if (SC_MP_EnumPlayers( & enum_pl, & local_258, local_257)) {
        local_256 = 0;
        for (i = 0; i < local_258; i++) {
            if (side2 == 2) {
                SC_MP_RecoverPlayer(t1084_);
            }
            local_256 = i + 1;
        }
    }
    return;
}

int ScriptMain(s_SC_NET_info *info) {
    dword idx;
    int input_342_unknown_342_2940_1;
    int input_355_unknown_355_3064_1;
    dword j;
    dword local_11;
    int local_12;
    int local_13;
    int local_296;
    int local_298;
    ushort* local_314;
    int local_315;
    int local_379;
    int local_8;
    s_SC_P_getinfo player_info;
    s_SC_MP_SRV_settings srv_settings;
    char* t2998_ret;
    ushort* t3021_ret;
    ushort* t3085_ret;
    ushort* t3121_ret;
    s_SC_MP_Recover t3600_0;
    c_Vector3 vec;

    switch (info->message) {
    case 3:
        switch (gMission_phase) {
        case MISSION_PHASE_NOACTIVE:
            if (gMissionTime <= -10.0f) break;
            gMissionTime = -10.0f;
            gMissionTime_update = -1.0f;
            func_0264(0);
            break;
        case MISSION_PHASE_INGAME:
            gMission_afterstart_time += info->elapsed_time;
            gMissionTime -= info->elapsed_time;
            func_0264(info->elapsed_time);
            switch (info->elapsed_time) {
            case 0:
                if (side6 != 1) {
                    local_8 = j + 1;
                }
                break;
            case 1:
                SC_P_GetPos(t1547_, &vec);
                for (idx = gCurStep - 1; idx < gCurStep; idx++) {
                    if (SC_IsNear3D( & vec, & gStepSwitch[idx], t1574_)) {
                        if (idx) {
                            gCurStep = idx;
                            t1595_ret = SC_MP_GetHandleofPl(t1593_);
                            SC_sgi(510, SC_MP_GetHandleofPl(t1593_));
                            SC_sgi(507, gCurStep);
                            func_1028();
                            SC_P_MP_AddPoints(t1610_, 1);
                        } else {
                            gMission_phase = 2;
                            t1628_ret = SC_MP_GetHandleofPl(t1626_);
                            SC_sgi(510, SC_MP_GetHandleofPl(t1626_));
                            SC_sgi(503, gMission_phase);
                            gPhaseTimer = 8.0f;
                            func_0355();
                            SC_P_MP_AddPoints(t1647_, 2);
                        }
                    } else {
                        local_9 = idx + 1;
                    }
                }
                break;
            }
            break;
        case MISSION_PHASE_WIN_DEFENDERS:
            break;
        case MISSION_PHASE_WIN_ATTACKERS:
            if (gPhaseTimer >= 0.0f) break;
            gNoActiveTime = 0;
            gMission_phase = 0;
            SC_sgi(503, gMission_phase);
            func_0852();
            SC_MP_SetInstantRecovery(1);
            SC_MP_RecoverAllNoAiPlayers();
            break;
        }
        break;
    case 4:
        gCLN_ShowInfo -= info->elapsed_time;
        switch (gCLN_ShowWaitingInfo) {
        case 0:
            func_0498(SC_ggi(508) - 1, 2);
            switch (SC_ggi(503)) {
            case 1:
                gCLN_MissionTime -= info->elapsed_time;
                break;
            case 3:
                local_299[local_11].z = 0;
                break;
            }
            break;
        case 1:
            if (gCLN_CurStep != SC_ggi(507) && gCLN_CurStep < idx34 && gCLN_CurStep > 0) {
                gCLN_ShowInfo = 5.0f;
                SC_SND_PlaySound2D(10425);
            }
            func_0498(t1827_ret, gCLN_CurStep);
            break;
        }
        break;
    case 9:
        SC_sgi(GVAR_MP_MISSIONTYPE, 9);
        gEndRule = info->field_4;
        gEndValue = info->param2;
        gTime = 0;
        SC_MP_EnableBotsFromScene(0);
        break;
    case 0:
        if ((gSidePoints[0] + gSidePoints[1]) != 0) {
            gSidePoints[0] = 0;
            gSidePoints[1] = 0;
            func_0249();
        }
        break;
    case 1:
        g_FPV_UsFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_USflag.BES");
        g_FPV_VcFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_VCflag.BES");
        g_FPV_NeFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_emptyflag.BES");
        SC_MP_SRV_SetForceSide(-1);
        SC_MP_SetChooseValidSides(3);
        SC_MP_SRV_SetClassLimit(18, 0);
        SC_MP_SRV_SetClassLimit(19, 0);
        SC_MP_SRV_SetClassLimit(39, 0);
        SC_MP_GetSRVsettings(&srv_settings);
        local_8 = 0;
        for (j = 0; j < 6; j++) {
            SC_MP_SRV_SetClassLimit(j + 1, t2149_);
            SC_MP_SRV_SetClassLimit(j + 21, t2161_);
            local_8 = j + 1;
        }
        break;
    case 2:
        local_8 = 0;
        local_314 = 0;
        local_298 = 0;
        local_10 = SC_ggi(502);
        switch (gCLN_gamephase) {
        case 2:
            break;
        case 0:
            if (gCLN_ShowWaitingInfo <= 0.0f) {
                local_314 = SC_Wtxt(1076);  // 1076: "Waiting for more players.";
            }
            gCLN_ShowStartInfo = 0;
            break;
        case 3:
            if (SC_ggi(509) == 0) {
                SC_SND_PlaySound2D(11117);
            } else {
                SC_SND_PlaySound2D(11116);
            }
            break;
        case 1:
            gCLN_ShowWaitingInfo = 3.0f;
            if (gCLN_ShowStartInfo == 0.0f) {
                gCLN_ShowStartInfo = 3.0f;
            }
            if (gCLN_ShowStartInfo > 0.0f) {
                local_8 = SC_PC_Get();
                if (j) {
                    SC_P_GetInfo(j, &player_info);
                    if (input_342_unknown_342_2940_1 == t2937_ret) {
                        local_314 = SC_Wtxt(5108);  // 5108: "Capture the flags one by one!";
                    } else {
                        local_314 = SC_Wtxt(5109);  // 5109: "Defend the flags! If the attackers seize one, defend the next!";
                    }
                    SC_GameInfoW(local_314);
                    local_314 = 0;
                }
            } else {
                if (gCLN_ShowInfo > 0.0f && gCLN_CurStep > 0) {
                    t2982_ret = SC_ggi(510);
                    local_9 = SC_MP_GetPlofHandle(t2982_ret);
                    if (idx) {
                        t2998_ret = SC_P_GetName(idx);
                        t3003_ret = SC_AnsiToUni(t2998_ret, &local_379);
                    } else {
                        t3012_ret = SC_AnsiToUni("'disconnected'", &local_379);
                    }
                    t3021_ret = SC_Wtxt(5107);  // 5107: "Attacker %s captured the flag %d."
                    t3028_ret = swprintf(&local_315, t3021_ret, &local_379, gCLN_CurStep);
                    local_314 = &local_315;
                }
                if (! j) break;
                SC_P_GetInfo(j, &player_info);
                if (input_355_unknown_355_3064_1 == t3061_ret) {
                    if (gCLN_CurStep == 1) {
                        local_314 = SC_Wtxt(5111);  // 5111: "Capture the last flag!";
                    } else {
                        t3085_ret = SC_Wtxt(5110);  // 5110: "Capture flag %d !"
                        t3093_ret = swprintf(&local_315, t3085_ret, gCLN_CurStep - 1);
                        local_314 = &local_315;
                    }
                } else {
                    if (gCLN_CurStep == 1) {
                        local_314 = SC_Wtxt(5113);  // 5113: "Defend the last flag!";
                    } else {
                        t3121_ret = SC_Wtxt(5112);  // 5112: "Defend flag %d !"
                        t3129_ret = swprintf(&local_315, t3121_ret, gCLN_CurStep - 1);
                        local_314 = &local_315;
                    }
                }
            }
            break;
        default:
            break;
        }
        break;
    case 5:
        switch (gMission_phase) {
        case MISSION_PHASE_INGAME:
            for (j = 0; j < abl_lists; j++) {
                if (info->field_4 == tmp441) {
                    abl_lists--;
                    abl_list[j] = tmp446;
                } else {
                    local_8 = j + 1;
                }
            }
            if (j < abl_lists) {
                info->fval1 = 0.1f;
            } else {
                if (gNextRecover > t3474_ret) {
                    info->fval1 = gNextRecover;
                } else {
                    info->fval1 = gNextRecover + t3487_ret;
                }
            }
            break;
        case MISSION_PHASE_NOACTIVE:
            info->fval1 = 3.0f;
            break;
        default:
            info->fval1 = -1.0f;
            break;
        }
        break;
    case 6:
        local_13 = info->param2;
        local_9 = info->field_4;
        if (gAttackingSide) {
            local_9 = 1 - idx;
        }
        if (idx) {
            if (gMission_phase == 1) {
                if (gCurStep < 2) {
                    local_10 = 0;
                } else {
                    local_10 = gCurStep - 1 - rand() % 2;
                }
            } else {
                local_10 = 0;
            }
        } else {
            if (gMission_phase == 1) {
                local_10 = gCurStep;
            } else {
                local_10 = gSteps - 1;
            }
        }
        local_8 = SC_MP_SRV_GetBestDMrecov(t3600_0, t3610_, &gRecTimer[768] + idx29 * 128, 3.0f);
        gRecTimer[768] + idx29 * 128 + j * 4 = 3.0f;
        tmp470 = tmp506;
        break;
    case 10:
        gTime = 0;
        SC_ZeroMem(&gSidePoints, 8);
        func_0249();
        SC_MP_SetInstantRecovery(1);
        if (gMission_phase != 0) {
            SC_MP_RestartMission();
            SC_MP_RecoverAllNoAiPlayers();
            gMission_phase = 0;
            SC_sgi(503, gMission_phase);
        }
        gCLN_ShowInfo = 0;
        SC_MP_SRV_ClearPlsStats();
        break;
    case 11:
        gEndRule = info->field_4;
        gEndValue = info->param2;
        gTime = 0;
        break;
    case 7:
        func_0752(info->field_4);
        break;
    default:
        for (j = 0; j < local_12; j++) {
            if (side2 != 0 && tmp24 < 2) {
                (&local_296) + tmp28 * 4 = 1;
            }
        }
        gMission_starting_timer -= info->elapsed_time;
        if (tmp37 && tmp39) {
            SC_MP_SetInstantRecovery(0);
            if (gMission_phase == 0) {
                gMission_phase = 1;
                gMission_afterstart_time = 0;
                SC_sgi(503, gMission_phase);
                func_0294();
                SC_MP_SRV_InitGameAfterInactive();
                if (gNoActiveTime > 6.0f) {
                    SC_MP_RestartMission();
                    SC_MP_RecoverAllNoAiPlayers();
                }
            }
            gMission_starting_timer = 8.0f;
        }
        if (gMission_starting_timer <= 0.0f && gMission_phase > 0) {
            gMission_phase = 0;
            gMission_afterstart_time = 0;
            SC_sgi(503, gMission_phase);
            func_0852();
            func_0294();
        }
        break;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

