// Structured decompilation of Compiler-testruns/Testrun1/tdm.scr
// Functions: 4

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\mplevel.inc>

int _init(s_SC_NET_info *info) {
    int local_0;

    DLD();
    DLD();
    return FALSE;
}

int func_0010(float time) {
    int local_0;

    switch (local_0) {
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
                    SC_MP_LoadNextMap();
                    return TRUE;
                }
                SC_message("EndRule unsopported: %d", gEndRule);
                return FALSE;
            }
            SC_MP_LoadNextMap();
            return TRUE;
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
    int i;
    int local_0;
    int local_10;
    int local_3;
    int local_74;
    int local_76;
    int local_8;
    s_SC_P_getinfo player_info;

    switch (info->message) {
    case 3:
        if ((func_0010())) break;
        i = 0;
        // Loop header - Block 26 @145
        for (i = 0; (i <= gRecs); i = (i + 1)) {
            gRecTimer[i] = (gRecTimer[i] - info->field_16);
        }
        i = 64;
        if ((SC_MP_EnumPlayers(&player_info.group, &i, -1))) {
            if (((i == 0))) {
                if ((((gSideFrags[0] + gSideFrags[1]) != 0))) {
                    gSideFrags[0] = 0;
                    gSideFrags[1] = 0;
                    func_0096();
                }
                gSideFrags[0] = 0;
                gSideFrags[1] = 0;
                func_0096();
            }
            gSideFrags[0] = 0;
            gSideFrags[1] = 0;
            func_0096();
        }
        gPlayersConnected = i;
        break;
    case 4:
        gCLN_SideFrags[0] = SC_ggi(GVAR_SIDE0FRAGS);
        gCLN_SideFrags[1] = SC_ggi(GVAR_SIDE1FRAGS);
        SC_MP_SetSideStats(0, gCLN_SideFrags[0], 0);
        SC_MP_SetSideStats(1, gCLN_SideFrags[1], 0);
        i = 0;
        // Loop header - Block 36 @270
        for (i = 0; (i <= data_383); i = (i + 1)) {
            local_8[i].field1 = 1;
            local_8[i] = (3 * i);
            local_8[i].field2 = gCLN_SideFrags[i];
            local_8[i].field3 = -1;
        }
        SC_MP_SetIconHUD(&player_info.max_hp, 2);
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
        SC_ZeroMem(&local_3, 60);
        local_3 = 1051;
        local_3.field10 = 2;
        local_3.field11 = 3;
        local_3.field12 = -2147483644;
        local_3.field13 = -2147483643;
        local_3.field8 = 28;
        local_3.field1 = 1;
        local_3.field4 = 1010;
        local_3.field6 = 512.0155639648438f;
        local_3.field5 = 1011;
        local_3.field7 = 2040.0f;
        local_3.field9 = 2;
        SC_MP_HUD_SetTabInfo(&local_3);
        SC_MP_AllowStPwD(1);
        SC_MP_AllowFriendlyFireOFF(1);
        SC_MP_SetItemsNoDisappear(0);
        if ((info->field_8)) {
            if ((info->field_4)) {
                SC_MP_GetSRVsettings(&local_74);
                SC_MP_SRV_InitWeaponsRecovery(ITOF(local_74.field2));
                SC_MP_Gvar_SetSynchro(500);
                SC_MP_Gvar_SetSynchro(501);
                func_0096();
                gRecs = 0;
                i = 0;
                sprintf(&local_0, "DM%d", i);
                if ((SC_NET_FillRecover(&gRec[gRecs], &local_0))) {
                    gRecs++;
                } else {
                    i++;
                }
                gRecs++;
                i++;
                i = (64 - gRecs);
                SC_MP_GetRecovers(1, &gRec[gRecs], &i);
                gRecs = (gRecs + i);
                SC_Log(3, "TDM respawns: %d", gRecs);
                if (((gRecs == 0))) {
                    SC_message("no recover place defined!");
                }
                SC_message("no recover place defined!");
                SC_ZeroMem(&gRecTimer, 256);
            }
            SC_MP_GetSRVsettings(&local_74);
            SC_MP_SRV_InitWeaponsRecovery(ITOF(local_74.field2));
            SC_MP_Gvar_SetSynchro(500);
            SC_MP_Gvar_SetSynchro(501);
            func_0096();
            gRecs = 0;
            i = 0;
            sprintf(&local_0, "DM%d", i);
            SC_NET_FillRecover(&gRec[gRecs], &local_0);
            gRecs++;
            i++;
            i = (64 - gRecs);
            SC_MP_GetRecovers(1, &gRec[gRecs], &i);
            gRecs = (gRecs + i);
            SC_Log(3, "TDM respawns: %d", gRecs);
            SC_message("no recover place defined!");
            SC_ZeroMem(&gRecTimer, 256);
        }
        // Loop header - Block 45 @494
        for (i = 0; (i <= data_430); i = (i + 1)) {
            sprintf(&local_0, "DM%d", i);
            SC_NET_FillRecover(&gRec[gRecs], &local_0);
            gRecs++;
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
        local_3 = info->field_8;
        i = SC_MP_SRV_GetBestDMrecov(&gRec, gRecs, &gRecTimer, 3.0f);
        gRecTimer[i] = 3.0f;
        local_3 = gRec[i];
        break;
    case 7:
        SC_P_GetInfo(info->field_4, &player_info);
        i = player_info.field2;
        if ((info->field_8)) {
            SC_P_GetInfo(info->field_8, &player_info);
            i = player_info.field2;
        } else {
            i = -1;
        }
        if (((i == i))) {
            gSideFrags[i]--;
        } else {
            if (((i != -1))) {
                gSideFrags[i]++;
            }
            gSideFrags[i]++;
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

