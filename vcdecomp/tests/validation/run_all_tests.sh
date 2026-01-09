#!/bin/bash
# Test runner for all validation unit tests (Linux/Mac)
#
# Usage: ./run_all_tests.sh

echo "Running all validation unit tests..."
echo "========================================"
echo ""

# Try to find Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Error: Python not found in PATH"
    exit 1
fi

echo "Using Python: $PYTHON"
$PYTHON --version
echo ""

TEST_FAILED=0

# Run compiler wrapper tests
echo ""
echo "========================================"
echo "1. Compiler Wrapper Tests"
echo "========================================"
$PYTHON -m unittest vcdecomp.tests.validation.test_compiler_wrapper -v

if [ $? -ne 0 ]; then
    echo ""
    echo "Compiler wrapper tests FAILED!"
    TEST_FAILED=1
fi

# Run bytecode comparison tests
echo ""
echo "========================================"
echo "2. Bytecode Comparison Tests"
echo "========================================"
$PYTHON -m unittest vcdecomp.tests.validation.test_bytecode_compare -v

if [ $? -ne 0 ]; then
    echo ""
    echo "Bytecode comparison tests FAILED!"
    TEST_FAILED=1
fi

# Summary
echo ""
echo "========================================"
echo "Test Summary"
echo "========================================"

if [ $TEST_FAILED -ne 0 ]; then
    echo ""
    echo "Some tests FAILED!"
    echo "Please review the output above for details."
    exit 1
else
    echo ""
    echo "All tests PASSED!"
    echo "- Compiler wrapper tests: PASS"
    echo "- Bytecode comparison tests: PASS"
    exit 0
fi
