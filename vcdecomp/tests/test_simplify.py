"""
Unit tests for expression simplification rules.

Tests the Ghidra-inspired simplification framework:
- Constant folding
- Algebraic identities
- Canonical term ordering
- Bitwise operation simplification
"""

import unittest
from dataclasses import field
from typing import Dict, List

from vcdecomp.core.ir.ssa import SSAFunction, SSAInstruction, SSAValue, SSAFunction
from vcdecomp.core.ir.cfg import CFG, BasicBlock
from vcdecomp.core.disasm import opcodes
from vcdecomp.core.ir.simplify import (
    RuleConstantFold,
    RuleTermOrder,
    RuleAndIdentity,
    RuleOrIdentity,
    RuleAddIdentity,
    RuleMulIdentity,
    RuleAndMask,
    RuleOrMask,
    simplify_expressions,
    create_constant_value,
)


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions for creating test SSA structures."""

    def create_test_ssa_function(self) -> SSAFunction:
        """Create a minimal SSA function for testing."""
        cfg = CFG(
            blocks={
                0: BasicBlock(block_id=0, start=0, end=100, predecessors=set(), successors=set())
            },
            entry_block=0,
            idom={0: 0},
            dom_tree={0: []},
            dom_order=[0]
        )

        return SSAFunction(
            cfg=cfg,
            values={},
            instructions={0: []},
            scr=None  # Not needed for these tests
        )

    def create_constant(self, value: int, ssa_func: SSAFunction, name: str = None) -> SSAValue:
        """Create a constant SSA value."""
        if name is None:
            name = f"const_{value}"

        const_val = SSAValue(
            name=name,
            value_type=opcodes.ResultType.INT,
            producer=None,
            metadata={"constant_value": value}
        )
        ssa_func.values[name] = const_val
        return const_val

    def create_variable(self, name: str, ssa_func: SSAFunction) -> SSAValue:
        """Create a variable SSA value."""
        var_val = SSAValue(
            name=name,
            value_type=opcodes.ResultType.INT,
            producer=100,  # Some address
        )
        ssa_func.values[name] = var_val
        return var_val

    def create_instruction(
        self,
        mnemonic: str,
        inputs: List[SSAValue],
        output_name: str,
        ssa_func: SSAFunction,
        address: int = 100
    ) -> SSAInstruction:
        """Create an SSA instruction."""
        output_val = SSAValue(
            name=output_name,
            value_type=opcodes.ResultType.INT,
            producer=address
        )
        ssa_func.values[output_name] = output_val

        inst = SSAInstruction(
            block_id=0,
            mnemonic=mnemonic,
            address=address,
            inputs=inputs,
            outputs=[output_val]
        )

        output_val.producer_inst = inst
        return inst


class TestRuleConstantFold(unittest.TestCase):
    """Test constant folding rule."""

    def test_add_constants(self):
        """Test: 2 + 3 → 5"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        const_2 = helper.create_constant(2, ssa_func)
        const_3 = helper.create_constant(3, ssa_func)

        inst = helper.create_instruction("ADD", [const_2, const_3], "temp_1", ssa_func)

        rule = RuleConstantFold()
        self.assertTrue(rule.matches(inst, ssa_func))

        result = rule.apply(inst, ssa_func)
        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "CONST")
        self.assertEqual(result.inputs[0].metadata["constant_value"], 5)

    def test_mul_constants(self):
        """Test: 10 * 4 → 40"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        const_10 = helper.create_constant(10, ssa_func)
        const_4 = helper.create_constant(4, ssa_func)

        inst = helper.create_instruction("MUL", [const_10, const_4], "temp_1", ssa_func)

        rule = RuleConstantFold()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        self.assertEqual(result.inputs[0].metadata["constant_value"], 40)

    def test_bitwise_and_constants(self):
        """Test: 0xff & 0x0f → 0x0f"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        const_ff = helper.create_constant(0xff, ssa_func)
        const_0f = helper.create_constant(0x0f, ssa_func)

        inst = helper.create_instruction("BA", [const_ff, const_0f], "temp_1", ssa_func)

        rule = RuleConstantFold()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        self.assertEqual(result.inputs[0].metadata["constant_value"], 0x0f)

    def test_neg_constant(self):
        """Test: NEG(5) → -5"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        const_5 = helper.create_constant(5, ssa_func)

        inst = helper.create_instruction("NEG", [const_5], "temp_1", ssa_func)

        rule = RuleConstantFold()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        # -5 as unsigned 32-bit
        expected = (-5) & 0xFFFFFFFF
        self.assertEqual(result.inputs[0].metadata["constant_value"], expected)

    def test_no_fold_with_variables(self):
        """Test: x + 3 should not fold (x is not constant)"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)
        const_3 = helper.create_constant(3, ssa_func)

        inst = helper.create_instruction("ADD", [var_x, const_3], "temp_1", ssa_func)

        rule = RuleConstantFold()
        self.assertFalse(rule.matches(inst, ssa_func))


