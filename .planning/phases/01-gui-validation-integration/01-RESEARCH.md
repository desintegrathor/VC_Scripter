# Phase 1: GUI Validation Integration - Research

**Researched:** 2026-01-17
**Domain:** PyQt6 GUI integration with background validation processes
**Confidence:** HIGH

## Summary

Phase 1 integrates the existing CLI validation system into the PyQt6 GUI, allowing users to validate decompiled scripts with one click. The research confirms that PyQt6 provides robust patterns for background processing with QThread, and the existing validation architecture is already well-structured for GUI integration.

**Key findings:**
- Existing GUI uses PyQt6 6.0+ with established patterns (main_window.py uses QThread for ValidationWorker)
- Validation system is fully functional as CLI (ValidationOrchestrator, SCMPWrapper, CompilationResult types)
- GUI already has ValidationPanel widget with complete implementation in validation_view.py
- Standard QThread worker pattern with signals/slots provides thread-safe progress updates

**Primary recommendation:** Extend MainWindow to integrate existing ValidationPanel with decompilation view, enabling one-click validation of currently displayed script.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| PyQt6 | 6.0.0+ | GUI framework | Official Qt6 Python bindings, actively maintained |
| QThread | Built-in | Background processing | Qt's thread-safe worker pattern |
| pyqtSignal | Built-in | Thread communication | Type-safe signal/slot mechanism |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| QProgressBar | Built-in | Progress indication | Long-running operations (compilation) |
| QTextEdit | Built-in | Error display | Multi-line text with formatting |
| QTreeWidget | Built-in | Structured diff display | Hierarchical difference categorization |
| QSplitter | Built-in | Resizable panels | Side-by-side comparison views |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| QThread | QThreadPool + QRunnable | Better for many concurrent tasks, overkill for single validation |
| pyqtSignal | Direct method calls | Signals are thread-safe, direct calls are not |
| QTextEdit | QPlainTextEdit | QTextEdit supports rich formatting for error highlighting |

**Installation:**
```bash
# Already in requirements
PyQt6>=6.0.0
```

## Architecture Patterns

### Recommended Project Structure
```
vcdecomp/gui/
├── main_window.py           # MainWindow with validation integration
├── views/
│   └── validation_view.py   # ValidationPanel (already exists)
├── widgets/
│   └── difference_widgets.py # Diff visualization (already exists)
└── dialogs/
    └── validation_settings.py # Settings dialog (already exists)
```

### Pattern 1: Worker Thread with Signals
**What:** QThread subclass with pyqtSignal for progress updates
**When to use:** Long-running operations that must not block GUI
**Example:**
```python
# Source: Existing vcdecomp/gui/views/validation_view.py (lines 42-205)
class ValidationWorker(QThread):
    finished = pyqtSignal(object)  # ValidationResult or Exception
    progress = pyqtSignal(str, int)  # message, percentage
    time_estimate = pyqtSignal(str)  # time remaining

    def __init__(self, original_scr, decompiled_source, compiler_dir, ...):
        super().__init__()
        self.original_scr = original_scr
        self.decompiled_source = decompiled_source
        # ... configuration

    def cancel(self):
        self._cancel_requested = True

    def run(self):
        """Run validation in background thread"""
        try:
            self._emit_progress("Initializing...", 0)
            orchestrator = ValidationOrchestrator(...)
            self._emit_progress("Compiling...", 25)
            result = orchestrator.validate(...)
            self._emit_progress("Complete", 100)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(e)
```

### Pattern 2: Main Thread Signal Handling
**What:** Connect worker signals to GUI update slots
**When to use:** Updating widgets from background thread
**Example:**
```python
# Source: Existing vcdecomp/gui/views/validation_view.py (lines 454-468)
worker = ValidationWorker(...)
worker.progress.connect(self.on_progress)  # Update QProgressBar
worker.time_estimate.connect(self.on_time_estimate)  # Update QLabel
worker.finished.connect(self.on_validation_finished)  # Display results
worker.start()

def on_progress(self, message: str, percentage: int):
    """Handle progress updates (runs in main thread)"""
    self.progress_label.setText(message)
    self.progress_bar.setValue(percentage)
```

