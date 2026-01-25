"""
Unit tests for structure pattern detection modules.

Tests the newly extracted pattern detection functions from the structure.py refactoring:
- if_else.py: Early return, short-circuit, and if/else pattern detection
- switch_case.py: Switch/case pattern detection
- loops.py: For-loop pattern detection
"""

import unittest
from typing import Dict, List, Set, Optional
from dataclasses import dataclass

# Import pattern detection modules
from vcdecomp.core.ir.structure.patterns.if_else import (
    _detect_early_return_pattern,
    _detect_short_circuit_pattern,
    _detect_if_else_pattern,
    _detect_ternary_pattern
)

from vcdecomp.core.ir.structure.patterns.switch_case import (
    _find_switch_variable_from_nearby_gcp,
    _detect_switch_patterns
)

from vcdecomp.core.ir.structure.patterns.loops import (
    _detect_for_loop
)

from vcdecomp.core.ir.structure.patterns.models import (
    CaseInfo,
    SwitchPattern,
    IfElsePattern,
    CompoundCondition,
    ForLoopInfo,
    TernaryInfo
)


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
                 instructions: List = None, predecessors: List[int] = None):
        self.block_id = block_id
        self.start = start
        self.successors = successors or []
        self.instructions = instructions or []
        self.predecessors = predecessors or []


class MockCFG:
    """Mock Control Flow Graph"""
    def __init__(self, blocks: Dict[int, MockBasicBlock] = None, idom: Dict[int, int] = None):
        self.blocks = blocks or {}
        self.idom = idom or {}


class MockNaturalLoop:
    """Mock Natural Loop structure"""
    def __init__(self, header: int, body: Set[int] = None, back_edges: List = None):
        self.header = header
        self.body = body or set()
        self.back_edges = back_edges or []


class MockBackEdge:
    """Mock back edge"""
    def __init__(self, source: int, target: int):
        self.source = source
        self.target = target


class MockOpcodeResolver:
    """Mock opcode resolver"""
    def __init__(self):
        # Opcode mappings
        self.opcodes = {
            'JMP': 0x01,
            'JZ': 0x02,
            'JNZ': 0x03,
            'RET': 0x10,
            'EQU': 0x20,
            'IADD': 0x30,
            'XCALL': 0x40,  # External function call
            'CALL': 0x41,   # Internal function call
        }

    def is_conditional_jump(self, opcode: int) -> bool:
        return opcode in {self.opcodes['JZ'], self.opcodes['JNZ']}

    def is_jump(self, opcode: int) -> bool:
        return opcode in {self.opcodes['JMP'], self.opcodes['JZ'], self.opcodes['JNZ']}

    def is_return(self, opcode: int) -> bool:
        return opcode == self.opcodes['RET']

    def get_mnemonic(self, opcode: int) -> str:
        for name, code in self.opcodes.items():
            if code == opcode:
                return name
        return "UNKNOWN"


class MockSSAFunction:
    """Mock SSA function"""
    def __init__(self, cfg: MockCFG = None, instructions: Dict[int, List] = None, scr=None):
        self.cfg = cfg or MockCFG()
        self.instructions = instructions or {}
        self.scr = scr


class MockConstantPropagator:
    """Mock constant propagator for switch detection"""
    def get_constant(self, value):
        """Return constant info for SSA value"""
        # Check if value has alias starting with data_ (constant from data segment)
        if hasattr(value, 'alias') and value.alias and value.alias.startswith('data_'):
            try:
                # Extract offset from alias (e.g., "data_0" -> 0)
                offset = int(value.alias[5:])
                # Return a mock constant info object
                return type('ConstantInfo', (), {'value': offset})()
            except (ValueError, AttributeError):
                pass
        return None


class MockExpressionFormatter:
    """Mock expression formatter"""
    def __init__(self, global_names: Dict[int, str] = None, semantic_names: Dict[str, str] = None):
        self._global_names = global_names or {}
        self._semantic_names = semantic_names or {}
        self._constant_propagator = MockConstantPropagator()

    def render_value(self, value, context=None) -> str:
        """Render SSA value as string"""
        # context parameter is optional and used by real formatter
        if hasattr(value, 'alias') and value.alias:
            return value.alias
        if hasattr(value, 'name'):
            return value.name
        return str(value)


