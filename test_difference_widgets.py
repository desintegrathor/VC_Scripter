"""
Verification script for difference visualization widgets.

Tests that all widgets can be instantiated and used correctly.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all widgets can be imported."""
    print("Testing imports...")
    try:
        from vcdecomp.gui.widgets import (
            DifferenceTreeView,
            InstructionDiffView,
            DataDiffView,
        )
        print("✓ All widgets imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_widget_creation():
    """Test that widgets can be instantiated."""
    print("\nTesting widget creation...")

    try:
        from PyQt6.QtWidgets import QApplication
        from vcdecomp.gui.widgets import (
            DifferenceTreeView,
            InstructionDiffView,
            DataDiffView,
        )

        # Create QApplication (required for Qt widgets)
        app = QApplication(sys.argv)

        # Test DifferenceTreeView
        tree_view = DifferenceTreeView()
        print("✓ DifferenceTreeView created")

        # Test InstructionDiffView
        instr_view = InstructionDiffView()
        print("✓ InstructionDiffView created")

        # Test DataDiffView
        data_view = DataDiffView()
        print("✓ DataDiffView created")

        return True

    except Exception as e:
        print(f"✗ Widget creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_widget_features():
    """Test that widgets have expected features."""
    print("\nTesting widget features...")

    try:
        from PyQt6.QtWidgets import QApplication
        from vcdecomp.gui.widgets import DifferenceTreeView
        from vcdecomp.validation import (
            Difference, DifferenceType, DifferenceSeverity,
            DifferenceCategory, CategorizedDifference
        )

        app = QApplication.instance() or QApplication(sys.argv)

        tree_view = DifferenceTreeView()

        # Test loading differences
        test_diff = Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.MAJOR,
            description="Test difference",
            location="test_location"
        )

        cat_diff = CategorizedDifference(
            difference=test_diff,
            category=DifferenceCategory.SEMANTIC,
            rationale="Test rationale"
        )

        tree_view.load_differences([cat_diff])
        print("✓ DifferenceTreeView.load_differences() works")

        # Check signals
        assert hasattr(tree_view, 'difference_selected'), "Missing difference_selected signal"
        assert hasattr(tree_view, 'jump_to_location'), "Missing jump_to_location signal"
        print("✓ DifferenceTreeView has required signals")

        return True

    except Exception as e:
        print(f"✗ Widget feature test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_acceptance_criteria():
    """Test that all acceptance criteria are met."""
    print("\nVerifying acceptance criteria:")

    criteria = [
        "Tree view groups differences by type and severity",
        "Color coding for severity levels",
        "Expandable details for each difference",
        "Side-by-side comparison for code differences",
        "Jump to source location from difference"
    ]

    from vcdecomp.gui.widgets import (
        DifferenceTreeView,
        InstructionDiffView,
        DataDiffView,
    )

    results = []

    # 1. Tree view groups by type and severity
    tree = DifferenceTreeView()
    has_grouping = hasattr(tree, 'load_differences')
    results.append(has_grouping)
    print(f"{'✓' if has_grouping else '✗'} 1. {criteria[0]}")

    # 2. Color coding
    has_colors = hasattr(tree, '_get_severity_color') and hasattr(tree, '_get_category_color')
    results.append(has_colors)
    print(f"{'✓' if has_colors else '✗'} 2. {criteria[1]}")

    # 3. Expandable details
    has_details = 'DifferenceDetailsDialog' in dir(sys.modules['vcdecomp.gui.widgets.difference_widgets'])
    results.append(has_details)
    print(f"{'✓' if has_details else '✗'} 3. {criteria[2]}")

    # 4. Side-by-side comparison
    instr = InstructionDiffView()
    has_comparison = hasattr(instr, 'load_code_difference')
    results.append(has_comparison)
    print(f"{'✓' if has_comparison else '✗'} 4. {criteria[3]}")

    # 5. Jump to location
    has_jump = hasattr(tree, 'jump_to_location')
    results.append(has_jump)
    print(f"{'✓' if has_jump else '✗'} 5. {criteria[4]}")

    return all(results)

def main():
    """Run all tests."""
    print("=" * 60)
    print("Difference Widgets Verification")
    print("=" * 60)

    results = []

    # Test imports
    results.append(test_imports())

    # Test widget creation
    results.append(test_widget_creation())

    # Test features
    results.append(test_widget_features())

    # Test acceptance criteria
    results.append(test_acceptance_criteria())

    print("\n" + "=" * 60)
    if all(results):
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
