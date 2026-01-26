"""
Use-Def chain analysis for SSA-level data flow optimizations.

This module provides efficient use-definition chain tracking for SSA values,
enabling data flow optimizations like:
- Copy propagation
- Constant propagation
- Dead value elimination
- Single-use inlining
- Common subexpression elimination

Use-def chains track:
- For each SSA value: which instructions USE it
- For each SSA value: which instruction DEFINES it

This is a foundational infrastructure that unlocks 7 high-impact data flow rules.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set

from .ssa import SSAFunction, SSAInstruction, SSAValue

logger = logging.getLogger(__name__)


class UseDefChain:
    """
    Track definitions and uses of SSA values for data flow analysis.

    This class builds efficient lookup structures on top of the existing
    SSA graph (SSAValue.uses, SSAValue.producer_inst) to support data flow
    optimization rules.

    Attributes:
        uses: Map from SSA value to list of instructions that use it
        defs: Map from SSA value to instruction that defines it
        inst_uses: Map from instruction to list of values it uses
        inst_defs: Map from instruction to list of values it defines
    """

    def __init__(self, ssa_func: SSAFunction, debug: bool = False):
        """
        Build use-def chains for all values in the SSA function.

        Args:
            ssa_func: SSA function to analyze
            debug: Enable debug logging
        """
        self.ssa_func = ssa_func
        self.debug = debug

        # Value → Instructions that use it
        self.uses: Dict[str, List[SSAInstruction]] = {}

        # Value → Instruction that defines it
        self.defs: Dict[str, SSAInstruction] = {}

        # Instruction → Values it uses (inputs)
        self.inst_uses: Dict[int, List[SSAValue]] = {}  # keyed by instruction address

        # Instruction → Values it defines (outputs)
        self.inst_defs: Dict[int, List[SSAValue]] = {}  # keyed by instruction address

        # Build the chains
        self._build_chains()

        if debug:
            self._log_stats()

    def _build_chains(self):
        """Build use-def chains from SSA function."""
        # Process all blocks
        for block_id in sorted(self.ssa_func.instructions.keys()):
            block_insts = self.ssa_func.instructions[block_id]

            for inst in block_insts:
                # Track instruction → values it uses
                self.inst_uses[inst.address] = inst.inputs

                # Track instruction → values it defines
                self.inst_defs[inst.address] = inst.outputs

                # Track value → instruction that defines it
                for output_val in inst.outputs:
                    self.defs[output_val.name] = inst

                # Track value → instructions that use it
                for input_val in inst.inputs:
                    if input_val.name not in self.uses:
                        self.uses[input_val.name] = []
                    self.uses[input_val.name].append(inst)

    def get_uses(self, value: SSAValue) -> List[SSAInstruction]:
        """
        Get all instructions that use this value.

        Args:
            value: SSA value to query

        Returns:
            List of instructions that use the value (may be empty)
        """
        return self.uses.get(value.name, [])

    def get_def(self, value: SSAValue) -> Optional[SSAInstruction]:
        """
        Get instruction that defines this value.

        Args:
            value: SSA value to query

        Returns:
            Instruction that produces the value, or None if no definition
            (e.g., function parameters, external inputs)
        """
        return self.defs.get(value.name)

    def use_count(self, value: SSAValue) -> int:
        """
        Count number of uses of this value.

        Args:
            value: SSA value to query

        Returns:
            Number of instructions that use the value
        """
        return len(self.get_uses(value))

    def is_single_use(self, value: SSAValue) -> bool:
        """
        Check if value is used exactly once.

        This is critical for inlining and substitution rules.

        Args:
            value: SSA value to query

        Returns:
            True if value is used exactly once, False otherwise
        """
        return self.use_count(value) == 1

    def is_unused(self, value: SSAValue) -> bool:
        """
        Check if value has no uses.

        Dead values can be eliminated to simplify output.

        Args:
            value: SSA value to query

        Returns:
            True if value is never used, False otherwise
        """
        return self.use_count(value) == 0

    def get_single_use(self, value: SSAValue) -> Optional[SSAInstruction]:
        """
        Get the single use of a value (if it exists).

        Args:
            value: SSA value to query

        Returns:
            The single instruction that uses the value, or None if zero or multiple uses
        """
        uses = self.get_uses(value)
        if len(uses) == 1:
            return uses[0]
        return None

    def get_instruction_uses(self, inst: SSAInstruction) -> List[SSAValue]:
        """
        Get all values used by an instruction.

        Args:
            inst: Instruction to query

        Returns:
            List of SSA values used as inputs (may be empty)
        """
        return self.inst_uses.get(inst.address, [])

    def get_instruction_defs(self, inst: SSAInstruction) -> List[SSAValue]:
        """
        Get all values defined by an instruction.

        Args:
            inst: Instruction to query

        Returns:
            List of SSA values produced as outputs (may be empty)
        """
        return self.inst_defs.get(inst.address, [])

    def is_copy_instruction(self, inst: SSAInstruction) -> bool:
        """
        Check if instruction is a simple copy (identity operation).

        A copy instruction has:
        - Exactly one input
        - Exactly one output
        - Mnemonic is COPY or ASSIGN or similar identity operation

        Args:
            inst: Instruction to check

        Returns:
            True if instruction is a copy, False otherwise
        """
        # Check structural requirements
        if len(inst.inputs) != 1 or len(inst.outputs) != 1:
            return False

        # Check mnemonic (COPY is an identity operation)
        # Note: Some decompilers use ASSIGN, MOV, or other mnemonics
        COPY_MNEMONICS = {"COPY", "ASSIGN", "MOV", "MOVE"}
        return inst.mnemonic in COPY_MNEMONICS

    def find_constant_def(self, value: SSAValue) -> Optional[int]:
        """
        Find the constant value if this value is defined as a constant.

        Args:
            value: SSA value to query

        Returns:
            Constant integer value, or None if not a constant
        """
        # Check if value has constant metadata
        if "constant_value" in value.metadata:
            return value.metadata["constant_value"]

        # Check if defined by CONST instruction
        def_inst = self.get_def(value)
        if def_inst and def_inst.mnemonic == "CONST":
            # Try to extract constant from instruction metadata
            if "value" in def_inst.metadata:
                return def_inst.metadata["value"]

        # Check if value name encodes constant (e.g., "const_42")
        if value.name.startswith("const_"):
            try:
                return int(value.name.split("_")[1])
            except (ValueError, IndexError):
                pass

        # Check if literal value (e.g., "lit_0x1234")
        if value.name.startswith("lit_"):
            try:
                lit_part = value.name.split("_", 1)[1]
                if lit_part.startswith("0x"):
                    return int(lit_part, 16)
                return int(lit_part)
            except (ValueError, IndexError):
                pass

        return None

    def get_transitive_uses(self, value: SSAValue, visited: Optional[Set[str]] = None) -> Set[SSAInstruction]:
        """
        Get all instructions that transitively use this value.

        This includes:
        1. Direct uses
        2. Uses of values defined by direct uses (transitive closure)

        Args:
            value: SSA value to query
            visited: Set of already visited value names (for cycle detection)

        Returns:
            Set of all instructions that transitively depend on this value
        """
        if visited is None:
            visited = set()

        if value.name in visited:
            return set()

        visited.add(value.name)
        result: Set[SSAInstruction] = set()

        # Add direct uses
        direct_uses = self.get_uses(value)
        result.update(direct_uses)

        # Add transitive uses through each direct use
        for use_inst in direct_uses:
            # For each output of the using instruction
            for output_val in use_inst.outputs:
                # Add all transitive uses of that output
                result.update(self.get_transitive_uses(output_val, visited))

        return result

    def _log_stats(self):
        """Log statistics about use-def chains."""
        total_values = len(self.ssa_func.values)
        total_defs = len(self.defs)
        total_use_sites = sum(len(uses) for uses in self.uses.values())

        single_use_count = sum(1 for uses in self.uses.values() if len(uses) == 1)
        unused_count = sum(1 for uses in self.uses.values() if len(uses) == 0)

        logger.debug("\n" + "=" * 60)
        logger.debug("Use-Def Chain Statistics")
        logger.debug("=" * 60)
        logger.debug(f"Total SSA values:     {total_values}")
        logger.debug(f"Values with defs:     {total_defs}")
        logger.debug(f"Total use sites:      {total_use_sites}")
        logger.debug(f"Single-use values:    {single_use_count} ({100*single_use_count/max(1,total_values):.1f}%)")
        logger.debug(f"Unused values:        {unused_count} ({100*unused_count/max(1,total_values):.1f}%)")
        logger.debug("=" * 60 + "\n")


def build_use_def_chains(ssa_func: SSAFunction, debug: bool = False) -> UseDefChain:
    """
    Convenience function to build use-def chains.

    Args:
        ssa_func: SSA function to analyze
        debug: Enable debug logging

    Returns:
        UseDefChain object with analysis results
    """
    return UseDefChain(ssa_func, debug=debug)
