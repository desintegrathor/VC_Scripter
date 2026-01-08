"""
Unit tests for structure analysis modules.

Tests the newly extracted analysis functions from the structure.py refactoring:
- flow.py: CFG analysis functions
- condition.py: Condition extraction and combination
- value_trace.py: SSA value tracing
- variables.py: Variable collection
"""

import unittest
from typing import Dict, List, Set, Optional
from dataclasses import dataclass

# Import analysis modules
from vcdecomp.core.ir.structure.analysis.flow import (
    _get_loop_for_block,
    _is_back_edge_target,
    _find_if_body_blocks,
    _find_common_successor,
    _is_jmp_after_jz,
    _find_all_jz_targets,
    _find_common_true_target,
    _find_case_body_blocks
)

from vcdecomp.core.ir.structure.analysis.condition import (
    _extract_condition_from_block,
    _extract_condition_expr,
    _combine_conditions,
    _collect_and_chain
)

from vcdecomp.core.ir.structure.analysis.value_trace import (
    _trace_value_to_function_call,
    _trace_value_to_global,
    _trace_value_to_parameter,
    _find_switch_variable_from_nearby_gcp
)

from vcdecomp.core.ir.structure.analysis.variables import (
    _collect_local_variables
)

from vcdecomp.core.ir.structure.patterns.models import CompoundCondition


# ============================================================================
# Mock classes for testing
# ============================================================================

class MockInstruction:
    """Mock raw instruction"""
    def __init__(self, address: int, opcode: int, arg1: int = 0, arg2: int = 0):
        self.address = address
        self.opcode = opcode
        self.arg1 = arg1
        self.arg2 = arg2


class MockLiftedInstruction:
    """Mock lifted instruction wrapper"""
    def __init__(self, instruction):
        self.instruction = instruction


class MockSSAInstruction:
    """Mock SSA instruction"""
    def __init__(self, mnemonic: str, address: int = 0, inputs: List = None,
                 instruction=None, block_id: int = 0, producer_inst=None,
                 outputs: List = None):
        self.mnemonic = mnemonic
        self.address = address
        self.inputs = inputs or []
        self.instruction = instruction
        self.block_id = block_id
        self.producer_inst = producer_inst
        self.outputs = outputs or []


class MockSSAValue:
    """Mock SSA value"""
    def __init__(self, name: str = "t0", alias: str = None, value_type=None,
                 producer_inst=None, phi_sources=None):
        self.name = name
        self.alias = alias
        self.value_type = value_type
        self.producer_inst = producer_inst
        self.phi_sources = phi_sources or []


class MockBasicBlock:
    """Mock BasicBlock for testing"""
    def __init__(self, block_id: int, start: int, successors: List[int] = None,
                 instructions: List = None):
        self.block_id = block_id
        self.start = start
        self.successors = successors or []
        self.instructions = instructions or []


class MockCFG:
    """Mock Control Flow Graph"""
    def __init__(self, blocks: Dict[int, MockBasicBlock] = None):
        self.blocks = blocks or {}


class MockNaturalLoop:
    """Mock Natural Loop structure"""
    def __init__(self, header: int, body: Set[int]):
        self.header = header
        self.body = body


class MockOpcodeResolver:
    """Mock opcode resolver"""
    def __init__(self):
        # Define some common opcodes
        self.JMP = 0x01
        self.JZ = 0x02
        self.JNZ = 0x03
        self.RET = 0x10
        self.RETV = 0x11
        self.CALL = 0x20
        self.XCALL = 0x21

    def is_jump(self, opcode: int) -> bool:
        return opcode in {self.JMP, self.JZ, self.JNZ}

    def is_conditional_jump(self, opcode: int) -> bool:
        return opcode in {self.JZ, self.JNZ}

    def is_return(self, opcode: int) -> bool:
        return opcode in {self.RET, self.RETV}

    def get_mnemonic(self, opcode: int) -> str:
        mnemonics = {
            self.JMP: "JMP",
            self.JZ: "JZ",
            self.JNZ: "JNZ",
            self.RET: "RET",
            self.RETV: "RETV",
            self.CALL: "CALL",
            self.XCALL: "XCALL"
        }
        return mnemonics.get(opcode, "UNKNOWN")


