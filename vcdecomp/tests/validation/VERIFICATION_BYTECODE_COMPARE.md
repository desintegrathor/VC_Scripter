# Bytecode Comparison Unit Tests - Verification Checklist

This document provides a manual verification checklist for the bytecode comparison unit tests.

## Pre-Verification Setup

1. **Environment Check**
   - [ ] Python 3.6+ is installed
   - [ ] Project is set up correctly
   - [ ] Working directory is project root

2. **File Verification**
   - [ ] `vcdecomp/tests/validation/test_bytecode_compare.py` exists
   - [ ] `vcdecomp/validation/bytecode_compare.py` exists
   - [ ] `vcdecomp/validation/difference_types.py` exists
   - [ ] `vcdecomp/core/loader/scr_loader.py` exists

## Test Execution

### Run All Tests
```bash
python -m unittest vcdecomp.tests.validation.test_bytecode_compare -v
```

**Expected Result**: All 29 tests pass with "OK" status

- [ ] All tests pass
- [ ] No errors or failures
- [ ] No warnings or deprecation notices

### Run Individual Test Classes

#### 1. Data Structure Tests
```bash
python -m unittest vcdecomp.tests.validation.test_bytecode_compare.TestDifferenceDataStructures -v
```
- [ ] 6 tests pass
- [ ] Difference creation works
- [ ] String representation correct
- [ ] Section comparison tracking works
- [ ] ComparisonResult aggregation works

#### 2. Bytecode Comparator Tests
```bash
python -m unittest vcdecomp.tests.validation.test_bytecode_compare.TestBytecodeComparator -v
```
- [ ] 14 tests pass
- [ ] Identical files detected correctly
- [ ] Header differences detected (entry point, parameters)
- [ ] Data differences detected (size, values)
- [ ] Code differences detected (instruction count, opcodes)
- [ ] XFN differences detected (count, names, signatures)

#### 3. Integration Tests
```bash
python -m unittest vcdecomp.tests.validation.test_bytecode_compare.TestCompareFilesIntegration -v
```
- [ ] 3 tests pass
- [ ] Successful comparison works end-to-end
- [ ] Load errors handled gracefully
- [ ] Both file load errors detected

#### 4. Categorization Tests
```bash
python -m unittest vcdecomp.tests.validation.test_bytecode_compare.TestDifferenceCategorization -v
```
- [ ] 5 tests pass
- [ ] Semantic differences categorized correctly
- [ ] Cosmetic differences categorized correctly
- [ ] Optimization differences categorized correctly
- [ ] Filtering functions work

#### 5. Categorizer Tests
```bash
python -m unittest vcdecomp.tests.validation.test_bytecode_compare.TestDifferenceCategorizer -v
```
- [ ] 4 tests pass
- [ ] Explicit category detection works
- [ ] Critical differences marked semantic
- [ ] Equivalent patterns marked optimization
- [ ] Alignment differences marked cosmetic

## Acceptance Criteria Verification

From `implementation_plan.json` subtask-6-2:

### ✅ Tests identical file comparison
- [ ] `test_compare_identical_files` passes
- [ ] All sections report as identical
- [ ] No differences found
- [ ] Result.identical is True

### ✅ Tests cosmetic difference detection
- [ ] Reordering differences detected
- [ ] Alignment differences detected
- [ ] Padding differences detected
- [ ] All marked with MINOR or INFO severity
- [ ] Categorized as COSMETIC

### ✅ Tests semantic difference detection
- [ ] Entry point differences detected (CRITICAL)
- [ ] Different opcodes detected (CRITICAL)
- [ ] Different data values detected (MAJOR)
- [ ] Missing XFN functions detected (CRITICAL)
- [ ] All categorized as SEMANTIC

### ✅ Tests all difference categories
- [ ] SEMANTIC category tested and working
- [ ] COSMETIC category tested and working
- [ ] OPTIMIZATION category tested and working
- [ ] UNKNOWN category handled

### ✅ All tests pass
- [ ] 29/29 tests pass
- [ ] No failures
- [ ] No errors
- [ ] No skipped tests

