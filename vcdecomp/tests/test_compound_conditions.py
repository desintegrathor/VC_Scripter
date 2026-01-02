"""
Unit tests for compound condition (AND/OR) reconstruction.

Tests the decompiler's ability to reconstruct logical operators from
short-circuit bytecode patterns.
"""

import unittest
from typing import Dict, List
from vcdecomp.core.ir.cfg import CFG, BasicBlock
from vcdecomp.core.ir.structure import _detect_short_circuit_pattern, CompoundCondition
from vcdecomp.parsing.disasm import Instruction
from vcdecomp.parsing import opcodes


class MockResolver:
    """Mock opcode resolver for testing"""

    def __init__(self):
        self.mnemonics = {
            0x01: "JMP",
            0x02: "JZ",
            0x03: "JNZ",
            0x10: "IGRE",  # Integer greater
            0x11: "UGEQ",  # Unsigned greater or equal
            0x20: "PUSH",
            0x30: "GADR",
            0x31: "DCP",
            0x32: "ADD",
        }

    def get_mnemonic(self, opcode: int) -> str:
        return self.mnemonics.get(opcode, f"UNK_{opcode:02X}")

    def is_conditional_jump(self, opcode: int) -> bool:
        return opcode in [0x02, 0x03]  # JZ, JNZ

    def is_unconditional_jump(self, opcode: int) -> bool:
        return opcode == 0x01  # JMP


def make_instruction(addr: int, opcode: int, arg1: int = 0, arg2: int = 0) -> Instruction:
    """Helper to create instruction"""
    return Instruction(
        address=addr,
        opcode=opcode,
        arg1=arg1,
        arg2=arg2,
        comment=""
    )


def make_block(block_id: int, start: int, instructions: List[Instruction]) -> BasicBlock:
    """Helper to create basic block"""
    return BasicBlock(
        block_id=block_id,
        start_address=start,
        instructions=instructions
    )


class TestSimpleOR(unittest.TestCase):
    """Test simple OR pattern: if (a || b)"""

    def setUp(self):
        self.resolver = MockResolver()

    def test_simple_or_pattern(self):
        """
        Bytecode pattern for: if (a > 0 || b > 0)

        Block 0:  IGRE; JZ block2; JMP block1
        Block 2:  IGRE; JZ block3; JMP block1
        Block 1:  <true body>
        Block 3:  <false body>
        """
        cfg = CFG()

        # Block 0: test a, if true goto body (block 1)
        block0 = make_block(0, 100, [
            make_instruction(100, 0x20, 10),     # PUSH a
            make_instruction(104, 0x20, 0),      # PUSH 0
            make_instruction(108, 0x10),         # IGRE (a > 0)
            make_instruction(112, 0x02, 200),    # JZ block2 (if false, try next)
            make_instruction(116, 0x01, 300),    # JMP block1 (if true, goto body)
        ])

        # Block 2: test b, if true goto body (block 1)
        block2 = make_block(2, 200, [
            make_instruction(200, 0x20, 20),     # PUSH b
            make_instruction(204, 0x20, 0),      # PUSH 0
            make_instruction(208, 0x10),         # IGRE (b > 0)
            make_instruction(212, 0x02, 400),    # JZ block3 (if false, goto end)
            make_instruction(216, 0x01, 300),    # JMP block1 (if true, goto body)
        ])

        # Block 1: true body
        block1 = make_block(1, 300, [
            make_instruction(300, 0x20, 999),    # Some action
        ])

        # Block 3: false body / merge
        block3 = make_block(3, 400, [
            make_instruction(400, 0x20, 0),      # Continue
        ])

        cfg.blocks = {0: block0, 1: block1, 2: block2, 3: block3}
        cfg.entry_block = 0

        # Test detection
        start_to_block = {100: 0, 200: 2, 300: 1, 400: 3}
        result = _detect_short_circuit_pattern(cfg, 0, self.resolver, start_to_block)

        self.assertIsNotNone(result, "Should detect OR pattern")
        self.assertEqual(result.operator, "||", "Should be OR operator")
        self.assertEqual(len(result.conditions), 2, "Should have 2 conditions")
        self.assertEqual(result.true_target, 1, "True target should be block 1")
        self.assertEqual(result.false_target, 3, "False target should be block 3")


class TestSimpleAND(unittest.TestCase):
    """Test simple AND pattern: if (a && b)"""

    def setUp(self):
        self.resolver = MockResolver()

    def test_simple_and_pattern(self):
        """
        Bytecode pattern for: if (a > 0 && b > 0)

        Block 0:  IGRE; JZ block2; IGRE; JZ block2; JMP block1
        Block 1:  <true body>
        Block 2:  <false body>
        """
        cfg = CFG()

        # Block 0: test a AND b, both must be true
        block0 = make_block(0, 100, [
            make_instruction(100, 0x20, 10),     # PUSH a
            make_instruction(104, 0x20, 0),      # PUSH 0
            make_instruction(108, 0x10),         # IGRE (a > 0)
            make_instruction(112, 0x02, 300),    # JZ block2 (if false, goto end)
            make_instruction(116, 0x20, 20),     # PUSH b
            make_instruction(120, 0x20, 0),      # PUSH 0
            make_instruction(124, 0x10),         # IGRE (b > 0)
            make_instruction(128, 0x02, 300),    # JZ block2 (if false, goto end)
            make_instruction(132, 0x01, 200),    # JMP block1 (both true, goto body)
        ])

        # Block 1: true body
        block1 = make_block(1, 200, [
            make_instruction(200, 0x20, 999),    # Some action
        ])

        # Block 2: false body / merge
        block2 = make_block(2, 300, [
            make_instruction(300, 0x20, 0),      # Continue
        ])

        cfg.blocks = {0: block0, 1: block1, 2: block2}
        cfg.entry_block = 0

        # Test detection
        start_to_block = {100: 0, 200: 1, 300: 2}
        result = _detect_short_circuit_pattern(cfg, 0, self.resolver, start_to_block)

        self.assertIsNotNone(result, "Should detect AND pattern")
        self.assertEqual(result.operator, "&&", "Should be AND operator")
        self.assertEqual(len(result.conditions), 2, "Should have 2 conditions")
        self.assertEqual(result.true_target, 1, "True target should be block 1")
        self.assertEqual(result.false_target, 2, "False target should be block 2")


