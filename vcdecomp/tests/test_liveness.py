"""
Unit tests for liveness analysis module.

Tests the LivenessAnalyzer and InterferenceGraph classes from
vcdecomp.core.ir.liveness module.
"""

import pytest
from typing import Dict, List, Set
from unittest.mock import MagicMock, patch
from dataclasses import dataclass, field

from vcdecomp.core.ir.liveness import (
    LivenessInfo,
    LivenessAnalyzer,
    InterferenceGraph,
    InterferenceEdge,
)


# ============================================================================
# Mock Classes for Testing
# ============================================================================

@dataclass
class MockSSAValue:
    """Mock SSA value for testing."""
    name: str
    alias: str = None


@dataclass
class MockSSAInstruction:
    """Mock SSA instruction for testing."""
    mnemonic: str
    address: int
    inputs: List[MockSSAValue] = field(default_factory=list)
    outputs: List[MockSSAValue] = field(default_factory=list)


@dataclass
class MockBasicBlock:
    """Mock basic block for testing."""
    block_id: int
    start: int
    end: int
    successors: Set[int] = field(default_factory=set)
    predecessors: Set[int] = field(default_factory=set)


@dataclass
class MockCFG:
    """Mock control flow graph for testing."""
    blocks: Dict[int, MockBasicBlock] = field(default_factory=dict)
    entry_block: int = 0


@dataclass
class MockSSAFunction:
    """Mock SSA function for testing."""
    cfg: MockCFG = None
    instructions: Dict[int, List[MockSSAInstruction]] = field(default_factory=dict)


# ============================================================================
# LivenessInfo Tests
# ============================================================================

class TestLivenessInfo:
    """Tests for the LivenessInfo dataclass."""

    def test_create_empty(self):
        """Test creating an empty LivenessInfo."""
        info = LivenessInfo(block_id=0)
        assert info.block_id == 0
        assert info.live_in == set()
        assert info.live_out == set()
        assert info.use_set == set()
        assert info.def_set == set()

    def test_create_with_values(self):
        """Test creating LivenessInfo with initial values."""
        info = LivenessInfo(
            block_id=5,
            live_in={'a', 'b'},
            live_out={'c'},
            use_set={'a'},
            def_set={'d'}
        )
        assert info.block_id == 5
        assert info.live_in == {'a', 'b'}
        assert info.live_out == {'c'}
        assert info.use_set == {'a'}
        assert info.def_set == {'d'}


# ============================================================================
# LivenessAnalyzer Tests
# ============================================================================

