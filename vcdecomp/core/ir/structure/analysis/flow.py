"""
Control flow graph analysis utilities.

This module contains functions for analyzing control flow patterns in the CFG,
including finding basic block relationships, successors, loop membership, and
short-circuit evaluation patterns.
"""

from __future__ import annotations

from typing import List, Optional, Set, Tuple, TYPE_CHECKING

from ...cfg import CFG, NaturalLoop, BasicBlock
from ....disasm import opcodes

if TYPE_CHECKING:
    from ..patterns.models import CompoundCondition


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


def _find_compound_merge_point(
    cfg: CFG,
    compound: "CompoundCondition",
    true_body: Set[int],
    false_body: Set[int]
) -> Optional[int]:
    """
    Find merge point for compound condition using proper CFG analysis.

    For compound conditions like ((A && B) || (C && D)), the merge point is where
    the TRUE and FALSE branches rejoin after executing their respective bodies.

    Algorithm:
    1. Find all exit blocks from true_body (blocks with successors outside body)
    2. Find all exit blocks from false_body (blocks with successors outside body)
    3. Find smallest common successor of all exits (first block reachable from all)
    4. Exclude blocks that are part of compound pattern itself

    Args:
        cfg: Control flow graph
        compound: Compound condition with involved_blocks
        true_body: Set of blocks in TRUE branch body
        false_body: Set of blocks in FALSE branch body

    Returns:
        Block ID of merge point, or None if no clear merge point
    """
    def get_exit_blocks(body: Set[int]) -> Set[int]:
        """Find blocks in body that have successors outside body."""
        exits = set()
        for block_id in body:
            block = cfg.blocks.get(block_id)
            if block:
                for succ in block.successors:
                    if succ not in body:
                        exits.add(block_id)
                        break
        return exits

    # Find exit blocks from both bodies
    true_exits = get_exit_blocks(true_body) if true_body else set()
    false_exits = get_exit_blocks(false_body) if false_body else set()

    # If no exits, no merge point
    if not true_exits and not false_exits:
        return None

    # Collect all successors of exit blocks (potential merge points)
    potential_merge = set()
    for exit_block in true_exits | false_exits:
        block = cfg.blocks.get(exit_block)
        if block:
            potential_merge.update(block.successors)

    # Remove blocks that are part of the bodies or compound pattern
    potential_merge -= true_body
    potential_merge -= false_body
    if compound.involved_blocks:
        potential_merge -= compound.involved_blocks

    if not potential_merge:
        return None

    # Find the block with smallest address (closest merge point)
    candidates = [(bid, cfg.blocks[bid].start) for bid in potential_merge if bid in cfg.blocks]
    if not candidates:
        return None

    return min(candidates, key=lambda x: x[1])[0]


def _find_compound_body_blocks(
    cfg: CFG,
    compound: "CompoundCondition",
    resolver: opcodes.OpcodeResolver
) -> Tuple[Set[int], Set[int], Optional[int]]:
    """
    Find body blocks for compound condition.

    This function properly detects the TRUE and FALSE body blocks for compound
    conditions (AND/OR patterns), ensuring that pattern infrastructure blocks
    (blocks that test conditions) are NOT included in the body.

    Key differences from _find_if_body_blocks:
    - Starts from compound.true_target (NOT compound.involved_blocks)
    - Excludes ALL compound.involved_blocks from body using stop_blocks
    - Computes proper merge point for compound patterns
    - Validates that bodies are non-empty

    Algorithm:
    1. Run BFS from true_target with stop_blocks = involved_blocks | {false_target}
    2. Remove any pattern blocks that leaked into body: true_body -= involved_blocks
    3. Run BFS from false_target with stop_blocks = involved_blocks | true_body
    4. Remove pattern blocks from false_body
    5. Find merge point using _find_compound_merge_point

    Args:
        cfg: Control flow graph
        compound: CompoundCondition with targets and involved_blocks
        resolver: Opcode resolver

    Returns:
        Tuple of (true_body, false_body, merge_point)
        - true_body: Set of blocks in TRUE branch
        - false_body: Set of blocks in FALSE branch (may be empty)
        - merge_point: Block where branches rejoin (may be None)
    """
    # Prepare stop blocks for TRUE body: pattern blocks + false target
    stop_blocks_true = compound.involved_blocks.copy() if compound.involved_blocks else set()
    if compound.false_target:
        stop_blocks_true.add(compound.false_target)

    # Find TRUE body using BFS
    true_body = _find_if_body_blocks(cfg, compound.true_target, stop_blocks_true, resolver)

    # CRITICAL: Remove any pattern blocks that leaked into body
    if compound.involved_blocks:
        true_body = true_body - compound.involved_blocks

    # Find FALSE body (if false_target exists)
    false_body = set()
    if compound.false_target:
        # Stop blocks: pattern blocks + true_target + true_body
        stop_blocks_false = compound.involved_blocks.copy() if compound.involved_blocks else set()
        stop_blocks_false.add(compound.true_target)
        stop_blocks_false.update(true_body)

        false_body = _find_if_body_blocks(cfg, compound.false_target, stop_blocks_false, resolver)

        # Remove pattern blocks from false body
        if compound.involved_blocks:
            false_body = false_body - compound.involved_blocks

    # Find merge point
    merge_point = _find_compound_merge_point(cfg, compound, true_body, false_body)

    return (true_body, false_body, merge_point)
