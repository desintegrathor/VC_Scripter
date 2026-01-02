// Structured decompilation of Compiler-testruns\Testrun1\tdm.scr
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
        *tmp8 = 0;
        // Loop header - Block 26 @145
        for (tmp8 = 0; (tmp8 < gRecs); tmp8 = (tmp10 + 1)) {
            gRecTimer[tmp9] = (gRecTimer[tmp8] - info->field_16);
            *tmp11 = (tmp10 + 1);
        }
        *tmp11 = 64;
        if ((SC_MP_EnumPlayers(local_10, local_2_v4, -1))) {
            if (((local_2_v4 == 0))) {
                if ((((gSideFrags[0] + gSideFrags[1]) != 0))) {
                    gSideFrags[0] = 0;
                    gSideFrags[1] = 0;
                    func_0096();
                }
            }
        }
        gPlayersConnected = local_2_v4;
        break;
    case 4:
        gCLN_SideFrags[0] = SC_ggi(GVAR_SIDE0FRAGS);
        gCLN_SideFrags[1] = SC_ggi(GVAR_SIDE1FRAGS);
        SC_MP_SetSideStats(0, gCLN_SideFrags[0], 0);
        SC_MP_SetSideStats(1, gCLN_SideFrags[1], 0);
        *local_2_v4 = 0;
        // Loop header - Block 36 @270
        for (local_2_v4 = 0; (local_2_v4 < 2); local_2_v4 = (tmp17 + 1)) {
            local_8[local_2_v4].field1 = 1;
            local_8[tmp13] = (3 * tmp12);
            local_8[tmp15].field2 = gCLN_SideFrags[tmp14];
            local_8[tmp16].field3 = -1;
            *local_2_v11 = (tmp17 + 1);
        }
        SC_MP_SetIconHUD(tmp30, 2);
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
        SC_ZeroMem(tmp31, 60);
        *tmp32 = 1051;
        (tmp33 + 40) = 2;
        ((tmp34 + 40) + 4) = 3;
        ((tmp35 + 40) + 8) = -2147483644;
        ((tmp36 + 40) + 12) = -2147483643;
        *(tmp37 + 32) = 28;
        *(tmp38 + 4) = 1;
        (tmp39 + 16) = 1010;
        ((tmp41 + 16) + 4) = 1011;
        *(tmp43 + 36) = 2;
        SC_MP_HUD_SetTabInfo(tmp44);
        SC_MP_AllowStPwD(1);
        SC_MP_AllowFriendlyFireOFF(1);
        SC_MP_SetItemsNoDisappear(0);
        if ((info->field_8)) {
            if ((info->field_4)) {
                SC_MP_GetSRVsettings(tmp46);
                SC_MP_SRV_InitWeaponsRecovery(ITOF((*(tmp47 + 8))));
                SC_MP_Gvar_SetSynchro(500);
                SC_MP_Gvar_SetSynchro(501);
                func_0096();
                gRecs = 0;
                *local_2_v11 = 0;
                sprintf(tmp48, "DM%d", local_2_v11);
                if ((SC_NET_FillRecover(&gRec[gRecs], tmp49))) {
                    gRecs++;
                } else {
                    *tmp18 = (local_2_v11 + 1);
                }
                *tmp18 = (64 - gRecs);
                SC_MP_GetRecovers(1, &gRec[gRecs], tmp19);
                gRecs = (gRecs + tmp20);
                SC_Log(3, "TDM respawns: %d", gRecs);
                if (((gRecs == 0))) {
                    SC_message("no recover place defined!");
                }
                SC_ZeroMem(&gRecTimer, 256);
            }
        }
        // Loop header - Block 45 @494
        for (local_2_v11 = 0; (local_2_v11 < 64); local_2_v11 = (local_2_v11_v11 + 1)) {
            *tmp18 = (local_2_v11 + 1);
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
        *tmp44 = info->field_8;
        *tmp20 = SC_MP_SRV_GetBestDMrecov(&gRec, gRecs, &gRecTimer, 3.0f);
        gRecTimer[tmp21] = 3.0f;
        tmp45 = gRec[local_2_v16];
        break;
    case 7:
        SC_P_GetInfo(info->field_4, tmp50);
        *local_2_v16 = local_7.side;
        if ((info->field_8)) {
            SC_P_GetInfo(info->field_8, tmp52);
            *local_2_v16 = local_7.side;
        } else {
            *local_2_v16 = -1;
        }
        if (((local_2_v16 == local_2_v16))) {
            gSideFrags[tmp23] = (gSideFrags[tmp22] - 1);
        } else {
            if (((tmp23 != -1))) {
                gSideFrags[tmp25] = (gSideFrags[tmp24] + 1);
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

