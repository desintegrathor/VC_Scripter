"""
Value tracing utilities for SSA analysis.

This module contains functions for tracing SSA values back to their sources,
including function calls, global variables, and function parameters.
"""

from __future__ import annotations

from typing import Optional, Set

from ...ssa import SSAFunction
from ...expr import ExpressionFormatter


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
