"""
Comprehensive verification script for ReportGenerator (subtask-3-3).

Tests all acceptance criteria:
1. Generates text report with color coding
2. Generates HTML report with expandable sections
3. Generates JSON report for programmatic use
4. Groups differences by category and severity
5. Includes summary statistics
"""

from pathlib import Path
import json
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from vcdecomp.validation.report_generator import ReportGenerator, ANSIColors
from vcdecomp.validation.validation_types import ValidationResult, ValidationVerdict
from vcdecomp.validation.compilation_types import (
    CompilationResult, CompilationError, CompilationStage, ErrorSeverity
)
from vcdecomp.validation.bytecode_compare import (
    ComparisonResult, SectionComparison, Difference, DifferenceType, DifferenceSeverity
)
from vcdecomp.validation.difference_types import (
    DifferenceCategory, CategorizedDifference, DifferenceSummary
)
from datetime import datetime


def create_test_validation_result() -> ValidationResult:
    """Create a comprehensive test ValidationResult with various differences."""

    # Create compilation result
    compilation_result = CompilationResult(
        success=True,
        stage=CompilationStage.SCMP,
        output_file=Path("test_output.scr"),
        errors=[
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.WARNING,
                message="Unused variable 'x'",
                file=Path("test.c"),
                line=42,
                column=5
            )
        ],
        returncode=0
    )

    # Create comparison result with various differences
    differences = [
        # Semantic differences
        Difference(
            type=DifferenceType.HEADER,
            severity=DifferenceSeverity.CRITICAL,
            description="Entry point offset differs",
            location="header.enter_ip",
            original_value=0x1000,
            recompiled_value=0x1100,
            details={"category": "constant", "impact": "Different code execution start"}
        ),
        Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.MAJOR,
            description="Different opcode at instruction",
            location="code[42]",
            original_value="IADD",
            recompiled_value="IMUL",
            details={"category": "control_flow", "impact": "Different arithmetic operation"}
        ),
        Difference(
            type=DifferenceType.XFN,
            severity=DifferenceSeverity.CRITICAL,
            description="Missing external function",
            location="xfn[5]",
            original_value="SC_message",
            recompiled_value=None,
            details={"category": "constant", "impact": "Function call will fail"}
        ),

        # Cosmetic differences
        Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.MINOR,
            description="String reordered",
            location="data[0x200]",
            original_value="Hello World",
            recompiled_value="Hello World",
            details={"category": "reordering", "impact": "Same string at different offset"}
        ),
        Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.INFO,
            description="Alignment padding differs",
            location="data[0x400]",
            original_value="4 bytes",
            recompiled_value="8 bytes",
            details={"category": "alignment", "impact": "No functional impact"}
        ),

        # Optimization differences
        Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.MINOR,
            description="Equivalent instruction sequence",
            location="code[100]",
            original_value="INC",
            recompiled_value="ADD 1",
            details={"category": "optimization", "impact": "Semantically equivalent"}
        ),

        # Unknown category
        Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.MINOR,
            description="Unknown constant differs",
            location="data[0x600]",
            original_value=0x12345678,
            recompiled_value=0x87654321,
            details={}
        ),
    ]

    # Categorize differences
    categorized_differences = []
    for diff in differences:
        if "category" in diff.details:
            cat_name = diff.details["category"]
            if cat_name == "optimization":
                category = DifferenceCategory.OPTIMIZATION
                rationale = "Explicitly marked as optimization"
            elif cat_name in ("reordering", "alignment"):
                category = DifferenceCategory.COSMETIC
                rationale = f"Cosmetic difference: {cat_name}"
            elif cat_name in ("constant", "control_flow"):
                category = DifferenceCategory.SEMANTIC
                rationale = f"Affects program semantics: {cat_name}"
            else:
                category = DifferenceCategory.UNKNOWN
                rationale = "Cannot determine category"
        else:
            category = DifferenceCategory.UNKNOWN
            rationale = "No explicit category provided"

        categorized_differences.append(
            CategorizedDifference(
                difference=diff,
                category=category,
                rationale=rationale
            )
        )

    # Create difference summary
    difference_summary = DifferenceSummary.from_categorized_differences(categorized_differences)

    # Create comparison result (sections dict contains all differences)
    comparison_result = ComparisonResult(
        original_file=Path("original.scr"),
        recompiled_file=Path("recompiled.scr"),
        identical=False,
        sections={
            "header": SectionComparison(
                section_name="header",
                identical=False,
                differences=[diff for diff in differences if diff.type == DifferenceType.HEADER]
            ),
            "data": SectionComparison(
                section_name="data",
                identical=False,
                differences=[diff for diff in differences if diff.type == DifferenceType.DATA]
            ),
            "code": SectionComparison(
                section_name="code",
                identical=False,
                differences=[diff for diff in differences if diff.type == DifferenceType.CODE]
            ),
            "xfn": SectionComparison(
                section_name="xfn",
                identical=False,
                differences=[diff for diff in differences if diff.type == DifferenceType.XFN]
            ),
        }
    )

    # Create validation result
    validation_result = ValidationResult(
        original_scr=Path("original.scr"),
        decompiled_source=Path("decompiled.c"),
        compilation_result=compilation_result,
        comparison_result=comparison_result,
        categorized_differences=categorized_differences,
        difference_summary=difference_summary,
        verdict=ValidationVerdict.PARTIAL,
        error_message=None,
        recommendations=[
            "Review semantic differences - entry point and opcodes differ",
            "Missing external function 'SC_message' needs investigation",
            "Cosmetic differences can be ignored if functionality is correct",
        ],
        metadata={
            "timestamp": datetime.now().isoformat(),
            "decompiler_version": "1.0.0",
        }
    )

    return validation_result