class TestCombinedANDOR(unittest.TestCase):
    """Test combined pattern: if ((a && b) || (c && d)) - THE FAILING CASE"""

    def setUp(self):
        self.resolver = MockResolver()

    def test_tdm_scr_pattern(self):
        """
        Real pattern from tdm.scr:
        if (((gSideFrags[0]>0)&&(gSideFrags[0]>=gEndValue))
            ||((gSideFrags[1]>1)&&(gSideFrags[1]>=gEndValue)))

        Block 0:  test1; JZ block2; test2; JZ block2; JMP block1
        Block 2:  test3; JZ block3; test4; JZ block3; JMP block1
        Block 1:  <true body>
        Block 3:  <false body>
        """
        cfg = CFG()

        # Block 0: First AND group (gSideFrags[0]>0 && gSideFrags[0]>=gEndValue)
        block0 = make_block(0, 1129, [
            make_instruction(1129, 0x30, 0x004),  # GADR gSideFrags
            make_instruction(1133, 0x32),         # ADD [0]
            make_instruction(1134, 0x31, 4),      # DCP
            make_instruction(1138, 0x10),         # IGRE (>0)
            make_instruction(1139, 0x02, 1151),   # JZ block2 (if false, try second OR)
            make_instruction(1140, 0x30, 0x004),  # GADR gSideFrags
            make_instruction(1144, 0x32),         # ADD [0]
            make_instruction(1145, 0x31, 4),      # DCP
            make_instruction(1147, 0x11),         # UGEQ (>=gEndValue)
            make_instruction(1148, 0x02, 1151),   # JZ block2 (if false, try second OR)
            make_instruction(1149, 0x01, 1175),   # JMP block1 (both true, goto body)
        ])

        # Block 2: Second AND group (gSideFrags[1]>1 && gSideFrags[1]>=gEndValue)
        block2 = make_block(2, 1151, [
            make_instruction(1153, 0x30, 0x004),  # GADR gSideFrags
            make_instruction(1157, 0x32),         # ADD [4] (second element)
            make_instruction(1158, 0x31, 4),      # DCP
            make_instruction(1162, 0x10),         # IGRE (>1)
            make_instruction(1163, 0x02, 1212),   # JZ block3 (if false, goto end)
            make_instruction(1164, 0x30, 0x004),  # GADR gSideFrags
            make_instruction(1168, 0x32),         # ADD [4]
            make_instruction(1169, 0x31, 4),      # DCP
            make_instruction(1171, 0x11),         # UGEQ (>=gEndValue)
            make_instruction(1172, 0x02, 1212),   # JZ block3 (if false, goto end)
            make_instruction(1173, 0x01, 1175),   # JMP block1 (both true, goto body)
        ])

        # Block 1: True body
        block1 = make_block(1, 1175, [
            make_instruction(1175, 0x20, 999),    # SC_MP_LoadNextMap
        ])

        # Block 3: False body
        block3 = make_block(3, 1212, [
            make_instruction(1212, 0x20, 0),      # Continue
        ])

        cfg.blocks = {0: block0, 1: block1, 2: block2, 3: block3}
        cfg.entry_block = 0

        # Test detection
        start_to_block = {1129: 0, 1151: 2, 1175: 1, 1212: 3}
        result = _detect_short_circuit_pattern(cfg, 0, self.resolver, start_to_block)

        self.assertIsNotNone(result, "Should detect compound (A&&B)||(C&&D) pattern")
        self.assertEqual(result.operator, "||", "Top-level should be OR")
        self.assertEqual(len(result.conditions), 2, "Should have 2 OR branches")

        # Check first AND group
        first_and = result.conditions[0]
        self.assertIsInstance(first_and, CompoundCondition, "First condition should be compound")
        self.assertEqual(first_and.operator, "&&", "First group should be AND")
        self.assertEqual(len(first_and.conditions), 2, "First AND should have 2 conditions")

        # Check second AND group
        second_and = result.conditions[1]
        self.assertIsInstance(second_and, CompoundCondition, "Second condition should be compound")
        self.assertEqual(second_and.operator, "&&", "Second group should be AND")
        self.assertEqual(len(second_and.conditions), 2, "Second AND should have 2 conditions")

        # Check targets
        self.assertEqual(result.true_target, 1, "True target should be block 1")
        self.assertEqual(result.false_target, 3, "False target should be block 3")


class TestComplexNesting(unittest.TestCase):
    """Test complex nesting: if ((a && b && c) || (d && e) || f)"""

    def setUp(self):
        self.resolver = MockResolver()

    def test_complex_or_with_multiple_ands(self):
        """
        Pattern: if ((a && b && c) || (d && e) || f)

        Block 0:  a; JZ block1; b; JZ block1; c; JZ block1; JMP body
        Block 1:  d; JZ block2; e; JZ block2; JMP body
        Block 2:  f; JZ end; JMP body
        """
        # This is an advanced test - implementation should handle it
        # For now, we'll mark it as expected to pass once full implementation is done
        pass


if __name__ == '__main__':
    unittest.main()
