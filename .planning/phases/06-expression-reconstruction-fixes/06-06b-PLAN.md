---
phase: 06-expression-reconstruction-fixes
plan: 06b
type: execute
wave: 2
depends_on: [06a]
files_modified:
  - vcdecomp/core/ir/structure/orchestrator.py
  - .planning/phases/06-expression-reconstruction-fixes/PATTERN1_FIX_VALIDATION.md
autonomous: true
gap_closure: true

must_haves:
  truths:
    - "Decompiled code has no undefined goto labels"
    - "Pattern 1 gaps (blocks 3, 46, 48) are resolved"
    - "All goto statements target defined labels"
  artifacts:
    - path: "vcdecomp/core/ir/structure/orchestrator.py"
      provides: "Fixed orphaned block detection and label emission"
      min_lines: 800
      pattern: "orphaned.*block|emit.*label"
    - path: ".planning/phases/06-expression-reconstruction-fixes/PATTERN1_FIX_VALIDATION.md"
      provides: "Comprehensive validation results"
      min_lines: 30
  key_links:
    - from: "orchestrator.py:_detect_orphaned_blocks (fixed)"
      to: "orchestrator.py:_emit_goto_statement"
      via: "Corrected orphaned check prevents invalid gotos"
      pattern: "if.*orphaned.*continue"
    - from: "orchestrator.py:_emit_block_label"
      to: "decompiled output"
      via: "Labels emitted for all reachable goto targets"
      pattern: "block_\\d+:"
---

<objective>
Implement Pattern 1 fix based on PATTERN1_ROOT_CAUSE.md, validate comprehensively, and commit.

Purpose: Close the final gap in Phase 6 syntax error fixes. Implement evidence-based fix from diagnostic analysis.

Output: Decompiled code with 0 undefined goto labels, Pattern 1 fully resolved.
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
@.planning/phases/06-expression-reconstruction-fixes/PATTERN1_ROOT_CAUSE.md
@.planning/phases/06-expression-reconstruction-fixes/06-06a-SUMMARY.md

# Source files
@vcdecomp/core/ir/structure/orchestrator.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: Implement targeted fix based on root cause</name>
  <files>vcdecomp/core/ir/structure/orchestrator.py</files>
  <action>
Implement the fix proposed in PATTERN1_ROOT_CAUSE.md.

**If PATTERN1_ROOT_CAUSE.md proposes a fix outside patterns A-D below, implement that fix. The patterns below are common examples, not exhaustive.**

Common fix patterns based on likely root causes:

**If Hypothesis A (orphaned check logic wrong):**
- Tighten orphaned detection: check if target block is in the current function's reachable blocks, not just has any predecessor
- Example: `if target_block not in reachable_from_entry(cfg, func_entry_block):`

**If Hypothesis B (label emission path missing):**
- Ensure all goto targets get labels emitted, even if block is orphaned
- Example: Track all goto targets, emit labels for them regardless of orphaned status

**If Hypothesis C (timing issue):**
- Run orphaned detection AFTER all gotos are collected, not during emission
- Example: Two-pass approach - collect gotos, detect orphaned, emit code

**If Hypothesis D (multiple passes):**
- Use a definitive orphaned check that isn't overwritten
- Example: Calculate orphaned blocks once at start, store in set

After implementing fix, remove all [PATTERN1_DEBUG] logging added in 06-06a.
  </action>
  <verify>
Run test and check for undefined gotos:
```bash
cd C:/Users/flori/source/repos/VC_Scripter
python -m vcdecomp structure decompiler_source_tests/test1/tt.scr > test1_fixed.c
grep "goto block_3" test1_fixed.c
grep "goto block_46" test1_fixed.c
grep "goto block_48" test1_fixed.c
grep "block_3:" test1_fixed.c
grep "block_46:" test1_fixed.c
grep "block_48:" test1_fixed.c
```

Should show:
- Either gotos removed (if blocks orphaned) OR labels emitted (if blocks needed)
- No goto without corresponding label
  </verify>
  <done>
test1_fixed.c has no undefined goto labels - all gotos either removed or have matching labels.
  </done>
</task>

<task type="auto">
  <name>Task 2: Comprehensive validation across all test cases</name>
  <files>.planning/phases/06-expression-reconstruction-fixes/PATTERN1_FIX_VALIDATION.md</files>
  <action>
Run full test suite and verify Pattern 1 fix across all test cases.

1. **Decompile all test files:**
```bash
cd C:/Users/flori/source/repos/VC_Scripter
python -m vcdecomp structure decompiler_source_tests/test1/tt.scr > test1_validation.c
python -m vcdecomp structure decompiler_source_tests/test2/tdm.scr > test2_validation.c
python -m vcdecomp structure decompiler_source_tests/test3/LEVEL.scr > test3_validation.c
```

