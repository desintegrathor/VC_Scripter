"""
Difference categorization system for bytecode comparison.

Provides formal categorization of differences into SEMANTIC, COSMETIC,
OPTIMIZATION, and UNKNOWN categories to help understand the nature and
impact of differences between original and recompiled bytecode.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional

from .bytecode_compare import Difference, DifferenceType, DifferenceSeverity


class DifferenceCategory(Enum):
    """
    High-level category describing the nature of a difference.

    Categories help distinguish between differences that affect program
    behavior vs. those that are purely cosmetic or optimization-related.
    """
    SEMANTIC = "semantic"           # Changes program behavior
    COSMETIC = "cosmetic"           # No behavioral impact (ordering, formatting, padding)
    OPTIMIZATION = "optimization"   # Semantically equivalent but different implementation
    UNKNOWN = "unknown"             # Cannot determine category


@dataclass
class CategorizedDifference:
    """
    A difference with its category determined.

    Attributes:
        difference: The original Difference object
        category: Determined category (SEMANTIC, COSMETIC, OPTIMIZATION, UNKNOWN)
        rationale: Human-readable explanation of why this category was assigned
    """
    difference: Difference
    category: DifferenceCategory
    rationale: str

    def __str__(self) -> str:
        """Human-readable representation."""
        category_symbol = {
            DifferenceCategory.SEMANTIC: "⚠️",
            DifferenceCategory.COSMETIC: "ℹ️",
            DifferenceCategory.OPTIMIZATION: "🔧",
            DifferenceCategory.UNKNOWN: "❓",
        }
        symbol = category_symbol.get(self.category, "•")

        return f"{symbol} [{self.category.value.upper()}] {self.difference}"


class DifferenceCategorizer:
    """
    Categorizes differences into semantic, cosmetic, optimization, or unknown.

    Uses heuristics based on difference type, severity, description, and
    the informal 'category' field in difference details.
    """

    # Keyword mappings for categorization
    SEMANTIC_KEYWORDS = {
        "entry point", "parameter count", "parameter type", "return value",
        "missing", "control flow", "function", "signature", "instruction count",
        "global pointer count", "critical", "behav"
    }

    COSMETIC_KEYWORDS = {
        "reorder", "alignment", "padding", "ordering", "offset", "different location",
        "cosmetic", "format"
    }

    OPTIMIZATION_KEYWORDS = {
        "optimization", "equivalent", "same result", "different encoding",
        "compiler difference"
    }

    def categorize(self, difference: Difference) -> CategorizedDifference:
        """
        Categorize a single difference.

        Args:
            difference: The difference to categorize

        Returns:
            CategorizedDifference with category and rationale
        """
        # First check if there's an explicit category in details
        if "category" in difference.details:
            explicit_category = difference.details["category"]
            category, rationale = self._categorize_from_explicit(
                explicit_category, difference
            )
            if category != DifferenceCategory.UNKNOWN:
                return CategorizedDifference(difference, category, rationale)

        # Fall back to heuristic categorization
        category, rationale = self._categorize_heuristic(difference)
        return CategorizedDifference(difference, category, rationale)

    def categorize_all(self, differences: List[Difference]) -> List[CategorizedDifference]:
        """
        Categorize a list of differences.

        Args:
            differences: List of differences to categorize

        Returns:
            List of categorized differences
        """
        return [self.categorize(diff) for diff in differences]

    def _categorize_from_explicit(
        self,
        explicit_category: str,
        difference: Difference
    ) -> tuple[DifferenceCategory, str]:
        """
        Categorize based on explicit category field in details.

        Returns:
            Tuple of (category, rationale)
        """
        explicit_lower = explicit_category.lower()

        if explicit_lower == "optimization":
            return (
                DifferenceCategory.OPTIMIZATION,
                f"Explicitly marked as optimization: {difference.description}"
            )

        if explicit_lower == "reordering":
            return (
                DifferenceCategory.COSMETIC,
                "Data reordering - same values at different offsets"
            )

        if explicit_lower == "alignment":
            return (
                DifferenceCategory.COSMETIC,
                "Alignment/padding difference - no functional impact"
            )

        if explicit_lower in ("constant", "control_flow"):
            return (
                DifferenceCategory.SEMANTIC,
                f"Affects program semantics: {explicit_lower}"
            )

        # Unknown explicit category
        return (DifferenceCategory.UNKNOWN, f"Unrecognized category: {explicit_category}")

    def _categorize_heuristic(self, difference: Difference) -> tuple[DifferenceCategory, str]:
        """
        Categorize using heuristics based on type, severity, and description.

        Returns:
            Tuple of (category, rationale)
        """
        desc_lower = difference.description.lower()
        impact_lower = difference.details.get("impact", "").lower()
        combined_text = f"{desc_lower} {impact_lower}"

        # Check for semantic indicators
        if any(keyword in combined_text for keyword in self.SEMANTIC_KEYWORDS):
            # Critical severity is almost always semantic
            if difference.severity == DifferenceSeverity.CRITICAL:
                return (
                    DifferenceCategory.SEMANTIC,
                    f"Critical severity with semantic impact: {difference.description}"
                )

            # Major severity with semantic keywords
            if difference.severity == DifferenceSeverity.MAJOR:
                return (
                    DifferenceCategory.SEMANTIC,
                    f"Major difference affecting program semantics: {difference.description}"
                )

        # Check for optimization indicators
        if any(keyword in combined_text for keyword in self.OPTIMIZATION_KEYWORDS):
            return (
                DifferenceCategory.OPTIMIZATION,
                "Semantically equivalent but different implementation"
            )

        # Check for cosmetic indicators
        if any(keyword in combined_text for keyword in self.COSMETIC_KEYWORDS):
            return (
                DifferenceCategory.COSMETIC,
                f"Cosmetic difference with no behavioral impact: {difference.description}"
            )

        # Heuristics based on severity alone
        if difference.severity == DifferenceSeverity.CRITICAL:
            return (
                DifferenceCategory.SEMANTIC,
                "Critical severity indicates semantic difference"
            )

        if difference.severity == DifferenceSeverity.INFO:
            return (
                DifferenceCategory.COSMETIC,
                "Informational severity suggests cosmetic difference"
            )

        # Type-based heuristics
        if difference.type == DifferenceType.HEADER:
            # Header differences are usually semantic unless explicitly cosmetic
            return (
                DifferenceCategory.SEMANTIC,
                "Header changes typically affect program behavior"
            )

        if difference.type == DifferenceType.XFN:
            # XFN differences are semantic (different external functions)
            return (
                DifferenceCategory.SEMANTIC,
                "External function table differences affect available APIs"
            )

        # Default: unknown
        return (
            DifferenceCategory.UNKNOWN,
            "Unable to determine category from available information"
        )


@dataclass
class DifferenceSummary:
    """
    Summary statistics for a set of categorized differences.

    Provides counts and lists of differences grouped by category and severity.
    """
    total_count: int = 0
    semantic_count: int = 0
    cosmetic_count: int = 0
    optimization_count: int = 0
    unknown_count: int = 0

    critical_count: int = 0
    major_count: int = 0
    minor_count: int = 0
    info_count: int = 0

    semantic_differences: List[CategorizedDifference] = None
    cosmetic_differences: List[CategorizedDifference] = None
    optimization_differences: List[CategorizedDifference] = None
    unknown_differences: List[CategorizedDifference] = None

    def __post_init__(self):
        """Initialize lists if not provided."""
        if self.semantic_differences is None:
            self.semantic_differences = []
        if self.cosmetic_differences is None:
            self.cosmetic_differences = []
        if self.optimization_differences is None:
            self.optimization_differences = []
        if self.unknown_differences is None:
            self.unknown_differences = []

    @staticmethod
    def from_categorized_differences(
        categorized: List[CategorizedDifference]
    ) -> DifferenceSummary:
        """
        Create a summary from a list of categorized differences.

        Args:
            categorized: List of categorized differences

        Returns:
            DifferenceSummary with counts and grouped differences
        """
        summary = DifferenceSummary(total_count=len(categorized))

        # Group by category
        for cat_diff in categorized:
            # Count by category
            if cat_diff.category == DifferenceCategory.SEMANTIC:
                summary.semantic_count += 1
                summary.semantic_differences.append(cat_diff)
            elif cat_diff.category == DifferenceCategory.COSMETIC:
                summary.cosmetic_count += 1
                summary.cosmetic_differences.append(cat_diff)
            elif cat_diff.category == DifferenceCategory.OPTIMIZATION:
                summary.optimization_count += 1
                summary.optimization_differences.append(cat_diff)
            else:
                summary.unknown_count += 1
                summary.unknown_differences.append(cat_diff)

            # Count by severity
            severity = cat_diff.difference.severity
            if severity == DifferenceSeverity.CRITICAL:
                summary.critical_count += 1
            elif severity == DifferenceSeverity.MAJOR:
                summary.major_count += 1
            elif severity == DifferenceSeverity.MINOR:
                summary.minor_count += 1
            elif severity == DifferenceSeverity.INFO:
                summary.info_count += 1

        return summary

    def __str__(self) -> str:
        """Human-readable summary."""
        lines = [
            f"Difference Summary ({self.total_count} total):",
            f"",
            f"By Category:",
            f"  Semantic:      {self.semantic_count:3d} (affects behavior)",
            f"  Cosmetic:      {self.cosmetic_count:3d} (no behavioral impact)",
            f"  Optimization:  {self.optimization_count:3d} (equivalent implementation)",
            f"  Unknown:       {self.unknown_count:3d} (unclear impact)",
            f"",
            f"By Severity:",
            f"  Critical:      {self.critical_count:3d}",
            f"  Major:         {self.major_count:3d}",
            f"  Minor:         {self.minor_count:3d}",
            f"  Info:          {self.info_count:3d}",
        ]
        return "\n".join(lines)


def categorize_differences(differences: List[Difference]) -> List[CategorizedDifference]:
    """
    Convenience function to categorize a list of differences.

    Args:
        differences: List of differences to categorize

    Returns:
        List of categorized differences
    """
    categorizer = DifferenceCategorizer()
    return categorizer.categorize_all(differences)


def get_summary(differences: List[Difference]) -> DifferenceSummary:
    """
    Convenience function to get a summary of categorized differences.

    Args:
        differences: List of differences to summarize

    Returns:
        DifferenceSummary with counts and grouped differences
    """
    categorized = categorize_differences(differences)
    return DifferenceSummary.from_categorized_differences(categorized)


def filter_by_category(
    categorized: List[CategorizedDifference],
    category: DifferenceCategory
) -> List[CategorizedDifference]:
    """
    Filter categorized differences by category.

    Args:
        categorized: List of categorized differences
        category: Category to filter by

    Returns:
        List of differences matching the category
    """
    return [cd for cd in categorized if cd.category == category]


def filter_by_severity(
    categorized: List[CategorizedDifference],
    severity: DifferenceSeverity
) -> List[CategorizedDifference]:
    """
    Filter categorized differences by severity.

    Args:
        categorized: List of categorized differences
        severity: Severity to filter by

    Returns:
        List of differences matching the severity
    """
    return [cd for cd in categorized if cd.difference.severity == severity]


def get_semantic_differences(
    categorized: List[CategorizedDifference]
) -> List[CategorizedDifference]:
    """
    Get only semantic differences (those that affect program behavior).

    Args:
        categorized: List of categorized differences

    Returns:
        List of semantic differences
    """
    return filter_by_category(categorized, DifferenceCategory.SEMANTIC)


def get_cosmetic_differences(
    categorized: List[CategorizedDifference]
) -> List[CategorizedDifference]:
    """
    Get only cosmetic differences (those with no behavioral impact).

    Args:
        categorized: List of categorized differences

    Returns:
        List of cosmetic differences
    """
    return filter_by_category(categorized, DifferenceCategory.COSMETIC)
