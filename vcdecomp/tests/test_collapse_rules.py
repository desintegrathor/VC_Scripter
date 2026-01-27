"""
Tests for the collapse rules module and TraceDAG algorithm.
"""

import pytest

from vcdecomp.core.ir.structure.blocks.hierarchy import (
    BlockType,
    EdgeType,
    BlockBasic,
    BlockList,
    BlockIf,
    BlockGraph,
    BlockEdge,
)
from vcdecomp.core.ir.structure.collapse.rules import (
    RuleBlockCat,
    RuleBlockProperIf,
    RuleBlockIfElse,
    DEFAULT_RULES,
)
from vcdecomp.core.ir.structure.collapse.trace_dag import (
    TraceDAG,
    BranchPoint,
    BlockTrace,
    BadEdgeScore,
)


def create_test_graph():
    """Create a simple test graph."""
    graph = BlockGraph()
    return graph


def add_block_to_graph(graph, cfg_block_id):
    """Add a basic block to the graph."""
    block = BlockBasic(
        block_type=BlockType.BASIC,
        block_id=graph._allocate_block_id(),
        original_block_id=cfg_block_id,
    )
    graph.blocks[block.block_id] = block
    graph.cfg_to_struct[cfg_block_id] = block
    return block


def add_edge(source, target, edge_type=EdgeType.NORMAL):
    """Add an edge between two blocks."""
    edge = BlockEdge(source=source, target=target, edge_type=edge_type)
    source.out_edges.append(edge)
    target.in_edges.append(edge)
    return edge


class TestRuleBlockCat:
    """Test the sequential block collapse rule."""

    def test_matches_simple_sequence(self):
        """Test that RuleBlockCat matches a simple sequence."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)
        block2 = add_block_to_graph(graph, 2)
        add_edge(block1, block2)

        rule = RuleBlockCat()
        assert rule.matches(graph, block1)

    def test_no_match_multiple_successors(self):
        """Test that RuleBlockCat doesn't match blocks with multiple successors."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)
        block2 = add_block_to_graph(graph, 2)
        block3 = add_block_to_graph(graph, 3)
        add_edge(block1, block2)
        add_edge(block1, block3)

        rule = RuleBlockCat()
        assert not rule.matches(graph, block1)

    def test_no_match_multiple_predecessors(self):
        """Test that RuleBlockCat doesn't match when successor has multiple predecessors."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)
        block2 = add_block_to_graph(graph, 2)
        block3 = add_block_to_graph(graph, 3)
        add_edge(block1, block3)
        add_edge(block2, block3)

        rule = RuleBlockCat()
        assert not rule.matches(graph, block1)

    def test_no_match_self_loop(self):
        """Test that RuleBlockCat doesn't match self-loops."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)
        add_edge(block1, block1)

        rule = RuleBlockCat()
        assert not rule.matches(graph, block1)

    def test_no_match_back_edge(self):
        """Test that RuleBlockCat doesn't match back edges."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)
        block2 = add_block_to_graph(graph, 2)
        add_edge(block1, block2, EdgeType.BACK_EDGE)

        rule = RuleBlockCat()
        assert not rule.matches(graph, block1)

    def test_apply_creates_list(self):
        """Test that RuleBlockCat creates a BlockList."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)
        block2 = add_block_to_graph(graph, 2)
        add_edge(block1, block2)
        graph.entry_block = block1

        rule = RuleBlockCat()
        result = rule.apply(graph, block1)

        assert isinstance(result, BlockList)
        assert len(result.components) == 2
        assert result.covered_blocks == {1, 2}


class TestRuleBlockProperIf:
    """Test the proper if (if-then) collapse rule."""

    def test_matches_if_then(self):
        """Test that RuleBlockProperIf matches if-then pattern."""
        graph = create_test_graph()

        # Create: cond -> body -> merge
        #         cond ------> merge
        cond = add_block_to_graph(graph, 1)
        body = add_block_to_graph(graph, 2)
        merge = add_block_to_graph(graph, 3)

        add_edge(cond, body)  # true branch
        add_edge(cond, merge)  # false branch (skip)
        add_edge(body, merge)

        rule = RuleBlockProperIf()
        assert rule.matches(graph, cond)

    def test_no_match_if_else(self):
        """Test that RuleBlockProperIf doesn't match if-else pattern."""
        graph = create_test_graph()

        # Create: cond -> true_body -> merge
        #         cond -> false_body -> merge
        cond = add_block_to_graph(graph, 1)
        true_body = add_block_to_graph(graph, 2)
        false_body = add_block_to_graph(graph, 3)
        merge = add_block_to_graph(graph, 4)

        add_edge(cond, true_body)
        add_edge(cond, false_body)
        add_edge(true_body, merge)
        add_edge(false_body, merge)

        rule = RuleBlockProperIf()
        # This should NOT match because it's a full if-else (both branches have content)
        assert not rule.matches(graph, cond)


