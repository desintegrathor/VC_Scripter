"""
Tests for the hierarchical block structure module.
"""

import pytest

from vcdecomp.core.ir.structure.blocks.hierarchy import (
    BlockType,
    EdgeType,
    StructuredBlock,
    BlockBasic,
    BlockList,
    BlockIf,
    BlockWhileDo,
    BlockDoWhile,
    BlockSwitch,
    BlockGoto,
    BlockGraph,
    BlockEdge,
    SwitchCase,
)


class TestBlockTypes:
    """Test block type creation and basic properties."""

    def test_block_basic_creation(self):
        """Test creating a basic block."""
        block = BlockBasic(
            block_type=BlockType.BASIC,
            block_id=0,
            original_block_id=5,
        )
        assert block.block_type == BlockType.BASIC
        assert block.block_id == 0
        assert block.original_block_id == 5
        assert block.covered_blocks == {5}

    def test_block_list_creation(self):
        """Test creating a list block."""
        comp1 = BlockBasic(block_type=BlockType.BASIC, block_id=0, original_block_id=1)
        comp2 = BlockBasic(block_type=BlockType.BASIC, block_id=1, original_block_id=2)

        list_block = BlockList(
            block_type=BlockType.LIST,
            block_id=2,
        )
        list_block.add_component(comp1)
        list_block.add_component(comp2)

        assert list_block.block_type == BlockType.LIST
        assert len(list_block.components) == 2
        assert list_block.covered_blocks == {1, 2}

    def test_block_if_creation(self):
        """Test creating an if block."""
        cond_block = BlockBasic(block_type=BlockType.BASIC, block_id=0, original_block_id=1)
        true_block = BlockBasic(block_type=BlockType.BASIC, block_id=1, original_block_id=2)
        false_block = BlockBasic(block_type=BlockType.BASIC, block_id=2, original_block_id=3)

        if_block = BlockIf(
            block_type=BlockType.IF,
            block_id=3,
            condition_block=cond_block,
            true_block=true_block,
            false_block=false_block,
            condition_expr="x > 0",
        )

        assert if_block.block_type == BlockType.IF
        assert if_block.condition_expr == "x > 0"
        assert if_block.has_else()
        assert if_block.true_block == true_block
        assert if_block.false_block == false_block

    def test_block_if_no_else(self):
        """Test if block without else branch."""
        if_block = BlockIf(
            block_type=BlockType.IF,
            block_id=0,
            condition_expr="x > 0",
            true_block=BlockBasic(block_type=BlockType.BASIC, block_id=1, original_block_id=1),
            false_block=None,
        )

        assert not if_block.has_else()

    def test_block_while_do_creation(self):
        """Test creating a while loop block."""
        while_block = BlockWhileDo(
            block_type=BlockType.WHILE_DO,
            block_id=0,
            condition_expr="i < 10",
            body_block=BlockBasic(block_type=BlockType.BASIC, block_id=1, original_block_id=1),
        )

        assert while_block.block_type == BlockType.WHILE_DO
        assert while_block.condition_expr == "i < 10"
        assert not while_block.is_for_loop

    def test_block_while_as_for_loop(self):
        """Test while block converted to for loop."""
        while_block = BlockWhileDo(
            block_type=BlockType.WHILE_DO,
            block_id=0,
            condition_expr="i < 10",
            is_for_loop=True,
            for_init="i = 0",
            for_increment="i++",
        )

        assert while_block.is_for_loop
        assert while_block.for_init == "i = 0"
        assert while_block.for_increment == "i++"


class TestBlockEdges:
    """Test edge creation and properties."""

    def test_edge_creation(self):
        """Test creating an edge."""
        block1 = BlockBasic(block_type=BlockType.BASIC, block_id=0, original_block_id=1)
        block2 = BlockBasic(block_type=BlockType.BASIC, block_id=1, original_block_id=2)

        edge = BlockEdge(source=block1, target=block2)

        assert edge.source == block1
        assert edge.target == block2
        assert edge.edge_type == EdgeType.NORMAL

    def test_edge_with_type(self):
        """Test creating an edge with specific type."""
        block1 = BlockBasic(block_type=BlockType.BASIC, block_id=0, original_block_id=1)
        block2 = BlockBasic(block_type=BlockType.BASIC, block_id=1, original_block_id=2)

        edge = BlockEdge(source=block1, target=block2, edge_type=EdgeType.BACK_EDGE)

        assert edge.edge_type == EdgeType.BACK_EDGE


