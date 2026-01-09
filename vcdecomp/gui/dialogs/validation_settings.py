"""
Validation settings dialog for configuring validation options.

Allows users to configure:
- Compiler executable paths
- Custom header file locations
- Comparison settings
- Cache settings
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    from PyQt6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
        QGroupBox, QLineEdit, QPushButton, QLabel,
        QSpinBox, QCheckBox, QComboBox, QListWidget,
        QFileDialog, QMessageBox, QDialogButtonBox,
        QTabWidget, QWidget
    )
    from PyQt6.QtCore import Qt, QSettings
    from PyQt6.QtGui import QFont
except ImportError:
    print("PyQt6 not installed. Install with: pip install PyQt6")
    sys.exit(1)


class ValidationSettingsDialog(QDialog):
    """
    Dialog for configuring validation settings.

    Settings are persisted across sessions using QSettings.
    All settings are validated before being accepted.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Validation Settings")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        # Settings storage
        self.settings = QSettings("VCDecompiler", "ValidationSettings")

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Create tab widget for organized settings
        tabs = QTabWidget()

        # Tab 1: Compiler Settings
        compiler_tab = self._create_compiler_tab()
        tabs.addTab(compiler_tab, "Compiler")

        # Tab 2: Headers & Includes
        headers_tab = self._create_headers_tab()
        tabs.addTab(headers_tab, "Headers")

        # Tab 3: Comparison Settings
        comparison_tab = self._create_comparison_tab()
        tabs.addTab(comparison_tab, "Comparison")

        # Tab 4: Cache Settings
        cache_tab = self._create_cache_tab()
        tabs.addTab(cache_tab, "Cache")

        layout.addWidget(tabs)

        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.RestoreDefaults
        )
        button_box.accepted.connect(self.accept_settings)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(
            self.restore_defaults
        )

        layout.addWidget(button_box)

    def _create_compiler_tab(self) -> QWidget:
        """Create the compiler settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Compiler directory group
        compiler_group = QGroupBox("Compiler Directory")
        compiler_layout = QVBoxLayout(compiler_group)

        desc_label = QLabel(
            "Directory containing SCMP.exe, SPP.exe, SCC.exe, and SASM.exe.\n"
            "Usually: original-resources/compiler/"
        )
        desc_label.setFont(QFont("Consolas", 9))
        desc_label.setStyleSheet("color: #888888;")
        desc_label.setWordWrap(True)
        compiler_layout.addWidget(desc_label)

        compiler_path_layout = QHBoxLayout()
        self.compiler_dir_edit = QLineEdit()
        self.compiler_dir_edit.setFont(QFont("Consolas", 9))
        self.compiler_dir_edit.setPlaceholderText("Path to compiler directory...")
        compiler_path_layout.addWidget(self.compiler_dir_edit)

        browse_btn = QPushButton("Browse...")
        browse_btn.setFont(QFont("Consolas", 9))
        browse_btn.clicked.connect(self.browse_compiler_dir)
        compiler_path_layout.addWidget(browse_btn)

        compiler_layout.addLayout(compiler_path_layout)
        layout.addWidget(compiler_group)

        # Timeout settings group
        timeout_group = QGroupBox("Compilation Timeout")
        timeout_layout = QFormLayout(timeout_group)
        timeout_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        self.timeout_spin = QSpinBox()
        self.timeout_spin.setFont(QFont("Consolas", 9))
        self.timeout_spin.setMinimum(5)
        self.timeout_spin.setMaximum(300)
        self.timeout_spin.setSuffix(" seconds")
        self.timeout_spin.setValue(30)
        timeout_layout.addRow("Timeout:", self.timeout_spin)

        timeout_desc = QLabel(
            "Maximum time to wait for compilation to complete.\n"
            "Increase if compiling large scripts."
        )
        timeout_desc.setFont(QFont("Consolas", 9))
        timeout_desc.setStyleSheet("color: #888888;")
        timeout_desc.setWordWrap(True)
        timeout_layout.addRow("", timeout_desc)

        layout.addWidget(timeout_group)

        layout.addStretch()
        return widget

    def _create_headers_tab(self) -> QWidget:
        """Create the headers settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Include directories group
        include_group = QGroupBox("Include Directories")
        include_layout = QVBoxLayout(include_group)

        desc_label = QLabel(
            "Additional directories to search for header files (.h) and include files (.inc).\n"
            "The compiler will search these directories when processing #include directives."
        )
        desc_label.setFont(QFont("Consolas", 9))
        desc_label.setStyleSheet("color: #888888;")
        desc_label.setWordWrap(True)
        include_layout.addWidget(desc_label)

        # List widget for include directories
        self.include_dirs_list = QListWidget()
        self.include_dirs_list.setFont(QFont("Consolas", 9))
        include_layout.addWidget(self.include_dirs_list)

        # Buttons for managing include directories
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("Add Directory...")
        add_btn.setFont(QFont("Consolas", 9))
        add_btn.clicked.connect(self.add_include_dir)
        btn_layout.addWidget(add_btn)

        remove_btn = QPushButton("Remove")
        remove_btn.setFont(QFont("Consolas", 9))
        remove_btn.clicked.connect(self.remove_include_dir)
        btn_layout.addWidget(remove_btn)

        clear_btn = QPushButton("Clear All")
        clear_btn.setFont(QFont("Consolas", 9))
        clear_btn.clicked.connect(self.clear_include_dirs)
        btn_layout.addWidget(clear_btn)

        btn_layout.addStretch()
        include_layout.addLayout(btn_layout)

        layout.addWidget(include_group)

        layout.addStretch()
        return widget

    def _create_comparison_tab(self) -> QWidget:
        """Create the comparison settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Opcode variant group
        variant_group = QGroupBox("Opcode Variant")
        variant_layout = QFormLayout(variant_group)
        variant_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        self.opcode_variant_combo = QComboBox()
        self.opcode_variant_combo.setFont(QFont("Consolas", 9))
        self.opcode_variant_combo.addItems(["auto", "v1.60", "v1.00"])
        variant_layout.addRow("Opcode Variant:", self.opcode_variant_combo)

        variant_desc = QLabel(
            "SCR opcode variant to use for comparison.\n"
            "'auto' - Automatically detect from file\n"
            "'v1.60' - Vietcong 1.60 (most common)\n"
            "'v1.00' - Vietcong 1.00 (original release)"
        )
        variant_desc.setFont(QFont("Consolas", 9))
        variant_desc.setStyleSheet("color: #888888;")
        variant_desc.setWordWrap(True)
        variant_layout.addRow("", variant_desc)

        layout.addWidget(variant_group)

        # Difference filtering group
        filter_group = QGroupBox("Difference Filtering")
        filter_layout = QVBoxLayout(filter_group)

        filter_desc = QLabel(
            "Configure which differences to report.\n"
            "Note: All differences are still detected, these settings only affect reporting."
        )
        filter_desc.setFont(QFont("Consolas", 9))
        filter_desc.setStyleSheet("color: #888888;")
        filter_desc.setWordWrap(True)
        filter_layout.addWidget(filter_desc)

        self.show_info_check = QCheckBox("Show INFO level differences (informational, no impact)")
        self.show_info_check.setFont(QFont("Consolas", 9))
        self.show_info_check.setChecked(True)
        filter_layout.addWidget(self.show_info_check)

        self.show_minor_check = QCheckBox("Show MINOR level differences (likely cosmetic)")
        self.show_minor_check.setFont(QFont("Consolas", 9))
        self.show_minor_check.setChecked(True)
        filter_layout.addWidget(self.show_minor_check)

        self.show_cosmetic_check = QCheckBox("Show COSMETIC differences (reordering, alignment)")
        self.show_cosmetic_check.setFont(QFont("Consolas", 9))
        self.show_cosmetic_check.setChecked(True)
        filter_layout.addWidget(self.show_cosmetic_check)

        layout.addWidget(filter_group)

        layout.addStretch()
        return widget

    def _create_cache_tab(self) -> QWidget:
        """Create the cache settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Cache enable/disable group
        cache_group = QGroupBox("Cache Settings")
        cache_layout = QVBoxLayout(cache_group)

        self.cache_enabled_check = QCheckBox("Enable validation result caching")
        self.cache_enabled_check.setFont(QFont("Consolas", 9))
        self.cache_enabled_check.setChecked(True)
        self.cache_enabled_check.toggled.connect(self.on_cache_enabled_toggled)
        cache_layout.addWidget(self.cache_enabled_check)

        cache_desc = QLabel(
            "Caching stores validation results to avoid recompiling unchanged code.\n"
            "Cached results are invalidated automatically when source code changes."
        )
        cache_desc.setFont(QFont("Consolas", 9))
        cache_desc.setStyleSheet("color: #888888;")
        cache_desc.setWordWrap(True)
        cache_layout.addWidget(cache_desc)

        layout.addWidget(cache_group)

        # Cache directory group
        cache_dir_group = QGroupBox("Cache Directory")
        cache_dir_layout = QVBoxLayout(cache_dir_group)

        cache_path_layout = QHBoxLayout()
        self.cache_dir_edit = QLineEdit()
        self.cache_dir_edit.setFont(QFont("Consolas", 9))
        self.cache_dir_edit.setPlaceholderText(".validation_cache")
        cache_path_layout.addWidget(self.cache_dir_edit)

        cache_browse_btn = QPushButton("Browse...")
        cache_browse_btn.setFont(QFont("Consolas", 9))
        cache_browse_btn.clicked.connect(self.browse_cache_dir)
        cache_path_layout.addWidget(cache_browse_btn)

        cache_dir_layout.addLayout(cache_path_layout)
        layout.addWidget(cache_dir_group)

        # Cache expiration group
        expiration_group = QGroupBox("Cache Expiration")
        expiration_layout = QFormLayout(expiration_group)
        expiration_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        self.cache_max_age_spin = QSpinBox()
        self.cache_max_age_spin.setFont(QFont("Consolas", 9))
        self.cache_max_age_spin.setMinimum(0)
        self.cache_max_age_spin.setMaximum(365)
        self.cache_max_age_spin.setSuffix(" days")
        self.cache_max_age_spin.setSpecialValueText("No expiration")
        self.cache_max_age_spin.setValue(0)
        expiration_layout.addRow("Max Age:", self.cache_max_age_spin)

        expiration_desc = QLabel(
            "Maximum age of cache entries. Set to 0 for no expiration.\n"
            "Expired entries are automatically removed."
        )
        expiration_desc.setFont(QFont("Consolas", 9))
        expiration_desc.setStyleSheet("color: #888888;")
        expiration_desc.setWordWrap(True)
        expiration_layout.addRow("", expiration_desc)

        layout.addWidget(expiration_group)

        # Cache management group
        management_group = QGroupBox("Cache Management")
        management_layout = QVBoxLayout(management_group)

        clear_cache_btn = QPushButton("Clear Cache Now")
        clear_cache_btn.setFont(QFont("Consolas", 9))
        clear_cache_btn.clicked.connect(self.clear_cache)
        management_layout.addWidget(clear_cache_btn)

        layout.addWidget(management_group)

        layout.addStretch()
        return widget

    def browse_compiler_dir(self):
        """Browse for compiler directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Compiler Directory",
            self.compiler_dir_edit.text() or ""
        )
        if dir_path:
            self.compiler_dir_edit.setText(dir_path)

    def browse_cache_dir(self):
        """Browse for cache directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Cache Directory",
            self.cache_dir_edit.text() or ""
        )
        if dir_path:
            self.cache_dir_edit.setText(dir_path)

    def add_include_dir(self):
        """Add an include directory to the list"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Include Directory",
            ""
        )
        if dir_path:
            self.include_dirs_list.addItem(dir_path)

    def remove_include_dir(self):
        """Remove selected include directory"""
        current_item = self.include_dirs_list.currentItem()
        if current_item:
            self.include_dirs_list.takeItem(self.include_dirs_list.row(current_item))

    def clear_include_dirs(self):
        """Clear all include directories"""
        self.include_dirs_list.clear()

    def on_cache_enabled_toggled(self, checked: bool):
        """Handle cache enabled checkbox toggle"""
        # Enable/disable cache-related widgets
        self.cache_dir_edit.setEnabled(checked)
        self.cache_max_age_spin.setEnabled(checked)

    def clear_cache(self):
        """Clear the validation cache"""
        reply = QMessageBox.question(
            self,
            "Clear Cache",
            "Are you sure you want to clear the validation cache?\n"
            "This will remove all cached validation results.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                cache_dir = Path(self.cache_dir_edit.text() or ".validation_cache")
                if cache_dir.exists():
                    import shutil
                    shutil.rmtree(cache_dir)
                    QMessageBox.information(
                        self,
                        "Cache Cleared",
                        f"Validation cache cleared successfully.\n{cache_dir}"
                    )
                else:
                    QMessageBox.information(
                        self,
                        "Cache Not Found",
                        f"Cache directory does not exist.\n{cache_dir}"
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to clear cache:\n{str(e)}"
                )

    def validate_settings(self) -> tuple[bool, str]:
        """
        Validate all settings before accepting.

        Returns:
            (valid, error_message) tuple
        """
        # Validate compiler directory
        compiler_dir = self.compiler_dir_edit.text().strip()
        if not compiler_dir:
            return False, "Compiler directory is required."

        compiler_path = Path(compiler_dir)
        if not compiler_path.exists():
            return False, f"Compiler directory does not exist:\n{compiler_dir}"

        # Check for required executables
        required_exes = ["SCMP.exe", "SPP.exe", "SCC.exe", "SASM.exe"]
        missing_exes = []
        for exe in required_exes:
            if not (compiler_path / exe).exists():
                missing_exes.append(exe)

        if missing_exes:
            return False, (
                f"Missing compiler executables in {compiler_dir}:\n" +
                "\n".join(f"  - {exe}" for exe in missing_exes)
            )

        # Validate include directories
        for i in range(self.include_dirs_list.count()):
            include_dir = self.include_dirs_list.item(i).text()
            if not Path(include_dir).exists():
                return False, f"Include directory does not exist:\n{include_dir}"

        # All validations passed
        return True, ""

    def accept_settings(self):
        """Validate and accept settings"""
        valid, error_msg = self.validate_settings()
        if not valid:
            QMessageBox.warning(
                self,
                "Invalid Settings",
                error_msg
            )
            return

        # Save settings
        self.save_settings()
        self.accept()

    def save_settings(self):
        """Save settings to persistent storage"""
        # Compiler settings
        self.settings.setValue("compiler_dir", self.compiler_dir_edit.text())
        self.settings.setValue("timeout", self.timeout_spin.value())

        # Header settings
        include_dirs = []
        for i in range(self.include_dirs_list.count()):
            include_dirs.append(self.include_dirs_list.item(i).text())
        self.settings.setValue("include_dirs", include_dirs)

        # Comparison settings
        self.settings.setValue("opcode_variant", self.opcode_variant_combo.currentText())
        self.settings.setValue("show_info", self.show_info_check.isChecked())
        self.settings.setValue("show_minor", self.show_minor_check.isChecked())
        self.settings.setValue("show_cosmetic", self.show_cosmetic_check.isChecked())

        # Cache settings
        self.settings.setValue("cache_enabled", self.cache_enabled_check.isChecked())
        self.settings.setValue("cache_dir", self.cache_dir_edit.text())
        self.settings.setValue("cache_max_age_days", self.cache_max_age_spin.value())

        self.settings.sync()

    def load_settings(self):
        """Load settings from persistent storage"""
        # Compiler settings
        self.compiler_dir_edit.setText(
            self.settings.value("compiler_dir", "./original-resources/compiler")
        )
        self.timeout_spin.setValue(
            int(self.settings.value("timeout", 30))
        )

        # Header settings
        include_dirs = self.settings.value("include_dirs", [])
        if include_dirs:
            for dir_path in include_dirs:
                self.include_dirs_list.addItem(dir_path)

        # Comparison settings
        variant = self.settings.value("opcode_variant", "auto")
        index = self.opcode_variant_combo.findText(variant)
        if index >= 0:
            self.opcode_variant_combo.setCurrentIndex(index)

        self.show_info_check.setChecked(
            self.settings.value("show_info", True, type=bool)
        )
        self.show_minor_check.setChecked(
            self.settings.value("show_minor", True, type=bool)
        )
        self.show_cosmetic_check.setChecked(
            self.settings.value("show_cosmetic", True, type=bool)
        )

        # Cache settings
        cache_enabled = self.settings.value("cache_enabled", True, type=bool)
        self.cache_enabled_check.setChecked(cache_enabled)

        self.cache_dir_edit.setText(
            self.settings.value("cache_dir", ".validation_cache")
        )
        self.cache_max_age_spin.setValue(
            int(self.settings.value("cache_max_age_days", 0))
        )

        # Update widget states
        self.on_cache_enabled_toggled(cache_enabled)

    def restore_defaults(self):
        """Restore default settings"""
        reply = QMessageBox.question(
            self,
            "Restore Defaults",
            "Are you sure you want to restore default settings?\n"
            "This will reset all validation settings to their defaults.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Clear all settings
            self.settings.clear()

            # Reload defaults
            self.compiler_dir_edit.setText("./original-resources/compiler")
            self.timeout_spin.setValue(30)
            self.include_dirs_list.clear()
            self.opcode_variant_combo.setCurrentText("auto")
            self.show_info_check.setChecked(True)
            self.show_minor_check.setChecked(True)
            self.show_cosmetic_check.setChecked(True)
            self.cache_enabled_check.setChecked(True)
            self.cache_dir_edit.setText(".validation_cache")
            self.cache_max_age_spin.setValue(0)

            QMessageBox.information(
                self,
                "Defaults Restored",
                "Default settings have been restored."
            )

    def get_settings(self) -> Dict:
        """
        Get current settings as a dictionary.

        Returns:
            Dictionary with all settings
        """
        include_dirs = []
        for i in range(self.include_dirs_list.count()):
            include_dirs.append(self.include_dirs_list.item(i).text())

        # Convert cache max age from days to seconds
        cache_max_age_days = self.cache_max_age_spin.value()
        cache_max_age_seconds = cache_max_age_days * 24 * 60 * 60 if cache_max_age_days > 0 else 0

        return {
            "compiler_dir": self.compiler_dir_edit.text(),
            "include_dirs": include_dirs,
            "timeout": self.timeout_spin.value(),
            "opcode_variant": self.opcode_variant_combo.currentText(),
            "cache_enabled": self.cache_enabled_check.isChecked(),
            "cache_dir": self.cache_dir_edit.text() or ".validation_cache",
            "cache_max_age": cache_max_age_seconds,
            "show_info": self.show_info_check.isChecked(),
            "show_minor": self.show_minor_check.isChecked(),
            "show_cosmetic": self.show_cosmetic_check.isChecked(),
        }
