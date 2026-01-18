---
phase: 06-expression-reconstruction-fixes
plan: 06a
type: execute
wave: 1
depends_on: []
files_modified:
  - vcdecomp/core/ir/structure/orchestrator.py
  - .planning/phases/06-expression-reconstruction-fixes/PATTERN1_ROOT_CAUSE.md
autonomous: true
gap_closure: true

must_haves:
  truths:
    - "Decompiled code has no undefined goto labels"
    - "Pattern 1 gaps (blocks 3, 46, 48) are resolved"
    - "Orphaned block detection correctly identifies unreachable blocks"
  artifacts:
    - path: "vcdecomp/core/ir/structure/orchestrator.py"
      provides: "Orphaned block detection and label emission"
      min_lines: 800
      pattern: "orphaned.*block|emit.*label"
    - path: ".planning/phases/06-expression-reconstruction-fixes/PATTERN1_ROOT_CAUSE.md"
      provides: "Evidence-based root cause analysis"
      min_lines: 20
  key_links:
    - from: "orchestrator.py:_detect_orphaned_blocks"
      to: "orchestrator.py:_emit_goto_statement"
      via: "Orphaned check prevents goto emission"
      pattern: "if.*orphaned.*continue"
    - from: "orchestrator.py:_emit_block_label"
      to: "decompiled output"
      via: "Label emission for all goto targets"
      pattern: "block_\\d+:"
---

<objective>
Diagnose Pattern 1 (undefined goto labels) by instrumenting code and analyzing why blocks 3, 46, 48 fail.

Purpose: Understand root cause before implementing fix. Pattern 1 was claimed fixed but verification shows 3 undefined gotos still exist.

Output: PATTERN1_ROOT_CAUSE.md with evidence-based hypothesis and fix proposal.
</objective>

<execution_context>
@~/.claude/get-shit-done/workflows/execute-plan.md
@~/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md

# Gap closure context
@.planning/phases/06-expression-reconstruction-fixes/06-VERIFICATION-FINAL.md
@.planning/phases/06-expression-reconstruction-fixes/06-05-SUMMARY.md
@.planning/phases/06-expression-reconstruction-fixes/DEBUG_FINDINGS.md

# Source files
@vcdecomp/core/ir/structure/orchestrator.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: Diagnostic instrumentation for Pattern 1 failure</name>
  <files>vcdecomp/core/ir/structure/orchestrator.py</files>
  <action>
Add diagnostic logging to understand why blocks 3, 46, 48 pass the orphaned check but labels are never emitted.

Instrument three critical points:

1. **At orphaned block detection (lines 763-819)** - Log the decision for blocks 3, 46, 48:
   - target_block value
   - Presence in cfg.blocks
   - Presence in func_block_ids
   - Predecessor count
   - Final orphaned decision (True/False)

2. **At label emission** - Log when labels ARE emitted:
   - Block ID receiving label
   - Reason for emission (jumped-to block, function entry, etc.)

3. **At goto emission (around line 800)** - Log goto targets:
   - Source block
   - Target block
   - Whether orphaned check skipped goto

Use [PATTERN1_DEBUG] prefix for all logging (WARNING level for pytest visibility).

DO NOT fix the bug yet - only add diagnostics to understand root cause.
  </action>
  <verify>
Run validation test and grep debug output:
```bash
cd C:/Users/flori/source/repos/VC_Scripter
PYTHONPATH=. python -m pytest vcdecomp/tests/test_validation.py::test_decompilation_validation[test1_tt] -v --log-cli-level=WARNING 2>&1 | grep PATTERN1_DEBUG > pattern1_debug_output.txt
cat pattern1_debug_output.txt
```

Output should show:
- Orphaned checks for blocks 3, 46, 48
- Label emission decisions for all blocks
- Goto emission decisions
  </verify>
  <done>
Debug output file exists showing orphaned detection and label emission decisions for blocks 3, 46, 48.
  </done>
</task>

<task type="auto">
  <name>Task 2: Root cause analysis from debug output</name>
  <files>.planning/phases/06-expression-reconstruction-fixes/PATTERN1_ROOT_CAUSE.md</files>
  <action>
Analyze the debug output from Task 1 to identify why Pattern 1 fails.

Create PATTERN1_ROOT_CAUSE.md with:

1. **Evidence section** - Copy relevant debug lines showing:
   - Orphaned check results for blocks 3, 46, 48
   - Label emission (or lack thereof) for these blocks
   - Goto emission that references these blocks

2. **Hypothesis section** - Based on evidence, determine one of:
   - A) Orphaned check logic is wrong (blocks ARE orphaned but check says no)
   - B) Labels need emission but separate code path fails to emit them
   - C) Gotos generated before orphaned check runs (timing issue)
   - D) Multiple CFG traversal passes overwrite orphaned detection
   - E) Other root cause identified from evidence

3. **Fix proposal section** - Specific code changes needed based on hypothesis

Be specific: cite line numbers, variable values, and control flow paths.
  </action>
  <verify>
```bash
cat C:/Users/flori/source/repos/VC_Scripter/.planning/phases/06-expression-reconstruction-fixes/PATTERN1_ROOT_CAUSE.md
```

File should have:
- Evidence section with actual debug output
- Clear hypothesis with reasoning
- Specific fix proposal with line numbers
  </verify>
  <done>
PATTERN1_ROOT_CAUSE.md exists with evidence-based hypothesis and fix proposal.
  </done>
</task>

</tasks>

<verification>
After all tasks complete:

1. **Debug output captured:**
```bash
cat pattern1_debug_output.txt | grep "block_3\|block_46\|block_48"
```
Should show orphaned checks and label emission for these blocks.

2. **Root cause documented:**
PATTERN1_ROOT_CAUSE.md should have clear hypothesis with evidence.

3. **Ready for implementation:**
Fix proposal should be specific enough to implement in next plan (06-06b).
</verification>

<success_criteria>
- pattern1_debug_output.txt exists with diagnostic logging
- PATTERN1_ROOT_CAUSE.md exists with evidence-based hypothesis
- Fix proposal is specific with line numbers and code changes
- Diagnostic logging added to orchestrator.py (will be removed in 06-06b)
- Checkpoint ready: user can review root cause before implementing fix
</success_criteria>

<output>
After completion, create `.planning/phases/06-expression-reconstruction-fixes/06-06a-SUMMARY.md`

Summary should include:
- Diagnostic logging approach
- Debug output analysis
- Root cause identified (hypothesis A/B/C/D/E)
- Fix proposal for implementation in 06-06b
</output>
