"""
Dominator analysis for control flow graphs.

This module implements dominator tree construction and related algorithms
based on the Lengauer-Tarjan algorithm, following Ghidra's implementation
in block.cc.

Key concepts:
- Immediate dominator (idom): The unique node that dominates a given node
  and is dominated by all other dominators of that node
- Dominator tree: Tree structure where parent is the immediate dominator
- Dominator depth: Distance from root in dominator tree
- Dominator subtree: All nodes dominated by a given node

Algorithm:
1. Compute reverse post-order traversal
2. Iteratively compute immediate dominators using intersection
3. Build dominator tree from idom relationships
4. Calculate depths and subtrees
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, TYPE_CHECKING
import logging

from ..blocks.hierarchy import (
    BlockGraph,
    StructuredBlock,
    BlockBasic,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class DominatorAnalysis:
    """
    Dominator tree analysis for a block graph.

    Computes immediate dominators, dominator tree, and related information
    using the iterative dataflow algorithm (Cooper-Harvey-Kennedy variant
    of Lengauer-Tarjan).
    """

    def __init__(self, graph: BlockGraph):
        """
        Initialize dominator analysis.

        Args:
            graph: The block graph to analyze
        """
        self.graph = graph
        self.idom: Dict[int, Optional[StructuredBlock]] = {}  # Immediate dominator map
        self.dom_children: Dict[int, List[StructuredBlock]] = {}  # Dominator tree children
        self.dom_depth: Dict[int, int] = {}  # Depth in dominator tree
        self.postorder: List[StructuredBlock] = []  # Reverse post-order traversal
        self.virtual_root: Optional[StructuredBlock] = None  # Virtual root if needed

    def compute(self) -> None:
        """
        Run the full dominator analysis.

        Computes immediate dominators, builds dominator tree, and calculates depths.
        """
        self._build_postorder()
        self._calc_forward_dominator()
        self._build_dom_tree()
        self._build_dom_depth()

    def _build_postorder(self) -> None:
        """
        Build reverse post-order traversal of the graph.

        Reverse post-order ensures that when processing a node, we've already
        processed most of its predecessors (except back edges).
        """
        visited: Set[int] = set()
        postorder_stack: List[StructuredBlock] = []

        def dfs(block: StructuredBlock):
            if block.block_id in visited:
                return
            visited.add(block.block_id)

            for edge in block.out_edges:
                target = edge.target
                if target.block_id not in visited:
                    dfs(target)

            postorder_stack.append(block)

        # Start from entry block
        if self.graph.entry_block is not None:
            dfs(self.graph.entry_block)

        # Reverse to get reverse post-order
        self.postorder = list(reversed(postorder_stack))

        logger.debug(f"Built postorder with {len(self.postorder)} blocks")

    def _calc_forward_dominator(self) -> None:
        """
        Calculate immediate dominators using iterative dataflow algorithm.

        This is the Cooper-Harvey-Kennedy algorithm, which is a simplified
        variant of Lengauer-Tarjan. It works by:
        1. Initialize root to dominate itself
        2. For each node in reverse post-order:
           - Compute intersection of dominators of all predecessors
           - Update if changed
        3. Repeat until no changes

        Time complexity: O(n^2) in worst case, but typically much faster.
        """
        if not self.postorder:
            return

        # Create index map for fast lookup
        block_to_idx: Dict[int, int] = {}
        for idx, block in enumerate(self.postorder):
            block_to_idx[block.block_id] = idx

        # Initialize: no dominators set
        for block in self.postorder:
            self.idom[block.block_id] = None

        # Root dominates itself
        root = self.postorder[0]
        self.idom[root.block_id] = root

        # Also initialize immediate successors of root
        for edge in root.out_edges:
            self.idom[edge.target.block_id] = root

        # Iteratively compute dominators
        changed = True
        iteration = 0
        max_iterations = len(self.postorder) * 10  # Safety limit

        while changed and iteration < max_iterations:
            changed = False
            iteration += 1

            # Process all nodes except root in reverse post-order
            for block in self.postorder[1:]:
                if self.idom[block.block_id] == root:
                    continue  # Skip immediate successors of root

                # Find first processed predecessor
                new_idom = None
                for edge in block.in_edges:
                    pred = edge.source
                    if self.idom.get(pred.block_id) is not None:
                        new_idom = pred
                        break

                if new_idom is None:
                    continue  # No processed predecessors yet

                # Intersect with all other processed predecessors
                for edge in block.in_edges:
                    pred = edge.source
                    if pred == new_idom:
                        continue

                    if self.idom.get(pred.block_id) is not None:
                        new_idom = self._intersect(pred, new_idom, block_to_idx)

                # Update if changed
                if self.idom[block.block_id] != new_idom:
                    self.idom[block.block_id] = new_idom
                    changed = True

        logger.debug(f"Computed dominators in {iteration} iterations")

        # Clear root's self-domination (Ghidra convention)
        self.idom[root.block_id] = None

    def _intersect(
        self,
        b1: StructuredBlock,
        b2: StructuredBlock,
        block_to_idx: Dict[int, int]
    ) -> StructuredBlock:
        """
        Find the common dominator of two nodes.

        This is the intersection operation in the dominator algorithm.
        It finds the lowest common ancestor in the current dominator tree.

        Args:
            b1: First block
            b2: Second block
            block_to_idx: Map from block ID to postorder index

        Returns:
            The common dominator
        """
        finger1 = block_to_idx[b1.block_id]
        finger2 = block_to_idx[b2.block_id]

        # Walk up dominator tree from both nodes until they meet
        while finger1 != finger2:
            while finger1 > finger2:
                idom = self.idom.get(self.postorder[finger1].block_id)
                if idom is None:
                    break
                finger1 = block_to_idx[idom.block_id]

            while finger2 > finger1:
                idom = self.idom.get(self.postorder[finger2].block_id)
                if idom is None:
                    break
                finger2 = block_to_idx[idom.block_id]

        return self.postorder[finger1]

    def _build_dom_tree(self) -> None:
        """
        Build dominator tree from immediate dominator relationships.

        Creates a mapping from each node to its children in the dominator tree.
        """
        self.dom_children.clear()

        # Initialize empty lists
        for block in self.graph.blocks.values():
            self.dom_children[block.block_id] = []

        # Add each node to its dominator's children
        for block in self.graph.blocks.values():
            idom = self.idom.get(block.block_id)
            if idom is not None:
                self.dom_children[idom.block_id].append(block)

        logger.debug(f"Built dominator tree")

    def _build_dom_depth(self) -> None:
        """
        Calculate depth in dominator tree for each node.

        Root has depth 1, its immediate children have depth 2, etc.
        """
        self.dom_depth.clear()

        # Process in reverse post-order (parents before children)
        for block in self.postorder:
            idom = self.idom.get(block.block_id)
            if idom is not None:
                # Depth is parent's depth + 1
                parent_depth = self.dom_depth.get(idom.block_id, 0)
                self.dom_depth[block.block_id] = parent_depth + 1
            else:
                # Root has depth 1
                self.dom_depth[block.block_id] = 1

        logger.debug(f"Computed dominator depths")

    def get_idom(self, block: StructuredBlock) -> Optional[StructuredBlock]:
        """Get the immediate dominator of a block."""
        return self.idom.get(block.block_id)

    def get_dom_children(self, block: StructuredBlock) -> List[StructuredBlock]:
        """Get the children of a block in the dominator tree."""
        return self.dom_children.get(block.block_id, [])

    def get_dom_depth(self, block: StructuredBlock) -> int:
        """Get the depth of a block in the dominator tree."""
        return self.dom_depth.get(block.block_id, 0)

    def dominates(self, dominator: StructuredBlock, dominated: StructuredBlock) -> bool:
        """
        Check if one block dominates another.

        Block A dominates block B if all paths from the entry to B pass through A.

        Args:
            dominator: The potential dominating block
            dominated: The potentially dominated block

        Returns:
            True if dominator dominates dominated
        """
        # A block dominates itself
        if dominator.block_id == dominated.block_id:
            return True

        # Walk up dominator tree from dominated
        current = dominated
        while True:
            idom = self.idom.get(current.block_id)
            if idom is None:
                return False
            if idom.block_id == dominator.block_id:
                return True
            current = idom

    def strictly_dominates(self, dominator: StructuredBlock, dominated: StructuredBlock) -> bool:
        """
        Check if one block strictly dominates another.

        Block A strictly dominates block B if A dominates B and A != B.

        Args:
            dominator: The potential dominating block
            dominated: The potentially dominated block

        Returns:
            True if dominator strictly dominates dominated
        """
        if dominator.block_id == dominated.block_id:
            return False
        return self.dominates(dominator, dominated)

    def get_dominated_set(self, block: StructuredBlock) -> Set[int]:
        """
        Get the set of all blocks dominated by a given block.

        This includes the block itself and all blocks in its dominator subtree.

        Args:
            block: The dominating block

        Returns:
            Set of block IDs dominated by block
        """
        dominated: Set[int] = {block.block_id}

        def collect_subtree(node: StructuredBlock):
            for child in self.get_dom_children(node):
                dominated.add(child.block_id)
                collect_subtree(child)

        collect_subtree(block)
        return dominated

    def get_dominator_frontier(self, block: StructuredBlock) -> Set[StructuredBlock]:
        """
        Get the dominance frontier of a block.

        The dominance frontier of block B is the set of all blocks Y such that:
        1. B dominates a predecessor of Y, but
        2. B does not strictly dominate Y

        This is used for SSA construction (phi node placement).

        Args:
            block: The block to get frontier for

        Returns:
            Set of blocks in the dominance frontier
        """
        frontier: Set[StructuredBlock] = set()
        dominated = self.get_dominated_set(block)

        # For each dominated block, check its successors
        for dom_id in dominated:
            dom_block = self.graph.blocks.get(dom_id)
            if dom_block is None:
                continue

            for edge in dom_block.out_edges:
                successor = edge.target
                # If successor is not strictly dominated, it's in frontier
                if not self.strictly_dominates(block, successor):
                    frontier.add(successor)

        return frontier


def compute_dominators(graph: BlockGraph) -> DominatorAnalysis:
    """
    Convenience function to compute dominator analysis for a graph.

    Args:
        graph: The block graph to analyze

    Returns:
        Completed DominatorAnalysis object
    """
    analysis = DominatorAnalysis(graph)
    analysis.compute()
    return analysis
