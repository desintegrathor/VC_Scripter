#!/usr/bin/env python3
"""
Example: Basic Single File Validation

This example demonstrates how to validate a single decompiled VC script
against its original bytecode.

Usage:
    python validate_single.py <original.scr> <decompiled.c>

Example:
    python validate_single.py mission_01.scr mission_01_decompiled.c
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from vcdecomp.validation import (
    ValidationOrchestrator,
    ValidationVerdict,
    ReportGenerator,
)


def main():
    """Run single file validation with basic reporting."""

    # Parse command line arguments
    if len(sys.argv) != 3:
        print("Usage: python validate_single.py <original.scr> <decompiled.c>")
        print("\nExample:")
        print("  python validate_single.py ../Compiler-testruns/Testrun1/tdm.scr decompiled/tdm.c")
        sys.exit(1)

    original_scr = sys.argv[1]
    decompiled_source = sys.argv[2]

    # Validate file existence
    if not os.path.exists(original_scr):
        print(f"Error: Original SCR file not found: {original_scr}")
        sys.exit(1)

    if not os.path.exists(decompiled_source):
        print(f"Error: Decompiled source file not found: {decompiled_source}")
        sys.exit(1)

    print("=" * 70)
    print("VC Script Validation - Single File")
    print("=" * 70)
    print(f"Original:   {original_scr}")
    print(f"Decompiled: {decompiled_source}")
    print()

    # Configure compiler path (adjust to your setup)
    compiler_dir = "original-resources/compiler"
    if not os.path.exists(compiler_dir):
        print(f"Warning: Compiler directory not found at {compiler_dir}")
        print("Attempting to use ../original-resources/compiler instead...")
        compiler_dir = "../original-resources/compiler"
        if not os.path.exists(compiler_dir):
            print("Error: Cannot find compiler directory!")
            print("Please specify the correct path to SCMP.exe, SPP.exe, etc.")
            sys.exit(1)

    # Create validation orchestrator
    print("Initializing validation orchestrator...")
    validator = ValidationOrchestrator(
        compiler_dir=compiler_dir,
        timeout=30,  # 30 second compilation timeout
        cache_enabled=True  # Enable caching for faster re-runs
    )

    # Run validation
    print("Running validation (this may take a moment)...")
    print()

    try:
        result = validator.validate(
            original_scr_path=original_scr,
            source_path=decompiled_source
        )

        # Print summary
        print("=" * 70)
        print("VALIDATION RESULT")
        print("=" * 70)
        print(f"Verdict: {result.verdict.name}")
        print()

        # Compilation status
        if result.compilation_succeeded:
            print("✓ Compilation: SUCCESS")
        else:
            print("✗ Compilation: FAILED")
            if result.compilation_result:
                print(f"  Errors: {result.compilation_result.error_count}")
                print(f"  Warnings: {result.compilation_result.warning_count}")
        print()

        # Difference summary
        if result.difference_summary:
            summary = result.difference_summary
            print(f"Total Differences: {summary.total_count}")
            print(f"  Semantic:     {summary.semantic_count} (affects behavior)")
            print(f"  Cosmetic:     {summary.cosmetic_count} (formatting only)")
            print(f"  Optimization: {summary.optimization_count} (equivalent code)")
            print(f"  Unknown:      {summary.unknown_count}")
            print()

            # Severity breakdown
            print("Severity Breakdown:")
            print(f"  Critical: {summary.critical_count}")
            print(f"  Major:    {summary.major_count}")
            print(f"  Minor:    {summary.minor_count}")
            print(f"  Info:     {summary.info_count}")
            print()

        # Recommendations
        if result.recommendations:
            print("Recommendations:")
            for i, rec in enumerate(result.recommendations, 1):
                print(f"  {i}. {rec}")
            print()

        # Generate and display detailed report
        print("=" * 70)
        print("DETAILED REPORT")
        print("=" * 70)
        print()

        generator = ReportGenerator()
        text_report = generator.generate_text_report(result, use_color=True)
        print(text_report)

        # Optionally save HTML report
        save_html = input("\nSave HTML report? (y/n): ").strip().lower()
        if save_html == 'y':
            report_filename = f"{Path(decompiled_source).stem}_validation.html"
            generator.save_report(result, report_filename, format="html")
            print(f"HTML report saved to: {report_filename}")

        # Return exit code based on verdict
        if result.verdict == ValidationVerdict.PASS:
            print("\n✓ VALIDATION PASSED")
            return 0
        elif result.verdict == ValidationVerdict.PARTIAL:
            print("\n⚠ PARTIAL VALIDATION (cosmetic differences only)")
            return 0
        else:
            print("\n✗ VALIDATION FAILED")
            return 1

    except Exception as e:
        print(f"Error during validation: {e}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
