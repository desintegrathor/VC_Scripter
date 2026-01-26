"""
Data flow optimization rules.

This module implements data flow analysis and optimization rules inspired by
Ghidra's data flow passes:

Phase 6 rules (12 rules):
- RuleCopyPropagation: Replace uses of copies with original values
- RuleConstantPropagation: Propagate constants through assignments
- RuleDeadValue: Remove unused SSA values (disabled - needs use-def chains)
- RuleIdentityCopy: Remove identity copy patterns (x = x)
- RulePhiSimplify: Simplify phi nodes with identical inputs (disabled - needs CFG)
- RuleSingleUseInline: Inline single-use temporary values (disabled - needs use counts)
- RuleRedundantCopy: Eliminate redundant copy chains
- RuleValueNumbering: Detect equivalent expressions (disabled - needs value numbering table)
- RuleUnusedResult: Eliminate operations whose results are unused (disabled - needs use-def)
- RuleCopyChain: Simplify copy chains (x = y, z = x → z = y)
- RuleTrivialPhi: Eliminate trivial phi nodes (disabled - needs CFG)
- RuleForwardSubstitution: Forward substitute simple expressions (disabled - needs use analysis)
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


class RuleCopyPropagation(SimplificationRule):
    """
    Replace uses of copies with original values.

    Examples:
        x = y
        z = x + 1  →  z = y + 1

    This is a fundamental SSA optimization enabled by use-def chains.

    Strategy:
    - For each instruction that uses a value
    - Check if that value is defined by a COPY instruction
    - Replace the use with the original source of the copy
    """

    def __init__(self):
        super().__init__("RuleCopyPropagation")
        self.is_disabled = False  # NOW ENABLED with use-def chains!

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        """
        Match if instruction has any input defined by a COPY instruction.
        """
        # Need use-def chains
        if not hasattr(ssa_func, 'use_def_chains'):
            return False

        chains = ssa_func.use_def_chains

        # Check each input
        for input_val in inst.inputs:
            def_inst = chains.get_def(input_val)
            if def_inst and chains.is_copy_instruction(def_inst):
                return True

        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Replace copy inputs with original sources.
        """
        chains = ssa_func.use_def_chains
        new_inputs = []
        changed = False

        for input_val in inst.inputs:
            def_inst = chains.get_def(input_val)
            if def_inst and chains.is_copy_instruction(def_inst):
                # Replace with the original source
                original_source = def_inst.inputs[0]
                new_inputs.append(original_source)
                changed = True
            else:
                # Keep original input
                new_inputs.append(input_val)

        if not changed:
            return None

        # Create new instruction with propagated values
        return SSAInstruction(
            block_id=inst.block_id,
            mnemonic=inst.mnemonic,
            address=inst.address,
            inputs=new_inputs,
            outputs=inst.outputs,
            instruction=inst.instruction,
            metadata=inst.metadata,
        )


class RuleConstantPropagation(SimplificationRule):
    """
    Propagate constants through assignments.

    Examples:
        x = 5
        y = x + 3  →  y = 5 + 3  →  y = 8

    This combines constant assignment tracking with constant folding.
    Works with use-def chains to find constant definitions.
    """

    def __init__(self):
        super().__init__("RuleConstantPropagation")
        self.is_disabled = False  # NOW ENABLED with use-def chains!

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        """
        Match if instruction has any input that's defined as a constant.
        """
        # Need use-def chains
        if not hasattr(ssa_func, 'use_def_chains'):
            return False

        chains = ssa_func.use_def_chains

        # Check each input - if it's a constant value, we can propagate
        for input_val in inst.inputs:
            # Skip values that are already constants
            if is_constant(input_val):
                continue

            # Check if defined as a constant
            const_val = chains.find_constant_def(input_val)
            if const_val is not None:
                return True

        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Replace variable inputs with their constant values.
        """
        chains = ssa_func.use_def_chains
        new_inputs = []
        changed = False

        for input_val in inst.inputs:
            # If already a constant, keep it
            if is_constant(input_val):
                new_inputs.append(input_val)
                continue

            # Try to find constant definition
            const_val = chains.find_constant_def(input_val)
            if const_val is not None:
                # Create constant value to replace variable
                const_ssa_val = create_constant_value(
                    const_val,
                    input_val.value_type,
                    ssa_func
                )
                new_inputs.append(const_ssa_val)
                changed = True
            else:
                # Keep original input
                new_inputs.append(input_val)

        if not changed:
            return None

        # Create new instruction with constant values
        return SSAInstruction(
            block_id=inst.block_id,
            mnemonic=inst.mnemonic,
            address=inst.address,
            inputs=new_inputs,
            outputs=inst.outputs,
            instruction=inst.instruction,
            metadata=inst.metadata,
        )


class RuleDeadValue(SimplificationRule):
    """
    Remove unused SSA values (dead code elimination).

    Examples:
        x = a + b  (x never used)
        →  (remove instruction if no side effects)

    Enabled by use-def chains which track value usage.

    Note: We cannot actually remove instructions in the current architecture
    (rules return replacement instructions, not None for removal).
    Instead, we mark dead values for later cleanup or convert to NOPs.

    For now, this rule is conservatively disabled to avoid breaking
    the IR structure. Future work could implement a separate DCE pass.
    """

    def __init__(self):
        super().__init__("RuleDeadValue")
        # Conservatively disabled - removing instructions requires
        # architectural changes to support returning None for deletion
        self.is_disabled = True

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        """
        Match instructions with unused outputs and no side effects.
        """
        # Need use-def chains
        if not hasattr(ssa_func, 'use_def_chains'):
            return False

        chains = ssa_func.use_def_chains

        # Skip instructions that must be preserved
        SIDE_EFFECT_OPS = {
            "CALL", "XCALL", "RET", "JMP", "JZ", "JNZ",
            "ASGN", "PHI", "CONST"  # PHI and CONST are structural
        }
        if inst.mnemonic in SIDE_EFFECT_OPS:
            return False

        # Check if all outputs are unused
        if not inst.outputs:
            return False

        for output_val in inst.outputs:
            if not chains.is_unused(output_val):
                return False

        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Mark for removal (currently disabled).

        In a proper implementation, we'd either:
        1. Return None to indicate removal (requires engine changes)
        2. Replace with NOP instruction
        3. Run separate DCE pass after simplification
        """
        # TODO: Implement proper dead code elimination
        # For now, do nothing
        return None


