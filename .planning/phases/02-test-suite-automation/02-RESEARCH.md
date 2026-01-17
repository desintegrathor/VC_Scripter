# Phase 2: Test Suite Automation - Research

**Researched:** 2026-01-17
**Domain:** pytest integration testing with compilation validation
**Confidence:** HIGH

## Summary

This phase builds a pytest-based test suite that validates decompilation quality by running the full decompile-compile-compare workflow on test scripts. The existing validation subsystem (`vcdecomp/validation/`) provides a mature, production-ready foundation with compilation orchestration, bytecode comparison, and error categorization already implemented. The primary task is creating pytest test functions that leverage this infrastructure to provide automated quality measurement and regression detection.

**Key findings:**
- Validation subsystem already implements the complete workflow (decompile → compile → compare → categorize)
- Test corpus is small (3 scripts in `decompiler_source_tests/`) with known original source
- pytest parametrization enables clean test organization and individual test targeting
- Existing `test_end_to_end_decompilation.py` provides pattern for pipeline testing

**Primary recommendation:** Use pytest parametrization with test discovery to iterate over test scripts, leveraging `ValidationOrchestrator` for the full validation workflow. Sequential execution with detailed failure reporting satisfies the user's goal to "see how deep in shit it is."

## Standard Stack

The established libraries for pytest-based integration testing with compilation validation:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pytest | 8.x | Test framework and runner | Industry standard Python testing framework, robust parametrization |
| pytest-subtests | 0.13+ | Subtest support for grouped assertions | Official pytest plugin, allows multiple assertions per test without stopping |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest-timeout | 2.3+ | Test execution timeouts | Long-running compilation tests |
| pytest-json-report | 1.5+ | JSON output for CI integration | Automated reporting and metrics |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pytest parametrize | pytest.mark.parametrize with indirect | Parametrize is cleaner for simple cases; indirect for complex fixture setup |
| Sequential execution | pytest-xdist (parallel) | User explicitly wants sequential to see clearer output |
| Manual test discovery | Dynamic discovery in conftest.py | Manual is simpler for small corpus (3 scripts) |

**Installation:**
```bash
pip install pytest pytest-subtests pytest-timeout pytest-json-report
```

## Architecture Patterns

### Recommended Project Structure
```
vcdecomp/tests/
├── test_validation.py           # Main validation test suite (Phase 2 deliverable)
├── test_end_to_end_decompilation.py  # Existing pattern reference
├── conftest.py                   # Shared fixtures (compiler paths, orchestrator)
└── fixtures/                     # Test data if needed
```

### Pattern 1: Parametrized Validation Tests
**What:** Use `@pytest.mark.parametrize` to run the same validation workflow on each test script
**When to use:** Testing multiple scripts with identical validation workflow
**Example:**
```python
# Source: pytest official docs + existing validation subsystem
import pytest
from pathlib import Path
from vcdecomp.validation import ValidationOrchestrator
from vcdecomp.core.loader import SCRFile
from vcdecomp.core.ir.structure import format_structured_function_named

# Discover test scripts
TEST_SCRIPTS = [
    ("test1/tt", Path("decompiler_source_tests/test1/tt.scr"), Path("decompiler_source_tests/test1/tt.c")),
    ("test2/tdm", Path("decompiler_source_tests/test2/tdm.scr"), Path("decompiler_source_tests/test2/tdm.c")),
    ("test3/LEVEL", Path("decompiler_source_tests/test3/LEVEL.SCR"), Path("decompiler_source_tests/test3/LEVEL.C")),
]

@pytest.fixture(scope="session")
def validation_orchestrator():
    """Create validation orchestrator once for all tests"""
    return ValidationOrchestrator(
        compiler_dir=Path("original-resources/compiler"),
        include_dirs=[Path("original-resources/compiler/inc")],
        timeout=120,
        cache_enabled=False,  # Always fresh decompilation per user requirement
    )

@pytest.mark.parametrize("test_id,scr_path,original_c", TEST_SCRIPTS)
def test_validation_workflow(test_id, scr_path, original_c, validation_orchestrator, tmp_path):
    """Test full decompile → compile → compare workflow for a script"""
    # Step 1: Decompile
    decompiled_path = tmp_path / f"{test_id}_decompiled.c"
    scr = SCRFile.load(str(scr_path))
    # ... decompilation logic ...

    # Step 2: Validate (compile + compare)
    result = validation_orchestrator.validate(scr_path, decompiled_path)

    # Step 3: Assert and report
    assert result.compilation_succeeded, f"Compilation failed: {result.error_message}"
    # Continue assertions even if compilation passed but bytecode differs
```

