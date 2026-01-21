"""
XFN Table Aggregation Package

Tools for extracting and aggregating function signatures from XFN tables
in compiled .scr bytecode files. XFN tables contain ground-truth type
information from the original Vietcong script compiler.

Usage:
    from vcdecomp.xfn import XFNSignatureParser, XFNAggregator

    # Parse a single XFN signature
    parser = XFNSignatureParser()
    sig = parser.parse("SC_P_GetPos(unsignedlong,*c_Vector3)void")

    # Aggregate from multiple scripts
    aggregator = XFNAggregator()
    result = aggregator.scan_directory("C:\\vc soubory\\LEVELS")
"""

from .signature_parser import XFNSignatureParser, ParsedSignature
from .aggregator import XFNAggregator, AggregationResult

__all__ = [
    "XFNSignatureParser",
    "ParsedSignature",
    "XFNAggregator",
    "AggregationResult",
]
