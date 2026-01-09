# Validation System User Guide

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [GUI Usage](#gui-usage)
4. [CLI Usage](#cli-usage)
5. [Understanding Differences](#understanding-differences)
6. [Batch Validation](#batch-validation)
7. [Regression Testing](#regression-testing)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## Overview

The Validation System is a critical component of VC Script Decompiler that verifies the accuracy of decompiled code by recompiling it with the original Pterodon compiler tools and comparing the resulting bytecode.

### What is Validation?

Validation is the process of:

1. **Recompiling** decompiled source code using the original game compiler (SCMP.exe)
2. **Comparing** the recompiled bytecode against the original .SCR file
3. **Categorizing** differences as semantic (behavior-changing) or cosmetic (superficial)
4. **Reporting** results with actionable recommendations

### Why Validation Matters

- **Confidence**: Verify that decompilation accurately represents the original script
- **Quality Assurance**: Identify decompilation bugs before modding
- **Regression Testing**: Ensure decompiler improvements don't break existing functionality
- **Debugging**: Pinpoint exactly where decompilation differs from original code

---

## Quick Start

### Prerequisites

1. Original Pterodon compiler tools in `original-resources/compiler/`:
   - SCMP.exe (orchestrator)
   - SPP.exe (preprocessor)
   - SCC.exe (compiler)
   - SASM.exe (assembler)

2. Original .SCR file and decompiled source code

### Simple Validation (CLI)

```bash
# Validate a single decompiled script
python -m vcdecomp validate original.scr decompiled.c
```

### Simple Validation (GUI)

1. Open VC Script Decompiler GUI
2. Click **View** → **Validation Panel**
3. Click **Validate** button
4. Select original .SCR and decompiled .c files
5. View results in the validation panel

---

## GUI Usage

### Opening the Validation Panel

The validation panel is available from the main window:

**View Menu** → **Validation Panel**

Or use the dock widget at the bottom of the window.

### Configuring Settings

Before your first validation, configure the compiler location:

1. Click **Settings...** button in the validation panel
2. **Compiler Tab**:
   - Browse to compiler directory (contains SCMP.exe, SPP.exe, etc.)
   - Set compilation timeout (default: 30 seconds)
3. **Headers Tab**:
   - Add include directories for header files
   - Headers from `original-resources/h/` and `original-resources/inc/`
4. **Comparison Tab**:
   - Select opcode variant (auto/v1.60/v1.00)
   - Configure difference filtering
5. **Cache Tab**:
   - Enable/disable validation caching
   - Set cache directory and expiration
6. Click **OK** to save settings

Settings persist across sessions automatically.

### Running a Validation

1. Click **Validate** button
2. Select original .SCR file
3. Select decompiled .c source file
4. Wait for validation to complete

### Understanding the Progress Display

During validation, you'll see:

- **Status message**: Current operation (compiling, comparing, etc.)
- **Progress bar**: Percentage complete (0-100%)
- **Time estimate**: Estimated time remaining
- **Cancel button**: Stop validation mid-process

Progress stages:
- 0-5%: Initialization
- 5-45%: Compilation (SPP, SCC, SASM)
- 45-80%: Bytecode comparison (header, data, code, XFN)
- 80-95%: Analysis and categorization
- 95-100%: Finalization

### Viewing Results

Results are displayed in two sections:

#### Summary Panel (Top)
- **Verdict**: PASS, PARTIAL, FAIL, or ERROR
- **Files**: Original and recompiled paths
- **Compilation**: Success or error details
- **Differences**: Count by category

#### Differences Tree (Bottom)
Hierarchical view of all differences:
- **Grouped by category**: Semantic, Cosmetic, Optimization, Unknown
- **Grouped by severity**: Critical, Major, Minor, Info
- **Color-coded**: Red (critical), Orange (major), Yellow (minor), Cyan (info)
- **Double-click**: View detailed difference information

### Exporting Reports

After validation completes:

1. Click **Export Report** button
2. Choose format: HTML, JSON, or Text
3. Select save location
4. Report includes all differences and recommendations

**Format Guide**:
- **HTML**: Interactive report with expandable sections (best for viewing)
- **JSON**: Structured data for programmatic analysis
- **Text**: Plain text with optional ANSI colors (best for logs)

---

## CLI Usage

### Basic Commands

#### Single File Validation

```bash
python -m vcdecomp validate <original.scr> <source.c> [options]
```

**Example:**
```bash
python -m vcdecomp validate mission_01.scr mission_01_decompiled.c
```

#### Batch Validation

```bash
python -m vcdecomp validate-batch --input-dir <dir> --original-dir <dir> [options]
```

**Example:**
```bash
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --jobs 8
```

### Command Options

#### Single File Validation Options

| Option | Description | Default |
|--------|-------------|---------|
| `--compiler-dir PATH` | Compiler directory location | `original-resources/compiler` |
| `--output-format {text,json,html}` | Output format | `text` |
| `--report-file PATH` | Save report to file | None (console only) |
| `--no-cache` | Disable validation cache | Caching enabled |
| `--no-color` | Disable ANSI colors | Colors enabled |

**Example with options:**
```bash
python -m vcdecomp validate mission_01.scr mission_01.c \
    --compiler-dir /path/to/compiler \
    --output-format html \
    --report-file validation_report.html \
    --no-cache
```

#### Batch Validation Options

| Option | Description | Default |
|--------|-------------|---------|
| `--input-dir DIR` | Directory with decompiled .c files | Required |
| `--original-dir DIR` | Directory with original .scr files | Required |
| `--compiler-dir PATH` | Compiler directory location | `original-resources/compiler` |
| `--jobs N` | Number of parallel validation jobs | 4 |
| `--report-file PATH` | Save JSON summary report | None |
| `--no-cache` | Disable validation cache | Caching enabled |

**Example with options:**
```bash
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --jobs 8 \
    --report-file batch_summary.json \
    --no-cache
```

### Exit Codes

The CLI returns exit codes for automation:

| Exit Code | Meaning |
|-----------|---------|
| 0 | PASS - validation succeeded |
| 1 | FAIL/PARTIAL - semantic differences detected |
| 2 | ERROR - compilation or validation error |

**CI/CD Example:**
```bash
if python -m vcdecomp validate original.scr decompiled.c; then
    echo "✓ Validation passed"
else
    echo "✗ Validation failed"
    exit 1
fi
```

---

## Understanding Differences

### Difference Categories

The validation system categorizes all differences into four types:

#### 1. Semantic Differences ⚠️

**Impact**: Changes script behavior

Semantic differences indicate that the recompiled bytecode will behave differently from the original. These must be fixed.

**Examples:**
- Different entry point
- Wrong opcode (e.g., ADD instead of SUB)
- Different constant value
- Missing or extra external function call
- Wrong parameter types

**What to do:**
- Review decompiled source code
- Check for decompilation errors
- Verify type inference
- Check control flow reconstruction

#### 2. Cosmetic Differences ✓

**Impact**: No behavior change

Cosmetic differences don't affect script behavior. They result from:
- Different data segment ordering
- Different alignment padding
- Different local variable allocation

**Examples:**
- String constants in different order
- Different padding bytes
- Constants at different offsets

**What to do:**
- Usually safe to ignore
- Verify no semantic impact
- Consider acceptable if behavior matches

#### 3. Optimization Differences 🔧

**Impact**: Minor performance difference, same behavior

Optimization differences indicate equivalent code with different performance characteristics.

**Examples:**
- `INC` instruction vs `ADD 1`
- `DEC` instruction vs `SUB 1`
- `MUL 2` vs left shift by 1 (`LS 1`)

**What to do:**
- Generally acceptable
- Behavior is semantically equivalent
- May affect performance minimally

#### 4. Unknown Differences ❓

**Impact**: Unclear

Differences that couldn't be automatically categorized.

**What to do:**
- Manually review
- Determine if semantic or cosmetic
- Report if categorization is incorrect

### Difference Severity Levels

Each difference has a severity level:

| Severity | Color | Description |
|----------|-------|-------------|
| **CRITICAL** | 🔴 Red | Breaks script execution (wrong entry point, missing function) |
| **MAJOR** | 🟠 Orange | Changes behavior (wrong opcode, wrong value) |
| **MINOR** | 🟡 Yellow | Likely cosmetic (reordering, extra data) |
| **INFO** | 🔵 Cyan | Informational only (alignment, padding) |

### Validation Verdicts

After comparison, validation returns one of four verdicts:

#### PASS ✅
- No semantic differences detected
- Only cosmetic differences (if any)
- Script behavior matches original
- **Safe to use for modding**

#### PARTIAL ⚠️
- Compilation succeeded
- Some differences detected
- Mix of semantic and cosmetic differences
- **Review differences before using**

#### FAIL ❌
- Compilation succeeded
- Significant semantic differences
- Behavior differs from original
- **Do not use for modding**

#### ERROR 🚫
- Compilation failed
- Cannot compare bytecode
- Syntax or compilation errors
- **Fix compilation errors first**

---

## Batch Validation

### Overview

Batch validation validates multiple files at once with parallel processing.

### Basic Usage

```bash
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/
```

This will:
1. Find all `.c` files in `decompiled/`
2. Match with `.scr` files in `scripts/` by name
3. Validate all pairs in parallel (4 jobs by default)
4. Display progress and summary

### File Matching

Files are matched by name:
```
decompiled/mission_01.c  →  scripts/mission_01.scr
decompiled/mission_02.c  →  scripts/mission_02.scr
```

### Parallel Processing

Control parallelism with `--jobs`:

```bash
# Use 8 parallel jobs (faster on multi-core CPUs)
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --jobs 8

# Use 1 job (sequential, easier to debug)
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --jobs 1
```

**Recommended values:**
- 1 job: Debugging
- 4 jobs: Default, balanced
- 8 jobs: Fast multi-core systems
- CPU cores: Maximum parallelism

### Progress Display

During batch validation:
```
Progress:
------------------------------------------------------------
[=============================>                     ] 14/25 | ✓ level_01.c                   PASS
```

- **Progress bar**: Visual indicator (50 chars)
- **Counter**: Completed/total files
- **Status**: ✓ (PASS), ! (FAIL/PARTIAL), ✗ (ERROR)
- **Filename**: Current file being processed
- **Verdict**: PASS, FAIL, PARTIAL, or ERROR

### Summary Report

After completion:
```
Summary Report
============================================================
Total files:     25
Passed:          20
Failed:          3
Partial:         1
Errors:          1

Failed/Error Files:
------------------------------------------------------------
✗ level_05.c: 12 differences (3 semantic)
✗ level_12.c: Compilation failed - Syntax error at line 42
```

### Saving Reports

Save batch results to JSON:

```bash
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --report-file batch_results.json
```

The JSON report includes:
- Timestamp
- Directory paths
- Per-file results
- Summary statistics

---

## Regression Testing

### Overview

Regression testing detects when decompiler changes introduce new failures (regressions) or fix existing issues (improvements).

### Creating a Baseline

Save current validation results as a baseline:

```bash
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --save-baseline
```

This creates `.validation-baseline.json` with expected results.

### Running Regression Tests

Compare current results against the baseline:

```bash
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --regression
```

### Understanding Regression Results

#### Regression 🔻
- Was PASS in baseline
- Is now FAIL or PARTIAL
- Indicates decompiler broke something
- **Must be fixed**

#### Improvement 🔺
- Was FAIL in baseline
- Is now PASS
- Indicates decompiler fixed an issue
- **Good news!**

#### Stable ↔️
- Same result as baseline
- No change in behavior

#### New ➕
- File not in baseline
- New decompiled script

### Example Output

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

✓ IMPROVEMENTS DETECTED:
------------------------------------------------------------
✓ ai_controller.c:
  Baseline: FAIL (3 semantic)
  Current:  PASS (0 semantic)
```

### CI/CD Integration

Use regression testing in continuous integration:

```bash
#!/bin/bash
# regression_test.sh

# Run decompiler on test suite
./decompile_all.sh

# Run regression test
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --regression \
    --report-file regression_report.json

# Check exit code
if [ $? -eq 1 ]; then
    echo "❌ Regressions detected! See regression_report.json"
    exit 1
else
    echo "✅ No regressions!"
fi
```

### Updating the Baseline

After fixing regressions and confirming improvements:

```bash
# Update baseline to new validated state
python -m vcdecomp validate-batch \
    --input-dir decompiled/ \
    --original-dir scripts/ \
    --save-baseline
```

---

## Troubleshooting

### Compilation Errors

#### Error: "Compiler directory not found"

**Cause**: SCMP.exe and related tools not found

**Solution**:
1. Verify compiler tools are in `original-resources/compiler/`
2. Or specify custom location: `--compiler-dir /path/to/compiler`
3. Ensure all 4 executables present:
   - SCMP.exe
   - SPP.exe
   - SCC.exe
   - SASM.exe

#### Error: "Compilation failed at SPP stage"

**Cause**: Preprocessor errors (missing headers, macro issues)

**Solution**:
1. Check include directories in settings
2. Add paths to header files: `original-resources/h/` and `original-resources/inc/`
3. Verify header files exist (sc_global.h, sc_def.h, etc.)
4. Check for missing #include directives in decompiled code

#### Error: "Compilation failed at SCC stage"

**Cause**: Compiler errors (syntax, type errors)

**Solution**:
1. Review decompiled source code for syntax errors
2. Check for missing semicolons, braces, parentheses
3. Verify function declarations match usage
4. Check type compatibility

#### Error: "Compilation failed at SASM stage"

**Cause**: Assembly errors (invalid instructions, labels)

**Solution**:
1. Usually indicates decompiler bug
2. Check for corrupted intermediate files
3. Try recompiling without cache: `--no-cache`
4. Report issue to decompiler developers

### Comparison Issues

#### Many Cosmetic Differences

**Cause**: Different constant ordering, alignment

**Solution**:
- Usually safe if verdict is PASS
- Verify no semantic differences
- Review differences to confirm cosmetic nature

#### Semantic Differences in Simple Scripts

**Cause**: Decompilation inaccuracies

**Solution**:
1. Compare decompiled code with original bytecode manually
2. Check control flow reconstruction
3. Verify type inference (int vs float)
4. Check for incorrect operator decompilation

#### XFN Table Differences

**Cause**: Missing or extra external function references

**Solution**:
1. Check external function calls in decompiled code
2. Verify function names match exactly (case-sensitive)
3. Check function signatures (parameter count, types)
4. Ensure all SC_* functions are declared

### Performance Issues

#### Slow Compilation

**Cause**: Large scripts, complex headers

**Solution**:
1. Increase timeout in settings (GUI) or wait longer (CLI)
2. Use validation cache for repeated runs
3. Simplify header includes if possible

#### Slow Batch Validation

**Cause**: Sequential processing, many files

**Solution**:
1. Increase parallel jobs: `--jobs 8`
2. Enable validation cache
3. Use faster storage (SSD)

### Cache Issues

#### Cache Not Working

**Cause**: Cache disabled or corrupted

**Solution**:
1. Verify cache is enabled in settings (GUI)
2. Check cache directory exists and is writable
3. Clear cache and retry:
   - GUI: Settings → Cache → Clear Cache Now
   - CLI: Delete `.validation_cache/` directory

#### Stale Cache Results

**Cause**: Source or headers changed but cache not invalidated

**Solution**:
1. Use `--no-cache` flag to force revalidation
2. Clear entire cache
3. Cache automatically detects source file changes via hash

---

## Best Practices

### For Modders

1. **Always validate before releasing mods**
   - Ensures your changes compile correctly
   - Verifies no unintended behavior changes

2. **Accept cosmetic differences**
   - Focus on semantic differences
   - Cosmetic differences don't affect gameplay

3. **Test in-game after validation**
   - Validation confirms bytecode equivalence
   - In-game testing confirms actual behavior

### For Decompiler Developers

1. **Use regression testing**
   - Create baseline before making changes
   - Run regression tests after each change
   - Update baseline only after confirming improvements

2. **Fix semantic differences first**
   - Critical and major severity
   - Directly impact decompilation accuracy

3. **Minimize cosmetic differences**
   - Improve data segment reconstruction
   - Match original constant ordering when possible

4. **Document known issues**
   - Track files with expected differences
   - Note limitations in baseline

### For CI/CD Pipelines

1. **Automate regression testing**
   ```bash
   python -m vcdecomp validate-batch \
       --input-dir decompiled/ \
       --original-dir scripts/ \
       --regression
   ```

2. **Use appropriate exit codes**
   - Check exit code for pass/fail
   - Exit 0 = success, non-zero = failure

3. **Save reports as artifacts**
   ```bash
   --report-file regression_report_$BUILD_NUMBER.json
   ```

4. **Set reasonable timeouts**
   - Large test suites may take time
   - Balance speed vs thoroughness

### Performance Optimization

1. **Enable caching**
   - Dramatically speeds up repeated validations
   - Automatically invalidates on source changes

2. **Use parallel processing**
   - `--jobs` flag for batch validation
   - Scales with CPU cores

3. **Optimize compiler directory location**
   - Use local drive (not network share)
   - SSD recommended for temporary files

---

## Additional Resources

- **API Documentation**: See `validation_api.md` for programmatic usage
- **Technical Documentation**: See `docs/SCC_TECHNICAL_ANALYSIS.md` for compiler details
- **Examples**: See `examples/` directory for sample scripts:
  - `validate_single.py` - Basic single file validation
  - `validate_batch.py` - Batch validation with custom filtering
  - `regression_test.py` - Regression testing for CI/CD
  - `custom_reporting.py` - Custom report generation
- **Issue Tracker**: Report bugs and issues on GitHub

---

**Document Version**: 1.0
**Last Updated**: 2026-01-09
**Part of**: VC Script Decompiler - Recompilation Validation System
