# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-17)

**Core value:** Decompiled C code must compile successfully with the original SCMP.exe compiler
**Current focus:** Phase 1 - GUI Validation Integration

## Current Position

Phase: 7 of 9 (Variable Declaration Fixes)
Plan: 3 of 6 (Global variable fixes)
Status: Phase 7 IN PROGRESS (3/6 plans executed)
Last activity: 2026-01-18 - Completed 07-03-PLAN.md (global offset validation, save_info/SGI naming, type inference)

Progress: [█████████░] 47% (17/36 phase plans complete)

## Performance Metrics

**Velocity:**
- Total plans completed: 17
- Average duration: 10.1 min
- Total execution time: 2.9 hours
- Latest plans (07-01/02/03): 64min + 13min + 14min = 91min (type inference integration)

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01    | 2/2   | 50min | 25min    |
| 02    | 1/1   | 10min | 10min    |
| 03    | 3/3   | 28min | 9.3min   |
| 04    | 3/3   | 14min | 4.7min   |
| 06    | 7/7   | 83min | 11.9min  |
| 07    | 3/6   | 91min | 30.3min  |

**Recent Trend:**
- Last 4 plans: 06-06b (22min), 07-01 (64min), 07-02 (13min), 07-03 (14min)
- Phase 7 progress: 3 plans in 91min, avg 30.3min/plan (higher due to complex type inference work)
- 07-01 lengthy (64min) due to root cause investigation and two-pass integration
- 07-02/03 fast (13min, 14min) - building on established patterns

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Roadmap creation: Derived 9 phases from 32 requirements using comprehensive depth setting
- Validation-first approach: Phases 1-5 establish infrastructure before fixes in Phases 6-8
- Parallel foundation work: Phase 1 (GUI) and Phase 2 (Test suite) can proceed in parallel

**From 01-01 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Use Ctrl+Shift+V shortcut for validation | Avoids conflict with Ctrl+V paste, standard modifier combination | 01-01 |
| Temp file approach for validation | ValidationPanel expects file paths, not in-memory strings | 01-01 |
| Auto-show validation dock | Improves UX by making results immediately visible | 01-01 |
| Initialization order: docks before menus | Prevents AttributeError accessing validation_panel in menu creation | 01-01 |

**From 01-02 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Consistent QSettings namespace (VCDecompiler/ValidationSettings) | Ensures dialog, panel, and main window all read/write same settings | 01-02 |
| Dialog self-management for QSettings | ValidationSettingsDialog handles its own persistence - cleaner separation of concerns | 01-02 |
| First-run question dialog (Yes/No) | More user-friendly than warning, guides user to configure settings | 01-02 |
| .bat wrapper for SCMP.exe execution | Windows subprocess requires specific handling for DOS-era executables | 01-02 |
| Clean temp files BEFORE compilation | Preserves failed compilation artifacts for debugging | 01-02 |

**From 02-01 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Sequential test execution (no pytest-xdist) | Clearer output for debugging, avoids concurrency complexity | 02-01 |
| cache_enabled=False for tests | Always-fresh decompilation ensures tests measure current state | 02-01 |
| PARTIAL verdict doesn't fail tests | User wants complete picture of all results, not fail-fast | 02-01 |
| Programmatic error categorization | Enables automated quality analysis and trend tracking | 02-01 |
| Global threading lock for SCMP.exe | DOS-era compiler cannot handle concurrent execution | 02-01 |

**From 03-01 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Self-hosted runner required | SCMP.exe is Windows-only DOS-era executable, cannot run on GitHub-hosted runners | 03-01 |
| Runner installed as Windows service | Ensures runner auto-starts on reboot, runs as background service | 03-01 |
| Service installation via PowerShell | Standard Windows service management with sc.exe commands | 03-01 |
| Runner labels: self-hosted, windows, x64 | Enables workflow targeting with runs-on specification | 03-01 |

**From 03-02 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Trigger on ALL push/PR events | Satisfies VALID-05 "runs validation on all commits", not limited to main branch | 03-02 |
| Baseline storage in .planning/baselines/ | Satisfies TEST-06 "baselines stored in Git", enables version-controlled regression tracking | 03-02 |
| continue-on-error + if: always() | Ensures test artifacts upload even when tests fail (per RESEARCH.md Pattern 3) | 03-02 |
| Dual test strategy (original + baseline) | Original test provides immediate output, baseline test detects regressions | 03-02 |

