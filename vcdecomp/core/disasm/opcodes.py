"""
Opcode definice pro Vietcong VM - OVĚŘENÉ MAPOVÁNÍ Z BINÁRNÍCH DAT

ZDROJ: Ground truth extrahované porovnáním:
       - Binárních opcode hodnot v .SCR souborech
       - Mnemoniků v sasm.dbg debug souborech

POZNÁMKA: Tabulka v sasm.exe na 0x417050 je pro DEBUG VÝPIS, ne pro runtime VM!
          Skutečné mapování VM opcodes je jiné.

Datum: 2025-01-25
Metoda: Párování binárních opcodes z .SCR s mnemoniky z sasm.dbg
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import Optional, Dict, Set

from .runtime_opcode_table import RUNTIME_OPCODE_MAP


class ArgType(IntEnum):
    """Typy argumentů instrukcí"""
    NONE = 0        # Žádný argument
    IMMEDIATE = 1   # Přímá hodnota (int)
    LABEL = 2       # Cíl skoku (index instrukce)
    DATA_OFFSET = 3 # Offset v data segmentu
    XFN_INDEX = 4   # Index do XFN tabulky
    STACK_OFFSET = 5  # Offset na stacku
    SIZE = 6        # Velikost v bytech


class ResultType(IntEnum):
    """Typy výsledků (pro type inference)"""
    VOID = 0
    CHAR = 1
    SHORT = 2
    INT = 3
    FLOAT = 4
    DOUBLE = 5
    POINTER = 6
    UNKNOWN = 7


@dataclass
class OpcodeInfo:
    """Metadata pro jednotlivé opcode"""
    mnemonic: str
    pops: int = 0           # Počet hodnot odstraněných ze stacku
    pushes: int = 0         # Počet hodnot přidaných na stack
    arg1_type: ArgType = ArgType.NONE
    arg2_type: ArgType = ArgType.NONE
    result_type: ResultType = ResultType.INT
    description: str = ""

    @property
    def stack_delta(self) -> int:
        """Změna velikosti stacku"""
        return self.pushes - self.pops


# =============================================================================
# OVĚŘENÉ MAPOVÁNÍ OPCODES Z GROUND TRUTH DAT
# =============================================================================
# Toto mapování bylo extrahováno z Compiler-testruns/ porovnáním
# binárních opcode hodnot v .SCR souborech s mnemoniky v sasm.dbg.
#
# Ověřené opcodes jsou označeny # VERIFIED
# Neověřené opcodes jsou označeny # INFERRED nebo jsou chybějící
# =============================================================================




# =============================================================================
# OPCODE INFO - Detailní informace o instrukcích
# =============================================================================

OPCODE_INFO: Dict[int, OpcodeInfo] = {
    # Stack operace
    0: OpcodeInfo("SSP", 0, 0, ArgType.IMMEDIATE, ArgType.NONE, ResultType.VOID, "Set stack pointer"),
    1: OpcodeInfo("LCP", 0, 1, ArgType.STACK_OFFSET, ArgType.NONE, ResultType.INT, "Load constant/parameter"),
    2: OpcodeInfo("GCP", 0, 1, ArgType.DATA_OFFSET, ArgType.NONE, ResultType.INT, "Get constant from data segment"),
    4: OpcodeInfo("LLD", 0, 1, ArgType.STACK_OFFSET, ArgType.NONE, ResultType.INT, "Local load from stack offset"),
    5: OpcodeInfo("DCP", 1, 1, ArgType.SIZE, ArgType.NONE, ResultType.INT, "Data copy - load from [stack_top] and push result"),
    7: OpcodeInfo("LADR", 0, 1, ArgType.STACK_OFFSET, ArgType.NONE, ResultType.POINTER, "Load address of local/param variable"),
    8: OpcodeInfo("RET", 0, 0, ArgType.IMMEDIATE, ArgType.NONE, ResultType.VOID, "Return from function"),

    # Aritmetika - Int
    12: OpcodeInfo("NEG", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Negate integer"),
    22: OpcodeInfo("SUB", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Subtract integers"),
    58: OpcodeInfo("ADD", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Add integers"),
    94: OpcodeInfo("IDIV", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Integer divide (unsigned)"),
    104: OpcodeInfo("DIV", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Integer divide (signed)"),
    128: OpcodeInfo("MUL", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Multiply integers"),
    111: OpcodeInfo("MOD", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Modulo"),

    # Porovnání - Int
    74: OpcodeInfo("LES", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Less than"),
    91: OpcodeInfo("GRE", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Greater than"),
    103: OpcodeInfo("EQU", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Equal"),
    20: OpcodeInfo("NEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Not equal"),
    106: OpcodeInfo("LEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Less or equal"),
    148: OpcodeInfo("GEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Greater or equal"),

    # Porovnání - Unsigned
    140: OpcodeInfo("ULES", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned less than"),
    146: OpcodeInfo("UGRE", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned greater than"),
    15: OpcodeInfo("UGEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned greater or equal"),
    68: OpcodeInfo("ULEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned less or equal"),

    # Aritmetika - Float
    27: OpcodeInfo("FADD", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.FLOAT, "Float add"),
    92: OpcodeInfo("FSUB", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.FLOAT, "Float subtract"),
    90: OpcodeInfo("FMUL", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.FLOAT, "Float multiply"),
    18: OpcodeInfo("FDIV", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.FLOAT, "Float divide"),
    130: OpcodeInfo("FNEG", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.FLOAT, "Float negate"),

    # Porovnání - Float
    93: OpcodeInfo("FLES", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Float less than"),
    31: OpcodeInfo("FLEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Float less or equal"),
    116: OpcodeInfo("FGRE", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Float greater than"),
    10: OpcodeInfo("FGEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Float greater or equal"),
    97: OpcodeInfo("FEQU", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Float equal"),
    105: OpcodeInfo("FNEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Float not equal"),

    # Aritmetika - Short
    29: OpcodeInfo("SNEG", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short negate"),

    # Porovnání - Short
    17: OpcodeInfo("SEQU", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Short equal"),
    19: OpcodeInfo("SLES", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Short less than"),
    49: OpcodeInfo("SLEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Short less or equal"),
    61: OpcodeInfo("SGRE", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Short greater than"),
    65: OpcodeInfo("SGEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Short greater or equal"),

    # Porovnání - Char
    36: OpcodeInfo("CEQU", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Char equal"),
    96: OpcodeInfo("CNEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Char not equal"),
    126: OpcodeInfo("CLES", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Char less than"),
    141: OpcodeInfo("CLEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Char less or equal"),
    133: OpcodeInfo("CGRE", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Char greater than"),
    56: OpcodeInfo("CGEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Char greater or equal"),

    # Konverze
    110: OpcodeInfo("ITOF", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.FLOAT, "Int to float"),
    32: OpcodeInfo("FTOI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Float to int"),
    129: OpcodeInfo("SCI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Signed char to int"),
    142: OpcodeInfo("SSI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Signed short to int"),
    88: OpcodeInfo("UCI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned char to int"),
    125: OpcodeInfo("USI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned short to int"),
    63: OpcodeInfo("ITOD", 1, 2, ArgType.NONE, ArgType.NONE, ResultType.DOUBLE, "Int to double"),
    81: OpcodeInfo("DTOI", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Double to int"),
    99: OpcodeInfo("FTOD", 1, 2, ArgType.NONE, ArgType.NONE, ResultType.DOUBLE, "Float to double"),
    51: OpcodeInfo("DTOF", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.FLOAT, "Double to float"),

    # Aritmetika - Double
    54: OpcodeInfo("DADD", 4, 2, ArgType.NONE, ArgType.NONE, ResultType.DOUBLE, "Double add"),
    79: OpcodeInfo("DSUB", 4, 2, ArgType.NONE, ArgType.NONE, ResultType.DOUBLE, "Double subtract"),
    84: OpcodeInfo("DMUL", 4, 2, ArgType.NONE, ArgType.NONE, ResultType.DOUBLE, "Double multiply"),
    83: OpcodeInfo("DDIV", 4, 2, ArgType.NONE, ArgType.NONE, ResultType.DOUBLE, "Double divide"),
    37: OpcodeInfo("DNEG", 2, 2, ArgType.NONE, ArgType.NONE, ResultType.DOUBLE, "Double negate"),

    # Porovnání - Double
    114: OpcodeInfo("DLES", 4, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Double less than"),
    147: OpcodeInfo("DLEQ", 4, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Double less or equal"),
    127: OpcodeInfo("DGRE", 4, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Double greater than"),
    138: OpcodeInfo("DGEQ", 4, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Double greater or equal"),
    55: OpcodeInfo("DEQU", 4, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Double equal"),
    121: OpcodeInfo("DNEQ", 4, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Double not equal"),

    # Bitové operace
    72: OpcodeInfo("BA", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Bitwise AND"),
    117: OpcodeInfo("BO", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Bitwise OR"),
    14: OpcodeInfo("BX", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Bitwise XOR"),
    66: OpcodeInfo("BN", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Bitwise NOT"),
    119: OpcodeInfo("LS", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Left shift"),
    35: OpcodeInfo("RS", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Right shift"),

    # Skoky
    24: OpcodeInfo("JMP", 0, 0, ArgType.LABEL, ArgType.NONE, ResultType.VOID, "Unconditional jump"),
    136: OpcodeInfo("JZ", 1, 0, ArgType.LABEL, ArgType.NONE, ResultType.VOID, "Jump if zero"),
    40: OpcodeInfo("JNZ", 1, 0, ArgType.LABEL, ArgType.NONE, ResultType.VOID, "Jump if not zero"),

    # Volání
    45: OpcodeInfo("CALL", 0, 0, ArgType.LABEL, ArgType.NONE, ResultType.VOID, "Internal function call"),
    25: OpcodeInfo("XCALL", 0, 0, ArgType.XFN_INDEX, ArgType.NONE, ResultType.VOID, "External function call"),

    # Adresy a pointery
    39: OpcodeInfo("ASP", 0, 0, ArgType.IMMEDIATE, ArgType.NONE, ResultType.VOID, "Adjust stack pointer"),
    43: OpcodeInfo("GADR", 0, 1, ArgType.DATA_OFFSET, ArgType.NONE, ResultType.POINTER, "Global address"),
    47: OpcodeInfo("DADR", 1, 1, ArgType.IMMEDIATE, ArgType.NONE, ResultType.POINTER, "Pointer arithmetic - add offset to address from stack"),
    26: OpcodeInfo("PNT", 1, 1, ArgType.IMMEDIATE, ArgType.NONE, ResultType.POINTER, "Pointer with offset"),
    44: OpcodeInfo("DLD", 0, 0, ArgType.STACK_OFFSET, ArgType.NONE, ResultType.VOID, "Data load"),
    59: OpcodeInfo("ASGN", 2, 0, ArgType.NONE, ArgType.NONE, ResultType.VOID, "Assignment"),
}

_INFO_BY_MNEMONIC = {}
for info in OPCODE_INFO.values():
    _INFO_BY_MNEMONIC.setdefault(info.mnemonic, info)

_ADDITIONAL_INFO = {
    # Stack / misc helpers
    "GLD": OpcodeInfo("GLD", 0, 1, ArgType.DATA_OFFSET, ArgType.NONE, ResultType.INT, "Load global data value"),
    "INC": OpcodeInfo("INC", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Increment integer"),
    "DEC": OpcodeInfo("DEC", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Decrement integer"),
    "AND": OpcodeInfo("AND", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Logical AND"),
    "OR": OpcodeInfo("OR", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Logical OR"),
    "NOT": OpcodeInfo("NOT", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Logical NOT"),
    "PCALL": OpcodeInfo("PCALL", 0, 0, ArgType.NONE, ArgType.NONE, ResultType.VOID, "Indirect call via pointer"),
    "CFA": OpcodeInfo("CFA", 0, 1, ArgType.NONE, ArgType.NONE, ResultType.POINTER, "Load call target address"),
    "ITRPT": OpcodeInfo("ITRPT", 0, 0, ArgType.NONE, ArgType.NONE, ResultType.VOID, "Interrupt/breakpoint"),
    "GDM": OpcodeInfo("GDM", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.POINTER, "Allocate data member"),
    "FDM": OpcodeInfo("FDM", 1, 0, ArgType.NONE, ArgType.NONE, ResultType.VOID, "Free data member"),
    "FINV": OpcodeInfo("FINV", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.FLOAT, "Float reciprocal"),
    "DINV": OpcodeInfo("DINV", 2, 2, ArgType.NONE, ArgType.NONE, ResultType.DOUBLE, "Double reciprocal"),

    # Char arithmetic / bit ops
    "CINC": OpcodeInfo("CINC", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char increment"),
    "CDEC": OpcodeInfo("CDEC", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char decrement"),
    "CNEG": OpcodeInfo("CNEG", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char negate"),
    "CBN": OpcodeInfo("CBN", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char bitwise NOT"),
    "CADD": OpcodeInfo("CADD", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char add"),
    "CSUB": OpcodeInfo("CSUB", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char subtract"),
    "CMUL": OpcodeInfo("CMUL", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char multiply"),
    "CDIV": OpcodeInfo("CDIV", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char divide"),
    "CMOD": OpcodeInfo("CMOD", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char modulo"),
    "CBA": OpcodeInfo("CBA", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char bitwise AND"),
    "CBX": OpcodeInfo("CBX", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char bitwise XOR"),
    "CBO": OpcodeInfo("CBO", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char bitwise OR"),
    "CLS": OpcodeInfo("CLS", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char left shift"),
    "CRS": OpcodeInfo("CRS", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Char right shift"),

    # Short arithmetic / bit ops
    "SINC": OpcodeInfo("SINC", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short increment"),
    "SDEC": OpcodeInfo("SDEC", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short decrement"),
    "SMUL": OpcodeInfo("SMUL", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short multiply"),
    "SDIV": OpcodeInfo("SDIV", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short divide"),
    "SADD": OpcodeInfo("SADD", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short add"),
    "SSUB": OpcodeInfo("SSUB", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short subtract"),
    "SMOD": OpcodeInfo("SMOD", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short modulo"),
    "SBA": OpcodeInfo("SBA", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short bitwise AND"),
    "SBX": OpcodeInfo("SBX", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short bitwise XOR"),
    "SBO": OpcodeInfo("SBO", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short bitwise OR"),
    "SBN": OpcodeInfo("SBN", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short bitwise NOT"),
    "SLS": OpcodeInfo("SLS", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short left shift"),
    "SRS": OpcodeInfo("SRS", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Short right shift"),
    "SNEQ": OpcodeInfo("SNEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Short not equal"),

    # Conversions (char/short/int/float/double)
    "CTOS": OpcodeInfo("CTOS", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Char to short"),
    "CTOI": OpcodeInfo("CTOI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Char to int"),
    "CTOF": OpcodeInfo("CTOF", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.FLOAT, "Char to float"),
    "CTOD": OpcodeInfo("CTOD", 1, 2, ArgType.NONE, ArgType.NONE, ResultType.DOUBLE, "Char to double"),
    "STOC": OpcodeInfo("STOC", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Short to char"),
    "STOI": OpcodeInfo("STOI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Short to int"),
    "STOF": OpcodeInfo("STOF", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.FLOAT, "Short to float"),
    "STOD": OpcodeInfo("STOD", 1, 2, ArgType.NONE, ArgType.NONE, ResultType.DOUBLE, "Short to double"),
    "ITOC": OpcodeInfo("ITOC", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Int to char"),
    "ITOS": OpcodeInfo("ITOS", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Int to short"),
    "FTOC": OpcodeInfo("FTOC", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Float to char"),
    "FTOS": OpcodeInfo("FTOS", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Float to short"),
    "DTOC": OpcodeInfo("DTOC", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.CHAR, "Double to char"),
    "DTOS": OpcodeInfo("DTOS", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Double to short"),

    # In-place sign/zero extensions (SCS/SCI/SSI/UCS/UCI/USI)
    "SCS": OpcodeInfo("SCS", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Signed char to short"),
    "SCI": OpcodeInfo("SCI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Signed char to int"),
    "SSI": OpcodeInfo("SSI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Signed short to int"),
    "UCS": OpcodeInfo("UCS", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.SHORT, "Unsigned char to short"),
    "UCI": OpcodeInfo("UCI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned char to int"),
    "USI": OpcodeInfo("USI", 1, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned short to int"),

    # Unsigned comparisons (char/short)
    "UCLES": OpcodeInfo("UCLES", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned char less than"),
    "UCLEQ": OpcodeInfo("UCLEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned char less or equal"),
    "UCGRE": OpcodeInfo("UCGRE", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned char greater than"),
    "UCGEQ": OpcodeInfo("UCGEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned char greater or equal"),
    "USLES": OpcodeInfo("USLES", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned short less than"),
    "USLEQ": OpcodeInfo("USLEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned short less or equal"),
    "USGRE": OpcodeInfo("USGRE", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned short greater than"),
    "USGEQ": OpcodeInfo("USGEQ", 2, 1, ArgType.NONE, ArgType.NONE, ResultType.INT, "Unsigned short greater or equal"),
}

for info in _ADDITIONAL_INFO.values():
    _INFO_BY_MNEMONIC.setdefault(info.mnemonic, info)


# =============================================================================
# OPCODE RESOLVERS
# =============================================================================

COMPILER_OPCODE_MAP: Dict[int, str] = {opcode: info.mnemonic for opcode, info in OPCODE_INFO.items()}

_JUMP_MNEMONICS = {"JMP", "JZ", "JNZ"}
_CONDITIONAL_JUMP_MNEMONICS = {"JZ", "JNZ"}
_CALL_MNEMONICS = {"CALL"}
_EXTERNAL_CALL_MNEMONICS = {"XCALL"}
_INTERNAL_CALL_MNEMONICS = {"CALL"}
_RETURN_MNEMONICS = {"RET"}


@dataclass
class OpcodeResolver:
    name: str
    opcode_map: Dict[int, str]

    def __post_init__(self) -> None:
        self.mnemonic_to_opcode: Dict[str, int] = {mnemonic: opcode for opcode, mnemonic in self.opcode_map.items()}
        self.jump_opcodes: Set[int] = {opcode for opcode, mnemonic in self.opcode_map.items() if mnemonic in _JUMP_MNEMONICS}
        self.conditional_jump_opcodes: Set[int] = {opcode for opcode, mnemonic in self.opcode_map.items() if mnemonic in _CONDITIONAL_JUMP_MNEMONICS}
        self.call_opcodes: Set[int] = {opcode for opcode, mnemonic in self.opcode_map.items() if mnemonic in _CALL_MNEMONICS}
        self.external_call_opcodes: Set[int] = {opcode for opcode, mnemonic in self.opcode_map.items() if mnemonic in _EXTERNAL_CALL_MNEMONICS}
        self.internal_call_opcodes: Set[int] = {opcode for opcode, mnemonic in self.opcode_map.items() if mnemonic in _INTERNAL_CALL_MNEMONICS}
        self.return_opcodes: Set[int] = {opcode for opcode, mnemonic in self.opcode_map.items() if mnemonic in _RETURN_MNEMONICS}

    def get_mnemonic(self, opcode: int) -> str:
        return self.opcode_map.get(opcode, f"UNK_{opcode}")

    def get_info(self, opcode: int) -> Optional[OpcodeInfo]:
        mnemonic = self.opcode_map.get(opcode)
        if not mnemonic:
            return None
        return _INFO_BY_MNEMONIC.get(mnemonic)

    def is_jump(self, opcode: int) -> bool:
        return opcode in self.jump_opcodes

    def is_conditional_jump(self, opcode: int) -> bool:
        return opcode in self.conditional_jump_opcodes

    def is_call(self, opcode: int) -> bool:
        return opcode in self.call_opcodes or opcode in self.external_call_opcodes

    def is_return(self, opcode: int) -> bool:
        return opcode in self.return_opcodes

    def is_internal_call(self, opcode: int) -> bool:
        return opcode in self.internal_call_opcodes


COMPILER_RESOLVER = OpcodeResolver("compiler", COMPILER_OPCODE_MAP)
RUNTIME_RESOLVER = OpcodeResolver("runtime", RUNTIME_OPCODE_MAP)
RESOLVERS: Dict[str, OpcodeResolver] = {resolver.name: resolver for resolver in (COMPILER_RESOLVER, RUNTIME_RESOLVER)}
DEFAULT_RESOLVER = RUNTIME_RESOLVER

OPCODE_MNEMONICS = DEFAULT_RESOLVER.opcode_map
MNEMONIC_TO_OPCODE = DEFAULT_RESOLVER.mnemonic_to_opcode
JUMP_OPCODES = DEFAULT_RESOLVER.jump_opcodes
CONDITIONAL_JUMP_OPCODES = DEFAULT_RESOLVER.conditional_jump_opcodes
CALL_OPCODES = DEFAULT_RESOLVER.call_opcodes
EXTERNAL_CALL_OPCODES = DEFAULT_RESOLVER.external_call_opcodes
INTERNAL_CALL_OPCODES = DEFAULT_RESOLVER.internal_call_opcodes
RETURN_OPCODES = DEFAULT_RESOLVER.return_opcodes


def get_resolver(name: str) -> OpcodeResolver:
    return RESOLVERS.get(name, DEFAULT_RESOLVER)


# =============================================================================
# HELPER FUNKCE
# =============================================================================

def get_mnemonic(opcode: int) -> str:
    return DEFAULT_RESOLVER.get_mnemonic(opcode)


def get_opcode_info(opcode: int) -> Optional[OpcodeInfo]:
    return DEFAULT_RESOLVER.get_info(opcode)


def is_jump(opcode: int) -> bool:
    return DEFAULT_RESOLVER.is_jump(opcode)


def is_conditional_jump(opcode: int) -> bool:
    return DEFAULT_RESOLVER.is_conditional_jump(opcode)


def is_call(opcode: int) -> bool:
    return DEFAULT_RESOLVER.is_call(opcode)


def is_return(opcode: int) -> bool:
    return DEFAULT_RESOLVER.is_return(opcode)


def is_internal_call(opcode: int) -> bool:
    return DEFAULT_RESOLVER.is_internal_call(opcode)


__all__ = [
    'ArgType', 'ResultType', 'OpcodeInfo', 'OpcodeResolver',
    'OPCODE_MNEMONICS', 'OPCODE_INFO',
    'COMPILER_RESOLVER', 'RUNTIME_RESOLVER', 'RESOLVERS', 'get_resolver',
    'get_mnemonic', 'get_opcode_info',
    'is_jump', 'is_conditional_jump', 'is_call', 'is_return', 'is_internal_call',
]