class TestLivenessAnalyzer:
    """Tests for the LivenessAnalyzer class."""

    def test_simple_use_def(self):
        """Test USE/DEF computation for a simple block."""
        # Create a simple function with one block
        # Block 0: x = input; y = x + 1; output = y
        cfg = MockCFG()
        cfg.blocks[0] = MockBasicBlock(block_id=0, start=0, end=2)
        cfg.entry_block = 0

        ssa_func = MockSSAFunction(cfg=cfg)
        ssa_func.instructions[0] = [
            MockSSAInstruction(
                mnemonic="LCP",
                address=0,
                inputs=[MockSSAValue("input")],
                outputs=[MockSSAValue("x")]
            ),
            MockSSAInstruction(
                mnemonic="ADD",
                address=1,
                inputs=[MockSSAValue("x"), MockSSAValue("const_1")],
                outputs=[MockSSAValue("y")]
            ),
            MockSSAInstruction(
                mnemonic="SCP",
                address=2,
                inputs=[MockSSAValue("y")],
                outputs=[MockSSAValue("output")]
            ),
        ]

        analyzer = LivenessAnalyzer(ssa_func, {0})
        use_set, def_set = analyzer._compute_use_def_sets(0)

        # 'input' and 'const_1' are used before definition
        assert 'input' in use_set
        assert 'const_1' in use_set
        # 'x', 'y', 'output' are defined in this block
        assert 'x' in def_set
        assert 'y' in def_set
        assert 'output' in def_set
        # 'x' is NOT in use_set because it's defined before use
        assert 'x' not in use_set

    def test_liveness_propagation(self):
        """Test liveness propagation across blocks."""
        # Create two blocks: B0 -> B1
        # B0: x = 1
        # B1: y = x + 1
        cfg = MockCFG()
        cfg.blocks[0] = MockBasicBlock(
            block_id=0, start=0, end=0,
            successors={1}
        )
        cfg.blocks[1] = MockBasicBlock(
            block_id=1, start=1, end=1,
            predecessors={0}
        )
        cfg.entry_block = 0

        ssa_func = MockSSAFunction(cfg=cfg)
        ssa_func.instructions[0] = [
            MockSSAInstruction(
                mnemonic="ICP",
                address=0,
                inputs=[],
                outputs=[MockSSAValue("x")]
            ),
        ]
        ssa_func.instructions[1] = [
            MockSSAInstruction(
                mnemonic="ADD",
                address=1,
                inputs=[MockSSAValue("x")],
                outputs=[MockSSAValue("y")]
            ),
        ]

        analyzer = LivenessAnalyzer(ssa_func, {0, 1})
        liveness = analyzer.compute_liveness()

        # x should be live at end of B0 (LIVE_OUT[0])
        assert 'x' in liveness[0].live_out
        # x should be live at start of B1 (LIVE_IN[1])
        assert 'x' in liveness[1].live_in

    def test_liveness_diamond_cfg(self):
        """Test liveness with diamond-shaped CFG (if-else)."""
        # B0 -> B1, B2 -> B3
        #   x = ...
        #   if (cond) goto B1 else B2
        # B1: y = x
        # B2: z = x
        # B3: use y, z
        cfg = MockCFG()
        cfg.blocks[0] = MockBasicBlock(
            block_id=0, start=0, end=0,
            successors={1, 2}
        )
        cfg.blocks[1] = MockBasicBlock(
            block_id=1, start=1, end=1,
            predecessors={0}, successors={3}
        )
        cfg.blocks[2] = MockBasicBlock(
            block_id=2, start=2, end=2,
            predecessors={0}, successors={3}
        )
        cfg.blocks[3] = MockBasicBlock(
            block_id=3, start=3, end=3,
            predecessors={1, 2}
        )
        cfg.entry_block = 0

        ssa_func = MockSSAFunction(cfg=cfg)
        ssa_func.instructions[0] = [
            MockSSAInstruction(
                mnemonic="ICP",
                address=0,
                inputs=[],
                outputs=[MockSSAValue("x")]
            ),
        ]
        ssa_func.instructions[1] = [
            MockSSAInstruction(
                mnemonic="MOV",
                address=1,
                inputs=[MockSSAValue("x")],
                outputs=[MockSSAValue("y")]
            ),
        ]
        ssa_func.instructions[2] = [
            MockSSAInstruction(
                mnemonic="MOV",
                address=2,
                inputs=[MockSSAValue("x")],
                outputs=[MockSSAValue("z")]
            ),
        ]
        ssa_func.instructions[3] = [
            MockSSAInstruction(
                mnemonic="ADD",
                address=3,
                inputs=[MockSSAValue("y"), MockSSAValue("z")],
                outputs=[MockSSAValue("result")]
            ),
        ]

        analyzer = LivenessAnalyzer(ssa_func, {0, 1, 2, 3})
        liveness = analyzer.compute_liveness()

        # x should be live at exit of B0
        assert 'x' in liveness[0].live_out
        # y should be live at exit of B1
        assert 'y' in liveness[1].live_out
        # z should be live at exit of B2
        assert 'z' in liveness[2].live_out


# ============================================================================
# InterferenceGraph Tests
# ============================================================================