class RuleIdentityCopy(SimplificationRule):
    """
    Remove identity copy patterns.

    Examples:
        x = x  →  (remove)

    This handles degenerate copy cases.
    """

    def __init__(self):
        super().__init__("RuleIdentityCopy")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Check for COPY where source and destination are the same
        if inst.mnemonic != "COPY":
            return False
        if len(inst.inputs) != 1:
            return False

        # In SSA form, this would be rare, but check if input and output
        # refer to the same value (which would be a bug in SSA construction)
        # For now, this is more of a safety check
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        # Would mark instruction for removal
        return None


class RulePhiSimplify(SimplificationRule):
    """
    Simplify phi nodes with identical inputs.

    Examples:
        x = phi(y, y, y)  →  x = y

    This detects degenerate phi nodes.
    """

    def __init__(self):
        super().__init__("RulePhiSimplify")
        self.is_disabled = True  # Requires CFG and phi nodes

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Would check if PHI instruction has all identical inputs
        # Our IR may not have explicit PHI instructions
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Replace phi with simple copy.
        """
        return None


class RuleSingleUseInline(SimplificationRule):
    """
    Inline single-use temporary values (disabled - complex transformation).

    Examples:
        temp = a + b
        result = temp * 2  (temp used only once)
        →  result = (a + b) * 2

    This reduces temporary variables and can enable further optimizations.

    Note: This transformation is complex because:
    1. It requires creating new intermediate values in the SSA graph
    2. Current rule architecture only supports returning single instructions
    3. Expression tree inlining needs careful type and precedence handling

    This is better handled during code emission rather than at IR level.
    """

    def __init__(self):
        super().__init__("RuleSingleUseInline")
        # Disabled - requires ability to create intermediate instructions
        # and modify the SSA graph structure. Better handled at emission.
        self.is_disabled = True

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        """
        Match instructions that use single-use values (potential inline candidates).
        """
        # Need use-def chains
        if not hasattr(ssa_func, 'use_def_chains'):
            return False

        chains = ssa_func.use_def_chains

        # Look for inputs that are single-use and simple to inline
        for input_val in inst.inputs:
            if chains.is_single_use(input_val):
                def_inst = chains.get_def(input_val)
                if def_inst and self._is_inlinable(def_inst):
                    return True

        return False

    def _is_inlinable(self, inst: SSAInstruction) -> bool:
        """Check if instruction is safe and beneficial to inline."""
        # Only inline simple arithmetic/logic operations
        INLINABLE_OPS = {
            "ADD", "SUB", "MUL", "DIV", "MOD",
            "AND", "OR", "XOR", "NOT",
            "SHL", "SHR",
        }
        return inst.mnemonic in INLINABLE_OPS

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Inline single-use values (currently disabled).

        Proper implementation would require creating nested expression trees
        which is beyond the current rule transformation model.
        """
        # TODO: Implement when IR supports expression tree transformations
        return None


