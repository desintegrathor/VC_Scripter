// Structured decompilation of Compiler-testruns/Testrun3/hitable.scr
// Functions: 2

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\sc_level.h>

int _init(s_SC_OBJ_info *info) {
    // Block 0 @0
    return FALSE;
}

int ScriptMain(s_SC_OBJ_info *info) {
    // Block 1 @1
    switch (local_0) {
    case 3:
        // Block 3 @10
        return TRUE;
    case 7:
        // Block 6 @18
        break;
    case 5:
        // Block 8 @24
        break;
    case 1:
        // Block 10 @30
        SC_LevScr_Event(SCM_OBJECTDESTROYED, info->master_nod);
        break;
    case 4:
        // Block 12 @42
        break;
    case 6:
        // Block 14 @48
        break;
    default:
        // Block 15 @49
        return FALSE;
    }
    // Block 4 @13
    goto block_6; // @18
}

