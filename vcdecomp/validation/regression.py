"""
Regression testing for validation results.

Provides baseline management and regression detection for CI/CD integration.
Compares current validation results against stored baselines to detect
decompiler regressions (new failures) and improvements (new passes).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any

from .validation_types import ValidationResult, ValidationVerdict


class RegressionStatus(Enum):
    """Status of a file in regression comparison."""
    PASS = "pass"               # Still passing
    FAIL = "fail"               # Still failing
    REGRESSION = "regression"   # Was passing, now failing
    IMPROVEMENT = "improvement" # Was failing, now passing
    NEW = "new"                 # New file not in baseline


@dataclass
class BaselineEntry:
    """Single file entry in baseline."""
    file: str
    verdict: str  # ValidationVerdict name
    compilation_succeeded: bool
    differences_count: int
    semantic_differences: int
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "file": self.file,
            "verdict": self.verdict,
            "compilation_succeeded": self.compilation_succeeded,
            "differences_count": self.differences_count,
            "semantic_differences": self.semantic_differences,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BaselineEntry:
        """Create from dictionary."""
        return cls(
            file=data["file"],
            verdict=data["verdict"],
            compilation_succeeded=data["compilation_succeeded"],
            differences_count=data["differences_count"],
            semantic_differences=data["semantic_differences"],
            timestamp=data["timestamp"],
        )


@dataclass
class RegressionBaseline:
    """
    Baseline of validation results for regression testing.

    Stores expected validation outcomes for a set of files.
    Used to detect regressions (new failures) and improvements (new passes).
    """
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    description: str = ""
    entries: Dict[str, BaselineEntry] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_entry(self, file: str, result: ValidationResult) -> None:
        """Add a validation result to the baseline."""
        entry = BaselineEntry(
            file=file,
            verdict=result.verdict.name,
            compilation_succeeded=result.compilation_succeeded,
            differences_count=len(result.categorized_differences) if result.categorized_differences else 0,
            semantic_differences=sum(
                1 for d in (result.categorized_differences or [])
                if d.category.name == 'SEMANTIC'
            ),
            timestamp=datetime.now().isoformat(),
        )
        self.entries[file] = entry

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "version": self.version,
            "created_at": self.created_at,
            "description": self.description,
            "entries": {
                file: entry.to_dict()
                for file, entry in self.entries.items()
            },
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RegressionBaseline:
        """Create from dictionary."""
        baseline = cls(
            version=data.get("version", "1.0"),
            created_at=data.get("created_at", ""),
            description=data.get("description", ""),
            metadata=data.get("metadata", {}),
        )

        entries_data = data.get("entries", {})
        for file, entry_data in entries_data.items():
            baseline.entries[file] = BaselineEntry.from_dict(entry_data)

        return baseline

    def save(self, path: Path) -> None:
        """Save baseline to JSON file."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> RegressionBaseline:
        """Load baseline from JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


@dataclass
class RegressionItem:
    """Single file in regression report."""
    file: str
    status: RegressionStatus
    baseline_verdict: Optional[str] = None
    current_verdict: Optional[str] = None
    baseline_differences: int = 0
    current_differences: int = 0
    baseline_semantic: int = 0
    current_semantic: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "file": self.file,
            "status": self.status.name,
            "baseline_verdict": self.baseline_verdict,
            "current_verdict": self.current_verdict,
            "baseline_differences": self.baseline_differences,
            "current_differences": self.current_differences,
            "baseline_semantic": self.baseline_semantic,
            "current_semantic": self.current_semantic,
        }


@dataclass
class RegressionReport:
    """
    Report comparing current results against baseline.

    Identifies regressions (new failures), improvements (new passes),
    and stable results (no change).
    """
    baseline_path: Path
    baseline_created: str
    report_created: str = field(default_factory=lambda: datetime.now().isoformat())

    # Categorized results
    regressions: List[RegressionItem] = field(default_factory=list)
    improvements: List[RegressionItem] = field(default_factory=list)
    stable_pass: List[RegressionItem] = field(default_factory=list)
    stable_fail: List[RegressionItem] = field(default_factory=list)
    new_files: List[RegressionItem] = field(default_factory=list)

    @property
    def has_regressions(self) -> bool:
        """Whether there are any regressions."""
        return len(self.regressions) > 0

    @property
    def has_improvements(self) -> bool:
        """Whether there are any improvements."""
        return len(self.improvements) > 0

    @property
    def total_files(self) -> int:
        """Total number of files compared."""
        return (
            len(self.regressions) +
            len(self.improvements) +
            len(self.stable_pass) +
            len(self.stable_fail) +
            len(self.new_files)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "baseline_path": str(self.baseline_path),
            "baseline_created": self.baseline_created,
            "report_created": self.report_created,
            "summary": {
                "total_files": self.total_files,
                "regressions": len(self.regressions),
                "improvements": len(self.improvements),
                "stable_pass": len(self.stable_pass),
                "stable_fail": len(self.stable_fail),
                "new_files": len(self.new_files),
            },
            "regressions": [r.to_dict() for r in self.regressions],
            "improvements": [i.to_dict() for i in self.improvements],
            "stable_pass": [s.to_dict() for s in self.stable_pass],
            "stable_fail": [s.to_dict() for s in self.stable_fail],
            "new_files": [n.to_dict() for n in self.new_files],
        }

    def save(self, path: Path) -> None:
        """Save report to JSON file."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)