class RuleRedundantCopy(SimplificationRule):
    """
    Eliminate redundant copy chains.

    Examples:
        x = COPY(y)
        →  Replace x with y throughout (if safe)

    This is similar to copy propagation but simpler.
    """

    def __init__(self):
        super().__init__("RuleRedundantCopy")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Look for consecutive COPY instructions
        if inst.mnemonic != "COPY":
            return False
        if len(inst.inputs) != 1:
            return False

        input_val = inst.inputs[0]
        if not input_val.producer_inst:
            return False

        # Check if input is also a COPY
        return input_val.producer_inst.mnemonic == "COPY"

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Bypass intermediate copy: COPY(COPY(x)) → COPY(x).
        """
        input_val = inst.inputs[0]
        original_source = input_val.producer_inst.inputs[0]

        return SSAInstruction(
            id=inst.id,
            mnemonic="COPY",
            inputs=[original_source],
            output=inst.output,
        )


class RuleCopyChain(SimplificationRule):
    """
    Simplify copy chains.

    Examples:
        x = COPY(y)
        z = COPY(x)
        →  z = COPY(y)

    This is handled by RuleRedundantCopy but kept for clarity.
    """

    def __init__(self):
        super().__init__("RuleCopyChain")

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Same as RuleRedundantCopy
        return False  # Delegate to RuleRedundantCopy

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleValueNumbering(SimplificationRule):
    """
    Detect equivalent expressions using value numbering.

    Examples:
        x = a + b
        y = a + b  (same operands, same operation)
        →  y = x

    This is a form of common subexpression elimination.
    """

    def __init__(self):
        super().__init__("RuleValueNumbering")
        self.is_disabled = True  # Requires value numbering table

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Would need to:
        # 1. Maintain hash table of expression → value
        # 2. Check if current expression already computed
        # 3. Replace with existing value
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleUnusedResult(SimplificationRule):
    """
    Eliminate operations whose results are unused (same as RuleDeadValue).

    Examples:
        x = expensive_operation()  (x never used)
        →  (remove if no side effects)

    This is essentially the same as RuleDeadValue. Kept for compatibility
    with Ghidra's rule naming but delegates to same logic.
    """

    def __init__(self):
        super().__init__("RuleUnusedResult")
        # Same limitation as RuleDeadValue - cannot remove instructions
        # in current architecture
        self.is_disabled = True

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        """
        Match instructions with unused results (same as RuleDeadValue).
        """
        # Need use-def chains
        if not hasattr(ssa_func, 'use_def_chains'):
            return False

        chains = ssa_func.use_def_chains

        # Skip instructions that must be preserved
        SIDE_EFFECT_OPS = {
            "CALL", "XCALL", "RET", "JMP", "JZ", "JNZ",
            "ASGN", "PHI", "CONST"
        }
        if inst.mnemonic in SIDE_EFFECT_OPS:
            return False

        # Check if all outputs are unused
        if not inst.outputs:
            return False

        for output_val in inst.outputs:
            if not chains.is_unused(output_val):
                return False

        return True

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        Mark for removal (currently disabled).
        """
        # Same limitation as RuleDeadValue
        return None


class RuleTrivialPhi(SimplificationRule):
    """
    Eliminate trivial phi nodes.

    Examples:
        x = phi(y)  (single input)  →  x = y
        x = phi(y, y)  (all same)  →  x = y

    This detects degenerate phi nodes.
    """

    def __init__(self):
        super().__init__("RuleTrivialPhi")
        self.is_disabled = True  # Requires CFG and phi nodes

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        # Similar to RulePhiSimplify
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        return None


class RuleForwardSubstitution(SimplificationRule):
    """
    Forward substitute simple expressions (delegates to other rules).

    Examples:
        x = 5
        y = x  (simple assignment)
        z = y + 3
        →  z = 5 + 3

    This combines constant propagation with copy propagation.
    Since we already have RuleCopyPropagation and RuleConstantPropagation,
    this rule is redundant - those rules will apply iteratively to achieve
    the same effect.

    Kept for Ghidra compatibility but disabled.
    """

    def __init__(self):
        super().__init__("RuleForwardSubstitution")
        # Redundant with RuleCopyPropagation + RuleConstantPropagation
        # Those rules will apply iteratively to achieve forward substitution
        self.is_disabled = True

    def matches(self, inst: SSAInstruction, ssa_func: SSAFunction) -> bool:
        """
        Delegate to RuleCopyPropagation and RuleConstantPropagation.
        """
        return False

    def apply(
        self, inst: SSAInstruction, ssa_func: SSAFunction
    ) -> Optional[SSAInstruction]:
        """
        No-op - other rules handle this.
        """
        return None
