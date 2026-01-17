# Project Research Summary

**Project:** VC-Script-Decompiler Quality Improvement
**Domain:** Binary decompiler validation and quality assurance
**Researched:** 2026-01-17
**Confidence:** HIGH

## Executive Summary

The VC-Script-Decompiler quality improvement project addresses a well-studied problem: improving decompiler correctness and compilability. Modern research shows state-of-the-art decompilers achieve only 55% accuracy, with 15+ distinct error types across control flow, type inference, and expression formatting. The recommended approach is validation-first development: build comprehensive automated testing infrastructure before attempting fixes, use batch validation across full corpus (not just 3 test scripts), and track objective metrics (compilation rate, semantic accuracy, error distribution).

The project has strong existing foundations - recompilation testing, bytecode comparison with semantic/cosmetic categorization, and parallel batch validation are already implemented. The critical gap is automation maturity: no CI integration, no systematic error classification, and limited test corpus coverage. The stack focuses on pytest ecosystem for testing (already in use), Ruff+mypy for quality gates, and leveraging the existing custom bytecode comparison infrastructure.

Key risk is "fixing without measuring" - making decompiler changes without comprehensive regression testing leads to whack-a-mole bug fixing where fixes introduce new bugs. Mitigation: Phase 1 must establish validation infrastructure and baseline metrics before any decompiler fixes in Phase 2+. Success depends on tracking objective metrics (X% scripts compile, Y% match bytecode) rather than subjective assessment.

## Key Findings

### Recommended Stack

The stack centers on three pillars: pytest ecosystem for test automation (already achieving 100% coverage on core modules), Ruff+mypy for code quality enforcement, and the existing custom validation infrastructure. Windows-only constraint (SCMP.exe compiler) drives tool selection.

**Core technologies:**
- pytest + pytest-xdist (parallel execution) - Industry standard, batch validation needs parallelization for 100+ scripts
- pytest-cov (coverage measurement) - Maintain 100% coverage requirement on core modules
- Ruff (linting/formatting) - 10-100x faster than alternatives, replaces 6 tools (Flake8, Black, isort, pyupgrade, autoflake, pydocstyle)
- mypy (type checking) - Project has 87% type hint coverage, mypy enforces this and catches type errors Ruff misses
- pre-commit (automation) - Auto-run quality checks before commits, prevent regressions
- Custom BytecodeComparator (existing) - Domain-specific SCR format comparison with semantic vs cosmetic categorization

**Optional extensions (Phase 2+):**
- hypothesis (property-based testing) - Generate random bytecode inputs to find edge cases
- pytest-benchmark (performance tracking) - Monitor decompilation speed regressions
- inline-snapshot (snapshot testing) - Validate decompiled C output format doesn't regress

**Version compatibility:** Full stack supports Python 3.10-3.14, project runs Python 3.13.7

### Expected Features

Research reveals a clear feature hierarchy based on 2025 academic benchmarks (DecompileBench, D-Helix, FuzzFlesh) and industry tools (IDA Pro, Ghidra).

**Must have (table stakes):**
- Recompilation testing - Core validation method, compile decompiled output and verify it works (COMPLETE)
- Bytecode comparison - Section-by-section comparison of original vs recompiled SCR files (COMPLETE)
- Difference categorization - Distinguish semantic vs cosmetic vs optimization differences (COMPLETE)
- Compilation error reporting - Show why decompiled code won't compile (COMPLETE)
- Batch validation with parallelization - Test 100+ scripts concurrently (COMPLETE via --jobs flag)
- Pass/fail verdicts - Clear success/failure indication (COMPLETE)

**Should have (competitive differentiators):**
- Coverage metrics - Track % of scripts that compile successfully over time (MISSING)
- Automated regression detection - Alert when decompiler changes break previously-working scripts (PARTIAL - exists but underutilized)
- Interactive error analysis - Click difference, see original vs decompiled side-by-side (MISSING)
- CI/CD integration - Run validation in GitHub Actions on every commit (MISSING)
- Error pattern aggregation - Identify that "70% of failures involve switch/case" (MISSING)
- One-click validation in GUI - Right-click code, validate immediately (MISSING - currently 4-click workflow)

