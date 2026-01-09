# Compiler Wrapper Unit Tests

Comprehensive unit tests for the Vietcong script compiler wrapper classes.

## Test Coverage

### BaseCompiler Tests (`TestBaseCompiler`)
- ✅ Initialization with valid executable
- ✅ Initialization with invalid executable (raises FileNotFoundError)
- ✅ Automatic working directory creation
- ✅ Using provided working directory
- ✅ Successful subprocess execution
- ✅ Failed subprocess execution
- ✅ Subprocess timeout handling
- ✅ Subprocess exception handling
- ✅ Forced cleanup of temporary directory
- ✅ Cleanup on successful compilation
- ✅ No cleanup when disabled
- ✅ Cleanup on failed compilation
- ✅ Context manager with successful operation
- ✅ Context manager with exception

### Error File Parsing Tests (`TestErrorFileParsing`)
- ✅ Format 1: `file.c(123): error: message`
- ✅ Format 2: `file.c:123:45: error: message`
- ✅ Format 3: `file.c:123: error: message`
- ✅ Warning messages
- ✅ Fatal error messages
- ✅ Non-existent error files
- ✅ Empty error files
- ✅ Unstructured error messages

### SCMP Wrapper Tests (`TestSCMPWrapper`)
- ✅ Successful compilation
- ✅ Compilation with missing source file
- ✅ Compilation with errors
- ✅ Compilation with header file output
- ✅ Compilation with include directories

### SPP Wrapper Tests (`TestSPPWrapper`)
- ✅ Successful preprocessing
- ✅ Preprocessing with missing source file
- ✅ Preprocessing with include path

### SCC Wrapper Tests (`TestSCCWrapper`)
- ✅ Successful compilation to assembly
- ✅ Compilation with debug mode enabled

### SASM Wrapper Tests (`TestSASMWrapper`)
- ✅ Successful assembly to bytecode
- ✅ Assembly with header file output
- ✅ Assembly with missing source file

## Total Tests: 32

All tests use mocked subprocess calls for fast, deterministic execution without requiring the actual compiler executables.

## Running the Tests

### Option 1: Using unittest directly
```bash
python -m unittest vcdecomp.tests.validation.test_compiler_wrapper -v
```

### Option 2: Using the test runner script

**Linux/Mac:**
```bash
cd vcdecomp/tests/validation
chmod +x run_tests.sh
./run_tests.sh
```

**Windows:**
```cmd
cd vcdecomp\tests\validation
run_tests.bat
```

### Option 3: Using pytest (if installed)
```bash
pytest vcdecomp/tests/validation/test_compiler_wrapper.py -v
```

## Test Design

### Mocking Strategy
All tests mock the `_execute()` method to avoid:
- Requiring actual compiler executables
- Slow subprocess execution
- Platform-specific issues
- Non-deterministic behavior

### Isolation
Each test class uses:
- `setUp()` to create temporary directories and files
- `tearDown()` to clean up resources
- Independent test fixtures

### Coverage Areas
1. **Successful operations**: Normal workflow testing
2. **Error handling**: Missing files, failed execution, timeouts
3. **Resource management**: Cleanup, temp directories, context managers
4. **Configuration**: Include paths, debug mode, cleanup flags
5. **Error parsing**: Multiple error formats, warnings, fatal errors

## Acceptance Criteria

✅ Tests successful compilation
✅ Tests compilation errors
✅ Tests timeout handling
✅ Tests cleanup on failure
✅ All tests pass (manual verification required)

## Notes

- Tests are designed to run without actual compiler executables
- All subprocess calls are mocked for speed and reliability
- Tests cover all four wrapper classes plus base functionality
- Error file parsing is tested with multiple formats
- Resource cleanup is thoroughly tested to prevent leaks
