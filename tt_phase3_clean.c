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
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    block_3:
    if (!tmp1) {
        data_ = tmp2;
    } else {
        SC_MP_EndRule_SetTimeLeft(data_, gMission_phase);
        SC_MP_LoadNextMap();
        return TRUE;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0119(void) {
    int local_0;  // Auto-generated

    c_Vector3 local_311;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
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
        local_0 = SC_ggf(400);
        local_0 = 30.0f;
        return local_0;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0155(void) {
    int local_0;  // Auto-generated

    c_Vector3 local_311;
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
        local_0 = SC_ggf(401);
        local_0 = 10.0f;
        return local_0;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0213(void) {
    int local_0;  // Auto-generated

    c_Vector3 local_311;
    int side;
    int side2;
    int side3;
    int side4;
    int sideB;
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
        local_0 = SC_ggf(402);
        local_0 = 480.0f;
        return local_0;
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

    tmp1 = tmp;
    SC_sgi(507, tmp1);
    if (!tmp3) {
        tmp4 = func_0213();
        tmp5 = tmp4;
        tmp6 = -1.0f;
        func_0264(0.0f);
        return;
    } else {
        tmp4 = gMissionTimeToBeat;
    }
    return;
}

int func_0334(int param_0) {
    c_Vector3 local_311;
    int tmp;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    block_46:
    block_48:
    return 0.0f;
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
    int tmp14;
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
    int tmp36;
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

    block_52:
    gSidePoints[tmp10] = tmp9;
    func_0249();
    SC_sgi(tmp19, tmp14);
    SC_sgi(tmp20, tmp15);
    if (!tmp16) {
        data_ = tmp17;
        SC_sgi(tmp35, data_1966);
        gSidePoints[data_1966] = tmp28;
        func_0249();
        SC_sgi(tmp36, data_1966);
        tmp33 = tmp32;
        data_ = tmp34;
        SC_sgi(502, data_);
        data_1966 = func_0334(data_);
        SC_sgi(507, 6);
        return;
    } else {
        data_ = tmp18;
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

int func_0752(void) {
    int local_0;  // Auto-generated

    c_Vector3 local_311;
    int local_7;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    SC_MP_SRV_GetAutoTeamBalance();
    if (!local_7) {
        local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
        return 7;
    } else {
        return 7;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0852(void) {
    int local_0;  // Auto-generated

    c_Vector3 local_311;
    int local_267;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;

    SC_MP_SRV_GetAutoTeamBalance();
    if (!local_267) {
        local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
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

int ScriptMain(s_SC_NET_info *info) {
    c_Vector3 local_311;
    int data_;
    int i;
    int j;
    int local_;
    int local_12;
    int local_315;
    int local_379;
    int local_419;
    int local_420;
    int local_421;
    int local_422;
    int n;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp14;
    int tmp15;
    int tmp17;
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
    int tmp31;
    int tmp32;
    int tmp33;
    int tmp34;
    int tmp35;
    int tmp36;
    int tmp37;
    int tmp38;
    int tmp39;
    int tmp4;
    int tmp40;
    int tmp41;
    int tmp42;
    int tmp43;
    int tmp44;
    int tmp45;
    int tmp6;
    int tmp8;
    int tmp9;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers enum_pl[64];
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_hud local_14;
    s_SC_P_getinfo local_413;

    block_157:
    func_0050(tmp3);
    if (!local_419) {
        return TRUE;
    } else {
        local_296.field1 = 0.0f;
        tmp6 = tmp3;
        local_ = 64;
        SC_MP_EnumPlayers(enum_pl, &local_, tmp20);
        gSidePoints[0.0f] = 0.0f;
        gSidePoints[1] = 0.0f;
        func_0249();
        tmp19 = 0.0f;
        tmp19 = 0.0f;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

