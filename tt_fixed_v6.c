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
    if (!tmp) {
        data_ = tmp3;
        SC_MP_EndRule_SetTimeLeft(data_, gMission_phase);
        SC_MP_LoadNextMap();
        return TRUE;
    } else {
        SC_MP_LoadNextMap();
        return TRUE;
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

    switch (gMainPhase%2) {
    case 0:
        tmp4 = func_0213();
        tmp5 = tmp4;
        break;
    default:
        tmp6 = -1.0f;
        func_0264(0.0f);
        return;
    }
    tmp4 = gMissionTimeToBeat;
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
    if (!tmp1) {
    } else {
        return 0;  // FIX (06-05): Synthesized return value
    }
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
    if (!tmp) {
        gSidePoints[tmp11] = tmp10;
        func_0249();
        SC_sgi(506, tmp15);
        SC_sgi(509, tmp16);
        data_ = tmp18;
        data_ = tmp19;
    } else {
        SC_sgi(tmp35, data_1966);
        gSidePoints[data_1966] = tmp28;
        func_0249();
        SC_sgi(506, data_1966);
        tmp33 = tmp32;
        data_ = tmp34;
    }
    SC_sgi(502, data_);
    data_1966 = func_0334(data_);
    SC_sgi(507, 6);
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

int ScriptMain(s_SC_NET_info *info) {
    dword MPIC_USflag;  // Auto-generated
    dword MPIC_VCflag;  // Auto-generated
    dword MPIC_emptyflag;  // Auto-generated
    int g;  // Auto-generated
    dword param_1;  // Auto-generated

    c_Vector3 local_311;
    float local_411;
    float local_420;
    int data_;
    int data_1959;
    int gSidePoints;
    int i;
    int idx;
    int j;
    int k;
    int local_;
    int local_10;
    int local_12;
    int local_13;
    int local_298;
    int local_314;
    int local_315;
    int local_379;
    int local_412;
    int local_418;
    int local_419;
    int local_421;
    int local_422;
    int local_8;
    int local_9;
    int n;
    int precov;
    int side;
    int side2;
    int side3;
    int sideB;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp100;
    int tmp101;
    int tmp102;
    int tmp103;
    int tmp104;
    int tmp105;
    int tmp106;
    int tmp107;
    int tmp108;
    int tmp109;
    int tmp11;
    int tmp110;
    int tmp111;
    int tmp113;
    int tmp114;
    int tmp115;
    int tmp116;
    int tmp118;
    int tmp12;
    int tmp120;
    int tmp121;
    int tmp122;
    int tmp123;
    int tmp125;
    int tmp126;
    int tmp127;
    int tmp128;
    int tmp129;
    int tmp13;
    int tmp130;
    int tmp131;
    int tmp132;
    int tmp133;
    int tmp134;
    int tmp135;
    int tmp136;
    int tmp137;
    int tmp138;
    int tmp139;
    int tmp14;
    int tmp140;
    int tmp141;
    int tmp142;
    int tmp143;
    int tmp144;
    int tmp145;
    int tmp146;
    int tmp147;
    int tmp148;
    int tmp149;
    int tmp15;
    int tmp150;
    int tmp151;
    int tmp152;
    int tmp154;
    int tmp155;
    int tmp156;
    int tmp157;
    int tmp158;
    int tmp159;
    int tmp16;
    int tmp160;
    int tmp161;
    int tmp162;
    int tmp163;
    int tmp164;
    int tmp165;
    int tmp166;
    int tmp167;
    int tmp168;
    int tmp169;
    int tmp170;
    int tmp171;
    int tmp18;
    int tmp2;
    int tmp20;
    int tmp21;
    int tmp22;
    int tmp23;
    int tmp24;
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
    int tmp46;
    int tmp47;
    int tmp48;
    int tmp49;
    int tmp5;
    int tmp50;
    int tmp51;
    int tmp52;
    int tmp53;
    int tmp54;
    int tmp55;
    int tmp56;
    int tmp57;
    int tmp58;
    int tmp59;
    int tmp60;
    int tmp61;
    int tmp62;
    int tmp63;
    int tmp64;
    int tmp65;
    int tmp66;
    int tmp67;
    int tmp68;
    int tmp69;
    int tmp7;
    int tmp70;
    int tmp71;
    int tmp72;
    int tmp73;
    int tmp74;
    int tmp75;
    int tmp76;
    int tmp77;
    int tmp78;
    int tmp79;
    int tmp80;
    int tmp81;
    int tmp82;
    int tmp83;
    int tmp84;
    int tmp85;
    int tmp86;
    int tmp87;
    int tmp88;
    int tmp89;
    int tmp9;
    int tmp90;
    int tmp91;
    int tmp92;
    int tmp93;
    int tmp94;
    int tmp95;
    int tmp96;
    int tmp97;
    int tmp98;
    int tmp99;
    s_SC_HUD_MP_icon icon;
    s_SC_HUD_MP_icon local_299;
    s_SC_MP_EnumPlayers enum_pl[64];
    s_SC_MP_EnumPlayers local_257;
    s_SC_MP_EnumPlayers local_265;
    s_SC_MP_EnumPlayers local_296;
    s_SC_MP_SRV_AtgSettings local_1;
    s_SC_MP_SRV_settings local_285;
    s_SC_MP_SRV_settings srv_settings;
    s_SC_MP_hud local_14;
    s_SC_P_getinfo local_413;
    s_SC_P_getinfo player_info;

    block_167:
    if (!tmp2) {
        func_0050(tmp4);
        local_296.field1 = 0.0f;
        tmp7 = tmp4;
        local_ = 64;
        SC_MP_EnumPlayers(enum_pl, &local_, tmp20);
        gSidePoints[0.0f] = 0.0f;
        gSidePoints[1] = 0.0f;
        func_0249();
        local_8 = 0.0f;
        local_8 = 0.0f;
    } else {
        data_ = tmp24;
        tmp30 = tmp29;
        tmp35 = tmp34;
        SC_ggi(tmp37);
        SC_ggi(508);
        func_0498(tmp38, 2);
        SC_ggi(507);
        i = SC_ggi(tmp44);
        SC_ggi(508);
        data_ = 5.0f;
        SC_SND_PlaySound2D(10425);
        SC_ggi(tmp45);
        func_0334();
        func_0498(i);
        SC_ggi(505);
        tmp47 = SC_ggi(505);
        tmp48 = SC_ggf(tmp53);
        SC_ggi(503);
        tmp48 = tmp52;
        local_8 = 0.0f;
        SC_sgi(499, 9);
        tmp57 = tmp56;
        tmp60 = tmp59;
        data_1959 = 0.0f;
        SC_MP_EnableBotsFromScene(0);
        tmp62 = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_USflag.BES");
        tmp63 = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_VCflag.BES");
        tmp64 = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_emptyflag.BES");
        SC_MP_SRV_SetForceSide(-1);
        SC_MP_SetChooseValidSides(3);
        SC_MP_SRV_SetClassLimit(18, 0.0f);
        SC_MP_SRV_SetClassLimit(19, 0.0f);
        SC_MP_SRV_SetClassLimit(39, 0.0f);
        SC_MP_GetSRVsettings(&srv_settings);
        local_8 = 0.0f;
        local_8 = 0.0f;
        local_314 = 0.0f;
        tmp66 = 0.0f;
        local_10 = SC_ggi(tmp70);
        SC_ggi(503);
        tmp68 = SC_ggi(tmp71);
        SC_ggi(tmp74);
        SC_SND_PlaySound2D(tmp75);
        SC_SND_PlaySound2D(11116);
        local_314 = SC_Wtxt(1076);
        tmp30 = 0.0f;
        tmp35 = 3.0f;
        tmp30 = 3.0f;
        local_8 = SC_PC_Get();
        SC_P_GetInfo(local_8, &player_info);
        SC_ggi(502);
        func_0334();
        local_314 = SC_Wtxt(5108);
        local_314 = SC_Wtxt(5109);
        SC_GameInfoW(local_314);
        local_314 = 0.0f;
        SC_ggi(510);
        local_9 = SC_MP_GetPlofHandle(j);
        SC_P_GetName(local_9);
        SC_AnsiToUni(j, &local_379);
        SC_AnsiToUni("'disconnected'", &local_379);
        SC_Wtxt(tmp89);
        swprintf(tmp89, local_422, &local_379, i);
        local_314 = &local_315;
        local_8 = SC_PC_Get();
        SC_P_GetInfo(local_8, &player_info);
        SC_ggi(502);
        func_0334();
        local_314 = SC_Wtxt(5111);
        SC_Wtxt(5110);
        swprintf(5110, local_422, tmp86);
        local_314 = &local_315;
        local_314 = SC_Wtxt(5113);
        SC_Wtxt(5112);
        swprintf(5112, local_422, tmp88);
        local_314 = &local_315;
        SC_ggi(tmp94);
        local_9 = SC_MP_GetPlofHandle(j);
        SC_P_GetName(local_9);
        SC_AnsiToUni(j, &local_379);
        SC_AnsiToUni("'disconnected'", &local_379);
        local_8 = 5101;
        local_8 = 5103;
        local_8 = 5102;
        local_8 = 5104;
        SC_Wtxt(local_8);
        swprintf(local_8, local_422, &local_379);
        local_314 = &local_315;
        tmp30 = 0.0f;
        SC_ggi(tmp100);
        local_9 = SC_MP_GetPlofHandle(j);
        SC_P_GetName(local_9);
        SC_AnsiToUni(j, &local_379);
        SC_AnsiToUni("'disconnected'", &local_379);
        SC_ggi(tmp101);
        local_8 = 5105;
        local_8 = 5106;
        SC_Wtxt(local_8);
        swprintf(local_8, local_422, &local_379);
        local_314 = &local_315;
        tmp30 = 0.0f;
        SC_GetScreenRes(&tmp104, &local_412);
        SC_Fnt_GetWidthW(local_314, 1.0f);
        tmp104 = tmp103;
        local_412 = tmp106;
        local_412 = 15.0f;
        SC_Fnt_WriteW(tmp107, local_412, local_314, 1.0f, -1);
        param_1->field_20 = 0.1f;
        local_8 = 0.0f;
        param_1->field_20 = 3.0f;
        param_1->field_20 = -1.0f;
        tmp123 = tmp122;
        local_9 = tmp126;
        local_9 = tmp127;
        local_10 = 0.0f;
        rand();
        local_10 = tmp132;
        local_10 = 0.0f;
        local_10 = gCurStep;
        local_10 = tmp134;
        local_8 = SC_MP_SRV_GetBestDMrecov(precov, tmp142, tmp146, 3.0f);
        tmp152 = 3.0f;
        tmp123 = tmp160;
        data_1959 = 0.0f;
        SC_ZeroMem(&gSidePoints, 8);
        func_0249();
        SC_MP_SetInstantRecovery(1);
        SC_MP_RestartMission();
        SC_MP_RecoverAllNoAiPlayers();
        tmp114 = 0.0f;
        SC_sgi(503, tmp114);
        data_ = 0.0f;
        SC_MP_SRV_ClearPlsStats();
        tmp57 = tmp165;
        tmp60 = tmp167;
        data_1959 = 0.0f;
        func_0752(tmp170);
    }
    return TRUE;
}

