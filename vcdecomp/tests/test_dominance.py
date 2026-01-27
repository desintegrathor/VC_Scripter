"""
Tests for dominator analysis.

Tests the dominator tree construction and related algorithms.
"""

import pytest
from vcdecomp.core.ir.structure.blocks.hierarchy import (
    BlockGraph,
    BlockBasic,
    BlockType,
    EdgeType,
)
from vcdecomp.core.ir.structure.analysis.dominance import (
    DominatorAnalysis,
    compute_dominators,
)


class TestDominatorAnalysis:
    """Test dominator analysis algorithms."""

    def test_simple_linear_graph(self):
        """Test dominators in a simple linear graph: A -> B -> C"""
        graph = BlockGraph()

        # Create blocks
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)
        block_c = BlockBasic(block_id=2, original_block_id=2)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_block(block_c)

        # Create edges: A -> B -> C
        graph.add_edge(block_a, block_b)
        graph.add_edge(block_b, block_c)

        graph.entry_block = block_a

        # Compute dominators
        dom = DominatorAnalysis(graph)
        dom.compute()

        # A dominates itself and has no idom
        assert dom.get_idom(block_a) is None
        assert dom.dominates(block_a, block_a)

        # A dominates B, and A is idom of B
        assert dom.get_idom(block_b) == block_a
        assert dom.dominates(block_a, block_b)

        # A dominates C, B is idom of C
        assert dom.get_idom(block_c) == block_b
        assert dom.dominates(block_a, block_c)
        assert dom.dominates(block_b, block_c)

        # Check depths
        assert dom.get_dom_depth(block_a) == 1
        assert dom.get_dom_depth(block_b) == 2
        assert dom.get_dom_depth(block_c) == 3

    def test_diamond_graph(self):
        """
        Test dominators in diamond graph:
               A
              / \\
             B   C
              \\ /
               D
        """
        graph = BlockGraph()

        # Create blocks
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)
        block_c = BlockBasic(block_id=2, original_block_id=2)
        block_d = BlockBasic(block_id=3, original_block_id=3)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_block(block_c)
        graph.add_block(block_d)

        # Create diamond
        graph.add_edge(block_a, block_b)
        graph.add_edge(block_a, block_c)
        graph.add_edge(block_b, block_d)
        graph.add_edge(block_c, block_d)

        graph.entry_block = block_a

        # Compute dominators
        dom = DominatorAnalysis(graph)
        dom.compute()

        # A dominates all
        assert dom.dominates(block_a, block_a)
        assert dom.dominates(block_a, block_b)
        assert dom.dominates(block_a, block_c)
        assert dom.dominates(block_a, block_d)

        # B and C don't dominate each other
        assert not dom.dominates(block_b, block_c)
        assert not dom.dominates(block_c, block_b)

        # B and C don't dominate D (both paths reach D)
        assert not dom.dominates(block_b, block_d)
        assert not dom.dominates(block_c, block_d)

        # A is immediate dominator of B, C, and D
        assert dom.get_idom(block_b) == block_a
        assert dom.get_idom(block_c) == block_a
        assert dom.get_idom(block_d) == block_a

        # Check depths
        assert dom.get_dom_depth(block_a) == 1
        assert dom.get_dom_depth(block_b) == 2
        assert dom.get_dom_depth(block_c) == 2
        assert dom.get_dom_depth(block_d) == 2

    def test_loop_graph(self):
        """
        Test dominators with a loop:
               A
               |
               B (header)
              / \\
             C   E
             |
             D --+
             (back edge to B)
        """
        graph = BlockGraph()

        # Create blocks
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)
        block_c = BlockBasic(block_id=2, original_block_id=2)
        block_d = BlockBasic(block_id=3, original_block_id=3)
        block_e = BlockBasic(block_id=4, original_block_id=4)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_block(block_c)
        graph.add_block(block_d)
        graph.add_block(block_e)

        # Create edges
        graph.add_edge(block_a, block_b)
        graph.add_edge(block_b, block_c)
        graph.add_edge(block_b, block_e)
        graph.add_edge(block_c, block_d)
        # Back edge
        edge = graph.add_edge(block_d, block_b)
        edge.edge_type = EdgeType.BACK_EDGE

        graph.entry_block = block_a

        # Compute dominators
        dom = DominatorAnalysis(graph)
        dom.compute()

        # A dominates all
        assert dom.dominates(block_a, block_b)
        assert dom.dominates(block_a, block_c)
        assert dom.dominates(block_a, block_d)
        assert dom.dominates(block_a, block_e)

        # B (loop header) dominates loop body
        assert dom.dominates(block_b, block_c)
        assert dom.dominates(block_b, block_d)
        assert dom.dominates(block_b, block_e)

        # Check immediate dominators
        assert dom.get_idom(block_b) == block_a
        assert dom.get_idom(block_c) == block_b
        assert dom.get_idom(block_d) == block_c
        assert dom.get_idom(block_e) == block_b

    def test_dominated_set(self):
        """Test getting the set of dominated blocks."""
        graph = BlockGraph()

        # Create blocks: A -> B -> C
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)
        block_c = BlockBasic(block_id=2, original_block_id=2)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_block(block_c)

        graph.add_edge(block_a, block_b)
        graph.add_edge(block_b, block_c)

        graph.entry_block = block_a

        # Compute dominators
        dom = DominatorAnalysis(graph)
        dom.compute()

        # A dominates all blocks
        dominated_a = dom.get_dominated_set(block_a)
        assert dominated_a == {0, 1, 2}

        # B dominates B and C
        dominated_b = dom.get_dominated_set(block_b)
        assert dominated_b == {1, 2}

        # C dominates only itself
        dominated_c = dom.get_dominated_set(block_c)
        assert dominated_c == {2}

    def test_dominance_frontier_diamond(self):
        """
        Test dominance frontier in diamond:
               A
              / \\
             B   C
              \\ /
               D

        DF(A) = {}
        DF(B) = {D}
        DF(C) = {D}
        DF(D) = {}
        """
        graph = BlockGraph()

        # Create blocks
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)
        block_c = BlockBasic(block_id=2, original_block_id=2)
        block_d = BlockBasic(block_id=3, original_block_id=3)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_block(block_c)
        graph.add_block(block_d)

        # Create diamond
        graph.add_edge(block_a, block_b)
        graph.add_edge(block_a, block_c)
        graph.add_edge(block_b, block_d)
        graph.add_edge(block_c, block_d)

        graph.entry_block = block_a

        # Compute dominators
        dom = DominatorAnalysis(graph)
        dom.compute()

        # Check frontiers
        df_a = dom.get_dominator_frontier(block_a)
        assert len(df_a) == 0

        df_b = dom.get_dominator_frontier(block_b)
        assert df_b == {block_d}

        df_c = dom.get_dominator_frontier(block_c)
        assert df_c == {block_d}

        df_d = dom.get_dominator_frontier(block_d)
        assert len(df_d) == 0

    def test_strictly_dominates(self):
        """Test strict domination (excludes self)."""
        graph = BlockGraph()

        # Create blocks: A -> B
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_edge(block_a, block_b)

        graph.entry_block = block_a

        # Compute dominators
        dom = DominatorAnalysis(graph)
        dom.compute()

        # A does not strictly dominate itself
        assert not dom.strictly_dominates(block_a, block_a)

        # A strictly dominates B
        assert dom.strictly_dominates(block_a, block_b)

        # B does not strictly dominate A
        assert not dom.strictly_dominates(block_b, block_a)

    def test_convenience_function(self):
        """Test the convenience function for computing dominators."""
        graph = BlockGraph()

        # Create simple graph: A -> B
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_edge(block_a, block_b)

        graph.entry_block = block_a

        # Use convenience function
        dom = compute_dominators(graph)

        # Check it works
        assert dom.get_idom(block_b) == block_a
        assert dom.dominates(block_a, block_b)
