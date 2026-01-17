# Architecture Patterns: Decompiler Quality Improvement Systems

**Domain:** Decompiler validation and testing systems
**Researched:** 2026-01-17
**Confidence:** HIGH

## Recommended Architecture

The architecture for a decompiler quality improvement system consists of five primary layers organized around the validation workflow. This design is informed by modern decompiler testing research (D-Helix, DecompileBench) and existing validation infrastructure in the VC Script Decompiler.

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │  CLI Runner  │  │  GUI Widget  │  │  Batch Processor   │    │
│  └──────┬───────┘  └──────┬───────┘  └─────────┬──────────┘    │
└─────────┼──────────────────┼──────────────────────┼─────────────┘
          │                  │                      │
┌─────────┼──────────────────┼──────────────────────┼─────────────┐
│         │      Orchestration & Test Management Layer             │
│  ┌──────▼──────────────────▼──────────────────────▼──────────┐  │
│  │            Validation Orchestrator (EXISTING)              │  │
│  │  - Coordinates validation workflow                         │  │
│  │  - Manages compilation, comparison, categorization         │  │
│  └────────────────────────┬───────────────────────────────────┘  │
│  ┌─────────────────────────▼────────────────────────┐            │
│  │         Test Suite Manager (NEW)                 │            │
│  │  - Test corpus organization                      │            │
│  │  - Test case selection and prioritization        │            │
│  │  - Batch execution coordination                  │            │
│  └────────────────────────┬─────────────────────────┘            │
└─────────────────────────────┼────────────────────────────────────┘
                              │
┌─────────────────────────────┼────────────────────────────────────┐
│         Validation & Comparison Layer (EXISTING)                 │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Compiler    │  │   Bytecode   │  │    Difference        │  │
│  │   Wrapper     │  │  Comparator  │  │   Categorizer        │  │
│  │   (SCMP.exe)  │  │              │  │  (Semantic/Cosmetic) │  │
│  └───────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────┬────────────────────────────────────┘
                              │
┌─────────────────────────────┼────────────────────────────────────┐
│            Analysis & Intelligence Layer (NEW)                   │
│  ┌─────────────────────────▼────────────────────────┐            │
│  │          Error Pattern Analyzer                  │            │
│  │  - Aggregate differences across test corpus      │            │
│  │  - Identify recurring error patterns             │            │
│  │  - Classify bug types (control flow, types, etc) │            │
│  └──────────────────────────────────────────────────┘            │
│  ┌──────────────────────────────────────────────────┐            │
│  │          Interactive Debugger Bridge             │            │
│  │  - Code location mapping (bytecode ↔ source)     │            │
│  │  - Error context extraction                      │            │
│  │  - Root cause hypothesis generation              │            │
│  └──────────────────────────────────────────────────┘            │
└─────────────────────────────┬────────────────────────────────────┘
                              │
┌─────────────────────────────┼────────────────────────────────────┐
│         Persistence & Regression Layer (PARTIAL)                 │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Regression   │  │ Validation   │  │   Test Result        │  │
│  │  Baseline     │  │    Cache     │  │   Database           │  │
│  │  (EXISTING)   │  │ (EXISTING)   │  │   (NEW)              │  │
│  └───────────────┘  └──────────────┘  └──────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### Component Boundaries

| Component | Responsibility | Input | Output |
|-----------|---------------|-------|--------|
| **CLI Runner** | Command-line interface for validation commands | User commands, file paths | Terminal output, reports |
| **GUI Widget** | Interactive validation UI with compile button | User interactions | Visual feedback, results |
| **Batch Processor** | Parallel validation of multiple files | Directory paths, test list | Batch report |
| **Validation Orchestrator** | End-to-end validation workflow | SCR + C source | ValidationResult |
| **Test Suite Manager** | Test corpus management, selection | Test corpus directory | Selected test cases |
| **Compiler Wrapper** | Interface to SCMP.exe | C source code | SCR bytecode or errors |
| **Bytecode Comparator** | Binary diff of SCR files | Two SCR files | List of Differences |
| **Difference Categorizer** | Semantic/cosmetic classification | Differences | CategorizedDifferences |
| **Error Pattern Analyzer** | Cross-test pattern detection | Multiple ValidationResults | Error patterns, statistics |
| **Interactive Debugger Bridge** | Map errors to code locations | Difference + source | Annotated source, context |
| **Regression Baseline** | Golden output storage | Test name | Expected result |
| **Validation Cache** | Performance optimization | File hash | Cached ValidationResult |
| **Test Result Database** | Historical test tracking | Test runs | Trends, regressions |

