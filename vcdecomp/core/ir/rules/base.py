"""
Base classes and utilities for simplification rules.

This module provides:
- SimplificationRule abstract base class
- Helper functions for constant detection and manipulation
- Commutative operation detection
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Union, List

from ...disasm import opcodes
from ..ssa import SSAFunction, SSAInstruction, SSAValue


class SimplificationRule(ABC):
    """
    Base class for expression simplification rules.

    Each rule implements pattern matching (matches) and transformation (apply).
    Rules are applied iteratively by the SimplificationEngine until convergence.
    """

    def __init__(self, name: str):
        self.name = name
        self.apply_count = 0
        self.is_disabled = False

    @abstractmethod
    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        """
        Check if this rule can be applied to the instruction.

        Args:
            inst: SSA instruction to check
            ssa_func: SSA function containing the instruction

        Returns:
            True if rule matches, False otherwise
        """
        pass

    @abstractmethod
    def apply(self, inst: SSAInstruction, ssa_func: SSAFunction) -> Union[SSAInstruction, List[SSAInstruction], None]:
        """
        Apply the transformation.

        Args:
            inst: SSA instruction to transform
            ssa_func: SSA function containing the instruction

        Returns:
            - None: No transformation
            - SSAInstruction: Single instruction replacement (most common)
            - List[SSAInstruction]: Multi-instruction transformation
              - First N-1 instructions inserted before target
              - Last instruction replaces target
              - Useful for rules that need intermediate values (e.g., De Morgan's laws)
        """
        pass

    def disable(self):
        """Disable this rule (won't be applied)."""
        self.is_disabled = True

    def enable(self):
        """Enable this rule."""
        self.is_disabled = False

    def reset_stats(self):
        """Reset statistics counters."""
        self.apply_count = 0

    def __repr__(self):
        status = "disabled" if self.is_disabled else f"applied={self.apply_count}"
        return f"{self.name}({status})"


# =============================================================================
# Helper Functions
# =============================================================================

def is_constant(value: SSAValue) -> bool:
    """
    Check if SSA value is a constant.

    A value is considered constant if:
    - It has no producer instruction (immediate value)
    - Its name starts with "const_" or "lit_"
    - Its producer is GCP (get constant from data segment)

    Args:
        value: SSA value to check

    Returns:
        True if value is constant, False otherwise
    """
    # Constants have no producer instruction (loaded from data segment or immediate)
    # OR their producer is GCP (get constant from data segment)
    if value.producer_inst is None:
        # Check if name indicates constant (e.g., "const_42")
        return value.name.startswith("const_") or value.name.startswith("lit_")

    if value.producer_inst.mnemonic == "GCP":
        return True

    return False


def get_constant_value(value: SSAValue, ssa_func: SSAFunction) -> Optional[int]:
    """
    Extract constant value from SSA value.

    Args:
        value: SSA value to extract from
        ssa_func: SSA function (unused but kept for API compatibility)

    Returns:
        Integer constant value, or None if not a constant
    """
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


def create_constant_value(
    value: int, value_type: opcodes.ResultType, ssa_func: SSAFunction
) -> SSAValue:
    """
    Create a new constant SSA value.

    Args:
        value: Integer constant value
        value_type: Type of the constant
        ssa_func: SSA function to add constant to

    Returns:
        SSA value representing the constant
    """
    name = f"const_{value}"

    # Check if this constant already exists
    if name in ssa_func.values:
        return ssa_func.values[name]

    # Create new constant value
    const_val = SSAValue(
        name=name,
        value_type=value_type,
        producer=None,
        metadata={"constant_value": value},
    )
    ssa_func.values[name] = const_val
    return const_val


def create_intermediate_value(
    name_prefix: str,
    value_type: opcodes.ResultType,
    ssa_func: SSAFunction
) -> SSAValue:
    """
    Create a new intermediate SSA value for multi-instruction transformations.

    This generates a unique temporary value name to avoid conflicts.

    Args:
        name_prefix: Prefix for the value name (e.g., "not_temp")
        value_type: Type of the value
        ssa_func: SSA function to add value to

    Returns:
        SSA value for the intermediate result
    """
    # Generate unique name by appending counter
    counter = 0
    while True:
        name = f"{name_prefix}_{counter}"
        if name not in ssa_func.values:
            break
        counter += 1

    # Create new intermediate value
    intermediate_val = SSAValue(
        name=name,
        value_type=value_type,
        producer=None,  # Will be set when instruction is created
    )
    ssa_func.values[name] = intermediate_val
    return intermediate_val


def is_commutative(mnemonic: str) -> bool:
    """
    Check if operation is commutative (a op b = b op a).

    Args:
        mnemonic: Operation mnemonic

    Returns:
        True if commutative, False otherwise
    """
    COMMUTATIVE_OPS = {
        "ADD",
        "MUL",  # Integer
        "FADD",
        "FMUL",  # Float
        "DADD",
        "DMUL",  # Double
        "BA",
        "BO",
        "BX",  # Bitwise AND, OR, XOR
        "EQU",
        "NEQ",  # Equality
        "FEQU",
        "FNEQ",  # Float equality
        "DEQU",
        "DNEQ",  # Double equality
    }
    return mnemonic in COMMUTATIVE_OPS


def is_associative(mnemonic: str) -> bool:
    """
    Check if operation is associative ((a op b) op c = a op (b op c)).

    Args:
        mnemonic: Operation mnemonic

    Returns:
        True if associative, False otherwise
    """
    ASSOCIATIVE_OPS = {
        "ADD",
        "MUL",  # Integer
        "FADD",
        "FMUL",  # Float (technically not always due to precision)
        "DADD",
        "DMUL",  # Double (technically not always due to precision)
        "BA",
        "BO",
        "BX",  # Bitwise AND, OR, XOR
    }
    return mnemonic in ASSOCIATIVE_OPS


def is_power_of_two(value: int) -> bool:
    """
    Check if value is a power of two.

    Args:
        value: Integer value to check

    Returns:
        True if value is power of two, False otherwise
    """
    if value <= 0:
        return False
    return (value & (value - 1)) == 0


def log2_of_power_of_two(value: int) -> Optional[int]:
    """
    Get log2 of a power-of-two value.

    Args:
        value: Power of two value

    Returns:
        Log2 of value, or None if not a power of two
    """
    if not is_power_of_two(value):
        return None

    log = 0
    while (1 << log) != value:
        log += 1
    return log
