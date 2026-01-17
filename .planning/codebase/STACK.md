# Technology Stack

**Analysis Date:** 2026-01-17

## Languages

**Primary:**
- Python 3.x - Main implementation language for decompiler
- C - Target language for decompiled output, original Vietcong scripts

**Secondary:**
- Batch (.bat) - Compilation scripts for legacy Windows compiler toolchain
- Assembly - Intermediate representation in decompilation pipeline

## Runtime

**Environment:**
- Python 3.x (version unspecified in codebase)
- Windows platform expected (Windows-specific compiler tools, batch files)

**Package Manager:**
- pip (standard Python package manager)
- Lockfile: Not present (no requirements.lock or Pipfile.lock)

## Frameworks

**Core:**
- No external application framework
- Built on Python standard library (argparse, struct, dataclasses, pathlib)

**Testing:**
- pytest - Testing framework
- unittest - Standard library testing module (used alongside pytest)

**Build/Dev:**
- No build system detected (setuptools, poetry, etc.)
- No setup.py or pyproject.toml present

## Key Dependencies

**Critical:**
- PyQt6 >=6.0.0 - GUI application framework
  - Location: `vcdecomp/requirements.txt`
  - Used in: `vcdecomp/gui/main_window.py`, `vcdecomp/gui/views/`, `vcdecomp/gui/dialogs/`, `vcdecomp/gui/widgets/`
  - Optional dependency (CLI works without it)

**Infrastructure:**
- Python standard library modules:
  - struct - Binary file parsing (`.scr` bytecode format)
  - dataclasses - Data structure definitions
  - pathlib - File path handling
  - subprocess - External compiler execution (`vcdecomp/validation/compiler_wrapper.py`)
  - tempfile - Temporary file management for validation
  - logging - Logging infrastructure
  - json - Configuration and data export
  - argparse - CLI interface

## Configuration

**Environment:**
- No environment variables required for core functionality
- Validation system uses compiler directory path (default: `original-resources/compiler`)
- Windows-specific console encoding fix applied in `vcdecomp/__main__.py` (UTF-8 for Windows)

**Build:**
- No build configuration files detected
- Legacy Vietcong compiler configuration:
  - Compiler executables in `original-resources/compiler/`: `scmp.exe`, `scc.exe`, `sasm.exe`, `spp.exe`
  - Batch scripts: `original-resources/compiler/compile.bat`

## Platform Requirements

**Development:**
- Python 3.x interpreter
- Windows OS (for legacy compiler integration in validation system)
- PyQt6 (optional, for GUI features only)

**Production:**
- Python 3.x runtime
- CLI tool - no deployment artifacts
- Standalone executable distribution not configured

---

*Stack analysis: 2026-01-17*
