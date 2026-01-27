"""
Binary search and jump table pattern detection for switch statements.

This module contains functions for detecting switch/case patterns that use
binary search trees or jump tables instead of linear if-else-if chains.
"""

from __future__ import annotations

from typing import Dict, Set, List, Optional, Tuple
import logging

from ...cfg import CFG
from ....disasm import opcodes
from ...ssa import SSAFunction, SSAInstruction, SSAValue
from ...expr import ExpressionFormatter

from .models import CaseInfo, SwitchPattern
from ..analysis.flow import _find_case_body_blocks

logger = logging.getLogger(__name__)


def _resolve_conditional_targets(
    block: "BasicBlock",
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver
) -> Tuple[Optional[int], Optional[int]]:
    """Resolve conditional jump targets using disassembler addresses."""
    if not block or not block.instructions:
        return (None, None)

    last_instr = block.instructions[-1]
    if not resolver.is_conditional_jump(last_instr.opcode):
        return (None, None)

    jump_target = start_to_block.get(last_instr.arg1)
    fallthrough_addr = last_instr.address + 1
    fallthrough = start_to_block.get(fallthrough_addr)
    if fallthrough is None:
        for succ in block.successors:
            if succ != jump_target:
                fallthrough = succ
                break

    return (jump_target, fallthrough)


