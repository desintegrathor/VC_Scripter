"""
Hierarchical block structure for control flow representation.

This module provides Ghidra-style hierarchical block types for representing
structured control flow. The block hierarchy allows nested structures to be
represented as a tree, where each node is a structured block containing
child blocks.

Modeled after Ghidra's block.hh hierarchy:
- BlockBasic: Leaf node containing original CFG block
- BlockList: Sequence of blocks (fall-through)
- BlockIf: Conditional with true/false branches
- BlockWhileDo/BlockDoWhile: Loop structures
- BlockSwitch: Multi-way branch
- BlockGoto: Unstructured jump wrapper

The BlockGraph maintains the working set of blocks during collapse,
tracking edges and providing operations for pattern matching and collapse.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from ....cfg import CFG
    from ....ssa import SSAFunction


class BlockType(Enum):
    """Types of structured blocks."""
    BASIC = auto()      # Leaf block (original CFG block)
    LIST = auto()       # Sequential list of blocks
    CONDITION = auto()  # Condition evaluation (internal)
    IF = auto()         # If-then or if-then-else
    WHILE_DO = auto()   # While loop (condition at top)
    DO_WHILE = auto()   # Do-while loop (condition at bottom)
    INF_LOOP = auto()   # Infinite loop (while(1))
    SWITCH = auto()     # Switch/case
    GOTO = auto()       # Unstructured goto wrapper


class EdgeType(Enum):
    """Types of edges in the block graph."""
    NORMAL = auto()       # Regular control flow
    GOTO_EDGE = auto()    # Unstructured goto
    LOOP_EDGE = auto()    # Edge within loop
    BACK_EDGE = auto()    # Back edge to loop header
    LOOP_EXIT = auto()    # Exit from loop
    BREAK_EDGE = auto()   # Break from switch/loop
    CONTINUE_EDGE = auto()  # Continue in loop
    IRREDUCIBLE = auto()  # Irreducible control flow


@dataclass
class BlockEdge:
    """
    Edge between structured blocks.

    Tracks source, target, and edge classification for pattern matching.
    """
    source: StructuredBlock
    target: StructuredBlock
    edge_type: EdgeType = EdgeType.NORMAL
    label: Optional[str] = None  # For switch case labels

    def is_back_edge(self) -> bool:
        """Check if this is a back edge."""
        return self.edge_type == EdgeType.BACK_EDGE

    def is_goto(self) -> bool:
        """Check if this is a goto edge."""
        return self.edge_type == EdgeType.GOTO_EDGE


@dataclass
class StructuredBlock:
    """
    Base class for all structured blocks.

    Each block has:
    - A unique block_id within the graph
    - A block_type indicating its structure
    - Lists of incoming and outgoing edges
    - Optional parent reference for hierarchy
    - Set of covered original CFG block IDs
    """
    block_type: BlockType
    block_id: int = -1

    # Graph edges
    in_edges: List[BlockEdge] = field(default_factory=list)
    out_edges: List[BlockEdge] = field(default_factory=list)

    # Hierarchy
    parent: Optional[StructuredBlock] = None

    # Tracking
    is_collapsed: bool = False
    covered_blocks: Set[int] = field(default_factory=set)  # Original CFG block IDs

    def get_successors(self) -> List[StructuredBlock]:
        """Get all successor blocks."""
        return [e.target for e in self.out_edges]

    def get_predecessors(self) -> List[StructuredBlock]:
        """Get all predecessor blocks."""
        return [e.source for e in self.in_edges]

    def successor_count(self) -> int:
        """Number of successors."""
        return len(self.out_edges)

    def predecessor_count(self) -> int:
        """Number of predecessors."""
        return len(self.in_edges)

    def has_single_successor(self) -> bool:
        """Check if block has exactly one successor."""
        return len(self.out_edges) == 1

    def has_single_predecessor(self) -> bool:
        """Check if block has exactly one predecessor."""
        return len(self.in_edges) == 1

    def get_single_successor(self) -> Optional[StructuredBlock]:
        """Get the single successor, or None if not exactly one."""
        if len(self.out_edges) == 1:
            return self.out_edges[0].target
        return None

    def get_single_predecessor(self) -> Optional[StructuredBlock]:
        """Get the single predecessor, or None if not exactly one."""
        if len(self.in_edges) == 1:
            return self.in_edges[0].source
        return None


@dataclass
class BlockBasic(StructuredBlock):
    """
    Basic block - leaf node containing an original CFG block.

    This is the starting point for collapse - each CFG block becomes
    a BlockBasic, then patterns are detected and collapsed into
    higher-level structures.
    """
    original_block_id: int = -1  # CFG block ID

    def __post_init__(self):
        if self.original_block_id >= 0:
            self.covered_blocks = {self.original_block_id}


@dataclass
class BlockList(StructuredBlock):
    """
    Sequential list of blocks.

    Represents fall-through execution where blocks execute in sequence.
    Created when collapsing: A -> B where B has single predecessor A.
    """
    components: List[StructuredBlock] = field(default_factory=list)

    def add_component(self, block: StructuredBlock):
        """Add a block to the sequence."""
        self.components.append(block)
        block.parent = self
        self.covered_blocks.update(block.covered_blocks)

    def __post_init__(self):
        # Ensure covered_blocks includes all components
        for comp in self.components:
            self.covered_blocks.update(comp.covered_blocks)


@dataclass
class BlockIf(StructuredBlock):
    """
    If-then or if-then-else block.

    Structure:
        if (condition) {
            true_block
        } [else {
            false_block
        }]

    The condition_block contains the comparison, true_block executes
    when condition is true, false_block (optional) when false.
    """
    condition_block: Optional[StructuredBlock] = None
    condition_expr: Optional[str] = None
    true_block: Optional[StructuredBlock] = None
    false_block: Optional[StructuredBlock] = None  # None for if-then (no else)

    def has_else(self) -> bool:
        """Check if this if has an else branch."""
        return self.false_block is not None

    def __post_init__(self):
        if self.condition_block:
            self.covered_blocks.update(self.condition_block.covered_blocks)
        if self.true_block:
            self.covered_blocks.update(self.true_block.covered_blocks)
        if self.false_block:
            self.covered_blocks.update(self.false_block.covered_blocks)


@dataclass
class BlockWhileDo(StructuredBlock):
    """
    While loop - condition tested at top.

    Structure:
        while (condition) {
            body_block
        }

    Or as for loop:
        for (init; condition; increment) {
            body_block
        }
    """
    condition_block: Optional[StructuredBlock] = None
    condition_expr: Optional[str] = None
    body_block: Optional[StructuredBlock] = None

    # For loop conversion
    is_for_loop: bool = False
    for_init: Optional[str] = None
    for_increment: Optional[str] = None

    def __post_init__(self):
        if self.condition_block:
            self.covered_blocks.update(self.condition_block.covered_blocks)
        if self.body_block:
            self.covered_blocks.update(self.body_block.covered_blocks)


@dataclass
class BlockDoWhile(StructuredBlock):
    """
    Do-while loop - condition tested at bottom.

    Structure:
        do {
            body_block
        } while (condition);
    """
    body_block: Optional[StructuredBlock] = None
    condition_block: Optional[StructuredBlock] = None
    condition_expr: Optional[str] = None

    def __post_init__(self):
        if self.body_block:
            self.covered_blocks.update(self.body_block.covered_blocks)
        if self.condition_block:
            self.covered_blocks.update(self.condition_block.covered_blocks)


@dataclass
class BlockInfLoop(StructuredBlock):
    """
    Infinite loop - while(1) or for(;;).

    Structure:
        while (1) {
            body_block
        }
    """
    body_block: Optional[StructuredBlock] = None

    def __post_init__(self):
        if self.body_block:
            self.covered_blocks.update(self.body_block.covered_blocks)


@dataclass
class SwitchCase:
    """A single case in a switch statement."""
    value: int
    body_block: Optional[StructuredBlock] = None
    is_default: bool = False
    has_break: bool = True
    fall_through_to: Optional[int] = None  # Next case value if fall-through


@dataclass
class BlockSwitch(StructuredBlock):
    """
    Switch/case block.

    Structure:
        switch (test_var) {
            case 1: ...
            case 2: ...
            default: ...
        }
    """
    header_block: Optional[StructuredBlock] = None
    test_var: Optional[str] = None
    cases: List[SwitchCase] = field(default_factory=list)
    default_case: Optional[SwitchCase] = None

    def __post_init__(self):
        if self.header_block:
            self.covered_blocks.update(self.header_block.covered_blocks)
        for case in self.cases:
            if case.body_block:
                self.covered_blocks.update(case.body_block.covered_blocks)
        if self.default_case and self.default_case.body_block:
            self.covered_blocks.update(self.default_case.body_block.covered_blocks)


@dataclass
class BlockGoto(StructuredBlock):
    """
    Unstructured goto wrapper.

    Used when control flow cannot be represented with structured constructs.
    Wraps a block that has an unstructured jump to a target.
    """
    wrapped_block: Optional[StructuredBlock] = None
    goto_target: Optional[StructuredBlock] = None
    target_label: Optional[str] = None

    def __post_init__(self):
        if self.wrapped_block:
            self.covered_blocks.update(self.wrapped_block.covered_blocks)


class BlockGraph:
    """
    Working graph of structured blocks.

    Maintains the set of blocks being collapsed, with operations for:
    - Adding/removing blocks
    - Redirecting edges during collapse
    - Tracking which blocks have been collapsed
    - Finding patterns for collapse rules
    """

    def __init__(self):
        self.blocks: Dict[int, StructuredBlock] = {}
        self.entry_block: Optional[StructuredBlock] = None
        self.root: Optional[StructuredBlock] = None
        self._next_block_id: int = 0

        # Mapping from original CFG block IDs to structured blocks
        self.cfg_to_struct: Dict[int, StructuredBlock] = {}

    def _allocate_block_id(self) -> int:
        """Allocate a new unique block ID."""
        block_id = self._next_block_id
        self._next_block_id += 1
        return block_id

    def add_block(self, block: StructuredBlock) -> StructuredBlock:
        """Add a block to the graph."""
        if block.block_id < 0:
            block.block_id = self._allocate_block_id()
        self.blocks[block.block_id] = block
        return block

    def remove_block(self, block: StructuredBlock):
        """Remove a block from the graph."""
        if block.block_id in self.blocks:
            del self.blocks[block.block_id]
        block.is_collapsed = True

    def replace_block(self, old_block: StructuredBlock, new_block: StructuredBlock):
        """
        Replace old_block with new_block, redirecting all edges.

        This is the core operation during collapse - the old block(s) are
        replaced with a new composite block, and all external edges are
        redirected to the new block.
        """
        # Add new block
        self.add_block(new_block)

        # Redirect incoming edges to new block
        for edge in old_block.in_edges:
            if edge.source != old_block and not edge.source.is_collapsed:
                # Update source's out_edges
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == old_block:
                        edge.source.out_edges[i] = BlockEdge(
                            source=edge.source,
                            target=new_block,
                            edge_type=out_edge.edge_type,
                            label=out_edge.label
                        )
                        new_block.in_edges.append(edge.source.out_edges[i])

        # Redirect outgoing edges from new block
        for edge in old_block.out_edges:
            if edge.target != old_block and not edge.target.is_collapsed:
                new_edge = BlockEdge(
                    source=new_block,
                    target=edge.target,
                    edge_type=edge.edge_type,
                    label=edge.label
                )
                new_block.out_edges.append(new_edge)

                # Update target's in_edges
                for i, in_edge in enumerate(edge.target.in_edges):
                    if in_edge.source == old_block:
                        edge.target.in_edges[i] = new_edge

        # Update entry block reference
        if self.entry_block == old_block:
            self.entry_block = new_block

        # Remove old block
        self.remove_block(old_block)

    def merge_blocks(self, first: StructuredBlock, second: StructuredBlock) -> BlockList:
        """
        Merge two sequential blocks into a BlockList.

        Precondition: first has single successor second, second has single predecessor first.
        """
        # Create new list block
        list_block = BlockList(
            block_type=BlockType.LIST,
            block_id=self._allocate_block_id(),
        )

        # Handle case where first is already a list
        if isinstance(first, BlockList):
            list_block.components = first.components.copy()
        else:
            list_block.components = [first]

        # Handle case where second is already a list
        if isinstance(second, BlockList):
            list_block.components.extend(second.components)
        else:
            list_block.components.append(second)

        # Update covered blocks
        list_block.covered_blocks = first.covered_blocks | second.covered_blocks

        # Set parent references
        for comp in list_block.components:
            comp.parent = list_block

        # Copy incoming edges from first (excluding edge from first to second)
        for edge in first.in_edges:
            if edge.source != second:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=list_block,
                    edge_type=edge.edge_type,
                    label=edge.label
                )
                list_block.in_edges.append(new_edge)
                # Update source's out_edges
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == first:
                        edge.source.out_edges[i] = new_edge

        # Copy outgoing edges from second (excluding edge from first to second)
        for edge in second.out_edges:
            if edge.target != first:
                new_edge = BlockEdge(
                    source=list_block,
                    target=edge.target,
                    edge_type=edge.edge_type,
                    label=edge.label
                )
                list_block.out_edges.append(new_edge)
                # Update target's in_edges
                for i, in_edge in enumerate(edge.target.in_edges):
                    if in_edge.source == second:
                        edge.target.in_edges[i] = new_edge

        # Add new block and remove old ones
        self.blocks[list_block.block_id] = list_block

        if self.entry_block == first:
            self.entry_block = list_block

        self.remove_block(first)
        self.remove_block(second)

        return list_block

    def get_uncollapsed_blocks(self) -> List[StructuredBlock]:
        """Get all blocks that haven't been collapsed."""
        return [b for b in self.blocks.values() if not b.is_collapsed]

    def is_fully_collapsed(self) -> bool:
        """Check if graph is fully collapsed to a single block."""
        uncollapsed = self.get_uncollapsed_blocks()
        return len(uncollapsed) == 1

    @classmethod
    def from_cfg(cls, cfg: "CFG", ssa_func: "SSAFunction") -> "BlockGraph":
        """
        Build a BlockGraph from a CFG.

        Creates a BlockBasic for each CFG block and connects them with edges.
        """
        graph = cls()

        # Create basic blocks for each CFG block
        for block_id, cfg_block in cfg.blocks.items():
            basic = BlockBasic(
                block_type=BlockType.BASIC,
                block_id=graph._allocate_block_id(),
                original_block_id=block_id,
            )
            graph.blocks[basic.block_id] = basic
            graph.cfg_to_struct[block_id] = basic

        # Create edges
        for block_id, cfg_block in cfg.blocks.items():
            source = graph.cfg_to_struct[block_id]
            for succ_id in cfg_block.successors:
                if succ_id in graph.cfg_to_struct:
                    target = graph.cfg_to_struct[succ_id]

                    # Determine edge type
                    edge_type = EdgeType.NORMAL
                    if succ_id in getattr(cfg_block, 'back_edge_targets', set()):
                        edge_type = EdgeType.BACK_EDGE

                    edge = BlockEdge(source=source, target=target, edge_type=edge_type)
                    source.out_edges.append(edge)
                    target.in_edges.append(edge)

        # Set entry block
        if cfg.entry_block in graph.cfg_to_struct:
            graph.entry_block = graph.cfg_to_struct[cfg.entry_block]

        return graph

    @classmethod
    def from_cfg_subset(
        cls,
        cfg: "CFG",
        ssa_func: "SSAFunction",
        block_ids: Set[int],
        entry_block_id: int
    ) -> "BlockGraph":
        """
        Build a BlockGraph from a subset of CFG blocks (for single function).

        Args:
            cfg: The full CFG
            ssa_func: SSA function data
            block_ids: Set of CFG block IDs to include
            entry_block_id: The entry block ID for this function

        Returns:
            BlockGraph containing only the specified blocks
        """
        graph = cls()

        # Create basic blocks only for blocks in the subset
        for block_id in block_ids:
            if block_id not in cfg.blocks:
                continue
            cfg_block = cfg.blocks[block_id]
            basic = BlockBasic(
                block_type=BlockType.BASIC,
                block_id=graph._allocate_block_id(),
                original_block_id=block_id,
            )
            graph.blocks[basic.block_id] = basic
            graph.cfg_to_struct[block_id] = basic

        # Create edges only between blocks in the subset
        for block_id in block_ids:
            if block_id not in cfg.blocks:
                continue
            cfg_block = cfg.blocks[block_id]
            source = graph.cfg_to_struct[block_id]

            for succ_id in cfg_block.successors:
                # Only create edge if successor is in our subset
                if succ_id in graph.cfg_to_struct:
                    target = graph.cfg_to_struct[succ_id]

                    # Determine edge type
                    edge_type = EdgeType.NORMAL
                    if succ_id in getattr(cfg_block, 'back_edge_targets', set()):
                        edge_type = EdgeType.BACK_EDGE

                    edge = BlockEdge(source=source, target=target, edge_type=edge_type)
                    source.out_edges.append(edge)
                    target.in_edges.append(edge)

        # Set entry block
        if entry_block_id in graph.cfg_to_struct:
            graph.entry_block = graph.cfg_to_struct[entry_block_id]

        return graph
