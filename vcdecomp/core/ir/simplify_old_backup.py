"""
Expression simplification engine for SSA-level optimizations.

This module implements Ghidra-inspired transformation rules that simplify
expressions through:
- Constant folding (evaluate operations on constants)
- Algebraic identities (x & -1 → x, x + 0 → x, etc.)
- Canonical term ordering (3 + x → x + 3 for CSE)
- Copy propagation (replace COPY uses with original)
- Bitwise operation simplification (nested AND/OR/XOR)

Modeled after Ghidra's ruleaction.cc transformation system.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from ..disasm import opcodes
from .ssa import SSAFunction, SSAInstruction, SSAValue

logger = logging.getLogger(__name__)


# =============================================================================
# Simplification Rule Base Class
# =============================================================================

class SimplificationRule(ABC):
    """Base class for expression simplification rules."""

    def __init__(self, name: str):
        self.name = name
        self.apply_count = 0

    @abstractmethod
    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        """Check if this rule can be applied to the instruction."""
        pass

    @abstractmethod
    def apply(self, inst: SSAInstruction, ssa_func: SSAFunction) -> Optional[SSAInstruction]:
        """
        Apply the transformation.

        Returns:
            New instruction if transformation succeeded, None otherwise.
        """
        pass

    def __repr__(self):
        return f"{self.name}(applied={self.apply_count})"


# =============================================================================
# Helper Functions
# =============================================================================

def is_constant(value: SSAValue) -> bool:
    """Check if SSA value is a constant."""
    # Constants have no producer instruction (loaded from data segment or immediate)
    # OR their producer is GCP (get constant from data segment)
    if value.producer_inst is None:
        # Check if name indicates constant (e.g., "const_42")
        return value.name.startswith("const_") or value.name.startswith("lit_")

    if value.producer_inst.mnemonic == "GCP":
        return True

    return False


def get_constant_value(value: SSAValue, ssa_func: SSAFunction) -> Optional[int]:
    """Extract constant value from SSA value."""
    if not is_constant(value):
        return None

    # Try to get from metadata
    if "constant_value" in value.metadata:
        return value.metadata["constant_value"]

    # Try to extract from name (const_42 → 42)
    if value.name.startswith("const_"):
        try:
            return int(value.name.split("_")[1])
        except (ValueError, IndexError):
            pass

    # Try to extract from literal name (lit_0x1234 → 0x1234)
    if value.name.startswith("lit_"):
        try:
            lit_part = value.name.split("_", 1)[1]
            if lit_part.startswith("0x"):
                return int(lit_part, 16)
            return int(lit_part)
        except (ValueError, IndexError):
            pass

    return None


def create_constant_value(value: int, value_type: opcodes.ResultType,
                         ssa_func: SSAFunction) -> SSAValue:
    """Create a new constant SSA value."""
    name = f"const_{value}"

    # Check if this constant already exists
    if name in ssa_func.values:
        return ssa_func.values[name]

    # Create new constant value
    const_val = SSAValue(
        name=name,
        value_type=value_type,
        producer=None,
        metadata={"constant_value": value}
    )
    ssa_func.values[name] = const_val
    return const_val


def is_commutative(mnemonic: str) -> bool:
    """Check if operation is commutative (a op b = b op a)."""
    COMMUTATIVE_OPS = {
        "ADD", "MUL",           # Integer
        "FADD", "FMUL",         # Float
        "DADD", "DMUL",         # Double
        "BA", "BO", "BX",       # Bitwise AND, OR, XOR
        "EQU", "NEQ",           # Equality
        "FEQU", "FNEQ",         # Float equality
        "DEQU", "DNEQ",         # Double equality
    }
    return mnemonic in COMMUTATIVE_OPS


# =============================================================================
# Rule 1: Constant Folding
# =============================================================================

class RuleConstantFold(SimplificationRule):
    """
    Fold arithmetic/bitwise operations on constants.

    Examples:
        2 + 3 → 5
        10 * 4 → 40
        0xff & 0x0f → 0x0f
    """

    def __init__(self):
        super().__init__("RuleConstantFold")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Must have at least one input
        if len(inst.inputs) < 1:
            return False

        # All inputs must be constants
        return all(is_constant(inp) for inp in inst.inputs)

    def apply(self, inst: SSAInstruction, ssa_func: SSAFunction) -> Optional[SSAInstruction]:
        # Get constant values
        const_values = []
        for inp in inst.inputs:
            val = get_constant_value(inp, ssa_func)
            if val is None:
                return None
            const_values.append(val)

        # Compute result based on operation
        result = self._compute_operation(inst.mnemonic, const_values)
        if result is None:
            return None

        # Create constant value for result
        result_const = create_constant_value(result, inst.outputs[0].value_type, ssa_func)

        # Create new instruction that just produces the constant
        # (In practice, we'll replace uses of the output with the constant directly)
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="CONST",
            address=inst.address,
            inputs=[result_const],
            outputs=inst.outputs,
            instruction=inst.instruction
        )

        self.apply_count += 1
        logger.debug(f"RuleConstantFold: {inst.mnemonic}({', '.join(str(v) for v in const_values)}) → {result}")
        return new_inst

    def _compute_operation(self, mnemonic: str, values: List[int]) -> Optional[int]:
        """Compute the result of the operation."""
        if len(values) == 1:
            v = values[0]
            if mnemonic == "NEG":
                return -v & 0xFFFFFFFF
            elif mnemonic == "BN":  # Bitwise NOT
                return ~v & 0xFFFFFFFF
            # Add more unary operations as needed
            return None

        if len(values) == 2:
            a, b = values

            # Integer arithmetic
            if mnemonic == "ADD":
                return (a + b) & 0xFFFFFFFF
            elif mnemonic == "SUB":
                return (a - b) & 0xFFFFFFFF
            elif mnemonic == "MUL":
                return (a * b) & 0xFFFFFFFF
            elif mnemonic in ("DIV", "IDIV"):
                if b == 0:
                    return None  # Don't fold division by zero
                return (a // b) & 0xFFFFFFFF
            elif mnemonic == "MOD":
                if b == 0:
                    return None
                return (a % b) & 0xFFFFFFFF

            # Bitwise operations
            elif mnemonic == "BA":  # Bitwise AND
                return (a & b) & 0xFFFFFFFF
            elif mnemonic == "BO":  # Bitwise OR
                return (a | b) & 0xFFFFFFFF
            elif mnemonic == "BX":  # Bitwise XOR
                return (a ^ b) & 0xFFFFFFFF
            elif mnemonic == "LS":  # Left shift
                return (a << (b & 0x1F)) & 0xFFFFFFFF
            elif mnemonic == "RS":  # Right shift
                return (a >> (b & 0x1F)) & 0xFFFFFFFF

            # Comparisons (return 0 or 1)
            elif mnemonic == "EQU":
                return 1 if a == b else 0
            elif mnemonic == "NEQ":
                return 1 if a != b else 0
            elif mnemonic == "LES":
                return 1 if a < b else 0
            elif mnemonic == "LEQ":
                return 1 if a <= b else 0
            elif mnemonic == "GRE":
                return 1 if a > b else 0
            elif mnemonic == "GEQ":
                return 1 if a >= b else 0

        return None


# =============================================================================
# Rule 2: Canonical Term Ordering
# =============================================================================

class RuleTermOrder(SimplificationRule):
    """
    Canonicalize commutative operations for CSE.

    Transform: 3 + x → x + 3
              const + var → var + const

    This enables common subexpression elimination by ensuring
    equivalent expressions have identical form.
    """

    def __init__(self):
        super().__init__("RuleTermOrder")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Must be commutative
        if not is_commutative(inst.mnemonic):
            return False

        # Must have exactly 2 inputs
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Constants should be on the right
        left_is_const = is_constant(left)
        right_is_const = is_constant(right)

        if left_is_const and not right_is_const:
            return True  # Need to swap

        # If both non-constant, order by name for determinism
        if not left_is_const and not right_is_const:
            return left.name > right.name

        return False

    def apply(self, inst: SSAInstruction, ssa_func: SSAFunction) -> Optional[SSAInstruction]:
        # Swap operands
        inst.inputs[0], inst.inputs[1] = inst.inputs[1], inst.inputs[0]

        self.apply_count += 1
        logger.debug(f"RuleTermOrder: Swapped operands of {inst.mnemonic}")
        return inst


# =============================================================================
# Rule 3: Algebraic Identities - AND
# =============================================================================

class RuleAndIdentity(SimplificationRule):
    """
    Simplify bitwise AND with identity values.

    Examples:
        x & -1 → x   (AND with all 1s)
        x & 0 → 0    (AND with 0)
        x & x → x    (AND with self)
    """

    def __init__(self):
        super().__init__("RuleAndIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BA":  # Bitwise AND
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(self, inst: SSAInstruction, ssa_func: SSAFunction) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x & 0 → 0
        right_val = get_constant_value(right, ssa_func)
        if right_val == 0:
            # Replace with constant 0
            const_zero = create_constant_value(0, inst.outputs[0].value_type, ssa_func)
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="CONST",
                address=inst.address,
                inputs=[const_zero],
                outputs=inst.outputs,
                instruction=inst.instruction
            )
            self.apply_count += 1
            logger.debug(f"RuleAndIdentity: x & 0 → 0")
            return new_inst

        # Check for x & -1 (0xFFFFFFFF) → x
        if right_val == 0xFFFFFFFF or right_val == -1:
            # Replace with left operand
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction
            )
            self.apply_count += 1
            logger.debug(f"RuleAndIdentity: x & -1 → x")
            return new_inst

        # Check for x & x → x
        if left.name == right.name:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction
            )
            self.apply_count += 1
            logger.debug(f"RuleAndIdentity: x & x → x")
            return new_inst

        return None


# =============================================================================
# Rule 4: Algebraic Identities - OR
# =============================================================================

class RuleOrIdentity(SimplificationRule):
    """
    Simplify bitwise OR with identity values.

    Examples:
        x | 0 → x    (OR with 0)
        x | -1 → -1  (OR with all 1s)
        x | x → x    (OR with self)
    """

    def __init__(self):
        super().__init__("RuleOrIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BO":  # Bitwise OR
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(self, inst: SSAInstruction, ssa_func: SSAFunction) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x | 0 → x
        right_val = get_constant_value(right, ssa_func)
        if right_val == 0:
            # Replace with left operand
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction
            )
            self.apply_count += 1
            logger.debug(f"RuleOrIdentity: x | 0 → x")
            return new_inst

        # Check for x | -1 → -1
        if right_val == 0xFFFFFFFF or right_val == -1:
            # Replace with constant -1
            const_all_ones = create_constant_value(0xFFFFFFFF, inst.outputs[0].value_type, ssa_func)
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="CONST",
                address=inst.address,
                inputs=[const_all_ones],
                outputs=inst.outputs,
                instruction=inst.instruction
            )
            self.apply_count += 1
            logger.debug(f"RuleOrIdentity: x | -1 → -1")
            return new_inst

        # Check for x | x → x
        if left.name == right.name:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction
            )
            self.apply_count += 1
            logger.debug(f"RuleOrIdentity: x | x → x")
            return new_inst

        return None


# =============================================================================
# Rule 5: Algebraic Identities - ADD
# =============================================================================

class RuleAddIdentity(SimplificationRule):
    """
    Simplify addition with identity values.

    Examples:
        x + 0 → x
        0 + x → x
    """

    def __init__(self):
        super().__init__("RuleAddIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("ADD", "FADD", "DADD"):
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(self, inst: SSAInstruction, ssa_func: SSAFunction) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x + 0 → x
        right_val = get_constant_value(right, ssa_func)
        if right_val == 0:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction
            )
            self.apply_count += 1
            logger.debug(f"RuleAddIdentity: x + 0 → x")
            return new_inst

        # Check for 0 + x → x (after term ordering, this shouldn't happen, but be safe)
        left_val = get_constant_value(left, ssa_func)
        if left_val == 0:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[right],
                outputs=inst.outputs,
                instruction=inst.instruction
            )
            self.apply_count += 1
            logger.debug(f"RuleAddIdentity: 0 + x → x")
            return new_inst

        return None


# =============================================================================
# Rule 6: Algebraic Identities - MUL
# =============================================================================

class RuleMulIdentity(SimplificationRule):
    """
    Simplify multiplication with identity values.

    Examples:
        x * 1 → x
        x * 0 → 0
    """

    def __init__(self):
        super().__init__("RuleMulIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("MUL", "FMUL", "DMUL"):
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(self, inst: SSAInstruction, ssa_func: SSAFunction) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x * 1 → x
        right_val = get_constant_value(right, ssa_func)
        if right_val == 1:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction
            )
            self.apply_count += 1
            logger.debug(f"RuleMulIdentity: x * 1 → x")
            return new_inst

        # Check for x * 0 → 0
        if right_val == 0:
            const_zero = create_constant_value(0, inst.outputs[0].value_type, ssa_func)
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="CONST",
                address=inst.address,
                inputs=[const_zero],
                outputs=inst.outputs,
                instruction=inst.instruction
            )
            self.apply_count += 1
            logger.debug(f"RuleMulIdentity: x * 0 → 0")
            return new_inst

        return None


# =============================================================================
# Rule 7: Nested AND Mask Simplification
# =============================================================================

class RuleAndMask(SimplificationRule):
    """
    Simplify nested AND operations with constants.

    Examples:
        (x & 0xff) & 0x0f → x & 0x0f
        (x & m1) & m2 → x & (m1 & m2)

    From Ghidra's ruleaction.cc.
    """

    def __init__(self):
        super().__init__("RuleAndMask")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BA":  # Bitwise AND
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant
        if not is_constant(right):
            return False

        # Left must be result of another AND with constant
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic != "BA":
            return False
        if len(left.producer_inst.inputs) != 2:
            return False

        # The inner AND's right operand must also be constant
        inner_right = left.producer_inst.inputs[1]
        return is_constant(inner_right)

    def apply(self, inst: SSAInstruction, ssa_func: SSAFunction) -> Optional[SSAInstruction]:
        left, right = inst.inputs
        inner_and = left.producer_inst

        # Get mask values
        outer_mask = get_constant_value(right, ssa_func)
        inner_mask = get_constant_value(inner_and.inputs[1], ssa_func)

        if outer_mask is None or inner_mask is None:
            return None

        # Combine masks
        combined_mask = outer_mask & inner_mask

        # Create new instruction: x & combined_mask
        combined_const = create_constant_value(combined_mask, inst.outputs[0].value_type, ssa_func)
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="BA",
            address=inst.address,
            inputs=[inner_and.inputs[0], combined_const],  # x, combined_mask
            outputs=inst.outputs,
            instruction=inst.instruction
        )

        self.apply_count += 1
        logger.debug(f"RuleAndMask: (x & 0x{inner_mask:x}) & 0x{outer_mask:x} → x & 0x{combined_mask:x}")
        return new_inst


# =============================================================================
# Rule 8: Nested OR Mask Simplification
# =============================================================================

class RuleOrMask(SimplificationRule):
    """
    Simplify nested OR operations with constants.

    Examples:
        (x | 0x0f) | 0xff → x | 0xff
        (x | m1) | m2 → x | (m1 | m2)
    """

    def __init__(self):
        super().__init__("RuleOrMask")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "BO":  # Bitwise OR
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant
        if not is_constant(right):
            return False

        # Left must be result of another OR with constant
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic != "BO":
            return False
        if len(left.producer_inst.inputs) != 2:
            return False

        # The inner OR's right operand must also be constant
        inner_right = left.producer_inst.inputs[1]
        return is_constant(inner_right)

    def apply(self, inst: SSAInstruction, ssa_func: SSAFunction) -> Optional[SSAInstruction]:
        left, right = inst.inputs
        inner_or = left.producer_inst

        # Get mask values
        outer_mask = get_constant_value(right, ssa_func)
        inner_mask = get_constant_value(inner_or.inputs[1], ssa_func)

        if outer_mask is None or inner_mask is None:
            return None

        # Combine masks
        combined_mask = outer_mask | inner_mask

        # Create new instruction: x | combined_mask
        combined_const = create_constant_value(combined_mask, inst.outputs[0].value_type, ssa_func)
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="BO",
            address=inst.address,
            inputs=[inner_or.inputs[0], combined_const],  # x, combined_mask
            outputs=inst.outputs,
            instruction=inst.instruction
        )

        self.apply_count += 1
        logger.debug(f"RuleOrMask: (x | 0x{inner_mask:x}) | 0x{outer_mask:x} → x | 0x{combined_mask:x}")
        return new_inst


# =============================================================================
# Simplification Engine
# =============================================================================

# Default rule set
DEFAULT_RULES = [
    RuleTermOrder(),        # Apply first for canonical form
    RuleConstantFold(),     # Fold constants
    RuleAndIdentity(),      # x & 0, x & -1, x & x
    RuleOrIdentity(),       # x | 0, x | -1, x | x
    RuleAddIdentity(),      # x + 0
    RuleMulIdentity(),      # x * 1, x * 0
    RuleAndMask(),          # (x & m1) & m2
    RuleOrMask(),           # (x | m1) | m2
]


@dataclass
class SimplificationStats:
    """Statistics from simplification pass."""
    iterations: int = 0
    total_changes: int = 0
    rules_applied: Dict[str, int] = None

    def __post_init__(self):
        if self.rules_applied is None:
            self.rules_applied = {}


def simplify_expressions(
    ssa_func: SSAFunction,
    rules: Optional[List[SimplificationRule]] = None,
    max_iterations: int = 10,
    debug: bool = False
) -> SimplificationStats:
    """
    Apply simplification rules iteratively until convergence.

    Args:
        ssa_func: SSA function to simplify
        rules: Optional custom rule set (uses DEFAULT_RULES if None)
        max_iterations: Maximum number of iterations (default 10)
        debug: Enable debug logging

    Returns:
        Statistics about the simplification process
    """
    if rules is None:
        rules = DEFAULT_RULES

    if debug:
        logger.setLevel(logging.DEBUG)

    stats = SimplificationStats()

    for iteration in range(max_iterations):
        changed = False
        stats.iterations = iteration + 1

        # Try each rule on each instruction
        for block_id in sorted(ssa_func.instructions.keys()):
            block_insts = ssa_func.instructions[block_id]

            for inst_idx, inst in enumerate(block_insts):
                # Skip PHI nodes and non-computational instructions
                if inst.mnemonic in ("PHI", "CONST", "ASGN", "XCALL", "CALL", "RET"):
                    continue

                for rule in rules:
                    if rule.matches(inst, ssa_func):
                        new_inst = rule.apply(inst, ssa_func)
                        if new_inst is not None:
                            # Replace instruction
                            block_insts[inst_idx] = new_inst
                            changed = True
                            stats.total_changes += 1
                            stats.rules_applied[rule.name] = stats.rules_applied.get(rule.name, 0) + 1

                            if debug:
                                logger.debug(f"  Replaced instruction at {inst.address}")

                            break  # Move to next instruction after one rule applies

        if not changed:
            logger.debug(f"Simplification converged after {iteration + 1} iterations")
            break

    # Log summary
    logger.info(f"Simplification complete: {stats.total_changes} changes in {stats.iterations} iterations")
    for rule_name, count in stats.rules_applied.items():
        logger.info(f"  {rule_name}: {count}")

    return stats
