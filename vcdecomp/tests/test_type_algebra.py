"""
Unit tests for bidirectional type inference with type algebra.

Tests the Ghidra-inspired type constraint propagation:
- Forward propagation (output from inputs)
- Backward propagation (inputs from output)
- Type algebra per operation
- Pointer arithmetic handling
"""

import unittest
from typing import Dict, List

from vcdecomp.core.ir.ssa import SSAFunction, SSAInstruction, SSAValue
from vcdecomp.core.ir.cfg import CFG, BasicBlock
from vcdecomp.core.disasm import opcodes
from vcdecomp.core.ir.type_algebra import (
    TypeAlgebra,
    TypeConstraint,
    ConstraintDirection,
    infer_types_bidirectional,
)


class TestHelperFunctions(unittest.TestCase):
    """Helper functions for creating test SSA structures."""

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
            scr=None
        )

    def create_value(
        self,
        name: str,
        value_type: opcodes.ResultType,
        ssa_func: SSAFunction
    ) -> SSAValue:
        """Create an SSA value."""
        val = SSAValue(
            name=name,
            value_type=value_type,
            producer=100
        )
        ssa_func.values[name] = val
        return val

    def create_instruction(
        self,
        mnemonic: str,
        inputs: List[SSAValue],
        output_name: str,
        output_type: opcodes.ResultType,
        ssa_func: SSAFunction
    ) -> SSAInstruction:
        """Create an SSA instruction."""
        output_val = SSAValue(
            name=output_name,
            value_type=output_type,
            producer=100
        )
        ssa_func.values[output_name] = output_val

        inst = SSAInstruction(
            block_id=0,
            mnemonic=mnemonic,
            address=100,
            inputs=inputs,
            outputs=[output_val]
        )

        output_val.producer_inst = inst
        return inst


class TestForwardPropagation(unittest.TestCase):
    """Test forward type propagation (output from inputs)."""

    def test_add_same_types(self):
        """Test: int + int → int (forward)"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        # Create: z = x + y where x, y are int
        x = helper.create_value("x", opcodes.ResultType.INT, ssa_func)
        y = helper.create_value("y", opcodes.ResultType.INT, ssa_func)
        inst = helper.create_instruction("ADD", [x, y], "z", opcodes.ResultType.UNKNOWN, ssa_func)

        known_types = {"x": opcodes.ResultType.INT, "y": opcodes.ResultType.INT, "z": opcodes.ResultType.UNKNOWN}
        constraints = TypeAlgebra.propagate(inst, known_types)

        # Should have forward constraint: z = int
        forward_constraints = [c for c in constraints if c.direction == ConstraintDirection.FORWARD]
        self.assertGreater(len(forward_constraints), 0)

        z_constraint = next((c for c in forward_constraints if c.value.name == "z"), None)
        self.assertIsNotNone(z_constraint)
        self.assertEqual(z_constraint.type, opcodes.ResultType.INT)

    def test_float_operation(self):
        """Test: FADD always produces float"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        x = helper.create_value("x", opcodes.ResultType.UNKNOWN, ssa_func)
        y = helper.create_value("y", opcodes.ResultType.UNKNOWN, ssa_func)
        inst = helper.create_instruction("FADD", [x, y], "z", opcodes.ResultType.UNKNOWN, ssa_func)

        known_types = {"x": opcodes.ResultType.UNKNOWN, "y": opcodes.ResultType.UNKNOWN, "z": opcodes.ResultType.UNKNOWN}
        constraints = TypeAlgebra.propagate(inst, known_types)

        # Should have constraint: z = float
        z_constraints = [c for c in constraints if c.value.name == "z"]
        self.assertGreater(len(z_constraints), 0)
        self.assertEqual(z_constraints[0].type, opcodes.ResultType.FLOAT)
        self.assertGreaterEqual(z_constraints[0].confidence, 0.99)

    def test_comparison_result(self):
        """Test: Comparison always returns int"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        x = helper.create_value("x", opcodes.ResultType.FLOAT, ssa_func)
        y = helper.create_value("y", opcodes.ResultType.FLOAT, ssa_func)
        inst = helper.create_instruction("LES", [x, y], "result", opcodes.ResultType.UNKNOWN, ssa_func)

        known_types = {"x": opcodes.ResultType.FLOAT, "y": opcodes.ResultType.FLOAT, "result": opcodes.ResultType.UNKNOWN}
        constraints = TypeAlgebra.propagate(inst, known_types)

        # Result should be int
        result_constraints = [c for c in constraints if c.value.name == "result"]
        self.assertGreater(len(result_constraints), 0)
        self.assertEqual(result_constraints[0].type, opcodes.ResultType.INT)


class TestBackwardPropagation(unittest.TestCase):
    """Test backward type propagation (inputs from output)."""

    def test_add_backward(self):
        """Test: If z = x + y and z is int, then x and y should be int"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        x = helper.create_value("x", opcodes.ResultType.UNKNOWN, ssa_func)
        y = helper.create_value("y", opcodes.ResultType.UNKNOWN, ssa_func)
        inst = helper.create_instruction("ADD", [x, y], "z", opcodes.ResultType.INT, ssa_func)

        known_types = {"x": opcodes.ResultType.UNKNOWN, "y": opcodes.ResultType.UNKNOWN, "z": opcodes.ResultType.INT}
        constraints = TypeAlgebra.propagate(inst, known_types)

        # Should have backward constraints: x = int, y = int
        backward_constraints = [c for c in constraints if c.direction == ConstraintDirection.BACKWARD]
        self.assertGreaterEqual(len(backward_constraints), 2)

        x_constraint = next((c for c in backward_constraints if c.value.name == "x"), None)
        y_constraint = next((c for c in backward_constraints if c.value.name == "y"), None)

        self.assertIsNotNone(x_constraint)
        self.assertIsNotNone(y_constraint)
        self.assertEqual(x_constraint.type, opcodes.ResultType.INT)
        self.assertEqual(y_constraint.type, opcodes.ResultType.INT)

    def test_float_operation_backward(self):
        """Test: FADD requires float inputs"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        x = helper.create_value("x", opcodes.ResultType.UNKNOWN, ssa_func)
        y = helper.create_value("y", opcodes.ResultType.UNKNOWN, ssa_func)
        inst = helper.create_instruction("FADD", [x, y], "z", opcodes.ResultType.FLOAT, ssa_func)

        known_types = {"x": opcodes.ResultType.UNKNOWN, "y": opcodes.ResultType.UNKNOWN, "z": opcodes.ResultType.FLOAT}
        constraints = TypeAlgebra.propagate(inst, known_types)

        # Should constrain inputs to float
        x_constraints = [c for c in constraints if c.value.name == "x"]
        y_constraints = [c for c in constraints if c.value.name == "y"]

        self.assertGreater(len(x_constraints), 0)
        self.assertGreater(len(y_constraints), 0)
        self.assertEqual(x_constraints[0].type, opcodes.ResultType.FLOAT)
        self.assertEqual(y_constraints[0].type, opcodes.ResultType.FLOAT)

    def test_conversion_backward(self):
        """Test: ITOF input must be int"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        x = helper.create_value("x", opcodes.ResultType.UNKNOWN, ssa_func)
        inst = helper.create_instruction("ITOF", [x], "y", opcodes.ResultType.FLOAT, ssa_func)

        known_types = {"x": opcodes.ResultType.UNKNOWN, "y": opcodes.ResultType.FLOAT}
        constraints = TypeAlgebra.propagate(inst, known_types)

        # Input must be int
        x_constraints = [c for c in constraints if c.value.name == "x"]
        self.assertGreater(len(x_constraints), 0)
        self.assertEqual(x_constraints[0].type, opcodes.ResultType.INT)
        self.assertGreaterEqual(x_constraints[0].confidence, 0.99)


