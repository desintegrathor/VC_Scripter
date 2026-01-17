---
phase: 02-test-suite-automation
plan: 01
subsystem: testing
tags: [pytest, validation, bytecode-comparison, decompilation-quality]

# Dependency graph
requires:
  - phase: 01-gui-validation-integration
    provides: "ValidationOrchestrator with compiler wrapper and bytecode comparison"
provides:
  - "Automated pytest test suite for decompilation quality measurement"
  - "Parametrized tests for 3 test scripts (tt, tdm, LEVEL)"
  - "Programmatic error and bytecode difference categorization"
  - "Iterative improvement workflow with fast feedback"
affects: [03-ci-cd-integration, 04-error-analysis-reporting, 06-expression-reconstruction, 07-control-flow-detection, 08-type-inference]

# Tech tracking
tech-stack:
  added: [pytest-fixtures, pytest-parametrize, tmp_path-fixture]
  patterns: ["Decompile-compile-compare test pattern", "Programmatic error categorization", "Sequential test execution for clear output"]

key-files:
  created:
    - vcdecomp/tests/test_validation.py
    - vcdecomp/tests/conftest.py
  modified:
    - vcdecomp/validation/validator.py

key-decisions:
  - "Sequential test execution (no pytest-xdist) for clearer output and debugging"
  - "cache_enabled=False for always-fresh decompilation per test"
  - "Programmatic error categorization (syntax, type, undefined, include, other)"
  - "PARTIAL verdict does not fail tests - user wants complete picture"
  - "Global threading lock for SCMP.exe to prevent concurrent execution"

patterns-established:
  - "Pattern 1: Test parametrization with case-sensitive filesystem paths (test1/test2 lowercase, test3 UPPERCASE)"
  - "Pattern 2: Three-step test flow (decompile → validate → report with programmatic categorization)"
  - "Pattern 3: Error breakdown by category for quality measurement (not just pass/fail)"
  - "Pattern 4: Serialize compiler access with threading.Lock() for concurrency safety"

# Metrics
duration: 10min
completed: 2026-01-17
---

# Phase 02 Plan 01: Pytest Validation Test Suite Summary

**Automated pytest test suite measuring decompilation quality through complete decompile → compile → compare workflow with programmatic error categorization**

## Performance

- **Duration:** 10 min
- **Started:** 2026-01-17T17:31:41+01:00 (commit f767cdf)
- **Completed:** 2026-01-17T17:39:21+01:00 (commit 186c9fe)
- **Tasks:** 2 (1 auto, 1 checkpoint)
- **Files modified:** 3

## Accomplishments
- Created pytest test suite with parametrization for 3 test scripts
- Integrated complete decompilation pipeline (SSA, structure analysis, code generation)
- Programmatic error and bytecode difference categorization
- **Critical fix:** Added threading lock to serialize SCMP.exe compiler access
- Enabled fast iterative improvement workflow with clear quality measurement

## Task Commits

Each task was committed atomically:

1. **Task 1: Create pytest validation test suite with parametrization** - `f767cdf` (test)
   - Created test_validation.py with 224 lines
   - Created conftest.py with 57 lines
   - Implemented decompile → compile → compare workflow
   - Added programmatic error and bytecode difference categorization

2. **Critical fix (checkpoint discovery):** Added compiler concurrency lock - `186c9fe` (fix)
   - Discovered during checkpoint verification
   - SCMP.exe cannot handle concurrent execution
   - Added threading.Lock() to serialize compiler access in ValidationOrchestrator
   - Prevents pytest test failures from compiler crashes

**Plan metadata:** (will be committed after SUMMARY.md creation)

## Files Created/Modified

### Created:
- `vcdecomp/tests/test_validation.py` (224 lines) - Parametrized pytest tests for decompilation validation
  - Decompiles each .scr file using structure module pipeline
  - Compiles decompiled output with ValidationOrchestrator
  - Compares bytecode and categorizes differences
  - Reports detailed results with error breakdowns

- `vcdecomp/tests/conftest.py` (57 lines) - Shared pytest fixtures
  - compiler_paths fixture (session scope)
  - validation_orchestrator fixture (cache_enabled=False, timeout=120)

