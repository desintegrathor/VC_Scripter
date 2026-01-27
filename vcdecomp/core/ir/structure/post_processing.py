"""
Post-processing transformations for structured code.

This module contains transformations that run after the collapse phase,
including for-loop detection and other final optimizations.

These are analogous to Ghidra's finalTransform() methods that run after
the main structuring phase is complete.

The post-processing pipeline consists of:
1. ActionFinalStructure - Block ordering, break/goto marking
2. ActionNormalizeBranches - Conditional normalization
3. ActionPreferComplement - Symmetric if/else preference
4. For-loop transformation - While to for-loop conversion
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING
import logging

from .blocks.hierarchy import (
    BlockWhileDo,
    BlockDoWhile,
    BlockList,
    StructuredBlock,
    BlockGraph,
)
from .analysis.for_loop_detection import ForLoopDetector, ForLoopPattern
from .actions import (
    ActionFinalStructure,
    # ActionNormalizeBranches,
    # ActionPreferComplement,
)

if TYPE_CHECKING:
    from ..ssa import SSAFunction

logger = logging.getLogger(__name__)


class PostProcessor:
    """
    Post-processes structured code after collapse.

    Applies transformations like:
    - While-loop to for-loop conversion
    - Code cleanup and optimization
    - Final formatting adjustments
    """

    def __init__(
        self,
        ssa_func: Optional['SSAFunction'] = None,
        enable_actions: bool = True
    ):
        """
        Initialize post-processor.

        Args:
            ssa_func: Optional SSA function for advanced analysis
            enable_actions: Enable Ghidra-style Action passes (default True)
        """
        self.ssa_func = ssa_func
        self.for_loop_detector = ForLoopDetector(ssa_func) if ssa_func else None

        # Ghidra-style Action passes
        self.enable_actions = enable_actions
        self.actions = []
        if enable_actions:
            self.actions.append(ActionFinalStructure())
            # NOTE: Normalization actions disabled for now - need to adjust
            # for string-based condition representation
            # self.actions.append(ActionNormalizeBranches())
            # self.actions.append(ActionPreferComplement())

    def process(self, root: StructuredBlock, graph: Optional[BlockGraph] = None) -> StructuredBlock:
        """
        Run all post-processing transformations.

        Args:
            root: Root of the structured block tree
            graph: Optional BlockGraph for Action passes

        Returns:
            Transformed root block
        """
        # Phase 1: Ghidra-style Action passes (if enabled and graph provided)
        if self.enable_actions and graph:
            for action in self.actions:
                count = action.apply(graph)
                if count > 0:
                    logger.debug(f"{action.name}: {count} changes")

        # Phase 2: Transform while loops to for loops where possible
        self._transform_for_loops(root)

        return root

    def _transform_for_loops(self, block: StructuredBlock) -> None:
        """
        Recursively transform while loops to for loops.

        Args:
            block: Block to process
        """
        # Process this block if it's a while loop
        if isinstance(block, BlockWhileDo) and not block.is_for_loop:
            pattern = self._detect_for_loop_pattern(block)
            if pattern is not None:
                self._apply_for_loop_transformation(block, pattern)

        # Recursively process children
        if isinstance(block, BlockWhileDo):
            if block.body_block:
                self._transform_for_loops(block.body_block)

        elif isinstance(block, BlockList):
            for component in block.components:
                self._transform_for_loops(component)

        # Add more block types as needed

    def _detect_for_loop_pattern(self, while_block: BlockWhileDo) -> Optional[ForLoopPattern]:
        """
        Detect if a while loop can be converted to a for loop.

        Uses SSA-based PHI node analysis if available, otherwise returns None.

        Args:
            while_block: The while loop to analyze

        Returns:
            ForLoopPattern if detected, None otherwise
        """
        if self.for_loop_detector is None:
            logger.debug("No SSA function available for for-loop detection")
            return None

        try:
            pattern = self.for_loop_detector.detect_for_loop(while_block)
            if pattern:
                logger.debug(f"Detected for-loop: {pattern.loop_variable}")
            return pattern
        except Exception as e:
            logger.debug(f"Error detecting for-loop: {e}")
            return None

    def _apply_for_loop_transformation(
        self,
        while_block: BlockWhileDo,
        pattern: ForLoopPattern
    ) -> None:
        """
        Transform a while loop to a for loop.

        Args:
            while_block: The while loop block
            pattern: The detected for-loop pattern
        """
        # Mark as for loop
        while_block.is_for_loop = True
        while_block.for_init = pattern.initializer
        while_block.for_increment = pattern.iterator

        logger.debug(
            f"Transformed while to for: "
            f"init={pattern.initializer}, "
            f"cond=<existing>, "
            f"iter={pattern.iterator}"
        )


def apply_post_processing(
    root: StructuredBlock,
    graph: Optional[BlockGraph] = None,
    ssa_func: Optional['SSAFunction'] = None,
    enable_actions: bool = True
) -> StructuredBlock:
    """
    Apply post-processing transformations to structured code.

    This is the main entry point for post-processing. It should be called
    after the collapse phase is complete.

    Args:
        root: Root of the structured block tree
        graph: Optional BlockGraph for Action passes
        ssa_func: Optional SSA function for advanced analysis
        enable_actions: Enable Ghidra-style Action passes (default True)

    Returns:
        Transformed root block
    """
    processor = PostProcessor(ssa_func, enable_actions=enable_actions)
    return processor.process(root, graph=graph)
