"""
Unit tests for structure analysis utilities and data models.

Tests the newly extracted utility functions and data classes from the
structure.py refactoring.
"""

import unittest
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import FrozenInstanceError

# Import utilities
from vcdecomp.core.ir.structure.utils.helpers import (
    _load_symbol_db,
    _build_start_map,
    _dominates,
    _is_control_flow_only,
    SHOW_BLOCK_COMMENTS
)

# Import data models
from vcdecomp.core.ir.structure.patterns.models import (
    CaseInfo,
    SwitchPattern,
    IfElsePattern,
    CompoundCondition,
    ForLoopInfo
)


# ============================================================================
# Mock classes for testing
# ============================================================================

class MockCFG:
    """Mock Control Flow Graph for testing"""

    def __init__(self, blocks=None, idom=None):
        self.blocks = blocks or {}
        self.idom = idom or {}


class MockBasicBlock:
    """Mock BasicBlock for testing"""

    def __init__(self, block_id: int, start: int):
        self.block_id = block_id
        self.start = start


class MockSSAInstruction:
    """Mock SSA instruction for testing"""

    def __init__(self, mnemonic: str, instruction=None):
        self.mnemonic = mnemonic
        self.instruction = instruction


class MockLiftedInstruction:
    """Mock lifted instruction wrapper"""

    def __init__(self, instruction):
        self.instruction = instruction


class MockInstruction:
    """Mock raw instruction"""

    def __init__(self, opcode: int):
        self.opcode = opcode


class MockOpcodeResolver:
    """Mock opcode resolver for testing"""

    def __init__(self):
        self.jump_opcodes = {0x01, 0x02, 0x03}  # JMP, JZ, JNZ
        self.return_opcodes = {0x10, 0x11}       # RET, RETV

    def is_jump(self, opcode: int) -> bool:
        return opcode in self.jump_opcodes

    def is_return(self, opcode: int) -> bool:
        return opcode in self.return_opcodes


# ============================================================================
# Tests for utility functions
# ============================================================================

class TestLoadSymbolDB(unittest.TestCase):
    """Test _load_symbol_db utility function"""

    def test_load_symbol_db_returns_optional(self):
        """Test that _load_symbol_db returns None or SymbolDatabase"""
        result = _load_symbol_db()
        # Result should be either None or a SymbolDatabase instance
        self.assertTrue(result is None or hasattr(result, 'load'))

    def test_load_symbol_db_handles_missing_file(self):
        """Test that missing symbol_db.json is handled gracefully"""
        # Should not raise exception even if file doesn't exist
        try:
            result = _load_symbol_db()
            # If it didn't crash, test passes
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"_load_symbol_db raised unexpected exception: {e}")


class TestBuildStartMap(unittest.TestCase):
    """Test _build_start_map utility function"""

    def test_build_start_map_empty_cfg(self):
        """Test building start map from empty CFG"""
        cfg = MockCFG(blocks={})
        result = _build_start_map(cfg)

        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    def test_build_start_map_single_block(self):
        """Test building start map with single block"""
        block = MockBasicBlock(block_id=0, start=100)
        cfg = MockCFG(blocks={0: block})
        result = _build_start_map(cfg)

        self.assertEqual(result, {100: 0})
        self.assertEqual(len(result), 1)

    def test_build_start_map_multiple_blocks(self):
        """Test building start map with multiple blocks"""
        blocks = {
            0: MockBasicBlock(0, 100),
            1: MockBasicBlock(1, 200),
            2: MockBasicBlock(2, 300),
            5: MockBasicBlock(5, 500)
        }
        cfg = MockCFG(blocks=blocks)
        result = _build_start_map(cfg)

        expected = {100: 0, 200: 1, 300: 2, 500: 5}
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 4)


