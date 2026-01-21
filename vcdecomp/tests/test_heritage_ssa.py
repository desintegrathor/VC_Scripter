"""
Unit tests for heritage-based incremental SSA construction.

Tests the newly added heritage SSA infrastructure:
- Dominance frontier computation in cfg.py
- LocationMap tracking in heritage/location_map.py
- HeritageOrchestrator in heritage/heritage_orchestrator.py
- PHI node placement using dominance frontiers
"""

import unittest
from typing import Dict, List, Set
from dataclasses import dataclass, field


# ============================================================================
# Tests for Dominance Frontier Computation
# ============================================================================

class TestDominanceFrontiers(unittest.TestCase):
    """Tests for dominance frontier computation in cfg.py"""

    def test_simple_diamond_cfg(self):
        """Test dominance frontiers for a simple diamond CFG.

        CFG structure:
            0 (entry)
           / \
          1   2
           \ /
            3 (join)

        Expected DF:
        - DF(0) = {}
        - DF(1) = {3}
        - DF(2) = {3}
        - DF(3) = {}
        """
        from vcdecomp.core.ir.cfg import CFG, BasicBlock, _compute_dominance_frontiers

        # Build blocks
        blocks = {
            0: BasicBlock(block_id=0, start=0, end=0, predecessors=set(), successors={1, 2}),
            1: BasicBlock(block_id=1, start=1, end=1, predecessors={0}, successors={3}),
            2: BasicBlock(block_id=2, start=2, end=2, predecessors={0}, successors={3}),
            3: BasicBlock(block_id=3, start=3, end=3, predecessors={1, 2}, successors=set()),
        }

        cfg = CFG(
            blocks=blocks,
            entry_block=0,
            idom={0: 0, 1: 0, 2: 0, 3: 0},
            dom_tree={0: [1, 2, 3], 1: [], 2: [], 3: []},
            dom_order=[0, 1, 2, 3]
        )

        _compute_dominance_frontiers(cfg)

        self.assertEqual(cfg.dominance_frontiers[0], set())
        self.assertEqual(cfg.dominance_frontiers[1], {3})
        self.assertEqual(cfg.dominance_frontiers[2], {3})
        self.assertEqual(cfg.dominance_frontiers[3], set())

    def test_loop_cfg(self):
        """Test dominance frontiers for a loop CFG.

        CFG structure:
            0 (entry)
            |
            1 (header) <---+
           / \             |
          2   3            |
          |   |            |
          +---+----> 4 ----+
                     |
                     5 (exit)

        Block 1 is the loop header with back edge from 4.
        """
        from vcdecomp.core.ir.cfg import CFG, BasicBlock, _compute_dominance_frontiers

        blocks = {
            0: BasicBlock(block_id=0, start=0, end=0, predecessors=set(), successors={1}),
            1: BasicBlock(block_id=1, start=1, end=1, predecessors={0, 4}, successors={2, 3}),
            2: BasicBlock(block_id=2, start=2, end=2, predecessors={1}, successors={4}),
            3: BasicBlock(block_id=3, start=3, end=3, predecessors={1}, successors={4}),
            4: BasicBlock(block_id=4, start=4, end=4, predecessors={2, 3}, successors={1, 5}),
            5: BasicBlock(block_id=5, start=5, end=5, predecessors={4}, successors=set()),
        }

        cfg = CFG(
            blocks=blocks,
            entry_block=0,
            idom={0: 0, 1: 0, 2: 1, 3: 1, 4: 1, 5: 4},
            dom_tree={0: [1], 1: [2, 3, 4], 2: [], 3: [], 4: [5], 5: []},
            dom_order=[0, 1, 2, 3, 4, 5]
        )

        _compute_dominance_frontiers(cfg)

        # Block 1 is the loop header - it should be in its own DF due to back edge
        self.assertIn(1, cfg.dominance_frontiers[4])
        # Block 4 is a join point for blocks 2 and 3
        self.assertIn(4, cfg.dominance_frontiers[2])
        self.assertIn(4, cfg.dominance_frontiers[3])

    def test_iterated_dominance_frontier(self):
        """Test iterated dominance frontier computation for PHI placement."""
        from vcdecomp.core.ir.cfg import CFG, BasicBlock, get_iterated_dominance_frontier

        # Simple diamond - if we have a definition in blocks 1 and 2,
        # we need a PHI at block 3
        blocks = {
            0: BasicBlock(block_id=0, start=0, end=0, predecessors=set(), successors={1, 2}),
            1: BasicBlock(block_id=1, start=1, end=1, predecessors={0}, successors={3}),
            2: BasicBlock(block_id=2, start=2, end=2, predecessors={0}, successors={3}),
            3: BasicBlock(block_id=3, start=3, end=3, predecessors={1, 2}, successors=set()),
        }

        cfg = CFG(
            blocks=blocks,
            entry_block=0,
            idom={0: 0, 1: 0, 2: 0, 3: 0},
            dom_tree={0: [1, 2, 3], 1: [], 2: [], 3: []},
            dom_order=[0, 1, 2, 3],
            dominance_frontiers={0: set(), 1: {3}, 2: {3}, 3: set()}
        )

        # Variable defined in blocks 1 and 2
        def_blocks = {1, 2}
        phi_blocks = get_iterated_dominance_frontier(cfg, def_blocks)

        # PHI should be placed at block 3 (the join point)
        self.assertEqual(phi_blocks, {3})

    def test_single_definition_no_phi(self):
        """Test that a single definition doesn't require PHI nodes."""
        from vcdecomp.core.ir.cfg import CFG, BasicBlock, get_iterated_dominance_frontier

        blocks = {
            0: BasicBlock(block_id=0, start=0, end=0, predecessors=set(), successors={1, 2}),
            1: BasicBlock(block_id=1, start=1, end=1, predecessors={0}, successors={3}),
            2: BasicBlock(block_id=2, start=2, end=2, predecessors={0}, successors={3}),
            3: BasicBlock(block_id=3, start=3, end=3, predecessors={1, 2}, successors=set()),
        }

        cfg = CFG(
            blocks=blocks,
            entry_block=0,
            idom={0: 0, 1: 0, 2: 0, 3: 0},
            dom_tree={0: [1, 2, 3], 1: [], 2: [], 3: []},
            dom_order=[0, 1, 2, 3],
            dominance_frontiers={0: set(), 1: {3}, 2: {3}, 3: set()}
        )

        # Variable defined only in block 0 (dominates all)
        def_blocks = {0}
        phi_blocks = get_iterated_dominance_frontier(cfg, def_blocks)

        # No PHI needed - block 0 dominates everything
        self.assertEqual(phi_blocks, set())