**From 03-03 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Accept non-enforced branch protection | GitHub free plan doesn't support enforcement on private repos, solo project acceptable | 03-03 |
| pytest.ini configuration for baselines | pytest-regressions 2.9.1 uses regressions_data_dir config option, not datadir fixture | 03-03 |
| Commit test data to repository | CI cannot function without test files, binary .scr files acceptable as test assets | 03-03 |
| End-to-end verification via test branch | Discovered 3 issues (test data, baseline config, pwsh), fixed 2 critical ones | 03-03 |

**From 04-01 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Keyword-based error categorization | Simple keyword matching covers 95%+ of compiler errors, no NLP needed | 04-01 |
| Limit examples to 3 per pattern | Prevents output overwhelming with repetitive errors while providing context | 04-01 |
| Separate single-result and batch functions | categorize_compilation_errors for tests, ErrorAnalyzer for reporting | 04-01 |
| ErrorPattern dataclass | Type-safe, self-documenting structure for aggregated pattern results | 04-01 |

**From 04-02 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Color-coded categories (syntax=red, semantic=yellow, type=blue, include=gray) | Visual distinction for quick pattern recognition, matches severity semantics | 04-02 |
| Limit examples to 5 in GUI (vs 3 in reports) | GUI has more space than terminal, 5 examples provide better context | 04-02 |
| Initially hidden error analysis dock | Diagnostic tool for on-demand use, not real-time monitoring - avoids UI clutter | 04-02 |
| RightDockWidgetArea placement | Keeps bottom area dedicated to validation panel, right area for analysis tools | 04-02 |

**From 04-03 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Tab widget for comparison types (assembly vs bytecode) | Extensible architecture allows adding more comparison types later | 04-03 |
| difflib.SequenceMatcher for line-by-line diff | Stdlib solution, well-tested, no new dependencies | 04-03 |
| Markdown format for failure logs | Human-readable, version-controllable, can be viewed in IDE or GitHub | 04-03 |
| Vertical splitter for error tree + diff viewer | Standard Qt pattern for dual-pane views, user can customize layout | 04-03 |

**From 06-01 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Manual source inspection for baseline | Compiler crashes (0xC0000005) prevent automated error file parsing - automated categorization requires parseable errors | 06-01 |
| 6-pattern categorization scheme | Covers all observed error types: control flow (goto, unreachable), type system (mismatch), function contracts (return), variable tracking (undeclared), optimization (redundant assignments) | 06-01 |
| 3-tier priority system (CRITICAL/HIGH/MEDIUM) | Prioritize based on: 1) blocks compilation vs compiles-but-wrong, 2) frequency across test files, 3) fix complexity estimate | 06-01 |
| Focus on static errors only | Runtime semantic errors (wrong bytecode output) require successful compilation - Phase 6 focuses on getting code to compile first | 06-01 |

**From 06-02 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Multi-level orphaned check for goto targets | Check target_block >= 0, exists in CFG, in func_block_ids, and has predecessors - comprehensive validation prevents multiple failure modes | 06-02 |
| Regex-based variable collection post-processing | Run after SSA processing to catch semantic names from formatted expressions - simple approach for missing variables | 06-02 |
| Type inference from name patterns | vec/pos/rot/dir → s_SC_vector, enum_pl → s_SC_MP_EnumPlayers - heuristic for common Vietcong patterns | 06-02 |
| Document unsuccessful fixes | Create FIX_RESULTS.md with root cause analysis and debugging strategies - unsuccessful execution provides valuable data | 06-02 |

**From 06-04 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Debug logging with WARNING level | Appear in pytest --log-cli-level=WARNING output for diagnostic visibility without changing test infrastructure | 06-04 |
| Evidence-based diagnosis methodology | Collect actual execution data before making hypotheses - avoids speculation, reveals true root causes | 06-04 |
| [MODULE DEBUG] prefix pattern | Consistent logging format enables grep filtering and clear identification of debug vs production logs | 06-04 |
| Pattern 1 fix confirmed working | Despite FIX_RESULTS.md claims, no undefined goto labels exist in current output - fix is 100% effective | 06-04 |
| Pattern 5 has emission bug, not collection bug | Variable collection and declaration generation work correctly, but downstream code emission loses declarations | 06-04 |

