"""
Tests for for-loop detection using SSA analysis.

Tests the PHI node-based for-loop detection algorithm.
"""

import pytest
from vcdecomp.core.ir.ssa import SSAValue, SSAInstruction, SSAFunction
from vcdecomp.core.ir.cfg import CFG
from vcdecomp.core.ir.structure.blocks.hierarchy import BlockWhileDo, BlockBasic, BlockType
from vcdecomp.core.ir.structure.analysis.for_loop_detection import (
    ForLoopDetector,
    ForLoopPattern,
)
from vcdecomp.core.disasm import opcodes


class TestForLoopDetection:
    """Test for-loop detection with SSA analysis."""

    def test_basic_for_loop_pattern(self):
        """
        Test detection of basic for loop pattern.

        Pattern:
            i = 0;           // init
            while (i < 10) { // condition
                ...          // body
                i++;         // increment
            }
        """
        # Create minimal SSA function with PHI node
        cfg = CFG()

        # Create values
        init_val = SSAValue(
            name="const_0",
            value_type=opcodes.ResultType.INT,
            producer=None,
            metadata={'constant': 0}
        )

        loop_var_phi = SSAValue(
            name="t100_0",
            value_type=opcodes.ResultType.INT,
            producer=-1,  # PHI address
            phi_sources=[(0, "const_0"), (2, "t100_1")],  # (pred_block, value_name)
            alias="i"
        )

        iter_val = SSAValue(
            name="t100_1",
            value_type=opcodes.ResultType.INT,
            producer=100,  # Iterator instruction address
            alias="i"
        )

        values = {
            "const_0": init_val,
            "t100_0": loop_var_phi,
            "t100_1": iter_val,
        }

        # Create instructions
        # Block 0: Initialization (before loop)
        init_inst = SSAInstruction(
            block_id=0,
            mnemonic="PUSH",
            address=0,
            inputs=[],
            outputs=[init_val],
        )
        init_val.producer_inst = init_inst

        # Block 1: Loop header with PHI
        phi_inst = SSAInstruction(
            block_id=1,
            mnemonic="PHI",
            address=-1,
            inputs=[init_val, iter_val],
            outputs=[loop_var_phi],
        )
        loop_var_phi.producer_inst = phi_inst

        # Block 2: Loop tail with iterator
        iter_inst = SSAInstruction(
            block_id=2,
            mnemonic="IADD",
            address=100,
            inputs=[loop_var_phi, init_val],  # i + 1
            outputs=[iter_val],
        )
        iter_val.producer_inst = iter_inst

        instructions = {
            0: [init_inst],
            1: [phi_inst],
            2: [iter_inst],
        }

        ssa_func = SSAFunction(
            cfg=cfg,
            values=values,
            instructions=instructions,
            scr=None
        )

        # Create while loop block structure
        header = BlockBasic(block_id=1, original_block_id=1)
        body = BlockBasic(block_id=2, original_block_id=2)
        body.covered_blocks = {2}

        while_block = BlockWhileDo(
            block_type=BlockType.WHILE_DO,
            block_id=10,
            condition_block=header,
            body_block=body,
        )

        # Run detection
        detector = ForLoopDetector(ssa_func)
        pattern = detector.detect_for_loop(while_block)

        # Verify pattern detected
        assert pattern is not None
        assert pattern.loop_variable == "t100_0"
        assert "0" in pattern.initializer or "const_0" in pattern.initializer
        assert "++" in pattern.iterator or "IADD" in pattern.iterator

    def test_no_phi_node(self):
        """Test that no pattern is detected without PHI nodes."""
        cfg = CFG()
        values = {}
        instructions = {
            1: [],  # Empty header
        }

        ssa_func = SSAFunction(
            cfg=cfg,
            values=values,
            instructions=instructions,
            scr=None
        )

        header = BlockBasic(block_id=1, original_block_id=1)
        body = BlockBasic(block_id=2, original_block_id=2)

        while_block = BlockWhileDo(
            block_type=BlockType.WHILE_DO,
            block_id=10,
            condition_block=header,
            body_block=body,
        )

        detector = ForLoopDetector(ssa_func)
        pattern = detector.detect_for_loop(while_block)

        # No PHI node, so no pattern
        assert pattern is None

    def test_phi_without_loop_structure(self):
        """Test that PHI node without proper loop structure is not detected."""
        cfg = CFG()

        # PHI node with wrong number of inputs
        loop_var_phi = SSAValue(
            name="t100_0",
            value_type=opcodes.ResultType.INT,
            producer=-1,
            phi_sources=[(0, "const_0")],  # Only one source - invalid
        )

        values = {"t100_0": loop_var_phi}

        phi_inst = SSAInstruction(
            block_id=1,
            mnemonic="PHI",
            address=-1,
            inputs=[],
            outputs=[loop_var_phi],
        )

        instructions = {1: [phi_inst]}

        ssa_func = SSAFunction(
            cfg=cfg,
            values=values,
            instructions=instructions,
            scr=None
        )

        header = BlockBasic(block_id=1, original_block_id=1)
        body = BlockBasic(block_id=2, original_block_id=2)

        while_block = BlockWhileDo(
            block_type=BlockType.WHILE_DO,
            block_id=10,
            condition_block=header,
            body_block=body,
        )

        detector = ForLoopDetector(ssa_func)
        pattern = detector.detect_for_loop(while_block)

        # Invalid PHI structure
        assert pattern is None

    def test_increment_formatting(self):
        """Test that different increment patterns are formatted correctly."""
        cfg = CFG()

        const_1 = SSAValue(
            name="const_1",
            value_type=opcodes.ResultType.INT,
            metadata={'constant': 1}
        )

        loop_var = SSAValue(
            name="t100_0",
            value_type=opcodes.ResultType.INT,
            alias="i"
        )

        # Test INC instruction -> i++
        iter_val = SSAValue(name="t100_1", value_type=opcodes.ResultType.INT)
        iter_inst = SSAInstruction(
            block_id=2,
            mnemonic="INC",
            address=100,
            inputs=[loop_var],
            outputs=[iter_val],
        )
        iter_val.producer_inst = iter_inst

        detector = ForLoopDetector(SSAFunction(cfg=cfg, values={}, instructions={}, scr=None))

        formatted = detector._format_iterator(iter_inst, "t100_0")
        assert formatted == "t100++"

        # Test IADD with 1 -> i++
        iter_inst2 = SSAInstruction(
            block_id=2,
            mnemonic="IADD",
            address=100,
            inputs=[loop_var, const_1],
            outputs=[iter_val],
        )

        formatted2 = detector._format_iterator(iter_inst2, "t100_0")
        assert "++" in formatted2

    def test_constant_value_extraction(self):
        """Test constant value extraction from SSA values."""
        cfg = CFG()
        detector = ForLoopDetector(SSAFunction(cfg=cfg, values={}, instructions={}, scr=None))

        # Test metadata constant
        val1 = SSAValue(
            name="test",
            value_type=opcodes.ResultType.INT,
            metadata={'constant': 5}
        )
        assert detector._get_constant_value(val1) == 5

        # Test const_ naming pattern
        val2 = SSAValue(
            name="const_10",
            value_type=opcodes.ResultType.INT,
        )
        assert detector._get_constant_value(val2) == 10

        # Test non-constant
        val3 = SSAValue(
            name="t100_0",
            value_type=opcodes.ResultType.INT,
        )
        assert detector._get_constant_value(val3) is None