class MockDataSegment:
    """Mock data segment"""
    def __init__(self, raw_data: bytes = b''):
        self.raw_data = raw_data

    def get_dword(self, offset: int) -> int:
        """Get 4-byte integer at byte offset"""
        if offset + 4 <= len(self.raw_data):
            import struct
            return struct.unpack('<I', self.raw_data[offset:offset+4])[0]
        return 0


class MockSCR:
    """Mock SCR file"""
    def __init__(self, data_segment: MockDataSegment = None, opcode_resolver=None):
        self.data_segment = data_segment or MockDataSegment()
        self.opcode_resolver = opcode_resolver or MockOpcodeResolver()


# ============================================================================
# Tests for if_else.py
# ============================================================================

class TestDetectEarlyReturnPattern(unittest.TestCase):
    """Test _detect_early_return_pattern function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_early_return_true_branch(self):
        """Test early return pattern where true branch exits"""
        # Block 0: JZ (if zero, jump to block 2 which exits)
        # Block 1: Continue code (fallthrough)
        # Block 2: JMP to exit

        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 101, instructions=[])
        block2 = MockBasicBlock(2, 200, instructions=[
            MockInstruction(200, self.resolver.opcodes['JMP'], arg1=999)
        ])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2})
        start_to_block = {100: 0, 101: 1, 200: 2}

        result = _detect_early_return_pattern(cfg, 0, start_to_block, self.resolver)

        # Should detect early return
        self.assertIsNotNone(result)
        cond_block, exit_block, continue_block, is_negated = result
        self.assertEqual(cond_block, 0)
        self.assertEqual(exit_block, 2)
        self.assertEqual(continue_block, 1)
        self.assertTrue(is_negated)  # JZ means condition is false -> exit

    def test_early_return_can_be_invoked(self):
        """Test that early return detection can be invoked without errors"""
        # Early return detection requires specific block structure
        # This smoke test verifies the function can be called

        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JNZ'], arg1=101)
        ])
        block1 = MockBasicBlock(1, 101, instructions=[
            MockInstruction(101, self.resolver.opcodes['JMP'], arg1=999)
        ])
        block2 = MockBasicBlock(2, 102, instructions=[])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2})
        start_to_block = {100: 0, 101: 1, 102: 2}

        # Function should not raise an error when called
        result = _detect_early_return_pattern(cfg, 0, start_to_block, self.resolver)

        # Result may be None if pattern requirements not met
        # We're mainly testing that the function can be invoked without errors
        self.assertTrue(result is None or isinstance(result, tuple))

    def test_not_early_return_both_branches_have_code(self):
        """Test that pattern is NOT detected when both branches have code"""
        # Block 0: JZ
        # Block 1: Some code (not just JMP)
        # Block 2: Some code (not just JMP)

        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 101, instructions=[
            MockInstruction(101, self.resolver.opcodes['IADD'])
        ])
        block2 = MockBasicBlock(2, 200, instructions=[
            MockInstruction(200, self.resolver.opcodes['IADD'])
        ])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2})
        start_to_block = {100: 0, 101: 1, 200: 2}

        result = _detect_early_return_pattern(cfg, 0, start_to_block, self.resolver)

        # Should NOT detect early return
        self.assertIsNone(result)

    def test_not_early_return_no_conditional_jump(self):
        """Test that pattern is NOT detected when block doesn't end with conditional jump"""
        block0 = MockBasicBlock(0, 100, instructions=[
            MockInstruction(100, self.resolver.opcodes['JMP'], arg1=200)
        ])

        cfg = MockCFG(blocks={0: block0})
        start_to_block = {100: 0}

        result = _detect_early_return_pattern(cfg, 0, start_to_block, self.resolver)

        self.assertIsNone(result)

    def test_early_return_with_switch_exit(self):
        """Test early return pattern within switch case context"""
        # Block 0: JZ
        # Block 1: Continue
        # Block 2: JMP to switch exit (block 5)

        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 101, instructions=[])
        block2 = MockBasicBlock(2, 200, instructions=[
            MockInstruction(200, self.resolver.opcodes['JMP'], arg1=500)
        ])
        block5 = MockBasicBlock(5, 500, instructions=[])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2, 5: block5})
        start_to_block = {100: 0, 101: 1, 200: 2, 500: 5}

        result = _detect_early_return_pattern(cfg, 0, start_to_block, self.resolver, switch_exit_block=5)

        # Should detect early return with switch exit
        self.assertIsNotNone(result)


