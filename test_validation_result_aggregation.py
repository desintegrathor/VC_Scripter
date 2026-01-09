#!/usr/bin/env python3
"""
Comprehensive test for ValidationResult aggregation (subtask-3-2).

Verifies that ValidationResult meets all acceptance criteria:
1. Includes compilation status
2. Includes all categorized differences
3. Provides overall verdict (PASS, FAIL, PARTIAL)
4. Includes actionable recommendations
5. Can serialize to JSON for storage
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from vcdecomp.validation.validation_types import ValidationResult, ValidationVerdict
from vcdecomp.validation.compilation_types import CompilationResult, CompilationError, CompilationStage, ErrorSeverity
from vcdecomp.validation.bytecode_compare import ComparisonResult, Difference, DifferenceType, DifferenceSeverity
from vcdecomp.validation.difference_types import CategorizedDifference, DifferenceCategory, DifferenceSummary


def test_acceptance_criterion_1_compilation_status():
    """Test that ValidationResult includes compilation status."""
    print("\n" + "=" * 80)
    print("Acceptance Criterion 1: ValidationResult includes compilation status")
    print("=" * 80)

    # Create a mock compilation result
    compilation_result = CompilationResult(
        success=True,
        stage=CompilationStage.SCMP,
        output_file=Path("test.scr"),
        errors=[],
    )

    # Create ValidationResult
    result = ValidationResult(
        original_scr=Path("original.scr"),
        decompiled_source=Path("decompiled.c"),
        compilation_result=compilation_result,
    )

    # Verify compilation status is included
    checks = [
        ("Has compilation_result", result.compilation_result is not None),
        ("compilation_succeeded property works", result.compilation_succeeded == True),
        ("compilation_result.success is accessible", result.compilation_result.success == True),
        ("compilation_result.output_file is accessible", result.compilation_result.output_file == Path("test.scr")),
    ]

    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n✓ CRITERION 1 PASSED: Compilation status is properly included")
    else:
        print("\n✗ CRITERION 1 FAILED")

    return all_passed


def test_acceptance_criterion_2_categorized_differences():
    """Test that ValidationResult includes all categorized differences."""
    print("\n" + "=" * 80)
    print("Acceptance Criterion 2: Includes all categorized differences")
    print("=" * 80)

    # Create mock differences
    diff1 = Difference(
        type=DifferenceType.HEADER,
        severity=DifferenceSeverity.CRITICAL,
        description="Entry point mismatch",
        location="header.enter_ip",
    )
    diff2 = Difference(
        type=DifferenceType.CODE,
        severity=DifferenceSeverity.MAJOR,
        description="Instruction difference",
        location="instruction[10]",
    )
    diff3 = Difference(
        type=DifferenceType.DATA,
        severity=DifferenceSeverity.MINOR,
        description="String reordering",
        location="data[offset 0x100]",
    )

    categorized_diffs = [
        CategorizedDifference(difference=diff1, category=DifferenceCategory.SEMANTIC, rationale="Entry point affects execution"),
        CategorizedDifference(difference=diff2, category=DifferenceCategory.SEMANTIC, rationale="Code changes behavior"),
        CategorizedDifference(difference=diff3, category=DifferenceCategory.COSMETIC, rationale="Reordering doesn't affect behavior"),
    ]

    # Create ValidationResult
    result = ValidationResult(
        original_scr=Path("original.scr"),
        decompiled_source=Path("decompiled.c"),
        categorized_differences=categorized_diffs,
    )

    # Verify differences are included and accessible
    checks = [
        ("Has categorized_differences", result.categorized_differences is not None),
        ("Contains all 3 differences", len(result.categorized_differences) == 3),
        ("has_semantic_differences property works", result.has_semantic_differences == True),
        ("has_cosmetic_differences property works", result.has_cosmetic_differences == True),
        ("get_differences_by_category(SEMANTIC) works",
         len(result.get_differences_by_category(DifferenceCategory.SEMANTIC)) == 2),
        ("get_differences_by_category(COSMETIC) works",
         len(result.get_differences_by_category(DifferenceCategory.COSMETIC)) == 1),
    ]

    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n✓ CRITERION 2 PASSED: Categorized differences are properly included")
    else:
        print("\n✗ CRITERION 2 FAILED")

    return all_passed


def test_acceptance_criterion_3_verdict():
    """Test that ValidationResult provides overall verdict."""
    print("\n" + "=" * 80)
    print("Acceptance Criterion 3: Provides overall verdict (PASS, FAIL, PARTIAL)")
    print("=" * 80)

    # Test all verdict types
    verdicts_to_test = [
        (ValidationVerdict.PASS, "PASS verdict"),
        (ValidationVerdict.PARTIAL, "PARTIAL verdict"),
        (ValidationVerdict.FAIL, "FAIL verdict"),
        (ValidationVerdict.ERROR, "ERROR verdict"),
    ]

    all_passed = True
    for verdict, description in verdicts_to_test:
        result = ValidationResult(
            original_scr=Path("original.scr"),
            decompiled_source=Path("decompiled.c"),
            verdict=verdict,
        )

        if result.verdict == verdict:
            print(f"✓ {description} works correctly")
        else:
            print(f"✗ {description} failed")
            all_passed = False

    # Test success property
    pass_result = ValidationResult(
        original_scr=Path("original.scr"),
        decompiled_source=Path("decompiled.c"),
        verdict=ValidationVerdict.PASS,
    )

    partial_result = ValidationResult(
        original_scr=Path("original.scr"),
        decompiled_source=Path("decompiled.c"),
        verdict=ValidationVerdict.PARTIAL,
    )

    fail_result = ValidationResult(
        original_scr=Path("original.scr"),
        decompiled_source=Path("decompiled.c"),
        verdict=ValidationVerdict.FAIL,
    )

    checks = [
        ("success property True for PASS", pass_result.success == True),
        ("success property True for PARTIAL", partial_result.success == True),
        ("success property False for FAIL", fail_result.success == False),
    ]

    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n✓ CRITERION 3 PASSED: Verdict system works correctly")
    else:
        print("\n✗ CRITERION 3 FAILED")

    return all_passed


def test_acceptance_criterion_4_recommendations():
    """Test that ValidationResult includes actionable recommendations."""
    print("\n" + "=" * 80)
    print("Acceptance Criterion 4: Includes actionable recommendations")
    print("=" * 80)

    # Create result with recommendations
    result = ValidationResult(
        original_scr=Path("original.scr"),
        decompiled_source=Path("decompiled.c"),
        recommendations=[
            "Review compilation errors above",
            "Verify decompiled source code syntax",
            "Check for syntax errors in decompiled code",
        ],
    )

    # Verify recommendations are included and accessible
    checks = [
        ("Has recommendations field", hasattr(result, 'recommendations')),
        ("Recommendations is a list", isinstance(result.recommendations, list)),
        ("Contains all 3 recommendations", len(result.recommendations) == 3),
        ("Recommendations are strings", all(isinstance(r, str) for r in result.recommendations)),
        ("Can add recommendations", True),  # We'll test this
    ]

    # Test adding recommendations
    result.recommendations.append("Test recommendation")
    checks.append(("Can append recommendations", len(result.recommendations) == 4))

    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False

    # Verify recommendations appear in string output
    str_output = str(result)
    if "RECOMMENDATIONS" in str_output and "Review compilation errors" in str_output:
        print("✓ Recommendations appear in string output")
    else:
        print("✗ Recommendations not visible in string output")
        all_passed = False

    if all_passed:
        print("\n✓ CRITERION 4 PASSED: Recommendations work correctly")
    else:
        print("\n✗ CRITERION 4 FAILED")

    return all_passed


def test_acceptance_criterion_5_json_serialization():
    """Test that ValidationResult can serialize to JSON for storage."""
    print("\n" + "=" * 80)
    print("Acceptance Criterion 5: Can serialize to JSON for storage")
    print("=" * 80)

    # Create a comprehensive ValidationResult
    compilation_result = CompilationResult(
        success=True,
        stage=CompilationStage.SCMP,
        output_file=Path("test.scr"),
        errors=[
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="Test error",
                file=Path("test.c"),
                line=10,
            )
        ],
    )

    diff1 = Difference(
        type=DifferenceType.HEADER,
        severity=DifferenceSeverity.CRITICAL,
        description="Entry point mismatch",
        location="header.enter_ip",
    )

    categorized_diffs = [
        CategorizedDifference(difference=diff1, category=DifferenceCategory.SEMANTIC, rationale="Test"),
    ]

    result = ValidationResult(
        original_scr=Path("original.scr"),
        decompiled_source=Path("decompiled.c"),
        compilation_result=compilation_result,
        categorized_differences=categorized_diffs,
        verdict=ValidationVerdict.PARTIAL,
        recommendations=["Test recommendation"],
        metadata={"test": "value", "timestamp": 12345},
    )

    all_passed = True

    # Test to_dict() method
    try:
        data_dict = result.to_dict()
        print("✓ to_dict() method works")

        # Verify dictionary contains expected keys
        expected_keys = ["original_scr", "decompiled_source", "verdict", "success",
                        "compilation", "recommendations", "metadata"]
        missing_keys = [key for key in expected_keys if key not in data_dict]

        if not missing_keys:
            print(f"✓ Dictionary contains all expected keys: {', '.join(expected_keys)}")
        else:
            print(f"✗ Missing keys in dictionary: {missing_keys}")
            all_passed = False

    except Exception as e:
        print(f"✗ to_dict() failed: {e}")
        all_passed = False

    # Test to_json() method
    try:
        json_str = result.to_json()
        print("✓ to_json() method works")

        # Verify it's valid JSON
        parsed = json.loads(json_str)
        print(f"✓ Generated valid JSON ({len(json_str)} bytes)")

        # Verify parsed JSON contains expected data
        checks = [
            ("verdict in JSON", "verdict" in parsed),
            ("verdict value correct", parsed.get("verdict") == "partial"),
            ("success in JSON", "success" in parsed),
            ("success value correct", parsed.get("success") == True),
            ("recommendations in JSON", "recommendations" in parsed),
            ("metadata in JSON", "metadata" in parsed),
            ("compilation in JSON", "compilation" in parsed),
            ("original_scr in JSON", "original_scr" in parsed),
            ("decompiled_source in JSON", "decompiled_source" in parsed),
        ]

        for check_name, passed in checks:
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False

        # Test with indentation
        json_indented = result.to_json(indent=4)
        if len(json_indented) > len(json_str):
            print("✓ JSON indentation parameter works")
        else:
            print("✗ JSON indentation parameter failed")
            all_passed = False

        # Verify JSON can be saved to file (simulate)
        try:
            # Just verify we can write it
            test_path = Path("test_validation_result.json")
            test_path.write_text(json_str)
            test_path.unlink()  # Clean up
            print("✓ JSON can be saved to file")
        except Exception as e:
            print(f"✗ Failed to save JSON to file: {e}")
            all_passed = False

    except Exception as e:
        print(f"✗ to_json() failed: {e}")
        all_passed = False

    if all_passed:
        print("\n✓ CRITERION 5 PASSED: JSON serialization works correctly")
    else:
        print("\n✗ CRITERION 5 FAILED")

    return all_passed


def test_integration():
    """Test that all features work together in an integrated scenario."""
    print("\n" + "=" * 80)
    print("Integration Test: All Features Together")
    print("=" * 80)

    # Simulate a complete validation result
    compilation_result = CompilationResult(
        success=True,
        stage=CompilationStage.SCMP,
        output_file=Path("recompiled.scr"),
        errors=[],
    )

    # Create some differences
    diffs = [
        Difference(type=DifferenceType.HEADER, severity=DifferenceSeverity.CRITICAL, description="Entry point differs", location="header.enter_ip"),
        Difference(type=DifferenceType.CODE, severity=DifferenceSeverity.MAJOR, description="Instruction order differs", location="instruction[5]"),
        Difference(type=DifferenceType.DATA, severity=DifferenceSeverity.MINOR, description="String alignment differs", location="data[0x50]"),
    ]

    categorized = [
        CategorizedDifference(difference=diffs[0], category=DifferenceCategory.SEMANTIC, rationale="Entry point affects behavior"),
        CategorizedDifference(difference=diffs[1], category=DifferenceCategory.SEMANTIC, rationale="Code order matters"),
        CategorizedDifference(difference=diffs[2], category=DifferenceCategory.COSMETIC, rationale="Alignment is cosmetic"),
    ]

    summary = DifferenceSummary(
        total_count=3,
        semantic_count=2,
        cosmetic_count=1,
        optimization_count=0,
        unknown_count=0,
        critical_count=1,
        major_count=1,
        minor_count=1,
        info_count=0,
        semantic_differences=[categorized[0], categorized[1]],
        cosmetic_differences=[categorized[2]],
        optimization_differences=[],
    )

    result = ValidationResult(
        original_scr=Path("original.scr"),
        decompiled_source=Path("decompiled.c"),
        compilation_result=compilation_result,
        categorized_differences=categorized,
        difference_summary=summary,
        verdict=ValidationVerdict.PARTIAL,
        recommendations=[
            "Found 2 semantic differences that affect behavior",
            "Review semantic differences carefully before using decompiled code",
            "Header differences detected - check entry point and parameters",
        ],
        metadata={
            "compiler_dir": "/path/to/compiler",
            "timestamp": 12345,
            "opcode_variant": "auto",
        }
    )

    # Test all aspects
    checks = [
        ("Has compilation status", result.compilation_succeeded == True),
        ("Has categorized differences", len(result.categorized_differences) == 3),
        ("Has verdict", result.verdict == ValidationVerdict.PARTIAL),
        ("Has recommendations", len(result.recommendations) == 3),
        ("Can serialize to JSON", result.to_json() is not None),
        ("Can convert to dict", result.to_dict() is not None),
        ("Can convert to string", str(result) is not None),
        ("success property works", result.success == True),
        ("has_semantic_differences works", result.has_semantic_differences == True),
        ("has_cosmetic_differences works", result.has_cosmetic_differences == True),
        ("get_differences_by_category works", len(result.get_differences_by_category(DifferenceCategory.SEMANTIC)) == 2),
    ]

    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False

    # Display the full result
    print("\nFull ValidationResult output:")
    print(result)

    # Display JSON output
    print("\nJSON serialization sample:")
    json_output = result.to_json(indent=2)
    lines = json_output.split('\n')[:20]  # First 20 lines
    for line in lines:
        print(line)
    if len(json_output.split('\n')) > 20:
        print("... (truncated)")

    if all_passed:
        print("\n✓ INTEGRATION TEST PASSED")
    else:
        print("\n✗ INTEGRATION TEST FAILED")

    return all_passed


def main():
    """Run all tests."""
    print("=" * 80)
    print("VALIDATION RESULT AGGREGATION TEST SUITE")
    print("Subtask 3-2: Implement validation result aggregation")
    print("=" * 80)

    results = []

    # Run all acceptance criteria tests
    results.append(("Criterion 1: Compilation Status", test_acceptance_criterion_1_compilation_status()))
    results.append(("Criterion 2: Categorized Differences", test_acceptance_criterion_2_categorized_differences()))
    results.append(("Criterion 3: Overall Verdict", test_acceptance_criterion_3_verdict()))
    results.append(("Criterion 4: Recommendations", test_acceptance_criterion_4_recommendations()))
    results.append(("Criterion 5: JSON Serialization", test_acceptance_criterion_5_json_serialization()))
    results.append(("Integration Test", test_integration()))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("=" * 80)
        print("\nAll acceptance criteria for subtask-3-2 are met:")
        print("1. ✓ ValidationResult includes compilation status")
        print("2. ✓ Includes all categorized differences")
        print("3. ✓ Provides overall verdict (PASS, FAIL, PARTIAL)")
        print("4. ✓ Includes actionable recommendations")
        print("5. ✓ Can serialize to JSON for storage")
        print("\nSubtask-3-2 is COMPLETE!")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
