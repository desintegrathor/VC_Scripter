# Roadmap: VC-Script-Decompiler Quality Improvement

## Overview

This roadmap transforms the VC-Script-Decompiler from producing broken output to generating compilable, validated C code. The journey starts by establishing automated validation infrastructure and test suites to measure current state, then systematically classifying errors to understand what's broken, tracking metrics to guide prioritization, and finally fixing the core decompiler bugs that prevent compilation. Each phase delivers measurable progress toward the core goal: decompiled code that compiles successfully with SCMP.exe.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: GUI Validation Integration** - One-click compile button in GUI
- [x] **Phase 2: Test Suite Automation** - Automated test suite with pytest integration
- [x] **Phase 3: CI/CD Pipeline** - Continuous integration with regression detection
- [x] **Phase 4: Error Analysis System** - Systematic error classification and pattern detection
- [ ] **Phase 5: Metrics Dashboard** - Progress tracking and compilation rate monitoring
- [x] **Phase 6: Expression Reconstruction Fixes** - Fix syntax errors in expression generation
- [ ] **Phase 7: Variable Declaration Fixes** - Correct variable and type declaration generation
- [ ] **Phase 8: Control Flow Fixes** - Fix if/else, switch, loop code emission
- [ ] **Phase 9: Validation Reporting** - Enhanced HTML/JSON reporting with detailed analysis

## Phase Details

### Phase 1: GUI Validation Integration
**Goal**: User can validate scripts directly from GUI with one click
**Depends on**: Nothing (first phase)
**Requirements**: VALID-01, VALID-02, VALID-03
**Success Criteria** (what must be TRUE):
  1. User can click "Compile" button in GUI to validate currently-open script
  2. Compilation failures show .err file content in GUI with clear error messages
  3. Compilation successes show bytecode comparison results in GUI with match/diff details
  4. Validation runs against decompiler output directly without requiring file save
**Status**: COMPLETE
**Plans**: 2 plans

Plans:
- [x] 01-01-PLAN.md — Validation Menu and Trigger Implementation
- [x] 01-02-PLAN.md — Settings Integration and End-to-End Testing

### Phase 2: Test Suite Automation
**Goal**: Automated test suite validates all test cases with pytest integration
**Depends on**: Nothing (parallel with Phase 1)
**Requirements**: TEST-01, TEST-02, TEST-03, TEST-04, TEST-07
**Success Criteria** (what must be TRUE):
  1. Test suite runs decompilation on all test cases automatically
  2. Test suite validates each decompiled output compiles successfully
  3. Test suite compares bytecode and reports semantic equivalence
  4. Test suite categorizes failures by error type (syntax, semantic, control flow)
  5. Developer can run `pytest vcdecomp/tests/test_validation.py` to validate entire suite
**Status**: COMPLETE
**Plans**: 1 plan

Plans:
- [x] 02-01-PLAN.md — Pytest validation test suite with parametrization

### Phase 3: CI/CD Pipeline
**Goal**: Every commit is automatically validated with regression detection
**Depends on**: Phase 2
**Requirements**: VALID-05, VALID-06, TEST-06
**Success Criteria** (what must be TRUE):
  1. GitHub Actions runs validation suite on every commit
  2. CI pipeline alerts when previously-passing scripts fail
  3. Test results persist as baseline for regression comparison
  4. Pull requests show validation status before merge
**Status**: COMPLETE
**Plans**: 3 plans

Plans:
- [x] 03-01-PLAN.md — Self-hosted Windows runner configuration
- [x] 03-02-PLAN.md — CI pipeline implementation with pytest integration
- [x] 03-03-PLAN.md — Branch protection and end-to-end integration testing

### Phase 4: Error Analysis System
**Goal**: Errors are systematically classified with pattern detection
**Depends on**: Phase 2
**Requirements**: ERROR-01, ERROR-02, ERROR-03, ERROR-04, ERROR-05
**Success Criteria** (what must be TRUE):
  1. Compilation errors are automatically parsed and categorized (syntax, type, semantic)
  2. Error patterns are identified and aggregated (e.g., "70% are switch/case bugs")
  3. Interactive error viewer shows original .asm vs decompiled .c side-by-side
  4. Bytecode differences are highlighted at instruction level
  5. Failed test cases are logged with reproducible steps for investigation
**Status**: COMPLETE
**Plans**: 3 plans

Plans:
- [x] 04-01-PLAN.md — Error Categorization Module with Pattern Aggregation
- [x] 04-02-PLAN.md — Error Analysis GUI with Hierarchical Tree Display
- [x] 04-03-PLAN.md — Side-by-Side Diff Viewer and Test Failure Logging

