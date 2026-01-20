"""
Unit tests for structure code emission modules.

Tests the newly extracted code emission functions from the structure.py refactoring:
- block_formatter.py: Block formatting and filtering functions
- code_emitter.py: Recursive code rendering for if/else and loops
"""

import unittest
from typing import Dict, List, Set, Optional
from dataclasses import dataclass

# Import emission modules
from vcdecomp.core.ir.structure.emit.block_formatter import (
    _format_block_lines,
    _format_block_lines_filtered
)

from vcdecomp.core.ir.structure.emit.code_emitter import (
    _render_if_else_recursive,
    _render_blocks_with_loops
)

from vcdecomp.core.ir.structure.patterns.models import (
    IfElsePattern,
    CompoundCondition,
    ForLoopInfo
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
                 instruction=None, block_id: int = 0, outputs: List = None):
        self.mnemonic = mnemonic
        self.address = address
        self.inputs = inputs or []
        self.instruction = instruction
        self.block_id = block_id
        self.outputs = outputs or []


class MockSSAValue:
    """Mock SSA value"""
    def __init__(self, name: str = "t0", alias: str = None, value_type=None,
                 producer_inst=None):
        self.name = name
        self.alias = alias
        self.value_type = value_type
        self.producer_inst = producer_inst


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
    def __init__(self, header: int, body: Set[int], back_edges: List = None):
        self.header = header
        self.body = body
        self.back_edges = back_edges or []


class MockBackEdge:
    """Mock back edge for loops"""
    def __init__(self, source: int, target: int):
        self.source = source
        self.target = target


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
        self.LLD = 0x30
        self.ASGN = 0x40

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
            self.XCALL: "XCALL",
            self.LLD: "LLD",
            self.ASGN: "ASGN"
        }
        return mnemonics.get(opcode, "UNKNOWN")


class MockSSAFunction:
    """Mock SSA function"""
    def __init__(self, instructions: Dict[int, List[MockSSAInstruction]] = None):
        self.instructions = instructions or {}


@dataclass
class MockExpression:
    """Mock expression with text"""
    text: str


class MockExpressionFormatter:
    """Mock expression formatter"""
    def __init__(self, expressions: Dict[int, List[MockExpression]] = None,
                 render_values: Dict[str, str] = None):
        self.expressions = expressions or {}
        self.render_values = render_values or {}
        self._struct_ranges = {}

    def render_value(self, value, context=None):
        """Mock render_value"""
        if hasattr(value, 'name') and value.name in self.render_values:
            return self.render_values[value.name]
        if hasattr(value, 'alias') and value.alias:
            return value.alias
        if hasattr(value, 'name'):
            return value.name
        return str(value)

    def _format_call(self, inst):
        """Mock _format_call"""
        return f"SC_Function();"


class MockDataSegment:
    """Mock data segment for reading constant values"""
    def __init__(self, data: bytes = None):
        self.data = data or b'\x00' * 1024

    def read_dword(self, offset: int) -> int:
        """Read a DWORD (4 bytes) from data segment"""
        byte_offset = offset * 4
        if byte_offset + 4 <= len(self.data):
            return int.from_bytes(self.data[byte_offset:byte_offset+4], 'little')
        return 0


class MockSCR:
    """Mock SCR file representation"""
    def __init__(self, data_segment: MockDataSegment = None):
        self.data_segment = data_segment or MockDataSegment()


def mock_format_block_expressions(ssa_func, block_id, formatter=None):
    """Mock implementation of format_block_expressions"""
    if formatter and hasattr(formatter, 'expressions') and block_id in formatter.expressions:
        return formatter.expressions[block_id]
    return []


# Patch format_block_expressions to use our mock
import vcdecomp.core.ir.structure.emit.block_formatter as block_formatter_module
original_format_block_expressions = block_formatter_module.format_block_expressions
block_formatter_module.format_block_expressions = mock_format_block_expressions


# ============================================================================
# Test Cases
# ============================================================================

