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


class RuleSextChain(SimplificationRule):
    """
    Collapse redundant sign extension chains.

    Examples:
        sext(sext(x, 8), 16) → sext(x, 16)
        sext(sext(char_val, short), int) → sext(char_val, int)

    This simplifies nested sign extensions by keeping only the final extension.
    """

    def __init__(self):
        super().__init__("RuleSextChain")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check if this looks like a sign extension
        # In VC-Script, we don't have explicit SEXT, but we can detect patterns
        # For now, match conversion chains
        if inst.mnemonic not in ("CTOI", "STOI"):
            return False

        if len(inst.inputs) != 1:
            return False

        # Input must be result of another sign extension
        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        inner_inst = input_val.producer_inst
        # Inner must also be a widening conversion
        return inner_inst.mnemonic in ("CTOI", "STOI")

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        inner_inst = inst.inputs[0].producer_inst
        original = inner_inst.inputs[0]

        # Collapse: CTOI(CTOI(x)) → CTOI(x)
        # Or: STOI(CTOI(x)) → STOI(x)
        # We can collapse to the outer conversion only

        new_inst = SSAInstruction(
            block_id=inst.block_id,
            mnemonic=inst.mnemonic,
            address=inst.address,
            inputs=[original],  # Skip intermediate conversion
            outputs=inst.outputs,
            instruction=inst.instruction,
        )

        self.apply_count += 1
        logger.debug(f"RuleSextChain: {inst.mnemonic}({inner_inst.mnemonic}(x)) → {inst.mnemonic}(x)")
        return new_inst


class RuleTruncateZext(SimplificationRule):
    """
    Eliminate truncate-then-extend patterns.

    Examples:
        zext(trunc(x, 8), 32) → x (if x was already 32-bit or less)
        char(int(char_val)) → char_val

    When we truncate then extend back, we might be able to eliminate both operations.
    """

    def __init__(self):
        super().__init__("RuleTruncateZext")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check if this is a widening conversion
        if inst.mnemonic not in ("CTOI", "STOI"):
            return False

        if len(inst.inputs) != 1:
            return False

        # Input must be result of a narrowing conversion
        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        inner_inst = input_val.producer_inst
        # Inner must be a narrowing conversion
        return inner_inst.mnemonic in ("ITOC", "ITOS")

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        inner_inst = inst.inputs[0].producer_inst
        original = inner_inst.inputs[0]

        # Check if we're converting back to the same size
        # ITOC→CTOI: int → char → int (not identity due to truncation)
        # ITOS→STOI: int → short → int (not identity due to truncation)

        # We can only eliminate if the narrowing didn't lose information
        # This is hard to prove statically, so be conservative

        # Special case: if both conversions cancel exactly
        if inst.mnemonic == "CTOI" and inner_inst.mnemonic == "ITOC":
            # int→char→int: Not safe to eliminate without range analysis
            return None

        if inst.mnemonic == "STOI" and inner_inst.mnemonic == "ITOS":
            # int→short→int: Not safe to eliminate without range analysis
            return None

        # In general, truncate-then-extend loses information
        # Only safe to eliminate with value range analysis
        return None


class RuleBoolZext(SimplificationRule):
    """
    Detect boolean-to-integer conversion patterns.

    Examples:
        (x == y) being used as int → already returns 0/1
        (x < y) cast to int → comparison already produces int result

    Comparisons in VC-Script produce integer 0/1 results, so extending
    them to int is redundant.
    """

    def __init__(self):
        super().__init__("RuleBoolZext")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check if this is a widening conversion (CTOI, STOI)
        if inst.mnemonic not in ("CTOI", "STOI"):
            return False

        if len(inst.inputs) != 1:
            return False

        # Input must be result of a comparison
        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        # Check if producer is a comparison (these produce 0/1 results)
        return input_val.producer_inst.mnemonic in (
            "EQU", "NEQ", "LES", "LEQ", "GRE", "GEQ",
            "FEQU", "FNEQ", "FLES", "FLEQ", "FGRE", "FGEQ",
            "DEQU", "DNEQ", "DLES", "DLEQ", "DGRE", "DGEQ",
        )

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Comparison already produces 0/1 (int-sized), no need to extend
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
        logger.debug(f"RuleBoolZext: Eliminated redundant bool→int conversion")
        return new_inst


