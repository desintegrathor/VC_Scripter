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
        gTime += param_0;
        SC_MP_EndRule_SetTimeLeft(gTime, gMission_phase);
        SC_MP_LoadNextMap();
        return TRUE;
        break;
    case 2:
        SC_MP_LoadNextMap();
        return TRUE;
        break;
    default:
        SC_message("EndRule unsopported: %d", gEndRule);
        break;
    }
block_3:
block_10:
}

int func_0119(void) {
    s_SC_MP_SRV_AtgSettings atg_settings;
    float local_0;
    int n;

    if (atg_settings.tt_respawntime > 1.0f) {
        return atg_settings.tt_respawntime;
    }
    local_0 = SC_ggf(400);
block_24:
    local_0 = 30.0f;
block_25:
    return local_0;
}

int func_0155(int param_0) {
    s_SC_MP_SRV_AtgSettings atg_settings;
    float local_0;
    int n;

    SC_MP_SRV_GetAtgSettings(&atg_settings);
block_27:
    local_0 = atg_settings.tt_respawntime / 3.0f;
block_28:
    local_0 = 5.0f;
block_29:
block_30:
    local_0 = 10.0f;
block_31:
    return local_0;
block_32:
    local_0 = SC_ggf(401);
block_33:
    local_0 = 10.0f;
block_34:
    return local_0;
}

int func_0213(void) {
    s_SC_MP_SRV_AtgSettings atg_settings;
    float local_0;
    int n;

    if (atg_settings.tt_timelimit > 59.0f) {
        return atg_settings.tt_timelimit;
    }
    local_0 = SC_ggf(402);
block_38:
    local_0 = 480.0f;
block_39:
    return local_0;
}

void func_0249(void) {
    SC_sgi(500, gSidePoints[0]);
    SC_sgi(501, gSidePoints[1]);
    return;
}

void func_0264(int param_0, float param_1) {
    gMissionTime_update -= param_0;
block_42:
    gMissionTime_update = 10.0f;
    SC_sgf(504, gMissionTime);
    SC_sgi(505, SC_ggi(505) + 1);
block_43:
    return;
}

void func_0294(void) {
    int n;

    gCurStep = gSteps - 1;
    SC_sgi(507, gCurStep);
block_45:
    gMissionTime = func_0213();
    gMissionTimePrev = gMissionTime;
block_46:
    gMissionTime = gMissionTimeToBeat;
block_47:
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
        gMainPhase++;
        gMainPhase += 2;
        break;
    case 2:
        SC_sgi(509, gAttackingSide);
        gSidePoints[gAttackingSide]++;
        func_0249();
        SC_sgi(506, gAttackingSide);
        gMissionTimeToBeat = gMissionTimePrev - gMissionTime;
        gMainPhase++;
        break;
    }
block_57:
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
block_74:
block_77:
block_80:
block_91:
block_96:
    SC_DUMMY_Set_DoNotRenHier2(tmp21, 1);
block_97:
block_103:
    local_5[ptr].id = 0;
block_104:
    local_5[ptr].id = g_FPV_UsFlag;
block_105:
block_106:
    local_5[ptr].id = g_FPV_VcFlag;
block_107:
block_108:
    local_5[ptr].id = g_FPV_NeFlag;
block_109:
block_110:
    local_5[ptr].y = -1;
    local_5[ptr].field_12 = tmp50;
    local_5[ptr].z = 1.0f;
    local_4 = ptr + 1;
block_111:
    local_3 = obj + 1;
}

