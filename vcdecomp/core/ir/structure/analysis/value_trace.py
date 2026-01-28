"""
Value tracing utilities for SSA analysis.

This module contains functions for tracing SSA values back to their sources,
including function calls, global variables, and function parameters.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set, Dict
import logging
import re
import sys

from ...ssa import SSAFunction
from ...expr import ExpressionFormatter

logger = logging.getLogger(__name__)

LOGICAL_OPS = {"AND", "OR"}
NEGATION_OPS = {"NOT"}


def _trace_branch_operands(
    value,
    max_depth: int = 10,
    operands: Optional[list] = None,
    addresses: Optional[Set[int]] = None,
    visited: Optional[Set[int]] = None,
) -> tuple[list, Set[int]]:
    """
    Trace operands for composite branch conditions (AND/OR/NOT).

    This helper expands logical operators so their underlying operands
    are included when collecting condition values for branch rendering.
    """
    if operands is None:
        operands = []
    if addresses is None:
        addresses = set()
    if visited is None:
        visited = set()

    if not value or max_depth < 0 or id(value) in visited:
        return operands, addresses

    visited.add(id(value))
    operands.append(value)

    producer = value.producer_inst
    if not producer:
        return operands, addresses

    addresses.add(producer.address)

    if producer.mnemonic in LOGICAL_OPS or producer.mnemonic in NEGATION_OPS:
        for input_value in producer.inputs:
            _trace_branch_operands(
                input_value,
                max_depth - 1,
                operands=operands,
                addresses=addresses,
                visited=visited,
            )
        return operands, addresses

    if producer.mnemonic == "PHI":
        for input_value in producer.inputs:
            _trace_branch_operands(
                input_value,
                max_depth - 1,
                operands=operands,
                addresses=addresses,
                visited=visited,
            )
        return operands, addresses

    for input_value in producer.inputs:
        _trace_branch_operands(
            input_value,
            max_depth - 1,
            operands=operands,
            addresses=addresses,
            visited=visited,
        )

    return operands, addresses


def _score_producer_quality(inst):
    """Score instruction quality for PHI resolution - prefer informative sources."""
    if inst.mnemonic in {'GCP', 'GLD', 'GADR'}:
        return 100  # Global load - highest priority
    if inst.mnemonic in {'LCP', 'LADR'}:
        return 50   # Parameter/local load
    if inst.mnemonic == 'DCP':
        return 30   # Pointer dereference (field access)
    if inst.mnemonic == 'IMOD':
        return 40   # Modulo expression
    if inst.mnemonic in {'XCALL', 'CALL'}:
        return 35   # Function call
    return 10       # Other (temporaries, arithmetic)


def _follow_ssa_value_across_blocks(
    value,
    ssa_func: SSAFunction,
    seen_blocks: Optional[Set[int]] = None,
    max_depth: int = 15
):
    """
    Follow SSA value definition across block boundaries.

    This helper traces an SSA value back to its producer instruction even when
    the producer is in a different block. This is critical for switch detection
    where values flow across multiple blocks.

    Pattern handled:
        Block 1: LADR [sp-4]  -> base_ptr
                 JMP Block 2
        Block 2: DADR base_ptr, offset -> field_ptr
                 JMP Block 3
        Block 3: DCP field_ptr -> value
                 EQU value, const

    Args:
        value: SSA value to trace
        ssa_func: SSA function containing the value
        seen_blocks: Set of block IDs already visited (to prevent infinite loops)
        max_depth: Maximum recursion depth (default: 5)

    Returns:
        Producer instruction if found, None otherwise
    """
    if not value or max_depth <= 0:
        return None

    if seen_blocks is None:
        seen_blocks = set()

    # Get producer instruction
    prod_inst = value.producer_inst

    # If we have a direct producer that's not a PHI, return it
    if prod_inst and prod_inst.mnemonic != "PHI":
        logger.debug(f"  _follow_ssa_value_across_blocks: Found producer {prod_inst.mnemonic} at {prod_inst.address} in block {prod_inst.block_id}")
        return prod_inst

    # Handle PHI nodes - trace backward through predecessors
    if prod_inst and prod_inst.mnemonic == "PHI":
        logger.debug(f"  _follow_ssa_value_across_blocks: Following PHI with {len(prod_inst.inputs)} inputs")

        # Avoid revisiting same block
        if prod_inst.block_id in seen_blocks:
            logger.debug(f"  _follow_ssa_value_across_blocks: Already visited block {prod_inst.block_id}")
            return None
        seen_blocks.add(prod_inst.block_id)

        # Try ALL PHI inputs and pick best producer
        results = []
        for phi_input in prod_inst.inputs:
            logger.debug(f"  _follow_ssa_value_across_blocks: Trying PHI input {phi_input.name}")
            # Use copy of seen_blocks to allow exploring all branches
            result = _follow_ssa_value_across_blocks(
                phi_input, ssa_func, seen_blocks.copy(), max_depth - 1
            )
            if result:
                score = _score_producer_quality(result)
                results.append((result, score))
                logger.debug(f"    -> Found producer {result.mnemonic} (score: {score})")

        if results:
            # Pick best producer (prefer global/parameter loads over temporaries)
            best = max(results, key=lambda x: x[1])
            logger.debug(f"  -> Selected best producer: {best[0].mnemonic}")
            return best[0]

    # No producer found through normal means
    logger.debug(f"  _follow_ssa_value_across_blocks: No producer found for {value.name}")
    return None


def _check_ssa_value_equivalence(
    value1,
    value2,
    ssa_func: SSAFunction,
    max_depth: int = 10
) -> bool:
    """
    Check if two SSA values represent the same semantic variable.

    Handles:
    - Direct SSA name match (v_123 == v_123)
    - Both load from same memory location (LCP [sp+4])
    - Both trace to same PHI node input
    - Both trace to same parameter field (info->message)
    - Both trace to same global variable

    Args:
        value1: First SSA value to compare
        value2: Second SSA value to compare
        ssa_func: SSA function containing the values
        max_depth: Maximum recursion depth (default: 10)

    Returns:
        True if values represent the same semantic variable, False otherwise
    """
    if not value1 or not value2 or max_depth <= 0:
        return False

    # Direct match
    if hasattr(value1, 'name') and hasattr(value2, 'name'):
        if value1.name == value2.name:
            return True

    # Trace to ultimate producers (through PHIs)
    prod1 = _follow_ssa_value_across_blocks(value1, ssa_func, max_depth=max_depth)
    prod2 = _follow_ssa_value_across_blocks(value2, ssa_func, max_depth=max_depth)

    if not prod1 or not prod2:
        return False

    # Same producer instruction
    if prod1 == prod2:
        return True

    # Both load from same stack offset (LCP [sp+4])
    if prod1.mnemonic == 'LCP' and prod2.mnemonic == 'LCP':
        if prod1.instruction and prod1.instruction.instruction and \
           prod2.instruction and prod2.instruction.instruction:
            if prod1.instruction.instruction.arg1 == prod2.instruction.instruction.arg1:
                logger.debug(f"    -> SSA equivalence: both LCP from same stack offset {prod1.instruction.instruction.arg1}")
                return True

    # Both load from same global (GCP/GLD data[X])
    if prod1.mnemonic in {'GCP', 'GLD'} and prod2.mnemonic in {'GCP', 'GLD'}:
        if prod1.instruction and prod1.instruction.instruction and \
           prod2.instruction and prod2.instruction.instruction:
            if prod1.instruction.instruction.arg1 == prod2.instruction.instruction.arg1:
                logger.debug(f"    -> SSA equivalence: both load from same global offset {prod1.instruction.instruction.arg1}")
                return True

    # Both dereference same base pointer (DCP)
    # Pattern: DCP(DADR(LADR [sp-4], 0)) - both access same field
    if prod1.mnemonic == 'DCP' and prod2.mnemonic == 'DCP':
        if len(prod1.inputs) > 0 and len(prod2.inputs) > 0:
            # Recursively check if the base pointers are equivalent
            return _check_ssa_value_equivalence(
                prod1.inputs[0], prod2.inputs[0], ssa_func, max_depth - 1
            )

    # Check if both trace to DADR (field offset) with same offset
    if prod1.mnemonic == 'DADR' and prod2.mnemonic == 'DADR':
        # Check if same field offset
        if prod1.instruction and prod1.instruction.instruction and \
           prod2.instruction and prod2.instruction.instruction:
            if prod1.instruction.instruction.arg1 == prod2.instruction.instruction.arg1:
                # Same offset, check if base addresses are equivalent
                if len(prod1.inputs) > 0 and len(prod2.inputs) > 0:
                    return _check_ssa_value_equivalence(
                        prod1.inputs[0], prod2.inputs[0], ssa_func, max_depth - 1
                    )

    # Check if both trace to LADR (parameter address) with same offset
    if prod1.mnemonic == 'LADR' and prod2.mnemonic == 'LADR':
        if prod1.instruction and prod1.instruction.instruction and \
           prod2.instruction and prod2.instruction.instruction:
            if prod1.instruction.instruction.arg1 == prod2.instruction.instruction.arg1:
                logger.debug(f"    -> SSA equivalence: both LADR from same parameter offset {prod1.instruction.instruction.arg1}")
                return True

    # PHASE 8B Priority 1: Check if both are XCALL/CALL with same function and arguments
    # This handles patterns like: switch(SC_ggi(GVAR_GAMEPHASE)) where each case has
    # its own XCALL instruction but they call the same function with the same argument
    if prod1.mnemonic in {'XCALL', 'CALL'} and prod2.mnemonic in {'XCALL', 'CALL'}:
        # Check if calling same function
        if prod1.mnemonic == prod2.mnemonic:
            # For XCALL, arg1 is XFN index; for CALL, arg1 is function address
            if prod1.instruction and prod1.instruction.instruction and \
               prod2.instruction and prod2.instruction.instruction:
                same_function = (prod1.instruction.instruction.arg1 ==
                                prod2.instruction.instruction.arg1)

                if same_function:
                    # Same function - now check if arguments match
                    # XCALL/CALL arguments are in the inputs list
                    args1 = _extract_call_arguments(prod1, ssa_func)
                    args2 = _extract_call_arguments(prod2, ssa_func)

                    # If both have same number of args
                    if len(args1) == len(args2):
                        # Recursively check if all arguments are equivalent
                        args_match = all(
                            _check_ssa_value_equivalence(a1, a2, ssa_func, max_depth-1)
                            for a1, a2 in zip(args1, args2)
                        )

                        if args_match:
                            logger.debug(f"    -> SSA equivalence: both call {prod1.mnemonic} "
                                        f"with same function and arguments")
                            return True

    return False


def _extract_call_arguments(call_inst, ssa_func: SSAFunction) -> list:
    """
    PHASE 8B Priority 1: Extract arguments passed to XCALL/CALL instruction.

    In the VC compiler, function arguments are passed via the SSA instruction inputs.
    For XCALL/CALL instructions, the inputs list contains the argument values.

    Args:
        call_inst: XCALL or CALL SSA instruction
        ssa_func: SSA function containing the instruction

    Returns:
        List of SSA values representing the arguments (in order)
    """
    args = []

    # Check if instruction has inputs (arguments)
    if hasattr(call_inst, 'inputs') and call_inst.inputs:
        # The inputs are the arguments passed to the function
        args = list(call_inst.inputs)

    logger.debug(f"    _extract_call_arguments: {call_inst.mnemonic} at {call_inst.address} "
                f"has {len(args)} arguments")

    return args


def call_is_condition_only(
    ssa_func: SSAFunction,
    call_inst,
    condition_addresses: Set[int],
) -> bool:
    """
    Check whether a CALL/XCALL return value is used exclusively in a jump condition.

    This is used to safely inline calls into conditions without dropping a statement
    whose return value is referenced elsewhere.
    """
    if not call_inst or not condition_addresses:
        return False

    return_values = list(call_inst.outputs or [])

    if not return_values:
        block_instructions = ssa_func.instructions.get(call_inst.block_id, [])
        call_index = None
        for idx, inst in enumerate(block_instructions):
            if inst.address == call_inst.address:
                call_index = idx
                break
        if call_index is not None:
            for idx in range(call_index + 1, min(call_index + 4, len(block_instructions))):
                next_inst = block_instructions[idx]
                if next_inst.mnemonic == "LLD" and next_inst.outputs:
                    return_values.extend(next_inst.outputs)
                    break

    if not return_values:
        return False

    for return_value in return_values:
        for use_addr, _ in return_value.uses:
            if use_addr not in condition_addresses:
                return False

    return True


def _is_simple_identifier(name: Optional[str]) -> bool:
    if not name:
        return False
    return re.match(r"^[A-Za-z_]\w*$", name) is not None


def _looks_like_address(value) -> bool:
    if value.alias and value.alias.startswith("&"):
        return True
    if value.producer_inst and value.producer_inst.mnemonic in {"LADR", "GADR", "DADR", "PNT"}:
        return True
    return False


def _get_assignment_source_target(asgn_inst) -> tuple:
    if not asgn_inst or len(asgn_inst.inputs) < 2:
        return (None, None)
    left, right = asgn_inst.inputs[0], asgn_inst.inputs[1]
    left_addr = _looks_like_address(left)
    right_addr = _looks_like_address(right)

    if right_addr and not left_addr:
        return (left, right)
    if left_addr and not right_addr:
        return (right, left)
    return (left, right)


def _build_condition_value_map(
    ssa_func: SSAFunction,
    block_id: int,
    jump_address: int,
    condition_values,
    formatter: ExpressionFormatter
) -> Dict[str, str]:
    """
    Build SSA rename mapping for condition values based on the last assignment.

    This helps map the SSA value used in a condition back to the variable
    assigned immediately before the conditional jump.
    """
    ssa_block = ssa_func.instructions.get(block_id, [])
    if not ssa_block:
        return {}

    jump_index = len(ssa_block)
    for idx, inst in enumerate(ssa_block):
        if inst.address == jump_address:
            jump_index = idx
            break

    last_asgn = None
    for idx in range(jump_index - 1, -1, -1):
        inst = ssa_block[idx]
        if inst.mnemonic == "ASGN" and len(inst.inputs) >= 2:
            last_asgn = inst
            break

    if not last_asgn:
        return {}

    source_value, target_value = _get_assignment_source_target(last_asgn)
    if not source_value or not target_value:
        return {}

    if hasattr(formatter, "_format_pointer_target"):
        target_name = formatter._format_pointer_target(target_value)
    else:
        target_name = formatter.render_value(target_value)

    if target_name.startswith("&"):
        target_name = target_name[1:]

    if not _is_simple_identifier(target_name):
        return {}

    for cond_value in condition_values or []:
        if not cond_value:
            continue
        if _check_ssa_value_equivalence(cond_value, source_value, ssa_func):
            return {source_value.name: target_name}
        if hasattr(cond_value, "name") and cond_value.name == source_value.name:
            return {source_value.name: target_name}

    return {}


@dataclass
class BoundInfo:
    """Information about loop bounds for array dimension inference."""
    min_value: int  # Minimum index seen
    max_value: int  # Maximum index seen
    step: int       # Iteration step (usually 1)
    confidence: float  # How certain we are about bounds (0.0-1.0)


def _trace_value_to_function_call(
    ssa_func: SSAFunction,
    value: "SSAValue",
    formatter: "ExpressionFormatter",
    max_depth: int = 10
) -> Optional[str]:
    """
    PHASE 8B.2: Trace a value back to its producer to check if it's a function call result.

    Enhanced to search across blocks for XCALL/CALL patterns.

    Pattern to detect:
    - XCALL/CALL instruction
    - Followed by LLD [sp+307] (load return value)
    - Value used in condition or assignment (possibly across blocks)

    Args:
        ssa_func: SSA function containing the value
        value: SSA value to trace
        formatter: Expression formatter for rendering
        max_depth: Maximum recursion depth (default: 10, increased from 5)

    Returns:
        Function call expression (e.g., "SC_ggi(GVAR_GAMEPHASE)") if found, None otherwise
    """
    if not value or max_depth <= 0:
        return None

    # DEBUG
    import sys
    import os
    debug = os.environ.get('VCDECOMP_SWITCH_DEBUG') == '1'

    # Check if this value came from any instruction
    if not value.producer_inst:
        return None

    producer = value.producer_inst

    # Direct XCALL/CALL result (rare but possible)
    if producer.mnemonic in {"XCALL", "CALL"}:
        return _format_xcall_expression(producer, formatter, ssa_func)

    # NEW PHASE 8B.2: Check if producer is LCP (stack reload pattern)
    # This indicates the value was stored to stack and is being reloaded,
    # which is common when function call results are used across blocks
    if producer.mnemonic == "LCP":
        # Extract stack offset from LCP instruction
        stack_offset = None
        if producer.instruction and producer.instruction.instruction:
            stack_offset = producer.instruction.instruction.arg1

        # Search current block and predecessors for XCALL+LLD pattern
        xcall_lld = _find_xcall_with_lld_in_predecessors(
            block_id=producer.block_id,
            stack_offset=stack_offset,
            ssa_func=ssa_func,
            max_depth=5  # Increased search depth for cross-block patterns
        )

        if xcall_lld:
            xcall_inst, lld_inst = xcall_lld
            return _format_xcall_expression(xcall_inst, formatter, ssa_func)

    # Pattern: LLD [sp+307] loads return value from stack
    # This is the standard return value slot after CALL/XCALL
    if producer.mnemonic == "LLD":
        # Look backwards in the same block for CALL/XCALL
        block_id = producer.block_id
        block_instructions = ssa_func.instructions.get(block_id, [])

        # Find the LLD instruction index
        lld_index = None
        for idx, inst in enumerate(block_instructions):
            if inst.address == producer.address:
                lld_index = idx
                break

        if lld_index is not None:
            # Look backwards for CALL/XCALL (should be immediately before or within a few instructions)
            for idx in range(lld_index - 1, max(0, lld_index - 5), -1):
                prev_inst = block_instructions[idx]
                if prev_inst.mnemonic in {"CALL", "XCALL"}:
                    return _format_xcall_expression(prev_inst, formatter, ssa_func)

    # NEW PHASE 8B.2: Trace through PHI nodes more thoroughly
    if producer.mnemonic == "PHI":
        # Try all PHI inputs, prioritize XCALL/CALL results
        for phi_input in producer.inputs:
            result = _trace_value_to_function_call(ssa_func, phi_input, formatter, max_depth - 1)
            if result:
                if debug:
                    logger.debug(f"  -> Traced function call through PHI: {result}")
                return result

    # NEW PHASE 8B.2: Follow SSA value across blocks to find XCALL
    # This handles cases where the value flows through multiple blocks
    if max_depth > 0:
        visited = set()
        to_visit = [(value, 0)]

        while to_visit:
            current_val, depth = to_visit.pop(0)

            if depth > max_depth or id(current_val) in visited:
                continue

            visited.add(id(current_val))

            if current_val.producer_inst:
                prod = current_val.producer_inst

                # Found XCALL/CALL?
                if prod.mnemonic in {"XCALL", "CALL"}:
                    return _format_xcall_expression(prod, formatter, ssa_func)

                # Follow LLD backward to XCALL in same block
                if prod.mnemonic == "LLD":
                    block_instructions = ssa_func.instructions.get(prod.block_id, [])
                    lld_idx = None
                    for idx, inst in enumerate(block_instructions):
                        if inst.address == prod.address:
                            lld_idx = idx
                            break

                    if lld_idx is not None:
                        for idx in range(lld_idx - 1, max(0, lld_idx - 5), -1):
                            prev_inst = block_instructions[idx]
                            if prev_inst.mnemonic in {"CALL", "XCALL"}:
                                return _format_xcall_expression(prev_inst, formatter, ssa_func)

                # Follow SSA inputs
                if hasattr(prod, 'inputs') and prod.inputs:
                    for inp in prod.inputs:
                        to_visit.append((inp, depth + 1))

    return None


def _find_xcall_with_lld_in_predecessors(
    block_id: int,
    stack_offset: Optional[int],
    ssa_func: SSAFunction,
    max_depth: int = 3,
    visited: Optional[Set[int]] = None
) -> Optional[tuple]:
    """
    Search for XCALL+LLD pattern in current block and predecessors.

    This function searches for the pattern where a function call (XCALL/CALL) is followed
    by an LLD instruction that loads the return value from the stack. This pattern often
    spans multiple blocks in the Vietcong compiler output.

    Pattern to detect:
        XCALL/CALL ...         # Function call
        LLD [sp+offset]        # Load return value (within 1-3 instructions)

    The cross-block pattern:
        Block N:
            XCALL SC_ggi       # Call function
            LLD [sp+419]       # Load return value
            JMP Block N+1
        Block N+1:
            LCP [sp+419]       # Reload value from stack
            EQU                # Use in comparison

    Args:
        block_id: Current block ID to search
        stack_offset: Expected stack offset for LLD (if known), or None to accept any
        ssa_func: SSA function containing the blocks
        max_depth: Maximum recursion depth for predecessor search (default: 3)
        visited: Set of visited block IDs to prevent cycles

    Returns:
        Tuple of (xcall_inst, lld_inst) if pattern found, None otherwise
    """
    import sys
    import os

    debug = os.environ.get('VCDECOMP_SWITCH_DEBUG') == '1'

    if visited is None:
        visited = set()

    # Prevent cycles
    if block_id in visited or max_depth <= 0:
        return None
    visited.add(block_id)

    # Get instructions for current block
    if block_id not in ssa_func.instructions:
        return None

    block_instructions = ssa_func.instructions[block_id]

    # Search current block for XCALL+LLD pattern
    for i, inst in enumerate(block_instructions):
        if inst.mnemonic in {"CALL", "XCALL"}:
            # Look ahead 1-3 instructions for LLD
            for j in range(i + 1, min(i + 4, len(block_instructions))):
                next_inst = block_instructions[j]
                if next_inst.mnemonic == "LLD":
                    # Found XCALL+LLD pattern
                    if stack_offset is None:
                        # Accept any LLD after XCALL
                        if debug:
                            print(f"[XCALL] Found XCALL+LLD in block {block_id}: "
                                  f"XCALL@{inst.address}, LLD@{next_inst.address}",
                                  file=sys.stderr)
                        return (inst, next_inst)
                    else:
                        # Verify LLD loads from expected stack offset
                        if next_inst.instruction and next_inst.instruction.instruction:
                            lld_offset = next_inst.instruction.instruction.arg1
                            if lld_offset == stack_offset:
                                if debug:
                                    print(f"[XCALL] Found XCALL+LLD in block {block_id}: "
                                          f"XCALL@{inst.address}, LLD@{next_inst.address}, offset={stack_offset}",
                                          file=sys.stderr)
                                return (inst, next_inst)

    # Pattern not found in current block, search predecessors
    if hasattr(ssa_func, 'cfg') and ssa_func.cfg:
        cfg = ssa_func.cfg
        # Get predecessors of current block from the CFG
        if block_id in cfg.blocks:
            current_block = cfg.blocks[block_id]
            predecessors = list(current_block.predecessors)

            # Recursively search predecessors
            for pred_id in predecessors:
                result = _find_xcall_with_lld_in_predecessors(
                    pred_id, stack_offset, ssa_func, max_depth - 1, visited
                )
                if result:
                    return result

    return None


def _format_xcall_expression(xcall_inst, formatter: "ExpressionFormatter", ssa_func: SSAFunction) -> Optional[str]:
    """
    PHASE 8B.2: Format XCALL/CALL instruction as C function call expression.

    Extracts function name and arguments from XCALL instruction to produce
    a readable expression like "SC_ggi(GVAR_GAMEPHASE)" or "SC_NOD_Get(100, 1)".

    Args:
        xcall_inst: XCALL or CALL SSA instruction
        formatter: Expression formatter for rendering arguments
        ssa_func: SSA function containing the instruction

    Returns:
        Formatted function call string, or None if formatting fails
    """
    import sys
    import os

    debug = os.environ.get('VCDECOMP_SWITCH_DEBUG') == '1'

    try:
        # Try using the formatter's _format_call method if available
        if hasattr(formatter, '_format_call'):
            call_expr = formatter._format_call(xcall_inst)
            # Extract just the call part (remove semicolon if present)
            if call_expr.endswith(";"):
                call_expr = call_expr[:-1].strip()
            # Strip off any "t###_ret = " or similar assignment prefix
            # We only want the function call expression, not the assignment
            if " = " in call_expr:
                call_expr = call_expr.split(" = ", 1)[1]
            if debug:
                logger.debug(f"  -> Formatted XCALL via _format_call: {call_expr}")
            return call_expr

        # Fallback: Manual formatting
        # Get function name from XCALL instruction
        func_name = None
        if xcall_inst.mnemonic == "XCALL":
            # External function call - should have XFN index
            if hasattr(xcall_inst, 'xfn_index') and xcall_inst.xfn_index is not None:
                # Resolve XFN name from script
                if ssa_func.scr and hasattr(ssa_func.scr, 'xfn_table'):
                    xfn_table = ssa_func.scr.xfn_table
                    if xcall_inst.xfn_index < len(xfn_table):
                        func_name = xfn_table[xcall_inst.xfn_index].name
        elif xcall_inst.mnemonic == "CALL":
            # Internal function call
            func_name = f"func_{xcall_inst.instruction.instruction.arg1}"

        if not func_name:
            # Last resort: generic name
            func_name = f"func_{xcall_inst.address}"

        # Extract arguments from instruction inputs
        args = []
        if hasattr(xcall_inst, 'inputs') and xcall_inst.inputs:
            for arg_value in xcall_inst.inputs:
                arg_str = _format_argument(arg_value, formatter, ssa_func)
                args.append(arg_str)

        result = f"{func_name}({', '.join(args)})"
        if debug:
            logger.debug(f"  -> Formatted XCALL manually: {result}")
        return result

    except Exception as e:
        # Fallback on error
        import sys
        import os
        debug = os.environ.get('VCDECOMP_SWITCH_DEBUG') == '1'
        if debug:
            print(f"[XCALL] _format_xcall_expression failed: {e}", file=sys.stderr)

        # Return generic function call
        if xcall_inst.mnemonic == "XCALL":
            return f"func_{xcall_inst.address}(...)"
        else:
            return f"func_{xcall_inst.address}(...)"


def _format_argument(arg_value, formatter: "ExpressionFormatter", ssa_func: SSAFunction) -> str:
    """
    PHASE 8B.2: Format a single function argument value.

    Attempts to resolve constants to their named equivalents (e.g., GVAR_GAMEPHASE instead of 500).

    Args:
        arg_value: SSA value representing the argument
        formatter: Expression formatter
        ssa_func: SSA function containing the value

    Returns:
        Formatted argument string
    """
    # Check if it's a constant value from data segment
    if hasattr(arg_value, 'alias') and arg_value.alias and arg_value.alias.startswith("data_"):
        try:
            offset = int(arg_value.alias[5:])
            # Try to get the constant value
            if ssa_func.scr and ssa_func.scr.data_segment:
                const_value = ssa_func.scr.data_segment.get_dword(offset * 4)

                # Check if this constant has a known name (like GVAR_GAMEPHASE)
                # This would require a constant name database - for now just return the value
                return str(const_value)
        except (ValueError, AttributeError):
            pass

    # Try to render using formatter
    if hasattr(formatter, 'render_value'):
        return formatter.render_value(arg_value)

    # Fallback: use alias or name
    if hasattr(arg_value, 'alias') and arg_value.alias:
        return arg_value.alias
    if hasattr(arg_value, 'name'):
        return arg_value.name

    return "?"


def _trace_value_to_global(
    value,
    formatter: ExpressionFormatter,
    ssa_func: Optional[SSAFunction] = None,
    visited: Optional[Set[int]] = None
) -> Optional[str]:
    """
    Trace an SSA value back to its global variable source.

    If value comes from GCP/GLD (load from global), return the global variable name.
    Otherwise return None.

    Pattern:
        GCP/GLD offset -> produces value with alias local_X
        We want to return the global name for that offset instead.

    Also handles indirection through stack:
        GCP offset -> stack -> LCP -> value
        In this case, LCP loads from stack where GCP stored the value.

    Args:
        value: SSA value to trace
        formatter: Expression formatter (must have _global_names attribute)
        ssa_func: SSA function containing the value (optional, enables cross-block tracing)
        visited: Set of visited value IDs to prevent infinite recursion

    Returns:
        Global variable name if found, None otherwise
    """
    if not value:
        return None

    # Prevent infinite recursion
    if visited is None:
        visited = set()
    if id(value) in visited:
        return None
    visited.add(id(value))

    # Check if value itself is a data_X alias (direct global reference)
    if value.alias and value.alias.startswith("data_"):
        try:
            offset = int(value.alias[5:])
            if hasattr(formatter, '_global_names'):
                global_name = formatter._global_names.get(offset)
                if global_name:
                    return global_name
        except ValueError:
            pass

    if not value.producer_inst:
        return None

    producer = value.producer_inst

    # Check if producer is GCP or GLD (global load)
    if producer.mnemonic in {"GCP", "GLD"}:
        if producer.instruction and producer.instruction.instruction:
            dword_offset = producer.instruction.instruction.arg1
            # Check if formatter has global name for this offset
            if hasattr(formatter, '_global_names'):
                global_name = formatter._global_names.get(dword_offset)
                if global_name:
                    return global_name

    # CRITICAL FIX: Check if producer is LCP (load from stack)
    # Pattern: GCP -> stack push -> LCP -> value
    # In this case, we need to trace through PHI or find the value's source
    elif producer.mnemonic == "LCP":
        # LCP loads from stack - the value might have been stored by GCP earlier

        # Pattern 1: Check if this LCP value has phi_sources
        if value.phi_sources:
            for _, phi_source in value.phi_sources:
                global_name = _trace_value_to_global(phi_source, formatter, ssa_func, visited)
                if global_name:
                    return global_name

        # Pattern 2: Use cross-block tracing to find the ultimate producer
        # This handles cases where the value flows through multiple blocks
        if ssa_func:
            ultimate_producer = _follow_ssa_value_across_blocks(value, ssa_func, visited.copy(), max_depth=10)
            if ultimate_producer and ultimate_producer.mnemonic in {"GCP", "GLD"}:
                if ultimate_producer.instruction and ultimate_producer.instruction.instruction:
                    dword_offset = ultimate_producer.instruction.instruction.arg1
                    if hasattr(formatter, '_global_names'):
                        global_name = formatter._global_names.get(dword_offset)
                        if global_name:
                            logger.debug(f"_trace_value_to_global: Found global via cross-block trace: {global_name}")
                            return global_name

        # Pattern 3: Search predecessors for GCP loading to same stack offset
        if ssa_func and producer.instruction and producer.instruction.instruction:
            stack_offset = producer.instruction.instruction.arg1
            global_name = _find_gcp_for_stack_offset(
                producer.block_id, stack_offset, ssa_func, formatter, set(), max_depth=10
            )
            if global_name:
                logger.debug(f"_trace_value_to_global: Found global via GCP search: {global_name}")
                return global_name

    # Check if producer is DCP (load from memory via pointer)
    # Pattern: GADR global -> DCP -> value
    # This happens when global is loaded via pointer dereference
    elif producer.mnemonic == "DCP":
        if len(producer.inputs) > 0:
            addr_value = producer.inputs[0]
            # Trace the address - might be GADR
            if addr_value.producer_inst and addr_value.producer_inst.mnemonic == "GADR":
                if addr_value.producer_inst.instruction and addr_value.producer_inst.instruction.instruction:
                    dword_offset = addr_value.producer_inst.instruction.instruction.arg1
                    if hasattr(formatter, '_global_names'):
                        global_name = formatter._global_names.get(dword_offset)
                        if global_name:
                            return global_name

    # Check if producer is PHI (merge point) - trace through inputs
    elif producer.mnemonic == "PHI":
        # Try to find global source from any PHI input
        for inp in producer.inputs:
            global_name = _trace_value_to_global(inp, formatter, ssa_func, visited)
            if global_name:
                return global_name

    return None


def _find_gcp_for_stack_offset(
    block_id: int,
    stack_offset: int,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    visited: Optional[Set[int]] = None,
    max_depth: int = 10
) -> Optional[str]:
    """
    Search predecessor blocks for a GCP instruction that loaded a value
    which was then stored to the given stack offset.

    Pattern:
        Block N: GCP data[X] -> value
                 (value flows through CFG, gets stored to stack)
        Block M: LCP [sp+offset] -> our_value

    We need to find the GCP in Block N that is the ultimate source.

    Args:
        block_id: Current block ID to search from
        stack_offset: Stack offset that LCP loads from
        ssa_func: SSA function containing the blocks
        formatter: Expression formatter (must have _global_names attribute)
        visited: Set of visited block IDs to prevent cycles
        max_depth: Maximum recursion depth for predecessor search

    Returns:
        Global variable name if found, None otherwise
    """
    if visited is None:
        visited = set()
    if block_id in visited or max_depth <= 0:
        return None
    visited.add(block_id)

    # Get SSA instructions for this block
    if not hasattr(ssa_func, 'instructions') or block_id not in ssa_func.instructions:
        return None

    block_instructions = ssa_func.instructions[block_id]

    # Search for GCP/GLD in this block
    for inst in block_instructions:
        if inst.mnemonic in {"GCP", "GLD"}:
            if inst.instruction and inst.instruction.instruction:
                dword_offset = inst.instruction.instruction.arg1
                if hasattr(formatter, '_global_names'):
                    global_name = formatter._global_names.get(dword_offset)
                    if global_name:
                        return global_name

    # Search predecessors
    if hasattr(ssa_func, 'cfg') and ssa_func.cfg and block_id in ssa_func.cfg.blocks:
        current_block = ssa_func.cfg.blocks[block_id]
        for pred_id in current_block.predecessors:
            result = _find_gcp_for_stack_offset(
                pred_id, stack_offset, ssa_func, formatter, visited, max_depth - 1
            )
            if result:
                return result

    return None


def _trace_value_to_parameter_field(
    value,
    formatter: ExpressionFormatter,
    ssa_func: SSAFunction,
    visited: Optional[Set[int]] = None
) -> Optional[str]:
    """
    Trace an SSA value back to a parameter field access pattern.

    Pattern to detect (Pilot script):
        LADR [sp-4]   -> Load address of parameter (info)
        DADR offset   -> Add field offset (0 for ->message, 4 for ->param1, etc.)
        DCP           -> Dereference to get field value

    This is different from _trace_value_to_parameter which handles direct LCP loads.

    Args:
        value: SSA value to trace
        formatter: Expression formatter
        ssa_func: SSA function containing the value
        visited: Set of visited value IDs to prevent infinite recursion

    Returns:
        Parameter field access string (e.g., "info->message") if found, None otherwise
    """
    if not value:
        return None

    # Prevent infinite recursion
    if visited is None:
        visited = set()
    if id(value) in visited:
        return None
    visited.add(id(value))

    if not value.producer_inst:
        logger.debug(f"_trace_value_to_parameter_field: value {value.name} has no producer")
        return None

    producer = value.producer_inst
    logger.debug(f"_trace_value_to_parameter_field: value {value.name}, producer {producer.mnemonic} at {producer.address}")

    # Pattern: DCP (dereference pointer)
    if producer.mnemonic == "DCP":
        if len(producer.inputs) == 0:
            logger.debug(f"  DCP has no inputs")
            return None

        # The input to DCP is the pointer (result of LADR+DADR)
        ptr_value = producer.inputs[0]
        logger.debug(f"  DCP input: {ptr_value.name} (alias: {ptr_value.alias})")

        # CRITICAL FIX: Use multi-block tracing to find the producer
        # The ptr_value might come from a different block via PHI or flow
        ptr_producer = _follow_ssa_value_across_blocks(ptr_value, ssa_func)

        if not ptr_producer:
            logger.debug(f"  DCP input has no producer - even across blocks")
            return None

        logger.debug(f"  DCP input producer: {ptr_producer.mnemonic} at {ptr_producer.address}")

        # Pattern: DADR (add offset to address)
        if ptr_producer.mnemonic == "DADR":
            if len(ptr_producer.inputs) == 0:
                logger.debug(f"    DADR has no inputs")
                return None

            # Get the field offset from DADR instruction
            field_offset = None
            if ptr_producer.instruction and ptr_producer.instruction.instruction:
                field_offset = ptr_producer.instruction.instruction.arg1
                logger.debug(f"    DADR field offset: {field_offset}")

            # The input to DADR is the base address (result of LADR)
            base_addr_value = ptr_producer.inputs[0]
            logger.debug(f"    DADR input: {base_addr_value.name} (alias: {base_addr_value.alias})")

            # CRITICAL FIX: Use multi-block tracing to find the base producer
            base_producer = _follow_ssa_value_across_blocks(base_addr_value, ssa_func)

            if not base_producer:
                logger.debug(f"    DADR input has no producer - even across blocks")
                return None

            logger.debug(f"    DADR input producer: {base_producer.mnemonic} at {base_producer.address}")

            # Pattern: LADR [sp-4] (load address of parameter)
            if base_producer.mnemonic == "LADR":
                if base_producer.instruction and base_producer.instruction.instruction:
                    stack_offset = base_producer.instruction.instruction.arg1
                    logger.debug(f"      LADR stack offset: {stack_offset}")

                    # [sp-4] is the first parameter in VC compiler convention
                    # Negative offsets are function parameters
                    if stack_offset < 0:
                        # Map field offsets to field names for s_SC_L_info struct
                        # typedef struct{ dword message,param1,param2,param3; float elapsed_time; float next_exe_time; c_Vector3 param4; }s_SC_L_info;
                        field_map = {
                            0: "message",       # offset 0
                            4: "param1",        # offset 4
                            8: "param2",        # offset 8
                            12: "param3",       # offset 12
                            16: "elapsed_time", # offset 16
                            20: "next_exe_time",# offset 20
                            # param4 (c_Vector3) starts at offset 24
                        }

                        field_name = field_map.get(field_offset)
                        if field_name:
                            # Default parameter name
                            param_name = "info"

                            # Try to get parameter name from function signature
                            if hasattr(formatter, '_func_signature') and formatter._func_signature:
                                func_sig = formatter._func_signature
                                # For level scripts, first parameter is typically s_SC_L_info
                                # For network scripts, first parameter is s_SC_NET_info
                                if func_sig.param_types and len(func_sig.param_types) > 0:
                                    param_type = func_sig.param_types[0]
                                    # Extract parameter name from "s_SC_L_info *info"
                                    parts = param_type.split()
                                    if parts:
                                        param_name = parts[-1].rstrip('*')

                            result = f"{param_name}->{field_name}"
                            logger.debug(f"      SUCCESS: Detected parameter field access: {result}")
                            return result
                        else:
                            logger.debug(f"      Field offset {field_offset} not in field_map")

    # Try to trace through PHI nodes
    if producer.mnemonic == "PHI":
        for inp in producer.inputs:
            result = _trace_value_to_parameter_field(inp, formatter, ssa_func, visited)
            if result:
                return result

    return None


def _trace_value_to_parameter(value, formatter: ExpressionFormatter, ssa_func: SSAFunction, max_depth: int = 5) -> Optional[str]:
    """
    PHASE 8B.3: Trace an SSA value back to its parameter source.

    Enhanced to handle negative stack offsets (function parameters).

    If value comes from LCP (load from stack parameter), return the parameter name.
    Otherwise return None.

    Pattern:
        LCP [sp+offset] -> produces value (positive offset: local variable or param)
        LCP [sp-offset] -> produces value (negative offset: function parameter)

    For ScriptMain(s_SC_NET_info *info):
        LCP [sp+306] = info->message (offset 0 in s_SC_NET_info)
        LCP [sp+310] = info->param1  (offset 4 in s_SC_NET_info)
        etc.

    For GetAttackingSide(dword main_phase, dword attacking_side):
        LCP [sp+4]  = main_phase (first parameter)
        LCP [sp+8]  = attacking_side (second parameter)
        LCP [sp-4]  = first parameter (alternative calling convention)
        LCP [sp-8]  = second parameter (alternative calling convention)

    Args:
        value: SSA value to trace
        formatter: Expression formatter (may have _func_signature and _param_names)
        ssa_func: SSA function containing the value
        max_depth: Maximum recursion depth for tracing (default: 5)

    Returns:
        Parameter name string (e.g., "param_1", "attacking_side") if found, None otherwise
    """
    if not value or max_depth <= 0:
        return None

    if not value.producer_inst:
        return None

    producer = value.producer_inst

    # Check if producer is LCP (load from stack/parameter)
    if producer.mnemonic == "LCP":
        stack_offset = _extract_stack_offset(producer)

        if stack_offset is not None:
            # PHASE 8B.3: Handle both positive and negative stack offsets
            # Negative offsets are function parameters in some calling conventions
            # Positive offsets can be local variables or parameters depending on context

            # Heuristic: Detect s_SC_L_info or s_SC_NET_info parameter struct fields
            # Different scripts use different stack base offsets:
            # - LEVEL.SCR (ScriptMain): base at [sp+87]
            # - TDM.SCR (ScriptMain): base at [sp+306]

            # Try s_SC_L_info pattern (LEVEL.SCR, base at sp+87)
            if 87 <= stack_offset <= 107:  # 87 + 20 dwords (struct size ~80 bytes)
                field_offset = (stack_offset - 87) * 4  # Convert dword index to byte offset
                field_map = {
                    0: "message",       # offset 0
                    4: "param1",        # offset 4
                    8: "param2",        # offset 8
                    12: "param3",       # offset 12
                    16: "elapsed_time", # offset 16
                    20: "next_exe_time",# offset 20
                    # param4 (c_Vector3) starts at offset 24
                }
                field_name = field_map.get(field_offset)
                param_name = "info"
                if field_name:
                    logger.debug(f"Detected s_SC_L_info field: info->{field_name} at stack offset {stack_offset}")
                    return f"{param_name}->{field_name}"

            # Try s_SC_NET_info pattern (TDM.SCR, base at sp+306)
            field_map = {
                306: "message",      # offset 0
                310: "param1",       # offset 4
                314: "param2",       # offset 8
                318: "param3",       # offset 12
                322: "elapsed_time", # offset 16
                326: "fval1",        # offset 20
            }

            field_name = field_map.get(stack_offset)
            if field_name:
                # Default parameter name for ScriptMain
                param_name = "info"

                # Try to get better parameter name from function signature
                if hasattr(formatter, '_func_signature') and formatter._func_signature:
                    func_sig = formatter._func_signature
                    if func_sig.param_types:
                        # Check if any parameter mentions s_SC_NET_info
                        for param_type in func_sig.param_types:
                            if 's_SC_NET_info' in param_type:
                                # Extract parameter name from "s_SC_NET_info *info"
                                parts = param_type.split()
                                if parts:
                                    param_name = parts[-1]
                                break

                return f"{param_name}->{field_name}"

            # PHASE 8B.3: Handle negative offsets (parameters)
            if stack_offset < 0:
                # Negative offset indicates function parameter
                # Map to param_N based on absolute offset
                # Typically parameters are at -4, -8, -12, etc. (4-byte aligned)
                param_index = (abs(stack_offset) // 4) - 1  # -4 → param_0, -8 → param_1
                if param_index >= 0:
                    return f"param_{param_index}"

            # PHASE 8B.3: Handle positive offsets
            # In VC compiler, positive stack offsets are LOCAL VARIABLES, not parameters.
            # Parameters are ONLY at negative offsets (sp-4, sp-8, etc.)
            # The compiler allocates locals with ASP, then accesses them with LCP [sp+N]
            #
            # DISABLED: The previous heuristic (stack_offset < 20 → param_N) was WRONG
            # and caused false positives like LCP [sp+11] being treated as param_1.
            #
            # Only trace backward for values that might have been STORED from parameters:
            if 0 < stack_offset < 100:  # Local variable range, might be param copy
                # Trace backward to find if this local was assigned from a parameter
                # Pattern: LCP [sp-4] → (store) → [sp+41] → LCP [sp+41]
                param_source = _trace_stack_slot_to_parameter(producer, ssa_func, max_depth=max_depth)
                if param_source:
                    return param_source

            # Fallback: check if this is a simple parameter load
            # Try to use parameter name mapping if available
            if hasattr(formatter, '_param_names'):
                param_name = formatter._param_names.get(stack_offset)
                if param_name:
                    return param_name

    # PHASE 8B.3: Trace through PHI nodes if producer is PHI
    if producer.mnemonic == "PHI" and max_depth > 0:
        for phi_input in producer.inputs:
            result = _trace_value_to_parameter(phi_input, formatter, ssa_func, max_depth - 1)
            if result:
                return result

    return None


def _extract_stack_offset(lcp_inst) -> Optional[int]:
    """
    PHASE 8B.3: Extract numeric stack offset from LCP instruction.

    Handles both positive and negative offsets.

    Args:
        lcp_inst: LCP instruction

    Returns:
        int: Stack offset (positive or negative)
        None: If offset cannot be determined
    """
    if not lcp_inst or lcp_inst.mnemonic != "LCP":
        return None

    # Try to extract from instruction argument
    if hasattr(lcp_inst, 'instruction') and lcp_inst.instruction:
        if hasattr(lcp_inst.instruction, 'instruction') and lcp_inst.instruction.instruction:
            # Get arg1 which contains the stack offset
            offset = lcp_inst.instruction.instruction.arg1

            # Handle signed integers (Python's ctypes or similar)
            # If offset is > 0x7FFFFFFF, it's a negative number in two's complement
            if offset > 0x7FFFFFFF:
                # Convert to negative
                offset = offset - 0x100000000

            return offset

    # Alternative: check if offset is stored directly
    if hasattr(lcp_inst, 'offset'):
        return lcp_inst.offset

    # Try examining inputs for constant offset
    if hasattr(lcp_inst, 'inputs') and lcp_inst.inputs and len(lcp_inst.inputs) > 0:
        offset_val = lcp_inst.inputs[0]
        if hasattr(offset_val, 'constant'):
            return offset_val.constant

    return None


def _trace_stack_slot_to_parameter(
    lcp_inst,
    ssa_func: SSAFunction,
    max_depth: int = 10
) -> Optional[str]:
    """
    Trace a stack slot back to parameter source.

    Pattern: LCP [sp-4] → (store via SSA) → [sp+41] → LCP [sp+41]

    This handles the case where the compiler copies a parameter from its standard
    location (negative offset) to a local stack slot (positive offset). The local
    slot is then used throughout the function.

    Example bytecode:
        534: LCP [sp-4]       ; Load first parameter (attacking_side)
        535: JMP label_0537   ; Jump to first test
        ...
        537: LCP [sp+41]      ; Reload from local stack slot
        539: EQU (with 0)     ; Test case 0

    Args:
        lcp_inst: LCP instruction loading from stack
        ssa_func: SSA function containing the instruction
        max_depth: Maximum search depth (default: 10)

    Returns:
        Parameter name string (e.g., "param_0") if traced to parameter, None otherwise
    """
    if not lcp_inst or max_depth <= 0:
        return None

    import sys
    import os
    debug = os.environ.get('VCDECOMP_SWITCH_DEBUG') == '1'

    # Get the stack offset this LCP loads from
    stack_offset = _extract_stack_offset(lcp_inst)
    if stack_offset is None:
        return None

    if debug:
        logger.debug(f"  _trace_stack_slot_to_parameter: Tracing LCP [sp+{stack_offset}] at {lcp_inst.address}")

    # Search backwards in the same block and predecessors for an LCP with negative offset
    # that might have been stored to this stack location
    visited_blocks = set()
    to_visit = [(lcp_inst.block_id, max_depth)]

    while to_visit:
        block_id, depth = to_visit.pop(0)

        if block_id in visited_blocks or depth <= 0:
            continue
        visited_blocks.add(block_id)

        if block_id not in ssa_func.instructions:
            continue

        block_instructions = ssa_func.instructions[block_id]

        # Search for LCP with negative offset (parameter load)
        # The pattern is typically:
        # 1. LCP [sp-4]    <- parameter load
        # 2. (implicit store to stack)
        # 3. LCP [sp+41]   <- our current instruction

        for inst in block_instructions:
            if inst.mnemonic == "LCP":
                inst_offset = _extract_stack_offset(inst)
                if inst_offset is not None and inst_offset < 0:
                    # Found a parameter load! Check if it could be the source
                    # Calculate parameter index
                    param_index = (abs(inst_offset) // 4) - 1  # -4 → param_0, -8 → param_1

                    if param_index >= 0:
                        param_name = f"param_{param_index}"
                        if debug:
                            logger.debug(f"    -> Found parameter load: LCP [sp{inst_offset}] = {param_name} at {inst.address}")
                        return param_name

        # Also check for SSA value flow: trace the producer of the value
        # stored at this stack location
        # This is more robust than just looking for LCP instructions
        for inst in block_instructions:
            # Look for instructions that might have stored to our stack offset
            # In SSA form, this would be represented by the value flow
            if hasattr(inst, 'outputs') and inst.outputs:
                for output in inst.outputs:
                    # Check if this output flows to our LCP location
                    # We need to check if this value is later loaded by LCP [sp+stack_offset]
                    if inst.mnemonic == "LCP":
                        inst_offset = _extract_stack_offset(inst)
                        if inst_offset is not None and inst_offset < 0:
                            # This is a parameter load - it might flow to our location
                            param_index = (abs(inst_offset) // 4) - 1
                            if param_index >= 0:
                                # Try to trace if this value flows to the high-offset location
                                # For now, use a simple heuristic: first param load in predecessor
                                param_name = f"param_{param_index}"
                                if debug:
                                    logger.debug(f"    -> Found parameter via SSA flow: {param_name}")
                                return param_name

        # Explore predecessors
        if hasattr(ssa_func, 'cfg') and ssa_func.cfg and block_id in ssa_func.cfg.blocks:
            current_block = ssa_func.cfg.blocks[block_id]
            for pred_id in current_block.predecessors:
                if pred_id not in visited_blocks:
                    to_visit.append((pred_id, depth - 1))

    if debug:
        logger.debug(f"  _trace_stack_slot_to_parameter: No parameter source found for LCP [sp+{stack_offset}]")

    return None


def _find_switch_variable_from_nearby_gcp(
    ssa_func: SSAFunction,
    current_block_id: int,
    var_value,
    formatter: ExpressionFormatter,
    func_block_ids: Set[int]
) -> Optional[str]:
    """
    Heuristic to find switch variable when normal tracing fails.

    Pattern: Compiler generates code like:
        Block 1: GCP data[X]  # Load global variable
                 JMP Block 2
        Block 2: LCP [sp+0]   # Load from stack (but value didn't propagate through CFG)
                 ...
                 EQU          # Compare in switch

    We look for GCP instructions in SSA blocks (which preserve correct mnemonics)
    to find the first global variable load - this is likely the switch variable.

    Args:
        ssa_func: SSA function to search
        current_block_id: Current block ID (unused but kept for API compatibility)
        var_value: Variable value being traced (unused but kept for API compatibility)
        formatter: Expression formatter (must have _global_names attribute)
        func_block_ids: Set of block IDs in the function to search

    Returns:
        Global variable name if found, None otherwise
    """
    import sys

    # Search through SSA instructions (which have correct mnemonics)
    ssa_blocks = ssa_func.instructions  # Dict[block_id, List[SSAInstruction]]

    # Find the FIRST (earliest) GCP/GLD instruction in the entire function
    # that loads a global variable - this is likely the switch variable
    gcp_candidates = []

    # Collect all GCP/GLD from all SSA blocks in function
    for block_id in func_block_ids:
        if block_id not in ssa_blocks:
            continue

        ssa_instrs = ssa_blocks[block_id]
        for ssa_instr in ssa_instrs:
            if ssa_instr.mnemonic in {'GCP', 'GLD'}:
                # Found a global load!
                # Get the dword offset from instruction
                if hasattr(ssa_instr, 'instruction') and hasattr(ssa_instr.instruction, 'instruction'):
                    dword_offset = ssa_instr.instruction.instruction.arg1

                    if hasattr(formatter, '_global_names'):
                        global_name = formatter._global_names.get(dword_offset)
                        if global_name:
                            # Record this as candidate with instruction address
                            gcp_candidates.append((ssa_instr.address, global_name, dword_offset))

    # If we found any GCP, use the FIRST one (earliest in function)
    if gcp_candidates:
        # Sort by instruction address (earliest first)
        gcp_candidates.sort(key=lambda x: x[0])
        # Return the first global variable name
        return gcp_candidates[0][1]

    return None


def trace_loop_bounds(ssa_func: SSAFunction) -> Dict[str, BoundInfo]:
    """
    Analyze loop patterns to extract array dimension bounds.

    Detects loop patterns like:
    - For loop: `for (i = 0; i < N; i++)` → bounds [0, N)
    - While loop with counter: track counter variable increments
    - Explicit bounds from comparison operations (ICL, ICLE, LES, LEQ, etc.)

    Extracts bounds from:
    - Loop condition comparisons: `i < 10` → max_bound = 10
    - Array access patterns: `arr[i]` where i bounded by loop
    - Constant offsets: `arr[i + 5]` → effective_max = loop_max + 5

    Args:
        ssa_func: SSA function to analyze

    Returns:
        Dict mapping variable name to BoundInfo with min/max/step/confidence
    """
    bounds: Dict[str, BoundInfo] = {}

    def _resolve_constant(value) -> Optional[int]:
        if value is None:
            return None
        if hasattr(value, 'constant_value') and value.constant_value is not None:
            return value.constant_value
        if value.alias and value.alias.isdigit():
            return int(value.alias)
        if value.alias and value.alias.startswith("data_"):
            try:
                offset_idx = int(value.alias[5:])
                if ssa_func.scr and ssa_func.scr.data_segment:
                    return ssa_func.scr.data_segment.get_dword(offset_idx * 4)
            except (ValueError, AttributeError):
                return None
        return None

    # Find all comparison instructions that might define loop bounds
    for block_id, ssa_instrs in ssa_func.instructions.items():
        for inst in ssa_instrs:
            # Look for comparison operations (LES, LEQ, GRE, GEQ, ICL, ICLE, etc.)
            if inst.mnemonic not in {"LES", "LEQ", "GRE", "GEQ", "ICL", "ICLE", "ULES", "ULEQ", "UGRE", "UGEQ"}:
                continue

            if len(inst.inputs) < 2:
                continue

            left_val = inst.inputs[0]
            right_val = inst.inputs[1]

            # Try to find pattern: variable < constant or constant > variable
            var_name = None
            bound_value = None
            confidence = 0.95  # High confidence for explicit constant bounds

            # Pattern 1: var < constant (or var <= constant)
            left_name = left_val.alias or left_val.name
            if left_name and not left_name.startswith("t") and ("_" not in left_name or left_name.startswith("local_")):
                # This looks like a loop counter variable (i, j, idx, etc.)
                # Try to extract bound from right side
                bound_value = _resolve_constant(right_val)
                if bound_value is not None:
                    var_name = left_name

            # Pattern 2: constant > var (or constant >= var)
            right_name = right_val.alias or right_val.name
            if not var_name and right_name and not right_name.startswith("t") and ("_" not in right_name or right_name.startswith("local_")):
                bound_value = _resolve_constant(left_val)
                if bound_value is not None:
                    var_name = right_name

            if var_name and bound_value is not None:
                # Adjust bound based on comparison type
                # LES (i < N) → max is N-1
                # LEQ (i <= N) → max is N
                max_bound = bound_value
                if inst.mnemonic in {"LES", "ICL", "ULES"}:
                    # Strictly less than - max index is bound-1
                    max_bound = bound_value - 1
                elif inst.mnemonic in {"LEQ", "ICLE", "ULEQ"}:
                    # Less than or equal - max index is bound
                    max_bound = bound_value
                elif inst.mnemonic in {"GRE", "UGRE"}:
                    # Greater than - this is a minimum bound
                    max_bound = bound_value + 1
                elif inst.mnemonic in {"GEQ", "UGEQ"}:
                    # Greater than or equal - this is a minimum bound
                    max_bound = bound_value

                # Sanity check: bounds should be reasonable for arrays
                if 0 <= max_bound <= 10000:
                    # Update bounds if better than existing
                    if var_name not in bounds or bounds[var_name].max_value < max_bound:
                        bounds[var_name] = BoundInfo(
                            min_value=0,  # Assume 0-based indexing (C standard)
                            max_value=max_bound,
                            step=1,  # Assume unit step unless evidence otherwise
                            confidence=confidence
                        )
                        logger.debug(f"Loop bound detected: {var_name} range [0, {max_bound}] from {inst.mnemonic}")

    # Look for increment patterns to detect step size
    for block_id, ssa_instrs in ssa_func.instructions.items():
        for inst in ssa_instrs:
            # Look for INC/DEC or ADD/SUB with constant
            if inst.mnemonic in {"INC", "IINC"}:
                # i++ pattern
                if inst.outputs and len(inst.outputs) > 0:
                    var_name = inst.outputs[0].alias or inst.outputs[0].name
                    if var_name in bounds:
                        bounds[var_name].step = 1
            elif inst.mnemonic in {"DEC", "IDEC"}:
                # i-- pattern (reverse loop)
                if inst.outputs and len(inst.outputs) > 0:
                    var_name = inst.outputs[0].alias or inst.outputs[0].name
                    if var_name in bounds:
                        bounds[var_name].step = -1
            elif inst.mnemonic in {"IADD", "ADD"} and len(inst.inputs) >= 2:
                # i += step pattern
                var_val = inst.inputs[0]
                step_val = inst.inputs[1]
                var_name = var_val.alias or var_val.name

                if var_name in bounds:
                    if hasattr(step_val, 'constant_value') and step_val.constant_value is not None:
                        bounds[var_name].step = step_val.constant_value
                    elif step_val.alias and step_val.alias.isdigit():
                        bounds[var_name].step = int(step_val.alias)

    logger.info(f"Traced loop bounds for {len(bounds)} variables: {list(bounds.keys())}")
    return bounds
