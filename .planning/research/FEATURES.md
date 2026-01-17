# Feature Landscape: Decompiler Quality & Validation Systems

**Domain:** Binary decompiler validation and quality assurance
**Researched:** 2026-01-17
**Confidence:** HIGH (based on 2025 academic research and industry tools)

## Executive Summary

Modern decompiler validation systems have evolved from simple "does it compile?" checks to sophisticated multi-dimensional quality frameworks. The 2025 research landscape reveals a clear hierarchy:

**Table stakes:** Recompilation testing, bytecode comparison, basic error reporting
**Differentiators:** Semantic equivalence testing, automated regression detection, interactive error analysis
**Anti-features:** Manual diff-reading workflows, undifferentiated "bytes differ" output, slow validation loops

VC_Scripter currently has strong table stakes (recompilation + bytecode compare + categorization), but lacks automation maturity (CI integration, batch regression, delta visualization).

---

## Table Stakes

Features users expect in any decompiler validation system. Missing = system feels incomplete.

| Feature | Why Expected | Complexity | Current State | Notes |
|---------|--------------|------------|---------------|-------|
| **Recompilation Testing** | Core validation method - compile decompiled output and verify it works | Low | ✅ COMPLETE | Via SCMP.exe wrapper, standard approach |
| **Bytecode Comparison** | Verify semantic equivalence by comparing binary outputs | Medium | ✅ COMPLETE | Section-by-section comparison (header, data, code, XFN) |
| **Difference Categorization** | Distinguish semantic vs cosmetic differences | Medium | ✅ COMPLETE | 4 categories: SEMANTIC, COSMETIC, OPTIMIZATION, UNKNOWN |
| **Compilation Error Reporting** | Show *why* decompiled code won't compile | Low | ✅ COMPLETE | Captures stdout/stderr from compiler |
| **Single-File Validation** | Validate one script at a time interactively | Low | ✅ COMPLETE | CLI and GUI both support |
| **Progress Feedback** | Show validation is working, not frozen | Low | ✅ COMPLETE | GUI has progress bar, CLI has logging |
| **Pass/Fail Verdict** | Clear success/failure indication | Low | ✅ COMPLETE | 4 verdicts: PASS, PARTIAL, FAIL, ERROR |
| **Basic Reporting** | Export results for later analysis | Low | ✅ PARTIAL | HTML/JSON export exists, needs templates |

### Feature Dependencies

```
Recompilation Testing
  └─> Compilation Error Reporting (if compilation fails)
  └─> Bytecode Comparison (if compilation succeeds)
        └─> Difference Categorization
              └─> Pass/Fail Verdict
                    └─> Basic Reporting
```

---

## Differentiators

Features that set validation systems apart. Not expected, but highly valued.

| Feature | Value Proposition | Complexity | Current State | Notes |
|---------|-------------------|------------|---------------|-------|
| **Semantic Equivalence Testing** | Verify behavior, not just bytecode - run tests to confirm identical output | High | ❌ MISSING | 2025 SOTA: differential fuzzing, symbolic execution |
| **Automated Regression Testing** | Detect when decompiler changes break previously-working scripts | Medium | ✅ PARTIAL | `validate-batch --regression` exists but underutilized |
| **Interactive Error Analysis** | Click difference → see original vs decompiled side-by-side | Medium | ❌ MISSING | Current: tree view only, no diff viewer |
| **Delta Visualization** | Visual diff of bytecode/instructions at difference location | High | ❌ MISSING | SOTA tools: hex diff, disassembly diff, CFG diff |
| **Test Oracle Generation** | Auto-generate test inputs to verify behavior | High | ❌ MISSING | 2025 research: LLM-based oracle generation showing 10-20% improvement |
| **Coverage Metrics** | Track % of bytecode/instruction types successfully decompiled | Medium | ❌ MISSING | "73% of scripts compile" more actionable than "27 scripts work" |
| **Benchmark Suite** | Standard set of test cases measuring decompiler quality | Medium | ✅ PARTIAL | 3 test cases in `Compiler-testruns/`, needs expansion |
| **Parallel Validation** | Validate many scripts concurrently | Low | ✅ COMPLETE | `validate-batch --jobs N` |
| **Baseline Tracking** | Save "known good" state, detect regressions | Low | ✅ COMPLETE | `--save-baseline` flag |
| **CI/CD Integration** | Run validation in GitHub Actions/GitLab CI | Low | ❌ MISSING | No GitHub Actions workflow, manual only |
| **Type Inference Quality Metrics** | Measure accuracy of recovered types (int vs float vs struct) | Medium | ❌ MISSING | 2025 research: 4 metrics (accuracy, precision, FPR, coverage) |
| **Decompiler Error Taxonomy** | Classify *why* decompilation failed (15 error types in 2025 research) | Medium | ❌ MISSING | Current: manual inspection required |
| **One-Click Validation in GUI** | Right-click decompiled code → validate immediately | Low | ❌ MISSING | Current: must click Validate, pick files manually |

