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
    dword local_3[16];
    int i;
    int local_10;
    int local_74;
    int local_76;
    int local_8;
    s_SC_P_getinfo player_info;

    switch (info->message) {
    case 3:
        if ((func_0010(info->field_16))) break;
        // Loop header - Block 26 @145
        for (local_2 = 0; (local_2 < gRecs); local_2++) {
            gRecTimer[local_2] = (gRecTimer[local_2] - info->field_16);
        }
        local_2 = 64;
        if ((SC_MP_EnumPlayers(&player_info.group, &local_2, -1))) {
            if (((local_2 == 0))) {
                if ((((gSideFrags[0] + gSideFrags[1]) != 0))) {
                    gSideFrags[0] = 0;
                    gSideFrags[1] = 0;
                    func_0096();
                }
            }
        }
        gPlayersConnected = local_2;
        break;
    case 4:
        gCLN_SideFrags[0] = SC_ggi(GVAR_SIDE0FRAGS);
        gCLN_SideFrags[1] = SC_ggi(GVAR_SIDE1FRAGS);
        SC_MP_SetSideStats(0, gCLN_SideFrags[0], 0);
        SC_MP_SetSideStats(1, gCLN_SideFrags[1], 0);
        // Loop header - Block 36 @270
        for (local_2 = 0; (local_2 < 2); local_2++) {
            local_8[local_2].field1 = 1;
            local_8[local_2] = (3 * local_2);
            local_8[local_2].field2 = gCLN_SideFrags[local_2];
            local_8[local_2].field3 = -1;
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
                local_2 = 0;
                sprintf(&local_0, "DM%d", local_2);
                if ((SC_NET_FillRecover(&gRec[gRecs], &local_0))) {
                    gRecs++;
                } else {
                    local_2++;
                }
                local_2 = (64 - gRecs);
                SC_MP_GetRecovers(1, &gRec[gRecs], &local_2);
                gRecs = (gRecs + local_2);
                SC_Log(3, "TDM respawns: %d", gRecs);
                if (((gRecs == 0))) {
                    SC_message("no recover place defined!");
                }
                SC_ZeroMem(&gRecTimer, 256);
            }
        }
        // Loop header - Block 45 @494
        for (local_2 = 0; (local_2 < 64); local_2++) {
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
        local_2 = SC_MP_SRV_GetBestDMrecov(&gRec, gRecs, &gRecTimer, 3.0f);
        gRecTimer[local_2] = 3.0f;
        local_3 = gRec[local_2];
        break;
    case 7:
        SC_P_GetInfo(info->field_4, &player_info);
        local_2 = player_info.field2;
        if ((info->field_8)) {
            SC_P_GetInfo(info->field_8, &player_info);
            local_2 = player_info.field2;
        } else {
            local_2 = -1;
        }
        if (((local_2 == local_2))) {
            gSideFrags[local_2]--;
        } else {
            if (((local_2 != -1))) {
                gSideFrags[local_2]++;
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