### Data Flow

The primary data flow follows the validation workflow:

```
1. TEST DISCOVERY
   User → Test Suite Manager → Test Corpus
   Returns: List of (original.scr, decompiled.c) pairs

2. VALIDATION EXECUTION
   Test Suite Manager → Validation Orchestrator
   For each test case:
     a) Check cache
     b) Compile decompiled.c → recompiled.scr
     c) Compare original.scr vs recompiled.scr
     d) Categorize differences
     e) Return ValidationResult

3. PATTERN ANALYSIS (NEW)
   Multiple ValidationResults → Error Pattern Analyzer
   Returns: Aggregated patterns, bug categories

4. INTERACTIVE INVESTIGATION (NEW)
   User selects error → Interactive Debugger Bridge
   Returns: Source code location, context, suggestions

5. REGRESSION TRACKING
   ValidationResult → Regression Comparator + Test Result Database
   Returns: Pass/fail/regression status
```

## Patterns to Follow

### Pattern 1: Pipeline Architecture
**What:** Linear sequence of transformations with clear inputs/outputs

**When:** Processing individual test cases through validation workflow

**Why:** Enables caching at each stage, clear error boundaries, easy to reason about

**Example:**
```python
# Each stage is independent, cacheable, testable
validation_result = (
    ValidationOrchestrator()
    .compile(source)         # Stage 1: C → SCR
    .compare(original)       # Stage 2: SCR diff
    .categorize()            # Stage 3: Semantic analysis
    .verdict()               # Stage 4: Pass/fail
)
```

### Pattern 2: Aggregate Analysis
**What:** Collect results from many test cases, analyze in aggregate

**When:** Finding patterns across multiple validation failures

**Why:** Individual failures don't show patterns; aggregation reveals systematic bugs

**Example:**
```python
# Pattern analyzer aggregates across corpus
pattern_analyzer = ErrorPatternAnalyzer()
for result in batch_results:
    pattern_analyzer.add(result)

patterns = pattern_analyzer.get_patterns()
# Returns: "70% of failures involve switch/case statements"
```

### Pattern 3: Golden Output Testing
**What:** Store known-good output, detect regressions

**When:** Ensuring decompiler improvements don't break existing functionality

**Why:** Catch regressions immediately, enable confident refactoring

**Example:**
```python
# Save baseline after verifying correctness
baseline.save("test_tdm", validation_result)

# Later, detect regressions
new_result = validate("tdm.scr", "tdm_decompiled.c")
if regression_detector.compare(baseline, new_result):
    alert("REGRESSION: New errors introduced")
```

### Pattern 4: Differential Testing Oracle
**What:** Use original compiler as oracle - recompile and compare

**When:** Validating decompiled code correctness

**Why:** The original compiler defines "correct" behavior definitively

**Example:**
```python
# The oracle is recompilation + bytecode comparison
oracle = DifferentialTestOracle(compiler=SCMP)
verdict = oracle.validate(
    original_bytecode=original_scr,
    decompiled_source=decompiled_c
)
# If recompiled bytecode matches original → decompilation correct
```

### Pattern 5: Interactive Investigation Workflow
**What:** Enable rapid error → source → fix cycles

**When:** Debugging decompilation failures

**Why:** Reduces time from "test failed" to "root cause identified"

**Example:**
```python
# User clicks error in GUI
error = selected_difference

# Bridge maps to decompiler source
debugger_bridge = InteractiveDebugger(error)
location = debugger_bridge.get_code_location()
# Returns: "vcdecomp/core/ir/structure/patterns/switch_case.py:147"

context = debugger_bridge.get_context()
# Returns: SSA graph, CFG, original bytecode at failure point
```

