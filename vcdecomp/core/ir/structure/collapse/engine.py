"""
Collapse engine for iterative control flow structuring.

This module provides the main collapse algorithm that iteratively applies
collapse rules until the graph is fully structured or no more patterns match.

Modeled after Ghidra's CollapseStructure in blockaction.cc.
"""

from __future__ import annotations

from typing import Dict, List, Optional, TYPE_CHECKING
import logging

from ..blocks.hierarchy import (
    BlockType,
    EdgeType,
    StructuredBlock,
    BlockGraph,
    BlockEdge,
)
from .rules import CollapseRule, DEFAULT_RULES, RuleBlockSwitch
from .trace_dag import TraceDAG

if TYPE_CHECKING:
    from ....ssa import SSAFunction

logger = logging.getLogger(__name__)


class CollapseStructure:
    """
    Main collapse engine for control flow structuring.

    Iteratively applies collapse rules to transform a flat CFG into
    a hierarchical block structure.
    """

    def __init__(self, graph: BlockGraph, rules: Optional[List[CollapseRule]] = None):
        """
        Initialize the collapse engine.

        Args:
            graph: The block graph to collapse
            rules: Optional list of collapse rules (uses DEFAULT_RULES if not provided)
        """
        self.graph = graph
        self.rules = rules or DEFAULT_RULES.copy()

        # Statistics
        self.iterations = 0
        self.rules_applied: Dict[str, int] = {}
        self.gotos_inserted = 0

    def set_switch_patterns(self, patterns):
        """Set switch patterns for the switch rule."""
        for rule in self.rules:
            if isinstance(rule, RuleBlockSwitch):
                rule.set_patterns(patterns)

    def collapse_all(self) -> Optional[StructuredBlock]:
        """
        Run the full collapse algorithm.

        Returns:
            The root block after collapse, or None if collapse failed
        """
        # Phase 1: Label back edges and loop structure
        self._label_loops()

        # Phase 2: Iterative collapse
        self._iterative_collapse()

        # Phase 3: Handle any remaining irreducible flow with gotos
        if not self.graph.is_fully_collapsed():
            self._handle_irreducible()

        # Set root
        uncollapsed = self.graph.get_uncollapsed_blocks()
        if len(uncollapsed) == 1:
            self.graph.root = uncollapsed[0]
        elif len(uncollapsed) > 1:
            # Multiple uncollapsed blocks - use entry as root
            self.graph.root = self.graph.entry_block
        else:
            self.graph.root = None

        return self.graph.root

    def _label_loops(self):
        """
        Label back edges and loop structure.

        This identifies natural loops by finding back edges in the CFG.
        """
        if self.graph.entry_block is None:
            return

        visited = set()
        in_stack = set()

        def dfs(block: StructuredBlock):
            if block.block_id in visited:
                return
            visited.add(block.block_id)
            in_stack.add(block.block_id)

            for edge in block.out_edges:
                target = edge.target
                if target.block_id in in_stack:
                    # This is a back edge
                    edge.edge_type = EdgeType.BACK_EDGE
                elif target.block_id not in visited:
                    dfs(target)

            in_stack.remove(block.block_id)

        dfs(self.graph.entry_block)

    def _iterative_collapse(self):
        """
        Iteratively apply collapse rules until no more patterns match.
        """
        max_iterations = len(self.graph.blocks) * 10  # Safety limit
        changed = True

        while changed and self.iterations < max_iterations:
            changed = False
            self.iterations += 1

            # Get current uncollapsed blocks
            blocks = self.graph.get_uncollapsed_blocks()

            # Try each rule on each block
            for block in blocks:
                if block.is_collapsed:
                    continue

                for rule in self.rules:
                    if rule.matches(self.graph, block):
                        result = rule.apply(self.graph, block)
                        if result is not None:
                            # Track statistics
                            self.rules_applied[rule.name] = self.rules_applied.get(rule.name, 0) + 1
                            changed = True
                            logger.debug(f"Applied {rule.name} at block {block.block_id} -> {result.block_id}")
                            break  # Restart from beginning after change

                if changed:
                    break  # Restart outer loop

            # Check if fully collapsed
            if self.graph.is_fully_collapsed():
                break

    def _handle_irreducible(self):
        """
        Handle irreducible control flow by inserting gotos.

        Uses TraceDAG heuristic to identify the best edges to mark as gotos.
        """
        uncollapsed = self.graph.get_uncollapsed_blocks()
        if len(uncollapsed) <= 1:
            return

        # Use TraceDAG to find goto edges
        trace_dag = TraceDAG(self.graph)
        goto_edges = trace_dag.find_goto_edges()

        # Mark edges as goto
        for edge in goto_edges:
            edge.edge_type = EdgeType.GOTO_EDGE
            self.gotos_inserted += 1

        # Try one more round of collapse
        if goto_edges:
            self._iterative_collapse()

    def get_statistics(self) -> Dict:
        """Get collapse statistics."""
        return {
            "iterations": self.iterations,
            "rules_applied": self.rules_applied.copy(),
            "gotos_inserted": self.gotos_inserted,
        }


def collapse_function(graph: BlockGraph, switch_patterns=None) -> Optional[StructuredBlock]:
    """
    Convenience function to collapse a function's block graph.

    Args:
        graph: The block graph to collapse
        switch_patterns: Optional pre-detected switch patterns

    Returns:
        The root block after collapse
    """
    collapser = CollapseStructure(graph)
    if switch_patterns:
        collapser.set_switch_patterns(switch_patterns)
    return collapser.collapse_all()
