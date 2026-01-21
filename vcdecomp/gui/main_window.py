"""
Main window for VC Script Decompiler GUI
"""

import sys
import tempfile
from pathlib import Path
from typing import Optional

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QSplitter, QTextEdit, QPlainTextEdit, QTabWidget, QMenuBar,
        QMenu, QFileDialog, QStatusBar, QLabel, QListWidget, QListWidgetItem,
        QDockWidget, QMessageBox, QComboBox, QStyle, QDialog
    )
    from PyQt6.QtGui import QAction, QActionGroup, QFont, QColor, QTextCharFormat, QSyntaxHighlighter
    from PyQt6.QtCore import Qt, QRegularExpression, QSettings
except ImportError:
    print("PyQt6 not installed. Install with: pip install PyQt6")
    sys.exit(1)

from ..core.loader import SCRFile
from ..core.disasm import Disassembler
from ..core.ir.ssa import build_ssa, build_ssa_all_blocks, build_ssa_incremental
from ..core.ir.expr import format_block_expressions
from ..core.ir.structure import format_structured_function_named
from .views import ValidationPanel
from .views.error_analysis_view import ErrorAnalysisPanel
from .dialogs import ValidationSettingsDialog


class SyntaxHighlighter(QSyntaxHighlighter):
    """Simple syntax highlighter for disassembly"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Keywords (mnemonics)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))  # Blue
        keyword_format.setFontWeight(QFont.Weight.Bold)

        keywords = [
            'CALL', 'RET', 'JMP', 'JZ', 'JNZ', 'XCALL',
            'LCP', 'GCP', 'LLD', 'GLD', 'LADR', 'GADR', 'DADR',
            'ADD', 'SUB', 'MUL', 'DIV', 'INC', 'DEC', 'NEG',
            'FADD', 'FSUB', 'FMUL', 'FDIV',
            'EQU', 'NEQ', 'LES', 'LEQ', 'GRE', 'GEQ',
            'AND', 'OR', 'NOT', 'ASP', 'SSP', 'DCP', 'ASGN', 'PNT'
        ]

        for word in keywords:
            pattern = QRegularExpression(rf'\b{word}\b')
            self.highlighting_rules.append((pattern, keyword_format))

        # Labels
        label_format = QTextCharFormat()
        label_format.setForeground(QColor("#DCDCAA"))  # Yellow
        pattern = QRegularExpression(r'^[\w_]+:')
        self.highlighting_rules.append((pattern, label_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))  # Green
        pattern = QRegularExpression(r';.*$')
        self.highlighting_rules.append((pattern, comment_format))

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))  # Light green
        pattern = QRegularExpression(r'\b-?\d+\b')
        self.highlighting_rules.append((pattern, number_format))

        # Hex numbers
        pattern = QRegularExpression(r'\b0x[0-9A-Fa-f]+\b')
        self.highlighting_rules.append((pattern, number_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))  # Orange
        pattern = QRegularExpression(r'"[^"]*"')
        self.highlighting_rules.append((pattern, string_format))

    def highlightBlock(self, text: str):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class HexView(QPlainTextEdit):
    """Hex dump view"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 10))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

    def set_data(self, data: bytes):
        """Display hex dump of data"""
        lines = []
        for i in range(0, len(data), 16):
            # Address
            line = f"{i:08x}  "

            # Hex bytes
            hex_part = ""
            ascii_part = ""
            for j in range(16):
                if i + j < len(data):
                    b = data[i + j]
                    hex_part += f"{b:02x} "
                    ascii_part += chr(b) if 32 <= b < 127 else "."
                else:
                    hex_part += "   "
                    ascii_part += " "

                if j == 7:
                    hex_part += " "

            lines.append(f"{line}{hex_part} |{ascii_part}|")

        self.setPlainText("\n".join(lines))


class DisassemblyView(QPlainTextEdit):
    """Disassembly view with syntax highlighting"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 10))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.highlighter = SyntaxHighlighter(self.document())

    def set_disassembly(self, text: str):
        """Display disassembly"""
        self.setPlainText(text)


class FunctionListWidget(QListWidget):
    """List of functions/labels"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 9))

    def set_functions(self, functions: dict):
        """Set list of functions"""
        self.clear()
        for addr, name in sorted(functions.items()):
            item = QListWidgetItem(f"[{addr:04d}] {name}")
            item.setData(Qt.ItemDataRole.UserRole, addr)
            self.addItem(item)


