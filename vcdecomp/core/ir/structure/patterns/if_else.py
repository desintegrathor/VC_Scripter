"""
If/else pattern detection for control flow analysis.

This module contains functions for detecting various if/else patterns:
- Simple if/else patterns with true/false branches
- Early return/break patterns
- Short-circuit evaluation (AND/OR compound conditions)
"""

from __future__ import annotations

from typing import Dict, Set, List, Optional, Tuple

from ...cfg import CFG, NaturalLoop
from ....disasm import opcodes
from ...ssa import SSAFunction
from ...expr import ExpressionFormatter

from .models import IfElsePattern, CompoundCondition, TernaryInfo
from ..analysis.flow import _find_common_successor, _find_if_body_blocks
from ..analysis.condition import _collect_and_chain, _collect_or_chain, render_condition
import re


def _detect_early_return_pattern(
    cfg: CFG,
    block_id: int,
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver,
    switch_exit_block: Optional[int] = None
) -> Optional[tuple]:
    """
    Detect early return/break pattern.

    Pattern:
    - Block ends with conditional jump (JZ/JNZ)
    - One branch contains only JMP to exit point (return/break)
    - Other branch continues with normal code

    This should be rendered as:
        if (condition) break;  // or return
        // continue without nesting

    Returns:
        (condition_value, exit_branch, continue_branch, is_negated) or None
        where is_negated=True if condition should be negated for "if (cond) exit"
    """
    block = cfg.blocks.get(block_id)
    if not block or not block.instructions:
        return None

    last_instr = block.instructions[-1]
    conditional_instr = None
    has_explicit_jump = False

    if resolver.is_conditional_jump(last_instr.opcode):
        conditional_instr = last_instr
    elif len(block.instructions) >= 2:
        second_last = block.instructions[-2]
        if (resolver.is_conditional_jump(second_last.opcode) and
                resolver.get_mnemonic(last_instr.opcode) == "JMP"):
            conditional_instr = second_last
            has_explicit_jump = True

    if conditional_instr is None:
        return None

    # Get true (jump target) and false (fallthrough) branches
    true_addr = last_instr.arg1
    false_addr = last_instr.address + 1
    true_block = start_to_block.get(true_addr)
    false_block = start_to_block.get(false_addr)

    if true_block is None or false_block is None:
        return None

    # Check if one branch is just JMP to exit
    def is_exit_jump(bid: int) -> bool:
        """Check if block is just unconditional JMP to exit point."""
        b = cfg.blocks.get(bid)
        if not b or not b.instructions:
            return False
        # Block should have exactly 1 instruction (JMP)
        if len(b.instructions) != 1:
            return False
        instr = b.instructions[0]
        mnem = resolver.get_mnemonic(instr.opcode)
        if mnem != "JMP":
            return False
        # Jump target should be exit point (outside current scope)
        # For switch cases, check if jumping to switch exit
        if switch_exit_block is not None:
            jump_target = start_to_block.get(instr.arg1)
            return jump_target == switch_exit_block
        return True

    mnemonic = resolver.get_mnemonic(last_instr.opcode)

    # Check which branch is the exit
    if is_exit_jump(true_block):
        # True branch exits, false continues
        # For JZ: condition is false -> exits, so render as "if (cond) continue" = "if (!cond) exit"
        # For JNZ: condition is true -> exits, so render as "if (cond) exit"
        is_negated = (mnemonic == "JZ")
        return (block_id, true_block, false_block, is_negated)
    elif is_exit_jump(false_block):
        # False branch exits, true continues
        # For JZ: condition is true -> exits, so render as "if (!cond) exit"
        # For JNZ: condition is false -> exits, so render as "if (cond) continue" = "if (!cond) exit"
        is_negated = (mnemonic == "JNZ")
        return (block_id, false_block, true_block, is_negated)

    return None