class RuleZextEliminate(SimplificationRule):
    """
    Eliminate unnecessary zero extensions based on value ranges.

    Examples:
        char_constant cast to int → if constant fits, just use constant
        Already-extended value being re-extended → redundant

    Note: Conservative - only eliminates when provably safe.
    """

    def __init__(self):
        super().__init__("RuleZextEliminate")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check for widening conversions
        if inst.mnemonic not in ("CTOI", "STOI"):
            return False

        if len(inst.inputs) != 1:
            return False

        input_val = inst.inputs[0]

        # Case 1: Input is a constant - check if it's already in range
        if is_constant(input_val):
            val = get_constant_value(input_val, ssa_func)
            if val is not None:
                # Check if value already fits in target range
                if inst.mnemonic == "CTOI" and 0 <= val <= 0xFF:
                    return True  # Char fits, extension is no-op
                if inst.mnemonic == "STOI" and 0 <= val <= 0xFFFF:
                    return True  # Short fits, extension is no-op

        # Case 2: Input is already extended (double extension)
        if input_val.producer_inst:
            producer = input_val.producer_inst
            # If already extended to same or larger size, redundant
            if producer.mnemonic in ("CTOI", "STOI"):
                return True

        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        input_val = inst.inputs[0]

        # If it's a constant, just use the constant directly
        if is_constant(input_val):
            # Value is already correct, just copy it
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=inst.inputs,
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleZextEliminate: Removed extension of constant")
            return new_inst

        # If input is already extended, skip this extension
        if input_val.producer_inst and input_val.producer_inst.mnemonic in ("CTOI", "STOI"):
            # Use the original pre-extended value
            original = input_val.producer_inst.inputs[0]
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic=inst.mnemonic,
                address=inst.address,
                inputs=[original],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleZextEliminate: Collapsed double extension")
            return new_inst

        return None


class RulePromoteTypes(SimplificationRule):
    """
    Apply C integer promotion rules to detect promoted operands.

    In C, char and short are promoted to int in expressions.
    This rule detects when small types have been promoted for arithmetic.

    Examples:
        ADD(CTOI(x), CTOI(y)) → both operands promoted for addition
        MUL(char, int) → char will be promoted

    Note: This is primarily for analysis/annotation rather than transformation.
    """

    def __init__(self):
        super().__init__("RulePromoteTypes")
        self.is_disabled = True  # Analysis-only, doesn't transform

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check if this is a binary arithmetic operation
        if inst.mnemonic not in ("ADD", "SUB", "MUL", "DIV", "MOD", "BA", "BO", "BX"):
            return False

        if len(inst.inputs) != 2:
            return False

        # Check if operands are promoted small types
        left, right = inst.inputs

        left_promoted = False
        right_promoted = False

        if left.producer_inst and left.producer_inst.mnemonic in ("CTOI", "STOI"):
            left_promoted = True

        if right.producer_inst and right.producer_inst.mnemonic in ("CTOI", "STOI"):
            right_promoted = True

        return left_promoted or right_promoted

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # This is an analysis rule - it could annotate types but doesn't transform
        # In the future, could add type annotations to SSA values here
        return None


class RuleCastPropagation(SimplificationRule):
    """
    Propagate cast information through expressions to detect redundant casts.

    Examples:
        (int)x + (int)y → result is already int
        (char)((char)x + (char)y) → outer cast may be redundant

    This helps eliminate casts that don't change the actual value range.
    """

    def __init__(self):
        super().__init__("RuleCastPropagation")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check for narrowing conversions (ITOC, ITOS)
        if inst.mnemonic not in ("ITOC", "ITOS"):
            return False

        if len(inst.inputs) != 1:
            return False

        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        producer = input_val.producer_inst

        # Check if producer is an arithmetic operation on already-narrowed values
        if producer.mnemonic not in ("ADD", "SUB", "MUL", "BA", "BO", "BX"):
            return False

        if len(producer.inputs) != 2:
            return False

        # Check if both operands are of the target narrow type
        left, right = producer.inputs

        target_size = "CTOI" if inst.mnemonic == "ITOC" else "STOI"

        left_narrow = left.producer_inst and left.producer_inst.mnemonic == target_size
        right_narrow = right.producer_inst and right.producer_inst.mnemonic == target_size

        # If both operands were widened from the narrow type, and now we're
        # narrowing back, there might be redundancy
        return left_narrow and right_narrow

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # This is complex - would need to operate on the producer instruction
        # to directly use the narrow values without promotion
        # For now, just detect the pattern (could optimize later)

        # In theory: (char)((int)a + (int)b) where a,b are char
        # Could become: a + b (char arithmetic)
        # But this requires multi-instruction transformation

        return None


