"""
Enhanced function boundary detection using RET instructions.

The original get_function_boundaries() in disassembler.py only considers CALL targets,
missing orphan functions (not called internally). This module uses RET instructions
to accurately detect all function boundaries.

This fixes the issue where multiple separate functions are merged together,
causing unreachable code to appear after return statements in decompiled output.
"""

from typing import Dict, List, Tuple, Set, Optional
import logging

from vcdecomp.core.loader.scr_loader import SCRFile
from vcdecomp.core.disasm.opcodes import OpcodeResolver
from .debug_output import debug_print

logger = logging.getLogger(__name__)


def _find_reachable_ret_boundary(
    instructions, func_start: int, func_end: int,
    return_opcodes: Set[int], jump_opcodes: Set[int]
) -> int:
    """
    Find the actual end of a function by walking RET instructions.

    For each RET in [func_start, func_end], check if any instruction
    in [func_start, ret_addr] jumps to an address in (ret_addr, func_end].
    If yes, the RET is an early return — keep scanning.
    If no, the RET ends the function.

    Returns the address of the first RET that ends the function,
    or func_end if no splitting point is found.
    """
    for instr in instructions:
        if instr.address < func_start or instr.address > func_end:
            continue
        if instr.opcode not in return_opcodes:
            continue

        ret_addr = instr.address

        # Check if any instruction in [func_start, ret_addr] jumps past this RET
        has_forward_jump = False
        for check_instr in instructions:
            if check_instr.address < func_start or check_instr.address > ret_addr:
                continue
            if check_instr.opcode in jump_opcodes:
                target = check_instr.arg1
                if ret_addr < target <= func_end:
                    has_forward_jump = True
                    break

        if not has_forward_jump:
            # No code before this RET jumps past it — this RET ends the function
            return ret_addr

    # No splitting RET found
    return func_end

def _load_saveinfo_function_names(scr: SCRFile) -> Dict[int, str]:
    """
    Build mapping of function start addresses to names from SaveInfo, if present.

    NOTE: SaveInfo does NOT contain function names! It only stores global variable
    information (name, data_segment_offset, size). The val1 field is a dword index
    into the data segment, NOT a code address.

    This function now returns an empty dict to prevent incorrectly treating
    data segment offsets as function entry points. For example, LEVEL.SCR has:
      - gphase: val1=224 (data segment offset, NOT code address)
      - g_dialog: val1=225 (data segment offset, NOT code address)

    These were incorrectly being added as function start addresses because 224/225
    happen to be valid code instruction indices, causing bogus "entry block not found"
    errors in the decompiler output.

    Function names come from:
      1. CALL targets (detected from code analysis)
      2. Entry point (ScriptMain from header.enter_ip)
      3. _init for orphan code at address 0
    """
    # SaveInfo only contains global variables, not function names
    return {}


def _ensure_unique_name(name: str, existing: Set[str], start_addr: int) -> str:
    """Ensure function name uniqueness within bounds mapping."""
    if name not in existing:
        return name
    suffix = f"_{start_addr:04d}"
    candidate = f"{name}{suffix}"
    if candidate not in existing:
        return candidate
    counter = 2
    while True:
        candidate = f"{name}{suffix}_{counter}"
        if candidate not in existing:
            return candidate
        counter += 1