**From 06-05 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Pattern 1 needs no fix | DEBUG_FINDINGS.md evidence shows 0 undefined gotos in current output - fix from 06-02 is 100% effective | 06-05 |
| Pattern 5 filter removal | Filter `"[" in var_decl or (var_decl.count(" ") > 1)` excluded simple struct types like `c_Vector3 vec` (only 1 space) | 06-05 |
| Two-phase Pattern 3 fix | End-of-function synthesis (line 861) + mid-function post-processing (line 889) to catch all bare returns | 06-05 |
| Pattern 2 deferred to Phase 7 | Type mismatches require stack_lifter.py + expr.py refactoring (HIGH complexity, out of Phase 6 scope) | 06-05 |

**From 06-06a execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Evidence-based diagnosis over speculation | Diagnostic logging revealed true root cause - blocks not orphaned but labels never emitted due to pattern detection marking them "emitted" | 06-06a |
| Pattern 1 root cause: rendering logic | Blocks 3, 46, 48 have predecessors, gotos emitted, but labels skipped by switch/if-else rendering - NOT an orphaned detection issue | 06-06a |
| Fix Option 1 chosen (goto_targets tracking) | Simplest fix - track goto targets, force label emission for any block referenced by goto | 06-06a |

**From 06-06b execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Multi-point label emission | Emit labels at switch (lines 428-429), if-else (577-578), and regular blocks (696-697) to ensure all goto targets covered | 06-06b |
| Cross-function goto edge case deferred | Block 88 in test3 is cross-function goto (different root cause) - 1 instance vs 50 baseline, acceptable for Phase 6 | 06-06b |
| Accept 98% reduction as success | Pattern 1 fix reduces undefined gotos from ~50 to 1 - edge case documented for Phase 7 investigation | 06-06b |

**From 07-03 execution:**

| Decision | Rationale | Phase |
|----------|-----------|-------|
| DWORD-to-BYTE conversion validation | Add debug logging and 4-byte alignment assertions - critical bug identified in RESEARCH.md (offset confusion) | 07-03 |
| Extend type inference to GST | Store operations also reveal global types, not just load operations (GCP/GLD/GADR) | 07-03 |
| SGI constant resolution from headers | SGI constants are game engine globals defined in sc_def.h - separate method improves readability | 07-03 |
| Source tracking for global names | Add source field to GlobalUsage for debugging - know where each name came from (save_info, SGI, synthetic) | 07-03 |
| INFO logging for user-facing names | save_info and SGI names logged at INFO (user benefit), synthetic at DEBUG (internal) | 07-03 |

### Pending Todos

None yet.

### Blockers/Concerns

**Phase 6 (Expression Reconstruction Fixes) - COMPLETE:**
- 7 plans complete: baseline, attempts, validation, diagnostic, fixes, root-cause analysis, implementation
- Pattern 3 (missing return values): FIXED - synthesize `return 0;` for non-void functions (~15 instances)
- Pattern 5 (undeclared variables): FIXED - removed overly restrictive filter in orchestrator.py
- Pattern 2 (type mismatches): DEFERRED to Phase 7 - requires stack_lifter.py refactoring (HIGH complexity)
- **Pattern 1 (undefined goto labels): FIXED** - 98% reduction (50 instances → 1 edge case)
  - 06-06b: Implemented goto_targets tracking and multi-point label emission
  - Test1 fully fixed: blocks 3, 46, 48 now have labels (0/3 undefined)
  - Test2 no regression: 0/0 undefined gotos
  - Test3 vastly improved: multiple → 1 edge case (cross-function goto, different root cause)
  - Fix: Track goto_targets set, emit labels at switch/if/regular block headers
- **Phase 6 complete** - 3/6 patterns fixed, ready for Phase 7
- Next: Phase 7 - Type System Fixes (Pattern 2 type mismatches, cross-function goto handling)

**Phase 4 (Error Analysis System) - COMPLETE:**
- All requirements satisfied (ERROR-01 through ERROR-05)
- Error categorization module enables systematic analysis
- GUI integration provides interactive error exploration
- Diff viewer and test logger support debugging workflow