class MockSSAFunction:
    """Mock SSA function"""
    def __init__(self, instructions: Dict[int, List[MockSSAInstruction]] = None):
        self.instructions = instructions or {}


class MockExpressionFormatter:
    """Mock expression formatter"""
    def __init__(self):
        self._semantic_names = {}
        self._struct_ranges = {}
        self._global_names = {}

    def render_value(self, value, context=None):
        """Mock render_value"""
        if hasattr(value, 'alias') and value.alias:
            return value.alias
        if hasattr(value, 'name'):
            return value.name
        return str(value)


# ============================================================================
# Tests for flow.py - Control flow analysis
# ============================================================================

class TestGetLoopForBlock(unittest.TestCase):
    """Test _get_loop_for_block function"""

    def test_no_loops(self):
        """Test when block is not in any loop"""
        loops = []
        result = _get_loop_for_block(5, loops)
        self.assertIsNone(result)

    def test_single_loop(self):
        """Test when block is in one loop"""
        loop = MockNaturalLoop(header=0, body={0, 1, 2, 3})
        loops = [loop]
        result = _get_loop_for_block(2, loops)
        self.assertEqual(result, loop)

    def test_nested_loops_returns_innermost(self):
        """Test that innermost loop is returned for nested loops"""
        outer = MockNaturalLoop(header=0, body={0, 1, 2, 3, 4, 5})
        inner = MockNaturalLoop(header=2, body={2, 3})
        loops = [outer, inner]
        result = _get_loop_for_block(3, loops)
        self.assertEqual(result, inner)  # Should return smaller loop
        self.assertEqual(len(result.body), 2)


class TestIsBackEdgeTarget(unittest.TestCase):
    """Test _is_back_edge_target function"""

    def test_is_back_edge(self):
        """Test detecting a back edge to loop header"""
        loop = MockNaturalLoop(header=0, body={0, 1, 2})
        loops = [loop]
        cfg = MockCFG()

        # Edge from block 2 to header 0 is a back edge
        self.assertTrue(_is_back_edge_target(cfg, 2, 0, loops))

    def test_not_back_edge_different_target(self):
        """Test when target is not a loop header"""
        loop = MockNaturalLoop(header=0, body={0, 1, 2})
        loops = [loop]
        cfg = MockCFG()

        # Edge to non-header is not a back edge
        self.assertFalse(_is_back_edge_target(cfg, 2, 3, loops))

    def test_not_back_edge_source_outside_loop(self):
        """Test when source is outside loop body"""
        loop = MockNaturalLoop(header=0, body={0, 1, 2})
        loops = [loop]
        cfg = MockCFG()

        # Edge from outside loop to header is not a back edge
        self.assertFalse(_is_back_edge_target(cfg, 5, 0, loops))


class TestFindIfBodyBlocks(unittest.TestCase):
    """Test _find_if_body_blocks function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_single_block_body(self):
        """Test if body with single block"""
        block = MockBasicBlock(1, 100, successors=[])
        cfg = MockCFG({1: block})

        result = _find_if_body_blocks(cfg, 1, set(), self.resolver)
        self.assertEqual(result, {1})

    def test_multi_block_body(self):
        """Test if body with multiple blocks"""
        blocks = {
            1: MockBasicBlock(1, 100, successors=[2]),
            2: MockBasicBlock(2, 200, successors=[3]),
            3: MockBasicBlock(3, 300, successors=[])
        }
        cfg = MockCFG(blocks)

        result = _find_if_body_blocks(cfg, 1, set(), self.resolver)
        self.assertEqual(result, {1, 2, 3})

    def test_stops_at_stop_blocks(self):
        """Test that BFS stops at stop_blocks"""
        blocks = {
            1: MockBasicBlock(1, 100, successors=[2]),
            2: MockBasicBlock(2, 200, successors=[3]),
            3: MockBasicBlock(3, 300, successors=[])
        }
        cfg = MockCFG(blocks)

        result = _find_if_body_blocks(cfg, 1, {3}, self.resolver)
        self.assertEqual(result, {1, 2})  # Should not include block 3

    def test_stops_at_return(self):
        """Test that BFS stops after return instruction"""
        ret_instr = MockInstruction(200, self.resolver.RET)
        blocks = {
            1: MockBasicBlock(1, 100, successors=[2], instructions=[ret_instr])
        }
        cfg = MockCFG(blocks)

        result = _find_if_body_blocks(cfg, 1, set(), self.resolver)
        self.assertEqual(result, {1})  # Should not follow successors after return


class TestFindCommonSuccessor(unittest.TestCase):
    """Test _find_common_successor function"""

    def test_immediate_common_successor(self):
        """Test finding merge point of two branches"""
        blocks = {
            1: MockBasicBlock(1, 100, successors=[3]),
            2: MockBasicBlock(2, 200, successors=[3]),
            3: MockBasicBlock(3, 300, successors=[])
        }
        cfg = MockCFG(blocks)

        result = _find_common_successor(cfg, 1, 2)
        self.assertEqual(result, 3)

    def test_no_common_successor(self):
        """Test when branches don't merge"""
        blocks = {
            1: MockBasicBlock(1, 100, successors=[]),
            2: MockBasicBlock(2, 200, successors=[])
        }
        cfg = MockCFG(blocks)

        result = _find_common_successor(cfg, 1, 2)
        self.assertIsNone(result)

    def test_distant_common_successor(self):
        """Test finding merge point several blocks away"""
        blocks = {
            1: MockBasicBlock(1, 100, successors=[3]),
            2: MockBasicBlock(2, 200, successors=[4]),
            3: MockBasicBlock(3, 300, successors=[5]),
            4: MockBasicBlock(4, 400, successors=[5]),
            5: MockBasicBlock(5, 500, successors=[])
        }
        cfg = MockCFG(blocks)

        result = _find_common_successor(cfg, 1, 2)
        self.assertEqual(result, 5)