def test_text_report_generation():
    """Test 1: Verify text report generation with color coding."""
    print("=" * 80)
    print("TEST 1: Text Report Generation with Color Coding")
    print("=" * 80)

    result = create_test_validation_result()
    generator = ReportGenerator(use_colors=True)

    # Generate text report
    text_report = generator.generate_text_report(result)

    # Verify report contains expected sections
    assert "VALIDATION REPORT" in text_report, "Missing report title"
    assert "VERDICT" in text_report, "Missing verdict section"
    assert "PARTIAL" in text_report, "Missing verdict value"
    assert "FILES" in text_report, "Missing files section"
    assert "COMPILATION" in text_report, "Missing compilation section"
    assert "BYTECODE COMPARISON" in text_report, "Missing comparison section"
    assert "DETAILED DIFFERENCES" in text_report, "Missing differences section"
    assert "RECOMMENDATIONS" in text_report, "Missing recommendations section"

    # Verify ANSI color codes are present
    assert ANSIColors.BOLD in text_report, "Missing ANSI bold codes"
    assert ANSIColors.RESET in text_report, "Missing ANSI reset codes"

    # Verify grouping by category
    assert "SEMANTIC DIFFERENCES" in text_report, "Missing semantic category"
    assert "COSMETIC DIFFERENCES" in text_report, "Missing cosmetic category"
    assert "OPTIMIZATION DIFFERENCES" in text_report, "Missing optimization category"

    # Verify summary statistics
    assert "By Category:" in text_report, "Missing category summary"
    assert "By Severity:" in text_report, "Missing severity summary"

    print("✓ Text report generated successfully")
    print(f"✓ Report length: {len(text_report)} characters")
    print("✓ Contains all required sections")
    print("✓ Contains ANSI color codes")
    print("✓ Groups differences by category and severity")
    print()

    # Test text report without colors
    generator_no_color = ReportGenerator(use_colors=False)
    text_report_no_color = generator_no_color.generate_text_report(result)

    assert ANSIColors.BOLD not in text_report_no_color, "Colors should be disabled"
    print("✓ Text report without colors works correctly")
    print()

    # Print sample of report
    print("Sample of text report (first 1000 chars):")
    print("-" * 80)
    print(text_report[:1000])
    print("-" * 80)
    print()


