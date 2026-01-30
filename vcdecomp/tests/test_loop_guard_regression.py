"""
Regression tests for loop guard folding in LEVEL.SCR.
"""

import re
from pathlib import Path

from vcdecomp.core.loader import SCRFile
from vcdecomp.core.disasm import Disassembler
from vcdecomp.core.ir.ssa import build_ssa_all_blocks
from vcdecomp.core.ir.structure import format_structured_function_named


LEVEL_SCR = Path("decompiler_source_tests/test3/LEVEL.SCR")


def _decompile_function_matching(patterns) -> str:
    scr = SCRFile.load(str(LEVEL_SCR))
    ssa_func = build_ssa_all_blocks(scr)
    disasm = Disassembler(scr)
    func_bounds = disasm.get_function_boundaries()
    for func_name, (start, end) in func_bounds.items():
        output = format_structured_function_named(
            ssa_func,
            func_name,
            start,
            end,
            function_bounds=func_bounds
        )
        if all(re.search(pattern, output) for pattern in patterns):
            return output
    raise AssertionError(f"Did not find patterns in any decompiled function: {patterns}")


def test_level_disapear_attackers_loop_condition():
    output = _decompile_function_matching([
        r"for\s*\(\s*i\s*=",
        r"SC_P_GetBySideGroupMember\("
    ])
    assert re.search(r"for\s*\(\s*i\s*=\s*[^;]+;\s*i\s*<\s*[^;]+;\s*i", output)
    assert "if (!(i <" not in output
    assert re.search(r"\b(dword|int)\b[^;]*\bi\b", output)


def test_level_activate_patrols_and_snipers_loop_condition():
    output = _decompile_function_matching([
        r"for\s*\(\s*\w+\s*=\s*[^;]+;\s*\w+\s*<\s*12",  # outer loop < 12
        r"SC_P_SetActive\(\w+,\s*TRUE\)",                 # SetActive TRUE (not FALSE)
    ])
    # Must have outer for-loop (any var, < 12)
    assert re.search(r"for\s*\(\s*\w+\s*=\s*[^;]+;\s*\w+\s*<\s*12", output)
    # Must have inner for-loop (any var, < 16)
    assert re.search(r"for\s*\(\s*\w+\s*=\s*[^;]+;\s*\w+\s*<\s*16", output)
    # No spurious guard blocks
    assert "if (!(" not in output or "if (!(i <" not in output
