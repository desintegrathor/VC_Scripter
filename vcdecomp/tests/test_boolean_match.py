"""
Tests for the boolean expression matching and expression normalizer modules.
"""

import pytest

from vcdecomp.core.ir.structure.analysis.boolean_match import (
    BooleanMatch,
    expressions_match,
    expressions_complement,
    negate_expression,
)
from vcdecomp.core.ir.structure.analysis.expression_order import (
    ExpressionNormalizer,
    normalize_expression,
    normalize_comparison,
    simplify_negation,
)


class TestBooleanMatchIdentical:
    """Test BooleanMatch.are_identical()."""

    def test_identical_simple(self):
        """Test identical simple expressions."""
        assert BooleanMatch.are_identical("x", "x")
        assert BooleanMatch.are_identical("x > 0", "x > 0")
        assert not BooleanMatch.are_identical("x", "y")

    def test_identical_whitespace_normalization(self):
        """Test that whitespace differences are ignored."""
        assert BooleanMatch.are_identical("x > 0", "x  >  0")
        assert BooleanMatch.are_identical("x>0", "x > 0")
        assert BooleanMatch.are_identical("  x > 0  ", "x > 0")

    def test_identical_commutative_equality(self):
        """Test that commutative operators allow swapped operands."""
        assert BooleanMatch.are_identical("a == b", "b == a")
        assert BooleanMatch.are_identical("a != b", "b != a")

    def test_identical_commutative_logical(self):
        """Test commutative logical operators."""
        assert BooleanMatch.are_identical("a && b", "b && a")
        assert BooleanMatch.are_identical("a || b", "b || a")

    def test_identical_non_commutative(self):
        """Test that non-commutative operators don't swap."""
        assert not BooleanMatch.are_identical("a < b", "b < a")
        assert not BooleanMatch.are_identical("a > b", "b > a")
        assert not BooleanMatch.are_identical("a <= b", "b <= a")
        assert not BooleanMatch.are_identical("a >= b", "b >= a")

    def test_identical_redundant_parens(self):
        """Test that redundant outer parentheses are removed."""
        assert BooleanMatch.are_identical("(x > 0)", "x > 0")
        assert BooleanMatch.are_identical("((x > 0))", "x > 0")


class TestBooleanMatchComplementary:
    """Test BooleanMatch.are_complementary()."""

    def test_complementary_simple_negation(self):
        """Test simple negation is detected as complement."""
        assert BooleanMatch.are_complementary("cond", "!cond")
        assert BooleanMatch.are_complementary("!cond", "cond")

    def test_complementary_parenthesized_negation(self):
        """Test negation with parentheses."""
        assert BooleanMatch.are_complementary("cond", "!(cond)")
        assert BooleanMatch.are_complementary("x > 0", "!(x > 0)")

    def test_complementary_comparison_operators(self):
        """Test complementary comparison operators."""
        assert BooleanMatch.are_complementary("a < b", "a >= b")
        assert BooleanMatch.are_complementary("a >= b", "a < b")
        assert BooleanMatch.are_complementary("a > b", "a <= b")
        assert BooleanMatch.are_complementary("a <= b", "a > b")
        assert BooleanMatch.are_complementary("a == b", "a != b")
        assert BooleanMatch.are_complementary("a != b", "a == b")

    def test_not_complementary(self):
        """Test expressions that are not complements."""
        assert not BooleanMatch.are_complementary("a < b", "a > b")
        assert not BooleanMatch.are_complementary("x", "y")
        assert not BooleanMatch.are_complementary("a == b", "a == c")


class TestBooleanMatchNegate:
    """Test BooleanMatch.negate()."""

    def test_negate_double_negation(self):
        """Test that double negation is removed."""
        assert BooleanMatch.negate("!!x") == "x"
        # Parentheses may be preserved, which is functionally equivalent
        result = BooleanMatch.negate("!!(x > 0)")
        assert result in ("x > 0", "(x > 0)")

    def test_negate_simple_negation(self):
        """Test that simple negation is removed."""
        assert BooleanMatch.negate("!x") == "x"
        assert BooleanMatch.negate("!(cond)") == "cond"

    def test_negate_comparison(self):
        """Test that comparisons are flipped."""
        assert BooleanMatch.negate("a < b") == "a >= b"
        assert BooleanMatch.negate("a >= b") == "a < b"
        assert BooleanMatch.negate("a > b") == "a <= b"
        assert BooleanMatch.negate("a <= b") == "a > b"
        assert BooleanMatch.negate("a == b") == "a != b"
        assert BooleanMatch.negate("a != b") == "a == b"

    def test_negate_fallback(self):
        """Test fallback wrapping in negation."""
        result = BooleanMatch.negate("complex_expr")
        assert result == "!complex_expr"

        result = BooleanMatch.negate("a + b")
        assert result == "!(a + b)"


class TestExpressionNormalizerComparison:
    """Test ExpressionNormalizer.normalize_comparison()."""

    def test_normalize_constant_on_left(self):
        """Test that constant is moved to right side."""
        assert ExpressionNormalizer.normalize_comparison("5 == x") == "x == 5"
        assert ExpressionNormalizer.normalize_comparison("0 != y") == "y != 0"

    def test_normalize_constant_with_less_than(self):
        """Test comparison operator is swapped correctly."""
        assert ExpressionNormalizer.normalize_comparison("5 < x") == "x > 5"
        assert ExpressionNormalizer.normalize_comparison("5 > x") == "x < 5"
        assert ExpressionNormalizer.normalize_comparison("5 <= x") == "x >= 5"
        assert ExpressionNormalizer.normalize_comparison("5 >= x") == "x <= 5"

    def test_normalize_already_normalized(self):
        """Test that already normalized expressions are unchanged."""
        assert ExpressionNormalizer.normalize_comparison("x > 5") == "x > 5"
        assert ExpressionNormalizer.normalize_comparison("y == 0") == "y == 0"

    def test_normalize_two_variables(self):
        """Test that two variables are left as-is."""
        assert ExpressionNormalizer.normalize_comparison("x < y") == "x < y"

    def test_normalize_two_constants(self):
        """Test that two constants are left as-is."""
        assert ExpressionNormalizer.normalize_comparison("5 < 10") == "5 < 10"


