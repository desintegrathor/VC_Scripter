// Structured decompilation of decompiler_source_tests/test1/tt.scr
// Functions: 15

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
int gSteps;
dword gRecs[12];
dword gRec[64];
dword gVar;
dword gVar11;
dword gVar1;
dword gVar2;
dword gVar8;
dword gVar9;
dword gVar3;
dword gVar4;
dword gVar6;
dword gVar5;
dword gVar10;
dword gVar7;
dword gVar12;
dword gRecTimer[384];
dword gStepSwitch[24];
int gEndRule;
int gEndValue;
int gTime;
dword gSidePoints[2];
dword gCLN_SidePoints[2];
int gCLN_gamephase;
int gMainPhase;
int gAttackingSide;
int gCurStep;
int gMission_phase;
float gNoActiveTime;
int gPhaseTimer;
int gMissionTime_update;
int gMissionTime;
float gMissionTimePrev;
int gMissionTimeToBeat;
int gCLN_MissionTimePrevID;
float gCLN_MissionTime;
int gCLN_CurStep;
int gCLN_ShowInfo;
int gCLN_ShowStartInfo;
int gCLN_ShowWaitingInfo;
int gMission_starting_timer;
int gMission_afterstart_time;
float gNextRecover;
dword gFlagNod[18];
dword gFlagPos[18];
dword gRespawn_id[12];
int g_FPV_UsFlag;
int g_FPV_VcFlag;
int g_FPV_NeFlag;

int _init(s_SC_NET_info *info) {
    c_Vector3 local_311;
    int n;
    int side;
    int sideB;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    return 0;  // FIX (06-05): Synthesized return value
}

int func_0050(float param_0) {
    c_Vector3 local_311;
    int data_;
    int n;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    block_3:
    switch (gEndRule) {
    case 0:
        if (tmp2) {
            data_ = tmp3;
        } else {
            SC_MP_EndRule_SetTimeLeft(data_, gMission_phase);
            if (tmp5) {
                SC_MP_LoadNextMap();
                return TRUE;
            }
            return 0;  // FIX (06-05): Synthesized return value
        }
        break;
    case 2:
        if (tmp9 && tmp12) {
        }
        SC_MP_LoadNextMap();
        return TRUE;
    default:
        SC_message("EndRule unsopported: %d", tmp1);
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0119(void) {
    c_Vector3 local_311;
    int m;
    int n;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings idx;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!tmp2) {
        return local_1->tt_respawntime;
    } else {
        tmp5 = SC_ggf(400);
        tmp5 = 30.0f;
        return tmp5;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0155(void) {
    c_Vector3 local_311;
    int m;
    int n;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings idx;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!tmp2) {
        tmp6 = tmp5;
        tmp6 = 5.0f;
        tmp6 = 10.0f;
        return tmp6;
    } else {
        tmp6 = SC_ggf(401);
        tmp6 = 10.0f;
        return tmp6;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0213(void) {
    c_Vector3 local_311;
    int m;
    int n;
    int side;
    int side2;
    int side3;
    int side4;
    int sideB;
    int tmp;
    int tmp1;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings idx;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!side2) {
        return local_1->tt_timelimit;
    } else {
        tmp = SC_ggf(402);
        tmp = 480.0f;
        return tmp;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

void func_0249(void) {
    c_Vector3 local_311;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    SC_sgi(500, tmp1);
    SC_sgi(501, tmp3);
    return;
}

void func_0264(float param_0) {
    c_Vector3 local_311;
    int idx;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    tmp1 = tmp;
    if (!tmp2) {
        tmp1 = 10.0f;
        SC_sgf(504, gMissionTime);
        SC_ggi(505);
        SC_sgi(505, tmp3);
    } else {
        return;
    }
    return;
}

void func_0294(void) {
    c_Vector3 local_311;
    int n;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    switch (gSteps) {
    case 0:
        tmp4 = func_0213();
        tmp5 = tmp4;
        break;
    default:
        tmp4 = gMissionTimeToBeat;
    }
    return;
}

int func_0334(int param_0) {
    c_Vector3 local_311;
    int n;
    int tmp;
    int tmp1;
    int tmp2;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    block_50:
    switch (n) {
    case 0:
        break;
    case 3:
        return 0.0f;
    default:
        return 0;  // FIX (06-05): Synthesized return value
    }
    return 0;  // FIX (06-05): Synthesized return value
}

void func_0355(void) {
    c_Vector3 local_311;
    int data_;
    int data_1966;
    int n;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp15;
    int tmp16;
    int tmp17;
    int tmp18;
    int tmp19;
    int tmp2;
    int tmp20;
    int tmp21;
    int tmp22;
    int tmp23;
    int tmp24;
    int tmp25;
    int tmp26;
    int tmp27;
    int tmp28;
    int tmp29;
    int tmp3;
    int tmp30;
    int tmp32;
    int tmp33;
    int tmp34;
    int tmp35;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    block_57:
    switch (gMission_phase) {
    case 3:
        gSidePoints[tmp11] = tmp10;
        func_0249();
        SC_sgi(506, tmp15);
        SC_sgi(509, tmp16);
        if (tmp17) {
            data_ = tmp18;
        } else {
            data_ = tmp19;
        }
        break;
    case 2:
        SC_sgi(tmp35, data_1966);
        if (tmp21) {
            gSidePoints[data_1966] = tmp28;
            func_0249();
            SC_sgi(506, data_1966);
            data_ = tmp34;
        } else {
            tmp33 = tmp32;
        }
        break;
    default:
        SC_sgi(502, data_);
        data_1966 = func_0334(data_);
        SC_sgi(507, 6);
        return;
    }
    return;
}

int func_0498(int param_0, int param_1) {
    c_Vector3 local_311;
    int idx;
    int m;
    int tmp;
    int tmp1;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    tmp = 0.0f;
    tmp1 = 0.0f;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0752(int param_0) {
    c_Vector3 local_311;
    int idx;
    int local_;
    int local_7;
    int n;
    int side;
    int side2;
    int side3;
    int side4;
    int side5;
    int sideB;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo player_info;

    SC_MP_SRV_GetAutoTeamBalance();
    if (!local_7) {
        local_ = SC_MP_SRV_GetTeamsNrDifference(1);
        return 7;
    } else {
        return 7;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0852(void) {
    c_Vector3 local_311;
    int idx;
    int k;
    int local_;
    int local_2;
    int local_265;
    int local_266;
    int local_267;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers enum_pl[64];
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    SC_MP_SRV_GetAutoTeamBalance();
    if (!local_267) {
        local_ = SC_MP_SRV_GetTeamsNrDifference(tmp6);
        return 267;
    } else {
        return 267;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_1028(void) {
    c_Vector3 local_311;
    int idx;
    int local_257;
    int local_258;
    int local_259;
    int local_260;
    int local_261;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers enum_pl[64];
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    SC_ggi(tmp4);
    func_0334();
    tmp1 = tmp;
    tmp2 = 64;
    SC_MP_EnumPlayers(enum_pl, &tmp2, tmp1);
    if (!local_259) {
        tmp3 = 0.0f;
    } else {
        return tmp1;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

