"""
Disassembler module
"""

from .opcodes import OPCODE_INFO, OPCODE_MNEMONICS, get_mnemonic, get_opcode_info

__all__ = ['OPCODE_INFO', 'OPCODE_MNEMONICS', 'get_mnemonic', 'get_opcode_info', 'Disassembler']


def __getattr__(name):
    if name == "Disassembler":
        from .disassembler import Disassembler

        return Disassembler
    raise AttributeError(f"module {__name__} has no attribute {name}")
