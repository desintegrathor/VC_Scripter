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
                params = ", ".join([f"int param{i}" for i in range(self.param_count)])

        return f"{self.return_type} {func_name}({params})"


def detect_function_signature(
    ssa_func: SSAFunction,
    func_start: int,
    func_end: Optional[int] = None
) -> FunctionSignature:
    """
    Detect function signature by analyzing bytecode patterns.

    Pattern detection:
    1. LCP [sp+N] with positive offset N = parameter at position N
    2. ASP N at function start = allocating N DWORDs of local space
    3. FADD/FMUL/FDIV with parameter = float parameter
    4. RET N = returns N values

    Args:
        ssa_func: SSA function data
        func_start: Starting address of function
        func_end: Ending address of function (optional)

    Returns:
        FunctionSignature with detected parameters and return type
    """
    cfg = ssa_func.cfg
    sig = FunctionSignature()

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

                if debug:
                    print(f"[SIG DEBUG] LCP at block {block_id}, offset={stack_offset}", file=sys.stderr)

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
                            if debug:
                                print(f"[SIG DEBUG] Found float usage after LCP", file=sys.stderr)

                    if debug:
                        print(f"[SIG DEBUG] Detected parameter at offset {param_offset}, is_float={is_float}", file=sys.stderr)

                    param_accesses[param_offset] = is_float

            # Check for RET instruction to detect return type
            elif instr.mnemonic == "RET" and instr.instruction:
                ret_count = instr.instruction.instruction.arg1
                if ret_count > 0:
                    sig.return_type = "int"  # Returns something
                else:
                    sig.return_type = "int"  # Default to int (may return FALSE/TRUE)

    # Determine parameter count from maximum offset
    if param_accesses:
        # Sort offsets to determine parameter positions
        sorted_offsets = sorted(param_accesses.keys())

        # Parameter count = number of distinct offsets
        sig.param_count = len(sorted_offsets)

        # Build parameter type list
        for offset in sorted_offsets:
            is_float = param_accesses[offset]
            if is_float:
                sig.param_types.append("float time")  # Common parameter name
            else:
                sig.param_types.append("int param")

    return sig


def get_function_signature_string(
    ssa_func: SSAFunction,
    func_name: str,
    func_start: int,
    func_end: Optional[int] = None,
    scr_header_enter_size: int = 0
) -> str:
    """
    Get complete function signature string for C output.

    Args:
        ssa_func: SSA function data
        func_name: Function name
        func_start: Function start address
        func_end: Function end address (optional)
        scr_header_enter_size: Entry parameter size from SCR header (for ScriptMain)

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

    # Detect signature from bytecode
    sig = detect_function_signature(ssa_func, func_start, func_end)

    # Convert to string
    return sig.to_c_signature(func_name)
