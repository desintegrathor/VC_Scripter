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


def _build_xcall_fingerprint(
    scr: SCRFile,
    func_start: int,
    func_end: int
) -> Set[str]:
    """
    Build an XCALL fingerprint for a function: the set of external function
    names called within [func_start, func_end].

    Args:
        scr: The parsed SCR file
        func_start: Start instruction address of the function
        func_end: End instruction address of the function

    Returns:
        Set of external function names (e.g., {"SC_P_IsReady", "SC_GetGroupPlayers"})
    """
    xcall_names = set()
    resolver = scr.opcode_resolver
    instructions = scr.code_segment.instructions

    # Find XCALL opcode
    xcall_opcode = None
    for opcode, mnemonic in resolver.opcode_map.items():
        if mnemonic == "XCALL":
            xcall_opcode = opcode
            break

    if xcall_opcode is None:
        return xcall_names

    xfn_entries = getattr(scr.xfn_table, 'entries', [])

    for instr in instructions:
        if instr.address < func_start or instr.address > func_end:
            continue
        if instr.opcode == xcall_opcode:
            xfn_index = instr.arg1
            if 0 <= xfn_index < len(xfn_entries):
                xfn = xfn_entries[xfn_index]
                if xfn.name:
                    # Extract function name (before parentheses)
                    paren_idx = xfn.name.find('(')
                    func_name = xfn.name[:paren_idx] if paren_idx > 0 else xfn.name
                    xcall_names.add(func_name)

    return xcall_names


def _build_header_xcall_fingerprint(func_body: str) -> Set[str]:
    """
    Build an XCALL fingerprint from a header function's source body.

    Extracts SC_* function calls from the source text.

    Args:
        func_body: Not used — we parse from function signatures instead.
                   The header parser doesn't keep bodies, so we extract
                   SC_* names from the function signature's context.

    Returns:
        Set of external function names found in the header function body.
    """
    # Since the header parser skips bodies, we can't build fingerprints
    # from source text. Instead, we'll match by parameter count only.
    return set()


def _extract_xcalls_from_source(source_text: str, xfn_names: Set[str] = None) -> Set[str]:
    """
    Extract external function call names from C source text.

    Matches SC_* calls by default. If xfn_names is provided, also matches
    any function name present in the XFN table (e.g., rand, sprintf, frnd).

    Args:
        source_text: C source code string
        xfn_names: Optional set of known XFN function names for broader matching

    Returns:
        Set of external function names found in the source
    """
    import re
    # Always match SC_* calls
    pattern = re.compile(r'\b(SC_\w+)\s*\(')
    result = set(pattern.findall(source_text))

    # Also match known XFN names (rand, sprintf, etc.)
    if xfn_names:
        for name in xfn_names:
            if not name.startswith("SC_"):
                # Check if this function is called in the source
                func_pattern = re.compile(r'\b(' + re.escape(name) + r')\s*\(')
                matches = func_pattern.findall(source_text)
                if matches:
                    result.update(matches)

    return result