class RuleIntegralPromotion(SimplificationRule):
    """
    Optimize arithmetic on promoted integral types.

    When both operands of an arithmetic operation are promoted from
    the same smaller type, we can sometimes optimize.

    Examples:
        CTOI(a) + CTOI(b) → could use char arithmetic if result fits
        STOI(x) * STOI(y) → short multiplication

    Note: Disabled by default as it requires careful value range analysis.
    """

    def __init__(self):
        super().__init__("RuleIntegralPromotion")
        self.is_disabled = True  # Requires value range analysis

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check for binary arithmetic
        if inst.mnemonic not in ("ADD", "SUB", "MUL"):
            return False

        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Both must be promoted from same type
        if not left.producer_inst or not right.producer_inst:
            return False

        left_conv = left.producer_inst.mnemonic
        right_conv = right.producer_inst.mnemonic

        # Same promotion type
        return left_conv == right_conv and left_conv in ("CTOI", "STOI")

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Would need to:
        # 1. Perform arithmetic in narrow type
        # 2. Verify no overflow
        # 3. Promote result

        # This is complex and requires value range analysis
        return None


class RuleFloatIntRoundtrip(SimplificationRule):
    """
    Detect and optimize float→int→float roundtrips.

    Examples:
        FTOI(ITOF(x)) → x (if x was originally int)
        ITOF(FTOI(f)) → not safe (loses precision)

    This detects unnecessary conversions through float.
    """

    def __init__(self):
        super().__init__("RuleFloatIntRoundtrip")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check for ITOF (int to float)
        if inst.mnemonic not in ("ITOF", "ITOD"):
            return False

        if len(inst.inputs) != 1:
            return False

        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        # Check if input is FTOI (float to int)
        producer = input_val.producer_inst
        return producer.mnemonic in ("FTOI", "DTOI")

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # ITOF(FTOI(x)) - this loses the fractional part
        # Not safe to eliminate without knowing the original type

        # Only safe if we know the original was an integer
        # For now, be conservative
        return None


class RuleConstantCast(SimplificationRule):
    """
    Propagate type information through constant casts.

    Examples:
        ITOC(0xFF) → 0xFF (already fits in char)
        ITOC(0x100) → 0x00 (truncates)
        STOI(constant) → constant (if in range)

    This ensures constants have correct values after casting.
    """

    def __init__(self):
        super().__init__("RuleConstantCast")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Any cast operation
        if inst.mnemonic not in ("CTOI", "STOI", "ITOC", "ITOS"):
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

        # Apply the cast to the constant
        if inst.mnemonic == "ITOC":
            result = input_val & 0xFF
        elif inst.mnemonic == "ITOS":
            result = input_val & 0xFFFF
        elif inst.mnemonic == "CTOI":
            result = input_val & 0xFF  # Zero-extend
        elif inst.mnemonic == "STOI":
            result = input_val & 0xFFFF  # Zero-extend
        else:
            return None

        # Create constant with cast value
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
        logger.debug(f"RuleConstantCast: {inst.mnemonic}({input_val}) → {result}")
        return new_inst