def test_html_report_generation():
    """Test 2: Verify HTML report generation with expandable sections."""
    print("=" * 80)
    print("TEST 2: HTML Report Generation with Expandable Sections")
    print("=" * 80)

    result = create_test_validation_result()
    generator = ReportGenerator()

    # Generate HTML report
    html_report = generator.generate_html_report(result)

    # Verify HTML structure
    assert "<!DOCTYPE html>" in html_report, "Missing DOCTYPE"
    assert "<html" in html_report, "Missing html tag"
    assert "<head>" in html_report, "Missing head section"
    assert "<body>" in html_report, "Missing body section"
    assert "</html>" in html_report, "Missing closing html tag"

    # Verify CSS styling
    assert "<style>" in html_report, "Missing CSS styles"
    assert ".container" in html_report, "Missing container class"
    assert ".verdict" in html_report, "Missing verdict class"
    assert ".difference" in html_report, "Missing difference class"

    # Verify JavaScript
    assert "<script>" in html_report, "Missing JavaScript"
    assert "DOMContentLoaded" in html_report, "Missing DOM ready handler"

    # Verify expandable sections (details/summary tags)
    assert "<details" in html_report, "Missing expandable sections"
    assert "<summary>" in html_report, "Missing summary tags"

    # Verify content sections
    assert "Validation Report" in html_report, "Missing report title"
    assert "Verdict" in html_report, "Missing verdict section"
    assert "Files" in html_report, "Missing files section"
    assert "Compilation" in html_report, "Missing compilation section"
    assert "Bytecode Comparison" in html_report, "Missing comparison section"
    assert "Detailed Differences" in html_report, "Missing differences section"
    assert "Recommendations" in html_report, "Missing recommendations section"

    # Verify category grouping
    assert "Semantic Differences" in html_report, "Missing semantic category"
    assert "Cosmetic Differences" in html_report, "Missing cosmetic category"
    assert "Optimization Differences" in html_report, "Missing optimization category"

    # Verify summary statistics (stat cards)
    assert "stat-card" in html_report, "Missing stat cards"

    # Verify color coding via CSS classes
    assert "verdict partial" in html_report or "verdict.partial" in html_report, "Missing verdict class"
    assert "semantic" in html_report.lower(), "Missing semantic styling"
    assert "cosmetic" in html_report.lower(), "Missing cosmetic styling"

    print("✓ HTML report generated successfully")
    print(f"✓ Report length: {len(html_report)} characters")
    print("✓ Contains valid HTML structure")
    print("✓ Contains CSS styles")
    print("✓ Contains JavaScript for interactivity")
    print("✓ Contains expandable sections (details/summary)")
    print("✓ Contains all required content sections")
    print("✓ Groups differences by category and severity")
    print()

    # Print sample of HTML
    print("Sample of HTML report (head section):")
    print("-" * 80)
    head_end = html_report.find("</head>")
    print(html_report[:head_end + 7][:500])
    print("...")
    print("-" * 80)
    print()


