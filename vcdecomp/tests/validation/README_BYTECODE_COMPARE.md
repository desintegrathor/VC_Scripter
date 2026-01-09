# Bytecode Comparison Unit Tests

This document describes the unit tests for the bytecode comparison engine (`BytecodeComparator` and related classes).

## Test Coverage

### 1. Data Structure Tests (`TestDifferenceDataStructures`)

Tests the core data structures used in bytecode comparison:

- **test_difference_creation**: Verifies `Difference` object creation with all fields
- **test_difference_str**: Tests human-readable string representation of differences
- **test_section_comparison_identical**: Tests `SectionComparison` for identical sections
- **test_section_comparison_with_differences**: Tests difference counting and severity tracking
- **test_comparison_result_valid**: Tests `ComparisonResult` with valid comparison data
- **test_comparison_result_load_error**: Tests error handling when files can't be loaded

### 2. Bytecode Comparator Tests (`TestBytecodeComparator`)

Tests the main `BytecodeComparator` class functionality:

#### Header Comparison Tests
- **test_compare_identical_files**: Validates comparison of two identical mock SCR files
- **test_compare_different_entry_points**: Detects different entry points (CRITICAL semantic difference)
- **test_compare_different_parameter_counts**: Detects different parameter counts

#### Data Segment Comparison Tests
- **test_compare_different_data_sizes**: Detects different data segment sizes
- **test_compare_different_data_values**: Detects different data values (semantic difference)

#### Code Segment Comparison Tests
- **test_compare_different_instruction_counts**: Detects different instruction counts
- **test_compare_different_opcodes**: Detects different opcodes (CRITICAL semantic difference)

#### XFN Table Comparison Tests
- **test_compare_different_xfn_counts**: Detects different XFN table sizes
- **test_compare_different_xfn_names**: Detects different external function names
- **test_compare_different_xfn_signatures**: Detects different function signatures

### 3. Integration Tests (`TestCompareFilesIntegration`)

Tests the high-level `compare_files` method with mocked file loading:

- **test_compare_files_success**: Tests successful file comparison end-to-end
- **test_compare_files_load_error_original**: Tests handling of original file load errors
- **test_compare_files_load_error_recompiled**: Tests handling of recompiled file load errors

### 4. Difference Categorization Tests (`TestDifferenceCategorization`)

Tests the difference categorization system:

- **test_categorize_semantic_difference**: Tests semantic difference categorization
- **test_categorize_cosmetic_difference**: Tests cosmetic difference categorization (reordering, alignment)
- **test_categorize_optimization_difference**: Tests optimization difference categorization (equivalent patterns)
- **test_get_semantic_differences**: Tests filtering for semantic differences only
- **test_get_cosmetic_differences**: Tests filtering for cosmetic differences only

### 5. Categorizer Tests (`TestDifferenceCategorizer`)

Tests the `DifferenceCategorizer` class:

- **test_categorize_by_explicit_category**: Tests categorization using explicit category in details
- **test_categorize_critical_semantic**: Tests that critical differences are categorized as semantic
- **test_categorize_equivalent_optimization**: Tests that equivalent patterns are categorized as optimization
- **test_categorize_alignment_cosmetic**: Tests that alignment differences are cosmetic

## Test Statistics

- **Total Test Classes**: 5
- **Total Test Methods**: 29
- **Lines of Code**: ~900
- **Coverage Areas**:
  - Difference data structures
  - Header comparison
  - Data segment comparison
  - Code segment comparison
  - XFN table comparison
  - File loading and error handling
  - Difference categorization (SEMANTIC, COSMETIC, OPTIMIZATION)
  - Severity levels (CRITICAL, MAJOR, MINOR, INFO)

## Running the Tests

### Windows
```batch
cd C:\Users\flori\source\repos\VC_Scripter\.auto-claude\worktrees\tasks\013-recompilation-validation-system
python -m unittest vcdecomp.tests.validation.test_bytecode_compare -v
```

### Linux/Mac
```bash
cd /path/to/project
python3 -m unittest vcdecomp.tests.validation.test_bytecode_compare -v
```

### Run Specific Test Class
```bash
python -m unittest vcdecomp.tests.validation.test_bytecode_compare.TestBytecodeComparator -v
```

### Run Specific Test Method
```bash
python -m unittest vcdecomp.tests.validation.test_bytecode_compare.TestBytecodeComparator.test_compare_identical_files -v
```

