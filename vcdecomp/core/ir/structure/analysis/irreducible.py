"""
Irreducible edge detection using Tarjan's algorithm.

This module implements Tarjan's algorithm for detecting irreducible edges
in a control flow graph. An edge is irreducible if it cannot be classified
as a tree, forward, cross, or back edge in any spanning tree of the graph.

Irreducible edges indicate complex control flow (e.g., multiple entry points
to a loop) that cannot be expressed with structured control flow.

Algorithm (from Ghidra's block.cc):
1. Build spanning tree with DFS, labeling edges as tree/forward/cross/back
2. For each back edge (y -> x), compute "reachunder" set:
   - All nodes reachable from y without going through x
3. If reachunder includes nodes outside the natural loop, edge is irreducible
4. Mark irreducible edges and potentially rebuild spanning tree

Reference: Tarjan, R. E. (1974). "Testing flow graph reducibility"
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple, Optional, TYPE_CHECKING
from enum import Enum, auto
import logging

from ..blocks.hierarchy import (
    BlockGraph,
    StructuredBlock,
    BlockEdge,
    EdgeType,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class SpanningEdgeType(Enum):
    """Edge classification in spanning tree."""
    TREE = auto()        # Edge in spanning tree
    FORWARD = auto()     # Edge to descendant (not in tree)
    CROSS = auto()       # Edge between subtrees
    BACK = auto()        # Edge to ancestor (loop back edge)
    IRREDUCIBLE = auto() # Edge that breaks reducibility


class SpanningTreeAnalysis:
    """
    Spanning tree construction and irreducible edge detection.

    Builds a DFS spanning tree and classifies edges, then uses Tarjan's
    algorithm to detect irreducible edges.
    """

    def __init__(self, graph: BlockGraph):
        """
        Initialize spanning tree analysis.

        Args:
            graph: The block graph to analyze
        """
        self.graph = graph
        self.preorder: List[StructuredBlock] = []
        self.postorder: List[StructuredBlock] = []
        self.rpostorder: List[StructuredBlock] = []  # Reverse post-order

        # Edge classification
        self.edge_type: Dict[Tuple[int, int], SpanningEdgeType] = {}

        # DFS state
        self.visit_time: Dict[int, int] = {}  # When node was discovered
        self.finish_time: Dict[int, int] = {}  # When node was finished
        self.num_descendants: Dict[int, int] = {}  # Number of descendants in tree

        # For irreducible detection
        self.union_find: Dict[int, int] = {}  # Union-find for collapsing reachunder
        self.irreducible_edges: Set[Tuple[int, int]] = set()

        # Timing
        self.time = 0

    def analyze(self) -> Tuple[int, bool]:
        """
        Run spanning tree analysis and irreducible edge detection.

        Returns:
            Tuple of (num_irreducible_edges, needs_rebuild)
            - num_irreducible_edges: Count of irreducible edges found
            - needs_rebuild: True if a tree edge is irreducible (need to rebuild)
        """
        self._build_spanning_tree()
        return self._find_irreducible_edges()

    def _build_spanning_tree(self) -> None:
        """
        Build spanning tree using depth-first search.

        Labels edges as tree, forward, cross, or back edges.
        Computes preorder, postorder, and reverse postorder traversals.
        """
        if self.graph.entry_block is None:
            return

        # Initialize state
        self.time = 0
        self.visit_time.clear()
        self.finish_time.clear()
        self.num_descendants.clear()
        self.edge_type.clear()
        self.preorder.clear()
        self.postorder.clear()

        # DFS stack: (block, edge_index, is_visiting)
        # is_visiting: True when first visiting, False when finishing
        stack: List[Tuple[StructuredBlock, int, bool]] = []
        on_stack: Set[int] = set()

        # Start DFS from entry
        entry = self.graph.entry_block
        stack.append((entry, 0, True))

        while stack:
            block, edge_idx, is_visiting = stack.pop()

            if is_visiting:
                # First visit to this block
                if block.block_id in self.visit_time:
                    continue  # Already visited

                # Record visit
                self.visit_time[block.block_id] = self.time
                self.time += 1
                self.preorder.append(block)
                on_stack.add(block.block_id)
                self.num_descendants[block.block_id] = 1

                # Push finish marker
                stack.append((block, 0, False))

                # Push children in reverse order (so we visit in order)
                for i in range(len(block.out_edges) - 1, -1, -1):
                    edge = block.out_edges[i]
                    target = edge.target

                    # Classify edge
                    edge_key = (block.block_id, target.block_id)

                    if target.block_id not in self.visit_time:
                        # Tree edge (first visit to target)
                        self.edge_type[edge_key] = SpanningEdgeType.TREE
                        stack.append((target, 0, True))
                    elif target.block_id in on_stack:
                        # Back edge (target is ancestor)
                        self.edge_type[edge_key] = SpanningEdgeType.BACK
                        # Update BlockEdge type
                        edge.edge_type = EdgeType.BACK_EDGE
                    elif self.visit_time[block.block_id] < self.visit_time[target.block_id]:
                        # Forward edge (target is descendant, already visited)
                        self.edge_type[edge_key] = SpanningEdgeType.FORWARD
                    else:
                        # Cross edge (target in different subtree)
                        self.edge_type[edge_key] = SpanningEdgeType.CROSS

            else:
                # Finishing this block
                if block.block_id not in self.finish_time:
                    self.finish_time[block.block_id] = self.time
                    self.time += 1
                    self.postorder.append(block)
                    on_stack.remove(block.block_id)

                    # Update parent's descendant count
                    for edge in block.in_edges:
                        parent = edge.source
                        edge_key = (parent.block_id, block.block_id)
                        if self.edge_type.get(edge_key) == SpanningEdgeType.TREE:
                            self.num_descendants[parent.block_id] += self.num_descendants[block.block_id]

        # Build reverse postorder
        self.rpostorder = list(reversed(self.postorder))

        logger.debug(f"Built spanning tree: {len(self.preorder)} nodes, {len(self.edge_type)} edges")

    def _find_irreducible_edges(self) -> Tuple[int, bool]:
        """
        Detect irreducible edges using Tarjan's algorithm.

        For each back edge (y -> x):
        1. Compute "reachunder" set: nodes reachable from y without going through x
        2. If reachunder includes nodes outside the natural loop, mark edge as irreducible

        Returns:
            Tuple of (num_irreducible, needs_rebuild)
        """
        irreducible_count = 0
        needs_rebuild = False

        # Initialize union-find for collapsing reachunder
        for block in self.graph.blocks.values():
            self.union_find[block.block_id] = block.block_id

        # Process blocks in reverse preorder (postorder)
        for x in reversed(self.preorder):
            reachunder: List[int] = []
            reachunder_set: Set[int] = set()

            # Find all back edges into x
            for edge in x.in_edges:
                y = edge.source
                edge_key = (y.block_id, x.block_id)

                if self.edge_type.get(edge_key) == SpanningEdgeType.BACK:
                    if y.block_id == x.block_id:
                        continue  # Self-loop, skip

                    # Add FIND(y) to reachunder
                    y_root = self._find(y.block_id)
                    if y_root not in reachunder_set:
                        reachunder.append(y_root)
                        reachunder_set.add(y_root)

            # Build reachunder set
            q = 0
            while q < len(reachunder):
                t_id = reachunder[q]
                q += 1

                t = self.graph.blocks.get(t_id)
                if t is None:
                    continue

                # Process incoming edges to t
                for edge in t.in_edges:
                    y = edge.source
                    edge_key = (y.block_id, t_id)
                    edge_type = self.edge_type.get(edge_key)

                    # Skip irreducible edges (already marked)
                    if edge_type == SpanningEdgeType.IRREDUCIBLE:
                        continue

                    # Skip back edges (already handled)
                    if edge_type == SpanningEdgeType.BACK:
                        continue

                    # Check if edge violates reducibility
                    y_root = self._find(y.block_id)

                    x_visit = self.visit_time.get(x.block_id, 0)
                    x_desc = self.num_descendants.get(x.block_id, 0)
                    y_visit = self.visit_time.get(y_root, 0)

                    # Check if y' is outside the natural loop of x
                    if (x_visit > y_visit) or (x_visit + x_desc <= y_visit):
                        # Irreducible edge found!
                        self.edge_type[edge_key] = SpanningEdgeType.IRREDUCIBLE
                        self.irreducible_edges.add(edge_key)
                        edge.edge_type = EdgeType.IRREDUCIBLE
                        irreducible_count += 1

                        # If a tree edge is irreducible, we need to rebuild
                        if edge_type == SpanningEdgeType.TREE:
                            needs_rebuild = True

                        logger.debug(f"Irreducible edge: {y.block_id} -> {t_id}")

                    elif y_root not in reachunder_set and y_root != x.block_id:
                        # Add y' to reachunder
                        reachunder.append(y_root)
                        reachunder_set.add(y_root)

            # Collapse reachunder into x (union-find merge)
            for node_id in reachunder:
                self.union_find[node_id] = x.block_id

        logger.debug(f"Found {irreducible_count} irreducible edges")
        return irreducible_count, needs_rebuild

    def _find(self, node_id: int) -> int:
        """
        Union-find FIND operation with path compression.

        Args:
            node_id: The node to find root for

        Returns:
            The root of the set containing node_id
        """
        if self.union_find[node_id] != node_id:
            # Path compression
            self.union_find[node_id] = self._find(self.union_find[node_id])
        return self.union_find[node_id]

    def get_edge_type(self, source: StructuredBlock, target: StructuredBlock) -> Optional[SpanningEdgeType]:
        """Get the spanning edge type for an edge."""
        edge_key = (source.block_id, target.block_id)
        return self.edge_type.get(edge_key)

    def is_irreducible(self, source: StructuredBlock, target: StructuredBlock) -> bool:
        """Check if an edge is irreducible."""
        edge_key = (source.block_id, target.block_id)
        return self.edge_type.get(edge_key) == SpanningEdgeType.IRREDUCIBLE

    def get_back_edges(self) -> List[Tuple[StructuredBlock, StructuredBlock]]:
        """Get all back edges (loop back edges)."""
        back_edges = []
        for (src_id, tgt_id), edge_type in self.edge_type.items():
            if edge_type == SpanningEdgeType.BACK:
                src = self.graph.blocks.get(src_id)
                tgt = self.graph.blocks.get(tgt_id)
                if src and tgt:
                    back_edges.append((src, tgt))
        return back_edges

    def get_irreducible_edges(self) -> List[Tuple[StructuredBlock, StructuredBlock]]:
        """Get all irreducible edges."""
        irreducible = []
        for (src_id, tgt_id), edge_type in self.edge_type.items():
            if edge_type == SpanningEdgeType.IRREDUCIBLE:
                src = self.graph.blocks.get(src_id)
                tgt = self.graph.blocks.get(tgt_id)
                if src and tgt:
                    irreducible.append((src, tgt))
        return irreducible


def detect_irreducible_edges(graph: BlockGraph) -> SpanningTreeAnalysis:
    """
    Convenience function to detect irreducible edges.

    Args:
        graph: The block graph to analyze

    Returns:
        SpanningTreeAnalysis with results
    """
    analysis = SpanningTreeAnalysis(graph)
    analysis.analyze()
    return analysis
