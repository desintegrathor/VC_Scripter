# Validate CLI Command Implementation (subtask-5-1)

## Overview

Implemented the `validate` command for the vcdecomp CLI that validates decompiled source code by recompiling it with the original Pterodon compiler tools and comparing the bytecode against the original .SCR file.

## Usage

### Basic Usage

```bash
python -m vcdecomp validate original.scr decompiled.c
```

This will:
1. Compile `decompiled.c` using the Pterodon compiler chain (SCMP.exe)
2. Compare the bytecode of the compiled output with `original.scr`
3. Print a text report to the console with color-coded differences
4. Exit with code 0 if validation passes, 1 if it fails

### Save Report to File

```bash
# Save as HTML (auto-detected from extension)
python -m vcdecomp validate original.scr decompiled.c --report-file report.html

# Save as JSON
python -m vcdecomp validate original.scr decompiled.c --report-file report.json

# Save as text file
python -m vcdecomp validate original.scr decompiled.c --report-file report.txt
```

### Specify Output Format

```bash
# Force JSON output to console
python -m vcdecomp validate original.scr decompiled.c --output-format json

# Force HTML output to file (override extension)
python -m vcdecomp validate original.scr decompiled.c --report-file report.txt --output-format html
```

### Advanced Options

```bash
# Specify custom compiler directory
python -m vcdecomp validate original.scr decompiled.c --compiler-dir /path/to/compiler

# Disable validation caching (force recompilation)
python -m vcdecomp validate original.scr decompiled.c --no-cache

# Disable colored output (for piping or logging)
python -m vcdecomp validate original.scr decompiled.c --no-color
```

## Command Arguments

### Required Arguments

- `original_scr`: Path to the original .SCR file (reference bytecode)
- `source_file`: Path to the decompiled source .c file to validate

### Optional Flags

- `--compiler-dir PATH`: Path to compiler directory containing SCMP.exe, SPP.exe, SCC.exe, SASM.exe
  - Default: `original-resources/compiler` (relative to project root)

- `--output-format {text,json,html}`: Output format for the report
  - Default: `text` (or auto-detect from `--report-file` extension)
  - `text`: Color-coded text with ANSI colors
  - `json`: Structured JSON for programmatic use
  - `html`: Interactive HTML with expandable sections

- `--report-file PATH`: Save detailed report to file
  - Format is auto-detected from extension (.txt, .json, .html)
  - Can be overridden with `--output-format`

- `--no-cache`: Disable validation caching
  - Forces recompilation even if source hasn't changed
  - Useful for testing or when header files change

- `--no-color`: Disable ANSI colors in text output
  - Useful for piping output or logging to files

## Exit Codes

The command returns different exit codes based on validation results:

- **0 (PASS)**: Validation passed - bytecode matches perfectly (or only cosmetic differences)
- **1 (FAIL/PARTIAL)**: Validation failed - semantic differences detected
- **2 (ERROR)**: Compilation error or validation error occurred

This allows for easy integration with CI/CD pipelines:

```bash
if python -m vcdecomp validate original.scr decompiled.c; then
    echo "Validation passed!"
else
    echo "Validation failed!"
    exit 1
fi
```

## Output Examples

### Text Output (Console)

```
Validating decompiled.c against original.scr...
Compiler directory: C:\Users\...\original-resources\compiler

================================================================================
                        VALIDATION REPORT
================================================================================
Verdict: PASS
Original:    original.scr
Recompiled:  decompiled.scr
Compiled at: 2026-01-09 10:15:30
================================================================================

Compilation: SUCCESS

Bytecode Comparison:
  Total differences: 0
  Semantic differences: 0
  Cosmetic differences: 0
  Optimization differences: 0

Verdict: PASS
The recompiled bytecode matches the original perfectly.

Recommendations:
  ✓ Decompilation is accurate - no action needed
```

### JSON Output

```json
{
  "verdict": "PASS",
  "original_scr_path": "original.scr",
  "recompiled_scr_path": "decompiled.scr",
  "compilation_succeeded": true,
  "difference_summary": {
    "total": 0,
    "semantic_count": 0,
    "cosmetic_count": 0,
    "optimization_count": 0,
    "unknown_count": 0
  },
  "recommendations": [
    "Decompilation is accurate - no action needed"
  ]
}
```

### HTML Output

Interactive HTML report with:
- Color-coded verdict banner
- Expandable difference sections
- Side-by-side bytecode comparison
- Detailed difference descriptions
- Summary statistics