# ============================================================================
# Tests for LocationMap
# ============================================================================

class TestLocationMap(unittest.TestCase):
    """Tests for heritage location tracking."""

    def test_basic_heritage_tracking(self):
        """Test basic heritage tracking operations."""
        from vcdecomp.core.ir.heritage.location_map import LocationMap, AddressSpace

        loc_map = LocationMap()

        # Initially nothing is heritaged
        is_done, pass_num = loc_map.is_heritaged(AddressSpace.STACK, 0, 4)
        self.assertFalse(is_done)
        self.assertIsNone(pass_num)

        # Mark a location as heritaged
        loc_map.mark_heritaged(AddressSpace.STACK, 0, 4, "local_0")

        # Now it should be heritaged
        is_done, pass_num = loc_map.is_heritaged(AddressSpace.STACK, 0, 4)
        self.assertTrue(is_done)
        self.assertEqual(pass_num, 0)

    def test_pass_advancement(self):
        """Test pass number tracking."""
        from vcdecomp.core.ir.heritage.location_map import LocationMap, AddressSpace

        loc_map = LocationMap()

        # Mark in pass 0
        loc_map.mark_heritaged(AddressSpace.STACK, 0, 4, "local_0")

        # Advance to pass 1
        loc_map.advance_pass()
        self.assertEqual(loc_map.current_pass, 1)

        # Mark in pass 1
        loc_map.mark_heritaged(AddressSpace.STACK, 4, 4, "local_4")

        # Check pass numbers
        _, pass_0 = loc_map.is_heritaged(AddressSpace.STACK, 0, 4)
        _, pass_1 = loc_map.is_heritaged(AddressSpace.STACK, 4, 4)
        self.assertEqual(pass_0, 0)
        self.assertEqual(pass_1, 1)

    def test_different_address_spaces(self):
        """Test tracking across different address spaces."""
        from vcdecomp.core.ir.heritage.location_map import LocationMap, AddressSpace

        loc_map = LocationMap()

        # Mark same offset in different spaces
        loc_map.mark_heritaged(AddressSpace.STACK, 0, 4, "local_0")
        loc_map.mark_heritaged(AddressSpace.PARAM, 0, 4, "param_0")
        loc_map.mark_heritaged(AddressSpace.GLOBAL, 0, 4, "data_0")

        # Each should be independently tracked
        is_stack, _ = loc_map.is_heritaged(AddressSpace.STACK, 0, 4)
        is_param, _ = loc_map.is_heritaged(AddressSpace.PARAM, 0, 4)
        is_global, _ = loc_map.is_heritaged(AddressSpace.GLOBAL, 0, 4)

        self.assertTrue(is_stack)
        self.assertTrue(is_param)
        self.assertTrue(is_global)

        # Different offset should not be heritaged
        is_done, _ = loc_map.is_heritaged(AddressSpace.STACK, 8, 4)
        self.assertFalse(is_done)

    def test_discovery_tracking(self):
        """Test tracking of variables discovered in each pass."""
        from vcdecomp.core.ir.heritage.location_map import LocationMap, AddressSpace

        loc_map = LocationMap()

        # Pass 0 discoveries
        loc_map.mark_heritaged(AddressSpace.STACK, 0, 4, "local_0")
        loc_map.mark_heritaged(AddressSpace.STACK, 4, 4, "local_4")

        discoveries_0 = loc_map.get_discoveries_in_pass(0)
        self.assertEqual(discoveries_0, {"local_0", "local_4"})

        # Advance and discover more
        loc_map.advance_pass()
        loc_map.mark_heritaged(AddressSpace.STACK, 8, 4, "local_8")

        discoveries_1 = loc_map.get_discoveries_in_pass(1)
        self.assertEqual(discoveries_1, {"local_8"})

        # Pass 0 discoveries unchanged
        discoveries_0_again = loc_map.get_discoveries_in_pass(0)
        self.assertEqual(discoveries_0_again, {"local_0", "local_4"})

    def test_overlapping_ranges(self):
        """Test detection of overlapping heritage ranges."""
        from vcdecomp.core.ir.heritage.location_map import LocationMap, AddressSpace

        loc_map = LocationMap()

        # Heritage a 4-byte range at offset 0
        loc_map.mark_heritaged(AddressSpace.STACK, 0, 4, "local_0")

        # Check overlaps
        overlaps = loc_map.get_overlapping_ranges(AddressSpace.STACK, 0, 4)
        self.assertEqual(len(overlaps), 1)
        self.assertEqual(overlaps[0].var_name, "local_0")

        # Partial overlap
        overlaps = loc_map.get_overlapping_ranges(AddressSpace.STACK, 2, 4)
        self.assertEqual(len(overlaps), 1)

        # No overlap
        overlaps = loc_map.get_overlapping_ranges(AddressSpace.STACK, 8, 4)
        self.assertEqual(len(overlaps), 0)