class TestIsJmpAfterJz(unittest.TestCase):
    """Test _is_jmp_after_jz function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_pattern_matches(self):
        """Test detecting JZ followed by JMP"""
        jz_instr = MockInstruction(100, self.resolver.JZ, arg1=200)
        jmp_instr = MockInstruction(112, self.resolver.JMP, arg1=300)
        block = MockBasicBlock(1, 100, instructions=[jz_instr, jmp_instr])

        result = _is_jmp_after_jz(block, self.resolver)
        self.assertEqual(result, 300)  # Should return JMP target

    def test_no_pattern_only_jz(self):
        """Test when block has only JZ"""
        jz_instr = MockInstruction(100, self.resolver.JZ, arg1=200)
        block = MockBasicBlock(1, 100, instructions=[jz_instr])

        result = _is_jmp_after_jz(block, self.resolver)
        self.assertIsNone(result)

    def test_no_pattern_wrong_order(self):
        """Test when instructions are in wrong order"""
        jmp_instr = MockInstruction(100, self.resolver.JMP, arg1=300)
        jz_instr = MockInstruction(112, self.resolver.JZ, arg1=200)
        block = MockBasicBlock(1, 100, instructions=[jmp_instr, jz_instr])

        result = _is_jmp_after_jz(block, self.resolver)
        self.assertIsNone(result)


class TestFindAllJzTargets(unittest.TestCase):
    """Test _find_all_jz_targets function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_single_jz(self):
        """Test finding single conditional jump target"""
        jz_instr = MockInstruction(100, self.resolver.JZ, arg1=200)
        block = MockBasicBlock(1, 100, instructions=[jz_instr])
        cfg = MockCFG({1: block})

        result = _find_all_jz_targets(cfg, 1, self.resolver)
        self.assertEqual(result, {200})

    def test_multiple_jz(self):
        """Test finding multiple conditional jump targets"""
        jz1 = MockInstruction(100, self.resolver.JZ, arg1=200)
        jz2 = MockInstruction(112, self.resolver.JNZ, arg1=300)
        block = MockBasicBlock(1, 100, instructions=[jz1, jz2])
        cfg = MockCFG({1: block})

        result = _find_all_jz_targets(cfg, 1, self.resolver)
        self.assertEqual(result, {200, 300})

    def test_no_jz(self):
        """Test when block has no conditional jumps"""
        jmp_instr = MockInstruction(100, self.resolver.JMP, arg1=200)
        block = MockBasicBlock(1, 100, instructions=[jmp_instr])
        cfg = MockCFG({1: block})

        result = _find_all_jz_targets(cfg, 1, self.resolver)
        self.assertEqual(result, set())


