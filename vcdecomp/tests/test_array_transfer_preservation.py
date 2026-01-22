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
    output = None
    for func_name, (start, end) in func_bounds.items():
        candidate = format_structured_function_named(
            ssa_func, func_name, start, end, resolver
        )
        if "SC_2VectorsDist" in candidate:
            output = candidate
            break

    assert output is not None, "GetFarestWills function not found in decompiled output"

    expected_block = textwrap.dedent(
        """
        local_3[1] = local_3[0];
        param_0[1] = param_0[0];
        """
    ).strip()

    normalized_output = _normalize_output(output)
    normalized_expected = _normalize_output(expected_block)

    assert normalized_expected in normalized_output
