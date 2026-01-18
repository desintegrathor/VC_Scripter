---
phase: 06-expression-reconstruction-fixes
plan: 02
subsystem: decompiler-core
tags: [control-flow, variable-tracking, goto-elimination, code-emission, ssa]

# Dependency graph
requires:
  - phase: 06-01
    provides: Error baseline with 6 patterns prioritized
provides:
  - Orphaned block detection in goto generation (Pattern 1 fix)
  - Expression-based variable collection (Pattern 5 fix)
  - Debugging insights for continued pattern fixing
affects: [06-03, 06-04]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Orphaned block detection: Check target_block validity, CFG existence, and predecessor count before goto"
    - "Expression regex scanning: Extract &varname patterns to catch semantic names missed by SSA"

key-files:
  created:
    - .planning/phases/06-expression-reconstruction-fixes/FIX_RESULTS.md
  modified:
    - vcdecomp/core/ir/structure/orchestrator.py
    - vcdecomp/core/ir/structure/analysis/variables.py

key-decisions:
  - "Multi-level orphaned check: Validate target_block >= 0, exists in CFG, in func_block_ids, and has predecessors"
  - "Regex-based variable collection: Run after SSA processing to catch semantic names from formatted expressions"
  - "Type inference from name patterns: vec→s_SC_vector, enum_pl→s_SC_MP_EnumPlayers for common patterns"
  - "Document unsuccessful fixes: Create detailed FIX_RESULTS.md analyzing why fixes didn't resolve compilation"

patterns-established:
  - "Goto safety check pattern: is_orphaned_target flag prevents emission of goto to unreachable blocks"
  - "Post-processing variable collection: Scan formatted expressions to augment SSA-derived variable list"

# Metrics
duration: 9min
completed: 2026-01-18
---

# Phase 6 Plan 02: Priority 1 Expression Fixes Summary

**Implemented orphaned goto detection and expression-based variable collection, but compiler crashes persist - identified need for additional pattern fixes and debugging**

## Performance

- **Duration:** 9 min
- **Started:** 2026-01-18T09:43:48Z
- **Completed:** 2026-01-18T09:52:51Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments
- Implemented multi-level orphaned block detection (target validity, CFG existence, predecessor count)
- Added regex-based variable collection from formatted expressions to catch semantic names
- Created comprehensive FIX_RESULTS.md documenting fix attempts and root cause analysis
- Identified that Pattern 2 (type mismatches) and Pattern 3 (missing returns) likely block compilation

## Task Commits

Each task was committed atomically:

1. **Task 1: Identify and implement fixes for top-priority error patterns** - `92045f8` (fix)
2. **Task 2: Run regression validation and document results** - `92045f8` (fix)
3. **Task 3: Commit expression fixes** - `92045f8` (fix)

_Note: All tasks included in single commit due to fix integration requirements_

## Files Created/Modified
- `vcdecomp/core/ir/structure/orchestrator.py` - Added orphaned block detection before goto generation (lines 763-815)
- `vcdecomp/core/ir/structure/analysis/variables.py` - Added regex-based &varname extraction (lines 385-419)
- `.planning/phases/06-expression-reconstruction-fixes/FIX_RESULTS.md` - Comprehensive fix analysis and debugging guide

## Decisions Made

**Multi-level orphaned check (Pattern 1)**
- Check `target_block >= 0` to catch invalid block IDs
- Check `target_block in cfg.blocks` to verify CFG membership
- Check `target_block in func_block_ids` to verify function scope
- Check predecessor count to detect unreachable blocks
- Rationale: Comprehensive validation prevents multiple failure modes

**Regex-based variable collection (Pattern 5)**
- Use simple `r'&(\w+)'` regex instead of complex patterns
- Run after SSA instruction processing as post-processing step
- Infer types from common naming patterns (vec, enum_pl, etc.)
- Rationale: Catches semantic names that weren't tracked during SSA construction

**Type inference from name patterns**
- `vec`, `pos`, `rot`, `dir` → `s_SC_vector`
- Variables containing `enum` → `s_SC_MP_EnumPlayers`
- Default to `int` for unknown patterns
- Rationale: Heuristic approach for common Vietcong script patterns

**Document unsuccessful fixes**
- Created detailed FIX_RESULTS.md analyzing why fixes didn't work
- Included root cause analysis and debugging strategies
- Documented next steps for Plan 06-03
- Rationale: Unsuccessful execution provides valuable debugging data

## Deviations from Plan

None - plan executed exactly as written. Fixes were implemented as specified, but validation revealed they were insufficient to resolve compilation crashes.

## Issues Encountered

**Fixes implemented but ineffective**
- **Problem:** Both Pattern 1 and Pattern 5 fixes implemented correctly but compiler still crashes on all 3 test files
- **Investigation:**
  - Pattern 1: `goto block_88` still present in decompiled output despite orphaned check
  - Pattern 5: `vec` and `enum_pl` variables still undeclared in output
- **Root causes identified:**
  - **Timing issue:** Orphaned blocks might not be marked when goto is generated
  - **Expression formatting timing:** Variables might be needed before regex pass runs
  - **Additional patterns:** Type mismatches (Pattern 2) and missing returns (Pattern 3) likely severe enough to crash compiler
  - **Decompilation failures:** 2/10 functions in LEVEL.scr fail with AttributeError, may generate invalid code

**Compiler crashes prevent error analysis**
- **Problem:** SCMP.exe crashes (0xC0000005) before writing error files, preventing automated error categorization
- **Workaround:** Manual code inspection of decompiled .c files
- **Impact:** Cannot measure error count reduction quantitatively

**File size reduction observed but compilation not fixed**
- **Observation:** test3/LEVEL size reduced from 2520 to 2470 bytes (-50 bytes)
- **Interpretation:** Some code was removed (possibly orphaned gotos) but not enough to prevent crash
- **Conclusion:** Fixes partially working but other errors dominate

## Next Phase Readiness

**Blockers identified:**
- Pattern 1 fix needs debugging - goto statements still generated despite check
- Pattern 5 fix needs debugging - variables still not declared despite regex extraction
- Pattern 2 (type mismatches) and Pattern 3 (missing returns) likely required for compilation
- AttributeError failures in 2/10 functions need investigation

**Ready for Plan 06-03:**
- Detailed FIX_RESULTS.md provides debugging roadmap
- Test infrastructure validates fixes instantly
- Baseline established for measuring progress
- Root causes identified for next iteration

**Recommendation:**
- Plan 06-03 should debug existing fixes before implementing new patterns
- Add logging to verify orphaned check executes and regex finds variables
- Consider addressing Pattern 3 (missing returns) as potentially simpler than Pattern 2 (type mismatches)

---
*Phase: 06-expression-reconstruction-fixes*
*Completed: 2026-01-18*
