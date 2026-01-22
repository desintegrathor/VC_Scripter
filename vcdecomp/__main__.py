"""
VC Script Decompiler - CLI Entry Point

Použití:
    python -m vcdecomp info <file.scr>                           # Zobrazí info o souboru
    python -m vcdecomp disasm <file.scr>                         # Disassembly
    python -m vcdecomp strings <file.scr>                        # Seznam stringů
    python -m vcdecomp validate <orig.scr> <src.c>               # Validace rekompilace
    python -m vcdecomp validate-batch --input-dir ... --original-dir ...  # Batch validace
    python -m vcdecomp gui [file.scr]                            # Otevře GUI
"""

import argparse
import json
import sys
import io
from pathlib import Path
from typing import Optional

from .core.disasm import Disassembler
from .core.ir.cfg import build_cfg
from .core.ir.stack_lifter import lift_function
from .core.ir.ssa import build_ssa
from .core.ir.expr import format_block_expressions
from .core.ir.structure import format_structured_function

# Fix pro Windows konzoli - force UTF-8 output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


VARIANT_CHOICES = ["auto", "runtime", "compiler"]


def cmd_info(args):
    """Zobrazí informace o SCR souboru"""
    from .core.loader import SCRFile

    scr = SCRFile.load(args.file, variant=args.variant)
    print(scr.info())


def cmd_disasm(args):
    """Disassembluje SCR soubor"""
    from .core.loader import SCRFile

    scr = SCRFile.load(args.file, variant=args.variant)
    disasm = Disassembler(scr)
    print(disasm.to_string())


def cmd_strings(args):
    """Zobrazí stringy z data segmentu"""
    from .core.loader import SCRFile

    scr = SCRFile.load(args.file, variant=args.variant)

    print(f"Strings in {args.file}:")
    print("=" * 60)

    for offset, s in sorted(scr.data_segment.strings.items()):
        escaped = s.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
        if len(escaped) > 60:
            escaped = escaped[:57] + "..."
        print(f"[{offset:6d}] \"{escaped}\"")

    print("=" * 60)
    print(f"Total: {len(scr.data_segment.strings)} strings")


def cmd_hex(args):
    """Zobrazí hex dump souboru"""
    from .core.loader import SCRFile

    scr = SCRFile.load(args.file, variant=args.variant)
    data = scr.raw_data

    # Omezíme délku
    limit = args.limit if args.limit else len(data)
    offset = args.offset if args.offset else 0

    print(f"Hex dump of {args.file} (offset={offset}, limit={limit}):")
    print("=" * 75)

    for i in range(offset, min(offset + limit, len(data)), 16):
        # Adresa
        line = f"{i:08x}  "

        # Hex bytes
        hex_part = ""
        ascii_part = ""
        for j in range(16):
            if i + j < len(data):
                b = data[i + j]
                hex_part += f"{b:02x} "
                ascii_part += chr(b) if 32 <= b < 127 else "."
            else:
                hex_part += "   "
                ascii_part += " "

            if j == 7:
                hex_part += " "

        print(f"{line}{hex_part} |{ascii_part}|")


def cmd_cfg(args):
    """Vytvoří přehled základních bloků a jejich hran"""
    from .core.loader import SCRFile

    scr = SCRFile.load(args.file, variant=args.variant)
    cfg = build_cfg(scr)

    print(f"CFG for {args.file}")
    print(f"Instructions: {scr.code_segment.code_count}")
    print(f"Blocks: {len(cfg.blocks)} (entry={cfg.entry_block})")
    print("")
    for block_id in sorted(cfg.blocks):
        block = cfg.blocks[block_id]
        instr_range = f"{block.start:04d}-{block.end:04d}"
        succ = ", ".join(str(s) for s in sorted(block.successors)) or "-"
        print(f"Block {block_id:03d} [{instr_range}] -> {succ}")


def cmd_lift(args):
    """Vypíše simulaci zásobníku pro blok"""
    from .core.loader import SCRFile

    scr = SCRFile.load(args.file, variant=args.variant)
    resolver = scr.opcode_resolver
    cfg, lifted = lift_function(scr, resolver)

    block_id = args.block if args.block is not None else cfg.entry_block
    block = cfg.blocks.get(block_id)
    block_instrs = lifted.get(block_id)
    if block is None or block_instrs is None:
        print(f"Block {block_id} not found")
        return

    print(f"Lifted block {block_id} [{block.start:04d}-{block.end:04d}] in {args.file}")
    in_stack = getattr(block, "_in_stack", [])
    if in_stack:
        print("Stack before block:", ", ".join(f"{v.name}:{v.value_type.name}" for v in in_stack))
    print("")
    for inst in block_instrs:
        mnemonic = resolver.get_mnemonic(inst.instruction.opcode)
        inputs = ", ".join(v.name for v in inst.inputs) or "-"
        outputs = ", ".join(v.name for v in inst.outputs) or "-"
        print(f"{inst.instruction.address:04d}: {mnemonic:8s} | in: {inputs} -> out: {outputs}")

    out_stack = getattr(block, "_out_stack", [])
    if out_stack:
        print("")
        print("Stack after block:", ", ".join(f"{v.name}:{v.value_type.name}" for v in out_stack))