def _detect_binary_search_switch(
    cfg: CFG,
    start_block: int,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    func_block_ids: Set[int]
) -> Optional[SwitchPattern]:
    """
    Detect binary search tree switch pattern.

    Binary search switches test a middle value and branch to subtrees:
        if (var == MID) goto case_MID;
        if (var < MID) goto left_subtree;  // tests 0..MID-1
        else goto right_subtree;            // tests MID+1..MAX

    Algorithm:
    1. Build decision tree from start_block recursively
    2. Verify all nodes test SAME variable
    3. Collect leaf nodes (case entry points) and their test values
    4. Build SwitchPattern from decision tree if valid

    Args:
        cfg: Control flow graph
        start_block: Starting block ID
        ssa_func: SSA function
        formatter: Expression formatter
        func_block_ids: Set of all block IDs in current function

    Returns:
        SwitchPattern if binary search detected, None otherwise
    """
    resolver = getattr(ssa_func.scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    ssa_blocks = ssa_func.instructions

    # Try to build decision tree
    start_to_block = {block.start: block_id for block_id, block in cfg.blocks.items()}
    tree_result = _build_decision_tree(
        start_block, cfg, ssa_blocks, resolver, func_block_ids,
        ssa_func, formatter, start_to_block, max_depth=10
    )

    if not tree_result:
        return None

    test_var, case_values, tree_blocks = tree_result

    # Need at least 3 cases to be worth using binary search
    # (2 cases would just be a simple if-else)
    if len(case_values) < 3:
        return None

    # Find common exit block (where cases merge after switch)
    exit_block = _find_switch_exit(case_values, cfg, func_block_ids)

    # Build case information
    cases: List[CaseInfo] = []
    all_blocks = set(tree_blocks)

    for value, block_id in sorted(case_values.items()):
        # Find all blocks in this case body
        # _find_case_body_blocks(cfg, case_entry, stop_blocks, resolver)
        stop_blocks = tree_blocks | ({exit_block} if exit_block else set())
        body_blocks = _find_case_body_blocks(
            cfg, block_id, stop_blocks, resolver
        )
        all_blocks.update(body_blocks)

        # Check if case has break (ends at exit) or falls through
        has_break = _case_has_break_check(block_id, body_blocks, exit_block, cfg, resolver)

        cases.append(CaseInfo(
            value=value,
            block_id=block_id,
            body_blocks=body_blocks,
            has_break=has_break
        ))

    logger.info(f"Detected binary search switch on '{test_var}' with {len(cases)} cases at block {start_block}")

    # Create initial pattern
    pattern = SwitchPattern(
        test_var=test_var,
        header_block=start_block,
        cases=cases,
        default_block=None,
        exit_block=exit_block,
        all_blocks=all_blocks
    )

    # Detect default case using Ghidra-inspired algorithm
    from .switch_default import detect_default_case, find_default_body_blocks
    default_block = detect_default_case(pattern, cfg, func_block_ids)
    if default_block is not None:
        pattern.default_block = default_block
        pattern.default_body_blocks = find_default_body_blocks(
            default_block, pattern, cfg, func_block_ids
        )
        pattern.all_blocks.add(default_block)
        pattern.all_blocks.update(pattern.default_body_blocks)

    return pattern


def _build_decision_tree(
    block_id: int,
    cfg: CFG,
    ssa_blocks: Dict[int, List[SSAInstruction]],
    resolver: opcodes.OpcodeResolver,
    func_block_ids: Set[int],
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    start_to_block: Dict[int, int],
    max_depth: int = 10,
    visited: Optional[Set[int]] = None,
    expected_var: Optional[str] = None
) -> Optional[Tuple[str, Dict[int, int], Set[int]]]:
    """
    Recursively build decision tree from binary search pattern.

    Returns:
        Tuple of (test_variable, case_map, tree_blocks) where:
        - test_variable: name of variable being tested
        - case_map: dict mapping case value -> case block ID
        - tree_blocks: set of blocks used in decision tree

        Returns None if pattern doesn't match binary search
    """
    if visited is None:
        visited = set()

    if max_depth <= 0 or block_id in visited or block_id not in func_block_ids:
        return None

    visited.add(block_id)
    block = cfg.blocks.get(block_id)

    if not block or not block.instructions:
        return None

    # Check if this block has a conditional jump
    last_instr = block.instructions[-1]
    if not resolver.is_conditional_jump(last_instr.opcode):
        # Leaf node - this is a case entry point
        # Return empty case map, caller will add the case
        if expected_var:
            return (expected_var, {}, {block_id})
        return None

    # Get SSA instructions for this block
    ssa_block = ssa_blocks.get(block_id, [])

    # Look for comparison instructions (EQU, LES, GRE, etc.)
    equ_result = _find_comparison_for_jump(block_id, ssa_block, cfg, ssa_func, formatter)

    if not equ_result:
        # No valid comparison, might be a leaf
        if expected_var:
            return (expected_var, {}, {block_id})
        return None

    comp_type, var_value, const_value = equ_result
    var_name = _format_variable(var_value, formatter)

    # Verify we're testing the same variable throughout tree
    if expected_var is not None and var_name != expected_var:
        logger.debug(f"Variable mismatch in decision tree: expected {expected_var}, got {var_name}")
        return None

    # Get true/false branches using disassembler jump targets
    if len(block.successors) < 2:
        return None

    jump_target, fallthrough = _resolve_conditional_targets(block, start_to_block, resolver)
    if jump_target is None or fallthrough is None:
        return None

    mnemonic = resolver.get_mnemonic(last_instr.opcode)
    if mnemonic == "JNZ":
        true_block, false_block = jump_target, fallthrough
    else:  # JZ
        true_block, false_block = fallthrough, jump_target

    case_map: Dict[int, int] = {}
    tree_blocks: Set[int] = {block_id}

    # Handle equality comparison (EQU) - this finds a specific case
    if comp_type == "EQU":
        # Try to get constant value
        const_val = _extract_constant_value(const_value, ssa_func)
        if const_val is not None:
            # True branch is the case for this value
            case_map[const_val] = true_block
            tree_blocks.add(true_block)

        # False branch continues searching
        false_result = _build_decision_tree(
            false_block, cfg, ssa_blocks, resolver, func_block_ids,
            ssa_func, formatter, start_to_block, max_depth - 1, visited, var_name
        )

        if false_result:
            _, false_cases, false_blocks = false_result
            case_map.update(false_cases)
            tree_blocks.update(false_blocks)

    # Handle range comparisons (LES, GRE, etc.) - binary search nodes
    elif comp_type in ["LES", "ULES", "GRE", "UGRE"]:
        # Both branches might lead to more comparisons or cases
        true_result = _build_decision_tree(
            true_block, cfg, ssa_blocks, resolver, func_block_ids,
            ssa_func, formatter, start_to_block, max_depth - 1, visited, var_name
        )

        false_result = _build_decision_tree(
            false_block, cfg, ssa_blocks, resolver, func_block_ids,
            ssa_func, formatter, start_to_block, max_depth - 1, visited, var_name
        )

        if true_result:
            _, true_cases, true_blocks = true_result
            case_map.update(true_cases)
            tree_blocks.update(true_blocks)

        if false_result:
            _, false_cases, false_blocks = false_result
            case_map.update(false_cases)
            tree_blocks.update(false_blocks)

    if case_map:
        return (var_name, case_map, tree_blocks)

    return None


def _find_comparison_for_jump(
    block_id: int,
    ssa_block: List[SSAInstruction],
    cfg: CFG,
    ssa_func: SSAFunction = None,
    formatter: ExpressionFormatter = None
) -> Optional[Tuple[str, SSAValue, SSAValue]]:
    """
    Find comparison instruction that feeds the conditional jump.

    Returns:
        Tuple of (comparison_type, variable, constant) or None
        comparison_type: "EQU", "LES", "GRE", "ULES", "UGRE", etc.
    """
    # Look for comparison instructions
    comparison_opcodes = ["EQU", "NEQ", "LES", "ULES", "GRE", "UGRE", "ILES", "IGRE"]

    for ssa_inst in reversed(ssa_block):
        if ssa_inst.mnemonic in comparison_opcodes:
            # Found a comparison - get its operands
            if len(ssa_inst.inputs) >= 2:
                arg1, arg2 = ssa_inst.inputs[0], ssa_inst.inputs[1]

                # Typically: variable compared to constant
                # arg1 should be variable, arg2 should be constant
                if _is_constant(arg2):
                    return (ssa_inst.mnemonic, arg1, arg2)
                elif _is_constant(arg1):
                    # Reverse comparison if constant is first
                    reversed_op = _reverse_comparison(ssa_inst.mnemonic)
                    return (reversed_op, arg2, arg1)

    return None


def _is_constant(value: SSAValue) -> bool:
    """Check if an SSA value is a constant."""
    if value.alias and (value.alias.startswith('data_') or value.alias.startswith('const_')):
        return True
    return False


def _reverse_comparison(op: str) -> str:
    """Reverse a comparison operator when operands are swapped."""
    reverse_map = {
        "EQU": "EQU",
        "NEQ": "NEQ",
        "LES": "GRE",
        "GRE": "LES",
        "ULES": "UGRE",
        "UGRE": "ULES",
        "ILES": "IGRE",
        "IGRE": "ILES"
    }
    return reverse_map.get(op, op)


def _format_variable(value: SSAValue, formatter: ExpressionFormatter) -> str:
    """Format an SSA value as a variable name."""
    if hasattr(value, 'alias') and value.alias:
        return value.alias
    return str(value)


def _extract_constant_value(value: SSAValue, ssa_func: SSAFunction) -> Optional[int]:
    """Extract integer constant value from SSA value."""
    # Data segment reference (data_123)
    if value.alias and value.alias.startswith('data_'):
        try:
            offset = int(value.alias[5:])  # Extract number from "data_123"
            if ssa_func.scr and ssa_func.scr.data_segment:
                const_raw = ssa_func.scr.data_segment.get_dword(offset * 4)
                return const_raw
        except (ValueError, AttributeError):
            pass

    return None


def _find_switch_exit(
    case_map: Dict[int, int],
    cfg: CFG,
    func_block_ids: Set[int]
) -> Optional[int]:
    """
    Find common exit block where switch cases merge.

    Looks for a block that is a successor of multiple case blocks.
    """
    if not case_map:
        return None

    case_blocks = set(case_map.values())

    # Find successors of all case blocks
    all_successors: Dict[int, int] = {}  # successor -> count

    for case_block in case_blocks:
        block = cfg.blocks.get(case_block)
        if block:
            for succ in block.successors:
                if succ in func_block_ids:
                    all_successors[succ] = all_successors.get(succ, 0) + 1

    # Find successor that is reached by most cases
    # (common exit point)
    if all_successors:
        exit_block = max(all_successors.items(), key=lambda x: x[1])[0]
        # Only use as exit if reached by at least 50% of cases
        if all_successors[exit_block] >= len(case_blocks) // 2:
            return exit_block

    return None


def _case_has_break_check(
    case_start: int,
    case_blocks: Set[int],
    exit_block: Optional[int],
    cfg: CFG,
    resolver: opcodes.OpcodeResolver
) -> bool:
    """
    Check if a case has an explicit break (jumps to exit).

    Returns True if case breaks, False if it falls through to next case.
    """
    if exit_block is None:
        return True

    # Check if any block in case body jumps to exit
    for block_id in case_blocks:
        block = cfg.blocks.get(block_id)
        if block:
            if exit_block in block.successors:
                return True

            # Check for unconditional jump to exit
            if block.instructions:
                last_instr = block.instructions[-1]
                if last_instr.opcode == "JMP" and last_instr.arg1:
                    target_block = cfg.address_to_block.get(last_instr.arg1)
                    if target_block == exit_block:
                        return True

    return False
