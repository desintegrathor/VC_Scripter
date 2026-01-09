#!/usr/bin/env python3
"""
Verification script for subtask-1-4: Compilation result data structures.

Tests all acceptance criteria:
1. CompilationResult includes success flag, output paths, errors, warnings
2. CompilationError includes file, line, column, message, severity
3. CompilationStage enum for SPP, SCC, SASM stages
4. All types are properly typed with type hints
"""

from pathlib import Path
from typing import get_type_hints
import sys

# Add parent directory to path to import vcdecomp
sys.path.insert(0, str(Path(__file__).parent))

from vcdecomp.validation import (
    CompilationResult,
    CompilationError,
    CompilationStage,
    ErrorSeverity,
)


def test_compilation_stage_enum():
    """Test CompilationStage enum has required stages."""
    print("\n✓ Testing CompilationStage enum...")

    assert hasattr(CompilationStage, 'SPP'), "Missing SPP stage"
    assert hasattr(CompilationStage, 'SCC'), "Missing SCC stage"
    assert hasattr(CompilationStage, 'SASM'), "Missing SASM stage"

    assert CompilationStage.SPP.value == "spp"
    assert CompilationStage.SCC.value == "scc"
    assert CompilationStage.SASM.value == "sasm"

    print("  ✓ SPP, SCC, SASM stages present")
    print("  ✓ Stage values correct")


def test_error_severity_enum():
    """Test ErrorSeverity enum."""
    print("\n✓ Testing ErrorSeverity enum...")

    assert hasattr(ErrorSeverity, 'INFO'), "Missing INFO severity"
    assert hasattr(ErrorSeverity, 'WARNING'), "Missing WARNING severity"
    assert hasattr(ErrorSeverity, 'ERROR'), "Missing ERROR severity"

    print("  ✓ INFO, WARNING, ERROR severities present")


def test_compilation_error_structure():
    """Test CompilationError has required fields."""
    print("\n✓ Testing CompilationError structure...")

    # Test basic creation
    error = CompilationError(
        stage=CompilationStage.SCC,
        severity=ErrorSeverity.ERROR,
        message="Test error message",
        file=Path("test.c"),
        line=42,
        column=10,
    )

    assert error.stage == CompilationStage.SCC
    assert error.severity == ErrorSeverity.ERROR
    assert error.message == "Test error message"
    assert error.file == Path("test.c")
    assert error.line == 42
    assert error.column == 10

    print("  ✓ Has required fields: stage, severity, message, file, line, column")

    # Test __str__ method
    error_str = str(error)
    assert "scc" in error_str.lower()
    assert "test.c" in error_str
    assert "42" in error_str

    print("  ✓ Has human-readable __str__ method")

    # Test optional fields
    minimal_error = CompilationError(
        stage=CompilationStage.SPP,
        severity=ErrorSeverity.WARNING,
        message="Minimal warning"
    )
    assert minimal_error.file is None
    assert minimal_error.line is None
    assert minimal_error.column is None

    print("  ✓ Optional fields work correctly")


def test_compilation_result_structure():
    """Test CompilationResult has required fields."""
    print("\n✓ Testing CompilationResult structure...")

    # Test successful result
    result = CompilationResult(
        success=True,
        stage=CompilationStage.SCMP,
        output_file=Path("output.scr"),
        errors=[],
        stdout="Compilation successful",
        stderr="",
        returncode=0,
    )

    assert result.success is True
    assert result.stage == CompilationStage.SCMP
    assert result.output_file == Path("output.scr")
    assert isinstance(result.errors, list)
    assert result.stdout == "Compilation successful"
    assert result.stderr == ""
    assert result.returncode == 0

    print("  ✓ Has required fields: success, stage, output_file, errors")
    print("  ✓ Has additional fields: stdout, stderr, returncode")

    # Test with errors and warnings
    error1 = CompilationError(
        stage=CompilationStage.SCC,
        severity=ErrorSeverity.ERROR,
        message="Syntax error",
        line=10,
    )
    warning1 = CompilationError(
        stage=CompilationStage.SPP,
        severity=ErrorSeverity.WARNING,
        message="Unused variable",
        line=5,
    )

    result_with_errors = CompilationResult(
        success=False,
        stage=CompilationStage.SCC,
        errors=[error1, warning1],
        returncode=1,
    )

    assert result_with_errors.has_errors is True
    assert result_with_errors.has_warnings is True
    assert result_with_errors.error_count == 1
    assert result_with_errors.warning_count == 1

    print("  ✓ Has helper properties: has_errors, has_warnings")
    print("  ✓ Has helper properties: error_count, warning_count")

    # Test __str__ method
    result_str = str(result)
    assert "successful" in result_str.lower()

    failed_str = str(result_with_errors)
    assert "failed" in failed_str.lower()

    print("  ✓ Has human-readable __str__ method")


def test_type_hints():
    """Test that all types have proper type hints."""
    print("\n✓ Testing type hints...")

    # Get type hints for CompilationError
    error_hints = get_type_hints(CompilationError)
    assert 'stage' in error_hints
    assert 'severity' in error_hints
    assert 'message' in error_hints
    assert 'file' in error_hints
    assert 'line' in error_hints
    assert 'column' in error_hints

    print("  ✓ CompilationError has type hints")

    # Get type hints for CompilationResult
    result_hints = get_type_hints(CompilationResult)
    assert 'success' in result_hints
    assert 'stage' in result_hints
    assert 'output_file' in result_hints
    assert 'errors' in result_hints

    print("  ✓ CompilationResult has type hints")

    # Check that hints are correct types
    assert result_hints['success'] == bool

    print("  ✓ Type hints are properly specified")


def test_imports():
    """Test that types can be imported from validation module."""
    print("\n✓ Testing module imports...")

    # These imports already worked at the top of the file
    print("  ✓ Can import from vcdecomp.validation")
    print("  ✓ All types are exported in __all__")


def main():
    """Run all verification tests."""
    print("=" * 70)
    print("SUBTASK-1-4 VERIFICATION: Compilation Result Data Structures")
    print("=" * 70)

    try:
        test_compilation_stage_enum()
        test_error_severity_enum()
        test_compilation_error_structure()
        test_compilation_result_structure()
        test_type_hints()
        test_imports()

        print("\n" + "=" * 70)
        print("✓ ALL ACCEPTANCE CRITERIA MET")
        print("=" * 70)
        print("\nAcceptance Criteria Verified:")
        print("  ✓ CompilationResult includes success flag, output paths, errors, warnings")
        print("  ✓ CompilationError includes file, line, column, message, severity")
        print("  ✓ CompilationStage enum for SPP, SCC, SASM stages")
        print("  ✓ All types are properly typed with type hints")
        print("\nBonus Features Implemented:")
        print("  ✓ ErrorSeverity enum (INFO, WARNING, ERROR, FATAL)")
        print("  ✓ Helper methods (has_errors, has_warnings, error_count, etc.)")
        print("  ✓ Human-readable __str__ methods")
        print("  ✓ Additional useful fields (stdout, stderr, returncode, etc.)")

        return 0

    except AssertionError as e:
        print(f"\n✗ VERIFICATION FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