## Integration with Existing Systems

The validate command integrates seamlessly with:

1. **ValidationOrchestrator**: Coordinates compilation and comparison
2. **ReportGenerator**: Generates reports in multiple formats
3. **ValidationCache**: Caches results to avoid redundant recompilation
4. **Compiler Wrappers**: Uses SCMPWrapper to invoke Pterodon tools
5. **Bytecode Comparator**: Deep comparison of .SCR file sections

## Error Handling

The command provides clear error messages for common issues:

```bash
# Missing original file
Error: Original SCR file not found: original.scr

# Missing source file
Error: Source file not found: decompiled.c

# Missing compiler
Error: Compiler directory not found: /path/to/compiler
Use --compiler-dir to specify the location of SCMP.exe

# Compilation error
Error during validation: Compilation failed at SPP stage
(See detailed error output above)
```

## Examples

### Example 1: Basic Validation

```bash
$ python -m vcdecomp validate Compiler-testruns/hello.scr Compiler-testruns/hello.c

Validating hello.c against hello.scr...
Compiler directory: C:\...\original-resources\compiler

Verdict: PASS
Compilation: SUCCESS
Total differences: 0
```

### Example 2: Validation with Report

```bash
$ python -m vcdecomp validate level01.scr level01_decompiled.c --report-file validation.html

Validating level01_decompiled.c against level01.scr...
Compiler directory: C:\...\original-resources\compiler

Report saved to: validation.html

Verdict: PARTIAL
Compilation: SUCCESS
Total differences: 5
  Semantic: 2
  Cosmetic: 3
```

### Example 3: CI/CD Integration

```bash
#!/bin/bash
# Validate all decompiled scripts

for scr in original/*.scr; do
    base=$(basename "$scr" .scr)
    if python -m vcdecomp validate "$scr" "decompiled/${base}.c" --no-color; then
        echo "✓ $base validated"
    else
        echo "✗ $base failed validation"
        exit 1
    fi
done

echo "All scripts validated successfully!"
```

## Implementation Details

### File Structure

```
vcdecomp/
  __main__.py          # CLI entry point (cmd_validate function added)
  validation/
    validator.py       # ValidationOrchestrator
    report_generator.py  # ReportGenerator
    compiler_wrapper.py  # SCMPWrapper
    bytecode_compare.py  # BytecodeComparator
    cache.py           # ValidationCache
```

### Code Flow

1. **Parse arguments**: Extract file paths and options from CLI
2. **Validate inputs**: Check that files and compiler directory exist
3. **Create validator**: Instantiate ValidationOrchestrator with settings
4. **Run validation**: Call `validator.validate()` which:
   - Compiles source with SCMPWrapper
   - Compares bytecode with BytecodeComparator
   - Categorizes differences
   - Generates recommendations
5. **Generate report**: Use ReportGenerator to format output
6. **Save report**: If --report-file specified, write to file
7. **Print summary**: Always print summary to console
8. **Return exit code**: Based on validation verdict

## Testing

Run the verification script to test the implementation:

```bash
python test_validate_command.py
```

This will verify:
- Module imports work correctly
- Command function exists and has correct signature
- Argparse is configured properly
- All acceptance criteria are met

## Acceptance Criteria ✓

All acceptance criteria from the spec have been met:

- ✓ Command: `python -m vcdecomp validate original.scr source.c`
- ✓ Outputs validation results to console
- ✓ Returns exit code 0 for pass, non-zero for fail
- ✓ Supports --output-format flag (text/json/html)
- ✓ Supports --report-file flag for saving report

## Future Enhancements

Potential improvements for future subtasks:

- **Batch validation** (subtask-5-2): Validate multiple files at once
- **Regression testing** (subtask-5-3): Compare against baseline results
- **Progress bar**: Show compilation progress for large files
- **Verbose mode**: Show detailed compilation steps
- **Quiet mode**: Suppress all output except errors
- **Filter differences**: Only show semantic or critical differences

## Commit

Commit: `46c5585`
Branch: `auto-claude/013-recompilation-validation-system`

## Related Documentation

- `.auto-claude/specs/013-recompilation-validation-system/spec.md` - Feature specification
- `docs/validation_system.md` - Validation system overview (to be created in Phase 6)
- Phase 3 implementation notes - ValidationOrchestrator, ReportGenerator, etc.