class TestFormatBlockLinesFiltered(unittest.TestCase):
    """Test _format_block_lines_filtered function"""

    def test_filter_simple_assignment(self):
        """Test filtering last assignment to variable"""
        # Create mock data
        ssa_func = MockSSAFunction()
        formatter = MockExpressionFormatter(
            expressions={
                1: [
                    MockExpression("int x = 0;"),
                    MockExpression("int y = 5;"),
                    MockExpression("i = 0;"),  # This should be filtered
                ]
            }
        )

        # Call function
        result = _format_block_lines_filtered(
            ssa_func, 1, "    ", formatter, "i"
        )

        # Verify: Should have 2 lines (third filtered)
        self.assertEqual(len(result), 2)
        self.assertIn("int x = 0;", result[0])
        self.assertIn("int y = 5;", result[1])

    def test_filter_increment(self):
        """Test filtering increment expression"""
        formatter = MockExpressionFormatter(
            expressions={
                1: [
                    MockExpression("x = x + 1;"),
                    MockExpression("i++;"),  # This should be filtered
                ]
            }
        )

        result = _format_block_lines_filtered(
            MockSSAFunction(), 1, "", formatter, "i"
        )

        self.assertEqual(len(result), 1)
        self.assertIn("x = x + 1;", result[0])

    def test_no_matching_variable(self):
        """Test when skip variable not found"""
        formatter = MockExpressionFormatter(
            expressions={
                1: [
                    MockExpression("x = 1;"),
                    MockExpression("y = 2;"),
                ]
            }
        )

        result = _format_block_lines_filtered(
            MockSSAFunction(), 1, "", formatter, "z"
        )

        # Should keep all expressions
        self.assertEqual(len(result), 2)

    def test_empty_block(self):
        """Test filtering on empty block"""
        formatter = MockExpressionFormatter(expressions={1: []})

        result = _format_block_lines_filtered(
            MockSSAFunction(), 1, "", formatter, "i"
        )

        self.assertEqual(len(result), 0)


class TestFormatBlockLines(unittest.TestCase):
    """Test _format_block_lines function"""

    def test_basic_block_formatting(self):
        """Test basic block formatting without recursion"""
        formatter = MockExpressionFormatter(
            expressions={
                1: [
                    MockExpression("int x = 0;"),
                    MockExpression("return x;"),
                ]
            }
        )

        result = _format_block_lines(
            MockSSAFunction(), 1, "    ", formatter
        )

        self.assertEqual(len(result), 2)
        self.assertIn("int x = 0;", result[0])
        self.assertIn("return x;", result[1])

    def test_skip_already_emitted_block(self):
        """Test that already emitted blocks are skipped"""
        formatter = MockExpressionFormatter(
            expressions={1: [MockExpression("x = 1;")]}
        )
        emitted_blocks = {1}

        result = _format_block_lines(
            MockSSAFunction(), 1, "", formatter,
            emitted_blocks=emitted_blocks
        )

        # Should return empty list (already emitted)
        self.assertEqual(len(result), 0)

    def test_early_return_pattern(self):
        """Test early return pattern rendering"""
        # Create basic blocks
        blocks = {
            1: MockBasicBlock(1, 0x100, [2, 3], [
                MockInstruction(0x100, 0x02)  # JZ instruction
            ])
        }
        cfg = MockCFG(blocks)

        # Create SSA instruction for conditional
        cond_value = MockSSAValue("t0", alias="condition")
        ssa_inst = MockSSAInstruction("JZ", 0x100, [cond_value])
        ssa_func = MockSSAFunction({1: [ssa_inst]})

        formatter = MockExpressionFormatter(
            expressions={1: [MockExpression("x = 1;"), MockExpression("if (condition) goto L2;")]},
            render_values={"t0": "condition"}
        )

        resolver = MockOpcodeResolver()
        early_returns = {1: (1, 2, 3, False)}  # header, exit, continue, is_negated
        emitted_blocks = set()

        result = _format_block_lines(
            ssa_func, 1, "", formatter,
            cfg=cfg, resolver=resolver,
            early_returns=early_returns,
            emitted_blocks=emitted_blocks
        )

        # Should render as "if (condition) break;"
        self.assertTrue(any("if (condition) break;" in line for line in result))

    def test_indentation(self):
        """Test that indentation is applied correctly"""
        formatter = MockExpressionFormatter(
            expressions={1: [MockExpression("x = 1;")]}
        )

        result = _format_block_lines(
            MockSSAFunction(), 1, "        ", formatter
        )

        # Check indentation
        self.assertTrue(result[0].startswith("        "))


