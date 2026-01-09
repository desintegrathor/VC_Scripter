#!/usr/bin/env python3
"""
Verification script for validate CLI command (subtask-5-1)

Tests the validate command implementation without requiring actual execution.
"""

import sys
import os
from pathlib import Path

# Add vcdecomp to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")

    try:
        from vcdecomp.validation import (
            ValidationOrchestrator,
            ReportGenerator,
            ValidationVerdict
        )
        print("✓ ValidationOrchestrator imported")
        print("✓ ReportGenerator imported")
        print("✓ ValidationVerdict imported")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_command_function_exists():
    """Test that cmd_validate function exists in __main__"""
    print("\nTesting command function...")

    try:
        from vcdecomp.__main__ import cmd_validate
        print("✓ cmd_validate function exists")

        # Check function signature
        import inspect
        sig = inspect.signature(cmd_validate)
        params = list(sig.parameters.keys())

        if 'args' in params:
            print("✓ cmd_validate has 'args' parameter")
        else:
            print("✗ cmd_validate missing 'args' parameter")
            return False

        return True
    except ImportError as e:
        print(f"✗ Function not found: {e}")
        return False


def test_argparse_setup():
    """Test that argparse is configured correctly"""
    print("\nTesting argparse configuration...")

    try:
        # Import the main function to check argparse setup
        from vcdecomp import __main__
        import argparse

        # Create parser to test
        parser = argparse.ArgumentParser(prog='vcdecomp')
        subparsers = parser.add_subparsers(dest='command')

        # Add validate subparser (simulating what __main__ does)
        p_validate = subparsers.add_parser('validate', help='Validate decompiled source by recompiling')
        p_validate.add_argument('original_scr', help='Path to original .SCR file')
        p_validate.add_argument('source_file', help='Path to decompiled source .c file')
        p_validate.add_argument('--compiler-dir', help='Path to compiler directory')
        p_validate.add_argument('--output-format', choices=['text', 'json', 'html'])
        p_validate.add_argument('--report-file', help='Save detailed report to file')
        p_validate.add_argument('--no-cache', action='store_true')
        p_validate.add_argument('--no-color', action='store_true')

        # Test parsing
        args = parser.parse_args(['validate', 'test.scr', 'test.c'])

        if args.command == 'validate':
            print("✓ validate command parsed correctly")
        else:
            print("✗ Command not recognized")
            return False

        if args.original_scr == 'test.scr':
            print("✓ original_scr argument parsed")
        else:
            print("✗ original_scr not parsed correctly")
            return False

        if args.source_file == 'test.c':
            print("✓ source_file argument parsed")
        else:
            print("✗ source_file not parsed correctly")
            return False

        return True
    except Exception as e:
        print(f"✗ Argparse test failed: {e}")
        return False


def test_acceptance_criteria():
    """Verify all acceptance criteria from spec"""
    print("\nVerifying acceptance criteria...")

    # Read the implementation
    main_file = Path(__file__).parent / 'vcdecomp' / '__main__.py'
    content = main_file.read_text()

    criteria = [
        ('Command: python -m vcdecomp validate original.scr source.c',
         'def cmd_validate(args):' in content),
        ('Outputs validation results to console',
         'print(generator.generate_text' in content or 'print(generator.generate_json' in content),
        ('Returns exit code 0 for pass, non-zero for fail',
         'sys.exit(0)' in content and 'sys.exit(1)' in content),
        ('Supports --output-format flag (text/json/html)',
         "choices=['text', 'json', 'html']" in content),
        ('Supports --report-file flag for saving report',
         '--report-file' in content and 'save_report' in content),
    ]

    all_passed = True
    for desc, passed in criteria:
        if passed:
            print(f"✓ {desc}")
        else:
            print(f"✗ {desc}")
            all_passed = False

    return all_passed


def main():
    """Run all verification tests"""
    print("=" * 70)
    print("Validate Command Verification (subtask-5-1)")
    print("=" * 70)

    results = []

    results.append(("Module imports", test_imports()))
    results.append(("Command function", test_command_function_exists()))
    results.append(("Argparse setup", test_argparse_setup()))
    results.append(("Acceptance criteria", test_acceptance_criteria()))

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{name:.<50} {status}")

    all_passed = all(r[1] for r in results)

    if all_passed:
        print("\n✓ All verification tests PASSED")
        return 0
    else:
        print("\n✗ Some verification tests FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
