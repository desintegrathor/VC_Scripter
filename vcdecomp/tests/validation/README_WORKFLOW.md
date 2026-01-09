# Integration Tests for Validation Workflow

## Overview

This test suite provides comprehensive integration tests for the complete validation workflow, testing the orchestration of compilation, comparison, and reporting steps.

## Test Coverage

### TestValidationWorkflowBasic
Tests the core validation orchestration:
- **test_validation_orchestrator_initialization**: Validates initialization with valid compiler directory
- **test_validation_orchestrator_invalid_compiler_dir**: Tests error handling for invalid compiler paths
- **test_full_validation_workflow_with_mocked_compilation**: End-to-end test with mocked compilation
- **test_validation_with_missing_original_scr**: Error recovery for missing original SCR
- **test_validation_with_missing_source_file**: Error recovery for missing source file
- **test_validation_with_compilation_error_mocked**: Handling of compilation errors

### TestReportGeneration
Tests all report generation formats:
- **test_generate_text_report**: Text format with ANSI colors
- **test_generate_html_report**: HTML format with expandable sections
- **test_generate_json_report**: JSON format for programmatic use
- **test_save_report_text**: Saving text reports to file
- **test_save_report_html**: Saving HTML reports to file
- **test_save_report_json**: Saving JSON reports to file
- **test_save_report_auto_detect_format**: Auto-detection from file extension

### TestValidationCache
Tests caching functionality:
- **test_cache_stores_and_retrieves_results**: Basic cache operations
- **test_cache_invalidates_on_source_change**: Cache invalidation on file changes
- **test_cache_disabled**: Cache disable functionality

### TestErrorRecovery
Tests error handling and recovery:
- **test_graceful_handling_of_comparison_exception**: Exception handling in comparison
- **test_validation_result_has_recommendations**: Recommendation generation on errors

## Running Tests

### Run all workflow integration tests:
```bash
python -m unittest vcdecomp.tests.validation.test_validation_workflow -v
```

### Run specific test class:
```bash
python -m unittest vcdecomp.tests.validation.test_validation_workflow.TestReportGeneration -v
```

### Run specific test:
```bash
python -m unittest vcdecomp.tests.validation.test_validation_workflow.TestReportGeneration.test_generate_html_report -v
```

### Windows batch script:
```bash
run_workflow_tests.bat
```

### Linux/Mac shell script:
```bash
./run_workflow_tests.sh
```

## Test Design

### Integration Testing Approach
These tests validate the **entire validation workflow** from end to end:

1. **Orchestration**: ValidationOrchestrator coordinates all steps
2. **Compilation**: Uses compiler wrappers (mocked for predictability)
3. **Comparison**: Uses BytecodeComparator with real SCR files
4. **Reporting**: Generates text/HTML/JSON reports
5. **Caching**: Tests validation result caching

### Mocking Strategy
- **Compilation step** is mocked to avoid dependency on 32-bit compiler executables
- **Comparison step** uses real bytecode comparison logic
- **Real test fixtures** from Compiler-testruns/ when available
- **Mock data** for predictable test scenarios

### Test Data
Tests use:
- Real SCR files from `Compiler-testruns/` when available
- Mock SCRFile objects for controlled scenarios
- Temporary files for output validation

## Dependencies

Required modules:
- `vcdecomp.validation.validator` - ValidationOrchestrator
- `vcdecomp.validation.validation_types` - ValidationResult, ValidationVerdict
- `vcdecomp.validation.report_generator` - ReportGenerator
- `vcdecomp.validation.cache` - ValidationCache
- `vcdecomp.validation.compilation_types` - CompilationResult, CompilationError
- `vcdecomp.validation.bytecode_compare` - BytecodeComparator

## Expected Results

All tests should **PASS** with the following characteristics:

✅ **TestValidationWorkflowBasic**: 6 tests
- Tests core orchestration logic
- Validates error handling for missing files
- Tests compilation error scenarios

✅ **TestReportGeneration**: 7 tests
- All report formats generate correctly
- File saving works for all formats
- Auto-detection from extension works

✅ **TestValidationCache**: 3 tests
- Cache stores and retrieves correctly
- Cache invalidates on file changes
- Cache can be disabled

✅ **TestErrorRecovery**: 2 tests
- Exceptions are handled gracefully
- Recommendations are provided

**Total: 18 tests**

## Notes

### Test Fixtures
- Tests look for SCR/C file pairs in `Compiler-testruns/`
- Tests are skipped if fixtures are not found (graceful degradation)
- Mock data is used when real files are unavailable

### Compiler Tools
- Some tests skip if compiler tools are not available
- Mocking allows tests to run without functional compiler
- Real compiler integration is tested separately

### Temporary Files
- All tests use temporary directories
- Cleanup is automatic via tearDown()
- Cache and output files are isolated per test

### Performance
- Integration tests are slower than unit tests
- Mocking keeps tests reasonably fast
- Full end-to-end tests may take several seconds

## Troubleshooting

### Tests Skip Due to Missing Fixtures
**Cause**: No test data in Compiler-testruns/
**Solution**: Ensure Compiler-testruns/ exists with .scr and .c files

### Tests Skip Due to Missing Compiler
**Cause**: SCMP.exe not found in original-resources/compiler/
**Solution**: Tests will run with mocked compilation (expected behavior)

### Cache Tests Fail
**Cause**: File permission issues or invalid temp directory
**Solution**: Check write permissions on temp directory

### Report Tests Fail
**Cause**: Encoding issues on Windows
**Solution**: Reports use UTF-8 encoding; check locale settings

## Integration with CI/CD

These tests are suitable for CI/CD pipelines:
- Fast execution with mocked compilation
- No external dependencies required
- Graceful skipping when fixtures unavailable
- Clear PASS/FAIL reporting

Recommended CI configuration:
```yaml
test:
  script:
    - python -m unittest vcdecomp.tests.validation.test_validation_workflow -v
```

## Related Documentation

- Main validation system: `docs/validation_system.md`
- Compiler wrapper tests: `vcdecomp/tests/validation/test_compiler_wrapper.py`
- Bytecode comparison tests: `vcdecomp/tests/validation/test_bytecode_compare.py`
- Complete test summary: `vcdecomp/tests/validation/TEST_SUMMARY.md`
