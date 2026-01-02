"""
Disassembler pro Vietcong VM

Převádí binární instrukce na čitelný assembler výstup.
"""

from typing import List, Set, Dict, Optional
from dataclasses import dataclass, field
import struct
import math

from ..loader.scr_loader import SCRFile, Instruction
from .opcodes import ArgType, OpcodeResolver, DEFAULT_RESOLVER


@dataclass
class DisasmLine:
    """Jeden řádek disassembly"""
    address: int
    mnemonic: str
    args: str
    comment: str = ""
    label: str = ""  # Label na této adrese
    raw_bytes: bytes = b""

    def __str__(self) -> str:
        parts = []
        if self.label:
            parts.append(f"{self.label}:")
        addr = f"{self.address:03d}"
        if self.args:
            instr = f"{self.mnemonic:8s} {self.args}"
        else:
            instr = self.mnemonic
        line = f"  {addr}: {instr:30s}"
        if self.comment:
            line += f" ; {self.comment}"
        parts.append(line)
        return "\n".join(parts)


class Disassembler:
    """
    Disassembler pro SCR soubory.

    Převádí instrukce na čitelný assembler výstup podobný sasm.dbg.
    """

    def __init__(self, scr: SCRFile, resolver: Optional[OpcodeResolver] = None):
        self.scr = scr
        self.resolver = resolver or getattr(scr, "opcode_resolver", DEFAULT_RESOLVER)
        self.labels: Dict[int, str] = {}  # address -> label name
        self.functions: Dict[int, str] = {}  # address -> function name
        self.data_usage: Dict[int, str] = {}  # dword_index -> "string" | "value"
        self._analyze_labels()
        self._analyze_data_usage()

    def _analyze_labels(self) -> None:
        """Analyzuje kód a vytvoří labely pro cíle skoků"""
        label_targets: Set[int] = set()
        call_targets: Set[int] = set()
        jump_opcodes = self.resolver.jump_opcodes
        internal_call_opcodes = self.resolver.internal_call_opcodes
        return_opcodes = self.resolver.return_opcodes
        code_count = self.scr.code_segment.code_count

        # Najdeme všechny cíle skoků a volání
        for instr in self.scr.code_segment.instructions:
            opcode = instr.opcode

            if opcode in jump_opcodes:
                label_targets.add(instr.arg1)
            elif opcode in internal_call_opcodes:
                # Interní CALL - cíl je lokální funkce
                call_targets.add(instr.arg1)

        # Vytvoříme labely
        for addr in sorted(label_targets):
            self.labels[addr] = f"label_{addr:04d}"

        # Funkce pojmenujeme
        for addr in sorted(call_targets):
            self.functions[addr] = f"func_{addr:04d}"

        # Entry point
        if self.scr.header.enter_ip >= 0:
            self.functions[self.scr.header.enter_ip] = "ScriptMain"
        elif self.scr.header.enter_ip == -2:
            # -2 znamená že ScriptMain existuje, ale adresa není specifikována
            # Zkontrolujeme, jestli adresa 0 je RET (dead code/epilog)
            if self.scr.code_segment.instructions:
                first_instr = self.scr.code_segment.instructions[0]
                if first_instr.address == 0 and first_instr.opcode in return_opcodes and 0 not in call_targets:
                    # Adresa 0 je RET a není CALL target -> dead code, ScriptMain je na adrese 1
                    self.functions[1] = "ScriptMain"
                else:
                    # Adresa 0 je normální kód nebo je CALL target -> ScriptMain začíná na 0
                    self.functions[0] = "ScriptMain"
            else:
                # Prázdný kód - fallback na adresu 0
                self.functions[0] = "ScriptMain"

        # Detekce ScriptMain pro záporné enter_ip (jiné než -2)
        # Najdeme kód za poslední helper funkcí - to je obvykle ScriptMain
        if self.scr.header.enter_ip < -2 or (self.scr.header.enter_ip < 0 and self.scr.header.enter_ip != -2):
            # Najdeme poslední RET před hlavním kódem
            sorted_call_targets = sorted(call_targets)
            if sorted_call_targets:
                last_helper_start = sorted_call_targets[-1]
                # Hledáme RET za posledním helper entry
                main_start = None
                for instr in self.scr.code_segment.instructions:
                    if instr.address > last_helper_start and instr.opcode in return_opcodes:
                        # RET najden, další instrukce je potenciální ScriptMain
                        next_addr = instr.address + 1
                        if next_addr < code_count:
                            main_start = next_addr
                            break
                if main_start is not None and main_start not in self.functions:
                    self.functions[main_start] = "ScriptMain"
            elif 0 not in self.functions:
                # Žádné helper funkce - ScriptMain je na adrese 0
                self.functions[0] = "ScriptMain"

        # Detekce init kódu (před první funkcí)
        if self.functions:
            first_func_addr = min(self.functions.keys())
            if first_func_addr > 0:
                # Je kód před první funkcí - přidáme jako _init
                self.functions[0] = "_init"

    def _analyze_data_usage(self) -> None:
        """Analyzuje jak jsou data používána a určí jejich typ"""
        for instr in self.scr.code_segment.instructions:
            mnemonic = self.resolver.get_mnemonic(instr.opcode)

            if mnemonic == "GADR":
                # GADR načítá adresu stringu pro čtení
                self.data_usage[instr.arg1] = "string"
            elif mnemonic == "DADR":
                # DADR načítá adresu pro zápis (cíl assignment) - není string
                if instr.arg1 not in self.data_usage:
                    self.data_usage[instr.arg1] = "value"
            elif mnemonic in ("GCP", "GLD"):
                # Hodnota - data jsou int/float (nepřepisujeme pokud už je string)
                if instr.arg1 not in self.data_usage:
                    self.data_usage[instr.arg1] = "value"

    def _is_reasonable_float(self, f: float) -> bool:
        """Kontroluje zda float hodnota vypadá rozumně (ne náhodná binární data)"""
        if math.isnan(f) or math.isinf(f):
            return False
        if f == 0.0:
            return True
        # Rozumný rozsah pro herní hodnoty: 0.001 - 10000
        if abs(f) < 0.001 or abs(f) > 10000:
            return False
        # Preferovat "hezká" čísla (celá, nebo s jedním desetinným místem)
        rounded = round(f, 1)
        if abs(f - rounded) < 0.0001:
            return True
        return False

    def _format_data_value(self, dword_index: int) -> str:
        """Formátuje hodnotu z data segmentu jako int nebo float"""
        byte_offset = dword_index * 4
        val = self.scr.data_segment.get_dword(byte_offset)

        # Zkusit float interpretaci
        f = struct.unpack('<f', struct.pack('<I', val))[0]
        if self._is_reasonable_float(f):
            # Formátovat float hezky
            if f == int(f):
                return f"= {int(f)}.0f"
            return f"= {f:.4g}f"
        elif val >= 0x80000000:
            # Záporné číslo
            return f"= {val - 0x100000000}"
        else:
            return f"= {val}"

    def format_arg(self, instr: Instruction, arg_num: int) -> str:
        """Formátuje argument instrukce"""
        info = self.resolver.get_info(instr.opcode)
        if info is None:
            return str(instr.arg1 if arg_num == 1 else instr.arg2)

        arg_type = info.arg1_type if arg_num == 1 else info.arg2_type
        value = instr.arg1 if arg_num == 1 else instr.arg2

        if arg_type == ArgType.NONE:
            return ""
        elif arg_type == ArgType.LABEL:
            # Reference na label
            if value in self.labels:
                return self.labels[value]
            elif value in self.functions:
                return self.functions[value]
            else:
                return f"@{value}"
        elif arg_type == ArgType.XFN_INDEX:
            # Index do XFN tabulky
            xfn = self.scr.get_xfn(value)
            if xfn:
                return f"${xfn.name}"
            else:
                return f"$extern{value:04d}"
        elif arg_type == ArgType.DATA_OFFSET:
            # Offset v data segmentu - value je DWORD index
            if self.data_usage.get(value) == "string":
                byte_offset = value * 4
                s = self.scr.data_segment.get_string(byte_offset)
                if s and len(s) < 40:
                    escaped = s.replace('\n', '\\n').replace('\r', '\\r')
                    return f"data[{value}]  ; \"{escaped}\""
            return f"data[{value}]"
        elif arg_type == ArgType.STACK_OFFSET:
            # Offset na stacku (může být záporný pro parametry)
            if value >= 0x80000000:
                # Záporná hodnota (signed int)
                signed_val = value - 0x100000000
                return f"[sp{signed_val:+d}]"
            else:
                return f"[sp+{value}]"
        else:
            # IMMEDIATE nebo neznámý
            if value >= 0x80000000:
                # Záporná hodnota
                signed_val = value - 0x100000000
                return str(signed_val)
            elif value > 0xFFFF:
                return f"0x{value:08X}"
            else:
                return str(value)

    def format_comment(self, instr: Instruction) -> str:
        """Vytvoří komentář pro instrukci"""
        info = self.resolver.get_info(instr.opcode)
        mnemonic = self.resolver.get_mnemonic(instr.opcode)
        comments = []

        # Speciální komentáře pro některé instrukce
        if mnemonic == "GCP":
            # arg1 je DWORD index
            dword_index = instr.arg1

            # Zobrazit podle skutečného použití dat
            if self.data_usage.get(dword_index) == "string":
                byte_offset = dword_index * 4
                s = self.scr.data_segment.get_string(byte_offset)
                if s:
                    escaped = s[:30].replace('\n', '\\n').replace('\r', '\\r')
                    comments.append(f'"{escaped}"')
            else:
                # Hodnota - zobrazit jako int nebo float
                comments.append(self._format_data_value(dword_index))
        elif mnemonic == "XCALL":
            xfn = self.scr.get_xfn(instr.arg1)
            if xfn:
                comments.append(f"args={xfn.arg_count}")
        elif mnemonic in {"LCP", "LLD", "GLD"}:
            if instr.arg1 >= 0x80000000:
                signed_val = instr.arg1 - 0x100000000
                if signed_val >= -2:
                    comments.append(f"param{abs(signed_val + 2)}")
        elif mnemonic == "PCALL":
            comments.append("indirect call via pointer")
        elif mnemonic == "CFA":
            comments.append("call function address")
        elif mnemonic == "ITRPT":
            comments.append("breakpoint/interrupt")

        return ", ".join(comments)

    def disassemble_instruction(self, instr: Instruction) -> DisasmLine:
        """Disassembluje jednu instrukci"""
        mnemonic = self.resolver.get_mnemonic(instr.opcode)
        info = self.resolver.get_info(instr.opcode)

        # Formátujeme argumenty
        args_parts = []
        if info:
            arg1 = self.format_arg(instr, 1)
            if arg1:
                args_parts.append(arg1)

            # arg2 většinou není použit, ale pro jistotu
            if info.arg2_type != ArgType.NONE:
                arg2 = self.format_arg(instr, 2)
                if arg2:
                    args_parts.append(arg2)
        else:
            # Neznámý opcode - zobrazíme oba argumenty jako raw
            args_parts.append(str(instr.arg1))
            if instr.arg2 != 0:
                args_parts.append(str(instr.arg2))

        args = ", ".join(args_parts)
        comment = self.format_comment(instr)

        # Label na této adrese
        label = ""
        if instr.address in self.functions:
            label = self.functions[instr.address]
        elif instr.address in self.labels:
            label = self.labels[instr.address]

        return DisasmLine(
            address=instr.address,
            mnemonic=mnemonic,
            args=args,
            comment=comment,
            label=label
        )

    def disassemble(self) -> List[DisasmLine]:
        """Disassembluje celý code segment"""
        lines = []
        for instr in self.scr.code_segment.instructions:
            lines.append(self.disassemble_instruction(instr))
        return lines

    def to_string(self) -> str:
        """Vrátí kompletní disassembly jako string"""
        output = []

        # Header
        output.append("; ==========================================")
        output.append(f"; Disassembly of: {self.scr.filename}")
        output.append(f"; Instructions: {self.scr.code_segment.code_count}")
        output.append(f"; External functions: {self.scr.xfn_table.xfn_count}")
        output.append("; ==========================================")
        output.append("")

        # XFN tabulka
        if self.scr.xfn_table.entries:
            output.append("; External Functions (XFN)")
            output.append("; ------------------------")
            for entry in self.scr.xfn_table.entries:
                output.append(f";   [{entry.index:3d}] {entry.name}")
            output.append("")

        # Stringy - pouze ty které jsou skutečně používané jako stringy (GADR/DADR)
        string_offsets = {idx * 4 for idx, usage in self.data_usage.items() if usage == "string"}
        if string_offsets:
            output.append("; Strings")
            output.append("; -------")
            for offset in sorted(string_offsets):
                s = self.scr.data_segment.get_string(offset)
                if s:
                    escaped = s.replace('\n', '\\n').replace('\r', '\\r')
                    if len(escaped) > 50:
                        escaped = escaped[:47] + "..."
                    output.append(f";   [{offset:4d}] \"{escaped}\"")
            output.append("")

        # Disassembly
        output.append("; Code")
        output.append("; ----")
        output.append("")

        lines = self.disassemble()
        for line in lines:
            output.append(str(line))

        return "\n".join(output)

    def get_function_boundaries(self) -> Dict[str, tuple]:
        """
        Detekuje hranice funkcí na základě CALL cílů a RET instrukcí.
        Vrací dict: function_name -> (start_addr, end_addr)
        """
        boundaries = {}

        # Seřadíme funkce podle adresy
        sorted_funcs = sorted(self.functions.items(), key=lambda x: x[0])

        for i, (start_addr, func_name) in enumerate(sorted_funcs):
            # Konec funkce je buď začátek další funkce nebo konec kódu
            if i + 1 < len(sorted_funcs):
                end_addr = sorted_funcs[i + 1][0] - 1
            else:
                end_addr = self.scr.code_segment.code_count - 1

            boundaries[func_name] = (start_addr, end_addr)

        return boundaries
