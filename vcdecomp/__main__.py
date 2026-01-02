"""
VC Script Decompiler - CLI Entry Point

Použití:
    python -m vcdecomp info <file.scr>      # Zobrazí info o souboru
    python -m vcdecomp disasm <file.scr>    # Disassembly
    python -m vcdecomp strings <file.scr>   # Seznam stringů
    python -m vcdecomp gui [file.scr]       # Otevře GUI
"""

import argparse
import sys
import io
from pathlib import Path

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
    _add_variant_option(p_structure)

    # symbols
    p_symbols = subparsers.add_parser('symbols', help='Export global variable symbol table')
    p_symbols.add_argument('file', help='Cesta k SCR souboru')
    p_symbols.add_argument('-o', '--output', required=True, help='Output file path')
    p_symbols.add_argument('-f', '--format', choices=['json', 'header', 'markdown'], default='json',
                          help='Export format (default: json)')
    _add_variant_option(p_symbols)

    # gui
    p_gui = subparsers.add_parser('gui', help='Spustí GUI aplikaci')
    p_gui.add_argument('file', nargs='?', help='Cesta k SCR souboru (volitelné)')

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
        elif args.command == 'gui':
            cmd_gui(args)
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
    from .core.ir.ssa import build_ssa_all_blocks
    from .core.headers.detector import generate_include_block
    from .core.ir.global_resolver import GlobalResolver

    scr = SCRFile.load(args.file, variant=args.variant)
    disasm = Disassembler(scr)
    func_bounds = disasm.get_function_boundaries()

    # Vždy zpracuj všechny funkce (--all je nyní výchozí)
    ssa_func = build_ssa_all_blocks(scr)

    print(f"// Structured decompilation of {args.file}")
    print(f"// Functions: {len(func_bounds)}")
    print()

    # Generate #include block
    include_block = generate_include_block(scr)
    print(include_block)
    print()

    # P0.1 FIX: Analyze and export global variables
    resolver = GlobalResolver(
        ssa_func,
        aggressive_typing=False,  # Conservative for now
        infer_structs=False       # Disabled until fully implemented
    )
    globals_usage = resolver.analyze()

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

            # Determine type and name
            var_type = usage.inferred_type if usage.inferred_type else "dword"
            var_name = usage.name if usage.name else f"data_{offset}"

            # Format declaration
            if usage.is_array_base and usage.array_element_size:
                # Array declaration: type name[size];
                # Try to infer array size from SaveInfo or usage patterns
                # For now, estimate based on known patterns
                if "RecTimer" in var_name or var_name == "gRec":
                    array_size = 64  # REC_MAX
                elif "SideFrags" in var_name:
                    array_size = 2   # 2 teams
                else:
                    array_size = 64  # Default
                print(f"{var_type} {var_name}[{array_size}];")
            else:
                # Simple variable: type name;
                print(f"{var_type} {var_name};")
        print()

    # Zpracuj funkce v pořadí podle adresy
    # FÁZE 4: Pass function_bounds for CALL instruction resolution
    for func_name, (func_start, func_end) in sorted(func_bounds.items(), key=lambda x: x[1][0]):
        text = format_structured_function_named(ssa_func, func_name, func_start, func_end, function_bounds=func_bounds)
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


if __name__ == '__main__':
    main()
