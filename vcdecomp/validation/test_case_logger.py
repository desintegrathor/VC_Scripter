"""
Test failure logging for reproducible debugging.

This module generates markdown-formatted failure reports for failed validation
test cases. Each report includes:

1. Reproducible Steps - Exact commands to recreate the failure
2. Artifacts - File paths for investigation
3. Error Summary - Categorized compilation errors

The reports enable developers to:
- Reproduce failures without re-running the test suite
- Investigate specific failures in isolation
- Track error patterns over time

Usage:
    from vcdecomp.validation.test_case_logger import log_failed_test_case
    from vcdecomp.validation.validation_types import ValidationResult
    from pathlib import Path

    result = ValidationResult(...)  # Failed validation
    log_failed_test_case(result, Path(".planning/test_failures"))
    # Creates: .planning/test_failures/{test_id}_failure.md

Output Format:
    The generated markdown file contains:
    - Test metadata (date, verdict)
    - Reproducible command-line steps
    - File paths to artifacts
    - Categorized error summary (syntax, semantic, type, include, other)
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from .validation_types import ValidationResult
from .error_analyzer import categorize_compilation_errors


def log_failed_test_case(result: ValidationResult, output_dir: Path) -> Path:
    """
    Generate a reproducible test failure report in markdown format.

    This function creates a markdown file documenting a failed validation test case
    with all information needed to reproduce and investigate the failure. The report
    includes commands, file paths, and categorized error summaries.

    Args:
        result: ValidationResult object representing the failed test
        output_dir: Directory to write the failure report markdown file

    Returns:
        Path to the generated markdown file

    Raises:
        OSError: If output directory cannot be created or file cannot be written

    Example:
        >>> from pathlib import Path
        >>> result = ValidationResult(
        ...     original_scr=Path("test.scr"),
        ...     decompiled_source=Path("test.c"),
        ...     verdict=ValidationVerdict.FAIL
        ... )
        >>> log_path = log_failed_test_case(result, Path(".planning/test_failures"))
        >>> print(log_path)
        .planning/test_failures/test_failure.md
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate test ID from original file name
    test_id = result.original_scr.stem

    # Create markdown file path
    output_file = output_dir / f"{test_id}_failure.md"

    # Generate timestamp
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # Build markdown content
    lines = []

    # Header
    lines.append(f"# Test Failure: {test_id}")
    lines.append("")
    lines.append(f"**Date:** {timestamp}")
    lines.append(f"**Verdict:** {result.verdict.value.upper()}")
    lines.append("")

    # Reproducible Steps
    lines.append("## Reproducible Steps")
    lines.append("")

    if result.compilation_result is None:
        # Decompilation failure
        lines.append("### Step 1: Decompile")
        lines.append("")
        lines.append("```bash")
        lines.append(f"python -m vcdecomp structure {result.original_scr} > {result.decompiled_source}")
        lines.append("```")
        lines.append("")
        lines.append("**Result:** Decompilation failed")
        lines.append("")
    else:
        # Decompilation succeeded, compilation may have failed
        lines.append("### Step 1: Decompile")
        lines.append("")
        lines.append("```bash")
        lines.append(f"python -m vcdecomp structure {result.original_scr} > {result.decompiled_source}")
        lines.append("```")
        lines.append("")
        lines.append("**Result:** Decompilation succeeded")
        lines.append("")

        lines.append("### Step 2: Compile")
        lines.append("")
        lines.append("```bash")
        output_scr = result.decompiled_source.with_suffix('.scr')
        output_h = result.decompiled_source.with_suffix('.h')
        lines.append(f"scmp.exe {result.decompiled_source} {output_scr} {output_h}")
        lines.append("```")
        lines.append("")

        if result.compilation_succeeded:
            lines.append("**Result:** Compilation succeeded (but bytecode differs)")
            lines.append("")
        else:
            lines.append("**Result:** Compilation failed")
            lines.append("")

    # Artifacts
    lines.append("## Artifacts")
    lines.append("")
    lines.append(f"- **Original .scr:** `{result.original_scr.absolute()}`")
    lines.append(f"- **Decompiled .c:** `{result.decompiled_source.absolute()}`")

    if result.compilation_result and result.compilation_result.output_file:
        lines.append(f"- **Recompiled .scr:** `{result.compilation_result.output_file.absolute()}`")

    if result.compilation_result and result.compilation_result.working_dir:
        lines.append(f"- **Working directory:** `{result.compilation_result.working_dir.absolute()}`")
        lines.append("  - Contains: `.err` error files, intermediate build artifacts")

    lines.append("")

    # Error Summary
    lines.append("## Error Summary")
    lines.append("")

    if result.compilation_result is None:
        lines.append("**Decompilation failure** - No compilation attempted")
        lines.append("")
    elif not result.compilation_result.errors:
        lines.append("**No compilation errors** - Bytecode comparison differences:")
        lines.append("")

        if result.categorized_differences:
            # Show bytecode difference summary
            lines.append(f"- Total differences: {len(result.categorized_differences)}")

            if result.difference_summary:
                lines.append(f"- Semantic: {result.difference_summary.semantic_count}")
                lines.append(f"- Cosmetic: {result.difference_summary.cosmetic_count}")
                lines.append(f"- Optimization: {result.difference_summary.optimization_count}")

            lines.append("")
    else:
        # Categorize and display compilation errors
        categorized = categorize_compilation_errors(result.compilation_result.errors)

        total_errors = len(result.compilation_result.errors)
        lines.append(f"**Total compilation errors:** {total_errors}")
        lines.append("")

        # Display each category with examples
        for error_type in ["syntax", "semantic", "type", "include", "other"]:
            errors = categorized.get(error_type, [])
            if not errors:
                continue

            count = len(errors)
            percentage = (count / total_errors * 100) if total_errors > 0 else 0

            lines.append(f"### {error_type.capitalize()} Errors ({count} - {percentage:.1f}%)")
            lines.append("")

            # Show first 5 examples
            for i, error in enumerate(errors[:5], 1):
                lines.append(f"{i}. {error.message}")

            if count > 5:
                lines.append(f"   ... and {count - 5} more")

            lines.append("")

    # Recommendations
    if result.recommendations:
        lines.append("## Recommendations")
        lines.append("")
        for i, rec in enumerate(result.recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")

    # Write to file
    output_file.write_text('\n'.join(lines), encoding='utf-8')

    return output_file