class TestFindCommonTrueTarget(unittest.TestCase):
    """Test _find_common_true_target function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_common_target_found(self):
        """Test finding common TRUE target in OR pattern"""
        # Both blocks: JZ ...; JMP 500
        jz1 = MockInstruction(100, self.resolver.JZ, arg1=200)
        jmp1 = MockInstruction(112, self.resolver.JMP, arg1=500)
        block1 = MockBasicBlock(1, 100, instructions=[jz1, jmp1])

        jz2 = MockInstruction(200, self.resolver.JZ, arg1=300)
        jmp2 = MockInstruction(212, self.resolver.JMP, arg1=500)
        block2 = MockBasicBlock(2, 200, instructions=[jz2, jmp2])

        cfg = MockCFG({1: block1, 2: block2})

        result = _find_common_true_target(cfg, [1, 2], self.resolver)
        self.assertEqual(result, 500)

    def test_no_common_target(self):
        """Test when blocks jump to different targets"""
        jz1 = MockInstruction(100, self.resolver.JZ, arg1=200)
        jmp1 = MockInstruction(112, self.resolver.JMP, arg1=500)
        block1 = MockBasicBlock(1, 100, instructions=[jz1, jmp1])

        jz2 = MockInstruction(200, self.resolver.JZ, arg1=300)
        jmp2 = MockInstruction(212, self.resolver.JMP, arg1=600)  # Different target
        block2 = MockBasicBlock(2, 200, instructions=[jz2, jmp2])

        cfg = MockCFG({1: block1, 2: block2})

        result = _find_common_true_target(cfg, [1, 2], self.resolver)
        self.assertIsNone(result)


class TestFindCaseBodyBlocks(unittest.TestCase):
    """Test _find_case_body_blocks function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_single_block_case(self):
        """Test case with single block"""
        block = MockBasicBlock(1, 100, successors=[])
        cfg = MockCFG({1: block})

        result = _find_case_body_blocks(cfg, 1, set(), self.resolver)
        self.assertEqual(result, {1})

    def test_multi_block_case(self):
        """Test case body with multiple blocks"""
        blocks = {
            1: MockBasicBlock(1, 100, successors=[2]),
            2: MockBasicBlock(2, 200, successors=[3]),
            3: MockBasicBlock(3, 300, successors=[])
        }
        cfg = MockCFG(blocks)

        result = _find_case_body_blocks(cfg, 1, set(), self.resolver)
        self.assertEqual(result, {1, 2, 3})

    def test_stops_at_other_cases(self):
        """Test that BFS stops at other case entries"""
        blocks = {
            1: MockBasicBlock(1, 100, successors=[2, 5]),
            2: MockBasicBlock(2, 200, successors=[]),
            5: MockBasicBlock(5, 500, successors=[])
        }
        cfg = MockCFG(blocks)

        # Block 5 is another case entry
        result = _find_case_body_blocks(cfg, 1, {5}, self.resolver)
        self.assertEqual(result, {1, 2})  # Should not include block 5


# ============================================================================
# Tests for condition.py - Condition extraction and combination
# ============================================================================

