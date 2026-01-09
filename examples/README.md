# Validation System Examples

This directory contains example scripts demonstrating various use cases for the VC Script Decompiler validation system.

## Overview

The validation system allows you to verify the accuracy of decompiled VC scripts by recompiling them with the original Pterodon compiler tools and comparing the resulting bytecode.

## Prerequisites

Before running these examples, ensure you have:

1. **Python 3.7+** installed
2. **vcdecomp package** installed or accessible in your Python path
3. **Original compiler tools** in `original-resources/compiler/` directory:
   - `SCMP.exe` (main compiler orchestrator)
   - `SPP.exe` (preprocessor)
   - `SCC.exe` (compiler)
   - `SASM.exe` (assembler)
4. **Test files** from `Compiler-testruns/` or your own decompiled scripts

## Examples

### 1. validate_single.py - Basic Single File Validation

Demonstrates basic validation workflow for a single script file.

**Purpose**: Learn the fundamentals of validation

**Usage**:
```bash
python examples/validate_single.py <original.scr> <decompiled.c>
```

**Example**:
```bash
# Validate a test script
python examples/validate_single.py \
    Compiler-testruns/Testrun1/tdm.scr \
    decompiled/tdm.c
```

**Features**:
- ✓ Simple validation workflow
- ✓ Colored console output
- ✓ Detailed difference reporting
- ✓ Interactive HTML report export
- ✓ Easy to understand and modify

**Learn**:
- How to create a `ValidationOrchestrator`
- How to run validation and interpret results
- How to generate reports with `ReportGenerator`
- Understanding validation verdicts (PASS, PARTIAL, FAIL, ERROR)

---

### 2. validate_batch.py - Batch Validation with Custom Filtering

Demonstrates batch validation of multiple scripts with custom filtering and parallel processing.

**Purpose**: Validate entire directories efficiently

**Usage**:
```bash
python examples/validate_batch.py <original_dir> <decompiled_dir>
```

**Example**:
```bash
# Validate all scripts in a mission directory
python examples/validate_batch.py \
    script-folders/mission_01/ \
    decompiled/mission_01/
```

**Features**:
- ✓ Automatic file pairing (matches .scr with .c files)
- ✓ Parallel validation (4 workers by default)
- ✓ Progress tracking
- ✓ Summary statistics
- ✓ Custom filtering (semantic differences, compilation failures)
- ✓ JSON report export
- ✓ Cache statistics

**Learn**:
- How to validate multiple files efficiently
- How to use `ThreadPoolExecutor` for parallel processing
- How to filter differences by category and severity
- How to aggregate validation results
- How to use `get_semantic_differences()` and `filter_by_severity()`

---

### 3. regression_test.py - Regression Testing

Demonstrates regression testing to detect when decompiler changes cause new failures or improvements.

**Purpose**: Track validation results over time for CI/CD integration

**Usage**:
```bash
# Create initial baseline
python examples/regression_test.py baseline <original_dir> <decompiled_dir>

# After decompiler changes, check for regressions
python examples/regression_test.py compare <original_dir> <decompiled_dir>

# Accept new results as baseline
python examples/regression_test.py update <original_dir> <decompiled_dir>
```

**Example**:
```bash
# Workflow:

# 1. Establish baseline
python examples/regression_test.py baseline \
    Compiler-testruns/ \
    decompiled/

# 2. Make decompiler improvements
# ... modify decompiler code ...

# 3. Check for regressions
python examples/regression_test.py compare \
    Compiler-testruns/ \
    decompiled/

# 4. If results are acceptable, update baseline
python examples/regression_test.py update \
    Compiler-testruns/ \
    decompiled/
```

**Features**:
- ✓ Baseline creation and management
- ✓ Regression detection (new failures)
- ✓ Improvement detection (new passes)
- ✓ Detailed comparison reports
- ✓ JSON report export
- ✓ Exit codes for CI/CD integration
- ✓ Automatic baseline backup on update

**Learn**:
- How to use `RegressionBaseline` class
- How to use `RegressionComparator` class
- How to detect regressions vs improvements
- How to integrate validation into CI/CD pipelines
- Understanding `RegressionStatus` and `RegressionReport`

**CI/CD Integration**:
```bash
# In your CI pipeline:
python examples/regression_test.py compare ../Compiler-testruns/ decompiled/

# Exit code 0: No regressions
# Exit code 1: Regressions detected (fail build)
```

---

### 4. custom_reporting.py - Custom Report Generation

Demonstrates how to generate custom validation reports with specific formatting and filtering.

**Purpose**: Learn advanced report generation techniques

**Usage**:
```bash
python examples/custom_reporting.py <original.scr> <decompiled.c>
```

**Example**:
```bash
python examples/custom_reporting.py \
    Compiler-testruns/Testrun1/tdm.scr \
    decompiled/tdm.c
```

