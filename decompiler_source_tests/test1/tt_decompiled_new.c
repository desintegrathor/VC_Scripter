// Structured decompilation of decompiler_source_tests/test1/tt.scr
// Functions: 15

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
int gSteps = 0;
dword gRecs[12];
dword gVar = 0;
dword gVar1 = 0;
dword gRec[1536];
dword gVar2 = 0;
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

int _init(s_SC_NET_info *info) {
    int n;

    return;
}

int func_0050(float param_0) {
    int n;

    switch (gEndRule) {
    case 0:
        break;
    case 2:
        break;
    default:
        SC_message("EndRule unsopported: %d", gEndRule);
        break;
    }
    gTime += param_0;
    if (gTime > ((float)gEndValue)) {
        SC_MP_LoadNextMap();
        return TRUE;
    }
    goto block_20;
block_3:
block_10:
block_14:
    SC_MP_LoadNextMap();
    return TRUE;
block_19:
block_20:
    return FALSE;
}

int func_0119(void) {
    s_SC_MP_SRV_AtgSettings atg_settings;
    float local_0;
    int n;

    if (atg_settings.tt_respawntime > 1.0f) {
        return atg_settings.tt_respawntime;
    }
}

int func_0155(int param_0) {
    s_SC_MP_SRV_AtgSettings atg_settings;
    float local_0;
    int n;

    if (atg_settings.tt_respawntime > 1.0f) {
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

    if (atg_settings.tt_timelimit > 59.0f) {
        return atg_settings.tt_timelimit;
    }
}

void func_0249(void) {
    SC_sgi(500, gSidePoints[0]);
    SC_sgi(501, gSidePoints[1]);
    return;
}

void func_0264(int param_0, float param_1) {
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
    if (!((gMainPhase % 2) == 0)) {
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

    switch (param_0%4) {
    case 0:
        break;
    case 3:
        return FALSE;
    }
}

void func_0355(void) {
    int n;

    switch (gMission_phase) {
    case 3:
        gSidePoints[(1 - gAttackingSide)]++;
        func_0249();
        SC_sgi(506, 1 - gAttackingSide);
        SC_sgi(509, 1 - gAttackingSide);
        break;
    case 2:
        if (!((gMainPhase % 2))) {
            gMissionTimeToBeat = gMissionTimePrev - gMissionTime;
        } else {
            gSidePoints[gAttackingSide]++;
            func_0249();
            SC_sgi(506, gAttackingSide);
        }
        break;
    }
block_57:
block_59:
    gMainPhase++;
block_60:
    gMainPhase += 2;
block_61:
block_63:
}

int func_0498(int param_0, int param_1) {
    s_SC_FpvMapSign local_5[4];
    int idx;
    int local_2;
    int local_41;
    int m;
    int n;
    void* tmp13;
    void* tmp21;
    void* tmp29;

    local_4 = 0;
    local_3 = 0;
    for (obj = 0; obj < 6; obj = obj + 1) {
        local_3 = obj + 1;
    }
    local_0 = 0;
    local_1 = 0;
    if (/* condition */) {
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
        goto block_85;
    }
    if (obj < param_0) {
        local_2 = 1;
        goto block_85;
    }
    if (tmp9) {
        if (!local_0) {
        } else {
        }
        SC_DUMMY_Set_DoNotRenHier2(tmp13, 1);
        goto block_91;
    }
block_74:
block_77:
block_80:
block_91:
block_96:
    SC_DUMMY_Set_DoNotRenHier2(tmp21, 1);
block_112:
    SC_MP_FpvMapSign_Set(ptr1, &local_5);
    return;
}

int func_0752(int param_0, int param_1) {
    int idx;
    int n;
    s_SC_P_getinfo player_info;

    switch (local_2.field_8) {
    case 0:
        SC_P_GetInfo(param_0, &player_info);
        break;
    case 1:
        break;
    }
block_115:
    return;
block_128:
    return;
}

int func_0852(void) {
    s_SC_MP_EnumPlayers enum_pl;
    int idx;
    int k;
    int local_2;
    int local_265;
    int local_266;

    if (!SC_MP_SRV_GetAutoTeamBalance()) {
        return;
    }
    if (/* condition */) {
        return;
    }
    if (!(local_0 > 0)) {
        local_1 = 1;
        local_2 = tmp6 / 2;
    } else {
        local_1 = 0;
        local_2 = local_0 / 2;
    }
    if (/* condition */) {
        if (!obj) {
            return;
        }
        while (!(ptr1 != 0)) {
            t1006_ret = SC_MP_SRV_P_SetSideClass(tmp21, 1 - ptr, 1 + 20 * ((1 - ptr)));
            local_8[ptr6].id = 0;
            local_2 = ptr1 - 1;
        }
        local_266 = rand() % obj;
        local_264 = ptr4;
        while (/* condition */) {
        }
        if (ptr6 == obj) {
            local_264 = 0;
        if (/* condition */) {
            return;
        }
    }
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
    local_257 = t1037_ret - local_260;
    local_258 = 64;
block_159:
    local_256 = 0;
    for (obj = 0; obj < ptr1; obj = obj + 1) {
        SC_MP_RecoverPlayer(tmp5);
        local_256 = obj + 1;
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
    int local_412;
    int local_418;
    int local_419;
    int local_420;
    float local_421;
    int local_8;
    int n;
    s_SC_P_getinfo player_info;
    s_SC_MP_SRV_settings srv_settings;
    s_SC_MP_Recover t3600_0;
    c_Vector3 vec;

    switch (info->message) {
    case 3:
        func_0050(info->elapsed_time);
        break;
    case 4:
        gCLN_ShowInfo -= info->elapsed_time;
        break;
    case 9:
        SC_sgi(GVAR_MP_MISSIONTYPE, 9);
        gEndRule = param_0->field_4;
        gEndValue = info->param2;
        gTime = 0;
        SC_MP_EnableBotsFromScene(0);
        break;
    case 0:
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
        break;
    case 2:
        local_8 = 0;
        local_314 = 0;
        local_298 = 0;
        local_10 = SC_ggi(502);
        break;
    case 5:
        break;
    case 6:
        local_13 = info->param2;
        local_9 = param_0->field_4;
        break;
    case 10:
        gTime = 0;
        SC_ZeroMem(&gSidePoints, 8);
        func_0249();
        SC_MP_SetInstantRecovery(1);
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
        local_8 = 0;
        break;
    }
block_167:
block_170:
    (&local_296) + 4 = 0;
    local_296 = info->elapsed_time;
    local_12 = 64;
    for (ptr27 = 0; ptr27 < obj; ptr27 = ptr27 + 1) {
        (&local_296) + tmp26 * 4 = 1;
        local_8 = ptr27 + 1;
    }
block_210:
block_212:
    gMission_phase = 3;
    SC_sgi(503, gMission_phase);
    gPhaseTimer = 8.0f;
    func_0355();
block_220:
    SC_P_GetPos(tmp102, &vec);
    local_9 = gCurStep - 1;
    for (ptr41 = gCurStep - 1; ptr41 < gCurStep; ptr41 = ptr41 + 1) {
        gCurStep = ptr41;
        t1595_ret = SC_MP_GetHandleofPl(t1593_);
        SC_sgi(t1593_, SC_MP_GetHandleofPl(t1593_));
        SC_sgi(507, gCurStep);
        func_1028();
        SC_P_MP_AddPoints(tmp116, 1);
        gMission_phase = 2;
        t1628_ret = SC_MP_GetHandleofPl(t1626_);
        SC_sgi(t1626_, SC_MP_GetHandleofPl(t1626_));
        SC_sgi(503, gMission_phase);
        gPhaseTimer = 8.0f;
        func_0355();
        SC_P_MP_AddPoints(tmp122, 2);
        local_9 = ptr41 + 1;
    }
block_228:
block_230:
block_231:
block_232:
block_236:
block_238:
block_255:
block_257:
block_267:
    (int)gCLN_MissionTime + 0.99f = tmp217;
block_268:
    local_299[ptr51].y = 2;
    local_11 = ptr51 + 1;
block_269:
    SC_MP_SetIconHUD(&icon, ptr51);
block_271:
block_274:
block_279:
    SC_ZeroMem(&gFlagNod, 72);
    local_8 = 0;
    for (ptr28 = 0; ptr28 < 6; ptr28 = ptr28 + 1) {
        t2286_ret = sprintf(&n, "TT_flag_%d", ptr28);
        local_295 = SC_NOD_GetNoMessage(0, &local_0);
        SC_NOD_GetPivotWorld(ptr54, &gFlagPos[ptr28]);
        gFlagNod[ptr28].field_0 = SC_NOD_Get(ptr54, &tmp285);
        gFlagNod[ptr28].field_4 = SC_NOD_Get(ptr54, &tmp286);
        gFlagNod[ptr28].field_8 = SC_NOD_Get(ptr54, &tmp287);
        local_8 = ptr28 + 1;
    }
block_284:
    for (ptr28 = 0; ptr28 < 32; ptr28 = ptr28 + 1) {
        t2484_ret = sprintf(&local_0, "TT_%c%d_%d", ptr55, ptr41, ptr28);
        gRecs[ptr] + ptr41 * 4++;
        local_8 = ptr28 + 1;
    }
block_301:
    gSteps = 0;
    local_8 = 0;
    for (ptr28 = 0; ptr28 < 6; ptr28 = ptr28 + 1) {
        gSteps = ptr28 + 1;
        local_8 = ptr28 + 1;
    }
    for (ptr28 = 0; ptr28 < (gSteps - 1); ptr28 = ptr28 + 1) {
        t2757_ret = sprintf(&local_0, "TTS_%d", ptr28);
        SC_message(&tmp435, &local_0);
        local_8 = ptr28 + 1;
    }
block_315:
    SC_sgi(508, gSteps);
block_316:
block_318:
block_323:
block_324:
block_403:
block_405:
    &idx.fval1 = 0.1f;
block_427:
block_428:
block_430:
block_446:
block_448:
    SC_MP_RestartMission();
    SC_MP_RecoverAllNoAiPlayers();
    gMission_phase = 0;
    SC_sgi(503, gMission_phase);
block_449:
    gCLN_ShowInfo = 0;
    SC_MP_SRV_ClearPlsStats();
block_451:
block_454:
}

