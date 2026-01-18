# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-17)

**Core value:** Decompiled C code must compile successfully with the original SCMP.exe compiler
**Current focus:** Phase 1 - GUI Validation Integration

## Current Position

Phase: 3 of 9 (CI/CD Pipeline)
Plan: 01 of 3 (complete)
Status: In progress
Last activity: 2026-01-18 - Completed 03-01-PLAN.md

Progress: [████████░░] 11% (4/36 phase plans complete)

## Performance Metrics

**Velocity:**
- Total plans completed: 4
- Average duration: 19 min
- Total execution time: 1.25 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01    | 2/2   | 50min | 25min    |
| 02    | 1/1   | 10min | 10min    |
| 03    | 1/3   | 15min | 15min    |

**Recent Trend:**
- Last 5 plans: 01-01 (15min), 01-02 (35min), 02-01 (10min), 03-01 (15min)
- Trend: Phase 3 plan 01 efficient - one-time infrastructure setup with checkpoints for manual steps

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

### Pending Todos

None yet.

### Blockers/Concerns

**Phase 6-8 (Decompiler Fixes):** Success depends on comprehensive error classification from Phase 4

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

## Session Continuity

Last session: 2026-01-18T13:45:00Z (phase 3 plan 01 completion)
Stopped at: Completed 03-01-PLAN.md (Self-Hosted Runner Setup)
Resume file: None
Next: Execute Phase 3 Plan 02 (Create CI Workflow)

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
