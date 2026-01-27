"""
Collapse rules for control flow structuring.

This package provides pattern-matching rules that detect and collapse
control flow patterns into hierarchical block structures.

All rules are modeled after Ghidra's blockaction.hh patterns.
"""

from __future__ import annotations

from typing import List

from .base import CollapseRule
from .basic import RuleBlockCat
from .conditions import RuleBlockOr
from .conditionals import RuleBlockProperIf, RuleBlockIfElse, RuleBlockIfNoExit
from .loops import RuleBlockWhileDo, RuleBlockDoWhile, RuleBlockInfLoop
from .switch import RuleBlockSwitch, RuleCaseFallthru
from .goto import RuleBlockGoto

# Export all rules
__all__ = [
    'CollapseRule',
    'RuleBlockCat',
    'RuleBlockOr',
    'RuleBlockProperIf',
    'RuleBlockIfElse',
    'RuleBlockIfNoExit',
    'RuleBlockWhileDo',
    'RuleBlockDoWhile',
    'RuleBlockInfLoop',
    'RuleBlockSwitch',
    'RuleCaseFallthru',
    'RuleBlockGoto',
    'PRIMARY_RULES',
    'SECONDARY_RULES',
    'DEFAULT_RULES',
]

# Primary rules (Ghidra order) - tried repeatedly until no changes
# Following Ghidra's collapseInternal() rule order
PRIMARY_RULES: List[CollapseRule] = [
    RuleBlockGoto(),      # 1. Handle unstructured first
    RuleBlockCat(),       # 2. Sequential merge
    RuleBlockOr(),        # 3. AND/OR conditions
    RuleBlockProperIf(),  # 4. If-then (no else)
    RuleBlockIfElse(),    # 5. If-then-else
    RuleBlockWhileDo(),   # 6. While loops
    RuleBlockDoWhile(),   # 7. Do-while loops
    RuleBlockInfLoop(),   # 8. Infinite loops
    RuleBlockSwitch(),    # 9. Switch/case (LAST)
]

# Secondary rules (lower priority, only when primary rules stuck)
SECONDARY_RULES: List[CollapseRule] = [
    RuleBlockIfNoExit(),  # 10. Non-exiting if bodies
    RuleCaseFallthru(),   # 11. Switch fall-through
]

# Default rule ordering - for backwards compatibility
DEFAULT_RULES: List[CollapseRule] = PRIMARY_RULES.copy()
