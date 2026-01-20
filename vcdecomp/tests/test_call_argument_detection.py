"""
Unit tests for CALL argument detection in stack_lifter.py.

Tests the robust hybrid approach that combines:
1. Precise eval stack depth simulation
2. SSP cross-validation
3. Stack snapshot constraints

Validates the fix for functions with 3+ arguments being incorrectly detected as void.
"""

import unittest
from typing import List, Optional
from dataclasses import dataclass

from vcdecomp.core.ir.stack_lifter import (
    _simulate_eval_stack_depth,
    _find_ssp_after_call,
    _assign_call_arguments,
    LiftedInstruction,
    StackValue
)
from vcdecomp.core.loader.scr_loader import Instruction
from vcdecomp.core.disasm import opcodes


# ============================================================================
# Mock classes for testing
# ============================================================================

class MockInstruction:
    """Mock raw instruction"""
    def __init__(self, opcode: int, arg1: int = 0, arg2: int = 0):
        self.opcode = opcode
        self.arg1 = arg1
        self.arg2 = arg2
        self._call_stack_snapshot = None


class MockLiftedInstruction:
    """Mock lifted instruction"""
    def __init__(self, instruction: MockInstruction, outputs: Optional[List[StackValue]] = None):
        self.instruction = instruction
        self.outputs = outputs or []
        self.inputs = []


# ============================================================================
# Test Cases
# ============================================================================

class TestEvalStackSimulation(unittest.TestCase):
    """Test eval stack depth simulation"""

    def setUp(self):
        """Set up test resolver"""
        self.resolver = opcodes.DEFAULT_RESOLVER

    def _create_lifted_sequence(self, mnemonics: List[str]) -> List[LiftedInstruction]:
        """
        Create lifted instruction sequence from mnemonics.

        Args:
            mnemonics: List of mnemonic names (e.g., ["GCP", "GCP", "ADD", "CALL"])

        Returns:
            List of LiftedInstruction objects
        """
        lifted = []

        for mnem in mnemonics:
            # Find opcode for mnemonic
            opcode = None
            for opc, info in opcodes.OPCODE_INFO.items():
                if info.mnemonic == mnem:
                    opcode = opc
                    break

            if opcode is None:
                raise ValueError(f"Unknown mnemonic: {mnem}")

            inst = MockInstruction(opcode)

            # Create dummy outputs based on opcode info
            info = self.resolver.get_info(opcode)
            outputs = [StackValue(None, None)] * info.pushes if info else []

            lifted_inst = MockLiftedInstruction(inst, outputs)
            lifted.append(lifted_inst)

        return lifted

    def test_simple_push_single_argument(self):
        """Test: GCP data[123]; CALL func -> depth = 1"""
        lifted = self._create_lifted_sequence(["GCP", "CALL"])

        # Simulate depth before CALL (index 1)
        depth = _simulate_eval_stack_depth(lifted, 1, self.resolver)

        self.assertEqual(depth, 1, "Should detect 1 value on stack (1 argument)")

    def test_two_arguments(self):
        """Test: GCP data[1]; GCP data[2]; CALL func -> depth = 2"""
        lifted = self._create_lifted_sequence(["GCP", "GCP", "CALL"])

        depth = _simulate_eval_stack_depth(lifted, 2, self.resolver)

        self.assertEqual(depth, 2, "Should detect 2 values on stack (2 arguments)")

    def test_three_arguments(self):
        """Test: GCP data[1]; GCP data[2]; GCP data[3]; CALL func -> depth = 3"""
        lifted = self._create_lifted_sequence(["GCP", "GCP", "GCP", "CALL"])

        depth = _simulate_eval_stack_depth(lifted, 3, self.resolver)

        self.assertEqual(depth, 3, "Should detect 3 values on stack (3 arguments)")

    def test_binary_operation_consumes_stack(self):
        """Test: GCP data[1]; GCP data[2]; ADD; CALL func -> depth = 1"""
        lifted = self._create_lifted_sequence(["GCP", "GCP", "ADD", "CALL"])

        depth = _simulate_eval_stack_depth(lifted, 3, self.resolver)

        self.assertEqual(depth, 1, "ADD consumes 2, produces 1 -> depth = 1")

    def test_store_operation_consumes_all(self):
        """Test: LADR [sp+0]; GCP data[123]; ASGN; CALL func -> depth = 0"""
        lifted = self._create_lifted_sequence(["LADR", "GCP", "ASGN", "CALL"])

        depth = _simulate_eval_stack_depth(lifted, 3, self.resolver)

        self.assertEqual(depth, 0, "ASGN consumes 2 values, stack is empty")

    def test_asp_does_not_affect_eval_stack(self):
        """Test: ASP 1; GCP data[123]; CALL func -> depth = 1 (ASP ignored)"""
        lifted = self._create_lifted_sequence(["ASP", "GCP", "CALL"])

        depth = _simulate_eval_stack_depth(lifted, 2, self.resolver)

        self.assertEqual(depth, 1, "ASP doesn't affect eval stack, only GCP counts")

    def test_ssp_does_not_affect_eval_stack(self):
        """Test: SSP 2; GCP data[123]; CALL func -> depth = 1 (SSP ignored)"""
        lifted = self._create_lifted_sequence(["SSP", "GCP", "CALL"])

        depth = _simulate_eval_stack_depth(lifted, 2, self.resolver)

        self.assertEqual(depth, 1, "SSP doesn't affect eval stack, only GCP counts")

    def test_control_flow_resets_depth(self):
        """Test: GCP; GCP; JZ label; GCP; CALL -> depth = 1 (reset at JZ)"""
        lifted = self._create_lifted_sequence(["GCP", "GCP", "JZ", "GCP", "CALL"])

        depth = _simulate_eval_stack_depth(lifted, 4, self.resolver)

        self.assertEqual(depth, 1, "JZ resets stack depth, only last GCP counts")

    def test_comparison_operations(self):
        """Test: GCP; GCP; EQU; CALL -> depth = 1 (EQU: 2 pop, 1 push)"""
        lifted = self._create_lifted_sequence(["GCP", "GCP", "EQU", "CALL"])

        depth = _simulate_eval_stack_depth(lifted, 3, self.resolver)

        self.assertEqual(depth, 1, "EQU compares 2 values, produces 1 bool result")

    def test_complex_expression(self):
        """Test: (a + b) * c as argument -> GCP a; GCP b; ADD; GCP c; MUL; CALL"""
        lifted = self._create_lifted_sequence(["GCP", "GCP", "ADD", "GCP", "MUL", "CALL"])

        depth = _simulate_eval_stack_depth(lifted, 5, self.resolver)

        self.assertEqual(depth, 1, "Complex expression results in 1 value on stack")