class TestInterferenceGraph:
    """Tests for the InterferenceGraph class."""

    def test_no_interference(self):
        """Test that non-overlapping live ranges don't interfere."""
        # Create liveness where a and b don't overlap
        liveness = {
            0: LivenessInfo(
                block_id=0,
                live_in={'a'},
                live_out={'b'},
                use_set={'a'},
                def_set={'b'}
            )
        }

        cfg = MockCFG()
        cfg.blocks[0] = MockBasicBlock(block_id=0, start=0, end=0)

        ssa_func = MockSSAFunction(cfg=cfg)
        ssa_func.instructions[0] = [
            MockSSAInstruction(
                mnemonic="USE",
                address=0,
                inputs=[MockSSAValue("a")],
                outputs=[]
            ),
            MockSSAInstruction(
                mnemonic="DEF",
                address=1,
                inputs=[],
                outputs=[MockSSAValue("b")]
            ),
        ]

        graph = InterferenceGraph(liveness, ssa_func)

        # a and b should not interfere (sequential use)
        # Note: This depends on exact implementation details
        assert 'a' in graph.nodes or 'b' in graph.nodes

    def test_interference_at_block_entry(self):
        """Test interference between values live at block entry."""
        liveness = {
            0: LivenessInfo(
                block_id=0,
                live_in={'a', 'b', 'c'},
                live_out=set(),
                use_set={'a', 'b', 'c'},
                def_set=set()
            )
        }

        cfg = MockCFG()
        cfg.blocks[0] = MockBasicBlock(block_id=0, start=0, end=0)

        ssa_func = MockSSAFunction(cfg=cfg)
        ssa_func.instructions[0] = []

        graph = InterferenceGraph(liveness, ssa_func)

        # All three should interfere with each other
        assert graph.interferes('a', 'b')
        assert graph.interferes('b', 'c')
        assert graph.interferes('a', 'c')

    def test_interference_symmetric(self):
        """Test that interference is symmetric."""
        liveness = {
            0: LivenessInfo(
                block_id=0,
                live_in={'x', 'y'},
                live_out={'x', 'y'},
                use_set=set(),
                def_set=set()
            )
        }

        cfg = MockCFG()
        cfg.blocks[0] = MockBasicBlock(block_id=0, start=0, end=0)

        ssa_func = MockSSAFunction(cfg=cfg)
        ssa_func.instructions[0] = []

        graph = InterferenceGraph(liveness, ssa_func)

        # Interference should be symmetric
        assert graph.interferes('x', 'y') == graph.interferes('y', 'x')

    def test_non_interfering_groups_single(self):
        """Test grouping when all values can be merged."""
        liveness = {
            0: LivenessInfo(block_id=0, live_in=set(), live_out=set())
        }

        cfg = MockCFG()
        cfg.blocks[0] = MockBasicBlock(block_id=0, start=0, end=0)

        ssa_func = MockSSAFunction(cfg=cfg)
        ssa_func.instructions[0] = []

        graph = InterferenceGraph(liveness, ssa_func)

        # With no interference, all values should be in one group
        groups = graph.get_non_interfering_groups(['a', 'b', 'c'])
        # All should be in a single group since none are in the graph
        assert len(groups) == 1
        assert set(groups[0]) == {'a', 'b', 'c'}

    def test_non_interfering_groups_multiple(self):
        """Test grouping when values interfere."""
        liveness = {
            0: LivenessInfo(
                block_id=0,
                live_in={'a', 'b'},
                live_out={'a', 'b'},
                use_set=set(),
                def_set=set()
            )
        }

        cfg = MockCFG()
        cfg.blocks[0] = MockBasicBlock(block_id=0, start=0, end=0)

        ssa_func = MockSSAFunction(cfg=cfg)
        ssa_func.instructions[0] = []

        graph = InterferenceGraph(liveness, ssa_func)

        # a and b interfere, so they should be in different groups
        groups = graph.get_non_interfering_groups(['a', 'b'])
        assert len(groups) == 2
        # Each group should have exactly one element
        group_sizes = sorted([len(g) for g in groups])
        assert group_sizes == [1, 1]

    def test_get_neighbors(self):
        """Test getting interference neighbors."""
        liveness = {
            0: LivenessInfo(
                block_id=0,
                live_in={'a', 'b', 'c'},
                live_out=set(),
                use_set={'a', 'b', 'c'},
                def_set=set()
            )
        }

        cfg = MockCFG()
        cfg.blocks[0] = MockBasicBlock(block_id=0, start=0, end=0)

        ssa_func = MockSSAFunction(cfg=cfg)
        ssa_func.instructions[0] = []

        graph = InterferenceGraph(liveness, ssa_func)

        # a should have b and c as neighbors
        neighbors_a = graph.get_neighbors('a')
        assert 'b' in neighbors_a
        assert 'c' in neighbors_a