class RuleSignExtendDetect(SimplificationRule):
    """
    Detect sign extension patterns vs zero extension.

    Examples:
        CTOI of signed char → sign extension expected
        CTOI of unsigned char → zero extension

    In VC-Script, we need to infer whether values are signed or unsigned
    based on usage patterns.

    Note: This is primarily for type annotation rather than transformation.
    """

    def __init__(self):
        super().__init__("RuleSignExtendDetect")
        self.is_disabled = True  # Analysis-only

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Look for widening conversions
        if inst.mnemonic not in ("CTOI", "STOI"):
            return False

        # Check if the input is used in signed context
        # (comparisons with negative numbers, arithmetic that goes negative, etc.)

        # This requires data flow analysis
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Would annotate the SSA value with sign information
        return None


class RuleNarrowingRedundant(SimplificationRule):
    """
    Detect redundant narrowing operations.

    Examples:
        ITOC(x & 0xFF) → x is already char-sized
        ITOS(x & 0xFFFF) → x is already short-sized
        ITOC(CTOI(c)) → c (roundtrip)

    This eliminates unnecessary narrowing when value range is known.
    """

    def __init__(self):
        super().__init__("RuleNarrowingRedundant")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check for narrowing operations
        if inst.mnemonic not in ("ITOC", "ITOS"):
            return False

        if len(inst.inputs) != 1:
            return False

        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        producer = input_val.producer_inst

        # Case 1: Narrowing a value that was just widened (roundtrip)
        if inst.mnemonic == "ITOC" and producer.mnemonic == "CTOI":
            return True
        if inst.mnemonic == "ITOS" and producer.mnemonic == "STOI":
            return True

        # Case 2: Narrowing a masked value (x & 0xFF → already char-sized)
        if producer.mnemonic == "BA":  # Bitwise AND
            if len(producer.inputs) == 2:
                # Check if mask matches the narrowing size
                mask_val = get_constant_value(producer.inputs[1], ssa_func)
                if mask_val is not None:
                    if inst.mnemonic == "ITOC" and mask_val == 0xFF:
                        return True  # AND with 0xFF, then ITOC is redundant
                    if inst.mnemonic == "ITOS" and mask_val == 0xFFFF:
                        return True  # AND with 0xFFFF, then ITOS is redundant

        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        input_val = inst.inputs[0]
        producer = input_val.producer_inst

        # Case 1: Roundtrip - use original value
        if ((inst.mnemonic == "ITOC" and producer.mnemonic == "CTOI") or
            (inst.mnemonic == "ITOS" and producer.mnemonic == "STOI")):
            
            original = producer.inputs[0]
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[original],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleNarrowingRedundant: Eliminated roundtrip {producer.mnemonic}→{inst.mnemonic}")
            return new_inst

        # Case 2: Masked value - just use the masked result
        if producer.mnemonic == "BA":
            # The AND already limited the range, ITOC/ITOS is no-op
            new_inst = SSAInstruction(
                block_id=inst.block_id,
                mnemonic="COPY",
                address=inst.address,
                inputs=[input_val],
                outputs=inst.outputs,
                instruction=inst.instruction,
            )
            self.apply_count += 1
            logger.debug(f"RuleNarrowingRedundant: Eliminated narrowing after mask")
            return new_inst

        return None


class RuleTypeCoercion(SimplificationRule):
    """
    Optimize type coercion in mixed-type expressions.

    Examples:
        ITOF(x) + float_const → promote x to float
        FTOI(f) < int_const → compare in appropriate domain

    This handles implicit type conversions in expressions.

    Note: Disabled by default - needs careful semantic analysis.
    """

    def __init__(self):
        super().__init__("RuleTypeCoercion")
        self.is_disabled = True  # Complex semantic analysis required

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Look for operations mixing int and float
        if inst.mnemonic not in ("ADD", "SUB", "MUL", "DIV", "EQU", "LES", "LEQ", "GRE", "GEQ"):
            return False

        if len(inst.inputs) != 2:
            return False

        left, right = inst.inputs

        # Check if one is float-converted and other is not
        left_float = left.producer_inst and left.producer_inst.mnemonic in ("ITOF", "ITOD")
        right_float = right.producer_inst and right.producer_inst.mnemonic in ("ITOF", "ITOD")

        # Mixed types
        return left_float != right_float

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Would need to:
        # 1. Determine dominant type
        # 2. Coerce other operand
        # 3. Use appropriate operator (FADD vs ADD, etc.)

        # This requires knowing the operator variants and is complex
        return None