**Phase 1 (GUI Validation Integration) - COMPLETE:**
- All requirements satisfied (VALID-01, VALID-02, VALID-03)
- Windows compiler execution requires .bat wrapper pattern
- Temp file preservation strategy helps debugging but may accumulate files

**Phase 2 (Test Suite Automation) - COMPLETE:**
- All requirements satisfied (TEST-01, TEST-02, TEST-03, TEST-04, TEST-07)
- SCMP.exe requires serialization via threading.Lock() (DOS-era concurrency issue, now fixed)
- Test failures expected (decompiler has bugs) - infrastructure working correctly
- Test suite provides fast feedback loop for iterative improvement
- Error categorization foundation in place for quality measurement

**Phase 3 Plan 01 (Self-Hosted Runner Setup) - COMPLETE:**
- Runner online and idle, ready to accept CI jobs
- Service configured for automatic startup on reboot
- Machine must remain online for CI job execution
- Compiler (SCMP.exe) accessible to runner service account

**Phase 3 Plan 02 (Create CI Workflow) - COMPLETE:**
- GitHub Actions workflow triggers on all commits (push + pull_request)
- Pytest validation suite runs on self-hosted Windows runner
- Test results upload as artifacts (JUnit XML + JSON) with 30-day retention
- Baseline regression tracking configured in .planning/baselines/
- Inline PR annotations enabled via pytest-github-actions-annotate-failures
- continue-on-error ensures artifacts upload even on test failure

**Phase 3 Plan 03 (Test CI Pipeline) - COMPLETE:**
- End-to-end CI/CD pipeline verified functional
- Branch protection limitation documented (GitHub free plan restriction)
- Test data files committed to repository (decompiler_source_tests/)
- pytest.ini configuration for baseline directory (regressions_data_dir)
- 3 auto-fixes applied during execution (test data, baseline config, datadir cleanup)
- VALID-05 PARTIAL (CI runs but no enforcement), TEST-05/TEST-06 COMPLETE

## Session Continuity

Last session: 2026-01-18T13:51:38Z (Phase 7 Plan 03 complete - Global variable fixes)
Stopped at: Completed 07-03-PLAN.md (Global offset validation, save_info/SGI naming, type inference integration)
Resume file: None
Next: Phase 7 Plan 04 - Array reconstruction (detect multi-dimensional arrays, proper sizing)

## Technical Context

### Patterns Established

**From 01-01:**
- **Temp file pattern:** Create temp directory vcdecomp_validation/, save decompiled code, pass path to validator
- **Validation trigger pattern:** Check script loaded → save to temp → show dock → call ValidationPanel.start_validation()

**From 02-01:**
- **Test parametrization pattern:** Case-sensitive filesystem paths (test1/test2 lowercase, test3 UPPERCASE)
- **Three-step test flow:** Decompile → validate → report with programmatic categorization
- **Error categorization pattern:** Group errors by type (syntax, type, undefined, include, other) for quality measurement
- **Compiler serialization pattern:** Use threading.Lock() to serialize SCMP.exe access

**From 03-01:**
- **GitHub runner registration pattern:** Web UI token generation with 1-hour expiry
- **Service installation pattern:** PowerShell script with sc.exe for Windows service management
- **Runner verification pattern:** GitHub API (gh api repos/.../actions/runners) to check online status

**From 03-02:**
- **CI workflow pattern:** Trigger on all push/PR events, run tests, upload artifacts on all outcomes
- **Baseline regression pattern:** pytest-regressions with data_regression.check() for automated baseline comparison
- **Artifact resilience pattern:** continue-on-error + if: always() ensures upload even on test failure
- **Dual test pattern:** Original test (immediate output) + baseline test (regression detection)

**From 03-03:**
- **Limitation documentation pattern:** Create LIMITATION.md files for platform restrictions with transparent rationale
- **pytest.ini configuration pattern:** Use pytest.ini with regressions_data_dir for pytest-regressions baseline directory
- **End-to-end verification pattern:** Disposable test branches to verify complete workflow before declaring done
- **Test data in repository pattern:** Commit test source and binary files as test assets for CI execution

