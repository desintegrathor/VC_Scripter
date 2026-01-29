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
    falls_through_to: Optional[int] = None  # Target case value if fall-through (e.g., case 0: falls through to case 3)
    detection_order: int = 0   # Order in which case was detected during BFS (preserves bytecode order)

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
    nested_headers: Set[int] = None      # Blocks that are nested switch headers (test different variable)
    dispatch_blocks: Set[int] = None    # All blocks in the comparison dispatch chain (if i==0, if i==1, etc.)
    _internal_type: str = "full"         # "full" (2+ cases) or "single_case" (1 case, renders as if)

    def __post_init__(self):
        if self.all_blocks is None:
            self.all_blocks = {self.header_block}
            self.all_blocks.update(c.block_id for c in self.cases)
            if self.default_block is not None:
                self.all_blocks.add(self.default_block)
        if self.default_body_blocks is None and self.default_block is not None:
            self.default_body_blocks = {self.default_block}
        if self.nested_headers is None:
            self.nested_headers = set()
        if self.dispatch_blocks is None:
            self.dispatch_blocks = set()


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
    condition_addrs: Set[int] = None      # Addresses of SSA instructions forming the condition

    # Body tracking (added for proper nested if/else detection)
    true_body: Set[int] = None            # All blocks in TRUE branch body
    false_body: Set[int] = None           # All blocks in FALSE branch body
    merge_point: Optional[int] = None     # Block where branches rejoin

    def __post_init__(self):
        if self.involved_blocks is None:
            self.involved_blocks = set()
        if self.condition_addrs is None:
            self.condition_addrs = set()


@dataclass
class ForLoopInfo:
    """Detected for-loop pattern."""
    var: str                       # Loop variable for display (e.g., "i")
    init: str                      # Initialization expression (e.g., "0")
    condition: str                 # Loop condition (e.g., "i < gRecs")
    increment: str                 # Increment expression (e.g., "i++")
    init_var: str = ""            # Original initialization variable (e.g., "local_2") for filtering
    guard_block: Optional[int] = None  # Optional guard block to omit (if condition is in loop body)


@dataclass
class WhileLoopInfo:
    """
    Detected while-loop pattern.

    Pattern (Ghidra-style):
    - Condition block has exactly 2 outgoing edges
    - One edge targets a clause block (loop body)
    - Clause block has single output flowing back to condition
    - Condition is evaluated BEFORE each iteration

    CFG structure:
        [condition] --false--> [exit]
            |
            v (true)
        [body] --back_edge--> [condition]
    """
    condition: str                 # Loop condition expression (e.g., "x > 0")
    header_block: int              # Block with the condition check (loop header)
    body_blocks: Set[int] = None   # All blocks in loop body
    exit_block: Optional[int] = None  # Block after loop (where false branch goes)

    def __post_init__(self):
        if self.body_blocks is None:
            self.body_blocks = set()


@dataclass
class DoWhileLoopInfo:
    """
    Detected do-while loop pattern.

    Pattern (Ghidra-style):
    - Body executes at least once
    - Condition block at end that loops back to start
    - Condition evaluated AFTER each iteration

    CFG structure:
        [body_start]
            |
            v
        [body_blocks]
            |
            v
        [condition] --true--> [body_start] (back edge)
            |
            v (false)
        [exit]
    """
    condition: str                 # Loop condition expression (e.g., "x > 0")
    body_start_block: int          # First block of loop body (entry point)
    condition_block: int           # Block with condition check (at end of body)
    body_blocks: Set[int] = None   # All blocks in loop body (including condition block)
    exit_block: Optional[int] = None  # Block after loop

    def __post_init__(self):
        if self.body_blocks is None:
            self.body_blocks = {self.body_start_block, self.condition_block}


@dataclass
class TernaryInfo:
    """
    Ternary operator pattern detected from if/else.

    Pattern:
    - true_body and false_body each contain exactly 1 block
    - Each block has exactly 1 assignment expression (no side effects)
    - Both assignments target the SAME variable
    - merge_block exists (branches rejoin)
    - Neither branch has function calls, returns, or breaks

    Renders as:
        result = (x > 0) ? 1 : 0;

    Instead of:
        if (x > 0) {
            result = 1;
        } else {
            result = 0;
        }
    """
    variable: str          # Variable being assigned (e.g., "result")
    condition: str         # Condition expression (e.g., "x > 0")
    true_value: str        # Expression for true branch (e.g., "1")
    false_value: str       # Expression for false branch (e.g., "0")
