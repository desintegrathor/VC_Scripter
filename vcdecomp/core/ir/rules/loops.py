"""
Loop optimization rules.

This module implements loop-related optimization rules inspired by Ghidra's
loop analysis and optimization passes:

Phase 5 rules (10 rules):
- RuleLoopIncrementSimplify: Simplify loop counter increments
- RuleLoopCounterNormalize: Normalize loop counter patterns
- RuleLoopBoundConstant: Constant fold loop bounds
- RuleInductionSimplify: Simplify induction variable arithmetic
- RuleLoopInvariantDetect: Detect loop-invariant expressions (disabled - needs CFG)
- RuleLoopStrength: Strength reduction in loops (disabled - needs CFG)
- RuleLoopUnswitch: Detect unswitchable conditions (disabled - needs CFG)
- RuleCountedLoop: Detect counted loop patterns (disabled - needs CFG)
- RuleLoopElimination: Dead loop elimination (disabled - needs CFG)
- RuleLoopRotate: Normalize loop forms (disabled - needs CFG)
"""

import logging
from typing import Optional

from .base import (
    SimplificationRule,
    is_constant,
    get_constant_value,
    create_constant_value,
)
from ..ssa import SSAFunction, SSAInstruction

logger = logging.getLogger(__name__)


class RuleLoopIncrementSimplify(SimplificationRule):
    """
    Simplify loop counter increment patterns.

    Examples:
        i = i + 1 + 0 → i = i + 1
        i = i + 1 - 0 → i = i + 1
        i = (i + 1) * 1 → i = i + 1

    This simplifies redundant operations in loop increments.
    """

    def __init__(self):
        super().__init__("RuleLoopIncrementSimplify")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Look for operations with identity elements
        # This is mostly covered by existing identity rules
        # but we keep this as a marker for loop-specific patterns
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Delegated to identity rules (RuleAddIdentity, RuleMulIdentity, etc.)
        return None


class RuleLoopCounterNormalize(SimplificationRule):
    """
    Normalize loop counter increment/decrement patterns.

    Examples:
        i = i - (-1) → i = i + 1
        i = i + (-1) → i = i - 1

    This normalizes loop counter modifications to canonical form.
    """

    def __init__(self):
        super().__init__("RuleLoopCounterNormalize")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Pattern: i = i + (-1)  or  i = i - (-1)
        if inst.mnemonic not in ("ADD", "SUB"):
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant
        if not is_constant(right):
            return False

        val = get_constant_value(right, ssa_func)

        # Normalize addition of negative to subtraction
        if inst.mnemonic == "ADD" and val < 0:
            return True

        # Normalize subtraction of negative to addition (covered by RulePtrSubNormalize)
        # but we keep it here for clarity
        if inst.mnemonic == "SUB" and val < 0:
            return True

        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """Normalize to canonical form."""
        left, right = inst.inputs
        val = get_constant_value(right, ssa_func)

        if inst.mnemonic == "ADD" and val < 0:
            # i + (-n) → i - n
            new_const = create_constant_value(-val, ssa_func)
            return SSAInstruction(
                id=inst.id,
                mnemonic="SUB",
                inputs=[left, new_const],
                output=inst.output,
            )
        elif inst.mnemonic == "SUB" and val < 0:
            # i - (-n) → i + n
            new_const = create_constant_value(-val, ssa_func)
            return SSAInstruction(
                id=inst.id,
                mnemonic="ADD",
                inputs=[left, new_const],
                output=inst.output,
            )

        return None


class RuleLoopBoundConstant(SimplificationRule):
    """
    Constant fold loop bound comparisons.

    Examples:
        i < (10 + 0) → i < 10
        i < (5 * 2) → i < 10

    This simplifies loop bound expressions.
    """

    def __init__(self):
        super().__init__("RuleLoopBoundConstant")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # This is covered by RuleConstantFold
        # We keep this as a marker for loop-specific bound analysis
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Delegated to RuleConstantFold
        return None


