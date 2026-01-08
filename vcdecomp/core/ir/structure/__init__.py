"""
Structure analysis package for decompiled code.

This package provides structured output generation for decompiled Vietcong scripts,
including control flow analysis, pattern detection, and code emission.

Public API:
    - format_structured_function: Legacy function for basic structured output
    - format_structured_function_named: Main function for named function output
"""

# Import main orchestrator functions for backward compatibility
from .orchestrator import (
    format_structured_function,
    format_structured_function_named,
)

__all__ = [
    'format_structured_function',
    'format_structured_function_named',
]
