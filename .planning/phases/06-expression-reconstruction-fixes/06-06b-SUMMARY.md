---
phase: 06-expression-reconstruction-fixes
plan: 06b
subsystem: decompiler
tags: [control-flow, goto, label-emission, pattern-detection, code-generation]

# Dependency graph
requires:
  - phase: 06-06a
    provides: Pattern 1 root cause diagnosis with evidence-based analysis
provides:
  - Pattern 1 fix (98% reduction in undefined goto labels)
  - goto_targets tracking mechanism for label emission
  - Validation methodology for goto/label correctness
affects: [Phase 7 (Type System Fixes), Phase 8 (Semantic Verification)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "goto_targets set tracking for control flow label emission"
    - "Multi-point label emission (switch/if/regular block headers)"
    - "Edge case documentation for cross-function gotos"

key-files:
  created:
    - .planning/phases/06-expression-reconstruction-fixes/PATTERN1_FIX_VALIDATION.md
  modified:
    - vcdecomp/core/ir/structure/orchestrator.py

key-decisions:
  - "Track goto targets in separate set instead of modifying emitted_blocks"
  - "Emit labels at three rendering points: switch headers, if headers, regular blocks"
  - "Defer cross-function goto handling to Phase 7 (edge case, 1 instance)"
  - "98% success threshold acceptable for Pattern 1 closure"

patterns-established:
  - "Label emission pattern: Check goto_targets before rendering any block type"
  - "Skip logic pattern: emitted_blocks AND NOT goto_targets"
  - "Target tracking pattern: Populate set when emitting goto, not when detecting block"

# Metrics
duration: 22min
completed: 2026-01-18
---

# Phase 06 Plan 06b: Pattern 1 Fix Implementation Summary

**Goto target label emission fix reduces undefined labels from ~50 to 1 edge case (98% reduction) via goto_targets tracking**

## Performance

- **Duration:** 22 min
- **Started:** 2026-01-18T11:32:26Z
- **Completed:** 2026-01-18T11:54:16Z
- **Tasks:** 3
- **Files modified:** 2 (1 code file, 1 validation doc created)

## Accomplishments

- **Pattern 1 fix implemented and verified** - 98% reduction in undefined goto labels (50 → 1)
- **Test1 fully fixed** - Blocks 3, 46, 48 now have labels (primary test case from 06-06a)
- **No regressions** - Test2 remains clean, test3 vastly improved
- **Edge case identified** - Cross-function goto documented for future handling

## Task Commits

Each task was committed atomically:

1. **Tasks 1-3: Implement fix, validate, and commit** - `539a96e` (fix)

**Note:** All three tasks executed in single commit due to tight coupling between implementation and validation.

## Files Created/Modified

- `vcdecomp/core/ir/structure/orchestrator.py` - Added goto_targets tracking and label emission at 4 points
- `.planning/phases/06-expression-reconstruction-fixes/PATTERN1_FIX_VALIDATION.md` - Comprehensive validation results (206 lines)

### Orchestrator.py Changes

**Change 1** (line 352): Initialize goto_targets set
```python
goto_targets: Set[int] = set()  # Track blocks referenced by goto statements
```

**Change 2** (line 357): Modify skip logic to preserve goto targets
```python
if block_id in emitted_blocks and block_id not in goto_targets:
    continue
```

**Change 3** (lines 428-429, 573-574, 688-689): Emit labels at 3 rendering points
- Before switch header rendering
- Before if/else header rendering
- Before regular block rendering

**Change 4** (lines 792, 824): Track targets when emitting gotos
```python
goto_targets.add(target_block)
```

## Decisions Made

**1. Separate goto_targets set instead of modifying emitted_blocks**
- **Rationale:** Clean separation of concerns - emitted_blocks tracks pattern rendering, goto_targets tracks control flow requirements
- **Alternative considered:** Modify emitted_blocks logic - rejected due to complexity

**2. Three-point label emission strategy**
- **Rationale:** Labels must appear before blocks rendered by any pattern (switch, if/else, regular)
- **Alternative considered:** Single emission point at end of block rendering - rejected because labels would appear after block content

**3. Defer cross-function goto to Phase 7**
- **Rationale:** Edge case (1 instance out of ~50), different root cause, Phase 6 scope is syntax fixes
- **Alternative considered:** Fix immediately - rejected due to scope creep risk

**4. 98% success threshold acceptable**
- **Rationale:** Primary pattern fully resolved, remaining edge case documented, compilation error clear
- **Alternative considered:** 100% target - rejected as unrealistic for edge cases

## Deviations from Plan

None - plan executed exactly as written.

Implementation followed PATTERN1_ROOT_CAUSE.md Option 1 proposal precisely:
1. Track goto_targets set
2. Modify skip logic
3. Emit labels for goto targets
4. Populate targets when emitting gotos

## Issues Encountered

**1. Block 3 initially missing label after first implementation**
- **Cause:** Label emission only in main loop, but block 3 rendered by if/else pattern
- **Resolution:** Added label emission before if/else rendering (line 573-574)
- **Time impact:** +5 minutes for diagnosis and fix

**2. Cross-function goto in test3 (block 88)**
- **Cause:** Block 88 outside function scope (goto at line 258, function ends at line 260)
- **Resolution:** Documented as edge case, deferred to Phase 7
- **Justification:** Different root cause than primary pattern, 1 instance vs ~50 baseline

## Validation Results

### Test 1: tt.scr (Primary Test Case)

**Before fix:**
- goto block_3 (line 36) → UNDEFINED
- goto block_46 (line 165) → UNDEFINED
- goto block_48 (line 166) → UNDEFINED

**After fix:**
- goto block_3 (line 119) → DEFINED (line 120) ✓
- goto block_46 (line 266) → DEFINED (line 267) ✓
- goto block_48 (line 268) → DEFINED (line 269) ✓

**Result:** 3/3 fixed ✓

### Test 2: tdm.scr

**Before fix:** 0 undefined gotos
**After fix:** 0 undefined gotos ✓
**Result:** No regression ✓

### Test 3: LEVEL.scr

**Before fix:** Multiple undefined gotos
**After fix:** 1 undefined goto (block 88, cross-function edge case)
**Result:** Vastly improved (98%+ reduction) ⚠

### Overall Statistics

- **Baseline (ERROR_BASELINE.md):** ~50 undefined goto instances
- **After fix:** 1 edge case remaining
- **Reduction:** 98% (49/50 fixed)
- **Primary pattern:** 100% fixed (blocks marked emitted but not rendered)
- **Edge case:** Cross-function goto (different root cause)

## Root Cause Verification

The fix correctly addresses the root cause identified in PATTERN1_ROOT_CAUSE.md:

**Problem:** Blocks 3, 46, 48 have predecessors (not orphaned), so gotos are emitted. But blocks are marked as "emitted" by switch/if-else pattern detection and never actually rendered, so labels don't appear.

**Solution:** Track goto_targets separately from emitted_blocks. Always emit labels for goto targets, even if blocks are in emitted_blocks.

**Evidence:**
- Block 3: If/else header, now gets label before `if (!tmp1)` statement
- Block 46/48: Regular blocks, now get labels before block content
- Skip logic prevents duplicate rendering while preserving label emission

## Next Phase Readiness

**Phase 6 Pattern 1 status:** CLOSED ✓

**Remaining Phase 6 work:**
- Pattern 2 (type mismatches): DEFERRED to Phase 7 per 06-05 decision
- Pattern 3 (missing returns): FIXED in 06-05
- Pattern 5 (undeclared variables): FIXED in 06-05

**Phase 7 prerequisites:**
- Pattern 1 syntax errors resolved (gotos/labels)
- Pattern 3 syntax errors resolved (bare returns)
- Pattern 5 syntax errors resolved (missing declarations)

**Blockers for compilation:**
- Pattern 2 type mismatches remain (HIGH complexity, requires stack_lifter.py refactoring)
- This is expected - Phase 6 focused on syntax errors, Phase 7 will tackle type system

**Edge case handling:**
- Cross-function goto (block 88) can be addressed in Phase 7 if needed
- Recommend: Add cross-function goto detection to orphaned check
- Impact: 1 instance, clear error message, low priority

## Lessons Learned

**1. Multi-point label emission required for pattern-driven code**
- Blocks rendered by different patterns (switch, if/else, regular) need labels at different points
- Single emission point insufficient when patterns consume blocks

**2. Separate tracking sets cleaner than overloading emitted_blocks**
- goto_targets has clear single responsibility
- emitted_blocks remains pattern rendering tracking
- No complex boolean logic needed

**3. Evidence-based diagnosis (06-06a) enabled precise fix**
- Debug logging showed exact blocks, predecessors, emission decisions
- Root cause analysis identified specific timing issue
- Fix implemented in 22 minutes due to clear diagnosis

**4. 98% success acceptable for production**
- Perfect fix vs good fix tradeoff
- Edge cases documented for future work
- Clear error messages guide user if edge case hits

---
*Phase: 06-expression-reconstruction-fixes*
*Completed: 2026-01-18*
