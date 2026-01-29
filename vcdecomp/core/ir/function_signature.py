"""
Function signature detection from bytecode.

Analyzes LCP/ASP/RET patterns to determine:
- Parameter count and types
- Return type
- Calling convention
"""

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass

from .ssa import SSAFunction
from .constant_propagation import ConstantPropagator


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


@dataclass
class CallSiteAnalysis:
    """Information about call-site argument usage for a function."""
    arg_counts: Set[int]
    args_all_constants: List[bool]


def _get_debug_param_name(ssa_func: SSAFunction, param_index: int) -> str:
    """
    Get parameter name from save_info debug symbols if available.

    Falls back to param_N if no debug info.
    """
    scr = ssa_func.scr
    if hasattr(scr, 'save_info') and scr.save_info and hasattr(scr.save_info, 'parameters'):
        params = scr.save_info.parameters
        if params and param_index < len(params):
            param = params[param_index]
            if hasattr(param, 'name') and param.name:
                return param.name
    return f"param_{param_index}"


def _is_constant_argument(constant_propagator: ConstantPropagator, value) -> bool:
    if getattr(value, "constant_value", None) is not None:
        return True
    return constant_propagator.get_constant(value) is not None


def _analyze_call_sites(
    ssa_func: SSAFunction,
    func_start: int
) -> Optional[CallSiteAnalysis]:
    """Analyze call sites to infer argument counts and constant-only arguments."""
    arg_counts: Set[int] = set()
    call_count = 0
    max_args = 0
    seen_counts: Dict[int, int] = {}
    all_constant_flags: Dict[int, bool] = {}

    constant_propagator = ConstantPropagator(ssa_func)
    constant_propagator.analyze()

    for block_instrs in ssa_func.instructions.values():
        for inst in block_instrs:
            if inst.mnemonic != "CALL":
                continue
            if not inst.instruction or not inst.instruction.instruction:
                continue
            if inst.instruction.instruction.arg1 != func_start:
                continue

            args = inst.inputs or []
            call_count += 1
            arg_counts.add(len(args))
            max_args = max(max_args, len(args))

            for idx in range(len(args)):
                seen_counts[idx] = seen_counts.get(idx, 0) + 1
                if idx not in all_constant_flags:
                    all_constant_flags[idx] = True
                if not _is_constant_argument(constant_propagator, args[idx]):
                    all_constant_flags[idx] = False

    if not arg_counts:
        return None

    args_all_constants: List[bool] = []
    for idx in range(max_args):
        seen = seen_counts.get(idx, 0)
        is_constant = all_constant_flags.get(idx, True)
        args_all_constants.append(seen == call_count and is_constant)

    return CallSiteAnalysis(arg_counts=arg_counts, args_all_constants=args_all_constants)


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

    # Track parameter accesses: stack_offset -> is_float
    # We store raw negative stack offsets and compute param indices at the end
    param_offset_accesses: Dict[int, bool] = {}  # stack_offset -> is_float

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

                # Check if this is a signed offset (two's complement)
                if stack_offset >= 0x80000000:
                    stack_offset = stack_offset - 0x100000000

                # Parameters are accessed with NEGATIVE offsets in the callee.
                # The calling convention pushes params right-to-left, then the
                # return address, then space for local frame. So parameter offsets
                # are: [sp-3] = last param, [sp-4] = second-to-last, etc.
                #
                # For a function with N params:
                #   [sp-3]   = param_{N-1} (last param)
                #   [sp-4]   = param_{N-2}
                #   [sp-(N+2)] = param_0 (first param)
                #
                # We record all negative offsets and compute param indices at the end.
                if stack_offset < 0 and stack_offset <= -3:
                    # Check if next instruction uses this as float
                    is_float = False
                    if i + 1 < len(ssa_instrs):
                        next_instr = ssa_instrs[i + 1]
                        if next_instr.mnemonic in {"FADD", "FSUB", "FMUL", "FDIV", "FGRE", "FLES", "FEQU"}:
                            is_float = True

                    param_offset_accesses[stack_offset] = is_float

            # Check for RET instruction to detect return type.
            # RET arg1 is the STACK CLEANUP SIZE (number of dwords to pop),
            # NOT a return value indicator. A function returns a value if there's
            # an LLD [sp-3] instruction before the RET that stores to the return slot.
            elif instr.mnemonic == "RET":
                # Look backwards for LLD [sp-3] pattern (return value store)
                found_return_value = False
                for prev_idx in range(i - 1, max(0, i - 5), -1):
                    prev_instr = ssa_instrs[prev_idx]
                    if prev_instr.mnemonic == "LLD":
                        if prev_instr.instruction and prev_instr.instruction.instruction:
                            offset = prev_instr.instruction.instruction.arg1
                            # Convert unsigned to signed
                            if offset >= 0x80000000:
                                offset = offset - 0x100000000
                            if offset == -3:
                                found_return_value = True
                                break
                    # Stop searching if we hit control flow
                    elif prev_instr.mnemonic in {"JMP", "JZ", "JNZ", "CALL", "XCALL"}:
                        break

                if found_return_value:
                    has_value_return = True
                else:
                    has_void_return = True

    # Determine parameter count from detected stack offsets.
    # Convert raw stack offsets to param indices.
    # Offsets: [sp-3] = last param, [sp-4] = second-to-last, etc.
    # The most negative offset determines param_count:
    #   min_offset = -(param_count + 2)
    #   param_count = -(min_offset) - 2
    # Param index: param_idx = offset - min_offset (0-based from most negative)
    if param_offset_accesses:
        min_offset = min(param_offset_accesses.keys())  # Most negative offset
        sig.param_count = (-min_offset) - 2  # e.g., -5 → 3 params, -4 → 2, -3 → 1

        # Convert offsets to param indices (0-based, param_0 = most negative offset)
        param_accesses: Dict[int, bool] = {}
        for offset, is_float in param_offset_accesses.items():
            param_idx = offset - min_offset  # most negative → 0, least negative → N-1
            param_accesses[param_idx] = is_float

        # Build parameter type list
        for param_idx in range(sig.param_count):
            is_float = param_accesses.get(param_idx, False)
            if is_float:
                sig.param_types.append(f"float param_{param_idx}")
            else:
                sig.param_types.append(f"int param_{param_idx}")

    # Apply call-site analysis to refine parameter count
    call_site_analysis = _analyze_call_sites(ssa_func, func_start)
    if call_site_analysis and len(call_site_analysis.arg_counts) == 1:
        call_arg_count = next(iter(call_site_analysis.arg_counts))
        if call_arg_count == 0:
            sig.param_count = 0
            sig.param_types = []
        else:
            if sig.param_count < call_arg_count:
                sig.param_count = call_arg_count
            while len(sig.param_types) < sig.param_count:
                param_index = len(sig.param_types)
                param_name = _get_debug_param_name(ssa_func, param_index)
                sig.param_types.append(f"int {param_name}")
        if call_site_analysis.args_all_constants:
            for idx, is_constant in enumerate(call_site_analysis.args_all_constants):
                if not is_constant or idx >= sig.param_count:
                    continue
                debug_name = _get_debug_param_name(ssa_func, idx)
                if debug_name != f"param_{idx}":
                    existing = sig.param_types[idx] if idx < len(sig.param_types) else "int"
                    parts = existing.split()
                    type_name = " ".join(parts[:-1]) if len(parts) >= 2 else existing
                    sig.param_types[idx] = f"{type_name} {debug_name}".strip()

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
