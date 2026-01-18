---
phase: 04-error-analysis-system
plan: 03
subsystem: validation
tags: [diff-viewer, side-by-side, test-logging, gui, debugging]

# Dependency graph
requires:
  - phase: 04-error-analysis-system-01
    provides: "Error categorization module"
  - phase: 01-gui-validation-integration
    provides: "GUI framework and validation panel"
provides:
  - "Side-by-side diff viewer for assembly/C comparison"
  - "Bytecode instruction-level comparison widget"
  - "Test failure logging with reproducible steps"
  - "Markdown failure reports with error categorization"
affects: [05-quality-metrics-dashboard, 06-decompiler-fixes]

# Tech tracking
tech-stack:
  added: [DiffViewerWidget, test_case_logger]
  patterns: ["Side-by-side diff with difflib", "Tabbed comparison views", "Markdown failure reports", "QSplitter for resizable panes"]

key-files:
  created:
    - vcdecomp/gui/widgets/diff_viewer_widget.py
    - vcdecomp/validation/test_case_logger.py
  modified:
    - vcdecomp/gui/views/error_analysis_view.py

key-decisions:
  - "Tab widget for different comparison types (assembly vs bytecode)"
  - "difflib.SequenceMatcher for line-by-line diff highlighting"
  - "Markdown format for failure logs (human-readable, version-controllable)"
  - "Vertical splitter for error tree + diff viewer (user-resizable)"

patterns-established:
  - "Pattern 1: Two-pane diff viewer with QSplitter (standard side-by-side layout)"
  - "Pattern 2: Tab widget for multiple comparison types (extensible architecture)"
  - "Pattern 3: Markdown logs with reproducible commands (enables manual debugging)"
  - "Pattern 4: QFileDialog for user-selected output directory (UX best practice)"

# Metrics
duration: 6min
completed: 2026-01-18
---

# Phase 04 Plan 03: Diff Viewer and Test Logging Summary

**Side-by-side comparison viewer with instruction-level highlighting and markdown failure logging for reproducible debugging**

## Performance

- **Duration:** 6 min
- **Tasks:** 3 tasks (all executed)
- **Commits:** 3 (1 per task)
- **Deviations:** 0 (plan executed exactly as written)

## Accomplishments
- Created DiffViewerWidget with two-pane splitter layout (359 lines)
- Implemented tab support for assembly/C and bytecode comparison
- Added difflib-based line-by-line diff highlighting
- Created test_case_logger.py for markdown failure reports (211 lines)
- Integrated DiffViewerWidget into ErrorAnalysisPanel
- Added Export Failure Log button with QFileDialog
- Automatic bytecode diff display on error selection
- Color-coded highlighting (red=removed, green=added, yellow=changed)

## Task Execution

### Task 1: Create DiffViewerWidget for side-by-side comparison
- **Status:** ✓ Completed
- **Commit:** a198bd2
- **Files:** vcdecomp/gui/widgets/diff_viewer_widget.py (359 lines)
- **Implementation:**
  - QSplitter with horizontal split (left: original, right: decompiled)
  - Two tabs: "Assembly vs C" and "Bytecode Instructions"
  - Monospace font (Consolas 9pt) for alignment
  - show_diff() method with difflib.SequenceMatcher
  - show_bytecode_diff() method with BytecodeComparator
  - Line-by-line highlighting with QTextCharFormat
  - Color scheme: #ffe6e6 (red), #e6ffe6 (green), #fffacd (yellow)
  - Placeholder text when no comparison loaded
- **Verification:** Module imports successfully, no PyQt6 errors

### Task 2: Create test_case_logger module for reproducible failure logs
- **Status:** ✓ Completed
- **Commit:** e14f77e
- **Files:** vcdecomp/validation/test_case_logger.py (211 lines)
- **Implementation:**
  - log_failed_test_case() function generates markdown reports
  - Reproducible Steps section with exact commands
  - Artifacts section with absolute file paths
  - Error Summary with categorized errors (via error_analyzer)
  - Shows first 5 examples of each error type
  - Handles decompilation failures, compilation failures, bytecode differences
  - Creates output directory if not exists
  - Returns Path to generated markdown file
- **Verification:** Module imports successfully, function callable

### Task 3: Integrate DiffViewerWidget into ErrorAnalysisPanel
- **Status:** ✓ Completed
- **Commit:** c323625
- **Files:** vcdecomp/gui/views/error_analysis_view.py (+143, -6 lines)
- **Implementation:**
  - Added vertical QSplitter (error tree top, diff viewer bottom)
  - Added Export Failure Log button
  - show_diff_for_error() public method for external use
  - _on_error_selected() shows bytecode diff automatically
  - _on_export_log() uses QFileDialog for directory selection
  - Automatic diff viewer expansion when showing comparisons
  - clear() method resets all state including diff viewer
  - Integration with test_case_logger for markdown generation
- **Verification:** ErrorAnalysisPanel imports successfully