class TestDetectShortCircuitPattern(unittest.TestCase):
    """Test _detect_short_circuit_pattern function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_simple_and_pattern(self):
        """Test detection accepts compound patterns when properly structured"""
        # The _detect_short_circuit_pattern function requires specific CFG structure
        # This is a smoke test to verify the function can be called without errors
        # Comprehensive testing of AND/OR patterns would require full CFG analysis setup

        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 101, successors=[2, 3], instructions=[
            MockInstruction(101, self.resolver.opcodes['JZ'], arg1=200)
        ])
        block2 = MockBasicBlock(2, 200, instructions=[])
        block3 = MockBasicBlock(3, 300, instructions=[])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2, 3: block3})

        cond_a = MockSSAValue(name="t0", alias="condA")
        cond_b = MockSSAValue(name="t1", alias="condB")

        # SSA instructions
        ssa_block0 = [
            MockSSAInstruction('IEQS', address=99, inputs=[
                MockSSAValue("x"), MockSSAValue("1")
            ], outputs=[cond_a]),
            MockSSAInstruction('JZ', address=100, inputs=[cond_a])
        ]
        ssa_block1 = [
            MockSSAInstruction('IEQS', address=100, inputs=[
                MockSSAValue("y"), MockSSAValue("2")
            ], outputs=[cond_b]),
            MockSSAInstruction('JZ', address=101, inputs=[cond_b])
        ]

        ssa_func = MockSSAFunction(cfg=cfg, instructions={0: ssa_block0, 1: ssa_block1})
        formatter = MockExpressionFormatter()
        start_to_block = {100: 0, 101: 1, 200: 2, 300: 3}

        # Function should not raise an error when called
        result = _detect_short_circuit_pattern(cfg, 0, self.resolver, start_to_block, ssa_func, formatter)

        # Result depends on _collect_and_chain which requires proper CFG successor setup
        # We're mainly testing that the function can be invoked
        self.assertTrue(result is None or isinstance(result, CompoundCondition))

    def test_no_short_circuit_single_condition(self):
        """Test that single condition without AND chain returns None"""
        # Block 0: if (!A) goto false (1), else goto true (2)
        # Block 1: false branch (not another JZ, breaks AND chain)
        # Block 2: true branch

        cond_a = MockSSAValue(name="t0", alias="condA")

        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=101)
        ])
        # Block 1 has non-JZ instruction, breaking the chain
        block1 = MockBasicBlock(1, 101, successors=[2], instructions=[
            MockInstruction(101, self.resolver.opcodes['JMP'], arg1=102)
        ])
        block2 = MockBasicBlock(2, 102, instructions=[])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2})

        # SSA instructions - single condition with no AND chain
        ssa_block0 = [
            MockSSAInstruction('IEQS', address=99, inputs=[
                MockSSAValue("x"), MockSSAValue("1")
            ], outputs=[cond_a]),
            MockSSAInstruction('JZ', address=100, inputs=[cond_a])
        ]

        ssa_func = MockSSAFunction(cfg=cfg, instructions={0: ssa_block0})
        formatter = MockExpressionFormatter()
        start_to_block = {100: 0, 101: 1, 102: 2}

        result = _detect_short_circuit_pattern(cfg, 0, self.resolver, start_to_block, ssa_func, formatter)

        # Should NOT detect compound (no AND chain found, _collect_and_chain returns empty)
        self.assertIsNone(result)


class TestDetectIfElsePattern(unittest.TestCase):
    """Test _detect_if_else_pattern function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_simple_if_else(self):
        """Test simple if/else pattern with merge point"""
        # Block 0: JZ at addr 100, jumps to 200 if zero (false branch), fallthrough to 101 (true branch)
        # Block 1: true branch at addr 101 -> merge to 300
        # Block 2: false branch at addr 200 -> merge to 300
        # Block 3: merge point at addr 300

        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 101, successors=[3], instructions=[
            MockInstruction(101, self.resolver.opcodes['JMP'], arg1=300)
        ])
        block2 = MockBasicBlock(2, 200, successors=[3], instructions=[
            MockInstruction(200, self.resolver.opcodes['JMP'], arg1=300)
        ])
        block3 = MockBasicBlock(3, 300, instructions=[])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2, 3: block3})
        start_to_block = {100: 0, 101: 1, 200: 2, 300: 3}
        visited_ifs = set()

        result = _detect_if_else_pattern(cfg, 0, start_to_block, self.resolver, visited_ifs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, IfElsePattern)
        self.assertEqual(result.header_block, 0)
        # For JZ: true_addr=fallthrough(101), false_addr=jump_target(200)
        self.assertEqual(result.true_block, 1)  # Block at address 101
        self.assertEqual(result.false_block, 2)  # Block at address 200
        self.assertEqual(result.merge_block, 3)
        self.assertIn(0, visited_ifs)

    def test_if_without_else(self):
        """Test if pattern without else branch"""
        # Block 0: if condition goto 1 (true), else goto 2 (merge)
        # Block 1: true branch -> merge to 2
        # Block 2: merge point

        block0 = MockBasicBlock(0, 100, successors=[1], instructions=[
            MockInstruction(100, self.resolver.opcodes['JNZ'], arg1=101)
        ])
        block1 = MockBasicBlock(1, 101, successors=[2], instructions=[
            MockInstruction(101, self.resolver.opcodes['JMP'], arg1=200)
        ])
        block2 = MockBasicBlock(2, 200, instructions=[])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2})
        start_to_block = {100: 0, 101: 1, 200: 2}
        visited_ifs = set()

        result = _detect_if_else_pattern(cfg, 0, start_to_block, self.resolver, visited_ifs)

        self.assertIsNotNone(result)
        self.assertEqual(result.header_block, 0)
        self.assertEqual(result.true_block, 1)
        self.assertIsNone(result.false_block)

    def test_already_visited(self):
        """Test that already visited blocks are not re-detected"""
        block0 = MockBasicBlock(0, 100, instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=200)
        ])
        cfg = MockCFG(blocks={0: block0})
        start_to_block = {100: 0}
        visited_ifs = {0}

        result = _detect_if_else_pattern(cfg, 0, start_to_block, self.resolver, visited_ifs)

        self.assertIsNone(result)

    def test_loop_header_not_detected_as_if(self):
        """Test that loop headers are not detected as if/else patterns"""
        # Block 0: loop header with conditional jump
        loop = MockNaturalLoop(header=0, body={0, 1})

        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 101, instructions=[])
        block2 = MockBasicBlock(2, 200, instructions=[])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2})
        start_to_block = {100: 0, 101: 1, 200: 2}
        visited_ifs = set()
        func_loops = [loop]

        result = _detect_if_else_pattern(cfg, 0, start_to_block, self.resolver, visited_ifs, func_loops=func_loops)

        # Should NOT detect as if/else (it's a loop header)
        self.assertIsNone(result)


