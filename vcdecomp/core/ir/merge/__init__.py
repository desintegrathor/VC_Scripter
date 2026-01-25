"""
Variable merging for SSA-to-source transformation.

This package provides cover-based variable merging to combine
multiple SSA values into source-level variables.
"""

from .cover import Cover, CoverPiece, compute_cover
from .high_variable import HighVariable, create_high_variable
from .merge_engine import MergeEngine, merge_ssa_values

__all__ = [
    "Cover",
    "CoverPiece",
    "compute_cover",
    "HighVariable",
    "create_high_variable",
    "MergeEngine",
    "merge_ssa_values",
]
