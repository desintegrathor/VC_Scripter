"""
Data models for control flow pattern detection.

This module contains dataclasses representing various control flow patterns
detected during decompilation: switch/case patterns, if/else patterns,
compound conditions, and for-loop information.
"""

from __future__ import annotations

from typing import List, Optional, Set
from dataclasses import dataclass


@dataclass
class CaseInfo:
    """Information about one case in a switch statement."""
    value: int                  # Case constant value
    block_id: int              # Block ID for this case body (entry point)
    body_blocks: Set[int] = None  # All blocks in this case body
    has_break: bool = True     # Whether case ends with break (vs fall-through)

    def __post_init__(self):
        if self.body_blocks is None:
            self.body_blocks = {self.block_id}


@dataclass
class SwitchPattern:
    """Detected switch/case pattern."""
    test_var: str              # Variable being tested (e.g., "local_0", "i")
    header_block: int          # Block ID where switch starts
    cases: List[CaseInfo]      # List of cases (value -> block)
    default_block: Optional[int] = None  # Default case block (or None)
    default_body_blocks: Set[int] = None  # All blocks in default body
    exit_block: Optional[int] = None     # Common exit point after switch
    all_blocks: Set[int] = None          # All blocks belonging to this switch

    def __post_init__(self):
        if self.all_blocks is None:
            self.all_blocks = {self.header_block}
            self.all_blocks.update(c.block_id for c in self.cases)
            if self.default_block is not None:
                self.all_blocks.add(self.default_block)
        if self.default_body_blocks is None and self.default_block is not None:
            self.default_body_blocks = {self.default_block}


@dataclass
class IfElsePattern:
    """Detected if/else pattern."""
    header_block: int              # Block with conditional jump
    true_block: int                # Block to execute if condition is true
    false_block: int               # Block to execute if condition is false
    merge_block: Optional[int]     # Block where both branches merge (None if no merge)
    true_body: Set[int] = None     # All blocks in true branch
    false_body: Set[int] = None    # All blocks in false branch

    def __post_init__(self):
        if self.true_body is None:
            self.true_body = {self.true_block}
        if self.false_body is None:
            self.false_body = {self.false_block}


@dataclass
class CompoundCondition:
    """
    Represents a compound logical condition (AND/OR of multiple tests).

    Used to reconstruct short-circuit evaluation patterns like:
    - (A && B)
    - (A || B)
    - ((A && B) || (C && D))

    Conditions can be:
    - Simple strings (rendered condition expressions)
    - Nested CompoundCondition objects (for complex nesting)
    """
    operator: str                          # "&&" or "||"
    conditions: List                       # List[Union[str, CompoundCondition]]
    true_target: int                       # Block to execute if TRUE
    false_target: int                      # Block to execute if FALSE
    involved_blocks: Set[int] = None      # All blocks involved in this compound condition

    def __post_init__(self):
        if self.involved_blocks is None:
            self.involved_blocks = set()


@dataclass
class ForLoopInfo:
    """Detected for-loop pattern."""
    var: str                       # Loop variable for display (e.g., "i")
    init: str                      # Initialization expression (e.g., "0")
    condition: str                 # Loop condition (e.g., "i < gRecs")
    increment: str                 # Increment expression (e.g., "i++")
    init_var: str = ""            # Original initialization variable (e.g., "local_2") for filtering
