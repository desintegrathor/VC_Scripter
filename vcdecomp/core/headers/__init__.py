"""
Header file parsing and database module.

Parses SC_GLOBAL.H, SC_DEF.H and other Vietcong script headers
to extract function signatures, constants, and structure definitions.
"""

from .parser import HeaderParser
from .database import HeaderDatabase

__all__ = ["HeaderParser", "HeaderDatabase"]
