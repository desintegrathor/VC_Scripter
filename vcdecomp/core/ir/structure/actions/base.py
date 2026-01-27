"""
Base class for structured code transformation actions.

Modeled after Ghidra's Action class in action.hh.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..blocks.hierarchy import BlockGraph


class Action(ABC):
    """
    Base class for code transformation actions.

    Each action represents a self-contained transformation pass that
    can be applied to a BlockGraph or SSA function. Actions are
    typically run in sequence as part of a decompilation pipeline.

    Modeled after Ghidra's Action class.
    """

    def __init__(self, name: str):
        """
        Initialize the action.

        Args:
            name: Human-readable name for this action
        """
        self.name = name
        self.count = 0  # Number of transformations applied

    @abstractmethod
    def apply(self, graph: BlockGraph) -> int:
        """
        Apply this action to a block graph.

        Args:
            graph: The block graph to transform

        Returns:
            Number of changes made (0 if no changes)
        """
        pass

    def reset(self) -> None:
        """Reset the action's state for a new analysis."""
        self.count = 0
