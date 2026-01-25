"""
Unit tests for LoadGuard array detection system.

Tests the Ghidra-inspired LoadGuard tracking:
- Indexed access pattern detection
- Array candidate identification
- Element size and type inference
- Array metadata marking
"""

import unittest
from typing import Dict, List

from vcdecomp.core.ir.ssa import SSAFunction, SSAInstruction, SSAValue
from vcdecomp.core.ir.cfg import CFG, BasicBlock
from vcdecomp.core.disasm import opcodes
from vcdecomp.core.loader.scr_loader import Instruction
from vcdecomp.core.ir.load_guard import LoadGuard, discover_arrays, IndexedAccess
from vcdecomp.core.ir.stack_lifter import LiftedInstruction


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

    def create_value(self, name: str, value_type: opcodes.ResultType, ssa_func: SSAFunction,
                     producer_inst=None) -> SSAValue:
        """Create an SSA value."""
        val = SSAValue(
            name=name,
            value_type=value_type,
            producer=100 if producer_inst else None,
            producer_inst=producer_inst
        )
        ssa_func.values[name] = val
        return val

    def create_instruction(
        self,
        mnemonic: str,
        inputs: List[SSAValue],
        output_name: str,
        ssa_func: SSAFunction,
        address: int = 100,
        arg1: int = 0,
        arg2: int = 0
    ) -> SSAInstruction:
        """Create an SSA instruction with optional bytecode instruction."""
        output_val = SSAValue(
            name=output_name,
            value_type=opcodes.ResultType.INT,
            producer=address
        )
        ssa_func.values[output_name] = output_val

        # Create fake bytecode instruction
        bytecode_inst = Instruction(address=address, opcode=0, arg1=arg1, arg2=arg2)

        # Create fake lifted instruction
        lifted_inst = LiftedInstruction(
            instruction=bytecode_inst,
            inputs=[],  # Simplified
            outputs=[]
        )

        inst = SSAInstruction(
            block_id=0,
            mnemonic=mnemonic,
            address=address,
            inputs=inputs,
            outputs=[output_val],
            instruction=lifted_inst
        )

        output_val.producer_inst = inst
        return inst


