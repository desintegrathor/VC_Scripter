"""
VC-Script Tool - Tkinter GUI

Provides decompilation (single file + folder) and compilation functionality.
"""

import json
import shutil
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from types import SimpleNamespace
from typing import Optional


# ---------------------------------------------------------------------------
# Settings persistence
# ---------------------------------------------------------------------------

SETTINGS_PATH = Path(__file__).parent / "vcdecomp_settings.json"

_SETTINGS_KEYS = [
    "decompile_mode", "decompile_input", "decompile_header",
    "decompile_output", "compile_script", "compile_output",
]


def _load_settings() -> dict:
    try:
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        return {k: data[k] for k in _SETTINGS_KEYS if k in data}
    except Exception:
        return {}


def _save_settings(settings: dict):
    try:
        SETTINGS_PATH.write_text(
            json.dumps(settings, indent=2), encoding="utf-8"
        )
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Decompilation args namespace
# ---------------------------------------------------------------------------

def _make_args(header: Optional[str] = None) -> SimpleNamespace:
    return SimpleNamespace(
        variant="auto",
        debug=False,
        verbose=False,
        legacy_ssa=False,
        no_collapse=False,
        no_simplify=False,
        no_array_detection=False,
        no_bidirectional_types=False,
        debug_simplify=False,
        debug_array_detection=False,
        debug_type_inference=False,
        header=header,
        dump_type_evidence=None,
    )


# ---------------------------------------------------------------------------
# Worker functions (run in background threads)
# ---------------------------------------------------------------------------

def _decompile_single(scr_path: Path, output_dir: Path, header: Optional[str],
                      status_cb):
    """Decompile a single .scr file producing .c and .asm."""
    from vcdecomp.core.ir.decompile_file import decompile_single_scr
    from vcdecomp.core.loader import SCRFile
    from vcdecomp.core.disasm import Disassembler
    from vcdecomp.core.headers.database import get_header_database

    # Ensure header db is initialised
    get_header_database()

    args = _make_args(header)
    basename = scr_path.stem

    status_cb(f"Decompiling {scr_path.name}...")
    c_text = decompile_single_scr(scr_path, args, header_path=Path(header) if header else None)
    out_c = output_dir / f"{basename}.c"
    out_c.write_text(c_text, encoding="utf-8")

    status_cb(f"Disassembling {scr_path.name}...")
    scr = SCRFile.load(str(scr_path))
    asm_text = Disassembler(scr).to_string()
    out_asm = output_dir / f"{basename}.asm"
    out_asm.write_text(asm_text, encoding="utf-8")

    status_cb(f"Done: {out_c.name}, {out_asm.name}")


def _decompile_folder(folder: Path, output_dir: Path, header: Optional[str],
                      status_cb):
    """Decompile all .SCR files in a folder with cross-file context."""
    from vcdecomp.core.ir.decompile_file import (
        decompile_single_scr,
        resolve_mission_header,
        run_pass1_analysis,
    )
    from vcdecomp.core.ir.cross_file_context import CrossFileContext
    from vcdecomp.core.loader import SCRFile
    from vcdecomp.core.disasm import Disassembler
    from vcdecomp.core.headers.database import get_header_database
    from vcdecomp.core.constants import _reset_constants

    get_header_database()
    args = _make_args(header)

    # Collect .SCR files
    scr_files = sorted(
        [f for f in folder.iterdir() if f.suffix.upper() == ".SCR"],
        key=lambda p: p.name.upper(),
    )
    if not scr_files:
        status_cb("No .SCR files found in folder")
        return

    total = len(scr_files)

    # Resolve mission header
    header_path = resolve_mission_header(folder, header)
    if header_path:
        from vcdecomp.core.headers.database import get_header_database as _get_hdb
        hdb = _get_hdb()
        hdb.load_mission_header(header_path)
        _reset_constants()

    # Pass 1
    ctx = CrossFileContext()
    for i, scr_path in enumerate(scr_files, 1):
        status_cb(f"Pass 1: [{i}/{total}] {scr_path.name}")
        try:
            scr, globals_usage, float_globals = run_pass1_analysis(scr_path, args)
            ctx.add_file_analysis(scr_path.name, scr, globals_usage, float_globals)
        except Exception as e:
            status_cb(f"Warning: {scr_path.name}: {e}")

    ctx.resolve()

    # Pass 2
    output_dir.mkdir(parents=True, exist_ok=True)
    for i, scr_path in enumerate(scr_files, 1):
        status_cb(f"Pass 2: [{i}/{total}] {scr_path.name}")
        try:
            c_text = decompile_single_scr(
                scr_path, args,
                cross_file_context=ctx,
                header_path=header_path,
                header_already_loaded=True,
            )
            (output_dir / f"{scr_path.stem}.c").write_text(c_text, encoding="utf-8")

            scr = SCRFile.load(str(scr_path))
            asm_text = Disassembler(scr).to_string()
            (output_dir / f"{scr_path.stem}.asm").write_text(asm_text, encoding="utf-8")
        except Exception as e:
            status_cb(f"Error: {scr_path.name}: {e}")

    status_cb(f"Done: {total} files decompiled")


