"""
Arithmetic simplification rules.

This module implements rules for arithmetic operations:
- RuleConstantFold: Evaluate operations on constants (2 + 3 → 5)
- RuleDoubleAdd: (x + a) + b → x + (a + b)
- RuleDoubleSub: (x - a) - b → x - (a + b)
- RuleSubToAdd: x - (-y) → x + y
- RuleNegateIdentity: -(-x) → x
"""

import logging
from typing import List, Optional

from .base import (
    SimplificationRule,
    is_constant,
    get_constant_value,
    create_constant_value,
)
from ..ssa import SSAFunction, SSAInstruction

logger = logging.getLogger(__name__)


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

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
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
        result_const = create_constant_value(
            result, inst.outputs[0].value_type, ssa_func
        )

        # Create new instruction that just produces the constant
        # (In practice, we'll replace uses of the output with the constant directly)
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="CONST",
            address=inst.address,
            inputs=[result_const],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(
            f"RuleConstantFold: {inst.mnemonic}({', '.join(str(v) for v in const_values)}) → {result}"
        )
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


class RuleDoubleAdd(SimplificationRule):
    """
    Simplify chained additions with constants.

    Examples:
        (x + 2) + 3 → x + 5
        (x + a) + b → x + (a + b) when a, b are constants
    """

    def __init__(self):
        super().__init__("RuleDoubleAdd")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "ADD":
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant
        if not is_constant(right):
            return False

        # Left must be result of another ADD
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic != "ADD":
            return False
        if len(left.producer_inst.inputs) != 2:
            return False

        # Inner ADD's right operand must be constant
        inner_right = left.producer_inst.inputs[1]
        return is_constant(inner_right)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs
        inner_add = left.producer_inst

        # Get constant values
        outer_const = get_constant_value(right, ssa_func)
        inner_const = get_constant_value(inner_add.inputs[1], ssa_func)

        if outer_const is None or inner_const is None:
            return None

        # Combine constants
        combined = (inner_const + outer_const) & 0xFFFFFFFF

        # Create new instruction: x + combined
        combined_const = create_constant_value(
            combined, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="ADD",
            address=inst.address,
            inputs=[inner_add.inputs[0], combined_const],  # x, combined
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(
            f"RuleDoubleAdd: (x + {inner_const}) + {outer_const} → x + {combined}"
        )
        return new_inst


class RuleDoubleSub(SimplificationRule):
    """
    Simplify chained subtractions with constants.

    Examples:
        (x - 2) - 3 → x - 5
        (x - a) - b → x - (a + b) when a, b are constants
    """

    def __init__(self):
        super().__init__("RuleDoubleSub")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "SUB":
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Right must be constant
        if not is_constant(right):
            return False

        # Left must be result of another SUB
        if not left.producer_inst:
            return False
        if left.producer_inst.mnemonic != "SUB":
            return False
        if len(left.producer_inst.inputs) != 2:
            return False

        # Inner SUB's right operand must be constant
        inner_right = left.producer_inst.inputs[1]
        return is_constant(inner_right)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs
        inner_sub = left.producer_inst

        # Get constant values
        outer_const = get_constant_value(right, ssa_func)
        inner_const = get_constant_value(inner_sub.inputs[1], ssa_func)

        if outer_const is None or inner_const is None:
            return None

        # Combine constants: x - a - b = x - (a + b)
        combined = (inner_const + outer_const) & 0xFFFFFFFF

        # Create new instruction: x - combined
        combined_const = create_constant_value(
            combined, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="SUB",
            address=inst.address,
            inputs=[inner_sub.inputs[0], combined_const],  # x, combined
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(
            f"RuleDoubleSub: (x - {inner_const}) - {outer_const} → x - {combined}"
        )
        return new_inst


class RuleNegateIdentity(SimplificationRule):
    """
    Remove double negation.

    Examples:
        -(-x) → x
    """

    def __init__(self):
        super().__init__("RuleNegateIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "NEG":
            return False
        if len(inst.inputs) != 1:
            return False

        # Input must be result of another NEG
        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False
        return input_val.producer_inst.mnemonic == "NEG"

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        inner_neg = inst.inputs[0].producer_inst

        # Get the original value (before double negation)
        original = inner_neg.inputs[0]

        # Create copy instruction
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="COPY",
            address=inst.address,
            inputs=[original],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleNegateIdentity: -(-x) → x")
        return new_inst