### Pattern 6: Parallel Test Execution
**What:** Run independent test cases concurrently

**When:** Batch validation of large test corpus

**Why:** Validation is I/O bound (compiler exec), parallelizes well

**Example:**
```python
# Batch processor uses process pool
with ProcessPoolExecutor(max_workers=8) as executor:
    futures = [
        executor.submit(validate, orig, decomp)
        for orig, decomp in test_pairs
    ]
    results = [f.result() for f in futures]
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Tightly Coupled Test Selection
**What:** Hard-coding test file paths in test code

**Why bad:** Makes it impossible to run custom test suites, user files

**Instead:** Use Test Suite Manager with configurable test discovery
```python
# BAD
TEST_FILES = ["testrun1/tdm.scr", "testrun2/gaz.scr"]

# GOOD
test_manager = TestSuiteManager()
test_files = test_manager.discover(
    input_dir="decompiled/",
    original_dir="scripts/",
    pattern="*.c"
)
```

### Anti-Pattern 2: Ignoring Test Corpus Organization
**What:** Dumping all test files in single directory without metadata

**Why bad:** Can't categorize tests (unit vs integration), no prioritization

**Instead:** Organize by category with metadata
```
test-corpus/
  unit/           # Small, focused tests
    operators/
    control_flow/
  integration/    # Full mission scripts
  regression/     # Known-bug reproducers
  metadata.json   # Test properties, expected failures
```

### Anti-Pattern 3: Binary Pass/Fail Verdicts
**What:** Only reporting "pass" or "fail" without nuance

**Why bad:** Hides useful information (cosmetic diffs vs semantic bugs)

**Instead:** Use categorical verdicts (EXISTING PATTERN - keep this)
```python
# Already implemented correctly
result.verdict = ValidationVerdict.PARTIAL  # Compiles but has differences
result.has_semantic_differences  # Boolean
result.get_differences_by_category(SEMANTIC)  # Details
```

### Anti-Pattern 4: Manual Error Investigation
**What:** Developer manually examines each failure one-by-one

**Why bad:** Doesn't scale, misses patterns, wastes developer time

**Instead:** Automated pattern detection, aggregated reports
```python
# Analyzer finds patterns automatically
analyzer.analyze(batch_results)
# Output: "20 failures all involve for-loop init expressions"
# Developer fixes one root cause, 20 tests pass
```

### Anti-Pattern 5: Throwing Away Test Results
**What:** Only keeping latest test run, no history

**Why bad:** Can't track progress, can't detect regressions

**Instead:** Persist results in database, track trends
```python
# Store every test run
test_db.record_run(
    timestamp=now(),
    decompiler_version=git_commit,
    results=validation_results
)

# Query historical data
trend = test_db.get_trend(test_name="tdm", days=30)
# Shows pass rate improving over time
```

### Anti-Pattern 6: GUI-Only Workflow
**What:** Validation only accessible through GUI

**Why bad:** Can't automate, can't integrate with CI, slow for batch

**Instead:** CLI-first with GUI as optional interface
```python
# Existing CLI is good foundation
python -m vcdecomp validate original.scr decompiled.c

# GUI enhances with interactivity, not replaces
gui.show_validation_result(result)  # Visualize what CLI provides
```

## Scalability Considerations

### At 10 Test Cases (Current)
**Challenge:** Manual workflow adequate but slow

**Approach:**
- Simple CLI validation command
- Manual result inspection
- No caching needed
- Single-threaded execution

**Architecture:**
```
User → validate command → ValidationOrchestrator → Report
```

### At 100 Test Cases (Near-term)
**Challenge:** Manual inspection becomes bottleneck

**Approach:**
- Batch validation with parallelization (8 workers)
- Validation cache for unchanged files
- Automated pattern detection
- Summary reports (not individual results)

**Architecture:**
```
User → validate-batch → TestSuiteManager → ThreadPoolExecutor
                                          → ErrorPatternAnalyzer
                                          → Aggregated Report
