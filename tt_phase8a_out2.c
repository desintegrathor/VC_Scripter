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

