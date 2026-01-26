"""
CFG Integration for SSA-level optimizations.

This module links SSA instructions with CFG basic blocks to enable
control flow analysis optimizations:
- Loop optimization rules
- Pattern detection rules (abs, min/max)
- Phi node simplification rules

Provides convenient API for rules to query:
- Which CFG block contains an instruction
- Whether an instruction is in a loop
- Loop header and body information
- Phi nodes at block boundaries
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set

from .cfg import CFG, BasicBlock, NaturalLoop, find_all_loops, is_loop_header
from .ssa import SSAFunction, SSAInstruction, SSAValue

logger = logging.getLogger(__name__)


class CFGIntegration:
    """
    Link SSA instructions with CFG basic blocks for control flow analysis.

    This class provides efficient lookup structures to answer queries like:
    - Which CFG block contains this instruction?
    - Is this instruction in a loop?
    - What are the phi nodes at a block boundary?
    - What loops exist in the function?

    Attributes:
        cfg: The control flow graph
        ssa_func: The SSA function
        loops: All natural loops in the function
        loop_headers: Set of block IDs that are loop headers
        block_to_loop: Map from block ID to the loop it belongs to
    """

    def __init__(self, ssa_func: SSAFunction, debug: bool = False):
        """
        Build CFG integration for SSA function.

        Args:
            ssa_func: SSA function to analyze
            debug: Enable debug logging
        """
        self.ssa_func = ssa_func
        self.cfg = ssa_func.cfg
        self.debug = debug

        # Find all natural loops
        self.loops: List[NaturalLoop] = find_all_loops(self.cfg)

        # Build quick lookup structures
        self.loop_headers: Set[int] = {loop.header for loop in self.loops}

        # Map each block to the loop it belongs to (innermost if nested)
        self.block_to_loop: Dict[int, NaturalLoop] = {}
        for loop in self.loops:
            for block_id in loop.body:
                # If block already mapped, keep innermost loop (later loops are nested)
                if block_id not in self.block_to_loop:
                    self.block_to_loop[block_id] = loop

        if debug:
            self._log_stats()

    def get_block_for_inst(self, inst: SSAInstruction) -> Optional[BasicBlock]:
        """
        Get CFG block containing instruction.

        Args:
            inst: SSA instruction

        Returns:
            BasicBlock containing the instruction, or None if not found
        """
        return self.cfg.blocks.get(inst.block_id)

    def is_in_loop(self, inst: SSAInstruction) -> bool:
        """
        Check if instruction is inside a loop.

        Args:
            inst: SSA instruction

        Returns:
            True if instruction is in a loop, False otherwise
        """
        return inst.block_id in self.block_to_loop

    def get_loop_for_inst(self, inst: SSAInstruction) -> Optional[NaturalLoop]:
        """
        Get the loop containing this instruction.

        Args:
            inst: SSA instruction

        Returns:
            NaturalLoop containing the instruction, or None if not in a loop
        """
        return self.block_to_loop.get(inst.block_id)

    def is_loop_header_block(self, block_id: int) -> bool:
        """
        Check if block is a loop header.

        Args:
            block_id: Block ID to check

        Returns:
            True if block is a loop header, False otherwise
        """
        return block_id in self.loop_headers

    def get_loop_by_header(self, header_block_id: int) -> Optional[NaturalLoop]:
        """
        Get loop by its header block ID.

        Args:
            header_block_id: Loop header block ID

        Returns:
            NaturalLoop with this header, or None if not a loop header
        """
        for loop in self.loops:
            if loop.header == header_block_id:
                return loop
        return None

    def get_phi_nodes(self, block_id: int) -> List[SSAInstruction]:
        """
        Get all phi nodes at the start of a block.

        PHI nodes are pseudo-instructions at block boundaries that merge
        values from different control flow paths.

        Args:
            block_id: Block ID

        Returns:
            List of phi instructions (mnemonic == "PHI") at block start
        """
        if block_id not in self.ssa_func.instructions:
            return []

        block_insts = self.ssa_func.instructions[block_id]
        phi_nodes = []

        for inst in block_insts:
            if inst.mnemonic == "PHI":
                phi_nodes.append(inst)
            else:
                # PHI nodes are always at the start of a block
                break

        return phi_nodes

    def is_loop_invariant(self, value: SSAValue, loop: NaturalLoop) -> bool:
        """
        Check if a value is loop-invariant (defined outside the loop).

        A value is loop-invariant if its defining instruction is outside
        the loop body.

        Args:
            value: SSA value to check
            loop: Loop to check against

        Returns:
            True if value is loop-invariant, False otherwise
        """
        # If value has no producer, it's a constant or parameter (invariant)
        if value.producer_inst is None:
            return True

        # Check if producer is outside loop
        producer_block = value.producer_inst.block_id
        return producer_block not in loop.body

    def get_loop_exit_blocks(self, loop: NaturalLoop) -> Set[int]:
        """
        Get blocks that exit the loop.

        An exit block is a block in the loop that has a successor
        outside the loop.

        Args:
            loop: Loop to analyze

        Returns:
            Set of block IDs that exit the loop
        """
        exit_blocks = set()

        for block_id in loop.body:
            block = self.cfg.blocks[block_id]
            for succ_id in block.successors:
                if succ_id not in loop.body:
                    exit_blocks.add(block_id)
                    break

        return exit_blocks

    def get_all_loops(self) -> List[NaturalLoop]:
        """
        Get all natural loops in the function.

        Returns:
            List of all loops, sorted by header address
        """
        return self.loops

    def get_dominators(self, block_id: int) -> Set[int]:
        """
        Get all blocks that dominate this block.

        A block X dominates Y if all paths from entry to Y must go through X.

        Args:
            block_id: Block to query

        Returns:
            Set of block IDs that dominate this block (including itself)
        """
        dominators = {block_id}
        current = block_id

        # Walk up the dominator tree
        while current in self.cfg.idom and self.cfg.idom[current] != current:
            current = self.cfg.idom[current]
            dominators.add(current)

        return dominators

    def dominates(self, dominator_id: int, block_id: int) -> bool:
        """
        Check if dominator_id dominates block_id.

        Args:
            dominator_id: Potential dominator block
            block_id: Block to check

        Returns:
            True if dominator_id dominates block_id, False otherwise
        """
        return dominator_id in self.get_dominators(block_id)

    def _log_stats(self):
        """Log statistics about CFG integration."""
        logger.debug("\n" + "=" * 60)
        logger.debug("CFG Integration Statistics")
        logger.debug("=" * 60)
        logger.debug(f"Total blocks:     {len(self.cfg.blocks)}")
        logger.debug(f"Entry block:      {self.cfg.entry_block}")
        logger.debug(f"Natural loops:    {len(self.loops)}")
        logger.debug(f"Loop headers:     {len(self.loop_headers)}")

        if self.loops:
            logger.debug("\nLoop details:")
            for i, loop in enumerate(self.loops):
                logger.debug(f"  Loop {i+1}: header={loop.header}, body size={len(loop.body)}")

        logger.debug("=" * 60 + "\n")


def build_cfg_integration(ssa_func: SSAFunction, debug: bool = False) -> CFGIntegration:
    """
    Convenience function to build CFG integration.

    Args:
        ssa_func: SSA function to analyze
        debug: Enable debug logging

    Returns:
        CFGIntegration object with analysis results
    """
    return CFGIntegration(ssa_func, debug=debug)
