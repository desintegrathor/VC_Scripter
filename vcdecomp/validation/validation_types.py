"""
Data structures for validation results.

Defines types for representing the outcome of validation workflows,
including compilation status, comparison results, and overall verdict.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Any
import json

from .compilation_types import CompilationResult
from .bytecode_compare import ComparisonResult
from .difference_types import CategorizedDifference, DifferenceCategory, DifferenceSummary


class ValidationVerdict(Enum):
    """Overall verdict of the validation process."""
    PASS = "pass"           # Bytecode is identical or only cosmetic differences
    PARTIAL = "partial"     # Bytecode compiles but has semantic differences
    FAIL = "fail"           # Compilation failed or critical differences found
    ERROR = "error"         # Validation process encountered an error


@dataclass
class ValidationResult:
    """
    Complete result of a validation workflow.

    Aggregates compilation results, comparison results, and provides
    an overall verdict with actionable recommendations.

    Attributes:
        original_scr: Path to the original .SCR file
        decompiled_source: Path to the decompiled source code
        compilation_result: Result of compiling the decompiled source
        comparison_result: Result of comparing original and recompiled bytecode
        categorized_differences: Differences categorized by type
        difference_summary: Summary statistics of differences
        verdict: Overall validation verdict
        error_message: Error message if validation failed
        recommendations: List of actionable recommendations
        metadata: Additional metadata (timestamps, versions, etc.)
    """
    original_scr: Path
    decompiled_source: Path
    compilation_result: Optional[CompilationResult] = None
    comparison_result: Optional[ComparisonResult] = None
    categorized_differences: List[CategorizedDifference] = field(default_factory=list)
    difference_summary: Optional[DifferenceSummary] = None
    verdict: ValidationVerdict = ValidationVerdict.ERROR
    error_message: Optional[str] = None
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        """Whether validation succeeded (PASS or PARTIAL)."""
        return self.verdict in (ValidationVerdict.PASS, ValidationVerdict.PARTIAL)

    @property
    def compilation_succeeded(self) -> bool:
        """Whether compilation succeeded."""
        return self.compilation_result is not None and self.compilation_result.success

    @property
    def comparison_succeeded(self) -> bool:
        """Whether comparison succeeded."""
        return self.comparison_result is not None and self.comparison_result.is_valid

    @property
    def bytecode_identical(self) -> bool:
        """Whether bytecode is identical."""
        return self.comparison_result is not None and self.comparison_result.identical

    @property
    def has_semantic_differences(self) -> bool:
        """Whether there are semantic differences."""
        if not self.categorized_differences:
            return False
        return any(
            diff.category == DifferenceCategory.SEMANTIC
            for diff in self.categorized_differences
        )

    @property
    def has_cosmetic_differences(self) -> bool:
        """Whether there are only cosmetic differences."""
        if not self.categorized_differences:
            return False
        return any(
            diff.category == DifferenceCategory.COSMETIC
            for diff in self.categorized_differences
        )

    def get_differences_by_category(self, category: DifferenceCategory) -> List[CategorizedDifference]:
        """Get all differences of a specific category."""
        return [diff for diff in self.categorized_differences if diff.category == category]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the validation result
        """
        return {
            "original_scr": str(self.original_scr),
            "decompiled_source": str(self.decompiled_source),
            "verdict": self.verdict.value,
            "success": self.success,
            "error_message": self.error_message,
            "compilation": {
                "succeeded": self.compilation_succeeded,
                "errors": [str(err) for err in self.compilation_result.errors]
                    if self.compilation_result else [],
                "output_file": str(self.compilation_result.output_file)
                    if self.compilation_result and self.compilation_result.output_file else None,
            } if self.compilation_result else None,
            "comparison": {
                "succeeded": self.comparison_succeeded,
                "identical": self.bytecode_identical,
                "difference_count": len(self.categorized_differences),
                "semantic_differences": len(self.get_differences_by_category(DifferenceCategory.SEMANTIC)),
                "cosmetic_differences": len(self.get_differences_by_category(DifferenceCategory.COSMETIC)),
                "optimization_differences": len(self.get_differences_by_category(DifferenceCategory.OPTIMIZATION)),
            } if self.comparison_result else None,
            "summary": {
                "total_count": self.difference_summary.total_count,
                "by_category": {
                    "semantic": self.difference_summary.semantic_count,
                    "cosmetic": self.difference_summary.cosmetic_count,
                    "optimization": self.difference_summary.optimization_count,
                    "unknown": self.difference_summary.unknown_count,
                },
                "by_severity": {
                    "critical": self.difference_summary.critical_count,
                    "major": self.difference_summary.major_count,
                    "minor": self.difference_summary.minor_count,
                    "info": self.difference_summary.info_count,
                },
            } if self.difference_summary else None,
            "recommendations": self.recommendations,
            "metadata": self.metadata,
        }

    def to_json(self, indent: int = 2) -> str:
        """
        Convert to JSON string.

        Args:
            indent: JSON indentation level

        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=indent)

    def __str__(self) -> str:
        """Human-readable validation result."""
        lines = []
        lines.append("=" * 80)
        lines.append("VALIDATION RESULT")
        lines.append("=" * 80)

        # Verdict
        verdict_symbols = {
            ValidationVerdict.PASS: "✓",
            ValidationVerdict.PARTIAL: "⚠",
            ValidationVerdict.FAIL: "✗",
            ValidationVerdict.ERROR: "✗",
        }
        symbol = verdict_symbols.get(self.verdict, "•")
        lines.append(f"\n{symbol} Verdict: {self.verdict.value.upper()}")

        # Files
        lines.append(f"\nOriginal:    {self.original_scr}")
        lines.append(f"Decompiled:  {self.decompiled_source}")

        # Compilation status
        lines.append("\n" + "-" * 80)
        lines.append("COMPILATION")
        lines.append("-" * 80)
        if self.compilation_result:
            if self.compilation_succeeded:
                lines.append(f"✓ Compilation succeeded")
                if self.compilation_result.output_file:
                    lines.append(f"  Output: {self.compilation_result.output_file}")
            else:
                lines.append(f"✗ Compilation failed")
                if self.compilation_result.errors:
                    lines.append(f"  Errors ({len(self.compilation_result.errors)}):")
                    for err in self.compilation_result.errors[:5]:  # Show first 5
                        lines.append(f"    {err}")
                    if len(self.compilation_result.errors) > 5:
                        lines.append(f"    ... and {len(self.compilation_result.errors) - 5} more")
        else:
            lines.append("⚠ No compilation result")

        # Comparison status
        if self.comparison_result:
            lines.append("\n" + "-" * 80)
            lines.append("BYTECODE COMPARISON")
            lines.append("-" * 80)
            if self.bytecode_identical:
                lines.append("✓ Bytecode is identical")
            elif self.categorized_differences:
                lines.append(f"⚠ Found {len(self.categorized_differences)} differences")

                # Show summary by category
                if self.difference_summary:
                    lines.append("\nBy Category:")
                    category_counts = [
                        ("Semantic", self.difference_summary.semantic_count),
                        ("Cosmetic", self.difference_summary.cosmetic_count),
                        ("Optimization", self.difference_summary.optimization_count),
                        ("Unknown", self.difference_summary.unknown_count),
                    ]
                    for cat_name, count in category_counts:
                        if count > 0:
                            lines.append(f"  {cat_name}: {count}")

                    lines.append("\nBy Severity:")
                    severity_counts = [
                        ("Critical", self.difference_summary.critical_count),
                        ("Major", self.difference_summary.major_count),
                        ("Minor", self.difference_summary.minor_count),
                        ("Info", self.difference_summary.info_count),
                    ]
                    for sev_name, count in severity_counts:
                        if count > 0:
                            lines.append(f"  {sev_name}: {count}")

        # Error message
        if self.error_message:
            lines.append("\n" + "-" * 80)
            lines.append("ERROR")
            lines.append("-" * 80)
            lines.append(self.error_message)

        # Recommendations
        if self.recommendations:
            lines.append("\n" + "-" * 80)
            lines.append("RECOMMENDATIONS")
            lines.append("-" * 80)
            for i, rec in enumerate(self.recommendations, 1):
                lines.append(f"{i}. {rec}")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)
