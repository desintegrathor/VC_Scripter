// Structured decompilation of decompiler_source_tests/test1/tt.scr
// Functions: 20

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
int gSteps = 0;
dword gRecs[12];
dword gRec[1536];
dword gVar = 0;
dword gVar1 = 0;
dword gVar2 = 0;
dword gVar8 = 0;
dword gVar9 = 0;
dword gVar3 = 0;
dword gVar4 = 0;
dword gVar6 = 0;
dword gVar5 = 0;
dword gVar10 = 0;
dword gVar7 = 0;
dword gVar11 = 0;
dword gRecTimer[384] = {0};
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
dword gFlagNod[18] = {0};
c_Vector3 gFlagPos[6] = {0};
dword gRespawn_id[12] = {0};
dword g_FPV_UsFlag = 0;
dword g_FPV_VcFlag = 0;
dword g_FPV_NeFlag = 0;

void _init(s_SC_NET_info *info) {
    int n;
    int side;
    int sideB;

    return;
}

int func_0050(float param_0) {
    int data_;
    int data_1959;
    int n;

    switch (gEndRule) {
    case 0:
        if (gMission_phase > 0) {
            gTime += param_0;
        }
        SC_MP_EndRule_SetTimeLeft(gTime, gMission_phase);
        if (gTime > ((float)gEndValue)) {
            SC_MP_LoadNextMap();
            return TRUE;
        }
        return FALSE;
    case 2:
        if (gSidePoints[0] >= gEndValue || gSidePoints[1] >= gEndValue) {
            SC_MP_LoadNextMap();
            return TRUE;
        }
        break;
    default:
        SC_message("EndRule unsopported: %d", gEndRule);
        break;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

float func_0119(void) {
    float t138_ret;
    int local_0;
    int n;
    s_SC_MP_SRV_AtgSettings atg_settings;

    SC_MP_SRV_GetAtgSettings(&atg_settings);
    if (atg_settings.tt_respawntime > 1.0f) {
        return atg_settings.tt_respawntime;
    } else {
        t138_ret = SC_ggf(400);
        local_0 = SC_ggf(400);
        if (local_0 == 0.0f) {
            local_0 = 30.0f;
        }
        return local_0;
    }
    return 0.0f;  // FIX (06-05): Synthesized return value
}

int func_0155(int param_0) {
    float t196_ret;
    int local_0;
    int n;
    s_SC_MP_SRV_AtgSettings atg_settings;

    SC_MP_SRV_GetAtgSettings(&atg_settings);
    if (atg_settings.tt_respawntime > 1.0f) {
        local_0 = atg_settings.tt_respawntime / 3.0f;
        if (local_0 < 5.0f) {
            local_0 = 5.0f;
        }
        if (local_0 > 10.0f) {
            local_0 = 10.0f;
        }
        return local_0;
    } else {
        t196_ret = SC_ggf(401);
        local_0 = SC_ggf(401);
        if (local_0 == 0.0f) {
            local_0 = 10.0f;
        }
        return local_0;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

float func_0213(void) {
    float t232_ret;
    int local_0;
    int n;
    int side;
    int side2;
    int side3;
    int side4;
    int sideB;
    s_SC_MP_SRV_AtgSettings atg_settings;

    SC_MP_SRV_GetAtgSettings(&atg_settings);
    if (atg_settings.tt_timelimit > 59.0f) {
        return atg_settings.tt_timelimit;
    } else {
        t232_ret = SC_ggf(402);
        local_0 = SC_ggf(402);
        if (local_0 == 0.0f) {
            local_0 = 480.0f;
        }
        return local_0;
    }
    return 0.0f;  // FIX (06-05): Synthesized return value
}

void func_0249(void) {
    SC_sgi(GVAR_SIDE0FRAGS, gSidePoints[0]);
    SC_sgi(GVAR_SIDE1FRAGS, gSidePoints[1]);
    return;
}

void func_0264(int param_0, float param_1) {
    int t286_ret;  // Auto-generated

    int data_;

    gMissionTime_update -= param_0;
    if (gMissionTime_update < 0.0f) {
        gMissionTime_update = 10.0f;
        SC_sgf(504, gMissionTime);
        t286_ret = SC_ggi(505);
        SC_sgi(505, SC_ggi(505) + 1);
    }
    return;
}

void func_0294(void) {
    int data_;
    int n;

    gCurStep = gSteps - 1;
    SC_sgi(507, gCurStep);
    if ((gMainPhase % 2) == 0) {
        gMissionTime = func_0213();
        gMissionTimePrev = gMissionTime;
    } else {
        gMissionTime = gMissionTimeToBeat;
    }
    gMissionTime_update = -1.0f;
    func_0264(0);
    return;
}

int func_0334(int param_0) {
    int n;

    switch (param_0%4) {
    case 0:
        break;
    case 3:
        return FALSE;
    default:
        return TRUE;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

void func_0355(void) {
    int data_;
    int data_1965;
    int data_1965_v1;
    int data_1965_v2;
    int n;
    int tmp27;
    int tmp9;

    switch (gMission_phase) {
    case 2:
        SC_sgi(509, gAttackingSide);
        if ((gMainPhase % 2)) {
            gSidePoints[gAttackingSide] = tmp27 + 1;
            func_0249();
            SC_sgi(506, gAttackingSide);
        } else {
            gMissionTimeToBeat = gMissionTimePrev - gMissionTime;
        }
        break;
    case 3:
        gSidePoints[(1 - gAttackingSide)] = tmp9 + 1;
        func_0249();
        SC_sgi(506, 1 - gAttackingSide);
        SC_sgi(509, 1 - gAttackingSide);
        if ((gMainPhase % 2)) {
            gMainPhase++;
        } else {
            gMainPhase += 2;
        }
        break;
    default:
        SC_sgi(GVAR_SIDE0DEATHS, gMainPhase);
        gAttackingSide = func_0334(gMainPhase);
        SC_sgi(507, 6);
        return;
    }
    return;
}

void func_0498(int param_0, int param_1) {
    int local_1;  // Auto-generated
    int local_3;  // Auto-generated
    int local_4;  // Auto-generated
    int y;  // Auto-generated
    int z;  // Auto-generated

    float param_0;
    int i;
    int idx;
    int local_0;
    int local_2;
    int local_41;
    int m;
    int n;
    int obj;
    int ptr;
    int ptr1;
    int ptr4;
    int ptr5;
    int t703_;
    int t717_;
    int t726_;
    int tmp17;
    int tmp25;
    int tmp50;
    s_SC_FpvMapSign local_5[4];
    void* tmp13;
    void* tmp21;
    void* tmp29;

    local_4 = 0;
    local_3 = 0;
    // Loop header - Block 70 @512
    for (obj = 0; obj < 6; obj = obj + 1) {
        local_0 = 0;
        local_1 = 0;
        local_2 = 0;
        if ((obj + 1) == param_0) {
        } else {
            if (obj < param_0) {
                local_2 = SGF_DV_ALARMZ;
            } else {
            }
        }
        if (local_41 == 0) {
            local_1 = SGI_DV_BOMB1;
        } else {
            if (local_41 == SGI_DV_BOMB2) {
                local_0 = SGI_DV_ALARMER;
            } else {
            }
        }
        local_2 = SGF_DV_ALARMY;
        if (local_0) {
        } else {
        }
        SC_DUMMY_Set_DoNotRenHier2(tmp13, SGI_JARAI_TREE);
        if (tmp17) {
            if (ptr4) {
            } else {
            }
        } else {
            if (tmp25) {
            } else {
                local_5[ptr].id = 0;
            }
        }
        SC_DUMMY_Set_DoNotRenHier2(tmp21, 1);
        goto block_101; // @648
        goto block_102; // @649
        block_101:
        block_102:
        SC_DUMMY_Set_DoNotRenHier2(tmp29, SGI_PHASE);
        local_5[ptr].id = g_FPV_UsFlag;
        goto block_109; // @691
        if (ptr4) {
            local_5[ptr].id = g_FPV_VcFlag;
        } else {
            if (ptr5) {
                local_5[ptr].id = g_FPV_NeFlag;
            } else {
            }
        }
        local_5[ptr].y = -1;
        local_5[ptr].field_12 = tmp50;
        local_5[ptr].z = SGI_DOLOOP;
        local_4 = ptr + 1;
        local_3 = obj + 1;
        continue;  // back to loop header @512
    }
    SC_MP_FpvMapSign_Set(ptr1, local_5);
    return;
}

void func_0752(int param_0, int param_1) {
    int local_1;  // Auto-generated
    int t765_ret;  // Auto-generated
    int t827_ret;  // Auto-generated

    int i;
    int idx;
    int local_0;
    int n;
    int ptr;
    int side;
    int side2;
    int side3;
    int side4;
    int side5;
    int sideB;
    s_SC_P_getinfo player_info;

    switch (local_2.field_8) {
    case 0:
        if (local_0 > 0) break;
        break;
    case 1:
        if (local_0 < 0) {
            local_1 = 0;
            t827_ret = SC_MP_SRV_P_SetSideClass(param_0, ptr, 1 + 20 * ptr);
            if (abl_lists < 64) {
                abl_list[abl_lists] = param_1;
                abl_lists++;
            }
            return;
        } else {
            return;
        }
        break;
    default:
        break;
    }
    goto block_116; // @762
    return;
    block_116:
    t765_ret = SC_MP_SRV_GetTeamsNrDifference(1);
    local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
    if (local_0 < 3 && local_0 > -3) {
        return;
    }
    return;
}

void func_0852(void) {
    int local_264;  // Auto-generated
    int t862_ret;  // Auto-generated
    int t870_ret;  // Auto-generated
    int t935_ret;  // Auto-generated

    int idx;
    int k;
    int local_0;
    int local_2;
    int local_265;
    int local_266;
    int obj;
    int ptr;
    int ptr1;
    int ptr4;
    int ptr5;
    int ptr6;
    int side;
    int side2;
    int side3;
    int sideB;
    int t959_;
    int tmp14;
    s_SC_MP_EnumPlayers enum_pl;

    t862_ret = SC_MP_SRV_GetAutoTeamBalance();
    if (SC_MP_SRV_GetAutoTeamBalance()) {
        t870_ret = SC_MP_SRV_GetTeamsNrDifference(1);
        local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
        if (local_0 < 3 && local_0 > -3) {
            return;
        }
    } else {
        return;
    }
    // Loop header - Block 146 @929
    while (TRUE) {  // loop body: blocks [146, 147, 148, 149, 150, 151, 152, 153, 155, 156]
        if (!(ptr1 != 0)) break;  // exit loop @1027
        t935_ret = rand();
        local_266 = rand() % obj;
        local_264 = ptr4;
        if (tmp14 == 0 || side2 == 0) {
            local_264 = ptr5 + 1;
            if (ptr6 == obj) {
                local_264 = 0;
            } else {
                return;
            }
        }
    }
    return;
}

void func_1028(void) {
    int local_256;  // Auto-generated
    int t1057_ret;  // Auto-generated

    int idx;
    int local_257;
    int local_258;
    int local_260;
    int obj;
    int ptr;
    int ptr1;
    int side;
    int side2;
    int side3;
    int sideB;
    int t1037_ret;
    int t1073_;
    int tmp5;
    s_SC_MP_EnumPlayers enum_pl;

    t1037_ret = SC_ggi(GVAR_SIDE0DEATHS);
    func_0334(t1037_ret);
    local_257 = t1037_ret - local_260;
    local_258 = 64;
    t1057_ret = SC_MP_EnumPlayers(&enum_pl, &local_258, ptr);
    if (SC_MP_EnumPlayers(&enum_pl, &local_258, ptr)) {
        local_256 = 0;
    }
    // Loop header - Block 160 @1065
    for (obj = 0; obj < ptr1; obj = obj + 1) {
        if (side2 == 2) {
            SC_MP_RecoverPlayer(tmp5);
        } else {
            local_256 = obj + 1;
        }
    }
    return;
}

DEBUG Propagate LADR: &param_0 → s_SC_NET_info
void ScriptMain(s_SC_NET_info *info) {
    int local_10;  // Auto-generated
    int local_11;  // Auto-generated
    int local_8;  // Auto-generated
    int local_9;  // Auto-generated
    int t1157_ret;  // Auto-generated
    int t1576_ret;  // Auto-generated
    int t1595_ret;  // Auto-generated
    int t1628_ret;  // Auto-generated
    int t1752_ret;  // Auto-generated
    int t1764_ret;  // Auto-generated
    int t1782_ret;  // Auto-generated
    int t1800_ret;  // Auto-generated
    int t1823_ret;  // Auto-generated
    int t1839_ret;  // Auto-generated
    int t1847_ret;  // Auto-generated
    int t1866_ret;  // Auto-generated
    int t1891_0;  // Auto-generated
    int t1893_ret;  // Auto-generated
    int t1975_ret;  // Auto-generated
    int t2000_ret;  // Auto-generated

    c_Vector3 t1567_0;
    c_Vector3 vec;
    dword* tmp187;
    dword* tmp197;
    dword* tmp200;
    dword* tmp206;
    dword* tmp214;
    float data_1976;
    float t1856_ret;
    int data_;
    int data_1967;
    int data_1968;
    int data_1968_v1;
    int data_1969;
    int data_1970;
    int data_1972;
    int data_1972_v1;
    int data_1977;
    int data_1978;
    int data_1982;
    int i;
    int idx;
    int j;
    int k;
    int local_12;
    int local_296;
    int local_299;
    int local_418;
    int local_419;
    int local_420;
    int obj;
    int ptr;
    int ptr27;
    int ptr28;
    int ptr29;
    int ptr30;
    int ptr32;
    int ptr33;
    int ptr37;
    int ptr38;
    int ptr39;
    int side;
    int side2;
    int side3;
    int side4;
    int side5;
    int side6;
    int side7;
    int sideB;
    int t1131_;
    int t1203_;
    int t1213_;
    int t1225_;
    int t1525_;
    int t1535_;
    int t1572_;
    int t1593_;
    int t1626_;
    int t1918_;
    int t1942_;
    int t1951_;
    int t1985_;
    int t2011_;
    int t2024_;
    int tmp103;
    int tmp110;
    int tmp117;
    int tmp123;
    int tmp164;
    int tmp185;
    int tmp195;
    int tmp219;
    int tmp22;
    int tmp26;
    int tmp35;
    int tmp57;
    int tmp99;
    s_SC_MP_EnumPlayers enum_pl[2];

    switch (info->message) {
    case 0:
        if (gSidePoints[0] + gSidePoints[1] != 0) {
            gSidePoints[0] = 0;
            gSidePoints[1] = 0;
            func_0249();
        }
        break;
    case 3:
        if (func_0050(info->elapsed_time)) break;
        local_296[0].status = 0;
        local_296 = info->elapsed_time;
        local_12 = 64;
        if (t1157_ret = SC_MP_EnumPlayers(enum_pl, &local_12, -1)) {
        }
        // Loop header - Block 193 @1322
        for (ptr28 = 0; ptr28 < 2; ptr28 = ptr28 + 1) {
            local_9 = 0;
            local_10 = 0;
            (&gRecTimer) + ptr28 * 768 + ptr32 * 128 + ptr * 4 = tmp57 - info->elapsed_time;
            local_10 = ptr + 1;
            local_9 = ptr32 + 1;
            local_8 = ptr28 + 1;
        }
        gNextRecover -= info->elapsed_time;
        if (gNextRecover < 0.0f) {
            gNextRecover = func_0119();
        }
        if (local_419 == 0) {
            gNoActiveTime += info->elapsed_time;
            if (gMissionTime > -10.0f) {
                gMissionTime = -10.0f;
                gMissionTime_update = -1.0f;
                func_0264(0);
            }
        } else {
            if (local_419 == 1) {
                gMission_afterstart_time += info->elapsed_time;
                gMissionTime -= info->elapsed_time;
                func_0264(info->elapsed_time);
                if (gMissionTime <= 0.0f) {
                    gMission_phase = 3;
                    SC_sgi(GVAR_SIDE1DEATHS, gMission_phase);
                    gPhaseTimer = 8.0f;
                    func_0355();
                } else {
                    if (gMission_afterstart_time > 5.0f && gCurStep > 0) {
                        local_8 = 0;
                        if (tmp99 == gAttackingSide && side6 == 1) {
                            SC_P_GetPos(tmp103, &vec);
                            local_9 = gCurStep - 1;
                            if (t1576_ret = SC_IsNear3D(&vec, &gStepSwitch[ptr33], tmp110)) {
                                if (ptr33) {
                                    gCurStep = ptr33;
                                    t1595_ret = SC_MP_GetHandleofPl(t1593_);
                                    SC_sgi(t1593_, SC_MP_GetHandleofPl(t1593_));
                                    SC_sgi(507, gCurStep);
                                    func_1028();
                                    SC_P_MP_AddPoints(tmp117, 1);
                                } else {
                                    gMission_phase = 2;
                                    t1628_ret = SC_MP_GetHandleofPl(t1626_);
                                    SC_sgi(t1626_, SC_MP_GetHandleofPl(t1626_));
                                    SC_sgi(GVAR_SIDE1DEATHS, gMission_phase);
                                    gPhaseTimer = 8.0f;
                                    func_0355();
                                    SC_P_MP_AddPoints(tmp123, 2);
                                }
                            } else {
                                local_9 = ptr33 + 1;
                            }
                        }
                        local_8 = ptr29 + 1;
                    }
                }
            } else {
                if (local_419 == 3) {
                } else {
                    if (local_419 == 2) {
                        gPhaseTimer -= info->elapsed_time;
                        if (gPhaseTimer < 0.0f) {
                            gNoActiveTime = 0;
                            gMission_phase = 0;
                            SC_sgi(GVAR_SIDE1DEATHS, gMission_phase);
                            func_0852();
                            SC_MP_SetInstantRecovery(1);
                            SC_MP_RecoverAllNoAiPlayers();
                        }
                    }
                }
            }
        }
        // Loop header - Block 216 @1517
        for (ptr29 = 0; ptr29 < obj; ptr29 = ptr29 + 1) {
            local_8 = ptr29 + 1;
        }
        break;
    case 4:
        gCLN_ShowInfo -= info->elapsed_time;
        if (gCLN_ShowStartInfo > 0.0f) {
            gCLN_ShowStartInfo -= info->elapsed_time;
        }
        if (gCLN_ShowWaitingInfo > 0.0f) {
            gCLN_ShowWaitingInfo -= info->elapsed_time;
        }
        t1752_ret = SC_ggi(GVAR_SIDE1DEATHS);
        if (local_419 == 0) {
            t1764_ret = SC_ggi(508);
            func_0498(SC_ggi(508) - 1, 2);
        } else {
            if (local_419 == 1) {
                if (t1782_ret = SC_ggi(507) && t1800_ret = SC_ggi(508) && gCLN_CurStep > 0) {
                    gCLN_ShowInfo = 5.0f;
                    SC_SND_PlaySound2D(10425);
                }
                t1823_ret = SC_ggi(GVAR_SIDE0DEATHS);
                func_0334(SC_ggi(GVAR_SIDE0DEATHS));
                func_0498(tmp164, gCLN_CurStep);
            }
        }
        if (t1839_ret = SC_ggi(505)) {
            t1847_ret = SC_ggi(505);
            gCLN_MissionTimePrevID = SC_ggi(505);
            t1856_ret = SC_ggf(504);
            gCLN_MissionTime = SC_ggf(504);
        } else {
            if (t1866_ret = SC_ggi(GVAR_SIDE1DEATHS)) {
                gCLN_MissionTime -= info->elapsed_time;
            }
        }
        // Loop header - Block 260 @1884
        for (ptr30 = 0; ptr30 < 2; ptr30 = ptr30 + 1) {
            t1891_0 = 500 + ptr30;
            t1893_ret = SC_ggi(t1891_0);
            gCLN_SidePoints[ptr30] = SC_ggi(t1891_0);
            SC_MP_SetSideStats(ptr30, 0, tmp185);
            *tmp187 = 1;
            (&local_299) + ptr30 * 16 = 3 * ptr30;
            *tmp197 = tmp195;
            *tmp200 = -1140850689;
            local_8 = ptr30 + 1;
        }
        local_11 = 2;
        if (gCLN_MissionTime > 0.0f && t1975_ret = SC_ggi(GVAR_SIDE1DEATHS)) {
            *tmp206 = -1140850689;
            (&local_299) + ptr39 * 16 = 6;
            if (t2000_ret = SC_ggi(GVAR_SIDE1DEATHS)) {
                *tmp214 = 0;
            } else {
                (int)gCLN_MissionTime + 0.99f = tmp219;
            }
            *((&local_299) + local_11 * 16 + 4) = 2;
            local_11++;
        }
        SC_MP_SetIconHUD(&local_299, local_11);
        break;
    default:
        // Loop header - Block 176 @1195
        for (ptr27 = 0; ptr27 < obj; ptr27 = ptr27 + 1) {
            if (side2 != 0 && tmp22 < 2) {
                (&local_296) + tmp26 * 4 = 1;
            }
            local_8 = ptr27 + 1;
        }
        gMission_starting_timer -= info->elapsed_time;
        if (tmp35 && local_296[0].status) {
            SC_MP_SetInstantRecovery(0);
            gMission_phase = 1;
            gMission_afterstart_time = 0;
            SC_sgi(GVAR_SIDE1DEATHS, gMission_phase);
            func_0294();
            SC_MP_SRV_InitGameAfterInactive();
            SC_MP_RestartMission();
            SC_MP_RecoverAllNoAiPlayers();
            gMission_starting_timer = 8.0f;
            local_8 = 0;
            local_9 = 0;
            local_10 = 0;
            (&gRecTimer) + ptr28 * 768 + ptr32 * 128 + ptr * 4 = tmp57 - info->elapsed_time;
            local_10 = ptr + 1;
            local_9 = ptr32 + 1;
            local_8 = ptr28 + 1;
            return TRUE;
        }
        if (gMission_starting_timer <= 0.0f && gMission_phase > 0) {
            gMission_phase = 0;
            gMission_afterstart_time = 0;
            SC_sgi(GVAR_SIDE1DEATHS, gMission_phase);
            func_0852();
            func_0294();
        }
    }
    return;
}

// Function abl_lists at 2020 - entry block not found

// Function abl_list at 2021 - entry block not found

// Function g_FPV_UsFlag at 2109 - entry block not found

// Function g_FPV_VcFlag at 2110 - entry block not found

// Function g_FPV_NeFlag at 2111 - entry block not found

