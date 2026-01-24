"""
SCR File Loader - Parser pro binární .SCR soubory Vietcong skriptů

Formát SCR souboru:
1. Header - entry point, parametry
2. Data segment - konstanty, stringy (4-byte aligned)
3. Global pointers - offsety globálních proměnných
4. Code segment - instrukce (12 bajtů každá: opcode + 2 argumenty)
5. XFN tabulka - externí funkce (28 bajtů/záznam)
6. Save info (optional)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, BinaryIO
import struct

from ..disasm.opcodes import (
    OpcodeResolver,
    DEFAULT_RESOLVER,
    RESOLVERS,
)
from .data_strings import extract_data_strings


@dataclass
class SCRHeader:
    """
    Header SCR souboru.

    Struktura:
        uint32_t enter_size     - Počet vstupních parametrů
        uint32_t enter_ip       - Entry point (index instrukce, -2 = ScriptMain)
        uint32_t ret_size       - Počet návratových hodnot
        uint32_t enter_array[]  - Typy parametrů (enter_size položek)
    """
    enter_size: int
    enter_ip: int  # Signed! -2 = 0xFFFFFFFE znamená ScriptMain entry
    ret_size: int
    enter_array: List[int] = field(default_factory=list)

    @property
    def size_bytes(self) -> int:
        """Velikost headeru v bytech"""
        return 12 + (4 * self.enter_size)

    @classmethod
    def from_bytes(cls, data: bytes) -> 'SCRHeader':
        """Parsuje header z bytes"""
        enter_size = struct.unpack_from('<I', data, 0)[0]
        enter_ip = struct.unpack_from('<i', data, 4)[0]  # Signed int!
        ret_size = struct.unpack_from('<I', data, 8)[0]

        enter_array = []
        offset = 12
        for _ in range(enter_size):
            enter_array.append(struct.unpack_from('<I', data, offset)[0])
            offset += 4

        return cls(enter_size, enter_ip, ret_size, enter_array)


@dataclass
class DataSegment:
    """
    Data segment obsahující konstanty a stringy.

    Struktura:
        uint32_t data_count     - Počet 32-bit slov
        uint32_t data[]         - Data (4-byte aligned)
    """
    data_count: int
    raw_data: bytes

    # Extrahované stringy: offset -> string
    strings: Dict[int, str] = field(default_factory=dict)

    @property
    def size_bytes(self) -> int:
        """Velikost segmentu v bytech (včetně count)"""
        return 4 + (4 * self.data_count)

    @classmethod
    def from_bytes(cls, data: bytes, offset: int = 0) -> Tuple['DataSegment', int]:
        """
        Parsuje data segment.
        Vrací (DataSegment, new_offset)
        """
        data_count = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        raw_data = data[offset:offset + (data_count * 4)]
        segment = cls(data_count, raw_data)
        segment._extract_strings()

        return segment, offset + (data_count * 4)

    def _extract_strings(self) -> None:
        """
        Extrahuje null-terminated stringy z dat.

        Filtruje extended ASCII a binary data - přijímá jen printable ASCII (0x20-0x7E)
        plus whitespace (\n, \r, \t). Tím se eliminují false positives jako 0xFF = 'ÿ'.
        """
        self.strings = {}
        i = 0
        while i < len(self.raw_data):
            # Hledáme začátek stringu (nenulový byte po null nebo na začátku)
            if i == 0 or (i > 0 and self.raw_data[i-1] == 0):
                # Zkusíme extrahovat string
                end = i
                while end < len(self.raw_data) and self.raw_data[end] != 0:
                    end += 1

                if end > i:
                    try:
                        s = self.raw_data[i:end].decode('latin-1')

                        # VYLEPŠENÝ FILTR: Jen printable ASCII (0x20-0x7E) + whitespace
                        # Tím eliminujeme extended ASCII (0x80-0xFF) jako 'ÿ', 'à', etc.
                        def is_valid_char(c):
                            # Printable ASCII range (space to tilde)
                            if 0x20 <= ord(c) <= 0x7E:
                                return True
                            # Allow common whitespace
                            if c in '\n\r\t':
                                return True
                            return False

                        # Skip single-char extended ASCII (e.g., 0xFF = 'ÿ')
                        if len(s) == 1 and not is_valid_char(s[0]):
                            i += 1
                            continue

                        # All characters must be valid
                        if all(is_valid_char(c) for c in s):
                            self.strings[i] = s
                    except:
                        pass
            i += 1

    def get_dword(self, offset: int) -> int:
        """Vrátí 32-bit hodnotu na daném offsetu"""
        if offset + 4 <= len(self.raw_data):
            return struct.unpack_from('<I', self.raw_data, offset)[0]
        return 0

    def get_float(self, offset: int) -> float:
        """Vrátí float hodnotu na daném offsetu"""
        if offset + 4 <= len(self.raw_data):
            return struct.unpack_from('<f', self.raw_data, offset)[0]
        return 0.0

    def get_string(self, offset: int) -> Optional[str]:
        """Vrátí string na daném offsetu nebo None"""
        return self.strings.get(offset)


@dataclass
class GlobalPointers:
    """
    Tabulka globálních pointerů.

    Struktura:
        uint32_t gptr_count     - Počet pointerů
        uint32_t offsets[]      - Offsety v data segmentu
    """
    gptr_count: int
    offsets: List[int] = field(default_factory=list)

    @property
    def size_bytes(self) -> int:
        """Velikost v bytech"""
        return 4 + (4 * self.gptr_count)

    @classmethod
    def from_bytes(cls, data: bytes, offset: int = 0) -> Tuple['GlobalPointers', int]:
        """Parsuje global pointers tabulku"""
        gptr_count = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        offsets = []
        for _ in range(gptr_count):
            offsets.append(struct.unpack_from('<I', data, offset)[0])
            offset += 4

        return cls(gptr_count, offsets), offset


@dataclass
class Instruction:
    """
    Jednotlivá instrukce (12 bytes).

    Struktura:
        uint32_t opcode     - Opcode (0-149)
        uint32_t arg1       - První argument
        uint32_t arg2       - Druhý argument
    """
    address: int      # Index instrukce (ne byte offset!)
    opcode: int
    arg1: int
    arg2: int

    @classmethod
    def from_bytes(cls, data: bytes, address: int) -> 'Instruction':
        """Parsuje instrukci z 12 bytes"""
        opcode, arg1, arg2 = struct.unpack('<III', data)
        return cls(address, opcode, arg1, arg2)


@dataclass
class CodeSegment:
    """
    Code segment obsahující instrukce.

    Struktura:
        uint32_t code_count     - Počet instrukcí
        Instruction code[]      - Instrukce (12 bytes each)
    """
    code_count: int
    instructions: List[Instruction] = field(default_factory=list)

    @property
    def size_bytes(self) -> int:
        """Velikost v bytech"""
        return 4 + (12 * self.code_count)

    @classmethod
    def from_bytes(cls, data: bytes, offset: int = 0) -> Tuple['CodeSegment', int]:
        """Parsuje code segment"""
        code_count = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        instructions = []
        for i in range(code_count):
            instr_data = data[offset:offset + 12]
            instructions.append(Instruction.from_bytes(instr_data, i))
            offset += 12

        return cls(code_count, instructions), offset


@dataclass
class XFNEntry:
    """
    Záznam v XFN (external function) tabulce (28 bytes).

    Struktura:
        uint32_t name_ptr       - Pointer na jméno (relativní offset)
        uint32_t reserved1      - Vždy 0
        uint32_t ret_size       - Velikost návratové hodnoty
        uint32_t arg_count      - Počet argumentů
        uint32_t arg_types      - Info o typech argumentů
        uint32_t field4         - Return type flag (1 = float, 0 = int/void/pointer)
        uint32_t last_flag      - 0, nebo 1 pro poslední záznam
    """
    index: int
    name: str
    name_ptr: int
    reserved1: int
    ret_size: int
    arg_count: int
    arg_types: int
    field4: int
    last_flag: int


@dataclass
class XFNTable:
    """
    Tabulka externích funkcí.

    Struktura:
        uint32_t xfn_count      - Počet funkcí
        XFNEntry entries[]      - Záznamy (28 bytes each)
        char names[]            - Jména funkcí (null-terminated, sekvenčně)

    Poznámka: První pole každého záznamu (field0) není pointer na jméno,
    jména jsou uložena sekvenčně za všemi záznamy.
    """
    xfn_count: int
    entries: List[XFNEntry] = field(default_factory=list)

    @classmethod
    def from_bytes(cls, data: bytes, offset: int = 0) -> Tuple['XFNTable', int]:
        """Parsuje XFN tabulku"""
        xfn_count = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        # Parsujeme záznamy (28 bytes each)
        raw_entries = []
        for i in range(xfn_count):
            entry_data = struct.unpack_from('<7I', data, offset)
            raw_entries.append({
                'index': i,
                'field0': entry_data[0],      # Neznámé pole (není pointer)
                'reserved1': entry_data[1],   # Vždy 0
                'arg_count': entry_data[2],   # Počet argumentů
                'ret_size': entry_data[3],    # Velikost návratové hodnoty
                'arg_types': entry_data[4],   # Info o typech
                'field5': entry_data[5],      # Další metadata
                'last_flag': entry_data[6],   # 1 pro poslední záznam
            })
            offset += 28

        # Jména jsou uložena sekvenčně za všemi záznamy
        names_offset = offset
        entries = []
        for raw in raw_entries:
            # Čteme null-terminated string
            name_end = names_offset
            while name_end < len(data) and data[name_end] != 0:
                name_end += 1

            try:
                name = data[names_offset:name_end].decode('latin-1')
            except:
                name = f"xfn_{raw['index']}"

            entries.append(XFNEntry(
                index=raw['index'],
                name=name,
                name_ptr=raw['field0'],  # Zachováme pro kompatibilitu
                reserved1=raw['reserved1'],
                ret_size=raw['ret_size'],
                arg_count=raw['arg_count'],
                arg_types=raw['arg_types'],
                field4=raw['field5'],
                last_flag=raw['last_flag'],
            ))

            # Posuneme na další jméno (za null terminator)
            names_offset = name_end + 1

        return cls(xfn_count, entries), names_offset


@dataclass
class SaveInfo:
    """
    Volitelná sekce save_info.

    Struktura:
        char magic[9]           - "sav_info\0"
        uint32_t count          - Počet položek
        SaveItem items[]        - Položky
    """
    count: int
    items: List[dict] = field(default_factory=list)

    @classmethod
    def from_bytes(cls, data: bytes, offset: int = 0) -> Optional['SaveInfo']:
        """Parsuje save_info sekci, vrací None pokud neexistuje"""
        if offset >= len(data):
            return None

        # Kontrola magic "sav_info"
        magic = data[offset:offset + 8]
        if magic != b'sav_info':
            return None

        offset += 9  # 8 + null terminator

        count = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        items = []
        for _ in range(count):
            # Čteme jméno (null-terminated)
            name_end = offset
            while name_end < len(data) and data[name_end] != 0:
                name_end += 1
            name = data[offset:name_end].decode('latin-1')
            offset = name_end + 1

            # Dvě hodnoty
            val1 = struct.unpack_from('<I', data, offset)[0]
            val2 = struct.unpack_from('<I', data, offset + 4)[0]
            offset += 8

            items.append({'name': name, 'val1': val1, 'val2': val2})

        return cls(count, items)


@dataclass
class SCRFile:
    """
    Kompletní parsovaný SCR soubor.
    """
    filename: str
    raw_data: bytes
    header: SCRHeader
    data_segment: DataSegment
    global_pointers: GlobalPointers
    code_segment: CodeSegment
    xfn_table: XFNTable
    save_info: Optional[SaveInfo] = None
    opcode_resolver: OpcodeResolver = field(default_factory=lambda: DEFAULT_RESOLVER)
    opcode_detection_scores: Dict[str, float] = field(default_factory=dict)
    opcode_variant_forced: bool = False
    data_strings: Dict[int, str] = field(default_factory=dict)  # offset → string

    @classmethod
    def load(cls, filename: str, variant: str = "auto") -> 'SCRFile':
        """Načte a parsuje SCR soubor"""
        with open(filename, 'rb') as f:
            data = f.read()
        return cls.from_bytes(data, filename, variant=variant)

    @classmethod
    def from_bytes(cls, data: bytes, filename: str = "<memory>", variant: str = "auto") -> 'SCRFile':
        """Parsuje SCR soubor z bytes"""
        offset = 0

        # 1. Header
        header = SCRHeader.from_bytes(data)
        offset = header.size_bytes

        # 2. Data segment
        data_segment, offset = DataSegment.from_bytes(data, offset)

        # 3. Global pointers
        global_pointers, offset = GlobalPointers.from_bytes(data, offset)

        # 4. Code segment
        code_segment, offset = CodeSegment.from_bytes(data, offset)

        # 5. XFN table
        xfn_table, offset = XFNTable.from_bytes(data, offset)

        # 6. Save info (optional)
        save_info = SaveInfo.from_bytes(data, offset)

        opcode_resolver, detection_scores = _detect_opcode_variant(code_segment, xfn_table)
        forced = False
        variant_normalized = (variant or "auto").lower()
        if variant_normalized != "auto":
            resolver = RESOLVERS.get(variant_normalized)
            if resolver is None:
                valid = ", ".join(sorted(RESOLVERS.keys()))
                raise ValueError(f"Unknown SCR opcode variant '{variant}'. Valid values: auto, {valid}")
            opcode_resolver = resolver
            forced = True

        # Extract strings from data segment (use enhanced extractor)
        data_strings = extract_data_strings(data_segment.raw_data, min_length=3)

        return cls(
            filename=filename,
            raw_data=data,
            header=header,
            data_segment=data_segment,
            global_pointers=global_pointers,
            code_segment=code_segment,
            xfn_table=xfn_table,
            save_info=save_info,
            opcode_resolver=opcode_resolver,
            opcode_detection_scores=detection_scores,
            opcode_variant_forced=forced,
            data_strings=data_strings,
        )

    def get_instruction(self, address: int) -> Optional[Instruction]:
        """Vrátí instrukci na dané adrese (indexu)"""
        if 0 <= address < len(self.code_segment.instructions):
            return self.code_segment.instructions[address]
        return None

    def get_xfn(self, index: int) -> Optional[XFNEntry]:
        """Vrátí XFN záznam podle indexu"""
        if 0 <= index < len(self.xfn_table.entries):
            return self.xfn_table.entries[index]
        return None

    def info(self) -> str:
        """Vrátí informace o souboru jako string"""
        lines = [
            f"=== SCR File Info: {self.filename} ===",
            f"File size: {len(self.raw_data)} bytes",
            "",
            "--- Header ---",
            f"Entry parameters: {self.header.enter_size}",
            f"Entry point (IP): {self.header.enter_ip} {'(ScriptMain)' if self.header.enter_ip == -2 else ''}",
            f"Return values: {self.header.ret_size}",
            f"Parameter types: {self.header.enter_array}",
            "",
            "--- Data Segment ---",
            f"Data words: {self.data_segment.data_count}",
            f"Data size: {len(self.data_segment.raw_data)} bytes",
            f"Strings found: {len(self.data_segment.strings)}",
            "",
            "--- Global Pointers ---",
            f"Count: {self.global_pointers.gptr_count}",
            "",
            "--- Code Segment ---",
            f"Instructions: {self.code_segment.code_count}",
            f"Code size: {self.code_segment.code_count * 12} bytes",
            "",
            "--- External Functions (XFN) ---",
            f"Count: {self.xfn_table.xfn_count}",
        ]

        variant_line = self.opcode_resolver.name
        if self.opcode_variant_forced:
            variant_line += " (forced)"
        if self.opcode_detection_scores:
            summary = ", ".join(f"{name}={score:.1f}" for name, score in self.opcode_detection_scores.items())
            variant_line += f" [{summary}]"
        lines.append(f"Opcode variant: {variant_line}")

        for entry in self.xfn_table.entries:
            lines.append(f"  [{entry.index:3d}] {entry.name}")

        if self.save_info:
            lines.append("")
            lines.append("--- Save Info ---")
            lines.append(f"Items: {self.save_info.count}")

        return "\n".join(lines)


def _as_signed(value: int) -> int:
    if value >= 0x80000000:
        return value - 0x100000000
    return value


def _is_valid_code_target(value: int, code_count: int) -> bool:
    if code_count <= 0:
        return False
    signed = _as_signed(value)
    return 0 <= signed < code_count


def _is_valid_xfn_index(value: int, xfn_count: int) -> bool:
    if xfn_count <= 0:
        return False
    signed = _as_signed(value)
    return 0 <= signed < xfn_count


def _count_xcall_matches(instructions: List[Instruction], opcode: Optional[int], xfn_count: int) -> Tuple[int, int]:
    if opcode is None or xfn_count <= 0:
        return 0, 0

    hits = total = 0
    for instr in instructions:
        if instr.opcode == opcode:
            total += 1
            if _is_valid_xfn_index(instr.arg1, xfn_count):
                hits += 1
    return hits, total


def _detect_opcode_variant(code_segment: CodeSegment, xfn_table: XFNTable) -> Tuple[OpcodeResolver, Dict[str, float]]:
    scores: Dict[str, float] = {}
    xfn_count = xfn_table.xfn_count
    code_count = code_segment.code_count
    instructions = code_segment.instructions

    for resolver in RESOLVERS.values():
        call_hits = call_misses = 0
        jump_hits = jump_misses = 0

        for instr in instructions:
            if instr.opcode in resolver.internal_call_opcodes:
                if _is_valid_code_target(instr.arg1, code_count):
                    call_hits += 1
                else:
                    call_misses += 1
            if instr.opcode in resolver.jump_opcodes:
                if _is_valid_code_target(instr.arg1, code_count):
                    jump_hits += 1
                else:
                    jump_misses += 1

        xcall_opcode = resolver.mnemonic_to_opcode.get("XCALL")
        xcall_hits, xcall_total = _count_xcall_matches(instructions, xcall_opcode, xfn_count)
        xcall_misses = xcall_total - xcall_hits

        score = (
            (call_hits * 3.0) - (call_misses * 4.0) +
            (jump_hits * 1.0) - (jump_misses * 1.5) +
            (xcall_hits * 12.0) - (xcall_misses * 16.0)
        )
        if resolver.name == DEFAULT_RESOLVER.name:
            score += 0.01
        scores[resolver.name] = score

    if not scores:
        return DEFAULT_RESOLVER, {}

    best_name = max(scores, key=scores.get)
    return RESOLVERS.get(best_name, DEFAULT_RESOLVER), scores
