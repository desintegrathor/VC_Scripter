# Phase 4: Error Analysis System - Research

**Researched:** 2026-01-18
**Domain:** Developer diagnostic tooling for compiler error analysis
**Confidence:** HIGH

## Summary

Researched systematic approaches to error classification, pattern detection, and interactive debugging for the decompiler's validation workflow. The phase builds on existing validation infrastructure (CompilationError, DifferenceCategory) to add diagnostic capabilities for understanding why decompiled code fails to compile.

Key findings:
- **Error classification** follows compiler theory (syntax, semantic, type errors) - already partially implemented via heuristics in test_validation.py
- **Pattern detection** uses aggregation and statistical analysis to identify systemic issues (e.g., "70% of failures are switch/case bugs")
- **Interactive visualization** leverages Python's difflib and Qt widgets for side-by-side comparison with diff highlighting
- **Bytecode comparison** at instruction level already exists (bytecode_compare.py) - needs UI integration only

**Primary recommendation:** Build analysis UI using existing ValidationResult data structures. Focus on programmatic categorization and aggregation rather than ML/AI complexity. Use Qt QTextEdit with difflib for side-by-side views.

## Standard Stack

The established libraries/tools for error analysis and comparison visualization:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| difflib | stdlib | Text comparison with unified/side-by-side diffs | Python standard library, battle-tested since 1996 |
| PyQt6/PySide6 | 6.x | GUI framework for interactive views | Already in project (vcdecomp/gui/), cross-platform |
| pytest | existing | Test execution and result collection | Already in project, standard Python testing |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| difflib.HtmlDiff | stdlib | HTML-based side-by-side comparison | Generating standalone reports or documentation |
| QTextEdit | PyQt6 | Syntax-highlighted text display | Assembly/C code side-by-side views |
| QTreeWidget | PyQt6 | Hierarchical error navigation | Already used in difference_widgets.py |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| difflib | unified_diff CLI | Less interactive, harder to navigate |
| Qt widgets | Web-based (Flask+HTML) | Requires server, less integrated with existing GUI |
| Manual categorization | ML/AI classification | Over-engineering for one-time diagnostic use |

**Installation:**
No new dependencies required - all tools already in project or Python stdlib.

## Architecture Patterns

### Recommended Project Structure
```
vcdecomp/
├── validation/
│   ├── error_analyzer.py      # Error pattern detection and aggregation
│   ├── compilation_types.py   # CompilationError (already exists)
│   └── difference_types.py    # DifferenceCategory (already exists)
├── gui/
│   ├── views/
│   │   ├── validation_view.py  # Existing validation panel
│   │   └── error_analysis_view.py  # NEW: Error analysis dock
│   └── widgets/
│       ├── difference_widgets.py  # Existing bytecode diff tree
│       ├── error_pattern_widget.py  # NEW: Pattern aggregation display
│       └── side_by_side_diff.py    # NEW: Assembly/C comparison
└── tests/
    └── test_validation.py      # Already categorizes errors (lines 154-173)
```

### Pattern 1: Error Categorization Pipeline
**What:** Parse CompilationError objects, categorize by error type, aggregate statistics
**When to use:** After validation completes with compilation failure
**Example:**
```python
# Source: Existing pattern from test_validation.py (lines 154-173)
def categorize_compilation_errors(errors: List[CompilationError]) -> Dict[str, int]:
    """Group errors by type for pattern detection."""
    error_types = {}
    for error in errors:
        msg_lower = error.message.lower()
        if "syntax" in msg_lower or "expected" in msg_lower:
            error_type = "syntax"
        elif "undefined" in msg_lower or "undeclared" in msg_lower:
            error_type = "undefined"
        elif "type" in msg_lower:
            error_type = "type"
        elif "include" in msg_lower or "cannot open" in msg_lower:
            error_type = "include"
        else:
            error_type = "other"

        error_types[error_type] = error_types.get(error_type, 0) + 1

    return error_types
```

