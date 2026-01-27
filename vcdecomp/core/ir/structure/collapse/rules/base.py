"""
Base class for collapse rules.

This module provides the abstract base class that all collapse rules inherit from.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ...blocks.hierarchy import BlockGraph, StructuredBlock


class CollapseRule(ABC):
    """
    Abstract base class for collapse rules.

    Each rule detects a specific control flow pattern and collapses
    it into a higher-level structured block.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        """
        Check if this rule matches at the given block.

        Args:
            graph: The block graph
            block: Block to check for pattern match

        Returns:
            True if the pattern matches
        """
        pass

    @abstractmethod
    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        """
        Apply the rule, collapsing the pattern into a new block.

        Args:
            graph: The block graph
            block: Block where pattern was matched

        Returns:
            The new collapsed block, or None if collapse failed
        """
        pass
