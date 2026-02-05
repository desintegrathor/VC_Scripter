"""
Single-File Decompilation Logic

Extracted from cmd_structure() in __main__.py. Provides a reusable function
for decompiling a single .scr file, used by both the `structure` CLI command
and the `structure-folder` multi-file decompilation.
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path
from typing import Callable, Dict, Optional, Set, Tuple

from .cross_file_context import CrossFileContext


def resolve_mission_header(
    scr_dir: Path,
    header_arg: Optional[str] = None,
) -> Optional[Path]:
    """
    Resolve mission header path from explicit arg or auto-detect.

    Auto-detection: looks for *_H.H files in scr_dir.
    Only auto-uses if exactly one is found.

    Returns:
        Path to header file or None
    """
    if header_arg:
        header_path = Path(header_arg)
        if header_path.exists():
            return header_path
        print(f"Warning: Header file not found: {header_path}", file=sys.stderr)
        return None

    # Auto-detect: look for *_H.H in directory
    candidates = list(scr_dir.glob("*_H.H")) + list(scr_dir.glob("*_h.h"))
    # Deduplicate (case-insensitive filesystem)
    seen = set()
    unique_candidates = []
    for c in candidates:
        key = str(c).lower()
        if key not in seen:
            seen.add(key)
            unique_candidates.append(c)

    if len(unique_candidates) == 1:
        return unique_candidates[0]

    return None


def _detect_float_globals(ssa_func) -> Set[int]:
    """
    Detect float globals from opcode evidence (FADD, FSUB, etc.).

    Returns set of byte offsets for globals used in float operations.
    """
    float_globals = set()
    FLOAT_OPCODES = {
        "FADD", "FSUB", "FMUL", "FDIV", "FMOD", "FNEG",
        "FLES", "FGRE", "FLEQ", "FGEQ", "FNEQ", "FEQ", "FEQU"
    }
    for block_id, instrs in ssa_func.instructions.items():
        for inst in instrs:
            if inst.mnemonic in FLOAT_OPCODES:
                for val in list(inst.inputs) + list(inst.outputs):
                    if val.alias:
                        if val.alias.startswith("data_"):
                            try:
                                dword_idx = int(val.alias.split("_")[1])
                                byte_offset = dword_idx * 4
                                float_globals.add(byte_offset)
                            except (IndexError, ValueError):
                                pass
    return float_globals


def _detect_array_strides(ssa_func, scr) -> Dict[int, Set[int]]:
    """
    Detect multi-dimensional array strides from access patterns.

    Returns: byte_offset -> set of strides
    """
    array_strides: Dict[int, Set[int]] = {}

    def _get_constant_value(value):
        if value is None:
            return None
        if hasattr(value, 'constant_value') and value.constant_value is not None:
            return value.constant_value
        if value.alias and value.alias.lstrip('-').isdigit():
            return int(value.alias)
        if value.alias and value.alias.startswith("data_") and scr.data_segment:
            try:
                offset_idx = int(value.alias[5:])
                return scr.data_segment.get_dword(offset_idx * 4)
            except (ValueError, AttributeError):
                return None
        return None

    for block_id, instrs in ssa_func.instructions.items():
        for inst in instrs:
            if inst.mnemonic == "ADD" and len(inst.inputs) >= 2:
                left = inst.inputs[0]
                right = inst.inputs[1]

                base_offset = None
                mul_val = None

                for candidate_base, candidate_mul in [(left, right), (right, left)]:
                    if candidate_base.alias and candidate_base.alias.startswith("&data_"):
                        try:
                            dword_idx = int(candidate_base.alias.split("_")[1])
                            base_offset = dword_idx * 4
                            mul_val = candidate_mul
                            break
                        except (IndexError, ValueError):
                            pass

                if base_offset is not None and mul_val is not None:
                    if mul_val.producer_inst and mul_val.producer_inst.mnemonic in {"MUL", "IMUL"}:
                        mul_inst = mul_val.producer_inst
                        if len(mul_inst.inputs) >= 2:
                            for mul_inp in mul_inst.inputs:
                                stride = _get_constant_value(mul_inp)
                                if stride and stride > 0:
                                    if base_offset not in array_strides:
                                        array_strides[base_offset] = set()
                                    array_strides[base_offset].add(stride)

    return array_strides


def decompile_single_scr(
    scr_path: Path,
    args,
    cross_file_context: Optional[CrossFileContext] = None,
    header_path: Optional[Path] = None,
    header_already_loaded: bool = False,
    progress_callback: Optional[Callable[[str], None]] = None,
) -> str:
    """
    Decompile a single .scr file and return the decompiled C source as a string.

    This is the core decompilation logic extracted from cmd_structure().

    Args:
        scr_path: Path to the .scr file
        args: Parsed CLI arguments (must have variant, debug/verbose, legacy_ssa, etc.)
        cross_file_context: Optional cross-file context for multi-file decompilation
        header_path: Optional mission header path (overrides auto-detection)
        header_already_loaded: Whether the header has already been loaded
        progress_callback: Optional callback for progress updates (receives status messages)

    Returns:
        The decompiled C source code as a string
    """
    def _progress(msg: str):
        if progress_callback:
            progress_callback(msg)
    from ..loader import SCRFile
    from .structure import format_structured_function_named
    from .ssa import build_ssa_all_blocks, build_ssa_incremental
    from ..headers.detector import generate_include_block
    from .global_resolver import GlobalResolver
    from .debug_output import set_debug_enabled

    # Debug output
    debug_mode = getattr(args, 'debug', False) or getattr(args, 'verbose', False)
    set_debug_enabled(debug_mode)

    _progress("Loading bytecode...")
    scr = SCRFile.load(str(scr_path), variant=getattr(args, 'variant', 'auto'))

    # Set flags on SCR object
    scr.enable_simplify = not getattr(args, 'no_simplify', False)
    scr.debug_simplify = getattr(args, 'debug_simplify', False)
    scr.enable_array_detection = not getattr(args, 'no_array_detection', False)
    scr.debug_array_detection = getattr(args, 'debug_array_detection', False)
    scr.enable_bidirectional_types = not getattr(args, 'no_bidirectional_types', False)
    scr.debug_type_inference = getattr(args, 'debug_type_inference', False)

    _progress("Analyzing functions...")
    from ..disasm import Disassembler
    disasm = Disassembler(scr)
    func_bounds = disasm.get_function_boundaries_v2()

    # Mission header support
    if header_path is None:
        header_arg = getattr(args, 'header', None)
        header_path = resolve_mission_header(scr_path.parent, header_arg)

    if header_path and not header_already_loaded:
        from ..headers.database import get_header_database as _get_hdb
        from ..constants import _reset_constants
        hdb = _get_hdb()
        hdb.load_mission_header(header_path)
        _reset_constants()
        if debug_mode:
            print(f"// Mission header loaded: {header_path.name}", file=sys.stderr)

    # Build SSA
    _progress("Building SSA...")
    use_legacy_ssa = getattr(args, 'legacy_ssa', False)
    heritage_metadata = None
    if not use_legacy_ssa:
        ssa_func, heritage_metadata = build_ssa_incremental(scr, return_metadata=True)
        if debug_mode:
            print(f"// Using incremental heritage SSA construction", file=sys.stderr)
            print(f"// Heritage: {len(heritage_metadata.get('variables', {}))} variables, "
                  f"{sum(len(v) for v in heritage_metadata.get('phi_blocks', {}).values())} PHI nodes",
                  file=sys.stderr)
    else:
        ssa_func = build_ssa_all_blocks(scr)
        if debug_mode:
            print(f"// Using legacy single-pass SSA construction", file=sys.stderr)

    # Mission header: match decompiled functions to header-defined functions
    if header_path:
        from .function_detector import match_header_functions
        header_source_text = header_path.read_text(encoding='latin-1')
        from ..headers.database import get_header_database as _get_hdb2
        hdb2 = _get_hdb2()
        rename_map = match_header_functions(
            scr, func_bounds, hdb2.mission_functions, header_source_text
        )
        # Store full header match data (params + return type) on SCR object
        # so orchestrator.py can override detected signatures
        scr._header_function_signatures = {}
        for old_name, new_info in rename_map.items():
            scr._header_function_signatures[new_info['name']] = new_info
            if old_name in func_bounds:
                func_bounds[new_info['name']] = func_bounds.pop(old_name)
        if debug_mode and rename_map:
            print(f"// Renamed {len(rename_map)} functions from header", file=sys.stderr)

    # Build output
    output_parts = []

    output_parts.append(f"// Structured decompilation of {scr_path.name}")
    output_parts.append(f"// Functions: {len(func_bounds)}")
    output_parts.append("")

    # Generate #include block
    include_block = generate_include_block(scr)
    output_parts.append(include_block)
    output_parts.append("")

    # Detect float globals
    float_globals = _detect_float_globals(ssa_func)

    # Detect array strides
    array_strides = _detect_array_strides(ssa_func, scr)

    # Resolve globals
    _progress("Resolving globals...")
    resolver = GlobalResolver(
        ssa_func,
        aggressive_typing=True,
        infer_structs=False,
        cross_file_context=cross_file_context,
    )
    globals_usage = resolver.analyze()

    # Inject cross-file-enriched globals into SSA cache so that expr.py
    # (which calls resolve_globals_with_types()) uses the same data
    ssa_func._cached_global_type_info_bytes = globals_usage

    # Build SaveInfo size mapping
    saveinfo_sizes = {}
    if scr.save_info:
        for item in scr.save_info.items:
            byte_offset = item['val1'] * 4
            size_dwords = item['val2']
            saveinfo_sizes[byte_offset] = size_dwords

    from ..headers.database import get_header_database
    from ..structures import get_struct_by_name
    header_db = get_header_database()

    def _format_dim_value(dim: int) -> str:
        if header_db:
            names = header_db.get_constant_names_by_value(dim)
            if names:
                max_names = [name for name in names if name.endswith("_MAX")]
                if max_names:
                    return max_names[0]
        return str(dim)

    def _infer_element_size(var_type: str) -> Optional[int]:
        if var_type.endswith("*"):
            return 4
        struct_def = get_struct_by_name(var_type)
        if struct_def:
            return struct_def.size
        type_sizes = {
            "char": 1, "short": 2, "int": 4, "float": 4,
            "double": 8, "dword": 4, "BOOL": 4,
        }
        return type_sizes.get(var_type, None)

    def _infer_array_dimensions(offset: int, total_dwords: int, element_size: int) -> Optional[list]:
        if offset not in array_strides:
            return None
        strides = sorted(array_strides[offset], reverse=True)
        if not strides:
            return None
        if not element_size or not any(stride > element_size for stride in strides):
            return None
        total_bytes = total_dwords * 4
        num_elements = total_bytes // element_size if element_size else total_dwords

        dimensions = []
        for stride in strides:
            if element_size and stride >= element_size:
                inner_dim = stride // element_size
                if inner_dim > 0 and num_elements % inner_dim == 0:
                    dimensions.append(inner_dim)
                    num_elements //= inner_dim

        if num_elements > 1:
            dimensions.insert(0, num_elements)

        if dimensions:
            product = 1
            for d in dimensions:
                product *= d
            expected = total_bytes // element_size if element_size else total_dwords
            if product != expected:
                return None

        return dimensions if len(dimensions) > 1 else None

    # Generate global variable declarations
    if globals_usage:
        global_lines = []
        global_lines.append("// Global variables")
        for offset in sorted(globals_usage.keys()):
            usage = globals_usage[offset]
            if usage.is_array_element:
                continue
            if usage.write_count == 0 and not usage.name.startswith("g"):
                continue
            if usage.source in ("SGI_constant", "SGI_runtime"):
                continue

            # Determine type
            if offset in float_globals:
                var_type = "float"
            elif usage.inferred_type:
                var_type = usage.inferred_type
            elif usage.header_type:
                var_type = usage.header_type
            elif usage.is_incremented or usage.is_decremented:
                var_type = "int"
            elif usage.possible_types:
                var_type = list(usage.possible_types)[0]
            else:
                var_type = "dword"

            # SDK type mapping
            if var_type in {"int", "dword"} and usage.is_array_base and usage.array_element_size:
                from ..structures import get_struct_by_size
                name_hints = {
                    "recover": "s_SC_MP_Recover",
                    "rec": "s_SC_MP_Recover",
                    "sphere": "s_sphere",
                    "vec": "c_Vector3",
                    "vector": "c_Vector3",
                }
                candidates = get_struct_by_size(usage.array_element_size)
                if candidates:
                    if len(candidates) == 1:
                        var_type = candidates[0].name
                    elif usage.name:
                        name_lower = usage.name.lower()
                        for hint, struct_name in name_hints.items():
                            if hint in name_lower:
                                for candidate in candidates:
                                    if candidate.name == struct_name:
                                        var_type = candidate.name
                                        break
                            if var_type not in {"int", "dword"}:
                                break

            # Float init detection from data segment
            detected_float_init = False
            if var_type in {"int", "dword"} and scr.data_segment:
                dword_idx = offset // 4
                if dword_idx < scr.data_segment.data_count:
                    from .expr import _is_likely_float
                    init_value = scr.data_segment.get_dword(offset)
                    if init_value != 0 and _is_likely_float(init_value):
                        var_type = "float"
                        detected_float_init = True

            var_name = usage.name if usage.name else f"data_{offset}"

            # SaveInfo array detection
            size_dwords = saveinfo_sizes.get(offset, 1)
            is_array = size_dwords > 1

            element_type = var_type
            element_size = usage.array_element_size or _infer_element_size(element_type)

            if is_array and element_type.endswith("*") and element_size and element_size != 4:
                element_type = element_type.replace(" *", "").rstrip("*").strip()
                element_size = _infer_element_size(element_type)

            # Format initializer
            if var_type == "float" and scr.data_segment:
                init_value = scr.data_segment.get_dword(offset)
                float_val = struct.unpack('<f', struct.pack('<I', init_value & 0xFFFFFFFF))[0]
                if float_val == 0.0:
                    initializer = " = 0.0f"
                elif float_val == int(float_val):
                    initializer = f" = {int(float_val)}.0f"
                else:
                    initializer = f" = {float_val}f"
            else:
                initializer = f" = {usage.initializer}" if usage.initializer else ""

            # Format declaration
            if is_array:
                if usage.array_dimensions:
                    dim_text = "".join(f"[{_format_dim_value(dim)}]" for dim in usage.array_dimensions)
                    global_lines.append(f"{element_type} {var_name}{dim_text}{initializer};")
                else:
                    inferred_dims = _infer_array_dimensions(offset, size_dwords, element_size or 4)
                    if inferred_dims:
                        dim_text = "".join(f"[{_format_dim_value(dim)}]" for dim in inferred_dims)
                        global_lines.append(f"{element_type} {var_name}{dim_text}{initializer};")
                    else:
                        array_size = size_dwords
                        if element_size and element_size > 0:
                            total_bytes = size_dwords * 4
                            if total_bytes % element_size == 0:
                                array_size = total_bytes // element_size
                        global_lines.append(f"{element_type} {var_name}[{array_size}]{initializer};")
            elif usage.is_array_base and usage.array_element_size:
                array_size = 64
                global_lines.append(f"{var_type} {var_name}[{array_size}]{initializer};")
            else:
                global_lines.append(f"{var_type} {var_name}{initializer};")

        global_lines.append("")
        output_parts.extend(global_lines)

    # Format functions
    style = 'normal' if debug_mode else 'quiet'
    use_collapse = not getattr(args, 'no_collapse', False)

    if not use_collapse and debug_mode:
        print(f"// Using flat mode (collapse disabled)", file=sys.stderr)

    def _is_trivial_init_function(func_text: str) -> bool:
        lines = func_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('void _init(') or line.startswith('dword _init('):
                continue
            if line in ('{', '}'):
                continue
            if ';' in line and not '(' in line and not '=' in line:
                continue
            if line.startswith('//'):
                continue
            if line == 'return;':
                continue
            return False
        return True

    sorted_funcs = sorted(func_bounds.items(), key=lambda x: x[1][0])
    total_funcs = len(sorted_funcs)

    for idx, (func_name, (func_start, func_end)) in enumerate(sorted_funcs, 1):
        _progress(f"Function {idx}/{total_funcs}: {func_name}")
        text = format_structured_function_named(
            ssa_func,
            func_name,
            func_start,
            func_end,
            function_bounds=func_bounds,
            style=style,
            heritage_metadata=heritage_metadata,
            use_collapse=use_collapse
        )

        if func_name == "_init" and _is_trivial_init_function(text):
            continue

        output_parts.append(text)
        output_parts.append("")

    return "\n".join(output_parts)


def run_pass1_analysis(scr_path: Path, args) -> Tuple:
    """
    Run Pass 1 analysis on a single .scr file for cross-file context building.

    Returns:
        Tuple of (scr, globals_usage, float_globals) - lightweight data for
        cross-file context merging. Does not keep the full SSA graph in memory.
    """
    from ..loader import SCRFile
    from .ssa import build_ssa_all_blocks, build_ssa_incremental
    from .global_resolver import GlobalResolver
    from .debug_output import set_debug_enabled

    debug_mode = getattr(args, 'debug', False) or getattr(args, 'verbose', False)
    set_debug_enabled(debug_mode)

    scr = SCRFile.load(str(scr_path), variant=getattr(args, 'variant', 'auto'))

    # Set flags
    scr.enable_simplify = not getattr(args, 'no_simplify', False)
    scr.debug_simplify = getattr(args, 'debug_simplify', False)
    scr.enable_array_detection = not getattr(args, 'no_array_detection', False)
    scr.debug_array_detection = getattr(args, 'debug_array_detection', False)
    scr.enable_bidirectional_types = not getattr(args, 'no_bidirectional_types', False)
    scr.debug_type_inference = getattr(args, 'debug_type_inference', False)

    # Build SSA (use legacy for speed in pass1 - we just need globals)
    use_legacy_ssa = getattr(args, 'legacy_ssa', False)
    if not use_legacy_ssa:
        ssa_func, _ = build_ssa_incremental(scr, return_metadata=True)
    else:
        ssa_func = build_ssa_all_blocks(scr)

    # Detect float globals
    float_globals = _detect_float_globals(ssa_func)

    # Run global resolver (without cross-file context in pass 1)
    resolver = GlobalResolver(
        ssa_func,
        aggressive_typing=True,
        infer_structs=False,
    )
    globals_usage = resolver.analyze()

    # Return lightweight data (not the full SSA graph)
    return scr, globals_usage, float_globals