2. **Check for undefined gotos (fixed Windows syntax):**
```bash
for file in test1_validation.c test2_validation.c test3_validation.c; do
  echo "=== Checking $file ===" >> pattern1_check_results.txt
  grep -n "goto block_" "$file" | while IFS= read -r line; do
    label=$(echo "$line" | sed -E 's/.*goto (block_[0-9]+).*/\1/')
    if ! grep -q "$label:" "$file"; then
      echo "UNDEFINED: $line" >> pattern1_check_results.txt
    fi
  done
done
```

3. **Create PATTERN1_FIX_VALIDATION.md** with:
   - Results for each test file
   - Count of undefined gotos (should be 0 for all)
   - Comparison to ERROR_BASELINE.md Pattern 1 count (was ~50 instances)
   - Verification that fix is comprehensive

4. **Run pytest validation:**
```bash
PYTHONPATH=. python -m pytest vcdecomp/tests/test_validation.py -v > pattern1_pytest_results.txt 2>&1
```

Include pytest results in validation doc.
  </action>
  <verify>
```bash
cat C:/Users/flori/source/repos/VC_Scripter/.planning/phases/06-expression-reconstruction-fixes/PATTERN1_FIX_VALIDATION.md
cat C:/Users/flori/source/repos/VC_Scripter/pattern1_check_results.txt
```

Should show:
- 0 undefined gotos across all test files
- Pattern 1 fixed completely (down from ~50 instances)
- Pytest results showing compilation status
  </verify>
  <done>
PATTERN1_FIX_VALIDATION.md shows 0 undefined gotos in all test files, Pattern 1 fix verified comprehensive.
  </done>
</task>

<task type="auto">
  <name>Task 3: Commit fix with comprehensive documentation</name>
  <files>Multiple files</files>
  <action>
Commit the Pattern 1 fix with detailed commit message.

1. **Stage files:**
```bash
cd C:/Users/flori/source/repos/VC_Scripter
git add vcdecomp/core/ir/structure/orchestrator.py
git add .planning/phases/06-expression-reconstruction-fixes/PATTERN1_ROOT_CAUSE.md
git add .planning/phases/06-expression-reconstruction-fixes/PATTERN1_FIX_VALIDATION.md
```

2. **Commit with message:**
```bash
git commit -m "$(cat <<'EOF'
fix(06-06b): fix Pattern 1 undefined goto labels (blocks 3, 46, 48)

Root cause: [Based on PATTERN1_ROOT_CAUSE.md hypothesis]

Fix: [Specific change made]

Verified:
- 0 undefined gotos in test1/tt.scr (was 3)
- 0 undefined gotos in test2/tdm.scr
- 0 undefined gotos in test3/LEVEL.scr
- Pattern 1 completely resolved (was ~50 instances in ERROR_BASELINE.md)

Evidence in PATTERN1_FIX_VALIDATION.md

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

DO NOT push - just commit locally.
  </action>
  <verify>
```bash
git log -1 --stat
git show --stat
```

Should show:
- Commit with comprehensive message
- orchestrator.py modified
- Two .md files added (ROOT_CAUSE and FIX_VALIDATION)
  </verify>
  <done>
Commit exists with Pattern 1 fix, root cause analysis, and validation docs.
  </done>
</task>

</tasks>

<verification>
After all tasks complete:

1. **No undefined gotos exist:**
```bash
python -m vcdecomp structure decompiler_source_tests/test1/tt.scr > final_check.c
grep "goto block_" final_check.c | while IFS= read -r line; do
  label=$(echo "$line" | sed -E 's/.*goto (block_[0-9]+).*/\1/')
  grep -q "$label:" final_check.c || echo "FAIL: $line"
done
```
Should produce no output (no failures).

2. **Pattern 1 gaps closed in VERIFICATION-FINAL.md:**
- Gap 1 (undefined gotos) should be closable
- Blocks 3, 46, 48 either have labels or gotos removed

3. **Compilation progress measured:**
Run pytest validation to see if fixing Pattern 1 enables compilation (unlikely due to Pattern 2, but measure).
</verification>

<success_criteria>
- PATTERN1_FIX_VALIDATION.md shows 0 undefined gotos across all tests
- orchestrator.py modified with targeted fix (no [PATTERN1_DEBUG] logging remaining)
- Git commit contains fix with comprehensive documentation
- Gap 1 from 06-VERIFICATION-FINAL.md resolved
- Pattern 1 fully closed
</success_criteria>

<output>
After completion, create `.planning/phases/06-expression-reconstruction-fixes/06-06b-SUMMARY.md`

Summary should include:
- Fix implemented based on PATTERN1_ROOT_CAUSE.md
- Pattern 1 fully validated (0 undefined gotos)
- Pattern 1 gaps fully closed
- Remaining gaps (Pattern 2 deferred to Phase 7)
- Final Phase 6 assessment: 3/6 patterns fixed, Pattern 1 NOW VERIFIED WORKING
</output>