class TestRuleTermOrder(unittest.TestCase):
    """Test canonical term ordering rule."""

    def test_swap_const_to_right(self):
        """Test: 3 + x → x + 3"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        const_3 = helper.create_constant(3, ssa_func)
        var_x = helper.create_variable("x", ssa_func)

        inst = helper.create_instruction("ADD", [const_3, var_x], "temp_1", ssa_func)

        rule = RuleTermOrder()
        self.assertTrue(rule.matches(inst, ssa_func))

        result = rule.apply(inst, ssa_func)
        self.assertIsNotNone(result)
        self.assertEqual(result.inputs[0].name, "x")
        self.assertEqual(result.inputs[1].name, "const_3")

    def test_order_by_name(self):
        """Test: z + x → x + z (alphabetical order)"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_z = helper.create_variable("z", ssa_func)
        var_x = helper.create_variable("x", ssa_func)

        inst = helper.create_instruction("ADD", [var_z, var_x], "temp_1", ssa_func)

        rule = RuleTermOrder()
        self.assertTrue(rule.matches(inst, ssa_func))

        result = rule.apply(inst, ssa_func)
        self.assertEqual(result.inputs[0].name, "x")
        self.assertEqual(result.inputs[1].name, "z")

    def test_no_swap_for_non_commutative(self):
        """Test: 3 - x should NOT swap (subtraction is not commutative)"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        const_3 = helper.create_constant(3, ssa_func)
        var_x = helper.create_variable("x", ssa_func)

        inst = helper.create_instruction("SUB", [const_3, var_x], "temp_1", ssa_func)

        rule = RuleTermOrder()
        self.assertFalse(rule.matches(inst, ssa_func))


class TestRuleAndIdentity(unittest.TestCase):
    """Test bitwise AND identity rule."""

    def test_and_with_zero(self):
        """Test: x & 0 → 0"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)
        const_0 = helper.create_constant(0, ssa_func)

        inst = helper.create_instruction("BA", [var_x, const_0], "temp_1", ssa_func)

        rule = RuleAndIdentity()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "CONST")
        self.assertEqual(result.inputs[0].metadata["constant_value"], 0)

    def test_and_with_minus_one(self):
        """Test: x & -1 → x"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)
        const_ff = helper.create_constant(0xFFFFFFFF, ssa_func)

        inst = helper.create_instruction("BA", [var_x, const_ff], "temp_1", ssa_func)

        rule = RuleAndIdentity()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "COPY")
        self.assertEqual(result.inputs[0].name, "x")

    def test_and_with_self(self):
        """Test: x & x → x"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)

        inst = helper.create_instruction("BA", [var_x, var_x], "temp_1", ssa_func)

        rule = RuleAndIdentity()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "COPY")
        self.assertEqual(result.inputs[0].name, "x")


class TestRuleOrIdentity(unittest.TestCase):
    """Test bitwise OR identity rule."""

    def test_or_with_zero(self):
        """Test: x | 0 → x"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)
        const_0 = helper.create_constant(0, ssa_func)

        inst = helper.create_instruction("BO", [var_x, const_0], "temp_1", ssa_func)

        rule = RuleOrIdentity()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "COPY")
        self.assertEqual(result.inputs[0].name, "x")

    def test_or_with_minus_one(self):
        """Test: x | -1 → -1"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)
        const_ff = helper.create_constant(0xFFFFFFFF, ssa_func)

        inst = helper.create_instruction("BO", [var_x, const_ff], "temp_1", ssa_func)

        rule = RuleOrIdentity()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "CONST")
        self.assertEqual(result.inputs[0].metadata["constant_value"], 0xFFFFFFFF)


