"""
Variable collection and declaration generation.

This module contains functions for collecting local variable declarations
from SSA function instructions and generating properly-typed declarations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Optional
import logging

from ....disasm import opcodes
from ...ssa import SSAFunction

logger = logging.getLogger(__name__)


@dataclass
class ArrayDims:
    """Information about array dimensions detected from usage patterns."""
    dimensions: List[int]  # List of dimension sizes [rows, cols] or [size] for 1D
    element_type: str  # Element type (int, float, struct name, etc.)
    element_size: int  # Size in bytes of each element
    confidence: float  # Confidence in the dimension calculation (0.0-1.0)


@dataclass
class StructTypeInfo:
    """Information about inferred struct types with confidence scoring."""
    struct_type: str  # Struct type name (e.g., "s_SC_MP_EnumPlayers")
    confidence: float  # Confidence in the inference (0.0-1.0)
    source: str  # Source of inference (e.g., "function_call", "field_access")


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


def _is_mul_add_pattern(inst) -> Tuple[bool, Optional[int], Optional[str], Optional[str]]:
    """
    Detect arr[i*width + j] pattern for multi-dimensional arrays.

    Pattern: ADD(MUL(index1, const_width), index2)
    Example: i*4 + j where i=[0,3), j=[0,4) → arr[3][4]

    Args:
        inst: SSA instruction to check

    Returns:
        Tuple of (is_pattern, stride, outer_index_var, inner_index_var)
    """
    if inst.mnemonic != "ADD" or len(inst.inputs) < 2:
        return (False, None, None, None)

    left = inst.inputs[0]
    right = inst.inputs[1]

    # Check if left is MUL instruction
    if left.producer_inst and left.producer_inst.mnemonic in {"MUL", "IMUL"}:
        mul_inst = left.producer_inst
        if len(mul_inst.inputs) >= 2:
            mul_left = mul_inst.inputs[0]
            mul_right = mul_inst.inputs[1]

            # Extract stride (width) from MUL constant
            stride = None
            if hasattr(mul_right, 'constant_value') and mul_right.constant_value is not None:
                stride = mul_right.constant_value
            elif mul_right.alias and mul_right.alias.isdigit():
                stride = int(mul_right.alias)

            if stride:
                outer_idx = mul_left.alias or mul_left.name
                inner_idx = right.alias or right.name
                return (True, stride, outer_idx, inner_idx)

    return (False, None, None, None)


def _detect_multidim_arrays(
    ssa_func: SSAFunction,
    func_block_ids: Set[int],
    inferred_struct_types: Dict[str, StructTypeInfo],
    loop_bounds: Dict[str, 'BoundInfo']
) -> Dict[str, ArrayDims]:
    """
    Detect multi-dimensional arrays from memory access patterns.

    Pattern: arr[i*width + j] → arr[i][j] where stride reveals inner dimension

    Args:
        ssa_func: SSA function to analyze
        func_block_ids: Block IDs in this function
        inferred_struct_types: Struct types inferred from function calls
        loop_bounds: Loop bound information from trace_loop_bounds()

    Returns:
        Dict mapping variable name to ArrayDims
    """
    multidim_arrays: Dict[str, ArrayDims] = {}

    # Scan for multi-dimensional indexing patterns
    for block_id in func_block_ids:
        ssa_instrs = ssa_func.instructions.get(block_id, [])
        for inst in ssa_instrs:
            # Look for memory access operations that might use multi-dim indexing
            if inst.mnemonic in {"LST", "LLD", "SSP", "ASP"}:
                # Check if offset calculation uses MUL+ADD pattern
                if len(inst.inputs) >= 1:
                    offset_val = inst.inputs[0]
                    if offset_val.producer_inst:
                        is_pattern, stride, outer_idx, inner_idx = _is_mul_add_pattern(offset_val.producer_inst)

                        if is_pattern and stride and outer_idx and inner_idx:
                            # Found multi-dimensional pattern!
                            # Extract base variable name
                            base_var = None
                            if len(inst.inputs) >= 2:
                                base_val = inst.inputs[1]
                                if base_val.alias and base_val.alias.startswith("&"):
                                    base_var = base_val.alias[1:]  # Strip &
                                elif base_val.alias:
                                    base_var = base_val.alias

                            if base_var and base_var.startswith("local_"):
                                # Calculate dimensions from stride and loop bounds
                                # Stride = inner_dimension * element_size
                                # Example: stride=16, element_size=4 → inner_dim=4

                                # Get element type and size
                                struct_info = inferred_struct_types.get(base_var)
                                element_type = struct_info.struct_type if struct_info else "int"
                                element_size = 4  # Default for int/float/pointer

                                # Calculate inner dimension from stride
                                inner_dim = stride // element_size

                                # Get outer dimension from loop bounds
                                outer_dim = None
                                if outer_idx in loop_bounds:
                                    outer_dim = loop_bounds[outer_idx].max_value + 1

                                # Get inner dimension confirmation from loop bounds
                                if inner_idx in loop_bounds:
                                    loop_inner_dim = loop_bounds[inner_idx].max_value + 1
                                    # Use loop bound if it matches stride calculation
                                    if loop_inner_dim == inner_dim:
                                        confidence = 0.95  # High confidence - stride and loop match
                                    else:
                                        # Prefer loop bound if available
                                        inner_dim = loop_inner_dim
                                        confidence = 0.85  # Medium-high confidence
                                else:
                                    confidence = 0.75  # Medium confidence - stride only

                                if outer_dim and inner_dim:
                                    multidim_arrays[base_var] = ArrayDims(
                                        dimensions=[outer_dim, inner_dim],
                                        element_type=element_type,
                                        element_size=element_size,
                                        confidence=confidence
                                    )
                                    logger.info(f"Multi-dimensional array detected: {base_var}[{outer_dim}][{inner_dim}] (confidence={confidence:.2f})")

    return multidim_arrays


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
    # Maps variable name -> StructTypeInfo (with confidence scoring)
    inferred_struct_types: Dict[str, StructTypeInfo] = {}

    # Phase 2: Import struct types from field tracker (via formatter._var_struct_types)
    # These are high-confidence struct types detected from function call patterns
    # BUGFIX: Only import struct types for variables that are actually used in the current function
    import sys

    # First, collect all variable names used in the current function's blocks
    vars_used_in_func = set()
    for block_id in func_block_ids:
        ssa_instrs = ssa_func.instructions.get(block_id, [])
        for inst in ssa_instrs:
            for output in inst.outputs:
                if output.alias:
                    vars_used_in_func.add(output.alias.lstrip('&'))
            for inp in inst.inputs:
                if inp.alias:
                    vars_used_in_func.add(inp.alias.lstrip('&'))

    if hasattr(formatter, '_var_struct_types'):
        print(f"DEBUG variables.py: formatter._var_struct_types has {len(formatter._var_struct_types)} entries", file=sys.stderr)
        for var_name, struct_type in formatter._var_struct_types.items():
            # Only import local variables (skip params and globals)
            if var_name.startswith('local_') or (var_name.startswith('&') and var_name[1:].startswith('local_')):
                # Remove & prefix if present
                clean_var_name = var_name[1:] if var_name.startswith('&') else var_name

                # BUGFIX: Skip variables not used in the current function
                # This prevents struct types from other functions leaking into this function
                if clean_var_name not in vars_used_in_func:
                    print(f"DEBUG variables.py: Skipping {clean_var_name} -> {struct_type} (not used in current function)", file=sys.stderr)
                    continue


                # ARRAY-FILLING FUNCTIONS: Use reduced confidence instead of skipping
                # Some engine functions take array parameters that get filled, but the same
                # stack variables are often reused for other purposes after the call.
                # However, we still emit the correct struct type to avoid compilation errors.
                #
                # Known array-filling functions:
                # - SC_MP_EnumPlayers: Fills s_SC_MP_EnumPlayers[64] array
                #
                # Example in tt.scr:
                #   ASP 256                           ; Allocate 256 dwords (1024 bytes)
                #   SC_MP_EnumPlayers(&local_X, ...) ; Fills array (field tracker sees struct)
                #   Must emit: s_SC_MP_EnumPlayers local_X; (or array)
                #
                ARRAY_FILLING_FUNCTIONS = {"s_SC_MP_EnumPlayers"}
                final_struct_type = struct_type
                confidence = 0.9  # Default high confidence from field tracker

                if struct_type in ARRAY_FILLING_FUNCTIONS:
                    # Still track it, but with lower confidence to indicate potential reuse
                    confidence = 0.7  # Lower than normal field tracker confidence
                    print(f"DEBUG variables.py: Using {struct_type} for {clean_var_name} with reduced confidence (array-filling function)", file=sys.stderr)
                else:
                    print(f"DEBUG variables.py: Imported {clean_var_name} -> {final_struct_type} (confidence={confidence}, source=field_tracker)", file=sys.stderr)

                # Store with confidence (0.9 normal, 0.7 for array-filling functions)
                inferred_struct_types[clean_var_name] = StructTypeInfo(
                    struct_type=final_struct_type,
                    confidence=confidence,  # Variable confidence based on function type
                    source="field_tracker"
                )

    # FIX (07-04): Track loop bounds for array dimension inference
    from .value_trace import trace_loop_bounds
    loop_bounds = trace_loop_bounds(ssa_func)

    # FIX (07-04): Track multi-dimensional arrays detected from indexing patterns
    multidim_arrays: Dict[str, ArrayDims] = {}

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
        # Skip global variables named from save_info (start with 'g' + uppercase letter)
        # Examples: gSidePoints, gEndRule, gAttackingSide
        if len(var_name) >= 2 and var_name[0] == 'g' and var_name[1].isupper():
            return

        # Check if variable has semantic name (i, player_info, etc.)
        display_name = var_name
        if var_name.startswith("local_"):
            semantic_name = formatter._semantic_names.get(var_name)
            if semantic_name:
                display_name = semantic_name

        # CRITICAL FIX (07-08): Allow type updates when we have opcode evidence
        # Previously, once a variable was declared, it couldn't be updated even if
        # we later discovered concrete opcode evidence (IADD→int, FADD→float).
        # This caused Pattern 2: struct types assigned from first encounter, literals fail later.
        #
        # New strategy: Always check for opcode types, and UPDATE if opcode is more specific
        already_declared = display_name in var_types
        if already_declared:
            # Check if this variable has confidence=1.0 type (ABSOLUTE certainty)
            # These should NEVER be overridden
            is_absolute_confidence = False
            if display_name in inferred_struct_types and inferred_struct_types[display_name].confidence == 1.0:
                is_absolute_confidence = True
            elif var_name in inferred_struct_types and inferred_struct_types[var_name].confidence == 1.0:
                is_absolute_confidence = True

            if not is_absolute_confidence:
                # Check if we have opcode evidence that should override the existing type
                if value.value_type != opcodes.ResultType.UNKNOWN:
                    opcode_type = result_type_to_c_type(value.value_type)
                    if opcode_type is not None and opcode_type in {"int", "float", "dword", "char", "short", "double"}:
                        # We have concrete opcode evidence - update the type
                        existing_type = var_types[display_name]
                        if existing_type.startswith("s_SC_") or existing_type == "int" or existing_type == "dword":
                            # Override struct types or generic types with concrete opcode types
                            logger.debug(f"[TYPE UPDATE] {display_name}: {existing_type} → {opcode_type} (opcode evidence)")
                            var_types[display_name] = opcode_type
            # Skip further processing if we don't have opcode evidence to update
            return

        # Determine type from instruction or value type
        var_type = default_type

        # TASK 1 (07-08): ABSOLUTE opcode-first priority to eliminate Pattern 2
        # Priority order (STRICT):
        # 1. Opcode-based concrete types (int/float/dword from IADD/FADD) - ABSOLUTE PRIORITY
        # 2. HIGH confidence (0.8+) struct types - ONLY if no opcode type
        # 3. MEDIUM confidence (0.5-0.8) struct types - ONLY if no opcode type
        # 4. Legacy field access patterns - DISABLED (too many false positives)
        # 5. LOW confidence (0.0-0.5) struct types - ignored

        # Get struct type info if available
        struct_type_info = None
        if display_name in inferred_struct_types:
            struct_type_info = inferred_struct_types[display_name]
        elif var_name in inferred_struct_types:
            struct_type_info = inferred_struct_types[var_name]

        # DEBUG: Log when processing local_1
        if display_name == "local_1" or var_name == "local_1":
            print(f"DEBUG variables.py: Processing {display_name} (var_name={var_name}), struct_type_info={struct_type_info}", file=sys.stderr)

        # Priority 1: ABSOLUTE PRIORITY - Opcode-based types (concrete evidence)
        # Variables used in FADD/IADD/IMUL operations MUST use opcode-derived types
        # This prevents field access heuristics from overriding concrete arithmetic type evidence
        opcode_type = None
        if value.value_type != opcodes.ResultType.UNKNOWN:
            opcode_type = result_type_to_c_type(value.value_type)


        # Priority 0: ABSOLUTE CONFIDENCE struct types (1.0) - these are CERTAIN
        # Examples: SC_MP_EnumPlayers first param is ALWAYS s_SC_MP_EnumPlayers[64]
        # These override even opcode types because they represent the true structure
        if struct_type_info and struct_type_info.confidence == 1.0:
            var_type = struct_type_info.struct_type
        elif opcode_type is not None and opcode_type in {"int", "float", "dword", "char", "short", "double"}:
            # CRITICAL: Concrete opcode type ALWAYS wins - skip all struct inference
            var_type = opcode_type
        # Priority 2: If no concrete opcode type, check HIGH confidence struct types (0.8+)
        # Phase 2 FIX: Re-enable for field_tracker sources ONLY
        # Field tracker uses LADR pattern matching which is much more reliable than
        # generic function call inference (which was disabled due to false positives)
        elif struct_type_info and struct_type_info.confidence >= 0.8:
            # Only use high-confidence types from field_tracker (not generic function calls)
            if struct_type_info.source == "field_tracker":
                var_type = struct_type_info.struct_type
                print(f"DEBUG variables.py: Using field_tracker type for {display_name}: {var_type}", file=sys.stderr)
            # else: skip - generic high-confidence types still cause false positives
        # Priority 3: Check MEDIUM confidence struct types (0.5-0.8)
        # Re-enabled for field_tracker and function_call sources
        elif struct_type_info and struct_type_info.confidence >= 0.5:
            # Use medium-confidence types from field_tracker or function_call
            if struct_type_info.source in ("field_tracker", "function_call"):
                var_type = struct_type_info.struct_type
                print(f"DEBUG variables.py: Using {struct_type_info.source} type for {display_name}: {var_type} (medium confidence={struct_type_info.confidence})", file=sys.stderr)
        # Priority 4: DISABLED - Legacy _struct_ranges causes false positives
        # Field access patterns alone are insufficient evidence for struct types
        # Only use confidence-scored struct inference from struct_type_map
        # elif var_name.startswith("local_"):
        #     struct_info = formatter._struct_ranges.get(var_name)
        #     if struct_info and isinstance(struct_info, tuple) and len(struct_info) >= 3:
        #         var_type = struct_info[2]
        # LOW confidence structs (<0.5) are ignored - fall through to default
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

                # SKIP storing struct types from function calls - TOO MANY FALSE POSITIVES
                # Variables passed to functions are frequently reused for other purposes.
                # Only trust field access patterns and explicit opcode types.
                # This prevents Pattern 2 type mismatches (int assigned to struct).
                #
                # Array-filling functions like SC_MP_EnumPlayers are handled by the skip
                # logic in the field_tracker import section above (lines 221-239).

                # Original logic (disabled):
                # struct_info = StructTypeInfo(struct_type=struct_type, confidence=0.4, source="function_call")
                # inferred_struct_types[var_name] = struct_info

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
                struct_info = inferred_struct_types.get(array_var)
                if struct_info:
                    local_arrays[array_var] = (struct_info.struct_type, max_bound)
                    # Also mark for semantic name if it exists
                    semantic_name = formatter._semantic_names.get(array_var)
                    if semantic_name:
                        local_arrays[semantic_name] = (struct_info.struct_type, max_bound)

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

                        # Skip if this variable has a high-confidence struct type from field_tracker
                        # (e.g., c_Vector3 with .x/.y/.z field access)
                        struct_info = inferred_struct_types.get(var_name)
                        if struct_info and struct_info.confidence >= 0.8:
                            print(f"DEBUG variables.py: Skipping SC_ZeroMem array detection for {var_name} - has struct type {struct_info.struct_type} (confidence={struct_info.confidence})", file=sys.stderr)
                            continue

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
                        # c_Vector3 is 12 bytes - skip array detection for this size
                        elif size == 12:
                            # Likely a c_Vector3 struct, not an array
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

                # Extract variable name from &local_X or local_X
                var_name = arg_value.alias or arg_value.name

                # Debug output for SC_P_GetPos specifically
                if call_name == "SC_P_GetPos":
                    print(f"DEBUG variables.py: SC_P_GetPos arg {arg_idx}: var_name={var_name}, struct_type={struct_type}", file=sys.stderr)

                if not struct_type:
                    continue

                if not var_name:
                    continue

                # Strip & prefix if present
                if var_name.startswith("&"):
                    var_name = var_name[1:]

                # Process local and tmp variables (struct buffer patterns)
                # Skip globals (data_), params (param_)
                if var_name.startswith("data_") or var_name.startswith("param_"):
                    continue

                # Re-enable struct inference from function calls with medium confidence
                # This is needed for patterns like: SC_P_GetPos(pl, &tmp)
                # where tmp must be c_Vector3 for the call to work
                # Only add if not already in inferred_struct_types with higher confidence
                if var_name not in inferred_struct_types or inferred_struct_types[var_name].confidence < 0.5:
                    struct_info = StructTypeInfo(struct_type=struct_type, confidence=0.5, source="function_call")
                    inferred_struct_types[var_name] = struct_info
                    print(f"DEBUG variables.py: Inferred struct type {struct_type} for {var_name} from {call_name} arg {arg_idx}", file=sys.stderr)

    # FIX (01-20): Infer variable types from XCALL return types (SDK)
    # Track variables that receive return values from external functions
    # This allows proper type inference for things like ushort* from SC_Wtxt
    return_type_vars: Dict[str, str] = {}  # var_name -> return_type

    # NOTE: SSA XCALL instructions don't have outputs populated, so we can't infer
    # types from XCALL outputs directly. Instead, we scan formatted expressions
    # for assignment patterns like "local_X = SC_FuncName(...)" below.

    # FIX (07-04): Detect multi-dimensional arrays from indexing patterns
    multidim_arrays = _detect_multidim_arrays(
        ssa_func,
        func_block_ids,
        inferred_struct_types,
        loop_bounds
    )

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

    # DEBUG: Log function name for context
    func_name = ssa_func.name if hasattr(ssa_func, 'name') else "unknown"
    func_entry = ssa_func.entry_block if hasattr(ssa_func, 'entry_block') else None
    if func_entry == 119:  # func_0119 has entry block 119
        print(f"DEBUG variables.py: Processing func with entry 119, name={func_name}, func_block_ids={func_block_ids}", file=sys.stderr)

    for block_id in func_block_ids:
        block_exprs = format_block_expressions(ssa_func, block_id, formatter=formatter)

        # DEBUG: Log all expressions that mention local_1
        for expr in block_exprs:
            if "local_1" in expr.text:
                print(f"DEBUG variables.py: Expression mentions local_1: '{expr.text}'", file=sys.stderr)

        # FIX (01-20): Scan expressions for function call assignments to infer return types
        # Pattern: "var_name = SC_FuncName(...)" -> look up SC_FuncName return type
        for expr in block_exprs:
            # Match: local_X = SC_FuncName(...) or t*_ret = SC_FuncName(...)
            assign_match = re.match(r'^\s*(local_\d+|t\d+_ret)\s*=\s*(SC_\w+)\(', expr.text)
            if assign_match:
                var_name = assign_match.group(1)
                func_name = assign_match.group(2)
                # Look up function return type
                if hasattr(formatter, '_header_db') and formatter._header_db:
                    func_sig = formatter._header_db.get_function_signature(func_name)
                    if func_sig and func_sig.get('return_type'):
                        return_type = func_sig['return_type']
                        # Only add if it's a meaningful type (not void/dword/int)
                        if return_type and return_type not in ('void', 'dword', 'int', 'BOOL'):
                            # Store in return_type_vars if not already set
                            if var_name not in return_type_vars:
                                return_type_vars[var_name] = return_type
                                logger.debug(f"Inferred {var_name} type from {func_name}: {return_type}")

        # FIX (01-20): Scan expressions for function calls with pointer arguments
        # Pattern: "SC_FuncName(tmp_var, ...)" where arg 0 expects void*/dword
        # This fixes issues like SC_DUMMY_Set_DoNotRenHier2(tmp16, ...) where tmp16 should be dword
        for expr in block_exprs:
            # Match: SC_FuncName(arg0, arg1, ...)
            call_match = re.search(r'(SC_\w+)\(([^)]*)\)', expr.text)
            if call_match:
                func_name = call_match.group(1)
                args_str = call_match.group(2)
                if args_str and hasattr(formatter, '_header_db') and formatter._header_db:
                    func_sig = formatter._header_db.get_function_signature(func_name)
                    # SDK database uses 'parameters' as list of (type, name) tuples
                    params = func_sig.get('parameters') if func_sig else None
                    if params:
                        # Split args by comma (simple parsing, may fail on complex expressions)
                        args = [a.strip() for a in args_str.split(',')]
                        for idx, arg in enumerate(args):
                            if idx >= len(params):
                                break
                            # params is a list of tuples: [(type, name), ...]
                            param_type = params[idx][0] if isinstance(params[idx], tuple) else ''
                            # Check if param expects pointer type (void*, or any type ending in *)
                            # NOTE: "dword" is NOT a pointer type - it's a 32-bit unsigned int
                            # Only types with "*" in them are actual pointers
                            if param_type and '*' in param_type:
                                # IMPORTANT: Only infer pointer type if the variable is passed DIRECTLY,
                                # not via address-of (&). If passed as &var, then var is the THING BEING
                                # POINTED TO, not a pointer itself.
                                if arg.startswith('&'):
                                    # Variable is passed by address - don't change its type
                                    continue

                                # Check if arg is a simple variable name (tmp*, local_*)
                                if re.match(r'^(tmp\d*|local_\d+)$', arg):
                                    # This variable should be void* (pointer type)
                                    # FIX (01-20): Use "void*" instead of "dword" for pointer types
                                    # The Vietcong compiler is strict about pointer types
                                    if arg not in return_type_vars:
                                        return_type_vars[arg] = 'void*'
                                        logger.debug(f"Inferred {arg} type from {func_name} param {idx} ({param_type}): void* (pointer arg)")

        # FIX (01-20): Detect dereferenced variables that need pointer types
        # Pattern: *var_name = value  or  value = *var_name
        # These variables must be pointer types
        for expr in block_exprs:
            # Match: *var_name = (dereference on left side of assignment)
            deref_matches = re.findall(r'\*\s*(tmp\d+|local_\d+)\s*=', expr.text)
            for var_name in deref_matches:
                if var_name not in return_type_vars:
                    return_type_vars[var_name] = 'dword*'
                    print(f"DEBUG variables.py: Deref var {var_name} -> dword* (from *{var_name} = ...)", file=sys.stderr)
            # Match: = *var_name (dereference on right side)
            deref_read_matches = re.findall(r'=\s*\*\s*(tmp\d+|local_\d+)\b', expr.text)
            for var_name in deref_read_matches:
                if var_name not in return_type_vars:
                    return_type_vars[var_name] = 'dword*'
                    print(f"DEBUG variables.py: Deref var {var_name} -> dword* (from = *{var_name})", file=sys.stderr)

        for expr in block_exprs:
            # Extract address-of references: &varname
            # These are the most common cause of undeclared variables
            addr_of_vars = re.findall(r'&(\w+)', expr.text)

            # DEBUG: Log address-of variables found
            if "local_1" in addr_of_vars:
                print(f"DEBUG variables.py: Found &local_1 in expression: {expr.text}", file=sys.stderr)

            for var_name in addr_of_vars:
                # Skip if already declared
                if var_name in var_types:
                    continue
                # Skip param_, data_ (globals and parameters)
                # Phase 2: DON'T skip local_ - they may only appear as &local_X (address-of)
                if var_name.startswith('param_') or var_name.startswith('data_'):
                    continue
                # Skip global variables named from save_info (start with 'g' + uppercase letter)
                # Examples: gSidePoints, gEndRule, gAttackingSide
                if len(var_name) >= 2 and var_name[0] == 'g' and var_name[1].isupper():
                    continue
                # Skip constants and keywords
                if var_name.isupper() or var_name.isdigit():
                    continue

                # This is an undeclared variable that needs declaration
                # Phase 2: Check field_tracker struct types FIRST
                var_type = "int"  # Default
                struct_info = inferred_struct_types.get(var_name)
                if struct_info and struct_info.source == "field_tracker" and struct_info.confidence >= 0.5:
                    # Use medium+ confidence field_tracker types (includes array-filling functions)
                    var_type = struct_info.struct_type
                    print(f"DEBUG variables.py: Undeclared var {var_name} gets field_tracker type: {var_type} (confidence={struct_info.confidence})", file=sys.stderr)
                # else: use int default (generic struct inference still disabled due to false positives)

                # Add to var_types
                var_types[var_name] = var_type

    # Phase 2: Add all medium+ confidence struct types to var_types
    # These may not have been processed by process_value (e.g., only used as &local_X)
    # Includes array-filling functions with confidence=0.7 and function_call with confidence=0.5
    for var_name, struct_info in inferred_struct_types.items():
        if struct_info.confidence >= 0.5:
            # Only add if not already declared
            if var_name not in var_types:
                var_types[var_name] = struct_info.struct_type
                print(f"DEBUG variables.py: Added {struct_info.source} var {var_name} -> {struct_info.struct_type} (confidence={struct_info.confidence})", file=sys.stderr)

            # Also check if this variable has a semantic name and apply struct type there too
            if hasattr(formatter, '_semantic_names'):
                semantic_name = formatter._semantic_names.get(var_name)
                if semantic_name and semantic_name not in var_types:
                    var_types[semantic_name] = struct_info.struct_type
                    print(f"DEBUG variables.py: Added semantic name {semantic_name} (from {var_name}) -> {struct_info.struct_type}", file=sys.stderr)
                elif semantic_name and semantic_name in var_types and var_types[semantic_name] == 'int':
                    # Override int default with struct type
                    var_types[semantic_name] = struct_info.struct_type
                    print(f"DEBUG variables.py: Updated semantic name {semantic_name} from int -> {struct_info.struct_type}", file=sys.stderr)

    # FIX (01-20): Apply XCALL return types to variables
    # This allows proper type inference for things like ushort* from SC_Wtxt
    # Applied after other type inference but with medium priority - override defaults but not field_tracker
    for var_name, return_type in return_type_vars.items():
        current_type = var_types.get(var_name, 'int')
        # Only override if current type is a generic default (int, dword)
        # Don't override high-confidence types from field_tracker
        if current_type in ('int', 'dword'):
            var_types[var_name] = return_type
            logger.debug(f"Variable {var_name} type changed {current_type} -> {return_type} (from function return)")

    # FIX (01-20): Detect struct-typed variables used with array subscripting
    # Pattern: local_5[tmp] = value when local_5 is typed as a struct
    # If the struct type is used with array indexing, declare as array of that struct
    struct_array_vars: Dict[str, Tuple[str, int]] = {}  # var_name -> (struct_type, array_size)
    for block_id in func_block_ids:
        block_exprs = format_block_expressions(ssa_func, block_id, formatter=formatter)
        for expr in block_exprs:
            # Match: var_name[index] (any subscript access, not just assignment)
            subscript_match = re.search(r'\b(local_\d+)\s*\[', expr.text)
            if subscript_match:
                var_name = subscript_match.group(1)
                # Check if this variable has a struct type
                var_type = var_types.get(var_name)
                if var_type and (var_type.startswith('s_SC_') or var_type.startswith('c_')):
                    # This struct variable is used with array subscripting
                    # Declare as array of that struct type
                    if var_name not in struct_array_vars:
                        # Default to 4 elements (common for sides arrays: US, VC, Neutral, +1)
                        struct_array_vars[var_name] = (var_type, 4)
                        print(f"DEBUG variables.py: Struct {var_name} ({var_type}) used with subscript - declaring as {var_type}[4]", file=sys.stderr)

    # FIX (07-04): Generate declarations (multi-dim arrays, 1D arrays, then regular variables)
    declarations = []

    # First, declare multi-dimensional arrays
    for var_name in sorted(var_types.keys()):
        if var_name in multidim_arrays:
            array_info = multidim_arrays[var_name]
            dims = array_info.dimensions
            element_type = array_info.element_type
            confidence = array_info.confidence

            # Format declaration based on number of dimensions
            if len(dims) == 1:
                decl = f"{element_type} {var_name}[{dims[0]}]"
            elif len(dims) == 2:
                decl = f"{element_type} {var_name}[{dims[0]}][{dims[1]}]"
            elif len(dims) == 3:
                decl = f"{element_type} {var_name}[{dims[0]}][{dims[1]}][{dims[2]}]"
            else:
                # Fallback for 4D+ (rare)
                dim_str = "][".join(str(d) for d in dims)
                decl = f"{element_type} {var_name}[{dim_str}]"

            # Add TODO comment for low confidence
            if confidence < 0.70:
                decl += f" /* TODO: verify array size (confidence={confidence:.2f}) */"

            declarations.append(decl)

    # Second, declare 1D arrays (not in multidim_arrays)
    for var_name in sorted(var_types.keys()):
        if var_name in local_arrays and var_name not in multidim_arrays:
            # Check if this variable has a high-confidence struct type from field_tracker
            # If so, declare as struct, not as array
            struct_info = inferred_struct_types.get(var_name)
            if struct_info and struct_info.confidence >= 0.8 and struct_info.source == "field_tracker":
                # Declare as struct, skip array declaration
                declarations.append(f"{struct_info.struct_type} {var_name}")
                print(f"DEBUG variables.py: Declaring {var_name} as {struct_info.struct_type} (field_tracker) instead of array", file=sys.stderr)
                continue
            element_type, array_size = local_arrays[var_name]
            declarations.append(f"{element_type} {var_name}[{array_size}]")

    # Third, declare struct array variables (detected from subscripting patterns)
    for var_name in sorted(struct_array_vars.keys()):
        if var_name not in local_arrays and var_name not in multidim_arrays:
            struct_type, array_size = struct_array_vars[var_name]
            declarations.append(f"{struct_type} {var_name}[{array_size}]")
            print(f"DEBUG variables.py: Declaring {var_name} as {struct_type}[{array_size}] (subscript detection)", file=sys.stderr)

    # Finally, declare regular variables (skip all arrays including struct arrays)
    for var_name in sorted(var_types.keys()):
        if var_name not in local_arrays and var_name not in multidim_arrays and var_name not in struct_array_vars:
            var_type = var_types[var_name]

            # BUGFIX: Handle array syntax in type string
            # If var_type contains "[...]", split it properly: "Type[256]" -> "Type var[256]"
            if "[" in var_type:
                # Split at first [
                base_type = var_type[:var_type.index("[")]
                array_part = var_type[var_type.index("["):]
                declarations.append(f"{base_type} {var_name}{array_part}")
            else:
                declarations.append(f"{var_type} {var_name}")

    # CRITICAL FIX (07-08): Post-process to eliminate Pattern 2
    # Remove struct types from tmp* variables that don't have field access
    # These are likely stack-reuse false positives from _struct_ranges
    cleaned_declarations = []
    for decl in declarations:
        # Check if this is a tmp variable with struct type
        if decl.startswith("s_SC_") and " tmp" in decl:
            # Extract variable name
            parts = decl.split()
            if len(parts) >= 2:
                var_name = parts[1].split('[')[0]  # Remove array brackets if present
                if var_name.startswith("tmp"):
                    # Replace struct type with int (safe default for tmp variables)
                    cleaned_declarations.append(f"int {var_name}")
                    continue
        cleaned_declarations.append(decl)

    # CRITICAL FIX: Deduplicate declarations
    # A variable may appear in both struct and int declarations if it has multiple inferred types
    # Keep only the first declaration (which should be the struct type, since structs are declared first)
    seen_vars = set()
    deduplicated_declarations = []
    for decl in cleaned_declarations:
        # Extract variable name from declaration
        # Handle: "type varname", "type varname[size]", "type varname[size1][size2]"
        parts = decl.split()
        if len(parts) >= 2:
            var_name = parts[1].split('[')[0].rstrip(';')  # Remove array brackets and semicolons
            if var_name not in seen_vars:
                seen_vars.add(var_name)
                deduplicated_declarations.append(decl)
            else:
                print(f"DEBUG variables.py: Skipping duplicate declaration for {var_name}: {decl}", file=sys.stderr)
        else:
            deduplicated_declarations.append(decl)

    return deduplicated_declarations
