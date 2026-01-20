"""
Function signature detection from bytecode.

Analyzes LCP/ASP/RET patterns to determine:
- Parameter count and types
- Return type
- Calling convention
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from .ssa import SSAFunction


@dataclass
class FunctionSignature:
    """Detected function signature."""
    param_count: int = 0
    param_types: List[str] = None  # List of parameter type names
    return_type: str = "int"  # Default to int
    has_varargs: bool = False

    def __post_init__(self):
        if self.param_types is None:
            self.param_types = []

    def to_c_signature(self, func_name: str) -> str:
        """Convert to C function signature string."""
        if self.param_count == 0:
            params = "void"
        else:
            # Use detected types or fallback to generic types
            if len(self.param_types) == self.param_count:
                params = ", ".join(self.param_types)
            else:
                # Fallback: use generic int/float based on count
                params = ", ".join([f"int param_{i}" for i in range(self.param_count)])

        return f"{self.return_type} {func_name}({params})"


def detect_function_signature(
    ssa_func: SSAFunction,
    func_start: int,
    func_end: Optional[int] = None,
    func_name: str = None
) -> FunctionSignature:
    """
    Detect function signature by analyzing bytecode patterns.

    Pattern detection:
    1. LCP [sp+N] with positive offset N = parameter at position N
    2. ASP N at function start = allocating N DWORDs of local space
    3. FADD/FMUL/FDIV with parameter = float parameter
    4. RET N = returns N values

    Special case: Entry point function uses header information.

    Args:
        ssa_func: SSA function data
        func_start: Starting address of function
        func_end: Ending address of function (optional)

    Returns:
        FunctionSignature with detected parameters and return type
    """
    cfg = ssa_func.cfg
    sig = FunctionSignature()

    # CRITICAL FIX: For ScriptMain entry point, use header information
    # Entry point parameters are defined in SCR header, not detected from LCP patterns
    if func_name == "ScriptMain" and ssa_func.scr and hasattr(ssa_func.scr, 'header'):
        header = ssa_func.scr.header
        if header.enter_size > 0:
            sig.param_count = header.enter_size
            # For entry point, first parameter is always s_SC_NET_info *info
            if header.enter_size == 1:
                sig.param_types = ["s_SC_NET_info *info"]
            else:
                # Multiple parameters - use generic types for additional ones
                sig.param_types = ["s_SC_NET_info *info"]
                for i in range(1, header.enter_size):
                    sig.param_types.append(f"int param_{i}")
            # Entry point always returns int
            sig.return_type = "int"
            return sig

    # Find entry block for this function
    entry_block_id = None
    for block_id, block in cfg.blocks.items():
        if block.start == func_start:
            entry_block_id = block_id
            break

    if entry_block_id is None:
        return sig  # Can't detect without entry block

    # Get all blocks in this function
    func_blocks = set()
    for block_id, block in cfg.blocks.items():
        if block.start >= func_start:
            if func_end is None or block.start <= func_end:
                func_blocks.add(block_id)

    # Track parameter accesses: offset -> is_float
    param_accesses: Dict[int, bool] = {}  # offset -> is_float

    # DEBUG: Track what we find
    import sys
    debug = False  # Set to True to enable debug output

    # Track if we've seen any RET that returns a value
    has_value_return = False
    has_void_return = False

    # Scan all instructions in function blocks
    for block_id in func_blocks:
        if block_id not in ssa_func.instructions:
            continue

        ssa_instrs = ssa_func.instructions[block_id]

        for i, instr in enumerate(ssa_instrs):
            # Check for LCP instruction (load from stack)
            if instr.mnemonic == "LCP" and instr.instruction:
                # Get the ORIGINAL bytecode offset, not the SSA-transformed one
                orig_instr = instr.instruction.instruction
                stack_offset = orig_instr.arg1

                # CRITICAL FIX: Check if this is a signed offset
                # The stack offset might be stored as unsigned int, but represents signed
                # If offset > 2^31, it's actually negative (two's complement)
                if stack_offset >= 0x80000000:
                    # Convert from unsigned to signed (two's complement)
                    stack_offset = stack_offset - 0x100000000

                # Parameters are accessed with NEGATIVE offsets in the callee
                # Example: func is called, parameter was pushed at caller's [sp+something]
                # Inside callee, it's at [sp-4] (just below return address)
                if stack_offset < 0:
                    # Parameter offset: -4 = param 0, -8 = param 1, etc.
                    param_offset = abs(stack_offset)

                    # Check if next instruction uses this as float
                    is_float = False
                    if i + 1 < len(ssa_instrs):
                        next_instr = ssa_instrs[i + 1]
                        if next_instr.mnemonic in {"FADD", "FSUB", "FMUL", "FDIV", "FGRE", "FLES", "FEQU"}:
                            is_float = True

                    param_accesses[param_offset] = is_float

            # Check for RET instruction to detect return type
            elif instr.mnemonic == "RET" and instr.instruction:
                ret_count = instr.instruction.instruction.arg1
                if ret_count > 0:
                    has_value_return = True
                else:
                    has_void_return = True

    # Determine parameter count from maximum offset
    if param_accesses:
        # Sort offsets to determine parameter positions
        sorted_offsets = sorted(param_accesses.keys())

        # Parameter count = number of distinct offsets
        sig.param_count = len(sorted_offsets)

        # Build parameter type list
        for param_index, offset in enumerate(sorted_offsets):
            is_float = param_accesses[offset]
            if is_float:
                sig.param_types.append(f"float param_{param_index}")
            else:
                sig.param_types.append(f"int param_{param_index}")

    # Determine return type from RET instructions
    # If ANY RET returns a value, function returns int
    # If ALL RET instructions return void, function is void
    if has_value_return:
        sig.return_type = "int"
    elif has_void_return:
        sig.return_type = "void"
    # else: default "int" from FunctionSignature init

    return sig


def get_function_signature_string(
    ssa_func: SSAFunction,
    func_name: str,
    func_start: int,
    func_end: Optional[int] = None,
    scr_header_enter_size: int = 0,
    type_engine: Optional['TypeInferenceEngine'] = None
) -> str:
    """
    Get complete function signature string for C output.

    Args:
        ssa_func: SSA function data
        func_name: Function name
        func_start: Function start address
        func_end: Function end address (optional)
        scr_header_enter_size: Entry parameter size from SCR header (for ScriptMain)
        type_engine: Optional TypeInferenceEngine for parameter type inference (Plan 07-06a)

    Returns:
        Complete C function signature like "int func_name(float time)"
    """
    # Special handling for entry point functions
    if scr_header_enter_size > 0 and func_name in ("ScriptMain", "_init", "main"):
        # Entry point always has s_SC_NET_info *info parameter
        from ..script_type_detector import detect_script_type
        scr = ssa_func.scr
        script_type = detect_script_type(scr)
        ret_type = "int" if scr.header.ret_size > 0 else "void"
        return f"{ret_type} {func_name}({script_type} *info)"

    # Plan 07-06a: Use type inference for parameter types and return type if available
    if type_engine:
        return _generate_function_signature_from_type_inference(
            ssa_func, func_name, type_engine
        )

    # Fallback: Detect signature from bytecode patterns
    sig = detect_function_signature(ssa_func, func_start, func_end)

    # Convert to string
    return sig.to_c_signature(func_name)


def _generate_function_signature_from_type_inference(
    ssa_func: SSAFunction,
    func_name: str,
    type_engine: 'TypeInferenceEngine'
) -> str:
    """
    Generate C function signature from type inference results.

    This uses TypeInferenceEngine.infer_parameter_types() and infer_return_type()
    to build semantic function signatures with correct types and names.

    Args:
        ssa_func: SSA function data
        func_name: Function name
        type_engine: Type inference engine with completed analysis

    Returns:
        Complete C function signature like "void process_node(c_Node* node, float damage)"
    """
    # Get parameter types from type inference (Plan 07-06a Task 1)
    param_infos = type_engine.infer_parameter_types()

    # Get return type from type inference
    return_type = type_engine.infer_return_type()

    # Build parameter list
    params = []
    low_confidence_params = []

    for param_info in param_infos:
        # Format: "type name"
        params.append(f"{param_info.type} {param_info.name}")

        # Track low confidence parameters for TODO comment
        if param_info.confidence < 0.70:
            low_confidence_params.append(param_info.name)

    # Handle empty parameter list
    if not params:
        param_str = "void"
    else:
        param_str = ", ".join(params)

    # Build full signature
    signature = f"{return_type} {func_name}({param_str})"

    # Add confidence annotation for uncertain signatures
    if low_confidence_params:
        signature += "  /* TODO: verify parameter types */"

    return signature
