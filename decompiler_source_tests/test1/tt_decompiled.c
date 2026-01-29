// Structured decompilation of decompiler_source_tests\test1\tt.scr
// Functions: 15

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
int gSteps = 0;
dword gRecs[2][6];
dword gVar = 0;
dword gVar1 = 0;
s_SC_MP_Recover gRec[2][6][32];
dword gVar2 = 0;
dword gRecTimer[2][6][32] = {0};
s_sphere gStepSwitch[6] = {0};
int gEndRule = 0;
int gEndValue = 0;
float gTime = 0.0f;
dword gSidePoints[2] = {0};
dword gCLN_SidePoints[2] = {0};
int gCLN_gamephase = 0;
int gMainPhase = 0;
int gAttackingSide = 0;
int gCurStep = 0;
int gMission_phase = 0;
float gNoActiveTime = 0.0f;
float gPhaseTimer = 0.0f;
float gMissionTime_update = 10.0f;
float gMissionTime = 0.0f;
float gMissionTimePrev = 0.0f;
float gMissionTimeToBeat = 0.0f;
int gCLN_MissionTimePrevID = 0;
float gCLN_MissionTime = 0.0f;
int gCLN_CurStep = 0;
float gCLN_ShowInfo = 0.0f;
float gCLN_ShowStartInfo = 0.0f;
float gCLN_ShowWaitingInfo = 0.0f;
float gMission_starting_timer = 0.0f;
float gMission_afterstart_time = 0.0f;
float gNextRecover = 0.0f;
dword gFlagNod[6][3] = {0};
c_Vector3 gFlagPos[6] = {0};
dword gRespawn_id[2][6] = {0};
dword g_FPV_UsFlag = 0;
dword g_FPV_VcFlag = 0;
dword g_FPV_NeFlag = 0;

int _init(s_SC_NET_info *info) {
    return;
}

int func_0050(float param_0) {
    switch (gEndRule) {
    case SC_MP_ENDRULE_TIME:
        if (gMission_phase > 0) {
            gTime += param_0;
        }
        break;
    case SC_MP_ENDRULE_POINTS:
        if (gSidePoints[0] >= gEndValue || gSidePoints[1] >= gEndValue) {
            SC_MP_LoadNextMap();
            return TRUE;
        }
        break;
    }
    SC_MP_EndRule_SetTimeLeft(gTime, gMission_phase);
    if (gTime > ((float)gEndValue)) {
        SC_MP_LoadNextMap();
        return TRUE;
    }
    goto block_20;
block_20:
    return FALSE;
}

int func_0119(void) {
    s_SC_MP_SRV_AtgSettings atg_settings;
    float local_0;
    int n;

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
    int n;

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
    int n;

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

void func_0264(int param_0, float param_1) {
    gMissionTime_update -= param_0;
    if (gMissionTime_update < 0.0f) {
        gMissionTime_update = 10.0f;
        SC_sgf(504, gMissionTime);
        SC_sgi(505, SC_ggi(505) + 1);
    }
    return;
}

void func_0294(void) {
    int n;

    gCurStep = gSteps - 1;
    SC_sgi(507, gCurStep);
    if ((gMainPhase % 2) != 0) {
        gMissionTime = gMissionTimeToBeat;
    } else {
        gMissionTime = func_0213();
        gMissionTimePrev = gMissionTime;
    }
    gMissionTime_update = -1.0f;
    func_0264(0);
    return;
}

int func_0334(int param_0) {
    if ((param_0 % 4) != 0) {
        if ((param_0 % 4) != 3) {
            return TRUE;
        }
    } else {
    }
    return FALSE;
}

void func_0355(void) {
    int n;

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
        break;
    }
    goto block_61;
block_61:
block_67:
    gMainPhase++;
block_68:
    SC_sgi(502, gMainPhase);
    func_0334(gMainPhase);
    gAttackingSide = gMainPhase;
    SC_sgi(507, 6);
    return;
}

