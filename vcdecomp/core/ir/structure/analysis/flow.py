"""
Control flow graph analysis utilities.

This module contains functions for analyzing control flow patterns in the CFG,
including finding basic block relationships, successors, loop membership, and
short-circuit evaluation patterns.
"""

from __future__ import annotations

from typing import List, Optional, Set

from ...cfg import CFG, NaturalLoop, BasicBlock
from ....disasm import opcodes


def _get_loop_for_block(block_id: int, loops: List[NaturalLoop]) -> Optional[NaturalLoop]:
    """Find the innermost loop containing this block."""
    containing_loops = [l for l in loops if block_id in l.body]
    if not containing_loops:
        return None
    # Return the smallest (innermost) loop
    return min(containing_loops, key=lambda l: len(l.body))


def _is_back_edge_target(cfg: CFG, source: int, target: int, loops: List[NaturalLoop]) -> bool:
    """Check if edge source→target is a back edge (target is loop header containing source)."""
    for loop in loops:
        if loop.header == target and source in loop.body:
            return True
    return False


def _find_if_body_blocks(cfg: CFG, entry: int, stop_blocks: Set[int], resolver: opcodes.OpcodeResolver) -> Set[int]:
    """
    Find all blocks belonging to an if branch using BFS.
    Similar to _find_case_body_blocks but for if/else branches.
    """
    body_blocks: Set[int] = set()
    worklist = [entry]
    visited: Set[int] = set()

    while worklist:
        block_id = worklist.pop(0)

        if block_id in visited:
            continue

        # Stop at barriers (merge point, other branches, etc.)
        if block_id in stop_blocks and block_id != entry:
            continue

        visited.add(block_id)
        body_blocks.add(block_id)

        # Get block
        block = cfg.blocks.get(block_id)
        if block and block.instructions:
            last_instr = block.instructions[-1]
            if resolver.is_return(last_instr.opcode):
                continue  # Don't follow after return

        # Add successors to worklist
        if block:
            for succ in block.successors:
                if succ not in visited:
                    worklist.append(succ)

    return body_blocks


def _find_common_successor(cfg: CFG, block_a: int, block_b: int) -> Optional[int]:
    """
    Find the immediate common successor (merge point) of two blocks.
    Returns the first block that is reachable from both branches.
    """
    # Get all successors of both blocks (BFS)
    def get_all_successors(start: int, max_depth: int = 20) -> Set[int]:
        visited = set()
        worklist = [(start, 0)]
        while worklist:
            block_id, depth = worklist.pop(0)
            if depth > max_depth or block_id in visited:
                continue
            visited.add(block_id)
            block = cfg.blocks.get(block_id)
            if block:
                for succ in block.successors:
                    worklist.append((succ, depth + 1))
        return visited

    succs_a = get_all_successors(block_a)
    succs_b = get_all_successors(block_b)

    # Find common successors
    common = succs_a & succs_b
    if not common:
        return None

    # Return the one with smallest address (closest merge point)
    candidates = [(bid, cfg.blocks[bid].start) for bid in common if bid in cfg.blocks]
    if not candidates:
        return None

    return min(candidates, key=lambda x: x[1])[0]


def _is_jmp_after_jz(
    block: BasicBlock,
    resolver: opcodes.OpcodeResolver
) -> Optional[int]:
    """
    Check if block ends with pattern: JZ target1; JMP target2

    This pattern indicates short-circuit evaluation:
    - If condition is FALSE, jump to target1 (next condition in OR, or exit)
    - If condition is TRUE, jump to target2 (true body)

    Returns:
        target2 (the JMP destination) if pattern matches, None otherwise
    """
    if not block or not block.instructions or len(block.instructions) < 2:
        return None

    last = block.instructions[-1]
    second_last = block.instructions[-2]

    # Check for: conditional jump followed by unconditional jump
    if (resolver.is_conditional_jump(second_last.opcode) and
        resolver.get_mnemonic(last.opcode) == "JMP"):
        return last.arg1  # The TRUE target

    return None


def _find_all_jz_targets(
    cfg: CFG,
    block_id: int,
    resolver: opcodes.OpcodeResolver
) -> Set[int]:
    """
    Find all JZ/JNZ targets within a block (for AND detection).

    In short-circuit AND evaluation, multiple conditions in sequence all
    jump to the same FALSE exit point:
        if (!cond1) goto exit;
        if (!cond2) goto exit;
        if (!cond3) goto exit;
        goto body;
    This is: if (cond1 && cond2 && cond3) body;

    Returns:
        Set of target addresses for all conditional jumps in the block
    """
    block = cfg.blocks.get(block_id)
    if not block:
        return set()

    targets = set()
    for instr in block.instructions:
        if resolver.is_conditional_jump(instr.opcode):
            targets.add(instr.arg1)

    return targets


def _find_common_true_target(
    cfg: CFG,
    blocks: List[int],
    resolver: opcodes.OpcodeResolver
) -> Optional[int]:
    """
    Find if multiple blocks all JMP to the same TRUE target (OR detection).

    In short-circuit OR evaluation, multiple condition groups all jump to
    the same TRUE body:
        if (cond1) goto body;
        if (cond2) goto body;
        if (cond3) goto body;
        goto exit;
    This is: if (cond1 || cond2 || cond3) body;

    Returns:
        The common target address if found, None otherwise
    """
    true_targets = []

    for block_id in blocks:
        block = cfg.blocks.get(block_id)
        if not block:
            continue

        jmp_target = _is_jmp_after_jz(block, resolver)
        if jmp_target is not None:
            true_targets.append(jmp_target)

    # Check if all jump to same target
    if len(true_targets) >= 2 and len(set(true_targets)) == 1:
        return true_targets[0]  # All jump to same target = OR pattern

    return None


def _find_case_body_blocks(cfg: CFG, case_entry: int, stop_blocks: Set[int], resolver: opcodes.OpcodeResolver) -> Set[int]:
    """
    Find all blocks belonging to a case body using BFS.

    Args:
        cfg: Control flow graph
        case_entry: Entry block of the case
        stop_blocks: Blocks where we should stop (other case entries, exit, default)
        resolver: Opcode resolver

    Returns:
        Set of all block IDs in the case body
    """
    body_blocks: Set[int] = set()
    worklist = [case_entry]
    visited: Set[int] = set()

    while worklist:
        block_id = worklist.pop(0)

        # Skip if already visited
        if block_id in visited:
            continue

        # Stop at barriers (other cases, exit, etc.)
        if block_id in stop_blocks and block_id != case_entry:
            continue

        visited.add(block_id)
        body_blocks.add(block_id)

        # Get block and check if it ends with return
        block = cfg.blocks.get(block_id)
        if block and block.instructions:
            last_instr = block.instructions[-1]
            if resolver.is_return(last_instr.opcode):
                continue  # Don't follow after return

        # Add successors to worklist
        if block:
            for succ in block.successors:
                if succ not in visited:
                    worklist.append(succ)

    return body_blocks
