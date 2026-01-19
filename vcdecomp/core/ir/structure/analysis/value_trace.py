"""
Value tracing utilities for SSA analysis.

This module contains functions for tracing SSA values back to their sources,
including function calls, global variables, and function parameters.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set, Dict
import logging

from ...ssa import SSAFunction
from ...expr import ExpressionFormatter

logger = logging.getLogger(__name__)


def _follow_ssa_value_across_blocks(
    value,
    ssa_func: SSAFunction,
    seen_blocks: Optional[Set[int]] = None,
    max_depth: int = 5
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

        # Try each PHI input
        for phi_input in prod_inst.inputs:
            logger.debug(f"  _follow_ssa_value_across_blocks: Trying PHI input {phi_input.name}")
            result = _follow_ssa_value_across_blocks(
                phi_input, ssa_func, seen_blocks, max_depth - 1
            )
            if result:
                return result

    # No producer found through normal means
    logger.debug(f"  _follow_ssa_value_across_blocks: No producer found for {value.name}")
    return None


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
    max_depth: int = 5
) -> Optional[str]:
    """
    FÁZE 1.6: Trace a value back to its producer to check if it's a function call result.

    Pattern to detect:
    - XCALL/CALL instruction
    - Followed by LLD [sp+307] (load return value)
    - Value used in condition or assignment

    Args:
        ssa_func: SSA function containing the value
        value: SSA value to trace
        formatter: Expression formatter for rendering
        max_depth: Maximum recursion depth (default: 5)

    Returns:
        Function call expression (e.g., "SC_MP_EnumPlayers(...)") if found, None otherwise
    """
    if not value or max_depth <= 0:
        return None

    # DEBUG
    import sys
    # print(f"DEBUG _trace_value_to_function_call: value={value.name}, has_producer={value.producer_inst is not None}", file=sys.stderr)

    # Check if this value came from LLD instruction
    if not value.producer_inst:
        return None

    producer = value.producer_inst
    # print(f"DEBUG producer: mnemonic={producer.mnemonic}, addr={producer.address}", file=sys.stderr)

    # Pattern: LLD [sp+307] loads return value from stack
    # This is the standard return value slot after CALL/XCALL
    if producer.mnemonic == "LLD":
        # Check if LLD is loading from sp+307 (return value slot)
        if producer.instruction and producer.instruction.instruction:
            load_offset = producer.instruction.instruction.arg1
            # sp+307 is the return value slot (stack pointer + 307 * 4 bytes typically)
            # But we also need to check if there's a recent CALL/XCALL before this LLD

            # Look backwards in the same block for CALL/XCALL
            block_id = producer.block_id
            block_instructions = ssa_func.instructions.get(block_id, [])

            # Find the LLD instruction index
            lld_index = None
            for idx, inst in enumerate(block_instructions):
                if inst.address == producer.address:
                    lld_index = idx
                    break

            if lld_index is None:
                return None

            # Look backwards for CALL/XCALL (should be immediately before or within a few instructions)
            for idx in range(lld_index - 1, max(0, lld_index - 5), -1):
                prev_inst = block_instructions[idx]
                if prev_inst.mnemonic in {"CALL", "XCALL"}:
                    # Found the function call! Format it using the expression formatter
                    # The formatter already knows how to render CALL/XCALL with arguments
                    try:
                        from ...expr import format_instruction
                        call_expr = format_instruction(prev_inst, formatter)
                        # Extract just the call part (remove semicolon if present)
                        if call_expr.endswith(";"):
                            call_expr = call_expr[:-1].strip()
                        return call_expr
                    except:
                        # Fallback: just return a placeholder
                        if prev_inst.mnemonic == "XCALL":
                            return f"func_{prev_inst.address}(...)"
                        else:
                            return f"func_{prev_inst.address}(...)"

    # If not direct LLD, check if value came from PHI that might wrap LLD
    if producer.mnemonic == "PHI" and len(producer.inputs) == 1:
        # Single-input PHI, trace through it
        return _trace_value_to_function_call(ssa_func, producer.inputs[0], formatter, max_depth - 1)

    return None


def _trace_value_to_global(value, formatter: ExpressionFormatter, visited=None) -> Optional[str]:
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
        # Try to find the source through PHI sources
        if value.phi_sources:
            for _, phi_source in value.phi_sources:
                global_name = _trace_value_to_global(phi_source, formatter, visited)
                if global_name:
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
            global_name = _trace_value_to_global(inp, formatter, visited)
            if global_name:
                return global_name

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


def _trace_value_to_parameter(value, formatter: ExpressionFormatter, ssa_func: SSAFunction) -> Optional[str]:
    """
    Trace an SSA value back to its parameter source.

    If value comes from LCP (load from stack parameter), return the parameter field access.
    Otherwise return None.

    Pattern:
        LCP [sp+offset] -> produces value
        We want to return the parameter field access for that offset.

    For ScriptMain(s_SC_NET_info *info):
        LCP [sp+306] = info->message (offset 0 in s_SC_NET_info)
        LCP [sp+310] = info->param1  (offset 4 in s_SC_NET_info)
        etc.

    Args:
        value: SSA value to trace
        formatter: Expression formatter (may have _func_signature and _param_names)
        ssa_func: SSA function containing the value

    Returns:
        Parameter field access string (e.g., "info->message") if found, None otherwise
    """
    if not value:
        return None

    if not value.producer_inst:
        return None

    producer = value.producer_inst

    # Check if producer is LCP (load from stack/parameter)
    if producer.mnemonic == "LCP":
        if producer.instruction and producer.instruction.instruction:
            stack_offset = producer.instruction.instruction.arg1

            # Heuristic: if offset is in range 306-326, likely s_SC_NET_info parameter
            # This is a common pattern in VC scripts for ScriptMain function
            # Map common offsets seen in tdm.scr
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

            # Fallback: check if this is a simple parameter load
            # Parameters are typically at positive stack offsets in VC compiler
            # Try to use parameter name mapping if available
            if hasattr(formatter, '_param_names'):
                param_name = formatter._param_names.get(stack_offset)
                if param_name:
                    return param_name

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
            if left_name and not left_name.startswith("t") and "_" not in left_name:
                # This looks like a loop counter variable (i, j, idx, etc.)
                # Try to extract bound from right side
                if hasattr(right_val, 'constant_value') and right_val.constant_value is not None:
                    var_name = left_name
                    bound_value = right_val.constant_value
                elif right_val.alias and right_val.alias.isdigit():
                    var_name = left_name
                    bound_value = int(right_val.alias)

            # Pattern 2: constant > var (or constant >= var)
            right_name = right_val.alias or right_val.name
            if not var_name and right_name and not right_name.startswith("t") and "_" not in right_name:
                if hasattr(left_val, 'constant_value') and left_val.constant_value is not None:
                    var_name = right_name
                    bound_value = left_val.constant_value
                elif left_val.alias and left_val.alias.isdigit():
                    var_name = right_name
                    bound_value = int(left_val.alias)

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