def _detect_param_count_from_bytecode(
    scr: SCRFile,
    func_start: int,
    func_end: int
) -> int:
    """
    Detect parameter count by looking at the RET instruction's cleanup size.

    In the Vietcong script VM, RET N pops N dwords from the stack frame.
    This N equals the ASP allocation size. The actual parameter count is
    determined by how the function is CALLED (the caller pushes N args
    before CALL), but the callee's LCP offsets to params depend on the
    current stack depth which varies throughout execution.

    Instead of trying to trace stack depth, we use the entry-point ASP
    size and the most negative LCP offset in the function's FIRST FEW
    instructions (before any XCALL/CALL which disrupts the stack).
    After ASP N, the last parameter is always at [sp-3] and the first
    parameter is at [sp-(param_count + 2)].

    Args:
        scr: The parsed SCR file
        func_start: Start instruction address
        func_end: End instruction address

    Returns:
        Detected parameter count (0 if no parameters detected)
    """
    resolver = scr.opcode_resolver
    instructions = scr.code_segment.instructions

    # Build opcode lookup
    opcode_names = {}
    for opcode, mnemonic in resolver.opcode_map.items():
        opcode_names[opcode] = mnemonic

    # Scan LCP instructions, but only BEFORE any XCALL/CALL disrupts the stack.
    # Also track the eval-stack depth from push/pop operations to normalize
    # LCP offsets back to the post-ASP frame.
    asp_size = 0
    eval_depth = 0  # Items pushed onto eval stack since ASP
    min_normalized_offset = 0

    for instr in instructions:
        if instr.address < func_start or instr.address > func_end:
            continue

        mnemonic = opcode_names.get(instr.opcode, "")

        # First instruction is typically ASP
        if instr.address == func_start and mnemonic == "ASP":
            asp_size = instr.arg1
            continue

        # Stop scanning at XCALL/CALL — stack tracking becomes unreliable
        if mnemonic in ("XCALL", "CALL"):
            break

        if mnemonic == "LCP":
            offset = instr.arg1
            if offset >= 0x80000000:
                offset = offset - 0x100000000
            # Normalize: remove eval_depth to get offset relative to post-ASP frame
            normalized = offset + eval_depth
            if normalized < 0 and normalized <= -3:
                if normalized < min_normalized_offset:
                    min_normalized_offset = normalized
            # LCP pushes one value
            eval_depth += 1
        elif mnemonic in ("GCP", "LADR", "GADR", "DADR", "DLD"):
            eval_depth += 1
        elif mnemonic == "LLD":
            eval_depth += 1
        elif mnemonic == "SSP":
            eval_depth -= instr.arg1
        elif mnemonic == "ASGN":
            eval_depth -= 1  # Pops 2 (addr + value), pushes 0
        elif mnemonic == "PNT":
            pass  # Modifies top, no net change
        elif mnemonic in ("ADD", "SUB", "MUL", "DIV", "MOD",
                          "IADD", "ISUB", "IMUL", "IDIV",
                          "EQU", "NEQU", "GRE", "LES", "GEQU", "LEQU"):
            eval_depth -= 1

    if min_normalized_offset < 0:
        return (-min_normalized_offset) - 2

    # Fallback: if no early LCP found (params accessed after XCALL),
    # scan ALL LCP instructions but use the raw minimum offset heuristic
    min_raw = 0
    for instr in instructions:
        if instr.address < func_start or instr.address > func_end:
            continue
        mnemonic = opcode_names.get(instr.opcode, "")
        if mnemonic == "LCP":
            offset = instr.arg1
            if offset >= 0x80000000:
                offset = offset - 0x100000000
            if offset < 0 and offset <= -3:
                if offset < min_raw:
                    min_raw = offset

    if min_raw < 0:
        # Without stack tracking, use raw offset - 2
        # This may be slightly off but provides a useful signal
        return (-min_raw) - 2

    return 0


