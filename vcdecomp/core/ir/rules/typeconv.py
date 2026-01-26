"""
Type conversion simplification rules.

This module implements rules for simplifying type conversions:
- RuleCastChain: Eliminate redundant cast chains
- RuleCastIdentity: Remove identity casts (int→int)
- RuleCastConstant: Fold constants through casts
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


class RuleCastChain(SimplificationRule):
    """
    Simplify chains of type conversions.

    Examples:
        int→float→int → int (identity if types match)
        char→int→char → char (if within range)
        int→short→int → int (preserving only conversion)
    """

    def __init__(self):
        super().__init__("RuleCastChain")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check if this is a type conversion operation
        if inst.mnemonic not in (
            "CTOI",
            "STOI",
            "ITOC",
            "ITOS",
            "ITOF",
            "ITOD",
            "FTOI",
            "FTOD",
            "DTOI",
            "DTOF",
        ):
            return False

        if len(inst.inputs) != 1:
            return False

        # Input must be result of another conversion
        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        inner_inst = input_val.producer_inst
        return inner_inst.mnemonic in (
            "CTOI",
            "STOI",
            "ITOC",
            "ITOS",
            "ITOF",
            "ITOD",
            "FTOI",
            "FTOD",
            "DTOI",
            "DTOF",
        )

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        inner_inst = inst.inputs[0].producer_inst
        original = inner_inst.inputs[0]

        # Check for identity chain: T1→T2→T1
        # Example: int→float→int could potentially just be int
        # But we need to be careful about precision loss

        # For now, only handle simple cases
        # ITOF→FTOI could lose precision, so keep it
        # CTOI→ITOC is safe if value fits in char range

        # Simple case: if we can determine the chain is identity, collapse it
        # For example: ITOC→CTOI → identity (with clamping)

        if inst.mnemonic == "CTOI" and inner_inst.mnemonic == "ITOC":
            # int→char→int: This is not quite identity due to truncation
            # But if we know the value fits, we can eliminate
            # For now, keep conservative
            pass

        # Most conversion chains should be kept for safety
        # unless we can prove they're no-ops
        return None


class RuleCastIdentity(SimplificationRule):
    """
    Remove identity casts (same type to same type).

    Examples:
        int→int (should not exist, but remove if present)
        float→float
    """

    def __init__(self):
        super().__init__("RuleCastIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # In practice, the compiler shouldn't generate identity casts
        # But if they exist, we should remove them

        # Since we don't have explicit type information in the opcode,
        # we rely on the SSA value types
        if len(inst.inputs) != 1:
            return False

        # Check if input and output types are the same
        input_type = inst.inputs[0].value_type
        output_type = inst.outputs[0].value_type if inst.outputs else None

        if output_type is None:
            return False

        # Same type = identity cast
        return input_type == output_type

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Replace with COPY
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="COPY",
            address=inst.address,
            inputs=inst.inputs,
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleCastIdentity: identity cast removed")
        return new_inst


class RuleCastConstant(SimplificationRule):
    """
    Fold constants through type conversions.

    Examples:
        int(5.7) → 5
        float(10) → 10.0
        char(300) → 44 (with overflow)
    """

    def __init__(self):
        super().__init__("RuleCastConstant")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check if this is a type conversion operation
        if inst.mnemonic not in (
            "CTOI",
            "STOI",
            "ITOC",
            "ITOS",
            "ITOF",
            "ITOD",
            "FTOI",
            "FTOD",
            "DTOI",
            "DTOF",
        ):
            return False

        if len(inst.inputs) != 1:
            return False

        # Input must be constant
        return is_constant(inst.inputs[0])

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        input_val = get_constant_value(inst.inputs[0], ssa_func)
        if input_val is None:
            return None

        # Compute result based on conversion type
        result = self._apply_conversion(inst.mnemonic, input_val)
        if result is None:
            return None

        # Create constant with result
        result_const = create_constant_value(
            result, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="CONST",
            address=inst.address,
            inputs=[result_const],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleCastConstant: {inst.mnemonic}({input_val}) → {result}")
        return new_inst

    def _apply_conversion(self, mnemonic: str, value: int) -> Optional[int]:
        """Apply type conversion to constant value."""
        # For integer conversions, we treat everything as integers
        # (float conversions would need proper float handling)

        if mnemonic == "ITOC":
            # Int to char: truncate to 8 bits
            return value & 0xFF
        elif mnemonic == "ITOS":
            # Int to short: truncate to 16 bits
            return value & 0xFFFF
        elif mnemonic == "CTOI":
            # Char to int: already an int, but ensure proper sign extension if signed
            # For now, treat as zero-extend
            return value & 0xFF
        elif mnemonic == "STOI":
            # Short to int: ensure proper sign extension if signed
            # For now, treat as zero-extend
            return value & 0xFFFF

        # Float conversions would need proper handling
        # For now, don't fold float conversions
        if mnemonic in ("ITOF", "ITOD", "FTOI", "FTOD", "DTOI", "DTOF"):
            return None

        return None
