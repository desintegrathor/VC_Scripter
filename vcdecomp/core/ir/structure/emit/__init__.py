"""
Code emission and formatting package.

This package contains modules for formatting and emitting decompiled code,
including block formatting and recursive code rendering.
"""

from .block_formatter import (
    _format_block_lines,
    _format_block_lines_filtered,
)

__all__ = [
    '_format_block_lines',
    '_format_block_lines_filtered',
]