### Priority Recommendation for MVP

**High value, low complexity (implement first):**
1. One-click validation in GUI (improves workflow dramatically)
2. CI/CD integration (prevents regressions)
3. Coverage metrics (makes progress measurable)

**High value, high complexity (defer to post-MVP):**
1. Semantic equivalence testing (requires test execution infrastructure)
2. Delta visualization (requires disassembler integration)
3. Test oracle generation (cutting-edge research, high risk)

---

## Anti-Features

Features to explicitly NOT build. Common mistakes in validation systems.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Manual Diff Reading** | Forcing users to read bytecode hex dumps is developer-hostile | Show categorized, interpreted differences with severity |
| **Undifferentiated "Bytes Differ"** | "Files don't match" without context is useless | Categorize: semantic vs cosmetic, show impact |
| **Slow Sequential Validation** | Testing 100 scripts one-by-one wastes developer time | Parallelize batch validation (already done ✅) |
| **No Regression Detection** | Re-testing everything from scratch on each change | Track baselines, only report new failures |
| **Compilation-Only Validation** | "It compiles" doesn't mean "it works correctly" | Add bytecode comparison (already done ✅), consider semantic tests |
| **Ignoring False Positives** | Reporting cosmetic differences as failures trains users to ignore warnings | Filter cosmetic differences, focus on semantic |
| **Non-Reproducible Results** | Different results on same inputs due to non-deterministic tools | Cache results, detect non-determinism |
| **No Export/Sharing** | Validation results trapped in GUI/terminal | Export HTML/JSON reports (already done ✅) |
| **Blocking UI During Validation** | GUI freezes while validating | Run in background thread (check current implementation) |
| **No Progress Indication** | Black box "validating..." for 5 minutes | Show progress bar, stage names (already done ✅) |
| **Testing Only "Easy" Cases** | Validation suite of trivial hello-world scripts | Use real-world production scripts (130 projects in DecompileBench 2025) |

---

## Feature Dependencies (Extended)

### Critical Path (Current)
```
Decompiled Source
  └─> Recompilation Testing
        ├─> [SUCCESS] Bytecode Comparison
        │     └─> Difference Categorization
        │           └─> Pass/Fail Verdict
        │                 └─> Report Export
        └─> [FAILURE] Compilation Error Reporting
              └─> Fail Verdict
```

### Future Enhancements
```
Decompiled Source
  └─> Recompilation Testing
        ├─> [SUCCESS] Bytecode Comparison
        │     ├─> Difference Categorization
        │     │     └─> Delta Visualization (NEW)
        │     │           └─> Interactive Error Analysis (NEW)
        │     └─> Semantic Equivalence Testing (NEW)
        │           └─> Test Oracle Generation (NEW)
        └─> [FAILURE] Compilation Error Reporting
              └─> Decompiler Error Taxonomy (NEW)
                    └─> Automated Bug Filing (NEW)

Batch Validation
  └─> Parallel Execution (EXISTS)
        └─> Baseline Tracking (EXISTS)
              └─> Regression Detection (PARTIAL)
                    └─> Coverage Metrics (NEW)
                          └─> Trend Visualization (NEW)
```

---

## Research-Backed Metrics (2025 SOTA)

Modern decompiler validation uses multi-dimensional assessment:

### 1. Recompilation Success Rate
**What:** Percentage of decompiled outputs that compile without errors
**Current industry:** Hex-Rays 58.3% average (DecompileBench 2025), 36.11% drop under -O3
**VC_Scripter target:** 90%+ (simpler language, no optimizations yet)

### 2. Runtime Behavior Consistency
**What:** Do original and recompiled binaries produce identical output?
**How:** Differential fuzzing - run both with random inputs, compare outputs
**2025 research:** Validated via OSS-Fuzz with 23,400 functions

### 3. Code Quality (LLM-as-Judge)
**What:** 12-dimensional assessment of readability and helpfulness
**Dimensions:**
- 5 readability aspects (type consistency, naming, structure)
- 5 helpfulness aspects (identifier semantics, comments)
- 2 hybrid criteria (modularity, abstraction)
**Note:** VC_Scripter uses deterministic heuristics, not LLM evaluation

### 4. Type Inference Accuracy
**What:** Correct identification of variable types
**Metrics:** Accuracy, Precision, False Positive Rate, Coverage
**VC_Scripter status:** Type inference exists but incomplete (some vars remain `dword`)

### 5. Semantic Equivalence Modulo Inputs (EMI)
**What:** Programs produce same output for all valid inputs
**How:** Symbolic execution to obtain path constraints
**Complexity:** HIGH - requires symbolic execution engine

