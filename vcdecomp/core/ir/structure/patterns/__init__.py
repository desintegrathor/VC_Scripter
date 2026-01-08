"""
Pattern detection module for control flow analysis.

This module provides data models and detection algorithms for various
control flow patterns in decompiled code.
"""

from .models import (
    CaseInfo,
    SwitchPattern,
    IfElsePattern,
    CompoundCondition,
    ForLoopInfo,
)

from .if_else import (
    _detect_early_return_pattern,
    _detect_short_circuit_pattern,
    _detect_if_else_pattern,
)

from .switch_case import (
    _detect_switch_patterns,
    _find_switch_variable_from_nearby_gcp,
)

__all__ = [
    # Data models
    "CaseInfo",
    "SwitchPattern",
    "IfElsePattern",
    "CompoundCondition",
    "ForLoopInfo",
    # If/else detection
    "_detect_early_return_pattern",
    "_detect_short_circuit_pattern",
    "_detect_if_else_pattern",
    # Switch/case detection
    "_detect_switch_patterns",
    "_find_switch_variable_from_nearby_gcp",
]