class TestRuleBlockIfElse:
    """Test the if-else collapse rule."""

    def test_matches_if_else(self):
        """Test that RuleBlockIfElse matches if-else pattern."""
        graph = create_test_graph()

        # Create: cond -> true_body -> merge
        #         cond -> false_body -> merge
        cond = add_block_to_graph(graph, 1)
        true_body = add_block_to_graph(graph, 2)
        false_body = add_block_to_graph(graph, 3)
        merge = add_block_to_graph(graph, 4)

        add_edge(cond, true_body)
        add_edge(cond, false_body)
        add_edge(true_body, merge)
        add_edge(false_body, merge)

        rule = RuleBlockIfElse()
        assert rule.matches(graph, cond)

    def test_no_match_branches_different_targets(self):
        """Test that RuleBlockIfElse doesn't match when branches go to different targets."""
        graph = create_test_graph()

        cond = add_block_to_graph(graph, 1)
        true_body = add_block_to_graph(graph, 2)
        false_body = add_block_to_graph(graph, 3)
        merge1 = add_block_to_graph(graph, 4)
        merge2 = add_block_to_graph(graph, 5)

        add_edge(cond, true_body)
        add_edge(cond, false_body)
        add_edge(true_body, merge1)
        add_edge(false_body, merge2)  # Different target

        rule = RuleBlockIfElse()
        assert not rule.matches(graph, cond)

    def test_apply_creates_if_block(self):
        """Test that RuleBlockIfElse creates a BlockIf."""
        graph = create_test_graph()

        cond = add_block_to_graph(graph, 1)
        true_body = add_block_to_graph(graph, 2)
        false_body = add_block_to_graph(graph, 3)
        merge = add_block_to_graph(graph, 4)

        add_edge(cond, true_body)
        add_edge(cond, false_body)
        add_edge(true_body, merge)
        add_edge(false_body, merge)

        graph.entry_block = cond

        rule = RuleBlockIfElse()
        result = rule.apply(graph, cond)

        assert isinstance(result, BlockIf)
        assert result.condition_block == cond
        assert result.true_block == true_body
        assert result.false_block == false_body
        assert result.covered_blocks == {1, 2, 3}


class TestDefaultRules:
    """Test the default rule set."""

    def test_default_rules_exist(self):
        """Test that default rules are defined."""
        assert len(DEFAULT_RULES) > 0

    def test_default_rules_have_names(self):
        """Test that all default rules have names."""
        for rule in DEFAULT_RULES:
            assert rule.name
            assert isinstance(rule.name, str)


class TestBranchPoint:
    """Test the BranchPoint class."""

    def test_mark_path_toggles_marks(self):
        """Test that mark_path toggles marks from BP to root."""
        # Create a hierarchy: root -> bp1 -> bp2
        root = BranchPoint(top=None, depth=0)
        bp1 = BranchPoint(top=None, parent=root, depth=1)
        bp2 = BranchPoint(top=None, parent=bp1, depth=2)

        # Initially all unmarked
        assert not root.is_marked
        assert not bp1.is_marked
        assert not bp2.is_marked

        # Mark path from bp2
        bp2.mark_path()
        assert root.is_marked
        assert bp1.is_marked
        assert bp2.is_marked

        # Mark again to unmark
        bp2.mark_path()
        assert not root.is_marked
        assert not bp1.is_marked
        assert not bp2.is_marked

    def test_distance_same_bp(self):
        """Test distance to self is 0."""
        bp = BranchPoint(top=None, depth=0)
        bp.mark_path()
        assert bp.distance(bp) == 0
        bp.mark_path()

    def test_distance_parent_child(self):
        """Test distance between parent and child."""
        root = BranchPoint(top=None, depth=0)
        bp1 = BranchPoint(top=None, parent=root, depth=1)
        bp2 = BranchPoint(top=None, parent=bp1, depth=2)

        # Distance from bp2 to root
        bp2.mark_path()
        assert bp2.distance(root) == 2  # bp2 -> bp1 -> root
        bp2.mark_path()

        # Distance from bp1 to root
        bp1.mark_path()
        assert bp1.distance(root) == 1
        bp1.mark_path()

    def test_distance_siblings(self):
        """Test distance between siblings."""
        root = BranchPoint(top=None, depth=0)
        bp1 = BranchPoint(top=None, parent=root, depth=1)
        bp2 = BranchPoint(top=None, parent=root, depth=1)

        # Distance between siblings (LCA is root)
        bp1.mark_path()
        assert bp1.distance(bp2) == 2  # bp1 -> root -> bp2
        bp1.mark_path()


