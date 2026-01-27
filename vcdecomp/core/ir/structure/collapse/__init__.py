"""
Collapse rules and engine for control flow structuring.

This package provides the iterative collapse algorithm that transforms
a flat CFG into a hierarchical block structure.
"""

from .rules import (
    CollapseRule,
    RuleBlockCat,
    RuleBlockProperIf,
    RuleBlockIfElse,
    RuleBlockWhileDo,
    RuleBlockDoWhile,
    RuleBlockSwitch,
    RuleBlockGoto,
    DEFAULT_RULES,
)
from .engine import CollapseStructure, collapse_function
from .trace_dag import TraceDAG, BlockTrace, BranchPoint, BadEdgeScore

__all__ = [
    "CollapseRule",
    "RuleBlockCat",
    "RuleBlockProperIf",
    "RuleBlockIfElse",
    "RuleBlockWhileDo",
    "RuleBlockDoWhile",
    "RuleBlockSwitch",
    "RuleBlockGoto",
    "DEFAULT_RULES",
    "CollapseStructure",
    "collapse_function",
    "TraceDAG",
    "BlockTrace",
    "BranchPoint",
    "BadEdgeScore",
]
