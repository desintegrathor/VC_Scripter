"""
Tests for the collapse rules module.
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
