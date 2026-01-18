---
phase: 07-variable-declaration-fixes
plan: 06b
type: execute
wave: 6
depends_on: [07-01, 07-02, 07-03, 07-04, 07-05, 07-06a]
files_modified:
  - vcdecomp/tests/test_validation.py
autonomous: false

must_haves:
  truths:
    - "Phase 7 validation completed across all test cases"
    - "Pattern 2 type mismatch reduction measured and documented"
    - "Compilation status improved vs Phase 6 baseline"
  artifacts:
    - path: ".test_artifacts_07-06b/PHASE7_COMPLETE.md"
      provides: "Comprehensive validation report"
      contains: "success_criteria"
  key_links:
    - from: "All Phase 7 plans"
      to: "Final validation"
      via: "End-to-end compilation test"
      pattern: "SCMP\\.exe.*test[123]"
---

<objective>
Validate complete variable declaration fixes end-to-end with manual verification.

Purpose: Plans 07-01 through 07-06a implement all variable declaration improvements. This plan validates the complete phase with compilation tests and manual verification of success criteria.

Output: PHASE7_COMPLETE.md report showing measurable progress across all 5 Phase 7 requirements.
</objective>

<execution_context>
@C:\Users\flori\.claude\get-shit-done\workflows\execute-plan.md
@C:\Users\flori\.claude\get-shit-done\templates\summary.md
</execution_context>

<context>
@C:\Users\flori\source\repos\VC_Scripter\.planning\PROJECT.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\ROADMAP.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\STATE.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-CONTEXT.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-RESEARCH.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-01-SUMMARY.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-02-SUMMARY.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-03-SUMMARY.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-04-SUMMARY.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-05-SUMMARY.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-06a-SUMMARY.md
</context>

<tasks>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Complete Phase 7 variable declaration improvements (Plans 07-01 through 07-06a)</what-built>
  <how-to-verify>
## Automated Validation Steps

1. Run full decompilation on test1/test2/test3:
   ```bash
   python -m vcdecomp structure test1.scr > .test_artifacts_07-06b/test1_complete.c
   python -m vcdecomp structure test2.scr > .test_artifacts_07-06b/test2_complete.c
   python -m vcdecomp structure test3.scr > .test_artifacts_07-06b/test3_complete.c
   ```

2. Attempt compilation with SCMP.exe:
   ```bash
   cd vcdecomp/compiler
   scmp.exe ../../.test_artifacts_07-06b/test1_complete.c test1_compiled.scr inc/sc_def.h
   # Capture exit code and .err files
   ```

3. Create comprehensive validation report: `.test_artifacts_07-06b/PHASE7_COMPLETE.md`

## Manual Verification Checklist

**Test1 Results:**
- [ ] Function signatures show semantic types (not "int func_XXXX(int param_0)")
- [ ] save_info parameter names appear in output
- [ ] Local variables have correct types (float for FADD, int for IADD)
- [ ] Pattern 2 instances (ERROR_BASELINE.md lines 59-94) reduced
- [ ] Global variables named from save_info or SGI constants
- [ ] Array declarations with dimensions (if any arrays present)
- [ ] Struct field access uses member names (if any structs present)

**Test2 Results:**
- [ ] Same checks as Test1
- [ ] Cross-reference with ERROR_BASELINE.md examples

**Test3 Results:**
- [ ] Same checks as Test1
- [ ] Verify Pattern 2 line 84 fix: `*tmp = -20000.0f` has correct pointer type

**Compilation Status:**
- [ ] Record exit codes for all three tests
- [ ] Count errors in .err files (if generated)
- [ ] Compare error count vs ERROR_BASELINE.md (Phase 6 baseline)
- [ ] Document improvement percentage

**Success Criteria Assessment:**
Check ROADMAP.md Phase 7 success criteria:
1. [ ] Local variables: refined types (not generic dword) - VERIFIED
2. [ ] Global variables: identified and named - VERIFIED
3. [ ] Arrays: correct dimensions - VERIFIED
4. [ ] Struct fields: member names reconstructed - VERIFIED
5. [ ] Function params: correct types and names - VERIFIED

**Pattern Resolution:**
From ERROR_BASELINE.md:
- Pattern 1 (goto undefined): [Phase 6 - complete]
- Pattern 2 (type mismatch): **[Phase 7 - Target for resolution]**
- Pattern 3 (missing return): [Deferred to Phase 8]
- Pattern 4 (sequential assigns): May be arrays now (check Plan 07-04 results)
- Pattern 5 (invalid cast): [Phase 6 - complete]

## Expected Outputs

1. Decompiled C files in .test_artifacts_07-06b/
2. Compilation results (exit codes, .err files if crashes)
3. PHASE7_COMPLETE.md with:
   - Before/after comparisons for all 5 success criteria
   - Compilation status table
   - Pattern resolution status
   - Improvement percentage vs ERROR_BASELINE.md
  </how-to-verify>
  <resume-signal>
Type "approved" if all success criteria verified, or describe issues found.
  </resume-signal>
</task>

</tasks>

<verification>
Overall phase checks:

1. All Phase 7 plans (07-01 through 07-06a) completed successfully
2. Test1/test2/test3 decompiled with all improvements applied
3. Compilation attempted with results documented
4. Success criteria measured against ROADMAP.md requirements
5. Pattern 2 reduction quantified vs ERROR_BASELINE.md
</verification>

<success_criteria>
Measurable completion:

1. PHASE7_COMPLETE.md exists with comprehensive validation results
2. All 5 Phase 7 success criteria assessed (verified or documented as partial)
3. Compilation results show improvement vs ERROR_BASELINE.md
4. Pattern 2 type mismatch instances reduced (measured reduction %)
5. Manual verification completed and approved by user
</success_criteria>

<output>
After completion, create `.planning/phases/07-variable-declaration-fixes/07-06b-SUMMARY.md`
</output>
