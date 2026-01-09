#!/bin/bash
# Test runner for bytecode comparison unit tests (Linux/Mac)
#
# Usage: ./run_bytecode_tests.sh

echo "Running bytecode comparison unit tests..."
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

# Run tests with unittest
$PYTHON -m unittest vcdecomp.tests.validation.test_bytecode_compare -v

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "Tests FAILED!"
    exit 1
fi

echo ""
echo "========================================"
echo "All tests passed!"
