"""
Background worker for decompilation to avoid blocking GUI.

Follows the ValidationWorker pattern from validation_view.py.
"""

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from PyQt6.QtCore import QThread, pyqtSignal
except ImportError:
    print("PyQt6 not installed. Install with: pip install PyQt6")
    import sys
    sys.exit(1)

from ...core.loader import SCRFile
from ...core.disasm import Disassembler
from ...core.ir.ssa import build_ssa_incremental
from ...core.ir.structure import format_structured_function_named


@dataclass
class DecompilationResult:
    """Result of decompilation operation"""
    scr: SCRFile
    disasm: Disassembler
    ssa_func: Any  # SSAFunction from build_ssa
    decomp_text: str
    func_bounds: Dict[str, tuple]
    heritage_metadata: Optional[Dict] = None


class DecompilationWorker(QThread):
    """Background worker for decompilation to avoid blocking GUI"""

    # Signals
    progress = pyqtSignal(str, int)  # Progress message, percentage (0-100)
    finished = pyqtSignal(object)  # DecompilationResult or Exception
    error = pyqtSignal(str)  # Error message

    def __init__(self, filename: str, variant: str = "auto"):
        super().__init__()
        self.filename = filename
        self.variant = variant
        self._cancel_requested = False
        self._start_time = None

    def cancel(self):
        """Request cancellation of decompilation"""
        self._cancel_requested = True

    def _emit_progress(self, message: str, percentage: int):
        """Emit progress update with small delay to ensure delivery"""
        self.progress.emit(message, percentage)
        # Small sleep to allow main thread event loop to process the signal
        # before we start a blocking operation
        self.msleep(10)

    def run(self):
        """Run decompilation in background thread"""
        try:
            self._start_time = time.time()

            # Step 1: Load SCR file
            self._emit_progress("Loading file...", 0)
            scr = SCRFile.load(self.filename, variant=self.variant)

            if self._cancel_requested:
                self.finished.emit(Exception("Decompilation cancelled by user"))
                return

            # Step 2: Create disassembler
            self._emit_progress("Disassembling...", 5)
            disasm = Disassembler(scr)

            if self._cancel_requested:
                self.finished.emit(Exception("Decompilation cancelled by user"))
                return

            # Step 3: Build SSA (incremental heritage) - this is the slow part
            # We use the same SSA for both decompilation and expressions tab
            self._emit_progress("Building SSA...", 10)
            ssa_func, heritage_metadata = build_ssa_incremental(scr, return_metadata=True)

            if self._cancel_requested:
                self.finished.emit(Exception("Decompilation cancelled by user"))
                return

            # Step 4: Detect function boundaries
            self._emit_progress("Detecting function boundaries...", 20)
            func_bounds = disasm.get_function_boundaries_v2()

            if self._cancel_requested:
                self.finished.emit(Exception("Decompilation cancelled by user"))
                return

            # Step 5: Format each function (25-95%)
            # This is the main bottleneck - format_structured_function_named is slow
            decomp_lines = [f"// Structured decompilation of {Path(self.filename).name}"]
            decomp_lines.append(f"// Functions: {len(func_bounds)}")
            decomp_lines.append("")

            sorted_funcs = sorted(func_bounds.items(), key=lambda x: x[1][0])
            total_funcs = len(sorted_funcs)

            for idx, (func_name, (func_start, func_end)) in enumerate(sorted_funcs):
                if self._cancel_requested:
                    self.finished.emit(Exception("Decompilation cancelled by user"))
                    return

                # Emit progress BEFORE the work (25-95% range = 70% span)
                func_progress = 25 + int((idx / max(total_funcs, 1)) * 70)
                self._emit_progress(f"Decompiling {idx + 1}/{total_funcs}: {func_name}", func_progress)

                text = format_structured_function_named(
                    ssa_func, func_name, func_start, func_end,
                    function_bounds=func_bounds,
                    heritage_metadata=heritage_metadata,
                    use_collapse=True  # Match CLI default
                )
                decomp_lines.append(text)
                decomp_lines.append("")

            # Step 6: Finalize (95-100%)
            self._emit_progress("Rendering output...", 95)
            decomp_text = "\n".join(decomp_lines)

            if self._cancel_requested:
                self.finished.emit(Exception("Decompilation cancelled by user"))
                return

            self._emit_progress("Complete", 100)

            # Return result
            result = DecompilationResult(
                scr=scr,
                disasm=disasm,
                ssa_func=ssa_func,  # Incremental SSA for expressions tab and decompilation
                decomp_text=decomp_text,
                func_bounds=func_bounds,
                heritage_metadata=heritage_metadata,
            )
            self.finished.emit(result)

        except Exception as e:
            self._emit_progress(f"Error: {str(e)}", 0)
            self.finished.emit(e)