def _compile_script(source_path: Path, output_dir: Path, status_cb):
    """Compile a .c script using the SCMP toolchain."""
    compiler_dir = Path(__file__).parent / "compiler"
    scmp = compiler_dir / "scmp.exe"

    if not scmp.exists():
        status_cb(f"Error: scmp.exe not found at {scmp}")
        return

    basename = source_path.stem
    work_c = compiler_dir / source_path.name
    work_scr = compiler_dir / f"{basename}.scr"
    work_h = compiler_dir / f"{basename}.h"
    err_files = [compiler_dir / f for f in ("spp.err", "scc.err", "sasm.err")]

    # Clean up previous artifacts
    for f in [work_scr, work_h] + err_files:
        if f.exists():
            f.unlink()

    # Copy source to compiler dir
    shutil.copy2(source_path, work_c)

    status_cb(f"Compiling {source_path.name}...")

    # Run scmp
    try:
        subprocess.Popen(
            f'"{scmp}" "{source_path.name}" "{basename}.scr" "{basename}.h"',
            shell=True,
            cwd=str(compiler_dir),
        )
    except Exception as e:
        status_cb(f"Error launching compiler: {e}")
        return

    # Poll for output
    start = time.time()
    timeout = 30
    while time.time() - start < timeout:
        time.sleep(0.5)

        # Check for errors first
        for ef in err_files:
            if ef.exists() and ef.stat().st_size > 0:
                err_text = ef.read_text(encoding="latin-1", errors="replace").strip()
                status_cb(f"Compilation error ({ef.name})")
                # Show error in messagebox (schedule on main thread)
                # We'll return the error and let the caller handle it
                raise RuntimeError(f"Compiler error ({ef.name}):\n\n{err_text}")

        if work_scr.exists() and work_scr.stat().st_size > 0:
            time.sleep(0.5)  # Let it finish writing
            break
    else:
        status_cb("Compilation timed out (30s)")
        return

    # Copy outputs
    out_scr = output_dir / f"{basename}.scr"
    shutil.copy2(work_scr, out_scr)
    status_cb(f"Created {out_scr.name} ({out_scr.stat().st_size:,} bytes)")

    if work_h.exists():
        out_h = output_dir / f"{basename}.h"
        shutil.copy2(work_h, out_h)

    # Clean up temp files in compiler dir
    for f in [work_c, work_scr, work_h] + err_files:
        if f.exists():
            try:
                f.unlink()
            except Exception:
                pass

    status_cb(f"Done: {out_scr.name}")