### Pattern 2: Subtest Pattern for Multiple Functions
**What:** Use `pytest.subtests` to test each function in a script independently while collecting all failures
**When to use:** When scripts contain multiple functions and you want to see all function-level failures in one run
**Example:**
```python
# Source: pytest-subtests official docs
def test_script_all_functions(test_id, scr_path, validation_orchestrator, subtests):
    """Test each function in a script independently"""
    scr = SCRFile.load(str(scr_path))
    ssa_func = build_ssa_all_blocks(scr)
    func_bounds = disasm.get_function_boundaries()

    for func_name, (start, end) in func_bounds.items():
        with subtests.test(function=func_name):
            # Decompile this function
            output = format_structured_function_named(ssa_func, func_name, start, end, resolver)
            # Assertions for this function
            assert len(output) > 0, f"Empty output for {func_name}"
```

### Pattern 3: Fresh Decompilation Per Test
**What:** Always decompile from .scr on every test run, never use cached decompilation
**When to use:** When testing current decompiler state (user requirement: "always fresh decompilation")
**Example:**
```python
# Disable validation cache, use temp directory for each test
@pytest.fixture
def temp_decompiled(tmp_path):
    """Provides temp path for decompiled output, auto-cleaned after test"""
    return tmp_path / "decompiled.c"

def test_with_fresh_decompilation(scr_path, temp_decompiled):
    # Decompile to temp path (fresh every time)
    scr = SCRFile.load(str(scr_path))
    # ... decompilation to temp_decompiled ...

    # Test continues with fresh output
```

### Anti-Patterns to Avoid
- **Caching decompiled output:** User wants to test current decompiler state, not cached results
- **Fail-fast mode:** User wants to "see complete picture of what's broken" - use subtests or parametrize with continue-on-failure
- **Shared temp files:** Use `tmp_path` fixture (per-test) not `tmp_path_factory` (shared)

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Test script discovery | Manual list maintenance | `pytest.mark.parametrize` with glob discovery | Automatically finds new test scripts |
| Compilation subprocess management | Raw `subprocess.run` | `ValidationOrchestrator.validate()` | Handles timeouts, error parsing, cleanup |
| Bytecode comparison | Manual hex comparison | `BytecodeComparator.compare_files()` | Handles SCR format, opcode variants, semantic vs cosmetic |
| Error categorization | Manual parsing of compiler output | `CompilationError` with `.err` file parsing | Already extracts file/line/severity from SCC/SPP/SASM errors |
| Test failure reporting | String concatenation | `ValidationResult.to_dict()` / `.to_json()` | Structured output ready for CI/reporting tools |

**Key insight:** The validation subsystem (`vcdecomp/validation/`) already implements the complex parts. Don't reimplement compilation orchestration, bytecode comparison, or error categorization - just call `ValidationOrchestrator.validate()` and inspect the `ValidationResult`.

## Common Pitfalls

### Pitfall 1: Not Preserving Artifacts on Failure
**What goes wrong:** Test fails, temp files cleaned up, debugging impossible
**Why it happens:** pytest's `tmp_path` auto-cleans after test completion
**How to avoid:** Use `--basetemp` flag or conditionally preserve on failure
**Warning signs:** "I need to debug but the .err file is gone"

**Prevention strategy:**
```python
@pytest.fixture
def preserve_on_failure(request, tmp_path):
    """Preserve temp files if test fails"""
    yield tmp_path
    if request.node.rep_call.failed:
        # Copy to permanent location
        artifacts_dir = Path(".test_artifacts") / request.node.name
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(tmp_path, artifacts_dir, dirs_exist_ok=True)
```

### Pitfall 2: Compiler Path Assumptions
**What goes wrong:** Tests pass on dev machine, fail in CI (compiler not found)
**Why it happens:** Hardcoded paths to `original-resources/compiler/SCMP.exe`
**How to avoid:** Use environment variable with fallback, validate in conftest.py
**Warning signs:** `FileNotFoundError: SCMP.exe not found`

**Prevention strategy:**
```python
# conftest.py
import os
def pytest_configure(config):
    compiler_dir = os.getenv("VCDECOMP_COMPILER_DIR", "original-resources/compiler")
    if not (Path(compiler_dir) / "SCMP.exe").exists():
        pytest.exit(f"Compiler not found at {compiler_dir}. Set VCDECOMP_COMPILER_DIR env var.")
```

### Pitfall 3: Sequential vs Parallel Confusion
**What goes wrong:** Assuming pytest-xdist is needed for parametrized tests
**Why it happens:** Confusing parametrization (creates separate test items) with parallel execution (runs items concurrently)
**How to avoid:** Understand that parametrization gives individual test items without needing xdist
**Warning signs:** User wants sequential but researching parallel execution tools