class TestIndexedAccessDetection(unittest.TestCase):
    """Test detection of indexed access patterns."""

    def test_simple_indexed_store(self):
        """
        Test detection of: arr[i] = value

        SSA Pattern:
            base = LADR [EBP-40]           ; Array base address
            scaled = i * 4                 ; IMUL
            addr = base + scaled           ; IADD
            ASGN(value, addr)              ; Store
        """
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        # Create base address (LADR)
        base_val = helper.create_value("base_arr", opcodes.ResultType.POINTER, ssa_func)
        ladr_inst = helper.create_instruction("LADR", [], "base_arr", ssa_func, address=100, arg1=40)
        base_val.producer_inst = ladr_inst

        # Create index variable
        index_val = helper.create_value("i", opcodes.ResultType.INT, ssa_func)

        # Create constant for element size
        const_4 = helper.create_value("const_4", opcodes.ResultType.INT, ssa_func)
        const_4.metadata["constant_value"] = 4

        # Create scaled index: i * 4
        scaled_inst = helper.create_instruction("IMUL", [index_val, const_4], "scaled", ssa_func, address=101)

        # Create address: base + scaled
        scaled_val = ssa_func.values["scaled"]
        addr_inst = helper.create_instruction("IADD", [base_val, scaled_val], "addr", ssa_func, address=102)

        # Create store: ASGN(value, addr)
        value_val = helper.create_value("value", opcodes.ResultType.INT, ssa_func)
        addr_val = ssa_func.values["addr"]
        asgn_inst = helper.create_instruction("ASGN", [value_val, addr_val], "asgn_result", ssa_func, address=103)

        # Add instructions to SSA function
        ssa_func.instructions[0] = [ladr_inst, scaled_inst, addr_inst, asgn_inst]

        # Run LoadGuard
        load_guard = LoadGuard(ssa_func)
        accesses = load_guard.discover_indexed_accesses()

        # Verify detection
        self.assertEqual(len(accesses), 1, "Should detect one indexed access")

        access = accesses[0]
        self.assertEqual(access.base.name, "base_arr")
        self.assertEqual(access.index.name, "i")
        self.assertEqual(access.elem_size, 4)
        self.assertEqual(access.access_type, "store")

    def test_simple_indexed_load(self):
        """
        Test detection of: value = arr[i]

        SSA Pattern:
            base = LADR [EBP-40]
            scaled = i * 4
            addr = base + scaled
            value = DCP(addr)              ; Load
        """
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        # Create base address
        base_val = helper.create_value("base_arr", opcodes.ResultType.POINTER, ssa_func)
        ladr_inst = helper.create_instruction("LADR", [], "base_arr", ssa_func, arg1=40)
        base_val.producer_inst = ladr_inst

        # Create index
        index_val = helper.create_value("i", opcodes.ResultType.INT, ssa_func)

        # Create element size constant
        const_4 = helper.create_value("const_4", opcodes.ResultType.INT, ssa_func)
        const_4.metadata["constant_value"] = 4

        # Scaled index
        scaled_inst = helper.create_instruction("IMUL", [index_val, const_4], "scaled", ssa_func, address=101)
        scaled_val = ssa_func.values["scaled"]

        # Address computation
        addr_inst = helper.create_instruction("IADD", [base_val, scaled_val], "addr", ssa_func, address=102)
        addr_val = ssa_func.values["addr"]

        # Load: DCP(addr)
        dcp_inst = helper.create_instruction("DCP", [addr_val], "value", ssa_func, address=103)

        ssa_func.instructions[0] = [ladr_inst, scaled_inst, addr_inst, dcp_inst]

        # Run LoadGuard
        load_guard = LoadGuard(ssa_func)
        accesses = load_guard.discover_indexed_accesses()

        # Verify
        self.assertEqual(len(accesses), 1)
        access = accesses[0]
        self.assertEqual(access.access_type, "load")
        self.assertEqual(access.elem_size, 4)

    def test_char_array_access(self):
        """Test detection of char array: arr[i] with elem_size=1"""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        # Base
        base_val = helper.create_value("base_arr", opcodes.ResultType.POINTER, ssa_func)
        ladr_inst = helper.create_instruction("LADR", [], "base_arr", ssa_func, arg1=20)
        base_val.producer_inst = ladr_inst

        # Index
        index_val = helper.create_value("i", opcodes.ResultType.INT, ssa_func)

        # elem_size = 1 (char)
        const_1 = helper.create_value("const_1", opcodes.ResultType.INT, ssa_func)
        const_1.metadata["constant_value"] = 1

        # Scaled: i * 1
        scaled_inst = helper.create_instruction("IMUL", [index_val, const_1], "scaled", ssa_func, address=101)
        scaled_val = ssa_func.values["scaled"]

        # Address
        addr_inst = helper.create_instruction("IADD", [base_val, scaled_val], "addr", ssa_func, address=102)
        addr_val = ssa_func.values["addr"]

        # Store
        value_val = helper.create_value("value", opcodes.ResultType.CHAR, ssa_func)
        asgn_inst = helper.create_instruction("ASGN", [value_val, addr_val], "result", ssa_func, address=103)

        ssa_func.instructions[0] = [ladr_inst, scaled_inst, addr_inst, asgn_inst]

        # Run
        load_guard = LoadGuard(ssa_func)
        accesses = load_guard.discover_indexed_accesses()

        # Verify
        self.assertEqual(len(accesses), 1)
        self.assertEqual(accesses[0].elem_size, 1)


