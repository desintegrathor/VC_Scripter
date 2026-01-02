[DEBUG P0.4.2 DCP+DADR] local_12 v0 @ 613: SKIPPED (DADR detected)
// Structured decompilation of Compiler-testruns/Testrun1/tdm.scr
// Functions: 4

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\mplevel.inc>

// Global variables
dword gRecs;
dword gRec;
dword gVar;
dword gVar1;
dword gRecTimer;
dword gNextRecover;
dword gSideFrags[2];
dword gCLN_SideFrags[2];
dword gEndRule;
dword gEndValue;
dword gTime;
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
        if (((gPlayersConnected > 0))) {
            gTime = (gTime + time);
        }
        SC_MP_EndRule_SetTimeLeft(gTime, (gPlayersConnected > 0));
        if (((gTime > ITOF(gEndValue)))) {
            SC_MP_LoadNextMap();
            return TRUE;
        }
        break;
    case 1:
        if (((gSideFrags[0] > 0))) {
            if (((gSideFrags[0] >= gEndValue))) {
            } else {
                if (((gSideFrags[1] > 1))) {
                    if (((gSideFrags[1] >= gEndValue))) {
                        SC_MP_LoadNextMap();
                        return TRUE;
                    }
                }
                SC_message("EndRule unsopported: %d", gEndRule);
                return FALSE;
            }
        }
        break;
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
        if ((func_0010(info->field_16))) break;
        // Loop header - Block 26 @145
        for (local_8 = 0; (local_8 < gRecs); local_8++) {
            gRecTimer[local_8] = (gRecTimer[local_8] - info->field_16);
            tmp = (local_8 + 1);
        }
        tmp4 = 64;
        if ((SC_MP_EnumPlayers(&tmp5, &tmp4, -1))) {
            if (((tmp4 == 0))) {
                if ((((gSideFrags[0] + gSideFrags[1]) != 0))) {
                    gSideFrags[0] = 0;
                    gSideFrags[1] = 0;
                    func_0096();
                }
            }
        }
        gPlayersConnected = tmp4;
        break;
    case 4:
        gCLN_SideFrags[0] = SC_ggi(GVAR_SIDE0FRAGS);
        gCLN_SideFrags[1] = SC_ggi(GVAR_SIDE1FRAGS);
        SC_MP_SetSideStats(0, gCLN_SideFrags[0], 0);
        SC_MP_SetSideStats(1, gCLN_SideFrags[1], 0);
        local_8_v2 = 0;
        // Loop header - Block 36 @270
        for (local_8_v2 = 0; (local_8_v2 < 2); local_8_v2 = (local_8_v2_v2 + 1)) {
            local_33[local_8_v2].field1 = 1;
            local_33[local_8_v2] = (3 * local_8_v2);
            local_33[local_8_v2].field2 = gCLN_SideFrags[local_8_v2];
            local_33[local_8_v2].field3 = -1;
            tmp1 = (local_8_v2 + 1);
        }
        SC_MP_SetIconHUD(&tmp6, 2);
        break;
    case 9:
        SC_sgi(GVAR_MP_MISSIONTYPE, 2);
        gEndRule = info->field_4;
        gEndValue = info->field_8;
        gTime = 0;
        SC_MP_EnableBotsFromScene(0);
        break;
    case 1:
        SC_MP_SRV_SetForceSide(-1);
        SC_MP_SetChooseValidSides(3);
        SC_MP_SRV_SetClassLimitsForDM();
        SC_ZeroMem(&tmp7, 60);
        tmp7 = 1051;
        tmp7.field10 = 2;
        tmp7.field11 = 3;
        tmp7.field12 = -2147483644;
        tmp7.field13 = -2147483643;
        tmp7.field8 = 28;
        tmp7.field1 = 1;
        tmp7.field4 = 1010;
        tmp7.field6 = 512.0155639648438f;
        tmp7.field5 = 1011;
        tmp7.field7 = 2040.0f;
        tmp7.field9 = 2;
        SC_MP_HUD_SetTabInfo(&tmp7);
        SC_MP_AllowStPwD(1);
        SC_MP_AllowFriendlyFireOFF(1);
        SC_MP_SetItemsNoDisappear(0);
        if ((info->field_8)) {
            if ((info->field_4)) {
                SC_MP_GetSRVsettings(&tmp8);
                SC_MP_SRV_InitWeaponsRecovery(ITOF(tmp8.field2));
                SC_MP_Gvar_SetSynchro(500);
                SC_MP_Gvar_SetSynchro(501);
                func_0096();
                gRecs = 0;
                local_8_v4 = 0;
                sprintf(&tmp10, "DM%d", local_8_v4);
                if ((SC_NET_FillRecover(&gRec[gRecs], &tmp10))) {
                    gRecs++;
                } else {
                    tmp2 = (local_8_v4 + 1);
                }
                local_8_v6 = (64 - gRecs);
                SC_MP_GetRecovers(1, &gRec[gRecs], &local_8_v6);
                gRecs = (gRecs + local_8_v6);
                SC_Log(3, "TDM respawns: %d", gRecs);
                if (((gRecs == 0))) {
                    SC_message("no recover place defined!");
                }
                SC_ZeroMem(&gRecTimer, 256);
            }
        }
        // Loop header - Block 45 @494
        for (local_8_v4 = 0; (local_8_v4 < 64); local_8_v4 = (local_8_v4_v4 + 1)) {
            tmp2 = (local_8_v4 + 1);
        }
        break;
    case 2:
        break;
    case 5:
        if ((info->field_8)) {
        } else {
        }
        break;
    case 6:
        tmp11 = info->field_8;
        tmp3 = SC_MP_SRV_GetBestDMrecov(&gRec, gRecs, &gRecTimer, 3.0f);
        gRecTimer[tmp3] = 3.0f;
        tmp12 = gRec[tmp3];
        break;
    case 7:
        SC_P_GetInfo(info->field_4, &tmp15);
        tmp13 = tmp15.field2;
        if ((info->field_8)) {
            SC_P_GetInfo(info->field_8, &tmp15);
            tmp14 = tmp15.field2;
        } else {
            local_11_v1 = -1;
        }
        if (((tmp13 == local_11_v1))) {
            gSideFrags[local_11_v1]--;
        } else {
            if (((local_11_v1 != -1))) {
                gSideFrags[local_11_v1]++;
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

