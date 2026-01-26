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


class RuleSubIdentity(SimplificationRule):
    """
    Simplify subtraction with identity values.

    Examples:
        x - 0 → x
        x - x → 0
    """

    def __init__(self):
        super().__init__("RuleSubIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("SUB", "FSUB", "DSUB"):
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x - 0 → x
        right_val = get_constant_value(right, ssa_func)
        if right_val == 0:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleSubIdentity: x - 0 → x")
            return new_inst

        # Check for x - x → 0
        if left.name == right.name:
            const_zero = create_constant_value(0, inst.outputs[0].value_type, ssa_func)
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="CONST",
                address=inst.address,
                inputs=[const_zero],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleSubIdentity: x - x → 0")
            return new_inst

        return None


class RuleDivIdentity(SimplificationRule):
    """
    Simplify division with identity values.

    Examples:
        x / 1 → x
    """

    def __init__(self):
        super().__init__("RuleDivIdentity")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("DIV", "IDIV", "FDIV", "DDIV"):
            return False
        if len(inst.inputs) != 2:
            return False
        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        # Check for x / 1 → x
        right_val = get_constant_value(right, ssa_func)
        if right_val == 1:
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[left],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleDivIdentity: x / 1 → x")
            return new_inst

        return None


class RuleMulByPowerOf2(SimplificationRule):
    """
    Convert multiplication by power of 2 to left shift.

    Examples:
        x * 2 → x << 1
        x * 4 → x << 2
        x * 8 → x << 3

    Only applies when beneficial (shift is usually faster/clearer for indexing).
    """

    def __init__(self):
        super().__init__("RuleMulByPowerOf2")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "MUL":
            return False
        if len(inst.inputs) != 2:
            return False

        # Right operand must be a power of 2 constant
        right = inst.inputs[1]
        if not is_constant(right):
            return False

        right_val = get_constant_value(right, ssa_func)
        if right_val is None or right_val <= 0:
            return False

        # Import helper from base
        from .base import is_power_of_two

        return is_power_of_two(right_val)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        right_val = get_constant_value(right, ssa_func)
        if right_val is None:
            return None

        # Get shift amount
        from .base import log2_of_power_of_two

        shift_amount = log2_of_power_of_two(right_val)
        if shift_amount is None:
            return None

        # Create shift instruction: x << shift_amount
        shift_const = create_constant_value(
            shift_amount, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="LS",  # Left shift
            address=inst.address,
            inputs=[left, shift_const],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleMulByPowerOf2: x * {right_val} → x << {shift_amount}")
        return new_inst


class RuleDivByPowerOf2(SimplificationRule):
    """
    Convert unsigned division by power of 2 to right shift.

    Examples:
        x / 2 → x >> 1
        x / 4 → x >> 2
        x / 8 → x >> 3

    Note: Only safe for unsigned division. Signed division requires arithmetic shift.
    """

    def __init__(self):
        super().__init__("RuleDivByPowerOf2")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Only for unsigned division (DIV, not IDIV)
        if inst.mnemonic != "DIV":
            return False
        if len(inst.inputs) != 2:
            return False

        # Right operand must be a power of 2 constant
        right = inst.inputs[1]
        if not is_constant(right):
            return False

        right_val = get_constant_value(right, ssa_func)
        if right_val is None or right_val <= 0:
            return False

        from .base import is_power_of_two

        return is_power_of_two(right_val)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        right_val = get_constant_value(right, ssa_func)
        if right_val is None:
            return None

        # Get shift amount
        from .base import log2_of_power_of_two

        shift_amount = log2_of_power_of_two(right_val)
        if shift_amount is None:
            return None

        # Create shift instruction: x >> shift_amount
        shift_const = create_constant_value(
            shift_amount, inst.outputs[0].value_type, ssa_func
        )
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="RS",  # Right shift
            address=inst.address,
            inputs=[left, shift_const],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleDivByPowerOf2: x / {right_val} → x >> {shift_amount}")
        return new_inst


class RuleModByPowerOf2(SimplificationRule):
    """
    Convert modulo by power of 2 to bitwise AND.

    Examples:
        x % 2 → x & 1
        x % 4 → x & 3
        x % 8 → x & 7

    This optimization: x % (2^n) = x & (2^n - 1)
    """

    def __init__(self):
        super().__init__("RuleModByPowerOf2")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "MOD":
            return False
        if len(inst.inputs) != 2:
            return False

        # Right operand must be a power of 2 constant
        right = inst.inputs[1]
        if not is_constant(right):
            return False

        right_val = get_constant_value(right, ssa_func)
        if right_val is None or right_val <= 0:
            return False

        from .base import is_power_of_two

        return is_power_of_two(right_val)

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left, right = inst.inputs

        right_val = get_constant_value(right, ssa_func)
        if right_val is None:
            return None

        # Compute mask: 2^n - 1
        mask = right_val - 1

        # Create AND instruction: x & mask
        mask_const = create_constant_value(mask, inst.outputs[0].value_type, ssa_func)
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="BA",  # Bitwise AND
            address=inst.address,
            inputs=[left, mask_const],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleModByPowerOf2: x % {right_val} → x & 0x{mask:x}")
        return new_inst


class RuleMulZero(SimplificationRule):
    """
    Simplify multiplication by zero.

    Examples:
        x * 0 → 0
        0 * x → 0
    """

    def __init__(self):
        super().__init__("RuleMulZero")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic not in ("MUL", "FMUL", "DMUL"):
            return False
        if len(inst.inputs) != 2:
            return False

        # Either operand can be zero
        left, right = inst.inputs
        left_val = get_constant_value(left, ssa_func)
        right_val = get_constant_value(right, ssa_func)

        return left_val == 0 or right_val == 0

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # x * 0 → 0
        const_zero = create_constant_value(0, inst.outputs[0].value_type, ssa_func)
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="CONST",
            address=inst.address,
            inputs=[const_zero],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleMulZero: x * 0 → 0")
        return new_inst


class RuleModOne(SimplificationRule):
    """
    Simplify modulo by one.

    Examples:
        x % 1 → 0 (anything mod 1 is always 0)
    """

    def __init__(self):
        super().__init__("RuleModOne")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        if inst.mnemonic != "MOD":
            return False
        if len(inst.inputs) != 2:
            return False

        # Right operand must be 1
        right = inst.inputs[1]
        if not is_constant(right):
            return False

        right_val = get_constant_value(right, ssa_func)
        return right_val == 1

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # x % 1 → 0
        const_zero = create_constant_value(0, inst.outputs[0].value_type, ssa_func)
        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic="CONST",
            address=inst.address,
            inputs=[const_zero],
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleModOne: x % 1 → 0")
        return new_inst


class RuleMulDistribute(SimplificationRule):
    """
    Factor common terms from addition (distributive property in reverse).

    Examples:
        x * a + x * b → x * (a + b)
        x * 2 + x * 3 → x * 5

    This is useful for loop index calculations and array access patterns.
    """

    def __init__(self):
        super().__init__("RuleMulDistribute")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Must be addition
        if inst.mnemonic != "ADD":
            return False
        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Both operands must be multiplications
        if not left.producer_inst or not right.producer_inst:
            return False

        left_mul = left.producer_inst
        right_mul = right.producer_inst

        if left_mul.mnemonic != "MUL" or right_mul.mnemonic != "MUL":
            return False

        if len(left_mul.inputs) != 2 or len(right_mul.inputs) != 2:
            return False

        # Check if they share a common factor
        # Pattern: x * a + x * b
        left_ops = set([left_mul.inputs[0].name, left_mul.inputs[1].name])
        right_ops = set([right_mul.inputs[0].name, right_mul.inputs[1].name])

        common = left_ops & right_ops
        return len(common) == 1

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        left_mul = inst.inputs[0].producer_inst
        right_mul = inst.inputs[1].producer_inst

        # Find the common factor and the unique multipliers
        left_ops = {left_mul.inputs[0].name: left_mul.inputs[0],
                    left_mul.inputs[1].name: left_mul.inputs[1]}
        right_ops = {right_mul.inputs[0].name: right_mul.inputs[0],
                     right_mul.inputs[1].name: right_mul.inputs[1]}

        common_names = set(left_ops.keys()) & set(right_ops.keys())
        if len(common_names) != 1:
            return None

        common_name = list(common_names)[0]
        common_factor = left_ops[common_name]

        # Get the unique multipliers
        left_multiplier = [v for k, v in left_ops.items() if k != common_name][0]
        right_multiplier = [v for k, v in right_ops.items() if k != common_name][0]

        # Check if both multipliers are constants (easiest case)
        left_const = get_constant_value(left_multiplier, ssa_func)
        right_const = get_constant_value(right_multiplier, ssa_func)

        if left_const is not None and right_const is not None:
            # x * a + x * b → x * (a + b)
            combined_multiplier = (left_const + right_const) & 0xFFFFFFFF

            # Create new multiplication: x * (a + b)
            combined_const = create_constant_value(
                combined_multiplier, inst.outputs[0].value_type, ssa_func
            )

            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="MUL",
                address=inst.address,
                inputs=[common_factor, combined_const],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )

            self.apply_count += 1
            logger.debug(f"RuleMulDistribute: x*{left_const} + x*{right_const} → x*{combined_multiplier}")
            return new_inst

        # For non-constant multipliers, we'd need to create an ADD instruction
        # This requires multi-instruction transformation
        return None


class RuleCollectTerms(SimplificationRule):
    """
    Reorganize addition trees to collect like terms and enable CSE.

    Examples:
        a + b + c + d → canonical order for better matching
        (x + 2) + (x + 3) → enables RuleDoubleAdd
        x + y + x → 2*x + y (with term collection)

    This is a complex rule that establishes canonical form for addition chains.
    """

    def __init__(self):
        super().__init__("RuleCollectTerms")
        self.is_disabled = True  # Complex - needs careful implementation

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Must be addition
        if inst.mnemonic != "ADD":
            return False
        if len(inst.inputs) != 2:
            return False

        # At least one operand should be another ADD
        left, right = inst.inputs
        has_nested_add = False

        if left.producer_inst and left.producer_inst.mnemonic == "ADD":
            has_nested_add = True
        if right.producer_inst and right.producer_inst.mnemonic == "ADD":
            has_nested_add = True

        return has_nested_add

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # This is a complex transformation that requires:
        # 1. Flattening the addition tree
        # 2. Collecting like terms
        # 3. Sorting terms into canonical order
        # 4. Rebuilding the tree

        # This requires multi-instruction transformation and is beyond
        # the scope of single-instruction rules

        # For now, leave as placeholder
        return None
