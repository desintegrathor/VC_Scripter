// Structured decompilation of Compiler-testruns/Testrun1/tdm.scr
// Functions: 4

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\mplevel.inc>

// Global variables
dword gRecs;
s_SC_MP_Recover * gRec;
dword gVar;
dword gVar1;
float * gRecTimer;
dword gNextRecover;
dword gSideFrags[2];
dword gCLN_SideFrags[2];
dword gEndRule;
int gEndValue;
float gTime;
dword gPlayersConnected;
dword gVar4;
dword gVar2;
dword gVar3;

int _init(s_SC_NET_info *info) {
    int local_0;

    DLD();
    DLD();
    return FALSE;
}

int func_0010(float time) {
    int local_0;

    switch (gEndRule) {
    case 0:
        if (gPlayersConnected > 0) {
            gTime = gTime + time;
        }
        SC_MP_EndRule_SetTimeLeft(gTime, gPlayersConnected > 0);
        if (gTime > ITOF(gEndValue)) {
            SC_MP_LoadNextMap();
            return TRUE;
        }
        break;
    case 1:
        if ((gSideFrags[0] > 0 && gSideFrags[0] >= gEndValue) || (gSideFrags[1] > 1 && gSideFrags[1] >= gEndValue)) {
            SC_MP_LoadNextMap();
            return TRUE;
        }
        SC_message("EndRule unsopported: %d", gEndRule);
        return FALSE;
    default:
    }
}

int func_0096(void) {
    SC_sgi(GVAR_SIDE0FRAGS, gSideFrags[0]);
    SC_sgi(GVAR_SIDE1FRAGS, gSideFrags[1]);
    return FALSE;
}

int ScriptMain(s_SC_NET_info *info) {
    char local_0[32];
    dword local_13[16];
    int i;
    int j;
    int local_10;
    int local_12;
    int local_297;
    int local_306;
    int local_307;
    int local_33;
    int local_41;
    int local_9;
    s_SC_P_getinfo player_info;

    switch (info->message) {
    case 3:
        if (func_0010(info->field_16)) break;
        // Loop header - Block 26 @145
        for (local_8 = 0; (local_8 < gRecs); local_8++) {
            gRecTimer[local_8] = gRecTimer[local_8] - info->field_16;
            local_8_v1 = local_8 + 1;
        }
        if (tmp32 && local_9 == 0 && gSideFrags[0] + gSideFrags[1] != 0) {
            gSideFrags[0] = 0;
            gSideFrags[1] = 0;
            func_0096();
        }
        gPlayersConnected = local_9;
        break;
    case 4:
        gCLN_SideFrags[0] = SC_ggi(GVAR_SIDE0FRAGS);
        gCLN_SideFrags[1] = SC_ggi(GVAR_SIDE1FRAGS);
        SC_MP_SetSideStats(0, gCLN_SideFrags[0], 0);
        SC_MP_SetSideStats(1, gCLN_SideFrags[1], 0);
        local_8_v1 = 0;
        // Loop header - Block 36 @270
        for (local_8_v1 = 0; (local_8_v1 < 2); local_8_v1 = local_8_v1_v1 + 1) {
            local_33[local_8_v1].field1 = 1;
            local_33[local_8_v1] = 3 * local_8_v1;
            local_33[local_8_v1].field2 = gCLN_SideFrags[local_8_v1];
            local_33[local_8_v1].field3 = -1;
            local_8_v2 = local_8_v1 + 1;
        }
        SC_MP_SetIconHUD(&tmp29, 2);
        break;
    case 9:
        SC_sgi(GVAR_MP_MISSIONTYPE, 2);
        gEndRule = info->field_4;
        gEndValue = info->field_8;
        gTime = 0;
        SC_MP_EnableBotsFromScene(0);
        break;
    case 1:
        if (info->field_8 && info->field_4) {
        }
        SC_MP_GetSRVsettings(&tmp31);
        SC_MP_SRV_InitWeaponsRecovery(ITOF(tmp31.field2));
        SC_MP_Gvar_SetSynchro(500);
        SC_MP_Gvar_SetSynchro(501);
        func_0096();
        gRecs = 0;
        local_8_v2 = 0;
        // Loop header - Block 45 @494
        for (local_8_v2 = 0; (local_8_v2 < 64); local_8_v2 = local_8_v2_v2 + 1) {
            sprintf(&tmp33, "DM%d", local_8_v2);
            if (SC_NET_FillRecover(&gRec[gRecs], &tmp33)) {
                gRecs++;
            } else {
                tmp = local_8_v2 + 1;
            }
            tmp = local_8_v2 + 1;
        }
        tmp = 64 - gRecs;
        SC_MP_GetRecovers(1, &gRec[gRecs], &tmp);
        gRecs = gRecs + tmp;
        SC_Log(3, "TDM respawns: %d", gRecs);
        if (gRecs == 0) {
            SC_message("no recover place defined!");
        }
        SC_ZeroMem(&gRecTimer, 256);
        break;
    case 2:
        break;
    case 5:
        if (info->field_8) {
        } else {
        }
        break;
    case 6:
        tmp34 = info->field_8;
        tmp1 = SC_MP_SRV_GetBestDMrecov(&gRec, gRecs, &gRecTimer, 3.0f);
        gRecTimer[tmp1] = 3.0f;
        tmp35 = gRec[tmp1];
        break;
    case 7:
        SC_P_GetInfo(info->field_4, &tmp36);
        sideA = tmp36.field2;
        if (info->field_8) {
            SC_P_GetInfo(info->field_8, &tmp36);
            sideB = tmp36.field2;
        } else {
            sideB = -1;
        }
        if (sideA == sideB) {
            gSideFrags[sideB]--;
        } else {
            if (sideB != -1) {
                gSideFrags[sideB]++;
            }
        }
        func_0096();
        break;
    case 10:
        gTime = 0;
        SC_ZeroMem(&gSideFrags, 8);
        func_0096();
        SC_MP_SRV_ClearPlsStats();
        SC_MP_SRV_InitGameAfterInactive();
        SC_MP_RecoverAllNoAiPlayers();
        break;
    case 11:
        gEndRule = info->field_4;
        gEndValue = info->field_8;
        gTime = 0;
        break;
    default:
        return TRUE;
    }
}

