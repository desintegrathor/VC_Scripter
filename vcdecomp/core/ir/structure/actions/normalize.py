"""
Actions for conditional normalization and preference.

Implements:
- ActionNormalizeBranches: Normalize comparison operators in conditionals
- ActionPreferComplement: Choose between symmetric if/else alternatives

Corresponds to Ghidra's ActionNormalizeBranches and ActionPreferComplement
in blockaction.cc:2117 and :2140.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .base import Action
from ..blocks.hierarchy import (
    BlockType,
    StructuredBlock,
    BlockIf,
    BlockList,
    BlockWhileDo,
    BlockDoWhile,
    BlockInfLoop,
    BlockSwitch,
)
from ...expr import (
    Expression,
    ExprType,
    BinaryOp,
)

if TYPE_CHECKING:
    from ..blocks.hierarchy import BlockGraph

logger = logging.getLogger(__name__)


class ActionNormalizeBranches(Action):
    """
    Normalize conditional branches to preferred comparison forms.

    This action flips conditionals to use preferred comparison operators.
    For example, it may prefer:
    - (x == 0) over (0 == x)
    - (x < 10) over (10 > x)
    - (x != NULL) over !(x == NULL)

    Corresponds to Ghidra's ActionNormalizeBranches in blockaction.cc:2117.
    """

    def __init__(self):
        """Initialize the normalize branches action."""
        super().__init__("ActionNormalizeBranches")

    def apply(self, graph: 'BlockGraph') -> int:
        """
        Apply branch normalization.

        Args:
            graph: The block graph

        Returns:
            Number of normalizations performed
        """
        self.count = 0

        if graph.root:
            self._normalize_block(graph.root)

        return self.count

    def _normalize_block(self, block: StructuredBlock) -> None:
        """
        Recursively normalize branches in a block.

        Args:
            block: The block to normalize
        """
        # Check if this is a conditional block with a condition we can normalize
        if isinstance(block, (BlockIf, BlockWhileDo, BlockDoWhile)):
            if hasattr(block, 'condition') and block.condition:
                normalized = self._normalize_condition(block.condition)
                if normalized is not block.condition:
                    block.condition = normalized
                    self.count += 1

        # Recurse into children
        if isinstance(block, BlockList):
            for component in block.components:
                self._normalize_block(component)

        elif isinstance(block, BlockIf):
            if block.true_block:
                self._normalize_block(block.true_block)
            if block.false_block:
                self._normalize_block(block.false_block)

        elif isinstance(block, (BlockWhileDo, BlockDoWhile, BlockInfLoop)):
            if block.body_block:
                self._normalize_block(block.body_block)

        elif isinstance(block, BlockSwitch):
            for case_block in block.case_blocks.values():
                if case_block:
                    self._normalize_block(case_block)
            if block.default_block:
                self._normalize_block(block.default_block)

    def _normalize_condition(self, condition: Expression) -> Expression:
        """
        Normalize a conditional expression.

        Applies transformations to prefer certain comparison forms:
        1. Constants on right side: (0 == x) -> (x == 0)
        2. Prefer != over !(...==...)
        3. Canonical comparison direction

        Args:
            condition: The condition to normalize

        Returns:
            Normalized condition (may be same object if no change)
        """
        # Only normalize binary comparisons
        if condition.type != ExprType.BINARY:
            return condition

        op = condition.op
        left = condition.left
        right = condition.right

        # Rule 1: Constant on right side
        # If left is constant and right is variable, flip
        if self._is_constant(left) and not self._is_constant(right):
            # Flip the comparison
            flipped_op = self._flip_comparison(op)
            if flipped_op:
                logger.debug(f"Normalized: flipped {op} to {flipped_op} (constant to right)")
                return BinaryOp(flipped_op, right, left)

        # Rule 2: Prefer x != y over !(x == y)
        if op == BinaryOp.NOT and left and left.type == ExprType.BINARY:
            if left.op == BinaryOp.EQ:
                logger.debug("Normalized: !(x == y) to (x != y)")
                return BinaryOp(BinaryOp.NE, left.left, left.right)

        # Rule 3: Prefer < over > when equivalent
        # This is more of a stylistic preference
        # (a > b) could be written as (b < a)
        # We prefer < when it reads more naturally

        return condition

    def _is_constant(self, expr: Expression) -> bool:
        """
        Check if an expression is a constant.

        Args:
            expr: The expression to check

        Returns:
            True if the expression is a constant
        """
        if expr is None:
            return False

        return expr.type in (
            ExprType.CONSTANT,
            ExprType.STRING_LITERAL,
        )

    def _flip_comparison(self, op: str) -> str:
        """
        Flip a comparison operator.

        Args:
            op: The operator to flip (e.g., "==", "<", ">")

        Returns:
            Flipped operator, or empty string if not flippable
        """
        flip_map = {
            BinaryOp.EQ: BinaryOp.EQ,  # == stays ==
            BinaryOp.NE: BinaryOp.NE,  # != stays !=
            BinaryOp.LT: BinaryOp.GT,  # < becomes >
            BinaryOp.GT: BinaryOp.LT,  # > becomes <
            BinaryOp.LE: BinaryOp.GE,  # <= becomes >=
            BinaryOp.GE: BinaryOp.LE,  # >= becomes <=
        }
        return flip_map.get(op, "")


class ActionPreferComplement(Action):
    """
    Choose between symmetric if/else structures.

    When there are two equivalent ways to structure an if/else
    (with or without negating the condition), this action chooses
    the more natural form based on heuristics.

    For example, prefer:
        if (x != 0) { A } else { B }
    over:
        if (x == 0) { B } else { A }

    Corresponds to Ghidra's ActionPreferComplement in blockaction.cc:2140.
    """

    def __init__(self):
        """Initialize the prefer complement action."""
        super().__init__("ActionPreferComplement")

    def apply(self, graph: 'BlockGraph') -> int:
        """
        Apply complement preference.

        Args:
            graph: The block graph

        Returns:
            Number of swaps performed
        """
        self.count = 0

        if graph.root:
            self._prefer_complement(graph.root)

        return self.count

    def _prefer_complement(self, block: StructuredBlock) -> None:
        """
        Recursively check for complement preferences.

        Args:
            block: The block to check
        """
        # Check if this is an if/else that should be flipped
        if isinstance(block, BlockIf):
            if self._should_flip_if_else(block):
                self._flip_if_else(block)
                self.count += 1

        # Recurse into children
        if isinstance(block, BlockList):
            for component in block.components:
                self._prefer_complement(component)

        elif isinstance(block, BlockIf):
            if block.true_block:
                self._prefer_complement(block.true_block)
            if block.false_block:
                self._prefer_complement(block.false_block)

        elif isinstance(block, (BlockWhileDo, BlockDoWhile, BlockInfLoop)):
            if block.body_block:
                self._prefer_complement(block.body_block)

        elif isinstance(block, BlockSwitch):
            for case_block in block.case_blocks.values():
                if case_block:
                    self._prefer_complement(case_block)
            if block.default_block:
                self._prefer_complement(block.default_block)

    def _should_flip_if_else(self, if_block: BlockIf) -> bool:
        """
        Determine if an if/else should be flipped.

        Heuristics:
        1. Prefer positive conditions over negative
        2. Prefer non-empty true branch
        3. Prefer simpler true branch
        4. Prefer == over != when both are equivalent

        Args:
            if_block: The if block to check

        Returns:
            True if the if/else should be flipped
        """
        # Must have both branches to flip
        if not if_block.true_block or not if_block.false_block:
            return False

        # Must have a condition
        if not hasattr(if_block, 'condition') or not if_block.condition:
            return False

        condition = if_block.condition

        # Heuristic 1: Prefer positive conditions
        # If condition starts with NOT, consider flipping
        if condition.type == ExprType.UNARY and condition.op == "!":
            logger.debug("Prefer complement: flipping NOT condition")
            return True

        # Heuristic 2: Prefer non-empty true branch
        # If true branch is empty but false is not, flip
        true_is_empty = self._is_empty_block(if_block.true_block)
        false_is_empty = self._is_empty_block(if_block.false_block)

        if true_is_empty and not false_is_empty:
            logger.debug("Prefer complement: true branch empty, false not")
            return True

        # Heuristic 3: Prefer simpler true branch
        # If false branch is significantly simpler, consider flipping
        true_size = self._estimate_block_size(if_block.true_block)
        false_size = self._estimate_block_size(if_block.false_block)

        # If false is much smaller (< 50% of true size), prefer it as true
        if false_size > 0 and true_size > false_size * 2:
            logger.debug(f"Prefer complement: false simpler ({false_size} vs {true_size})")
            return True

        return False

    def _flip_if_else(self, if_block: BlockIf) -> None:
        """
        Flip an if/else by swapping branches and negating condition.

        Args:
            if_block: The if block to flip
        """
        # Swap branches
        if_block.true_block, if_block.false_block = (
            if_block.false_block,
            if_block.true_block
        )

        # Negate condition
        if hasattr(if_block, 'condition') and if_block.condition:
            if_block.condition = self._negate_condition(if_block.condition)

        logger.debug(f"Flipped if/else at block {if_block.block_id}")

    def _negate_condition(self, condition: Expression) -> Expression:
        """
        Negate a conditional expression.

        Args:
            condition: The condition to negate

        Returns:
            Negated condition
        """
        from ...expr import UnaryOp

        # If already a NOT, remove it
        if condition.type == ExprType.UNARY and condition.op == "!":
            return condition.operand

        # If it's a comparison, flip it
        if condition.type == ExprType.BINARY:
            negated_op = self._negate_comparison(condition.op)
            if negated_op:
                return BinaryOp(negated_op, condition.left, condition.right)

        # Otherwise wrap in NOT
        return UnaryOp("!", condition)

    def _negate_comparison(self, op: str) -> str:
        """
        Negate a comparison operator.

        Args:
            op: The operator to negate

        Returns:
            Negated operator, or empty string if not negatable
        """
        negate_map = {
            BinaryOp.EQ: BinaryOp.NE,  # == becomes !=
            BinaryOp.NE: BinaryOp.EQ,  # != becomes ==
            BinaryOp.LT: BinaryOp.GE,  # < becomes >=
            BinaryOp.GE: BinaryOp.LT,  # >= becomes <
            BinaryOp.GT: BinaryOp.LE,  # > becomes <=
            BinaryOp.LE: BinaryOp.GT,  # <= becomes >
        }
        return negate_map.get(op, "")

    def _is_empty_block(self, block: StructuredBlock) -> bool:
        """
        Check if a block is effectively empty.

        Args:
            block: The block to check

        Returns:
            True if the block has no significant content
        """
        # BlockList with no components is empty
        if isinstance(block, BlockList):
            return len(block.components) == 0

        # Other block types are considered non-empty
        # (they have structure even if no instructions)
        return False

    def _estimate_block_size(self, block: StructuredBlock) -> int:
        """
        Estimate the size/complexity of a block.

        Args:
            block: The block to estimate

        Returns:
            Rough size estimate (number of sub-blocks)
        """
        if isinstance(block, BlockList):
            return len(block.components)

        # Count nested blocks
        size = 1
        if isinstance(block, BlockIf):
            if block.true_block:
                size += self._estimate_block_size(block.true_block)
            if block.false_block:
                size += self._estimate_block_size(block.false_block)

        elif isinstance(block, (BlockWhileDo, BlockDoWhile, BlockInfLoop)):
            if block.body_block:
                size += self._estimate_block_size(block.body_block)

        elif isinstance(block, BlockSwitch):
            for case_block in block.case_blocks.values():
                if case_block:
                    size += self._estimate_block_size(case_block)
            if block.default_block:
                size += self._estimate_block_size(block.default_block)

        return size