**Defer (v2+):**
- Semantic equivalence via differential fuzzing - Run both binaries with random inputs, compare outputs (HIGH complexity)
- Test oracle generation - Auto-generate test cases from SCR bytecode (Research-level, cutting edge)
- Delta visualization - Visual hex diff + disassembly diff at error location (HIGH complexity)
- Type inference quality metrics - Measure accuracy of recovered variable types (Research-level)

**Anti-features to avoid:**
- Manual diff-reading workflows - Don't force users to read bytecode hex dumps
- Undifferentiated "bytes differ" output - Always categorize semantic vs cosmetic
- Testing only with 3 scripts - Must test against full corpus (100+ scripts)
- Perfect decompilation obsession - Prioritize compilability over readability

### Architecture Approach

The recommended architecture follows a five-layer pipeline design informed by D-Helix and DecompileBench research: User Interface → Orchestration → Validation/Comparison → Analysis/Intelligence → Persistence. This separates concerns cleanly and enables caching at each stage.

**Major components:**

1. **Validation Orchestrator (EXISTING)** - Coordinates end-to-end workflow: compile decompiled.c → compare bytecode → categorize differences → verdict. Already implemented with caching support.

2. **Test Suite Manager (NEW)** - Test corpus organization, test case selection/prioritization, batch execution coordination. Enables scaling from 10 test cases to 1000+ with incremental testing and statistical analysis.

3. **Error Pattern Analyzer (NEW)** - Aggregate validation results across corpus, identify recurring patterns ("20% of failures are switch/case bugs"), classify error types. Transforms raw failures into actionable insights.

4. **Interactive Debugger Bridge (NEW)** - Map errors to source code locations, extract context (SSA graph, CFG, bytecode), generate root cause hypotheses. Reduces time from "test failed" to "root cause identified."

5. **Test Result Database (NEW)** - Historical tracking of validation runs, trend analysis, regression detection. Track metrics: pass rate over time, error type distribution, coverage improvements.

**Key patterns to follow:**
- Pipeline architecture - Linear transformation stages with clear inputs/outputs, cacheable
- Differential testing oracle - Use original SCMP.exe compiler as ground truth via recompilation
- Golden output testing - Store baselines, detect regressions immediately
- Aggregate analysis - Collect results from many tests, find systematic patterns