```

### At 1000+ Test Cases (Long-term)
**Challenge:** Runtime, storage, result analysis

**Approach:**
- Incremental testing (only changed files)
- Distributed execution (multiple machines)
- Test result database with indexing
- Statistical analysis, ML-based pattern detection
- Test prioritization (run likely-to-fail first)

**Architecture:**
```
User → CI System → Test Prioritizer → Distributed Workers
                                     → Result Database
                                     → Trend Analyzer
                                     → Regression Detector
```

## Integration Points

### With Existing Validation Layer
**Status:** EXISTING - well-architected

**Integration:** New components consume existing interfaces
```python
# Existing ValidationOrchestrator is clean interface
from vcdecomp.validation import ValidationOrchestrator

# New Test Suite Manager uses it
class TestSuiteManager:
    def __init__(self, orchestrator: ValidationOrchestrator):
        self.orchestrator = orchestrator

    def run_batch(self, test_cases):
        return [self.orchestrator.validate(tc) for tc in test_cases]
```

### With GUI
**Status:** GUI exists but needs validation integration

**Integration:** Add compile button that invokes ValidationOrchestrator
```python
# GUI widget
class ValidationPanel:
    def on_compile_clicked(self):
        result = self.orchestrator.validate(
            original_scr=self.current_scr,
            decompiled_source=self.editor.get_text()
        )
        self.show_result(result)
```

### With Decompiler Core
**Status:** Independent - validation doesn't modify decompiler

**Integration:** One-way dependency (validation → decompiler output)
```python
# Validation consumes decompiler output
decompiled_code = decompiler.decompile("script.scr")
validation_result = validator.validate(
    original="script.scr",
    decompiled=decompiled_code
)
```

### With CI/CD (Future)
**Status:** Not yet implemented

**Integration:** CLI + exit codes enable CI integration
```bash
# CI script
python -m vcdecomp validate-batch \
  --input-dir decompiled/ \
  --original-dir scripts/ \
  --report-file report.json \
  --fail-on-regression

# Exit code 0 = all pass, 1 = failures detected
```

## Build Order Recommendations

Based on component dependencies and value delivery:

### Phase 1: Test Infrastructure (Foundation)
**Build first:** Test Suite Manager, batch processing
**Why:** Enables running validation at scale
**Dependencies:** None (uses existing ValidationOrchestrator)
**Deliverable:** `validate-batch` command working

### Phase 2: Error Analysis (Intelligence)
**Build second:** Error Pattern Analyzer, aggregated reports
**Why:** Transforms raw failures into actionable insights
**Dependencies:** Phase 1 (needs batch results to analyze)
**Deliverable:** Pattern reports showing "20% of failures are switch/case bugs"

### Phase 3: Regression Tracking (Quality Gate)
**Build third:** Test Result Database, regression detection
**Why:** Prevents backsliding, enables confident refactoring
**Dependencies:** Phase 1 (needs test runs to track)
**Deliverable:** Regression alerts when new bugs introduced

### Phase 4: Interactive Investigation (Developer UX)
**Build fourth:** Interactive Debugger Bridge, GUI integration
**Why:** Accelerates bug fixes, but requires stable test infrastructure
**Dependencies:** Phase 1-2 (needs error patterns to investigate)
**Deliverable:** Click error → see source location + context

### Dependency Graph
```
Phase 1 (Test Infrastructure)
    ├── Phase 2 (Error Analysis)
    │       └── Phase 4 (Interactive Investigation)
    └── Phase 3 (Regression Tracking)
```

## Validation-Specific Patterns

### Pattern: Difference Categorization
**Already implemented:** DifferenceCategory (SEMANTIC, COSMETIC, OPTIMIZATION, UNKNOWN)

**Usage:** Don't treat all differences equally
```python
# SEMANTIC differences = bugs to fix
semantic_diffs = result.get_differences_by_category(SEMANTIC)
if semantic_diffs:
    print("FAIL: Behavioral differences detected")

