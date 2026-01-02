"""
C header parsing module for extracting symbols, types, and constants.
"""

from .header_parser import HeaderParser, parse_headers
from .symbol_db import SymbolDatabase

__all__ = ['HeaderParser', 'parse_headers', 'SymbolDatabase']
