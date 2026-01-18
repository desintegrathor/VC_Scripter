"""
Error categorization and pattern detection for compilation failures.

This module provides programmatic error analysis capabilities for the validation
system. It enables:

1. Single-result categorization: Group compilation errors by type (syntax, semantic, etc.)
2. Batch pattern detection: Aggregate errors across multiple validation runs
3. Insight generation: Produce human-readable summaries ("70% are syntax errors")

Usage:
    # Categorize errors from a single compilation result
    from vcdecomp.validation.error_analyzer import categorize_compilation_errors
    from vcdecomp.validation.compilation_types import CompilationError

    errors = [...]  # List of CompilationError objects
    categorized = categorize_compilation_errors(errors)
    # Returns: {"syntax": [...], "semantic": [...], "type": [...], ...}

    # Analyze patterns across multiple validation results
    from vcdecomp.validation.error_analyzer import ErrorAnalyzer
    from vcdecomp.validation.validation_types import ValidationResult

    results = [...]  # List of ValidationResult objects
    analyzer = ErrorAnalyzer()
    patterns = analyzer.analyze_batch_results(results)
    insights = analyzer.generate_insights()
    # Returns: ["70.5% (142) are syntax errors", "15.2% (31) are type errors", ...]

Known Error Patterns (based on SCMP.exe compiler output):
    - Syntax errors: "syntax error", "expected ';'", "expected ')'"
    - Semantic errors: "undefined symbol 'foo'", "undeclared identifier", "not declared"
    - Type errors: "type mismatch", "incompatible types", "invalid conversion"
    - Include errors: "cannot open include file", "include not found"
    - Other: All other compilation errors
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict

from .compilation_types import CompilationError
from .validation_types import ValidationResult


def categorize_compilation_errors(errors: List[CompilationError]) -> Dict[str, List[CompilationError]]:
    """
    Categorize compilation errors by type using keyword matching.

    This function groups compilation errors into well-known categories based on
    error message patterns observed in SCMP.exe output. The categorization enables
    programmatic error analysis for quality measurement and decompiler improvement.

    Categories:
        - syntax: Syntax errors (missing semicolons, parentheses, braces)
        - semantic: Undefined symbols, undeclared identifiers
        - type: Type mismatches, incompatible types
        - include: Missing or inaccessible header files
        - other: All other compilation errors

    Args:
        errors: List of CompilationError objects to categorize

    Returns:
        Dictionary mapping error type strings to lists of errors:
        {
            "syntax": [CompilationError(...), ...],
            "semantic": [CompilationError(...), ...],
            "type": [CompilationError(...), ...],
            "include": [CompilationError(...), ...],
            "other": [CompilationError(...), ...]
        }

    Example:
        >>> errors = [
        ...     CompilationError(stage=CompilationStage.SCC, severity=ErrorSeverity.ERROR,
        ...                      message="expected ';' before 'return'"),
        ...     CompilationError(stage=CompilationStage.SCC, severity=ErrorSeverity.ERROR,
        ...                      message="undefined symbol 'foo'"),
        ... ]
        >>> categorized = categorize_compilation_errors(errors)
        >>> len(categorized["syntax"])
        1
        >>> len(categorized["semantic"])
        1
    """
    # Initialize empty categories
    error_types: Dict[str, List[CompilationError]] = {
        "syntax": [],
        "semantic": [],
        "type": [],
        "include": [],
        "other": []
    }

    for error in errors:
        # Categorize based on keywords in error message (case-insensitive)
        msg_lower = error.message.lower()

        if "syntax" in msg_lower or "expected" in msg_lower:
            error_types["syntax"].append(error)
        elif "undefined" in msg_lower or "undeclared" in msg_lower or "not declared" in msg_lower:
            error_types["semantic"].append(error)
        elif "type" in msg_lower or "incompatible" in msg_lower:
            error_types["type"].append(error)
        elif "include" in msg_lower or "cannot open" in msg_lower:
            error_types["include"].append(error)
        else:
            error_types["other"].append(error)

    return error_types


@dataclass
class ErrorPattern:
    """
    Represents an aggregated error pattern across multiple validation runs.

    An ErrorPattern summarizes how frequently a particular error type occurs
    in a batch of validation results, along with example errors for inspection.

    Attributes:
        error_type: Category name (e.g., "syntax", "semantic", "type")
        count: Total number of errors of this type across all results
        percentage: Percentage of total errors (0-100)
        examples: Sample CompilationError objects (max 3)

    Example:
        >>> pattern = ErrorPattern(
        ...     error_type="syntax",
        ...     count=142,
        ...     percentage=70.5,
        ...     examples=[error1, error2, error3]
        ... )
        >>> print(pattern)
        syntax: 142 errors (70.5%)
          Example: expected ';' before 'return'
          Example: expected ')' before ';'
          Example: syntax error
    """
    error_type: str
    count: int
    percentage: float
    examples: List[CompilationError] = field(default_factory=list)

    def __str__(self) -> str:
        """Human-readable error pattern representation."""
        lines = [f"{self.error_type}: {self.count} errors ({self.percentage:.1f}%)"]

        for example in self.examples[:3]:  # Limit to 3 examples
            lines.append(f"  Example: {example.message}")

        return "\n".join(lines)


class ErrorAnalyzer:
    """
    Aggregate and analyze error patterns across multiple validation results.

    ErrorAnalyzer collects compilation errors from a batch of validation results,
    categorizes them, computes statistics, and generates human-readable insights.
    This enables systematic identification of the most common decompiler failure modes.

    Usage:
        >>> analyzer = ErrorAnalyzer()
        >>> patterns = analyzer.analyze_batch_results(validation_results)
        >>> insights = analyzer.generate_insights()
        >>> for insight in insights:
        ...     print(insight)
        70.5% (142) are syntax errors
        15.2% (31) are type errors
        10.1% (20) are semantic errors
    """

    def __init__(self):
        """Initialize error analyzer with empty state."""
        self._patterns: List[ErrorPattern] = []
        self._total_errors: int = 0

    def analyze_batch_results(self, results: List[ValidationResult]) -> List[ErrorPattern]:
        """
        Analyze error patterns across multiple validation results.

        This method:
        1. Extracts compilation errors from all results
        2. Categorizes each error by type (syntax, semantic, type, include, other)
        3. Accumulates counts by category
        4. Stores first 3 examples of each category
        5. Calculates percentages
        6. Returns patterns sorted by frequency (most common first)

        Args:
            results: List of ValidationResult objects to analyze

        Returns:
            List of ErrorPattern objects sorted by count (descending)

        Example:
            >>> results = [
            ...     ValidationResult(..., compilation_result=CompilationResult(...)),
            ...     ValidationResult(..., compilation_result=CompilationResult(...)),
            ... ]
            >>> patterns = analyzer.analyze_batch_results(results)
            >>> patterns[0].error_type  # Most common error type
            'syntax'
        """
        # Accumulate errors by category across all results
        all_categorized: Dict[str, List[CompilationError]] = {
            "syntax": [],
            "semantic": [],
            "type": [],
            "include": [],
            "other": []
        }

        # Process each validation result
        for result in results:
            # Skip results without compilation results or with successful compilation
            if not result.compilation_result or result.compilation_succeeded:
                continue

            # Categorize errors from this result
            categorized = categorize_compilation_errors(result.compilation_result.errors)

            # Accumulate into global counts
            for error_type, errors in categorized.items():
                all_categorized[error_type].extend(errors)

        # Calculate total error count
        self._total_errors = sum(len(errors) for errors in all_categorized.values())

        # Build ErrorPattern objects
        patterns: List[ErrorPattern] = []
        for error_type, errors in all_categorized.items():
            if not errors:
                continue  # Skip empty categories

            count = len(errors)
            percentage = (count / self._total_errors * 100) if self._total_errors > 0 else 0.0
            examples = errors[:3]  # Store first 3 examples

            patterns.append(ErrorPattern(
                error_type=error_type,
                count=count,
                percentage=percentage,
                examples=examples
            ))

        # Sort by count (descending) - most common errors first
        patterns.sort(key=lambda p: p.count, reverse=True)

        self._patterns = patterns
        return patterns

    def generate_insights(self) -> List[str]:
        """
        Generate human-readable insights from analyzed patterns.

        Returns list of insight strings formatted as:
        "70.5% (142) are syntax errors"

        Insights are sorted by frequency (most common first).

        Returns:
            List of human-readable insight strings

        Example:
            >>> insights = analyzer.generate_insights()
            >>> insights[0]
            '70.5% (142) are syntax errors'
        """
        insights: List[str] = []

        for pattern in self._patterns:
            insight = f"{pattern.percentage:.1f}% ({pattern.count}) are {pattern.error_type} errors"
            insights.append(insight)

        return insights
