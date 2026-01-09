# Validation System API Reference

## Table of Contents

1. [Overview](#overview)
2. [Module Structure](#module-structure)
3. [Quick Start](#quick-start)
4. [Core Classes](#core-classes)
5. [Compilation](#compilation)
6. [Bytecode Comparison](#bytecode-comparison)
7. [Validation Workflow](#validation-workflow)
8. [Report Generation](#report-generation)
9. [Caching](#caching)
10. [Regression Testing](#regression-testing)
11. [Code Examples](#code-examples)

---

## Overview

The validation system provides a Python API for programmatic validation of decompiled VC scripts. This documentation covers all public classes, methods, and usage patterns.

### Installation

The validation system is part of the `vcdecomp` package:

```python
from vcdecomp.validation import (
    ValidationOrchestrator,
    ReportGenerator,
    BytecodeComparator,
    # ... other imports
)
```

---

## Module Structure

The `vcdecomp.validation` module is organized into several submodules:

```
vcdecomp/validation/
├── __init__.py              # Public API exports
├── compiler_wrapper.py      # Compiler tool wrappers
├── compilation_types.py     # Compilation result types
├── bytecode_compare.py      # Bytecode comparison engine
├── difference_types.py      # Difference categorization
├── validator.py             # Main validation orchestrator
├── validation_types.py      # Validation result types
├── report_generator.py      # Report formatting
├── cache.py                 # Validation caching
└── regression.py            # Regression testing
```

### Public API

All public classes and functions are exported from `vcdecomp.validation`:

```python
from vcdecomp.validation import (
    # Compilation
    BaseCompiler,
    SCMPWrapper,
    SPPWrapper,
    SCCWrapper,
    SASMWrapper,
    CompilationResult,
    CompilationError,
    CompilationStage,
    ErrorSeverity,

    # Bytecode comparison
    BytecodeComparator,
    ComparisonResult,
    SectionComparison,
    Difference,
    DifferenceType,
    DifferenceSeverity,

    # Difference categorization
    DifferenceCategory,
    DifferenceCategorizer,
    CategorizedDifference,
    DifferenceSummary,
    categorize_differences,
    get_summary,
    filter_by_category,
    filter_by_severity,
    get_semantic_differences,
    get_cosmetic_differences,

    # Validation
    ValidationResult,
    ValidationVerdict,
    ValidationOrchestrator,

    # Reporting
    ReportGenerator,
    ANSIColors,

    # Caching
    ValidationCache,
    CacheEntry,
    CacheStatistics,

    # Regression testing
    RegressionBaseline,
    RegressionComparator,
    RegressionReport,
    RegressionItem,
    RegressionStatus,
    BaselineEntry,
)
```

---

## Quick Start

### Simple Validation

```python
from vcdecomp.validation import ValidationOrchestrator

# Create orchestrator
validator = ValidationOrchestrator(
    compiler_dir="original-resources/compiler"
)

# Run validation
result = validator.validate(
    original_scr_path="mission_01.scr",
    source_path="mission_01_decompiled.c"
)

# Check result
if result.verdict == ValidationVerdict.PASS:
    print("✓ Validation passed!")
else:
    print(f"✗ Validation failed: {result.verdict}")
    print(f"Semantic differences: {result.difference_summary.semantic_count}")
```

### Generate Report

```python
from vcdecomp.validation import ValidationOrchestrator, ReportGenerator

# Validate
validator = ValidationOrchestrator()
result = validator.validate("original.scr", "decompiled.c")

# Generate report
generator = ReportGenerator()

# Text report to console
print(generator.generate_text_report(result))

# HTML report to file
generator.save_report(result, "validation_report.html", format="html")
```

---

## Core Classes

### ValidationOrchestrator

**Purpose**: High-level validation workflow coordinator

**Constructor**:
```python
ValidationOrchestrator(
    compiler_dir: str = "original-resources/compiler",
    include_dirs: List[str] = None,
    timeout: int = 30,
    opcode_variant: str = "auto",
    cache_dir: str = ".validation_cache",
    cache_enabled: bool = True,
    cache_max_age: int = 0
)
```

**Parameters**:
- `compiler_dir`: Path to directory containing SCMP.exe, SPP.exe, SCC.exe, SASM.exe
- `include_dirs`: List of directories to search for header files
- `timeout`: Compilation timeout in seconds (default: 30)
- `opcode_variant`: SCR opcode variant ("auto", "v1.60", "v1.00")
- `cache_dir`: Directory for cache storage (default: `.validation_cache`)
- `cache_enabled`: Enable validation caching (default: True)
- `cache_max_age`: Cache expiration in seconds (0 = no expiration)

**Methods**:

#### validate()
```python
def validate(
    self,
    original_scr_path: str,
    source_path: str,
    use_cache: bool = None
) -> ValidationResult
```

Validates decompiled source code against original bytecode.

**Parameters**:
- `original_scr_path`: Path to original .SCR file
- `source_path`: Path to decompiled .c source file
- `use_cache`: Override cache setting (None = use orchestrator setting)

**Returns**: `ValidationResult` object

**Raises**:
- `FileNotFoundError`: If files don't exist
- `ValidationError`: If validation fails

**Example**:
```python
validator = ValidationOrchestrator(compiler_dir="compiler/")
result = validator.validate("test.scr", "test.c")
print(f"Verdict: {result.verdict}")
```

#### get_cache_statistics()
```python
def get_cache_statistics(self) -> CacheStatistics
```

Returns cache performance statistics.

**Returns**: `CacheStatistics` with hits, misses, and hit rate

#### clear_cache()
```python
def clear_cache(self) -> int
```

Clears all cached validation results.

**Returns**: Number of entries removed

---

## Compilation

### SCMPWrapper

**Purpose**: Wrapper for SCMP.exe (full compilation orchestrator)

**Constructor**:
```python
SCMPWrapper(
    compiler_dir: str,
    timeout: int = 30
)
```

**Methods**:

#### compile()
```python
def compile(
    self,
    source_path: str,
    output_path: str,
    include_dirs: List[str] = None,
    keep_temp_files: bool = False
) -> CompilationResult
```

Compiles source .c file to .scr bytecode.

**Parameters**:
- `source_path`: Input .c file
- `output_path`: Output .scr file
- `include_dirs`: Directories for header search
- `keep_temp_files`: Preserve intermediate files for debugging

**Returns**: `CompilationResult`

**Example**:
```python
from vcdecomp.validation import SCMPWrapper

wrapper = SCMPWrapper(compiler_dir="compiler/")
result = wrapper.compile(
    source_path="test.c",
    output_path="test.scr",
    include_dirs=["headers/"]
)

if result.success:
    print("Compilation succeeded!")
else:
    for error in result.errors:
        print(f"{error.file}:{error.line}: {error.message}")
```

### SPPWrapper

**Purpose**: Wrapper for SPP.exe (preprocessor)

**Constructor**:
```python
SPPWrapper(
    compiler_dir: str,
    timeout: int = 30
)
```

**Methods**:

#### preprocess()
```python
def preprocess(
    self,
    source_path: str,
    output_path: str,
    include_dirs: List[str] = None
) -> CompilationResult
```

Preprocesses source file (handles #include, #define, etc.).

**Returns**: `CompilationResult` with preprocessed output

### SCCWrapper

**Purpose**: Wrapper for SCC.exe (compiler)

**Constructor**:
```python
SCCWrapper(
    compiler_dir: str,
    timeout: int = 30
)
```

**Methods**:

#### compile()
```python
def compile(
    self,
    source_path: str,
    output_path: str
) -> CompilationResult
```

Compiles preprocessed source to assembly (.sca).

### SASMWrapper

**Purpose**: Wrapper for SASM.exe (assembler)

**Constructor**:
```python
SASMWrapper(
    compiler_dir: str,
    timeout: int = 30
)
```

**Methods**:

#### assemble()
```python
def assemble(
    self,
    assembly_path: str,
    output_path: str
) -> CompilationResult
```

Assembles .sca file to .scr bytecode.

### CompilationResult

**Purpose**: Represents compilation outcome

**Attributes**:
- `success: bool` - Compilation succeeded
- `output_path: str` - Path to output file
- `errors: List[CompilationError]` - Compilation errors
- `warnings: List[CompilationError]` - Compilation warnings
- `stdout: str` - Standard output
- `stderr: str` - Standard error
- `returncode: int` - Process return code
- `stage: CompilationStage` - Stage where error occurred (if any)
- `working_dir: str` - Temporary working directory
- `intermediate_files: Dict[str, str]` - Intermediate file paths

**Methods**:

#### has_errors()
```python
def has_errors(self) -> bool
```

Returns True if compilation had errors.

#### has_warnings()
```python
def has_warnings(self) -> bool
```

Returns True if compilation had warnings.

#### error_count()
```python
def error_count(self) -> int
```

Returns number of errors.

#### warning_count()
```python
def warning_count(self) -> int
```

Returns number of warnings.

#### get_errors_by_stage()
```python
def get_errors_by_stage(self, stage: CompilationStage) -> List[CompilationError]
```

Returns errors for a specific compilation stage.

### CompilationError

**Purpose**: Represents a single compilation error or warning

**Attributes**:
- `file: str` - Source file
- `line: int` - Line number
- `column: int` - Column number
- `message: str` - Error message
- `severity: ErrorSeverity` - ERROR or WARNING
- `stage: CompilationStage` - Compilation stage (SPP, SCC, SASM)

---

## Bytecode Comparison

### BytecodeComparator

**Purpose**: Deep comparison of two .SCR files

**Constructor**:
```python
BytecodeComparator(opcode_variant: str = "auto")
```

**Parameters**:
- `opcode_variant`: SCR format variant ("auto", "v1.60", "v1.00")

**Methods**:

#### compare_files()
```python
def compare_files(
    self,
    original_path: str,
    recompiled_path: str
) -> ComparisonResult
```

Compares two .SCR files section by section.

**Parameters**:
- `original_path`: Path to original .SCR file
- `recompiled_path`: Path to recompiled .SCR file

**Returns**: `ComparisonResult` with all differences

**Example**:
```python
from vcdecomp.validation import BytecodeComparator

comparator = BytecodeComparator()
result = comparator.compare_files("original.scr", "recompiled.scr")

print(f"Total differences: {len(result.all_differences)}")
for diff in result.all_differences:
    print(f"{diff.type}: {diff.description}")
```

### ComparisonResult

**Purpose**: Contains all differences found during comparison

**Attributes**:
- `original_path: str` - Original .SCR path
- `recompiled_path: str` - Recompiled .SCR path
- `all_differences: List[Difference]` - All differences
- `sections: Dict[str, SectionComparison]` - Per-section results
- `files_identical: bool` - True if files are identical

**Methods**:

#### get_differences_by_type()
```python
def get_differences_by_type(self, diff_type: DifferenceType) -> List[Difference]
```

Returns differences of a specific type (HEADER, DATA, CODE, XFN).

#### get_differences_by_severity()
```python
def get_differences_by_severity(self, severity: DifferenceSeverity) -> List[Difference]
```

Returns differences of a specific severity (CRITICAL, MAJOR, MINOR, INFO).

### Difference

**Purpose**: Represents a single difference between files

**Attributes**:
- `type: DifferenceType` - HEADER, DATA, CODE, XFN, STRUCTURE
- `severity: DifferenceSeverity` - CRITICAL, MAJOR, MINOR, INFO
- `description: str` - Human-readable description
- `details: Dict` - Additional context
- `location: str` - Location in file (section, offset, etc.)

**DifferenceType Enum**:
- `HEADER` - Header differences
- `DATA` - Data segment differences
- `CODE` - Code segment differences
- `XFN` - External function table differences
- `STRUCTURE` - File structure differences

**DifferenceSeverity Enum**:
- `CRITICAL` - Breaks execution
- `MAJOR` - Changes behavior
- `MINOR` - Likely cosmetic
- `INFO` - Informational only

---

## Validation Workflow

### ValidationResult

**Purpose**: Complete validation outcome with all details

**Attributes**:
- `verdict: ValidationVerdict` - Overall result (PASS, FAIL, PARTIAL, ERROR)
- `original_scr_path: str` - Original .SCR path
- `recompiled_scr_path: str` - Recompiled .SCR path
- `source_path: str` - Source .c path
- `compilation_result: CompilationResult` - Compilation outcome
- `comparison_result: ComparisonResult` - Comparison outcome
- `categorized_differences: List[CategorizedDifference]` - Categorized differences
- `difference_summary: DifferenceSummary` - Summary statistics
- `recommendations: List[str]` - Actionable recommendations
- `timestamp: datetime` - Validation timestamp

**Properties**:

#### compilation_succeeded
```python
@property
def compilation_succeeded(self) -> bool
```

Returns True if compilation succeeded.

**Methods**:

#### get_differences_by_category()
```python
def get_differences_by_category(
    self,
    category: DifferenceCategory
) -> List[CategorizedDifference]
```

Returns differences of a specific category (SEMANTIC, COSMETIC, OPTIMIZATION).

#### to_dict()
```python
def to_dict(self) -> Dict
```

Serializes result to dictionary (JSON-compatible).

#### to_json()
```python
def to_json(self) -> str
```

Serializes result to JSON string.

**Example**:
```python
result = validator.validate("test.scr", "test.c")

# Check verdict
if result.verdict == ValidationVerdict.PASS:
    print("✓ Validation passed")

# Get semantic differences
semantic = result.get_differences_by_category(DifferenceCategory.SEMANTIC)
print(f"Semantic differences: {len(semantic)}")

# Save to JSON
with open("result.json", "w") as f:
    f.write(result.to_json())
```

### ValidationVerdict

**Purpose**: Overall validation outcome

**Enum Values**:
- `PASS` - No semantic differences, validation passed
- `PARTIAL` - Some differences, may be acceptable
- `FAIL` - Significant semantic differences
- `ERROR` - Compilation or validation error

---

## Report Generation

### ReportGenerator

**Purpose**: Formats validation results into human-readable reports

**Constructor**:
```python
ReportGenerator(
    use_colors: bool = True
)
```

**Parameters**:
- `use_colors`: Enable ANSI colors in text reports (default: True)

**Methods**:

#### generate_text_report()
```python
def generate_text_report(
    self,
    result: ValidationResult
) -> str
```

Generates color-coded text report.

**Returns**: String with ANSI color codes

**Example**:
```python
generator = ReportGenerator()
report = generator.generate_text_report(result)
print(report)
```

#### generate_html_report()
```python
def generate_html_report(
    self,
    result: ValidationResult
) -> str
```

Generates interactive HTML report with expandable sections.

**Returns**: HTML string (standalone, includes CSS/JS)

#### generate_json_report()
```python
def generate_json_report(
    self,
    result: ValidationResult
) -> str
```

Generates structured JSON report.

**Returns**: JSON string

#### save_report()
```python
def save_report(
    self,
    result: ValidationResult,
    output_path: str,
    format: str = None
) -> None
```

Saves report to file.

**Parameters**:
- `result`: ValidationResult to format
- `output_path`: Output file path
- `format`: Format ("text", "html", "json"). Auto-detected from extension if None

**Example**:
```python
generator = ReportGenerator()

# Auto-detect format from extension
generator.save_report(result, "report.html")  # HTML
generator.save_report(result, "report.json")  # JSON
generator.save_report(result, "report.txt")   # Text

# Explicit format
generator.save_report(result, "output.txt", format="html")  # HTML in .txt file
```

---

## Caching

### ValidationCache

**Purpose**: Cache validation results to avoid redundant recompilation

**Constructor**:
```python
ValidationCache(
    cache_dir: str = ".validation_cache",
    max_age_seconds: int = 0
)
```

**Parameters**:
- `cache_dir`: Directory for cache storage
- `max_age_seconds`: Cache expiration (0 = no expiration)

**Methods**:

#### get()
```python
def get(
    self,
    source_path: str,
    scr_path: str
) -> Optional[ValidationResult]
```

Retrieves cached validation result.

**Returns**: Cached ValidationResult or None if not found/expired

#### set()
```python
def set(
    self,
    source_path: str,
    scr_path: str,
    result: ValidationResult
) -> None
```

Stores validation result in cache.

#### invalidate()
```python
def invalidate(
    self,
    source_path: str,
    scr_path: str
) -> bool
```

Invalidates cached result for specific files.

**Returns**: True if entry was invalidated

#### clear()
```python
def clear(self) -> int
```

Clears all cached entries.

**Returns**: Number of entries removed

#### get_statistics()
```python
def get_statistics(self) -> CacheStatistics
```

Returns cache performance statistics.

**Example**:
```python
from vcdecomp.validation import ValidationCache

cache = ValidationCache(cache_dir=".cache", max_age_seconds=86400)  # 24 hours

# Try to get cached result
cached = cache.get("test.c", "test.scr")
if cached:
    print("Using cached result")
    result = cached
else:
    print("Running validation...")
    result = validator.validate("test.scr", "test.c")
    cache.set("test.c", "test.scr", result)

# Get statistics
stats = cache.get_statistics()
print(f"Cache hit rate: {stats.hit_rate:.1%}")
```

### CacheStatistics

**Purpose**: Cache performance metrics

**Attributes**:
- `hits: int` - Cache hits
- `misses: int` - Cache misses
- `invalidations: int` - Cache invalidations
- `total_entries: int` - Total cached entries
- `hit_rate: float` - Hit rate (0.0-1.0)

---

## Regression Testing

### RegressionBaseline

**Purpose**: Stores expected validation outcomes

**Constructor**:
```python
RegressionBaseline(
    version: str = "1.0",
    description: str = ""
)
```

**Methods**:

#### add_entry()
```python
def add_entry(
    self,
    file: str,
    verdict: ValidationVerdict,
    compilation_succeeded: bool,
    differences_count: int,
    semantic_differences: int
) -> None
```

Adds file to baseline.

#### save()
```python
def save(self, path: str) -> None
```

Saves baseline to JSON file.

#### load()
```python
@classmethod
def load(cls, path: str) -> RegressionBaseline
```

Loads baseline from JSON file.

**Example**:
```python
from vcdecomp.validation import RegressionBaseline

# Create baseline
baseline = RegressionBaseline(description="Test suite baseline")
baseline.add_entry(
    file="test1.c",
    verdict=ValidationVerdict.PASS,
    compilation_succeeded=True,
    differences_count=0,
    semantic_differences=0
)
baseline.save(".validation-baseline.json")

# Load baseline
loaded = RegressionBaseline.load(".validation-baseline.json")
```

### RegressionComparator

**Purpose**: Compares current results against baseline

**Constructor**:
```python
RegressionComparator(baseline: RegressionBaseline)
```

**Methods**:

#### compare()
```python
def compare(
    self,
    current_results: Dict[str, ValidationResult]
) -> RegressionReport
```

Compares current validation results against baseline.

**Parameters**:
- `current_results`: Dictionary mapping filename to ValidationResult

**Returns**: `RegressionReport` with regressions and improvements

**Example**:
```python
from vcdecomp.validation import RegressionBaseline, RegressionComparator

# Load baseline
baseline = RegressionBaseline.load(".validation-baseline.json")

# Run current validations
current_results = {}
for file in files:
    result = validator.validate(file.scr, file.c)
    current_results[file.c] = result

# Compare
comparator = RegressionComparator(baseline)
report = comparator.compare(current_results)

# Check for regressions
if report.regressions:
    print(f"⚠ {len(report.regressions)} regressions detected!")
    for reg in report.regressions:
        print(f"  {reg.file}: {reg.baseline_verdict} → {reg.current_verdict}")
```

### RegressionReport

**Purpose**: Results of regression comparison

**Attributes**:
- `baseline_path: str` - Baseline file path
- `regressions: List[RegressionItem]` - Files that regressed
- `improvements: List[RegressionItem]` - Files that improved
- `stable_pass: List[RegressionItem]` - Files still passing
- `stable_fail: List[RegressionItem]` - Files still failing
- `new_files: List[RegressionItem]` - Files not in baseline

**Properties**:

#### has_regressions
```python
@property
def has_regressions(self) -> bool
```

Returns True if any regressions detected.

**Methods**:

#### to_dict()
```python
def to_dict(self) -> Dict
```

Serializes report to dictionary.

#### to_json()
```python
def to_json(self) -> str
```

Serializes report to JSON string.

### RegressionItem

**Purpose**: Single file regression comparison

**Attributes**:
- `file: str` - Filename
- `status: RegressionStatus` - REGRESSION, IMPROVEMENT, PASS, FAIL, NEW
- `baseline_verdict: ValidationVerdict` - Baseline verdict
- `current_verdict: ValidationVerdict` - Current verdict
- `baseline_differences: int` - Baseline difference count
- `current_differences: int` - Current difference count
- `baseline_semantic: int` - Baseline semantic count
- `current_semantic: int` - Current semantic count

---

## Code Examples

### Example 1: Simple Validation

```python
from vcdecomp.validation import ValidationOrchestrator

def validate_script(original_scr: str, decompiled_c: str):
    """Simple validation with result printing."""
    validator = ValidationOrchestrator()
    result = validator.validate(original_scr, decompiled_c)

    print(f"Verdict: {result.verdict.name}")
    print(f"Compilation: {'✓' if result.compilation_succeeded else '✗'}")
    print(f"Semantic differences: {result.difference_summary.semantic_count}")

    return result.verdict == ValidationVerdict.PASS

# Usage
if validate_script("mission_01.scr", "mission_01.c"):
    print("Validation passed!")
```

### Example 2: Batch Validation with Reports

```python
from pathlib import Path
from vcdecomp.validation import ValidationOrchestrator, ReportGenerator

def batch_validate(input_dir: str, original_dir: str, report_dir: str):
    """Validate all files in directory and save reports."""
    validator = ValidationOrchestrator()
    generator = ReportGenerator()

    input_path = Path(input_dir)
    original_path = Path(original_dir)
    report_path = Path(report_dir)
    report_path.mkdir(exist_ok=True)

    results = {}
    for source_file in input_path.glob("*.c"):
        scr_file = original_path / f"{source_file.stem}.scr"
        if not scr_file.exists():
            print(f"⚠ Skipping {source_file.name}: No matching .scr")
            continue

        print(f"Validating {source_file.name}...")
        result = validator.validate(str(scr_file), str(source_file))
        results[source_file.name] = result

        # Save individual report
        report_file = report_path / f"{source_file.stem}_validation.html"
        generator.save_report(result, str(report_file))

    # Print summary
    passed = sum(1 for r in results.values() if r.verdict == ValidationVerdict.PASS)
    print(f"\nSummary: {passed}/{len(results)} passed")

    return results

# Usage
results = batch_validate("decompiled/", "scripts/", "reports/")
```

### Example 3: Custom Difference Analysis

```python
from vcdecomp.validation import (
    ValidationOrchestrator,
    DifferenceCategory,
    DifferenceSeverity
)

def analyze_differences(original_scr: str, decompiled_c: str):
    """Detailed difference analysis."""
    validator = ValidationOrchestrator()
    result = validator.validate(original_scr, decompiled_c)

    # Get semantic differences
    semantic = result.get_differences_by_category(DifferenceCategory.SEMANTIC)

    # Group by severity
    by_severity = {}
    for diff in semantic:
        severity = diff.difference.severity
        if severity not in by_severity:
            by_severity[severity] = []
        by_severity[severity].append(diff)

    # Print analysis
    print("Semantic Differences by Severity:")
    for severity in [DifferenceSeverity.CRITICAL, DifferenceSeverity.MAJOR]:
        diffs = by_severity.get(severity, [])
        if diffs:
            print(f"\n{severity.name} ({len(diffs)}):")
            for diff in diffs:
                print(f"  - {diff.difference.description}")

    return by_severity

# Usage
analysis = analyze_differences("test.scr", "test.c")
```

### Example 4: Validation with Caching

```python
from vcdecomp.validation import ValidationOrchestrator, ValidationCache

def cached_validation(original_scr: str, decompiled_c: str, force: bool = False):
    """Validation with manual cache control."""
    cache = ValidationCache(cache_dir=".cache", max_age_seconds=3600)

    # Try cache first (unless force)
    if not force:
        cached = cache.get(decompiled_c, original_scr)
        if cached:
            print("Using cached result")
            stats = cache.get_statistics()
            print(f"Cache hit rate: {stats.hit_rate:.1%}")
            return cached

    # Run validation
    print("Running validation...")
    validator = ValidationOrchestrator(cache_enabled=False)  # Manual cache control
    result = validator.validate(original_scr, decompiled_c)

    # Cache result
    cache.set(decompiled_c, original_scr, result)

    return result

# Usage
result = cached_validation("test.scr", "test.c")  # Uses cache if available
result = cached_validation("test.scr", "test.c", force=True)  # Force revalidation
```

### Example 5: Regression Testing Workflow

```python
from vcdecomp.validation import (
    ValidationOrchestrator,
    RegressionBaseline,
    RegressionComparator
)
from pathlib import Path

def create_baseline(input_dir: str, original_dir: str):
    """Create regression baseline."""
    validator = ValidationOrchestrator()
    baseline = RegressionBaseline(description="Test suite baseline")

    input_path = Path(input_dir)
    original_path = Path(original_dir)

    for source_file in input_path.glob("*.c"):
        scr_file = original_path / f"{source_file.stem}.scr"
        if not scr_file.exists():
            continue

        result = validator.validate(str(scr_file), str(source_file))
        baseline.add_entry(
            file=source_file.name,
            verdict=result.verdict,
            compilation_succeeded=result.compilation_succeeded,
            differences_count=len(result.categorized_differences),
            semantic_differences=result.difference_summary.semantic_count
        )

    baseline.save(".validation-baseline.json")
    print(f"Baseline created with {len(baseline.entries)} entries")

def check_regressions(input_dir: str, original_dir: str):
    """Check for regressions against baseline."""
    # Load baseline
    baseline = RegressionBaseline.load(".validation-baseline.json")

    # Run current validations
    validator = ValidationOrchestrator()
    current_results = {}

    input_path = Path(input_dir)
    original_path = Path(original_dir)

    for source_file in input_path.glob("*.c"):
        scr_file = original_path / f"{source_file.stem}.scr"
        if not scr_file.exists():
            continue

        result = validator.validate(str(scr_file), str(source_file))
        current_results[source_file.name] = result

    # Compare
    comparator = RegressionComparator(baseline)
    report = comparator.compare(current_results)

    # Report results
    if report.has_regressions:
        print(f"⚠ {len(report.regressions)} regressions detected!")
        for reg in report.regressions:
            print(f"  {reg.file}: {reg.baseline_verdict.name} → {reg.current_verdict.name}")
        return False
    else:
        print(f"✓ No regressions! ({len(report.improvements)} improvements)")
        return True

# Usage
create_baseline("decompiled/", "scripts/")  # Once
passed = check_regressions("decompiled/", "scripts/")  # After changes
```

---

## Error Handling

### Common Exceptions

```python
from vcdecomp.validation import ValidationOrchestrator

try:
    validator = ValidationOrchestrator(compiler_dir="invalid/path")
    result = validator.validate("test.scr", "test.c")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except TimeoutError as e:
    print(f"Compilation timeout: {e}")
except Exception as e:
    print(f"Validation error: {e}")
```

### Checking Compilation Errors

```python
result = validator.validate("test.scr", "test.c")

if not result.compilation_succeeded:
    print("Compilation failed:")
    for error in result.compilation_result.errors:
        print(f"  {error.file}:{error.line}: {error.message}")
```

---

## Additional Resources

- **User Guide**: See `validation_system.md` for GUI and CLI usage
- **Technical Docs**: See `docs/SCC_TECHNICAL_ANALYSIS.md` for compiler details
- **Source Code**: Browse `vcdecomp/validation/` for implementation details
- **Examples**: See `examples/` directory for more code samples

---

**Document Version**: 1.0
**Last Updated**: 2026-01-09
**Part of**: VC Script Decompiler - Recompilation Validation System
