"""
Regression test for default-case break preservation in switch reconstruction.
"""

from pathlib import Path

from vcdecomp.core.loader import SCRFile
from vcdecomp.core.disasm import Disassembler
from vcdecomp.core.ir.ssa import build_ssa_all_blocks
from vcdecomp.core.ir.structure import format_structured_function_named


def _extract_default_block_lines(output: str) -> list[str]:
    lines = output.splitlines()
    default_index = None
    for idx, line in enumerate(lines):
        if line.strip() == "default:":
            default_index = idx
            break
    if default_index is None:
        return []

    default_lines = []
    for line in lines[default_index + 1:]:
        stripped = line.strip()
        if stripped.startswith("case ") or stripped == "default:" or stripped == "}":
            break
        default_lines.append(line)
    return default_lines


def test_srv_check_end_rule_default_break():
    scr_path = Path("decompiler_source_tests/test2/tdm.scr")
    assert scr_path.exists(), "Expected tdm.scr fixture to be available"

    scr = SCRFile.load(str(scr_path))
    ssa_func = build_ssa_all_blocks(scr)
    disasm = Disassembler(scr)
    func_bounds = disasm.get_function_boundaries()

    target_output = None
    for func_name, (start, end) in func_bounds.items():
        try:
            output = format_structured_function_named(
                ssa_func, func_name, start, end, func_bounds, "quiet"
            )
        except Exception:
            continue
        if "switch (gEndRule)" in output:
            target_output = output
            break

    assert target_output is not None, "Expected SRV_CheckEndRule output to be found"

    default_lines = _extract_default_block_lines(target_output)
    assert default_lines, "Expected default case in SRV_CheckEndRule output"
    assert any("SC_message(" in line for line in default_lines)
    assert any(line.strip() == "break;" for line in default_lines)
    assert not any(line.strip() == "return TRUE;" for line in default_lines)