class TestPointerArithmetic(unittest.TestCase):
    """Test pointer arithmetic type handling."""

    def test_pointer_plus_int(self):
        """Test: ptr + int → ptr"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        ptr = helper.create_value("ptr", opcodes.ResultType.POINTER, ssa_func)
        offset = helper.create_value("offset", opcodes.ResultType.INT, ssa_func)
        inst = helper.create_instruction("ADD", [ptr, offset], "result", opcodes.ResultType.UNKNOWN, ssa_func)

        known_types = {
            "ptr": opcodes.ResultType.POINTER,
            "offset": opcodes.ResultType.INT,
            "result": opcodes.ResultType.UNKNOWN
        }
        constraints = TypeAlgebra.propagate(inst, known_types)

        # Result should be pointer
        result_constraints = [c for c in constraints if c.value.name == "result"]
        self.assertGreater(len(result_constraints), 0)
        self.assertEqual(result_constraints[0].type, opcodes.ResultType.POINTER)

    def test_pointer_minus_int(self):
        """Test: ptr - int → ptr"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        ptr = helper.create_value("ptr", opcodes.ResultType.POINTER, ssa_func)
        offset = helper.create_value("offset", opcodes.ResultType.INT, ssa_func)
        inst = helper.create_instruction("SUB", [ptr, offset], "result", opcodes.ResultType.UNKNOWN, ssa_func)

        known_types = {
            "ptr": opcodes.ResultType.POINTER,
            "offset": opcodes.ResultType.INT,
            "result": opcodes.ResultType.UNKNOWN
        }
        constraints = TypeAlgebra.propagate(inst, known_types)

        # Result should be pointer
        result_constraints = [c for c in constraints if c.value.name == "result"]
        self.assertGreater(len(result_constraints), 0)
        self.assertEqual(result_constraints[0].type, opcodes.ResultType.POINTER)

    def test_address_operation(self):
        """Test: LADR/GADR always produce pointers"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        inst = helper.create_instruction("LADR", [], "ptr", opcodes.ResultType.UNKNOWN, ssa_func)

        known_types = {"ptr": opcodes.ResultType.UNKNOWN}
        constraints = TypeAlgebra.propagate(inst, known_types)

        # Should be pointer
        ptr_constraints = [c for c in constraints if c.value.name == "ptr"]
        self.assertGreater(len(ptr_constraints), 0)
        self.assertEqual(ptr_constraints[0].type, opcodes.ResultType.POINTER)


class TestCopyPropagation(unittest.TestCase):
    """Test COPY operation bidirectional propagation."""

    def test_copy_forward(self):
        """Test: If x is int, then COPY(x) is int"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        x = helper.create_value("x", opcodes.ResultType.INT, ssa_func)
        inst = helper.create_instruction("COPY", [x], "y", opcodes.ResultType.UNKNOWN, ssa_func)

        known_types = {"x": opcodes.ResultType.INT, "y": opcodes.ResultType.UNKNOWN}
        constraints = TypeAlgebra.propagate(inst, known_types)

        # y should be int
        y_constraints = [c for c in constraints if c.value.name == "y"]
        self.assertGreater(len(y_constraints), 0)
        self.assertEqual(y_constraints[0].type, opcodes.ResultType.INT)

    def test_copy_backward(self):
        """Test: If COPY(x) = y and y is float, then x is float"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        x = helper.create_value("x", opcodes.ResultType.UNKNOWN, ssa_func)
        inst = helper.create_instruction("COPY", [x], "y", opcodes.ResultType.FLOAT, ssa_func)

        known_types = {"x": opcodes.ResultType.UNKNOWN, "y": opcodes.ResultType.FLOAT}
        constraints = TypeAlgebra.propagate(inst, known_types)

        # x should be float
        x_constraints = [c for c in constraints if c.value.name == "x"]
        self.assertGreater(len(x_constraints), 0)
        self.assertEqual(x_constraints[0].type, opcodes.ResultType.FLOAT)


class TestPHIPropagation(unittest.TestCase):
    """Test PHI node type propagation."""

    def test_phi_forward(self):
        """Test: If all PHI inputs agree, output is that type"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        x = helper.create_value("x", opcodes.ResultType.INT, ssa_func)
        y = helper.create_value("y", opcodes.ResultType.INT, ssa_func)
        z = helper.create_value("z", opcodes.ResultType.INT, ssa_func)
        inst = helper.create_instruction("PHI", [x, y, z], "result", opcodes.ResultType.UNKNOWN, ssa_func)

        known_types = {
            "x": opcodes.ResultType.INT,
            "y": opcodes.ResultType.INT,
            "z": opcodes.ResultType.INT,
            "result": opcodes.ResultType.UNKNOWN
        }
        constraints = TypeAlgebra.propagate(inst, known_types)

        # Result should be int
        result_constraints = [c for c in constraints if c.value.name == "result"]
        self.assertGreater(len(result_constraints), 0)
        self.assertEqual(result_constraints[0].type, opcodes.ResultType.INT)

    def test_phi_backward(self):
        """Test: If PHI output known, propagate to unknown inputs"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        x = helper.create_value("x", opcodes.ResultType.FLOAT, ssa_func)
        y = helper.create_value("y", opcodes.ResultType.UNKNOWN, ssa_func)
        inst = helper.create_instruction("PHI", [x, y], "result", opcodes.ResultType.FLOAT, ssa_func)

        known_types = {
            "x": opcodes.ResultType.FLOAT,
            "y": opcodes.ResultType.UNKNOWN,
            "result": opcodes.ResultType.FLOAT
        }
        constraints = TypeAlgebra.propagate(inst, known_types)

        # y should be float
        y_constraints = [c for c in constraints if c.value.name == "y"]
        self.assertGreater(len(y_constraints), 0)
        self.assertEqual(y_constraints[0].type, opcodes.ResultType.FLOAT)


class TestBidirectionalInference(unittest.TestCase):
    """Test the full bidirectional inference engine."""

    def test_simple_chain(self):
        """Test: Type propagates through a chain of operations"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        # Create chain: z = (x + y) * 2
        # where result z is known to be int
        x = helper.create_value("x", opcodes.ResultType.UNKNOWN, ssa_func)
        y = helper.create_value("y", opcodes.ResultType.UNKNOWN, ssa_func)
        two = helper.create_value("two", opcodes.ResultType.INT, ssa_func)

        add_inst = helper.create_instruction("ADD", [x, y], "temp", opcodes.ResultType.UNKNOWN, ssa_func)
        temp = ssa_func.values["temp"]

        mul_inst = helper.create_instruction("MUL", [temp, two], "z", opcodes.ResultType.INT, ssa_func)

        ssa_func.instructions[0] = [add_inst, mul_inst]

        # Run bidirectional inference
        stats = infer_types_bidirectional(ssa_func, debug=False)

        # x and y should be inferred as int
        self.assertEqual(x.value_type, opcodes.ResultType.INT)
        self.assertEqual(y.value_type, opcodes.ResultType.INT)
        self.assertEqual(temp.value_type, opcodes.ResultType.INT)

        # Should have refined types
        self.assertGreater(stats["types_refined"], 0)


if __name__ == "__main__":
    unittest.main()
