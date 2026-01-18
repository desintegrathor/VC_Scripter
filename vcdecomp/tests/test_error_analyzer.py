"""
Unit tests for error_analyzer module.

Tests categorization logic, pattern aggregation, and insight generation
to ensure error analysis capabilities work correctly.
"""

import pytest
from pathlib import Path

from vcdecomp.validation.error_analyzer import (
    categorize_compilation_errors,
    ErrorAnalyzer,
    ErrorPattern
)
from vcdecomp.validation.compilation_types import (
    CompilationError,
    CompilationStage,
    ErrorSeverity,
    CompilationResult
)
from vcdecomp.validation.validation_types import ValidationResult


class TestCategorizeCompilationErrors:
    """Test categorize_compilation_errors function."""

    def test_syntax_errors(self):
        """Test that syntax errors are categorized correctly."""
        errors = [
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="expected ';' before 'return'"
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="syntax error at line 42"
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="expected ')' before ';'"
            ),
        ]

        categorized = categorize_compilation_errors(errors)

        assert len(categorized["syntax"]) == 3
        assert len(categorized["semantic"]) == 0
        assert len(categorized["type"]) == 0
        assert len(categorized["include"]) == 0
        assert len(categorized["other"]) == 0

    def test_semantic_errors(self):
        """Test that semantic errors are categorized correctly."""
        errors = [
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="undefined symbol 'foo'"
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="undeclared identifier 'bar'"
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="variable 'baz' not declared"
            ),
        ]

        categorized = categorize_compilation_errors(errors)

        assert len(categorized["syntax"]) == 0
        assert len(categorized["semantic"]) == 3
        assert len(categorized["type"]) == 0
        assert len(categorized["include"]) == 0
        assert len(categorized["other"]) == 0

    def test_type_errors(self):
        """Test that type errors are categorized correctly."""
        errors = [
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="type mismatch in assignment"
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="incompatible types: int and float"
            ),
        ]

        categorized = categorize_compilation_errors(errors)

        assert len(categorized["syntax"]) == 0
        assert len(categorized["semantic"]) == 0
        assert len(categorized["type"]) == 2
        assert len(categorized["include"]) == 0
        assert len(categorized["other"]) == 0

    def test_include_errors(self):
        """Test that include errors are categorized correctly."""
        errors = [
            CompilationError(
                stage=CompilationStage.SPP,
                severity=ErrorSeverity.ERROR,
                message="cannot open include file 'missing.h'"
            ),
            CompilationError(
                stage=CompilationStage.SPP,
                severity=ErrorSeverity.ERROR,
                message="include not found: nonexistent.h"
            ),
        ]

        categorized = categorize_compilation_errors(errors)

        assert len(categorized["syntax"]) == 0
        assert len(categorized["semantic"]) == 0
        assert len(categorized["type"]) == 0
        assert len(categorized["include"]) == 2
        assert len(categorized["other"]) == 0

    def test_other_errors(self):
        """Test that unrecognized errors go to 'other' category."""
        errors = [
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="internal compiler error"
            ),
            CompilationError(
                stage=CompilationStage.SASM,
                severity=ErrorSeverity.ERROR,
                message="assembler directive invalid"
            ),
        ]

        categorized = categorize_compilation_errors(errors)

        assert len(categorized["syntax"]) == 0
        assert len(categorized["semantic"]) == 0
        assert len(categorized["type"]) == 0
        assert len(categorized["include"]) == 0
        assert len(categorized["other"]) == 2

    def test_mixed_errors(self):
        """Test categorization of mixed error types."""
        errors = [
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="expected ';' before 'return'"
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="undefined symbol 'foo'"
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="type mismatch in assignment"
            ),
            CompilationError(
                stage=CompilationStage.SPP,
                severity=ErrorSeverity.ERROR,
                message="cannot open include file 'missing.h'"
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="internal compiler error"
            ),
        ]

        categorized = categorize_compilation_errors(errors)

        assert len(categorized["syntax"]) == 1
        assert len(categorized["semantic"]) == 1
        assert len(categorized["type"]) == 1
        assert len(categorized["include"]) == 1
        assert len(categorized["other"]) == 1

    def test_empty_list(self):
        """Test that empty error list returns empty categories."""
        errors = []
        categorized = categorize_compilation_errors(errors)

        assert len(categorized["syntax"]) == 0
        assert len(categorized["semantic"]) == 0
        assert len(categorized["type"]) == 0
        assert len(categorized["include"]) == 0
        assert len(categorized["other"]) == 0


