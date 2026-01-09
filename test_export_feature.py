#!/usr/bin/env python3
"""
Test script to verify the export validation report feature.

This script verifies:
1. Import of ReportGenerator in validation_view.py
2. Export button is present and properly configured
3. Export handler logic is implemented correctly
"""

import sys
from pathlib import Path

def test_import_validation_view():
    """Test that validation_view.py can be imported"""
    print("Test 1: Importing validation_view module...")
    try:
        from vcdecomp.gui.views.validation_view import ValidationPanel, ValidationStatus
        print("✓ Successfully imported ValidationPanel and ValidationStatus")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False

def test_report_generator_import():
    """Test that ReportGenerator is available"""
    print("\nTest 2: Checking ReportGenerator import...")
    try:
        from vcdecomp.validation import ReportGenerator
        print("✓ ReportGenerator is available from validation module")
        return True
    except ImportError as e:
        print(f"✗ Failed to import ReportGenerator: {e}")
        return False

def test_validation_panel_has_export_button():
    """Test that ValidationPanel has export button"""
    print("\nTest 3: Checking ValidationPanel for export button...")
    try:
        from vcdecomp.gui.views.validation_view import ValidationPanel

        # Check if the class has the export handler method
        if hasattr(ValidationPanel, 'on_export_clicked'):
            print("✓ ValidationPanel has on_export_clicked method")
        else:
            print("✗ ValidationPanel missing on_export_clicked method")
            return False

        return True
    except Exception as e:
        print(f"✗ Error checking ValidationPanel: {e}")
        return False

def test_export_handler_logic():
    """Test the export handler logic without GUI"""
    print("\nTest 4: Verifying export handler logic...")
    try:
        from vcdecomp.gui.views.validation_view import ValidationPanel
        import inspect

        # Get the source code of on_export_clicked
        source = inspect.getsource(ValidationPanel.on_export_clicked)

        # Check for key components
        checks = [
            ("validation_result check", "if not self.validation_result" in source),
            ("QFileDialog usage", "QFileDialog.getSaveFileName" in source),
            ("Format detection", "format_type" in source),
            ("ReportGenerator usage", "ReportGenerator" in source),
            ("Success notification", "Export Successful" in source),
            ("Error handling", "except Exception" in source),
        ]

        all_passed = True
        for check_name, check_result in checks:
            if check_result:
                print(f"  ✓ {check_name}")
            else:
                print(f"  ✗ {check_name}")
                all_passed = False

        return all_passed
    except Exception as e:
        print(f"✗ Error verifying export handler: {e}")
        return False

def test_button_state_management():
    """Test that export button state is managed correctly"""
    print("\nTest 5: Checking export button state management...")
    try:
        from vcdecomp.gui.views.validation_view import ValidationPanel
        import inspect

        # Check on_validation_finished method
        source = inspect.getsource(ValidationPanel.on_validation_finished)

        checks = [
            ("Enable on success", "self.export_btn.setEnabled(True)" in source),
            ("Disable on error", "self.export_btn.setEnabled(False)" in source),
        ]

        # Check start_validation method
        start_source = inspect.getsource(ValidationPanel.start_validation)
        checks.append(("Disable on start", "self.export_btn.setEnabled(False)" in start_source))

        all_passed = True
        for check_name, check_result in checks:
            if check_result:
                print(f"  ✓ {check_name}")
            else:
                print(f"  ✗ {check_name}")
                all_passed = False

        return all_passed
    except Exception as e:
        print(f"✗ Error checking button state management: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 80)
    print("EXPORT VALIDATION REPORT FEATURE - VERIFICATION TESTS")
    print("=" * 80)
    print()

    tests = [
        test_import_validation_view,
        test_report_generator_import,
        test_validation_panel_has_export_button,
        test_export_handler_logic,
        test_button_state_management,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("\n✓ All tests passed! Export feature is ready.")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
