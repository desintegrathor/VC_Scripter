"""
Control flow graph analysis utilities.

This module contains functions for analyzing control flow patterns in the CFG,
including finding basic block relationships, successors, loop membership, and
short-circuit evaluation patterns.
"""

from __future__ import annotations

from typing import List, Optional, Set, Tuple, TYPE_CHECKING

from ...cfg import CFG, NaturalLoop, BasicBlock, dominates
from ....disasm import opcodes

if TYPE_CHECKING:
    from ..patterns.models import CompoundCondition


def _get_loop_for_block(block_id: int, loops: List[NaturalLoop]) -> Optional[NaturalLoop]:
    """Find the innermost loop containing this block."""
    containing_loops = [l for l in loops if block_id in l.body]
    if not containing_loops:
        return None
    # Prefer loops whose bodies are strict subsets of others (nested loops)
    innermost_candidates = []
    for loop in containing_loops:
        is_inner = True
        for other in containing_loops:
            if loop is other:
                continue
            if other.body.issubset(loop.body) and other.body != loop.body:
                is_inner = False
                break
        if is_inner:
            innermost_candidates.append(loop)
    if innermost_candidates:
        containing_loops = innermost_candidates
    # Return the smallest (innermost) loop by body size
    return min(containing_loops, key=lambda l: len(l.body))


def _is_back_edge_target(cfg: CFG, source: int, target: int, loops: List[NaturalLoop]) -> bool:
    """Check if edge source→target is a back edge (target is loop header containing source)."""
    for loop in loops:
        if loop.header == target and source in loop.body:
            return True
    return False


def _find_if_body_blocks(
    cfg: CFG,
    entry: int,
    stop_blocks: Set[int],
    resolver: opcodes.OpcodeResolver,
    context_stop_blocks: Optional[Set[int]] = None
) -> Set[int]:
    """
    Find all blocks belonging to an if branch using BFS.
    Similar to _find_case_body_blocks but for if/else branches.

    Args:
        cfg: Control flow graph
        entry: Entry block of the if branch
        stop_blocks: Blocks where we should stop (merge point, other branches)
        resolver: Opcode resolver
        context_stop_blocks: Optional additional stop blocks from enclosing structures
                             (e.g., case blocks when detecting if/else inside a switch case)
    """
    body_blocks: Set[int] = set()
    worklist = [entry]
    visited: Set[int] = set()

    # PHASE 3.1: Combine stop_blocks with context_stop_blocks
    effective_stop = set(stop_blocks)
    if context_stop_blocks:
        effective_stop.update(context_stop_blocks)

    def _is_dominated(candidate: int) -> bool:
        if not cfg.idom:
            return True
        return dominates(cfg, entry, candidate)

    while worklist:
        block_id = worklist.pop(0)

        if block_id in visited:
            continue

        # Stop at barriers (merge point, other branches, context boundaries)
        if block_id in effective_stop and block_id != entry:
            continue

        # Dominance is a hard signal for structured bodies
        if block_id != entry and not _is_dominated(block_id):
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


