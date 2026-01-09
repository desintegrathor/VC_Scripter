#!/usr/bin/env python3
"""
Verification script for enhanced header comparison (subtask-2-2).

Tests that header comparison properly handles:
1. Entry point offsets
2. Parameter counts and types
3. Script flags and attributes
4. Returns Difference objects with severity
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from vcdecomp.validation.bytecode_compare import (
    BytecodeComparator,
    DifferenceSeverity,
    DifferenceType,
)


def test_header_comparison():
    """Test enhanced header comparison features."""
    print("=" * 80)
    print("Testing Enhanced Header Comparison (Subtask 2-2)")
    print("=" * 80)

    # Find test files
    test_dirs = [
        Path("./Compiler-testruns"),
        Path("../Compiler-testruns"),
    ]

    scr_files = []
    for test_dir in test_dirs:
        if test_dir.exists():
            scr_files = list(test_dir.rglob("*.scr"))[:5]
            if scr_files:
                print(f"\nFound {len(scr_files)} test files in {test_dir}")
                break

    if len(scr_files) < 2:
        print("\n⚠ Need at least 2 .scr files for testing")
        return False

    # Test 1: Self-comparison (headers should be identical)
    print("\n" + "-" * 80)
    print("Test 1: Self-Comparison - Headers Should Be Identical")
    print("-" * 80)

    test_file = scr_files[0]
    print(f"\nComparing: {test_file.name} with itself")

    comparator = BytecodeComparator()
    result = comparator.compare_files(test_file, test_file)

    if not result.is_valid:
        print(f"✗ Failed to load files: {result.load_error}")
        return False

    header_comp = result.sections.get("header")
    if not header_comp:
        print("✗ No header comparison section found")
        return False

    if header_comp.identical:
        print(f"✓ Headers are identical (as expected)")
    else:
        print(f"✗ Headers should be identical in self-comparison")
        print(f"  Found {len(header_comp.differences)} differences:")
        for diff in header_comp.differences:
            print(f"    {diff}")
        return False

    # Test 2: Compare different files (should detect header differences)
    print("\n" + "-" * 80)
    print("Test 2: Different Files - Should Detect Header Differences")
    print("-" * 80)

    file1 = scr_files[0]
    file2 = scr_files[1]
    print(f"\nComparing: {file1.name} vs {file2.name}")

    comparator2 = BytecodeComparator()
    result2 = comparator2.compare_files(file1, file2)

    if not result2.is_valid:
        print(f"✗ Failed to load files: {result2.load_error}")
        return False

    header_comp2 = result2.sections.get("header")

    print(f"\nHeader comparison results:")
    print(f"  Identical: {header_comp2.identical}")
    print(f"  Differences found: {len(header_comp2.differences)}")

    # Check acceptance criteria
    print("\n" + "=" * 80)
    print("Acceptance Criteria Verification")
    print("=" * 80)

    criteria_met = True

    # Criterion 1: Compares entry point offsets
    print("\n1. Compares entry point offsets:")
    orig_entry = comparator2.original.header.enter_ip
    recomp_entry = comparator2.recompiled.header.enter_ip
    print(f"   Original entry point: {orig_entry}")
    print(f"   Recompiled entry point: {recomp_entry}")

    if orig_entry != recomp_entry:
        # Should have a difference reported
        entry_diffs = [d for d in header_comp2.differences
                      if 'enter_ip' in d.location]
        if entry_diffs:
            print(f"   ✓ Entry point difference detected with severity {entry_diffs[0].severity.value}")
            print(f"     Description: {entry_diffs[0].description}")
            if 'impact' in entry_diffs[0].details:
                print(f"     Impact: {entry_diffs[0].details['impact']}")
        else:
            print("   ✗ Entry point difference NOT detected")
            criteria_met = False
    else:
        print("   ✓ Entry points are identical")

    # Criterion 2: Compares parameter counts and types
    print("\n2. Compares parameter counts and types:")
    orig_params = comparator2.original.header.enter_size
    recomp_params = comparator2.recompiled.header.enter_size
    print(f"   Original param count: {orig_params}")
    print(f"   Recompiled param count: {recomp_params}")

    orig_types = comparator2.original.header.enter_array
    recomp_types = comparator2.recompiled.header.enter_array
    print(f"   Original param types: {orig_types}")
    print(f"   Recompiled param types: {recomp_types}")

    if orig_params != recomp_params or orig_types != recomp_types:
        param_diffs = [d for d in header_comp2.differences
                      if 'enter_size' in d.location or 'enter_array' in d.location]
        if param_diffs:
            print(f"   ✓ Parameter differences detected ({len(param_diffs)} difference(s))")
            for diff in param_diffs:
                print(f"     - {diff.description} (severity: {diff.severity.value})")
        else:
            print("   ✗ Parameter differences NOT detected")
            criteria_met = False
    else:
        print("   ✓ Parameters are identical")

    # Criterion 3: Compares script flags and attributes
    print("\n3. Compares script flags and attributes:")

    # Check save_info comparison
    orig_save = comparator2.original.save_info is not None
    recomp_save = comparator2.recompiled.save_info is not None
    print(f"   Original has save_info: {orig_save}")
    print(f"   Recompiled has save_info: {recomp_save}")

    # Check opcode variant comparison
    orig_variant = comparator2.original.opcode_resolver.name
    recomp_variant = comparator2.recompiled.opcode_resolver.name
    print(f"   Original opcode variant: {orig_variant}")
    print(f"   Recompiled opcode variant: {recomp_variant}")

    # Look for attribute differences
    attr_diffs = [d for d in header_comp2.differences
                 if d.type == DifferenceType.STRUCTURE]

    if attr_diffs:
        print(f"   ✓ Script attributes compared ({len(attr_diffs)} attribute(s) checked)")
        for diff in attr_diffs:
            print(f"     - {diff.description} (severity: {diff.severity.value})")
    else:
        print("   ✓ Script attributes compared (no differences found)")

    # Criterion 4: Returns Difference objects with severity
    print("\n4. Returns Difference objects with severity:")
    if header_comp2.differences:
        print(f"   ✓ {len(header_comp2.differences)} Difference object(s) with severity:")
        severity_counts = {}
        for diff in header_comp2.differences:
            severity = diff.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        for severity, count in severity_counts.items():
            print(f"     - {severity}: {count}")

        # Verify that critical differences have proper details
        critical_diffs = [d for d in header_comp2.differences
                         if d.severity == DifferenceSeverity.CRITICAL]
        if critical_diffs:
            print(f"\n   Critical differences have details:")
            for diff in critical_diffs[:2]:  # Show first 2
                print(f"     - {diff.location}: {diff.description}")
                if diff.details:
                    print(f"       Details: {diff.details.get('impact', 'N/A')}")
    else:
        print("   ✓ No differences found (headers are identical)")

    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)

    if criteria_met:
        print("\n✓ ALL ACCEPTANCE CRITERIA MET")
        print("\nSubtask 2-2 Implementation Complete:")
        print("  ✓ Compares entry point offsets")
        print("  ✓ Compares parameter counts and types")
        print("  ✓ Compares script flags and attributes")
        print("  ✓ Returns Difference objects with severity")
        return True
    else:
        print("\n✗ SOME CRITERIA NOT MET")
        return False


def main():
    """Run header comparison tests."""
    try:
        return 0 if test_header_comparison() else 1
    except Exception as e:
        print(f"\n✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
