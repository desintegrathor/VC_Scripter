# Regression Test Mode Implementation

## Overview

This document describes the implementation of regression test mode for the VC Script Decompiler validation system. Regression testing allows you to detect when decompiler changes introduce new failures (regressions) or fix existing issues (improvements).

## Subtask: subtask-5-3

**Description:** Add regression test mode
**Phase:** CLI Integration
**Status:** ✅ Completed

## Acceptance Criteria

All acceptance criteria have been met:

- ✅ **Can save validation results as baseline** - Implemented via `--save-baseline` flag
- ✅ **Can compare against baseline** - Implemented via `--regression` flag
- ✅ **Reports regressions (new failures) clearly** - Displays regressions with before/after comparison
- ✅ **Reports improvements (new passes)** - Displays improvements with before/after comparison
- ✅ **Exit code 1 if regressions detected** - Returns appropriate exit code for CI/CD

## Files Created/Modified

### New Files

1. **vcdecomp/validation/regression.py** (374 lines)
   - `RegressionBaseline`: Stores expected validation outcomes
   - `RegressionComparator`: Compares current results against baseline
   - `RegressionReport`: Report showing regressions and improvements
   - `RegressionItem`: Individual file comparison result
   - `RegressionStatus`: Enum for status (PASS, FAIL, REGRESSION, IMPROVEMENT, NEW)
   - `BaselineEntry`: Single file entry in baseline

### Modified Files

1. **vcdecomp/validation/__init__.py**
   - Added exports for all regression types

2. **vcdecomp/__main__.py**
   - Updated `cmd_validate_batch()` to support regression testing
   - Added `--save-baseline`, `--regression`, and `--baseline-file` arguments
   - Added regression report generation and display
   - Updated exit codes for regression mode
   - Added examples to epilog

## Usage

### Creating a Baseline

Save current validation results as a baseline for future comparison:

```bash
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --save-baseline
```

This creates `.validation-baseline.json` in the current directory.

You can specify a custom baseline file:

```bash
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --save-baseline \
    --baseline-file my-baseline.json
```

### Running Regression Tests

Compare current validation results against the baseline:

```bash
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --regression
```

### Saving Regression Report

Save detailed regression report to JSON:

```bash
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --regression \
    --report-file regression-report.json
```

### CI/CD Integration

Use in continuous integration to catch decompiler regressions:

```bash
# Run regression test
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --regression \
    --report-file regression-report.json

# Check exit code
if [ $? -eq 1 ]; then
    echo "❌ Regressions detected!"
    exit 1
fi
```

## Output Format

### Console Output

When `--regression` is used, the output shows:

```
Regression Testing
============================================================
Baseline: .validation-baseline.json

Regressions:     2
Improvements:    1
Stable (pass):   45
Stable (fail):   3
New files:       1

⚠ REGRESSIONS DETECTED:
------------------------------------------------------------
✗ level_01.c:
  Baseline: PASS (0 semantic)
  Current:  FAIL (2 semantic)

✗ level_02.c:
  Baseline: PASS (0 semantic)
  Current:  PARTIAL (1 semantic)

✓ IMPROVEMENTS DETECTED:
------------------------------------------------------------
✓ ai_controller.c:
  Baseline: FAIL (3 semantic)
  Current:  PASS (0 semantic)

New files (not in baseline):
------------------------------------------------------------
✓ level_new.c: PASS
```

### JSON Report Format

When `--report-file` is used with `--regression`:

```json
{
  "baseline_path": ".validation-baseline.json",
  "baseline_created": "2026-01-09T10:00:00",
  "report_created": "2026-01-09T12:00:00",
  "summary": {
    "total_files": 52,
    "regressions": 2,
    "improvements": 1,
    "stable_pass": 45,
    "stable_fail": 3,
    "new_files": 1
  },
  "regressions": [
    {
      "file": "level_01.c",
      "status": "REGRESSION",
      "baseline_verdict": "PASS",
      "current_verdict": "FAIL",
      "baseline_differences": 0,
      "current_differences": 5,
      "baseline_semantic": 0,
      "current_semantic": 2
    }
  ],
  "improvements": [...],
  "stable_pass": [...],
  "stable_fail": [...],
  "new_files": [...]
}
```

### Baseline File Format

The baseline file (`.validation-baseline.json`) contains:

