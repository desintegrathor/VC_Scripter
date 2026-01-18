---
phase: 06-expression-reconstruction-fixes
verified: 2026-01-18T12:00:00Z
status: gaps_found
score: 1/5 must-haves verified
gaps:
  - truth: "Decompiled expressions compile without syntax errors"
    status: failed
    reason: "Compiler crashes (0xC0000005) on all 3 test files - code too malformed to parse"
    artifacts:
      - path: ".test_artifacts_verification/test_decompilation_validation_0/test1_tt_decompiled.c"
        issue: "Line 35: goto block_3 to undefined label; Line 59: tmp5 declared as s_SC_MP_EnumPlayers but assigned float values (lines 65-66)"
    missing:
      - "Pattern 1 fix ineffective: goto block_3 still generated despite orphaned block detection"
      - "Pattern 2 (type mismatches) unfixed: variables declared with wrong types"
      - "Pattern 3 (missing returns) unfixed: int functions have bare return; statements"
      - "Pattern 5 fix ineffective: undeclared variables still missing"

  - truth: "Operator precedence is correctly preserved in expressions"
    status: uncertain
    reason: "Cannot verify - no successful compilation, no error messages about precedence"
    artifacts: []
    missing:
      - "Need compileable output to verify precedence with test cases"

  - truth: "Type casts are generated where needed for type mismatches"
    status: failed
    reason: "Type system is fundamentally broken - variables declared with wrong base types"
    artifacts:
      - path: "vcdecomp/core/ir/expr.py"
        issue: "Type inference produces wrong types (s_SC_MP_EnumPlayers instead of float)"
    missing:
      - "Fix stack_lifter.py type tracking for correct base type inference"
      - "Fix expr.py variable type declaration logic"

  - truth: "Complex expressions with multiple operators render correctly"
    status: partial
    reason: "Orphaned block detection works (logs show blocks skipped) but gotos still generated in some cases"
    artifacts:
      - path: "vcdecomp/core/ir/structure/orchestrator.py"
        issue: "Lines 763-815: orphaned check implemented but goto block_3 still in output"
    missing:
      - "Debug why orphaned check does not catch all cases"
      - "Fix timing issue - blocks may not be marked orphaned when goto generated"

  - truth: "Regression tests confirm previously-working expressions still work"
    status: verified
    reason: "Regression baseline YAML files created and capture current (failing) state"
    artifacts:
      - path: ".planning/baselines/test_validation/test_decompilation_validation_with_baseline/*.yml"
        issue: "None - baselines correctly capture compilation_succeeded: false"
    missing: []
---

# Phase 6: Expression Reconstruction Fixes Verification Report

**Phase Goal:** Expression reconstruction produces syntactically valid C code
**Verified:** 2026-01-18T12:00:00Z
**Status:** gaps_found
**Re-verification:** No - initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Decompiled expressions compile without syntax errors | X FAILED | Compiler crashes (exit code 0xC0000005) on all 3 test files. Manual inspection shows goto block_3 (undefined label), type mismatches (s_SC_MP_EnumPlayers assigned float), missing return values |
| 2 | Operator precedence is correctly preserved in expressions | ? UNCERTAIN | Cannot verify - no successful compilation, no parseable error messages to check precedence issues |
| 3 | Type casts are generated where needed for type mismatches | X FAILED | Type system broken at fundamental level - variables declared with wrong base types (struct instead of float). Type casts cannot fix incorrect base type declarations |
| 4 | Complex expressions with multiple operators render correctly | PARTIAL | Orphaned block detection implemented (logs show 19 blocks skipped in test1/tt), but goto block_3 still appears in output line 35, indicating fix incomplete |
| 5 | Regression tests confirm previously-working expressions still work | VERIFIED | 3 baseline YAML files created in .planning/baselines/test_validation/ capturing current state (compilation_succeeded: false). CI can now detect regressions |

**Score:** 1/5 truths verified (20%)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| vcdecomp/core/ir/expr.py | Fixed expression formatting | PARTIAL | File exists with original code. No fixes applied (Plan 06-02 focused on orchestrator.py and variables.py instead) |
| vcdecomp/core/ir/parenthesization.py | Corrected parenthesization logic | EXISTS (not modified) | File exists unchanged - baseline analysis found no precedence issues requiring parenthesization fixes |
| vcdecomp/core/ir/structure/orchestrator.py | Orphaned block goto prevention | SUBSTANTIVE | Lines 763-815: Multi-level orphaned target check implemented. 226 lines total. Imported by tests |
| vcdecomp/core/ir/structure/analysis/variables.py | Variable collection from expressions | SUBSTANTIVE | Lines 385-419: Regex-based &varname extraction with type inference |
| ERROR_BASELINE.md | Documented error patterns | VERIFIED | 357 lines documenting 6 error patterns with CRITICAL/HIGH/MEDIUM priority |
| FIX_RESULTS.md | Before/after fix analysis | VERIFIED | Documents 2 fixes applied with root cause analysis of why fixes were ineffective |
| PHASE_COMPLETION.md | Phase outcomes and remaining work | VERIFIED | 297 lines with comprehensive analysis, metrics tables, and Phase 7 roadmap |
| Regression baseline YAMLs | Baseline files for CI | VERIFIED | 3 files with verdict: fail, compilation_succeeded: false |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| expr.py | parenthesization.py | needs_parens calls | WIRED | grep shows needs_parens() calls exist in expr.py |
| test_validation.py | expr.py | decompilation pipeline | WIRED | Test calls decompilation which uses ExpressionFormatter |
| orchestrator.py | Orphaned block detection | is_orphaned_target flag | PARTIAL | Logic exists but goto block_3 still in output - incomplete coverage |
| variables.py | Regex extraction | re.findall | PARTIAL | Code exists but variables still undeclared - runs too late or results filtered |