class TestRenderIfElseRecursive(unittest.TestCase):
    """Test _render_if_else_recursive function"""

    def test_simple_if_else(self):
        """Test simple if/else rendering"""
        # Create blocks
        blocks = {
            1: MockBasicBlock(1, 0x100, [2, 3], [
                MockInstruction(0x100, 0x02)  # JZ
            ]),
            2: MockBasicBlock(2, 0x110, [4]),
            3: MockBasicBlock(3, 0x120, [4]),
            4: MockBasicBlock(4, 0x130, [])
        }
        cfg = MockCFG(blocks)

        # Create if/else pattern
        if_pattern = IfElsePattern(
            header_block=1,
            true_block=2,
            false_block=3,
            merge_block=4,
            true_body={2},
            false_body={3}
        )

        # Create SSA
        cond_value = MockSSAValue("t0", alias="x")
        ssa_inst = MockSSAInstruction("JZ", 0x100, [cond_value])
        ssa_func = MockSSAFunction({
            1: [ssa_inst],
            2: [],
            3: []
        })

        formatter = MockExpressionFormatter(
            expressions={
                1: [],
                2: [MockExpression("y = 1;")],
                3: [MockExpression("y = 2;")]
            },
            render_values={"t0": "x"}
        )

        resolver = MockOpcodeResolver()
        visited_ifs = set()
        emitted_blocks = set()
        block_to_if = {1: if_pattern}
        start_to_block = {}

        result = _render_if_else_recursive(
            if_pattern, "", ssa_func, formatter,
            block_to_if, visited_ifs, emitted_blocks,
            cfg, start_to_block, resolver
        )

        # Verify structure
        self.assertTrue(any("if (x)" in line for line in result))
        self.assertTrue(any("} else {" in line for line in result))
        self.assertTrue(any("y = 1;" in line for line in result))
        self.assertTrue(any("y = 2;" in line for line in result))

    def test_if_without_else(self):
        """Test if without else branch"""
        blocks = {
            1: MockBasicBlock(1, 0x100, [2, 3], [
                MockInstruction(0x100, 0x02)  # JZ
            ]),
            2: MockBasicBlock(2, 0x110, [3]),
            3: MockBasicBlock(3, 0x120, [])
        }
        cfg = MockCFG(blocks)

        if_pattern = IfElsePattern(
            header_block=1,
            true_block=2,
            false_block=3,
            merge_block=3,
            true_body={2},
            false_body=set()  # No else
        )

        cond_value = MockSSAValue("t0", alias="condition")
        ssa_inst = MockSSAInstruction("JZ", 0x100, [cond_value])
        ssa_func = MockSSAFunction({1: [ssa_inst], 2: []})

        formatter = MockExpressionFormatter(
            expressions={1: [], 2: [MockExpression("x = 1;")]},
            render_values={"t0": "condition"}
        )

        resolver = MockOpcodeResolver()
        result = _render_if_else_recursive(
            if_pattern, "", ssa_func, formatter,
            {1: if_pattern}, set(), set(),
            cfg, {}, resolver
        )

        # Should have if but no else
        self.assertTrue(any("if (condition)" in line for line in result))
        self.assertFalse(any("} else {" in line for line in result))

    def test_compound_condition(self):
        """Test compound condition rendering"""
        blocks = {
            1: MockBasicBlock(1, 0x100, [2, 3], [
                MockInstruction(0x100, 0x02)  # JZ
            ]),
            2: MockBasicBlock(2, 0x110, []),
            3: MockBasicBlock(3, 0x120, [])
        }
        cfg = MockCFG(blocks)

        # Create compound condition
        compound = CompoundCondition(
            operator="&&",
            conditions=["x > 0", "y < 10"],
            involved_blocks={1},
            true_target=2,
            false_target=3
        )

        if_pattern = IfElsePattern(
            header_block=1,
            true_block=2,
            false_block=3,
            merge_block=None,
            true_body={2},
            false_body={3}
        )
        if_pattern.compound = compound

        ssa_func = MockSSAFunction({1: [], 2: [], 3: []})
        formatter = MockExpressionFormatter(expressions={1: [], 2: [], 3: []})
        resolver = MockOpcodeResolver()

        result = _render_if_else_recursive(
            if_pattern, "", ssa_func, formatter,
            {1: if_pattern}, set(), set(),
            cfg, {}, resolver
        )

        # Should have compound condition
        result_text = '\n'.join(result)
        self.assertIn("x > 0", result_text)
        self.assertIn("y < 10", result_text)