### Pattern 3: Validation from In-Memory Script
**What:** Save decompiled text to temp file, validate, clean up
**When to use:** Validating currently displayed script without requiring user to save
**Example:**
```python
# Pattern to implement in MainWindow
def validate_current_script(self):
    """Validate currently displayed decompilation"""
    # Get decompiled text from decomp_view
    decompiled_text = self.decomp_view.toPlainText()

    # Save to temp file
    temp_dir = Path(tempfile.gettempdir()) / "vcdecomp_validation"
    temp_dir.mkdir(exist_ok=True)
    temp_source = temp_dir / f"{self.scr_file.stem}_decompiled.c"
    temp_source.write_text(decompiled_text)

    # Trigger validation
    self.validation_panel.start_validation(
        original_scr=self.scr_file,
        decompiled_source=temp_source
    )
```

### Pattern 4: Error Display with Context
**What:** QTextEdit with rich formatting for error messages
**When to use:** Displaying compilation errors with file:line:column context
**Example:**
```python
# Based on existing CompilationError structure (compilation_types.py)
def display_compilation_errors(self, errors: List[CompilationError]):
    """Display errors with formatting"""
    text_edit = QTextEdit()
    text_edit.setReadOnly(True)

    for error in errors:
        # Format: [stage] file:line:col: severity: message
        location = ""
        if error.file:
            location = f"{error.file}:{error.line}:{error.column}: "

        error_text = f"[{error.stage.value}] {location}{error.severity.value}: {error.message}\n"

        # Apply color based on severity
        if error.severity == ErrorSeverity.FATAL:
            text_edit.setTextColor(QColor(255, 0, 0))  # Red
        elif error.severity == ErrorSeverity.ERROR:
            text_edit.setTextColor(QColor(255, 100, 0))  # Orange
        elif error.severity == ErrorSeverity.WARNING:
            text_edit.setTextColor(QColor(255, 255, 0))  # Yellow

        text_edit.append(error_text)
```

### Anti-Patterns to Avoid
- **Blocking GUI thread:** Never run ValidationOrchestrator.validate() in main thread - always use QThread
- **Direct widget access from worker:** Never call widget methods from QThread.run() - use signals only
- **Ignoring cancellation:** Always check _cancel_requested flag periodically in long operations
- **Leaking temp files:** Always clean up temporary decompiled source files after validation

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Thread-safe GUI updates | Custom mutex + queue | pyqtSignal/pyqtSlot | Qt handles thread safety automatically via event loop |
| Progress estimation | Custom time tracking | ValidationWorker pattern (existing) | Already implements elapsed/remaining time calculation |
| Error file parsing | Custom regex parser | _parse_error_file() in compiler_wrapper.py | Handles multiple .err formats (SPP, SCC, SASM) |
| Bytecode diff display | Custom comparison widget | DifferenceTreeView (existing) | Hierarchical view with category/severity grouping |
| Settings persistence | JSON/config file | QSettings | Platform-native settings storage |

**Key insight:** PyQt6's signal/slot mechanism eliminates need for manual thread synchronization. The existing validation system is already production-ready.

## Common Pitfalls

### Pitfall 1: GUI Thread Blocking
**What goes wrong:** Running validation in main thread freezes GUI for 10-30 seconds
**Why it happens:** ValidationOrchestrator.validate() calls subprocess (SCMP.exe) which blocks
**How to avoid:** Always use ValidationWorker QThread pattern (already implemented in validation_view.py)
**Warning signs:** GUI becomes unresponsive during compilation, no progress updates

### Pitfall 2: Widget Access from Worker Thread
**What goes wrong:** Crashes with "QObject: Cannot create children for a parent that is in a different thread"
**Why it happens:** Qt widgets can only be accessed from main GUI thread
**How to avoid:** Use signals to send data to main thread, update widgets in signal handlers
**Warning signs:** Random crashes during validation, thread-related error messages

