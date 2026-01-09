"""
Difference visualization widgets for bytecode comparison results.

Provides specialized widgets to display and explore differences between
original and recompiled bytecode in various formats.
"""

import sys
from typing import List, Optional, Dict, Any

try:
    from PyQt6.QtWidgets import (
        QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QHBoxLayout,
        QTextEdit, QLabel, QSplitter, QGroupBox, QDialog, QPushButton
    )
    from PyQt6.QtCore import Qt, pyqtSignal
    from PyQt6.QtGui import QFont, QColor, QBrush, QTextCharFormat, QTextCursor
except ImportError:
    print("PyQt6 not installed. Install with: pip install PyQt6")
    sys.exit(1)

try:
    from ...validation import (
        Difference, DifferenceType, DifferenceSeverity,
        DifferenceCategory, CategorizedDifference
    )
except ImportError:
    # For standalone testing
    pass


class DifferenceTreeView(QTreeWidget):
    """
    Enhanced tree view for displaying differences with expandable details.

    Features:
    - Groups differences by category and severity
    - Color coding for different severity levels
    - Expandable details on double-click
    - Context menu for actions
    - Filtering by category/severity

    Signals:
        difference_selected: Emitted when a difference is selected (with Difference object)
        jump_to_location: Emitted when user wants to jump to a difference location
    """

    difference_selected = pyqtSignal(object)  # CategorizedDifference
    jump_to_location = pyqtSignal(str, str)  # location, context

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 9))
        self.setHeaderLabels(["Description", "Severity", "Category", "Location"])
        self.setAlternatingRowColors(True)
        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 120)
        self.setColumnWidth(3, 150)

        # Enable item selection
        self.itemSelectionChanged.connect(self._on_selection_changed)
        self.itemDoubleClicked.connect(self._on_item_double_clicked)

        # Store mapping from tree items to difference objects
        self._item_to_diff: Dict[QTreeWidgetItem, CategorizedDifference] = {}

    def load_differences(self, categorized_differences: List[CategorizedDifference]):
        """
        Load and display categorized differences in the tree.

        Groups differences by category, then by severity within each category.
        """
        self.clear()
        self._item_to_diff.clear()

        if not categorized_differences:
            no_diffs_item = QTreeWidgetItem(["No differences found", "", "", ""])
            self.addTopLevelItem(no_diffs_item)
            return

        # Group by category first
        by_category: Dict[DifferenceCategory, List[CategorizedDifference]] = {}
        for cat_diff in categorized_differences:
            category = cat_diff.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(cat_diff)

        # Add category nodes
        for category in [DifferenceCategory.SEMANTIC, DifferenceCategory.COSMETIC,
                        DifferenceCategory.OPTIMIZATION, DifferenceCategory.UNKNOWN]:
            if category not in by_category:
                continue

            diffs = by_category[category]

            # Create category node
            cat_item = QTreeWidgetItem([
                f"{category.value.upper()} ({len(diffs)})",
                "",
                "",
                ""
            ])
            cat_item.setFont(0, QFont("Consolas", 9, QFont.Weight.Bold))
            cat_item.setBackground(0, self._get_category_color(category))
            self.addTopLevelItem(cat_item)

            # Group by severity within category
            by_severity: Dict[DifferenceSeverity, List[CategorizedDifference]] = {}
            for cat_diff in diffs:
                severity = cat_diff.difference.severity
                if severity not in by_severity:
                    by_severity[severity] = []
                by_severity[severity].append(cat_diff)

            # Add severity sub-nodes
            for severity in [DifferenceSeverity.CRITICAL, DifferenceSeverity.MAJOR,
                            DifferenceSeverity.MINOR, DifferenceSeverity.INFO]:
                if severity not in by_severity:
                    continue

                sev_diffs = by_severity[severity]

                # Create severity node
                sev_item = QTreeWidgetItem([
                    f"{severity.value.upper()} ({len(sev_diffs)})",
                    severity.value,
                    "",
                    ""
                ])
                sev_item.setFont(0, QFont("Consolas", 9, QFont.Weight.Bold))
                sev_item.setForeground(1, QBrush(self._get_severity_color(severity)))
                cat_item.addChild(sev_item)

                # Add individual differences
                for cat_diff in sev_diffs:
                    diff = cat_diff.difference
                    diff_item = QTreeWidgetItem([
                        diff.description[:80] + ("..." if len(diff.description) > 80 else ""),
                        diff.severity.value,
                        cat_diff.category.value,
                        diff.location or ""
                    ])

                    # Color by severity
                    severity_color = self._get_severity_color(diff.severity)
                    diff_item.setForeground(1, QBrush(severity_color))

                    # Store reference
                    self._item_to_diff[diff_item] = cat_diff

                    sev_item.addChild(diff_item)

                sev_item.setExpanded(True)

            cat_item.setExpanded(True)

    def _get_category_color(self, category: DifferenceCategory) -> QBrush:
        """Get background color for category."""
        colors = {
            DifferenceCategory.SEMANTIC: QColor(100, 50, 50),      # Dark red
            DifferenceCategory.COSMETIC: QColor(50, 50, 100),      # Dark blue
            DifferenceCategory.OPTIMIZATION: QColor(50, 100, 50),  # Dark green
            DifferenceCategory.UNKNOWN: QColor(80, 80, 80),        # Gray
        }
        return QBrush(colors.get(category, QColor(80, 80, 80)))

    def _get_severity_color(self, severity: DifferenceSeverity) -> QColor:
        """Get text color for severity."""
        colors = {
            DifferenceSeverity.CRITICAL: QColor(255, 0, 0),      # Red
            DifferenceSeverity.MAJOR: QColor(255, 165, 0),       # Orange
            DifferenceSeverity.MINOR: QColor(255, 255, 0),       # Yellow
            DifferenceSeverity.INFO: QColor(0, 255, 255),        # Cyan
        }
        return colors.get(severity, QColor(255, 255, 255))

    def _on_selection_changed(self):
        """Handle selection change."""
        selected = self.selectedItems()
        if selected and selected[0] in self._item_to_diff:
            cat_diff = self._item_to_diff[selected[0]]
            self.difference_selected.emit(cat_diff)

    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle double-click to show details or jump to location."""
        if item in self._item_to_diff:
            cat_diff = self._item_to_diff[item]

            # Show details dialog
            dialog = DifferenceDetailsDialog(cat_diff, self)
            dialog.exec()


class DifferenceDetailsDialog(QDialog):
    """
    Dialog showing expandable details for a single difference.

    Displays all available information about a difference including
    original/recompiled values and additional context.
    """

    def __init__(self, cat_diff: CategorizedDifference, parent=None):
        super().__init__(parent)
        self.cat_diff = cat_diff
        self.setWindowTitle(f"Difference Details - {cat_diff.difference.location}")
        self.setMinimumSize(600, 400)

        self._init_ui()

    def _init_ui(self):
        """Initialize the dialog UI."""
        layout = QVBoxLayout(self)

        diff = self.cat_diff.difference

        # Header info
        header_text = QTextEdit()
        header_text.setReadOnly(True)
        header_text.setMaximumHeight(150)
        header_text.setFont(QFont("Consolas", 9))

        header_lines = [
            f"Type: {diff.type.value}",
            f"Severity: {diff.severity.value}",
            f"Category: {self.cat_diff.category.value}",
            f"Location: {diff.location}",
            "",
            f"Description: {diff.description}",
            "",
            f"Rationale: {self.cat_diff.rationale}",
        ]
        header_text.setPlainText("\n".join(header_lines))
        layout.addWidget(header_text)

        # Values comparison
        if diff.original_value is not None or diff.recompiled_value is not None:
            values_group = QGroupBox("Values Comparison")
            values_layout = QVBoxLayout(values_group)

            values_text = QTextEdit()
            values_text.setReadOnly(True)
            values_text.setFont(QFont("Consolas", 9))

            value_lines = []
            if diff.original_value is not None:
                value_lines.append(f"Original:\n{self._format_value(diff.original_value)}")

            if diff.recompiled_value is not None:
                value_lines.append(f"\nRecompiled:\n{self._format_value(diff.recompiled_value)}")

            values_text.setPlainText("\n".join(value_lines))
            values_layout.addWidget(values_text)
            layout.addWidget(values_group)

        # Additional details
        if diff.details:
            details_group = QGroupBox("Additional Details")
            details_layout = QVBoxLayout(details_group)

            details_text = QTextEdit()
            details_text.setReadOnly(True)
            details_text.setFont(QFont("Consolas", 9))

            detail_lines = []
            for key, value in diff.details.items():
                detail_lines.append(f"{key}: {value}")

            details_text.setPlainText("\n".join(detail_lines))
            details_layout.addWidget(details_text)
            layout.addWidget(details_group)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def _format_value(self, value: Any) -> str:
        """Format a value for display."""
        if isinstance(value, (list, tuple)):
            return "\n".join(str(item) for item in value)
        elif isinstance(value, dict):
            return "\n".join(f"  {k}: {v}" for k, v in value.items())
        else:
            return str(value)


class InstructionDiffView(QWidget):
    """
    Side-by-side view for comparing code differences at the instruction level.

    Shows original and recompiled instructions side-by-side with
    highlighting for differences.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title
        title = QLabel("Instruction Comparison")
        title.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        layout.addWidget(title)

        # Create splitter for side-by-side view
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Original code
        orig_group = QGroupBox("Original")
        orig_layout = QVBoxLayout(orig_group)
        self.original_text = QTextEdit()
        self.original_text.setReadOnly(True)
        self.original_text.setFont(QFont("Consolas", 9))
        orig_layout.addWidget(self.original_text)
        splitter.addWidget(orig_group)

        # Recompiled code
        recomp_group = QGroupBox("Recompiled")
        recomp_layout = QVBoxLayout(recomp_group)
        self.recompiled_text = QTextEdit()
        self.recompiled_text.setReadOnly(True)
        self.recompiled_text.setFont(QFont("Consolas", 9))
        recomp_layout.addWidget(self.recompiled_text)
        splitter.addWidget(recomp_group)

        layout.addWidget(splitter)

    def load_code_difference(self, diff: Difference):
        """
        Load a code difference for side-by-side comparison.

        Args:
            diff: Difference object with code comparison data
        """
        self.original_text.clear()
        self.recompiled_text.clear()

        if diff.type != DifferenceType.CODE:
            self.original_text.setPlainText("Not a code difference")
            return

        # Extract instruction data from details
        details = diff.details

        if "original_instruction" in details:
            orig_instr = details["original_instruction"]
            self.original_text.setPlainText(self._format_instruction(orig_instr))
        elif diff.original_value:
            self.original_text.setPlainText(str(diff.original_value))

        if "recompiled_instruction" in details:
            recomp_instr = details["recompiled_instruction"]
            self.recompiled_text.setPlainText(self._format_instruction(recomp_instr))
        elif diff.recompiled_value:
            self.recompiled_text.setPlainText(str(diff.recompiled_value))

        # Highlight differences
        self._highlight_differences()

    def _format_instruction(self, instr: Any) -> str:
        """Format an instruction for display."""
        if isinstance(instr, dict):
            lines = []
            for key, value in instr.items():
                lines.append(f"{key}: {value}")
            return "\n".join(lines)
        else:
            return str(instr)

    def _highlight_differences(self):
        """Highlight differences between original and recompiled text."""
        # Simple highlighting - could be enhanced with diff algorithm
        orig_text = self.original_text.toPlainText()
        recomp_text = self.recompiled_text.toPlainText()

        if orig_text != recomp_text:
            # Apply yellow background to both
            fmt = QTextCharFormat()
            fmt.setBackground(QColor(255, 255, 0, 50))  # Light yellow

            cursor = self.original_text.textCursor()
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.setCharFormat(fmt)

            cursor = self.recompiled_text.textCursor()
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.setCharFormat(fmt)