def _detect_short_circuit_pattern(
    cfg: CFG,
    header_block_id: int,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter
) -> Optional[CompoundCondition]:
    """
    Detect short-circuit && and || patterns using multi-block analysis.

    NEW IMPLEMENTATION: Follows fallthrough chains across multiple blocks
    to detect AND chains and OR chains, then identifies combined patterns.

    Patterns detected:
    1. Simple AND: Block A → Block B → JMP (JZ to same false target)
    2. Simple OR: Block A → Block B → JMP (JNZ to same true target)
    3. Combined: (AND) OR (AND) - multiple AND chains to same TRUE target

    Args:
        cfg: Control flow graph
        header_block_id: Starting block to analyze
        resolver: Opcode resolver
        start_to_block: Mapping from addresses to block IDs
        ssa_func: SSA function for condition extraction
        formatter: Expression formatter

    Returns:
        CompoundCondition if pattern detected, None otherwise
    """
    # Step 1: Try to collect an AND chain starting from this block
    visited_and = set()
    and_blocks, and_true_target, and_false_target = _collect_and_chain(
        header_block_id, cfg, resolver, start_to_block, visited_and
    )

    # Step 1b: Also try to collect an OR chain starting from this block
    visited_or = set()
    or_blocks, or_true_target, or_false_target = _collect_or_chain(
        header_block_id, cfg, resolver, start_to_block, visited_or
    )

    # Prefer OR chain if it has more blocks than AND chain (OR is usually the outer pattern)
    # OR chain with 2+ blocks takes precedence over single-block AND chain
    if or_blocks and len(or_blocks) >= 2:
        # We have a multi-block OR chain - use it
        or_conditions = []
        or_condition_addrs: Set[int] = set()
        for block_id in or_blocks:
            condition_render = render_condition(
                ssa_func,
                block_id,
                formatter,
                cfg,
                resolver,
                negate=False
            )
            if condition_render.text:
                or_conditions.append(condition_render.text)
                or_condition_addrs.update(condition_render.addresses)

        if len(or_conditions) >= 2:
            # Import here to avoid circular dependency
            from ..analysis.flow import _find_compound_body_blocks

            # Create temporary compound to calculate bodies
            temp_compound = CompoundCondition(
                operator="||",
                conditions=or_conditions,
                true_target=or_true_target if or_true_target is not None else -1,
                false_target=or_false_target if or_false_target is not None else -1,
                involved_blocks=set(or_blocks),
                condition_addrs=set(or_condition_addrs)
            )

            # Calculate bodies for this OR compound
            true_body, false_body, merge_point = _find_compound_body_blocks(
                cfg, temp_compound, resolver
            )

            # VALIDATION: Empty body means bad detection
            if true_body:
                # Create final compound with calculated bodies
                return CompoundCondition(
                    operator="||",
                    conditions=or_conditions,
                    true_target=or_true_target if or_true_target is not None else -1,
                    false_target=or_false_target if or_false_target is not None else -1,
                    involved_blocks=set(or_blocks),
                    condition_addrs=set(or_condition_addrs),
                    true_body=true_body,
                    false_body=false_body,
                    merge_point=merge_point
                )

    # Fall back to AND chain detection
    true_target = and_true_target
    false_target = and_false_target

    # No AND chain detected
    if not and_blocks:
        return None

    # Step 2: Extract conditions from each block in the AND chain
    and_conditions = []
    and_condition_addrs: Set[int] = set()
    for block_id in and_blocks:
        condition_render = render_condition(
            ssa_func,
            block_id,
            formatter,
            cfg,
            resolver,
            negate=False
        )
        if condition_render.text:
            and_conditions.append(condition_render.text)
            and_condition_addrs.update(condition_render.addresses)

    if not and_conditions:
        return None

    # Step 3: Create AND compound (or single condition if len==1)
    if len(and_conditions) > 1:
        # Import here to avoid circular dependency
        from ..analysis.flow import _find_compound_body_blocks

        # Create temporary compound to calculate bodies
        temp_compound = CompoundCondition(
            operator="&&",
            conditions=and_conditions,
            true_target=true_target if true_target is not None else -1,
            false_target=false_target if false_target is not None else -1,
            involved_blocks=set(and_blocks),
            condition_addrs=set(and_condition_addrs)
        )

        # Calculate bodies for this AND compound
        true_body, false_body, merge_point = _find_compound_body_blocks(
            cfg, temp_compound, resolver
        )

        # VALIDATION: Empty body means bad detection
        if not true_body:
            return None  # Don't create compound with empty body

        # Create final compound with calculated bodies
        and_compound = CompoundCondition(
            operator="&&",
            conditions=and_conditions,
            true_target=true_target if true_target is not None else -1,
            false_target=false_target if false_target is not None else -1,
            involved_blocks=set(and_blocks),
            condition_addrs=set(and_condition_addrs),
            true_body=true_body,
            false_body=false_body,
            merge_point=merge_point
        )
    else:
        # Single condition - might still be part of OR
        and_compound = and_conditions[0]  # Just the string
        and_condition_addrs = set(and_condition_addrs)

    # Step 4: Check if false_target leads to another OR branch
    if false_target is None or true_target is None:
        # No clear targets, return what we have
        if isinstance(and_compound, CompoundCondition):
            return and_compound
        return None

    # Step 5: Recursively check if false_target is start of another AND chain
    # that jumps to the SAME true_target (indicating OR)
    next_branch = _detect_short_circuit_pattern(
        cfg, false_target, resolver, start_to_block, ssa_func, formatter
    )

    # Step 6: If next branch jumps to same TRUE target, combine with OR
    if next_branch and next_branch.true_target == true_target:
        # Import here to avoid circular dependency
        from ..analysis.flow import _find_compound_body_blocks

        # Build OR compound
        or_conditions = []
        or_involved_blocks = set()
        or_condition_addrs: Set[int] = set()

        # Add first AND branch
        if isinstance(and_compound, CompoundCondition):
            or_conditions.append(and_compound)
            or_involved_blocks.update(and_compound.involved_blocks)
            or_condition_addrs.update(and_compound.condition_addrs)
        else:
            or_conditions.append(and_compound)
            or_involved_blocks.update(and_blocks)
            or_condition_addrs.update(and_condition_addrs)

        # Add second AND branch (or more if recursively nested)
        or_conditions.append(next_branch)
        or_involved_blocks.update(next_branch.involved_blocks)
        or_condition_addrs.update(next_branch.condition_addrs)

        # Create temporary OR compound to calculate bodies
        temp_or_compound = CompoundCondition(
            operator="||",
            conditions=or_conditions,
            true_target=true_target,
            false_target=next_branch.false_target,  # Use last branch's false target
            involved_blocks=or_involved_blocks,
            condition_addrs=or_condition_addrs
        )

        # Calculate bodies for OR compound
        true_body, false_body, merge_point = _find_compound_body_blocks(
            cfg, temp_or_compound, resolver
        )

        # VALIDATION: Empty body means bad detection
        if not true_body:
            return None  # Don't create compound with empty body

        # Return final OR compound with calculated bodies
        return CompoundCondition(
            operator="||",
            conditions=or_conditions,
            true_target=true_target,
            false_target=next_branch.false_target,  # Use last branch's false target
            involved_blocks=or_involved_blocks,
            condition_addrs=or_condition_addrs,
            true_body=true_body,
            false_body=false_body,
            merge_point=merge_point
        )

    # No OR detected, return the AND compound
    if isinstance(and_compound, CompoundCondition):
        return and_compound

    # Single condition, not compound
    return None


