#!/bin/bash
# Test runner for compiler wrapper unit tests
#
# Usage: ./run_tests.sh

set -e

echo "Running compiler wrapper unit tests..."
echo "========================================"
echo

# Find Python executable
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Error: Python not found in PATH"
    exit 1
fi

echo "Using Python: $PYTHON ($($PYTHON --version))"
echo

# Run tests with unittest
$PYTHON -m unittest vcdecomp.tests.validation.test_compiler_wrapper -v

echo
echo "========================================"
echo "All tests passed!"