def test_json_report_generation():
    """Test 3: Verify JSON report generation for programmatic use."""
    print("=" * 80)
    print("TEST 3: JSON Report Generation for Programmatic Use")
    print("=" * 80)

    result = create_test_validation_result()
    generator = ReportGenerator()

    # Generate JSON report
    json_report = generator.generate_json_report(result)

    # Verify it's valid JSON
    try:
        data = json.loads(json_report)
        print("✓ Valid JSON structure")
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}")
        raise

    # Verify top-level structure
    assert "original_scr" in data, "Missing original_scr field"
    assert "decompiled_source" in data, "Missing decompiled_source field"
    assert "verdict" in data, "Missing verdict field"
    assert "success" in data, "Missing success field"
    assert "compilation" in data, "Missing compilation field"
    assert "comparison" in data, "Missing comparison field"
    assert "summary" in data, "Missing summary field"
    assert "recommendations" in data, "Missing recommendations field"
    assert "report_metadata" in data, "Missing report metadata"

    # Verify compilation section
    assert data["compilation"]["succeeded"] == True, "Compilation succeeded should be True"
    assert isinstance(data["compilation"]["errors"], list), "Errors should be a list"

    # Verify comparison section
    assert data["comparison"]["identical"] == False, "Identical should be False"
    assert "difference_count" in data["comparison"], "Missing difference_count"
    assert "semantic_differences" in data["comparison"], "Missing semantic_differences count"
    assert "cosmetic_differences" in data["comparison"], "Missing cosmetic_differences count"

    # Verify summary section
    assert "total_count" in data["summary"], "Missing total_count"
    assert "by_category" in data["summary"], "Missing by_category breakdown"
    assert "by_severity" in data["summary"], "Missing by_severity breakdown"

    assert data["summary"]["by_category"]["semantic"] > 0, "Should have semantic differences"
    assert data["summary"]["by_category"]["cosmetic"] > 0, "Should have cosmetic differences"
    assert data["summary"]["by_severity"]["critical"] > 0, "Should have critical differences"

    # Verify detailed differences
    assert "differences" in data, "Missing detailed differences"
    assert isinstance(data["differences"], list), "Differences should be a list"
    assert len(data["differences"]) > 0, "Should have differences"

    # Verify difference structure
    first_diff = data["differences"][0]
    assert "type" in first_diff, "Difference missing type"
    assert "severity" in first_diff, "Difference missing severity"
    assert "category" in first_diff, "Difference missing category"
    assert "location" in first_diff, "Difference missing location"
    assert "description" in first_diff, "Difference missing description"
    assert "rationale" in first_diff, "Difference missing rationale"

    # Verify report metadata
    assert "format_version" in data["report_metadata"], "Missing format version"
    assert "generated_at" in data["report_metadata"], "Missing generation timestamp"
    assert "generator" in data["report_metadata"], "Missing generator info"

    print("✓ JSON report generated successfully")
    print(f"✓ Report contains {len(data['differences'])} differences")
    print(f"✓ Total difference count: {data['summary']['total_count']}")
    print(f"✓ Semantic: {data['summary']['by_category']['semantic']}")
    print(f"✓ Cosmetic: {data['summary']['by_category']['cosmetic']}")
    print(f"✓ Optimization: {data['summary']['by_category']['optimization']}")
    print(f"✓ Critical: {data['summary']['by_severity']['critical']}")
    print(f"✓ Major: {data['summary']['by_severity']['major']}")
    print(f"✓ Minor: {data['summary']['by_severity']['minor']}")
    print()

    # Print sample of JSON
    print("Sample of JSON report (summary section):")
    print("-" * 80)
    print(json.dumps(data["summary"], indent=2))
    print("-" * 80)
    print()


def test_save_report():
    """Test 4: Verify report saving functionality with format auto-detection."""
    print("=" * 80)
    print("TEST 4: Report Saving with Format Auto-Detection")
    print("=" * 80)

    result = create_test_validation_result()
    generator = ReportGenerator()

    # Test saving text report
    text_path = Path("test_report.txt")
    generator.save_report(result, text_path, format="auto")
    assert text_path.exists(), "Text report file not created"
    text_content = text_path.read_text(encoding="utf-8")
    assert "VALIDATION REPORT" in text_content, "Text report missing content"
    text_path.unlink()  # Clean up
    print("✓ Text report saved successfully (.txt)")

    # Test saving HTML report
    html_path = Path("test_report.html")
    generator.save_report(result, html_path, format="auto")
    assert html_path.exists(), "HTML report file not created"
    html_content = html_path.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in html_content, "HTML report missing DOCTYPE"
    html_path.unlink()  # Clean up
    print("✓ HTML report saved successfully (.html)")

    # Test saving JSON report
    json_path = Path("test_report.json")
    generator.save_report(result, json_path, format="auto")
    assert json_path.exists(), "JSON report file not created"
    json_content = json_path.read_text(encoding="utf-8")
    json_data = json.loads(json_content)  # Verify valid JSON
    assert "verdict" in json_data, "JSON report missing content"
    json_path.unlink()  # Clean up
    print("✓ JSON report saved successfully (.json)")

    # Test explicit format override
    override_path = Path("test_report_override.custom")
    generator.save_report(result, override_path, format="html")
    assert override_path.exists(), "Override format file not created"
    override_content = override_path.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in override_content, "Override should generate HTML"
    override_path.unlink()  # Clean up
    print("✓ Explicit format override works correctly")

    print()


