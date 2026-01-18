"""
Variable collection and declaration generation.

This module contains functions for collecting local variable declarations
from SSA function instructions and generating properly-typed declarations.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple, Optional
import logging

from ....disasm import opcodes
from ...ssa import SSAFunction

logger = logging.getLogger(__name__)


def result_type_to_c_type(result_type: opcodes.ResultType) -> Optional[str]:
    """
    Map ResultType enum values from opcodes.py to C type strings.

    Args:
        result_type: ResultType enum value from SSA value.value_type

    Returns:
        C type string (e.g., "float", "int", "double") or None if unmapped
    """
    mapping = {
        opcodes.ResultType.FLOAT: "float",
        opcodes.ResultType.INT: "int",
        opcodes.ResultType.DOUBLE: "double",
        opcodes.ResultType.CHAR: "char",
        opcodes.ResultType.SHORT: "short",
        opcodes.ResultType.UNKNOWN: None,  # Fallback to default_type
        opcodes.ResultType.VOID: None,  # Don't declare void types
        opcodes.ResultType.POINTER: None,  # Pointers need more context, use default
    }
    c_type = mapping.get(result_type)
    if c_type is None and result_type not in [opcodes.ResultType.UNKNOWN, opcodes.ResultType.VOID, opcodes.ResultType.POINTER]:
        logger.warning(f"Unmapped ResultType: {result_type}, using fallback")
    return c_type


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

    # FIX #5: Track struct types inferred from function calls
    # Maps variable name -> struct type (e.g., "local_5" -> "s_SC_P_getinfo")
    inferred_struct_types: Dict[str, str] = {}

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

        # FIX #5: First check if we inferred a struct type from function calls
        # Try both display_name and var_name since semantic names might differ
        if display_name in inferred_struct_types:
            var_type = inferred_struct_types[display_name]
        elif var_name in inferred_struct_types:
            var_type = inferred_struct_types[var_name]
        # FIX (07-02): Check SSA refined type from type inference BEFORE struct ranges
        # Type inference provides high-confidence opcode-based types (FADD→float, IADD→int)
        # This prevents low-confidence struct guesses from overriding concrete type evidence
        elif value.value_type != opcodes.ResultType.UNKNOWN:
            refined_type = result_type_to_c_type(value.value_type)
            if refined_type is not None:
                var_type = refined_type
            else:
                # Fallback path for unmapped types
                var_type = default_type
        # Check if this is a structure variable (has field access)
        elif var_name.startswith("local_"):
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
                var_type = default_type
        else:
            var_type = default_type

        # Store variable type
        var_types[display_name] = var_type

    # FIX #5: FIRST pass - infer struct types from function calls
    # This must run BEFORE array detection so array detection can use struct types
    from ....structures import infer_struct_from_function

    for block_id in func_block_ids:
        ssa_instrs = ssa_func.instructions.get(block_id, [])
        for inst in ssa_instrs:
            # Look for XCALL instructions (external function calls)
            if inst.mnemonic != "XCALL" or not inst.inputs:
                continue

            # Get function name from XFN table
            call_name = None
            if inst.instruction and inst.instruction.instruction:
                xfn_idx = inst.instruction.instruction.arg1
                xfn_entry = ssa_func.scr.get_xfn(xfn_idx) if ssa_func.scr else None
                if xfn_entry:
                    full_name = xfn_entry.name
                    paren_idx = full_name.find("(")
                    call_name = full_name[:paren_idx] if paren_idx > 0 else full_name

            if not call_name:
                continue

            # Check each argument to see if it's a struct pointer parameter
            for arg_idx, arg_value in enumerate(inst.inputs):
                # Infer struct type from function signature
                struct_type = infer_struct_from_function(call_name, arg_idx)
                if not struct_type:
                    continue

                # Extract variable name from &local_X or local_X
                var_name = arg_value.alias or arg_value.name
                if not var_name:
                    continue

                # Strip & prefix if present
                if var_name.startswith("&"):
                    var_name = var_name[1:]

                # Only process local variables
                if not var_name.startswith("local_"):
                    continue

                # Store the inferred struct type
                # Store using both local_X name AND semantic name if it exists
                inferred_struct_types[var_name] = struct_type

                # Also store for semantic name if it exists
                semantic_name = formatter._semantic_names.get(var_name)
                if semantic_name:
                    inferred_struct_types[semantic_name] = struct_type

    # FIX 1.3: New pass - detect arrays from indexed access patterns
    # Track variables used in array indexing (MUL with struct size)
    array_index_vars: Dict[str, Set[str]] = {}  # array_var -> {index_vars}
    array_max_indices: Dict[str, int] = {}  # array_var -> max_index_seen
    
    # Scan for array indexing patterns: ADD(base, MUL(index, element_size))
    for block_id in func_block_ids:
        ssa_instrs = ssa_func.instructions.get(block_id, [])
        for inst in ssa_instrs:
            # Look for ADD instructions (used in array indexing)
            if inst.mnemonic == "ADD" and len(inst.inputs) == 2:
                left = inst.inputs[0]
                right = inst.inputs[1]
                
                # Check if left is a base address (&local_X, &data_X)
                base_var = None
                if left.alias and left.alias.startswith("&"):
                    base_var = left.alias[1:]  # Strip &
                    # Only track local variables for array inference
                    if not base_var.startswith("local_"):
                        base_var = None
                
                if base_var and right.producer_inst:
                    # Check if right is MUL (index * element_size)
                    if right.producer_inst.mnemonic == "MUL" and len(right.producer_inst.inputs) == 2:
                        # Found array indexing pattern!
                        mul_left = right.producer_inst.inputs[0]
                        mul_right = right.producer_inst.inputs[1]
                        
                        # Extract index variable (usually left operand of MUL)
                        index_var = mul_left.alias or mul_left.name
                        if index_var:
                            if base_var not in array_index_vars:
                                array_index_vars[base_var] = set()
                            array_index_vars[base_var].add(index_var)
    
    # For each detected array, try to infer size from loop bounds
    from ...cfg import find_loops_in_function
    cfg = ssa_func.cfg
    
    # Get loops in this function (need entry block)
    entry_block = None
    for block_id in func_block_ids:
        block = cfg.blocks.get(block_id)
        if block and len(block.predecessors) == 0:
            entry_block = block_id
            break
    
    if entry_block is not None:
        func_loops = find_loops_in_function(cfg, func_block_ids, entry_block)
        
        # For each array, find loops that use its index variables
        for array_var, index_vars in array_index_vars.items():
            max_bound = 0
            
            # Search loops for bounds on index variables
            for loop in func_loops:
                for block_id in loop.body:
                    ssa_block = ssa_func.instructions.get(block_id, [])
                    for inst in ssa_block:
                        # Look for comparison instructions with index variables
                        if inst.mnemonic in ("LES", "LEQ", "GRE", "GEQ", "ULES", "ULEQ"):
                            for inp in inst.inputs:
                                inp_name = inp.alias or inp.name
                                if inp_name in index_vars:
                                    # Found comparison with index variable
                                    # Try to extract the bound (other operand)
                                    other_inp = inst.inputs[1] if inst.inputs[0] == inp else inst.inputs[0]
                                    
                                    # Try to get constant bound
                                    bound_val = None
                                    if other_inp.alias and other_inp.alias.isdigit():
                                        bound_val = int(other_inp.alias)
                                    elif hasattr(other_inp, 'constant_value') and other_inp.constant_value is not None:
                                        bound_val = other_inp.constant_value
                                    
                                    if bound_val is not None and bound_val > max_bound:
                                        max_bound = bound_val
            
            # If we found a reasonable bound, mark this as an array
            if max_bound > 0 and max_bound <= 1000:  # Sanity check
                # Get the struct type if known
                struct_type = inferred_struct_types.get(array_var)
                if struct_type:
                    local_arrays[array_var] = (struct_type, max_bound)
                    # Also mark for semantic name if it exists
                    semantic_name = formatter._semantic_names.get(array_var)
                    if semantic_name:
                        local_arrays[semantic_name] = (struct_type, max_bound)

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

    # FIX #5: Second pass - infer struct types from function calls
    # Import struct type mapping from structures module
    from ....structures import infer_struct_from_function

    for block_id in func_block_ids:
        ssa_instrs = ssa_func.instructions.get(block_id, [])
        for inst in ssa_instrs:
            # Look for XCALL instructions (external function calls)
            if inst.mnemonic != "XCALL" or not inst.inputs:
                continue

            # Get function name from XFN table
            call_name = None
            if inst.instruction and inst.instruction.instruction:
                xfn_idx = inst.instruction.instruction.arg1
                xfn_entry = ssa_func.scr.get_xfn(xfn_idx) if ssa_func.scr else None
                if xfn_entry:
                    full_name = xfn_entry.name
                    paren_idx = full_name.find("(")
                    call_name = full_name[:paren_idx] if paren_idx > 0 else full_name

            if not call_name:
                continue

            # Check each argument to see if it's a struct pointer parameter
            for arg_idx, arg_value in enumerate(inst.inputs):
                # Infer struct type from function signature
                struct_type = infer_struct_from_function(call_name, arg_idx)
                if not struct_type:
                    continue

                # Extract variable name from &local_X or local_X
                var_name = arg_value.alias or arg_value.name
                if not var_name:
                    continue

                # Strip & prefix if present
                if var_name.startswith("&"):
                    var_name = var_name[1:]

                # Only process local variables
                if not var_name.startswith("local_"):
                    continue

                # Store the inferred struct type
                # Store using both local_X name AND semantic name if it exists
                inferred_struct_types[var_name] = struct_type

                # Also store for semantic name if it exists
                semantic_name = formatter._semantic_names.get(var_name)
                if semantic_name:
                    inferred_struct_types[semantic_name] = struct_type


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

    # FIX (Pattern 5 - 06-02): Collect all variable references from formatted expressions
    # This catches variables that appear in generated code but weren't tracked by SSA
    # (e.g., semantic names that were resolved but never registered)
    from ...expr import format_block_expressions
    import re

    for block_id in func_block_ids:
        block_exprs = format_block_expressions(ssa_func, block_id, formatter=formatter)
        for expr in block_exprs:
            # Extract address-of references: &varname
            # These are the most common cause of undeclared variables
            addr_of_vars = re.findall(r'&(\w+)', expr.text)

            for var_name in addr_of_vars:
                # Skip if already declared
                if var_name in var_types:
                    continue
                # Skip param_, data_, local_ (should be handled elsewhere)
                if var_name.startswith('param_') or var_name.startswith('data_'):
                    continue
                # Skip constants and keywords
                if var_name.isupper() or var_name.isdigit():
                    continue

                # This is an undeclared variable that needs declaration
                # Determine type - check if it's in inferred structs first
                var_type = "int"  # Default
                if var_name in inferred_struct_types:
                    var_type = inferred_struct_types[var_name]
                # Check if this is a vector/array-like name pattern
                elif var_name in ('vec', 'pos', 'rot', 'dir'):
                    var_type = "s_SC_vector"  # Common vector struct
                elif 'enum' in var_name.lower():
                    var_type = "s_SC_MP_EnumPlayers"  # Common enum struct

                # Add to var_types
                var_types[var_name] = var_type

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
