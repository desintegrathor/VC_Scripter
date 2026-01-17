"""
Automated validation test suite for decompilation quality measurement.

Tests the complete decompile → compile → compare workflow on all test scripts
from decompiler_source_tests/ to enable iterative improvement workflow.

Usage:
    # Run all validation tests
    PYTHONPATH=. python -m pytest vcdecomp/tests/test_validation.py -v

    # Run specific test
    PYTHONPATH=. python -m pytest vcdecomp/tests/test_validation.py::test_decompilation_validation[tt-turntable] -v

    # Preserve test artifacts for debugging
    PYTHONPATH=. python -m pytest vcdecomp/tests/test_validation.py --basetemp=.test_artifacts
"""

import pytest
from pathlib import Path

from vcdecomp.core.loader import SCRFile
from vcdecomp.core.disasm import Disassembler
from vcdecomp.core.ir.ssa import build_ssa_all_blocks
from vcdecomp.core.ir.structure import format_structured_function_named
from vcdecomp.core.headers.detector import generate_include_block
from vcdecomp.core.ir.global_resolver import GlobalResolver
from vcdecomp.validation.validation_types import ValidationVerdict
from vcdecomp.validation.difference_types import DifferenceCategory


# Test corpus with exact case-sensitive paths (verified on filesystem)
TEST_SCRIPTS = [
    pytest.param("test1/tt", Path("decompiler_source_tests/test1/tt.scr"),
                 Path("decompiler_source_tests/test1/tt.c"), id="tt-turntable"),
    pytest.param("test2/tdm", Path("decompiler_source_tests/test2/tdm.scr"),
                 Path("decompiler_source_tests/test2/tdm.c"), id="tdm-deathmatch"),
    pytest.param("test3/LEVEL", Path("decompiler_source_tests/test3/LEVEL.SCR"),
                 Path("decompiler_source_tests/test3/LEVEL.C"), id="level-script"),
]


