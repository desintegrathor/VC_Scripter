# Batch Validation Implementation

## Overview

This document describes the implementation of the batch validation feature (subtask-5-2) for the VC Script Decompiler validation system.

## Acceptance Criteria

All 5 acceptance criteria have been met:

- ✅ **Can validate entire directories**: Automatically discovers all `.c` files in input directory
- ✅ **Matches files by name**: Pairs `.c` files with `.scr` files using filename matching
- ✅ **Generates summary report for all files**: Provides detailed console summary and optional JSON report
- ✅ **Supports parallel validation with --jobs flag**: Uses ThreadPoolExecutor for concurrent processing
- ✅ **Shows progress bar for batch operations**: Real-time progress display with status indicators

## Command Usage

```bash
python -m vcdecomp validate-batch --input-dir <path> --original-dir <path> [options]
```

### Required Arguments

- `--input-dir`: Directory containing decompiled `.c` source files
- `--original-dir`: Directory containing original `.scr` compiled files

### Optional Arguments

- `--compiler-dir`: Path to compiler directory (default: `original-resources/compiler`)
- `--jobs`: Number of parallel validation jobs (default: 4)
- `--report-file`: Save batch summary report to JSON file
- `--no-cache`: Disable validation cache

### Examples

1. **Basic batch validation:**
   ```bash
   python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/
   ```

2. **With 8 parallel jobs:**
   ```bash
   python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --jobs 8
   ```

3. **With JSON report output:**
   ```bash
   python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --report-file batch_report.json
   ```

4. **Disable caching (force revalidation):**
   ```bash
   python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --no-cache
   ```

## Implementation Details

### File Matching

The implementation matches files by name using the following algorithm:

1. Find all `.c` files in the input directory using `Path.glob("*.c")`
2. For each `.c` file, construct the expected `.scr` filename using `source_file.stem + ".scr"`
3. Check if the `.scr` file exists in the original directory
4. If found, add the pair to the validation queue
5. If not found, print a warning to stderr

Example:
```
Input:  decompiled/level_01.c
Output: scripts/level_01.scr
```

### Parallel Processing

Validation tasks are executed in parallel using Python's `concurrent.futures.ThreadPoolExecutor`:

- **Thread pool size**: Controlled by `--jobs` argument (default: 4)
- **Task submission**: All validation pairs are submitted to the executor
- **Progress tracking**: Results are processed as they complete using `as_completed()`
- **Error handling**: Exceptions are caught per-task and reported in the summary

### Progress Display

Real-time progress is shown during batch processing:

```
Progress:
------------------------------------------------------------
[=============================>                     ] 14/25 | ✓ level_01.c                   PASS
```

Components:
- **Progress bar**: Visual indicator (50 characters wide, updated per completion)
- **Counter**: Shows `completed/total` counts
- **Status symbol**: ✓ (PASS), ! (FAIL/PARTIAL), ✗ (ERROR)
- **Filename**: Name of the file being validated (30 characters, left-aligned)
- **Verdict**: PASS, FAIL, PARTIAL, or ERROR

### Summary Report

After batch processing completes, a summary is printed to the console:

```
Summary Report
============================================================
Total files:     25
Passed:          20
Failed:          3
Partial:         1
Errors:          1
```

If there are failures or errors, details are shown:

```
Failed/Error Files:
------------------------------------------------------------
✗ level_05.c: 12 differences (3 semantic)
✗ level_12.c: Compilation failed - Syntax error; Undefined symbol; ...
✗ level_18.c: File not found: scripts/level_18.scr
```

### JSON Report Format

When `--report-file` is specified, a JSON report is generated:

```json
{
  "timestamp": "2026-01-09T10:15:30.123456",
  "input_dir": "/path/to/decompiled",
  "original_dir": "/path/to/scripts",
  "compiler_dir": "/path/to/compiler",
  "total": 25,
  "passed": 20,
  "failed": 3,
  "partial": 1,
  "errors": 1,
  "results": [
    {
      "file": "level_01.c",
      "verdict": "PASS",
      "compilation_succeeded": true,
      "differences_count": 0,
      "semantic_differences": 0
    },
    {
      "file": "level_05.c",
      "verdict": "FAIL",
      "compilation_succeeded": true,
      "differences_count": 12,
      "semantic_differences": 3
    },
    {
      "file": "level_12.c",
      "verdict": "ERROR",
      "error": "Compilation failed: Syntax error at line 42"
    }
  ]
}
```

## Exit Codes

The command uses exit codes to indicate batch validation status:

- **0**: All files passed validation
- **1**: Some files failed or had errors

## Error Handling

The implementation handles various error conditions:

1. **Directory not found**: Validates that both input and original directories exist
2. **No files found**: Reports error if no `.c` files are found in input directory
3. **No matching pairs**: Reports error if no `.c`/`.scr` pairs can be matched
4. **Validation errors**: Catches exceptions during validation and includes in summary
5. **Missing compiler**: Validates compiler directory exists before starting

## Integration with Validation System

The batch validator integrates with the existing validation infrastructure:

- **ValidationOrchestrator**: Used for individual file validation
- **ValidationVerdict**: Used to categorize results (PASS, FAIL, PARTIAL, ERROR)
- **Caching**: Respects `--no-cache` flag to disable cache when needed
- **Compiler wrapper**: Uses existing SCMP wrapper for compilation

## Performance Considerations

1. **Parallelism**: Default of 4 jobs balances CPU usage and I/O
2. **Caching**: Validation cache significantly speeds up repeated runs
3. **Memory**: ThreadPoolExecutor uses threads (not processes) to reduce overhead
4. **Progress**: Updates are printed per-completion (not per-second) to minimize overhead

## Testing

The implementation can be verified using `test_batch_validation.py`:

```bash
python test_batch_validation.py
```

This test script verifies:
- Command registration and argument parsing
- Function existence and callability
- Acceptance criteria coverage by code inspection

## Files Modified

- `vcdecomp/__main__.py`: Added `cmd_validate_batch()` function and argparse configuration

## Implementation Statistics

- **Lines of code**: ~220 lines (including documentation)
- **Functions**: 1 main function + 1 nested helper
- **Dependencies**: `concurrent.futures`, `json`, `datetime`, `pathlib`

## Future Enhancements

Potential improvements for future versions:

1. **Filtering options**: Add `--pattern` to filter files by glob pattern
2. **HTML report**: Generate visual HTML report in addition to JSON
3. **Incremental validation**: Only validate files that changed since last run
4. **Detailed logs**: Write per-file logs to a directory
5. **Statistics**: Track validation time per file for performance analysis

## Related Subtasks

- **subtask-5-1**: Single file validation (dependency)
- **subtask-5-3**: Regression test mode (will build on batch validation)
- **Phase 3**: Validation orchestrator (provides core validation logic)
- **Phase 2**: Bytecode comparison (provides difference detection)

## Conclusion

The batch validation feature is fully implemented and meets all acceptance criteria. It provides efficient parallel processing, clear progress indication, and comprehensive reporting suitable for CI/CD integration and large-scale validation workflows.