### Pattern 2: Side-by-Side Diff with difflib
**What:** Display assembly (.asm) vs decompiled C (.c) with line-by-line alignment
**When to use:** Investigating semantic differences in bytecode
**Example:**
```python
# Source: Python difflib documentation + Qt integration pattern
from difflib import HtmlDiff, unified_diff
from PyQt6.QtWidgets import QTextEdit, QSplitter

class SideBySideDiffWidget(QSplitter):
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.left_pane = QTextEdit()
        self.right_pane = QTextEdit()
        self.addWidget(self.left_pane)
        self.addWidget(self.right_pane)

    def show_diff(self, original_asm: str, decompiled_c: str):
        """Display side-by-side comparison with diff highlighting."""
        original_lines = original_asm.splitlines()
        decompiled_lines = decompiled_c.splitlines()

        # Compute diff and highlight changes
        differ = difflib.Differ()
        diff = list(differ.compare(original_lines, decompiled_lines))

        # Apply syntax highlighting to changed lines
        self._highlight_diff(self.left_pane, original_lines, diff, is_left=True)
        self._highlight_diff(self.right_pane, decompiled_lines, diff, is_left=False)
```

### Pattern 3: Error Pattern Aggregation
**What:** Aggregate errors across multiple test cases to identify systemic issues
**When to use:** Running batch validation (validate-batch command)
**Example:**
```python
# Pattern for error aggregation
class ErrorPatternDetector:
    def __init__(self):
        self.error_counts = {}  # {error_type: count}
        self.error_examples = {}  # {error_type: [CompilationError]}

    def analyze_batch_results(self, results: List[ValidationResult]):
        """Detect patterns across multiple validation runs."""
        total_failures = 0
        for result in results:
            if not result.compilation_succeeded:
                total_failures += 1
                categorized = categorize_compilation_errors(result.compilation_result.errors)
                for error_type, count in categorized.items():
                    self.error_counts[error_type] = self.error_counts.get(error_type, 0) + count
                    if error_type not in self.error_examples:
                        self.error_examples[error_type] = []
                    self.error_examples[error_type].extend(result.compilation_result.errors[:3])

        # Generate insights
        if total_failures > 0:
            insights = []
            for error_type, count in sorted(self.error_counts.items(), key=lambda x: -x[1]):
                percentage = (count / sum(self.error_counts.values())) * 100
                insights.append(f"{percentage:.1f}% ({count}) are {error_type} errors")

            return insights
```

### Anti-Patterns to Avoid
- **Over-engineering categorization:** Don't use ML/AI for simple keyword matching - heuristics sufficient for diagnostic tool
- **Building custom diff algorithm:** Don't reinvent difflib - it's battle-tested and handles edge cases
- **Mixing analysis with validation:** Keep ErrorAnalyzer separate from ValidationOrchestrator - single responsibility
- **Storing analysis results long-term:** This is one-time diagnostic tooling - focus on immediate insights, not persistence

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Text diffing algorithm | Custom line-by-line comparison | difflib.unified_diff, difflib.HtmlDiff | Handles whitespace, line endings, Unicode, performance edge cases |
| Syntax highlighting | Manual token parsing and coloring | QSyntaxHighlighter (Qt) or Pygments | Proper tokenization for C, assembly, complex regex |
| Tree-based error navigation | Custom hierarchical widget | QTreeWidget with QTreeWidgetItem | Built-in expand/collapse, selection, keyboard nav |
| Test result collection | Custom pytest plugin | pytest --json-report | Standard format, extensible, already integrated |
| Bytecode instruction diff | Custom opcode comparison | Existing BytecodeComparator | Already handles variants, alignment, metadata |

**Key insight:** Phase focuses on *presentation* of existing analysis data, not inventing new algorithms. Validation infrastructure already captures all needed information.

## Common Pitfalls

### Pitfall 1: Keyword-Based Classification Fragility
**What goes wrong:** Heuristic error categorization breaks when compiler changes error message format
**Why it happens:** Test suite uses string matching ("syntax" in msg_lower) which is brittle
**How to avoid:**
- Parse .err files with multiple regex patterns (already in compiler_wrapper.py lines 308-340)
- Use CompilationStage + ErrorSeverity as primary classification, keywords as fallback
- Document known error message patterns in error_analyzer.py
**Warning signs:** Tests start miscategorizing errors after compiler update

