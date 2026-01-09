#!/usr/bin/env python3
"""
Example: Batch Validation with Custom Filtering

This example demonstrates how to validate multiple decompiled scripts
with custom filtering and reporting.

Usage:
    python validate_batch.py <original_dir> <decompiled_dir>

Example:
    python validate_batch.py ../script-folders/mission_01/ decompiled/mission_01/
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from vcdecomp.validation import (
    ValidationOrchestrator,
    ValidationVerdict,
    ReportGenerator,
    get_semantic_differences,
    filter_by_severity,
    DifferenceSeverity,
)


def find_script_pairs(original_dir: str, decompiled_dir: str) -> List[Tuple[str, str]]:
    """
    Find pairs of original .scr files and decompiled .c files.

    Returns:
        List of (original_scr, decompiled_c) tuples
    """
    pairs = []

    original_path = Path(original_dir)
    decompiled_path = Path(decompiled_dir)

    # Find all .scr files in original directory
    for scr_file in original_path.glob("*.scr"):
        # Look for corresponding .c file
        c_file = decompiled_path / f"{scr_file.stem}.c"

        if c_file.exists():
            pairs.append((str(scr_file), str(c_file)))
        else:
            print(f"Warning: No decompiled file found for {scr_file.name}")

    return pairs


def validate_single_pair(
    validator: ValidationOrchestrator,
    original_scr: str,
    decompiled_source: str
) -> Tuple[str, object]:
    """
    Validate a single script pair.

    Returns:
        Tuple of (filename, validation_result)
    """
    filename = Path(original_scr).name

    try:
        result = validator.validate(original_scr, decompiled_source)
        return (filename, result)
    except Exception as e:
        print(f"Error validating {filename}: {e}")
        return (filename, None)


def main():
    """Run batch validation with custom filtering and reporting."""

    # Parse command line arguments
    if len(sys.argv) != 3:
        print("Usage: python validate_batch.py <original_dir> <decompiled_dir>")
        print("\nExample:")
        print("  python validate_batch.py ../Compiler-testruns/Testrun1/ decompiled/")
        sys.exit(1)

    original_dir = sys.argv[1]
    decompiled_dir = sys.argv[2]

    # Validate directories
    if not os.path.exists(original_dir):
        print(f"Error: Original directory not found: {original_dir}")
        sys.exit(1)

    if not os.path.exists(decompiled_dir):
        print(f"Error: Decompiled directory not found: {decompiled_dir}")
        sys.exit(1)

    print("=" * 70)
    print("VC Script Validation - Batch Mode")
    print("=" * 70)
    print(f"Original:   {original_dir}")
    print(f"Decompiled: {decompiled_dir}")
    print()

    # Find script pairs
    print("Scanning for script pairs...")
    pairs = find_script_pairs(original_dir, decompiled_dir)

    if not pairs:
        print("No script pairs found!")
        sys.exit(1)

    print(f"Found {len(pairs)} script pair(s) to validate")
    print()

    # Configure compiler path
    compiler_dir = "original-resources/compiler"
    if not os.path.exists(compiler_dir):
        compiler_dir = "../original-resources/compiler"
        if not os.path.exists(compiler_dir):
            print("Error: Cannot find compiler directory!")
            sys.exit(1)

    # Create validation orchestrator
    validator = ValidationOrchestrator(
        compiler_dir=compiler_dir,
        timeout=60,  # Longer timeout for batch
        cache_enabled=True
    )

    # Run validation in parallel
    print("Starting parallel validation (4 workers)...")
    print()

    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all validation tasks
        futures = {
            executor.submit(validate_single_pair, validator, orig, decomp): (orig, decomp)
            for orig, decomp in pairs
        }

        # Collect results as they complete
        for i, future in enumerate(as_completed(futures), 1):
            filename, result = future.result()
            results.append((filename, result))

            # Print progress
            if result:
                verdict_symbol = {
                    ValidationVerdict.PASS: "✓",
                    ValidationVerdict.PARTIAL: "⚠",
                    ValidationVerdict.FAIL: "✗",
                    ValidationVerdict.ERROR: "✗"
                }.get(result.verdict, "?")

                print(f"[{i}/{len(pairs)}] {verdict_symbol} {filename}: {result.verdict.name}")
            else:
                print(f"[{i}/{len(pairs)}] ✗ {filename}: ERROR")

    # Generate summary report
    print()
    print("=" * 70)
    print("BATCH VALIDATION SUMMARY")
    print("=" * 70)
    print()

    # Count results by verdict
    pass_count = sum(1 for _, r in results if r and r.verdict == ValidationVerdict.PASS)
    partial_count = sum(1 for _, r in results if r and r.verdict == ValidationVerdict.PARTIAL)
    fail_count = sum(1 for _, r in results if r and r.verdict == ValidationVerdict.FAIL)
    error_count = sum(1 for _, r in results if r is None or r.verdict == ValidationVerdict.ERROR)

    print(f"Total Files:  {len(results)}")
    print(f"  Passed:     {pass_count} ({100*pass_count/len(results):.1f}%)")
    print(f"  Partial:    {partial_count} ({100*partial_count/len(results):.1f}%)")
    print(f"  Failed:     {fail_count} ({100*fail_count/len(results):.1f}%)")
    print(f"  Errors:     {error_count} ({100*error_count/len(results):.1f}%)")
    print()

    # Custom filtering: Show only files with semantic differences
    print("=" * 70)
    print("FILES WITH SEMANTIC DIFFERENCES")
    print("=" * 70)
    print()

    semantic_issues = []
    for filename, result in results:
        if result and result.categorized_differences:
            semantic_diffs = get_semantic_differences(result.categorized_differences)
            if semantic_diffs:
                semantic_issues.append((filename, semantic_diffs))

    if semantic_issues:
        for filename, diffs in semantic_issues:
            print(f"• {filename}")
            print(f"  Semantic differences: {len(diffs)}")

            # Show critical differences only
            critical_diffs = filter_by_severity(diffs, DifferenceSeverity.CRITICAL)
            if critical_diffs:
                print(f"  Critical issues:")
                for diff in critical_diffs[:3]:  # Show first 3
                    print(f"    - {diff.description}")
            print()
    else:
        print("No semantic differences found! ✓")
        print()

    # Custom filtering: Show compilation failures
    print("=" * 70)
    print("COMPILATION FAILURES")
    print("=" * 70)
    print()

    compilation_failures = [
        (filename, result)
        for filename, result in results
        if result and not result.compilation_succeeded
    ]

    if compilation_failures:
        for filename, result in compilation_failures:
            print(f"• {filename}")
            if result.compilation_result:
                print(f"  Errors: {result.compilation_result.error_count}")
                for error in result.compilation_result.errors[:3]:  # Show first 3
                    print(f"    - {error.message}")
            print()
    else:
        print("All files compiled successfully! ✓")
        print()

    # Save detailed JSON report
    report_file = "batch_validation_report.json"
    print(f"Saving detailed JSON report to {report_file}...")

    # Create comprehensive report
    generator = ReportGenerator()

    # Generate individual reports and save as JSON
    batch_report = {
        "summary": {
            "total": len(results),
            "passed": pass_count,
            "partial": partial_count,
            "failed": fail_count,
            "errors": error_count,
        },
        "files": []
    }

    for filename, result in results:
        if result:
            batch_report["files"].append({
                "filename": filename,
                "verdict": result.verdict.name,
                "compilation_succeeded": result.compilation_succeeded,
                "semantic_differences": result.difference_summary.semantic_count if result.difference_summary else 0,
                "cosmetic_differences": result.difference_summary.cosmetic_count if result.difference_summary else 0,
                "total_differences": result.difference_summary.total_count if result.difference_summary else 0,
            })

    # Save JSON
    import json
    with open(report_file, 'w') as f:
        json.dump(batch_report, f, indent=2)

    print(f"Report saved to: {report_file}")
    print()

    # Display cache statistics
    cache_stats = validator.get_cache_statistics()
    if cache_stats.total > 0:
        print("=" * 70)
        print("CACHE STATISTICS")
        print("=" * 70)
        print(f"Cache hits:   {cache_stats.hits}")
        print(f"Cache misses: {cache_stats.misses}")
        print(f"Hit rate:     {cache_stats.hit_rate:.1%}")
        print()

    # Return exit code
    if fail_count > 0 or error_count > 0:
        print("✗ BATCH VALIDATION FAILED")
        return 1
    elif partial_count > 0:
        print("⚠ BATCH VALIDATION PARTIAL (cosmetic differences)")
        return 0
    else:
        print("✓ BATCH VALIDATION PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
