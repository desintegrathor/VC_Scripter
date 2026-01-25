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
    WhileLoopInfo,
    DoWhileLoopInfo,
    TernaryInfo,
)

from .if_else import (
    _detect_early_return_pattern,
    _detect_short_circuit_pattern,
    _detect_if_else_pattern,
    _detect_ternary_pattern,
)

from .switch_case import (
    _detect_switch_patterns,
    _find_switch_variable_from_nearby_gcp,
)

from .loops import (
    _detect_for_loop,
    _detect_while_loop,
    _detect_do_while_loop,
    _detect_loop_type,
)

__all__ = [
    # Data models
    "CaseInfo",
    "SwitchPattern",
    "IfElsePattern",
    "CompoundCondition",
    "ForLoopInfo",
    "WhileLoopInfo",
    "DoWhileLoopInfo",
    "TernaryInfo",
    # If/else detection
    "_detect_early_return_pattern",
    "_detect_short_circuit_pattern",
    "_detect_if_else_pattern",
    "_detect_ternary_pattern",
    # Switch/case detection
    "_detect_switch_patterns",
    "_find_switch_variable_from_nearby_gcp",
    # Loop detection
    "_detect_for_loop",
    "_detect_while_loop",
    "_detect_do_while_loop",
    "_detect_loop_type",
]
