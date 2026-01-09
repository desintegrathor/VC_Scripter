"""
Validation view for recompilation validation system
"""

import sys
import time
from pathlib import Path
from typing import Optional
from enum import Enum

try:
    from PyQt6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
        QTreeWidget, QTreeWidgetItem, QGroupBox, QTextEdit,
        QProgressBar, QFileDialog, QMessageBox, QSplitter, QDialog
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
    from PyQt6.QtGui import QFont, QColor, QBrush
except ImportError:
    print("PyQt6 not installed. Install with: pip install PyQt6")
    sys.exit(1)

from ...validation import (
    ValidationOrchestrator,
    ValidationResult,
    ValidationVerdict,
    DifferenceCategory,
    DifferenceSeverity,
    ReportGenerator,
)
from ..dialogs import ValidationSettingsDialog


class ValidationStatus(Enum):
    """Validation panel status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETE = "complete"
    ERROR = "error"


class ValidationWorker(QThread):
    """Background worker for validation to avoid blocking GUI"""

    finished = pyqtSignal(object)  # ValidationResult or Exception
    progress = pyqtSignal(str, int)  # Progress message, percentage (0-100)
    time_estimate = pyqtSignal(str)  # Estimated time remaining

    def __init__(
        self,
        original_scr: str,
        decompiled_source: str,
        compiler_dir: str,
        include_dirs: Optional[list] = None,
        timeout: int = 30,
        opcode_variant: str = "auto",
        cache_enabled: bool = True,
        cache_dir: str = ".validation_cache",
        cache_max_age: int = 0,
    ):
        super().__init__()
        self.original_scr = original_scr
        self.decompiled_source = decompiled_source
        self.compiler_dir = compiler_dir
        self.include_dirs = include_dirs or []
        self.timeout = timeout
        self.opcode_variant = opcode_variant
        self.cache_enabled = cache_enabled
        self.cache_dir = cache_dir
        self.cache_max_age = cache_max_age
        self._cancel_requested = False
        self._start_time = None

    def cancel(self):
        """Request cancellation of validation"""
        self._cancel_requested = True

    def _emit_progress(self, message: str, percentage: int):
        """Emit progress update with time estimate"""
        self.progress.emit(message, percentage)

        if self._start_time and percentage > 0:
            elapsed = time.time() - self._start_time
            estimated_total = elapsed / (percentage / 100.0)
            remaining = estimated_total - elapsed

            if remaining > 0:
                if remaining < 60:
                    time_str = f"{remaining:.0f} seconds remaining"
                else:
                    minutes = remaining / 60
                    time_str = f"{minutes:.1f} minutes remaining"
                self.time_estimate.emit(time_str)

    def run(self):
        """Run validation in background thread"""
        import time

        try:
            self._start_time = time.time()
            self._emit_progress("Initializing validation...", 0)

            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            # Step 1: Initialize orchestrator (5%)
            orchestrator = ValidationOrchestrator(
                compiler_dir=self.compiler_dir,
                include_dirs=self.include_dirs,
                timeout=self.timeout,
                opcode_variant=self.opcode_variant,
                cache_dir=self.cache_dir,
                cache_enabled=self.cache_enabled,
                cache_max_age=self.cache_max_age,
            )
            self._emit_progress("Validation initialized", 5)

            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            # Step 2: Compile (30% of total work)
            self._emit_progress("Starting compilation...", 10)

            # We'll simulate sub-steps of compilation for better progress tracking
            from pathlib import Path

            original_scr = Path(self.original_scr)
            decompiled_source = Path(self.decompiled_source)

            # Validate files
            if not original_scr.exists():
                raise FileNotFoundError(f"Original SCR not found: {original_scr}")
            if not decompiled_source.exists():
                raise FileNotFoundError(f"Decompiled source not found: {decompiled_source}")

            self._emit_progress("Preprocessing source code (SPP)...", 15)
            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            self._emit_progress("Compiling to assembly (SCC)...", 25)
            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            self._emit_progress("Assembling bytecode (SASM)...", 35)
            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            # Run the actual validation (this includes all the compilation steps)
            result = orchestrator.validate(self.original_scr, self.decompiled_source)

            # Check if compilation succeeded
            if not result.compilation_succeeded:
                self._emit_progress("Compilation failed", 100)
                self.finished.emit(result)
                return

            self._emit_progress("Compilation complete", 45)
            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            # Step 3: Comparison (40% of total work)
            self._emit_progress("Comparing headers...", 50)
            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            self._emit_progress("Comparing data segments...", 60)
            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            self._emit_progress("Comparing code segments...", 70)
            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            self._emit_progress("Comparing external function tables...", 80)
            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            # Step 4: Analysis and reporting (25% of total work)
            self._emit_progress("Categorizing differences...", 85)
            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            self._emit_progress("Generating recommendations...", 95)
            if self._cancel_requested:
                self.finished.emit(Exception("Validation cancelled by user"))
                return

            self._emit_progress("Validation complete", 100)
            self.finished.emit(result)

        except Exception as e:
            self._emit_progress(f"Validation failed: {str(e)}", 0)
            self.finished.emit(e)


class ValidationPanel(QWidget):
    """Panel for validation operations and results display"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.status = ValidationStatus.IDLE
        self.validation_result: Optional[ValidationResult] = None
        self.worker: Optional[ValidationWorker] = None
        self.original_scr_path: Optional[str] = None
        self.decompiled_source_path: Optional[str] = None
        self.compiler_dir: Optional[str] = None

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        # Header with status
        header_layout = QHBoxLayout()

        self.status_label = QLabel("Status: Idle")
        self.status_label.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        header_layout.addWidget(self.status_label)

        header_layout.addStretch()

        # Cancel button (hidden by default)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(QFont("Consolas", 10))
        self.cancel_btn.clicked.connect(self.on_cancel_clicked)
        self.cancel_btn.setVisible(False)
        header_layout.addWidget(self.cancel_btn)

        # Settings button
        self.settings_btn = QPushButton("Settings...")
        self.settings_btn.setFont(QFont("Consolas", 10))
        self.settings_btn.clicked.connect(self.on_settings_clicked)
        header_layout.addWidget(self.settings_btn)

        # Validate button
        self.validate_btn = QPushButton("Validate")
        self.validate_btn.setFont(QFont("Consolas", 10))
        self.validate_btn.clicked.connect(self.on_validate_clicked)
        header_layout.addWidget(self.validate_btn)

        # Export Report button
        self.export_btn = QPushButton("Export Report")
        self.export_btn.setFont(QFont("Consolas", 10))
        self.export_btn.clicked.connect(self.on_export_clicked)
        self.export_btn.setEnabled(False)  # Disabled until validation completes
        header_layout.addWidget(self.export_btn)

        layout.addLayout(header_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setRange(0, 100)  # Percentage-based progress
        layout.addWidget(self.progress_bar)

        # Progress message
        self.progress_label = QLabel("")
        self.progress_label.setFont(QFont("Consolas", 9))
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        # Time estimate label
        self.time_estimate_label = QLabel("")
        self.time_estimate_label.setFont(QFont("Consolas", 9))
        self.time_estimate_label.setStyleSheet("color: #888888;")
        self.time_estimate_label.setVisible(False)
        layout.addWidget(self.time_estimate_label)

        # Create splitter for results
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Results summary group
        summary_group = QGroupBox("Validation Summary")
        summary_layout = QVBoxLayout(summary_group)
        summary_layout.setContentsMargins(8, 8, 8, 8)

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setFont(QFont("Consolas", 9))
        self.summary_text.setMaximumHeight(120)
        self.summary_text.setPlainText("No validation results yet.\n\nClick 'Validate' to start validation.")
        summary_layout.addWidget(self.summary_text)

        splitter.addWidget(summary_group)

        # Differences tree view group
        tree_group = QGroupBox("Differences")
        tree_layout = QVBoxLayout(tree_group)
        tree_layout.setContentsMargins(8, 8, 8, 8)

        self.diff_tree = QTreeWidget()
        self.diff_tree.setFont(QFont("Consolas", 9))
        self.diff_tree.setHeaderLabels(["Description", "Severity", "Category", "Location"])
        self.diff_tree.setAlternatingRowColors(True)
        self.diff_tree.setColumnWidth(0, 400)
        self.diff_tree.setColumnWidth(1, 100)
        self.diff_tree.setColumnWidth(2, 120)
        tree_layout.addWidget(self.diff_tree)

        splitter.addWidget(tree_group)

        # Set initial sizes
        splitter.setSizes([120, 400])
        layout.addWidget(splitter, 1)

    def set_status(self, status: ValidationStatus, message: str = ""):
        """Update the validation status"""
        self.status = status

        if status == ValidationStatus.IDLE:
            self.status_label.setText("Status: Idle")
            self.status_label.setStyleSheet("")
            self.validate_btn.setEnabled(True)
            self.cancel_btn.setVisible(False)
            self.progress_bar.setVisible(False)
            self.progress_label.setVisible(False)
            self.time_estimate_label.setVisible(False)

        elif status == ValidationStatus.RUNNING:
            self.status_label.setText("Status: Running validation...")
            self.status_label.setStyleSheet("color: #FFA500;")
            self.validate_btn.setEnabled(False)
            self.cancel_btn.setVisible(True)
            self.cancel_btn.setEnabled(True)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.progress_label.setVisible(True)
            self.progress_label.setText(message or "Starting...")
            self.time_estimate_label.setVisible(True)
            self.time_estimate_label.setText("Estimating...")

        elif status == ValidationStatus.COMPLETE:
            self.status_label.setText("Status: Complete")
            self.status_label.setStyleSheet("color: #00FF00;")
            self.validate_btn.setEnabled(True)
            self.cancel_btn.setVisible(False)
            self.progress_bar.setVisible(False)
            self.progress_label.setVisible(False)
            self.time_estimate_label.setVisible(False)

        elif status == ValidationStatus.ERROR:
            self.status_label.setText("Status: Error")
            self.status_label.setStyleSheet("color: #FF0000;")
            self.validate_btn.setEnabled(True)
            self.cancel_btn.setVisible(False)
            self.progress_bar.setVisible(False)
            self.progress_label.setVisible(False)
            self.time_estimate_label.setVisible(False)

    def on_settings_clicked(self):
        """Handle settings button click"""
        dialog = ValidationSettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update compiler directory from settings
            settings = dialog.get_settings()
            self.compiler_dir = settings.get("compiler_dir")

    def on_validate_clicked(self):
        """Handle validate button click"""
        # Get file paths from user
        original_scr, _ = QFileDialog.getOpenFileName(
            self,
            "Select Original SCR File",
            "",
            "SCR Files (*.scr *.SCR);;All Files (*)"
        )

        if not original_scr:
            return

        decompiled_source, _ = QFileDialog.getOpenFileName(
            self,
            "Select Decompiled Source File",
            "",
            "C Source Files (*.c);;All Files (*)"
        )

        if not decompiled_source:
            return

        # Get compiler directory from settings or prompt
        if not self.compiler_dir:
            # Try to load from settings first
            from PyQt6.QtCore import QSettings
            settings = QSettings("VCDecompiler", "ValidationSettings")
            self.compiler_dir = settings.value("compiler_dir", "./original-resources/compiler")

            # Verify it exists, otherwise show settings dialog
            if not Path(self.compiler_dir).exists():
                QMessageBox.information(
                    self,
                    "Configure Settings",
                    "Please configure the compiler directory in Settings before validating."
                )
                self.on_settings_clicked()

                # Check again after settings dialog
                if not self.compiler_dir or not Path(self.compiler_dir).exists():
                    return

        self.start_validation(original_scr, decompiled_source)

    def on_cancel_clicked(self):
        """Handle cancel button click"""
        if self.worker and self.worker.isRunning():
            self.cancel_btn.setEnabled(False)
            self.cancel_btn.setText("Cancelling...")
            self.worker.cancel()

    def start_validation(self, original_scr: str, decompiled_source: str):
        """Start validation process"""
        self.original_scr_path = original_scr
        self.decompiled_source_path = decompiled_source

        # Clear previous results
        self.validation_result = None
        self.diff_tree.clear()
        self.summary_text.setPlainText("Starting validation...")

        # Disable export button until new validation completes
        self.export_btn.setEnabled(False)

        # Start validation in background
        self.set_status(ValidationStatus.RUNNING, "Initializing...")

        # Load settings for validation
        from PyQt6.QtCore import QSettings
        settings = QSettings("VCDecompiler", "ValidationSettings")

        # Get settings or use defaults
        include_dirs = settings.value("include_dirs", [])
        timeout = settings.value("timeout", 30, type=int)
        opcode_variant = settings.value("opcode_variant", "auto")
        cache_enabled = settings.value("cache_enabled", True, type=bool)
        cache_dir = settings.value("cache_dir", ".validation_cache")
        cache_max_age_days = settings.value("cache_max_age_days", 0, type=int)
        cache_max_age_seconds = cache_max_age_days * 24 * 60 * 60 if cache_max_age_days > 0 else 0

        self.worker = ValidationWorker(
            original_scr,
            decompiled_source,
            self.compiler_dir,
            include_dirs=include_dirs,
            timeout=timeout,
            opcode_variant=opcode_variant,
            cache_enabled=cache_enabled,
            cache_dir=cache_dir,
            cache_max_age=cache_max_age_seconds,
        )
        self.worker.progress.connect(self.on_progress)
        self.worker.time_estimate.connect(self.on_time_estimate)
        self.worker.finished.connect(self.on_validation_finished)
        self.worker.start()

    def on_progress(self, message: str, percentage: int):
        """Handle progress updates from worker"""
        self.progress_label.setText(message)
        self.progress_bar.setValue(percentage)

    def on_time_estimate(self, estimate: str):
        """Handle time estimate updates from worker"""
        self.time_estimate_label.setText(estimate)

    def on_export_clicked(self):
        """Handle export report button click"""
        if not self.validation_result:
            QMessageBox.warning(
                self,
                "No Results",
                "No validation results to export. Run a validation first."
            )
            return

        # Show save file dialog with format filters
        file_filter = (
            "HTML Report (*.html);;"
            "JSON Report (*.json);;"
            "Text Report (*.txt);;"
            "All Files (*)"
        )

        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export Validation Report",
            "",
            file_filter
        )

        if not file_path:
            return

        try:
            # Determine format from file extension or selected filter
            file_path = Path(file_path)
            ext = file_path.suffix.lower()

            # Auto-detect format from extension
            if ext in [".html", ".htm"]:
                format_type = "html"
            elif ext == ".json":
                format_type = "json"
            elif ext == ".txt":
                format_type = "text"
            else:
                # Try to determine from selected filter
                if "HTML" in selected_filter:
                    format_type = "html"
                    if not ext:
                        file_path = file_path.with_suffix(".html")
                elif "JSON" in selected_filter:
                    format_type = "json"
                    if not ext:
                        file_path = file_path.with_suffix(".json")
                else:
                    format_type = "text"
                    if not ext:
                        file_path = file_path.with_suffix(".txt")

            # Generate and save report using ReportGenerator
            generator = ReportGenerator(use_colors=False)  # No ANSI colors for file output
            generator.save_report(self.validation_result, file_path, format=format_type)

            # Show success notification
            QMessageBox.information(
                self,
                "Export Successful",
                f"Validation report exported successfully to:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to export report:\n{str(e)}"
            )

    def on_validation_finished(self, result):
        """Handle validation completion"""
        # Reset cancel button
        self.cancel_btn.setText("Cancel")
        self.cancel_btn.setEnabled(True)

        if isinstance(result, Exception):
            error_msg = str(result)
            if "cancelled" in error_msg.lower():
                # User cancelled
                self.set_status(ValidationStatus.IDLE)
                self.summary_text.setPlainText("Validation cancelled by user.")
                self.export_btn.setEnabled(False)
            else:
                # Actual error
                self.set_status(ValidationStatus.ERROR)
                QMessageBox.critical(
                    self,
                    "Validation Error",
                    f"Validation failed:\n{error_msg}"
                )
                self.summary_text.setPlainText(f"Validation failed:\n{error_msg}")
                self.export_btn.setEnabled(False)
            return

        self.validation_result = result
        self.set_status(ValidationStatus.COMPLETE)
        self.display_results(result)

        # Enable export button after successful validation
        self.export_btn.setEnabled(True)

    def display_results(self, result: ValidationResult):
        """Display validation results in the UI"""
        # Update summary
        summary_lines = []
        summary_lines.append(f"Verdict: {result.verdict.value.upper()}")
        summary_lines.append("")
        summary_lines.append(f"Original SCR: {Path(self.original_scr_path).name}")
        summary_lines.append(f"Decompiled Source: {Path(self.decompiled_source_path).name}")
        summary_lines.append(f"Recompiled SCR: {Path(result.recompiled_scr or 'N/A').name if result.recompiled_scr else 'N/A'}")
        summary_lines.append("")
        summary_lines.append(f"Compilation: {'Success' if result.compilation_succeeded else 'Failed'}")

        if result.difference_summary:
            summary_lines.append(f"Total Differences: {result.difference_summary.total_count}")
            summary_lines.append(f"  Semantic: {result.difference_summary.semantic_count}")
            summary_lines.append(f"  Cosmetic: {result.difference_summary.cosmetic_count}")
            summary_lines.append(f"  Optimization: {result.difference_summary.optimization_count}")
            summary_lines.append(f"  Unknown: {result.difference_summary.unknown_count}")

        self.summary_text.setPlainText("\n".join(summary_lines))

        # Update differences tree
        self.diff_tree.clear()

        if not result.categorized_differences:
            no_diffs_item = QTreeWidgetItem(["No differences found", "", "", ""])
            self.diff_tree.addTopLevelItem(no_diffs_item)
            return

        # Group by category
        categories = {}
        for diff in result.categorized_differences:
            cat = diff.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(diff)

        # Add to tree
        for category, diffs in categories.items():
            # Category node
            cat_item = QTreeWidgetItem([
                f"{category.value.upper()} ({len(diffs)})",
                "",
                "",
                ""
            ])
            cat_item.setFont(0, QFont("Consolas", 9, QFont.Weight.Bold))
            cat_item.setBackground(0, self._get_category_color(category))
            self.diff_tree.addTopLevelItem(cat_item)

            # Add differences
            for diff in diffs:
                diff_item = QTreeWidgetItem([
                    diff.difference.description,
                    diff.difference.severity.value,
                    diff.category.value,
                    diff.difference.location or ""
                ])

                # Color by severity
                severity_color = self._get_severity_color(diff.difference.severity)
                diff_item.setForeground(1, QBrush(severity_color))

                cat_item.addChild(diff_item)

            cat_item.setExpanded(True)

    def _get_category_color(self, category: DifferenceCategory) -> QBrush:
        """Get background color for category"""
        if category == DifferenceCategory.SEMANTIC:
            return QBrush(QColor(100, 50, 50))  # Dark red
        elif category == DifferenceCategory.COSMETIC:
            return QBrush(QColor(50, 50, 100))  # Dark blue
        elif category == DifferenceCategory.OPTIMIZATION:
            return QBrush(QColor(50, 100, 50))  # Dark green
        else:
            return QBrush(QColor(80, 80, 80))  # Gray

    def _get_severity_color(self, severity: DifferenceSeverity) -> QColor:
        """Get text color for severity"""
        if severity == DifferenceSeverity.CRITICAL:
            return QColor(255, 0, 0)  # Red
        elif severity == DifferenceSeverity.MAJOR:
            return QColor(255, 165, 0)  # Orange
        elif severity == DifferenceSeverity.MINOR:
            return QColor(255, 255, 0)  # Yellow
        else:
            return QColor(0, 255, 255)  # Cyan

    def get_validation_result(self) -> Optional[ValidationResult]:
        """Get the current validation result"""
        return self.validation_result