class DataDiffView(QWidget):
    """
    Hex comparison view for data segment differences.

    Shows byte-level differences in data segments with hex and ASCII representation.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title
        title = QLabel("Data Comparison (Hex View)")
        title.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        layout.addWidget(title)

        # Create splitter for side-by-side view
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Original data
        orig_group = QGroupBox("Original")
        orig_layout = QVBoxLayout(orig_group)
        self.original_hex = QTextEdit()
        self.original_hex.setReadOnly(True)
        self.original_hex.setFont(QFont("Consolas", 9))
        orig_layout.addWidget(self.original_hex)
        splitter.addWidget(orig_group)

        # Recompiled data
        recomp_group = QGroupBox("Recompiled")
        recomp_layout = QVBoxLayout(recomp_group)
        self.recompiled_hex = QTextEdit()
        self.recompiled_hex.setReadOnly(True)
        self.recompiled_hex.setFont(QFont("Consolas", 9))
        recomp_layout.addWidget(self.recompiled_hex)
        splitter.addWidget(recomp_group)

        layout.addWidget(splitter)

    def load_data_difference(self, diff: Difference):
        """
        Load a data difference for hex comparison.

        Args:
            diff: Difference object with data comparison data
        """
        self.original_hex.clear()
        self.recompiled_hex.clear()

        if diff.type != DifferenceType.DATA:
            self.original_hex.setPlainText("Not a data difference")
            return

        # Extract data from details
        details = diff.details

        if "original_data" in details:
            orig_data = details["original_data"]
            self.original_hex.setPlainText(self._format_hex(orig_data))
        elif diff.original_value:
            if isinstance(diff.original_value, (bytes, bytearray)):
                self.original_hex.setPlainText(self._format_hex(diff.original_value))
            else:
                self.original_hex.setPlainText(str(diff.original_value))

        if "recompiled_data" in details:
            recomp_data = details["recompiled_data"]
            self.recompiled_hex.setPlainText(self._format_hex(recomp_data))
        elif diff.recompiled_value:
            if isinstance(diff.recompiled_value, (bytes, bytearray)):
                self.recompiled_hex.setPlainText(self._format_hex(diff.recompiled_value))
            else:
                self.recompiled_hex.setPlainText(str(diff.recompiled_value))

    def _format_hex(self, data: Any) -> str:
        """
        Format data as hex dump.

        Format: offset | hex bytes | ASCII
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif not isinstance(data, (bytes, bytearray)):
            return str(data)

        lines = []
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]

            # Offset
            offset = f"{i:08x}"

            # Hex bytes
            hex_part = " ".join(f"{b:02x}" for b in chunk)
            hex_part = hex_part.ljust(48)  # 16 bytes * 3 chars

            # ASCII part
            ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)

            lines.append(f"{offset} | {hex_part} | {ascii_part}")

        return "\n".join(lines) if lines else "(empty)"