class TestDominates(unittest.TestCase):
    """Test _dominates utility function"""

    def test_dominates_self(self):
        """Test that a block dominates itself"""
        cfg = MockCFG(idom={})

        self.assertTrue(_dominates(cfg, 0, 0))
        self.assertTrue(_dominates(cfg, 5, 5))

    def test_dominates_direct_parent(self):
        """Test domination with direct parent"""
        # idom: 1's immediate dominator is 0
        cfg = MockCFG(idom={1: 0})

        self.assertTrue(_dominates(cfg, 0, 1))
        self.assertFalse(_dominates(cfg, 1, 0))

    def test_dominates_chain(self):
        """Test domination through chain: 0 -> 1 -> 2 -> 3"""
        cfg = MockCFG(idom={1: 0, 2: 1, 3: 2})

        # 0 dominates all
        self.assertTrue(_dominates(cfg, 0, 1))
        self.assertTrue(_dominates(cfg, 0, 2))
        self.assertTrue(_dominates(cfg, 0, 3))

        # 1 dominates 2 and 3
        self.assertTrue(_dominates(cfg, 1, 2))
        self.assertTrue(_dominates(cfg, 1, 3))

        # 2 dominates only 3
        self.assertTrue(_dominates(cfg, 2, 3))

        # No backward domination
        self.assertFalse(_dominates(cfg, 3, 2))
        self.assertFalse(_dominates(cfg, 2, 1))
        self.assertFalse(_dominates(cfg, 1, 0))

    def test_dominates_no_path(self):
        """Test domination when no path exists"""
        cfg = MockCFG(idom={1: 0, 3: 2})

        # 0 doesn't dominate 3 (different tree)
        self.assertFalse(_dominates(cfg, 0, 3))
        self.assertFalse(_dominates(cfg, 2, 1))

    def test_dominates_self_loop(self):
        """Test domination with self-loop in idom (edge case)"""
        cfg = MockCFG(idom={0: 0, 1: 0})

        # Should handle self-loop gracefully
        self.assertTrue(_dominates(cfg, 0, 0))
        self.assertTrue(_dominates(cfg, 0, 1))


