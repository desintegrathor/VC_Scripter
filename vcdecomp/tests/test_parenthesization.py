"""
Unit tests for parenthesization module.
"""

import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from vcdecomp.core.ir.parenthesization import (
    is_simple_expression,
    needs_parens_in_condition,
    needs_parens,
    wrap_if_needed,
    get_operator_info,
    ExpressionContext,
)


def test_is_simple_expression():
    """Test detection of simple expressions."""
    # Simple identifiers
    assert is_simple_expression("variable")
    assert is_simple_expression("gVar")
    assert is_simple_expression("local_123")
    assert is_simple_expression("_internal")

    # Literals
    assert is_simple_expression("123")
    assert is_simple_expression("0.5f")
    assert is_simple_expression("-42")
    assert is_simple_expression('"string"')

    # Function calls
    assert is_simple_expression("func()")
    assert is_simple_expression("SC_GetInfo(a, b)")
    assert is_simple_expression("calculate(x)")

    # Field/array access
    assert is_simple_expression("obj.field")
    assert is_simple_expression("ptr->member")
    assert is_simple_expression("arr[index]")
    assert is_simple_expression("data[0]")

    # Complex expressions (NOT simple)
    assert not is_simple_expression("a + b")
    assert not is_simple_expression("x > 5")
    assert not is_simple_expression("a && b")
    assert not is_simple_expression("(a + b)")
    assert not is_simple_expression("")

    print("[OK] test_is_simple_expression passed")


def test_needs_parens_in_condition():
    """Test parenthesization logic for if/while conditions."""
    # Simple expressions don't need parens
    assert not needs_parens_in_condition("variable")
    assert not needs_parens_in_condition("func()")
    assert not needs_parens_in_condition("obj->field")

    # Comparison operators don't need extra parens
    assert not needs_parens_in_condition("a > b", ">")
    assert not needs_parens_in_condition("x == 5", "==")
    assert not needs_parens_in_condition("count != 0", "!=")

    # Logical operators don't need extra parens
    assert not needs_parens_in_condition("a && b", "&&")
    assert not needs_parens_in_condition("x || y", "||")
    assert not needs_parens_in_condition("!flag", "!")

    # Already parenthesized expressions
    assert not needs_parens_in_condition("(a > b)")
    assert not needs_parens_in_condition("((a + b) != 0)")

    print("[OK]test_needs_parens_in_condition passed")


def test_operator_precedence():
    """Test operator precedence table lookup."""
    # Multiplicative > Additive
    mul_info = get_operator_info("*")
    add_info = get_operator_info("+")
    assert mul_info.precedence < add_info.precedence  # Lower number = higher precedence

    # Comparison > Logical AND
    cmp_info = get_operator_info("==")
    and_info = get_operator_info("&&")
    assert cmp_info.precedence < and_info.precedence

    # Logical AND > Logical OR
    or_info = get_operator_info("||")
    assert and_info.precedence < or_info.precedence

    print("[OK]test_operator_precedence passed")


def test_needs_parens_precedence():
    """Test parenthesization based on operator precedence."""
    # a + b * c: no parens needed around b * c (higher precedence)
    assert not needs_parens(
        child_expr="b * c",
        child_operator="*",
        parent_operator="+",
        context=ExpressionContext.IN_EXPRESSION,
        is_left_operand=False
    )

    # (a * b) + c: parens needed around a * b when it's right operand of /
    # Wait, that's not right. Let me reconsider.
    # a / (b + c): parens needed around b + c (lower precedence)
    assert needs_parens(
        child_expr="b + c",
        child_operator="+",
        parent_operator="/",
        context=ExpressionContext.IN_EXPRESSION,
        is_left_operand=False
    )

    # a * b + c: no parens around a * b when it's left operand of +
    assert not needs_parens(
        child_expr="a * b",
        child_operator="*",
        parent_operator="+",
        context=ExpressionContext.IN_EXPRESSION,
        is_left_operand=True
    )

    print("[OK]test_needs_parens_precedence passed")


def test_needs_parens_associativity():
    """Test parenthesization based on associativity."""
    # Left associative: a - b - c = (a - b) - c
    # Right operand needs parens: a - (b - c)
    assert needs_parens(
        child_expr="b - c",
        child_operator="-",
        parent_operator="-",
        context=ExpressionContext.IN_EXPRESSION,
        is_left_operand=False  # Right operand
    )

    # Left operand doesn't need parens: (a - b) - c
    assert not needs_parens(
        child_expr="a - b",
        child_operator="-",
        parent_operator="-",
        context=ExpressionContext.IN_EXPRESSION,
        is_left_operand=True  # Left operand
    )

    print("[OK]test_needs_parens_associativity passed")


def test_needs_parens_comparisons():
    """Test specific cases from decompiler output."""
    # Case: if (gPlayersConnected > 0) - no extra parens needed
    assert not needs_parens(
        child_expr="gPlayersConnected > 0",
        child_operator=">",
        parent_operator=None,
        context=ExpressionContext.IN_CONDITION
    )

    # Case: if ((a + b) != 0) - actually, parens NOT needed due to precedence!
    # + has higher precedence than !=, so a + b != 0 parses as (a + b) != 0
    # But for readability, we might want to keep them in complex expressions
    # The "a + b" part does NOT need parens when used with !=:
    assert not needs_parens(
        child_expr="a + b",
        child_operator="+",
        parent_operator="!=",
        context=ExpressionContext.IN_EXPRESSION,
        is_left_operand=True
    )

    # But the whole "((a + b) != 0)" in condition context:
    assert not needs_parens(
        child_expr="(a + b) != 0",
        child_operator="!=",
        parent_operator=None,
        context=ExpressionContext.IN_CONDITION
    )

    print("[OK]test_needs_parens_comparisons passed")


def test_wrap_if_needed():
    """Test wrapping utility function."""
    assert wrap_if_needed("expr", True) == "(expr)"
    assert wrap_if_needed("expr", False) == "expr"
    assert wrap_if_needed("a + b", True) == "(a + b)"
    assert wrap_if_needed("func()", False) == "func()"

    print("[OK]test_wrap_if_needed passed")


def run_all_tests():
    """Run all test functions."""
    print("Running parenthesization unit tests...\n")

    test_is_simple_expression()
    test_needs_parens_in_condition()
    test_operator_precedence()
    test_needs_parens_precedence()
    test_needs_parens_associativity()
    test_needs_parens_comparisons()
    test_wrap_if_needed()

    print("\n[SUCCESS] All tests passed!")


if __name__ == "__main__":
    run_all_tests()
