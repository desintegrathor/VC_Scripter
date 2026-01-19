// Structured decompilation of decompiler_source_tests/test1/tt.scr
// Functions: 14

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
int gSteps;
dword gRecs[12];
dword SGI_ALLYDEATHCOUNT;
dword SGI_C4COUNT;
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

int ScriptMain(s_SC_NET_info *info) {
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0050(void) {
    int data_;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;

    goto block_3; // @57
    block_3:
    if (!tmp1) {
        data_ = tmp2;
    } else {
        SC_MP_EndRule_SetTimeLeft(data_, gMission_phase);
        SC_MP_LoadNextMap();
        return TRUE;
        SC_MP_LoadNextMap();
        return TRUE;
        SC_message("EndRule unsopported: %d", gEndRule);
        return FALSE;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0119(void) {
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    int idx;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!tmp2) {
        return tmp4;
    } else {
        local_0 = SC_ggf(400);
        local_0 = 1106247680;
        return local_0;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0155(void) {
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    int idx;
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

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!tmp2) {
        tmp6 = tmp5;
        tmp6 = 1084227584;
        tmp6 = 1092616192;
        return tmp6;
    } else {
        local_0 = SC_ggf(401);
        local_0 = 1092616192;
        return local_0;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0213(void) {
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    int idx;
    int side;
    int side2;
    int side3;
    int side4;
    int sideB;

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!side2) {
        return side4;
    } else {
        local_0 = SC_ggf(402);
        local_0 = 1139802112;
        return local_0;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0249(void) {
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    SC_sgi(GVAR_SIDE0FRAGS, tmp1);
    SC_sgi(GVAR_SIDE1FRAGS, tmp3);
    return FALSE;
}

int func_0264(void) {
    int idx;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    tmp1 = tmp;
    if (!tmp2) {
        tmp1 = 1092616192;
        SC_sgf(504, gMissionTime);
        SC_ggi(505);
        SC_sgi(505, tmp3);
    } else {
        return FALSE;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0294(void) {
    int n;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;

    tmp1 = tmp;
    SC_sgi(507, tmp1);
    if (!tmp3) {
        tmp4 = func_0213();
        tmp5 = tmp4;
        tmp6 = -1082130432;
        func_0264(0);
        return FALSE;
    } else {
        tmp4 = gMissionTimeToBeat;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0334(void) {
    int tmp;

    goto block_46; // @343
    block_46:
    goto block_48; // @348
    block_48:
    return FALSE;
}

int func_0355(void) {
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

    goto block_52; // @362
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
        SC_sgi(GVAR_SIDE0DEATHS, data_);
        data_1966 = func_0334(data_);
        SC_sgi(507, 6);
        return FALSE;
    } else {
        data_ = tmp18;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0498(void) {
    int idx;
    int m;
    int tmp;
    int tmp1;

    tmp = 0;
    tmp1 = 0;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0752(void) {
    int idx;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated
    int local_2;  // Auto-generated

    int local_7;

    SC_MP_SRV_GetAutoTeamBalance();
    if (!local_7) {
        local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
        return 7;
        SC_P_GetInfo(idx, &local_2);
        local_1 = 1;
        local_1 = 0;
        return 7;
        SC_MP_SRV_P_SetSideClass(param_0, local_1, 1 + 20 * local_1);
        abl_list[abl_lists] = param_0;
        abl_lists++;
        return 7;
    } else {
        return 7;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0852(void) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated
    int local_2;  // Auto-generated
    int local_264;  // Auto-generated
    int local_265;  // Auto-generated
    int local_266;  // Auto-generated

    int local_267;

    SC_MP_SRV_GetAutoTeamBalance();
    if (!local_267) {
        local_0 = SC_MP_SRV_GetTeamsNrDifference(1);
        return 267;
        local_1 = 0;
        local_2 = local_0 / 2;
        local_1 = 1;
        local_2 = ((-local_0)) / 2;
        local_265 = 64;
        SC_MP_EnumPlayers(&i, &local_265, local_1);
        return 267;
        rand();
        local_266 = local_267 % local_265;
        local_264 = local_266;
        return local_2;
    } else {
        return 267;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_1028(void) {
    int enum_pl;
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

    SC_ggi(tmp4);
    func_0334();
    tmp1 = tmp;
    tmp2 = 64;
    SC_MP_EnumPlayers(&enum_pl, &tmp2, tmp1);
    if (!local_259) {
        tmp3 = 0;
    } else {
        return tmp1;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