### Pitfall 2: Diff Alignment for Different Code Structures
**What goes wrong:** Side-by-side diff shows misaligned content when assembly and C have different line counts
**Why it happens:** difflib aligns by line similarity, but .asm (instruction-based) and .c (statement-based) have different granularity
**How to avoid:**
- Use unified_diff for instruction-level bytecode comparison (original vs recompiled .scr)
- Use HtmlDiff for source-level comparison (original.c vs decompiled.c) only
- Don't try to align .asm with decompiled.c - they're fundamentally different representations
**Warning signs:** User confusion when viewing "diffs" that don't line up conceptually

### Pitfall 3: Performance with Large Error Sets
**What goes wrong:** Loading 1000+ errors into QTreeWidget freezes GUI
**Why it happens:** Qt widgets block UI thread during bulk insertion
**How to avoid:**
- Batch insert with beginInsertRows/endInsertRows (Qt best practice)
- Limit initial display to top 100 errors, lazy-load on expand
- Use QSortFilterProxyModel for filtering instead of rebuilding tree
**Warning signs:** GUI becomes unresponsive when loading batch validation results

### Pitfall 4: Confusing "Reproducible Steps" with "Reproduction Script"
**What goes wrong:** ERROR-05 requirement misinterpreted as needing automated reproduction
**Why it happens:** "Reproducible steps" sounds like automation, but it means human-readable instructions
**How to avoid:**
- Store ValidationResult metadata: original_scr path, decompiled_source path, timestamp
- Generate markdown checklist: "1. Run: python -m vcdecomp structure test1.scr > test1.c  2. Run: scmp.exe test1.c test1_new.scr  3. Compare: diff test1.scr test1_new.scr"
- Don't build automation to re-run tests - that's what CI does
**Warning signs:** Building complex test replay infrastructure when simple markdown suffices

## Code Examples

Verified patterns from existing codebase and stdlib:

### Error Categorization (Production Pattern)
```python
# Source: vcdecomp/tests/test_validation.py (lines 154-173)
# This is the EXISTING pattern - ERROR-01 satisfied by extending this

def categorize_compilation_errors(errors: List[CompilationError]) -> Dict[str, List[CompilationError]]:
    """
    Categorize compilation errors by type.

    Returns dict mapping error types to lists of errors of that type.
    Used for both display (ERROR-03) and aggregation (ERROR-02).
    """
    categorized = {
        "syntax": [],      # "expected", "syntax error"
        "type": [],        # "type mismatch", "incompatible types"
        "semantic": [],    # "undefined", "undeclared", "not declared"
        "include": [],     # "cannot open", "no such file"
        "other": []        # Uncategorized
    }

    for error in errors:
        msg_lower = error.message.lower()

        # Syntax errors
        if "syntax" in msg_lower or "expected" in msg_lower:
            categorized["syntax"].append(error)
        # Semantic errors (undefined symbols, scope)
        elif "undefined" in msg_lower or "undeclared" in msg_lower or "not declared" in msg_lower:
            categorized["semantic"].append(error)
        # Type errors
        elif "type" in msg_lower or "incompatible" in msg_lower:
            categorized["type"].append(error)
        # Include errors
        elif "include" in msg_lower or "cannot open" in msg_lower:
            categorized["include"].append(error)
        else:
            categorized["other"].append(error)

    return categorized
```

### difflib Side-by-Side Comparison (Stdlib Pattern)
```python
# Source: Python difflib documentation (https://docs.python.org/3/library/difflib.html)
# Pattern for ERROR-03 requirement (side-by-side view)

from difflib import HtmlDiff

def generate_side_by_side_html(original_asm: str, decompiled_c: str, context_lines: int = 3):
    """
    Generate HTML with side-by-side comparison.

    Args:
        original_asm: Disassembled bytecode (.asm file content)
        decompiled_c: Decompiled C source (.c file content)
        context_lines: Number of context lines around differences

    Returns:
        HTML string with syntax-highlighted comparison
    """
    differ = HtmlDiff(wrapcolumn=80)

    original_lines = original_asm.splitlines(keepends=True)
    decompiled_lines = decompiled_c.splitlines(keepends=True)

    html = differ.make_file(
        original_lines,
        decompiled_lines,
        fromdesc="Original Assembly (.asm)",
        todesc="Decompiled C (.c)",
        context=True,  # Only show differences + context
        numlines=context_lines
    )

    return html
```