class TestRuleAddIdentity(unittest.TestCase):
    """Test addition identity rule."""

    def test_add_zero(self):
        """Test: x + 0 → x"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)
        const_0 = helper.create_constant(0, ssa_func)

        inst = helper.create_instruction("ADD", [var_x, const_0], "temp_1", ssa_func)

        rule = RuleAddIdentity()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "COPY")
        self.assertEqual(result.inputs[0].name, "x")


class TestRuleMulIdentity(unittest.TestCase):
    """Test multiplication identity rule."""

    def test_mul_one(self):
        """Test: x * 1 → x"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)
        const_1 = helper.create_constant(1, ssa_func)

        inst = helper.create_instruction("MUL", [var_x, const_1], "temp_1", ssa_func)

        rule = RuleMulIdentity()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "COPY")
        self.assertEqual(result.inputs[0].name, "x")

    def test_mul_zero(self):
        """Test: x * 0 → 0"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)
        const_0 = helper.create_constant(0, ssa_func)

        inst = helper.create_instruction("MUL", [var_x, const_0], "temp_1", ssa_func)

        rule = RuleMulIdentity()
        result = rule.apply(inst, ssa_func)

        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "CONST")
        self.assertEqual(result.inputs[0].metadata["constant_value"], 0)


class TestRuleAndMask(unittest.TestCase):
    """Test nested AND mask simplification."""

    def test_nested_and_masks(self):
        """Test: (x & 0xff) & 0x0f → x & 0x0f"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)
        const_ff = helper.create_constant(0xff, ssa_func)
        const_0f = helper.create_constant(0x0f, ssa_func)

        # Create inner AND: x & 0xff
        inner_inst = helper.create_instruction("BA", [var_x, const_ff], "temp_inner", ssa_func, address=100)

        # Create outer AND: (x & 0xff) & 0x0f
        temp_inner = ssa_func.values["temp_inner"]
        outer_inst = helper.create_instruction("BA", [temp_inner, const_0f], "temp_outer", ssa_func, address=101)

        rule = RuleAndMask()
        self.assertTrue(rule.matches(outer_inst, ssa_func))

        result = rule.apply(outer_inst, ssa_func)
        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "BA")

        # Should have x and 0x0f (0xff & 0x0f = 0x0f)
        self.assertEqual(result.inputs[0].name, "x")
        self.assertEqual(result.inputs[1].metadata["constant_value"], 0x0f)


class TestRuleOrMask(unittest.TestCase):
    """Test nested OR mask simplification."""

    def test_nested_or_masks(self):
        """Test: (x | 0x0f) | 0xff → x | 0xff"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        var_x = helper.create_variable("x", ssa_func)
        const_0f = helper.create_constant(0x0f, ssa_func)
        const_ff = helper.create_constant(0xff, ssa_func)

        # Create inner OR: x | 0x0f
        inner_inst = helper.create_instruction("BO", [var_x, const_0f], "temp_inner", ssa_func, address=100)

        # Create outer OR: (x | 0x0f) | 0xff
        temp_inner = ssa_func.values["temp_inner"]
        outer_inst = helper.create_instruction("BO", [temp_inner, const_ff], "temp_outer", ssa_func, address=101)

        rule = RuleOrMask()
        self.assertTrue(rule.matches(outer_inst, ssa_func))

        result = rule.apply(outer_inst, ssa_func)
        self.assertIsNotNone(result)
        self.assertEqual(result.mnemonic, "BO")

        # Should have x and 0xff (0x0f | 0xff = 0xff)
        self.assertEqual(result.inputs[0].name, "x")
        self.assertEqual(result.inputs[1].metadata["constant_value"], 0xff)


class TestSimplificationEngine(unittest.TestCase):
    """Test the overall simplification engine."""

    def test_multiple_passes(self):
        """Test that simplification converges across multiple passes."""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        # Create: (x + 0) * 1 → should simplify to x
        var_x = helper.create_variable("x", ssa_func)
        const_0 = helper.create_constant(0, ssa_func)
        const_1 = helper.create_constant(1, ssa_func)

        # x + 0
        inst1 = helper.create_instruction("ADD", [var_x, const_0], "temp_1", ssa_func, address=100)
        ssa_func.instructions[0].append(inst1)

        # temp_1 * 1
        temp_1 = ssa_func.values["temp_1"]
        inst2 = helper.create_instruction("MUL", [temp_1, const_1], "temp_2", ssa_func, address=101)
        ssa_func.instructions[0].append(inst2)

        stats = simplify_expressions(ssa_func, max_iterations=10)

        # Should apply RuleAddIdentity and RuleMulIdentity
        self.assertGreater(stats.total_changes, 0)
        self.assertIn("RuleAddIdentity", stats.rules_applied)
        self.assertIn("RuleMulIdentity", stats.rules_applied)


if __name__ == "__main__":
    unittest.main()