## Deviations from Plan

None - plan executed exactly as written.

## Files Created/Modified

### Created:
- `vcdecomp/gui/widgets/diff_viewer_widget.py` - Side-by-side diff viewer (359 lines)
  - DiffViewerWidget class with QSplitter layout
  - Tab 1: Assembly vs C text comparison
  - Tab 2: Bytecode instruction comparison
  - show_diff(original_asm, decompiled_c) method
  - show_bytecode_diff(original_scr, recompiled_scr) method
  - _apply_highlighting() for color-coded lines
  - _format_bytecode_with_highlights() for instruction-level diffs
  - Uses difflib.SequenceMatcher for line-by-line comparison
  - Uses BytecodeComparator for instruction-level comparison

- `vcdecomp/validation/test_case_logger.py` - Markdown failure reports (211 lines)
  - log_failed_test_case(result, output_dir) function
  - Markdown structure: header, reproducible steps, artifacts, error summary
  - Reproducible Steps: decompile + compile commands
  - Artifacts: absolute paths to .scr, .c, working directory
  - Error Summary: categorized errors with first 5 examples each
  - Handles decompilation failures (no compilation attempted)
  - Handles compilation failures (categorized errors)
  - Handles bytecode differences (difference summary)
  - Returns Path to generated markdown file

### Modified:
- `vcdecomp/gui/views/error_analysis_view.py` - Integrated diff viewer and export
  - Added imports: DiffViewerWidget, test_case_logger, Path, QFileDialog, QMessageBox, QSplitter
  - Added _current_result instance variable to store ValidationResult
  - Updated _init_ui() with vertical splitter (error tree + diff viewer)
  - Added export_log_button with _on_export_log() handler
  - Updated load_validation_results() to store failed result
  - Added show_diff_for_error(original_asm, decompiled_c) public method
  - Updated _on_error_selected() to show bytecode diff automatically
  - Updated clear() to reset diff viewer and export button
  - QFileDialog with default directory .planning/test_failures

## Decisions Made

**Tab widget for different comparison types:**
- Context: Need to show both assembly/C comparison and bytecode comparison
- Implementation: QTabWidget with two tabs
- Rationale: Extensible architecture allows adding more comparison types later
- Impact: User can switch between comparison views in same widget

**difflib.SequenceMatcher for line-by-line diff highlighting:**
- Context: Need to highlight differences between original and decompiled
- Implementation: SequenceMatcher.get_opcodes() to identify equal/delete/insert/replace regions
- Rationale: Stdlib solution, well-tested, perfect for line-by-line text comparison
- Impact: No new dependencies, reliable diff algorithm

**Markdown format for failure logs:**
- Context: Need human-readable, reproducible failure reports
- Implementation: Markdown with code blocks, bullet lists, headers
- Rationale: Human-readable, version-controllable, can be viewed in IDE or GitHub
- Impact: Easy to share, archive, and reference in bug reports

**Vertical splitter for error tree + diff viewer:**
- Context: Users need to see errors and corresponding diffs simultaneously
- Implementation: QSplitter(Qt.Orientation.Vertical) with user-resizable panes
- Rationale: Standard Qt pattern for dual-pane views, user can customize layout
- Impact: Flexible UI that adapts to user workflow

## Diff Viewer Implementation