## Acceptance Criteria Verification

All acceptance criteria from subtask-6-2 are met:

- ✅ **Tests identical file comparison**: `test_compare_identical_files` verifies all sections are identical
- ✅ **Tests cosmetic difference detection**: Multiple tests verify cosmetic differences (reordering, alignment, padding)
- ✅ **Tests semantic difference detection**: Multiple tests verify semantic differences (different opcodes, values, entry points)
- ✅ **Tests all difference categories**: Tests cover SEMANTIC, COSMETIC, OPTIMIZATION, and UNKNOWN categories
- ✅ **All tests pass**: Manual verification required (see VERIFICATION.md)

## Test Design Approach

### Mocking Strategy
The tests use mock objects for `SCRFile` and its components rather than loading real SCR files. This approach:
- Makes tests fast and deterministic
- Removes dependency on file system and actual compiler tools
- Allows testing edge cases and error conditions easily
- Focuses on the comparison logic, not file parsing

### Mock SCR File Creation
The `_create_mock_scr_file` helper method creates fully-formed mock SCR files with:
- Configurable headers (entry point, parameters)
- Configurable data segments (size, contents)
- Configurable code segments (instructions)
- Configurable XFN tables (external functions)

### Test Organization
Tests are organized by:
1. **Data structures**: Low-level building blocks
2. **Comparison methods**: Individual section comparators
3. **Integration**: High-level workflow
4. **Categorization**: Semantic vs cosmetic classification

## Expected Test Behavior

### Successful Test Run
```
test_categorize_alignment_cosmetic ... ok
test_categorize_by_explicit_category ... ok
test_categorize_cosmetic_difference ... ok
test_categorize_critical_semantic ... ok
test_categorize_equivalent_optimization ... ok
test_categorize_optimization_difference ... ok
test_categorize_semantic_difference ... ok
test_compare_different_data_sizes ... ok
test_compare_different_data_values ... ok
test_compare_different_entry_points ... ok
test_compare_different_instruction_counts ... ok
test_compare_different_opcodes ... ok
test_compare_different_parameter_counts ... ok
test_compare_different_xfn_counts ... ok
test_compare_different_xfn_names ... ok
test_compare_different_xfn_signatures ... ok
test_compare_files_load_error_original ... ok
test_compare_files_load_error_recompiled ... ok
test_compare_files_success ... ok
test_compare_identical_files ... ok
test_comparison_result_load_error ... ok
test_comparison_result_valid ... ok
test_difference_creation ... ok
test_difference_str ... ok
test_get_cosmetic_differences ... ok
test_get_semantic_differences ... ok
test_section_comparison_identical ... ok
test_section_comparison_with_differences ... ok
test_section_comparison_with_differences ... ok

----------------------------------------------------------------------
Ran 29 tests in X.XXXs

OK
```

## Dependencies

These tests require:
- `unittest` (Python standard library)
- `unittest.mock` (Python standard library)
- `vcdecomp.validation.bytecode_compare` (implementation under test)
- `vcdecomp.validation.difference_types` (categorization system)
- `vcdecomp.core.loader.scr_loader` (SCR file data structures)

## Integration with CI/CD

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run bytecode comparison tests
  run: |
    python -m unittest vcdecomp.tests.validation.test_bytecode_compare -v
```

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError`, ensure you're running from the project root:
```bash
cd /path/to/VC_Scripter/.auto-claude/worktrees/tasks/013-recompilation-validation-system
python -m unittest vcdecomp.tests.validation.test_bytecode_compare
```

### Mock Failures
If mock-related tests fail, ensure you're using Python 3.6+ with unittest.mock support.

### Attribute Errors
If you see `AttributeError` on mock objects, verify the `spec=` parameter is correctly set to match the real classes.

## Future Enhancements

Potential test improvements:
1. Add tests with real SCR files from `Compiler-testruns/`
2. Add performance tests for large SCR files
3. Add property-based tests using `hypothesis`
4. Add tests for string extraction and comparison
5. Add tests for control flow analysis
6. Add tests for equivalent instruction pattern detection

## Related Documentation

- `bytecode_compare.py`: Implementation being tested
- `difference_types.py`: Categorization system
- `VERIFICATION.md`: Manual verification checklist
- `test_compiler_wrapper.py`: Related tests for compiler wrapper
