"""
TraceDAG heuristic for handling irreducible control flow.

This module provides a DAG-based heuristic for identifying which edges
should be marked as gotos when the control flow cannot be fully structured.

Modeled after Ghidra's TraceDAG in blockaction.cc.

The algorithm works by:
1. Building a DAG of possible traces through the graph
2. Starting from a virtual root BranchPoint with traces to each entry
3. Pushing traces forward, creating new BranchPoints at branches
4. Retiring BranchPoints when all paths merge at a common exit
5. When stuck, scoring edges to find the most likely unstructured goto
6. Removing the worst edge and continuing until complete

Key concepts:
- BranchPoint: A node where control flow splits (has multiple out-edges)
- BlockTrace: A single path being traced from a BranchPoint
- BadEdgeScore: Metrics for ranking how likely an edge is to be a goto
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, TYPE_CHECKING

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
    A point where control flow branches, tracking paths to retirement.

    A BranchPoint is created when a trace encounters a block with multiple
    out-edges. It tracks all the sub-traces emanating from that point
    and can be "retired" when all those traces either terminate or
    converge at a common exit block.

    The parent/depth hierarchy allows calculating distances between
    BranchPoints via their Lowest Common Ancestor (LCA).
    """
    top: Optional[StructuredBlock]           # The block that embodies this branch point (None for virtual root)
    parent: Optional['BranchPoint'] = None   # Parent BranchPoint (up the hierarchy)
    pathout: int = -1                        # Index of path from parent (-1 for root)
    depth: int = 0                           # Nesting depth from root
    paths: List['BlockTrace'] = field(default_factory=list)  # BlockTrace for each out-edge
    is_marked: bool = False                  # Used for LCA distance calculation

    def mark_path(self) -> None:
        """
        Toggle marks from this BranchPoint up to the root.

        Used for LCA (Lowest Common Ancestor) finding. Call once before
        distance calculations, then call again to unmark.
        """
        cur: Optional[BranchPoint] = self
        while cur is not None:
            cur.is_marked = not cur.is_marked
            cur = cur.parent

    def distance(self, other: 'BranchPoint') -> int:
        """
        Calculate distance to another BranchPoint via their LCA.

        Assumes the path from self to root has been marked via mark_path().
        Distance = (self.depth - lca.depth) + (other.depth - lca.depth)

        Args:
            other: The other BranchPoint to measure distance to

        Returns:
            The number of edges from self to other via LCA
        """
        cur: Optional[BranchPoint] = other
        while cur is not None:
            if cur.is_marked:
                # Found the LCA (Lowest Common Ancestor)
                return (self.depth - cur.depth) + (other.depth - cur.depth)
            cur = cur.parent
        # No common ancestor found (shouldn't happen in well-formed trees)
        return self.depth + other.depth + 1

    def get_path_start(self, i: int) -> Optional[StructuredBlock]:
        """
        Get the first FlowBlock along the i-th BlockTrace path.

        Args:
            i: Index of the path

        Returns:
            The first block along that path, or None if out of range
        """
        if self.top is None:
            return None
        dag_edge_count = 0
        for j, edge in enumerate(self.top.out_edges):
            if not _is_loop_dag_edge(edge):
                continue
            if dag_edge_count == i:
                return edge.target
            dag_edge_count += 1
        return None

    def create_traces(self) -> None:
        """
        Create child BlockTraces for each DAG out-edge from this BranchPoint.

        Skips back edges, goto edges, and other non-DAG edges.
        """
        if self.top is None:
            return
        for i, edge in enumerate(self.top.out_edges):
            if not _is_loop_dag_edge(edge):
                continue
            trace = BlockTrace(
                top=self,
                pathout=len(self.paths),
                edge_index=i,
                bottom=self.top,
                destnode=edge.target
            )
            self.paths.append(trace)