### Bytecode Instruction Diff (Existing Pattern)
```python
# Source: vcdecomp/validation/bytecode_compare.py (already exists)
# Pattern for ERROR-04 requirement (bytecode diff highlighting)

from vcdecomp.validation.bytecode_compare import BytecodeComparator

def show_bytecode_diff_with_context(original_scr: Path, recompiled_scr: Path):
    """
    Compare bytecode files at instruction level and highlight differences.

    This functionality ALREADY EXISTS - just needs UI integration.
    """
    comparator = BytecodeComparator()
    result = comparator.compare_files(original_scr, recompiled_scr)

    # result.all_differences contains Difference objects with:
    # - type: DifferenceType (HEADER, CODE, DATA, XFN)
    # - severity: DifferenceSeverity (CRITICAL, MAJOR, MINOR, INFO)
    # - description: Human-readable explanation
    # - details: Dict with specific offset, instruction info

    for diff in result.all_differences:
        print(f"{diff.severity.value}: {diff.description}")
        if diff.type == DifferenceType.CODE:
            # CODE differences have instruction-level details
            offset = diff.details.get("offset", "unknown")
            original_instr = diff.details.get("original", "")
            recompiled_instr = diff.details.get("recompiled", "")
            print(f"  @ {offset}: {original_instr} -> {recompiled_instr}")
```

### Test Case Logging (ERROR-05 Requirement)
```python
# Pattern for reproducible debugging steps

def log_failed_test_case(result: ValidationResult, output_dir: Path):
    """
    Log test failure with reproducible steps for investigation.

    Creates markdown file with:
    1. Command to reproduce decompilation
    2. Command to reproduce compilation
    3. Paths to artifacts (source, bytecode, errors)
    4. Error summary
    """
    test_id = result.original_scr.stem
    log_file = output_dir / f"{test_id}_failure.md"

    with open(log_file, 'w') as f:
        f.write(f"# Test Failure: {test_id}\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Verdict:** {result.verdict.value}\n\n")

        f.write("## Reproducible Steps\n\n")
        f.write("### 1. Decompile\n")
        f.write(f"```bash\n")
        f.write(f"python -m vcdecomp structure {result.original_scr} > decompiled.c\n")
        f.write(f"```\n\n")

        f.write("### 2. Compile\n")
        f.write(f"```bash\n")
        f.write(f"cd {result.metadata['compiler_dir']}\n")
        f.write(f"scmp.exe decompiled.c output.scr output.h\n")
        f.write(f"```\n\n")

        f.write("## Artifacts\n")
        f.write(f"- Original: `{result.original_scr}`\n")
        f.write(f"- Decompiled: `{result.decompiled_source}`\n")
        if result.compilation_result:
            f.write(f"- Working dir: `{result.compilation_result.working_dir}`\n")
            f.write(f"- Error files: `spp.err`, `scc.err`, `sasm.err`\n")

        f.write("\n## Error Summary\n")
        if result.compilation_result and result.compilation_result.errors:
            categorized = categorize_compilation_errors(result.compilation_result.errors)
            for error_type, errors in categorized.items():
                if errors:
                    f.write(f"\n### {error_type.capitalize()} Errors ({len(errors)})\n")
                    for error in errors[:5]:  # First 5 of each type
                        f.write(f"- {error}\n")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual error inspection | Programmatic categorization (test_validation.py) | Phase 2 (2026-01-18) | Enables automated quality metrics |
| Text-based diff output | Interactive GUI with DifferenceTreeView | Phase 1 (2026-01-18) | Better navigation and understanding |
| Single test execution | Batch validation with baselines | Phase 3 (2026-01-18) | Enables pattern detection across corpus |
| Static .err file reading | Structured CompilationError objects | Phase 2 (2026-01-18) | Enables filtering, sorting, aggregation |

**Deprecated/outdated:**
- Manual review of .err files: Replaced by CompilationError parsing (compiler_wrapper.py lines 274-382)
- CLI-only validation: GUI validation panel now primary workflow (Phase 1)
- Unstructured diff output: Categorized differences with severity/category (difference_types.py)

## Open Questions

1. **How to handle assembly vs C code alignment in side-by-side view?**
   - What we know: .asm is instruction-based (one opcode per line), .c is statement-based (multi-line statements)
   - What's unclear: Best UX for comparing fundamentally different representations
   - Recommendation: Show them in separate tabs, not side-by-side. Use bytecode comparison (original.scr vs recompiled.scr) for instruction-level diff.

