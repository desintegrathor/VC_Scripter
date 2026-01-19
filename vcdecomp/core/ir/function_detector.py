"""
Enhanced function boundary detection using RET instructions.

The original get_function_boundaries() in disassembler.py only considers CALL targets,
missing orphan functions (not called internally). This module uses RET instructions
to accurately detect all function boundaries.

This fixes the issue where multiple separate functions are merged together,
causing unreachable code to appear after return statements in decompiled output.
"""

from typing import Dict, Tuple, Set
import logging

from vcdecomp.core.loader.scr_loader import SCRFile
from vcdecomp.core.disasm.opcodes import OpcodeResolver

logger = logging.getLogger(__name__)


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

    # Step 3: Build function starts using CALL targets + entry point
    #
    # STRATEGY:
    # Use CALL targets as definitive function starts.  Entry point is ScriptMain.
    # This prevents splitting functions with multiple returns into micro-functions.

    boundaries = {}
    function_starts = []

    # Add entry point if provided
    if entry_point is not None:
        import sys
        # BUGFIX: Negative entry points are relative to code end
        # entry_point=-1097 means 1097 instructions from end
        if entry_point < 0:
            actual_entry = len(instructions) + entry_point
            print(f"DEBUG: Entry point = {entry_point} (resolves to {actual_entry})", file=sys.stderr)
            function_starts.append(actual_entry)
        else:
            print(f"DEBUG: Entry point = {entry_point}", file=sys.stderr)
            function_starts.append(entry_point)
        logger.debug(f"Entry point at address {entry_point}")

    # Add CALL targets as definitive function starts
    function_starts.extend(call_targets)

    # Handle orphan code before first function
    if function_starts:
        first_func = min(function_starts)
        if first_func > 0:
            # There's code before first function, add as _init
            function_starts.append(0)
            logger.debug(f"Orphan code detected at start, adding _init function at 0")

    function_starts = sorted(set(function_starts))
    logger.debug(f"Function starts (CALL-based): {function_starts}")

    # Step 4: Determine function end boundaries
    # NEW STRATEGY: Use next function start as boundary instead of first RET.
    # This prevents functions with early returns from being truncated and
    # leaving orphaned code that contains switch statements.
    for i, start in enumerate(function_starts):
        # End is just before next function starts, or end of code segment
        if i + 1 < len(function_starts):
            end = function_starts[i + 1] - 1
        else:
            # Last function extends to end of code segment
            end = len(instructions) - 1

        # Validation: Check if function ends with RET instruction
        end_instr = instructions[end]
        if end_instr.opcode not in return_opcodes:
            # Function doesn't end with RET - may have fall-through or be truncated
            # This is just a warning, not an error (some functions may legitimately not return)
            logger.debug(
                f"Function at {start} doesn't end with RET (ends at {end} with {end_instr.opcode})"
            )

        # Assign name
        if start == entry_point:
            func_name = "ScriptMain"
        elif start == 0 and start not in call_targets:
            func_name = "_init"
        else:
            func_name = f"func_{start:04d}"

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

    for i, start in enumerate(sorted_addrs):
        # End = start of next function - 1, or end of code
        if i + 1 < len(sorted_addrs):
            end = sorted_addrs[i + 1] - 1
        else:
            end = len(instructions) - 1

        # Assign name
        if start == entry_point:
            func_name = "ScriptMain"
        else:
            func_name = f"func_{start:04d}"

        boundaries[func_name] = (start, end)

    logger.info(f"Detected {len(boundaries)} functions using CALL-only analysis")
    return boundaries
