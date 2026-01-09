#!/usr/bin/env python3
"""
Example: Regression Testing

This example demonstrates how to use the validation system for regression
testing - detecting when decompiler changes cause new failures or improvements.

Usage:
    python regression_test.py <mode> <original_dir> <decompiled_dir>

Modes:
    baseline  - Create baseline from current validation results
    compare   - Compare current results against baseline
    update    - Update baseline with current results

Example:
    # First run: Create baseline
    python regression_test.py baseline ../Compiler-testruns/ decompiled/

    # After decompiler changes: Check for regressions
    python regression_test.py compare ../Compiler-testruns/ decompiled/

    # Accept new results as baseline
    python regression_test.py update ../Compiler-testruns/ decompiled/
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from vcdecomp.validation import (
    ValidationOrchestrator,
    ValidationVerdict,
    RegressionBaseline,
    RegressionComparator,
    RegressionStatus,
)


def find_script_pairs(original_dir: str, decompiled_dir: str) -> List[Tuple[str, str]]:
    """Find pairs of original .scr and decompiled .c files."""
    pairs = []

    original_path = Path(original_dir)
    decompiled_path = Path(decompiled_dir)

    for scr_file in original_path.rglob("*.scr"):
        # Try to find corresponding .c file
        relative_path = scr_file.relative_to(original_path)
        c_file = decompiled_path / relative_path.with_suffix(".c")

        if c_file.exists():
            pairs.append((str(scr_file), str(c_file)))

    return pairs


def validate_all(
    validator: ValidationOrchestrator,
    pairs: List[Tuple[str, str]]
) -> Dict[str, object]:
    """
    Validate all script pairs and return results dictionary.

    Returns:
        Dictionary mapping filenames to ValidationResult objects
    """
    results = {}

    print(f"Validating {len(pairs)} file(s)...")
    print()

    for i, (original, decompiled) in enumerate(pairs, 1):
        filename = Path(original).name
        print(f"[{i}/{len(pairs)}] Validating {filename}...", end=" ")

        try:
            result = validator.validate(original, decompiled)
            results[filename] = result

            verdict_symbol = {
                ValidationVerdict.PASS: "✓",
                ValidationVerdict.PARTIAL: "⚠",
                ValidationVerdict.FAIL: "✗",
                ValidationVerdict.ERROR: "✗"
            }.get(result.verdict, "?")

            print(f"{verdict_symbol} {result.verdict.name}")

        except Exception as e:
            print(f"✗ ERROR: {e}")
            results[filename] = None

    print()
    return results


def create_baseline_mode(original_dir: str, decompiled_dir: str, baseline_file: str):
    """Create baseline from current validation results."""

    print("=" * 70)
    print("REGRESSION TEST - CREATE BASELINE")
    print("=" * 70)
    print()

    # Find script pairs
    pairs = find_script_pairs(original_dir, decompiled_dir)
    if not pairs:
        print("No script pairs found!")
        sys.exit(1)

    print(f"Found {len(pairs)} script pair(s)")
    print()

    # Configure validator
    compiler_dir = "original-resources/compiler"
    if not os.path.exists(compiler_dir):
        compiler_dir = "../original-resources/compiler"

    validator = ValidationOrchestrator(
        compiler_dir=compiler_dir,
        timeout=60,
        cache_enabled=True
    )

    # Validate all files
    results = validate_all(validator, pairs)

    # Create baseline
    print(f"Creating baseline at {baseline_file}...")
    baseline = RegressionBaseline(baseline_file)

    for filename, result in results.items():
        if result:
            baseline.add_result(filename, result)

    baseline.save()

    # Print summary
    print()
    print("=" * 70)
    print("BASELINE CREATED")
    print("=" * 70)
    print(f"Files in baseline: {len(baseline.entries)}")
    print(f"Baseline file:     {baseline_file}")
    print()

    # Summary statistics
    pass_count = sum(1 for e in baseline.entries.values() if e.verdict == ValidationVerdict.PASS.name)
    partial_count = sum(1 for e in baseline.entries.values() if e.verdict == ValidationVerdict.PARTIAL.name)
    fail_count = sum(1 for e in baseline.entries.values() if e.verdict == ValidationVerdict.FAIL.name)

    print(f"Baseline Statistics:")
    print(f"  Passed:  {pass_count}")
    print(f"  Partial: {partial_count}")
    print(f"  Failed:  {fail_count}")
    print()


def compare_mode(original_dir: str, decompiled_dir: str, baseline_file: str):
    """Compare current results against baseline."""

    print("=" * 70)
    print("REGRESSION TEST - COMPARE AGAINST BASELINE")
    print("=" * 70)
    print()

    # Load baseline
    if not os.path.exists(baseline_file):
        print(f"Error: Baseline file not found: {baseline_file}")
        print("Run in 'baseline' mode first to create a baseline.")
        sys.exit(1)

    baseline = RegressionBaseline(baseline_file)
    baseline.load()

    print(f"Loaded baseline from {baseline_file}")
    print(f"Baseline created: {baseline.created_at}")
    print(f"Files in baseline: {len(baseline.entries)}")
    print()

    # Find script pairs
    pairs = find_script_pairs(original_dir, decompiled_dir)
    if not pairs:
        print("No script pairs found!")
        sys.exit(1)

    # Configure validator
    compiler_dir = "original-resources/compiler"
    if not os.path.exists(compiler_dir):
        compiler_dir = "../original-resources/compiler"

    validator = ValidationOrchestrator(
        compiler_dir=compiler_dir,
        timeout=60,
        cache_enabled=True
    )

    # Validate all files
    current_results = validate_all(validator, pairs)

    # Compare with baseline
    print("Comparing with baseline...")
    print()

    comparator = RegressionComparator(baseline)
    report = comparator.compare(current_results)

    # Print report
    print("=" * 70)
    print("REGRESSION REPORT")
    print("=" * 70)
    print()

    print(f"Total files:   {report.total_files}")
    print(f"Regressions:   {report.regression_count} ✗")
    print(f"Improvements:  {report.improvement_count} ✓")
    print(f"Stable:        {report.stable_count}")
    print(f"New files:     {report.new_files_count}")
    print()

    # Show regressions (most important!)
    if report.regressions:
        print("=" * 70)
        print("REGRESSIONS (New Failures)")
        print("=" * 70)
        print()

        for item in report.regressions:
            print(f"✗ {item.filename}")
            print(f"  Before: {item.baseline_verdict}")

            if item.baseline_semantic_diffs is not None:
                print(f"          {item.baseline_semantic_diffs} semantic difference(s)")

            print(f"  After:  {item.current_verdict}")

            if item.current_semantic_diffs is not None:
                print(f"          {item.current_semantic_diffs} semantic difference(s)")

            print()
    else:
        print("✓ No regressions detected!")
        print()

    # Show improvements
    if report.improvements:
        print("=" * 70)
        print("IMPROVEMENTS (New Passes)")
        print("=" * 70)
        print()

        for item in report.improvements:
            print(f"✓ {item.filename}")
            print(f"  Before: {item.baseline_verdict} ({item.baseline_semantic_diffs} semantic)")
            print(f"  After:  {item.current_verdict} ({item.current_semantic_diffs} semantic)")
            print()

    # Show new files
    if report.new_files:
        print("=" * 70)
        print("NEW FILES (Not in Baseline)")
        print("=" * 70)
        print()

        for item in report.new_files:
            print(f"• {item.filename}: {item.current_verdict}")

        print()

    # Save detailed JSON report
    report_file = "regression_report.json"
    print(f"Saving detailed report to {report_file}...")

    report_data = {
        "timestamp": datetime.now().isoformat(),
        "baseline_file": baseline_file,
        "baseline_created": baseline.created_at,
        "summary": {
            "total_files": report.total_files,
            "regressions": report.regression_count,
            "improvements": report.improvement_count,
            "stable": report.stable_count,
            "new_files": report.new_files_count,
        },
        "regressions": [
            {
                "filename": item.filename,
                "baseline_verdict": item.baseline_verdict,
                "current_verdict": item.current_verdict,
                "baseline_semantic_diffs": item.baseline_semantic_diffs,
                "current_semantic_diffs": item.current_semantic_diffs,
            }
            for item in report.regressions
        ],
        "improvements": [
            {
                "filename": item.filename,
                "baseline_verdict": item.baseline_verdict,
                "current_verdict": item.current_verdict,
            }
            for item in report.improvements
        ],
    }

    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)

    print(f"Report saved to: {report_file}")
    print()

    # Exit code based on regressions
    if report.regression_count > 0:
        print("✗ REGRESSIONS DETECTED - Decompiler may have regressed!")
        return 1
    elif report.improvement_count > 0:
        print("✓ IMPROVEMENTS DETECTED - Decompiler is getting better!")
        return 0
    else:
        print("✓ NO CHANGES - Results are stable")
        return 0


def update_mode(original_dir: str, decompiled_dir: str, baseline_file: str):
    """Update baseline with current results (accept new baseline)."""

    print("=" * 70)
    print("REGRESSION TEST - UPDATE BASELINE")
    print("=" * 70)
    print()

    # Backup existing baseline
    if os.path.exists(baseline_file):
        backup_file = f"{baseline_file}.backup"
        print(f"Backing up existing baseline to {backup_file}...")
        import shutil
        shutil.copy2(baseline_file, backup_file)
        print()

    # Create new baseline (reuse create_baseline_mode)
    create_baseline_mode(original_dir, decompiled_dir, baseline_file)

    print("Baseline updated successfully!")


def main():
    """Main entry point for regression testing."""

    # Parse arguments
    if len(sys.argv) < 4:
        print("Usage: python regression_test.py <mode> <original_dir> <decompiled_dir> [baseline_file]")
        print()
        print("Modes:")
        print("  baseline  - Create baseline from current validation results")
        print("  compare   - Compare current results against baseline")
        print("  update    - Update baseline with current results")
        print()
        print("Example:")
        print("  python regression_test.py baseline ../Compiler-testruns/ decompiled/")
        print("  python regression_test.py compare ../Compiler-testruns/ decompiled/")
        sys.exit(1)

    mode = sys.argv[1]
    original_dir = sys.argv[2]
    decompiled_dir = sys.argv[3]
    baseline_file = sys.argv[4] if len(sys.argv) > 4 else ".validation-baseline.json"

    # Validate mode
    if mode not in ["baseline", "compare", "update"]:
        print(f"Error: Invalid mode '{mode}'")
        print("Valid modes: baseline, compare, update")
        sys.exit(1)

    # Validate directories
    if not os.path.exists(original_dir):
        print(f"Error: Original directory not found: {original_dir}")
        sys.exit(1)

    if not os.path.exists(decompiled_dir):
        print(f"Error: Decompiled directory not found: {decompiled_dir}")
        sys.exit(1)

    # Execute mode
    if mode == "baseline":
        create_baseline_mode(original_dir, decompiled_dir, baseline_file)
        return 0
    elif mode == "compare":
        return compare_mode(original_dir, decompiled_dir, baseline_file)
    elif mode == "update":
        update_mode(original_dir, decompiled_dir, baseline_file)
        return 0


if __name__ == "__main__":
    sys.exit(main())
