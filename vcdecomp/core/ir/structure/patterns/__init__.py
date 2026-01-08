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

__all__ = [
    "CaseInfo",
    "SwitchPattern",
    "IfElsePattern",
    "CompoundCondition",
    "ForLoopInfo",
]
