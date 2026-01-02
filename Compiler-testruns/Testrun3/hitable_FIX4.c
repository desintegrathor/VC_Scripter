[DEBUG PHI ALL] @-1 PHI phi_3_0_0 (alias=None), var_name=None, inputs=[('t3_0', None)]
[DEBUG PHI ALL] @-2 PHI phi_12_0_1 (alias=data_5), var_name=None, inputs=[('t30_0', 'data_5')]
[DEBUG PHI ALL] @-3 PHI phi_12_1_2 (alias=None), var_name=None, inputs=[('t33_0', None)]
[DEBUG PHI ALL] @-4 PHI phi_14_0_3 (alias=data_5), var_name=None, inputs=[('phi_12_0_1', 'data_5')]
[DEBUG PHI ALL] @-5 PHI phi_14_1_4 (alias=None), var_name=None, inputs=[('phi_12_1_2', None)]
[DEBUG PHI ALL] @-6 PHI phi_15_0_5 (alias=data_5), var_name=None, inputs=[('phi_14_0_3', 'data_5')]
[DEBUG PHI ALL] @-7 PHI phi_15_1_6 (alias=None), var_name=None, inputs=[('phi_14_1_4', None)]
// Structured decompilation of Compiler-testruns/Testrun3/hitable.scr
// Functions: 2

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\sc_level.h>

// Global variables
dword gVar;

int _init(s_SC_OBJ_info *info) {
    return FALSE;
}

int ScriptMain(s_SC_OBJ_info *info) {
    int local_0;

    switch (gVar) {
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

