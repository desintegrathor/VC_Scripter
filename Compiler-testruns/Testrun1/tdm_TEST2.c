[DEBUG PHI ALL] @-1 PHI phi_3_0_0 (alias=data_328), var_name=None, inputs=[('t10_0', 'data_328')]
[DEBUG PHI ALL] @-2 PHI phi_3_0_0 (alias=data_328), var_name=None, inputs=[('t10_0', 'data_328')]
[DEBUG PHI ALL] @-3 PHI phi_3_0_0 (alias=data_328), var_name=None, inputs=[('t10_0', 'data_328')]
[DEBUG PHI ALL] @-4 PHI phi_3_0_0 (alias=data_328), var_name=None, inputs=[('t10_0', 'data_328')]
[DEBUG PHI ALL] @-5 PHI phi_3_0_0 (alias=data_328), var_name=None, inputs=[('t10_0', 'data_328')]
[DEBUG PHI ALL] @-6 PHI phi_9_0_1 (alias=data_328), var_name=None, inputs=[('phi_3_0_0', 'data_328')]
[DEBUG PHI ALL] @-7 PHI phi_9_1_2 (alias=data_330), var_name=None, inputs=[('t27_0', 'data_330')]
[DEBUG PHI ALL] @-8 PHI phi_9_2_3 (alias=None), var_name=None, inputs=[('t30_0', None)]
[DEBUG PHI ALL] @-9 PHI phi_9_0_1 (alias=data_328), var_name=None, inputs=[('phi_3_0_0', 'data_328')]
[DEBUG PHI ALL] @-10 PHI phi_9_1_2 (alias=data_330), var_name=None, inputs=[('t27_0', 'data_330')]
[DEBUG PHI ALL] @-11 PHI phi_9_2_3 (alias=None), var_name=None, inputs=[('t30_0', None)]
[DEBUG PHI ALL] @-12 PHI phi_9_0_1 (alias=data_328), var_name=None, inputs=[('phi_3_0_0', 'data_328')]
[DEBUG PHI ALL] @-13 PHI phi_9_1_2 (alias=data_330), var_name=None, inputs=[('t27_0', 'data_330')]
[DEBUG PHI ALL] @-14 PHI phi_9_2_3 (alias=None), var_name=None, inputs=[('t30_0', None)]
[DEBUG PHI ALL] @-15 PHI phi_9_0_1 (alias=data_328), var_name=None, inputs=[('phi_3_0_0', 'data_328')]
[DEBUG PHI ALL] @-16 PHI phi_9_1_2 (alias=data_330), var_name=None, inputs=[('t27_0', 'data_330')]
[DEBUG PHI ALL] @-17 PHI phi_9_2_3 (alias=None), var_name=None, inputs=[('t30_0', None)]
[DEBUG PHI ALL] @-18 PHI phi_9_0_1 (alias=data_328), var_name=None, inputs=[('phi_3_0_0', 'data_328')]
[DEBUG PHI ALL] @-19 PHI phi_9_1_2 (alias=data_330), var_name=None, inputs=[('t27_0', 'data_330')]
[DEBUG PHI ALL] @-20 PHI phi_9_2_3 (alias=None), var_name=None, inputs=[('t30_0', None)]
[DEBUG PHI ALL] @-21 PHI phi_9_0_1 (alias=data_328), var_name=None, inputs=[('phi_3_0_0', 'data_328')]
[DEBUG PHI ALL] @-22 PHI phi_9_1_2 (alias=data_330), var_name=None, inputs=[('t27_0', 'data_330')]
[DEBUG PHI ALL] @-23 PHI phi_9_2_3 (alias=None), var_name=None, inputs=[('t30_0', None)]
[DEBUG PHI ALL] @-24 PHI phi_9_0_1 (alias=data_328), var_name=None, inputs=[('phi_3_0_0', 'data_328')]
[DEBUG PHI ALL] @-25 PHI phi_9_1_2 (alias=data_330), var_name=None, inputs=[('t27_0', 'data_330')]
[DEBUG PHI ALL] @-26 PHI phi_9_2_3 (alias=None), var_name=None, inputs=[('t30_0', None)]
[DEBUG PHI ALL] @-27 PHI phi_9_0_1 (alias=data_328), var_name=None, inputs=[('phi_3_0_0', 'data_328')]
[DEBUG PHI ALL] @-28 PHI phi_9_1_2 (alias=data_330), var_name=None, inputs=[('t27_0', 'data_330')]
[DEBUG PHI ALL] @-29 PHI phi_9_2_3 (alias=None), var_name=None, inputs=[('t30_0', None)]
[DEBUG PHI ALL] @-30 PHI phi_17_0_4 (alias=data_328), var_name=None, inputs=[('phi_9_0_1', 'data_328')]
[DEBUG PHI ALL] @-31 PHI phi_17_1_5 (alias=data_330), var_name=None, inputs=[('phi_9_1_2', 'data_330')]
[DEBUG PHI ALL] @-32 PHI phi_17_2_6 (alias=None), var_name=None, inputs=[('phi_9_2_3', None)]
[DEBUG PHI ALL] @-33 PHI phi_17_0_4 (alias=data_328), var_name=None, inputs=[('phi_9_0_1', 'data_328')]
[DEBUG PHI ALL] @-34 PHI phi_17_1_5 (alias=data_330), var_name=None, inputs=[('phi_9_1_2', 'data_330')]
[DEBUG PHI ALL] @-35 PHI phi_17_2_6 (alias=None), var_name=None, inputs=[('phi_9_2_3', None)]
Error: argument of type 'CFG' is not iterable
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\__main__.py", line 532, in <module>
    main()
    ~~~~^^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\__main__.py", line 279, in main
    cmd_structure(args)
    ~~~~~~~~~~~~~^^^^^^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\__main__.py", line 481, in cmd_structure
    text = format_structured_function_named(ssa_func, func_name, func_start, func_end, function_bounds=func_bounds)
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\structure.py", line 2942, in format_structured_function_named
    case_lines = _render_blocks_with_loops(
        case_body_sorted,
    ...<11 lines>...
        early_returns
    )
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\structure.py", line 858, in _render_blocks_with_loops
    lines.extend(_format_block_lines(
                 ~~~~~~~~~~~~~~~~~~~^
        ssa_func, body_block_id, indent, formatter,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        early_returns
        ^^^^^^^^^^^^^
    ))
    ^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\structure.py", line 289, in _format_block_lines
    return _render_if_else_recursive(
        block_to_if[block_id], indent, ssa_func, formatter,
        block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
        early_returns
    )
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\structure.py", line 392, in _render_if_else_recursive
    true_block_lines = _format_block_lines(
        ssa_func, compound.true_target, indent + "    ", formatter,
        cfg, block_to_if, visited_ifs, start_to_block, resolver, emitted_blocks,
        early_returns
    )
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\structure.py", line 287, in _format_block_lines
    block_id in block_to_if and block_id == block_to_if[block_id].header_block and
    ^^^^^^^^^^^^^^^^^^^^^^^
TypeError: argument of type 'CFG' is not iterable
// Structured decompilation of Compiler-testruns/Testrun1/tdm.scr
// Functions: 4

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\mplevel.inc>

// Global variables
dword gRecs;
s_SC_MP_Recover * gRec;
dword gVar;
dword gVar1;
float * gRecTimer;
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

int _init(s_SC_NET_info *info) {
    int local_0;

    DLD();
    DLD();
    return FALSE;
}

