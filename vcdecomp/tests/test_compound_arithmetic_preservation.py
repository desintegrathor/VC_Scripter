import unittest

from vcdecomp.core.disasm import opcodes
from vcdecomp.core.ir.expr import ExpressionFormatter, format_block_expressions
from vcdecomp.core.ir.ssa import SSAFunction, SSAInstruction, SSAValue, _mark_simple_arithmetic_compound_stores


class _MockDataSegment:
    raw_data = b""

    @staticmethod
    def get_dword(offset: int) -> int:
        return 0


class _MockSCR:
    data_segment = _MockDataSegment()
    xfn_table = []

    @staticmethod
    def get_xfn(_idx):
        return None


def _make_value(name: str, alias: str) -> SSAValue:
    return SSAValue(name=name, alias=alias, value_type=opcodes.ResultType.INT)


def _build_compound_store(op_mnemonic: str, target_expr: str, rhs_expr: str, temp_name: str) -> SSAFunction:
    left_value = _make_value(f"{temp_name}_lhs", target_expr)
    right_value = _make_value(f"{temp_name}_rhs", rhs_expr)

    temp_value = SSAValue(
        name=temp_name,
        value_type=opcodes.ResultType.INT,
        metadata={"simple_arithmetic": True},
    )

    add_inst = SSAInstruction(
        block_id=0,
        mnemonic=op_mnemonic,
        address=1,
        inputs=[left_value, right_value],
        outputs=[temp_value],
    )
    temp_value.producer_inst = add_inst
    temp_value.uses.append((2, 0))

    addr_value = _make_value(f"{temp_name}_addr", f"&{target_expr}")

    asgn_inst = SSAInstruction(
        block_id=0,
        mnemonic="ASGN",
        address=2,
        inputs=[temp_value, addr_value],
        outputs=[],
    )

    instructions = {0: [add_inst, asgn_inst]}
    values = {
        left_value.name: left_value,
        right_value.name: right_value,
        temp_value.name: temp_value,
        addr_value.name: addr_value,
    }
    ssa_func = SSAFunction(cfg=None, values=values, instructions=instructions, scr=_MockSCR())
    ssa_func._cached_global_type_info_bytes = {}
    _mark_simple_arithmetic_compound_stores(ssa_func.instructions)
    return ssa_func


class TestCompoundArithmeticPreservation(unittest.TestCase):
    def _render_single_line(self, ssa_func: SSAFunction, temp_name: str) -> str:
        formatter = ExpressionFormatter(ssa_func, rename_map={temp_name: "tmp0"})
        expressions = format_block_expressions(ssa_func, 0, formatter)
        self.assertEqual(len(expressions), 1)
        return expressions[0].text

    def test_preserves_add_equals(self):
        ssa_func = _build_compound_store("ADD", "gTime", "time", "t_add_time")
        output = self._render_single_line(ssa_func, "t_add_time")
        self.assertEqual(output, "gTime += time;")

    def test_preserves_sub_equals(self):
        ssa_func = _build_compound_store(
            "SUB",
            "gRecTimer[i]",
            "info->elapsed_time",
            "t_sub_timer",
        )
        output = self._render_single_line(ssa_func, "t_sub_timer")
        self.assertEqual(output, "gRecTimer[i] -= info->elapsed_time;")

    def test_preserves_increment(self):
        ssa_func = _build_compound_store("ADD", "gSideFrags[side]", "1", "t_inc_frags")
        output = self._render_single_line(ssa_func, "t_inc_frags")
        self.assertEqual(output, "gSideFrags[side]++;")


if __name__ == "__main__":
    unittest.main()
