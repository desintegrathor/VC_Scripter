"""
Diff viewer widget for side-by-side comparison of assembly and decompiled code.

Provides visual comparison capabilities for debugging decompiler output by showing:
1. Assembly vs C source comparison with syntax highlighting
2. Bytecode instruction-level differences
3. Line-by-line highlighting of changed/added/removed content
"""

import sys
from pathlib import Path
from typing import Optional, Tuple, List
from difflib import unified_diff, SequenceMatcher

try:
    from PyQt6.QtWidgets import (
        QSplitter, QTextEdit, QWidget, QVBoxLayout,
        QLabel, QTabWidget, QGroupBox
    )
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QTextCharFormat, QTextCursor, QColor, QFont, QBrush
except ImportError:
    print("PyQt6 not installed. Install with: pip install PyQt6")
    sys.exit(1)

try:
    from ...validation.bytecode_compare import BytecodeComparator, ComparisonResult
except ImportError:
    # For standalone testing
    BytecodeComparator = None
    ComparisonResult = None


class DiffViewerWidget(QWidget):
    """
    Side-by-side diff viewer for comparing assembly and decompiled C code.

    Features:
    - Two-pane splitter view (original left, decompiled right)
    - Syntax highlighting for differences
    - Monospace font for proper alignment
    - Tab support for multiple comparison types
    - Bytecode instruction-level comparison

    Usage:
        viewer = DiffViewerWidget()
        viewer.show_diff(original_asm, decompiled_c)
        viewer.show_bytecode_diff(original_scr_path, recompiled_scr_path)
    """

    def __init__(self, parent=None):
        """
        Initialize the diff viewer widget.

        Args:
            parent: Optional parent widget
        """
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create tab widget for different comparison types
        self.tabs = QTabWidget()

        # Tab 1: Assembly vs C comparison
        self.text_diff_tab = self._create_text_diff_tab()
        self.tabs.addTab(self.text_diff_tab, "Assembly vs C")

        # Tab 2: Bytecode instruction comparison
        self.bytecode_diff_tab = self._create_bytecode_diff_tab()
        self.tabs.addTab(self.bytecode_diff_tab, "Bytecode Instructions")

        layout.addWidget(self.tabs)

        # Show placeholder by default
        self._show_placeholder()

    def _create_text_diff_tab(self) -> QWidget:
        """
        Create the text diff comparison tab.

        Returns:
            Widget containing side-by-side text editors
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create horizontal splitter for side-by-side view
        self.text_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left pane: Original assembly
        left_group = QGroupBox("Original Assembly")
        left_layout = QVBoxLayout(left_group)
        self.original_text = QTextEdit()
        self.original_text.setReadOnly(True)
        self.original_text.setFont(QFont("Consolas", 9))
        self.original_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        left_layout.addWidget(self.original_text)
        self.text_splitter.addWidget(left_group)

        # Right pane: Decompiled C
        right_group = QGroupBox("Decompiled C")
        right_layout = QVBoxLayout(right_group)
        self.decompiled_text = QTextEdit()
        self.decompiled_text.setReadOnly(True)
        self.decompiled_text.setFont(QFont("Consolas", 9))
        self.decompiled_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        right_layout.addWidget(self.decompiled_text)
        self.text_splitter.addWidget(right_group)

        # Equal split
        self.text_splitter.setSizes([500, 500])

        layout.addWidget(self.text_splitter)
        return tab

    def _create_bytecode_diff_tab(self) -> QWidget:
        """
        Create the bytecode instruction comparison tab.

        Returns:
            Widget containing side-by-side bytecode viewers
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create horizontal splitter for side-by-side view
        self.bytecode_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left pane: Original bytecode
        left_group = QGroupBox("Original Bytecode")
        left_layout = QVBoxLayout(left_group)
        self.original_bytecode = QTextEdit()
        self.original_bytecode.setReadOnly(True)
        self.original_bytecode.setFont(QFont("Consolas", 9))
        self.original_bytecode.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        left_layout.addWidget(self.original_bytecode)
        self.bytecode_splitter.addWidget(left_group)

        # Right pane: Recompiled bytecode
        right_group = QGroupBox("Recompiled Bytecode")
        right_layout = QVBoxLayout(right_group)
        self.recompiled_bytecode = QTextEdit()
        self.recompiled_bytecode.setReadOnly(True)
        self.recompiled_bytecode.setFont(QFont("Consolas", 9))
        self.recompiled_bytecode.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        right_layout.addWidget(self.recompiled_bytecode)
        self.bytecode_splitter.addWidget(right_group)

        # Equal split
        self.bytecode_splitter.setSizes([500, 500])

        layout.addWidget(self.bytecode_splitter)
        return tab

    def _show_placeholder(self):
        """Show placeholder text when no comparison is loaded."""
        placeholder = "No comparison loaded.\n\nSelect an error from the list above to view differences."
        self.original_text.setPlainText(placeholder)
        self.decompiled_text.setPlainText(placeholder)
        self.original_bytecode.setPlainText(placeholder)
        self.recompiled_bytecode.setPlainText(placeholder)

    def show_diff(self, original_asm: str, decompiled_c: str):
        """
        Show side-by-side comparison of assembly and C code with highlighting.

        This method:
        1. Splits input into lines
        2. Uses difflib to identify differences
        3. Applies color highlighting to changed/added/removed lines
        4. Displays in side-by-side panes

        Args:
            original_asm: Original assembly code as string
            decompiled_c: Decompiled C code as string
        """
        # Switch to text diff tab
        self.tabs.setCurrentIndex(0)

        # Split into lines
        original_lines = original_asm.splitlines()
        decompiled_lines = decompiled_c.splitlines()

        # Compute line-by-line diff
        matcher = SequenceMatcher(None, original_lines, decompiled_lines)

        # Collect highlighted lines
        original_highlighted = []
        decompiled_highlighted = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                # Unchanged lines - no highlighting
                original_highlighted.extend((line, None) for line in original_lines[i1:i2])
                decompiled_highlighted.extend((line, None) for line in decompiled_lines[j1:j2])
            elif tag == 'delete':
                # Lines only in original - light red
                original_highlighted.extend((line, '#ffe6e6') for line in original_lines[i1:i2])
            elif tag == 'insert':
                # Lines only in decompiled - light green
                decompiled_highlighted.extend((line, '#e6ffe6') for line in decompiled_lines[j1:j2])
            elif tag == 'replace':
                # Changed lines - light yellow
                original_highlighted.extend((line, '#fffacd') for line in original_lines[i1:i2])
                decompiled_highlighted.extend((line, '#fffacd') for line in decompiled_lines[j1:j2])

        # Apply highlighting to text edits
        self._apply_highlighting(self.original_text, original_highlighted)
        self._apply_highlighting(self.decompiled_text, decompiled_highlighted)

    def _apply_highlighting(self, text_edit: QTextEdit, lines: List[Tuple[str, Optional[str]]]):
        """
        Apply line-by-line highlighting to a text edit widget.

        Args:
            text_edit: QTextEdit widget to apply highlighting to
            lines: List of (line_text, background_color) tuples
        """
        text_edit.clear()
        cursor = text_edit.textCursor()

        for line_text, bg_color in lines:
            # Create format with optional background color
            fmt = QTextCharFormat()
            if bg_color:
                fmt.setBackground(QColor(bg_color))

            # Insert line with formatting
            cursor.insertText(line_text + '\n', fmt)

        # Reset cursor to top
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        text_edit.setTextCursor(cursor)

    def show_bytecode_diff(self, original_scr: Path, recompiled_scr: Path):
        """
        Show instruction-level bytecode comparison.

        This method:
        1. Uses BytecodeComparator to load and compare .SCR files
        2. Extracts code segment instruction differences
        3. Formats disassembly for both files
        4. Highlights differences at instruction level

        Args:
            original_scr: Path to original .SCR file
            recompiled_scr: Path to recompiled .SCR file
        """
        # Switch to bytecode diff tab
        self.tabs.setCurrentIndex(1)

        if BytecodeComparator is None:
            self.original_bytecode.setPlainText("BytecodeComparator not available")
            self.recompiled_bytecode.setPlainText("BytecodeComparator not available")
            return

        try:
            # Load comparison using BytecodeComparator
            comparator = BytecodeComparator()
            comparison = comparator.compare_files(original_scr, recompiled_scr)

            if not comparison.is_valid:
                error_msg = f"Comparison failed: {comparison.load_error}"
                self.original_bytecode.setPlainText(error_msg)
                self.recompiled_bytecode.setPlainText(error_msg)
                return

            # Extract code segment differences
            if 'code' not in comparison.sections:
                self.original_bytecode.setPlainText("No code section found")
                self.recompiled_bytecode.setPlainText("No code section found")
                return

            code_comparison = comparison.sections['code']

            # Format disassembly with difference highlighting
            original_disasm = self._format_bytecode_with_highlights(
                comparator.original,
                code_comparison,
                is_original=True
            )
            recompiled_disasm = self._format_bytecode_with_highlights(
                comparator.recompiled,
                code_comparison,
                is_original=False
            )

            # Apply to text edits
            self._apply_highlighting(self.original_bytecode, original_disasm)
            self._apply_highlighting(self.recompiled_bytecode, recompiled_disasm)

        except Exception as e:
            error_msg = f"Error loading bytecode comparison: {e}"
            self.original_bytecode.setPlainText(error_msg)
            self.recompiled_bytecode.setPlainText(error_msg)

    def _format_bytecode_with_highlights(
        self,
        scr_file,
        code_comparison,
        is_original: bool
    ) -> List[Tuple[str, Optional[str]]]:
        """
        Format bytecode disassembly with instruction-level highlighting.

        Args:
            scr_file: SCRFile object with instructions
            code_comparison: SectionComparison for code segment
            is_original: True if formatting original file, False if recompiled

        Returns:
            List of (line_text, background_color) tuples
        """
        lines = []

        # Build set of instruction addresses with differences
        diff_addresses = set()
        for diff in code_comparison.differences:
            # Extract address from location string (e.g., "instruction[42]")
            if diff.location.startswith("instruction["):
                try:
                    addr = int(diff.location.split('[')[1].split(']')[0])
                    diff_addresses.add(addr)
                except (IndexError, ValueError):
                    pass

        # Format each instruction
        for i, instr in enumerate(scr_file.code_segment.instructions):
            # Get mnemonic from opcode resolver
            mnemonic = scr_file.opcode_resolver.opcode_map.get(
                instr.opcode, f"OP_{instr.opcode}"
            )

            # Format instruction line
            line = f"{i:5d}  {mnemonic:12s}  {instr.arg1:8d}  {instr.arg2:8d}"

            # Highlight if this instruction differs
            bg_color = '#fffacd' if i in diff_addresses else None  # Light yellow for differences

            lines.append((line, bg_color))

        # Add header
        header = [
            ("Index  Mnemonic      Arg1        Arg2", None),
            ("=" * 50, None),
        ]

        return header + lines

    def clear(self):
        """Clear all diff views and show placeholder."""
        self._show_placeholder()