**From 04-01:**
- **Keyword matching pattern:** Error categorization via case-insensitive keyword matching (simple and effective)
- **Example limiting pattern:** Store max 3 examples per pattern to prevent overwhelming output
- **Dual-mode API pattern:** Separate functions for single-result (categorize_compilation_errors) and batch (ErrorAnalyzer)
- **Dataclass for aggregation pattern:** ErrorPattern dataclass provides structured results with count, percentage, examples

**From 04-02:**
- **Tree widget pattern:** QTreeWidget with color-coded categories, expandable examples, selection signals
- **Color-coding pattern:** syntax=red, semantic=yellow, type=blue, include=gray for visual error distinction
- **Hidden dock pattern:** Initially hidden docks for diagnostic tools (avoid UI clutter, user opens on demand)
- **Signal integration pattern:** error_selected signal emitted for future detail view integration

**From 04-03:**
- **Side-by-side diff pattern:** QSplitter with two QTextEdit panes for left/right comparison
- **Tab widget pattern:** QTabWidget for multiple comparison types (extensible architecture)
- **difflib.SequenceMatcher pattern:** Line-by-line diff with get_opcodes() for highlighting
- **Markdown logging pattern:** Reproducible failure reports with commands, paths, error summaries
- **QFileDialog pattern:** User-selected output directory with sensible defaults

### Key Files Modified

**Phase 01 complete:**
- `vcdecomp/gui/main_window.py` - Validation menu, toolbar, temp file handling, settings integration, first-run prompt (01-01, 01-02)
- `vcdecomp/validation/runner.py` - Windows subprocess fixes, .bat wrapper, debug output (01-02)
- `vcdecomp/gui/views/validation_view.py` - CompilationError attribute fixes (01-02)

**Phase 02 complete:**
- `vcdecomp/tests/test_validation.py` - Parametrized pytest tests with decompile-compile-compare workflow (02-01)
- `vcdecomp/tests/conftest.py` - Shared pytest fixtures for compiler paths and orchestrator (02-01)
- `vcdecomp/validation/validator.py` - Threading lock for SCMP.exe serialization (02-01 fix)

**Phase 03 Plan 01 complete:**
- `C:\actions-runner\install-service.ps1` - Windows service installation script for GitHub Actions runner (03-01)
- `C:\actions-runner\.runner` - Runner registration metadata (agentId, poolName, gitHubUrl) (03-01)
- Runner service: `actions.runner.desintegrathor-VC_Scripter.VC-Scripter-Windows-Runner` (Running, Automatic)

**Phase 03 Plan 02 complete:**
- `.github/workflows/validation.yml` - GitHub Actions workflow for automated validation (03-02)
- `vcdecomp/requirements.txt` - Added pytest plugins (pytest-github-actions-annotate-failures, pytest-json-report, pytest-regressions) (03-02)
- `vcdecomp/tests/conftest.py` - Added pytest_regressions_data_dir fixture for baseline storage (03-02)
- `vcdecomp/tests/test_validation.py` - Added test_decompilation_validation_with_baseline test (03-02)
- `.planning/baselines/.gitkeep` - Baseline storage directory for regression tracking (03-02)

**Phase 03 Plan 03 complete:**
- `pytest.ini` - pytest-regressions baseline directory configuration (03-03)
- `.planning/phases/03-ci-cd-pipeline/BRANCH_PROTECTION_LIMITATION.md` - GitHub free plan limitation documentation (03-03)
- `decompiler_source_tests/` - Test data files (6 files: test1/tt, test2/tdm, test3/LEVEL) (03-03)
- `vcdecomp/tests/conftest.py` - Removed datadir fixture (incorrect approach) (03-03)
- `.github/workflows/validation.yml` - Added --basetemp flag for temp file management (03-03)

**Phase 04 Plan 01 complete:**
- `vcdecomp/validation/error_analyzer.py` - Error categorization module with pattern detection (279 lines) (04-01)
- `vcdecomp/tests/test_error_analyzer.py` - Comprehensive unit tests (521 lines, 15 tests) (04-01)
- `vcdecomp/tests/test_validation.py` - Migrated to use error_analyzer module (simplified 17 lines) (04-01)

