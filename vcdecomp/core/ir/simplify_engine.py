"""
Fixed-point simplification engine for SSA-level optimizations.

This module implements a Ghidra-inspired transformation engine that applies
simplification rules iteratively until convergence (no more changes).

Key features:
- Fixed-point iteration semantics
- Exhaustive rule application per iteration
- Convergence detection
- Statistics tracking
- Rule enable/disable support
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .rules import SimplificationRule, ALL_RULES
from .ssa import SSAFunction, SSAInstruction
from .use_def import UseDefChain

logger = logging.getLogger(__name__)


@dataclass
class SimplificationStats:
    """Statistics from simplification pass."""

    iterations: int = 0
    total_changes: int = 0
    rules_applied: Dict[str, int] = field(default_factory=dict)
    convergence_reason: str = "not_started"

    def __repr__(self):
        return (
            f"SimplificationStats(iterations={self.iterations}, "
            f"total_changes={self.total_changes}, "
            f"reason={self.convergence_reason})"
        )


class SimplificationEngine:
    """
    Fixed-point transformation engine modeled after Ghidra's ActionPool.

    Applies rules iteratively until convergence (no rule makes changes).
    This enables emergent simplification where one rule enables another.

    Example:
        RuleTermOrder: 3 + x → x + 3
        ↓
        RuleDoubleAdd: (x + 2) + 3 → x + 5  (now possible after reordering)
        ↓
        RuleAddIdentity: x + 0 → x  (if 5 was combined to 0)
    """

    def __init__(
        self,
        rules: Optional[List[SimplificationRule]] = None,
        max_iterations: int = 100,
        debug: bool = False,
    ):
        """
        Initialize simplification engine.

        Args:
            rules: List of rules to apply (uses ALL_RULES if None)
            max_iterations: Maximum iterations before stopping (default 100)
            debug: Enable debug logging
        """
        self.rules = rules if rules is not None else ALL_RULES
        self.max_iterations = max_iterations
        self.debug = debug

        if debug:
            logger.setLevel(logging.DEBUG)

    def simplify_to_fixpoint(self, ssa_func: SSAFunction) -> SimplificationStats:
        """
        Apply all rules iteratively until convergence.

        Convergence occurs when:
        1. No rule makes any changes in an iteration, OR
        2. Maximum iteration limit is reached

        Args:
            ssa_func: SSA function to simplify

        Returns:
            Statistics about the simplification process
        """
        stats = SimplificationStats()

        logger.info(
            f"SimplificationEngine: Starting with {len(self.rules)} rules, max_iterations={self.max_iterations}"
        )

        # Build use-def chains for data flow analysis
        # Rules can access via ssa_func.use_def_chains
        if self.debug:
            logger.debug("Building use-def chains...")
        ssa_func.use_def_chains = UseDefChain(ssa_func, debug=self.debug)

        for iteration in range(self.max_iterations):
            changes_this_iteration = 0

            # Apply each rule exhaustively
            for rule in self.rules:
                if rule.is_disabled:
                    continue

                changes = self._apply_rule_exhaustive(rule, ssa_func)
                changes_this_iteration += changes
                stats.rules_applied[rule.name] = (
                    stats.rules_applied.get(rule.name, 0) + changes
                )

                if self.debug and changes > 0:
                    logger.debug(
                        f"  Iteration {iteration + 1}: {rule.name} made {changes} changes"
                    )

            stats.total_changes += changes_this_iteration
            stats.iterations = iteration + 1

            # Rebuild use-def chains if changes were made
            # This ensures accurate analysis for next iteration
            if changes_this_iteration > 0:
                if self.debug:
                    logger.debug(f"Rebuilding use-def chains after {changes_this_iteration} changes...")
                ssa_func.use_def_chains = UseDefChain(ssa_func, debug=False)

            # Check convergence
            if changes_this_iteration == 0:
                stats.convergence_reason = "no_changes"
                logger.info(
                    f"SimplificationEngine: Converged after {stats.iterations} iterations "
                    f"({stats.total_changes} total changes)"
                )
                break

        # Check if we hit max iterations without converging
        if stats.iterations >= self.max_iterations:
            stats.convergence_reason = "max_iterations"
            logger.warning(
                f"SimplificationEngine: Reached max iterations ({self.max_iterations}) "
                f"without full convergence. {stats.total_changes} changes made."
            )
        elif stats.convergence_reason == "not_started":
            # No iterations ran (shouldn't happen)
            stats.convergence_reason = "error"

        # Log summary
        if self.debug:
            self._log_summary(stats)

        return stats

    def _apply_rule_exhaustive(
        self, rule: SimplificationRule, ssa_func: SSAFunction
    ) -> int:
        """
        Apply a single rule to all matching instructions until no more matches.

        This implements the "ActionPool" behavior from Ghidra where each rule
        is applied exhaustively before moving to the next rule.

        Args:
            rule: Rule to apply
            ssa_func: SSA function

        Returns:
            Number of times the rule was successfully applied
        """
        changes = 0
        made_change = True

        # Keep applying this rule until it makes no more changes
        while made_change:
            made_change = False

            for block_id in sorted(ssa_func.instructions.keys()):
                block_insts = ssa_func.instructions[block_id]

                for inst_idx in range(len(block_insts)):
                    inst = block_insts[inst_idx]

                    # Skip non-computational instructions
                    if self._should_skip_instruction(inst):
                        continue

                    # Check if rule matches
                    if rule.matches(inst, ssa_func):
                        new_inst = rule.apply(inst, ssa_func)

                        if new_inst is not None:
                            # Replace instruction in place
                            block_insts[inst_idx] = new_inst
                            changes += 1
                            made_change = True

                            if self.debug:
                                logger.debug(
                                    f"    {rule.name}: Transformed instruction at {inst.address}"
                                )

                            # After transformation, break and restart scan
                            # (new instruction might enable other transformations)
                            break

                if made_change:
                    break  # Restart from first block

        return changes

    def _should_skip_instruction(self, inst: SSAInstruction) -> bool:
        """
        Check if instruction should be skipped.

        Skip:
        - PHI nodes (handled by SSA construction)
        - CONST (already constant)
        - Control flow (CALL, XCALL, RET, JMP, JZ, JNZ)
        - Memory operations that need special handling (ASGN handled by LoadGuard)

        Args:
            inst: Instruction to check

        Returns:
            True if should skip, False otherwise
        """
        SKIP_OPCODES = {
            "PHI",
            "CONST",
            "CALL",
            "XCALL",
            "RET",
            "JMP",
            "JZ",
            "JNZ",
            "ASGN",  # Memory stores handled separately
        }
        return inst.mnemonic in SKIP_OPCODES

    def _log_summary(self, stats: SimplificationStats):
        """Log detailed summary of simplification results."""
        logger.debug("\n" + "=" * 60)
        logger.debug("SimplificationEngine Summary")
        logger.debug("=" * 60)
        logger.debug(f"Iterations: {stats.iterations}")
        logger.debug(f"Total changes: {stats.total_changes}")
        logger.debug(f"Convergence: {stats.convergence_reason}")
        logger.debug("\nRules applied:")

        # Sort by number of applications
        sorted_rules = sorted(
            stats.rules_applied.items(), key=lambda x: x[1], reverse=True
        )

        for rule_name, count in sorted_rules:
            logger.debug(f"  {rule_name:30s} : {count:4d} times")

        # Show disabled rules
        disabled = [r.name for r in self.rules if r.is_disabled]
        if disabled:
            logger.debug(f"\nDisabled rules: {', '.join(disabled)}")

        logger.debug("=" * 60 + "\n")

    def reset_rule_stats(self):
        """Reset statistics for all rules."""
        for rule in self.rules:
            rule.reset_stats()

    def enable_rule(self, rule_name: str):
        """Enable a rule by name."""
        for rule in self.rules:
            if rule.name == rule_name:
                rule.enable()
                logger.info(f"Enabled rule: {rule_name}")
                return
        logger.warning(f"Rule not found: {rule_name}")

    def disable_rule(self, rule_name: str):
        """Disable a rule by name."""
        for rule in self.rules:
            if rule.name == rule_name:
                rule.disable()
                logger.info(f"Disabled rule: {rule_name}")
                return
        logger.warning(f"Rule not found: {rule_name}")


# =============================================================================
# Convenience Functions (Backward Compatibility)
# =============================================================================


def simplify_expressions(
    ssa_func: SSAFunction,
    rules: Optional[List[SimplificationRule]] = None,
    max_iterations: int = 100,
    debug: bool = False,
) -> SimplificationStats:
    """
    Apply simplification rules iteratively until convergence.

    This is a convenience wrapper around SimplificationEngine for
    backward compatibility with the old API.

    Args:
        ssa_func: SSA function to simplify
        rules: Optional custom rule set (uses ALL_RULES if None)
        max_iterations: Maximum number of iterations (default 100)
        debug: Enable debug logging

    Returns:
        Statistics about the simplification process
    """
    engine = SimplificationEngine(
        rules=rules, max_iterations=max_iterations, debug=debug
    )
    return engine.simplify_to_fixpoint(ssa_func)