def test_grouping_and_statistics():
    """Test 5: Verify grouping by category/severity and summary statistics."""
    print("=" * 80)
    print("TEST 5: Grouping by Category/Severity and Summary Statistics")
    print("=" * 80)

    result = create_test_validation_result()
    generator = ReportGenerator()

    # Verify the result has proper grouping
    semantic_diffs = [d for d in result.categorized_differences if d.category == DifferenceCategory.SEMANTIC]
    cosmetic_diffs = [d for d in result.categorized_differences if d.category == DifferenceCategory.COSMETIC]
    optimization_diffs = [d for d in result.categorized_differences if d.category == DifferenceCategory.OPTIMIZATION]

    print(f"Total differences: {len(result.categorized_differences)}")
    print(f"Semantic: {len(semantic_diffs)}")
    print(f"Cosmetic: {len(cosmetic_diffs)}")
    print(f"Optimization: {len(optimization_diffs)}")
    print()

    # Verify summary statistics match
    assert result.difference_summary.total_count == len(result.categorized_differences)
    assert result.difference_summary.semantic_count == len(semantic_diffs)
    assert result.difference_summary.cosmetic_count == len(cosmetic_diffs)
    assert result.difference_summary.optimization_count == len(optimization_diffs)
    print("✓ Summary statistics are accurate")

    # Verify all formats include grouping
    text_report = generator.generate_text_report(result)
    html_report = generator.generate_html_report(result)
    json_report = generator.generate_json_report(result)
    json_data = json.loads(json_report)

    # Text report grouping
    assert "SEMANTIC DIFFERENCES" in text_report
    assert "COSMETIC DIFFERENCES" in text_report
    assert "OPTIMIZATION DIFFERENCES" in text_report
    print("✓ Text report groups differences by category")

    # HTML report grouping
    assert "Semantic Differences" in html_report
    assert "Cosmetic Differences" in html_report
    assert "Optimization Differences" in html_report
    print("✓ HTML report groups differences by category")

    # JSON report grouping
    assert json_data["summary"]["by_category"]["semantic"] == len(semantic_diffs)
    assert json_data["summary"]["by_category"]["cosmetic"] == len(cosmetic_diffs)
    assert json_data["summary"]["by_category"]["optimization"] == len(optimization_diffs)
    print("✓ JSON report includes category statistics")

    # Verify severity grouping in all formats
    critical_count = sum(1 for d in result.categorized_differences if d.difference.severity == DifferenceSeverity.CRITICAL)
    major_count = sum(1 for d in result.categorized_differences if d.difference.severity == DifferenceSeverity.MAJOR)

    assert "Critical" in text_report
    assert "Major" in text_report
    print("✓ Text report groups differences by severity")

    assert "Critical" in html_report or "critical" in html_report
    assert "Major" in html_report or "major" in html_report
    print("✓ HTML report groups differences by severity")

    assert json_data["summary"]["by_severity"]["critical"] == critical_count
    assert json_data["summary"]["by_severity"]["major"] == major_count
    print("✓ JSON report includes severity statistics")

    print()


def main():
    """Run all tests."""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "REPORT GENERATOR VERIFICATION TESTS" + " " * 23 + "║")
    print("║" + " " * 30 + "Subtask 3-3" + " " * 37 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    tests = [
        ("Text Report Generation", test_text_report_generation),
        ("HTML Report Generation", test_html_report_generation),
        ("JSON Report Generation", test_json_report_generation),
        ("Report Saving", test_save_report),
        ("Grouping and Statistics", test_grouping_and_statistics),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ TEST FAILED: {test_name}")
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
            print()

    # Summary
    print()
    print("=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()

    if failed == 0:
        print("✓ ALL ACCEPTANCE CRITERIA VERIFIED")
        print()
        print("Acceptance Criteria Status:")
        print("  ✓ Generates text report with color coding")
        print("  ✓ Generates HTML report with expandable sections")
        print("  ✓ Generates JSON report for programmatic use")
        print("  ✓ Groups differences by category and severity")
        print("  ✓ Includes summary statistics")
        print()
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