class StringListWidget(QListWidget):
    """List of strings from data segment"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 9))

    def set_strings(self, strings: dict):
        """Set list of strings"""
        self.clear()
        for offset, s in sorted(strings.items()):
            escaped = s.replace('\n', '\\n').replace('\r', '\\r')
            if len(escaped) > 50:
                escaped = escaped[:47] + "..."
            item = QListWidgetItem(f"[{offset:4d}] \"{escaped}\"")
            item.setData(Qt.ItemDataRole.UserRole, offset)
            self.addItem(item)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.scr: Optional[SCRFile] = None
        self.disasm: Optional[Disassembler] = None
        self.variant: str = "auto"
        self.ssa_func = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("VC Script Decompiler")
        self.setGeometry(100, 100, 1400, 900)

        # Create central widget with tabs
        self.central_tabs = QTabWidget()
        self.setCentralWidget(self.central_tabs)

        # Hex view tab
        self.hex_view = HexView()
        self.central_tabs.addTab(self.hex_view, "Hex")

        # Disassembly view tab
        self.disasm_view = DisassemblyView()
        self.central_tabs.addTab(self.disasm_view, "Disassembly")

        # Decompilation view tab
        self.decomp_view = QPlainTextEdit()
        self.decomp_view.setReadOnly(True)
        self.decomp_view.setFont(QFont("Consolas", 10))
        self.decomp_view.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.central_tabs.addTab(self.decomp_view, "Decompilation")

        # Info view tab
        self.info_view = QPlainTextEdit()
        self.info_view.setReadOnly(True)
        self.info_view.setFont(QFont("Consolas", 10))
        self.central_tabs.addTab(self.info_view, "Info")

        # Expressions view tab
        self.expr_tab = QWidget()
        expr_layout = QVBoxLayout(self.expr_tab)
        expr_layout.setContentsMargins(4, 4, 4, 4)
        self.expr_block_selector = QComboBox()
        self.expr_block_selector.currentIndexChanged.connect(self.on_expr_block_changed)
        expr_layout.addWidget(self.expr_block_selector)
        self.expr_view = QPlainTextEdit()
        self.expr_view.setReadOnly(True)
        self.expr_view.setFont(QFont("Consolas", 10))
        self.expr_view.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        expr_layout.addWidget(self.expr_view, 1)
        self.central_tabs.addTab(self.expr_tab, "Expressions")

        # Dock widgets (create before menus so View menu can reference them)
        # Functions dock
        self.func_dock = QDockWidget("Functions", self)
        self.func_list = FunctionListWidget()
        self.func_dock.setWidget(self.func_list)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.func_dock)

        # Strings dock
        self.strings_dock = QDockWidget("Strings", self)
        self.strings_list = StringListWidget()
        self.strings_dock.setWidget(self.strings_list)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.strings_dock)

        # XFN dock
        self.xfn_dock = QDockWidget("External Functions", self)
        self.xfn_list = QListWidget()
        self.xfn_list.setFont(QFont("Consolas", 9))
        self.xfn_dock.setWidget(self.xfn_list)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.xfn_dock)

        # Validation dock
        self.validation_dock = QDockWidget("Validation", self)
        self.validation_panel = ValidationPanel()
        self.validation_dock.setWidget(self.validation_panel)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.validation_dock)

        # Error Analysis dock
        self.error_analysis_dock = QDockWidget("Error Analysis", self)
        self.error_analysis_panel = ErrorAnalysisPanel()
        self.error_analysis_dock.setWidget(self.error_analysis_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.error_analysis_dock)
        # Initially hidden (user opens when needed)
        self.error_analysis_dock.hide()

        # Create menus (after docks so View menu can reference them)
        self.create_menus()

        # Create toolbar
        self.toolbar = self.addToolBar("Main")
        self.toolbar.addAction(self.open_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.validate_action)

        # Set icons for toolbar actions
        self.open_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self.validate_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_menus(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        self.open_action = QAction("&Open...", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)
        file_menu.addAction(self.open_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        view_menu.addAction(self.func_dock.toggleViewAction())
        view_menu.addAction(self.strings_dock.toggleViewAction())
        view_menu.addAction(self.xfn_dock.toggleViewAction())
        view_menu.addAction(self.validation_dock.toggleViewAction())
        view_menu.addAction(self.error_analysis_dock.toggleViewAction())

        # Options menu
        options_menu = menubar.addMenu("&Options")
        variant_menu = options_menu.addMenu("Opcode &Variant")
        self.variant_group = QActionGroup(self)
        self.variant_group.setExclusive(True)
        for name in ("auto", "runtime", "compiler"):
            action = QAction(name.capitalize(), self, checkable=True)
            if name == self.variant:
                action.setChecked(True)
            action.triggered.connect(lambda checked, value=name: self.set_variant(value) if checked else None)
            self.variant_group.addAction(action)
            variant_menu.addAction(action)

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")

        self.validate_action = QAction("&Validate Current Script", self)
        self.validate_action.setShortcut("Ctrl+Shift+V")
        self.validate_action.triggered.connect(self.validate_current_script)
        tools_menu.addAction(self.validate_action)

        tools_menu.addSeparator()

        settings_action = QAction("&Settings...", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self.show_validation_settings)
        tools_menu.addAction(settings_action)

    def set_variant(self, variant: str):
        """Set opcode resolver variant"""
        self.variant = variant
        self.statusBar().showMessage(f"Opcode variant set to {variant}")

    def show_validation_settings(self):
        """Show validation settings dialog"""
        dialog = ValidationSettingsDialog(self)

        # Dialog loads its own settings internally via QSettings
        # (see validation_settings.py line 45: self.settings = QSettings("VCDecompiler", "ValidationSettings"))
        # Dialog also saves automatically when user clicks OK (line 473: save_settings())

        # Just show the dialog - no need to manually load/save
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.statusBar().showMessage("Validation settings saved", 3000)

    def validate_current_script(self):
        """Validate the currently loaded script"""
        # Check if a script is loaded
        if self.scr is None:
            QMessageBox.warning(
                self,
                "No Script Loaded",
                "No script loaded. Open a .scr file first."
            )
            return

        # Check if compiler directory is configured
        # Read from same QSettings namespace that ValidationPanel uses
        settings = QSettings("VCDecompiler", "ValidationSettings")
        compiler_dir = settings.value("compiler_dir", "")

        if not compiler_dir or not Path(compiler_dir).exists():
            result = QMessageBox.question(
                self,
                "Configure Compiler",
                "Compiler directory not configured. Would you like to configure validation settings now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )

            if result == QMessageBox.StandardButton.Yes:
                self.show_validation_settings()

                # Check again after settings dialog
                settings = QSettings("VCDecompiler", "ValidationSettings")
                compiler_dir = settings.value("compiler_dir", "")
                if not compiler_dir or not Path(compiler_dir).exists():
                    QMessageBox.warning(self, "Validation Cancelled", "Cannot validate without valid compiler directory.")
                    return
            else:
                return

        # Get decompiled text from the decompilation view
        decompiled_text = self.decomp_view.toPlainText()

        # Create temp directory for validation
        temp_dir = Path(tempfile.gettempdir()) / "vcdecomp_validation"
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Save decompiled code to temp file
        temp_source = temp_dir / f"{Path(self.scr.filename).stem}_decompiled.c"
        temp_source.write_text(decompiled_text, encoding='utf-8')

        # Show validation dock
        self.validation_dock.show()

        # Switch to validation dock (raise it if tabbed with other docks)
        self.validation_dock.raise_()

        # Start validation
        self.validation_panel.start_validation(
            original_scr=self.scr.filename,
            decompiled_source=str(temp_source)
        )

    def open_file(self, filename: str = None):
        """Open SCR file"""
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Open SCR File",
                "",
                "SCR Files (*.scr *.SCR);;All Files (*)"
            )

        if not filename:
            return

        try:
            self.load_file(filename)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{e}")

    def load_file(self, filename: str):
        """Load and parse SCR file"""
        self.scr = SCRFile.load(filename, variant=self.variant)
        self.disasm = Disassembler(self.scr)
        self.ssa_func = build_ssa(self.scr)

        # Update views
        self.setWindowTitle(f"VC Script Decompiler - {Path(filename).name}")

        # Hex view
        self.hex_view.set_data(self.scr.raw_data)

        # Disassembly view
        self.disasm_view.set_disassembly(self.disasm.to_string())

        # Decompilation view - use build_ssa_incremental for better quality
        # (build_ssa_all_blocks has issues with cross-function PHI dependencies)
        try:
            ssa_func, heritage_metadata = build_ssa_incremental(self.scr, return_metadata=True)
            # Use v2 boundary detection for more accurate function splitting
            # (v1 sometimes combines multiple functions into one mega-function)
            func_bounds = self.disasm.get_function_boundaries_v2()

            decomp_lines = [f"// Structured decompilation of {Path(filename).name}"]
            decomp_lines.append(f"// Functions: {len(func_bounds)}")
            decomp_lines.append("")

            for func_name, (func_start, func_end) in sorted(func_bounds.items(), key=lambda x: x[1][0]):
                text = format_structured_function_named(
                    ssa_func, func_name, func_start, func_end,
                    function_bounds=func_bounds,
                    heritage_metadata=heritage_metadata
                )
                decomp_lines.append(text)
                decomp_lines.append("")

            self.decomp_view.setPlainText("\n".join(decomp_lines))
        except Exception as e:
            self.decomp_view.setPlainText(f"// Decompilation error: {e}")

        # Info view
        self.info_view.setPlainText(self.scr.info())

        # Functions list
        self.func_list.set_functions(self.disasm.functions)

        # Strings list
        self.strings_list.set_strings(self.scr.data_segment.strings)

        # XFN list
        self.xfn_list.clear()
        for entry in self.scr.xfn_table.entries:
            self.xfn_list.addItem(f"[{entry.index:3d}] {entry.name}")

        # Expressions view
        self.populate_expression_blocks()

        # Status
        self.statusBar().showMessage(
            f"Loaded ({self.scr.opcode_resolver.name}{' forced' if self.scr.opcode_variant_forced else ''}): "
            f"{self.scr.code_segment.code_count} instructions, "
            f"{self.scr.xfn_table.xfn_count} XFN, "
            f"{len(self.scr.data_segment.strings)} strings"
        )

        # Switch to disassembly tab
        self.central_tabs.setCurrentWidget(self.disasm_view)

    def populate_expression_blocks(self):
        if not self.ssa_func:
            self.expr_block_selector.clear()
            self.expr_view.setPlainText("No expressions available.")
            return

        self.expr_block_selector.blockSignals(True)
        self.expr_block_selector.clear()
        for block_id in sorted(self.ssa_func.instructions.keys()):
            self.expr_block_selector.addItem(f"Block {block_id}", block_id)
        self.expr_block_selector.blockSignals(False)

        if self.expr_block_selector.count() > 0:
            self.expr_block_selector.setCurrentIndex(0)
            self.update_expression_view(self.expr_block_selector.currentData())
        else:
            self.expr_view.setPlainText("No expressions available.")

    def on_expr_block_changed(self, index: int):
        block_id = self.expr_block_selector.itemData(index)
        if block_id is None:
            self.expr_view.setPlainText("No block selected.")
            return
        self.update_expression_view(block_id)

    def update_expression_view(self, block_id: int):
        if not self.ssa_func:
            self.expr_view.setPlainText("No expressions available.")
            return

        expressions = format_block_expressions(self.ssa_func, block_id)
        lines = [f"// Block {block_id}"]
        if not expressions:
            lines.append("// (no instructions)")
        else:
            for expr in expressions:
                addr = expr.address
                addr_str = f"{addr:04d}" if addr >= 0 else f"phi{abs(addr)}"
                lines.append(f"{addr_str}: {expr.text}")
        self.expr_view.setPlainText("\n".join(lines))


def run_gui(filename: str = None):
    """Run the GUI application"""
    app = QApplication(sys.argv)

    # Set dark theme (optional)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    if filename:
        window.load_file(filename)

    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
