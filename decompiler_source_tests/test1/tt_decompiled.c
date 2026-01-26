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
    goto block_6;
block_3:
block_6:
    SC_MP_EndRule_SetTimeLeft(gTime, gMission_phase);
block_7:
    SC_MP_LoadNextMap();
    return TRUE;
block_8:
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

    SC_MP_SRV_GetAtgSettings(&atg_settings);
block_22:
    return atg_settings.tt_respawntime;
block_23:
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

    SC_MP_SRV_GetAtgSettings(&atg_settings);
block_36:
    return atg_settings.tt_timelimit;
block_37:
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
    if (!gMissionTime_update < 0.0f) {
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
    }
block_50:
block_52:
block_54:
    return TRUE;
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
            gSidePoints[gAttackingSide]++;
            func_0249();
            SC_sgi(506, gAttackingSide);
        } else {
            gMissionTimeToBeat = gMissionTimePrev - gMissionTime;
        }
        break;
    }
block_57:
block_59:
    gMainPhase++;
block_61:
block_63:
block_68:
    SC_sgi(502, gMainPhase);
    gAttackingSide = func_0334(gMainPhase);
    SC_sgi(507, 6);
    return;
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
    SC_MP_FpvMapSign_Set(ptr1, &local_5);
    return;
block_74:
block_77:
block_80:
block_71:
    local_0 = 0;
    local_1 = 0;
    local_2 = 0;
block_72:
block_75:
    local_1 = 1;
block_78:
    local_0 = 1;
block_81:
    local_2 = 1;
block_82:
block_83:
block_84:
    local_2 = 1;
block_85:
block_86:
block_87:
block_88:
block_89:
block_90:
    SC_DUMMY_Set_DoNotRenHier2(tmp13, 1);
block_91:
block_92:
block_93:
block_94:
block_95:
block_96:
    SC_DUMMY_Set_DoNotRenHier2(tmp21, 1);
block_97:
block_98:
block_99:
block_100:
block_101:
block_102:
    SC_DUMMY_Set_DoNotRenHier2(tmp29, 1);
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
}