def _detect_if_else_pattern(
    cfg: CFG,
    block_id: int,
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver,
    visited_ifs: Set[int],
    func_loops: Optional[List] = None,
    context_stop_blocks: Optional[Set[int]] = None,
    ssa_func: Optional[SSAFunction] = None,
    formatter: Optional = None  # ExpressionFormatter
) -> Optional[IfElsePattern]:
    """
    Detect if/else pattern starting at block_id.

    Pattern:
    - Block ends with conditional jump (JZ/JNZ)
    - Has exactly 2 successors (true and false branches)
    - Branches may or may not merge at a common successor

    NOTE: If ssa_func and formatter are provided, will attempt to detect
    compound conditions (AND/OR chains) before falling back to simple if/else.

    Args:
        cfg: Control flow graph
        block_id: Block to check
        start_to_block: Address to block ID mapping
        resolver: Opcode resolver
        visited_ifs: Set of already processed if patterns
        func_loops: List of loops in function (optional, to avoid misdetecting loop headers)
        context_stop_blocks: Blocks to stop at (for switch case analysis)
        ssa_func: SSA function (optional, for compound condition detection)
        formatter: Expression formatter (optional, for compound condition detection)
    """
    if block_id in visited_ifs:
        return None

    # NEW: Try to detect compound conditions first (if we have SSA/formatter available)
    # This must be done BEFORE simple if/else detection to avoid breaking up compound patterns
    if ssa_func is not None and formatter is not None:
        compound = _detect_short_circuit_pattern(
            cfg, block_id, resolver, start_to_block, ssa_func, formatter
        )
        if compound:
            # Convert CompoundCondition to IfElsePattern for compatibility
            # NOTE: Don't add to visited_ifs here - let the rendering code do that
            # Adding here would prevent _format_block_lines from calling _render_if_else_recursive

            # Create IfElsePattern representing the compound condition
            # We'll use a special marker to indicate this is compound
            if_pattern = IfElsePattern(
                header_block=block_id,
                true_block=compound.true_target,
                false_block=compound.false_target,
                merge_block=-1  # Will be determined later
            )
            # Store compound info in the pattern for later rendering
            # We'll use a custom attribute (Python allows this)
            if_pattern.compound = compound  # type: ignore
            return if_pattern

    # FÁZE 3.2 FIX: Don't detect loop headers as if/else
    # Loop headers have back edges and should be handled by loop detection instead
    if func_loops:
        for loop in func_loops:
            if loop.header == block_id:
                return None  # This is a loop header, not an if/else

    block = cfg.blocks.get(block_id)
    if not block or not block.instructions:
        return None

    last_instr = block.instructions[-1]
    conditional_instr = None
    has_explicit_jump = False

    if resolver.is_conditional_jump(last_instr.opcode):
        conditional_instr = last_instr
    elif len(block.instructions) >= 2:
        second_last = block.instructions[-2]
        if (resolver.is_conditional_jump(second_last.opcode) and
                resolver.get_mnemonic(last_instr.opcode) == "JMP"):
            conditional_instr = second_last
            has_explicit_jump = True

    if conditional_instr is None:
        return None

    # FÁZE 2C: Allow 1 or 2 successors (1 = if-without-else, 2 = if/else)
    if len(block.successors) < 1 or len(block.successors) > 2:
        return None

    # Get true and false blocks
    # CRITICAL FIX: JZ vs JNZ have opposite semantics!
    # JZ (Jump if Zero) = jump when condition is FALSE (zero)
    #   -> arg1 is FALSE branch, fallthrough is TRUE branch
    # JNZ (Jump if Not Zero) = jump when condition is TRUE (not zero)
    #   -> arg1 is TRUE branch, fallthrough is FALSE branch

    mnemonic = resolver.get_mnemonic(conditional_instr.opcode)
    jump_addr = conditional_instr.arg1
    fallthrough_addr = conditional_instr.address + 1

    if has_explicit_jump:
        jmp_target = last_instr.arg1
        if mnemonic == "JZ":
            # JZ: jump target is FALSE branch, JMP is TRUE branch
            true_addr = jmp_target
            false_addr = jump_addr
        elif mnemonic == "JNZ":
            # JNZ: jump target is TRUE branch, JMP is FALSE branch
            true_addr = jump_addr
            false_addr = jmp_target
        else:
            true_addr = jmp_target
            false_addr = jump_addr
    else:
        if mnemonic == "JZ":
            # JZ: jump target is FALSE branch, fallthrough is TRUE branch
            true_addr = fallthrough_addr
            false_addr = jump_addr
        elif mnemonic == "JNZ":
            # JNZ: jump target is TRUE branch, fallthrough is FALSE branch
            true_addr = jump_addr
            false_addr = fallthrough_addr
        else:
            # Other conditional jumps - assume JZ behavior (most common)
            true_addr = fallthrough_addr
            false_addr = jump_addr

    true_block = start_to_block.get(true_addr)
    if true_block is None:
        return None

    # For if-without-else, false branch might not exist (just fallthrough to merge)
    false_block = start_to_block.get(false_addr)

    # If only 1 successor, this is if-without-else (jump target is true branch, no false branch)
    if len(block.successors) == 1:
        false_block = None  # No else branch

    # Find merge point (common successor)
    # For if-without-else, merge point is the fallthrough (false_block will be None)
    if false_block is not None:
        merge_block = _find_common_successor(cfg, true_block, false_block)
    else:
        # If-without-else: merge point is the next block after jump
        merge_block = start_to_block.get(false_addr)

    # Find all blocks in each branch
    # CRITICAL FIX: Exclude the other branch from body detection to prevent overlap
    stop_blocks = {merge_block} if merge_block else set()

    # BUG FIX #4: Add context stop blocks (e.g., switch case boundaries)
    if context_stop_blocks:
        stop_blocks.update(context_stop_blocks)

    # FIX #2: Add loop body blocks to stop blocks to prevent if/else from capturing loop code
    # This prevents if/else BFS from crossing into loop bodies that should be rendered inside loops
    if func_loops:
        for loop in func_loops:
            # Add all blocks in loop body (including header) to stop blocks
            stop_blocks.update(loop.body)
            # Also add the loop header itself
            stop_blocks.add(loop.header)

    # For true branch, exclude false branch entry to prevent crossing
    true_stop = stop_blocks | {false_block} if false_block else stop_blocks
    true_body = _find_if_body_blocks(cfg, true_block, true_stop, resolver)

    # For false branch, exclude true branch entry to prevent crossing
    if false_block:
        # CRITICAL FIX: If false_block IS the merge point, there's no else branch
        if false_block == merge_block:
            false_body = set()
        else:
            # FÁZE 3.1 FIX: Check if false_block is "empty" (just unconditional JMP)
            # This happens when compiler optimizes: if (cond) { return; }
            # The false branch is just "JMP to merge", not actual else code
            false_block_obj = cfg.blocks.get(false_block)
            is_empty_false = False

            if false_block_obj and false_block_obj.instructions:
                # Check if first instruction is unconditional JMP
                first_instr = false_block_obj.instructions[0]
                if resolver.get_mnemonic(first_instr.opcode) == "JMP":
                    # Empty false branch - just jumps to merge point
                    is_empty_false = True

            if is_empty_false:
                false_body = set()
            else:
                false_stop = stop_blocks | {true_block}
                false_body = _find_if_body_blocks(cfg, false_block, false_stop, resolver)
    else:
        false_body = set()

    visited_ifs.add(block_id)

    return IfElsePattern(
        header_block=block_id,
        true_block=true_block,
        false_block=false_block,
        merge_block=merge_block,
        true_body=true_body,
        false_body=false_body
    )


