---
phase: 06-expression-reconstruction-fixes
plan: 06a
subsystem: decompiler-control-flow
tags: [goto-labels, orphaned-blocks, cfg-analysis, diagnostic-logging]

# Dependency graph
requires:
  - phase: 06-05
    provides: Pattern 3 & 5 fixes applied, diagnostic methodology
provides:
  - Root cause analysis for Pattern 1 (undefined goto labels)
  - Diagnostic logging infrastructure for orphaned block detection
  - Evidence-based fix proposal for plan 06-06b
affects: [06-06b, control-flow-reconstruction, goto-label-emission]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Evidence-based diagnosis: instrument code, capture output, analyze evidence"
    - "[MODULE_DEBUG] logging prefix pattern for diagnostic visibility"

key-files:
  created:
    - .planning/phases/06-expression-reconstruction-fixes/PATTERN1_ROOT_CAUSE.md
    - pattern1_debug_output.txt
  modified:
    - vcdecomp/core/ir/structure/orchestrator.py

key-decisions:
  - "Diagnostic logging at WARNING level for pytest visibility without infrastructure changes"
  - "Root cause identified as Hypothesis B: blocks marked emitted but never rendered"
  - "Recommended fix: Track goto_targets set and force label emission for referenced blocks"

patterns-established:
  - "Diagnostic workflow: Add logging → Run tests → Extract evidence → Analyze → Document root cause → Propose fix"
  - "[PATTERN1_DEBUG] prefix enables grep filtering of diagnostic output"

# Metrics
duration: 5min
completed: 2026-01-18
---

# Phase 06-06a: Pattern 1 Root Cause Diagnosis

**Identified why blocks 3, 46, 48 emit gotos but never render labels: pattern detection marks blocks as 'emitted' but rendering logic skips them (unreachable dead code)**

## Performance

- **Duration:** 5 min (319 seconds)
- **Started:** 2026-01-18T11:23:42Z
- **Completed:** 2026-01-18T11:29:01Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- **Root cause identified**: Blocks pass orphaned check (have predecessors) so gotos emitted, but blocks themselves never rendered
- **Evidence collected**: Debug logging shows blocks NOT ORPHANED with predecessor counts
- **Fix proposed**: Track goto_targets set and force label emission for referenced blocks (Option 1 - ~10 line change)

## Task Commits

Each task was committed atomically:

1. **Task 1: Diagnostic instrumentation** - `5824a6a` (feat)
   - Added [PATTERN1_DEBUG] logging at orphaned check and goto emission points
   - Captured debug output showing blocks 3, 46, 48 have predecessors

2. **Task 2: Root cause analysis** - `2cd412e` (docs)
   - Created PATTERN1_ROOT_CAUSE.md with evidence-based analysis
   - Documented 3 fix options, recommended Option 1 (simplest)

## Files Created/Modified

**Created:**
- `.planning/phases/06-expression-reconstruction-fixes/PATTERN1_ROOT_CAUSE.md` (258 lines) - Comprehensive root cause analysis with evidence, hypothesis, and fix proposal
- `pattern1_debug_output.txt` (12 lines) - Captured diagnostic output showing orphaned checks and goto emission for blocks 3, 46, 48

**Modified:**
- `vcdecomp/core/ir/structure/orchestrator.py` (lines 768-831) - Added diagnostic logging at orphaned block detection (conditional + unconditional jumps) and goto emission

## Evidence Summary

### Blocks 3, 46, 48 Analysis

**Orphaned Check Results:**
```
Block 3:  NOT ORPHANED (has 1 predecessors: [1])
Block 46: NOT ORPHANED (has 1 predecessors: [44])
Block 48: NOT ORPHANED (has 1 predecessors: [46])
```

**Goto Emission:**
```c
Line 36:  goto block_3; // @57
Line 165: goto block_46; // @343
Line 166: goto block_48; // @348
```

**Label Emission:**
```bash
grep "^block_3:\|^block_46:\|^block_48:" test1_tt_decompiled.c
# Result: No matches - labels never emitted
```

### Root Cause

Blocks 3, 46, 48 are being:
1. Detected as part of switch/if-else patterns
2. Added to `emitted_blocks` set by pattern detection
3. Skipped during main block rendering loop (line 355 checks `if block_id in emitted_blocks: continue`)
4. Never actually rendered by pattern-specific code (unreachable dead code after returns)

Result: Gotos emitted (because blocks have predecessors), but labels never emitted (because blocks marked as "emitted" but never actually rendered).

## Decisions Made

**1. Evidence-based diagnosis methodology**
- Rationale: Avoid speculation, use diagnostic logging to capture actual execution data
- Implementation: WARNING-level logging for pytest visibility, [PATTERN1_DEBUG] prefix for filtering
- Outcome: Root cause identified in single test run with clear evidence

**2. Hypothesis B confirmed: Blocks marked emitted but never rendered**
- Evidence: Debug output shows blocks NOT ORPHANED, gotos emitted, labels missing
- Context analysis: Blocks completely absent from output (not just missing labels)
- Conclusion: Pattern detection marks blocks as emitted, but rendering skips them

**3. Recommended fix: Option 1 (Track goto_targets)**
- Rationale: Simplest fix (~10 lines), directly addresses root cause
- Alternative Option 2: Post-processing to find missing labels (more complex)
- Alternative Option 3: Fix pattern detection (highest complexity, architectural change)
- Decision: Option 1 balances simplicity with correctness

## Deviations from Plan

None - plan executed exactly as written. Diagnostic instrumentation and root cause analysis completed as specified.

## Issues Encountered

None - diagnostic logging worked as expected, evidence clearly showed root cause.

## Next Phase Readiness

**Ready for 06-06b (implementation):**
- Root cause documented with evidence
- Fix proposal specified with code examples
- Clear verification strategy defined
- Diagnostic logging in place for verification after fix

**Fix approach for 06-06b:**
1. Add `goto_targets = set()` at function start
2. Track target blocks when emitting gotos
3. Modify main block loop to never skip goto targets
4. Emit label when rendering goto target blocks
5. Remove diagnostic logging
6. Verify blocks 3, 46, 48 now have labels

**Estimated complexity for 06-06b:** LOW (15-20 line change based on Option 1 proposal)

---
*Phase: 06-expression-reconstruction-fixes*
*Completed: 2026-01-18*