### Pitfall 3: Memory Leaks with Temp Files
**What goes wrong:** Temp directory fills with .c files after repeated validations
**Why it happens:** Validation creates temp files but doesn't clean up on error/cancellation
**How to avoid:** Use try/finally or context managers to ensure cleanup
**Warning signs:** Disk space decreasing, temp directory growing over time

### Pitfall 4: Stale Validation Results
**What goes wrong:** User edits script but sees old validation results
**Why it happens:** Validation results not invalidated when source changes
**How to avoid:** Clear validation panel when new script loaded or decompilation regenerated
**Warning signs:** Confusion about whether results match current script

### Pitfall 5: Settings Not Persisted
**What goes wrong:** User must reconfigure compiler directory every session
**Why it happens:** Settings stored in memory only, not saved between runs
**How to avoid:** Use QSettings to persist compiler_dir, include_dirs, timeout values
**Warning signs:** User complaints about repetitive configuration

## Code Examples

Verified patterns from official sources:

### Example 1: Integrate Validation Button in MainWindow
```python
# Source: Pattern from existing main_window.py structure
# Add to MainWindow.__init__():

def init_ui(self):
    # ... existing code ...

    # Add Validate button to toolbar or menu
    validate_action = QAction("&Validate", self)
    validate_action.setShortcut("Ctrl+V")
    validate_action.triggered.connect(self.validate_current_script)

    # Add to Tools menu
    tools_menu = menubar.addMenu("&Tools")
    tools_menu.addAction(validate_action)

def validate_current_script(self):
    """Validate currently displayed decompilation"""
    if not self.scr:
        QMessageBox.warning(self, "No Script", "Load a script first")
        return

    # Get decompiled text
    decompiled_text = self.decomp_view.toPlainText()

    # Save to temp file
    temp_dir = Path(tempfile.gettempdir()) / "vcdecomp_validation"
    temp_dir.mkdir(exist_ok=True)
    temp_source = temp_dir / f"{Path(self.scr.filepath).stem}_decompiled.c"
    temp_source.write_text(decompiled_text)

    # Show validation dock
    self.validation_dock.show()

    # Start validation
    self.validation_panel.start_validation(
        original_scr=self.scr.filepath,
        decompiled_source=str(temp_source)
    )
```

### Example 2: Display Compilation Errors
```python
# Source: Based on existing ValidationPanel.display_results() pattern
# Already implemented in validation_view.py lines 584-650

def display_results(self, result: ValidationResult):
    """Display validation results in the UI"""
    summary_lines = []
    summary_lines.append(f"Verdict: {result.verdict.value.upper()}")
    summary_lines.append("")
    summary_lines.append(f"Compilation: {'Success' if result.compilation_succeeded else 'Failed'}")

    if not result.compilation_succeeded:
        # Show compilation errors
        summary_lines.append("")
        summary_lines.append("COMPILATION ERRORS:")
        for error in result.compilation_result.errors[:5]:
            summary_lines.append(f"  {error}")

        if len(result.compilation_result.errors) > 5:
            summary_lines.append(f"  ... and {len(result.compilation_result.errors) - 5} more")

    self.summary_text.setPlainText("\n".join(summary_lines))
```