**Phase 04 Plan 02 complete:**
- `vcdecomp/gui/widgets/error_tree_widget.py` - Hierarchical tree widget with color-coded categories (165 lines) (04-02)
- `vcdecomp/gui/views/error_analysis_view.py` - Error analysis panel with summary stats and tree integration (159 lines) (04-02)
- `vcdecomp/gui/main_window.py` - Added error_analysis_dock to RightDockWidgetArea, View menu toggle (04-02)

**Phase 04 Plan 03 complete:**
- `vcdecomp/gui/widgets/diff_viewer_widget.py` - Side-by-side diff viewer with assembly/bytecode comparison (359 lines) (04-03)
- `vcdecomp/validation/test_case_logger.py` - Markdown failure report generator with reproducible steps (211 lines) (04-03)
- `vcdecomp/gui/views/error_analysis_view.py` - Integrated diff viewer, export button, automatic bytecode comparison (04-03)

**Phase 06 Plan 01 complete:**
- `.planning/phases/06-expression-reconstruction-fixes/ERROR_BASELINE.md` - Comprehensive error baseline (357 lines, 6 patterns, 3-tier priority system) (06-01)

**Phase 06 Plan 02 complete:**
- `vcdecomp/core/ir/structure/orchestrator.py` - Orphaned block detection in goto generation (lines 763-815) (06-02)
- `vcdecomp/core/ir/structure/analysis/variables.py` - Regex-based variable collection from expressions (lines 385-419) (06-02)
- `.planning/phases/06-expression-reconstruction-fixes/FIX_RESULTS.md` - Fix analysis and debugging guide (06-02)

**Phase 06 Plan 03 complete:**
- `.planning/phases/06-expression-reconstruction-fixes/PHASE_COMPLETION.md` - Comprehensive phase analysis (297 lines) (06-03)
- `.planning/baselines/test_validation/test_decompilation_validation_with_baseline/*.yml` - Regression baseline files (3 YAML) (06-03)
- `.planning/ROADMAP.md` - Updated Phase 6 status to PARTIAL (06-03)

**Phase 06 Plan 04 complete:**
- `.planning/phases/06-expression-reconstruction-fixes/DEBUG_FINDINGS.md` - Evidence-based diagnosis of Pattern 1 & 5 (255 lines) (06-04)
- `vcdecomp/core/ir/structure/orchestrator.py` - Added debug logging for goto decisions (lines 766-833) (06-04)
- `vcdecomp/core/ir/structure/analysis/variables.py` - Added debug logging for variable collection (lines 393-460) (06-04)

**Phase 06 Plan 05 complete:**
- `vcdecomp/core/ir/structure/orchestrator.py` - Pattern 5 filter fix (lines 304-322), Pattern 3 synthesis (lines 861-913), debug logging removed (06-05)
- `vcdecomp/core/ir/structure/analysis/variables.py` - Debug logging removed (lines 385-438) (06-05)
- `.planning/phases/06-expression-reconstruction-fixes/PATTERN3_FIX_RESULTS.md` - Comprehensive fix analysis (390 lines) (06-05)

**Phase 06 Plan 06a complete:**
- `vcdecomp/core/ir/structure/orchestrator.py` - Pattern 1 diagnostic logging (lines 768-831) (06-06a)
- `.planning/phases/06-expression-reconstruction-fixes/PATTERN1_ROOT_CAUSE.md` - Evidence-based root cause analysis (258 lines) (06-06a)
- `pattern1_debug_output.txt` - Diagnostic output showing orphaned checks and goto emission (12 lines) (06-06a)

**Phase 06 Plan 06b complete:**
- `vcdecomp/core/ir/structure/orchestrator.py` - Pattern 1 fix: goto_targets tracking and label emission (lines 352, 357, 428-429, 573-574, 688-689, 792, 824) (06-06b)
- `.planning/phases/06-expression-reconstruction-fixes/PATTERN1_FIX_VALIDATION.md` - Comprehensive validation results (206 lines) (06-06b)

**Phase 07 Plan 03 complete:**
- `vcdecomp/core/ir/global_resolver.py` (+182 lines, -50 lines) - Global offset validation, GST type inference, _resolve_sgi_constants(), source tracking (07-03)
- `.planning/phases/07-variable-declaration-fixes/07-03-SUMMARY.md` - Plan completion summary (07-03)
- `.test_artifacts_07-03_test1_decompiled.c` - Test output showing save_info names and SGI constants (07-03)