2. **Should error patterns persist across sessions for trend analysis?**
   - What we know: Phase context says "one-time diagnostic use" - not production monitoring
   - What's unclear: User might want to track "did we improve?" over time
   - Recommendation: Save analysis results as JSON alongside baselines (.planning/baselines/), but don't build database

3. **What constitutes a "pattern" vs isolated error?**
   - What we know: Requirement says "e.g., 70% are switch/case bugs"
   - What's unclear: Minimum threshold for calling something a pattern (3 occurrences? 10%?)
   - Recommendation: Display all error types with percentages, let user decide what's significant. No hard thresholds.

## Sources

### Primary (HIGH confidence)
- Python difflib documentation: https://docs.python.org/3/library/difflib.html
- PyQt6 documentation: https://doc.qt.io/qtforpython-6.9/
- Existing codebase patterns:
  - vcdecomp/tests/test_validation.py (error categorization, lines 154-173)
  - vcdecomp/validation/compiler_wrapper.py (error parsing, lines 274-382)
  - vcdecomp/validation/difference_types.py (bytecode categorization)
  - vcdecomp/gui/widgets/difference_widgets.py (DifferenceTreeView pattern)

### Secondary (MEDIUM confidence)
- [Learn C++ - Syntax and semantic errors](https://www.learncpp.com/cpp-tutorial/syntax-and-semantic-errors/) - Compiler error classification
- [GeeksforGeeks - Semantic Analysis](https://www.geeksforgeeks.org/compiler-design/semantic-analysis-in-compiler-design/) - Error detection stages
- [CodeReview GitHub](https://github.com/FabriceSalvaire/CodeReview) - Qt-based diff viewer implementation
- [Towards Data Science - Side-by-side comparison in Python](https://towardsdatascience.com/side-by-side-comparison-of-strings-in-python-b9491ac858/) - difflib patterns

### Tertiary (LOW confidence)
- [SigNoz - Log Aggregation Tools 2026](https://signoz.io/comparisons/log-aggregation-tools/) - Error pattern detection approaches (too enterprise-focused)
- [Visual Studio 2026 Debugging](https://devblogs.microsoft.com/visualstudio/visual-studio-2026-debugging-with-copilot/) - AI-powered debugging (over-engineered for this use case)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - difflib and PyQt6 already in project, well-documented
- Architecture: HIGH - Patterns directly extracted from existing codebase
- Pitfalls: MEDIUM - Based on general Qt/GUI development experience, not project-specific issues yet

**Research date:** 2026-01-18
**Valid until:** 60 days (stable domain - compiler theory and GUI frameworks don't change rapidly)

---

## Key Takeaways for Planning

1. **No new dependencies needed** - Everything builds on existing infrastructure (ValidationResult, CompilationError, DifferenceCategory)

2. **Focus on presentation, not algorithms** - Error categorization already exists in tests, bytecode comparison already exists in validation module. Phase 4 adds UI and aggregation.

3. **Extend existing patterns** - DifferenceTreeView (difference_widgets.py) provides template for ErrorTreeView. Same PyQt6 widget patterns.

4. **Simple is sufficient** - Keyword-based categorization works for diagnostic tool. Don't over-engineer with ML/NLP.

5. **Reproducible steps = markdown checklist** - Not automation, just human-readable "how to reproduce" documentation.

Sources:
- [Syntax and semantic errors - Learn C++](https://www.learncpp.com/cpp-tutorial/syntax-and-semantic-errors/)
- [Semantic Analysis in Compiler Design - GeeksforGeeks](https://www.geeksforgeeks.org/compiler-design/semantic-analysis-in-compiler-design/)
- [Python difflib documentation](https://docs.python.org/3/library/difflib.html)
- [CodeReview - Qt-based diff viewer](https://github.com/FabriceSalvaire/CodeReview)
- [Side-by-side comparison in Python](https://towardsdatascience.com/side-by-side-comparison-of-strings-in-python-b9491ac858/)
- [Log Aggregation Tools 2026 - SigNoz](https://signoz.io/comparisons/log-aggregation-tools/)
- [Visual Studio 2026 Debugging](https://devblogs.microsoft.com/visualstudio/visual-studio-2026-debugging-with-copilot/)
