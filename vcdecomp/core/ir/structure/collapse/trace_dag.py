"""
TraceDAG heuristic for handling irreducible control flow.

This module provides a DAG-based heuristic for identifying which edges
should be marked as gotos when the control flow cannot be fully structured.

Modeled after Ghidra's TraceDAG in blockaction.cc.

The algorithm works by:
1. Building a DAG of possible traces through the graph
2. Identifying branch points where traces diverge
3. Finding edges that cross between traces (likely unstructured jumps)
4. Selecting the minimal set of edges to mark as gotos
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, TYPE_CHECKING

from ..blocks.hierarchy import (
    BlockType,
    EdgeType,
    StructuredBlock,
    BlockGraph,
    BlockEdge,
)

if TYPE_CHECKING:
    pass


@dataclass
class BranchPoint:
    """
    A point where control flow branches.

    Tracks which blocks are reachable from each branch of the split.
    """
    block: StructuredBlock
    true_reachable: Set[int] = field(default_factory=set)
    false_reachable: Set[int] = field(default_factory=set)

    def blocks_in_both(self) -> Set[int]:
        """Get blocks reachable from both branches (merge points)."""
        return self.true_reachable & self.false_reachable

    def blocks_in_true_only(self) -> Set[int]:
        """Get blocks reachable only from true branch."""
        return self.true_reachable - self.false_reachable

    def blocks_in_false_only(self) -> Set[int]:
        """Get blocks reachable only from false branch."""
        return self.false_reachable - self.true_reachable


@dataclass
class BlockTrace:
    """
    A single path through the DAG.

    Represents one possible execution path from entry to a terminal point.
    """
    blocks: List[StructuredBlock] = field(default_factory=list)
    visited: Set[int] = field(default_factory=set)

    def add_block(self, block: StructuredBlock):
        """Add a block to the trace."""
        self.blocks.append(block)
        self.visited.add(block.block_id)

    def contains(self, block: StructuredBlock) -> bool:
        """Check if trace contains block."""
        return block.block_id in self.visited

    def copy(self) -> "BlockTrace":
        """Create a copy of this trace."""
        new_trace = BlockTrace()
        new_trace.blocks = self.blocks.copy()
        new_trace.visited = self.visited.copy()
        return new_trace


class TraceDAG:
    """
    DAG-based heuristic for identifying goto edges.

    Builds traces through the graph and identifies edges that cross
    between independent traces, marking them as candidates for gotos.
    """

    def __init__(self, graph: BlockGraph):
        self.graph = graph
        self.branch_points: List[BranchPoint] = []
        self.traces: List[BlockTrace] = []

    def find_goto_edges(self) -> List[BlockEdge]:
        """
        Find edges that should be marked as gotos.

        Returns:
            List of edges to mark as goto
        """
        if self.graph.entry_block is None:
            return []

        # Build traces from entry
        self._build_traces()

        # Find cross-trace edges
        goto_candidates = self._find_cross_trace_edges()

        # Score and select best edges to cut
        return self._select_goto_edges(goto_candidates)

    def _build_traces(self):
        """Build all possible traces from entry."""
        if self.graph.entry_block is None:
            return

        initial_trace = BlockTrace()
        self._extend_trace(initial_trace, self.graph.entry_block)

    def _extend_trace(self, trace: BlockTrace, block: StructuredBlock):
        """
        Extend a trace from the given block.

        Recursively follows edges, splitting at branches.
        """
        if block.is_collapsed:
            return

        if trace.contains(block):
            # Would create a cycle - stop
            return

        trace.add_block(block)

        successors = [e.target for e in block.out_edges if not e.target.is_collapsed]

        if len(successors) == 0:
            # Terminal - save trace
            self.traces.append(trace)
        elif len(successors) == 1:
            # Linear - continue
            self._extend_trace(trace, successors[0])
        else:
            # Branch - create branch point and fork traces
            branch = BranchPoint(block=block)

            for i, succ in enumerate(successors):
                new_trace = trace.copy()
                self._extend_trace(new_trace, succ)

                # Track reachability for branch point
                if i == 0:
                    branch.true_reachable = new_trace.visited - trace.visited
                else:
                    branch.false_reachable = new_trace.visited - trace.visited

            self.branch_points.append(branch)

    def _find_cross_trace_edges(self) -> List[BlockEdge]:
        """
        Find edges that cross between independent traces.

        These are edges that go from a block in one branch to a block
        that should only be reachable from a different branch.
        """
        candidates = []

        for branch in self.branch_points:
            true_only = branch.blocks_in_true_only()
            false_only = branch.blocks_in_false_only()

            # Check all edges from true-only blocks
            for block_id in true_only:
                block = self._find_block_by_id(block_id)
                if block is None:
                    continue

                for edge in block.out_edges:
                    if edge.target.block_id in false_only:
                        # Edge crosses from true branch to false branch
                        candidates.append(edge)

            # Check all edges from false-only blocks
            for block_id in false_only:
                block = self._find_block_by_id(block_id)
                if block is None:
                    continue

                for edge in block.out_edges:
                    if edge.target.block_id in true_only:
                        # Edge crosses from false branch to true branch
                        candidates.append(edge)

        return candidates

    def _find_block_by_id(self, block_id: int) -> Optional[StructuredBlock]:
        """Find a block by its ID."""
        return self.graph.blocks.get(block_id)

    def _select_goto_edges(self, candidates: List[BlockEdge]) -> List[BlockEdge]:
        """
        Select which candidate edges to mark as goto.

        Uses heuristics to minimize the number of gotos while breaking
        all irreducible cycles.
        """
        if not candidates:
            # No cross-trace edges found - fall back to simple heuristic
            return self._fallback_goto_selection()

        # Score each candidate
        scored = []
        for edge in candidates:
            score = self._score_goto_candidate(edge)
            scored.append((score, edge))

        # Sort by score (lower is better)
        scored.sort(key=lambda x: x[0])

        # Select edges greedily
        selected = []
        resolved_blocks = set()

        for score, edge in scored:
            # Check if this edge helps resolve something not yet resolved
            target_id = edge.target.block_id
            if target_id not in resolved_blocks:
                selected.append(edge)
                resolved_blocks.add(target_id)

        return selected

    def _score_goto_candidate(self, edge: BlockEdge) -> int:
        """
        Score a goto candidate (lower is better).

        Prefers:
        - Edges to blocks with few predecessors
        - Forward edges over back edges
        - Edges that don't break loops
        """
        score = 0

        # Prefer edges to blocks with more predecessors (less disruption)
        score += 10 - min(10, edge.target.predecessor_count())

        # Penalize back edges (likely loop structure)
        if edge.edge_type == EdgeType.BACK_EDGE:
            score += 50

        # Penalize if target is likely a loop header
        if edge.target.predecessor_count() > 1:
            has_back_edge = any(
                e.edge_type == EdgeType.BACK_EDGE
                for e in edge.target.in_edges
            )
            if has_back_edge:
                score += 30

        return score

    def _fallback_goto_selection(self) -> List[BlockEdge]:
        """
        Fallback goto selection when TraceDAG doesn't find candidates.

        Simply marks edges entering blocks with multiple predecessors.
        """
        selected = []
        uncollapsed = self.graph.get_uncollapsed_blocks()

        for block in uncollapsed:
            if block.predecessor_count() > 1:
                # Mark all but one incoming edge as goto
                for edge in block.in_edges[1:]:
                    if edge.edge_type == EdgeType.NORMAL:
                        selected.append(edge)

        return selected
