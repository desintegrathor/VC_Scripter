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
    BlockBasic,
    BlockGraph,
    BlockEdge,
)
from .rules import CollapseRule, DEFAULT_RULES, PRIMARY_RULES, SECONDARY_RULES, RuleBlockSwitch
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

    def __init__(
        self,
        graph: BlockGraph,
        rules: Optional[List[CollapseRule]] = None,
        primary_rules: Optional[List[CollapseRule]] = None,
        secondary_rules: Optional[List[CollapseRule]] = None,
    ):
        """
        Initialize the collapse engine.

        Args:
            graph: The block graph to collapse
            rules: Optional list of collapse rules (uses DEFAULT_RULES if not provided)
                   Deprecated in favor of primary_rules/secondary_rules
            primary_rules: Primary rules tried repeatedly until no changes
            secondary_rules: Secondary rules tried only when primary stuck
        """
        self.graph = graph

        # Support both old single-list and new two-phase rule systems
        if primary_rules is not None:
            self.primary_rules = primary_rules
            self.secondary_rules = secondary_rules or []
            self.rules = primary_rules  # For backwards compatibility
        elif rules is not None:
            self.rules = rules
            self.primary_rules = rules
            self.secondary_rules = []
        else:
            self.rules = DEFAULT_RULES.copy()
            self.primary_rules = PRIMARY_RULES.copy()
            self.secondary_rules = SECONDARY_RULES.copy()

        # Statistics
        self.iterations = 0
        self.rules_applied: Dict[str, int] = {}
        self.gotos_inserted = 0

        # Switch header blocks - these are reserved and should not be collapsed by other rules
        self.switch_header_cfg_ids: set = set()

    def set_switch_patterns(self, patterns):
        """Set switch patterns for the switch rule."""
        # Update both rules list and primary_rules list
        for rule_list in [self.rules, self.primary_rules]:
            for rule in rule_list:
                if isinstance(rule, RuleBlockSwitch):
                    rule.set_patterns(patterns)

        # Track which CFG block IDs are switch headers
        self.switch_header_cfg_ids = set()
        for pattern in patterns:
            self.switch_header_cfg_ids.add(pattern.header_block)

    def collapse_all(self) -> Optional[StructuredBlock]:
        """
        Run the full collapse algorithm.

        Following Ghidra's approach:
        1. Label loops (back edges)
        2. Collapse boolean conditions first (AND/OR patterns)
        3. Apply structural collapse rules iteratively
        4. Handle any remaining irreducible flow

        Returns:
            The root block after collapse, or None if collapse failed
        """
        # Phase 1: Label back edges and loop structure
        self._label_loops()

        # Phase 2: Collapse boolean conditions first (Ghidra-style)
        # This is done separately before main collapse because condition
        # combining should happen eagerly before other patterns
        self._collapse_conditions()

        # Phase 3: Iterative structural collapse
        self._iterative_collapse()

        # Phase 4: Handle any remaining irreducible flow with gotos
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

    def _collapse_conditions(self):
        """
        Collapse boolean AND/OR condition patterns.

        This is run as a separate phase before main structural collapse,
        following Ghidra's collapseConditions() approach. It repeatedly
        applies the BlockOr rule until no more patterns are found.

        The reason this is separate: combining boolean conditions should
        happen eagerly, before other structural patterns are applied.
        This produces cleaner, more readable conditions like:
          if (a || b || c)  instead of  if (a) { } else if (b) { } else if (c)
        """
        # Find the RuleBlockOr in our rule lists
        or_rule = None
        for rule in self.primary_rules:
            if isinstance(rule, RuleBlockOr):
                or_rule = rule
                break

        if or_rule is None:
            # No OR rule available, skip this phase
            return

        # Apply RuleBlockOr repeatedly until no changes
        max_iterations = len(self.graph.blocks) * 5  # Safety limit
        condition_iterations = 0

        while condition_iterations < max_iterations:
            changed = False
            condition_iterations += 1

            # Get current uncollapsed blocks
            blocks = self.graph.get_uncollapsed_blocks()

            # Try to apply OR rule to each block
            for block in blocks:
                if block.is_collapsed:
                    continue

                if or_rule.matches(self.graph, block):
                    result = or_rule.apply(self.graph, block)
                    if result is not None:
                        # Track statistics
                        self.rules_applied[or_rule.name] = self.rules_applied.get(or_rule.name, 0) + 1
                        changed = True
                        logger.debug(f"Collapsed condition: {or_rule.name} at block {block.block_id} -> {result.block_id}")
                        break  # Restart from beginning after change

            if not changed:
                break  # No more OR patterns found

        logger.debug(f"Condition collapse completed in {condition_iterations} iterations")

    def _iterative_collapse(self):
        """
        Iteratively apply collapse rules using Ghidra-style two-phase iteration.

        Phase 1 (Inner loop): Try primary rules repeatedly until no changes
        Phase 2 (Outer loop): Try secondary rules when stuck, then retry primary
        """
        max_iterations = len(self.graph.blocks) * 10  # Safety limit

        while self.iterations < max_iterations:
            # Inner loop: Try primary rules until no changes
            primary_changed = True
            while primary_changed and self.iterations < max_iterations:
                primary_changed = False
                self.iterations += 1

                # Get current uncollapsed blocks
                blocks = self.graph.get_uncollapsed_blocks()

                # Try each primary rule on each block
                for block in blocks:
                    if block.is_collapsed:
                        continue

                    # Check if this block is a switch header (should only be collapsed by switch rule)
                    is_switch_header = False
                    if isinstance(block, BlockBasic):
                        if block.original_block_id in self.switch_header_cfg_ids:
                            is_switch_header = True

                    for rule in self.primary_rules:
                        # Skip non-switch rules for switch headers
                        if is_switch_header and not isinstance(rule, RuleBlockSwitch):
                            continue

                        if rule.matches(self.graph, block):
                            result = rule.apply(self.graph, block)
                            if result is not None:
                                # Track statistics
                                self.rules_applied[rule.name] = self.rules_applied.get(rule.name, 0) + 1
                                primary_changed = True
                                logger.debug(f"Applied {rule.name} at block {block.block_id} -> {result.block_id}")
                                break  # Restart from beginning after change

                    if primary_changed:
                        break  # Restart block iteration

                # Check if fully collapsed
                if self.graph.is_fully_collapsed():
                    return

            # Outer loop: Try secondary rules when primary stuck
            secondary_changed = False

            if self.secondary_rules:
                blocks = self.graph.get_uncollapsed_blocks()

                for block in blocks:
                    if block.is_collapsed:
                        continue

                    for rule in self.secondary_rules:
                        if rule.matches(self.graph, block):
                            result = rule.apply(self.graph, block)
                            if result is not None:
                                self.rules_applied[rule.name] = self.rules_applied.get(rule.name, 0) + 1
                                secondary_changed = True
                                logger.debug(f"Applied secondary {rule.name} at block {block.block_id} -> {result.block_id}")
                                break

                    if secondary_changed:
                        break

            # If secondary rules made progress, restart primary iteration
            if not secondary_changed:
                break  # Neither primary nor secondary matched - done

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
