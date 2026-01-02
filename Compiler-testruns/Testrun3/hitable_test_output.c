[DEBUG structure.py:1655] _trace_value_to_parameter() returned: None
[DEBUG structure.py:1657] _trace_value_to_global() returned: None
[DEBUG structure.py:1660] render_value() returned: 'local_0'
[DEBUG structure.py:1664] Switch test_var set to: 'local_0'
[DEBUG structure.py:1655] _trace_value_to_parameter() returned: None
[DEBUG structure.py:1657] _trace_value_to_global() returned: None
[DEBUG structure.py:1660] render_value() returned: 'local_0'
[DEBUG structure.py:1655] _trace_value_to_parameter() returned: None
[DEBUG structure.py:1657] _trace_value_to_global() returned: None
[DEBUG structure.py:1660] render_value() returned: 'local_0'
[DEBUG structure.py:1655] _trace_value_to_parameter() returned: None
[DEBUG structure.py:1657] _trace_value_to_global() returned: None
[DEBUG structure.py:1660] render_value() returned: 'local_0'
[DEBUG structure.py:1655] _trace_value_to_parameter() returned: None
[DEBUG structure.py:1657] _trace_value_to_global() returned: None
[DEBUG structure.py:1660] render_value() returned: 'local_0'
[DEBUG structure.py:1655] _trace_value_to_parameter() returned: None
[DEBUG structure.py:1657] _trace_value_to_global() returned: None
[DEBUG structure.py:1660] render_value() returned: 'local_0'
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
    goto block_6; // @18
}

