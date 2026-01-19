py : Skipping orphaned block 2 at address 312 in function func_0292 - no predecessors (unreachable code)
At line:1 char:169
+ ... oding UTF8; py -m vcdecomp structure decompiler_source_tests\test3\LE ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Skipping orphan...reachable code):String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
Skipping orphaned block 3 at address 316 in function func_0292 - no predecessors (unreachable code)
Skipping orphaned block 4 at address 329 in function func_0292 - no predecessors (unreachable code)
Skipping orphaned block 5 at address 336 in function func_0292 - no predecessors (unreachable code)
Skipping orphaned block 6 at address 337 in function func_0292 - no predecessors (unreachable code)
Skipping orphaned block 7 at address 345 in function func_0292 - no predecessors (unreachable code)
Skipping orphaned block 8 at address 354 in function func_0292 - no predecessors (unreachable code)
Skipping orphaned block 10 at address 362 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 11 at address 366 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 12 at address 370 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 13 at address 374 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 14 at address 378 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 15 at address 391 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 16 at address 395 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 17 at address 404 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 18 at address 413 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 19 at address 417 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 20 at address 421 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 21 at address 434 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 22 at address 438 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 23 at address 447 in function func_0355 - no predecessors (unreachable code)
Skipping orphaned block 32 at address 527 in function func_0511 - no predecessors (unreachable code)
Skipping orphaned block 33 at address 531 in function func_0511 - no predecessors (unreachable code)
Skipping orphaned block 34 at address 552 in function func_0511 - no predecessors (unreachable code)
Skipping orphaned block 35 at address 583 in function func_0511 - no predecessors (unreachable code)
Skipping orphaned block 36 at address 590 in function func_0511 - no predecessors (unreachable code)
Skipping orphaned block 37 at address 602 in function func_0511 - no predecessors (unreachable code)
Skipping orphaned block 38 at address 611 in function func_0511 - no predecessors (unreachable code)
Skipping orphaned block 41 at address 633 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 42 at address 637 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 43 at address 644 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 44 at address 645 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 45 at address 658 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 46 at address 666 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 47 at address 675 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 48 at address 683 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 49 at address 687 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 50 at address 694 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 51 at address 702 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 52 at address 711 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 53 at address 715 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 54 at address 720 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 55 at address 721 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 57 at address 739 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 61 at address 821 in function func_0612 - no predecessors (unreachable code)
Skipping orphaned block 67 at address 909 in function func_0612 - no predecessors (unreachable code)
// Structured decompilation of decompiler_source_tests\test3\LEVEL.SCR
// Functions: 9

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword SGI_ALLYDEATHCOUNT;
dword SGI_LEVELPHASE;
dword gVar;
int SGI_CURRENTMISSION;
int gphase;
int g_dialog;
dword g_will_group[4];
int g_dochange;
int g_final_enter_timer;
dword g_will_pos[12];
dword g_vill_visited[4];
int g_pilot_phase;
int g_pilot_timer;
dword g_pilot_vill_nr;
int g_showinfo_timer;
int g_trashes_enabled;
dword gShot_pos[3];
int gEndTimer;
int gPilotCommTime;
dword g_save[2];
dword g_music[2];
int gStartMusicTime;
dword SGI_LEVPILOT_S1G0;
dword SGI_LEVPILOT_S1G1;
dword SGI_LEVPILOT_S1G2;
dword SGI_LEVPILOT_S1G3;
dword SGI_LEVPILOT_S1G4;
dword SGI_LEVPILOT_EVACVILLID;
dword SGI_LEVPILOT_HELI3_ATTACK;
dword SGI_LEVPILOT_JUSTLOADEDVALUE;
dword SGI_REWARD_PILOT;
dword SGI_DEBR_01;

// Function ScriptMain at -1058 - entry block not found

void func_0292(void) {
    int j;
    int tmp;
    int vec;
    s_SC_MP_EnumPlayers tmp2;

    SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0);
    SC_ZeroMem(&vec, 12);
    *tmp = -962838528;
    tmp2 = 0;
    return;
}

void func_0355(void) {
    int k;
    int tmp;

    tmp = 0;
    return;
}

void func_0448(void) {
    int j;

    SC_P_GetBySideGroupMember(2, 0, 1);
    return FALSE;
}

void func_0511(void) {
    dword local_3[16];
    int idx;
    int tmp;
    int vec;

    SC_P_GetPos(param_0, &vec);
    SC_ZeroMem(&local_3, 8);
    tmp = 0;
    return;
}

void func_0612(void) {
    c_Vector3 local_7;
    int data_;
    int j;
    int local_;
    int local_10;
    int local_11;
    int local_12;
    int local_13;
    int local_14;
    int local_2;
    int local_4;
    int tmp;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
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
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;
    int vec;
    s_SC_MP_EnumPlayers tmp1;

    if (!tmp) {
        SC_PC_GetPos(&local_4);
        tmp1 = 0;
    } else {
        tmp3 = tmp2;
        data_ = 2;
        SC_PC_Get();
        func_0511(local_, &local_2);
        rand();
        tmp9 = tmp8;
        func_0448();
        SC_P_ScriptMessage(local_, 0, tmp9);
        frnd(30.0f);
        tmp3 = tmp10;
        rand();
        SC_SpeechRadio2(tmp14, 0.0f);
        func_0448();
        SC_HUD_RadarShowPlayer(local_, -16711936);
        tmp3 = tmp15;
        data_ = 1;
        frnd(10.0f);
        tmp3 = tmp17;
        tmp9 = 255;
        func_0448();
        SC_P_ScriptMessage(local_, 0, tmp9);
        SC_HUD_RadarShowPlayer(0, 0);
        SC_PC_GetPos(&local_4);
        func_0448();
        SC_P_GetPos(local_, &local_7);
        SC_IsNear2D(&local_4, &local_7, tmp18);
        data_ = 4;
        tmp3 = 0;
        SC_SetSideAlly(1, 2, -1.0f);
        SC_sgi(SGI_LEVELPHASE, 2);
        SC_ggi(tmp25);
        tmp3 = tmp20;
        tmp3 = 1069547520;
        func_0448();
        SC_PC_Get();
        local_10 = SC_P_GetDistance(local_13, tmp24);
        SC_PC_GetPos(&local_7);
        func_0448();
        SC_P_Ai_Go(local_, &local_7);
        func_0448();
        SC_P_Ai_Stop(local_);
        return &local_7;
    }
    return;
}

void func_0985(void) {
    SC_P_Ai_SetMoveMode(param_0, SC_P_AI_MOVEMODE_SNEAK);
    SC_P_Ai_SetMovePos(param_0, SC_P_AI_MOVEPOS_STAND);
    return FALSE;
}

void func_0994(void) {
    int j;
    int k;
    int tmp;
    s_SC_MP_EnumPlayers local_;

    tmp = param_0;
    local_ = SC_NOD_Get(0, "maj_uh-1d_vreck");
    if (!local_) {
        SC_DUMMY_Set_DoNotRenHier2(local_, 1);
    } else {
        return TRUE;
    }
    return;
}

void func_1021(void) {
    int enum_pl;
    int local_;
    int local_256;
    int local_257;
    int tmp;

    local_ = 64;
    SC_sgi(SGI_DEBR_01, 0);
    SC_sgi(SGI_REWARD_PILOT, 1);
    SC_MP_EnumPlayers(&enum_pl, &local_, 1);
    if (!local_257) {
        SC_sgi(SGI_DEBR_01, -1);
        SC_sgi(SGI_REWARD_PILOT, 0);
    } else {
        return 257;
    }
    if (!tmp) goto block_88; // @1056
    return;
}