int func_0752(int param_0, int param_1) {
    int idx;
    int n;
    s_SC_P_getinfo player_info;

    switch (local_2.field_8) {
    case 0:
        break;
    case 1:
        break;
    }
block_115:
    return;
block_120:
    SC_P_GetInfo(param_0, &player_info);
block_124:
block_128:
    return;
block_114:
block_116:
    local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
block_117:
block_118:
block_119:
    return;
block_129:
    t827_ret = SC_MP_SRV_P_SetSideClass(param_0, ptr, 1 + 20 * ptr);
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

block_134:
    return;
block_143:
block_145:
    return;
block_150:
block_154:
    return;
block_157:
    return;
block_133:
block_135:
    local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
block_136:
block_137:
block_138:
    return;
block_139:
block_140:
    local_1 = 0;
    local_2 = local_0 / 2;
block_141:
    local_1 = 1;
    local_2 = tmp6 / 2;
block_142:
    local_265 = 64;
block_144:
    while (ptr1 != 0) {
        local_266 = rand() % obj;
        local_264 = ptr4;
        local_264 = ptr5 + 1;
        local_264 = 0;
        t1006_ret = SC_MP_SRV_P_SetSideClass(tmp21, 1 - ptr, 1 + 20 * ((1 - ptr)));
        local_8[ptr6].id = 0;
        local_2 = ptr1 - 1;
    }
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
    goto block_164;
    local_256 = 0;
    for (obj = 0; obj < ptr1; obj = obj + 1) {
        local_256 = obj + 1;
    }
    if (!(side2 == 2)) {
        SC_MP_RecoverPlayer(tmp5);
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
block_171:
block_181:
    gMission_starting_timer -= info->elapsed_time;
block_210:
block_230:
block_236:
block_238:
block_255:
block_257:
block_269:
    SC_MP_SetIconHUD(&icon, ptr52);
block_271:
block_274:
block_316:
block_318:
block_323:
block_337:
block_347:
block_403:
block_405:
    &idx.fval1 = 0.1f;
block_428:
block_430:
block_446:
block_449:
    gCLN_ShowInfo = 0;
    SC_MP_SRV_ClearPlsStats();
block_451:
block_454:
block_241:
block_242:
    gCLN_ShowWaitingInfo -= info->elapsed_time;
block_243:
    t1752_ret = SC_ggi(503);
block_245:
block_246:
    func_0498(SC_ggi(508) - 1, 2);
block_248:
block_249:
block_250:
    gCLN_CurStep = SC_ggi(507);
block_251:
block_252:
block_253:
    gCLN_ShowInfo = 5.0f;
    SC_SND_PlaySound2D(10425);
block_254:
    t1823_ret = SC_ggi(502);
    func_0334(SC_ggi(502));
    func_0498(local_420, gCLN_CurStep);
block_256:
    gCLN_MissionTimePrevID = SC_ggi(505);
    gCLN_MissionTime = SC_ggf(504);
block_258:
    gCLN_MissionTime -= info->elapsed_time;
block_259:
    local_8 = 0;
    for (ptr29 = 0; ptr29 < 2; ptr29 = ptr29 + 1) {
        t1891_0 = 500 + ptr29;
        gCLN_SidePoints[ptr29] = SC_ggi(t1891_0);
        SC_MP_SetSideStats(ptr29, 0, tmp183);
        local_299[ptr29].y = 1;
        local_299[ptr29].icon_id = 3 * ptr29;
        local_299[ptr29].z = tmp193;
        local_299[ptr29].field_12 = -1140850689;
        local_8 = ptr29 + 1;
    }
block_262:
    local_11 = 2;
block_263:
block_264:
block_265:
    local_299[ptr51].field_12 = -1140850689;
    local_299[ptr51].icon_id = 6;
block_266:
    local_299[ptr51].z = 0;
block_267:
    (int)gCLN_MissionTime + 0.99f = tmp217;
block_268:
    local_299[ptr51].y = 2;
    local_11 = ptr51 + 1;
    for (ptr29 = 0; ptr29 < 6; ptr29 = ptr29 + 1) {
        SC_MP_SRV_SetClassLimit(ptr29 + 1, tmp242);
        SC_MP_SRV_SetClassLimit(ptr29 + 21, tmp247);
        local_8 = ptr29 + 1;
    }
block_278:
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
block_279:
    SC_ZeroMem(&gFlagNod, 72);
    local_8 = 0;
    for (ptr29 = 0; ptr29 < 6; ptr29 = ptr29 + 1) {
        t2286_ret = sprintf(&n, "TT_flag_%d", ptr29);
        local_295 = SC_NOD_GetNoMessage(0, &local_0);
        SC_NOD_GetPivotWorld(ptr54, &gFlagPos[ptr29]);
        gFlagNod[ptr29].field_0 = SC_NOD_Get(ptr54, &tmp285);
        gFlagNod[ptr29].field_4 = SC_NOD_Get(ptr54, &tmp286);
        gFlagNod[ptr29].field_8 = SC_NOD_Get(ptr54, &tmp287);
        local_8 = ptr29 + 1;
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
    for (ptr46 = 0; ptr46 < 2; ptr46 = ptr46 + 1) {
        local_294 = 68;
        local_294 = 65;
        local_9 = 0;
        local_8 = 0;
        t2484_ret = sprintf(&local_0, "TT_%c%d_%d", ptr55, ptr, ptr29);
        gRecs[ptr46] + ptr * 4++;
        local_8 = ptr29 + 1;
        local_8 = 32 - tmp382;
        SC_MP_GetRecovers(tmp388, (&gRec) + ptr46 * 3072 + ptr * 512 + tmp397 * 16, &local_8);
        gRecs[ptr46] + ptr * 4 += ptr29;
        local_9 = ptr + 1;
        local_10 = ptr46 + 1;
    }
block_301:
    gSteps = 0;
    local_8 = 0;
    for (ptr29 = 0; ptr29 < 6; ptr29 = ptr29 + 1) {
        gSteps = ptr29 + 1;
        local_8 = ptr29 + 1;
    }
block_306:
    local_8 = 0;
    for (ptr29 = 0; ptr29 < gSteps; ptr29 = ptr29 + 1) {
        SC_Log(3, "TurnTable recovers #%d: att:%d  def:%d", ptr29, tmp423, tmp427);
        local_8 = ptr29 + 1;
    }
block_309:
    SC_ZeroMem(&gRecTimer, 1536);
    local_8 = 0;
    for (ptr29 = 0; ptr29 < (gSteps - 1); ptr29 = ptr29 + 1) {
        t2757_ret = sprintf(&local_0, "TTS_%d", ptr29);
        SC_message(&tmp435, &local_0);
        local_8 = ptr29 + 1;
    }
block_315:
    SC_sgi(508, gSteps);
block_330:
block_332:
block_333:
block_334:
    local_314 = SC_Wtxt(1076);  // 1076: "Waiting for more players.";
block_335:
    gCLN_ShowStartInfo = 0;
block_338:
    gCLN_ShowWaitingInfo = 3.0f;
block_339:
    gCLN_ShowStartInfo = 3.0f;
block_340:
block_341:
    local_8 = SC_PC_Get();
block_342:
    SC_P_GetInfo(ptr29, &player_info);
    t2933_ret = SC_ggi(502);
    func_0334(t2933_ret);
block_343:
    local_314 = SC_Wtxt(5108);
block_344:
    local_314 = SC_Wtxt(5109);
block_345:
    SC_GameInfoW(ptr56);
    local_314 = 0;
block_346:
block_348:
block_349:
block_350:
    t2982_ret = SC_ggi(510);
    local_9 = SC_MP_GetPlofHandle(SC_ggi(510));
block_351:
    t2998_ret = SC_P_GetName(ptr);
    t3003_ret = SC_AnsiToUni(SC_P_GetName(ptr), &local_379);
block_352:
    t3012_ret = SC_AnsiToUni("'disconnected'", &local_379);
block_353:
    t3021_ret = SC_Wtxt(5107);
    t3028_ret = swprintf(5107, SC_Wtxt(5107), &local_379, gCLN_CurStep);
    local_314 = &local_315;
block_354:
    local_8 = SC_PC_Get();
block_355:
    SC_P_GetInfo(ptr29, &player_info);
    t3057_ret = SC_ggi(502);
    func_0334(t3057_ret);
block_356:
block_357:
    local_314 = SC_Wtxt(5111);
block_358:
    t3085_ret = SC_Wtxt(5110);
    t3093_ret = swprintf(5110, SC_Wtxt(5110), gCLN_CurStep - 1);
    local_314 = &local_315;
block_359:
block_360:
block_361:
    local_314 = SC_Wtxt(5113);
block_362:
    t3121_ret = SC_Wtxt(5112);
    t3129_ret = swprintf(5112, SC_Wtxt(5112), gCLN_CurStep - 1);
    local_314 = &local_315;
block_363:
block_365:
block_366:
    t3147_ret = SC_ggi(510);
    local_9 = SC_MP_GetPlofHandle(SC_ggi(510));
block_367:
    t3163_ret = SC_P_GetName(ptr);
    t3168_ret = SC_AnsiToUni(SC_P_GetName(ptr), &local_379);
block_368:
    t3177_ret = SC_AnsiToUni("'disconnected'", &local_379);
block_369:
block_371:
block_372:
    local_8 = 5101;
block_374:
block_375:
    local_8 = 5103;
block_377:
block_378:
    local_8 = 5102;
block_380:
block_381:
    local_8 = 5104;
block_382:
    t3231_ret = SC_Wtxt(ptr29);
    t3237_ret = swprintf(ptr29, SC_Wtxt(ptr29), &local_379);
    local_314 = &local_315;
    gCLN_ShowStartInfo = 0;
block_384:
block_385:
    t3259_ret = SC_ggi(510);
    local_9 = SC_MP_GetPlofHandle(SC_ggi(510));
block_386:
    t3275_ret = SC_P_GetName(ptr);
    t3280_ret = SC_AnsiToUni(SC_P_GetName(ptr), &local_379);
block_387:
    t3289_ret = SC_AnsiToUni("'disconnected'", &local_379);
block_388:
    t3296_ret = SC_ggi(506);
block_390:
block_391:
    local_8 = 5105;
block_393:
block_394:
    local_8 = 5106;
block_395:
    t3326_ret = SC_Wtxt(ptr29);
    t3332_ret = swprintf(ptr29, SC_Wtxt(ptr29), &local_379);
    local_314 = &local_315;
    gCLN_ShowStartInfo = 0;
block_396:
block_397:
    SC_GetScreenRes(&local_411, &local_412);
    local_411 = 1.0f - SC_Fnt_GetWidthW(ptr56, 1.0f);
block_398:
    local_412 = 0.5f * ptr64 - 40.0f;
block_399:
    local_412 = 15.0f;
block_400:
    SC_Fnt_WriteW(ptr62 * 0.5f, ptr64, ptr56, 1.0f, -1);
block_401:
block_433:
block_434:
block_435:
block_436:
    local_10 = 0;
block_437:
    local_10 = gCurStep - 1 - rand() % 2;
block_438:
block_439:
    local_10 = 0;
block_440:
block_441:
block_442:
    local_10 = gCurStep;
block_443:
    local_10 = gSteps - 1;
block_444:
    local_8 = SC_MP_SRV_GetBestDMrecov((&gRec) + ptr * 3072 + ptr45 * 512, tmp577, (&gRecTimer) + ptr * 768 + ptr45 * 128, 3.0f);
    (&gRecTimer) + ptr * 768 + ptr45 * 128 + ptr27 * 4 = 3.0f;
    ptr66 = tmp596;
block_456:
    return TRUE;
}

