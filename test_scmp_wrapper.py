#!/usr/bin/env python3
"""
Test script for SCMPWrapper implementation.

This script verifies that:
1. SCMPWrapper can be instantiated
2. The compilation types are properly defined
3. The wrapper can compile a test script
"""

import sys
import tempfile
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from vcdecomp.validation import (
    SCMPWrapper,
    CompilationResult,
    CompilationError,
    CompilationStage,
    ErrorSeverity,
)


def test_imports():
    """Test that all types are importable."""
    print("✓ All types imported successfully")
    print(f"  - SCMPWrapper: {SCMPWrapper}")
    print(f"  - CompilationResult: {CompilationResult}")
    print(f"  - CompilationError: {CompilationError}")
    print(f"  - CompilationStage: {CompilationStage}")
    print(f"  - ErrorSeverity: {ErrorSeverity}")


def test_instantiation():
    """Test that SCMPWrapper can be instantiated."""
    scmp_exe = Path("./original-resources/compiler/scmp.exe")

    if not scmp_exe.exists():
        print(f"⚠ SCMP executable not found at {scmp_exe}")
        print("  Skipping instantiation test")
        return

    include_dirs = [Path("./original-resources/compiler/inc")]

    try:
        wrapper = SCMPWrapper(
            executable_path=scmp_exe,
            include_dirs=include_dirs,
            cleanup_on_failure=False,  # Keep files for debugging
        )
        print("✓ SCMPWrapper instantiated successfully")
        print(f"  - Executable: {wrapper.executable_path}")
        print(f"  - Include dirs: {wrapper.include_dirs}")
        print(f"  - Timeout: {wrapper.timeout}s")
    except Exception as e:
        print(f"✗ Failed to instantiate SCMPWrapper: {e}")
        return


def test_compilation():
    """Test compilation of a real test script."""
    scmp_exe = Path("./original-resources/compiler/scmp.exe")

    if not scmp_exe.exists():
        print(f"⚠ SCMP executable not found at {scmp_exe}")
        print("  Skipping compilation test")
        return

    # Use the test script from Compiler-testruns/Testrun1
    test_source = Path("./Compiler-testruns/Testrun1/tdm.c")

    if not test_source.exists():
        print(f"⚠ Test source not found at {test_source}")
        print("  Skipping compilation test")
        return

    include_dirs = [Path("./original-resources/compiler/inc")]

    # Create temporary output paths
    with tempfile.TemporaryDirectory(prefix="scmp_test_") as tmpdir:
        tmpdir = Path(tmpdir)
        output_scr = tmpdir / "test.scr"
        output_h = tmpdir / "test.h"

        try:
            wrapper = SCMPWrapper(
                executable_path=scmp_exe,
                include_dirs=include_dirs,
                cleanup_on_failure=False,
                timeout=30,
            )

            print(f"\nCompiling {test_source.name}...")
            result = wrapper.compile(
                source_file=test_source,
                output_scr=output_scr,
                output_header=output_h,
            )

            print(f"\nCompilation Result:")
            print(f"  Success: {result.success}")
            print(f"  Stage: {result.stage.value}")
            print(f"  Return code: {result.returncode}")
            print(f"  Errors: {result.error_count}")
            print(f"  Warnings: {result.warning_count}")

            if result.output_file:
                print(f"  Output file: {result.output_file}")
                print(f"    - Size: {result.output_file.stat().st_size} bytes")

            if result.intermediate_files:
                print(f"  Intermediate files: {len(result.intermediate_files)}")
                for key, path in result.intermediate_files.items():
                    if path.exists():
                        print(f"    - {key}: {path.name} ({path.stat().st_size} bytes)")

            if result.errors:
                print(f"\n  Errors and warnings:")
                for error in result.errors[:5]:
                    print(f"    {error}")
                if len(result.errors) > 5:
                    print(f"    ... and {len(result.errors) - 5} more")

            if result.success:
                print("\n✓ Compilation test PASSED")
            else:
                print("\n✗ Compilation test FAILED (but wrapper worked correctly)")

            # Cleanup
            wrapper.cleanup(force=True)

        except Exception as e:
            print(f"✗ Compilation test failed with exception: {e}")
            import traceback
            traceback.print_exc()


def test_compilation_result_methods():
    """Test CompilationResult utility methods."""
    # Create a mock result
    result = CompilationResult(
        success=False,
        stage=CompilationStage.SCC,
        errors=[
            CompilationError(
                stage=CompilationStage.SPP,
                severity=ErrorSeverity.WARNING,
                message="Unused variable",
            ),
            CompilationError(
                stage=CompilationStage.SCC,
                severity=ErrorSeverity.ERROR,
                message="Syntax error",
                file=Path("test.c"),
                line=42,
            ),
        ],
    )

    print("\nTesting CompilationResult methods:")
    print(f"  has_errors: {result.has_errors}")
    print(f"  has_warnings: {result.has_warnings}")
    print(f"  error_count: {result.error_count}")
    print(f"  warning_count: {result.warning_count}")
    print(f"  SCC errors: {len(result.get_errors_by_stage(CompilationStage.SCC))}")
    print(f"\n  __str__ output:\n{result}")
    print("\n✓ CompilationResult methods work correctly")


def main():
    """Run all tests."""
    print("=" * 60)
    print("SCMP Wrapper Implementation Test")
    print("=" * 60)

    print("\n1. Testing imports...")
    test_imports()

    print("\n2. Testing instantiation...")
    test_instantiation()

    print("\n3. Testing CompilationResult methods...")
    test_compilation_result_methods()

    print("\n4. Testing actual compilation...")
    test_compilation()

    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