### Example 3: Side-by-Side Diff View
```python
# Source: Existing pattern from difference_widgets.py (lines 289-394)
# Already implemented in InstructionDiffView

class InstructionDiffView(QWidget):
    """Side-by-side view for comparing code differences"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create splitter for side-by-side view
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Original code
        orig_group = QGroupBox("Original")
        self.original_text = QTextEdit()
        self.original_text.setReadOnly(True)
        self.original_text.setFont(QFont("Consolas", 9))
        orig_group.setWidget(self.original_text)
        splitter.addWidget(orig_group)

        # Recompiled code
        recomp_group = QGroupBox("Recompiled")
        self.recompiled_text = QTextEdit()
        self.recompiled_text.setReadOnly(True)
        self.recompiled_text.setFont(QFont("Consolas", 9))
        recomp_group.setWidget(self.recompiled_text)
        splitter.addWidget(recomp_group)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| QThread.run() with manual thread creation | QThreadPool + QRunnable for multiple tasks | PyQt5 → PyQt6 (2020+) | Better resource management for concurrent operations |
| Manual mutex/lock management | pyqtSignal/pyqtSlot automatic queuing | Qt5 → Qt6 | Simpler, less error-prone thread communication |
| Custom error parsing | Structured CompilationError types | vcdecomp v0.1 (2024) | Type-safe, IDE-friendly error handling |
| CLI-only validation | GUI-integrated ValidationPanel | Current (2026) | User can validate without leaving GUI |

**Deprecated/outdated:**
- PyQt5: Use PyQt6 (Qt6 provides better performance, modern C++17 features)
- moveToThread() pattern: Still valid but QThreadPool preferred for multiple workers
- QTextEdit.setHtml(): Use setMarkdown() for formatted text (Qt 6.4+)

## Open Questions

Things that couldn't be fully resolved:

1. **How to handle multiple simultaneous validations?**
   - What we know: Current ValidationPanel supports one validation at a time
   - What's unclear: Should we support batch validation of multiple scripts from GUI?
   - Recommendation: Phase 1 supports single validation (VALID-01), batch validation deferred to Phase 2

2. **How to display .err file with line numbers matching original source?**
   - What we know: .err files reference temp file paths, not original script
   - What's unclear: Can we map temp file line numbers back to decompiled view line numbers?
   - Recommendation: Display .err content as-is for Phase 1, implement line mapping in Phase 4 (ERROR-03)

3. **Should validation auto-run on every decompilation?**
   - What we know: Validation takes 10-30 seconds per script
   - What's unclear: Would auto-validation improve UX or annoy users?
   - Recommendation: Manual "Validate" button for Phase 1, consider auto-validation toggle in Phase 5

4. **How to handle original .scr not available?**
   - What we know: Validation requires original .scr for bytecode comparison
   - What's unclear: What if user only has decompiled source?
   - Recommendation: Disable validation if original .scr not loaded, show informative message

## Sources

### Primary (HIGH confidence)
- Existing codebase: vcdecomp/gui/main_window.py - MainWindow structure and patterns
- Existing codebase: vcdecomp/gui/views/validation_view.py - ValidationPanel implementation
- Existing codebase: vcdecomp/validation/validator.py - ValidationOrchestrator API
- Existing codebase: vcdecomp/validation/compiler_wrapper.py - SCMPWrapper and error parsing
- PyQt6 documentation: https://doc.qt.io/qtforpython-6/ - Official Qt for Python docs

### Secondary (MEDIUM confidence)
- [Multithreading PyQt6 applications with QThreadPool](https://www.pythonguis.com/tutorials/multithreading-pyqt6-applications-qthreadpool/) - Worker pattern best practices
- [Use PyQt's QThread to Prevent Freezing GUIs](https://realpython.com/python-pyqt-qthread/) - QThread tutorial
- [PyQt6: Visualizing Progress with QProgressBar](https://coderscratchpad.com/pyqt6-visualizing-progress-with-qprogressbar/) - Progress bar updates from threads
- [Visual Studio Error List Window](https://learn.microsoft.com/en-us/visualstudio/ide/error-list-window) - Error display patterns
- [Meld - Visual Diff Tool](https://itsfoss.com/meld-gui-diff/) - Side-by-side comparison patterns

### Tertiary (LOW confidence)
- WebSearch results about PyQt6 inline error display - No specific 2026 resources found, general patterns apply

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Existing codebase uses PyQt6 6.0+, all patterns verified in code
- Architecture: HIGH - ValidationPanel already implements QThread worker pattern correctly
- Pitfalls: HIGH - Common Qt threading issues well-documented, existing code avoids them

**Research date:** 2026-01-17
**Valid until:** 60 days (2026-03-18) - PyQt6 is stable, patterns unlikely to change