class TestRenderBlocksWithLoops(unittest.TestCase):
    """Test _render_blocks_with_loops function"""

    def test_simple_block_sequence(self):
        """Test rendering simple block sequence without loops"""
        blocks = {
            1: MockBasicBlock(1, 0x100, [2]),
            2: MockBasicBlock(2, 0x110, [3]),
            3: MockBasicBlock(3, 0x120, [])
        }
        cfg = MockCFG(blocks)

        ssa_func = MockSSAFunction({1: [], 2: [], 3: []})
        formatter = MockExpressionFormatter(
            expressions={
                1: [MockExpression("x = 1;")],
                2: [MockExpression("y = 2;")],
                3: [MockExpression("return;")]
            }
        )

        resolver = MockOpcodeResolver()
        result = _render_blocks_with_loops(
            [1, 2, 3], "", ssa_func, formatter,
            cfg, [], {}, resolver, {}, set(), set()
        )

        # Should render all blocks
        result_text = '\n'.join(result)
        self.assertIn("x = 1;", result_text)
        self.assertIn("y = 2;", result_text)
        self.assertIn("return;", result_text)

    def test_while_loop(self):
        """Test rendering while loop"""
        blocks = {
            1: MockBasicBlock(1, 0x100, [2, 3]),  # Loop header
            2: MockBasicBlock(2, 0x110, [1]),     # Loop body -> back to header
            3: MockBasicBlock(3, 0x120, [])       # Exit
        }
        cfg = MockCFG(blocks)

        loop = MockNaturalLoop(header=1, body={1, 2})
        ssa_func = MockSSAFunction({1: [], 2: []})
        formatter = MockExpressionFormatter(
            expressions={
                1: [],
                2: [MockExpression("x++;")]
            }
        )

        resolver = MockOpcodeResolver()
        result = _render_blocks_with_loops(
            [1], "", ssa_func, formatter,
            cfg, [loop], {}, resolver, {}, set(), set()
        )

        # Should have while loop
        result_text = '\n'.join(result)
        self.assertIn("while (TRUE)", result_text)
        self.assertIn("x++;", result_text)

    def test_skip_already_emitted(self):
        """Test that already emitted blocks are skipped"""
        blocks = {
            1: MockBasicBlock(1, 0x100, []),
            2: MockBasicBlock(2, 0x110, [])
        }
        cfg = MockCFG(blocks)

        ssa_func = MockSSAFunction({1: [], 2: []})
        formatter = MockExpressionFormatter(
            expressions={
                1: [MockExpression("x = 1;")],
                2: [MockExpression("y = 2;")]
            }
        )

        emitted_blocks = {1}  # Block 1 already emitted
        resolver = MockOpcodeResolver()

        result = _render_blocks_with_loops(
            [1, 2], "", ssa_func, formatter,
            cfg, [], {}, resolver, {}, set(), emitted_blocks
        )

        # Should only have block 2
        result_text = '\n'.join(result)
        self.assertNotIn("x = 1;", result_text)
        self.assertIn("y = 2;", result_text)

    def test_return_stops_rendering(self):
        """Test that return statement stops rendering remaining blocks"""
        blocks = {
            1: MockBasicBlock(1, 0x100, [2], [
                MockInstruction(0x100, 0x10)  # RET
            ]),
            2: MockBasicBlock(2, 0x110, [])
        }
        cfg = MockCFG(blocks)

        ssa_func = MockSSAFunction({1: [], 2: []})
        formatter = MockExpressionFormatter(
            expressions={
                1: [MockExpression("return 0;")],
                2: [MockExpression("unreachable;")]
            }
        )

        resolver = MockOpcodeResolver()
        result = _render_blocks_with_loops(
            [1, 2], "", ssa_func, formatter,
            cfg, [], {}, resolver, {}, set(), set()
        )

        # Should stop after return
        result_text = '\n'.join(result)
        self.assertIn("return 0;", result_text)
        self.assertNotIn("unreachable;", result_text)


class TestEmitImports(unittest.TestCase):
    """Test that all emit modules import correctly"""

    def test_import_block_formatter(self):
        """Test block_formatter module imports"""
        from vcdecomp.core.ir.structure.emit import (
            _format_block_lines,
            _format_block_lines_filtered
        )
        self.assertIsNotNone(_format_block_lines)
        self.assertIsNotNone(_format_block_lines_filtered)

    def test_import_code_emitter(self):
        """Test code_emitter module imports"""
        from vcdecomp.core.ir.structure.emit import (
            _render_if_else_recursive,
            _render_blocks_with_loops
        )
        self.assertIsNotNone(_render_if_else_recursive)
        self.assertIsNotNone(_render_blocks_with_loops)

    def test_package_level_imports(self):
        """Test package-level imports work"""
        from vcdecomp.core.ir.structure.emit import (
            _format_block_lines,
            _format_block_lines_filtered,
            _render_if_else_recursive,
            _render_blocks_with_loops
        )
        # All should be imported successfully
        self.assertTrue(callable(_format_block_lines))
        self.assertTrue(callable(_format_block_lines_filtered))
        self.assertTrue(callable(_render_if_else_recursive))
        self.assertTrue(callable(_render_blocks_with_loops))


# ============================================================================
# Test Suite
# ============================================================================

def suite():
    """Create test suite"""
    test_suite = unittest.TestSuite()

    # Block formatter tests
    test_suite.addTest(unittest.makeSuite(TestFormatBlockLinesFiltered))
    test_suite.addTest(unittest.makeSuite(TestFormatBlockLines))

    # Code emitter tests
    test_suite.addTest(unittest.makeSuite(TestRenderIfElseRecursive))
    test_suite.addTest(unittest.makeSuite(TestRenderBlocksWithLoops))

    # Import tests
    test_suite.addTest(unittest.makeSuite(TestEmitImports))

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
