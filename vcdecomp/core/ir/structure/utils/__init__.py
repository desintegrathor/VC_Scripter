"""
Utility functions for structure analysis.

This package contains helper functions and utilities used across
the structure analysis pipeline.
"""

from .helpers import (
    SHOW_BLOCK_COMMENTS,
    _load_symbol_db,
    _build_start_map,
    _dominates,
    _is_control_flow_only,
)

__all__ = [
    "SHOW_BLOCK_COMMENTS",
    "_load_symbol_db",
    "_build_start_map",
    "_dominates",
    "_is_control_flow_only",
]
