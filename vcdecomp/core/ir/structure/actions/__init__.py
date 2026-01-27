"""
High-level action passes for structured code refinement.

This package provides Ghidra-style Action classes that run after the main
collapse phase to perform final code transformations and optimizations.

These correspond to Ghidra's Action hierarchy in blockaction.hh:
- ActionFinalStructure: Block ordering and label finalization
- ActionNormalizeBranches: Conditional normalization
- ActionPreferComplement: Symmetric if/else preference
- ActionReturnSplit: Return epilog handling
- ActionNodeJoin: Conditional merging

Each action is a self-contained transformation pass that operates on
the structured block tree.
"""

from __future__ import annotations

from .base import Action
from .final_structure import ActionFinalStructure
# NOTE: Normalization actions disabled - need to adjust for string-based conditions
# from .normalize import ActionNormalizeBranches, ActionPreferComplement

__all__ = [
    'Action',
    'ActionFinalStructure',
    # 'ActionNormalizeBranches',
    # 'ActionPreferComplement',
]