**Key distinction:**
- Parametrization = one test function → many test items (collection time)
- pytest-xdist = run test items in parallel (execution time)
- User wants parametrization (many items) but NOT xdist (sequential execution)

### Pitfall 4: Bytecode Comparison Interpretation
**What goes wrong:** Treating all bytecode differences as failures
**Why it happens:** Not understanding semantic vs cosmetic vs optimization differences
**How to avoid:** Use `ValidationResult.verdict` and category counts, not just "identical or not"
**Warning signs:** Test fails on cosmetic differences that don't affect behavior

**Correct interpretation:**
```python
# BAD: Treat all differences as failures
assert result.bytecode_identical, "Bytecode differs"

# GOOD: Categorize and report appropriately
if result.verdict == ValidationVerdict.PASS:
    # Identical or only cosmetic/optimization differences
    pass
elif result.verdict == ValidationVerdict.PARTIAL:
    # Has semantic differences but compiles
    pytest.fail(f"Semantic differences: {result.difference_summary.semantic_count}")
else:
    # Compilation failed or critical error
    pytest.fail(f"Validation failed: {result.error_message}")
```

## Code Examples

Verified patterns from the validation subsystem:

### Complete Validation Test
```python
# Source: vcdecomp/validation/validator.py + pytest docs
import pytest
from pathlib import Path
from vcdecomp.core.loader import SCRFile
from vcdecomp.core.disasm import Disassembler
from vcdecomp.core.ir.ssa import build_ssa_all_blocks
from vcdecomp.core.ir.structure import format_structured_function_named
from vcdecomp.core.ir.global_resolver import GlobalResolver
from vcdecomp.core.headers.detector import generate_include_block
from vcdecomp.validation import ValidationOrchestrator, ValidationVerdict

# Test data discovery
TEST_CORPUS = [
    pytest.param("test1/tt", "decompiler_source_tests/test1/tt.scr",
                 id="tt-turntable"),
    pytest.param("test2/tdm", "decompiler_source_tests/test2/tdm.scr",
                 id="tdm-deathmatch"),
    pytest.param("test3/LEVEL", "decompiler_source_tests/test3/LEVEL.SCR",
                 id="level-script"),
]

@pytest.fixture(scope="session")
def compiler_paths():
    """Paths to compiler and includes"""
    return {
        "compiler_dir": Path("original-resources/compiler"),
        "include_dirs": [Path("original-resources/compiler/inc")],
    }

@pytest.fixture(scope="session")
def orchestrator(compiler_paths):
    """Validation orchestrator for all tests"""
    return ValidationOrchestrator(
        compiler_dir=compiler_paths["compiler_dir"],
        include_dirs=compiler_paths["include_dirs"],
        timeout=120,
        cache_enabled=False,  # Always fresh per requirement
    )

@pytest.mark.parametrize("test_id,scr_path", TEST_CORPUS)
def test_decompilation_validation(test_id, scr_path, orchestrator, tmp_path):
    """
    Test complete decompile → compile → compare workflow.

    Success criteria:
    1. Decompilation produces valid C code
    2. C code compiles successfully with original compiler
    3. Recompiled bytecode is semantically equivalent to original
    """
    scr_path = Path(scr_path)
    assert scr_path.exists(), f"Test script not found: {scr_path}"

    # Step 1: Decompile
    decompiled_path = tmp_path / f"{test_id.replace('/', '_')}_decompiled.c"

    scr = SCRFile.load(str(scr_path))
    ssa_func = build_ssa_all_blocks(scr)
    disasm = Disassembler(scr)
    func_bounds = disasm.get_function_boundaries()

    # Generate includes
    includes = generate_include_block(scr)

    # Analyze globals
    resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
    resolver.analyze()

    # Decompile all functions
    outputs = []
    for func_name, (start, end) in func_bounds.items():
        output = format_structured_function_named(
            ssa_func, func_name, start, end, resolver
        )
        outputs.append(output)

    # Write decompiled output
    with open(decompiled_path, 'w') as f:
        f.write(includes)
        f.write('\n\n')
        f.write('\n\n'.join(outputs))

    # Step 2: Validate (compile + compare)
    result = orchestrator.validate(scr_path, decompiled_path)

    # Step 3: Report results
    print("\n" + "=" * 80)
    print(f"VALIDATION RESULT: {test_id}")
    print("=" * 80)
    print(result)

    # Step 4: Assert based on verdict
    assert result.compilation_succeeded, (
        f"Compilation failed for {test_id}:\n"
        f"{result.error_message}\n"
        f"Errors: {[str(e) for e in result.compilation_result.errors[:3]]}"
    )

    # Compilation succeeded - check bytecode equivalence
    if result.verdict == ValidationVerdict.PASS:
        # Perfect or cosmetic-only differences
        print(f"✓ {test_id}: PASS")
    elif result.verdict == ValidationVerdict.PARTIAL:
        # Has semantic differences
        semantic_count = result.difference_summary.semantic_count
        print(f"⚠ {test_id}: PARTIAL ({semantic_count} semantic differences)")
        # Don't fail - collect all results
    else:
        # Should not reach here if compilation succeeded
        pytest.fail(f"Unexpected verdict: {result.verdict}")
```