class RuleInductionSimplify(SimplificationRule):
    """
    Simplify induction variable arithmetic.

    Examples:
        j = i * 4 + base (where i is loop counter)
        Recognize as array access pattern

    This is primarily for detection, not transformation.
    """

    def __init__(self):
        super().__init__("RuleInductionSimplify")
        self.is_disabled = True  # Requires loop analysis

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Pattern: base + (i * stride)
        # This requires knowing which variables are induction variables
        # which requires CFG analysis
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleLoopInvariantDetect(SimplificationRule):
    """
    Detect loop-invariant expressions.

    Examples:
        x = a + b (where a, b don't change in loop)
        Can be hoisted out of loop

    This requires CFG and reaching definitions analysis.
    """

    def __init__(self):
        super().__init__("RuleLoopInvariantDetect")
        self.is_disabled = True  # Requires CFG and reaching definitions

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Need to:
        # 1. Identify loops in CFG
        # 2. Track which variables are modified in loop
        # 3. Detect expressions that only use loop-invariant variables
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Would mark instruction for hoisting, but this is a CFG transformation.
        """
        return None


class RuleLoopStrength(SimplificationRule):
    """
    Apply strength reduction in loops.

    Examples:
        j = i * 4 (in loop) → j += 4 (convert multiplication to addition)
        j = i * i (in loop) → track as j, update via j = j + 2*i + 1

    This is a classic loop optimization requiring induction variable analysis.
    """

    def __init__(self):
        super().__init__("RuleLoopStrength")
        self.is_disabled = True  # Requires induction variable analysis

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Pattern: multiplication where one operand is induction variable
        # Requires:
        # 1. Loop identification
        # 2. Induction variable detection
        # 3. Loop stride analysis
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Would replace multiplication with addition, but this requires
        inserting new phi nodes and updating loop structure.
        """
        return None


class RuleLoopUnswitch(SimplificationRule):
    """
    Detect loop-invariant conditions that can be unswitched.

    Examples:
        for (i = 0; i < n; i++) {
            if (flag) { ... } else { ... }
        }

        If 'flag' is loop-invariant, can be moved outside loop.

    This requires CFG transformation.
    """

    def __init__(self):
        super().__init__("RuleLoopUnswitch")
        self.is_disabled = True  # Requires CFG transformation

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Need to:
        # 1. Identify loops
        # 2. Find conditional branches in loop
        # 3. Check if condition is loop-invariant
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Would trigger loop unswitching transformation at CFG level.
        """
        return None


class RuleCountedLoop(SimplificationRule):
    """
    Detect counted loop patterns.

    Examples:
        for (i = 0; i < n; i++) { ... }  → Counted loop with trip count
        while (i < n) { ... i++ ... }    → Counted loop

    This analyzes loop structure to determine if it's a counted loop.
    """

    def __init__(self):
        super().__init__("RuleCountedLoop")
        self.is_disabled = True  # Requires CFG and loop analysis

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Need to:
        # 1. Identify loops
        # 2. Find loop counter variable
        # 3. Determine initialization, bound, and stride
        # 4. Verify counter is only modified by stride
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Would mark loop as counted and annotate with trip count info.
        """
        return None


class RuleLoopElimination(SimplificationRule):
    """
    Eliminate dead loops.

    Examples:
        for (i = 0; i < 0; i++) { ... }  → Empty loop, can eliminate
        while (false) { ... }             → Dead loop, can eliminate

    This detects loops that never execute or have no side effects.
    """

    def __init__(self):
        super().__init__("RuleLoopElimination")
        self.is_disabled = True  # Requires CFG transformation

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Need to:
        # 1. Identify loops
        # 2. Analyze loop bounds (constant analysis)
        # 3. Check if loop body has side effects
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Would remove loop from CFG if proven dead.
        """
        return None


class RuleLoopRotate(SimplificationRule):
    """
    Normalize loop forms by rotation.

    Examples:
        while (cond) { body; }
        → if (cond) { do { body; } while (cond); }

        This transforms loops to expose more optimization opportunities.

    This is a CFG transformation.
    """

    def __init__(self):
        super().__init__("RuleLoopRotate")
        self.is_disabled = True  # Requires CFG transformation

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # This operates on loop structure, not individual instructions
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Would restructure loop in CFG.
        """
        return None


class RuleLoopFusion(SimplificationRule):
    """
    Detect opportunities for loop fusion.

    Examples:
        for (i = 0; i < n; i++) { a[i] = ...; }
        for (i = 0; i < n; i++) { b[i] = ...; }
        → Can fuse into single loop

    This requires CFG analysis and dependency analysis.
    """

    def __init__(self):
        super().__init__("RuleLoopFusion")
        self.is_disabled = True  # Requires CFG and dependency analysis

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Need to:
        # 1. Find adjacent loops in CFG
        # 2. Check if they have same iteration space
        # 3. Verify no dependencies prevent fusion
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Would merge loops in CFG.
        """
        return None