class TestArrayCandidateGrouping(unittest.TestCase):
    """Test grouping of accesses into array candidates."""

    def test_multiple_accesses_same_array(self):
        """Test that multiple accesses to same base are grouped together."""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        # Create base
        base_val = helper.create_value("base_arr", opcodes.ResultType.POINTER, ssa_func)
        ladr_inst = helper.create_instruction("LADR", [], "base_arr", ssa_func, arg1=40)
        base_val.producer_inst = ladr_inst

        instructions = [ladr_inst]

        # Create 3 different indexed accesses to same array
        for i in range(3):
            index_val = helper.create_value(f"i{i}", opcodes.ResultType.INT, ssa_func)
            const_4 = helper.create_value(f"const_4_{i}", opcodes.ResultType.INT, ssa_func)
            const_4.metadata["constant_value"] = 4

            scaled_inst = helper.create_instruction(
                "IMUL", [index_val, const_4], f"scaled_{i}", ssa_func, address=100 + i * 10
            )
            scaled_val = ssa_func.values[f"scaled_{i}"]

            addr_inst = helper.create_instruction(
                "IADD", [base_val, scaled_val], f"addr_{i}", ssa_func, address=101 + i * 10
            )
            addr_val = ssa_func.values[f"addr_{i}"]

            value_val = helper.create_value(f"val_{i}", opcodes.ResultType.INT, ssa_func)
            asgn_inst = helper.create_instruction(
                "ASGN", [value_val, addr_val], f"result_{i}", ssa_func, address=102 + i * 10
            )

            instructions.extend([scaled_inst, addr_inst, asgn_inst])

        # Add all instructions to SSA function
        ssa_func.instructions[0] = instructions

        # Run LoadGuard
        load_guard = LoadGuard(ssa_func)
        load_guard.discover_indexed_accesses()
        candidates = load_guard.group_into_array_candidates()

        # Verify: Should have 1 candidate with 3 accesses
        self.assertEqual(len(candidates), 1)

        candidate = list(candidates.values())[0]
        self.assertEqual(len(candidate.accesses), 3)
        self.assertEqual(candidate.element_size, 4)
        self.assertGreaterEqual(candidate.confidence, 0.9)  # High confidence with 3+ accesses

    def test_element_type_inference(self):
        """Test that element type is inferred from element size."""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        # Create different arrays with different element sizes
        test_cases = [
            (1, opcodes.ResultType.CHAR),
            (2, opcodes.ResultType.SHORT),
            (4, opcodes.ResultType.INT),
            (8, opcodes.ResultType.DOUBLE),
        ]

        instructions = []

        for elem_size, expected_type in test_cases:
            base_val = helper.create_value(f"base_{elem_size}", opcodes.ResultType.POINTER, ssa_func)
            ladr_inst = helper.create_instruction("LADR", [], f"base_{elem_size}", ssa_func, arg1=elem_size * 10)
            base_val.producer_inst = ladr_inst

            index_val = helper.create_value(f"i_{elem_size}", opcodes.ResultType.INT, ssa_func)
            const_val = helper.create_value(f"const_{elem_size}", opcodes.ResultType.INT, ssa_func)
            const_val.metadata["constant_value"] = elem_size

            scaled_inst = helper.create_instruction(
                "IMUL", [index_val, const_val], f"scaled_{elem_size}", ssa_func, address=100 + elem_size
            )
            scaled_val = ssa_func.values[f"scaled_{elem_size}"]

            addr_inst = helper.create_instruction(
                "IADD", [base_val, scaled_val], f"addr_{elem_size}", ssa_func, address=101 + elem_size
            )
            addr_val = ssa_func.values[f"addr_{elem_size}"]

            value_val = helper.create_value(f"val_{elem_size}", opcodes.ResultType.INT, ssa_func)
            asgn_inst = helper.create_instruction(
                "ASGN", [value_val, addr_val], f"result_{elem_size}", ssa_func, address=102 + elem_size
            )

            instructions.extend([ladr_inst, scaled_inst, addr_inst, asgn_inst])

        # Add all instructions
        ssa_func.instructions[0] = instructions

        # Run LoadGuard
        load_guard = LoadGuard(ssa_func)
        load_guard.discover_indexed_accesses()
        candidates = load_guard.group_into_array_candidates()

        # Verify type inference for each
        self.assertEqual(len(candidates), len(test_cases))

        for elem_size, expected_type in test_cases:
            # Find candidate with this element size
            found = False
            for candidate in candidates.values():
                if candidate.element_size == elem_size:
                    self.assertEqual(candidate.element_type, expected_type,
                                   f"Element size {elem_size} should infer type {expected_type.name}")
                    found = True
                    break
            self.assertTrue(found, f"Should find candidate with elem_size={elem_size}")


class TestLoadGuardAPI(unittest.TestCase):
    """Test the public API."""

    def test_discover_arrays_api(self):
        """Test the discover_arrays() public API function."""
        ssa_func = TestHelperFunctions().create_test_ssa_function()
        helper = TestHelperFunctions()

        # Create a simple array access
        base_val = helper.create_value("base", opcodes.ResultType.POINTER, ssa_func)
        ladr_inst = helper.create_instruction("LADR", [], "base", ssa_func, arg1=40)
        base_val.producer_inst = ladr_inst

        index_val = helper.create_value("i", opcodes.ResultType.INT, ssa_func)
        const_4 = helper.create_value("const_4", opcodes.ResultType.INT, ssa_func)
        const_4.metadata["constant_value"] = 4

        scaled_inst = helper.create_instruction("IMUL", [index_val, const_4], "scaled", ssa_func, address=101)
        scaled_val = ssa_func.values["scaled"]

        addr_inst = helper.create_instruction("IADD", [base_val, scaled_val], "addr", ssa_func, address=102)
        addr_val = ssa_func.values["addr"]

        value_val = helper.create_value("value", opcodes.ResultType.INT, ssa_func)
        asgn_inst = helper.create_instruction("ASGN", [value_val, addr_val], "result", ssa_func, address=103)

        ssa_func.instructions[0] = [ladr_inst, scaled_inst, addr_inst, asgn_inst]

        # Call public API
        load_guard = discover_arrays(ssa_func)

        # Verify results
        self.assertGreater(len(load_guard.indexed_accesses), 0)
        self.assertGreater(len(load_guard.array_candidates), 0)

        # Check metadata was set
        self.assertTrue(base_val.metadata.get("is_array", False))
        self.assertEqual(base_val.metadata.get("array_elem_type"), opcodes.ResultType.INT)
        self.assertEqual(base_val.metadata.get("array_elem_size"), 4)


if __name__ == "__main__":
    unittest.main()