### Requirements Coverage

**DECOMP-01: Expression reconstruction produces valid C syntax**

| Requirement | Status | Blocking Issue |
|-------------|--------|----------------|
| Decompiled expressions compile without syntax errors | X BLOCKED | Compiler crashes - 6 error patterns identified, 2 fixes attempted but ineffective |
| Operator precedence correctly preserved | ? NEEDS HUMAN | Cannot verify without successful compilation |
| Type casts generated where needed | X BLOCKED | Base type inference broken (Pattern 2) - casts cannot fix wrong base types |
| Complex expressions render correctly | PARTIAL | Orphaned blocks detected but some gotos still generated |
| Regression tests stable | SATISFIED | Baselines created and committed |

**Overall:** 1/5 acceptance criteria met (20%)

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| test1_tt_decompiled.c | 35 | goto block_3; (undefined label) | BLOCKER | Compiler cannot parse - crashes with 0xC0000005 |
| test1_tt_decompiled.c | 59, 65-66 | tmp5 declared s_SC_MP_EnumPlayers but assigned float | BLOCKER | Type system violation - compiler crashes |
| test1_tt_decompiled.c | 47, 69, 97, 119, 148 | return; in int functions (5 instances) | BLOCKER | Missing return values - undefined behavior |
| test1_tt_decompiled.c | Throughout | Multiple sequential assignments to same variable | WARNING | Code quality issue - SSA temporaries not optimized |

**Blocker count:** 3 distinct patterns preventing compilation (goto undefined, type mismatch, missing return)

### Human Verification Required

#### 1. Verify orphaned block detection is executing

**Test:** Add logging to orchestrator.py lines 765, 780 to print when is_orphaned_target=True
**Expected:** Log should show "Skipping goto to block_3 - orphaned" but output still has goto block_3
**Why human:** Need to trace execution to determine if check runs for block_3 or if block_3 is reached through different code path

#### 2. Verify regex variable extraction finds missing variables

**Test:** Add logging to variables.py line 396 to print all addr_of_vars found
**Expected:** Should find vec, enum_pl if they appear in expressions
**Why human:** Need to trace whether regex finds variables but they get filtered later, or regex does not find them at all

#### 3. Determine minimum pattern fixes needed for compilation

**Test:** Manually fix one pattern at a time in test1_tt_decompiled.c and try compiling
**Expected:** Find which single pattern (goto, type, return) crashes compiler first
**Why human:** Cannot automate without parseable error output - compiler crashes immediately

### Gaps Summary

**Phase 6 attempted to fix expression reconstruction bugs but achieved 0% compilation success (0/3 tests compile).**

**Root causes of failure:**

1. **Pattern 1 (undefined goto) - Fix ineffective**
   - Orphaned block detection implemented correctly in orchestrator.py (lines 763-815)
   - Logs show 19 orphaned blocks detected and skipped in test1/tt
   - BUT goto block_3 still appears in output (line 35)
   - Hypothesis: Block_3 may not be detected as orphaned when goto is generated, OR goto generated through different code path not covered by fix

2. **Pattern 5 (undeclared variables) - Fix ineffective**
   - Regex extraction implemented in variables.py (line 395)
   - Code should find &vec and &enum_pl patterns
   - BUT variables still missing from decompiled output
   - Hypothesis: Regex runs but variables filtered out by skip conditions, OR regex runs too late in pipeline

3. **Pattern 2 (type mismatches) - Not attempted**
   - High complexity requiring stack_lifter.py refactoring
   - Variables declared with wrong base types (struct instead of primitive)
   - Impact: Severe enough to crash compiler alone

4. **Pattern 3 (missing returns) - Not attempted**
   - Int functions have bare return; statements (5 instances in test1/tt)
   - Medium complexity fix
   - Impact: May crash compiler or be severe error

5. **Pattern interaction effects**
   - Multiple patterns may need fixing simultaneously
   - Compiler crashes before generating error messages
   - Cannot measure incremental progress

**What would make this phase successful:**

1. Debug existing fixes (Pattern 1 & 5) to determine why ineffective
2. Implement Pattern 3 (missing returns) as it is medium complexity
3. Begin Pattern 2 (type mismatches) investigation - may require multi-phase effort
4. Get at least 1/3 tests to compile (even with errors) to enable automated error analysis

---

_Verified: 2026-01-18T12:00:00Z_
_Verifier: Claude (gsd-verifier)_