# ============================================================================
# Tests for HeritageRange
# ============================================================================

class TestHeritageRange(unittest.TestCase):
    """Tests for HeritageRange dataclass."""

    def test_range_overlap(self):
        """Test range overlap detection."""
        from vcdecomp.core.ir.heritage.location_map import HeritageRange, AddressSpace

        range1 = HeritageRange(AddressSpace.STACK, 0, 4, 0)
        range2 = HeritageRange(AddressSpace.STACK, 2, 4, 0)
        range3 = HeritageRange(AddressSpace.STACK, 4, 4, 0)
        range4 = HeritageRange(AddressSpace.PARAM, 0, 4, 0)

        # Overlapping ranges
        self.assertTrue(range1.overlaps(range2))
        self.assertTrue(range2.overlaps(range1))

        # Adjacent but not overlapping
        self.assertFalse(range1.overlaps(range3))

        # Same offset, different address space
        self.assertFalse(range1.overlaps(range4))

    def test_range_contains(self):
        """Test range containment."""
        from vcdecomp.core.ir.heritage.location_map import HeritageRange, AddressSpace

        # 8-byte range
        range_large = HeritageRange(AddressSpace.STACK, 0, 8, 0)

        # Contains smaller range at start
        self.assertTrue(range_large.contains(AddressSpace.STACK, 0, 4))

        # Contains smaller range in middle
        self.assertTrue(range_large.contains(AddressSpace.STACK, 2, 4))

        # Does not contain range that extends past end
        self.assertFalse(range_large.contains(AddressSpace.STACK, 6, 4))

        # Does not contain different address space
        self.assertFalse(range_large.contains(AddressSpace.PARAM, 0, 4))