@dataclass
class BlockTrace:
    """
    A single trace path through the DAG from a BranchPoint.

    BlockTraces track the current position in the trace (bottom) and the
    next block to push into (destnode). Multiple traces from the same
    BranchPoint must either all terminate or all converge at the same
    exit block before the BranchPoint can be retired.

    Attributes:
        top: Parent BranchPoint this trace belongs to
        pathout: Index of this trace in parent's paths list
        edge_index: Index of out-edge from top's block (-1 for virtual)
        bottom: Current block the trace has reached (None for virtual)
        destnode: Next block this trace will try to push into
        edgelump: Count of merged edges going to destnode (for multiple paths)
        is_active: Whether this trace is still active
        is_terminal: Whether all paths from here exit without merging
        derived_bp: If this trace spawned a child BranchPoint
    """
    top: BranchPoint
    pathout: int
    edge_index: int = -1
    bottom: Optional[StructuredBlock] = None
    destnode: Optional[StructuredBlock] = None
    edgelump: int = 1
    is_active: bool = False
    is_terminal: bool = False
    derived_bp: Optional[BranchPoint] = None

    def __hash__(self):
        """Hash by identity for use in sets/dicts."""
        return id(self)

    def __eq__(self, other):
        """Equality by identity."""
        return self is other


@dataclass
class BadEdgeScore:
    """
    Score for ranking how likely an edge is to be an unstructured goto.

    Multiple metrics are combined to determine which edge to remove:
    1. siblingedge: Edges from same BranchPoint to same exit (structural conflict)
    2. terminal: Whether destnode has no exits (naturally terminating)
    3. distance: Minimum LCA distance to other traces with same exit
    4. depth: BranchPoint depth (shallower = more fundamental)

    Sorting puts edges with same exitproto together for conflict detection.
    """
    trace: BlockTrace
    exitproto: StructuredBlock              # Putative exit block (destnode)
    distance: int = -1                      # Min distance to other traces with same exit
    terminal: int = 0                       # 1 if destnode has no exits, 0 otherwise
    siblingedge: int = 0                    # Count of sibling traces with same exit

    def __lt__(self, other: 'BadEdgeScore') -> bool:
        """
        Sort for grouping by exit block, then branch point, then path index.

        This ordering groups conflicting edges together for processing.
        """
        # Primary: by exit block ID
        if self.exitproto.block_id != other.exitproto.block_id:
            return self.exitproto.block_id < other.exitproto.block_id
        # Secondary: by branch point block ID
        self_bp_id = self.trace.top.top.block_id if self.trace.top.top else -1
        other_bp_id = other.trace.top.top.block_id if other.trace.top.top else -1
        if self_bp_id != other_bp_id:
            return self_bp_id < other_bp_id
        # Tertiary: by path index
        return self.trace.pathout < other.trace.pathout

    def compare_final(self, other: 'BadEdgeScore') -> bool:
        """
        Compare for determining which edge is MORE likely to be bad (a goto).

        Returns True if self is LESS likely to be bad than other.
        The edge with the highest badness score should be removed.

        Priority order (from Ghidra):
        1. More sibling edges = more structural conflict = MORE likely bad
        2. Non-terminal is worse (terminal edges naturally end)
        3. Shorter distance = more structural conflict = MORE likely bad
        4. Shallower depth = more fundamental conflict = MORE likely bad
        """
        # A bigger sibling edge count means LESS likely to be the bad edge
        # (we want to preserve edges that are part of structured patterns)
        if self.siblingedge != other.siblingedge:
            return other.siblingedge < self.siblingedge

        # Terminal edges are better (less likely to be gotos)
        if self.terminal != other.terminal:
            return self.terminal < other.terminal

        # Less distance between branchpoints means less likely to be bad
        if self.distance != other.distance:
            return self.distance < other.distance

        # Less depth means less likely to be bad
        return self.trace.top.depth < other.trace.top.depth


def _is_loop_dag_edge(edge: BlockEdge) -> bool:
    """
    Check if an edge is part of the DAG sub-graph (not a special edge).

    DAG edges are normal control flow edges that should be traced.
    Non-DAG edges (back edges, gotos, loop exits) are skipped.
    """
    return edge.edge_type in (EdgeType.NORMAL,)


