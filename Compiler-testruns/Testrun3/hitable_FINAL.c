// Structured decompilation of Compiler-testruns/Testrun3/hitable.scr
// Functions: 2

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\sc_level.h>

int _init(s_SC_OBJ_info *info) {
    return FALSE;
}

int ScriptMain(s_SC_OBJ_info *info) {
    int local_0;

    switch (local_0) {
    case 3:
        return TRUE;
    case 7:
        break;
    case 5:
        break;
    case 1:
        SC_LevScr_Event(52, info->master_nod);
        break;
    case 4:
        break;
    case 6:
        break;
    default:
        return FALSE;
    }
}