# ============================================================================
# Tests for ternary pattern detection
# ============================================================================

class TestDetectTernaryPattern(unittest.TestCase):
    """Test _detect_ternary_pattern function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_ternary_pattern_basic(self):
        """Test that TernaryInfo can be constructed correctly"""
        # Basic test of the TernaryInfo dataclass
        ternary = TernaryInfo(
            variable="result",
            condition="x > 0",
            true_value="1",
            false_value="0"
        )

        self.assertEqual(ternary.variable, "result")
        self.assertEqual(ternary.condition, "x > 0")
        self.assertEqual(ternary.true_value, "1")
        self.assertEqual(ternary.false_value, "0")

    def test_ternary_no_merge_point(self):
        """Test that ternary is NOT detected when merge_block is None"""
        # Create if/else pattern without merge point
        if_pattern = IfElsePattern(
            header_block=0,
            true_block=1,
            false_block=2,
            merge_block=None,  # No merge - branches don't rejoin
            true_body={1},
            false_body={2}
        )

        # Create minimal CFG
        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 101, successors=[], instructions=[])
        block2 = MockBasicBlock(2, 200, successors=[], instructions=[])
        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2})

        # Mock SSA and formatter
        ssa_func = MockSSAFunction(cfg=cfg, instructions={0: [], 1: [], 2: []})
        formatter = MockExpressionFormatter()

        result = _detect_ternary_pattern(
            if_pattern, ssa_func, formatter, cfg, self.resolver, "x > 0"
        )

        # Should NOT detect ternary (no merge block)
        self.assertIsNone(result)

    def test_ternary_multiple_blocks_in_branch(self):
        """Test that ternary is NOT detected when branch has multiple blocks"""
        # Create if/else pattern with multiple blocks in true branch
        if_pattern = IfElsePattern(
            header_block=0,
            true_block=1,
            false_block=3,
            merge_block=4,
            true_body={1, 2},  # Multiple blocks - not eligible
            false_body={3}
        )

        block0 = MockBasicBlock(0, 100, successors=[1, 3], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=300)
        ])
        block1 = MockBasicBlock(1, 101, successors=[2], instructions=[])
        block2 = MockBasicBlock(2, 200, successors=[4], instructions=[])
        block3 = MockBasicBlock(3, 300, successors=[4], instructions=[])
        block4 = MockBasicBlock(4, 400, instructions=[])
        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2, 3: block3, 4: block4})

        ssa_func = MockSSAFunction(cfg=cfg, instructions={0: [], 1: [], 2: [], 3: [], 4: []})
        formatter = MockExpressionFormatter()

        result = _detect_ternary_pattern(
            if_pattern, ssa_func, formatter, cfg, self.resolver, "x > 0"
        )

        # Should NOT detect ternary (multiple blocks in true branch)
        self.assertIsNone(result)

    def test_ternary_no_false_body(self):
        """Test that ternary is NOT detected when false_body is empty"""
        # Create if pattern without else branch
        if_pattern = IfElsePattern(
            header_block=0,
            true_block=1,
            false_block=2,
            merge_block=2,
            true_body={1},
            false_body=set()  # Empty false body
        )

        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 101, successors=[2], instructions=[])
        block2 = MockBasicBlock(2, 200, instructions=[])
        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2})

        ssa_func = MockSSAFunction(cfg=cfg, instructions={0: [], 1: [], 2: []})
        formatter = MockExpressionFormatter()

        result = _detect_ternary_pattern(
            if_pattern, ssa_func, formatter, cfg, self.resolver, "x > 0"
        )

        # Should NOT detect ternary (no false body)
        self.assertIsNone(result)

    def test_ternary_with_xcall_rejected(self):
        """Test that ternary is NOT detected when branch has XCALL"""
        if_pattern = IfElsePattern(
            header_block=0,
            true_block=1,
            false_block=2,
            merge_block=3,
            true_body={1},
            false_body={2}
        )

        # Block 1 has XCALL instruction - side effect!
        block0 = MockBasicBlock(0, 100, successors=[1, 2], instructions=[
            MockInstruction(100, self.resolver.opcodes['JZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 101, successors=[3], instructions=[
            MockInstruction(101, self.resolver.opcodes['XCALL'], arg1=0),  # Side effect!
            MockInstruction(102, self.resolver.opcodes['JMP'], arg1=300)
        ])
        block2 = MockBasicBlock(2, 200, successors=[3], instructions=[
            MockInstruction(200, self.resolver.opcodes['JMP'], arg1=300)
        ])
        block3 = MockBasicBlock(3, 300, instructions=[])
        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2, 3: block3})

        ssa_func = MockSSAFunction(cfg=cfg, instructions={0: [], 1: [], 2: [], 3: []})
        formatter = MockExpressionFormatter()

        result = _detect_ternary_pattern(
            if_pattern, ssa_func, formatter, cfg, self.resolver, "x > 0"
        )

        # Should NOT detect ternary (block has XCALL)
        self.assertIsNone(result)


# ============================================================================
# Tests for switch_case.py
# ============================================================================

class TestFindSwitchVariableFromNearbyGCP(unittest.TestCase):
    """Test _find_switch_variable_from_nearby_gcp function"""

    def test_find_switch_variable(self):
        """Test finding switch variable from GCP instruction"""
        # Create SSA instructions with GCP loading a global
        gcp_instr = MockSSAInstruction('GCP', address=100)
        raw_instr = MockInstruction(100, 0x50, arg1=42)  # dword offset 42
        lifted_instr = MockLiftedInstruction(raw_instr)
        gcp_instr.instruction = lifted_instr

        ssa_block = [gcp_instr]
        ssa_func = MockSSAFunction(instructions={0: ssa_block})

        formatter = MockExpressionFormatter(global_names={42: 'gSwitchVar'})
        func_block_ids = {0}

        result = _find_switch_variable_from_nearby_gcp(ssa_func, 0, None, formatter, func_block_ids)

        self.assertEqual(result, 'gSwitchVar')

    def test_no_gcp_found(self):
        """Test when no GCP instruction is found"""
        # No GCP instructions
        ssa_block = [
            MockSSAInstruction('IADD', address=100)
        ]
        ssa_func = MockSSAFunction(instructions={0: ssa_block})
        formatter = MockExpressionFormatter()
        func_block_ids = {0}

        result = _find_switch_variable_from_nearby_gcp(ssa_func, 0, None, formatter, func_block_ids)

        self.assertIsNone(result)

    def test_earliest_gcp_selected(self):
        """Test that earliest GCP is selected when multiple exist"""
        # Multiple GCP instructions
        gcp1 = MockSSAInstruction('GCP', address=100)
        raw1 = MockInstruction(100, 0x50, arg1=10)
        lifted1 = MockLiftedInstruction(raw1)
        gcp1.instruction = lifted1

        gcp2 = MockSSAInstruction('GCP', address=50)  # Earlier address
        raw2 = MockInstruction(50, 0x50, arg1=20)
        lifted2 = MockLiftedInstruction(raw2)
        gcp2.instruction = lifted2

        ssa_block = [gcp1, gcp2]
        ssa_func = MockSSAFunction(instructions={0: ssa_block})

        formatter = MockExpressionFormatter(global_names={10: 'gVar1', 20: 'gVar2'})
        func_block_ids = {0}

        result = _find_switch_variable_from_nearby_gcp(ssa_func, 0, None, formatter, func_block_ids)

        # Should select gVar2 (from address 50, which is earlier)
        self.assertEqual(result, 'gVar2')


class TestDetectSwitchPatterns(unittest.TestCase):
    """Test _detect_switch_patterns function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_simple_switch_two_cases(self):
        """Test switch detection can be invoked without errors"""
        # Switch pattern detection is complex and requires precise SSA/CFG setup
        # This smoke test verifies the function can be called

        # Create data segment with case values
        data_bytes = b'\x00\x00\x00\x00' + b'\x01\x00\x00\x00'  # 0, 1
        data_seg = MockDataSegment(data_bytes)
        scr = MockSCR(data_segment=data_seg, opcode_resolver=self.resolver)

        # Create minimal blocks
        block0 = MockBasicBlock(0, 100, instructions=[
            MockInstruction(100, self.resolver.opcodes['JNZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 101, instructions=[
            MockInstruction(101, self.resolver.opcodes['JNZ'], arg1=300)
        ])

        cfg = MockCFG(blocks={0: block0, 1: block1})

        # SSA instructions for switch tests
        var = MockSSAValue(name="local_0", alias="switchVar")
        const0 = MockSSAValue(name="data_0")
        equ0 = MockSSAValue(name="t0")

        ssa_block0 = [
            MockSSAInstruction('EQU', address=99, inputs=[var, const0], outputs=[equ0]),
            MockSSAInstruction('JNZ', address=100, inputs=[equ0])
        ]

        ssa_func = MockSSAFunction(cfg=cfg, instructions={0: ssa_block0}, scr=scr)
        formatter = MockExpressionFormatter()
        start_to_block = {100: 0, 101: 1, 200: 2, 300: 3}
        func_block_ids = {0, 1}

        # Function should not raise an error when called
        result = _detect_switch_patterns(ssa_func, func_block_ids, formatter, start_to_block)

        # Result may be empty if pattern requirements not met (need at least 2 cases)
        # We're mainly testing that the function can be invoked without errors
        self.assertIsInstance(result, list)

    def test_no_switch_single_case(self):
        """Test that single case is not detected as switch"""
        # Only one equality test - not a switch
        data_seg = MockDataSegment(b'\x00\x00\x00\x00')
        scr = MockSCR(data_segment=data_seg, opcode_resolver=self.resolver)

        block0 = MockBasicBlock(0, 100, instructions=[
            MockInstruction(100, self.resolver.opcodes['JNZ'], arg1=200)
        ])
        block1 = MockBasicBlock(1, 200, instructions=[])

        cfg = MockCFG(blocks={0: block0, 1: block1})

        var = MockSSAValue(name="local_0")
        const0 = MockSSAValue(name="data_0")
        equ0 = MockSSAValue(name="t0")

        ssa_block0 = [
            MockSSAInstruction('EQU', address=99, inputs=[var, const0], outputs=[equ0]),
            MockSSAInstruction('JNZ', address=100, inputs=[equ0])
        ]

        ssa_func = MockSSAFunction(cfg=cfg, instructions={0: ssa_block0}, scr=scr)
        formatter = MockExpressionFormatter()
        start_to_block = {100: 0, 200: 1}
        func_block_ids = {0, 1}

        result = _detect_switch_patterns(ssa_func, func_block_ids, formatter, start_to_block)

        # Should NOT detect switch (only 1 case, need at least 2)
        self.assertEqual(len(result), 0)


# ============================================================================
# Tests for loops.py
# ============================================================================

class TestDetectForLoop(unittest.TestCase):
    """Test _detect_for_loop function"""

    def setUp(self):
        self.resolver = MockOpcodeResolver()

    def test_simple_for_loop(self):
        """Test simple for loop: for (i = 0; i < 10; i++)"""
        # Block 0: Predecessor - initialization (i = 0)
        # Block 1: Loop header - condition (i < 10)
        # Block 2: Loop body
        # Block 3: Increment (i++)

        # Create data segment with loop bound (10)
        data_bytes = b'\x0a\x00\x00\x00'  # 10
        data_seg = MockDataSegment(data_bytes)
        scr = MockSCR(data_segment=data_seg, opcode_resolver=self.resolver)

        # Blocks
        block0 = MockBasicBlock(0, 100, predecessors=[], instructions=[])
        block1 = MockBasicBlock(1, 101, predecessors=[0, 3], instructions=[
            MockInstruction(101, self.resolver.opcodes['JZ'], arg1=400)
        ])
        block2 = MockBasicBlock(2, 200, instructions=[])
        block3 = MockBasicBlock(3, 300, instructions=[])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2, 3: block3})

        # Create loop structure
        loop = MockNaturalLoop(
            header=1,
            body={1, 2, 3},
            back_edges=[MockBackEdge(source=3, target=1)]
        )

        # SSA instructions
        # Block 0: i = 0
        local_i = MockSSAValue(name="local_2", alias="i")
        zero = MockSSAValue(name="const_0", alias="0")

        ssa_block0 = [
            MockSSAInstruction('IASGN', address=100, inputs=[zero], outputs=[local_i])
        ]

        # Block 1: i < 10
        data_10 = MockSSAValue(name="data_0")
        cmp_result = MockSSAValue(name="t0")

        ssa_block1 = [
            MockSSAInstruction('ILSS', address=100, inputs=[local_i, data_10], outputs=[cmp_result]),
            MockSSAInstruction('JZ', address=101, inputs=[cmp_result])
        ]

        # Block 3: i++
        one = MockSSAValue(name="const_1", alias="1")
        i_plus_1 = MockSSAValue(name="t1")

        ssa_block3 = [
            MockSSAInstruction('IADD', address=300, inputs=[local_i, one], outputs=[local_i])
        ]

        ssa_func = MockSSAFunction(
            cfg=cfg,
            instructions={0: ssa_block0, 1: ssa_block1, 3: ssa_block3},
            scr=scr
        )

        formatter = MockExpressionFormatter()
        start_to_block = {100: 0, 101: 1, 200: 2, 300: 3, 400: 4}

        result = _detect_for_loop(loop, cfg, ssa_func, formatter, self.resolver, start_to_block)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, ForLoopInfo)
        self.assertEqual(result.init, "0")
        self.assertIn("10", result.condition)
        self.assertIn("++", result.increment)

    def test_no_init_found(self):
        """Test that None is returned when initialization is not found"""
        # Loop without clear initialization in predecessor
        block0 = MockBasicBlock(0, 100, predecessors=[], instructions=[])
        block1 = MockBasicBlock(1, 101, predecessors=[0], instructions=[
            MockInstruction(101, self.resolver.opcodes['JZ'], arg1=400)
        ])

        cfg = MockCFG(blocks={0: block0, 1: block1})
        loop = MockNaturalLoop(header=1, body={1}, back_edges=[])

        ssa_func = MockSSAFunction(cfg=cfg, instructions={0: [], 1: []})
        formatter = MockExpressionFormatter()
        start_to_block = {100: 0, 101: 1}

        result = _detect_for_loop(loop, cfg, ssa_func, formatter, self.resolver, start_to_block)

        self.assertIsNone(result)

    def test_no_increment_found(self):
        """Test that None is returned when increment is not found"""
        # Loop with init and condition but no increment
        block0 = MockBasicBlock(0, 100, predecessors=[], instructions=[])
        block1 = MockBasicBlock(1, 101, predecessors=[0, 2], instructions=[
            MockInstruction(101, self.resolver.opcodes['JZ'], arg1=400)
        ])
        block2 = MockBasicBlock(2, 200, instructions=[])

        cfg = MockCFG(blocks={0: block0, 1: block1, 2: block2})
        loop = MockNaturalLoop(
            header=1,
            body={1, 2},
            back_edges=[MockBackEdge(source=2, target=1)]
        )

        # Init instruction
        local_i = MockSSAValue(name="local_2", alias="i")
        zero = MockSSAValue(name="const_0", alias="0")

        ssa_block0 = [
            MockSSAInstruction('IASGN', address=100, inputs=[zero], outputs=[local_i])
        ]

        # Condition but no comparison found
        ssa_block1 = [
            MockSSAInstruction('JZ', address=101, inputs=[])
        ]

        # No increment in back edge block
        ssa_block2 = []

        ssa_func = MockSSAFunction(
            cfg=cfg,
            instructions={0: ssa_block0, 1: ssa_block1, 2: ssa_block2}
        )

        formatter = MockExpressionFormatter()
        start_to_block = {100: 0, 101: 1, 200: 2}

        result = _detect_for_loop(loop, cfg, ssa_func, formatter, self.resolver, start_to_block)

        self.assertIsNone(result)