def _is_loop_dag_in_edge(edge: BlockEdge) -> bool:
    """Check if an incoming edge is part of the DAG sub-graph."""
    return edge.edge_type in (EdgeType.NORMAL,)


class TraceDAG:
    """
    DAG-based heuristic for identifying goto edges.

    Implements Ghidra's TraceDAG algorithm:
    1. Initialize with virtual root BranchPoint and traces to entry
    2. Push traces forward, creating BranchPoints at splits
    3. Retire BranchPoints when all paths merge
    4. When stuck, select worst edge using BadEdgeScore metrics
    5. Mark worst edge as goto and continue
    6. Repeat until all traces complete

    The algorithm produces a minimal set of goto edges that, when marked,
    allow the remaining control flow to be structured.
    """

    def __init__(self, graph: BlockGraph):
        self.graph = graph
        self.branch_list: List[BranchPoint] = []
        self.active_traces: List[BlockTrace] = []
        self.likely_gotos: List[Tuple[StructuredBlock, StructuredBlock]] = []
        self.finish_block: Optional[StructuredBlock] = None
        self._visit_counts: Dict[int, int] = {}  # block_id -> visit count
        self._active_count: int = 0
        self._missed_active_count: int = 0
        self._current_iter_idx: int = 0

    def find_goto_edges(self) -> List[BlockEdge]:
        """
        Main entry point - find edges that should be marked as gotos.

        Returns:
            List of BlockEdge objects to mark as goto
        """
        if self.graph.entry_block is None:
            return []

        # Reset state
        self.branch_list.clear()
        self.active_traces.clear()
        self.likely_gotos.clear()
        self._visit_counts.clear()
        self._active_count = 0
        self._missed_active_count = 0
        self._current_iter_idx = 0

        # Initialize root BranchPoint and traces
        self._initialize()

        # Main tracing loop
        self._push_branches()

        # Clean up visit counts
        self._clear_visit_counts()

        # Convert to BlockEdge objects
        return self._convert_to_edges()

    def _initialize(self) -> None:
        """Create root BranchPoint and initial traces."""
        # Create virtual root BranchPoint (no actual block)
        root = BranchPoint(top=None, depth=0)
        self.branch_list.append(root)

        # Create trace for entry block
        if self.graph.entry_block is not None:
            trace = BlockTrace(
                top=root,
                pathout=len(root.paths),
                edge_index=-1,
                bottom=None,  # Virtual - no actual source block
                destnode=self.graph.entry_block
            )
            root.paths.append(trace)
            self._insert_active(trace)

    def _push_branches(self) -> None:
        """
        Main tracing loop - advance or remove traces until done.

        Cycles through active traces, trying to:
        1. Retire a BranchPoint if all paths merged
        2. Open (advance) a trace into its destnode
        3. If neither possible, increment miss count

        When miss count equals active count (can't advance any trace),
        select the worst edge and remove it as a likely goto.
        """
        exit_block: Optional[StructuredBlock] = None

        self._current_iter_idx = 0
        self._missed_active_count = 0

        while self._active_count > 0:
            # Wrap around the active list
            if self._current_iter_idx >= len(self.active_traces):
                self._current_iter_idx = 0

            if not self.active_traces:
                break

            cur_trace = self.active_traces[self._current_iter_idx]

            if self._missed_active_count >= self._active_count:
                # Could not push any trace further - select an edge to remove
                bad_trace = self._select_bad_edge()
                if bad_trace is not None:
                    self._remove_trace(bad_trace)
                self._current_iter_idx = 0
                self._missed_active_count = 0
            elif self._check_retirement(cur_trace):
                # Can retire this trace's BranchPoint
                exit_block = self._get_retirement_exit(cur_trace.top)
                self._retire_branch(cur_trace.top, exit_block)
                self._current_iter_idx = 0
                self._missed_active_count = 0
            elif self._check_open(cur_trace):
                # Can advance this trace
                self._open_branch(cur_trace)
                self._current_iter_idx = 0
                self._missed_active_count = 0
            else:
                # Can't advance this trace
                self._missed_active_count += 1
                self._current_iter_idx += 1

    def _select_bad_edge(self) -> Optional[BlockTrace]:
        """
        Select the most likely unstructured edge from active BlockTraces.

        Builds a list of BadEdgeScore for each non-terminal active trace,
        then groups them by exit block to detect conflicts. Finally,
        selects the trace with the worst score (most likely to be a goto).

        Returns:
            The BlockTrace corresponding to the unstructured edge, or None
        """
        scores: List[BadEdgeScore] = []

        for trace in self.active_traces:
            # Skip terminal traces and virtual edges
            if trace.is_terminal:
                continue
            if trace.destnode is None:
                continue
            if trace.top.top is None and trace.bottom is None:
                continue  # Never remove virtual edges

            score = BadEdgeScore(
                trace=trace,
                exitproto=trace.destnode,
                distance=-1,
                siblingedge=0,
                terminal=1 if trace.destnode.successor_count() == 0 else 0
            )
            scores.append(score)

        if not scores:
            # No eligible traces found - return first active trace as fallback
            for trace in self.active_traces:
                if not trace.is_terminal:
                    return trace
            return None

        # Sort for grouping by exit block
        scores.sort()

        # Process exit conflicts (multiple traces to same exit)
        self._process_exit_conflicts(scores)

        # Find worst edge (most likely to be a goto)
        worst = scores[0]
        for score in scores[1:]:
            if worst.compare_final(score):
                worst = score

        return worst.trace

    def _process_exit_conflicts(self, scores: List[BadEdgeScore]) -> None:
        """
        Calculate distance and sibling metrics for traces with same exit.

        For each group of traces pointing to the same exit block,
        calculates:
        - siblingedge: count of traces from the same BranchPoint
        - distance: minimum LCA distance to any other trace in the group

        Args:
            scores: Sorted list of BadEdgeScore (sorted by exitproto)
        """
        i = 0
        while i < len(scores):
            # Find range with same exit block
            start = i
            exit_block = scores[i].exitproto
            while i < len(scores) and scores[i].exitproto == exit_block:
                i += 1
            end = i

            if end - start > 1:
                # Multiple traces to same exit - calculate metrics
                self._calculate_conflict_metrics(scores[start:end])

    def _calculate_conflict_metrics(self, conflict_group: List[BadEdgeScore]) -> None:
        """
        Calculate sibling count and distance for conflicting traces.

        For each pair of traces in the conflict group:
        - If from same BranchPoint, increment siblingedge count
        - Calculate LCA distance and track minimum

        Args:
            conflict_group: List of BadEdgeScore with same exit block
        """
        for i, score1 in enumerate(conflict_group):
            # Mark path to root for LCA calculation
            score1.trace.top.mark_path()

            for j, score2 in enumerate(conflict_group):
                if i == j:
                    continue

                # Check if siblings (same parent BranchPoint)
                if score1.trace.top is score2.trace.top:
                    score1.siblingedge += 1
                    score2.siblingedge += 1

                # Calculate distance via LCA
                dist = score1.trace.top.distance(score2.trace.top)
                # Distance is symmetric - update minimum for both
                if score1.distance == -1 or dist < score1.distance:
                    score1.distance = dist
                if score2.distance == -1 or dist < score2.distance:
                    score2.distance = dist

            # Unmark the path
            score1.trace.top.mark_path()

    def _check_retirement(self, trace: BlockTrace) -> bool:
        """
        Check if trace's BranchPoint can be retired.

        A BranchPoint can be retired when all its child traces are either:
        - Terminal (no more paths to follow)
        - Active and pointing to the same destnode

        Only checks from the first sibling (pathout == 0) to avoid
        redundant checks.

        Args:
            trace: The BlockTrace to check

        Returns:
            True if the BranchPoint can be retired
        """
        if trace.pathout != 0:
            return False  # Only check from first sibling

        bp = trace.top

        # Special conditions for root BranchPoint retirement
        if bp.depth == 0:
            for path in bp.paths:
                if not path.is_active:
                    return False
                if not path.is_terminal:
                    return False  # All root paths must be terminal
            return True

        # For non-root: all paths must either be terminal or point to same exit
        exit_block: Optional[StructuredBlock] = None
        for path in bp.paths:
            if not path.is_active:
                return False
            if path.is_terminal:
                continue
            if path.destnode is None:
                return False
            if exit_block is None:
                exit_block = path.destnode
            elif exit_block is not path.destnode:
                return False  # Different exits

        return True

    def _get_retirement_exit(self, bp: BranchPoint) -> Optional[StructuredBlock]:
        """
        Get the common exit block for a retiring BranchPoint.

        Args:
            bp: The BranchPoint being retired

        Returns:
            The common exit block, or None if all paths terminate
        """
        for path in bp.paths:
            if not path.is_terminal and path.destnode is not None:
                return path.destnode
        return None

    def _check_open(self, trace: BlockTrace) -> bool:
        """
        Check if trace can advance into its destnode.

        A block can be "opened" (trace can advance into it) when all
        incoming DAG edges have been traced. This ensures we don't
        advance past merge points prematurely.

        Args:
            trace: The BlockTrace to check

        Returns:
            True if trace can advance into destnode
        """
        if trace.is_terminal:
            return False
        if trace.destnode is None:
            return False

        is_root = False
        if trace.top.depth == 0:
            if trace.bottom is None:
                return True  # Virtual root can always open first level
            is_root = True

        dest = trace.destnode

        # If there's a designated finish block, only root can open it
        if dest is self.finish_block and not is_root:
            return False

        # Count incoming DAG edges
        ignore_count = trace.edgelump + self._get_visit_count(dest)
        dag_in_count = 0
        for edge in dest.in_edges:
            if _is_loop_dag_in_edge(edge):
                dag_in_count += 1
                if dag_in_count > ignore_count:
                    return False

        return True

    def _open_branch(self, trace: BlockTrace) -> None:
        """
        Advance trace into destnode, potentially creating new BranchPoint.

        If destnode has multiple out-edges, creates a new BranchPoint
        with child traces. Otherwise, simply advances the trace.

        Args:
            trace: The BlockTrace to advance
        """
        dest = trace.destnode
        if dest is None:
            return

        # Count DAG out-edges
        dag_out_count = 0
        for edge in dest.out_edges:
            if _is_loop_dag_edge(edge):
                dag_out_count += 1

        if dag_out_count == 0:
            # Terminal - mark trace as terminal
            trace.is_terminal = True
            trace.bottom = dest
            trace.destnode = None
            trace.edgelump = 0
        elif dag_out_count == 1:
            # Linear - advance trace
            for edge in dest.out_edges:
                if _is_loop_dag_edge(edge):
                    trace.bottom = dest
                    trace.destnode = edge.target
                    break
        else:
            # Branch - create new BranchPoint
            new_bp = BranchPoint(
                top=dest,
                parent=trace.top,
                pathout=trace.pathout,
                depth=trace.top.depth + 1
            )
            new_bp.create_traces()

            if len(new_bp.paths) == 0:
                # No new traces (all edges were non-DAG)
                trace.is_terminal = True
                trace.bottom = dest
                trace.destnode = None
                trace.edgelump = 0
                return

            # Link trace to new BranchPoint
            trace.derived_bp = new_bp
            trace.bottom = dest
            trace.destnode = None
            trace.is_terminal = True  # This trace becomes terminal

            # Remove parent trace from active list
            self._remove_active(trace)
            self.branch_list.append(new_bp)

            # Add new traces to active list
            for new_trace in new_bp.paths:
                self._insert_active(new_trace)

    def _remove_trace(self, trace: BlockTrace) -> None:
        """
        Mark edge as goto and handle trace removal.

        Records the edge as a likely goto, then either:
        - Marks trace as terminal (if it has moved past root branch)
        - Actually removes the trace from the BranchPoint (if at root)

        Args:
            trace: The BlockTrace to remove
        """
        if trace.bottom is not None and trace.destnode is not None:
            self.likely_gotos.append((trace.bottom, trace.destnode))
            # Record that we're ignoring this edge
            self._increment_visit_count(trace.destnode, trace.edgelump)

        parent_bp = trace.top

        if trace.bottom is not parent_bp.top:
            # Trace has moved past root branch - just mark as terminal
            trace.is_terminal = True
            trace.bottom = None
            trace.destnode = None
            trace.edgelump = 0
            # Do NOT remove from active list
            return

        # Otherwise, actually remove the path from the BranchPoint
        self._remove_active(trace)

        # Adjust pathout indices for traces above this one
        size = len(parent_bp.paths)
        for i in range(trace.pathout + 1, size):
            moved_trace = parent_bp.paths[i]
            moved_trace.pathout -= 1
            if moved_trace.derived_bp is not None:
                moved_trace.derived_bp.pathout -= 1
            parent_bp.paths[i - 1] = moved_trace

        parent_bp.paths.pop()  # Remove the vacated slot

    def _retire_branch(self, bp: BranchPoint, exit_block: Optional[StructuredBlock]) -> None:
        """
        Retire a BranchPoint when all paths have merged.

        Removes all child traces from active list and updates the parent
        trace to continue from the common exit block.

        Args:
            bp: The BranchPoint to retire
            exit_block: The common exit block (None if all paths terminal)
        """
        edgeout_bl: Optional[StructuredBlock] = None
        edgelump_sum = 0

        # Remove all child traces from active list
        for path in bp.paths:
            if not path.is_terminal:
                edgelump_sum += path.edgelump
                if edgeout_bl is None:
                    edgeout_bl = path.bottom
            self._remove_active(path)

        # If this is the root BranchPoint, we're done
        if bp.depth == 0:
            return

        # Update parent trace
        if bp.parent is not None and bp.pathout >= 0 and bp.pathout < len(bp.parent.paths):
            parent_trace = bp.parent.paths[bp.pathout]
            parent_trace.derived_bp = None

            if edgeout_bl is None:
                # All traces were terminal
                parent_trace.is_terminal = True
                parent_trace.bottom = None
                parent_trace.destnode = None
                parent_trace.edgelump = 0
            else:
                # Continue from exit block
                parent_trace.bottom = edgeout_bl
                parent_trace.destnode = exit_block
                parent_trace.edgelump = edgelump_sum
                parent_trace.is_terminal = False

            # Re-activate parent trace
            self._insert_active(parent_trace)

    def _insert_active(self, trace: BlockTrace) -> None:
        """Add trace to active list."""
        if not trace.is_active:
            self.active_traces.append(trace)
            trace.is_active = True
            self._active_count += 1

    def _remove_active(self, trace: BlockTrace) -> None:
        """Remove trace from active list."""
        if trace.is_active:
            try:
                self.active_traces.remove(trace)
            except ValueError:
                pass  # Already removed
            trace.is_active = False
            self._active_count -= 1

    def _get_visit_count(self, block: StructuredBlock) -> int:
        """Get visit count for a block."""
        return self._visit_counts.get(block.block_id, 0)

    def _increment_visit_count(self, block: StructuredBlock, count: int = 1) -> None:
        """Increment visit count for a block."""
        self._visit_counts[block.block_id] = self._get_visit_count(block) + count

    def _clear_visit_counts(self) -> None:
        """Clear visit counts for blocks we modified."""
        self._visit_counts.clear()

    def _convert_to_edges(self) -> List[BlockEdge]:
        """Convert likely_gotos to actual BlockEdge objects."""
        result = []
        for source, target in self.likely_gotos:
            for edge in source.out_edges:
                if edge.target is target:
                    result.append(edge)
                    break
        return result

    # Keep the old interface for compatibility
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