def _detect_ternary_pattern(
    if_pattern: IfElsePattern,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    cfg: CFG,
    resolver: opcodes.OpcodeResolver,
    condition_text: str
) -> Optional[TernaryInfo]:
    """
    Detect if an if/else pattern can be rendered as a ternary operator.

    Criteria:
    1. true_body and false_body each contain exactly 1 block
    2. Each block has exactly 1 assignment expression (no side effects)
    3. Both assignments target the SAME variable
    4. merge_block exists (branches rejoin)
    5. Neither branch has function calls (XCALL/CALL), returns, or breaks

    Args:
        if_pattern: The if/else pattern to analyze
        ssa_func: SSA function data
        formatter: Expression formatter
        cfg: Control flow graph
        resolver: Opcode resolver
        condition_text: Pre-rendered condition expression

    Returns:
        TernaryInfo if pattern matches, None otherwise
    """
    # Import here to avoid circular import
    from ...expr import format_block_expressions

    # Criterion 4: merge_block must exist (branches rejoin)
    if if_pattern.merge_block is None:
        return None

    # Criterion 1a: true_body must have exactly 1 block
    if len(if_pattern.true_body) != 1:
        return None

    # Criterion 1b: false_body must have exactly 1 block (and not be empty)
    if not if_pattern.false_body or len(if_pattern.false_body) != 1:
        return None

    true_block_id = next(iter(if_pattern.true_body))
    false_block_id = next(iter(if_pattern.false_body))

    # Criterion 5a: Check true block for side effects (XCALL/CALL/RET/break)
    true_block = cfg.blocks.get(true_block_id)
    if true_block and true_block.instructions:
        for instr in true_block.instructions:
            mnem = resolver.get_mnemonic(instr.opcode)
            # Skip if block has function calls or returns
            if mnem in {"XCALL", "CALL", "RET"}:
                return None
            # JMP is OK (used to jump to merge point)

    # Criterion 5b: Check false block for side effects
    false_block = cfg.blocks.get(false_block_id)
    if false_block and false_block.instructions:
        for instr in false_block.instructions:
            mnem = resolver.get_mnemonic(instr.opcode)
            if mnem in {"XCALL", "CALL", "RET"}:
                return None

    # Criterion 2 & 3: Get expressions from each block and validate
    true_exprs = format_block_expressions(ssa_func, true_block_id, formatter=formatter)
    false_exprs = format_block_expressions(ssa_func, false_block_id, formatter=formatter)

    # Filter out control flow (goto, etc.)
    true_assignments = []
    for expr in true_exprs:
        text = expr.text.strip()
        if text.startswith("goto ") or not text:
            continue
        true_assignments.append(text)

    false_assignments = []
    for expr in false_exprs:
        text = expr.text.strip()
        if text.startswith("goto ") or not text:
            continue
        false_assignments.append(text)

    # Criterion 2: Each block must have exactly 1 assignment
    if len(true_assignments) != 1 or len(false_assignments) != 1:
        return None

    true_stmt = true_assignments[0].rstrip(';')
    false_stmt = false_assignments[0].rstrip(';')

    # Parse assignments with regex: "variable = expression"
    # Must handle complex variable names like "local_0", "gData[i]", etc.
    # Pattern: capture variable name, then "=", then the rest (value)
    assign_pattern = re.compile(r'^(\S+)\s*=\s*(.+)$')

    true_match = assign_pattern.match(true_stmt)
    false_match = assign_pattern.match(false_stmt)

    if not true_match or not false_match:
        return None

    true_var, true_value = true_match.groups()
    false_var, false_value = false_match.groups()

    # Criterion 3: Both assignments must target the SAME variable
    if true_var != false_var:
        return None

    # Additional safety check: values should not contain function calls
    # (Some expressions might slip through bytecode check)
    if '(' in true_value or '(' in false_value:
        # Could be a function call - skip to be safe
        # Exception: type casts like "(float)" or "(int)" are OK
        # Simple heuristic: if there's a comma, it's likely a function call
        if ',' in true_value or ',' in false_value:
            return None
        # Check for function call pattern: identifier followed by (
        func_call_pattern = re.compile(r'\b[a-zA-Z_]\w*\s*\(')
        if func_call_pattern.search(true_value) or func_call_pattern.search(false_value):
            # Exception for casts: (type)value
            cast_pattern = re.compile(r'^\(\w+\)\s*\S+$')
            if not (cast_pattern.match(true_value.strip()) or cast_pattern.match(false_value.strip())):
                return None

    return TernaryInfo(
        variable=true_var,
        condition=condition_text,
        true_value=true_value,
        false_value=false_value
    )