int func_0498(int param_0, int param_1) {
    s_SC_FpvMapSign local_5[4];
    int idx;
    int local_2;
    int local_41;
    int n;

    local_4 = 0;
    local_3 = 0;
block_74:
block_77:
block_80:
block_91:
block_96:
    SC_DUMMY_Set_DoNotRenHier2(t617_, 1);
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0752(int param_0, int param_1) {
    int idx;
    int n;
    s_SC_P_getinfo player_info;

    switch (local_2.field_8) {
    case 0:
        if (local_0 > 0) {
        } else {
        }
        break;
    case 1:
        if (local_0 < 0) {
        } else {
            return;
        }
        break;
    }
block_115:
    return;
}

int func_0852(void) {
    s_SC_MP_EnumPlayers enum_pl;
    int idx;
    int k;
    int local_2;
    int local_265;
    int local_266;
    int m;

    if (! SC_MP_SRV_GetAutoTeamBalance()) {
        return;
    }
    local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
    if (/* condition */) {
        return;
    }
    if (local_0 <= 0) {
        local_1 = 1;
        local_2 = tmp6 / 2;
    } else {
        local_1 = 0;
        local_2 = local_0 / 2;
    }
    local_265 = 64;
    t921_ret = SC_MP_EnumPlayers(&enum_pl, &local_265, ptr);
block_156:
    t1006_ret = SC_MP_SRV_P_SetSideClass(t994_, 1 - ptr, 1 + 20 * ((1 - ptr)));
    local_8[ptr5].id = 0;
    local_2 = ptr1 - 1;
block_157:
    return;
}

int func_1028(void) {
    s_SC_MP_EnumPlayers enum_pl;
    int idx;
    int local_257;
    int local_258;
    int local_260;

    t1037_ret = SC_ggi(502);
    func_0334(t1037_ret);
    local_257 = 1 - t1037_ret;
    local_258 = 64;
    t1057_ret = SC_MP_EnumPlayers(&enum_pl, &local_258, ptr);
block_159:
    local_256 = 0;
    for (local_256 = 0; local_256 < ptr1; local_256++) {
        if (side2 != 2) {
            SC_MP_RecoverPlayer(t1084_);
        } else {
            local_256 = obj + 1;
        }
    }
block_164:
    return;
}

int ScriptMain(s_SC_NET_info *info) {
    s_SC_MP_EnumPlayers enum_pl[32];
    s_SC_HUD_MP_icon icon[32];
    char local_0[32];
    s_SC_MP_hud hudinfo;
    int i;
    int j;
    int k;
    int local_12;
    int local_13;
    int local_294;
    void* local_295;
    int local_296;
    int local_298;
    ushort* local_314;
    int local_315;
    int local_379;
    float local_411;
    float local_412;
    int local_418;
    int local_419;
    int local_420;
    float local_421;
    int local_8;
    int m;
    int n;
    s_SC_P_getinfo player_info;
    s_SC_MP_SRV_settings srv_settings;
    char* t2998_ret;
    ushort* t3021_ret;
    ushort* t3085_ret;
    ushort* t3121_ret;
    char* t3163_ret;
    ushort* t3231_ret;
    char* t3275_ret;
    ushort* t3326_ret;
    s_SC_MP_Recover t3600_0;
    c_Vector3 vec;

    switch (info->message) {
    case 3:
        func_0050(info->elapsed_time);
        switch (info->elapsed_time) {
        case 0:
            gNoActiveTime += info->elapsed_time;
            if (gMissionTime > -10.0f) {
                gMissionTime = -10.0f;
                gMissionTime_update = -1.0f;
                func_0264(0);
            }
            break;
        case 1:
            gMission_afterstart_time += info->elapsed_time;
            gMissionTime -= info->elapsed_time;
            func_0264(info->elapsed_time);
            switch (info->elapsed_time) {
            case 0:
                if (side6 == 1) {
                } else {
                    local_8 = obj + 1;
                }
                break;
            case 1:
                SC_P_GetPos(t1547_, &vec);
                // Loop header - Block 221 @1557
                for (local_9 = gCurStep - 1; local_9 < gCurStep; local_9++) {
                    if (SC_IsNear3D( & vec, & gStepSwitch[ptr29], t1574_)) {
                        if (ptr29) {
                            gCurStep = ptr29;
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
                        local_9 = ptr29 + 1;
                    }
                }
                break;
            }
            break;
        case 3:
            break;
        case 2:
            gPhaseTimer -= info->elapsed_time;
            if (gPhaseTimer < 0.0f) {
                gNoActiveTime = 0;
                gMission_phase = 0;
                SC_sgi(503, gMission_phase);
                func_0852();
                SC_MP_SetInstantRecovery(1);
                SC_MP_RecoverAllNoAiPlayers();
            }
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
                local_299[ptr46].z = 0;
                break;
            }
            break;
        case 1:
            if (gCLN_CurStep != SC_ggi(507) && gCLN_CurStep < idx && gCLN_CurStep > 0) {
                gCLN_ShowInfo = 5.0f;
                SC_SND_PlaySound2D(10425);
            }
            t1823_ret = SC_ggi(502);
            func_0334(t1823_ret);
            func_0498(t1823_ret, gCLN_CurStep);
            break;
        }
        break;
    case 9:
        SC_sgi(GVAR_MP_MISSIONTYPE, 9);
        gEndRule = param_0->field_4;
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
        for (local_8 = 0; local_8 < 6; local_8++) {
            SC_MP_SRV_SetClassLimit(obj + 1, t2149_);
            SC_MP_SRV_SetClassLimit(obj + 21, t2161_);
            local_8 = obj + 1;
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
                if (obj) {
                    SC_P_GetInfo(obj, &player_info);
                    t2933_ret = SC_ggi(502);
                    func_0334(t2933_ret);
                    if (local_413.field_8 == t2933_ret) {
                        local_314 = SC_Wtxt(5108);
                    } else {
                        local_314 = SC_Wtxt(5109);
                    }
                    SC_GameInfoW(ptr51);
                    local_314 = 0;
                }
            } else {
                if (gCLN_ShowInfo > 0.0f && gCLN_CurStep > 0) {
                    t2982_ret = SC_ggi(510);
                    local_9 = SC_MP_GetPlofHandle(t2982_ret);
                    if (ptr29) {
                        t2998_ret = SC_P_GetName(ptr29);
                        t3003_ret = SC_AnsiToUni(t2998_ret, &local_379);
                    } else {
                        t3012_ret = SC_AnsiToUni("'disconnected'", &local_379);
                    }
                    t3021_ret = SC_Wtxt(5107);
                    t3028_ret = swprintf(&local_315, t3021_ret, &local_379, gCLN_CurStep);
                    local_314 = &local_315;
                }
                local_8 = SC_PC_Get();
                if (obj) {
                    SC_P_GetInfo(obj, &player_info);
                    t3057_ret = SC_ggi(502);
                    func_0334(t3057_ret);
                    if (local_413.field_8 == t3057_ret) {
                        if (gCLN_CurStep == 1) {
                            local_314 = SC_Wtxt(5111);
                        } else {
                            t3085_ret = SC_Wtxt(5110);
                            t3093_ret = swprintf(&local_315, t3085_ret, gCLN_CurStep - 1);
                            local_314 = &local_315;
                        }
                    } else {
                        if (gCLN_CurStep == 1) {
                            local_314 = SC_Wtxt(5113);
                        } else {
                            t3121_ret = SC_Wtxt(5112);
                            t3129_ret = swprintf(&local_315, t3121_ret, gCLN_CurStep - 1);
                            local_314 = &local_315;
                        }
                    }
                }
            }
            break;
        default:
            break;
        }
        break;
    case 5:
        switch (info->param2) {
        case 1:
            // Loop header - Block 410 @3415
            for (local_8 = 0; local_8 < abl_lists; local_8++) {
                if ((param_0- > field_4) == tmp430) {
                    abl_lists--;
                    abl_list[obj] = tmp435;
                } else {
                    local_8 = obj + 1;
                }
            }
            if (obj < abl_lists) {
                param_0->fval1 = 0.1f;
            } else {
                if (gNextRecover > local_421) {
                    param_0->fval1 = gNextRecover;
                } else {
                    func_0119(gNextRecover);
                    param_0->fval1 = gNextRecover + local_421;
                }
            }
            break;
        case 0:
            param_0->fval1 = 3.0f;
            break;
        default:
            param_0->fval1 = -1.0f;
            break;
        }
        break;
    case 6:
        local_13 = info->param2;
        local_9 = param_0->field_4;
        if (gAttackingSide) {
            local_9 = 1 - ptr29;
        }
        if (ptr29) {
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
        local_8 = SC_MP_SRV_GetBestDMrecov(t3600_0, t3610_, &gRecTimer[768] + ptr40 * 128, 3.0f);
        gRecTimer[768] + ptr40 * 128 + obj * 4 = 3.0f;
        ptr56 = tmp492;
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
        gEndRule = param_0->field_4;
        gEndValue = info->param2;
        gTime = 0;
        break;
    case 7:
        func_0752(param_0->field_4);
        break;
    default:
        // Loop header - Block 176 @1195
        for (local_8 = 0; local_8 < ptr; local_8++) {
            if (side2 != 0 && tmp22 < 2) {
                (&local_296) + tmp26 * 4 = 1;
            }
        }
        gMission_starting_timer -= info->elapsed_time;
        if (tmp35 && tmp37) {
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

