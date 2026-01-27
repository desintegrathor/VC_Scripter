"""
Default case detection for switch statements.

Implements Ghidra-inspired algorithm for detecting default cases in switch
statements. The default case is the block executed when the switch variable
doesn't match any explicit case value.

Based on Ghidra's jumptable.cc:
- Guard branch detection (lines 1408-1426)
- Default block identification (lines 2569-2586)
- JumpValuesRangeDefault (lines 325-382)

Algorithm:
1. Find blocks that are direct successors of switch header
2. Identify blocks NOT in explicit case map (candidates)
3. Apply heuristics to select the most likely default
4. Verify default doesn't dominate other cases (would be header)
"""

from __future__ import annotations

from typing import Dict, Set, Optional, List, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from ...cfg import CFG
    from .models import SwitchPattern

logger = logging.getLogger(__name__)


def detect_default_case(
    pattern: 'SwitchPattern',
    cfg: 'CFG',
    func_block_ids: Set[int]
) -> Optional[int]:
    """
    Detect the default case block for a switch statement.

    This implements Ghidra's approach to finding the default block:
    - Look for direct successors of header NOT in explicit cases
    - Apply heuristics to distinguish default from exit block
    - Verify default is actually reachable

    Args:
        pattern: Detected switch pattern
        cfg: Control flow graph
        func_block_ids: Set of all block IDs in function

    Returns:
        Block ID of default case, or None if no default detected
    """
    header_block = cfg.blocks.get(pattern.header_block)
    if not header_block:
        return None

    # Collect all explicit case blocks
    case_blocks = {case.block_id for case in pattern.cases}

    # Find direct successors of header that are NOT explicit cases
    # These are candidates for default or exit
    candidates = set()
    for succ_id in header_block.successors:
        if succ_id not in case_blocks and succ_id in func_block_ids:
            candidates.add(succ_id)

    if not candidates:
        logger.debug(f"No default candidate found for switch at {pattern.header_block}")
        return None

    # If we have an exit block, prefer candidates that are NOT the exit
    # The default case has a body; the exit is just where cases merge
    if pattern.exit_block is not None:
        non_exit_candidates = candidates - {pattern.exit_block}
        if non_exit_candidates:
            candidates = non_exit_candidates

    # Apply heuristics to select most likely default
    best_candidate = None
    best_score = -1

    for candidate_id in candidates:
        score = _score_default_candidate(
            candidate_id,
            pattern,
            cfg,
            case_blocks,
            func_block_ids
        )

        if score > best_score:
            best_score = score
            best_candidate = candidate_id

    # Only accept if score is positive (meets minimum criteria)
    if best_score > 0:
        logger.info(f"Detected default case at block {best_candidate} for switch at {pattern.header_block} (score={best_score})")
        return best_candidate

    return None


def _score_default_candidate(
    candidate_id: int,
    pattern: 'SwitchPattern',
    cfg: 'CFG',
    case_blocks: Set[int],
    func_block_ids: Set[int]
) -> float:
    """
    Score a default case candidate using heuristics.

    Higher score = more likely to be default case

    Heuristics (from Ghidra's approach):
    1. Has non-empty body (+2)
    2. Not dominated by cases (+3)
    3. Flows to exit block (+1)
    4. Has similar structure to other cases (+1)
    5. Not the most common successor of cases (-2, likely exit)

    Args:
        candidate_id: Block ID to score
        pattern: Switch pattern
        cfg: Control flow graph
        case_blocks: Set of explicit case block IDs
        func_block_ids: All block IDs in function

    Returns:
        Score (higher = more likely default)
    """
    score = 0.0
    candidate = cfg.blocks.get(candidate_id)

    if not candidate:
        return -100.0

    # Heuristic 1: Has instructions (non-empty body)
    if candidate.instructions:
        score += 2.0

    # Heuristic 2: Not dominated by other cases
    # (If it's dominated by a case, it's probably part of that case's body)
    is_dominated_by_case = False
    for case_id in case_blocks:
        if _dominates(case_id, candidate_id, cfg):
            is_dominated_by_case = True
            break

    if not is_dominated_by_case:
        score += 3.0
    else:
        # Dominated by case = probably part of case body, not default
        score -= 5.0

    # Heuristic 3: Flows to exit block
    if pattern.exit_block is not None:
        if pattern.exit_block in candidate.successors:
            score += 1.0

    # Heuristic 4: Has similar structure to other cases
    # (Similar number of successors, similar branching pattern)
    if case_blocks:
        avg_case_successors = sum(
            len(cfg.blocks[cid].successors)
            for cid in case_blocks
            if cid in cfg.blocks
        ) / len(case_blocks)

        candidate_successors = len(candidate.successors)
        similarity = 1.0 - abs(candidate_successors - avg_case_successors) / (avg_case_successors + 1)
        score += similarity

    # Heuristic 5: NOT the most common successor of cases
    # (The exit block is usually the most common successor)
    successor_counts: Dict[int, int] = {}
    for case_id in case_blocks:
        case_block = cfg.blocks.get(case_id)
        if case_block:
            for succ in case_block.successors:
                successor_counts[succ] = successor_counts.get(succ, 0) + 1

    if successor_counts:
        max_count = max(successor_counts.values())
        candidate_count = successor_counts.get(candidate_id, 0)

        # If this is the most common successor, it's probably the exit
        if candidate_count == max_count and max_count >= len(case_blocks) // 2:
            score -= 2.0

    return score


