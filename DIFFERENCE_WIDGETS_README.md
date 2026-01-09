# Difference Visualization Widgets

## Overview

This module provides specialized widgets for visualizing bytecode comparison differences in the GUI. Created for subtask-4-3 of the Recompilation Validation System.

## Widgets

### 1. DifferenceTreeView

Enhanced tree widget for displaying differences with hierarchical grouping.

**Features:**
- ✓ Groups differences by category (SEMANTIC, COSMETIC, OPTIMIZATION, UNKNOWN)
- ✓ Sub-groups by severity (CRITICAL, MAJOR, MINOR, INFO)
- ✓ Color coding for categories and severities
- ✓ Expandable details on double-click (shows DifferenceDetailsDialog)
- ✓ Signals for selection and navigation

**Signals:**
- `difference_selected(CategorizedDifference)` - Emitted when a difference is selected
- `jump_to_location(str, str)` - Emitted when user wants to jump to location

**Usage:**
```python
from vcdecomp.gui.widgets import DifferenceTreeView

tree = DifferenceTreeView()
tree.load_differences(categorized_differences)

# Connect signals
tree.difference_selected.connect(on_diff_selected)
tree.jump_to_location.connect(on_jump)
```

### 2. InstructionDiffView

Side-by-side comparison view for code differences.

**Features:**
- ✓ Side-by-side layout (original vs recompiled)
- ✓ Instruction-level comparison
- ✓ Syntax highlighting for differences
- ✓ Formatted instruction display

**Usage:**
```python
from vcdecomp.gui.widgets import InstructionDiffView

view = InstructionDiffView()
view.load_code_difference(code_difference)
```

### 3. DataDiffView

Hex dump comparison view for data segment differences.

**Features:**
- ✓ Side-by-side hex dump (original vs recompiled)
- ✓ Byte-level comparison
- ✓ Hex and ASCII display
- ✓ Offset display

**Usage:**
```python
from vcdecomp.gui.widgets import DataDiffView

view = DataDiffView()
view.load_data_difference(data_difference)
```

### 4. DifferenceDetailsDialog

Modal dialog showing expandable details for a single difference.

**Features:**
- ✓ Full difference information (type, severity, category, location)
- ✓ Categorization rationale
- ✓ Original vs recompiled values
- ✓ Additional details dictionary

**Usage:**
```python
# Automatically shown when double-clicking in DifferenceTreeView
# Or manually:
from vcdecomp.gui.widgets.difference_widgets import DifferenceDetailsDialog

dialog = DifferenceDetailsDialog(categorized_difference)
dialog.exec()
```

## Color Coding

### Category Colors (Background):
- **SEMANTIC** (Dark Red): Changes that affect program behavior
- **COSMETIC** (Dark Blue): No behavioral impact (ordering, padding)
- **OPTIMIZATION** (Dark Green): Semantically equivalent
- **UNKNOWN** (Gray): Cannot determine category

### Severity Colors (Text):
- **CRITICAL** (Red): Definitely affects behavior
- **MAJOR** (Orange): Significant difference
- **MINOR** (Yellow): Minor difference
- **INFO** (Cyan): Informational only

## Integration Example

To integrate these widgets into a validation panel:

```python
from vcdecomp.gui.widgets import DifferenceTreeView, InstructionDiffView, DataDiffView

# Create tree view
self.diff_tree = DifferenceTreeView()
self.diff_tree.difference_selected.connect(self.on_diff_selected)

# Create detail views
self.instr_view = InstructionDiffView()
self.data_view = DataDiffView()

# Load results
self.diff_tree.load_differences(result.categorized_differences)

def on_diff_selected(self, cat_diff):
    """Handle difference selection."""
    if cat_diff.difference.type == DifferenceType.CODE:
        self.instr_view.load_code_difference(cat_diff.difference)
    elif cat_diff.difference.type == DifferenceType.DATA:
        self.data_view.load_data_difference(cat_diff.difference)
```

## Acceptance Criteria Met

- ✅ Tree view groups differences by type and severity
- ✅ Color coding for severity levels
- ✅ Expandable details for each difference
- ✅ Side-by-side comparison for code differences
- ✅ Jump to source location from difference (via signals)

## Dependencies

- PyQt6 (QtWidgets, QtCore, QtGui)
- vcdecomp.validation (Difference, CategorizedDifference types)

## Files

- `vcdecomp/gui/widgets/__init__.py` - Module exports
- `vcdecomp/gui/widgets/difference_widgets.py` - Widget implementations (18KB)
- `test_difference_widgets.py` - Verification script

## Notes

This implementation takes a **simple, focused approach** compared to previous attempts:
- Uses standard Qt widgets (QTreeWidget, QTextEdit) rather than custom implementations
- Leverages existing categorization system from Phase 2
- Minimal dependencies and complexity
- Clear separation of concerns (tree view, code view, data view)
- Easy to extend and maintain