def cmd_gui(args):
    """Spustí GUI aplikaci"""
    try:
        from .gui.main_window import run_gui
        run_gui(args.file if args.file else None)
    except ImportError as e:
        print(f"Error: GUI dependencies not installed.")
        print(f"Install with: pip install PyQt6")
        print(f"Details: {e}")
        sys.exit(1)


def _add_variant_option(subparser):
    subparser.add_argument(
        '--variant',
        choices=VARIANT_CHOICES,
        default='auto',
        help='Volba opcode mapy: auto (detekce), runtime, nebo compiler'
    )


def main():
    parser = argparse.ArgumentParser(
        prog='vcdecomp',
        description='VC Script Decompiler - Dekompilátor pro Vietcong skripty (.SCR)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Příklady:
    python -m vcdecomp info level.scr
    python -m vcdecomp disasm level.scr > output.asm
    python -m vcdecomp strings level.scr
    python -m vcdecomp validate original.scr decompiled.c
    python -m vcdecomp validate original.scr decompiled.c --report-file report.html
    python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --jobs 8
    python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --report-file batch_report.json
    python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --save-baseline
    python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --regression
    python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --regression --report-file regression.json
    python -m vcdecomp gui level.scr
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Dostupné příkazy')

    # info
    p_info = subparsers.add_parser('info', help='Zobrazí informace o SCR souboru')
    p_info.add_argument('file', help='Cesta k SCR souboru')
    _add_variant_option(p_info)

    # disasm
    p_disasm = subparsers.add_parser('disasm', help='Disassembluje SCR soubor')
    p_disasm.add_argument('file', help='Cesta k SCR souboru')
    _add_variant_option(p_disasm)

    # strings
    p_strings = subparsers.add_parser('strings', help='Zobrazí stringy z data segmentu')
    p_strings.add_argument('file', help='Cesta k SCR souboru')
    _add_variant_option(p_strings)

    # hex
    p_hex = subparsers.add_parser('hex', help='Zobrazí hex dump souboru')
    p_hex.add_argument('file', help='Cesta k SCR souboru')
    p_hex.add_argument('-o', '--offset', type=int, default=0, help='Počáteční offset')
    p_hex.add_argument('-l', '--limit', type=int, default=256, help='Počet bytů')
    _add_variant_option(p_hex)

    # lift
    p_lift = subparsers.add_parser('lift', help='Simuluje zásobník v bloku')
    p_lift.add_argument('file', help='Cesta k SCR souboru')
    p_lift.add_argument('-b', '--block', type=int, help='ID základního bloku (default entry)')
    _add_variant_option(p_lift)

    # cfg
    p_cfg = subparsers.add_parser('cfg', help='Vytvoří CFG přehled')
    p_cfg.add_argument('file', help='Cesta k SCR souboru')
    _add_variant_option(p_cfg)

    # ssa
    p_ssa = subparsers.add_parser('ssa', help='Zobrazí SSA IR pro blok')
    p_ssa.add_argument('file', help='Cesta k SCR souboru')
    p_ssa.add_argument('-b', '--block', type=int, help='ID bloku (default entry)')
    _add_variant_option(p_ssa)

    # expr
    p_expr = subparsers.add_parser('expr', help='Vypíše výrazovou formu SSA bloku')
    p_expr.add_argument('file', help='Cesta k SCR souboru')
    p_expr.add_argument('-b', '--block', type=int, help='ID bloku (default entry)')
    p_expr.add_argument('--all', action='store_true', help='Zpracuje všechny bloky/funkce')
    p_expr.add_argument('--show-mnemonics', action='store_true', help='Připojí původní mnemonic jako komentář')
    _add_variant_option(p_expr)

    # structure
    p_structure = subparsers.add_parser('structure', help='Strukturovaná dekompilace všech funkcí')
    p_structure.add_argument('file', help='Cesta k SCR souboru')
    p_structure.add_argument(
        '--debug', '-d',
        action='store_true',
        default=False,
        help='Enable DEBUG output to stderr (for development/debugging)'
    )
    p_structure.add_argument(
        '--verbose', '-v',
        action='store_true',
        default=False,
        help='Enable verbose DEBUG output (same as --debug, for future expansion)'
    )
    p_structure.add_argument(
        '--legacy-ssa',
        action='store_true',
        default=False,
        help='Use legacy single-pass SSA construction (faster but lower quality)'
    )
    _add_variant_option(p_structure)

    # symbols
    p_symbols = subparsers.add_parser('symbols', help='Export global variable symbol table')
    p_symbols.add_argument('file', help='Cesta k SCR souboru')
    p_symbols.add_argument('-o', '--output', required=True, help='Output file path')
    p_symbols.add_argument('-f', '--format', choices=['json', 'header', 'markdown'], default='json',
                          help='Export format (default: json)')
    _add_variant_option(p_symbols)

    # validate
    p_validate = subparsers.add_parser('validate', help='Validate decompiled source by recompiling')
    p_validate.add_argument('original_scr', help='Path to original .SCR file')
    p_validate.add_argument('source_file', help='Path to decompiled source .c file')
    p_validate.add_argument('--compiler-dir', help='Path to compiler directory (default: original-resources/compiler)')
    p_validate.add_argument('--output-format', choices=['text', 'json', 'html'],
                           help='Output format for report (default: auto-detect from --report-file or text)')
    p_validate.add_argument('--report-file', help='Save detailed report to file')
    p_validate.add_argument('--no-cache', action='store_true', help='Disable validation cache')
    p_validate.add_argument('--no-color', action='store_true', help='Disable colored output')

    # validate-batch
    p_validate_batch = subparsers.add_parser('validate-batch', help='Validate multiple files in batch mode')
    p_validate_batch.add_argument('--input-dir', required=True, help='Directory containing decompiled .c files')
    p_validate_batch.add_argument('--original-dir', required=True, help='Directory containing original .scr files')
    p_validate_batch.add_argument('--compiler-dir', help='Path to compiler directory (default: original-resources/compiler)')
    p_validate_batch.add_argument('--jobs', type=int, default=4, help='Number of parallel validation jobs (default: 4)')
    p_validate_batch.add_argument('--report-file', help='Save batch summary report to JSON file')
    p_validate_batch.add_argument('--no-cache', action='store_true', help='Disable validation cache')
    p_validate_batch.add_argument('--save-baseline', action='store_true', help='Save current results as baseline for regression testing')
    p_validate_batch.add_argument('--regression', action='store_true', help='Compare results against baseline to detect regressions')
    p_validate_batch.add_argument('--baseline-file', help='Path to baseline file (default: .validation-baseline.json)')

    # gui
    p_gui = subparsers.add_parser('gui', help='Spustí GUI aplikaci')
    p_gui.add_argument('file', nargs='?', help='Cesta k SCR souboru (volitelné)')

    # xfn-aggregate
    p_xfn = subparsers.add_parser('xfn-aggregate', help='Aggregate XFN function signatures from .scr files')
    p_xfn.add_argument('directory', help='Directory containing .scr files to scan')
    p_xfn.add_argument('-f', '--format', choices=['summary', 'sdk', 'json'],
                      default='summary', help='Output format (default: summary)')
    p_xfn.add_argument('-o', '--output', help='Output file path (required for sdk/json formats)')
    p_xfn.add_argument('--no-recursive', action='store_true', help='Do not scan subdirectories')
    p_xfn.add_argument('--merge-sdk', action='store_true',
                      help='Merge with existing SDK functions.json')
    p_xfn.add_argument('--sdk-path', help='Path to SDK functions.json (default: vcdecomp/sdk/data/functions.json)')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'info':
            cmd_info(args)
        elif args.command == 'disasm':
            cmd_disasm(args)
        elif args.command == 'strings':
            cmd_strings(args)
        elif args.command == 'hex':
            cmd_hex(args)
        elif args.command == 'lift':
            cmd_lift(args)
        elif args.command == 'cfg':
            cmd_cfg(args)
        elif args.command == 'ssa':
            cmd_ssa(args)
        elif args.command == 'expr':
            cmd_expr(args)
        elif args.command == 'structure':
            cmd_structure(args)
        elif args.command == 'symbols':
            cmd_symbols(args)
        elif args.command == 'validate':
            cmd_validate(args)
        elif args.command == 'validate-batch':
            cmd_validate_batch(args)
        elif args.command == 'gui':
            cmd_gui(args)
        elif args.command == 'xfn-aggregate':
            cmd_xfn_aggregate(args)
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise  # Pro debugging
        sys.exit(1)


def cmd_ssa(args):
    """Vypíše SSA pohled na blok"""
    from .core.loader import SCRFile

    scr = SCRFile.load(args.file, variant=args.variant)
    ssa_func = build_ssa(scr)

    block_id = args.block if args.block is not None else ssa_func.cfg.entry_block
    block_instrs = ssa_func.instructions.get(block_id)
    if block_instrs is None:
        print(f"Block {block_id} not found")
        return

    print(f"SSA block {block_id} in {args.file}")

    block = ssa_func.cfg.blocks.get(block_id)
    if block:
        in_stack = getattr(block, "_in_stack", [])
        phi_values = [val for val in in_stack if getattr(val, "phi_sources", None)]
        if phi_values:
            print("Phi values:")
            for val in phi_values:
                sources = ", ".join(f"b{pred}:{src.name}" for pred, src in (val.phi_sources or []))
                print(f"  {val.name} <- {sources}")
            print("")

    print("")
    for inst in block_instrs:
        addr = inst.address
        addr_str = f"{addr:04d}" if addr >= 0 else f"phi{abs(addr)}"
        inputs = ", ".join(f"{val.name}:{val.value_type.name}" for val in inst.inputs) or "-"
        outputs = ", ".join(f"{val.name}:{val.value_type.name}" for val in inst.outputs) or "-"
        print(f"{addr_str}: {inst.mnemonic:8s} | in: {inputs} -> out: {outputs}")


def cmd_expr(args):
    """Vytvoří expresní dump pro blok"""
    from .core.loader import SCRFile
    from .core.ir.ssa import build_ssa_all_blocks

    scr = SCRFile.load(args.file, variant=args.variant)
    disasm = Disassembler(scr)
    func_bounds = disasm.get_function_boundaries()

    # Mapování adresa -> název funkce
    addr_to_func = {}
    for func_name, (start, end) in func_bounds.items():
        for addr in range(start, end + 1):
            addr_to_func[addr] = func_name

    if args.all:
        # Použij build_ssa_all_blocks pro zpracování všech bloků
        ssa_func = build_ssa_all_blocks(scr)

        # Zpracuj všechny bloky seskupené podle funkcí
        print(f"; Expressions for all functions in {args.file}")
        print(f"; Total blocks: {len(ssa_func.cfg.blocks)}")
        print(f"; Functions: {len(func_bounds)}")
        print()

        current_func = None
        for block_id in sorted(ssa_func.cfg.blocks.keys()):
            block = ssa_func.cfg.blocks.get(block_id)
            if block:
                func_name = addr_to_func.get(block.start, "unknown")
                if func_name != current_func:
                    if current_func is not None:
                        print("}\n")
                    print(f"// === {func_name} ===")
                    print(f"void {func_name}(void) {{")
                    current_func = func_name

            expressions = format_block_expressions(ssa_func, block_id)
            if expressions:
                print(f"    // Block {block_id} @{block.start if block else '?'}")
                for expr in expressions:
                    if args.show_mnemonics:
                        addr = f"{expr.address:04d}" if expr.address >= 0 else f"phi{abs(expr.address)}"
                        print(f"    {expr.text}    // {expr.mnemonic} @{addr}")
                    else:
                        print(f"    {expr.text}")

        if current_func is not None:
            print("}")
    else:
        # Původní chování - jeden blok
        ssa_func = build_ssa(scr)
        block_id = args.block if args.block is not None else ssa_func.cfg.entry_block
        expressions = format_block_expressions(ssa_func, block_id)

        print(f"Expressions for block {block_id} in {args.file}")
        if not expressions:
            print("(no instructions)")
            return

        for expr in expressions:
            if args.show_mnemonics:
                addr = f"{expr.address:04d}" if expr.address >= 0 else f"phi{abs(expr.address)}"
                print(f"{expr.text}    # {expr.mnemonic} @{addr}")
            else:
                print(expr.text)


def cmd_structure(args):
    """Strukturovaný výstup - dekompilace všech funkcí"""
    from .core.loader import SCRFile
    from .core.ir.structure import format_structured_function_named
    from .core.ir.ssa import build_ssa_all_blocks, build_ssa_incremental
    from .core.headers.detector import generate_include_block
    from .core.ir.global_resolver import GlobalResolver
    from .core.ir.debug_output import set_debug_enabled

    # Debug output: OFF by default, enable with --debug or --verbose
    debug_mode = getattr(args, 'debug', False) or getattr(args, 'verbose', False)
    set_debug_enabled(debug_mode)

    scr = SCRFile.load(args.file, variant=args.variant)
    disasm = Disassembler(scr)

    # Use RET-based function detection to prevent unreachable code
    func_bounds = disasm.get_function_boundaries_v2()

    # Build SSA - use incremental (best quality) by default, --legacy-ssa for old algorithm
    use_legacy_ssa = getattr(args, 'legacy_ssa', False)
    heritage_metadata = None
    if not use_legacy_ssa:
        # Default: Use multi-pass heritage SSA for improved quality
        ssa_func, heritage_metadata = build_ssa_incremental(scr, return_metadata=True)
        if debug_mode:
            print(f"// Using incremental heritage SSA construction", file=sys.stderr)
            print(f"// Heritage: {len(heritage_metadata.get('variables', {}))} variables, "
                  f"{sum(len(v) for v in heritage_metadata.get('phi_blocks', {}).values())} PHI nodes",
                  file=sys.stderr)
    else:
        # Legacy: Traditional SSA construction (faster but lower quality)
        ssa_func = build_ssa_all_blocks(scr)
        if debug_mode:
            print(f"// Using legacy single-pass SSA construction", file=sys.stderr)

    print(f"// Structured decompilation of {args.file}")
    print(f"// Functions: {len(func_bounds)}")
    print()

    # Generate #include block
    include_block = generate_include_block(scr)
    print(include_block)
    print()

    # P0.1 FIX: Analyze and export global variables
    # FIX 4: Enable aggressive type inference for globals
    resolver = GlobalResolver(
        ssa_func,
        aggressive_typing=True,   # FIX 4: Enabled for int/float inference
        infer_structs=False       # Disabled until fully implemented
    )
    globals_usage = resolver.analyze()

    # FIX #7: Build SaveInfo size mapping (byte_offset -> size_in_dwords)
    saveinfo_sizes = {}
    if scr.save_info:
        for item in scr.save_info.items:
            byte_offset = item['val1'] * 4  # Convert dword offset to byte offset
            size_dwords = item['val2']
            saveinfo_sizes[byte_offset] = size_dwords

    from .core.headers.database import get_header_database
    from .core.structures import get_struct_by_name
    header_db = get_header_database()

    def _format_dim_value(dim: int) -> str:
        if header_db:
            names = header_db.get_constant_names_by_value(dim)
            if names:
                max_names = [name for name in names if name.endswith("_MAX")]
                return max_names[0] if max_names else names[0]
        return str(dim)

    def _infer_element_size(var_type: str) -> Optional[int]:
        if var_type.endswith("*"):
            return 4
        struct_def = get_struct_by_name(var_type)
        if struct_def:
            return struct_def.size
        type_sizes = {
            "char": 1,
            "short": 2,
            "int": 4,
            "float": 4,
            "double": 8,
            "dword": 4,
            "BOOL": 4,
        }
        return type_sizes.get(var_type, None)

    # Generate global variable declarations
    if globals_usage:
        print("// Global variables")
        # Sort by offset for consistent output
        for offset in sorted(globals_usage.keys()):
            usage = globals_usage[offset]
            # Skip array elements (only declare array base)
            if usage.is_array_element:
                continue

            # P0.1 FIX: Filter out read-only constants (likely from data segment)
            # Real global variables are written to at least once
            if usage.write_count == 0 and not usage.name.startswith("g"):
                # Skip pure read-only data_XXX entries (likely constants)
                continue

            # COMPILATION FIX: Skip SGI constants (they're #define macros in headers)
            if usage.source in ("SGI_constant", "SGI_runtime"):
                # SGI_* names are macros, not variables - skip declaration
                continue

            # Determine type and name
            # FIX 4.4: Improved fallback logic for type inference
            if usage.inferred_type:
                var_type = usage.inferred_type
            elif usage.is_incremented or usage.is_decremented:
                # INC/DEC operations imply integer type
                var_type = "int"
            elif usage.possible_types:
                # Use first detected type if available
                var_type = list(usage.possible_types)[0]
            else:
                # True fallback - unknown type
                var_type = "dword"

            var_name = usage.name if usage.name else f"data_{offset}"

            # FIX #7: Use SaveInfo to detect arrays and get accurate sizes
            # Check if this global has a size > 1 in SaveInfo
            size_dwords = saveinfo_sizes.get(offset, 1)
            is_array = size_dwords > 1

            element_type = var_type
            element_size = usage.array_element_size or _infer_element_size(element_type)

            # Preserve pointer element types for pointer arrays
            if is_array and element_type.endswith("*") and element_size and element_size != 4:
                element_type = element_type.replace(" *", "").rstrip("*").strip()
                element_size = _infer_element_size(element_type)

            # Format declaration
            if is_array:
                initializer = f" = {usage.initializer}" if usage.initializer else ""
                if usage.array_dimensions:
                    dim_text = "".join(f"[{_format_dim_value(dim)}]" for dim in usage.array_dimensions)
                    print(f"{element_type} {var_name}{dim_text}{initializer};")
                else:
                    # Array declaration: type name[size];
                    array_size = size_dwords
                    if element_size and element_size > 0:
                        total_bytes = size_dwords * 4
                        if total_bytes % element_size == 0:
                            array_size = total_bytes // element_size

                    print(f"{element_type} {var_name}[{array_size}]{initializer};")
            elif usage.is_array_base and usage.array_element_size:
                # Fallback: use dynamic array detection (for scripts without SaveInfo)
                array_size = 64  # Default estimate
                initializer = f" = {usage.initializer}" if usage.initializer else ""
                print(f"{var_type} {var_name}[{array_size}]{initializer};")
            else:
                # Simple variable: type name;
                initializer = f" = {usage.initializer}" if usage.initializer else ""
                print(f"{var_type} {var_name}{initializer};")
        print()

    # Zpracuj funkce v pořadí podle adresy
    # Pass function_bounds for CALL instruction resolution
    # Pass style for debug output control: 'quiet' (default) or 'normal'/'verbose' with --debug
    # Heritage: Pass heritage_metadata for improved variable names (default with incremental SSA)
    style = 'normal' if debug_mode else 'quiet'
    for func_name, (func_start, func_end) in sorted(func_bounds.items(), key=lambda x: x[1][0]):
        text = format_structured_function_named(ssa_func, func_name, func_start, func_end, function_bounds=func_bounds, style=style, heritage_metadata=heritage_metadata)
        print(text)
        print()


def cmd_symbols(args):
    """Export global variable symbol table"""
    from .core.loader import SCRFile
    from .core.ir.ssa import build_ssa_all_blocks
    from .core.ir.global_resolver import GlobalResolver
    from .core.ir.symbol_export import SymbolTableExporter

    scr = SCRFile.load(args.file, variant=args.variant)
    ssa_func = build_ssa_all_blocks(scr)

    # Enhanced global analysis with type inference and struct reconstruction
    resolver = GlobalResolver(
        ssa_func,
        aggressive_typing=True,
        infer_structs=True
    )
    globals_usage = resolver.analyze()

    # Export
    exporter = SymbolTableExporter(globals_usage, scr)

    output_path = Path(args.output)

    if args.format == 'json':
        exporter.export_to_json(output_path)
        print(f"Exported {len(globals_usage)} symbols to JSON: {output_path}")
    elif args.format == 'header':
        exporter.export_to_c_header(output_path)
        print(f"Exported {len(globals_usage)} symbols to C header: {output_path}")
    elif args.format == 'markdown':
        exporter.export_to_markdown(output_path)
        print(f"Exported {len(globals_usage)} symbols to Markdown: {output_path}")

    # Print statistics
    sgi_mapped = sum(1 for u in globals_usage.values() if u.sgi_name)
    structs = sum(1 for u in globals_usage.values() if u.is_struct_base)
    arrays = sum(1 for u in globals_usage.values() if u.is_array_base)

    print(f"\nStatistics:")
    print(f"  Total globals: {len(globals_usage)}")
    print(f"  SGI mapped: {sgi_mapped}")
    print(f"  Structs detected: {structs}")
    print(f"  Arrays detected: {arrays}")


def cmd_validate(args):
    """Validate decompiled source by recompiling and comparing bytecode"""
    from .validation import ValidationOrchestrator, ReportGenerator, ValidationVerdict

    # Resolve paths
    original_scr = Path(args.original_scr).resolve()
    source_file = Path(args.source_file).resolve()

    # Determine compiler directory
    if args.compiler_dir:
        compiler_dir = Path(args.compiler_dir).resolve()
    else:
        # Default to original-resources/compiler relative to project root
        compiler_dir = Path(__file__).parent.parent / "original-resources" / "compiler"

    # Check files exist
    if not original_scr.exists():
        print(f"Error: Original SCR file not found: {original_scr}", file=sys.stderr)
        sys.exit(1)

    if not source_file.exists():
        print(f"Error: Source file not found: {source_file}", file=sys.stderr)
        sys.exit(1)

    if not compiler_dir.exists():
        print(f"Error: Compiler directory not found: {compiler_dir}", file=sys.stderr)
        print(f"Use --compiler-dir to specify the location of SCMP.exe", file=sys.stderr)
        sys.exit(1)

    # Create validator
    print(f"Validating {source_file.name} against {original_scr.name}...")
    print(f"Compiler directory: {compiler_dir}")
    print()

    validator = ValidationOrchestrator(
        compiler_dir=str(compiler_dir),
        cache_enabled=not args.no_cache
    )

    # Run validation
    try:
        result = validator.validate(
            original_scr=str(original_scr),
            decompiled_source=str(source_file)
        )
    except Exception as e:
        print(f"Error during validation: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine output format
    output_format = args.output_format
    if args.report_file and not output_format:
        # Auto-detect from file extension
        ext = Path(args.report_file).suffix.lower()
        if ext == '.html':
            output_format = 'html'
        elif ext == '.json':
            output_format = 'json'
        else:
            output_format = 'text'
    elif not output_format:
        output_format = 'text'

    # Generate report
    generator = ReportGenerator(use_colors=not args.no_color)

    if args.report_file:
        # Save to file
        report_path = Path(args.report_file)
        generator.save_report(result, str(report_path), format=output_format)
        print(f"Report saved to: {report_path}")
        print()

    # Always print summary to console
    if output_format == 'json' and not args.report_file:
        # If JSON output to console, print the JSON
        print(generator.generate_json_report(result))
    else:
        # Print text summary to console
        print(generator.generate_text_report(result))

    # Exit with appropriate code
    if result.verdict == ValidationVerdict.PASS:
        sys.exit(0)
    elif result.verdict == ValidationVerdict.ERROR:
        sys.exit(2)
    else:
        # FAIL or PARTIAL
        sys.exit(1)


def cmd_validate_batch(args):
    """Validate multiple files in batch mode"""
    import concurrent.futures
    import json
    from datetime import datetime
    from .validation import (
        ValidationOrchestrator,
        ValidationVerdict,
        RegressionBaseline,
        RegressionComparator,
        RegressionStatus,
    )

    # Resolve directories
    input_dir = Path(args.input_dir).resolve()
    original_dir = Path(args.original_dir).resolve()

    # Determine compiler directory
    if args.compiler_dir:
        compiler_dir = Path(args.compiler_dir).resolve()
    else:
        compiler_dir = Path(__file__).parent.parent / "original-resources" / "compiler"

    # Validate directories exist
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    if not original_dir.exists() or not original_dir.is_dir():
        print(f"Error: Original directory not found: {original_dir}", file=sys.stderr)
        sys.exit(1)

    if not compiler_dir.exists():
        print(f"Error: Compiler directory not found: {compiler_dir}", file=sys.stderr)
        print(f"Use --compiler-dir to specify the location of SCMP.exe", file=sys.stderr)
        sys.exit(1)

    # Find all source files and match with originals
    source_files = list(input_dir.glob("*.c"))

    if not source_files:
        print(f"Error: No .c files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    # Build list of validation pairs
    validation_pairs = []
    for source_file in source_files:
        # Find matching .scr file by name
        scr_name = source_file.stem + ".scr"
        scr_path = original_dir / scr_name

        if scr_path.exists():
            validation_pairs.append((scr_path, source_file))
        else:
            print(f"Warning: No matching .scr file for {source_file.name}", file=sys.stderr)

    if not validation_pairs:
        print(f"Error: No matching file pairs found", file=sys.stderr)
        sys.exit(1)

    print(f"Batch Validation")
    print(f"================")
    print(f"Input directory:    {input_dir}")
    print(f"Original directory: {original_dir}")
    print(f"Compiler directory: {compiler_dir}")
    print(f"Pairs to validate:  {len(validation_pairs)}")
    print(f"Parallel jobs:      {args.jobs}")
    print()

    # Create validator
    validator = ValidationOrchestrator(
        compiler_dir=str(compiler_dir),
        cache_enabled=not args.no_cache
    )

    # Function to validate a single pair
    def validate_pair(pair):
        scr_path, source_path = pair
        try:
            result = validator.validate(
                original_scr=str(scr_path),
                decompiled_source=str(source_path)
            )
            return (source_path.name, result, None)
        except Exception as e:
            return (source_path.name, None, str(e))

    # Run validations in parallel
    results = []
    completed = 0
    total = len(validation_pairs)

    print("Progress:")
    print("-" * 60)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        # Submit all tasks
        futures = {executor.submit(validate_pair, pair): pair for pair in validation_pairs}

        # Process as they complete
        for future in concurrent.futures.as_completed(futures):
            pair = futures[future]
            scr_path, source_path = pair
            completed += 1

            name, result, error = future.result()
            results.append((name, result, error))

            # Show progress
            progress_pct = (completed * 100) // total
            progress_bar = "=" * (progress_pct // 2) + ">" + " " * (50 - progress_pct // 2)

            if error:
                status = "ERROR"
                symbol = "✗"
            elif result.verdict == ValidationVerdict.PASS:
                status = "PASS"
                symbol = "✓"
            elif result.verdict == ValidationVerdict.ERROR:
                status = "ERROR"
                symbol = "✗"
            else:
                status = result.verdict.name
                symbol = "!"

            print(f"[{progress_bar}] {completed:3d}/{total:3d} | {symbol} {name:30s} {status}")

    print("-" * 60)
    print()

    # Generate summary report
    print("Summary Report")
    print("=" * 60)

    pass_count = 0
    fail_count = 0
    partial_count = 0
    error_count = 0

    for name, result, error in results:
        if error:
            error_count += 1
        elif result.verdict == ValidationVerdict.PASS:
            pass_count += 1
        elif result.verdict == ValidationVerdict.FAIL:
            fail_count += 1
        elif result.verdict == ValidationVerdict.PARTIAL:
            partial_count += 1
        else:
            error_count += 1

    print(f"Total files:     {total}")
    print(f"Passed:          {pass_count}")
    print(f"Failed:          {fail_count}")
    print(f"Partial:         {partial_count}")
    print(f"Errors:          {error_count}")
    print()

    # Regression testing mode
    regression_report = None
    if args.regression or args.save_baseline:
        baseline_path = Path(args.baseline_file) if args.baseline_file else Path(".validation-baseline.json")

        # Build results dict for regression testing
        results_dict = {}
        for name, result, error in results:
            if result:  # Only include successful validations
                results_dict[name] = result

        if args.save_baseline:
            # Save current results as baseline
            print("Saving baseline...")
            baseline = RegressionBaseline(
                description=f"Baseline created from batch validation of {len(results_dict)} files"
            )
            for name, result in results_dict.items():
                baseline.add_entry(name, result)
            baseline.save(baseline_path)
            print(f"✓ Baseline saved to: {baseline_path}")
            print()

        if args.regression:
            # Compare against baseline
            if not baseline_path.exists():
                print(f"Error: Baseline file not found: {baseline_path}", file=sys.stderr)
                print(f"Create a baseline first with --save-baseline", file=sys.stderr)
                sys.exit(1)

            print("Regression Testing")
            print("=" * 60)
            print(f"Baseline: {baseline_path}")
            print()

            # Load baseline and compare
            baseline = RegressionBaseline.load(baseline_path)
            comparator = RegressionComparator(baseline)
            regression_report = comparator.compare(results_dict)
            regression_report.baseline_path = baseline_path

            # Display regression results
            print(f"Regressions:     {len(regression_report.regressions)}")
            print(f"Improvements:    {len(regression_report.improvements)}")
            print(f"Stable (pass):   {len(regression_report.stable_pass)}")
            print(f"Stable (fail):   {len(regression_report.stable_fail)}")
            print(f"New files:       {len(regression_report.new_files)}")
            print()

            # Show regressions
            if regression_report.has_regressions:
                print("⚠ REGRESSIONS DETECTED:")
                print("-" * 60)
                for item in regression_report.regressions:
                    print(f"✗ {item.file}:")
                    print(f"  Baseline: {item.baseline_verdict} ({item.baseline_semantic} semantic)")
                    print(f"  Current:  {item.current_verdict} ({item.current_semantic} semantic)")
                print()

            # Show improvements
            if regression_report.has_improvements:
                print("✓ IMPROVEMENTS DETECTED:")
                print("-" * 60)
                for item in regression_report.improvements:
                    print(f"✓ {item.file}:")
                    print(f"  Baseline: {item.baseline_verdict} ({item.baseline_semantic} semantic)")
                    print(f"  Current:  {item.current_verdict} ({item.current_semantic} semantic)")
                print()

            # Show new files
            if regression_report.new_files:
                print("New files (not in baseline):")
                print("-" * 60)
                for item in regression_report.new_files:
                    symbol = "✓" if item.current_verdict == "PASS" else "✗"
                    print(f"{symbol} {item.file}: {item.current_verdict}")
                print()

    # Show failures and errors (if not in regression mode)
    if not args.regression and (fail_count > 0 or error_count > 0):
        print("Failed/Error Files:")
        print("-" * 60)
        for name, result, error in results:
            if error:
                print(f"✗ {name}: {error}")
            elif result and result.verdict in (ValidationVerdict.FAIL, ValidationVerdict.ERROR):
                # Show brief error summary
                if result.compilation_succeeded:
                    diff_summary = f"{len(result.categorized_differences)} differences"
                    semantic_count = sum(1 for d in result.categorized_differences
                                       if d.category.name == 'SEMANTIC')
                    if semantic_count > 0:
                        diff_summary += f" ({semantic_count} semantic)"
                    print(f"✗ {name}: {diff_summary}")
                else:
                    error_msgs = [e.message for e in result.compilation_result.errors[:3]]
                    print(f"✗ {name}: Compilation failed - {'; '.join(error_msgs)}")
        print()

    # Save regression report if in regression mode
    if args.regression and regression_report and args.report_file:
        report_path = Path(args.report_file)
        regression_report.save(report_path)
        print(f"Regression report saved to: {report_path}")
        print()

    # Save detailed report if requested (and not in regression mode)
    if args.report_file and not args.regression:
        report_path = Path(args.report_file)

        # Generate batch report
        batch_report = {
            "timestamp": datetime.now().isoformat(),
            "input_dir": str(input_dir),
            "original_dir": str(original_dir),
            "compiler_dir": str(compiler_dir),
            "total": total,
            "passed": pass_count,
            "failed": fail_count,
            "partial": partial_count,
            "errors": error_count,
            "results": []
        }

        for name, result, error in results:
            if error:
                batch_report["results"].append({
                    "file": name,
                    "verdict": "ERROR",
                    "error": error
                })
            else:
                batch_report["results"].append({
                    "file": name,
                    "verdict": result.verdict.name,
                    "compilation_succeeded": result.compilation_succeeded,
                    "differences_count": len(result.categorized_differences) if result.categorized_differences else 0,
                    "semantic_differences": sum(1 for d in result.categorized_differences
                                               if d.category.name == 'SEMANTIC') if result.categorized_differences else 0
                })

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(batch_report, f, indent=2)

        print(f"Detailed report saved to: {report_path}")
        print()

    # Exit with appropriate code
    if args.regression and regression_report:
        # In regression mode, exit 1 if regressions detected
        if regression_report.has_regressions:
            sys.exit(1)
        else:
            sys.exit(0)
    else:
        # Normal mode
        if pass_count == total:
            sys.exit(0)  # All passed
        elif error_count > 0 or fail_count > 0:
            sys.exit(1)  # Some failures
        else:
            sys.exit(0)  # All passed or partial


def cmd_xfn_aggregate(args):
    """Aggregate XFN function signatures from .scr files"""
    from .xfn import XFNAggregator, AggregationResult
    from .xfn.aggregator import merge_with_sdk

    directory = Path(args.directory).resolve()
    if not directory.exists():
        print(f"Error: Directory not found: {directory}", file=sys.stderr)
        sys.exit(1)

    # Validate output is provided for formats that need it
    if args.format in ('sdk', 'json') and not args.output:
        print(f"Error: --output is required for {args.format} format", file=sys.stderr)
        sys.exit(1)

    print(f"XFN Function Aggregation")
    print(f"=" * 50)
    print(f"Directory: {directory}")
    print(f"Recursive: {not args.no_recursive}")
    print()

    # Progress callback
    last_progress = [0]  # Use list to allow mutation in nested function

    def progress_callback(current, total, filename):
        progress_pct = (current * 100) // total
        if progress_pct >= last_progress[0] + 5:  # Update every 5%
            last_progress[0] = progress_pct
            bar = "=" * (progress_pct // 2) + ">" + " " * (50 - progress_pct // 2)
            print(f"\r[{bar}] {progress_pct}% ({current}/{total})", end="", flush=True)

    # Run aggregation
    aggregator = XFNAggregator(verbose=False)

    print("Scanning...")
    result = aggregator.scan_directory(
        str(directory),
        recursive=not args.no_recursive,
        progress_callback=progress_callback
    )
    print()  # Newline after progress bar
    print()

    # Handle output based on format
    if args.format == 'summary':
        print(result.summary())

    elif args.format == 'sdk':
        # Export SDK-compatible format
        output_path = Path(args.output)

        if args.merge_sdk:
            # Merge with existing SDK
            sdk_path = args.sdk_path
            if not sdk_path:
                sdk_path = Path(__file__).parent / "sdk" / "data" / "functions.json"

            if not Path(sdk_path).exists():
                print(f"Error: SDK file not found: {sdk_path}", file=sys.stderr)
                sys.exit(1)

            # Load existing SDK to count differences
            with open(sdk_path, 'r', encoding='utf-8') as f:
                existing_sdk = json.load(f)

            merged = merge_with_sdk(result, str(sdk_path), str(output_path))

            new_count = len(merged) - len(existing_sdk)
            print(f"Merged with existing SDK:")
            print(f"  Existing functions: {len(existing_sdk)}")
            print(f"  New functions:      {new_count}")
            print(f"  Total functions:    {len(merged)}")
        else:
            # Export standalone SDK format
            sdk_data = result.to_sdk_format()
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(sdk_data, f, indent=2)
            print(f"Functions exported: {len(sdk_data)}")

        print(f"Output saved to: {output_path}")

    elif args.format == 'json':
        # Export full JSON with usage statistics
        output_path = Path(args.output)
        json_data = result.to_json(include_usage=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)

        print(f"Full report saved to: {output_path}")
        print(f"  Functions: {json_data['metadata']['function_count']}")
        print(f"  Structs:   {json_data['metadata']['struct_count']}")

    # Print any errors
    if result.scripts_failed > 0:
        print()
        print(f"Warning: {result.scripts_failed} scripts failed to parse")
        if len(result.errors) <= 5:
            for filepath, error in result.errors:
                print(f"  - {Path(filepath).name}: {error}")
        else:
            for filepath, error in result.errors[:3]:
                print(f"  - {Path(filepath).name}: {error}")
            print(f"  ... and {len(result.errors) - 3} more errors")


if __name__ == '__main__':
    main()