# ============================================================================
# Tests for Stack Lifter Heritage Functions
# ============================================================================

class TestStackLifterHeritage(unittest.TestCase):
    """Tests for heritage-related functions in stack_lifter.py."""

    def test_collect_variable_definitions(self):
        """Test variable definition collection."""
        from vcdecomp.core.ir.stack_lifter import collect_variable_definitions
        from vcdecomp.core.disasm import opcodes

        # Create mock lifted instructions
        @dataclass
        class MockInstruction:
            opcode: int
            arg1: int
            address: int

        @dataclass
        class MockLiftedInstruction:
            instruction: MockInstruction

        # Mock resolver that returns LLD for opcode 100 and LCP for opcode 101
        class MockResolver:
            def get_mnemonic(self, opcode):
                return {100: "LLD", 101: "LCP", 102: "GLD"}.get(opcode, "NOP")

        resolver = MockResolver()

        lifted = {
            0: [
                MockLiftedInstruction(MockInstruction(100, 8, 0)),   # LLD [sp+8] -> store to local_8
                MockLiftedInstruction(MockInstruction(101, 8, 1)),   # LCP [sp+8] -> load from local_8
            ],
            1: [
                MockLiftedInstruction(MockInstruction(100, 8, 10)),  # LLD [sp+8] -> another store to local_8
                MockLiftedInstruction(MockInstruction(102, 100, 11)), # GLD data[100] -> store to data_100
            ],
        }

        var_defs = collect_variable_definitions(lifted, resolver)

        # local_8 defined in blocks 0 and 1
        self.assertEqual(var_defs["local_8"], {0, 1})

        # data_100 defined in block 1
        self.assertEqual(var_defs["data_100"], {1})


# ============================================================================
# Integration Test
# ============================================================================

class TestHeritageIntegration(unittest.TestCase):
    """Integration tests for heritage-based SSA construction."""

    def test_build_ssa_incremental_import(self):
        """Test that build_ssa_incremental can be imported."""
        from vcdecomp.core.ir.ssa import build_ssa_incremental
        self.assertIsNotNone(build_ssa_incremental)

    def test_heritage_orchestrator_import(self):
        """Test that HeritageOrchestrator can be imported."""
        from vcdecomp.core.ir.heritage import HeritageOrchestrator
        self.assertIsNotNone(HeritageOrchestrator)


if __name__ == '__main__':
    unittest.main()