def match_header_functions(
    scr: SCRFile,
    func_bounds: Dict[str, Tuple[int, int]],
    header_functions: Dict,
    header_source: Optional[str] = None
) -> Dict[str, Dict]:
    """
    Match decompiled func_NNNN functions to header-defined functions
    using XCALL fingerprinting and parameter count matching.

    Matching strategy:
    1. Build XCALL fingerprint (set of SC_* calls) for each decompiled function
    2. Build XCALL fingerprint for each header function from source text
    3. Detect parameter count from bytecode LCP patterns
    4. Match: identical XCALL fingerprint + matching param count → unique match

    Args:
        scr: The parsed SCR file
        func_bounds: Dict mapping function_name -> (start_addr, end_addr)
        header_functions: Dict of header function signatures (from parse_mission_header)
        header_source: Optional raw source text of the header file (for XCALL fingerprinting)

    Returns:
        Dict mapping old_func_name -> {
            'name': new_name,
            'return_type': str,
            'parameters': list,
        }
        Only contains entries where a confident match was found.
    """
    if not header_functions:
        return {}

    rename_map = {}

    # Build XCALL fingerprints AND detect param counts for each decompiled function
    decompiled_fingerprints = {}
    decompiled_param_counts = {}
    for func_name, (start, end) in func_bounds.items():
        # Only try to match func_NNNN names (not ScriptMain, _init, etc.)
        if not func_name.startswith("func_"):
            continue
        fingerprint = _build_xcall_fingerprint(scr, start, end)
        decompiled_fingerprints[func_name] = fingerprint
        decompiled_param_counts[func_name] = _detect_param_count_from_bytecode(scr, start, end)

    # Collect all XFN names from the SCR file (for matching non-SC_* externals like rand)
    all_xfn_names = set()
    xfn_entries = getattr(scr.xfn_table, 'entries', [])
    for xfn in xfn_entries:
        if xfn.name:
            paren_idx = xfn.name.find('(')
            xfn_name = xfn.name[:paren_idx] if paren_idx > 0 else xfn.name
            all_xfn_names.add(xfn_name)

    # Build XCALL fingerprints for header functions (from source text)
    header_fingerprints = {}
    if header_source:
        import re
        # Find function bodies — handle both styles:
        #   RetType FuncName(params)\n{    AND    RetType FuncName(params){
        func_body_pattern = re.compile(
            r'(?:^|\n)\w+\s+\*?(\w+)\s*\([^)]*\)\s*\{',
            re.MULTILINE
        )
        for match in func_body_pattern.finditer(header_source):
            func_name = match.group(1)
            if func_name not in header_functions:
                continue

            # Find the body by brace counting from the '{'
            body_start = match.end() - 1
            brace_count = 1
            pos = body_start + 1
            while pos < len(header_source) and brace_count > 0:
                if header_source[pos] == '{':
                    brace_count += 1
                elif header_source[pos] == '}':
                    brace_count -= 1
                pos += 1

            body_text = header_source[body_start:pos]
            header_fingerprints[func_name] = _extract_xcalls_from_source(
                body_text, all_xfn_names
            )

    # Build header param counts
    header_param_counts = {}
    for func_name, func_data in header_functions.items():
        params = func_data.get('parameters', [])
        # Filter out void-only params
        param_count = len([p for p in params if p[0] != 'void' or p[1]])
        header_param_counts[func_name] = param_count

    def _try_match(decomp_candidates, header_candidates, use_param_filter=True):
        """Try to match decompiled functions to header functions."""
        for decomp_name, decomp_fp in decomp_candidates.items():
            if decomp_name in rename_map:
                continue

            candidates = []
            for header_name, header_fp in header_candidates.items():
                # Skip already-matched header functions
                if any(v['name'] == header_name for v in rename_map.values()):
                    continue

                # Check XCALL fingerprint match
                if decomp_fp != header_fp:
                    continue

                # Filter by parameter count if enabled
                if use_param_filter:
                    decomp_pc = decompiled_param_counts.get(decomp_name, -1)
                    header_pc = header_param_counts.get(header_name, -1)
                    if decomp_pc >= 0 and header_pc >= 0 and decomp_pc != header_pc:
                        continue

                candidates.append(header_name)

            if len(candidates) == 1:
                header_name = candidates[0]
                func_data = header_functions[header_name]
                rename_map[decomp_name] = {
                    'name': header_name,
                    'return_type': func_data.get('return_type', 'dword'),
                    'parameters': func_data.get('parameters', []),
                }

    # Phase 1: Exact XCALL fingerprint match (with param count disambiguation)
    if header_fingerprints:
        _try_match(decompiled_fingerprints, header_fingerprints, use_param_filter=True)

    # Phase 2: Exact XCALL fingerprint match (without param count — for functions
    # where param detection might be inaccurate)
    if header_fingerprints:
        _try_match(
            {k: v for k, v in decompiled_fingerprints.items()
             if k not in rename_map and v},
            {k: v for k, v in header_fingerprints.items()
             if not any(m['name'] == k for m in rename_map.values())},
            use_param_filter=False
        )

    # Phase 3: Fuzzy XCALL match (subset/superset with ≥50% overlap)
    # For functions where the header body calls SC_Log but the compiled code
    # might inline or optimize differently
    if header_fingerprints:
        unmatched_decomp = {
            k: v for k, v in decompiled_fingerprints.items()
            if k not in rename_map and v
        }
        unmatched_header = {
            k: v for k, v in header_fingerprints.items()
            if not any(m['name'] == k for m in rename_map.values()) and v
        }

        for decomp_name, decomp_fp in unmatched_decomp.items():
            candidates = []
            for header_name, header_fp in unmatched_header.items():
                if decomp_fp.issubset(header_fp) or header_fp.issubset(decomp_fp):
                    overlap = len(decomp_fp & header_fp)
                    union = len(decomp_fp | header_fp)
                    if union > 0 and overlap / union >= 0.5:
                        # Also check param count
                        decomp_pc = decompiled_param_counts.get(decomp_name, -1)
                        header_pc = header_param_counts.get(header_name, -1)
                        if decomp_pc >= 0 and header_pc >= 0 and decomp_pc != header_pc:
                            continue
                        candidates.append(header_name)

            if len(candidates) == 1:
                header_name = candidates[0]
                already_matched = any(
                    v['name'] == header_name for v in rename_map.values()
                )
                if not already_matched:
                    func_data = header_functions[header_name]
                    rename_map[decomp_name] = {
                        'name': header_name,
                        'return_type': func_data.get('return_type', 'dword'),
                        'parameters': func_data.get('parameters', []),
                    }

    debug_print(f"DEBUG HEADER MATCH: Matched {len(rename_map)} functions from header")
    for old_name, new_info in sorted(rename_map.items()):
        debug_print(f"  {old_name} -> {new_info['name']}")

    return rename_map


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
