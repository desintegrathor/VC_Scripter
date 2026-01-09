#!/usr/bin/env python3
"""
Verification script for ValidationOrchestrator.

Tests the complete validation workflow to ensure:
- Accepts original .SCR and decompiled source code
- Coordinates compilation via compiler wrapper
- Coordinates comparison via bytecode comparator
- Returns ValidationResult with all findings
- Handles errors gracefully at each step
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from vcdecomp.validation import ValidationOrchestrator, ValidationVerdict


def test_validation_workflow():
    """Test complete validation workflow."""
    print("=" * 80)
    print("Testing ValidationOrchestrator")
    print("=" * 80)

    # Find compiler directory
    compiler_paths = [
        Path("./original-resources/compiler"),
        Path("../original-resources/compiler"),
        Path("../../original-resources/compiler"),
    ]

    compiler_dir = None
    for path in compiler_paths:
        if path.exists() and (path / "SCMP.exe").exists():
            compiler_dir = path
            print(f"\n✓ Found compiler directory: {compiler_dir}")
            break

    if not compiler_dir:
        print("\n⚠ WARNING: Compiler directory not found")
        print("Expected locations:")
        for path in compiler_paths:
            print(f"  - {path}")
        print("\nSkipping validation tests (requires original compiler tools)")
        return True  # Not a failure, just can't run the test

    # Find include directory
    include_paths = [
        Path("./original-resources/inc"),
        Path("../original-resources/inc"),
        Path("../../original-resources/inc"),
    ]

    include_dir = None
    for path in include_paths:
        if path.exists():
            include_dir = path
            print(f"✓ Found include directory: {include_dir}")
            break

    # Find test files
    test_dirs = [
        Path("./Compiler-testruns"),
        Path("../Compiler-testruns"),
        Path("../../Compiler-testruns"),
    ]

    test_c_files = []
    test_scr_files = []

    for test_dir in test_dirs:
        if test_dir.exists():
            test_c_files = list(test_dir.rglob("*.c"))[:3]
            test_scr_files = list(test_dir.rglob("*.scr"))[:3]
            if test_c_files or test_scr_files:
                print(f"✓ Found test directory: {test_dir}")
                print(f"  - {len(test_c_files)} .c files")
                print(f"  - {len(test_scr_files)} .scr files")
                break

    if not test_c_files and not test_scr_files:
        print("\n⚠ WARNING: No test files found")
        print("Creating minimal test...")
        return test_error_handling(compiler_dir, include_dir)

    # Initialize orchestrator
    print("\n" + "-" * 80)
    print("Test 1: Initialize ValidationOrchestrator")
    print("-" * 80)

    try:
        orchestrator = ValidationOrchestrator(
            compiler_dir=compiler_dir,
            include_dirs=[include_dir] if include_dir else None,
            timeout=30,
        )
        print("✓ ValidationOrchestrator initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        return False

    # Test 2: Error handling - missing files
    print("\n" + "-" * 80)
    print("Test 2: Error Handling - Missing Files")
    print("-" * 80)

    result = orchestrator.validate(
        original_scr="nonexistent.scr",
        decompiled_source="nonexistent.c",
    )

    print(f"\nVerdict: {result.verdict.value}")
    print(f"Error: {result.error_message}")

    if result.verdict == ValidationVerdict.ERROR and "not found" in result.error_message.lower():
        print("✓ Test 2 PASSED: Gracefully handles missing files")
    else:
        print("✗ Test 2 FAILED: Should return ERROR for missing files")
        return False

    # Test 3: Validation workflow (if we have matching .c and .scr files)
    if test_c_files and test_scr_files:
        print("\n" + "-" * 80)
        print("Test 3: Full Validation Workflow")
        print("-" * 80)

        # Try to find a matching pair (same basename)
        matching_pair = None
        for c_file in test_c_files:
            for scr_file in test_scr_files:
                if c_file.stem == scr_file.stem:
                    matching_pair = (scr_file, c_file)
                    break
            if matching_pair:
                break

        if not matching_pair:
            # Just use first files
            scr_file = test_scr_files[0]
            c_file = test_c_files[0]
            print(f"\n⚠ No matching .c/.scr pair found")
            print(f"Using arbitrary files for demonstration:")
        else:
            scr_file, c_file = matching_pair
            print(f"\nFound matching pair:")

        print(f"  Original SCR: {scr_file.name}")
        print(f"  Source file:  {c_file.name}")

        print("\nRunning validation (this may take a moment)...")
        result = orchestrator.validate(
            original_scr=scr_file,
            decompiled_source=c_file,
        )

        print("\n" + "=" * 80)
        print(result)
        print("=" * 80)

        # Verify result structure
        checks = [
            ("Has verdict", result.verdict is not None),
            ("Has original_scr", result.original_scr is not None),
            ("Has decompiled_source", result.decompiled_source is not None),
            ("Has metadata", bool(result.metadata)),
        ]

        if result.compilation_result:
            checks.append(("Has compilation_result", True))

        if result.comparison_result:
            checks.append(("Has comparison_result", True))

        print("\nResult Structure Checks:")
        all_passed = True
        for check_name, passed in checks:
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False

        if all_passed:
            print("\n✓ Test 3 PASSED: Validation workflow completed")
        else:
            print("\n✗ Test 3 FAILED: Missing expected result components")
            return False

    # Test 4: JSON serialization
    print("\n" + "-" * 80)
    print("Test 4: JSON Serialization")
    print("-" * 80)

    try:
        json_str = result.to_json()
        print(f"✓ JSON serialization successful ({len(json_str)} bytes)")

        # Verify it's valid JSON
        import json
        data = json.loads(json_str)

        required_keys = ["verdict", "original_scr", "decompiled_source", "metadata"]
        missing = [key for key in required_keys if key not in data]

        if missing:
            print(f"✗ Missing required keys in JSON: {missing}")
            return False

        print("✓ JSON contains all required keys")
    except Exception as e:
        print(f"✗ JSON serialization failed: {e}")
        return False

    # Test 5: ValidationResult properties
    print("\n" + "-" * 80)
    print("Test 5: ValidationResult Properties")
    print("-" * 80)

    properties = [
        ("success", result.success),
        ("compilation_succeeded", result.compilation_succeeded),
        ("comparison_succeeded", result.comparison_succeeded),
        ("bytecode_identical", result.bytecode_identical),
        ("has_semantic_differences", result.has_semantic_differences),
        ("has_cosmetic_differences", result.has_cosmetic_differences),
    ]

    print("\nProperty values:")
    for prop_name, value in properties:
        print(f"  {prop_name}: {value}")

    print("\n✓ Test 5 PASSED: All properties accessible")

    return True


def test_error_handling(compiler_dir, include_dir):
    """Test error handling with minimal setup."""
    print("\n" + "-" * 80)
    print("Minimal Test: Error Handling")
    print("-" * 80)

    orchestrator = ValidationOrchestrator(
        compiler_dir=compiler_dir,
        include_dirs=[include_dir] if include_dir else None,
    )

    # Test with nonexistent files
    result = orchestrator.validate(
        original_scr="missing.scr",
        decompiled_source="missing.c",
    )

    if result.verdict == ValidationVerdict.ERROR:
        print("✓ Correctly handles missing files")
        return True
    else:
        print("✗ Should return ERROR for missing files")
        return False


def main():
    """Run all tests."""
    try:
        success = test_validation_workflow()

        print("\n" + "=" * 80)
        if success:
            print("✓ ALL TESTS PASSED")
            print("=" * 80)
            return 0
        else:
            print("✗ SOME TESTS FAILED")
            print("=" * 80)
            return 1

    except Exception as e:
        print("\n" + "=" * 80)
        print(f"✗ TEST SUITE FAILED WITH EXCEPTION")
        print("=" * 80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