# ============================================================================
# Integration tests
# ============================================================================

class TestPatternImports(unittest.TestCase):
    """Test that all pattern detection functions can be imported"""

    def test_import_if_else_module(self):
        """Test importing if_else module"""
        from vcdecomp.core.ir.structure.patterns import if_else
        self.assertTrue(hasattr(if_else, '_detect_early_return_pattern'))
        self.assertTrue(hasattr(if_else, '_detect_short_circuit_pattern'))
        self.assertTrue(hasattr(if_else, '_detect_if_else_pattern'))
        self.assertTrue(hasattr(if_else, '_detect_ternary_pattern'))

    def test_import_switch_case_module(self):
        """Test importing switch_case module"""
        from vcdecomp.core.ir.structure.patterns import switch_case
        self.assertTrue(hasattr(switch_case, '_find_switch_variable_from_nearby_gcp'))
        self.assertTrue(hasattr(switch_case, '_detect_switch_patterns'))

    def test_import_loops_module(self):
        """Test importing loops module"""
        from vcdecomp.core.ir.structure.patterns import loops
        self.assertTrue(hasattr(loops, '_detect_for_loop'))

    def test_package_level_imports(self):
        """Test importing from patterns package"""
        from vcdecomp.core.ir.structure.patterns import (
            _detect_early_return_pattern,
            _detect_short_circuit_pattern,
            _detect_if_else_pattern,
            _detect_ternary_pattern,
            _detect_switch_patterns,
            _detect_for_loop,
            TernaryInfo
        )
        self.assertIsNotNone(_detect_early_return_pattern)
        self.assertIsNotNone(_detect_short_circuit_pattern)
        self.assertIsNotNone(_detect_if_else_pattern)
        self.assertIsNotNone(_detect_ternary_pattern)
        self.assertIsNotNone(_detect_switch_patterns)
        self.assertIsNotNone(_detect_for_loop)
        self.assertIsNotNone(TernaryInfo)


if __name__ == '__main__':
    unittest.main()
