"""
Error analysis view for interactive error pattern exploration.

Provides a dock panel for analyzing error patterns across multiple validation
runs. Displays aggregated error statistics with hierarchical tree view for
drilling down into specific error instances.

Enhanced with:
- Side-by-side diff viewer for assembly vs C comparison
- Bytecode instruction-level comparison
- Test failure log export functionality
"""

import sys
from pathlib import Path
from typing import List, Optional

try:
    from PyQt6.QtWidgets import (
        QWidget, QVBoxLayout, QPushButton, QLabel, QGroupBox, QTextEdit,
        QSplitter, QMessageBox, QFileDialog, QHBoxLayout
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
    from ...validation.test_case_logger import log_failed_test_case
    from ..widgets.error_tree_widget import ErrorTreeWidget
    from ..widgets.diff_viewer_widget import DiffViewerWidget
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
    - Side-by-side diff viewer for assembly/C comparison
    - Bytecode instruction-level comparison
    - Test failure log export
    - Manual refresh button for on-demand analysis

    Signals:
        detail_requested: Emitted when user selects an error (for future integration)
    """

    detail_requested = pyqtSignal(object)  # CompilationError

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_result: Optional[ValidationResult] = None
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

        # Main content: vertical splitter (error tree top, diff viewer bottom)
        self.main_splitter = QSplitter(Qt.Orientation.Vertical)

        # Top: ErrorTreeWidget
        tree_group = QGroupBox("Error Patterns")
        tree_layout = QVBoxLayout(tree_group)
        tree_layout.setContentsMargins(8, 8, 8, 8)

        self.error_tree = ErrorTreeWidget()
        self.error_tree.error_selected.connect(self._on_error_selected)
        tree_layout.addWidget(self.error_tree, 1)

        self.main_splitter.addWidget(tree_group)

        # Bottom: Diff viewer (initially collapsed)
        diff_group = QGroupBox("Comparison View")
        diff_layout = QVBoxLayout(diff_group)
        diff_layout.setContentsMargins(8, 8, 8, 8)

        self.diff_viewer = DiffViewerWidget()
        diff_layout.addWidget(self.diff_viewer)

        self.main_splitter.addWidget(diff_group)

        # Set initial sizes (error tree larger, diff viewer smaller)
        self.main_splitter.setSizes([400, 200])

        layout.addWidget(self.main_splitter, 1)

        # Bottom buttons
        button_layout = QHBoxLayout()

        self.export_log_button = QPushButton("Export Failure Log")
        self.export_log_button.setFont(QFont("Consolas", 9))
        self.export_log_button.clicked.connect(self._on_export_log)
        self.export_log_button.setEnabled(False)
        button_layout.addWidget(self.export_log_button)

        button_layout.addStretch()

        self.analyze_btn = QPushButton("Analyze Test Results")
        self.analyze_btn.setFont(QFont("Consolas", 10))
        self.analyze_btn.clicked.connect(self._on_analyze_clicked)
        self.analyze_btn.setEnabled(False)  # Disabled until integration complete
        button_layout.addWidget(self.analyze_btn)

        layout.addLayout(button_layout)

    def load_validation_results(self, results: List[ValidationResult]):
        """
        Load validation results and display aggregated error analysis.

        This method:
        1. Uses ErrorAnalyzer to aggregate errors across results
        2. Updates summary label with total counts
        3. Populates error tree with categorized patterns
        4. Stores first failed result for diff viewing

        Args:
            results: List of ValidationResult objects to analyze
        """
        if not results:
            self.summary_label.setText("No results to analyze.")
            self.error_tree.clear()
            self.export_log_button.setEnabled(False)
            return

        # Store first failed result for diff viewing and export
        for result in results:
            if not result.success:
                self._current_result = result
                break

        # Use ErrorAnalyzer to aggregate errors
        analyzer = ErrorAnalyzer()
        patterns = analyzer.analyze_batch_results(results)

        if not patterns:
            self.summary_label.setText(f"Analyzed {len(results)} validation results.\n\nNo compilation errors found.")
            self.error_tree.load_error_patterns([])
            self.export_log_button.setEnabled(False)
            return

        # Calculate total error count
        total_errors = sum(pattern.count for pattern in patterns)

        # Update summary label
        summary_text = f"Analyzed {len(results)} validation results.\n\nTotal errors: {total_errors}"
        self.summary_label.setText(summary_text)

        # Load patterns into tree
        self.error_tree.load_error_patterns(patterns)

        # Enable export if we have a failed result
        self.export_log_button.setEnabled(self._current_result is not None)

    def clear(self):
        """
        Clear error analysis display.

        Used when starting new analysis or resetting state.
        """
        self.summary_label.setText("No results to analyze.")
        self.error_tree.clear()
        self.diff_viewer.clear()
        self.export_log_button.setEnabled(False)
        self._current_result = None

    def show_diff_for_error(self, original_asm: str, decompiled_c: str):
        """
        Show side-by-side diff for a specific error.

        This is a public method that can be called from external code
        when original assembly and decompiled C are available.

        Args:
            original_asm: Original assembly code as string
            decompiled_c: Decompiled C code as string
        """
        self.diff_viewer.show_diff(original_asm, decompiled_c)

        # Make sure diff viewer is visible
        if self.main_splitter.sizes()[1] < 100:
            # If diff viewer is collapsed, expand it
            total = sum(self.main_splitter.sizes())
            self.main_splitter.setSizes([total // 2, total // 2])

    def _on_error_selected(self, error: CompilationError):
        """
        Handle error selection from tree.

        Shows bytecode diff if validation result is available.

        Args:
            error: CompilationError object that was selected
        """
        # Emit signal for future integration with detail view
        self.detail_requested.emit(error)

        # Show bytecode diff if we have validation result with comparison
        if self._current_result and self._current_result.comparison_result:
            try:
                if self._current_result.compilation_result and self._current_result.compilation_result.output_file:
                    self.diff_viewer.show_bytecode_diff(
                        self._current_result.original_scr,
                        self._current_result.compilation_result.output_file
                    )

                    # Expand diff viewer if collapsed
                    if self.main_splitter.sizes()[1] < 100:
                        total = sum(self.main_splitter.sizes())
                        self.main_splitter.setSizes([total // 2, total // 2])
            except Exception as e:
                # If bytecode diff fails, just ignore (diff viewer shows error internally)
                pass

    def _on_export_log(self):
        """Handle export failure log button click."""
        if not self._current_result:
            QMessageBox.warning(
                self,
                "No Results",
                "No validation result loaded to export."
            )
            return

        # Ask user for output directory
        default_dir = Path(".planning/test_failures")
        output_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory for Failure Log",
            str(default_dir.absolute()),
            QFileDialog.Option.ShowDirsOnly
        )

        if not output_dir:
            return  # User cancelled

        try:
            # Generate failure log
            output_path = log_failed_test_case(
                self._current_result,
                Path(output_dir)
            )

            # Show success message
            QMessageBox.information(
                self,
                "Export Successful",
                f"Failure log saved to:\n{output_path.absolute()}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to export failure log:\n{e}"
            )

    def _on_analyze_clicked(self):
        """
        Handle analyze button click.

        Future integration point for triggering batch analysis of test results.
        Currently disabled pending test result storage implementation.
        """
        # TODO: Implement when test result storage is available
        # For now, this button is disabled
        pass
