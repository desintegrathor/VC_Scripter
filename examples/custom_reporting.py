#!/usr/bin/env python3
"""
Example: Custom Report Generation

This example demonstrates how to generate custom validation reports
with filtering, custom formatting, and multiple output formats.

Usage:
    python custom_reporting.py <original.scr> <decompiled.c>

Example:
    python custom_reporting.py mission_01.scr mission_01_decompiled.c
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from vcdecomp.validation import (
    ValidationOrchestrator,
    ValidationVerdict,
    ReportGenerator,
    get_semantic_differences,
    get_cosmetic_differences,
    filter_by_severity,
    filter_by_category,
    DifferenceSeverity,
    DifferenceCategory,
)


def generate_custom_text_report(result) -> str:
    """Generate a custom text report with specific formatting."""

    lines = []
    lines.append("=" * 80)
    lines.append("CUSTOM VALIDATION REPORT")
    lines.append("=" * 80)
    lines.append("")

    # Header
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Original:  {result.original_scr_path}")
    lines.append(f"Source:    {result.source_path}")
    lines.append("")

    # Overall verdict
    verdict_symbols = {
        ValidationVerdict.PASS: "✓ PASS",
        ValidationVerdict.PARTIAL: "⚠ PARTIAL",
        ValidationVerdict.FAIL: "✗ FAIL",
        ValidationVerdict.ERROR: "✗ ERROR"
    }

    lines.append("VERDICT")
    lines.append("-" * 80)
    lines.append(f"{verdict_symbols.get(result.verdict, '?')} - {result.verdict.name}")
    lines.append("")

    # Compilation status
    lines.append("COMPILATION")
    lines.append("-" * 80)
    if result.compilation_succeeded:
        lines.append("✓ Compilation successful")
    else:
        lines.append("✗ Compilation failed")
        if result.compilation_result:
            lines.append(f"  Errors: {result.compilation_result.error_count}")
            lines.append(f"  Warnings: {result.compilation_result.warning_count}")
    lines.append("")

    # Summary statistics
    if result.difference_summary:
        summary = result.difference_summary
        lines.append("DIFFERENCE SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total:        {summary.total_count}")
        lines.append(f"  Semantic:   {summary.semantic_count} (affects program behavior)")
        lines.append(f"  Cosmetic:   {summary.cosmetic_count} (formatting/ordering only)")
        lines.append(f"  Optimization: {summary.optimization_count} (equivalent code patterns)")
        lines.append(f"  Unknown:    {summary.unknown_count} (uncategorized)")
        lines.append("")

        lines.append(f"By Severity:")
        lines.append(f"  Critical:   {summary.critical_count}")
        lines.append(f"  Major:      {summary.major_count}")
        lines.append(f"  Minor:      {summary.minor_count}")
        lines.append(f"  Info:       {summary.info_count}")
        lines.append("")

    # Critical issues only
    if result.categorized_differences:
        critical_diffs = filter_by_severity(
            result.categorized_differences,
            DifferenceSeverity.CRITICAL
        )

        if critical_diffs:
            lines.append("CRITICAL ISSUES")
            lines.append("-" * 80)
            for i, diff in enumerate(critical_diffs, 1):
                lines.append(f"{i}. {diff.description}")
                if diff.details:
                    lines.append(f"   {diff.details}")
                lines.append("")

    # Semantic differences (excluding critical, already shown)
    if result.categorized_differences:
        semantic_diffs = get_semantic_differences(result.categorized_differences)
        non_critical_semantic = [
            d for d in semantic_diffs
            if d.severity != DifferenceSeverity.CRITICAL
        ]

        if non_critical_semantic:
            lines.append("SEMANTIC DIFFERENCES (Non-Critical)")
            lines.append("-" * 80)
            for i, diff in enumerate(non_critical_semantic[:10], 1):  # Show max 10
                severity_label = diff.severity.name
                lines.append(f"{i}. [{severity_label}] {diff.description}")
                lines.append("")

            if len(non_critical_semantic) > 10:
                lines.append(f"... and {len(non_critical_semantic) - 10} more semantic differences")
                lines.append("")

    # Recommendations
    if result.recommendations:
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 80)
        for i, rec in enumerate(result.recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")

    lines.append("=" * 80)

    return "\n".join(lines)


def generate_semantic_only_report(result) -> str:
    """Generate a report showing only semantic differences."""

    lines = []
    lines.append("SEMANTIC DIFFERENCES REPORT")
    lines.append("=" * 80)
    lines.append("")

    if not result.categorized_differences:
        lines.append("No differences found.")
        return "\n".join(lines)

    semantic_diffs = get_semantic_differences(result.categorized_differences)

    if not semantic_diffs:
        lines.append("✓ No semantic differences found!")
        lines.append("")
        lines.append("The recompiled bytecode is semantically equivalent to the original.")
        return "\n".join(lines)

    lines.append(f"Found {len(semantic_diffs)} semantic difference(s)")
    lines.append("")

    # Group by section
    by_section = {}
    for diff in semantic_diffs:
        section = diff.type.name
        if section not in by_section:
            by_section[section] = []
        by_section[section].append(diff)

    for section, diffs in by_section.items():
        lines.append(f"{section} SECTION")
        lines.append("-" * 80)

        for i, diff in enumerate(diffs, 1):
            lines.append(f"{i}. [{diff.severity.name}] {diff.description}")
            if diff.details:
                lines.append(f"   Details: {diff.details}")
            lines.append("")

    return "\n".join(lines)


def generate_statistics_report(result) -> str:
    """Generate a statistics-focused report."""

    lines = []
    lines.append("VALIDATION STATISTICS")
    lines.append("=" * 80)
    lines.append("")

    lines.append(f"Files:")
    lines.append(f"  Original SCR:  {result.original_scr_path}")
    lines.append(f"  Decompiled:    {result.source_path}")
    lines.append("")

    lines.append(f"Result:")
    lines.append(f"  Verdict:       {result.verdict.name}")
    lines.append(f"  Compilation:   {'SUCCESS' if result.compilation_succeeded else 'FAILED'}")
    lines.append("")

    if result.difference_summary:
        s = result.difference_summary

        lines.append(f"Differences by Category:")
        lines.append(f"  Semantic:      {s.semantic_count:4d} ({100*s.semantic_count/max(s.total_count,1):5.1f}%)")
        lines.append(f"  Cosmetic:      {s.cosmetic_count:4d} ({100*s.cosmetic_count/max(s.total_count,1):5.1f}%)")
        lines.append(f"  Optimization:  {s.optimization_count:4d} ({100*s.optimization_count/max(s.total_count,1):5.1f}%)")
        lines.append(f"  Unknown:       {s.unknown_count:4d} ({100*s.unknown_count/max(s.total_count,1):5.1f}%)")
        lines.append(f"  Total:         {s.total_count:4d}")
        lines.append("")

        lines.append(f"Differences by Severity:")
        lines.append(f"  Critical:      {s.critical_count:4d} ({100*s.critical_count/max(s.total_count,1):5.1f}%)")
        lines.append(f"  Major:         {s.major_count:4d} ({100*s.major_count/max(s.total_count,1):5.1f}%)")
        lines.append(f"  Minor:         {s.minor_count:4d} ({100*s.minor_count/max(s.total_count,1):5.1f}%)")
        lines.append(f"  Info:          {s.info_count:4d} ({100*s.info_count/max(s.total_count,1):5.1f}%)")
        lines.append(f"  Total:         {s.total_count:4d}")
        lines.append("")

    lines.append("=" * 80)

    return "\n".join(lines)


def main():
    """Generate custom validation reports."""

    # Parse arguments
    if len(sys.argv) != 3:
        print("Usage: python custom_reporting.py <original.scr> <decompiled.c>")
        print("\nExample:")
        print("  python custom_reporting.py ../Compiler-testruns/Testrun1/tdm.scr decompiled/tdm.c")
        sys.exit(1)

    original_scr = sys.argv[1]
    decompiled_source = sys.argv[2]

    # Validate files
    if not os.path.exists(original_scr):
        print(f"Error: Original SCR file not found: {original_scr}")
        sys.exit(1)

    if not os.path.exists(decompiled_source):
        print(f"Error: Decompiled source file not found: {decompiled_source}")
        sys.exit(1)

    print("=" * 80)
    print("Custom Validation Report Generator")
    print("=" * 80)
    print()

    # Configure validator
    compiler_dir = "original-resources/compiler"
    if not os.path.exists(compiler_dir):
        compiler_dir = "../original-resources/compiler"
        if not os.path.exists(compiler_dir):
            print("Error: Cannot find compiler directory!")
            sys.exit(1)

    # Run validation
    print("Running validation...")
    validator = ValidationOrchestrator(
        compiler_dir=compiler_dir,
        timeout=30,
        cache_enabled=True
    )

    result = validator.validate(original_scr, decompiled_source)
    print("✓ Validation complete")
    print()

    # Generate reports
    base_name = Path(decompiled_source).stem

    # 1. Custom text report
    print("Generating custom text report...")
    custom_report = generate_custom_text_report(result)
    custom_file = f"{base_name}_custom.txt"
    with open(custom_file, 'w') as f:
        f.write(custom_report)
    print(f"  Saved to: {custom_file}")

    # 2. Semantic-only report
    print("Generating semantic differences report...")
    semantic_report = generate_semantic_only_report(result)
    semantic_file = f"{base_name}_semantic.txt"
    with open(semantic_file, 'w') as f:
        f.write(semantic_report)
    print(f"  Saved to: {semantic_file}")

    # 3. Statistics report
    print("Generating statistics report...")
    stats_report = generate_statistics_report(result)
    stats_file = f"{base_name}_statistics.txt"
    with open(stats_file, 'w') as f:
        f.write(stats_report)
    print(f"  Saved to: {stats_file}")

    # 4. Standard HTML report (using ReportGenerator)
    print("Generating HTML report...")
    generator = ReportGenerator()
    html_file = f"{base_name}_validation.html"
    generator.save_report(result, html_file, format="html")
    print(f"  Saved to: {html_file}")

    # 5. JSON report (for programmatic use)
    print("Generating JSON report...")
    json_file = f"{base_name}_validation.json"
    generator.save_report(result, json_file, format="json")
    print(f"  Saved to: {json_file}")

    print()
    print("=" * 80)
    print("All reports generated successfully!")
    print("=" * 80)
    print()

    # Display custom report to console
    print(custom_report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
