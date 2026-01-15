Error: 'VariableVersion' object has no attribute 'ssa_names'
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\__main__.py", line 1024, in <module>
    main()
    ~~~~^^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\__main__.py", line 311, in main
    cmd_structure(args)
    ~~~~~~~~~~~~~^^^^^^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\__main__.py", line 560, in cmd_structure
    text = format_structured_function_named(ssa_func, func_name, func_start, func_end, function_bounds=func_bounds)
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\structure\orchestrator.py", line 193, in format_structured_function_named
    rename_map = renamer.analyze_and_rename()
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\variable_renaming.py", line 138, in analyze_and_rename
    self._infer_semantic_types()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\variable_renaming.py", line 548, in _infer_semantic_types
    ver.semantic_type = self._guess_semantic_type(var_name, ver)
                        ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\variable_renaming.py", line 594, in _guess_semantic_type
    for ssa_name in ver.ssa_names:
                    ^^^^^^^^^^^^^
AttributeError: 'VariableVersion' object has no attribute 'ssa_names'
// Structured decompilation of decompilation/TUNNELS01/SCRIPTS/LEVEL.scr
// Functions: 240

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword gVar;
BOOL gVar1;
BOOL gVar2;
dword gVar3;
dword gVar20;
dword gVar19;
dword gVar17;
dword gVar4;
BOOL gVar5;
dword gVar6;
dword gVar7;
dword gVar8;
int gVar9;
dword gVar10;
dword gVar11;
int gVar12;
dword gVar13;
dword gVar14;
int gVar15;
dword gVar16;
dword gData;
dword gphase;
dword gVar18;