**Anti-patterns to avoid:**
- Tightly coupled test selection (hard-coded file paths)
- Binary pass/fail without nuance (hides semantic vs cosmetic differences)
- GUI-only workflow (prevents CI automation)
- Throwing away test history (can't track progress)

### Critical Pitfalls

Based on 2024-2025 decompiler research (D-LiFT, BIN2WRONG, FuzzFlesh) and industry experience:

1. **Fixing Without Validation Infrastructure** - Teams fix bugs by eyeballing output, discover fixes broke other scripts. Prevention: Build validation first (Phase 1), fix second (Phase 2+). Validate via recompilation + bytecode comparison + baseline tracking. Never fix without automated regression testing.

2. **Testing with Too Few Test Cases** - Working with 3 test scripts creates false confidence. State-of-the-art decompilers have 15+ error types, small test suites miss most patterns. Prevention: Batch validate ALL available scripts from day 1, track pass rate (127/200 = 63.5%), prioritize fixes by frequency.

3. **Chasing Perfect Decompilation Instead of Compilability** - Spending weeks on variable naming/formatting while code doesn't compile. Prevention: Priority hierarchy: compilability first → semantic correctness second → readability third. Variables named `local_X` are acceptable if code compiles and validates.

4. **Refactoring Before Understanding Failure Modes** - Refactoring large modules breaks working code without knowing what was broken vs working. Prevention: Bug inventory first, baseline test coverage, only refactor modules blocking specific bug fixes, incremental refactoring with validation after each step.

5. **Trusting Bytecode Comparison Without Understanding Compiler** - Assuming all bytecode differences mean decompiler bugs, when compilers have non-deterministic behavior (register allocation variance). Prevention: Categorize differences (semantic vs non-semantic), study SCMP.exe internals, accept non-semantic differences, document known compiler quirks.

**Additional critical warnings:**
- Not tracking regression baselines - Fixes introduce new bugs, discovered weeks later
- Ignoring control flow reconstruction complexity - Underestimating if/else/switch difficulty
- Expression tree refactoring without safety net - Operator precedence bugs create silent semantic errors

## Implications for Roadmap

Based on research, suggested phase structure emphasizes validation infrastructure before bug fixing:

### Phase 1: Validation Infrastructure & Baseline
**Rationale:** Cannot improve decompiler without measuring current state. Research shows 55% accuracy is state-of-the-art, but project doesn't know current pass rate. Fixes without validation lead to whack-a-mole regressions.

**Delivers:**
- Test suite manager for corpus organization
- CI/CD integration (GitHub Actions)
- Baseline validation results across ALL test scripts
- Coverage metrics dashboard (X% compile, Y% validate)
- Regression detection in CI

**Addresses (from FEATURES.md):**
- Coverage metrics (measure % scripts that compile)
- CI/CD integration (prevent regressions)
- Baseline tracking (detect when changes break working code)

**Avoids (from PITFALLS.md):**
- Fixing without validation infrastructure (Pitfall 1)
- Testing with too few test cases (Pitfall 2)
- Not tracking regression baselines (Pitfall 6)

**Uses (from STACK.md):**
- pytest + pytest-xdist for parallel batch testing
- pytest-html for test reports
- pre-commit for automation

**Research needed:** LOW - CI/CD patterns are well-established, batch testing is standard

### Phase 2: Error Classification & Pattern Analysis
**Rationale:** With baseline established, need to understand what's broken systematically. Research shows 15+ error types (control flow, type inference, expression formatting). Aggregate analysis reveals patterns - fix one root cause, 20 tests pass.

**Delivers:**
- Error pattern analyzer (aggregates failures across corpus)
- Bug taxonomy (classify errors: syntax, semantic, control flow, types)
- Prioritized bug list (sorted by frequency - impact)
- Automated pattern detection ("70% of failures involve switch/case")

**Addresses (from FEATURES.md):**
- Error pattern aggregation
- Automated bug classification

**Avoids (from PITFALLS.md):**
- Manual error investigation that doesn't scale (Pitfall 4 anti-pattern)
- Refactoring before understanding failure modes (Pitfall 4)

**Research needed:** MEDIUM - Error categorization heuristics are domain-specific to VC scripts

### Phase 3: Core Decompiler Fixes (Compilability)
**Rationale:** With validation infrastructure and error classification in place, can safely fix bugs. Priority: get code to compile (not perfect, just compilable). Research shows compilation success is first gate before semantic correctness.

**Delivers:**
- Fix top 5 error patterns by frequency
- Compilation success rate improvement (target: 0% → 50%+)
- Regression-free bug fixes (validated via Phase 1 infrastructure)

**Addresses (from FEATURES.md):**
- Compilation error reporting improvements
- Table stakes features (code that compiles)

**Avoids (from PITFALLS.md):**
- Chasing perfect decompilation instead of compilability (Pitfall 3)
- Expression tree refactoring without safety net (Pitfall 9)

**Uses (from ARCHITECTURE.md):**
- Validation orchestrator for testing each fix
- Regression baseline to ensure no backsliding

**Research needed:** MEDIUM-HIGH - Control flow reconstruction is complex, may need pattern-independent structuring research

### Phase 4: Semantic Correctness (Bytecode Equivalence)
**Rationale:** Code compiles, but does it match original bytecode? Research shows bytecode comparison catches semantic bugs. Categorization (semantic vs cosmetic) is critical - not all differences are bugs.

**Delivers:**
- Refined difference categorization
- Semantic accuracy rate improvement (target: 70%+ of compiled scripts match bytecode)
- Interactive debugger bridge (click error → see source location)

**Addresses (from FEATURES.md):**
- Interactive error analysis
- Delta visualization (basic)

**Avoids (from PITFALLS.md):**
- Trusting bytecode comparison without understanding compiler (Pitfall 5)

**Uses (from STACK.md):**
- Custom BytecodeComparator refinement
- Debugging tools (ipdb integration)

**Research needed:** MEDIUM - SCMP.exe compiler quirks need empirical documentation

### Phase 5: Automation & Developer Experience
**Rationale:** Decompiler works reliably, now optimize workflow. Research shows validation should be frictionless - one-click in GUI, fast batch mode, clear reports.

**Delivers:**
- One-click GUI validation
- Validation speed optimization (100 scripts in <30s)
- Enhanced HTML reports with visual diffs
- pytest-watcher for continuous testing during development

**Addresses (from FEATURES.md):**
- One-click validation in GUI
- Interactive error analysis enhancements

**Uses (from STACK.md):**
- pytest-watcher for file watching
- Enhanced reporting tools

**Research needed:** LOW - Developer UX patterns are well-understood

### Phase 6: Advanced Testing (Optional)
**Rationale:** For research-grade validation. Decompiler works, but can we prove semantic equivalence formally?

**Delivers:**
- Property-based testing with hypothesis
- Differential fuzzing (run original vs recompiled with random inputs)
- Performance benchmarking suite
- Snapshot testing for output format

**Addresses (from FEATURES.md):**
- Semantic equivalence via differential testing
- Test oracle generation (if feasible)

**Uses (from STACK.md):**
- hypothesis for property-based testing
- pytest-benchmark for performance tracking

**Research needed:** HIGH - Semantic equivalence testing requires symbolic execution or fuzzing infrastructure

### Phase Ordering Rationale

**Why this order:**
1. **Validation before fixes** - Cannot improve what you don't measure. Phase 1 establishes measurement infrastructure.
2. **Understanding before action** - Phase 2 classifies errors systematically, avoiding random bug fixing.
3. **Compilability before correctness** - Phase 3 gets code to compile (necessary condition), Phase 4 ensures correctness (sufficient condition).
4. **Reliability before UX** - Phase 5 enhances workflow after core decompiler is stable.
5. **Foundation before advanced** - Phase 6 research-level features require stable Phases 1-5.

**How this avoids pitfalls:**
- Phases 1-2 prevent "fixing without validation" (Pitfall 1)
- Phase 1 batch validation prevents "too few test cases" (Pitfall 2)
- Phase 3-4 ordering prevents "chasing perfection before compilation" (Pitfall 3)
- Phase 2 prevents "refactoring before understanding failures" (Pitfall 4)

**Dependency structure:**
```
Phase 1 (Validation Infrastructure)
  ├── Phase 2 (Error Classification) - needs baseline data
  │     └── Phase 3 (Compilability Fixes) - needs prioritized bug list
  │           └── Phase 4 (Semantic Correctness) - needs compiling code
  │                 └── Phase 5 (Developer UX) - needs stable decompiler
  │                       └── Phase 6 (Advanced Testing) - optional
  └── Phase 5 (parallel track - can start after Phase 1)
```

### Research Flags

**Phases likely needing deeper research during planning:**

- **Phase 3 (Control Flow Fixes):** Control flow reconstruction is one of the hardest decompiler problems (NDSS 2017 "No More Gotos"). May need research on pattern-independent structuring, dominance trees, natural loop detection. Switch/case jump table detection has multiple variants.

- **Phase 4 (Compiler Quirks):** SCMP.exe has undocumented behavior. Need empirical testing to discover edge cases, non-deterministic outputs, optimization artifacts. Document what differences are acceptable.

- **Phase 6 (Semantic Equivalence):** Cutting-edge research territory. Differential fuzzing requires test execution infrastructure, symbolic execution is complex. Consider deferring unless critical.

**Phases with standard patterns (skip research-phase):**

- **Phase 1 (CI/CD Integration):** Well-documented patterns, GitHub Actions templates available. pytest integration is standard.

- **Phase 2 (Error Classification):** Aggregate analysis patterns are well-understood. Error taxonomy is project-specific but methodology is standard.

- **Phase 5 (Developer UX):** One-click validation, file watching, progress bars are solved problems with established patterns.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All versions verified from PyPI/GitHub (Jan 2026), tools are mature and widely adopted |
| Features | HIGH | Based on 2025 academic research (DecompileBench, D-Helix, FuzzFlesh), industry consensus |
| Architecture | HIGH | D-Helix USENIX 2024 paper provides validated testing framework architecture, patterns are proven |
| Pitfalls | HIGH | 7 academic papers (2024-2025) documenting decompiler bugs, testing failures, accuracy limitations |

**Overall confidence:** HIGH

Research is grounded in recent academic literature (2024-2025), official tool documentation, and industry tools. The domain (decompiler validation) is well-studied with established best practices.

### Gaps to Address

**Gap 1: SCMP.exe compiler internals**
- **What's unknown:** Exact optimization behavior, non-deterministic patterns, what bytecode differences are compiler variance vs decompiler bugs
- **How to handle:** Empirical testing during Phase 4. Document compiler quirks as discovered. Study SCC_TECHNICAL_ANALYSIS.md already in repo.

**Gap 2: Optimal difference categorization**
- **What's unknown:** Current 4 categories (SEMANTIC, COSMETIC, OPTIMIZATION, UNKNOWN) may need refinement based on VC-specific patterns. Research shows 15 error types exist.
- **How to handle:** Start with existing categorization (already well-designed), refine during Phase 2 error classification based on empirical data.

**Gap 3: Test corpus coverage**
- **What's unknown:** Project has Compiler-testruns (with source) and script-folders (production), but unknown how many total scripts exist, what patterns they cover
- **How to handle:** Phase 1 should inventory full test corpus, classify by complexity/type, ensure stratified sampling.

**Gap 4: Scalability at 1000+ scripts**
- **What's unknown:** Batch validation performance at scale, whether caching is sufficient
- **How to handle:** Start with current corpus size (likely 100-200 scripts), optimize if Phase 1 reveals performance issues.

**Gap 5: Advanced testing feasibility**
- **What's unknown:** Whether differential fuzzing or symbolic execution are practical for VC scripts (simpler language than C, may be easier)
- **How to handle:** Defer to Phase 6 (optional), research during planning if stakeholder requests it.

## Sources

### Primary (HIGH confidence)

**Decompiler Research (2024-2025):**
- [DecompileBench: Comprehensive Benchmark](https://arxiv.org/html/2505.11340v1) - 23,400 functions, 3D evaluation framework, 15 error types
- [D-Helix: Generic Testing Framework](https://www.usenix.org/conference/usenixsecurity24/presentation/zou) - USENIX Security 2024, testing architecture
- [FuzzFlesh: Randomised Testing](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2025.13) - CFG-based testing, switch/loop bugs
- [Evaluating Decompiler Effectiveness](https://dl.acm.org/doi/10.1145/3650212.3652144) - ISSTA 2024, 55% accuracy finding
- [Understanding Java Decompiler Bugs](https://dl.acm.org/doi/10.1145/3649860) - OOPSLA 2024, bug taxonomy

**Tool Documentation:**
- [pytest 9.1.0 Documentation](https://docs.pytest.org) - Released Jan 2026
- [Ruff 0.14.13 Documentation](https://docs.astral.sh/ruff/) - Released Jan 15, 2026
- [mypy 1.19.1 Documentation](https://mypy.readthedocs.io/) - Released Dec 15, 2025
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/) - Parallel execution patterns

### Secondary (MEDIUM confidence)

**Validation Methodology:**
- [Semantic Equivalence for HHVM Bytecode](https://www.semanticscholar.org/paper/Semantic-Equivalence-Checking-for-HHVM-Bytecode-Benton/fd8d33963b6a0cecdf3f0c4140855363acd8d431) - Bytecode comparison patterns
- [Compiler Optimization Testing](https://arxiv.org/html/2504.04321v1) - Metamorphic testing, EMI variants
- [Test Automation Architecture 2025](https://www.testwheel.com/blog/test-automation-architecture/) - Modern patterns

**Control Flow Reconstruction:**
- [No More Gotos](https://www.ndss-symposium.org/wp-content/uploads/2017/09/11_4_2.pdf) - NDSS 2017, pattern-independent structuring
- [Recovering Control Flow Without CFGs](https://purplesyringa.moe/blog/recovering-control-flow-structures-without-cfgs/) - Modern approaches

### Tertiary (LOW confidence, project-specific)

**VC_Scripter Codebase:**
- CLAUDE.md - Project documentation, constraints
- vcdecomp/validation/ - Existing validation infrastructure
- docs/SCC_TECHNICAL_ANALYSIS.md - Compiler internals (already in repo)
- Compiler-testruns/ - Test scripts with source

---
*Research completed: 2026-01-17*
*Ready for roadmap: YES*
