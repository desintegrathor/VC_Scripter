"""
Utility helper functions for structure analysis.

This module contains standalone utility functions that are used across
the structure analysis pipeline but don't fit into specific categories.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from pathlib import Path

from vcdecomp.core.disasm import opcodes
from vcdecomp.parsing.symbol_db import SymbolDatabase


# Configuration: Show block comments for debugging
SHOW_BLOCK_COMMENTS = False  # Set to True to show "// Block X @addr" comments


def _load_symbol_db() -> Optional[SymbolDatabase]:
    """Load symbol database from compiler/symbol_db.json if available."""
    try:
        # Try to find symbol_db.json in compiler directory
        current = Path(__file__).parent
        while current.parent != current:  # Walk up until root
            symbol_db_path = current / "compiler" / "symbol_db.json"
            if symbol_db_path.exists():
                return SymbolDatabase.load(symbol_db_path)
            current = current.parent
        return None
    except Exception:
        return None


def _build_start_map(cfg) -> Dict[int, int]:
    """
    Build a mapping from instruction addresses to block IDs.

    Args:
        cfg: Control Flow Graph

    Returns:
        Dictionary mapping block start addresses to block IDs
    """
    return {block.start: block_id for block_id, block in cfg.blocks.items()}


def _dominates(cfg, a: int, b: int) -> bool:
    """
    Check if block 'a' dominates block 'b' in the CFG.

    A block 'a' dominates block 'b' if all paths from entry to 'b' pass through 'a'.

    Args:
        cfg: Control Flow Graph
        a: Potential dominator block ID
        b: Block ID to check

    Returns:
        True if 'a' dominates 'b', False otherwise
    """
    if a == b:
        return True
    current = b
    idom = cfg.idom
    while current in idom:
        parent = idom[current]
        if parent == a:
            return True
        if parent == current:
            break
        current = parent
    return False


def _is_control_flow_only(ssa_block: List, resolver: opcodes.OpcodeResolver) -> bool:
    """
    Check if block contains only control flow instructions (no visible statements).

    Args:
        ssa_block: List of SSA instructions in the block
        resolver: Opcode resolver for checking instruction types

    Returns:
        True if block has only jumps/returns (empty from user perspective)
    """
    if not ssa_block:
        return True

    for inst in ssa_block:
        # PHI nodes are synthetic SSA instructions, not user code - skip them
        if inst.mnemonic == "PHI":
            continue

        # Get opcode from underlying instruction: SSAInstruction -> LiftedInstruction -> Instruction
        if inst.instruction and inst.instruction.instruction:
            opcode = inst.instruction.instruction.opcode
            # If any instruction is NOT a control flow instruction, block has content
            if not (resolver.is_jump(opcode) or resolver.is_return(opcode)):
                return False

    return True