### Error Categorization Analysis
```python
# Source: vcdecomp/validation/difference_types.py
def test_error_categorization(test_id, scr_path, orchestrator, tmp_path):
    """Test error categorization for debugging workflow"""
    decompiled_path = tmp_path / f"{test_id}_decompiled.c"
    # ... decompilation ...

    result = orchestrator.validate(scr_path, decompiled_path)

    if result.categorized_differences:
        # Analyze by category
        from vcdecomp.validation.difference_types import DifferenceCategory

        semantic = result.get_differences_by_category(DifferenceCategory.SEMANTIC)
        cosmetic = result.get_differences_by_category(DifferenceCategory.COSMETIC)
        optimization = result.get_differences_by_category(DifferenceCategory.OPTIMIZATION)

        print(f"\nDifference Breakdown for {test_id}:")
        print(f"  Semantic: {len(semantic)}")
        print(f"  Cosmetic: {len(cosmetic)}")
        print(f"  Optimization: {len(optimization)}")

        # Show first few semantic differences
        if semantic:
            print("\nFirst semantic differences:")
            for diff in semantic[:3]:
                print(f"  - {diff.rationale}")
                print(f"    {diff.difference.description}")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual test running | pytest parametrization | pytest 3.0+ (2017) | Individual test targeting, better reporting |
| unittest.TestCase | pytest functions with fixtures | pytest 2.0+ (2010) | Cleaner test code, better fixture composition |
| Manual subprocess handling | pytest-subprocess plugin | 2020 | Safer subprocess mocking/validation |
| Inline subtests | pytest-subtests plugin (now core) | pytest 9.0 (2025) | Native subtest support |

**Deprecated/outdated:**
- `unittest.TestCase.subTest()` → Use `pytest.subtests` fixture (merged into pytest 9.0)
- `pytest.mark.parametrize(indirect=True)` for simple cases → Use direct parametrization
- Manual test ID generation → Use `pytest.param(..., id="name")` for readable IDs

## Open Questions

Things that couldn't be fully resolved:

1. **Test organization granularity**
   - What we know: 3 test scripts currently, could grow to dozens
   - What's unclear: Whether to organize by script type (MP vs SP) or complexity level
   - Recommendation: Start flat (single `test_validation.py`), reorganize after seeing decompilation quality patterns

2. **Failure threshold for CI**
   - What we know: User wants to "see how deep in shit it is" - implies seeing all failures
   - What's unclear: What percentage of failures should block CI (if any)
   - Recommendation: Phase 4 (Error Analysis) will inform failure thresholds based on actual data

3. **Artifact preservation strategy**
   - What we know: `.err` files, intermediate `.c` files, and bytecode diffs are valuable for debugging
   - What's unclear: How much to preserve (all tests? only failures?) and where (`.test_artifacts/`? CI storage?)
   - Recommendation: Preserve only failures initially, expand if storage allows

## Sources

### Primary (HIGH confidence)
- pytest official documentation (parametrize, fixtures, subtests) - [pytest.org](https://docs.pytest.org/)
- Existing validation subsystem code (`vcdecomp/validation/validator.py`, `difference_types.py`, `compiler_wrapper.py`)
- Existing test patterns (`vcdecomp/tests/test_end_to_end_decompilation.py`, `test_regression_baseline.py`)

### Secondary (MEDIUM confidence)
- pytest-subtests documentation - [GitHub](https://github.com/pytest-dev/pytest-subtests)
- pytest parametrization best practices - [Mergify article](https://articles.mergify.com/pytest-parametrize/)

### Tertiary (LOW confidence)
- pytest-subprocess for future subprocess mocking needs - marked for validation

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - pytest is established standard, validation subsystem already built
- Architecture: HIGH - patterns verified against existing codebase and official docs
- Pitfalls: MEDIUM - based on common pytest issues + domain knowledge of compilation testing

**Research date:** 2026-01-17
**Valid until:** 90 days (pytest stable, validation subsystem mature)