class TestSSPDetection(unittest.TestCase):
    """Test SSP detection after CALL"""

    def setUp(self):
        self.resolver = opcodes.DEFAULT_RESOLVER

    def _create_lifted_sequence(self, mnemonics: List[str]) -> List[LiftedInstruction]:
        """Helper to create lifted instruction sequence"""
        lifted = []

        for mnem in mnemonics:
            # Find opcode for mnemonic
            opcode = None
            for opc, info in opcodes.OPCODE_INFO.items():
                if info.mnemonic == mnem:
                    opcode = opc
                    break

            if opcode is None:
                raise ValueError(f"Unknown mnemonic: {mnem}")

            # Special handling for SSP arg1
            arg1 = 2 if mnem == "SSP" else 0
            inst = MockInstruction(opcode, arg1=arg1)

            lifted_inst = MockLiftedInstruction(inst)
            lifted.append(lifted_inst)

        return lifted

    def test_ssp_immediately_after_call(self):
        """Test: CALL func; SSP 2 -> returns 2"""
        lifted = self._create_lifted_sequence(["CALL", "SSP"])

        ssp_value = _find_ssp_after_call(lifted, 0, self.resolver)

        self.assertEqual(ssp_value, 2, "Should find SSP value = 2")

    def test_ssp_with_one_instruction_gap(self):
        """Test: CALL func; LLD [sp+0]; SSP 2 -> returns None (unreliable)"""
        lifted = self._create_lifted_sequence(["CALL", "LLD", "SSP"])

        ssp_value = _find_ssp_after_call(lifted, 0, self.resolver)

        self.assertIsNone(ssp_value, "SSP after LLD is unreliable (includes local cleanup)")

    def test_no_ssp_after_call(self):
        """Test: CALL func; RET -> returns None"""
        lifted = self._create_lifted_sequence(["CALL", "RET"])

        ssp_value = _find_ssp_after_call(lifted, 0, self.resolver)

        self.assertIsNone(ssp_value, "No SSP found")

    def test_control_flow_before_ssp(self):
        """Test: CALL func; JZ label -> returns None (stop at control flow)"""
        lifted = self._create_lifted_sequence(["CALL", "JZ"])

        ssp_value = _find_ssp_after_call(lifted, 0, self.resolver)

        self.assertIsNone(ssp_value, "Should stop at control flow boundary")