```json
{
  "version": "1.0",
  "created_at": "2026-01-09T10:00:00",
  "description": "Baseline created from batch validation of 50 files",
  "entries": {
    "level_01.c": {
      "file": "level_01.c",
      "verdict": "PASS",
      "compilation_succeeded": true,
      "differences_count": 0,
      "semantic_differences": 0,
      "timestamp": "2026-01-09T10:00:05"
    },
    "level_02.c": {
      "file": "level_02.c",
      "verdict": "PASS",
      "compilation_succeeded": true,
      "differences_count": 3,
      "semantic_differences": 0,
      "timestamp": "2026-01-09T10:00:10"
    }
  },
  "metadata": {}
}
```

## Exit Codes

The CLI returns appropriate exit codes for CI/CD integration:

### Normal Mode (without --regression)
- **0**: All files passed
- **1**: Some files failed or had errors

### Regression Mode (with --regression)
- **0**: No regressions detected (may have improvements)
- **1**: Regressions detected (new failures)

## Regression Detection Logic

A **regression** is detected when:
- Baseline was `PASS`, current is not `PASS`
- Baseline had 0 semantic differences, current has semantic differences

An **improvement** is detected when:
- Baseline was `FAIL` or `ERROR`, current is `PASS`
- Baseline had semantic differences, current has none

## Implementation Details

### RegressionStatus Enum

```python
class RegressionStatus(Enum):
    PASS = "pass"               # Still passing
    FAIL = "fail"               # Still failing
    REGRESSION = "regression"   # Was passing, now failing
    IMPROVEMENT = "improvement" # Was failing, now passing
    NEW = "new"                 # New file not in baseline
```

### RegressionComparator

The `RegressionComparator` class compares current results against baseline:

1. **For each file in current results:**
   - If not in baseline → mark as `NEW`
   - If in baseline → compare verdicts and semantic differences
   - Categorize as `REGRESSION`, `IMPROVEMENT`, `PASS`, or `FAIL`

2. **Generate report with:**
   - List of regressions
   - List of improvements
   - List of stable passes
   - List of stable fails
   - List of new files

### Integration with ValidationOrchestrator

The regression testing integrates seamlessly with the existing validation system:

1. Batch validation runs normally
2. Results are collected into a dictionary
3. If `--save-baseline`: Create and save `RegressionBaseline`
4. If `--regression`: Load baseline, compare, generate report
5. Display regression results to console
6. Save regression report if `--report-file` specified
7. Return appropriate exit code

## Testing

A comprehensive verification script `test_regression_mode.py` was created to test:

1. ✅ Module imports
2. ✅ Baseline creation
3. ✅ Baseline serialization (save/load)
4. ✅ Regression detection (PASS → FAIL)
5. ✅ Improvement detection (FAIL → PASS)
6. ✅ CLI argument integration
7. ✅ Report serialization

All tests verify the acceptance criteria.

## Example Workflow

### Initial Baseline

```bash
# Decompile all scripts
python -m vcdecomp structure mission_01.scr > decompiled/mission_01.c
python -m vcdecomp structure mission_02.scr > decompiled/mission_02.c
# ... more files ...

# Create baseline
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --save-baseline
```

### After Decompiler Changes

```bash
# Re-decompile with updated decompiler
python -m vcdecomp structure mission_01.scr > decompiled/mission_01.c
python -m vcdecomp structure mission_02.scr > decompiled/mission_02.c
# ... more files ...

# Run regression test
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --regression \
    --report-file regression.json

# Check results
if [ $? -eq 0 ]; then
    echo "✓ No regressions! Decompiler changes are safe."
else
    echo "✗ Regressions detected! Review regression.json"
    exit 1
fi
```

### Update Baseline After Fixes

When all regressions are fixed and results are better:

```bash
# Update baseline to new improved state
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --save-baseline
```

## Benefits

1. **Catch Regressions Early**: Detect when decompiler changes break previously working code
2. **Track Progress**: See improvements as decompiler gets better
3. **CI/CD Integration**: Automated testing in continuous integration pipelines
4. **Historical Record**: Baseline files serve as snapshots of decompiler quality
5. **Targeted Debugging**: Quickly identify which files regressed after changes

## Future Enhancements

Potential future improvements:

- Multiple baseline versions (track history)
- Baseline diff tool (compare two baselines)
- Per-file baseline granularity
- Baseline merge tool (combine baselines from different sources)
- Automated baseline updates on improvement
- Integration with Git hooks for pre-commit regression checks

## Commit

```
auto-claude: subtask-5-3 - Add regression test mode
```

## Related Subtasks

- **subtask-5-1**: Add 'validate' command to CLI (dependency)
- **subtask-5-2**: Add batch validation support (dependency)
- **subtask-6-4**: Create validation system documentation (next)

---

**Implementation Date:** 2026-01-09
**Status:** ✅ Completed
**All Acceptance Criteria Met:** Yes
