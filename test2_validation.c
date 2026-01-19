Skipping orphaned block 2 at address 13 in function func_0010 - no predecessors (unreachable code)
// Structured decompilation of decompiler_source_tests/test2/tdm.scr
// Functions: 3

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword gRecs;
s_SC_MP_Recover gRec[64];
dword gVar;
dword gVar1;
float gRecTimer[64];
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

// Function ScriptMain at -112 - entry block not found

int func_0010(float param_0) {
    int data_;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;

    goto block_3; // @17
    block_3:
    if (!tmp1) {
        data_ = tmp2;
    } else {
        SC_MP_EndRule_SetTimeLeft(data_, tmp3);
        SC_MP_LoadNextMap();
        return TRUE;
        SC_MP_LoadNextMap();
        return TRUE;
        SC_message("EndRule unsopported: %d", gEndRule);
        return FALSE;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0096(void) {
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    SC_sgi(GVAR_SIDE0FRAGS, tmp1);
    SC_sgi(GVAR_SIDE1FRAGS, tmp3);
    return FALSE;
}