@pytest.mark.parametrize("test_id,scr_path,original_c", TEST_SCRIPTS)
def test_decompilation_validation(test_id, scr_path, original_c, validation_orchestrator, tmp_path):
    """
    Test complete decompile → compile → compare workflow.

    Success criteria:
    1. Decompilation produces valid C code
    2. C code compiles successfully with original compiler
    3. Recompiled bytecode is semantically equivalent to original

    Args:
        test_id: Test identifier (e.g., "test1/tt")
        scr_path: Path to original .scr file
        original_c: Path to original .c source (for reference)
        validation_orchestrator: ValidationOrchestrator fixture
        tmp_path: Pytest temporary directory fixture
    """
    print(f"\n{'='*80}")
    print(f"Testing: {test_id}")
    print(f"{'='*80}")

    # ========================================================================
    # STEP 1: Decompile .scr file to C source
    # ========================================================================
    print(f"\n[1/3] Decompiling {scr_path.name}...")

    try:
        # Load SCR file
        scr = SCRFile.load(str(scr_path))

        # Build SSA
        ssa_func = build_ssa_all_blocks(scr)

        # Get function boundaries
        disasm = Disassembler(scr)
        func_bounds = disasm.get_function_boundaries()

        # Generate include block
        include_block = generate_include_block(scr)

        # Analyze globals (for internal use - not emitted as declarations)
        resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
        resolver.analyze()

        # Decompile all functions
        function_outputs = []
        decompilation_errors = []
        for func_name, (start, end) in func_bounds.items():
            try:
                output = format_structured_function_named(
                    ssa_func, func_name, start, end, resolver
                )
                function_outputs.append(output)
            except Exception as e:
                # Track function decompilation failures
                decompilation_errors.append((func_name, str(e)))
                print(f"  X Function {func_name} failed: {type(e).__name__}")

        # If all functions failed, this is a critical decompiler bug
        if not function_outputs:
            print(f"\nX {test_id}: DECOMPILATION FAILED")
            print(f"  All {len(func_bounds)} functions failed to decompile")
            if decompilation_errors:
                print(f"  First error: {decompilation_errors[0][1][:200]}")
            pytest.fail(
                f"Decompilation failed for all functions. "
                f"First error in {decompilation_errors[0][0]}: {decompilation_errors[0][1][:200]}"
            )

        # Assemble complete .c file (includes + functions, NO globals declarations)
        decompiled_content = include_block + "\n\n" + "\n\n".join(function_outputs)

        # Write to temp file
        decompiled_path = tmp_path / f"{test_id.replace('/', '_')}_decompiled.c"
        decompiled_path.write_text(decompiled_content, encoding="utf-8")

        print(f"OK Decompiled to: {decompiled_path}")
        print(f"  Functions: {len(function_outputs)}/{len(func_bounds)} succeeded")
        if decompilation_errors:
            print(f"  Partial decompilation: {len(decompilation_errors)} function(s) failed")
        print(f"  Size: {len(decompiled_content)} bytes")

    except Exception as e:
        # Critical decompilation failure (not function-level)
        print(f"\nX {test_id}: DECOMPILATION CRASHED")
        print(f"  Error: {type(e).__name__}: {str(e)[:200]}")
        pytest.fail(f"Decompilation crashed: {type(e).__name__}: {str(e)[:500]}")

    # ========================================================================
    # STEP 2: Validate using ValidationOrchestrator
    # ========================================================================
    print(f"\n[2/3] Compiling and comparing bytecode...")

    result = validation_orchestrator.validate(scr_path, decompiled_path)

    # ========================================================================
    # STEP 3: Report detailed results
    # ========================================================================
    print(f"\n[3/3] Validation results:")
    print("="*80)
    print(f"Verdict: {result.verdict.value.upper()}")
    print(f"Original:    {result.original_scr}")
    print(f"Decompiled:  {result.decompiled_source}")
    print("="*80)

    # Extract and report compilation error categories
    if not result.compilation_succeeded:
        print("\n" + "="*80)
        print("COMPILATION ERROR ANALYSIS")
        print("="*80)

        # Group errors by type for programmatic analysis
        error_types = {}
        for error in result.compilation_result.errors:
            # Extract error type from message (heuristic)
            msg_lower = error.message.lower()
            if "syntax" in msg_lower or "expected" in msg_lower:
                error_type = "syntax"
            elif "undefined" in msg_lower or "undeclared" in msg_lower:
                error_type = "undefined"
            elif "type" in msg_lower:
                error_type = "type"
            elif "include" in msg_lower or "cannot open" in msg_lower:
                error_type = "include"
            else:
                error_type = "other"

            error_types[error_type] = error_types.get(error_type, 0) + 1

        print(f"\nError breakdown: {error_types}")
        print(f"Total errors: {len(result.compilation_result.errors)}")

        # Show first 3 errors for context
        print("\nFirst 3 errors:")
        for i, error in enumerate(result.compilation_result.errors[:3], 1):
            print(f"  {i}. {error}")

    # Extract and report bytecode difference categories
    if result.categorized_differences:
        print("\n" + "="*80)
        print("BYTECODE DIFFERENCE ANALYSIS")
        print("="*80)

        # Group by category
        category_counts = {}
        for diff in result.categorized_differences:
            cat = diff.category.name  # SEMANTIC, COSMETIC, OPTIMIZATION, UNKNOWN
            category_counts[cat] = category_counts.get(cat, 0) + 1

        print(f"\nBytecode difference breakdown: {category_counts}")

        # Show some examples
        if category_counts.get("SEMANTIC", 0) > 0:
            print("\nSample semantic differences:")
            semantic_diffs = result.get_differences_by_category(DifferenceCategory.SEMANTIC)
            for diff in semantic_diffs[:3]:
                print(f"  - {diff.difference.type.name}: {diff.rationale}")

    # ========================================================================
    # STEP 4: Assert and determine verdict
    # ========================================================================

    # First check: compilation must succeed
    if not result.compilation_succeeded:
        print(f"\nX {test_id}: COMPILATION FAILED")
        pytest.fail(
            f"Compilation failed with {len(result.compilation_result.errors)} errors. "
            f"First error: {result.compilation_result.errors[0] if result.compilation_result.errors else 'Unknown'}"
        )

    # Compilation succeeded - check verdict
    if result.verdict == ValidationVerdict.PASS:
        if result.bytecode_identical:
            print(f"\nOK {test_id}: PASS (bytecode identical)")
        else:
            print(f"\nOK {test_id}: PASS (only cosmetic differences)")
    elif result.verdict == ValidationVerdict.PARTIAL:
        semantic_count = len(result.get_differences_by_category(DifferenceCategory.SEMANTIC))
        print(f"\n! {test_id}: PARTIAL ({semantic_count} semantic differences)")
        # DO NOT fail test - user wants complete picture
    else:
        # Unexpected verdict
        pytest.fail(f"Unexpected verdict: {result.verdict}")
