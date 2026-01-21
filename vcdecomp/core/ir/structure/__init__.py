"""
Structure analysis package for decompiled code.

This package provides structured output generation for decompiled Vietcong scripts,
including control flow analysis, pattern detection, and code emission.

Public API:

Main Entry Points:
    - format_structured_function: Legacy function for basic structured output
    - format_structured_function_named: Main function for named function output

Data Models (commonly used classes):
    - CaseInfo: Information about one case in a switch statement
    - SwitchPattern: Detected switch/case pattern
    - IfElsePattern: Detected if/else pattern
    - CompoundCondition: Compound logical condition (AND/OR)
    - ForLoopInfo: Detected for-loop pattern

Pattern Detection (advanced usage):
    - _detect_if_else_pattern: Detect if/else control flow patterns
    - _detect_switch_patterns: Detect switch/case patterns
    - _detect_for_loop: Detect for-loop patterns
    - _detect_early_return_pattern: Detect early return/break patterns
    - _detect_short_circuit_pattern: Detect short-circuit AND/OR conditions

Analysis Functions (advanced usage):
    - _extract_condition_from_block: Extract condition from a block
    - render_condition: Render condition with SSA values and instruction addresses
    - _find_if_body_blocks: Find blocks belonging to if/else branches
    - _collect_local_variables: Collect all local variables in a function

Code Emission (advanced usage):
    - _render_if_else_recursive: Recursively render if/else structures
    - _render_blocks_with_loops: Render blocks with loop detection
    - _format_block_lines: Format block contents as code lines

Utilities:
    - SHOW_BLOCK_COMMENTS: Configuration flag for debug comments
"""

# Main orchestrator functions for backward compatibility
from .orchestrator import (
    format_structured_function,
    format_structured_function_named,
)

# Data models - commonly used classes
from .patterns.models import (
    CaseInfo,
    SwitchPattern,
    IfElsePattern,
    CompoundCondition,
    ForLoopInfo,
)

# Pattern detection functions - for advanced usage and testing
from .patterns.if_else import (
    _detect_if_else_pattern,
    _detect_early_return_pattern,
    _detect_short_circuit_pattern,
)

from .patterns.switch_case import (
    _detect_switch_patterns,
)

from .patterns.loops import (
    _detect_for_loop,
)

# Analysis functions - for advanced usage
from .analysis.condition import (
    _extract_condition_from_block,
    render_condition,
)

from .analysis.flow import (
    _find_if_body_blocks,
)

from .analysis.variables import (
    _collect_local_variables,
)

# Code emission functions - for advanced usage
from .emit.code_emitter import (
    _render_if_else_recursive,
    _render_blocks_with_loops,
)

from .emit.block_formatter import (
    _format_block_lines,
)

# Utilities
from .utils.helpers import (
    SHOW_BLOCK_COMMENTS,
)

# Public API - maintain backward compatibility
__all__ = [
    # Main entry points (most commonly used)
    'format_structured_function',
    'format_structured_function_named',

    # Data models (commonly used classes)
    'CaseInfo',
    'SwitchPattern',
    'IfElsePattern',
    'CompoundCondition',
    'ForLoopInfo',

    # Pattern detection (advanced usage)
    '_detect_if_else_pattern',
    '_detect_switch_patterns',
    '_detect_for_loop',
    '_detect_early_return_pattern',
    '_detect_short_circuit_pattern',

    # Analysis functions (advanced usage)
    '_extract_condition_from_block',
    'render_condition',
    '_find_if_body_blocks',
    '_collect_local_variables',

    # Code emission (advanced usage)
    '_render_if_else_recursive',
    '_render_blocks_with_loops',
    '_format_block_lines',

    # Utilities
    'SHOW_BLOCK_COMMENTS',
]
