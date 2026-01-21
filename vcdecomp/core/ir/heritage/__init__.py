"""
Heritage-based incremental SSA construction.

This package implements Ghidra-style multi-pass SSA construction where
variable locations are "heritaged" (converted to SSA form) incrementally
across multiple passes, allowing for better type inference and variable
splitting as more information becomes available.

Key components:
- LocationMap: Tracks which memory locations have been heritaged
- HeritageOrchestrator: Coordinates multi-pass SSA construction
"""

from .location_map import LocationMap, HeritageRange, AddressSpace
from .heritage_orchestrator import HeritageOrchestrator

__all__ = [
    "LocationMap",
    "HeritageRange",
    "AddressSpace",
    "HeritageOrchestrator",
]