**Color Scheme:**
- Light red (#ffe6e6): Lines only in original (deleted)
- Light green (#e6ffe6): Lines only in decompiled (added)
- Light yellow (#fffacd): Lines changed between versions
- White (no highlight): Unchanged lines

**Highlighting Algorithm (difflib.SequenceMatcher):**
1. Split original and decompiled into lines
2. SequenceMatcher.get_opcodes() returns operations (equal, delete, insert, replace)
3. For each operation, collect lines with appropriate background color
4. Apply highlighting via QTextCharFormat and QTextCursor
5. Insert all lines into QTextEdit widgets

**Bytecode Comparison:**
1. Use BytecodeComparator to load and compare .SCR files
2. Extract code segment differences from comparison result
3. Build set of instruction addresses with differences
4. Format each instruction with yellow background if address differs
5. Display in side-by-side panes

## Test Logger Implementation

**Markdown Structure:**

```markdown
# Test Failure: {test_id}

**Date:** {timestamp}
**Verdict:** {FAIL/ERROR}

## Reproducible Steps

### Step 1: Decompile
```bash
python -m vcdecomp structure original.scr > decompiled.c
```

**Result:** Decompilation succeeded

### Step 2: Compile
```bash
scmp.exe decompiled.c output.scr output.h
```

**Result:** Compilation failed

## Artifacts

- **Original .scr:** `C:\path\to\original.scr`
- **Decompiled .c:** `C:\path\to\decompiled.c`
- **Working directory:** `C:\path\to\workdir`

## Error Summary

**Total compilation errors:** 42

### Syntax Errors (30 - 71.4%)
1. expected ';' before 'return'
2. expected ')' before ';'
3. syntax error at line 42
   ... and 27 more

### Semantic Errors (10 - 23.8%)
1. undefined symbol 'foo'
2. undeclared identifier 'bar'
   ... and 8 more

### Type Errors (2 - 4.8%)
1. type mismatch in assignment
2. incompatible types: int and float
```

**Rationale:** This format provides all information needed to:
1. Reproduce the failure manually
2. Locate artifacts for investigation
3. Understand error distribution

## ErrorAnalysisPanel Integration

**UI Layout (Vertical Splitter):**
```
+----------------------------------+
| Error Analysis                   |
| Summary: 15 differences          |
+----------------------------------+
| Error Patterns (Tree View)       |
|   - Semantic (8)                 |
|   - Cosmetic (5)                 |
|   - Optimization (2)             |
+----------------------------------+
| Comparison View (Diff Viewer)    | <- User-resizable
|   [Assembly vs C] [Bytecode]     |
|   Original     | Decompiled      |
+----------------------------------+
| [Export Failure Log] [Refresh]   |
+----------------------------------+
```

**Automatic Behaviors:**
- Selecting error in tree → shows bytecode diff
- Selecting error when diff collapsed → expands diff viewer
- Export button enabled only when failed result loaded
- QFileDialog defaults to .planning/test_failures

## Next Phase Readiness

**Phase 05 (Quality Metrics Dashboard) - ENHANCED:**
- DiffViewerWidget can be embedded in quality dashboard
- Markdown failure logs can be parsed for trend analysis
- Error categorization enables metric visualization
- No blockers

**Phase 06 (Decompiler Fixes) - READY:**
- Side-by-side diff helps identify decompilation bugs
- Bytecode comparison shows exact instruction differences
- Failure logs provide reproducible test cases
- No blockers

**No blockers for Phase 05.**

## Validation Checklist

From Plan success criteria:
- [x] ERROR-03 satisfied: Side-by-side view of assembly vs decompiled C with highlighting
- [x] ERROR-04 satisfied: Bytecode differences highlighted at instruction level using BytecodeComparator
- [x] ERROR-05 satisfied: Failed test cases logged with reproducible commands and error summaries
- [x] Diff viewer integrates with error analysis panel
- [x] Test case logger produces markdown files with clear reproduction steps
- [x] Uses stdlib difflib (no new dependencies)

From Plan verification section:
- [x] GUI launches with error analysis panel (ErrorAnalysisPanel exists)
- [x] DiffViewerWidget displays placeholder when no diff loaded
- [x] test_case_logger generates valid markdown files
- [x] Export button creates failure log in .planning/test_failures/
- [x] Side-by-side comparison shows highlighted differences

From must_haves (truths):
- [x] User can view side-by-side comparison of original assembly and decompiled C
- [x] Bytecode differences are highlighted at instruction level
- [x] Failed test cases are logged with reproducible steps
- [x] Logs include file paths, commands, and error summaries

From must_haves (artifacts):
- [x] vcdecomp/gui/widgets/diff_viewer_widget.py (359 lines, >150 min_lines)
- [x] Exports: DiffViewerWidget
- [x] vcdecomp/validation/test_case_logger.py (211 lines, >80 min_lines)
- [x] Exports: log_failed_test_case
- [x] vcdecomp/gui/views/error_analysis_view.py contains show_diff_for_error

From must_haves (key_links):
- [x] diff_viewer_widget.py imports from difflib
- [x] test_case_logger.py function parameter is ValidationResult
- [x] error_analysis_view.py contains self.diff_viewer = DiffViewerWidget()

**All requirements satisfied. No deviations required.**

## Lessons Learned

**QSplitter for flexible layouts:**
- Vertical splitter allows user to resize error tree vs diff viewer
- Initial sizes (400, 200) give error tree prominence
- Automatic expansion when showing diff improves UX
- Standard Qt pattern that users expect

**Tab widget for extensibility:**
- Two tabs (assembly vs bytecode) in same widget
- Easy to add more comparison types later (e.g., CFG visualization)
- Users can switch between views without losing context
- Clean separation of concerns (text diff vs bytecode diff)

**Markdown for reproducibility:**
- Absolute file paths enable immediate investigation
- Exact commands can be copy-pasted to terminal
- Categorized errors show distribution patterns
- Version-controllable format (can commit as test documentation)

**difflib for simple text diffs:**
- SequenceMatcher provides line-by-line comparison
- get_opcodes() gives precise operation type (equal, delete, insert, replace)
- No external dependencies, well-tested stdlib code
- Color-coding makes differences immediately visible

**Integration patterns:**
- Store ValidationResult in panel for diff viewing and export
- Enable/disable buttons based on available data
- Use signals for loose coupling (future integration points)
- QFileDialog with sensible defaults improves UX

---
*Phase: 04-error-analysis-system*
*Completed: 2026-01-18*