class TestCallArgumentAssignment(unittest.TestCase):
    """Test end-to-end CALL argument assignment"""

    def setUp(self):
        self.resolver = opcodes.DEFAULT_RESOLVER

    def _create_call_scenario(self, arg_mnemonics: List[str],
                              after_call: List[str],
                              snapshot_size: int) -> List[LiftedInstruction]:
        """
        Create CALL scenario with arguments and post-CALL instructions.

        Args:
            arg_mnemonics: Instructions before CALL (e.g., ["GCP", "GCP"])
            after_call: Instructions after CALL (e.g., ["SSP"])
            snapshot_size: Size of stack snapshot to simulate

        Returns:
            List of lifted instructions with CALL at position len(arg_mnemonics)
        """
        # Create argument sequence
        lifted = []
        for mnem in arg_mnemonics:
            opcode = None
            for opc, info in opcodes.OPCODE_INFO.items():
                if info.mnemonic == mnem:
                    opcode = opc
                    break

            if opcode is None:
                raise ValueError(f"Unknown mnemonic: {mnem}")

            inst = MockInstruction(opcode)
            info = self.resolver.get_info(opcode)
            outputs = [StackValue(None, None)] * info.pushes if info else []
            lifted_inst = MockLiftedInstruction(inst, outputs)
            lifted.append(lifted_inst)

        # Add CALL instruction with stack snapshot
        call_opcode = None
        for opc, info in opcodes.OPCODE_INFO.items():
            if info.mnemonic == "CALL":
                call_opcode = opc
                break

        call_inst = MockInstruction(call_opcode, arg1=0x1000)  # Dummy address
        call_inst._call_stack_snapshot = [StackValue(None, None)] * snapshot_size
        call_lifted = MockLiftedInstruction(call_inst)
        lifted.append(call_lifted)

        # Add post-CALL instructions
        for mnem in after_call:
            opcode = None
            for opc, info in opcodes.OPCODE_INFO.items():
                if info.mnemonic == mnem:
                    opcode = opc
                    break

            if opcode is None:
                raise ValueError(f"Unknown mnemonic: {mnem}")

            # Special handling for SSP arg1
            arg1 = snapshot_size if mnem == "SSP" else 0
            inst = MockInstruction(opcode, arg1=arg1)
            lifted_inst = MockLiftedInstruction(inst)
            lifted.append(lifted_inst)

        return lifted

    def test_void_function_no_arguments(self):
        """Test: void func(void) -> 0 arguments"""
        lifted = self._create_call_scenario(
            arg_mnemonics=[],
            after_call=["RET"],
            snapshot_size=0
        )

        _assign_call_arguments(lifted, self.resolver)

        call_idx = len([]) # CALL is at index 0
        self.assertEqual(len(lifted[call_idx].inputs), 0, "Void function should have 0 arguments")

    def test_one_argument_with_ssp(self):
        """Test: func(int) with SSP cleanup -> 1 argument"""
        lifted = self._create_call_scenario(
            arg_mnemonics=["GCP"],
            after_call=["SSP"],
            snapshot_size=1
        )

        _assign_call_arguments(lifted, self.resolver)

        call_idx = 1  # CALL is at index 1
        self.assertEqual(len(lifted[call_idx].inputs), 1, "Should detect 1 argument")

    def test_two_arguments_with_ssp(self):
        """Test: func(int, int) with SSP cleanup -> 2 arguments"""
        lifted = self._create_call_scenario(
            arg_mnemonics=["GCP", "GCP"],
            after_call=["SSP"],
            snapshot_size=2
        )

        _assign_call_arguments(lifted, self.resolver)

        call_idx = 2
        self.assertEqual(len(lifted[call_idx].inputs), 2, "Should detect 2 arguments")

    def test_three_arguments_no_ssp(self):
        """
        Critical test: func(int, int, int) without SSP -> 3 arguments

        This was the failing case before the fix (returned 0 arguments).
        """
        lifted = self._create_call_scenario(
            arg_mnemonics=["GCP", "GCP", "GCP"],
            after_call=["RET"],
            snapshot_size=3
        )

        _assign_call_arguments(lifted, self.resolver)

        call_idx = 3
        self.assertEqual(len(lifted[call_idx].inputs), 3,
                        "CRITICAL: Should detect 3 arguments even without SSP")

    def test_four_arguments_stack_depth_only(self):
        """Test: func(int, int, int, int) -> 4 arguments (stack depth detection)"""
        lifted = self._create_call_scenario(
            arg_mnemonics=["GCP", "GCP", "GCP", "GCP"],
            after_call=["RET"],
            snapshot_size=4
        )

        _assign_call_arguments(lifted, self.resolver)

        call_idx = 4
        self.assertEqual(len(lifted[call_idx].inputs), 4, "Should detect 4 arguments")

    def test_ssp_mismatch_uses_minimum(self):
        """Test: Stack depth = 3, SSP = 2 -> uses 2 (conservative)"""
        lifted = self._create_call_scenario(
            arg_mnemonics=["GCP", "GCP", "GCP"],
            after_call=["SSP"],  # SSP will have snapshot_size from fixture
            snapshot_size=2  # SSP arg1 = 2
        )

        _assign_call_arguments(lifted, self.resolver)

        call_idx = 3
        self.assertEqual(len(lifted[call_idx].inputs), 2,
                        "Should use minimum of stack_depth (3) and SSP (2)")

    def test_expression_as_argument(self):
        """Test: func(a + b) -> 1 argument after ADD"""
        lifted = self._create_call_scenario(
            arg_mnemonics=["GCP", "GCP", "ADD"],
            after_call=["SSP"],
            snapshot_size=1
        )

        _assign_call_arguments(lifted, self.resolver)

        call_idx = 3
        self.assertEqual(len(lifted[call_idx].inputs), 1,
                        "Expression (a+b) collapses to 1 value on stack")


