"""
Verification script for validation settings dialog.

Tests:
1. Dialog can be imported
2. Dialog can be instantiated
3. Settings can be saved and loaded
4. Settings validation works
5. All acceptance criteria are met
"""

import sys
from pathlib import Path

# Verify imports
try:
    from vcdecomp.gui.dialogs import ValidationSettingsDialog
    print("✓ ValidationSettingsDialog imported successfully")
except ImportError as e:
    print(f"✗ Failed to import ValidationSettingsDialog: {e}")
    sys.exit(1)

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QSettings
    print("✓ PyQt6 imports successful")
except ImportError as e:
    print(f"✗ PyQt6 not available: {e}")
    sys.exit(1)


def test_dialog_instantiation():
    """Test 1: Dialog can be instantiated"""
    print("\n=== Test 1: Dialog Instantiation ===")
    app = QApplication.instance() or QApplication(sys.argv)

    try:
        dialog = ValidationSettingsDialog()
        print("✓ Dialog instantiated successfully")

        # Check that all UI elements exist
        assert hasattr(dialog, 'compiler_dir_edit'), "Missing compiler_dir_edit"
        assert hasattr(dialog, 'timeout_spin'), "Missing timeout_spin"
        assert hasattr(dialog, 'include_dirs_list'), "Missing include_dirs_list"
        assert hasattr(dialog, 'opcode_variant_combo'), "Missing opcode_variant_combo"
        assert hasattr(dialog, 'cache_enabled_check'), "Missing cache_enabled_check"
        assert hasattr(dialog, 'cache_dir_edit'), "Missing cache_dir_edit"
        assert hasattr(dialog, 'cache_max_age_spin'), "Missing cache_max_age_spin"
        print("✓ All UI elements present")

        return True
    except Exception as e:
        print(f"✗ Dialog instantiation failed: {e}")
        return False


def test_settings_persistence():
    """Test 2: Settings can be saved and loaded"""
    print("\n=== Test 2: Settings Persistence ===")
    app = QApplication.instance() or QApplication(sys.argv)

    try:
        # Clear existing settings
        settings = QSettings("VCDecompiler", "ValidationSettings")
        settings.clear()
        print("✓ Cleared existing settings")

        # Create dialog and set some values
        dialog = ValidationSettingsDialog()
        dialog.compiler_dir_edit.setText("./test/compiler")
        dialog.timeout_spin.setValue(45)
        dialog.opcode_variant_combo.setCurrentText("v1.60")
        dialog.cache_enabled_check.setChecked(False)
        dialog.cache_max_age_spin.setValue(7)
        print("✓ Set test values")

        # Save settings
        dialog.save_settings()
        print("✓ Settings saved")

        # Create new dialog and verify values loaded
        dialog2 = ValidationSettingsDialog()
        assert dialog2.compiler_dir_edit.text() == "./test/compiler", "Compiler dir not loaded"
        assert dialog2.timeout_spin.value() == 45, "Timeout not loaded"
        assert dialog2.opcode_variant_combo.currentText() == "v1.60", "Opcode variant not loaded"
        assert dialog2.cache_enabled_check.isChecked() == False, "Cache enabled not loaded"
        assert dialog2.cache_max_age_spin.value() == 7, "Cache max age not loaded"
        print("✓ Settings loaded correctly")

        # Cleanup
        settings.clear()
        print("✓ Settings cleaned up")

        return True
    except Exception as e:
        print(f"✗ Settings persistence test failed: {e}")
        return False


def test_settings_validation():
    """Test 3: Settings validation works"""
    print("\n=== Test 3: Settings Validation ===")
    app = QApplication.instance() or QApplication(sys.argv)

    try:
        dialog = ValidationSettingsDialog()

        # Test 1: Empty compiler directory should fail
        dialog.compiler_dir_edit.setText("")
        valid, msg = dialog.validate_settings()
        assert not valid, "Empty compiler dir should be invalid"
        print(f"✓ Empty compiler dir rejected: {msg}")

        # Test 2: Non-existent directory should fail
        dialog.compiler_dir_edit.setText("./nonexistent/path")
        valid, msg = dialog.validate_settings()
        assert not valid, "Non-existent dir should be invalid"
        print(f"✓ Non-existent dir rejected: {msg}")

        # Test 3: Directory without executables should fail
        test_dir = Path("./test_compiler_dir")
        test_dir.mkdir(exist_ok=True)
        dialog.compiler_dir_edit.setText(str(test_dir))
        valid, msg = dialog.validate_settings()
        assert not valid, "Dir without executables should be invalid"
        print(f"✓ Dir without executables rejected: {msg}")

        # Cleanup
        test_dir.rmdir()

        print("✓ All validation tests passed")
        return True
    except Exception as e:
        print(f"✗ Validation test failed: {e}")
        # Cleanup
        test_dir = Path("./test_compiler_dir")
        if test_dir.exists():
            test_dir.rmdir()
        return False


