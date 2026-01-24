import textwrap
from pathlib import Path

from vcdecomp.core.loader import SCRFile
from vcdecomp.core.disasm import Disassembler
from vcdecomp.core.ir.ssa import build_ssa_all_blocks
from vcdecomp.core.ir.structure import format_structured_function_named
from vcdecomp.core.ir.global_resolver import GlobalResolver


def _normalize_output(text: str) -> str:
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def test_get_farest_wills_preserves_array_transfer():
    scr_path = Path("decompiler_source_tests/test3/LEVEL.SCR")
    scr = SCRFile.load(str(scr_path))
    ssa_func = build_ssa_all_blocks(scr)

    disasm = Disassembler(scr)
    resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
    resolver.analyze()

    func_bounds = disasm.get_function_boundaries()

    # Look for the func_0511 function which is GetFarestWills in LEVEL.SCR
    # It has the specific array transfer pattern we're testing for
    output = None
    target_func = "func_0511"
    for func_name, (start, end) in func_bounds.items():
        if func_name == target_func:
            output = format_structured_function_named(
                ssa_func, func_name, start, end, func_bounds
            )
            break

    assert output is not None, f"Function {target_func} not found in decompiled output"
    assert "SC_2VectorsDist" in output, "GetFarestWills should contain SC_2VectorsDist call"

    # Test that array transfer patterns are preserved in decompiled output.
    # The key pattern is param_0[1] = param_0[0]; which shows array element transfer.
    expected_patterns = [
        "param_0[1] = param_0[0];",  # Array index transfer pattern
    ]

    for pattern in expected_patterns:
        assert pattern in output, f"Expected pattern not found: {pattern}"