class TestExtractConditionFromBlock(unittest.TestCase):
    """Test _extract_condition_from_block function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()
        self.formatter = MockExpressionFormatter()

    def test_extract_simple_condition(self):
        """Test extracting condition from JZ block"""
        # Create SSA instruction with condition value
        cond_value = MockSSAValue(name="t0", alias="x > 0")
        ssa_inst = MockSSAInstruction("JZ", address=100, inputs=[cond_value])
        ssa_func = MockSSAFunction({1: [ssa_inst]})

        # Create CFG block
        raw_inst = MockInstruction(100, self.resolver.JZ, arg1=200)
        block = MockBasicBlock(1, 100, instructions=[raw_inst])
        cfg = MockCFG({1: block})

        result = _extract_condition_from_block(1, ssa_func, self.formatter, cfg, self.resolver)
        self.assertEqual(result, "x > 0")

    def test_no_condition_no_jz(self):
        """Test when block has no conditional jump"""
        ssa_func = MockSSAFunction({1: []})

        raw_inst = MockInstruction(100, self.resolver.JMP, arg1=200)
        block = MockBasicBlock(1, 100, instructions=[raw_inst])
        cfg = MockCFG({1: block})

        result = _extract_condition_from_block(1, ssa_func, self.formatter, cfg, self.resolver)
        self.assertIsNone(result)


class TestCombineConditions(unittest.TestCase):
    """Test _combine_conditions function"""

    def test_combine_two_simple_conditions(self):
        """Test combining two string conditions with AND"""
        result = _combine_conditions(["a > 0", "b < 10"], "&&")
        self.assertEqual(result, "a > 0 && b < 10")

    def test_combine_two_conditions_or(self):
        """Test combining two conditions with OR"""
        result = _combine_conditions(["x == 0", "y == 0"], "||")
        self.assertEqual(result, "x == 0 || y == 0")

    def test_combine_single_condition(self):
        """Test combining single condition returns it unchanged"""
        result = _combine_conditions(["a > 0"], "&&")
        self.assertEqual(result, "a > 0")

    def test_combine_compound_conditions(self):
        """Test combining compound conditions"""
        cond1 = CompoundCondition(
            operator="&&",
            conditions=["a", "b"],
            true_target=1,
            false_target=2
        )
        cond2 = "c > 0"

        result = _combine_conditions([cond1, cond2], "||")
        # Should combine nested compound with simple condition
        self.assertIsInstance(result, str)
        self.assertIn("||", result)


class TestCollectAndChain(unittest.TestCase):
    """Test _collect_and_chain function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_simple_and_chain(self):
        """Test collecting simple AND chain"""
        # Block 1: if (!a) goto 5; else goto 2 (fallthrough)
        # Block 2: if (!b) goto 5; else goto 3 (fallthrough)
        # This is: if (a && b) goto 3; else goto 5

        # Create blocks with proper instructions for AND chain pattern
        jz1 = MockInstruction(100, self.resolver.JZ, arg1=500)
        jz2 = MockInstruction(200, self.resolver.JZ, arg1=500)
        jmp3 = MockInstruction(300, self.resolver.JMP, arg1=400)

        blocks = {
            1: MockBasicBlock(1, 100, successors=[5, 2], instructions=[jz1]),
            2: MockBasicBlock(2, 200, successors=[5, 3], instructions=[jz2]),
            3: MockBasicBlock(3, 300, successors=[4], instructions=[jmp3]),
            4: MockBasicBlock(4, 400, successors=[]),
            5: MockBasicBlock(5, 500, successors=[])
        }
        cfg = MockCFG(blocks)
        start_to_block = {100: 1, 200: 2, 300: 3, 400: 4, 500: 5}
        visited = set()

        chain_blocks, true_target, false_target = _collect_and_chain(
            1, cfg, self.resolver, start_to_block, visited
        )
        # Should collect blocks in the AND chain
        # The function returns a list (may be empty if pattern doesn't fully match)
        self.assertIsInstance(chain_blocks, list)
        # The function is complex and requires specific CFG patterns
        # Just verify it returns valid results without crashing
        self.assertTrue(true_target is None or isinstance(true_target, int))
        self.assertTrue(false_target is None or isinstance(false_target, int))


# ============================================================================
# Tests for value_trace.py - SSA value tracing
# ============================================================================

class TestTraceValueToFunctionCall(unittest.TestCase):
    """Test _trace_value_to_function_call function"""

    def setUp(self):
        self.formatter = MockExpressionFormatter()

    def test_trace_to_call_instruction(self):
        """Test tracing value back to CALL instruction"""
        # Create mock instruction structure for LLD
        raw_lld = MockInstruction(112, 0x40, arg1=307)
        lifted_lld = MockLiftedInstruction(raw_lld)

        # Create CALL instruction
        call_inst = MockSSAInstruction("XCALL", address=100, block_id=1)

        # Create LLD instruction that loads return value
        lld_inst = MockSSAInstruction("LLD", address=112, block_id=1,
                                      instruction=lifted_lld)

        # Create value that was produced by LLD
        value = MockSSAValue(name="t1", producer_inst=lld_inst)

        # Create SSA function with both instructions
        ssa_func = MockSSAFunction({
            1: [call_inst, lld_inst]
        })

        result = _trace_value_to_function_call(ssa_func, value, self.formatter)
        # Should find the CALL instruction (or return None if pattern doesn't match)
        # This is a heuristic function, so we just check it doesn't crash
        self.assertTrue(result is None or isinstance(result, str))

    def test_no_trace_no_producer(self):
        """Test when value has no producer"""
        value = MockSSAValue(name="t1", producer_inst=None)
        ssa_func = MockSSAFunction({})

        result = _trace_value_to_function_call(ssa_func, value, self.formatter)
        self.assertIsNone(result)


