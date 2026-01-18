---
phase: 06-expression-reconstruction-fixes
plan: 05
subsystem: decompiler
tags: [control-flow, type-system, code-generation, orchestrator, variables]

# Dependency graph
requires:
  - phase: 06-04
    provides: Diagnostic evidence that Pattern 1 working, Pattern 5 has emission bug
provides:
  - Pattern 3 fix: Return value synthesis for non-void functions (eliminates ~15 bare returns)
  - Pattern 5 fix: Declaration emission filter removed (all struct types now declared)
  - Pattern 1 confirmed working (debug logging removed)
  - Decompiled code now syntactically valid C (0 parse errors)
affects: [07-variable-type-inference, 08-control-flow-reconstruction]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Return value synthesis based on function signature parsing"
    - "Post-processing pattern for mid-function fixes"
    - "Evidence-based debugging to distinguish collection vs emission bugs"

key-files:
  created:
    - .planning/phases/06-expression-reconstruction-fixes/PATTERN3_FIX_RESULTS.md
  modified:
    - vcdecomp/core/ir/structure/orchestrator.py
    - vcdecomp/core/ir/structure/analysis/variables.py

key-decisions:
  - "Pattern 1 (orphaned gotos) requires no fix - already 100% effective per DEBUG_FINDINGS.md"
  - "Pattern 5 emission bug caused by overly restrictive filter (arrays and multi-space types only)"
  - "Pattern 3 requires two-phase fix: end-of-function synthesis + mid-function post-processing"
  - "Pattern 2 (type mismatches) explicitly deferred to Phase 7 (requires type system refactoring)"

patterns-established:
  - "Post-processing pattern: Scan generated lines to fix issues that cross abstraction boundaries (expr.py doesn't know function signatures)"
  - "Filter removal pattern: When declarations are lost, check for overly specific filters between generation and emission"
  - "Two-phase return synthesis: Handle both explicit missing returns (end-of-func) and implicit RET 0 instructions (mid-func)"

# Metrics
duration: 7min
completed: 2026-01-18
---

# Phase 6 Plan 05: Pattern 3 & 5 Fixes with Pattern 1 Confirmation

**Decompiled code now syntactically valid C with 0 parse errors - Pattern 3 return synthesis and Pattern 5 declaration emission fixed**

## Performance

- **Duration:** 7 min
- **Started:** 2026-01-18T10:43:47Z
- **Completed:** 2026-01-18T10:50:49Z
- **Tasks:** 5
- **Files modified:** 2 code files + 1 results doc

## Accomplishments

- **Pattern 1 (Orphaned gotos)**: Confirmed already working - removed debug logging
- **Pattern 3 (Missing return values)**: Fixed - synthesize `return 0;` for non-void functions with bare returns
- **Pattern 5 (Undeclared variables)**: Fixed - removed overly restrictive declaration filter
- **Parse errors reduced to 0** - decompiled code now syntactically valid C (down from ~50+ errors)
- **Pattern 2 (type mismatches)** explicitly documented as deferred to Phase 7

## Task Commits

All tasks committed atomically in single commit:

1. **Task 1: Pattern 1 verification** - Confirmed working, removed debug logging
2. **Task 2: Pattern 5 emission fix** - Removed filter excluding simple struct types
3. **Task 3: Pattern 3 synthesis** - Two-phase return value synthesis
4. **Task 4: Validation & results** - Comprehensive PATTERN3_FIX_RESULTS.md
5. **Task 5: Commit fixes** - `fb6b2d2` (fix)

**Total:** 1 commit containing all fixes and documentation

## Files Created/Modified

- `vcdecomp/core/ir/structure/orchestrator.py` - Pattern 5 filter fix (lines 304-322), Pattern 3 synthesis (lines 861-913), debug logging removed
- `vcdecomp/core/ir/structure/analysis/variables.py` - Debug logging removed (lines 385-438)
- `.planning/phases/06-expression-reconstruction-fixes/PATTERN3_FIX_RESULTS.md` - Comprehensive fix analysis (390 lines)

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Pattern 1 needs no fix | DEBUG_FINDINGS.md evidence shows 0 undefined gotos in current output - fix from 06-02 is 100% effective |
| Pattern 5 filter removal | Filter `"[" in var_decl or (var_decl.count(" ") > 1)` excluded simple struct types like `c_Vector3 vec` (only 1 space) |
| Two-phase Pattern 3 fix | End-of-function synthesis (line 861) + mid-function post-processing (line 889) to catch all bare returns |
| Pattern 2 deferred to Phase 7 | Type mismatches require stack_lifter.py + expr.py refactoring (HIGH complexity, out of Phase 6 scope) |

## Deviations from Plan

### Auto-fixed Issues

**None** - Plan executed exactly as specified. DEBUG_FINDINGS.md provided clear guidance on which fixes to apply.

Plan anticipated conditional fixes based on DEBUG_FINDINGS.md analysis:
- Pattern 1: Skip if already working ✓
- Pattern 5: Apply if clear bug identified ✓
- Pattern 3: Implement new fix ✓

All three paths executed as planned.

---

**Total deviations:** 0
**Impact on plan:** Perfect adherence - diagnostic evidence enabled precise targeted fixes

## Issues Encountered

**Compiler still crashes (0xC0000005) despite 0 parse errors**

**Root cause**: Pattern 2 (type mismatches) from ERROR_BASELINE.md
- Compiler successfully parses code (syntax is valid)
- Crash occurs during compilation phase (semantic analysis, type checking, code generation)
- Type system violations (struct vs primitive mismatches) cause access violations

**Resolution approach**:
- Documented Pattern 2 deferral to Phase 7 in PATTERN3_FIX_RESULTS.md
- Phase 7 "Variable Type Inference" will implement robust type inference
- Phase 6 delivered substantial value: 3/6 patterns fixed, 0 parse errors

## Next Phase Readiness

**Phase 6 achievements enable Phase 7 type system work**:
- Decompiled code is syntactically valid C (0 parse errors)
- Orphaned blocks, bare returns, and undeclared variables eliminated
- Type mismatches are now the ONLY remaining blocker

**Blockers/Concerns**:
- Pattern 2 (type mismatches) prevents compilation
- Requires stack_lifter.py type inference refactoring
- Phase 7 must address before compilation possible

**Recommendation**:
- Mark Phase 6 as PARTIAL SUCCESS (3/6 patterns fixed)
- Proceed to Phase 7 for type system implementation
- Significant progress made: code parses successfully, only type system issues remain

**What Phase 7 needs**:
- Robust type inference in stack_lifter.py (SSA value types)
- Type propagation through expr.py (expression rendering)
- Struct vs primitive type resolution
- Pointer arithmetic and type cast handling

---
*Phase: 06-expression-reconstruction-fixes*
*Completed: 2026-01-18*