# ============================================================================
# Integration Test with Real Bytecode Patterns
# ============================================================================

class TestRealBytecodePatterns(unittest.TestCase):
    """Test against actual bytecode patterns from tt.scr"""

    def setUp(self):
        self.resolver = opcodes.DEFAULT_RESOLVER

    def test_pattern_asp_asp_call_no_ssp(self):
        """
        Real pattern from tt.scr: func_0213() - 0 arguments

        Bytecode:
            ASP 1         ; Allocate return slot
            ASP 1         ; Allocate local/temp
            CALL func_0213
            LLD [sp+0]    ; Load return value
            ; No SSP

        Expected: 0 arguments (void function)
        """
        # Create sequence
        lifted = []

        # ASP 1
        asp_opcode = opcodes.OPCODE_INFO[39].mnemonic  # ASP = 39
        inst1 = MockInstruction(39, arg1=1)
        lifted.append(MockLiftedInstruction(inst1))

        # ASP 1
        inst2 = MockInstruction(39, arg1=1)
        lifted.append(MockLiftedInstruction(inst2))

        # CALL
        call_opcode = 45  # CALL = 45
        call_inst = MockInstruction(call_opcode, arg1=0x0213)
        call_inst._call_stack_snapshot = []  # No values on eval stack
        lifted.append(MockLiftedInstruction(call_inst))

        # LLD [sp+0]
        lld_opcode = 4  # LLD = 4
        inst3 = MockInstruction(lld_opcode, arg1=0)
        lifted.append(MockLiftedInstruction(inst3))

        # Process
        _assign_call_arguments(lifted, self.resolver)

        call_idx = 2
        self.assertEqual(len(lifted[call_idx].inputs), 0,
                        "func_0213() should be detected as void (0 args)")

    def test_pattern_gcp_call_ssp(self):
        """
        Real pattern: func(global_var) - 1 argument

        Bytecode:
            GCP data[123]
            CALL func
            SSP 1

        Expected: 1 argument
        """
        lifted = []

        # GCP
        gcp_opcode = 2
        inst1 = MockInstruction(gcp_opcode, arg1=123)
        info = self.resolver.get_info(gcp_opcode)
        lifted.append(MockLiftedInstruction(inst1, [StackValue(None, None)]))

        # CALL
        call_opcode = 45
        call_inst = MockInstruction(call_opcode, arg1=0x1000)
        call_inst._call_stack_snapshot = [StackValue(None, None)]
        lifted.append(MockLiftedInstruction(call_inst))

        # SSP 1
        ssp_opcode = 0
        inst2 = MockInstruction(ssp_opcode, arg1=1)
        lifted.append(MockLiftedInstruction(inst2))

        _assign_call_arguments(lifted, self.resolver)

        call_idx = 1
        self.assertEqual(len(lifted[call_idx].inputs), 1, "Should detect 1 argument")


if __name__ == '__main__':
    unittest.main()