def _find_case_body_blocks(
    cfg: CFG,
    case_entry: int,
    stop_blocks: Set[int],
    resolver: opcodes.OpcodeResolver,
    known_exit_blocks: Optional[Set[int]] = None,
    convergence_threshold: int = 2
) -> Set[int]:
    """
    Find all blocks belonging to a case body using BFS with improved stopping.

    This function performs breadth-first traversal from the case entry block,
    stopping at various boundaries to prevent code leakage between cases.

    IMPROVED (Ghidra-style): Convergence detection now distinguishes between:
    - If/else merges WITHIN a case (should NOT stop - all preds from same case)
    - Switch exit convergence (SHOULD stop - preds from different cases or stop_blocks)

    Args:
        cfg: Control flow graph
        case_entry: Entry block of the case
        stop_blocks: Blocks where we should stop (other case entries, exit, default)
        resolver: Opcode resolver
        known_exit_blocks: Optional set of known exit points to stop at
        convergence_threshold: Stop at blocks with >= this many predecessors from
                               different sources (convergence points)

    Returns:
        Set of all block IDs in the case body
    """
    body_blocks: Set[int] = set()
    worklist = [case_entry]
    visited: Set[int] = set()

    # Combine stop_blocks with known_exit_blocks
    effective_stop = set(stop_blocks)
    if known_exit_blocks:
        effective_stop.update(known_exit_blocks)

    _debug_body = False  # Set to True to debug specific case

    def _is_dominated(candidate: int) -> bool:
        if not cfg.idom:
            return True
        return dominates(cfg, case_entry, candidate)

    while worklist:
        block_id = worklist.pop(0)

        if _debug_body:
            import sys
            print(f"DEBUG BODY: Processing block_id={block_id}, worklist={worklist}, visited={visited}", file=sys.stderr)

        # Skip if already visited
        if block_id in visited:
            if _debug_body:
                print(f"DEBUG BODY: Skipping {block_id} - already visited", file=sys.stderr)
            continue

        # Stop at barriers (other cases, exit, etc.)
        if block_id in effective_stop and block_id != case_entry:
            if _debug_body:
                print(f"DEBUG BODY: Stopping at {block_id} - in effective_stop {effective_stop}", file=sys.stderr)
            continue

        # Dominance check: require that the block is dominated by the case entry,
        # OR that all of its predecessors are already in the case body.
        # The second condition handles blocks that are reachable from the case entry
        # but not dominated by it in the global dominator tree (e.g., continuation
        # blocks after nested if/else within a case that the dominator tree resolves
        # to a dispatch chain block instead).
        if block_id != case_entry and not _is_dominated(block_id):
            predecessors = getattr(cfg.blocks.get(block_id), 'predecessors', [])
            all_preds_in_body = predecessors and all(
                p in body_blocks or p in visited or p == case_entry
                for p in predecessors
            )
            if not all_preds_in_body:
                if _debug_body:
                    import sys
                    print(f"DEBUG BODY: Skipping {block_id} - not dominated by case entry and has external preds", file=sys.stderr)
                continue

        block = cfg.blocks.get(block_id)
        if not block:
            if _debug_body:
                print(f"DEBUG BODY: Block {block_id} not found in CFG", file=sys.stderr)
            continue

        # IMPROVED CONVERGENCE DETECTION (Ghidra-style):
        # Only stop at true switch convergence points, NOT at if/else merges within a case.
        #
        # Key insight: If/else merges within a case have ALL predecessors from the same
        # case body (blocks we've already visited). Switch exit convergence has predecessors
        # from DIFFERENT cases (stop_blocks) or external blocks.
        #
        # Algorithm:
        # 1. Count predecessors that are in body_blocks (same case)
        # 2. Count predecessors that are in stop_blocks (different cases)
        # 3. Count other predecessors (external blocks)
        # 4. Only stop if we have predecessors from DIFFERENT cases (stop_blocks)
        #    or multiple external predecessors
        if block_id != case_entry:
            predecessors = getattr(block, 'predecessors', [])
            if predecessors and len(predecessors) >= convergence_threshold:
                preds_in_body = sum(1 for p in predecessors if p in body_blocks or p in visited)
                # FIX: Don't count case_entry as "from other cases" - it's OUR case's entry!
                # Also don't count predecessors that are already in body_blocks/visited
                preds_from_other_cases = sum(
                    1 for p in predecessors
                    if p in effective_stop
                    and p != case_entry  # Our case's entry
                    and p not in body_blocks  # Already part of our case
                    and p not in visited  # Already part of our case
                )
                preds_external = len(predecessors) - preds_in_body - preds_from_other_cases

                if _debug_body:
                    import sys
                    print(f"DEBUG BODY: Convergence check for {block_id}: preds={predecessors}, in_body={preds_in_body}, from_other_cases={preds_from_other_cases}, external={preds_external}", file=sys.stderr)

                # CRITICAL FIX: Only stop if there are predecessors from other cases/stop_blocks
                # OR if there are multiple external predecessors (not from our case)
                # This allows if/else merges within a case to pass through
                if preds_from_other_cases > 0:
                    # This block has predecessors from other switch cases - it's the switch exit
                    if _debug_body:
                        print(f"DEBUG BODY: Stopping at {block_id} - has preds from other cases", file=sys.stderr)
                    continue

                if preds_external >= convergence_threshold and preds_in_body == 0:
                    # All predecessors are external (not from our case body) - likely switch exit
                    if _debug_body:
                        print(f"DEBUG BODY: Stopping at {block_id} - external preds >= threshold", file=sys.stderr)
                    continue

                # If all predecessors are from body_blocks/visited, this is an if/else merge
                # within our case - DON'T stop, include this block in the case body

        visited.add(block_id)
        body_blocks.add(block_id)

        if _debug_body:
            import sys
            print(f"DEBUG BODY: Added {block_id} to body_blocks, successors={block.successors}", file=sys.stderr)

        # Check if block ends with return - don't follow after return
        if block.instructions:
            last_instr = block.instructions[-1]
            if resolver.is_return(last_instr.opcode):
                continue

            # Check for "break blocks"
            # A break block is a single-instruction JMP to the exit block.
            # We include it in the body but don't follow its successors.
            mnem = resolver.get_mnemonic(last_instr.opcode)
            if mnem == "JMP" and len(block.instructions) == 1:
                # This is a potential break block - find where it jumps
                target_addr = last_instr.arg1
                target_block = None
                for bid, b in cfg.blocks.items():
                    if b.start == target_addr:
                        target_block = bid
                        break

                # If the target is a stop block (exit), this is a break
                # Include the break block but don't traverse further
                if target_block in effective_stop:
                    continue

        # Add successors to worklist
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
