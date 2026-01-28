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
    int n;

    return;
}

int func_0050(float param_0) {
    int n;

    if (n != 0) {
        if (local_0 != 2) {
            SC_message(&data_2119, gEndRule);
        } else {
            if (gSidePoints[0] >= gEndValue || gSidePoints[1] >= gEndValue) {
                SC_MP_LoadNextMap();
                return TRUE;
            }
        }
    } else {
        if (gMission_phase > 0) {
            gTime += param_0;
        }
        SC_MP_EndRule_SetTimeLeft(gTime, gMission_phase);
        if (gTime > ((float)gEndValue)) {
            SC_MP_LoadNextMap();
            return TRUE;
        }
    }
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
    int n;

    if (local_0 != 0) {
        if (local_0 != 3) {
            return TRUE;
        }
    } else {
    }
    return FALSE;
}

void func_0355(void) {
    int n;

block_63:
block_64:
    SC_sgi(509, gAttackingSide);
block_65:
    gSidePoints[gAttackingSide]++;
    func_0249();
    SC_sgi(506, gAttackingSide);
block_66:
    gMissionTimeToBeat = gMissionTimePrev - gMissionTime;
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
    dword local_4;
    int local_41;
    int m;
    int n;

    local_4 = 0;
    local_3 = 0;
block_91:
block_96:
    SC_DUMMY_Set_DoNotRenHier2(t617_, 1);
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0752(int param_0, int param_1) {
    int idx;
    dword local_1;
    int n;
    s_SC_P_getinfo player_info;

    if (! SC_MP_SRV_GetAutoTeamBalance()) {
        return;
    }
    local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
    if (/* condition */) {
        return;
    } else {
        SC_P_GetInfo(param_0, &player_info);
        if (local_2.field_8 != 0 || local_0 <= 0) {
            local_1 = 1;
        } else {
            if (local_2.field_8 != 1 || local_0 >= 0) {
                return;
            }
            local_1 = 0;
        }
        t827_ret = SC_MP_SRV_P_SetSideClass(param_0, local_1, local_1 * 20 + 1);
        if (abl_lists < 64) {
            abl_list[abl_lists] = param_1;
            abl_lists++;
        }
        return;
    }
}

int func_0852(void) {
    s_SC_MP_EnumPlayers enum_pl;
    int idx;
    int k;
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
block_156:
    t1006_ret = SC_MP_SRV_P_SetSideClass(t994_, 1 - local_1, ((1 - local_1)) * 20 + 1);
    local_8[j].id = 0;
    local_2 = i - 1;
block_157:
    return;
}

int func_1028(void) {
    s_SC_MP_EnumPlayers enum_pl;
    int idx;
    dword local_257;
    int local_258;
    int local_260;

    t1037_ret = SC_ggi(502);
    func_0334(t1037_ret);
    local_257 = 1 - t1037_ret;
    local_258 = 64;
    t1057_ret = SC_MP_EnumPlayers(&enum_pl, &local_258, local_257);
block_159:
    local_256 = 0;
    for (i = 0; i < local_258; i++) {
        SC_MP_RecoverPlayer(t1084_);
        local_256 = i + 1;
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
    int idx;
    dword j;
    int k;
    dword local_11;
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
    int n;
    s_SC_P_getinfo player_info;
    s_SC_MP_SRV_settings srv_settings;
    int strict_cmp_0;
    int strict_cmp_1;
    int strict_cmp_2;
    char* t2998_ret;
    ushort* t3021_ret;
    ushort* t3085_ret;
    ushort* t3121_ret;
    char* t3163_ret;
    ushort* t3231_ret;
    char* t3275_ret;
    ushort* t3326_ret;
    s_SC_MP_Recover t3600_0;
    dword* tmp222;
    dword* tmp238;
    dword* tmp241;
    c_Vector3 vec;

    for (j = 0; j < local_12; j++) {
        *(&local_296) + tmp26 * 4 = 1;
        local_8 = j + 1;
    }
block_192:
    local_8 = 0;
    for (j = 0; j < 2; j++) {
        local_9 = 0;
        local_10 = 0;
        gRecTimer[768] + idx * 128 + idx29 * 4 -= info->elapsed_time;
        local_10 = idx29 + 1;
        local_9 = idx + 1;
        local_8 = j + 1;
    }
block_210:
block_211:
    gMission_afterstart_time += info->elapsed_time;
    gMissionTime -= info->elapsed_time;
    func_0264(info->elapsed_time);
    t1489_0 = LN(gMissionTime > 0.0f);
block_212:
    gMission_phase = 3;
    SC_sgi(503, gMission_phase);
    gPhaseTimer = 8.0f;
    func_0355();
block_215:
    local_8 = 0;
    for (j = 0; j < local_12; j++) {
        SC_P_GetPos(t1547_, &vec);
        local_9 = gCurStep - 1;
        t1576_ret = SC_IsNear3D(&vec, &gStepSwitch[idx], t1574_);
        gCurStep = idx;
        t1595_ret = SC_MP_GetHandleofPl(t1593_);
        SC_sgi(510, SC_MP_GetHandleofPl(t1593_));
        SC_sgi(507, gCurStep);
        func_1028();
        SC_P_MP_AddPoints(t1610_, 1);
        gMission_phase = 2;
        t1628_ret = SC_MP_GetHandleofPl(t1626_);
        SC_sgi(510, SC_MP_GetHandleofPl(t1626_));
        SC_sgi(503, gMission_phase);
        gPhaseTimer = 8.0f;
        func_0355();
        SC_P_MP_AddPoints(t1647_, 2);
        local_9 = idx + 1;
        local_8 = j + 1;
    }
block_228:
block_230:
block_231:
block_232:
block_233:
    gPhaseTimer -= info->elapsed_time;
block_234:
    gNoActiveTime = 0;
    gMission_phase = 0;
    SC_sgi(503, gMission_phase);
    func_0852();
    SC_MP_SetInstantRecovery(1);
    SC_MP_RecoverAllNoAiPlayers();
block_235:
block_236:
    for (j = 0; j < 6; j++) {
        t2286_ret = sprintf(&n, "TT_flag_%d", j);
        local_295 = SC_NOD_GetNoMessage(0, &local_0);
        SC_NOD_GetPivotWorld(local_295, &gFlagPos[j]);
        gFlagNod[j].field_0 = SC_NOD_Get(local_295, "vlajkaUS");
        gFlagNod[j].field_4 = SC_NOD_Get(local_295, "Vlajka VC");
        gFlagNod[j].field_8 = SC_NOD_Get(local_295, "vlajka N");
        local_8 = j + 1;
    }
block_284:
block_285:
    SC_MP_Gvar_SetSynchro(500);
    SC_MP_Gvar_SetSynchro(501);
    func_0249();
    SC_MP_Gvar_SetSynchro(503);
    SC_sgi(503, 0);
    SC_MP_Gvar_SetSynchro(502);
    SC_sgi(502, 0);
    SC_MP_Gvar_SetSynchro(506);
    SC_sgi(506, 0);
    SC_MP_Gvar_SetSynchro(509);
    SC_sgi(509, 0);
    SC_MP_Gvar_SetSynchro(510);
    SC_sgi(510, 0);
    SC_MP_Gvar_SetSynchro(507);
    SC_sgi(507, 0);
    SC_MP_Gvar_SetSynchro(508);
    SC_MP_Gvar_SetSynchro(504);
    SC_MP_Gvar_SetSynchro(505);
    SC_sgf(504, 0.0f);
    SC_sgi(505, 0);
    SC_ZeroMem(&gRecs, 48);
    local_10 = 0;
    for (local_10 = 0; local_10 < 2; local_10++) {
        local_294 = 68;
        local_294 = 65;
        local_9 = 0;
        local_8 = 0;
        t2484_ret = sprintf(&local_0, "TT_%c%d_%d", local_294, idx, j);
        t2513_ret = SC_NET_FillRecover(&gRec[3072] + idx * 512 + tmp288 * 16, &local_0);
        gRecs[idx29] + idx * 4++;
        local_8 = j + 1;
        local_8 = 32 - tmp317;
        SC_MP_GetRecovers(t2595_, &gRec[3072] + idx * 512 + tmp331 * 16, &local_8);
        gRecs[idx29] + idx * 4 += j;
        local_9 = idx + 1;
        local_10 = idx29 + 1;
    }
block_301:
    gSteps = 0;
    local_8 = 0;
    for (j = 0; j < 6; j++) {
        gSteps = j + 1;
        local_8 = j + 1;
    }
    for (j = 0; j < (gSteps - 1; j++) {
        t2757_ret = sprintf(&local_0, "TTS_%d", j);
        t2769_ret = SC_GetScriptHelper(&local_0, &gStepSwitch[j]);
        SC_message(&data_2636, &local_0);
        local_8 = j + 1;
    }
block_315:
    SC_sgi(508, gSteps);
block_316:
block_318:
block_319:
    local_8 = 0;
    local_314 = 0;
    local_298 = 0;
    local_10 = SC_ggi(502);
block_323:
block_329:
block_337:
block_338:
    gCLN_ShowWaitingInfo = 3.0f;
block_339:
    gCLN_ShowStartInfo = 3.0f;
block_405:
    &idx.fval1 = 0.1f;
block_409:
    local_8 = 0;
block_413:
    local_8 = j + 1;
block_427:
block_428:
block_456:
    return TRUE;
}