# COSMETIC differences = acceptable
cosmetic_diffs = result.get_differences_by_category(COSMETIC)
if only cosmetic_diffs:
    print("PASS: Functionally equivalent")
```

### Pattern: Recompilation as Oracle
**Core insight:** Original compiler is ground truth

**Workflow:**
1. Decompile: `original.scr` → `decompiled.c`
2. Recompile: `decompiled.c` → `recompiled.scr`
3. Compare: `original.scr` vs `recompiled.scr`
4. If bytecode identical → perfect decompilation
5. If differences only cosmetic → acceptable decompilation
6. If semantic differences → decompilation bug

### Pattern: Test Corpus with Ground Truth
**Organization:**
```
test-corpus/
  with-source/          # Known source + compiled bytecode
    testrun1/
      tdm.c             # Original source (ground truth)
      tdm.scr           # Compiled output
    testrun2/
      gaz_67.c
      gaz_67.scr

  production/           # Real game scripts (no source)
    mission1/
      level.scr         # Validate via recompilation only
      player.scr
```

**Usage:**
- `with-source/`: Can compare decompiled vs original source (bonus validation)
- `production/`: Only recompilation validation available

### Pattern: Confidence Levels for Differences
**Insight:** Some categorizations are uncertain

**Implementation:**
```python
@dataclass
class CategorizedDifference:
    category: DifferenceCategory
    confidence: float  # 0.0 to 1.0
    rationale: str

# High confidence
CategorizedDifference(
    category=SEMANTIC,
    confidence=0.95,
    rationale="Entry point mismatch - definitely semantic"
)

# Low confidence
CategorizedDifference(
    category=COSMETIC,
    confidence=0.6,
    rationale="Instruction reordering - likely cosmetic but uncertain"
)
```

## Sources

**Decompiler Testing Research:**
- [D-Helix: A Generic Decompiler Testing Framework Using Symbolic Differentiation](https://www.usenix.org/conference/usenixsecurity24/presentation/zou) - HIGH confidence: Official USENIX paper on modern decompiler testing framework architecture
- [DecompileBench: A Comprehensive Benchmark for Evaluating Decompilers](https://arxiv.org/html/2505.11340v1) - HIGH confidence: 2025 research on decompiler validation with runtime consistency checking
- [How Far We Have Come: Testing Decompilation Correctness of C Decompilers](https://monkbai.github.io/files/issta-20.pdf) - HIGH confidence: Academic paper on decompiler correctness testing methodology

**Compiler Validation:**
- [A Survey of Compiler Testing](https://dl.acm.org/doi/10.1145/3363562) - MEDIUM confidence: Comprehensive survey of compiler testing approaches applicable to decompilers
- [Semantic Equivalence Checking for HHVM Bytecode](https://www.semanticscholar.org/paper/Semantic-Equivalence-Checking-for-HHVM-Bytecode-Benton/fd8d33963b6a0cecdf3f0c4140855363acd8d431) - MEDIUM confidence: Bytecode comparison methodology

**Test Automation Architecture:**
- [Test Automation Architecture - How It is Evolving in 2025](https://www.testwheel.com/blog/test-automation-architecture/) - MEDIUM confidence: Modern test automation patterns
- [Top 10 Test Automation Frameworks in 2025](https://testgrid.io/blog/test-automation-framework/) - LOW confidence: Framework survey (not decompiler-specific)

**Interactive Analysis Tools:**
- [IDA Pro: Powerful Disassembler, Decompiler & Debugger](https://hex-rays.com/ida-pro) - HIGH confidence: Industry-standard decompiler with interactive debugging
- [Binary Ninja](https://binary.ninja/) - HIGH confidence: Modern decompiler with API-driven automation
- [Ghidra: Decompiling and Debugging](https://dev.to/glsolaria/decompiling-and-debugging-with-ghidra-15k3) - MEDIUM confidence: Open-source decompiler workflow patterns
- [decomp2dbg: Interactive symbols from decompiler to debugger](https://github.com/mahaloz/decomp2dbg) - MEDIUM confidence: Integration pattern between decompilation and debugging
