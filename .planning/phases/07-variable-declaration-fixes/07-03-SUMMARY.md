---
phase: 07-variable-declaration-fixes
plan: 03
subsystem: global-variables
tags: [global-resolver, type-inference, save-info, sgi-constants, headers]

# Dependency graph
requires:
  - phase: 07-variable-declaration-fixes
    plan: 01
    provides: Opcode-based type inference in stack_lifter and integrate_with_ssa_values()
  - phase: 07-variable-declaration-fixes
    plan: 02
    provides: Type inference integration in orchestrator and variables.py
provides:
  - Global variable offset validation (DWORD-to-BYTE conversion with assertions)
  - Type inference integration for global variables (GCP, GLD, GADR, GST opcodes)
  - save_info integration for global variable names (highest priority)
  - SGI constant resolution from headers (second priority after save_info)
  - Source tracking for all global variable names
affects: [global variable declarations, struct inference, array detection]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "DWORD-to-BYTE offset conversion with 4-byte alignment validation"
    - "save_info > SGI > global_pointer > synthetic naming priority"
    - "Source tracking for debugging global variable name resolution"

key-files:
  created:
    - .test_artifacts_07-03_test1_decompiled.c
    - .test_artifacts_07-03_validation.txt
  modified:
    - vcdecomp/core/ir/global_resolver.py

key-decisions:
  - "Add DWORD-to-BYTE conversion logging and 4-byte alignment assertions to prevent offset bugs"
  - "Extend type inference to GST (store) operations in addition to GCP/GLD/GADR (load)"
  - "Add _resolve_sgi_constants() method to map global offsets to SGI constant names from headers"
  - "Add source field to GlobalUsage dataclass for debugging name resolution"
  - "Implement comprehensive logging for all naming decisions (save_info at INFO, others at DEBUG)"

patterns-established:
  - "Pattern: Validate offset conversion with assertions and debug logging"
  - "Pattern: Source tracking enables debugging of name resolution priority"
  - "Pattern: INFO logging for user-facing name sources (save_info, SGI), DEBUG for internal (synthetic)"

# Metrics
duration: 14min
completed: 2026-01-18
---

# Phase 7 Plan 03: Global Variable Fixes Summary

**Global variables now use correct offsets (DWORD-to-BYTE validated), meaningful names (save_info > SGI constants), and inferred types (int/float) instead of generic dword**

## Performance

- **Duration:** 14 min
- **Started:** 2026-01-18T13:37:25Z
- **Completed:** 2026-01-18T13:51:38Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Global offset handling fixed with DWORD-to-BYTE conversion validation and 4-byte alignment assertions
- Type inference integrated for global variables using TypeInferenceEngine results
- save_info names loaded for globals (highest priority - original source code variable names)
- SGI constants resolved from headers for engine globals (second priority)
- Source tracking added for all global variable names (debugging support)
- Comprehensive logging added for offset conversion and name resolution

## Task Commits

Each task was committed together (modified same file):

1. **Task 1 & 2: Fix global offset handling and enhance naming** - `8d4fce3` (feat)

## Files Created/Modified

**Created:**
- `.test_artifacts_07-03_test1_decompiled.c` - Test output showing save_info names (gSteps, gRecs, etc.) and SGI constants (SGI_ALLYDEATHCOUNT, SGI_C4COUNT)
- `.test_artifacts_07-03_validation.txt` - Validation logs showing INFO-level naming decisions

**Modified:**
- `vcdecomp/core/ir/global_resolver.py` (+182 lines, -50 lines) - Added offset validation, GST type inference, _resolve_sgi_constants(), source tracking

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Add DWORD-to-BYTE conversion logging at DEBUG level | Enables verification that all global accesses use correct byte offsets (critical bug identified in RESEARCH.md) |
| Add 4-byte alignment assertions | Defensive programming - crashes immediately if offset calculation is wrong instead of silent corruption |
| Extend type inference to GST operations | Store operations also reveal global variable types, not just load operations |
| Create _resolve_sgi_constants() helper method | SGI constants are game engine globals defined in headers - separate method improves readability |
| Add source field to GlobalUsage dataclass | Debugging support - know where each name came from (save_info, SGI, synthetic, etc.) |
| Log save_info names at INFO level | User-facing feature - important to show debug symbols are being used |
| Log SGI constants at INFO level | User-facing feature - shows engine globals are recognized |

## Deviations from Plan

None - plan executed exactly as written. All tasks completed with expected outputs.

## Issues Encountered

None - implementation worked as expected on first run. Verification showed:
- save_info names loaded correctly (gSteps, gRecs, gRec, gEndRule, etc.)
- SGI constants resolved correctly (SGI_ALLYDEATHCOUNT, SGI_C4COUNT)
- Type inference working (int gSteps, float gNoActiveTime, etc.)
- No assertion errors (all offsets 4-byte aligned)

## Next Phase Readiness

**Ready:**
- Global variable detection using correct DWORD-to-BYTE conversion
- Global names sourced from save_info (highest priority) and SGI constants
- Global types inferred from type_inference results (not generic dword)
- Comprehensive logging in place for debugging

**Verification:**
Test1 decompiled output shows:
```c
// Global variables
int gSteps;
dword gRecs[12];
dword SGI_ALLYDEATHCOUNT;
dword SGI_C4COUNT;
dword gRec[64];
int gEndRule;
int gEndValue;
int gTime;
float gNoActiveTime;
int gPhaseTimer;
float gMissionTimePrev;
float gCLN_MissionTime;
int gCLN_CurStep;
float gNextRecover;
```

**Next steps:**
1. Phase 07-04: Array reconstruction and multi-dimensional array support
2. Phase 07-05: Struct field naming and access pattern inference
3. Full regression testing on test1/test2/test3 to measure overall Pattern 2 reduction

---
*Phase: 07-variable-declaration-fixes*
*Completed: 2026-01-18*
