"""
Variable collection and declaration generation.

This module contains functions for collecting local variable declarations
from SSA function instructions and generating properly-typed declarations.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from ....disasm import opcodes
from ...ssa import SSAFunction


def _collect_local_variables(ssa_func: SSAFunction, func_block_ids: Set[int], formatter) -> List[str]:
    """
    Collect local variable declarations for a function.

    Returns list of declaration strings like "int i", "float local_2", etc.
    """
    from collections import defaultdict

    # Track variable names and their types
    var_types: Dict[str, str] = {}

    # P0.3: Track local arrays detected from usage patterns
    local_arrays: Dict[str, Tuple[str, int]] = {}  # var_name -> (element_type, size)

    def process_value(value, default_type="int"):
        """Process a value to extract variable names and types."""
        if not value:
            return

        var_name = value.alias or value.name
        if not var_name:
            return

        # Strip & prefix to get actual variable name
        is_addr_of = var_name.startswith("&")
        if is_addr_of:
            var_name = var_name[1:]

        # Only process local variables (local_X, i, j, etc.)
        # Skip parameters (param_X, info), globals (data_X, gVar), SSA temps (tX_X), and PHI values
        if var_name.startswith("param_") or var_name.startswith("data_") or var_name == "info":
            return
        if var_name.startswith("t") and "_" in var_name:  # Skip tX_X temps
            return
        if var_name.startswith("phi_"):  # Skip PHI nodes (SSA internals)
            return
        if var_name.startswith("gData") or var_name.startswith("gVar"):  # Skip globals
            return

        # Check if variable has semantic name (i, player_info, etc.)
        display_name = var_name
        if var_name.startswith("local_"):
            semantic_name = formatter._semantic_names.get(var_name)
            if semantic_name:
                display_name = semantic_name

        # Don't re-declare if we already have this variable
        if display_name in var_types:
            return

        # Determine type from instruction or value type
        var_type = default_type

        # Check if this is a structure variable (has field access)
        if var_name.startswith("local_"):
            # Check if formatter knows this is a struct
            struct_info = formatter._struct_ranges.get(var_name)
            if struct_info:
                # struct_info is a tuple like (start, end, 'struct_name')
                # Extract just the struct name
                if isinstance(struct_info, tuple) and len(struct_info) >= 3:
                    var_type = struct_info[2]
                else:
                    var_type = str(struct_info)
            else:
                # Infer from value type
                if value.value_type == opcodes.ResultType.FLOAT:
                    var_type = "float"
                elif value.value_type == opcodes.ResultType.DOUBLE:
                    var_type = "double"
                # Don't use void* unless we're sure it's a pointer
                # Most POINTER types in SSA are actually int addresses
                else:
                    var_type = default_type
        else:
            # Simple variables (i, j, etc.)
            if value.value_type == opcodes.ResultType.FLOAT:
                var_type = "float"
            elif value.value_type == opcodes.ResultType.DOUBLE:
                var_type = "double"
            else:
                var_type = default_type

        # Store variable type
        var_types[display_name] = var_type

    # P0.3: First pass - detect local arrays from usage patterns
    for block_id in func_block_ids:
        ssa_instrs = ssa_func.instructions.get(block_id, [])
        for inst in ssa_instrs:
            # Pattern 1: sprintf(&local_X, ...) → char array
            if inst.mnemonic == "XCALL" and inst.inputs:
                # Get function name from XFN table
                call_name = None
                if inst.instruction and inst.instruction.instruction:
                    xfn_idx = inst.instruction.instruction.arg1
                    xfn_entry = ssa_func.scr.get_xfn(xfn_idx) if ssa_func.scr else None
                    if xfn_entry:
                        full_name = xfn_entry.name
                        paren_idx = full_name.find("(")
                        call_name = full_name[:paren_idx] if paren_idx > 0 else full_name

                if call_name == "sprintf" and len(inst.inputs) >= 1:
                    # First argument is buffer
                    buffer_arg = inst.inputs[0]
                    buf_name = buffer_arg.alias or buffer_arg.name
                    if buf_name and buf_name.startswith("&local_"):
                        var_name = buf_name[1:]  # Strip &
                        local_arrays[var_name] = ("char", 32)  # Default buffer size

            # Pattern 2: SC_ZeroMem(&local_X, size) → byte array
            if inst.mnemonic == "XCALL" and inst.inputs and inst.mnemonic == "XCALL":
                # Get function name from XFN table
                call_name = None
                if inst.instruction and inst.instruction.instruction:
                    xfn_idx = inst.instruction.instruction.arg1
                    xfn_entry = ssa_func.scr.get_xfn(xfn_idx) if ssa_func.scr else None
                    if xfn_entry:
                        full_name = xfn_entry.name
                        paren_idx = full_name.find("(")
                        call_name = full_name[:paren_idx] if paren_idx > 0 else full_name

                if call_name and "ZeroMem" in call_name and len(inst.inputs) >= 2:
                    # First arg is buffer, second is size
                    buffer_arg = inst.inputs[0]
                    size_arg = inst.inputs[1]

                    buf_name = buffer_arg.alias or buffer_arg.name
                    # Skip globals
                    if buf_name and buf_name.startswith("&local_"):
                        var_name = buf_name[1:]  # Strip &
                        # Try to get constant size
                        size = 64  # Default
                        if hasattr(size_arg, 'constant_value'):
                            size = size_arg.constant_value
                        elif size_arg.producer_inst and size_arg.producer_inst.mnemonic in ["IPUSH", "PUSH"]:
                            # Size is a constant
                            if size_arg.producer_inst.instruction:
                                size = size_arg.producer_inst.instruction.instruction.arg1

                        # Infer element type from size
                        if size == 60 or size == 156:  # Known struct sizes
                            # This is likely a struct, keep as int for now
                            pass
                        elif size >= 8:
                            # Likely an array
                            element_type = "dword"
                            array_size = size // 4
                            local_arrays[var_name] = (element_type, array_size)

    # Process all instructions in function blocks
    for block_id in func_block_ids:
        ssa_instrs = ssa_func.instructions.get(block_id, [])
        for inst in ssa_instrs:
            # Check outputs (variables being assigned)
            for output in inst.outputs:
                process_value(output, default_type="int")

            # Check inputs (variables being read) - these might be address-of operations
            for inp in inst.inputs:
                process_value(inp, default_type="int")

    # P0.3: Generate declarations (arrays first, then regular variables)
    declarations = []

    # First, declare arrays
    for var_name in sorted(var_types.keys()):
        if var_name in local_arrays:
            element_type, array_size = local_arrays[var_name]
            declarations.append(f"{element_type} {var_name}[{array_size}]")

    # Then, declare regular variables (skip arrays)
    for var_name in sorted(var_types.keys()):
        if var_name not in local_arrays:
            var_type = var_types[var_name]
            declarations.append(f"{var_type} {var_name}")

    return declarations