class TestBlockTrace:
    """Test the BlockTrace class."""

    def test_identity_equality(self):
        """Test that BlockTrace uses identity for equality."""
        bp = BranchPoint(top=None, depth=0)
        trace1 = BlockTrace(top=bp, pathout=0)
        trace2 = BlockTrace(top=bp, pathout=0)

        # Same attributes but different identity
        assert trace1 != trace2
        assert trace1 == trace1


class TestBadEdgeScore:
    """Test the BadEdgeScore class."""

    def test_sorting_by_exit_block(self):
        """Test that scores sort by exit block first."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)
        block2 = add_block_to_graph(graph, 2)

        bp = BranchPoint(top=None, depth=0)
        trace1 = BlockTrace(top=bp, pathout=0)
        trace2 = BlockTrace(top=bp, pathout=1)

        score1 = BadEdgeScore(trace=trace1, exitproto=block2)
        score2 = BadEdgeScore(trace=trace2, exitproto=block1)

        # block1.block_id < block2.block_id, so score2 should be less
        assert score2 < score1

    def test_compare_final_sibling_edge(self):
        """Test that more sibling edges = less likely to be bad."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)

        bp = BranchPoint(top=None, depth=0)
        trace1 = BlockTrace(top=bp, pathout=0)
        trace2 = BlockTrace(top=bp, pathout=1)

        score1 = BadEdgeScore(trace=trace1, exitproto=block1, siblingedge=0)
        score2 = BadEdgeScore(trace=trace2, exitproto=block1, siblingedge=2)

        # More sibling edges = less likely to be bad
        # compare_final returns True if self is LESS likely bad
        assert score2.compare_final(score1)  # score2 (2 siblings) is less bad
        assert not score1.compare_final(score2)  # score1 (0 siblings) is more bad

    def test_compare_final_terminal(self):
        """Test terminal vs non-terminal edge comparison."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)

        bp = BranchPoint(top=None, depth=0)
        trace1 = BlockTrace(top=bp, pathout=0)
        trace2 = BlockTrace(top=bp, pathout=1)

        score1 = BadEdgeScore(trace=trace1, exitproto=block1, terminal=0)
        score2 = BadEdgeScore(trace=trace2, exitproto=block1, terminal=1)

        # Per Ghidra: non-terminal (terminal=0) is LESS likely to be the bad edge
        # because switches frequently exit to terminal nodes (return blocks)
        assert score1.compare_final(score2)  # score1 (non-terminal) is less bad
        assert not score2.compare_final(score1)  # score2 (terminal) is more bad


class TestTraceDAG:
    """Test the TraceDAG algorithm."""

    def test_empty_graph(self):
        """Test TraceDAG on empty graph."""
        graph = create_test_graph()
        trace_dag = TraceDAG(graph)
        result = trace_dag.find_goto_edges()
        assert result == []

    def test_linear_sequence(self):
        """Test TraceDAG on linear sequence (no gotos needed)."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)
        block2 = add_block_to_graph(graph, 2)
        block3 = add_block_to_graph(graph, 3)

        add_edge(block1, block2)
        add_edge(block2, block3)
        graph.entry_block = block1

        trace_dag = TraceDAG(graph)
        result = trace_dag.find_goto_edges()
        assert result == []

    def test_diamond_pattern(self):
        """Test TraceDAG on diamond pattern (if-else, no gotos needed)."""
        graph = create_test_graph()
        entry = add_block_to_graph(graph, 1)
        true_branch = add_block_to_graph(graph, 2)
        false_branch = add_block_to_graph(graph, 3)
        merge = add_block_to_graph(graph, 4)

        add_edge(entry, true_branch)
        add_edge(entry, false_branch)
        add_edge(true_branch, merge)
        add_edge(false_branch, merge)
        graph.entry_block = entry

        trace_dag = TraceDAG(graph)
        result = trace_dag.find_goto_edges()
        # Diamond pattern is structurable - no gotos needed
        assert result == []

    def test_irreducible_pattern(self):
        """Test TraceDAG on irreducible control flow."""
        graph = create_test_graph()
        block1 = add_block_to_graph(graph, 1)
        block2 = add_block_to_graph(graph, 2)
        block3 = add_block_to_graph(graph, 3)

        # Create irreducible pattern: 1->2, 1->3, 2->3, 3->2
        add_edge(block1, block2)
        add_edge(block1, block3)
        add_edge(block2, block3)
        add_edge(block3, block2)
        graph.entry_block = block1

        trace_dag = TraceDAG(graph)
        result = trace_dag.find_goto_edges()
        # Should identify at least one goto edge
        assert len(result) >= 1