class RegressionComparator:
    """
    Compares current validation results against baseline.

    Identifies regressions, improvements, and stable results.
    """

    def __init__(self, baseline: RegressionBaseline):
        """
        Initialize comparator with baseline.

        Args:
            baseline: Baseline to compare against
        """
        self.baseline = baseline

    def compare(
        self,
        current_results: Dict[str, ValidationResult]
    ) -> RegressionReport:
        """
        Compare current results against baseline.

        Args:
            current_results: Dict of {filename: ValidationResult}

        Returns:
            RegressionReport with categorized results
        """
        report = RegressionReport(
            baseline_path=Path(""),  # Will be set by caller
            baseline_created=self.baseline.created_at,
        )

        # Compare each current result against baseline
        for file, result in current_results.items():
            if file not in self.baseline.entries:
                # New file not in baseline
                item = RegressionItem(
                    file=file,
                    status=RegressionStatus.NEW,
                    current_verdict=result.verdict.name,
                    current_differences=len(result.categorized_differences or []),
                    current_semantic=sum(
                        1 for d in (result.categorized_differences or [])
                        if d.category.name == 'SEMANTIC'
                    ),
                )
                report.new_files.append(item)
                continue

            # Compare against baseline
            baseline_entry = self.baseline.entries[file]
            status = self._determine_status(baseline_entry, result)

            item = RegressionItem(
                file=file,
                status=status,
                baseline_verdict=baseline_entry.verdict,
                current_verdict=result.verdict.name,
                baseline_differences=baseline_entry.differences_count,
                current_differences=len(result.categorized_differences or []),
                baseline_semantic=baseline_entry.semantic_differences,
                current_semantic=sum(
                    1 for d in (result.categorized_differences or [])
                    if d.category.name == 'SEMANTIC'
                ),
            )

            # Categorize
            if status == RegressionStatus.REGRESSION:
                report.regressions.append(item)
            elif status == RegressionStatus.IMPROVEMENT:
                report.improvements.append(item)
            elif status == RegressionStatus.PASS:
                report.stable_pass.append(item)
            else:  # FAIL
                report.stable_fail.append(item)

        return report

    def _determine_status(
        self,
        baseline: BaselineEntry,
        current: ValidationResult
    ) -> RegressionStatus:
        """
        Determine regression status by comparing baseline and current.

        A regression is when:
        - Baseline was PASS, current is not PASS
        - Baseline had 0 semantic differences, current has semantic differences

        An improvement is when:
        - Baseline was FAIL/ERROR, current is PASS
        - Baseline had semantic differences, current has none

        Args:
            baseline: Baseline entry
            current: Current validation result

        Returns:
            RegressionStatus
        """
        baseline_pass = baseline.verdict == "PASS"
        current_pass = current.verdict == ValidationVerdict.PASS

        baseline_has_semantic = baseline.semantic_differences > 0
        current_has_semantic = current.has_semantic_differences

        # Regression: was passing, now not passing
        if baseline_pass and not current_pass:
            return RegressionStatus.REGRESSION

        # Regression: had no semantic differences, now has semantic differences
        if not baseline_has_semantic and current_has_semantic:
            return RegressionStatus.REGRESSION

        # Improvement: was failing, now passing
        if not baseline_pass and current_pass:
            return RegressionStatus.IMPROVEMENT

        # Improvement: had semantic differences, now has none
        if baseline_has_semantic and not current_has_semantic:
            return RegressionStatus.IMPROVEMENT

        # Stable
        if current_pass:
            return RegressionStatus.PASS
        else:
            return RegressionStatus.FAIL
