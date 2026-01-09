#!/bin/bash
# Run integration tests for validation workflow

echo "Running integration tests for validation workflow..."
echo ""

python -m unittest vcdecomp.tests.validation.test_validation_workflow -v

echo ""
echo "Tests complete!"