def detect_function_boundaries_v2(
    scr: SCRFile,
    resolver: OpcodeResolver,
    entry_point: int = None
) -> Dict[str, Tuple[int, int]]:
    """
    Detect function boundaries using RET instructions.

    This function analyzes RET instructions to determine where functions end,
    then creates function segments between RET boundaries. This is more accurate
    than only using CALL targets, which misses orphan functions.

    Strategy:
    1. Find all RET instructions
    2. Each RET marks the end of a function
    3. Next instruction after RET starts a new function
    4. Assign names based on CALL targets or default naming

    Args:
        scr: The parsed SCR file
        resolver: Opcode resolver for the script variant
        entry_point: Optional entry point address (usually from header.enter_ip)

    Returns:
        Dict mapping function_name -> (start_addr, end_addr)
        Example: {"ScriptMain": (0, 50), "func_0051": (51, 100)}
    """
    instructions = scr.code_segment.instructions
    return_opcodes = resolver.return_opcodes
    internal_call_opcodes = resolver.internal_call_opcodes

    # Step 1: Find all RET addresses
    ret_addresses = []
    for instr in instructions:
        if instr.opcode in return_opcodes:
            ret_addresses.append(instr.address)

    ret_addresses.sort()
    logger.debug(f"Found {len(ret_addresses)} RET instructions at addresses: {ret_addresses}")

    # Step 2: Find CALL targets for naming
    call_targets = set()
    for instr in instructions:
        if instr.opcode in internal_call_opcodes:
            call_targets.add(instr.arg1)

    logger.debug(f"Found {len(call_targets)} CALL targets: {sorted(call_targets)}")

    saveinfo_names = _load_saveinfo_function_names(scr)
    saveinfo_starts = set(saveinfo_names.keys())

    # Step 3: Build function starts using CALL targets + entry point
    #
    # STRATEGY:
    # Use CALL targets as definitive function starts.  Entry point is ScriptMain.
    # This prevents splitting functions with multiple returns into micro-functions.

    boundaries = {}
    function_starts = []

    # Add entry point if provided
    if entry_point is not None:
        # BUGFIX: Negative entry points are relative to code end
        # entry_point=-1097 means 1097 instructions from end
        if entry_point < 0:
            actual_entry = len(instructions) + entry_point
            debug_print(f"DEBUG: Entry point = {entry_point} (resolves to {actual_entry})")
            function_starts.append(actual_entry)
        else:
            debug_print(f"DEBUG: Entry point = {entry_point}")
            function_starts.append(entry_point)
        logger.debug(f"Entry point at address {entry_point}")

    # Add CALL targets as definitive function starts
    function_starts.extend(call_targets)

    # Add SaveInfo-reported function starts (if present)
    function_starts.extend(saveinfo_starts)

    # Handle orphan code before first function
    if function_starts:
        first_func = min(function_starts)
        if first_func > 0:
            # There's code before first function, add as _init
            function_starts.append(0)
            logger.debug(f"Orphan code detected at start, adding _init function at 0")

    function_starts = sorted(set(function_starts))
    logger.debug(f"Function starts (CALL-based): {function_starts}")

    # Step 4: Split at RET boundaries where code after RET is unreachable
    jump_opcodes = resolver.jump_opcodes

    # Resolve entry point for name assignment
    entry_point_resolved = None
    if entry_point is not None:
        if entry_point < 0:
            entry_point_resolved = len(instructions) + entry_point
        else:
            entry_point_resolved = entry_point

    used_names: Set[str] = set()
    final_ranges: List[Tuple[int, int]] = []

    for i, start in enumerate(function_starts):
        if i + 1 < len(function_starts):
            initial_end = function_starts[i + 1] - 1
        else:
            initial_end = len(instructions) - 1

        # Iteratively split this range at unreachable RET boundaries
        current_start = start
        while current_start <= initial_end:
            actual_end = _find_reachable_ret_boundary(
                instructions, current_start, initial_end,
                return_opcodes, jump_opcodes
            )
            final_ranges.append((current_start, actual_end))

            if actual_end >= initial_end:
                break
            current_start = actual_end + 1

    # Step 5: Assign names
    for start, end in sorted(final_ranges):
        if start == entry_point_resolved:
            func_name = "ScriptMain"
        elif start == 0 and start not in call_targets:
            func_name = "_init"
        elif start in saveinfo_names:
            func_name = saveinfo_names[start]
        else:
            func_name = f"func_{start:04d}"

        func_name = _ensure_unique_name(func_name, used_names, start)
        used_names.add(func_name)

        boundaries[func_name] = (start, end)
        logger.debug(f"Function {func_name}: addresses {start} to {end}")

    logger.info(f"Detected {len(boundaries)} functions using RET-based analysis")
    return boundaries


def detect_function_boundaries_call_only(
    scr: SCRFile,
    resolver: OpcodeResolver,
    entry_point: int = None
) -> Dict[str, Tuple[int, int]]:
    """
    Detect function boundaries using only CALL targets (legacy method).

    This is the original algorithm that only considers CALL targets,
    which can miss orphan functions. Kept for backward compatibility.

    Args:
        scr: The parsed SCR file
        resolver: Opcode resolver for the script variant
        entry_point: Optional entry point address

    Returns:
        Dict mapping function_name -> (start_addr, end_addr)
    """
    instructions = scr.code_segment.instructions
    internal_call_opcodes = resolver.internal_call_opcodes

    saveinfo_names = _load_saveinfo_function_names(scr)

    # Find CALL targets
    call_targets = set()
    for instr in instructions:
        if instr.opcode in internal_call_opcodes:
            call_targets.add(instr.arg1)

    # Add entry point
    if entry_point is not None:
        call_targets.add(entry_point)

    sorted_addrs = sorted(call_targets)
    boundaries = {}

    used_names: Set[str] = set()
    for i, start in enumerate(sorted_addrs):
        # End = start of next function - 1, or end of code
        if i + 1 < len(sorted_addrs):
            end = sorted_addrs[i + 1] - 1
        else:
            end = len(instructions) - 1

        # Assign name
        if start == entry_point:
            func_name = "ScriptMain"
        elif start in saveinfo_names:
            func_name = saveinfo_names[start]
        else:
            func_name = f"func_{start:04d}"

        func_name = _ensure_unique_name(func_name, used_names, start)
        used_names.add(func_name)

        boundaries[func_name] = (start, end)

    logger.info(f"Detected {len(boundaries)} functions using CALL-only analysis")
    return boundaries