class TestErrorPattern:
    """Test ErrorPattern dataclass."""

    def test_error_pattern_creation(self):
        """Test ErrorPattern creation with basic attributes."""
        pattern = ErrorPattern(
            error_type="syntax",
            count=10,
            percentage=50.0,
            examples=[]
        )

        assert pattern.error_type == "syntax"
        assert pattern.count == 10
        assert pattern.percentage == 50.0
        assert pattern.examples == []

    def test_error_pattern_str(self):
        """Test ErrorPattern string representation."""
        errors = [
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="expected ';'"
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="syntax error"
            ),
        ]

        pattern = ErrorPattern(
            error_type="syntax",
            count=10,
            percentage=50.0,
            examples=errors
        )

        result = str(pattern)
        assert "syntax: 10 errors (50.0%)" in result
        assert "expected ';'" in result
        assert "syntax error" in result


class TestErrorAnalyzer:
    """Test ErrorAnalyzer class."""

    def test_analyze_batch_results_single_result(self):
        """Test analyzing a single validation result."""
        # Create mock compilation result with errors
        errors = [
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="expected ';' before 'return'"
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="undefined symbol 'foo'"
            ),
        ]

        compilation_result = CompilationResult(
            success=False,
            stage=CompilationStage.SCC,
            errors=errors
        )

        validation_result = ValidationResult(
            original_scr=Path("test.scr"),
            decompiled_source=Path("test.c"),
            compilation_result=compilation_result
        )

        # Analyze
        analyzer = ErrorAnalyzer()
        patterns = analyzer.analyze_batch_results([validation_result])

        # Verify patterns
        assert len(patterns) == 2  # syntax and semantic
        assert patterns[0].count == 1
        assert patterns[1].count == 1

        # Verify one pattern is syntax, one is semantic
        pattern_types = {p.error_type for p in patterns}
        assert "syntax" in pattern_types
        assert "semantic" in pattern_types

    def test_analyze_batch_results_multiple_results(self):
        """Test analyzing multiple validation results."""
        # Create 3 validation results with different error distributions
        results = []

        # Result 1: 3 syntax errors
        result1 = ValidationResult(
            original_scr=Path("test1.scr"),
            decompiled_source=Path("test1.c"),
            compilation_result=CompilationResult(
                success=False,
                stage=CompilationStage.SCC,
                errors=[
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        message="expected ';'"
                    ),
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        message="expected ')'"
                    ),
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        message="syntax error"
                    ),
                ]
            )
        )
        results.append(result1)

        # Result 2: 2 type errors
        result2 = ValidationResult(
            original_scr=Path("test2.scr"),
            decompiled_source=Path("test2.c"),
            compilation_result=CompilationResult(
                success=False,
                stage=CompilationStage.SCC,
                errors=[
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        message="type mismatch"
                    ),
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        message="incompatible types"
                    ),
                ]
            )
        )
        results.append(result2)

        # Result 3: 1 semantic error
        result3 = ValidationResult(
            original_scr=Path("test3.scr"),
            decompiled_source=Path("test3.c"),
            compilation_result=CompilationResult(
                success=False,
                stage=CompilationStage.SCC,
                errors=[
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        message="undefined symbol 'foo'"
                    ),
                ]
            )
        )
        results.append(result3)

        # Analyze
        analyzer = ErrorAnalyzer()
        patterns = analyzer.analyze_batch_results(results)

        # Total errors: 6 (3 syntax + 2 type + 1 semantic)
        # Verify patterns sorted by count
        assert len(patterns) == 3
        assert patterns[0].error_type == "syntax"
        assert patterns[0].count == 3
        assert patterns[0].percentage == pytest.approx(50.0, rel=0.1)

        assert patterns[1].error_type == "type"
        assert patterns[1].count == 2
        assert patterns[1].percentage == pytest.approx(33.3, rel=0.1)

        assert patterns[2].error_type == "semantic"
        assert patterns[2].count == 1
        assert patterns[2].percentage == pytest.approx(16.7, rel=0.1)

    def test_analyze_batch_results_skips_successful_compilation(self):
        """Test that successful compilations are skipped."""
        # Create mix of successful and failed results
        results = []

        # Successful result (should be skipped)
        result1 = ValidationResult(
            original_scr=Path("test1.scr"),
            decompiled_source=Path("test1.c"),
            compilation_result=CompilationResult(
                success=True,
                stage=CompilationStage.SCC,
                errors=[]
            )
        )
        results.append(result1)

        # Failed result (should be analyzed)
        result2 = ValidationResult(
            original_scr=Path("test2.scr"),
            decompiled_source=Path("test2.c"),
            compilation_result=CompilationResult(
                success=False,
                stage=CompilationStage.SCC,
                errors=[
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        message="expected ';'"
                    ),
                ]
            )
        )
        results.append(result2)

        # Analyze
        analyzer = ErrorAnalyzer()
        patterns = analyzer.analyze_batch_results(results)

        # Should only have 1 error from the failed result
        assert len(patterns) == 1
        assert patterns[0].count == 1
        assert patterns[0].error_type == "syntax"

    def test_generate_insights(self):
        """Test insight generation."""
        # Create validation results
        results = []

        result = ValidationResult(
            original_scr=Path("test.scr"),
            decompiled_source=Path("test.c"),
            compilation_result=CompilationResult(
                success=False,
                stage=CompilationStage.SCC,
                errors=[
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        message="expected ';'"
                    ),
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        message="expected ')'"
                    ),
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        message="undefined symbol 'foo'"
                    ),
                ]
            )
        )
        results.append(result)

        # Analyze and generate insights
        analyzer = ErrorAnalyzer()
        analyzer.analyze_batch_results(results)
        insights = analyzer.generate_insights()

        # Should have 2 insights (syntax and semantic)
        assert len(insights) == 2

        # First insight should be most common (syntax: 2 errors)
        assert "66.7%" in insights[0]
        assert "(2)" in insights[0]
        assert "syntax errors" in insights[0]

        # Second insight (semantic: 1 error)
        assert "33.3%" in insights[1]
        assert "(1)" in insights[1]
        assert "semantic errors" in insights[1]

    def test_empty_results_list(self):
        """Test analyzing empty results list."""
        analyzer = ErrorAnalyzer()
        patterns = analyzer.analyze_batch_results([])

        assert len(patterns) == 0

        insights = analyzer.generate_insights()
        assert len(insights) == 0

    def test_examples_limited_to_three(self):
        """Test that examples are limited to 3 per pattern."""
        # Create 5 syntax errors
        errors = [
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message=f"expected ';' at line {i}"
            )
            for i in range(5)
        ]

        compilation_result = CompilationResult(
            success=False,
            stage=CompilationStage.SCC,
            errors=errors
        )

        validation_result = ValidationResult(
            original_scr=Path("test.scr"),
            decompiled_source=Path("test.c"),
            compilation_result=compilation_result
        )

        # Analyze
        analyzer = ErrorAnalyzer()
        patterns = analyzer.analyze_batch_results([validation_result])

        # Should have 1 pattern with 3 examples
        assert len(patterns) == 1
        assert patterns[0].count == 5
        assert len(patterns[0].examples) == 3  # Limited to 3