class TestBlockGraph:
    """Test block graph operations."""

    def test_allocate_block_id(self):
        """Test block ID allocation."""
        graph = BlockGraph()

        id1 = graph._allocate_block_id()
        id2 = graph._allocate_block_id()
        id3 = graph._allocate_block_id()

        assert id1 == 0
        assert id2 == 1
        assert id3 == 2

    def test_add_block(self):
        """Test adding blocks to graph."""
        graph = BlockGraph()

        block = BlockBasic(block_type=BlockType.BASIC, block_id=-1, original_block_id=1)
        graph.add_block(block)

        assert block.block_id >= 0
        assert block.block_id in graph.blocks

    def test_remove_block(self):
        """Test removing blocks from graph."""
        graph = BlockGraph()

        block = BlockBasic(block_type=BlockType.BASIC, block_id=0, original_block_id=1)
        graph.blocks[0] = block

        graph.remove_block(block)

        assert 0 not in graph.blocks
        assert block.is_collapsed

    def test_merge_blocks(self):
        """Test merging two sequential blocks."""
        graph = BlockGraph()

        block1 = BlockBasic(block_type=BlockType.BASIC, block_id=0, original_block_id=1)
        block2 = BlockBasic(block_type=BlockType.BASIC, block_id=1, original_block_id=2)

        graph.blocks[0] = block1
        graph.blocks[1] = block2

        # Create edge
        edge = BlockEdge(source=block1, target=block2)
        block1.out_edges.append(edge)
        block2.in_edges.append(edge)

        # Merge
        list_block = graph.merge_blocks(block1, block2)

        assert isinstance(list_block, BlockList)
        assert len(list_block.components) == 2
        assert list_block.covered_blocks == {1, 2}
        assert block1.is_collapsed
        assert block2.is_collapsed

    def test_get_uncollapsed_blocks(self):
        """Test getting uncollapsed blocks."""
        graph = BlockGraph()

        block1 = BlockBasic(block_type=BlockType.BASIC, block_id=0, original_block_id=1)
        block2 = BlockBasic(block_type=BlockType.BASIC, block_id=1, original_block_id=2)
        block2.is_collapsed = True

        graph.blocks[0] = block1
        graph.blocks[1] = block2

        uncollapsed = graph.get_uncollapsed_blocks()

        assert len(uncollapsed) == 1
        assert block1 in uncollapsed
        assert block2 not in uncollapsed

    def test_is_fully_collapsed_true(self):
        """Test fully collapsed detection - true case."""
        graph = BlockGraph()
        block = BlockBasic(block_type=BlockType.BASIC, block_id=0, original_block_id=1)
        graph.blocks[0] = block
        graph.root = block

        assert graph.is_fully_collapsed()

    def test_is_fully_collapsed_false(self):
        """Test fully collapsed detection - false case."""
        graph = BlockGraph()
        block1 = BlockBasic(block_type=BlockType.BASIC, block_id=0, original_block_id=1)
        block2 = BlockBasic(block_type=BlockType.BASIC, block_id=1, original_block_id=2)

        graph.blocks[0] = block1
        graph.blocks[1] = block2

        assert not graph.is_fully_collapsed()


class TestSwitchCase:
    """Test switch case structure."""

    def test_switch_case_creation(self):
        """Test creating a switch case."""
        body = BlockBasic(block_type=BlockType.BASIC, block_id=0, original_block_id=1)

        case = SwitchCase(
            value=42,
            body_block=body,
            has_break=True,
        )

        assert case.value == 42
        assert not case.is_default
        assert case.has_break

    def test_default_case(self):
        """Test creating a default case."""
        case = SwitchCase(
            value=-1,
            is_default=True,
        )

        assert case.is_default
        assert case.value == -1


class TestBlockSwitch:
    """Test switch block structure."""

    def test_switch_creation(self):
        """Test creating a switch block."""
        case1 = SwitchCase(value=1)
        case2 = SwitchCase(value=2)
        default = SwitchCase(value=-1, is_default=True)

        switch = BlockSwitch(
            block_type=BlockType.SWITCH,
            block_id=0,
            test_var="x",
            cases=[case1, case2],
            default_case=default,
        )

        assert switch.block_type == BlockType.SWITCH
        assert switch.test_var == "x"
        assert len(switch.cases) == 2
        assert switch.default_case == default
