"""
Loop analysis using dominator-based algorithms.

This module provides loop detection and analysis using dominator trees,
following Ghidra's LoopBody structure in blockaction.cc.

Key concepts:
- Loop head: Entry point to the loop (target of back edge)
- Loop tail: Block with back edge to head
- Loop body: All blocks dominated by head that can reach tail
- Loop exit: Block outside loop reachable from loop body
- Natural loop: Loop with single entry point (head)

Algorithm:
1. Detect back edges using dominator analysis
2. For each back edge (tail -> head), compute loop body:
   - Start with blocks reachable from head
   - Include blocks that can reach tail without leaving through head
3. Identify loop exits (edges leaving loop body)
4. Handle nested loops by tracking containment relationships
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, TYPE_CHECKING
import logging

from ..blocks.hierarchy import (
    BlockGraph,
    StructuredBlock,
    BlockEdge,
    EdgeType,
)
from .dominance import DominatorAnalysis

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


@dataclass
class LoopBody:
    """
    Represents a natural loop in the control flow graph.

    A loop is defined by:
    - head: The loop header (entry point)
    - tails: Blocks with back edges to the head
    - body: Set of blocks in the loop
    - exits: Edges that leave the loop
    """
    head: StructuredBlock
    tails: List[StructuredBlock] = field(default_factory=list)
    body: Set[int] = field(default_factory=set)  # Block IDs in loop body
    exits: List[Tuple[StructuredBlock, StructuredBlock]] = field(default_factory=list)
    depth: int = 0  # Nesting depth (0 = outermost)
    container: Optional['LoopBody'] = None  # Immediately containing loop

    def add_tail(self, tail: StructuredBlock) -> None:
        """Add a tail block (has back edge to head)."""
        if tail not in self.tails:
            self.tails.append(tail)

    def contains_block(self, block: StructuredBlock) -> bool:
        """Check if a block is in the loop body."""
        return block.block_id in self.body

    def is_exit_edge(self, source: StructuredBlock, target: StructuredBlock) -> bool:
        """Check if an edge exits the loop."""
        return (source.block_id in self.body) and (target.block_id not in self.body)


class LoopAnalysis:
    """
    Comprehensive loop analysis using dominator trees.

    Detects natural loops, computes loop bodies, identifies exits,
    and tracks nesting relationships.
    """

    def __init__(self, graph: BlockGraph, dom_analysis: DominatorAnalysis):
        """
        Initialize loop analysis.

        Args:
            graph: The block graph to analyze
            dom_analysis: Pre-computed dominator analysis
        """
        self.graph = graph
        self.dom = dom_analysis
        self.loops: List[LoopBody] = []
        self.block_to_loops: Dict[int, List[LoopBody]] = {}  # Which loops contain each block

    def analyze(self) -> List[LoopBody]:
        """
        Run full loop analysis.

        Returns:
            List of detected loops, sorted by nesting depth (innermost first)
        """
        self._detect_loops()
        self._compute_loop_bodies()
        self._identify_exits()
        self._compute_nesting()
        self._sort_by_depth()
        return self.loops

    def _detect_loops(self) -> None:
        """
        Detect loops by finding back edges.

        A back edge is an edge (tail -> head) where head dominates tail.
        This indicates a loop with head as the loop header.
        """
        self.loops.clear()
        loop_heads: Dict[int, LoopBody] = {}  # Map from head block ID to LoopBody

        # Find all back edges
        for block in self.graph.blocks.values():
            for edge in block.out_edges:
                target = edge.target

                # Check if this is a back edge (target dominates source)
                if self.dom.dominates(target, block):
                    # Found a back edge: block -> target
                    head = target
                    tail = block

                    # Mark edge as back edge
                    edge.edge_type = EdgeType.BACK_EDGE

                    # Get or create LoopBody for this head
                    if head.block_id not in loop_heads:
                        loop_body = LoopBody(head=head)
                        loop_heads[head.block_id] = loop_body
                        self.loops.append(loop_body)
                    else:
                        loop_body = loop_heads[head.block_id]

                    # Add this tail
                    loop_body.add_tail(tail)

                    logger.debug(f"Found loop: head={head.block_id}, tail={tail.block_id}")

    def _compute_loop_bodies(self) -> None:
        """
        Compute the body of each loop.

        The loop body includes all blocks that:
        1. Are dominated by the loop head
        2. Can reach a loop tail without leaving the loop
        """
        for loop in self.loops:
            self._compute_single_loop_body(loop)

    def _compute_single_loop_body(self, loop: LoopBody) -> None:
        """
        Compute body for a single loop.

        Algorithm:
        1. Start with all blocks dominated by head
        2. Do backward reachability from tails
        3. Body = dominated ∩ reachable
        """
        # Get all blocks dominated by head
        dominated = self.dom.get_dominated_set(loop.head)

        # Compute blocks reachable from tails (backward search)
        reachable: Set[int] = set()
        worklist: List[StructuredBlock] = list(loop.tails)
        visited: Set[int] = set()

        while worklist:
            block = worklist.pop()
            if block.block_id in visited:
                continue
            visited.add(block.block_id)

            # Add to reachable if dominated by head
            if block.block_id in dominated:
                reachable.add(block.block_id)

                # Add predecessors (but stop at head)
                if block.block_id != loop.head.block_id:
                    for edge in block.in_edges:
                        pred = edge.source
                        if pred.block_id not in visited:
                            worklist.append(pred)

        # Loop body is the reachable dominated set
        loop.body = reachable

        # Track which loops contain each block
        for block_id in loop.body:
            if block_id not in self.block_to_loops:
                self.block_to_loops[block_id] = []
            self.block_to_loops[block_id].append(loop)

        logger.debug(f"Loop {loop.head.block_id}: body size = {len(loop.body)}")

    def _identify_exits(self) -> None:
        """
        Identify exit edges for each loop.

        An exit edge is an edge from a block in the loop body to a block
        outside the loop body.
        """
        for loop in self.loops:
            loop.exits.clear()

            for block_id in loop.body:
                block = self.graph.blocks.get(block_id)
                if block is None:
                    continue

                for edge in block.out_edges:
                    target = edge.target

                    # Skip back edges
                    if edge.edge_type == EdgeType.BACK_EDGE:
                        continue

                    # Check if this exits the loop
                    if target.block_id not in loop.body:
                        loop.exits.append((block, target))
                        # Mark edge as loop exit
                        edge.edge_type = EdgeType.LOOP_EXIT

                        logger.debug(f"Loop {loop.head.block_id}: exit {block.block_id} -> {target.block_id}")

    def _compute_nesting(self) -> None:
        """
        Compute nesting relationships between loops.

        A loop A is nested in loop B if A's head is in B's body.
        """
        # For each loop, find its immediate container
        for loop in self.loops:
            # Find all loops that contain this loop's head
            containers = []
            for other_loop in self.loops:
                if other_loop is loop:
                    continue

                if loop.head.block_id in other_loop.body:
                    containers.append(other_loop)

            # Immediate container is the smallest (innermost) container
            if containers:
                # Sort by body size (smaller = more nested)
                containers.sort(key=lambda l: len(l.body))
                loop.container = containers[0]

        # Compute depths
        for loop in self.loops:
            depth = 0
            current = loop.container
            while current is not None:
                depth += 1
                current = current.container
            loop.depth = depth

    def _sort_by_depth(self) -> None:
        """Sort loops by depth (innermost first)."""
        self.loops.sort(key=lambda l: l.depth, reverse=True)

    def get_loop_for_block(self, block: StructuredBlock) -> Optional[LoopBody]:
        """
        Get the innermost loop containing a block.

        Args:
            block: The block to check

        Returns:
            The innermost LoopBody containing the block, or None
        """
        loops = self.block_to_loops.get(block.block_id, [])
        if not loops:
            return None

        # Return innermost loop (highest depth)
        return max(loops, key=lambda l: l.depth)

    def is_loop_header(self, block: StructuredBlock) -> bool:
        """Check if a block is a loop header."""
        return any(loop.head.block_id == block.block_id for loop in self.loops)

    def get_loop_by_header(self, head: StructuredBlock) -> Optional[LoopBody]:
        """Get the loop with the given header block."""
        for loop in self.loops:
            if loop.head.block_id == head.block_id:
                return loop
        return None

    def get_containing_loops(self, block: StructuredBlock) -> List[LoopBody]:
        """
        Get all loops containing a block (innermost to outermost).

        Args:
            block: The block to check

        Returns:
            List of LoopBody objects, sorted by depth (innermost first)
        """
        loops = self.block_to_loops.get(block.block_id, [])
        # Sort by depth (highest first = innermost)
        return sorted(loops, key=lambda l: l.depth, reverse=True)


def analyze_loops(graph: BlockGraph, dom_analysis: DominatorAnalysis) -> LoopAnalysis:
    """
    Convenience function to perform loop analysis.

    Args:
        graph: The block graph to analyze
        dom_analysis: Pre-computed dominator analysis

    Returns:
        Completed LoopAnalysis object
    """
    analysis = LoopAnalysis(graph, dom_analysis)
    analysis.analyze()
    return analysis
