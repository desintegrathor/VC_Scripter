# Requirements: VC-Script-Decompiler Quality Improvement

**Defined:** 2026-01-17
**Core Value:** Decompiled C code must compile successfully with the original SCMP.exe compiler

## v1 Requirements

Requirements for systematically improving decompiler from "broken output" to "compilable, validated C code"

### Validation Infrastructure

- [ ] **VALID-01**: User can click "Compile" button in GUI to validate currently-open script
- [ ] **VALID-02**: Compilation failures show .err file content in GUI
- [ ] **VALID-03**: Compilation successes show bytecode comparison results in GUI
- [ ] **VALID-04**: System tracks compilation success rate over time (coverage metrics)
- [ ] **VALID-05**: CI/CD pipeline runs validation on all commits (GitHub Actions)
- [ ] **VALID-06**: Regression detection alerts when previously-passing scripts fail
- [ ] **VALID-07**: Validation reports export to HTML/JSON with full details

### Test Suite Automation

- [ ] **TEST-01**: Automated test suite runs decompilation on all test cases
- [ ] **TEST-02**: Test suite validates each decompiled output compiles
- [ ] **TEST-03**: Test suite compares bytecode for semantic equivalence
- [ ] **TEST-04**: Test suite categorizes failures by error type
- [ ] **TEST-05**: Test corpus expands beyond 3 current test cases to 10+ cases
- [ ] **TEST-06**: Test results persist as baseline for regression detection
- [ ] **TEST-07**: pytest integration allows running `pytest vcdecomp/tests/test_validation.py`

### Error Analysis & Classification

- [ ] **ERROR-01**: Compilation errors parsed and categorized (syntax, type, semantic)
- [ ] **ERROR-02**: Error patterns identified and aggregated ("70% are switch/case bugs")
- [ ] **ERROR-03**: Interactive error viewer shows original .asm vs decompiled .c side-by-side
- [ ] **ERROR-04**: Bytecode differences highlighted at instruction level
- [ ] **ERROR-05**: Failed test cases logged with reproducible steps

### Core Decompiler Fixes

- [ ] **DECOMP-01**: Expression reconstruction produces valid C syntax (no syntax errors)
- [ ] **DECOMP-02**: Variable declarations generated correctly (locals, globals, arrays)
- [ ] **DECOMP-03**: Type inference produces correct C types (int, float, struct) instead of `dword`
- [ ] **DECOMP-04**: Function signatures detected with correct parameter names
- [ ] **DECOMP-05**: Control flow patterns (if/else, switch, loops) emit valid C code
- [ ] **DECOMP-06**: Struct field access reconstructed correctly
- [ ] **DECOMP-07**: Array indexing generates bounds-correct code

### Quality Metrics & Tracking

- [ ] **METRIC-01**: Dashboard shows compilation success rate (% of scripts that compile)
- [ ] **METRIC-02**: Dashboard shows semantic equivalence rate (% matching bytecode)
- [ ] **METRIC-03**: Trend graphs track progress over time
- [ ] **METRIC-04**: Per-error-type frequency counts guide fix prioritization
- [ ] **METRIC-05**: Test coverage reports show which patterns are tested

## v2 Requirements

Deferred to future milestones after achieving compilable output.

### Advanced Validation

- **VALID-ADV-01**: Semantic equivalence testing via differential fuzzing
- **VALID-ADV-02**: Symbolic execution for behavior verification
- **VALID-ADV-03**: CFG-based validation (control flow graph comparison)
- **VALID-ADV-04**: Performance benchmarking (decompilation speed tracking)

### Developer Experience

- **DX-01**: Interactive debugger for decompilation pipeline stages
- **DX-02**: Hot-reload for testing decompiler changes
- **DX-03**: VS Code extension for syntax highlighting of .scr files
- **DX-04**: Decompiler plugin API for custom passes

### Code Quality

- **QUALITY-01**: Readability scoring (LLM-as-judge evaluation)
- **QUALITY-02**: Identifier naming improvements (meaningful variable names)
- **QUALITY-03**: Comment generation from bytecode patterns
- **QUALITY-04**: Code formatting to match original style

## Out of Scope

Explicitly excluded to maintain focus on core value.

| Feature | Reason |
|---------|--------|
| Decompiler rewrite from scratch | Existing architecture is sound, fix incrementally |
| Cross-platform validation (Linux/Mac) | Original compiler is Windows-only, Wine support deferred |
| Symbol table integration from .dbg files | Compilability first, then readability improvements |
| Advanced type inference from usage patterns | Basic types sufficient for v1 |
| Optimization of decompiled code | Correctness before optimization |
| Multi-language support | VC scripts only (C-like language) |
| Real-time decompilation in game | Offline tool only |
| Decompiler web service/API | Desktop GUI sufficient |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| VALID-01 | Phase 1 | Pending |
| VALID-02 | Phase 1 | Pending |
| VALID-03 | Phase 1 | Pending |
| VALID-04 | Phase 5 | Pending |
| VALID-05 | Phase 3 | Pending |
| VALID-06 | Phase 3 | Pending |
| VALID-07 | Phase 9 | Pending |
| TEST-01 | Phase 2 | Pending |
| TEST-02 | Phase 2 | Pending |
| TEST-03 | Phase 2 | Pending |
| TEST-04 | Phase 2 | Pending |
| TEST-05 | Phase 9 | Pending |
| TEST-06 | Phase 3 | Pending |
| TEST-07 | Phase 2 | Pending |
| ERROR-01 | Phase 4 | Pending |
| ERROR-02 | Phase 4 | Pending |
| ERROR-03 | Phase 4 | Pending |
| ERROR-04 | Phase 4 | Pending |
| ERROR-05 | Phase 4 | Pending |
| DECOMP-01 | Phase 6 | Pending |
| DECOMP-02 | Phase 7 | Pending |
| DECOMP-03 | Phase 7 | Pending |
| DECOMP-04 | Phase 7 | Pending |
| DECOMP-05 | Phase 8 | Pending |
| DECOMP-06 | Phase 7 | Pending |
| DECOMP-07 | Phase 7 | Pending |
| METRIC-01 | Phase 5 | Pending |
| METRIC-02 | Phase 5 | Pending |
| METRIC-03 | Phase 5 | Pending |
| METRIC-04 | Phase 5 | Pending |
| METRIC-05 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 32 total
- Mapped to phases: 32
- Unmapped: 0

---
*Requirements defined: 2026-01-17*
*Last updated: 2026-01-17 after roadmap creation*