### Phase 5: Metrics Dashboard
**Goal**: Compilation success rate and trends are tracked over time
**Depends on**: Phase 2, Phase 4
**Requirements**: VALID-04, METRIC-01, METRIC-02, METRIC-03, METRIC-04, METRIC-05
**Success Criteria** (what must be TRUE):
  1. Dashboard shows compilation success rate (percentage of scripts that compile)
  2. Dashboard shows semantic equivalence rate (percentage matching bytecode)
  3. Trend graphs track progress over time across multiple validation runs
  4. Per-error-type frequency counts guide fix prioritization decisions
  5. Test coverage reports show which control flow patterns are tested
**Plans**: TBD

Plans:
- [ ] 05-01: TBD during planning

### Phase 6: Expression Reconstruction Fixes
**Goal**: Expression reconstruction produces syntactically valid C code
**Depends on**: Phase 4, Phase 5
**Requirements**: DECOMP-01
**Success Criteria** (what must be TRUE):
  1. Decompiled expressions compile without syntax errors
  2. Operator precedence is correctly preserved in expressions
  3. Type casts are generated where needed for type mismatches
  4. Complex expressions with multiple operators render correctly
  5. Regression tests confirm previously-working expressions still work
**Status**: PARTIAL (2/5 success criteria verified, Pattern 2 deferred to Phase 7)
**Plans**: 7 plans complete
**Verification**: .planning/phases/06-expression-reconstruction-fixes/06-VERIFICATION.md

Plans:
- [x] 06-01-PLAN.md — Baseline Error Analysis
- [x] 06-02-PLAN.md — Fix High-Priority Expression Bugs
- [x] 06-03-PLAN.md — Regression Validation
- [x] 06-04-PLAN.md — Debug Ineffective Fixes (Patterns 1 & 5)
- [x] 06-05-PLAN.md — Pattern 3 Fix and Corrected Fixes
- [x] 06-06a-PLAN.md — Pattern 1 Diagnosis (orphaned block detection)
- [x] 06-06b-PLAN.md — Pattern 1 Fix and Validation

### Phase 7: Variable Declaration Fixes
**Goal**: Variables are declared correctly with proper types and scoping
**Depends on**: Phase 4, Phase 5
**Requirements**: DECOMP-02, DECOMP-03, DECOMP-04, DECOMP-06, DECOMP-07
**Success Criteria** (what must be TRUE):
  1. Local variables are declared with correct types (not generic `dword`)
  2. Global variables are identified and declared properly
  3. Arrays are declared with correct dimensions and types
  4. Struct field access reconstructs member names correctly
  5. Function parameters have correct types and names in signatures
**Plans**: 7 plans

Plans:
- [ ] 07-01-PLAN.md — Stack Lifter and Type Inference Integration
- [ ] 07-02-PLAN.md — Variable Declaration with Refined Types
- [ ] 07-03-PLAN.md — Global Variable Detection and Naming
- [ ] 07-04-PLAN.md — Array Dimension Reconstruction
- [ ] 07-05-PLAN.md — Struct Field Access Reconstruction
- [ ] 07-06a-PLAN.md — Function Signature Reconstruction
- [ ] 07-06b-PLAN.md — Phase 7 Complete Validation

### Phase 8: Control Flow Fixes
**Goal**: Control flow patterns emit compilable, correct C code
**Depends on**: Phase 4, Phase 5, Phase 6, Phase 7
**Requirements**: DECOMP-05
**Success Criteria** (what must be TRUE):
  1. If/else statements generate syntactically valid C code
  2. Switch/case statements with jump tables decompile correctly
  3. For/while loops emit correct initialization, condition, and increment
  4. Early returns and break/continue statements are placed correctly
  5. Nested control flow (loops in conditionals) generates proper bracing
**Plans**: TBD

Plans:
- [ ] 08-01: TBD during planning

### Phase 9: Validation Reporting
**Goal**: Validation results export to detailed HTML/JSON reports
**Depends on**: Phase 3, Phase 4, Phase 5
**Requirements**: VALID-07, TEST-05
**Success Criteria** (what must be TRUE):
  1. Validation reports export to HTML with syntax highlighting
  2. Reports export to HTML with syntax highlighting
  3. Reports export to JSON for programmatic analysis
  4. Reports include full bytecode comparison details
  5. Test corpus expands beyond 3 test cases to 10+ comprehensive cases
  6. Reports are readable and actionable for debugging decompiler issues
**Plans**: TBD

Plans:
- [ ] 09-01: TBD during planning

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. GUI Validation Integration | 2/2 | Complete | 2026-01-17 |
| 2. Test Suite Automation | 1/1 | Complete | 2026-01-17 |
| 3. CI/CD Pipeline | 3/3 | Complete | 2026-01-18 |
| 4. Error Analysis System | 3/3 | Complete | 2026-01-18 |
| 5. Metrics Dashboard | 0/TBD | Skipped | - |
| 6. Expression Reconstruction Fixes | 7/7 | Partial | 2026-01-18 |
| 7. Variable Declaration Fixes | 0/6 | Not started | - |
| 8. Control Flow Fixes | 0/TBD | Not started | - |
| 9. Validation Reporting | 0/TBD | Not started | - |