**Features**:
- ✓ Custom text report with specific formatting
- ✓ Semantic-only report (filters out cosmetic differences)
- ✓ Statistics report (counts and percentages)
- ✓ Standard HTML report
- ✓ JSON report for programmatic use
- ✓ Multiple output formats in one run

**Generates**:
1. `{filename}_custom.txt` - Custom formatted text report
2. `{filename}_semantic.txt` - Semantic differences only
3. `{filename}_statistics.txt` - Statistics and percentages
4. `{filename}_validation.html` - Standard HTML report
5. `{filename}_validation.json` - JSON report

**Learn**:
- How to filter differences by category
- How to filter differences by severity
- How to create custom report formats
- How to use `get_semantic_differences()` and `get_cosmetic_differences()`
- How to aggregate statistics from `DifferenceSummary`

---

## Common Patterns

### Pattern 1: Basic Validation
```python
from vcdecomp.validation import ValidationOrchestrator

validator = ValidationOrchestrator(
    compiler_dir="original-resources/compiler"
)

result = validator.validate("original.scr", "decompiled.c")

if result.verdict == ValidationVerdict.PASS:
    print("Validation passed!")
```

### Pattern 2: Generate Reports
```python
from vcdecomp.validation import ReportGenerator

generator = ReportGenerator()

# Text report with colors
print(generator.generate_text_report(result, use_color=True))

# Save HTML report
generator.save_report(result, "report.html", format="html")

# Save JSON report
generator.save_report(result, "report.json", format="json")
```

### Pattern 3: Filter Differences
```python
from vcdecomp.validation import (
    get_semantic_differences,
    filter_by_severity,
    DifferenceSeverity
)

# Get only semantic differences (affects behavior)
semantic_diffs = get_semantic_differences(result.categorized_differences)

# Get only critical issues
critical_diffs = filter_by_severity(
    result.categorized_differences,
    DifferenceSeverity.CRITICAL
)
```

### Pattern 4: Regression Testing
```python
from vcdecomp.validation import RegressionBaseline, RegressionComparator

# Create baseline
baseline = RegressionBaseline(".validation-baseline.json")
baseline.add_result("test.scr", result)
baseline.save()

# Compare with baseline
comparator = RegressionComparator(baseline)
report = comparator.compare(current_results)

if report.regression_count > 0:
    print(f"Regressions detected: {report.regression_count}")
```

---

## Tips and Best Practices

### 1. Use Caching
Enable caching to speed up repeated validations:
```python
validator = ValidationOrchestrator(
    cache_enabled=True,
    cache_dir=".validation_cache"
)
```

### 2. Adjust Timeouts
Increase timeout for complex scripts:
```python
validator = ValidationOrchestrator(
    timeout=60  # 60 seconds for large scripts
)
```

### 3. Custom Include Directories
Specify additional header file locations:
```python
validator = ValidationOrchestrator(
    include_dirs=["inc/", "custom_headers/"]
)
```

### 4. Disable Cache for Single Run
Override cache setting per validation:
```python
result = validator.validate("test.scr", "test.c", use_cache=False)
```

### 5. Focus on Semantic Differences
Cosmetic differences (like different data ordering) don't affect program behavior:
```python
semantic_diffs = get_semantic_differences(result.categorized_differences)
if len(semantic_diffs) == 0:
    print("Bytecode is semantically equivalent!")
```

### 6. Check Critical Issues First
Critical differences (like wrong entry point) should be fixed immediately:
```python
critical = filter_by_severity(diffs, DifferenceSeverity.CRITICAL)
if critical:
    print("CRITICAL ISSUES FOUND:")
    for diff in critical:
        print(f"  - {diff.description}")
```

---

## Troubleshooting

### Issue: "Compiler directory not found"
**Solution**: Ensure `original-resources/compiler/` exists with all 4 executables:
```bash
ls original-resources/compiler/
# Should show: SCMP.exe, SPP.exe, SCC.exe, SASM.exe
```

### Issue: "Compilation failed with errors"
**Solution**: Check `compilation_result.errors` for details:
```python
if not result.compilation_succeeded:
    for error in result.compilation_result.errors:
        print(f"{error.file}:{error.line}: {error.message}")
```

### Issue: "Validation is slow"
**Solution**: Enable caching and use parallel processing:
```python
# Enable caching
validator = ValidationOrchestrator(cache_enabled=True)

# Use parallel processing for batch validation
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(validate_file, f) for f in files]
```

### Issue: "Too many cosmetic differences"
**Solution**: Filter to show only semantic differences:
```python
semantic_only = get_semantic_differences(result.categorized_differences)
print(f"Only {len(semantic_only)} semantic differences matter")
```

---

## Further Reading

- **User Guide**: `docs/validation_system.md`
- **API Reference**: `docs/validation_api.md`
- **GUI Documentation**: See validation panel in main application

---

## Support

For more information or issues:
- Check the main documentation in `docs/`
- Review test cases in `vcdecomp/tests/validation/`
- Examine the validation module source in `vcdecomp/validation/`