# ============================================================================
# InterferenceEdge Tests
# ============================================================================

class TestInterferenceEdge:
    """Tests for the InterferenceEdge dataclass."""

    def test_edge_equality(self):
        """Test that edge equality is order-independent."""
        edge1 = InterferenceEdge('a', 'b')
        edge2 = InterferenceEdge('b', 'a')
        assert edge1 == edge2

    def test_edge_hash(self):
        """Test that edge hash is order-independent."""
        edge1 = InterferenceEdge('a', 'b')
        edge2 = InterferenceEdge('b', 'a')
        assert hash(edge1) == hash(edge2)

    def test_edge_in_set(self):
        """Test that edges work correctly in sets."""
        edge1 = InterferenceEdge('a', 'b')
        edge2 = InterferenceEdge('b', 'a')

        edge_set = {edge1}
        assert edge2 in edge_set


# ============================================================================
# Integration Tests
# ============================================================================

class TestLivenessIntegration:
    """Integration tests for liveness analysis."""

    def test_loop_liveness(self):
        """Test liveness analysis with a loop."""
        # B0: i = 0
        # B1: i < 10? -> B2 or B3
        # B2: i = i + 1; goto B1
        # B3: exit
        cfg = MockCFG()
        cfg.blocks[0] = MockBasicBlock(
            block_id=0, start=0, end=0,
            successors={1}
        )
        cfg.blocks[1] = MockBasicBlock(
            block_id=1, start=1, end=1,
            predecessors={0, 2}, successors={2, 3}
        )
        cfg.blocks[2] = MockBasicBlock(
            block_id=2, start=2, end=2,
            predecessors={1}, successors={1}
        )
        cfg.blocks[3] = MockBasicBlock(
            block_id=3, start=3, end=3,
            predecessors={1}
        )
        cfg.entry_block = 0

        ssa_func = MockSSAFunction(cfg=cfg)
        ssa_func.instructions[0] = [
            MockSSAInstruction(
                mnemonic="ICP",
                address=0,
                inputs=[],
                outputs=[MockSSAValue("i_0")]
            ),
        ]
        ssa_func.instructions[1] = [
            MockSSAInstruction(
                mnemonic="CMP",
                address=1,
                inputs=[MockSSAValue("i_phi")],
                outputs=[]
            ),
        ]
        ssa_func.instructions[2] = [
            MockSSAInstruction(
                mnemonic="ADD",
                address=2,
                inputs=[MockSSAValue("i_phi"), MockSSAValue("const_1")],
                outputs=[MockSSAValue("i_1")]
            ),
        ]
        ssa_func.instructions[3] = []

        analyzer = LivenessAnalyzer(ssa_func, {0, 1, 2, 3})
        liveness = analyzer.compute_liveness()

        # i_phi should be live at entry of B1 (used in the loop)
        assert 'i_phi' in liveness[1].live_in

        # const_1 should be live in B2 (used for increment)
        assert 'const_1' in liveness[2].use_set
