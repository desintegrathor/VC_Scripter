py : Skipping orphaned block 2 at address 13 in function func_0010 - no predecessors (unreachable code)
At line:1 char:50
+ ... _Scripter'; py -m vcdecomp structure decompiler_source_tests\test2\td ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Skipping orphan...reachable code):String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
// Structured decompilation of decompiler_source_tests\test2\tdm.scr
// Functions: 3

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword gRecs;
dword gRec[64];
dword SGI_ALLYDEATHCOUNT;
dword gVar;
dword gRecTimer[64];
dword gNextRecover;
dword gSideFrags[2];
dword gCLN_SideFrags[2];
int gEndRule;
int gEndValue;
int gTime;
int gPlayersConnected;
dword gVar3;
dword gVar1;
dword gVar2;

// Function ScriptMain at -112 - entry block not found

void func_0010(void) {
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
    return;
}

void func_0096(void) {
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    SC_sgi(GVAR_SIDE0FRAGS, tmp1);
    SC_sgi(GVAR_SIDE1FRAGS, tmp3);
    return FALSE;
}