class TestExpressionNormalizerAdditive:
    """Test ExpressionNormalizer.normalize_additive()."""

    def test_normalize_constant_first(self):
        """Test that constant is moved to end."""
        assert ExpressionNormalizer.normalize_additive("5 + x") == "x + 5"

    def test_normalize_already_normalized(self):
        """Test that already normalized is unchanged."""
        assert ExpressionNormalizer.normalize_additive("x + 5") == "x + 5"

    def test_normalize_alphabetical_variables(self):
        """Test that variables are sorted alphabetically."""
        assert ExpressionNormalizer.normalize_additive("y + x") == "x + y"
        assert ExpressionNormalizer.normalize_additive("b + a") == "a + b"

    def test_normalize_no_change_needed(self):
        """Test expressions that don't need normalization."""
        assert ExpressionNormalizer.normalize_additive("a + b") == "a + b"
        assert ExpressionNormalizer.normalize_additive("x + y") == "x + y"


class TestExpressionNormalizerNegation:
    """Test ExpressionNormalizer.simplify_negation()."""

    def test_double_negation(self):
        """Test double negation removal."""
        assert ExpressionNormalizer.simplify_negation("!!x") == "x"
        assert ExpressionNormalizer.simplify_negation("!!!!x") == "x"

    def test_negated_comparison(self):
        """Test negated comparison simplification."""
        assert ExpressionNormalizer.simplify_negation("!(x < 5)") == "x >= 5"
        assert ExpressionNormalizer.simplify_negation("!(x == 5)") == "x != 5"
        assert ExpressionNormalizer.simplify_negation("!(x >= 5)") == "x < 5"

    def test_negated_zero(self):
        """Test negated zero becomes TRUE."""
        assert ExpressionNormalizer.simplify_negation("!0") == "TRUE"

    def test_no_simplification_needed(self):
        """Test expressions that don't need simplification."""
        assert ExpressionNormalizer.simplify_negation("x > 5") == "x > 5"
        assert ExpressionNormalizer.simplify_negation("!x") == "!x"


class TestExpressionNormalizerFull:
    """Test ExpressionNormalizer.normalize() (full normalization)."""

    def test_full_normalize(self):
        """Test full normalization applies all rules."""
        # Negation + comparison normalization
        result = ExpressionNormalizer.normalize("!(5 == x)")
        assert result == "x != 5"

    def test_full_normalize_comparison_only(self):
        """Test normalization of comparison only."""
        assert ExpressionNormalizer.normalize("5 < x") == "x > 5"


class TestIsConstant:
    """Test ExpressionNormalizer._is_constant()."""

    def test_integer_constant(self):
        """Test integer constants."""
        assert ExpressionNormalizer._is_constant("5")
        assert ExpressionNormalizer._is_constant("0")
        assert ExpressionNormalizer._is_constant("-10")
        assert ExpressionNormalizer._is_constant("12345")

    def test_float_constant(self):
        """Test float constants."""
        assert ExpressionNormalizer._is_constant("3.14")
        assert ExpressionNormalizer._is_constant("3.14f")
        assert ExpressionNormalizer._is_constant("-2.5")

    def test_hex_constant(self):
        """Test hex constants."""
        assert ExpressionNormalizer._is_constant("0x10")
        assert ExpressionNormalizer._is_constant("0xFF")
        assert ExpressionNormalizer._is_constant("0xDEADBEEF")

    def test_special_constants(self):
        """Test special constants."""
        assert ExpressionNormalizer._is_constant("NULL")
        assert ExpressionNormalizer._is_constant("TRUE")
        assert ExpressionNormalizer._is_constant("FALSE")
        assert ExpressionNormalizer._is_constant("true")
        assert ExpressionNormalizer._is_constant("false")

    def test_not_constant(self):
        """Test non-constants."""
        assert not ExpressionNormalizer._is_constant("x")
        assert not ExpressionNormalizer._is_constant("myVar")
        assert not ExpressionNormalizer._is_constant("func()")


class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    def test_expressions_match(self):
        """Test expressions_match convenience function."""
        assert expressions_match("a == b", "b == a")
        assert not expressions_match("a < b", "b < a")

    def test_expressions_complement(self):
        """Test expressions_complement convenience function."""
        assert expressions_complement("a < b", "a >= b")
        assert not expressions_complement("a < b", "a > b")

    def test_negate_expression(self):
        """Test negate_expression convenience function."""
        assert negate_expression("a < b") == "a >= b"
        assert negate_expression("!x") == "x"

    def test_normalize_expression(self):
        """Test normalize_expression convenience function."""
        assert normalize_expression("5 == x") == "x == 5"

    def test_normalize_comparison(self):
        """Test normalize_comparison convenience function."""
        assert normalize_comparison("5 < x") == "x > 5"

    def test_simplify_negation(self):
        """Test simplify_negation convenience function."""
        assert simplify_negation("!!x") == "x"
