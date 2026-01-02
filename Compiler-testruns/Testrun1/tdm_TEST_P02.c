DEBUG ASGN@25: source=t23_0, has_producer=True
  producer: FADD@23
DEBUG early_return block 23: jz_index=9, checking for CALL+LLD
  check_idx=8: SSP@138
  check_idx=7: LLD@137
  Found LLD at 7
    call_idx=6: CALL@136
  Found CALL/XCALL at 6! Formatting...
  CALL inputs: ['t134_0']
  Formatted: func_0010(info->field_16);
  func_call_cond set to: func_0010(info->field_16)
DEBUG ASGN@143: source=t141_0, has_producer=True
  producer: GCP@141
DEBUG ASGN@164: source=t158_0, has_producer=True
  producer: FSUB@158
DEBUG ASGN@171: source=t169_0, has_producer=True
  producer: ADD@169
DEBUG ASGN@177: source=t175_0, has_producer=True
  producer: GCP@175
DEBUG ASGN@209: source=t205_0, has_producer=True
  producer: GCP@205
DEBUG ASGN@215: source=t211_0, has_producer=True
  producer: GCP@211
DEBUG ASGN@220: source=t218_0, has_producer=True
  producer: LCP@218
DEBUG ASGN@237: source=t232_0, has_producer=True
  producer: LLD@232
DEBUG Pattern 2: ASGN@237 source from LLD@232
  Found LLD at index 10 in block 35
    check_idx=9: XCALL@231
  Found CALL/XCALL! Formatting...
  call_expr_override=SC_ggi(GVAR_SIDE0FRAGS)
DEBUG ASGN@248: source=t243_0, has_producer=True
  producer: LLD@243
DEBUG Pattern 2: ASGN@248 source from LLD@243
  Found LLD at index 21 in block 35
    check_idx=20: XCALL@242
  Found CALL/XCALL! Formatting...
  call_expr_override=SC_ggi(GVAR_SIDE1FRAGS)
DEBUG ASGN@268: source=t266_0, has_producer=True
  producer: GCP@266
DEBUG ASGN@281: source=t274_0, has_producer=True
  producer: GCP@274
DEBUG ASGN@291: source=t285_0, has_producer=True
  producer: MUL@285
DEBUG ASGN@305: source=t298_0, has_producer=True
  producer: DCP@298
DEBUG ASGN@314: source=t307_0, has_producer=True
  producer: GCP@307
DEBUG ASGN@321: source=t319_0, has_producer=True
  producer: ADD@319
DEBUG ASGN@343: source=t341_0, has_producer=True
  producer: DCP@341
DEBUG ASGN@349: source=t347_0, has_producer=True
  producer: DCP@347
DEBUG ASGN@353: source=t351_0, has_producer=True
  producer: GCP@351
DEBUG ASGN@377: source=t375_0, has_producer=True
  producer: GCP@375
DEBUG ASGN@384: source=t379_0, has_producer=True
  producer: GCP@379
DEBUG ASGN@391: source=t386_0, has_producer=True
  producer: GCP@386
DEBUG ASGN@398: source=t393_0, has_producer=True
  producer: GCP@393
DEBUG ASGN@405: source=t400_0, has_producer=True
  producer: GCP@400
DEBUG ASGN@410: source=t407_0, has_producer=True
  producer: GCP@407
DEBUG ASGN@415: source=t412_0, has_producer=True
  producer: GCP@412
DEBUG ASGN@422: source=t417_0, has_producer=True
  producer: GCP@417
DEBUG ASGN@429: source=t424_0, has_producer=True
  producer: GCP@424
DEBUG ASGN@436: source=t431_0, has_producer=True
  producer: GCP@431
DEBUG ASGN@443: source=t438_0, has_producer=True
  producer: GCP@438
DEBUG ASGN@448: source=t445_0, has_producer=True
  producer: GCP@445
DEBUG ASGN@488: source=t486_0, has_producer=True
  producer: GCP@486
DEBUG ASGN@492: source=t490_0, has_producer=True
  producer: GCP@490
DEBUG ASGN@525: source=t523_0, has_producer=True
  producer: ADD@523
DEBUG ASGN@533: source=t531_0, has_producer=True
  producer: ADD@531
DEBUG ASGN@541: source=t539_0, has_producer=True
  producer: SUB@539
DEBUG ASGN@556: source=t554_0, has_producer=True
  producer: ADD@554
DEBUG ASGN@533: source=t531_0, has_producer=True
  producer: ADD@531
DEBUG ASGN@595: source=t592_0, has_producer=True
  producer: GCP@592
DEBUG ASGN@601: source=t598_0, has_producer=True
  producer: GCP@598
DEBUG ASGN@613: source=t611_0, has_producer=True
  producer: DCP@611
DEBUG ASGN@625: source=t622_0, has_producer=True
  producer: LLD@622
DEBUG Pattern 2: ASGN@625 source from LLD@622
  Found LLD at index 63 in block 61
    check_idx=62: XCALL@621
  Found CALL/XCALL! Formatting...
  call_expr_override=SC_MP_SRV_GetBestDMrecov(&gRec, gRecs, &gRecTimer, 3.0f)
DEBUG ASGN@633: source=t627_0, has_producer=True
  producer: GCP@627
DEBUG ASGN@642: source=t640_0, has_producer=True
  producer: DCP@640
DEBUG ASGN@660: source=t658_0, has_producer=True
  producer: DCP@658
DEBUG ASGN@676: source=t674_0, has_producer=True
  producer: DCP@674
DEBUG ASGN@681: source=t679_0, has_producer=True
  producer: GCP@679
DEBUG ASGN@706: source=t700_0, has_producer=True
  producer: SUB@700
DEBUG ASGN@733: source=t727_0, has_producer=True
  producer: ADD@727
DEBUG ASGN@745: source=t743_0, has_producer=True
  producer: GCP@743
DEBUG ASGN@765: source=t763_0, has_producer=True
  producer: DCP@763
DEBUG ASGN@771: source=t769_0, has_producer=True
  producer: DCP@769
DEBUG ASGN@775: source=t773_0, has_producer=True
  producer: GCP@773
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