def test_get_settings():
    """Test 4: get_settings() returns correct dictionary"""
    print("\n=== Test 4: get_settings() Method ===")
    app = QApplication.instance() or QApplication(sys.argv)

    try:
        dialog = ValidationSettingsDialog()

        # Set some values
        dialog.compiler_dir_edit.setText("./compiler")
        dialog.timeout_spin.setValue(60)
        dialog.opcode_variant_combo.setCurrentText("auto")
        dialog.cache_enabled_check.setChecked(True)
        dialog.cache_dir_edit.setText(".cache")
        dialog.cache_max_age_spin.setValue(30)

        # Add include directory
        dialog.include_dirs_list.addItem("./inc")
        dialog.include_dirs_list.addItem("./headers")

        # Get settings
        settings = dialog.get_settings()

        # Verify all keys present
        required_keys = [
            "compiler_dir", "include_dirs", "timeout", "opcode_variant",
            "cache_enabled", "cache_dir", "cache_max_age",
            "show_info", "show_minor", "show_cosmetic"
        ]

        for key in required_keys:
            assert key in settings, f"Missing key: {key}"
        print(f"✓ All {len(required_keys)} required keys present")

        # Verify values
        assert settings["compiler_dir"] == "./compiler"
        assert settings["timeout"] == 60
        assert settings["opcode_variant"] == "auto"
        assert settings["cache_enabled"] == True
        assert settings["cache_dir"] == ".cache"
        assert settings["cache_max_age"] == 30 * 24 * 60 * 60  # Converted to seconds
        assert settings["include_dirs"] == ["./inc", "./headers"]
        print("✓ All values correct")

        return True
    except Exception as e:
        print(f"✗ get_settings test failed: {e}")
        return False


def test_acceptance_criteria():
    """Test 5: Verify all acceptance criteria are met"""
    print("\n=== Test 5: Acceptance Criteria ===")
    app = QApplication.instance() or QApplication(sys.argv)

    criteria = {
        "User can configure compiler executable paths": False,
        "Can specify custom header file locations": False,
        "Can adjust comparison sensitivity": False,
        "Settings persist across sessions": False,
        "Validates settings before accepting": False,
    }

    try:
        dialog = ValidationSettingsDialog()

        # Criterion 1: Configure compiler executable paths
        if hasattr(dialog, 'compiler_dir_edit') and hasattr(dialog, 'browse_compiler_dir'):
            criteria["User can configure compiler executable paths"] = True
            print("✓ User can configure compiler executable paths")

        # Criterion 2: Specify custom header file locations
        if hasattr(dialog, 'include_dirs_list') and hasattr(dialog, 'add_include_dir'):
            criteria["Can specify custom header file locations"] = True
            print("✓ Can specify custom header file locations")

        # Criterion 3: Adjust comparison sensitivity
        if (hasattr(dialog, 'opcode_variant_combo') and
            hasattr(dialog, 'show_info_check') and
            hasattr(dialog, 'show_minor_check') and
            hasattr(dialog, 'show_cosmetic_check')):
            criteria["Can adjust comparison sensitivity"] = True
            print("✓ Can adjust comparison sensitivity")

        # Criterion 4: Settings persist across sessions
        if hasattr(dialog, 'save_settings') and hasattr(dialog, 'load_settings'):
            # Test persistence
            settings = QSettings("VCDecompiler", "ValidationSettings")
            settings.clear()

            dialog.compiler_dir_edit.setText("./test")
            dialog.save_settings()

            dialog2 = ValidationSettingsDialog()
            if dialog2.compiler_dir_edit.text() == "./test":
                criteria["Settings persist across sessions"] = True
                print("✓ Settings persist across sessions")

            settings.clear()

        # Criterion 5: Validates settings before accepting
        if hasattr(dialog, 'validate_settings') and hasattr(dialog, 'accept_settings'):
            dialog.compiler_dir_edit.setText("")
            valid, msg = dialog.validate_settings()
            if not valid:
                criteria["Validates settings before accepting"] = True
                print("✓ Validates settings before accepting")

        # Summary
        print("\n=== Acceptance Criteria Summary ===")
        all_met = all(criteria.values())
        for criterion, met in criteria.items():
            status = "✓" if met else "✗"
            print(f"{status} {criterion}")

        if all_met:
            print("\n✓ All acceptance criteria met!")
        else:
            print("\n✗ Some acceptance criteria not met")

        return all_met
    except Exception as e:
        print(f"✗ Acceptance criteria test failed: {e}")
        return False


def main():
    """Run all verification tests"""
    print("=" * 60)
    print("Validation Settings Dialog - Verification Tests")
    print("=" * 60)

    results = []

    results.append(("Dialog Instantiation", test_dialog_instantiation()))
    results.append(("Settings Persistence", test_settings_persistence()))
    results.append(("Settings Validation", test_settings_validation()))
    results.append(("get_settings() Method", test_get_settings()))
    results.append(("Acceptance Criteria", test_acceptance_criteria()))

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed! Settings dialog is ready.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