def _dominates(dominator_id: int, target_id: int, cfg: 'CFG') -> bool:
    """
    Check if dominator_id dominates target_id in the CFG.

    A block A dominates block B if every path from entry to B goes through A.

    This is a simplified check using reachability:
    - If we can reach target from entry WITHOUT going through dominator,
      then dominator does NOT dominate target

    Args:
        dominator_id: Potential dominator block
        target_id: Target block to check
        cfg: Control flow graph

    Returns:
        True if dominator dominates target
    """
    if dominator_id == target_id:
        return True

    # Simple BFS from entry to target, avoiding dominator
    from collections import deque

    # Find entry block (block with no predecessors)
    entry_id = None
    for block_id, block in cfg.blocks.items():
        if not block.predecessors:
            entry_id = block_id
            break

    if entry_id is None:
        # No clear entry, use heuristic
        return False

    visited = set()
    queue = deque([entry_id])

    while queue:
        current_id = queue.popleft()

        if current_id in visited:
            continue

        visited.add(current_id)

        # Skip the dominator block in our search
        if current_id == dominator_id:
            continue

        # If we reached target without going through dominator,
        # then dominator does NOT dominate target
        if current_id == target_id:
            return False

        # Continue BFS
        current = cfg.blocks.get(current_id)
        if current:
            for succ_id in current.successors:
                if succ_id not in visited:
                    queue.append(succ_id)

    # Could not reach target without going through dominator
    # Therefore, dominator DOES dominate target
    return True


def find_default_body_blocks(
    default_block: int,
    pattern: 'SwitchPattern',
    cfg: 'CFG',
    func_block_ids: Set[int]
) -> Set[int]:
    """
    Find all blocks in the default case body.

    Similar to _find_case_body_blocks in jump_table.py, this traces
    from the default entry block to find all blocks that belong to
    the default case.

    Args:
        default_block: Default case entry block
        pattern: Switch pattern
        cfg: Control flow graph
        func_block_ids: All block IDs in function

    Returns:
        Set of block IDs in default body
    """
    from collections import deque

    # Blocks we should stop at (don't include in default body)
    stop_blocks = {pattern.header_block}  # Don't go back to switch header

    # Add all explicit case blocks as stop blocks
    for case in pattern.cases:
        stop_blocks.add(case.block_id)

    # Add exit block if present
    if pattern.exit_block is not None:
        stop_blocks.add(pattern.exit_block)

    # BFS from default_block
    visited = set()
    queue = deque([default_block])
    body_blocks = set()

    while queue:
        current_id = queue.popleft()

        if current_id in visited:
            continue

        if current_id not in func_block_ids:
            continue

        if current_id in stop_blocks:
            continue

        visited.add(current_id)
        body_blocks.add(current_id)

        # Follow successors
        current = cfg.blocks.get(current_id)
        if current:
            for succ_id in current.successors:
                if succ_id not in visited:
                    queue.append(succ_id)

    return body_blocks


def detect_guard_branch(
    pattern: 'SwitchPattern',
    cfg: 'CFG',
    func_block_ids: Set[int]
) -> Optional[int]:
    """
    Detect guard branch that checks range before switch.

    A guard branch pattern (from Ghidra jumptable.cc:1408):
    - Conditional branch before switch header
    - Tests if switch variable is in valid range
    - If out of range, branches to default
    - If in range, continues to switch

    Pattern:
        [guard] --out_of_range--> [default]
           |
           v (in_range)
        [switch_header]

    Args:
        pattern: Switch pattern
        cfg: Control flow graph
        func_block_ids: All block IDs in function

    Returns:
        Guard block ID if detected, None otherwise
    """
    header_block = cfg.blocks.get(pattern.header_block)
    if not header_block:
        return None

    # Look at predecessors of header
    for pred_id in header_block.predecessors:
        pred_block = cfg.blocks.get(pred_id)
        if not pred_block:
            continue

        # Guard should be conditional branch with 2 successors
        if len(pred_block.successors) != 2:
            continue

        # One successor should be header
        if pattern.header_block not in pred_block.successors:
            continue

        # Other successor is potential default target
        other_succ = None
        for succ_id in pred_block.successors:
            if succ_id != pattern.header_block:
                other_succ = succ_id
                break

        if other_succ is None:
            continue

        # Check if this looks like a range check
        # (Has comparison instruction with constant)
        if _has_range_check(pred_block):
            logger.info(f"Detected guard branch at block {pred_id} for switch at {pattern.header_block}")
            return pred_id

    return None


def _has_range_check(block) -> bool:
    """
    Check if block contains a range check instruction.

    Range checks typically compare a variable to a constant:
    - x < MAX
    - x <= MAX
    - x > MIN
    - x >= MIN

    Args:
        block: Basic block to check

    Returns:
        True if block has range check
    """
    if not block or not block.instructions:
        return False

    # Look for comparison instructions
    comparison_opcodes = ["LES", "ULES", "GRE", "UGRE", "ILES", "IGRE", "ISLE", "USLE", "IGRE", "UGRE"]

    for instr in block.instructions:
        if hasattr(instr, 'opcode') and instr.opcode in comparison_opcodes:
            return True

        # Also check mnemonic for SSA instructions
        if hasattr(instr, 'mnemonic') and instr.mnemonic in comparison_opcodes:
            return True

    return False