int func_0752(int param_0, int param_1) {
    int idx;
    int n;
    s_SC_P_getinfo player_info;

    switch (local_2.field_8) {
    case 0:
        local_1 = 1;
        break;
    case 1:
        local_1 = 0;
        break;
    }
    t827_ret = SC_MP_SRV_P_SetSideClass(param_0, ptr, 1 + 20 * ptr);
block_115:
    return;
block_128:
    return;
block_130:
    abl_list[abl_lists] = param_1;
    abl_lists++;
block_131:
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
block_140:
    local_1 = 0;
    local_2 = local_0 / 2;
block_141:
    local_1 = 1;
    local_2 = tmp6 / 2;
block_142:
    local_265 = 64;
    t921_ret = SC_MP_EnumPlayers(&enum_pl, &local_265, ptr);
block_152:
    local_264 = 0;
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
    t1057_ret = SC_MP_EnumPlayers(&enum_pl, &local_258, ptr);
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
        (&local_296) + 4 = 0;
        local_296 = info->elapsed_time;
        local_12 = 64;
        t1157_ret = SC_MP_EnumPlayers(&enum_pl, &local_12, -1);
        local_8 = 0;
        local_9 = 0;
        local_10 = 0;
        (&gRecTimer) + ptr27 * 768 + ptr40 * 128 + ptr * 4 -= info->elapsed_time;
        local_10 = ptr + 1;
        local_9 = ptr40 + 1;
        local_8 = ptr27 + 1;
        gNextRecover -= info->elapsed_time;
        gNextRecover = func_0119();
        gNoActiveTime += info->elapsed_time;
        gMissionTime = -10.0f;
        gMissionTime_update = -1.0f;
        func_0264(0);
        gMission_afterstart_time += info->elapsed_time;
        gMissionTime -= info->elapsed_time;
        func_0264(info->elapsed_time);
        gMission_phase = 3;
        SC_sgi(503, gMission_phase);
        gPhaseTimer = 8.0f;
        func_0355();
        local_8 = 0;
        SC_P_GetPos(tmp102, &vec);
        local_9 = gCurStep - 1;
        t1576_ret = SC_IsNear3D(&vec, &gStepSwitch[ptr41], tmp109);
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
        local_8 = ptr27 + 1;
        gPhaseTimer -= info->elapsed_time;
        gNoActiveTime = 0;
        gMission_phase = 0;
        SC_sgi(503, gMission_phase);
        func_0852();
        SC_MP_SetInstantRecovery(1);
        SC_MP_RecoverAllNoAiPlayers();
        break;
    case 4:
        gCLN_ShowInfo -= info->elapsed_time;
        gCLN_ShowStartInfo -= info->elapsed_time;
        gCLN_ShowWaitingInfo -= info->elapsed_time;
        t1752_ret = SC_ggi(503);
        func_0498(SC_ggi(508) - 1, 2);
        gCLN_CurStep = SC_ggi(507);
        gCLN_ShowInfo = 5.0f;
        SC_SND_PlaySound2D(10425);
        t1823_ret = SC_ggi(502);
        func_0334(SC_ggi(502));
        func_0498(local_420, gCLN_CurStep);
        gCLN_MissionTimePrevID = SC_ggi(505);
        gCLN_MissionTime = SC_ggf(504);
        gCLN_MissionTime -= info->elapsed_time;
        local_8 = 0;
        t1891_0 = 500 + ptr30;
        gCLN_SidePoints[ptr30] = SC_ggi(t1891_0);
        SC_MP_SetSideStats(ptr30, 0, tmp183);
        local_299[ptr30].y = 1;
        local_299[ptr30].icon_id = 3 * ptr30;
        local_299[ptr30].z = tmp193;
        local_299[ptr30].field_12 = -1140850689;
        local_8 = ptr30 + 1;
        local_11 = 2;
        local_299[ptr51].field_12 = -1140850689;
        local_299[ptr51].icon_id = 6;
        local_299[ptr51].z = 0;
        (int)gCLN_MissionTime + 0.99f = tmp217;
        local_299[ptr51].y = 2;
        local_11 = ptr51 + 1;
        SC_MP_SetIconHUD(&icon, ptr51);
        break;
    case 9:
        SC_sgi(GVAR_MP_MISSIONTYPE, 9);
        gEndRule = param_0->field_4;
        gEndValue = info->param2;
        gTime = 0;
        SC_MP_EnableBotsFromScene(0);
        break;
    case 0:
        gSidePoints[0] = 0;
        gSidePoints[1] = 0;
        func_0249();
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
        SC_MP_SRV_SetClassLimit(ptr27 + 1, tmp242);
        SC_MP_SRV_SetClassLimit(ptr27 + 21, tmp247);
        local_8 = ptr27 + 1;
        SC_ZeroMem(&hudinfo, 60);
        hudinfo.title = 5100;
        tmp249 = 1;
        tmp252 + 4 = 3;
        tmp255 + 8 = -2147483644;
        tmp258 + 12 = -2147483643;
        hudinfo.pl_mask = 27;
        hudinfo.use_sides = 1;
        tmp265 = 1010;
        tmp268 = 1140850943;
        tmp271 + 4 = 1011;
        tmp274 + 4 = 2040.0f;
        hudinfo.side_mask = 1;
        SC_MP_HUD_SetTabInfo(&hudinfo);
        SC_MP_AllowStPwD(1);
        SC_MP_AllowFriendlyFireOFF(1);
        SC_MP_SetItemsNoDisappear(0);
        SC_ZeroMem(&gFlagNod, 72);
        local_8 = 0;
        t2286_ret = sprintf(&n, "TT_flag_%d", ptr27);
        local_295 = SC_NOD_GetNoMessage(0, &local_0);
        SC_NOD_GetPivotWorld(ptr54, &gFlagPos[ptr27]);
        gFlagNod[ptr27].field_0 = SC_NOD_Get(ptr54, &tmp285);
        gFlagNod[ptr27].field_4 = SC_NOD_Get(ptr54, &tmp286);
        gFlagNod[ptr27].field_8 = SC_NOD_Get(ptr54, &tmp287);
        local_8 = ptr27 + 1;
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
        local_294 = 68;
        local_294 = 65;
        local_9 = 0;
        local_8 = 0;
        t2484_ret = sprintf(&local_0, "TT_%c%d_%d", ptr55, ptr40, ptr27);
        t2513_ret = SC_NET_FillRecover((&gRec) + ptr * 3072 + ptr40 * 512 + tmp353 * 16, &local_0);
        gRecs[ptr] + ptr40 * 4++;
        local_8 = ptr27 + 1;
        local_8 = 32 - tmp382;
        SC_MP_GetRecovers(tmp388, (&gRec) + ptr * 3072 + ptr40 * 512 + tmp397 * 16, &local_8);
        gRecs[ptr] + ptr40 * 4 += ptr27;
        local_9 = ptr40 + 1;
        local_10 = ptr + 1;
        gSteps = 0;
        local_8 = 0;
        gSteps = ptr27 + 1;
        local_8 = ptr27 + 1;
        local_8 = 0;
        SC_Log(3, "TurnTable recovers #%d: att:%d  def:%d", ptr27, tmp423, tmp427);
        local_8 = ptr27 + 1;
        SC_ZeroMem(&gRecTimer, 1536);
        local_8 = 0;
        t2757_ret = sprintf(&local_0, "TTS_%d", ptr27);
        t2769_ret = SC_GetScriptHelper(&local_0, &gStepSwitch[ptr27]);
        SC_message(&tmp435, &local_0);
        local_8 = ptr27 + 1;
        SC_sgi(508, gSteps);
        break;
    case 2:
        local_8 = 0;
        local_314 = 0;
        local_298 = 0;
        local_10 = SC_ggi(502);
        gCLN_gamephase = SC_ggi(503);
        SC_SND_PlaySound2D(11117);
        SC_SND_PlaySound2D(11116);
        local_314 = SC_Wtxt(1076);  // 1076: "Waiting for more players.";
        gCLN_ShowStartInfo = 0;
        gCLN_ShowWaitingInfo = 3.0f;
        gCLN_ShowStartInfo = 3.0f;
        local_8 = SC_PC_Get();
        SC_P_GetInfo(ptr37, &player_info);
        t2933_ret = SC_ggi(502);
        func_0334(t2933_ret);
        local_314 = SC_Wtxt(5108);
        local_314 = SC_Wtxt(5109);
        SC_GameInfoW(ptr56);
        local_314 = 0;
        t2982_ret = SC_ggi(510);
        local_9 = SC_MP_GetPlofHandle(SC_ggi(510));
        t2998_ret = SC_P_GetName(ptr40);
        t3003_ret = SC_AnsiToUni(SC_P_GetName(ptr40), &local_379);
        t3012_ret = SC_AnsiToUni("'disconnected'", &local_379);
        t3021_ret = SC_Wtxt(5107);
        t3028_ret = swprintf(5107, SC_Wtxt(5107), &local_379, gCLN_CurStep);
        local_314 = &local_315;
        local_8 = SC_PC_Get();
        SC_P_GetInfo(ptr37, &player_info);
        t3057_ret = SC_ggi(502);
        func_0334(t3057_ret);
        local_314 = SC_Wtxt(5111);
        t3085_ret = SC_Wtxt(5110);
        t3093_ret = swprintf(5110, SC_Wtxt(5110), gCLN_CurStep - 1);
        local_314 = &local_315;
        local_314 = SC_Wtxt(5113);
        t3121_ret = SC_Wtxt(5112);
        t3129_ret = swprintf(5112, SC_Wtxt(5112), gCLN_CurStep - 1);
        local_314 = &local_315;
        t3147_ret = SC_ggi(510);
        local_9 = SC_MP_GetPlofHandle(SC_ggi(510));
        t3163_ret = SC_P_GetName(ptr40);
        t3168_ret = SC_AnsiToUni(SC_P_GetName(ptr40), &local_379);
        t3177_ret = SC_AnsiToUni("'disconnected'", &local_379);
        local_8 = 5101;
        local_8 = 5103;
        local_8 = 5102;
        local_8 = 5104;
        t3231_ret = SC_Wtxt(ptr37);
        t3237_ret = swprintf(ptr37, SC_Wtxt(ptr37), &local_379);
        local_314 = &local_315;
        gCLN_ShowStartInfo = 0;
        t3259_ret = SC_ggi(510);
        local_9 = SC_MP_GetPlofHandle(SC_ggi(510));
        t3275_ret = SC_P_GetName(ptr40);
        t3280_ret = SC_AnsiToUni(SC_P_GetName(ptr40), &local_379);
        t3289_ret = SC_AnsiToUni("'disconnected'", &local_379);
        t3296_ret = SC_ggi(506);
        local_8 = 5105;
        local_8 = 5106;
        t3326_ret = SC_Wtxt(ptr38);
        t3332_ret = swprintf(ptr38, SC_Wtxt(ptr38), &local_379);
        local_314 = &local_315;
        gCLN_ShowStartInfo = 0;
        SC_GetScreenRes(&local_411, &local_412);
        t3357_ret = SC_Fnt_GetWidthW(ptr56, 1.0f);
        local_411 = 1.0f - SC_Fnt_GetWidthW(ptr56, 1.0f);
        local_412 = 0.5f * ptr64 - 40.0f;
        local_412 = 15.0f;
        SC_Fnt_WriteW(ptr62 * 0.5f, ptr64, ptr56, 1.0f, -1);
        break;
    case 5:
        &idx.fval1 = 0.1f;
        local_8 = 0;
        abl_lists--;
        abl_list[ptr38] = tmp537;
        local_8 = ptr38 + 1;
        &idx.fval1 = 0.1f;
        func_0155(gNextRecover);
        &idx.fval1 = gNextRecover;
        func_0119(gNextRecover);
        &idx.fval1 = gNextRecover + local_421;
        &idx.fval1 = 3.0f;
        &idx.fval1 = -1.0f;
        break;
    case 6:
        local_13 = info->param2;
        local_9 = param_0->field_4;
        local_9 = 1 - ptr40;
        local_10 = 0;
        local_10 = gCurStep - 1 - rand() % 2;
        local_10 = 0;
        local_10 = gCurStep;
        local_10 = gSteps - 1;
        local_8 = SC_MP_SRV_GetBestDMrecov((&gRec) + ptr40 * 3072 + ptr * 512, tmp577, (&gRecTimer) + ptr40 * 768 + ptr * 128, 3.0f);
        (&gRecTimer) + ptr40 * 768 + ptr * 128 + ptr27 * 4 = 3.0f;
        ptr66 = tmp596;
        break;
    case 10:
        gTime = 0;
        SC_ZeroMem(&gSidePoints, 8);
        func_0249();
        SC_MP_SetInstantRecovery(1);
        SC_MP_RestartMission();
        SC_MP_RecoverAllNoAiPlayers();
        gMission_phase = 0;
        SC_sgi(503, gMission_phase);
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
        local_8 = 0;
        (&local_296) + tmp26 * 4 = 1;
        local_8 = ptr27 + 1;
        gMission_starting_timer -= info->elapsed_time;
        SC_MP_SetInstantRecovery(0);
        gMission_phase = 1;
        gMission_afterstart_time = 0;
        SC_sgi(503, gMission_phase);
        func_0294();
        SC_MP_SRV_InitGameAfterInactive();
        SC_MP_RestartMission();
        SC_MP_RecoverAllNoAiPlayers();
        gMission_starting_timer = 8.0f;
        SC_MP_SetInstantRecovery(1);
        gMission_phase = 0;
        gMission_afterstart_time = 0;
        SC_sgi(503, gMission_phase);
        func_0852();
        func_0294();
        break;
    }
block_167:
block_238:
block_271:
block_274:
block_318:
block_403:
block_430:
block_446:
block_451:
block_454:
}