## Code Quality Checks

### Import Verification
```bash
python -c "from vcdecomp.tests.validation.test_bytecode_compare import *; print('Imports OK')"
```
- [ ] No import errors
- [ ] All dependencies available

### Syntax Check
```bash
python -m py_compile vcdecomp/tests/validation/test_bytecode_compare.py
```
- [ ] No syntax errors
- [ ] File compiles successfully

### Coverage Check (Optional)
```bash
python -m coverage run -m unittest vcdecomp.tests.validation.test_bytecode_compare
python -m coverage report -m
```
- [ ] Coverage report generated
- [ ] Key methods covered

## Test Output Analysis

### Expected Output Format
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

----------------------------------------------------------------------
Ran 29 tests in 0.XXXs

OK
```

### Verify Each Test Output
- [ ] All tests show "ok"
- [ ] No "FAIL" or "ERROR" markers
- [ ] Total test count is 29
- [ ] Final status is "OK"

## Functional Verification

### Test Mock Objects Work Correctly
- [ ] Mock SCR files can be created
- [ ] Mock headers have all required fields
- [ ] Mock data segments work correctly
- [ ] Mock code segments work correctly
- [ ] Mock XFN tables work correctly

### Test Comparison Logic
- [ ] Identical files return no differences
- [ ] Different entry points detected
- [ ] Different opcodes detected
- [ ] Different data detected
- [ ] Different XFN entries detected

### Test Categorization Logic
- [ ] Critical differences → SEMANTIC
- [ ] Minor differences → COSMETIC (if reordering/alignment)
- [ ] Equivalent patterns → OPTIMIZATION
- [ ] Explicit categories honored

### Test Error Handling
- [ ] File load errors caught and reported
- [ ] Invalid data handled gracefully
- [ ] Missing fields handled

## Integration Verification

### Test with Real Loader Components
- [ ] Tests use correct SCRFile imports
- [ ] Tests use correct data structure types
- [ ] Tests match actual API signatures

### Test with Categorization System
- [ ] Tests use DifferenceCategory enum
- [ ] Tests use DifferenceCategorizer class
- [ ] Tests match categorization rules

## Performance Check

### Test Execution Speed
- [ ] All tests complete in < 5 seconds
- [ ] No individual test takes > 1 second
- [ ] Mock objects don't cause slowdown

### Memory Usage
- [ ] No memory leaks from mock objects
- [ ] Tests can run repeatedly without issues

## Documentation Verification

- [ ] README_BYTECODE_COMPARE.md exists and is accurate
- [ ] This VERIFICATION.md is complete
- [ ] Code comments are clear
- [ ] Docstrings are present

## Sign-Off

**Test Results Summary:**
- Total Tests: 29
- Passed: ___
- Failed: ___
- Errors: ___
- Skipped: ___

**Acceptance Criteria Met:**
- [ ] Tests identical file comparison: YES / NO
- [ ] Tests cosmetic difference detection: YES / NO
- [ ] Tests semantic difference detection: YES / NO
- [ ] Tests all difference categories: YES / NO
- [ ] All tests pass: YES / NO

**Overall Status:** ✅ PASS / ❌ FAIL

**Verified By:** _________________

**Date:** _________________

**Notes:**
```
[Any issues, warnings, or observations]
```

## Troubleshooting

### Common Issues

**Issue**: ImportError for vcdecomp modules
**Solution**: Run from project root directory

**Issue**: Mock attribute errors
**Solution**: Verify mock spec= parameters match real classes

**Issue**: Tests fail on comparison
**Solution**: Check that mock objects have all required fields

**Issue**: Categorization tests fail
**Solution**: Verify difference_types.py implementation is correct

### Getting Help

If tests fail or you encounter issues:
1. Check the error message carefully
2. Verify file paths and imports
3. Check that all dependencies are installed
4. Review the implementation code
5. Consult the documentation

## Next Steps

After verification is complete:
1. Update implementation_plan.json status to "completed"
2. Commit changes with appropriate message
3. Proceed to next subtask (subtask-6-3)
