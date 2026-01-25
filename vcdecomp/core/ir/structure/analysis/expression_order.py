"""
Expression normalizer for consistent output.

This module provides functions to normalize expressions for:
- Consistent comparison ordering (variable on left, constant on right)
- Consistent additive term ordering (constants last)
- Negation simplification

Modeled after Ghidra's expression normalization in ruleaction.hh.
"""

from __future__ import annotations

from typing import Optional, Tuple, List
import re
import logging

logger = logging.getLogger(__name__)


class ExpressionNormalizer:
    """
    Normalizes expressions for consistent, readable output.
    """

    @staticmethod
    def normalize_comparison(expr: str) -> str:
        """
        Normalize a comparison expression.

        Rules:
        - Variable on left, constant on right: "5 == x" -> "x == 5"
        - Prefer < over > when possible: "x > 5" stays, "5 < x" -> "x > 5"

        Args:
            expr: The comparison expression

        Returns:
            Normalized expression
        """
        expr = expr.strip()

        # Parse the comparison
        parts = ExpressionNormalizer._parse_comparison(expr)
        if not parts:
            return expr

        left, op, right = parts

        # Check if we should swap
        left_is_const = ExpressionNormalizer._is_constant(left)
        right_is_const = ExpressionNormalizer._is_constant(right)

        # If constant on left and variable on right, swap
        if left_is_const and not right_is_const:
            swapped_op = ExpressionNormalizer._swap_comparison_op(op)
            if swapped_op:
                return f"{right} {swapped_op} {left}"

        return f"{left} {op} {right}"

    @staticmethod
    def normalize_additive(expr: str) -> str:
        """
        Normalize an additive expression.

        Rules:
        - Constants last: "5 + x" -> "x + 5"
        - Variables in alphabetical order: "y + x" -> "x + y"

        Args:
            expr: The additive expression

        Returns:
            Normalized expression
        """
        expr = expr.strip()

        # Only handle simple addition
        if " + " not in expr:
            return expr

        parts = expr.split(" + ")
        if len(parts) != 2:
            return expr

        left = parts[0].strip()
        right = parts[1].strip()

        # If left is constant and right is not, swap
        left_is_const = ExpressionNormalizer._is_constant(left)
        right_is_const = ExpressionNormalizer._is_constant(right)

        if left_is_const and not right_is_const:
            return f"{right} + {left}"

        # If both are variables, sort alphabetically
        if not left_is_const and not right_is_const:
            if left > right:
                return f"{right} + {left}"

        return f"{left} + {right}"

    @staticmethod
    def simplify_negation(expr: str) -> str:
        """
        Simplify negation in an expression.

        Rules:
        - Double negation: "!!x" -> "x"
        - Negated comparison: "!(x < 5)" -> "x >= 5"
        - Negated equality: "!(x == 5)" -> "x != 5"

        Args:
            expr: The expression

        Returns:
            Simplified expression
        """
        expr = expr.strip()

        # Double negation
        if expr.startswith("!!"):
            return ExpressionNormalizer.simplify_negation(expr[2:])

        # Negated parenthesized expression
        if expr.startswith("!(") and expr.endswith(")"):
            inner = expr[2:-1]
            # Check if it's a comparison we can flip
            parts = ExpressionNormalizer._parse_comparison(inner)
            if parts:
                left, op, right = parts
                flipped_op = ExpressionNormalizer._negate_comparison_op(op)
                if flipped_op:
                    return f"{left} {flipped_op} {right}"

        # Negated zero check
        if expr.startswith("!") and not expr.startswith("!("):
            inner = expr[1:]
            # "!0" -> "TRUE", "!x" stays as is
            if inner == "0":
                return "TRUE"

        return expr

    @staticmethod
    def normalize(expr: str) -> str:
        """
        Apply all normalization rules.

        Args:
            expr: Expression to normalize

        Returns:
            Fully normalized expression
        """
        # First simplify negation
        expr = ExpressionNormalizer.simplify_negation(expr)

        # Then normalize comparison
        expr = ExpressionNormalizer.normalize_comparison(expr)

        # Finally normalize additive (if applicable)
        if " + " in expr:
            # Only normalize if not inside a comparison
            if not any(op in expr for op in ["==", "!=", "<", ">", "<=", ">="]):
                expr = ExpressionNormalizer.normalize_additive(expr)

        return expr

    @staticmethod
    def _parse_comparison(expr: str) -> Optional[Tuple[str, str, str]]:
        """
        Parse a comparison expression into (left, op, right).
        """
        operators = ["==", "!=", ">=", "<=", ">", "<"]

        for op in operators:
            if f" {op} " in expr:
                parts = expr.split(f" {op} ", 1)
                if len(parts) == 2:
                    return (parts[0].strip(), op, parts[1].strip())

        return None

    @staticmethod
    def _is_constant(expr: str) -> bool:
        """Check if an expression is a constant."""
        expr = expr.strip()

        # Numeric constant
        if expr.lstrip('-').isdigit():
            return True

        # Float constant
        if re.match(r'^-?\d+\.?\d*f?$', expr):
            return True

        # Hex constant
        if re.match(r'^0x[0-9a-fA-F]+$', expr):
            return True

        # NULL
        if expr == "NULL":
            return True

        # TRUE/FALSE
        if expr in ("TRUE", "FALSE", "true", "false"):
            return True

        return False

    @staticmethod
    def _swap_comparison_op(op: str) -> Optional[str]:
        """Get the operator for swapped operands."""
        swap_map = {
            "<": ">",
            ">": "<",
            "<=": ">=",
            ">=": "<=",
            "==": "==",
            "!=": "!=",
        }
        return swap_map.get(op)

    @staticmethod
    def _negate_comparison_op(op: str) -> Optional[str]:
        """Get the negated operator."""
        negate_map = {
            "==": "!=",
            "!=": "==",
            "<": ">=",
            ">=": "<",
            ">": "<=",
            "<=": ">",
        }
        return negate_map.get(op)


def normalize_expression(expr: str) -> str:
    """
    Normalize an expression for consistent output.

    Args:
        expr: Expression to normalize

    Returns:
        Normalized expression
    """
    return ExpressionNormalizer.normalize(expr)


def normalize_comparison(expr: str) -> str:
    """
    Normalize a comparison expression.

    Args:
        expr: Comparison expression

    Returns:
        Normalized comparison
    """
    return ExpressionNormalizer.normalize_comparison(expr)


def simplify_negation(expr: str) -> str:
    """
    Simplify negation in an expression.

    Args:
        expr: Expression with potential negation

    Returns:
        Simplified expression
    """
    return ExpressionNormalizer.simplify_negation(expr)
