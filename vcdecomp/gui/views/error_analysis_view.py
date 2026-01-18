"""
Error analysis view for interactive error pattern exploration.

Provides a dock panel for analyzing error patterns across multiple validation
runs. Displays aggregated error statistics with hierarchical tree view for
drilling down into specific error instances.
"""

import sys
from typing import List, Optional

try:
    from PyQt6.QtWidgets import (
        QWidget, QVBoxLayout, QPushButton, QLabel, QGroupBox, QTextEdit
    )
    from PyQt6.QtCore import Qt, pyqtSignal
    from PyQt6.QtGui import QFont
except ImportError:
    print("PyQt6 not installed. Install with: pip install PyQt6")
    sys.exit(1)

try:
    from ...validation.error_analyzer import ErrorAnalyzer, ErrorPattern
    from ...validation.validation_types import ValidationResult
    from ...validation.compilation_types import CompilationError
    from ..widgets.error_tree_widget import ErrorTreeWidget
except ImportError:
    # For standalone testing
    pass


class ErrorAnalysisPanel(QWidget):
    """
    Panel for error pattern analysis and visualization.

    Features:
    - Load validation results for batch analysis
    - Display aggregated error statistics summary
    - Hierarchical tree view for exploring error patterns
    - Manual refresh button for on-demand analysis

    Signals:
        detail_requested: Emitted when user selects an error (for future integration)
    """

    detail_requested = pyqtSignal(object)  # CompilationError

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        # Title label
        title_label = QLabel("Error Analysis")
        title_label.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Stats summary group
        summary_group = QGroupBox("Summary")
        summary_layout = QVBoxLayout(summary_group)
        summary_layout.setContentsMargins(8, 8, 8, 8)

        self.summary_label = QLabel("No results to analyze.")
        self.summary_label.setFont(QFont("Consolas", 9))
        self.summary_label.setWordWrap(True)
        summary_layout.addWidget(self.summary_label)

        layout.addWidget(summary_group)

        # ErrorTreeWidget (main content)
        tree_group = QGroupBox("Error Patterns")
        tree_layout = QVBoxLayout(tree_group)
        tree_layout.setContentsMargins(8, 8, 8, 8)

        self.error_tree = ErrorTreeWidget()
        self.error_tree.error_selected.connect(self._on_error_selected)
        tree_layout.addWidget(self.error_tree, 1)

        layout.addWidget(tree_group, 1)

        # Refresh button
        self.analyze_btn = QPushButton("Analyze Test Results")
        self.analyze_btn.setFont(QFont("Consolas", 10))
        self.analyze_btn.clicked.connect(self._on_analyze_clicked)
        self.analyze_btn.setEnabled(False)  # Disabled until integration complete
        layout.addWidget(self.analyze_btn)

    def load_validation_results(self, results: List[ValidationResult]):
        """
        Load validation results and display aggregated error analysis.

        This method:
        1. Uses ErrorAnalyzer to aggregate errors across results
        2. Updates summary label with total counts
        3. Populates error tree with categorized patterns

        Args:
            results: List of ValidationResult objects to analyze
        """
        if not results:
            self.summary_label.setText("No results to analyze.")
            self.error_tree.clear()
            return

        # Use ErrorAnalyzer to aggregate errors
        analyzer = ErrorAnalyzer()
        patterns = analyzer.analyze_batch_results(results)

        if not patterns:
            self.summary_label.setText(f"Analyzed {len(results)} validation results.\n\nNo compilation errors found.")
            self.error_tree.load_error_patterns([])
            return

        # Calculate total error count
        total_errors = sum(pattern.count for pattern in patterns)

        # Update summary label
        summary_text = f"Analyzed {len(results)} validation results.\n\nTotal errors: {total_errors}"
        self.summary_label.setText(summary_text)

        # Load patterns into tree
        self.error_tree.load_error_patterns(patterns)

    def clear(self):
        """
        Clear error analysis display.

        Used when starting new analysis or resetting state.
        """
        self.summary_label.setText("No results to analyze.")
        self.error_tree.clear()

    def _on_error_selected(self, error: CompilationError):
        """
        Handle error selection from tree.

        Emits detail_requested signal for future side-by-side view integration.

        Args:
            error: CompilationError object that was selected
        """
        # Emit signal for future integration with detail view
        self.detail_requested.emit(error)

    def _on_analyze_clicked(self):
        """
        Handle analyze button click.

        Future integration point for triggering batch analysis of test results.
        Currently disabled pending test result storage implementation.
        """
        # TODO: Implement when test result storage is available
        # For now, this button is disabled
        pass
