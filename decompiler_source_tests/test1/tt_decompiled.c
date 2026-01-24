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
        if (!(gTime > ((float)gEndValue))) break;
        SC_MP_LoadNextMap();
        return TRUE;
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
    return FALSE;
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
    SC_sgi(500, gSidePoints[0]);
    SC_sgi(501, gSidePoints[1]);
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
    case 3:
        return FALSE;
    }
    return TRUE;
}

void func_0355(void) {
    int data_;
    int data_1965;
    int data_1965_v1;
    int data_1965_v2;
    int n;

    switch (gMission_phase) {
    case 3:
        gSidePoints[(1 - gAttackingSide)]++;
        func_0249();
        SC_sgi(506, 1 - gAttackingSide);
        SC_sgi(509, 1 - gAttackingSide);
        if ((gMainPhase % 2)) {
            gMainPhase++;
        } else {
            gMainPhase += 2;
        }
        break;
    case 2:
        SC_sgi(509, gAttackingSide);
        if ((gMainPhase % 2)) {
            gSidePoints[gAttackingSide]++;
            func_0249();
            SC_sgi(506, gAttackingSide);
        } else {
            gMissionTimeToBeat = gMissionTimePrev - gMissionTime;
        }
        gMainPhase++;
        break;
    }
    SC_sgi(502, gMainPhase);
    gAttackingSide = func_0334(gMainPhase);
    SC_sgi(507, 6);
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
                local_2 = 1;
            } else {
            }
        }
        if (local_41 == 0) {
            local_1 = 1;
        } else {
            if (local_41 == 1) {
                local_0 = 1;
            } else {
            }
        }
        local_2 = 1;
        if (local_0) {
        } else {
        }
        SC_DUMMY_Set_DoNotRenHier2(tmp13, 1);
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
        SC_DUMMY_Set_DoNotRenHier2(tmp29, 1);
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
        local_5[ptr].z = 1.0f;
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
        if (local_0 > 0) {
            local_1 = 1;
        } else {
            return;
        }
        break;
    case 1:
        if (local_0 < 0) {
            local_1 = 0;
        } else {
        }
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
    t827_ret = SC_MP_SRV_P_SetSideClass(param_0, ptr, 1 + 20 * ptr);
    if (abl_lists < 64) {
        abl_list[abl_lists] = param_1;
        abl_lists++;
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

    t1037_ret = SC_ggi(502);
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

int ScriptMain(s_SC_NET_info *info) {
    int local_10;  // Auto-generated
    int local_11;  // Auto-generated
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
    int t2087_ret;  // Auto-generated
    int t2096_ret;  // Auto-generated
    int t2105_ret;  // Auto-generated
    int t2286_ret;  // Auto-generated
    int t2484_ret;  // Auto-generated
    int t2513_ret;  // Auto-generated
    int t2757_ret;  // Auto-generated
    int t2769_ret;  // Auto-generated
    int t2813_ret;  // Auto-generated
    int t2823_ret;  // Auto-generated
    int t2831_ret;  // Auto-generated
    int t2852_ret;  // Auto-generated
    int t2915_ret;  // Auto-generated
    int t2982_ret;  // Auto-generated
    int t2986_ret;  // Auto-generated
    int t3012_ret;  // Auto-generated
    int t3028_ret;  // Auto-generated
    int t3039_ret;  // Auto-generated
    int t3093_ret;  // Auto-generated
    int t3129_ret;  // Auto-generated
    int t3147_ret;  // Auto-generated
    int t3151_ret;  // Auto-generated
    int t3168_ret;  // Auto-generated
    int t3177_ret;  // Auto-generated
    int t3237_ret;  // Auto-generated
    int t3259_ret;  // Auto-generated
    int t3263_ret;  // Auto-generated
    int t3280_ret;  // Auto-generated
    int t3289_ret;  // Auto-generated
    int t3296_ret;  // Auto-generated
    int t3332_ret;  // Auto-generated
    int t3562_ret;  // Auto-generated
    int t3622_ret;  // Auto-generated
    int y;  // Auto-generated
    int z;  // Auto-generated

    c_Vector3 t1567_0;
    c_Vector3 t2307_0;
    c_Vector3 vec;
    char local_0[32];
    char* t2998_ret;
    char* t3163_ret;
    char* t3275_ret;
    float data_1976;
    float local_411;
    float local_421;
    float ptr62;
    float t1856_ret;
    float t3357_ret;
    int data_;
    int data_1;
    int data_1549;
    int data_1957;
    int data_1958;
    int data_1959;
    int data_1964;
    int data_1968;
    int data_1968_v1;
    int data_1969;
    int data_1970;
    int data_1972;
    int data_1979;
    int data_1982;
    int data_1983;
    int data_1984;
    int data_2677;
    int data_2682;
    int i;
    int idx;
    int idx1;
    int idx2;
    int idx3;
    int j;
    int k;
    int local_12;
    int local_13;
    int local_294;
    int local_296;
    int local_298;
    int local_315;
    int local_379;
    int local_412;
    int local_418;
    int local_419;
    int local_420;
    int local_8;
    int n;
    int obj;
    int precov;
    int ptr;
    int ptr27;
    int ptr28;
    int ptr36;
    int ptr40;
    int ptr41;
    int ptr49;
    int ptr50;
    int ptr51;
    int ptr53;
    int ptr54;
    int ptr55;
    int ptr56;
    int ptr57;
    int ptr58;
    int ptr59;
    int ptr60;
    int ptr61;
    int ptr64;
    int ptr66;
    int side;
    int side10;
    int side11;
    int side2;
    int side3;
    int side4;
    int side5;
    int side6;
    int side7;
    int side8;
    int side9;
    int sideB;
    int sphere;
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
    int t2033_;
    int t2933_ret;
    int t3057_ret;
    int tmp102;
    int tmp109;
    int tmp116;
    int tmp122;
    int tmp183;
    int tmp193;
    int tmp217;
    int tmp22;
    int tmp242;
    int tmp247;
    int tmp249;
    int tmp252;
    int tmp255;
    int tmp258;
    int tmp26;
    int tmp265;
    int tmp268;
    int tmp271;
    int tmp274;
    int tmp35;
    int tmp353;
    int tmp377;
    int tmp382;
    int tmp388;
    int tmp397;
    int tmp416;
    int tmp423;
    int tmp427;
    int tmp532;
    int tmp537;
    int tmp577;
    int tmp596;
    s_SC_HUD_MP_icon icon[32];
    s_SC_MP_EnumPlayers enum_pl[32];
    s_SC_MP_Recover t2510_0;
    s_SC_MP_Recover t2617_0;
    s_SC_MP_Recover t3600_0;
    s_SC_MP_SRV_settings srv_settings;
    s_SC_MP_hud hudinfo;
    s_SC_P_getinfo player_info;
    s_sphere t2767_0;
    unsigned short* t3003_ret;
    ushort* local_314;
    ushort* t2881_ret;
    ushort* t2945_ret;
    ushort* t2955_ret;
    ushort* t3021_ret;
    ushort* t3073_ret;
    ushort* t3085_ret;
    ushort* t3109_ret;
    ushort* t3121_ret;
    ushort* t3231_ret;
    ushort* t3326_ret;
    void* local_295;
    void* t2294_ret;
    void* t2314_ret;
    void* t2330_ret;
    void* t2346_ret;

    switch (info->message) {
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
            (&gRecTimer) + ptr28 * 768 + ptr40 * 128 + ptr * 4 -= info->elapsed_time;
            local_10 = ptr + 1;
            local_9 = ptr40 + 1;
            local_8 = ptr28 + 1;
        }
        gNextRecover -= info->elapsed_time;
        if (gNextRecover < 0.0f) {
            gNextRecover = func_0119();
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
        t1752_ret = SC_ggi(503);
        break;
    case 9:
        SC_sgi(GVAR_MP_MISSIONTYPE, 9);
        gEndRule = param_0->field_4;
        gEndValue = info->param2;
        gTime = 0;
        SC_MP_EnableBotsFromScene(0);
        break;
    case 0:
        if (gSidePoints[0] + gSidePoints[1] != 0) {
            gSidePoints[0] = 0;
            gSidePoints[1] = 0;
            func_0249();
        }
        break;
    case 1:
        t2087_ret = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_USflag.BES");
        g_FPV_UsFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_USflag.BES");
        t2096_ret = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_VCflag.BES");
        g_FPV_VcFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_VCflag.BES");
        t2105_ret = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_emptyflag.BES");
        g_FPV_NeFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_emptyflag.BES");
        SC_MP_SRV_SetForceSide(-1);
        SC_MP_SetChooseValidSides(3);
        SC_MP_SRV_SetClassLimit(18, 0);
        SC_MP_SRV_SetClassLimit(19, 0);
        SC_MP_SRV_SetClassLimit(39, 0);
        SC_MP_GetSRVsettings(&srv_settings);
        // Loop header - Block 276 @2136
        for (ptr28 = 0; ptr28 < 6; ptr28 = ptr28 + 1) {
            SC_MP_SRV_SetClassLimit(ptr28 + 1, tmp242);
            SC_MP_SRV_SetClassLimit(ptr28 + 21, tmp247);
            local_8 = ptr28 + 1;
        }
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
        if (!info->param2) break;
        SC_ZeroMem(&gFlagNod, 72);
        // Loop header - Block 280 @2276
        for (ptr28 = 0; ptr28 < 6; ptr28 = ptr28 + 1) {
            t2286_ret = sprintf(local_0, "TT_flag_%d", ptr28);
            t2294_ret = SC_NOD_GetNoMessage(0, local_0);
            local_295 = SC_NOD_GetNoMessage(0, local_0);
            if (ptr54) {
                SC_NOD_GetPivotWorld(ptr54, &gFlagPos[ptr28]);
                t2314_ret = SC_NOD_Get(ptr54, &tmp285);
                gFlagNod[ptr28].field_0 = SC_NOD_Get(ptr54, &tmp285);
                t2330_ret = SC_NOD_Get(ptr54, &tmp286);
                gFlagNod[ptr28].field_4 = SC_NOD_Get(ptr54, &tmp286);
                t2346_ret = SC_NOD_Get(ptr54, &tmp287);
                gFlagNod[ptr28].field_8 = SC_NOD_Get(ptr54, &tmp287);
            } else {
                local_8 = ptr28 + 1;
            }
            local_8 = ptr28 + 1;
        }
        if (!param_0->field_4) break;
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
        // Loop header - Block 286 @2445
        for (ptr = 0; ptr < 2; ptr = ptr + 1) {
            if (ptr) {
                local_294 = 68;
            } else {
                local_294 = 65;
            }
            local_9 = 0;
            local_8 = 0;
            t2484_ret = sprintf(local_0, "TT_%c%d_%d", ptr55, ptr40, ptr28);
            if (t2513_ret = SC_NET_FillRecover((&gRec) + ptr * 3072 + ptr40 * 512 + tmp353 * 16, local_0)) {
                gRecs[ptr] + ptr40 * 4++;
            } else {
                local_8 = ptr28 + 1;
            }
            if (tmp377) {
                local_8 = 32 - tmp382;
                SC_MP_GetRecovers(tmp388, (&gRec) + ptr * 3072 + ptr40 * 512 + tmp397 * 16, &local_8);
                gRecs[ptr] + ptr40 * 4 += ptr28;
            } else {
                local_9 = ptr40 + 1;
            }
            local_10 = ptr + 1;
        }
        gSteps = 0;
        // Loop header - Block 302 @2670
        for (ptr28 = 0; ptr28 < 6; ptr28 = ptr28 + 1) {
            if (tmp416) {
                gSteps = ptr28 + 1;
            } else {
                local_8 = ptr28 + 1;
            }
            local_8 = ptr28 + 1;
        }
        // Loop header - Block 307 @2702
        for (ptr28 = 0; ptr28 < gSteps; ptr28 = ptr28 + 1) {
            SC_Log(3, "TurnTable recovers #%d: att:%d  def:%d", ptr28, tmp423, tmp427);
            local_8 = ptr28 + 1;
        }
        SC_ZeroMem(&gRecTimer, 1536);
        // Loop header - Block 310 @2745
        for (ptr36 = 0; ptr36 < (gSteps - 1); ptr36 = ptr36 + 1) {
            t2757_ret = sprintf(local_0, "TTS_%d", ptr36);
            if (t2769_ret = SC_GetScriptHelper(local_0, &gStepSwitch[ptr36])) {
            } else {
                SC_message(&tmp435, local_0);
            }
            local_8 = ptr36 + 1;
        }
        SC_sgi(508, gSteps);
        break;
    case 2:
        local_8 = 0;
        local_314 = 0;
        local_298 = 0;
        t2813_ret = SC_ggi(502);
        local_10 = SC_ggi(502);
        if (t2823_ret = SC_ggi(503)) {
            t2831_ret = SC_ggi(503);
            gCLN_gamephase = SC_ggi(503);
            t2852_ret = SC_ggi(509);
            SC_SND_PlaySound2D(11117);
            SC_SND_PlaySound2D(11116);
        }
        break;
    case 5:
        if (info->param2) {
            &idx.fval1 = 0.1f;
        } else {
            local_8 = 0;
            &idx.fval1 = 3.0f;
            &idx.fval1 = -1.0f;
        }
        break;
    case 6:
        local_13 = info->param2;
        local_9 = param_0->field_4;
        if (gAttackingSide) {
            local_9 = 1 - ptr40;
        }
        if (ptr40) {
            local_10 = 0;
            t3562_ret = rand();
            local_10 = gCurStep - 1 - rand() % 2;
            local_10 = 0;
        } else {
            local_10 = gCurStep;
            local_10 = gSteps - 1;
        }
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
            SC_sgi(503, gMission_phase);
            func_0294();
            SC_MP_SRV_InitGameAfterInactive();
            SC_MP_RestartMission();
            SC_MP_RecoverAllNoAiPlayers();
            gMission_starting_timer = 8.0f;
            local_8 = 0;
            local_9 = 0;
            local_10 = 0;
            (&gRecTimer) + ptr28 * 768 + ptr40 * 128 + ptr * 4 -= info->elapsed_time;
            local_10 = ptr + 1;
            local_9 = ptr40 + 1;
            local_8 = ptr28 + 1;
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
            local_8 = ptr28 + 1;
            gPhaseTimer -= info->elapsed_time;
            gNoActiveTime = 0;
            gMission_phase = 0;
            SC_sgi(503, gMission_phase);
            func_0852();
            SC_MP_SetInstantRecovery(1);
            SC_MP_RecoverAllNoAiPlayers();
            return TRUE;
        }
        if (gMission_starting_timer <= 0.0f && gMission_phase > 0) {
            gMission_phase = 0;
            gMission_afterstart_time = 0;
            SC_sgi(503, gMission_phase);
            func_0852();
            func_0294();
        }
    }
    if (local_419 == 0) {
        t1764_ret = SC_ggi(508);
        func_0498(SC_ggi(508) - 1, 2);
    } else {
        if (local_419 == 1) {
            if (t1782_ret = SC_ggi(507) && t1800_ret = SC_ggi(508) && gCLN_CurStep > 0) {
                gCLN_ShowInfo = 5.0f;
                SC_SND_PlaySound2D(10425);
            }
            t1823_ret = SC_ggi(502);
            func_0334(SC_ggi(502));
            func_0498(local_420, gCLN_CurStep);
        }
    }
    t1839_ret = SC_ggi(505);
    if (505 != SC_ggi(505)) {
        t1847_ret = SC_ggi(505);
        gCLN_MissionTimePrevID = SC_ggi(505);
        t1856_ret = SC_ggf(504);
        gCLN_MissionTime = SC_ggf(504);
    } else {
        if (t1866_ret = SC_ggi(503)) {
            gCLN_MissionTime -= info->elapsed_time;
        }
    }
    local_8 = 0;
    // Loop header - Block 260 @1884
    for (ptr28 = 0; ptr28 < 2; ptr28 = ptr28 + 1) {
        t1891_0 = 500 + ptr28;
        t1893_ret = SC_ggi(t1891_0);
        gCLN_SidePoints[ptr28] = SC_ggi(t1891_0);
        SC_MP_SetSideStats(ptr28, 0, tmp183);
        local_299[ptr28].y = 1;
        local_299[ptr28].icon_id = 3 * ptr28;
        local_299[ptr28].z = tmp193;
        local_299[ptr28].field_12 = -1140850689;
        local_8 = ptr28 + 1;
        continue;  // back to loop header @1884
    }
    local_11 = 2;
    if (gCLN_MissionTime > 0.0f && t1975_ret = SC_ggi(503)) {
        local_299[ptr51].field_12 = -1140850689;
        local_299[ptr51].icon_id = 6;
        if (t2000_ret = SC_ggi(503)) {
            local_299[ptr51].z = 0;
        } else {
            (int)gCLN_MissionTime + 0.99f = tmp217;
        }
        local_299[ptr51].y = 2;
        local_11 = ptr51 + 1;
    }
    if (local_419 == 0) {
        if (gCLN_ShowWaitingInfo <= 0.0f) {
            t2881_ret = SC_Wtxt(1076);  // 1076: "Waiting for more players."
            local_314 = SC_Wtxt(1076);  // 1076: "Waiting for more players.";
        }
        gCLN_ShowStartInfo = 0;
    } else {
        if (local_419 == 1) {
            gCLN_ShowWaitingInfo = 3.0f;
            if (gCLN_ShowStartInfo == 0.0f) {
                gCLN_ShowStartInfo = 3.0f;
            }
            if (gCLN_ShowStartInfo > 0.0f) {
                t2915_ret = SC_PC_Get();
                local_8 = SC_PC_Get();
                if (ptr28) {
                    SC_P_GetInfo(ptr28, &player_info);
                    t2933_ret = SC_ggi(502);
                    func_0334(t2933_ret);
                    if (t2933_ret == local_421) {
                        t2945_ret = SC_Wtxt(5108);
                        local_314 = SC_Wtxt(5108);
                    } else {
                        t2955_ret = SC_Wtxt(5109);
                        local_314 = SC_Wtxt(5109);
                    }
                    SC_GameInfoW(ptr56);
                    local_314 = 0;
                }
            } else {
                if (gCLN_ShowInfo > 0.0f && gCLN_CurStep > 0) {
                    t2982_ret = SC_ggi(510);
                    t2986_ret = SC_MP_GetPlofHandle(SC_ggi(510));
                    local_9 = SC_MP_GetPlofHandle(SC_ggi(510));
                    if (ptr40) {
                        t2998_ret = SC_P_GetName(ptr40);
                        t3003_ret = SC_AnsiToUni(SC_P_GetName(ptr40), &local_379);
                    } else {
                        t3012_ret = SC_AnsiToUni("'disconnected'", &local_379);
                    }
                    t3021_ret = SC_Wtxt(5107);
                    t3028_ret = swprintf(5107, SC_Wtxt(5107), &local_379, gCLN_CurStep);
                    local_314 = &local_315;
                    SC_GetScreenRes(&local_411, &local_412);
                    t3357_ret = SC_Fnt_GetWidthW(ptr57, 1.0f);
                    local_411 = 1.0f - SC_Fnt_GetWidthW(ptr57, 1.0f);
                    local_412 = 0.5f * ptr64 - 40.0f;
                    local_412 = 15.0f;
                    SC_Fnt_WriteW(ptr62 * 0.5f, ptr64, ptr57, 1.0f, -1);
                }
                t3039_ret = SC_PC_Get();
                local_8 = SC_PC_Get();
                if (ptr28) {
                    SC_P_GetInfo(ptr28, &player_info);
                    t3057_ret = SC_ggi(502);
                    func_0334(t3057_ret);
                    if (t3057_ret == local_421) {
                        if (gCLN_CurStep == 1) {
                            t3073_ret = SC_Wtxt(5111);
                            local_314 = SC_Wtxt(5111);
                        } else {
                            t3085_ret = SC_Wtxt(5110);
                            t3093_ret = swprintf(5110, SC_Wtxt(5110), gCLN_CurStep - 1);
                            local_314 = &local_315;
                        }
                    } else {
                        if (gCLN_CurStep == 1) {
                            t3109_ret = SC_Wtxt(5113);
                            local_314 = SC_Wtxt(5113);
                        } else {
                            t3121_ret = SC_Wtxt(5112);
                            t3129_ret = swprintf(5112, SC_Wtxt(5112), gCLN_CurStep - 1);
                            local_314 = &local_315;
                        }
                    }
                }
            }
        } else {
            if (local_419 == 2) {
                t3147_ret = SC_ggi(510);
                t3151_ret = SC_MP_GetPlofHandle(SC_ggi(510));
                local_9 = SC_MP_GetPlofHandle(SC_ggi(510));
                if (ptr40) {
                    t3163_ret = SC_P_GetName(ptr40);
                    t3168_ret = SC_AnsiToUni(SC_P_GetName(ptr40), &local_379);
                } else {
                    t3177_ret = SC_AnsiToUni("'disconnected'", &local_379);
                }
                if (local_420 == 0) {
                    local_8 = 5101;
                } else {
                    if (local_420 == 1) {
                        local_8 = 5103;
                    } else {
                        if (local_420 == 2) {
                            local_8 = 5102;
                        } else {
                            if (local_420 == 3) {
                                local_8 = 5104;
                            }
                        }
                    }
                }
                t3231_ret = SC_Wtxt(ptr28);
                t3237_ret = swprintf(ptr28, SC_Wtxt(ptr28), &local_379);
                local_314 = &local_315;
                gCLN_ShowStartInfo = 0;
            } else {
                if (local_419 == 3) {
                    t3259_ret = SC_ggi(510);
                    t3263_ret = SC_MP_GetPlofHandle(SC_ggi(510));
                    local_9 = SC_MP_GetPlofHandle(SC_ggi(510));
                    if (ptr40) {
                        t3275_ret = SC_P_GetName(ptr40);
                        t3280_ret = SC_AnsiToUni(SC_P_GetName(ptr40), &local_379);
                    } else {
                        t3289_ret = SC_AnsiToUni("'disconnected'", &local_379);
                    }
                    t3296_ret = SC_ggi(506);
                    if (local_420 == 0) {
                        local_8 = 5105;
                    } else {
                        if (local_420 == 1) {
                            local_8 = 5106;
                        }
                    }
                    t3326_ret = SC_Wtxt(ptr28);
                    t3332_ret = swprintf(ptr28, SC_Wtxt(ptr28), &local_379);
                    local_314 = &local_315;
                    gCLN_ShowStartInfo = 0;
                }
            }
        }
    }
    // Loop header - Block 410 @3415
    for (ptr28 = 0; ptr28 < abl_lists; ptr28 = ptr28 + 1) {
        if (param_0->field_4 == tmp532) {
            abl_lists--;
            abl_list[ptr28] = tmp537;
            if (ptr27 < abl_lists) {
                &idx.fval1 = 0.1f;
            } else {
                if (func_0155(gNextRecover)) {
                    &idx.fval1 = gNextRecover;
                } else {
                    func_0119(gNextRecover);
                    &idx.fval1 = gNextRecover + local_421;
                }
            }
        } else {
            local_8 = ptr28 + 1;
        }
    }
    t3622_ret = SC_MP_SRV_GetBestDMrecov((&gRec) + ptr40 * 3072 + ptr * 512, tmp577, (&gRecTimer) + ptr40 * 768 + ptr * 128, 3.0f);
    local_8 = SC_MP_SRV_GetBestDMrecov((&gRec) + ptr40 * 3072 + ptr * 512, tmp577, (&gRecTimer) + ptr40 * 768 + ptr * 128, 3.0f);
    (&gRecTimer) + ptr40 * 768 + ptr * 128 + ptr27 * 4 = 3.0f;
    ptr66 = tmp596;
}

