"""
Boolean expression matching and comparison utilities.

This module provides functions for comparing, complementing, and
normalizing boolean expressions. It's used during control flow
structuring to detect patterns like:
- Identical conditions in nested ifs (short-circuit candidates)
- Complementary conditions (a < b vs a >= b)
- Double negation simplification

Modeled after Ghidra's bool.hh and bool.cc.
"""

from __future__ import annotations

from typing import Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)


# Comparison operators and their complements
COMPLEMENT_OPS = {
    "==": "!=",
    "!=": "==",
    "<": ">=",
    ">=": "<",
    ">": "<=",
    "<=": ">",
}

# Commutative operators
COMMUTATIVE_OPS = {"==", "!=", "&&", "||", "+", "*", "&", "|", "^"}


class BooleanMatch:
    """
    Utility class for boolean expression comparison and manipulation.
    """

    @staticmethod
    def are_identical(expr1: str, expr2: str) -> bool:
        """
        Check if two expressions are semantically identical.

        Handles:
        - Whitespace differences
        - Commutative operators (a == b vs b == a)
        - Redundant parentheses

        Args:
            expr1: First expression
            expr2: Second expression

        Returns:
            True if expressions are identical
        """
        # Normalize both expressions
        norm1 = BooleanMatch._normalize(expr1)
        norm2 = BooleanMatch._normalize(expr2)

        if norm1 == norm2:
            return True

        # Try commutative check for simple comparisons
        parts1 = BooleanMatch._parse_binary_expr(norm1)
        parts2 = BooleanMatch._parse_binary_expr(norm2)

        if parts1 and parts2:
            left1, op1, right1 = parts1
            left2, op2, right2 = parts2

            if op1 == op2 and op1 in COMMUTATIVE_OPS:
                # Check if operands are swapped
                if left1 == right2 and right1 == left2:
                    return True

        return False

    @staticmethod
    def are_complementary(expr1: str, expr2: str) -> bool:
        """
        Check if two expressions are logical complements.

        For example:
        - "a < b" and "a >= b" are complements
        - "x == 0" and "x != 0" are complements
        - "cond" and "!cond" are complements

        Args:
            expr1: First expression
            expr2: Second expression

        Returns:
            True if expressions are complements
        """
        norm1 = BooleanMatch._normalize(expr1)
        norm2 = BooleanMatch._normalize(expr2)

        # Check for simple negation: "cond" vs "!cond"
        if norm1 == f"!{norm2}" or norm2 == f"!{norm1}":
            return True

        # Check with space after negation (from normalization): "cond" vs "! cond"
        if norm1 == f"! {norm2}" or norm2 == f"! {norm1}":
            return True

        # Check for negation with parentheses: "cond" vs "!(cond)"
        if norm1 == f"!({norm2})" or norm2 == f"!({norm1})":
            return True

        # Check with space: "cond" vs "! (cond)"
        if norm1 == f"! ({norm2})" or norm2 == f"! ({norm1})":
            return True

        # Check for complementary comparison operators
        parts1 = BooleanMatch._parse_binary_expr(norm1)
        parts2 = BooleanMatch._parse_binary_expr(norm2)

        if parts1 and parts2:
            left1, op1, right1 = parts1
            left2, op2, right2 = parts2

            # Same operands, complementary operators
            if left1 == left2 and right1 == right2:
                if COMPLEMENT_OPS.get(op1) == op2:
                    return True

            # Swapped operands with adjusted complement
            # e.g., "a < b" is complement of "b <= a" (which is same as "a > b" complement)
            if left1 == right2 and right1 == left2:
                swapped_op2 = BooleanMatch._swap_comparison_operands(op2)
                if swapped_op2 and COMPLEMENT_OPS.get(op1) == swapped_op2:
                    return True

        return False

    @staticmethod
    def negate(expr: str) -> str:
        """
        Intelligently negate an expression.

        Handles:
        - Comparison operators (a < b -> a >= b)
        - Double negation removal (!!x -> x)
        - De Morgan's laws (!(a && b) -> !a || !b)
        - Simple negation (!x -> x, x -> !x)

        Args:
            expr: Expression to negate

        Returns:
            Negated expression
        """
        expr = BooleanMatch._normalize(expr)

        # Remove double negation (handle "!! x" with spaces too)
        if expr.startswith("!!"):
            return expr[2:].strip()
        if expr.startswith("! !"):
            return expr[3:].strip()
        if expr.startswith("!(!(") and expr.endswith("))"):
            inner = expr[4:-2]
            if BooleanMatch._is_balanced(inner):
                return inner.strip()

        # Remove simple negation (handle "! x" with space too)
        if expr.startswith("!"):
            inner = expr[1:].strip()
            if inner.startswith("(") and inner.endswith(")"):
                # Check if parentheses are the outer wrapper
                inner_content = inner[1:-1]
                if BooleanMatch._is_balanced(inner_content):
                    return inner_content.strip()
            return inner

        # Try to negate comparison
        parts = BooleanMatch._parse_binary_expr(expr)
        if parts:
            left, op, right = parts
            if op in COMPLEMENT_OPS:
                return f"{left} {COMPLEMENT_OPS[op]} {right}"

        # Try De Morgan's law
        if expr.startswith("(") and expr.endswith(")"):
            inner = expr[1:-1]
            dm_result = BooleanMatch._try_demorgan(inner)
            if dm_result:
                return dm_result

        # Fallback: wrap in negation
        if " " in expr or any(c in expr for c in "()"):
            return f"!({expr})"
        return f"!{expr}"

    @staticmethod
    def _normalize(expr: str) -> str:
        """Normalize an expression for comparison."""
        # Remove leading/trailing whitespace
        expr = expr.strip()

        # Normalize whitespace around operators
        expr = re.sub(r'\s+', ' ', expr)
        expr = re.sub(r'\s*([<>=!&|]+)\s*', r' \1 ', expr)
        expr = re.sub(r'\s+', ' ', expr)

        # Remove redundant outer parentheses
        while expr.startswith("(") and expr.endswith(")"):
            inner = expr[1:-1]
            if BooleanMatch._is_balanced(inner):
                expr = inner
            else:
                break

        return expr.strip()

    @staticmethod
    def _is_balanced(expr: str) -> bool:
        """Check if parentheses are balanced."""
        depth = 0
        for c in expr:
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth < 0:
                    return False
        return depth == 0

    @staticmethod
    def _parse_binary_expr(expr: str) -> Optional[Tuple[str, str, str]]:
        """
        Parse a simple binary expression into (left, operator, right).

        Returns None if not a simple binary expression.
        """
        # List of operators to look for (order matters - longer first)
        operators = ["==", "!=", ">=", "<=", ">", "<", "&&", "||"]

        for op in operators:
            if f" {op} " in expr:
                parts = expr.split(f" {op} ", 1)
                if len(parts) == 2:
                    return (parts[0].strip(), op, parts[1].strip())

        return None

    @staticmethod
    def _swap_comparison_operands(op: str) -> Optional[str]:
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
    def _try_demorgan(expr: str) -> Optional[str]:
        """
        Try to apply De Morgan's law.

        !(a && b) -> !a || !b
        !(a || b) -> !a && !b
        """
        # Look for && or ||
        if " && " in expr:
            parts = expr.split(" && ", 1)
            if len(parts) == 2:
                left = BooleanMatch.negate(parts[0].strip())
                right = BooleanMatch.negate(parts[1].strip())
                return f"{left} || {right}"

        if " || " in expr:
            parts = expr.split(" || ", 1)
            if len(parts) == 2:
                left = BooleanMatch.negate(parts[0].strip())
                right = BooleanMatch.negate(parts[1].strip())
                return f"{left} && {right}"

        return None


def expressions_match(expr1: str, expr2: str) -> bool:
    """Check if two expressions are identical."""
    return BooleanMatch.are_identical(expr1, expr2)


def expressions_complement(expr1: str, expr2: str) -> bool:
    """Check if two expressions are complementary."""
    return BooleanMatch.are_complementary(expr1, expr2)


def negate_expression(expr: str) -> str:
    """Intelligently negate an expression."""
    return BooleanMatch.negate(expr)