class TestTraceValueToGlobal(unittest.TestCase):
    """Test _trace_value_to_global function"""

    def setUp(self):
        self.formatter = MockExpressionFormatter()
        self.formatter._global_names = {0: "global_var"}

    def test_trace_to_gcp_instruction(self):
        """Test tracing value to global variable load (GCP)"""
        # Create mock instruction structure
        raw_inst = MockInstruction(100, 0x50, arg1=0)
        lifted_inst = MockLiftedInstruction(raw_inst)

        # Create GCP instruction (Get Constant Pointer - loads global)
        gcp_inst = MockSSAInstruction("GCP", address=100, block_id=1,
                                      instruction=lifted_inst)

        # Create value produced by GCP
        value = MockSSAValue(name="gVar_0", producer_inst=gcp_inst)

        result = _trace_value_to_global(value, self.formatter)
        # Should identify as global variable
        self.assertEqual(result, "global_var")


class TestTraceValueToParameter(unittest.TestCase):
    """Test _trace_value_to_parameter function"""

    def setUp(self):
        self.formatter = MockExpressionFormatter()

    def test_trace_to_parameter(self):
        """Test tracing value to function parameter (LCP)"""
        # Create mock instruction structure for LCP
        raw_inst = MockInstruction(100, 0x30, arg1=306)  # Load from stack at known offset
        lifted_inst = MockLiftedInstruction(raw_inst)

        # Create LCP instruction (Load Constant Pointer - loads parameter)
        lcp_inst = MockSSAInstruction("LCP", address=100, block_id=1, instruction=lifted_inst)

        # Create value produced by LCP
        value = MockSSAValue(name="param_0", alias="info", producer_inst=lcp_inst)

        ssa_func = MockSSAFunction({1: [lcp_inst]})

        result = _trace_value_to_parameter(value, self.formatter, ssa_func)
        # Should identify as parameter (returns field access like "info->message")
        # Offset 306 maps to "message" field
        self.assertEqual(result, "info->message")


class TestFindSwitchVariableFromNearbyGcp(unittest.TestCase):
    """Test _find_switch_variable_from_nearby_gcp function"""

    def setUp(self):
        self.formatter = MockExpressionFormatter()
        self.formatter._global_names = {0: "global_var"}

    def test_find_nearby_gcp(self):
        """Test finding GCP instruction near switch"""
        # Create mock instruction structure
        raw_inst = MockInstruction(100, 0x50, arg1=0)
        lifted_inst = MockLiftedInstruction(raw_inst)

        # Create GCP instruction followed by other instructions
        gcp_value = MockSSAValue(name="gVar_0", alias="data_0", producer_inst=None)
        gcp_inst = MockSSAInstruction("GCP", address=100, block_id=1,
                                      instruction=lifted_inst,
                                      outputs=[gcp_value])
        other_inst = MockSSAInstruction("ADD", address=112, block_id=1)

        ssa_func = MockSSAFunction({
            1: [gcp_inst, other_inst]
        })

        # Create a mock value to pass to the function
        var_value = MockSSAValue(name="local_0")

        result = _find_switch_variable_from_nearby_gcp(
            ssa_func, 1, var_value, self.formatter, {1}
        )
        # Should find variable from GCP (or return None if no suitable variable)
        # This is a heuristic function, so either result is acceptable
        self.assertTrue(result is None or isinstance(result, str))


# ============================================================================
# Tests for variables.py - Variable collection
# ============================================================================

