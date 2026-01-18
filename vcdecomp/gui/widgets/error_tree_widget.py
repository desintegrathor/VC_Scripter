"""
Error tree widget for hierarchical error pattern display.

Provides a tree view for displaying aggregated error patterns from batch validation
runs. Groups errors by type (syntax, semantic, type, include, other) with counts,
percentages, and expandable examples.
"""

import sys
from typing import List, Optional

try:
    from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PyQt6.QtCore import Qt, pyqtSignal
    from PyQt6.QtGui import QFont, QColor, QBrush
except ImportError:
    print("PyQt6 not installed. Install with: pip install PyQt6")
    sys.exit(1)

try:
    from ...validation.error_analyzer import ErrorPattern
    from ...validation.compilation_types import CompilationError
except ImportError:
    # For standalone testing
    pass


class ErrorTreeWidget(QTreeWidget):
    """
    Hierarchical tree view for displaying error patterns.

    Features:
    - Groups errors by type (syntax, semantic, type, include, other)
    - Shows counts and percentages for each category
    - Color-coded categories for visual distinction
    - Expandable examples under each category
    - Selection signals for detail viewing

    Signals:
        error_selected: Emitted when user selects an error item (with CompilationError object)
    """

    error_selected = pyqtSignal(object)  # CompilationError

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 9))
        self.setHeaderLabels(["Error Type", "Count", "Percentage", "Examples"])
        self.setAlternatingRowColors(True)
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 400)

        # Enable item selection
        self.itemSelectionChanged.connect(self._on_selection_changed)

        # Store mapping from tree items to error objects
        self._item_to_error: dict[QTreeWidgetItem, CompilationError] = {}

    def load_error_patterns(self, patterns: List[ErrorPattern]):
        """
        Load and display error patterns in the tree.

        Groups errors by type with counts and percentages, then shows expandable
        examples under each category.

        Args:
            patterns: List of ErrorPattern objects from ErrorAnalyzer.analyze_batch_results()
        """
        self.clear()
        self._item_to_error.clear()

        if not patterns:
            # Show placeholder when no patterns provided
            no_errors_item = QTreeWidgetItem(["No errors to display", "", "", ""])
            self.addTopLevelItem(no_errors_item)
            return

        # Add top-level items for each error type
        for pattern in patterns:
            # Create category node
            cat_item = QTreeWidgetItem([
                f"{pattern.error_type.upper()} ERRORS ({pattern.count})",
                str(pattern.count),
                f"{pattern.percentage:.1f}%",
                ""
            ])
            cat_item.setFont(0, QFont("Consolas", 9, QFont.Weight.Bold))
            cat_item.setBackground(0, self._get_error_type_color(pattern.error_type))
            self.addTopLevelItem(cat_item)

            # Add child items for examples (limit to first 5)
            for example in pattern.examples[:5]:
                # Format example text: file:line - message
                example_text = self._format_example(example)

                # Truncate long messages to 100 chars
                if len(example_text) > 100:
                    example_text = example_text[:97] + "..."

                example_item = QTreeWidgetItem([
                    "",
                    "",
                    "",
                    example_text
                ])

                # Store CompilationError object in item data for detail view
                self._item_to_error[example_item] = example

                cat_item.addChild(example_item)

            # Make category nodes expandable (collapsed by default)
            cat_item.setExpanded(False)

    def _get_error_type_color(self, error_type: str) -> QBrush:
        """Get background color for error type."""
        colors = {
            "syntax": QColor(255, 230, 230),      # Light red (#ffe6e6)
            "semantic": QColor(255, 250, 205),    # Light yellow (#fffacd)
            "type": QColor(230, 242, 255),        # Light blue (#e6f2ff)
            "include": QColor(240, 240, 240),     # Light gray (#f0f0f0)
            "other": QColor(255, 255, 255),       # White
        }
        return QBrush(colors.get(error_type, QColor(255, 255, 255)))

    def _format_example(self, error: CompilationError) -> str:
        """
        Format an error example for display.

        Format: file:line - message

        Args:
            error: CompilationError object

        Returns:
            Formatted string for display
        """
        parts = []

        # Add file and line if available
        if error.file:
            file_str = error.file.name if hasattr(error.file, 'name') else str(error.file)
            parts.append(file_str)

        if error.line:
            if parts:
                parts[-1] += f":{error.line}"
            else:
                parts.append(f"line {error.line}")

        # Add message
        message = error.message
        if parts:
            return f"{':'.join(parts)} - {message}"
        else:
            return message

    def _on_selection_changed(self):
        """Handle selection change."""
        selected = self.selectedItems()
        if selected and selected[0] in self._item_to_error:
            error = self._item_to_error[selected[0]]
            self.error_selected.emit(error)