---

## Comparison Matrix: VC_Scripter vs SOTA (2025)

| Feature | VC_Scripter | Hex-Rays/IDA | Ghidra | DecompileBench | D-Helix |
|---------|-------------|--------------|---------|----------------|---------|
| Recompilation testing | ✅ | ❌ | ❌ | ✅ | ✅ |
| Bytecode comparison | ✅ | ❌ | ❌ | ✅ | ✅ |
| Difference categorization | ✅ (4 types) | N/A | N/A | ✅ (15 types) | ✅ |
| Semantic equivalence | ❌ | ❌ | ❌ | ✅ (fuzzing) | ✅ (symbolic) |
| Batch validation | ✅ | ❌ | ❌ | ✅ | ✅ |
| Regression tracking | ✅ | ❌ | ❌ | ✅ | ❌ |
| Interactive GUI | ✅ | ✅ | ✅ | ❌ | ❌ |
| CI integration | ❌ | N/A | N/A | ✅ | ❌ |
| Coverage metrics | ❌ | ❌ | ❌ | ✅ | ❌ |
| Test oracle generation | ❌ | ❌ | ❌ | ✅ (LLM) | ❌ |

**Key insight:** VC_Scripter has stronger validation infrastructure than commercial decompilers (IDA/Ghidra don't validate at all), but lags behind 2025 academic SOTA in semantic testing and automation.

---

## Immediate Opportunities (Low-Hanging Fruit)

### 1. One-Click GUI Validation (1-2 days)
**Gap:** GUI requires 4 clicks to validate currently-open file
**Fix:** Add "Validate This Script" button that auto-selects current .scr + decompiled output
**Impact:** 10x faster validation workflow

### 2. CI/CD Integration (1 day)
**Gap:** No GitHub Actions workflow to validate on commit
**Fix:** Add `.github/workflows/validate.yml` running batch validation
**Impact:** Catch regressions before merge

### 3. Coverage Dashboard (2-3 days)
**Gap:** No visibility into "73 of 100 scripts compile" progress
**Fix:** Track recompilation rate over time, show trend graph
**Impact:** Measurable progress, identify patterns

### 4. Decompiler Bug Classification (3-5 days)
**Gap:** All failures look identical "compilation failed"
**Fix:** Parse compiler errors, classify by type (syntax, type, semantic)
**Impact:** Prioritize fixes by frequency

### 5. Diff Viewer Integration (3-5 days)
**Gap:** Can't see *what* changed in source code
**Fix:** Show side-by-side original assembly vs decompiled C at failure point
**Impact:** Faster debugging

---

## Long-Term Vision (Post-MVP)

### Phase 1: Automation (Month 1-2)
- CI/CD integration
- Coverage metrics dashboard
- Automated regression detection
- One-click validation

### Phase 2: Analysis (Month 3-4)
- Interactive diff viewer
- Delta visualization (bytecode hex diff)
- Decompiler error taxonomy
- Type inference quality metrics

### Phase 3: Advanced Testing (Month 5-6)
- Semantic equivalence via differential testing
- Automated test generation (from .scr inputs)
- CFG-based validation (verify control flow matches)
- Performance benchmarking

### Phase 4: Research Integration (Month 7+)
- Symbolic execution for equivalence
- LLM-based code quality scoring
- Fuzzing infrastructure (OSS-Fuzz style)
- Large-scale benchmark suite (100+ scripts)

---

## Sources

### 2025 Decompiler Validation Research
- [DecompileBench: A Comprehensive Benchmark for Evaluating Decompilers in Real-World Scenarios](https://arxiv.org/html/2505.11340v1) - 23,400 real-world functions, 3D evaluation framework
- [Decompile-Bench: Million-Scale Binary-Source Function Pairs](https://arxiv.org/html/2505.12668v1) - 2 million function pairs, 20% improvement in re-executability
- [FuzzFlesh: Randomised Testing of Decompilers via CFG-Based Program Generation](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2025.13) - CFG-based testing, runtime path validation
- [Bin2Wrong: A Unified Fuzzing Framework](https://www.usenix.org/system/files/atc25-yang-zao.pdf) - 10.39x-17.18x better binary diversity than previous work

### Semantic Equivalence & Testing
- [Compiler Optimization Testing Based on Optimization-Guided Equivalence Transformations](https://arxiv.org/html/2504.04321v1) - Metamorphic testing, EMI variants
- [DALEQ - Explainable Equivalence for Java Bytecode](https://www.semanticscholar.org/paper/DALEQ-Explainable-Equivalence-for-Java-Bytecode-Dietrich-Hassanshahi/6e5f1e1489e5635bcdc5052cfd030273f1e9cddf) - Bytecode equivalence normalization
- [Can LLMs Recover Program Semantics? A Systematic Evaluation with Symbolic Execution](https://arxiv.org/html/2511.19130) - Symbolic execution for semantic fidelity

### Test Oracle & Quality Metrics
- [Doc2OracLL: Investigating the Impact of Documentation on LLM-based Test Oracle Generation](https://arxiv.org/html/2412.09360) - 10-20% improvement with documentation
- [Benchmarking Binary Type Inference Techniques in Decompilers](https://sure-workshop.org/accepted-papers/2025/sure25-8.pdf) - 4 metrics: accuracy, precision, FPR, coverage
- [Evaluating the Effectiveness of Decompilers](https://dl.acm.org/doi/10.1145/3650212.3652144) - 12-dimensional code quality assessment

### Industry Tools & Comparisons
- [Ghidra vs IDA Pro: Comparison](https://osintteam.blog/ghidra-vs-ida-pro-a-comparison-of-two-popular-reverse-engineering-tools-55223fad9193) - Qualitative decompiler comparison
- [Is This the Same Code? WebAssembly Decompilation Study](https://arxiv.org/html/2411.02278v1) - Framework for empirically evaluating decompilers
- [Java Decompiler Diversity and Meta-decompilation](https://arxiv.org/pdf/2005.11315) - 84% syntactic correctness, 78% semantic equivalence

### Regression Testing & Automation
- [Regression Testing Automation: A Detailed Guide](https://www.globalapptesting.com/blog/regression-testing-automation) - 72.3% of teams adopting AI-driven workflows
- [Top Automation Testing Trends to Watch in 2025](https://testguild.com/automation-testing-trends/) - CI/CD integration, agentic AI

---

## Confidence Assessment

| Area | Confidence | Source Quality |
|------|------------|----------------|
| Table stakes features | HIGH | Multiple 2025 papers, industry consensus |
| Differentiating features | HIGH | 2025 SOTA research (DecompileBench, FuzzFlesh, Bin2Wrong) |
| Anti-features | MEDIUM | Industry best practices, not formal research |
| Coverage metrics | HIGH | Benchmarking Binary Type Inference paper (2025) |
| Semantic equivalence | HIGH | Multiple 2025 papers on symbolic execution, EMI |
| Test oracle generation | MEDIUM | Emerging research (2024-2025), limited production use |
| LLM-based quality scoring | MEDIUM | Very recent (2025), not widely adopted yet |

### Research Gaps

1. **Domain-specific validation:** Most research focuses on general-purpose C decompilation. VC script language is simpler (no pointers, no dynamic allocation) - validation may be easier.

2. **Proprietary compiler quirks:** SCMP.exe has undocumented behavior. Need empirical testing to discover edge cases.

3. **Optimal difference categorization:** Current 4 categories (SEMANTIC, COSMETIC, OPTIMIZATION, UNKNOWN) may need refinement based on VC-specific patterns.

4. **Scalability:** Unknown if batch validation performance is acceptable for 1000+ scripts. May need optimization.

---

## Recommendations for Roadmap

### Phase Structure Suggestion

**Phase 1: Fix Core Decompiler (Foundation)**
- Goal: Get existing decompiler to produce compilable C
- Validation role: Identify what's broken (error classification)
- Focus: Compilation error reporting, one-click validation

**Phase 2: Semantic Correctness (Equivalence)**
- Goal: Compilable C that matches original bytecode
- Validation role: Detect semantic differences
- Focus: Bytecode comparison refinement, difference categorization

**Phase 3: Automation & Regression (Scale)**
- Goal: Never break what works, measure progress
- Validation role: CI integration, coverage tracking
- Focus: Regression testing, coverage metrics, benchmarks

**Phase 4: Advanced Analysis (Quality)**
- Goal: Understand *why* failures happen, fix systematically
- Validation role: Error taxonomy, delta visualization
- Focus: Interactive debugging, semantic equivalence testing

### Research Flags for Phases

- **Phase 1:** LOW research needed - standard compilation error handling
- **Phase 2:** MEDIUM research needed - difference categorization heuristics are domain-specific
- **Phase 3:** LOW research needed - CI/CD patterns are well-established
- **Phase 4:** HIGH research needed - semantic equivalence testing requires new infrastructure

### Critical Success Metrics

1. **Recompilation rate:** Track % of scripts that compile successfully
   - Target: 0% → 50% (Phase 1) → 90% (Phase 2) → 95% (Phase 3)

2. **Semantic equivalence rate:** Track % of compiled scripts matching bytecode
   - Target: N/A (Phase 1) → 70% (Phase 2) → 90% (Phase 3)

3. **Validation speed:** Time to validate full test suite
   - Target: <30s for 100 scripts (parallel execution)

4. **Regression detection:** Catch 100% of regressions before merge
   - Requires: CI integration, baseline tracking