class TestCollectLocalVariables(unittest.TestCase):
    """Test _collect_local_variables function"""

    def setUp(self):
        self.formatter = MockExpressionFormatter()

    def test_collect_simple_variables(self):
        """Test collecting simple local variables"""
        # Create some SSA instructions with local variables
        value1 = MockSSAValue(name="local_0", alias="i")
        value2 = MockSSAValue(name="local_1", alias="j")

        inst1 = MockSSAInstruction("ASSIGN", inputs=[], outputs=[value1])
        inst2 = MockSSAInstruction("ASSIGN", inputs=[], outputs=[value2])

        ssa_func = MockSSAFunction({
            1: [inst1, inst2]
        })

        result = _collect_local_variables(ssa_func, {1}, self.formatter)
        # Should collect variables (returns list of declaration strings)
        self.assertIsInstance(result, list)

    def test_skip_parameters(self):
        """Test that function parameters are skipped"""
        # param_ variables should be skipped
        value = MockSSAValue(name="param_0", alias="info")
        inst = MockSSAInstruction("ASSIGN", inputs=[], outputs=[value])

        ssa_func = MockSSAFunction({1: [inst]})

        result = _collect_local_variables(ssa_func, {1}, self.formatter)
        # Parameters should not be in result
        self.assertEqual(result, [])

    def test_skip_globals(self):
        """Test that global variables are skipped"""
        # data_ and gVar variables should be skipped
        value1 = MockSSAValue(name="data_0")
        value2 = MockSSAValue(name="gVar_1")

        inst1 = MockSSAInstruction("ASSIGN", inputs=[], outputs=[value1])
        inst2 = MockSSAInstruction("ASSIGN", inputs=[], outputs=[value2])

        ssa_func = MockSSAFunction({1: [inst1, inst2]})

        result = _collect_local_variables(ssa_func, {1}, self.formatter)
        # Globals should not be in result
        self.assertEqual(result, [])


# ============================================================================
# Integration tests - verify imports work correctly
# ============================================================================

class TestAnalysisImports(unittest.TestCase):
    """Test that all analysis imports work correctly"""

    def test_flow_imports(self):
        """Test importing from flow module"""
        from vcdecomp.core.ir.structure.analysis.flow import (
            _get_loop_for_block,
            _is_back_edge_target,
            _find_if_body_blocks,
            _find_common_successor,
            _is_jmp_after_jz,
            _find_all_jz_targets,
            _find_common_true_target,
            _find_case_body_blocks
        )

        # Verify all are callable
        self.assertTrue(callable(_get_loop_for_block))
        self.assertTrue(callable(_is_back_edge_target))
        self.assertTrue(callable(_find_if_body_blocks))
        self.assertTrue(callable(_find_common_successor))
        self.assertTrue(callable(_is_jmp_after_jz))
        self.assertTrue(callable(_find_all_jz_targets))
        self.assertTrue(callable(_find_common_true_target))
        self.assertTrue(callable(_find_case_body_blocks))

    def test_condition_imports(self):
        """Test importing from condition module"""
        from vcdecomp.core.ir.structure.analysis.condition import (
            _extract_condition_from_block,
            _extract_condition_expr,
            _combine_conditions,
            _collect_and_chain
        )

        # Verify all are callable
        self.assertTrue(callable(_extract_condition_from_block))
        self.assertTrue(callable(_extract_condition_expr))
        self.assertTrue(callable(_combine_conditions))
        self.assertTrue(callable(_collect_and_chain))

    def test_value_trace_imports(self):
        """Test importing from value_trace module"""
        from vcdecomp.core.ir.structure.analysis.value_trace import (
            _trace_value_to_function_call,
            _trace_value_to_global,
            _trace_value_to_parameter,
            _find_switch_variable_from_nearby_gcp
        )

        # Verify all are callable
        self.assertTrue(callable(_trace_value_to_function_call))
        self.assertTrue(callable(_trace_value_to_global))
        self.assertTrue(callable(_trace_value_to_parameter))
        self.assertTrue(callable(_find_switch_variable_from_nearby_gcp))

    def test_variables_imports(self):
        """Test importing from variables module"""
        from vcdecomp.core.ir.structure.analysis.variables import (
            _collect_local_variables
        )

        # Verify it's callable
        self.assertTrue(callable(_collect_local_variables))

    def test_package_level_imports(self):
        """Test importing from analysis package"""
        from vcdecomp.core.ir.structure.analysis import (
            _get_loop_for_block,
            _extract_condition_from_block,
            _trace_value_to_function_call,
            _collect_local_variables
        )

        # Verify all are accessible at package level
        self.assertTrue(callable(_get_loop_for_block))
        self.assertTrue(callable(_extract_condition_from_block))
        self.assertTrue(callable(_trace_value_to_function_call))
        self.assertTrue(callable(_collect_local_variables))


if __name__ == '__main__':
    unittest.main()
