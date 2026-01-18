---
phase: 06-expression-reconstruction-fixes
plan: 01
subsystem: decompiler-core
tags: [expression-reconstruction, validation, error-analysis, baseline-metrics]

# Dependency graph
requires:
  - phase: 04-error-analysis-system
    provides: Error categorization module (error_analyzer.py) for systematic error classification
  - phase: 02-test-suite-automation
    provides: Validation test suite infrastructure for decompile-compile-compare workflow
provides:
  - Comprehensive error baseline documenting 6 categories of expression reconstruction bugs
  - Prioritized fix targets for Phase 6 Plans 02-04
  - Baseline metrics for measuring fix effectiveness
affects:
  - 06-02: Will use baseline to guide undefined goto label fixes
  - 06-03: Will use baseline to guide type mismatch fixes
  - 06-04: Will use baseline to measure overall improvement

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Manual source inspection for compiler crash scenarios (when automated error analysis fails)
    - Priority-based fix ordering (CRITICAL → HIGH → MEDIUM based on frequency × severity)

key-files:
  created:
    - .planning/phases/06-expression-reconstruction-fixes/ERROR_BASELINE.md
  modified: []

key-decisions:
  - "Manual inspection approach: Compiler crashes prevent automated error file parsing, manual source review required"
  - "6-pattern categorization: Undefined goto, type mismatch, missing return, multiple assignments, undeclared vars, unreachable code"
  - "3-tier priority system: CRITICAL (blocks compilation) → HIGH (correctness) → MEDIUM (code quality)"

patterns-established:
  - "Baseline-driven debugging: Establish quantitative baseline before fixes, measure improvement after"
  - "Compiler crash diagnosis: When SCMP.exe crashes (0xC0000005), inspect decompiled source manually"
  - "Pattern extraction from multiple test files: Cross-reference errors across all test cases to identify systematic vs edge-case bugs"

# Metrics
duration: 6min
completed: 2026-01-18
---

# Phase 6 Plan 01: Expression Error Baseline Summary

**Documented 6 categories of expression reconstruction bugs causing compiler crashes in 100% of test cases with prioritized fix targets**

## Performance

- **Duration:** 6 min
- **Started:** 2026-01-18T09:33:49Z
- **Completed:** 2026-01-18T09:39:57Z
- **Tasks:** 3
- **Files modified:** 1

## Accomplishments

- Executed validation test suite on 3 test scripts (tt.scr, tdm.scr, LEVEL.scr)
- Identified compiler crash (0xC0000005 access violation) as 100% failure mode
- Manually inspected decompiled code to extract 6 error patterns
- Created comprehensive 357-line ERROR_BASELINE.md with prioritized fix targets
- Established measurement methodology for Phase 6 success criteria

## Task Commits

Each task was committed atomically:

1. **Task 1: Run validation test suite and collect error data** - (no commit - analysis only)
2. **Task 2: Analyze error patterns and create baseline report** - (no commit - report creation)
3. **Task 3: Commit baseline report** - `d759a28` (docs)

**Plan metadata:** Final commit in this summary documentation.

## Files Created/Modified

- `.planning/phases/06-expression-reconstruction-fixes/ERROR_BASELINE.md` - Comprehensive error baseline with 6 patterns, 3-tier priority system, baseline metrics for all 3 test scripts

## Error Pattern Summary

### CRITICAL Priority (Blocks compilation)

1. **Pattern 1: Undefined goto labels** - Orphaned CFG blocks emitted as goto to non-existent labels
2. **Pattern 5: Undeclared variables** - Variables like `vec`, `enum_pl`, `abl_list` used but not declared

### HIGH Priority (Major correctness issues)

3. **Pattern 2: Type mismatches** - `int` variables assigned float literals, struct types used as scalars
4. **Pattern 3: Missing return values** - `int` functions with `return;` instead of `return <value>;`

### MEDIUM Priority (Code quality)

5. **Pattern 4: Multiple sequential assignments** - SSA temporaries not optimized: `tmp=1; tmp=2; tmp=3; return tmp;`
6. **Pattern 6: Unreachable code** - Dead code after return statements

## Baseline Metrics

- **Test 1 (tt.scr)**: 11/15 functions decompiled, compiler crash, 21+ error instances
- **Test 2 (tdm.scr)**: Compiler crash, 2+ error instances identified
- **Test 3 (LEVEL.scr)**: Compiler crash, 7+ error instances identified

**Success criteria for Phase 6**: 1/3 tests compile successfully, Pattern 1 & 5 eliminated, Pattern 3 reduced 50%

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Manual source inspection for baseline | Compiler crashes (0xC0000005) prevent automated error file parsing - automated categorization requires parseable errors |
| 6-pattern categorization scheme | Covers all observed error types: control flow (goto, unreachable), type system (mismatch), function contracts (return), variable tracking (undeclared), optimization (redundant assignments) |
| 3-tier priority system (CRITICAL/HIGH/MEDIUM) | Prioritize based on: 1) blocks compilation vs compiles-but-wrong, 2) frequency across test files, 3) fix complexity estimate |
| Focus on static errors only | Runtime semantic errors (wrong bytecode output) require successful compilation - Phase 6 focuses on getting code to compile first |

## Deviations from Plan

None - plan executed exactly as written.

**Note**: Plan anticipated automated error categorization using Phase 4's error_analyzer module, but compiler crashes prevented this. Adapted to manual inspection approach while maintaining plan objectives (identify patterns, prioritize fixes, establish baseline).

## Issues Encountered

**Issue 1: Compiler crashes instead of producing errors**
- **Problem**: SCMP.exe crashes with access violation (0xC0000005) instead of writing error files
- **Root cause**: Decompiled code is so malformed that compiler internal parser crashes
- **Impact**: Automated error categorization (Phase 4 infrastructure) cannot run
- **Resolution**: Manual source code inspection of 3 decompiled files to extract error patterns
- **Outcome**: Baseline created successfully with 6 documented patterns

**Issue 2: Partial decompilation failures**
- **Problem**: Test output shows 4/15 functions failed with AttributeError during decompilation
- **Analysis**: Separate bug in structure orchestrator (not expression reconstruction)
- **Impact**: Some functions missing from decompiled output, baseline incomplete
- **Resolution**: Documented as known limitation, focused on successfully decompiled functions
- **Follow-up**: AttributeError bug should be addressed separately (not in Phase 6 scope)

## Next Phase Readiness

**Phase 6 Plan 02 (Priority 1 fixes) - READY**
- Baseline identifies exact files to fix:
  - `vcdecomp/core/ir/structure/emit/code_emitter.py` - skip orphaned block goto emission
  - `vcdecomp/core/ir/structure/analysis/variables.py` - comprehensive variable collection
- Success criteria defined: Compiler should parse code (even if errors remain)

**Phase 6 Plan 03 (Priority 2 fixes) - READY**
- Baseline identifies type mismatch and missing return patterns
- Files to modify:
  - `vcdecomp/core/ir/stack_lifter.py` - type inference improvements
  - `vcdecomp/core/ir/expr.py` - variable type declarations
  - `vcdecomp/core/ir/structure/analysis/flow.py` - return value detection

**Blockers/Concerns:**
- Pattern 2 (type mismatches) is HIGH complexity - may require significant refactoring of stack lifter and SSA builder
- AttributeError failures in 4 functions suggest additional bugs outside Phase 6 scope
- Baseline uses manual inspection - may have missed errors that only appear during compilation (would be discovered when compiler starts parsing successfully)

---
*Phase: 06-expression-reconstruction-fixes*
*Completed: 2026-01-18*