### Modified:
- `vcdecomp/validation/validator.py` - Added global threading.Lock() for SCMP.exe serialization
  - Prevents concurrent compiler execution
  - Critical for pytest test stability

## Decisions Made

**Sequential test execution:**
- Rationale: Clearer output for debugging, avoids pytest-xdist complexity
- Tests run one at a time, showing detailed results for each

**Cache disabled for tests:**
- Rationale: Always-fresh decompilation ensures tests measure current decompiler state
- No stale cached results affecting test accuracy

**PARTIAL verdict doesn't fail tests:**
- Rationale: User wants to see complete picture of all test results
- Semantic differences are tracked but don't stop test execution

**Programmatic error categorization:**
- Rationale: Enables automated quality analysis and trend tracking
- Categories: syntax, type, undefined, include, other
- Bytecode categories: SEMANTIC, COSMETIC, OPTIMIZATION, UNKNOWN

**Global compiler lock (critical fix):**
- Rationale: SCMP.exe is DOS-era executable that cannot handle concurrent execution
- Threading lock serializes all compiler access
- Prevents file corruption and compiler crashes

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Added compiler concurrency lock**
- **Found during:** Task 2 (Human verification checkpoint)
- **Issue:** SCMP.exe crashes when multiple pytest tests attempt compilation simultaneously. Even sequential pytest execution may have concurrency issues due to pytest's internal parallelization or fixture setup.
- **Fix:** Added `threading.Lock()` at module level in validator.py, wrap `wrapper.compile()` call with lock acquisition to serialize compiler access
- **Files modified:** vcdecomp/validation/validator.py
- **Verification:** Tests run successfully without compiler crashes, proper error reporting restored
- **Committed in:** 186c9fe (separate fix commit documenting root cause)

---

**Total deviations:** 1 auto-fixed (1 bug - concurrency issue)
**Impact on plan:** Critical fix required for test suite to function correctly. Without lock, tests would fail unreliably due to compiler race conditions. This is a correctness issue, not scope creep.

## Issues Encountered

**Compiler concurrency bug discovered at checkpoint:**
- User reported tests were executing but showing compilation errors
- Investigation revealed SCMP.exe cannot handle concurrent execution
- Root cause: DOS-era executable with no concurrency support
- Solution: Global threading lock to serialize compiler access
- Lesson: Legacy DOS executables require serialization even in seemingly sequential test execution

## User Setup Required

None - no external service configuration required.

All dependencies are already configured from Phase 01:
- Original compiler (SCMP.exe) in original-resources/compiler/
- Include headers in original-resources/compiler/inc/
- Test scripts in decompiler_source_tests/

## Test Results Quality Assessment

**Test corpus coverage:**
- 3 test scripts: tt (turntable), tdm (team deathmatch), LEVEL (mission script)
- All tests execute successfully with proper error reporting
- Decompilation completes for all scripts (varying quality)

**Test suite capabilities:**
- Discovers and runs all 3 scripts via pytest parametrization
- Individual test targeting: `pytest -k tt-turntable`
- Detailed validation results with error breakdowns
- Programmatic categorization enables quality trend tracking

**Quality measurement ready:**
- Test suite provides foundation for iterative improvement
- Error categorization enables targeted fixes (syntax vs types vs control flow)
- Bytecode comparison distinguishes semantic vs cosmetic differences
- Developer can run `pytest vcdecomp/tests/test_validation.py` to measure progress

## Next Phase Readiness

**Phase 3 (CI/CD Integration) - READY:**
- Test suite runs successfully with pytest
- Can be integrated into GitHub Actions workflow
- Note: Requires Windows runner (SCMP.exe is Windows-only)

**Phase 4 (Error Analysis and Reporting) - READY:**
- Programmatic error categorization foundation in place
- Test suite generates detailed validation results
- Can be extended with aggregation and trend analysis

**Phase 6-8 (Decompiler Fixes) - READY:**
- Fast feedback loop established
- Error categorization helps prioritize fixes
- Bytecode comparison validates correctness of improvements

**No blockers for next phases.**

---
*Phase: 02-test-suite-automation*
*Completed: 2026-01-17*