# ---------------------------------------------------------------------------
# GUI Application
# ---------------------------------------------------------------------------

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("VC-Script Tool")
        self.root.resizable(False, False)

        self.settings = _load_settings()
        self._busy = False

        # --- Variables ---
        self.decompile_mode = tk.StringVar(value=self.settings.get("decompile_mode", "single"))
        self.decompile_input = tk.StringVar(value=self.settings.get("decompile_input", ""))
        self.decompile_header = tk.StringVar(value=self.settings.get("decompile_header", ""))
        self.decompile_output = tk.StringVar(value=self.settings.get("decompile_output", ""))
        self.compile_script = tk.StringVar(value=self.settings.get("compile_script", ""))
        self.compile_output = tk.StringVar(value=self.settings.get("compile_output", ""))
        self.status_var = tk.StringVar(value="Ready")

        self._build_ui()

    # ---- UI Construction ----

    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}

        # Decompile frame
        dec_frame = ttk.LabelFrame(self.root, text="Decompile", padding=8)
        dec_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))

        # Mode radio buttons
        mode_frame = ttk.Frame(dec_frame)
        mode_frame.grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Radiobutton(mode_frame, text="Single file", variable=self.decompile_mode,
                        value="single", command=self._on_mode_change).pack(side="left", padx=(0, 12))
        ttk.Radiobutton(mode_frame, text="Folder", variable=self.decompile_mode,
                        value="folder", command=self._on_mode_change).pack(side="left")

        # Input row
        ttk.Label(dec_frame, text="Input:").grid(row=1, column=0, sticky="w", **pad)
        ttk.Entry(dec_frame, textvariable=self.decompile_input, width=50, state="readonly"
                  ).grid(row=1, column=1, sticky="ew", **pad)
        self.btn_select_input = ttk.Button(dec_frame, text="Select file",
                                           command=self._select_decompile_input)
        self.btn_select_input.grid(row=1, column=2, **pad)

        # Header row
        ttk.Label(dec_frame, text="Header (optional):").grid(row=2, column=0, sticky="w", **pad)
        ttk.Entry(dec_frame, textvariable=self.decompile_header, width=50, state="readonly"
                  ).grid(row=2, column=1, sticky="ew", **pad)
        ttk.Button(dec_frame, text="Select header",
                   command=self._select_decompile_header).grid(row=2, column=2, **pad)

        # Output row
        ttk.Label(dec_frame, text="Output:").grid(row=3, column=0, sticky="w", **pad)
        ttk.Entry(dec_frame, textvariable=self.decompile_output, width=50, state="readonly"
                  ).grid(row=3, column=1, sticky="ew", **pad)
        ttk.Button(dec_frame, text="Select output",
                   command=self._select_decompile_output).grid(row=3, column=2, **pad)

        # Decompile button
        self.btn_decompile = ttk.Button(dec_frame, text="Decompile",
                                        command=self._do_decompile)
        self.btn_decompile.grid(row=4, column=2, sticky="e", **pad)

        dec_frame.columnconfigure(1, weight=1)

        # Compile frame
        comp_frame = ttk.LabelFrame(self.root, text="Compile", padding=8)
        comp_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=4)

        ttk.Label(comp_frame, text="Script:").grid(row=0, column=0, sticky="w", **pad)
        ttk.Entry(comp_frame, textvariable=self.compile_script, width=50, state="readonly"
                  ).grid(row=0, column=1, sticky="ew", **pad)
        ttk.Button(comp_frame, text="Select script",
                   command=self._select_compile_script).grid(row=0, column=2, **pad)

        ttk.Label(comp_frame, text="Output:").grid(row=1, column=0, sticky="w", **pad)
        ttk.Entry(comp_frame, textvariable=self.compile_output, width=50, state="readonly"
                  ).grid(row=1, column=1, sticky="ew", **pad)
        ttk.Button(comp_frame, text="Select output",
                   command=self._select_compile_output).grid(row=1, column=2, **pad)

        self.btn_compile = ttk.Button(comp_frame, text="Compile",
                                      command=self._do_compile)
        self.btn_compile.grid(row=2, column=2, sticky="e", **pad)

        comp_frame.columnconfigure(1, weight=1)

        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(4, 10))
        ttk.Label(status_frame, text="Status:").pack(side="left")
        ttk.Label(status_frame, textvariable=self.status_var).pack(side="left", padx=4)

        # Update button text based on mode
        self._on_mode_change()

    def _on_mode_change(self):
        mode = self.decompile_mode.get()
        if mode == "single":
            self.btn_select_input.config(text="Select file")
        else:
            self.btn_select_input.config(text="Select folder")

    # ---- Path selectors ----

    def _select_decompile_input(self):
        mode = self.decompile_mode.get()
        if mode == "single":
            path = filedialog.askopenfilename(
                title="Select .SCR file",
                filetypes=[("SCR files", "*.scr"), ("All files", "*.*")],
            )
        else:
            path = filedialog.askdirectory(title="Select mission folder")
        if path:
            self.decompile_input.set(path)
            self._persist()

    def _select_decompile_header(self):
        path = filedialog.askopenfilename(
            title="Select header file",
            filetypes=[("Header files", "*.h *.H"), ("All files", "*.*")],
        )
        if path:
            self.decompile_header.set(path)
            self._persist()

    def _select_decompile_output(self):
        path = filedialog.askdirectory(title="Select output directory")
        if path:
            self.decompile_output.set(path)
            self._persist()

    def _select_compile_script(self):
        path = filedialog.askopenfilename(
            title="Select .C source file",
            filetypes=[("C source", "*.c"), ("All files", "*.*")],
        )
        if path:
            self.compile_script.set(path)
            self._persist()

    def _select_compile_output(self):
        path = filedialog.askdirectory(title="Select output directory")
        if path:
            self.compile_output.set(path)
            self._persist()

    # ---- Persistence ----

    def _persist(self):
        self.settings.update({
            "decompile_mode": self.decompile_mode.get(),
            "decompile_input": self.decompile_input.get(),
            "decompile_header": self.decompile_header.get(),
            "decompile_output": self.decompile_output.get(),
            "compile_script": self.compile_script.get(),
            "compile_output": self.compile_output.get(),
        })
        _save_settings(self.settings)

    # ---- Status helpers ----

    def _set_status(self, msg: str):
        self.root.after(0, lambda: self.status_var.set(msg))

    def _set_busy(self, busy: bool):
        self._busy = busy
        state = "disabled" if busy else "!disabled"
        self.root.after(0, lambda: self.btn_decompile.state([state]))
        self.root.after(0, lambda: self.btn_compile.state([state]))

    # ---- Actions ----

    def _do_decompile(self):
        if self._busy:
            return

        inp = self.decompile_input.get().strip()
        out = self.decompile_output.get().strip()
        header = self.decompile_header.get().strip() or None

        if not inp:
            messagebox.showwarning("Missing input", "Please select an input file or folder.")
            return
        if not out:
            messagebox.showwarning("Missing output", "Please select an output directory.")
            return

        inp_path = Path(inp)
        out_path = Path(out)
        out_path.mkdir(parents=True, exist_ok=True)

        mode = self.decompile_mode.get()
        self._set_busy(True)
        self._persist()

        def _worker():
            try:
                if mode == "single":
                    _decompile_single(inp_path, out_path, header, self._set_status)
                else:
                    _decompile_folder(inp_path, out_path, header, self._set_status)
            except Exception as e:
                self._set_status(f"Error: {e}")
                self.root.after(0, lambda: messagebox.showerror("Decompilation Error", str(e)))
            finally:
                self._set_busy(False)

        threading.Thread(target=_worker, daemon=True).start()

    def _do_compile(self):
        if self._busy:
            return

        script = self.compile_script.get().strip()
        out = self.compile_output.get().strip()

        if not script:
            messagebox.showwarning("Missing script", "Please select a .C source file.")
            return
        if not out:
            messagebox.showwarning("Missing output", "Please select an output directory.")
            return

        script_path = Path(script)
        out_path = Path(out)
        out_path.mkdir(parents=True, exist_ok=True)

        self._set_busy(True)
        self._persist()

        def _worker():
            try:
                _compile_script(script_path, out_path, self._set_status)
            except RuntimeError as e:
                self._set_status("Compilation failed")
                self.root.after(0, lambda: messagebox.showerror("Compilation Error", str(e)))
            except Exception as e:
                self._set_status(f"Error: {e}")
                self.root.after(0, lambda: messagebox.showerror("Compilation Error", str(e)))
            finally:
                self._set_busy(False)

        threading.Thread(target=_worker, daemon=True).start()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_gui(initial_file: Optional[str] = None):
    root = tk.Tk()
    app = App(root)
    if initial_file:
        app.decompile_input.set(initial_file)
        app.decompile_mode.set("single")
    root.mainloop()


if __name__ == "__main__":
    run_gui()