class TestIsControlFlowOnly(unittest.TestCase):
    """Test _is_control_flow_only utility function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_empty_block(self):
        """Test that empty block is control flow only"""
        result = _is_control_flow_only([], self.resolver)
        self.assertTrue(result)

    def test_phi_only_block(self):
        """Test block with only PHI instructions"""
        block = [
            MockSSAInstruction("PHI"),
            MockSSAInstruction("PHI"),
        ]
        result = _is_control_flow_only(block, self.resolver)
        self.assertTrue(result)

    def test_jump_only_block(self):
        """Test block with only jump instructions"""
        inst = MockInstruction(opcode=0x01)  # JMP
        lifted = MockLiftedInstruction(inst)
        block = [
            MockSSAInstruction("JMP", lifted)
        ]
        result = _is_control_flow_only(block, self.resolver)
        self.assertTrue(result)

    def test_return_only_block(self):
        """Test block with only return instructions"""
        inst = MockInstruction(opcode=0x10)  # RET
        lifted = MockLiftedInstruction(inst)
        block = [
            MockSSAInstruction("RET", lifted)
        ]
        result = _is_control_flow_only(block, self.resolver)
        self.assertTrue(result)

    def test_phi_and_jump_block(self):
        """Test block with PHI and jump (still control flow only)"""
        inst = MockInstruction(opcode=0x02)  # JZ
        lifted = MockLiftedInstruction(inst)
        block = [
            MockSSAInstruction("PHI"),
            MockSSAInstruction("JZ", lifted),
        ]
        result = _is_control_flow_only(block, self.resolver)
        self.assertTrue(result)

    def test_block_with_real_instruction(self):
        """Test block with actual computational instruction"""
        inst = MockInstruction(opcode=0x20)  # Some non-control-flow opcode
        lifted = MockLiftedInstruction(inst)
        block = [
            MockSSAInstruction("PUSH", lifted)
        ]
        result = _is_control_flow_only(block, self.resolver)
        self.assertFalse(result)

    def test_block_with_mixed_instructions(self):
        """Test block with both control flow and real instructions"""
        inst1 = MockInstruction(opcode=0x20)  # PUSH
        inst2 = MockInstruction(opcode=0x01)  # JMP
        lifted1 = MockLiftedInstruction(inst1)
        lifted2 = MockLiftedInstruction(inst2)
        block = [
            MockSSAInstruction("PHI"),
            MockSSAInstruction("PUSH", lifted1),
            MockSSAInstruction("JMP", lifted2),
        ]
        result = _is_control_flow_only(block, self.resolver)
        self.assertFalse(result)

    def test_instruction_without_underlying_instruction(self):
        """Test SSA instruction without underlying instruction (edge case)"""
        block = [
            MockSSAInstruction("SOME_OP", None)
        ]
        result = _is_control_flow_only(block, self.resolver)
        # Should handle gracefully and consider it control flow
        self.assertTrue(result)


class TestConstants(unittest.TestCase):
    """Test module constants"""

    def test_show_block_comments_is_bool(self):
        """Test that SHOW_BLOCK_COMMENTS is a boolean"""
        self.assertIsInstance(SHOW_BLOCK_COMMENTS, bool)

    def test_show_block_comments_default_false(self):
        """Test that SHOW_BLOCK_COMMENTS defaults to False"""
        self.assertEqual(SHOW_BLOCK_COMMENTS, False)


# ============================================================================
# Tests for data models
# ============================================================================

class TestCaseInfo(unittest.TestCase):
    """Test CaseInfo data class"""

    def test_case_info_creation(self):
        """Test creating CaseInfo with required fields"""
        case = CaseInfo(value=42, block_id=1)

        self.assertEqual(case.value, 42)
        self.assertEqual(case.block_id, 1)
        self.assertTrue(case.has_break)
        self.assertEqual(case.body_blocks, {1})

    def test_case_info_with_all_fields(self):
        """Test creating CaseInfo with all fields"""
        case = CaseInfo(
            value=100,
            block_id=5,
            body_blocks={5, 6, 7},
            has_break=False
        )

        self.assertEqual(case.value, 100)
        self.assertEqual(case.block_id, 5)
        self.assertEqual(case.body_blocks, {5, 6, 7})
        self.assertFalse(case.has_break)

    def test_case_info_post_init_sets_body_blocks(self):
        """Test that __post_init__ sets body_blocks to {block_id} if None"""
        case = CaseInfo(value=1, block_id=3)
        self.assertEqual(case.body_blocks, {3})

    def test_case_info_post_init_preserves_body_blocks(self):
        """Test that __post_init__ preserves explicit body_blocks"""
        case = CaseInfo(value=1, block_id=3, body_blocks={3, 4, 5})
        self.assertEqual(case.body_blocks, {3, 4, 5})


class TestSwitchPattern(unittest.TestCase):
    """Test SwitchPattern data class"""

    def test_switch_pattern_creation(self):
        """Test creating SwitchPattern with required fields"""
        cases = [
            CaseInfo(value=0, block_id=1),
            CaseInfo(value=1, block_id=2)
        ]
        switch = SwitchPattern(
            test_var="local_0",
            header_block=0,
            cases=cases
        )

        self.assertEqual(switch.test_var, "local_0")
        self.assertEqual(switch.header_block, 0)
        self.assertEqual(len(switch.cases), 2)
        self.assertIsNone(switch.default_block)
        self.assertIsNone(switch.exit_block)

    def test_switch_pattern_post_init_sets_all_blocks(self):
        """Test that __post_init__ computes all_blocks from cases"""
        cases = [
            CaseInfo(value=0, block_id=1),
            CaseInfo(value=1, block_id=2),
            CaseInfo(value=2, block_id=3)
        ]
        switch = SwitchPattern(
            test_var="i",
            header_block=0,
            cases=cases
        )

        # Should include header and all case blocks
        self.assertEqual(switch.all_blocks, {0, 1, 2, 3})

    def test_switch_pattern_with_default(self):
        """Test SwitchPattern with default case"""
        cases = [CaseInfo(value=0, block_id=1)]
        switch = SwitchPattern(
            test_var="x",
            header_block=0,
            cases=cases,
            default_block=5
        )

        self.assertEqual(switch.default_block, 5)
        self.assertEqual(switch.all_blocks, {0, 1, 5})
        self.assertEqual(switch.default_body_blocks, {5})

    def test_switch_pattern_preserves_explicit_all_blocks(self):
        """Test that explicit all_blocks is preserved"""
        cases = [CaseInfo(value=0, block_id=1)]
        explicit_blocks = {0, 1, 2, 3, 4}
        switch = SwitchPattern(
            test_var="x",
            header_block=0,
            cases=cases,
            all_blocks=explicit_blocks
        )

        self.assertEqual(switch.all_blocks, explicit_blocks)


class TestIfElsePattern(unittest.TestCase):
    """Test IfElsePattern data class"""

    def test_if_else_pattern_creation(self):
        """Test creating IfElsePattern with required fields"""
        pattern = IfElsePattern(
            header_block=0,
            true_block=1,
            false_block=2,
            merge_block=3
        )

        self.assertEqual(pattern.header_block, 0)
        self.assertEqual(pattern.true_block, 1)
        self.assertEqual(pattern.false_block, 2)
        self.assertEqual(pattern.merge_block, 3)

    def test_if_else_pattern_post_init_sets_bodies(self):
        """Test that __post_init__ sets true_body and false_body"""
        pattern = IfElsePattern(
            header_block=0,
            true_block=1,
            false_block=2,
            merge_block=None
        )

        self.assertEqual(pattern.true_body, {1})
        self.assertEqual(pattern.false_body, {2})

    def test_if_else_pattern_without_merge(self):
        """Test IfElsePattern without merge block (early return)"""
        pattern = IfElsePattern(
            header_block=0,
            true_block=1,
            false_block=2,
            merge_block=None
        )

        self.assertIsNone(pattern.merge_block)

    def test_if_else_pattern_preserves_explicit_bodies(self):
        """Test that explicit bodies are preserved"""
        pattern = IfElsePattern(
            header_block=0,
            true_block=1,
            false_block=2,
            merge_block=3,
            true_body={1, 4, 5},
            false_body={2, 6, 7}
        )

        self.assertEqual(pattern.true_body, {1, 4, 5})
        self.assertEqual(pattern.false_body, {2, 6, 7})


class TestCompoundCondition(unittest.TestCase):
    """Test CompoundCondition data class"""

    def test_compound_condition_and(self):
        """Test creating AND compound condition"""
        cond = CompoundCondition(
            operator="&&",
            conditions=["a > 0", "b < 10"],
            true_target=1,
            false_target=2
        )

        self.assertEqual(cond.operator, "&&")
        self.assertEqual(len(cond.conditions), 2)
        self.assertEqual(cond.true_target, 1)
        self.assertEqual(cond.false_target, 2)

    def test_compound_condition_or(self):
        """Test creating OR compound condition"""
        cond = CompoundCondition(
            operator="||",
            conditions=["x == 0", "y == 0"],
            true_target=5,
            false_target=6
        )

        self.assertEqual(cond.operator, "||")
        self.assertEqual(len(cond.conditions), 2)

    def test_compound_condition_nested(self):
        """Test nested compound conditions"""
        inner1 = CompoundCondition(
            operator="&&",
            conditions=["a", "b"],
            true_target=1,
            false_target=2
        )
        inner2 = CompoundCondition(
            operator="&&",
            conditions=["c", "d"],
            true_target=1,
            false_target=2
        )
        outer = CompoundCondition(
            operator="||",
            conditions=[inner1, inner2],
            true_target=1,
            false_target=2
        )

        self.assertEqual(outer.operator, "||")
        self.assertEqual(len(outer.conditions), 2)
        self.assertIsInstance(outer.conditions[0], CompoundCondition)
        self.assertIsInstance(outer.conditions[1], CompoundCondition)

    def test_compound_condition_post_init_sets_involved_blocks(self):
        """Test that __post_init__ initializes involved_blocks"""
        cond = CompoundCondition(
            operator="&&",
            conditions=["test"],
            true_target=1,
            false_target=2
        )

        self.assertEqual(cond.involved_blocks, set())
        self.assertIsInstance(cond.involved_blocks, set)

    def test_compound_condition_preserves_involved_blocks(self):
        """Test that explicit involved_blocks is preserved"""
        blocks = {0, 1, 2}
        cond = CompoundCondition(
            operator="||",
            conditions=["test"],
            true_target=1,
            false_target=2,
            involved_blocks=blocks
        )

        self.assertEqual(cond.involved_blocks, blocks)


class TestForLoopInfo(unittest.TestCase):
    """Test ForLoopInfo data class"""

    def test_for_loop_info_creation(self):
        """Test creating ForLoopInfo with required fields"""
        loop = ForLoopInfo(
            var="i",
            init="0",
            condition="i < 10",
            increment="i++"
        )

        self.assertEqual(loop.var, "i")
        self.assertEqual(loop.init, "0")
        self.assertEqual(loop.condition, "i < 10")
        self.assertEqual(loop.increment, "i++")
        self.assertEqual(loop.init_var, "")

    def test_for_loop_info_with_init_var(self):
        """Test ForLoopInfo with init_var for filtering"""
        loop = ForLoopInfo(
            var="i",
            init="0",
            condition="i < count",
            increment="i++",
            init_var="local_2"
        )

        self.assertEqual(loop.var, "i")
        self.assertEqual(loop.init_var, "local_2")

    def test_for_loop_info_complex_expressions(self):
        """Test ForLoopInfo with complex expressions"""
        loop = ForLoopInfo(
            var="idx",
            init="start + offset",
            condition="idx < (end - 1)",
            increment="idx += 2"
        )

        self.assertEqual(loop.init, "start + offset")
        self.assertEqual(loop.condition, "idx < (end - 1)")
        self.assertEqual(loop.increment, "idx += 2")


# ============================================================================
# Integration tests - verify imports work correctly
# ============================================================================

class TestImports(unittest.TestCase):
    """Test that all imports work correctly"""

    def test_utils_imports(self):
        """Test importing from utils package"""
        from vcdecomp.core.ir.structure.utils import (
            _load_symbol_db,
            _build_start_map,
            _dominates,
            _is_control_flow_only,
            SHOW_BLOCK_COMMENTS
        )

        # Verify all imports are callable/accessible
        self.assertTrue(callable(_load_symbol_db))
        self.assertTrue(callable(_build_start_map))
        self.assertTrue(callable(_dominates))
        self.assertTrue(callable(_is_control_flow_only))
        self.assertIsInstance(SHOW_BLOCK_COMMENTS, bool)

    def test_patterns_imports(self):
        """Test importing from patterns package"""
        from vcdecomp.core.ir.structure.patterns import (
            CaseInfo,
            SwitchPattern,
            IfElsePattern,
            CompoundCondition,
            ForLoopInfo
        )

        # Verify all classes can be instantiated
        self.assertTrue(callable(CaseInfo))
        self.assertTrue(callable(SwitchPattern))
        self.assertTrue(callable(IfElsePattern))
        self.assertTrue(callable(CompoundCondition))
        self.assertTrue(callable(ForLoopInfo))

    def test_models_direct_import(self):
        """Test importing directly from models module"""
        from vcdecomp.core.ir.structure.patterns.models import CaseInfo

        case = CaseInfo(value=1, block_id=0)
        self.assertEqual(case.value, 1)

    def test_helpers_direct_import(self):
        """Test importing directly from helpers module"""
        from vcdecomp.core.ir.structure.utils.helpers import _build_start_map

        self.assertTrue(callable(_build_start_map))


if __name__ == '__main__':
    unittest.main()
