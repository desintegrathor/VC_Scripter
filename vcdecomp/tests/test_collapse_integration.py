"""
Integration tests for collapse engine with advanced analyses.

Tests that the collapse engine correctly uses dominator analysis, loop analysis,
and irreducible edge detection.
"""

import pytest
from vcdecomp.core.ir.structure.blocks.hierarchy import (
    BlockGraph,
    BlockBasic,
    BlockType,
    EdgeType,
)
from vcdecomp.core.ir.structure.collapse.engine import CollapseStructure
from vcdecomp.core.ir.structure.collapse.analysis_helpers import (
    is_loop_header,
    get_loop_body,
    dominates,
)


class TestCollapseIntegration:
    """Test collapse engine integration with advanced analyses."""

    def test_analysis_computation(self):
        """Test that analyses are computed when enabled."""
        graph = BlockGraph()

        # Create simple CFG: A -> B -> C
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)
        block_c = BlockBasic(block_id=2, original_block_id=2)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_block(block_c)

        graph.add_edge(block_a, block_b)
        graph.add_edge(block_b, block_c)

        graph.entry_block = block_a

        # Create collapser with analysis enabled
        collapser = CollapseStructure(graph)
        collapser.use_advanced_analysis = True

        # Run collapse
        collapser.collapse_all()

        # Check that analyses were computed
        assert collapser.get_dominator_analysis() is not None
        assert collapser.get_loop_analysis() is not None
        assert collapser.get_spanning_tree() is not None

    def test_analysis_disabled(self):
        """Test that analyses can be disabled."""
        graph = BlockGraph()

        block_a = BlockBasic(block_id=0, original_block_id=0)
        graph.add_block(block_a)
        graph.entry_block = block_a

        # Create collapser with analysis disabled
        collapser = CollapseStructure(graph)
        collapser.use_advanced_analysis = False

        # Run collapse
        collapser.collapse_all()

        # Check that analyses were NOT computed
        assert collapser.get_dominator_analysis() is None
        assert collapser.get_loop_analysis() is None
        assert collapser.get_spanning_tree() is None

    def test_loop_detection_with_analysis(self):
        """Test that loop detection uses analysis when available."""
        graph = BlockGraph()

        # Create simple loop: A -> B -> A
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)

        graph.add_block(block_a)
        graph.add_block(block_b)

        graph.add_edge(block_a, block_b)
        edge_back = graph.add_edge(block_b, block_a)

        graph.entry_block = block_a

        # Create collapser with analysis enabled
        collapser = CollapseStructure(graph)
        collapser.use_advanced_analysis = True
        collapser._compute_analyses()

        # Check loop was detected
        loop_analysis = collapser.get_loop_analysis()
        assert loop_analysis is not None
        assert len(loop_analysis.loops) == 1

        loop = loop_analysis.loops[0]
        assert loop.head == block_a
        assert block_b in loop.tails

    def test_statistics_with_analyses(self):
        """Test that statistics include analysis data."""
        graph = BlockGraph()

        # Create loop
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)

        graph.add_block(block_a)
        graph.add_block(block_b)

        graph.add_edge(block_a, block_b)
        graph.add_edge(block_b, block_a)

        graph.entry_block = block_a

        # Collapse with analysis
        collapser = CollapseStructure(graph)
        collapser.use_advanced_analysis = True
        collapser.collapse_all()

        # Check statistics
        stats = collapser.get_statistics()
        assert "loops_detected" in stats
        assert stats["loops_detected"] >= 1

    def test_helper_is_loop_header(self):
        """Test is_loop_header helper function."""
        graph = BlockGraph()

        # Create loop: A -> B -> A
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)

        graph.add_block(block_a)
        graph.add_block(block_b)

        graph.add_edge(block_a, block_b)
        edge_back = graph.add_edge(block_b, block_a)
        edge_back.edge_type = EdgeType.BACK_EDGE

        graph.entry_block = block_a

        # Test without analysis (fallback)
        assert is_loop_header(block_a, None) is True
        assert is_loop_header(block_b, None) is False

    def test_helper_dominates(self):
        """Test dominates helper function."""
        graph = BlockGraph()

        # Create CFG: A -> B -> C
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)
        block_c = BlockBasic(block_id=2, original_block_id=2)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_block(block_c)

        graph.add_edge(block_a, block_b)
        graph.add_edge(block_b, block_c)

        graph.entry_block = block_a

        # Compute dominator analysis
        collapser = CollapseStructure(graph)
        collapser.use_advanced_analysis = True
        collapser._compute_analyses()

        dom_analysis = collapser.get_dominator_analysis()

        # Test domination
        assert dominates(block_a, block_a, dom_analysis) is True
        assert dominates(block_a, block_b, dom_analysis) is True
        assert dominates(block_a, block_c, dom_analysis) is True
        assert dominates(block_b, block_c, dom_analysis) is True
        assert dominates(block_b, block_a, dom_analysis) is False

    def test_helper_get_loop_body(self):
        """Test get_loop_body helper function."""
        graph = BlockGraph()

        # Create loop: A -> B -> C -> A, A -> D (exit)
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)
        block_c = BlockBasic(block_id=2, original_block_id=2)
        block_d = BlockBasic(block_id=3, original_block_id=3)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_block(block_c)
        graph.add_block(block_d)

        graph.add_edge(block_a, block_b)
        graph.add_edge(block_b, block_c)
        edge_back = graph.add_edge(block_c, block_a)
        graph.add_edge(block_a, block_d)

        graph.entry_block = block_a

        # Compute analysis
        collapser = CollapseStructure(graph)
        collapser.use_advanced_analysis = True
        collapser._compute_analyses()

        loop_analysis = collapser.get_loop_analysis()

        # Get loop body
        body = get_loop_body(block_a, loop_analysis)
        assert body is not None
        assert block_a.block_id in body
        assert block_b.block_id in body
        assert block_c.block_id in body
        assert block_d.block_id not in body  # Exit is outside loop

    def test_backwards_compatibility(self):
        """Test that collapse works without analyses (backwards compatibility)."""
        graph = BlockGraph()

        # Create simple CFG
        block_a = BlockBasic(block_id=0, original_block_id=0)
        block_b = BlockBasic(block_id=1, original_block_id=1)

        graph.add_block(block_a)
        graph.add_block(block_b)
        graph.add_edge(block_a, block_b)

        graph.entry_block = block_a

        # Collapse without analysis
        collapser = CollapseStructure(graph)
        collapser.use_advanced_analysis = False
        result = collapser.collapse_all()

        # Should still work
        assert result is not None
