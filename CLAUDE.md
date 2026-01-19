# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VC-Script-Decompiler** decompiles Vietcong (2003) game scripts from `.scr` bytecode back to readable C-like source code. The scripts use a proprietary C-like language with external engine functions.

## Essential Commands

### Running the Decompiler
```bash
# Decompile a script (full structured output with debug)
python -m vcdecomp structure script.scr > output.c

# Decompile without debug output (clean version)
# Method 1: Filter out DEBUG lines with Python
python -m vcdecomp structure script.scr | python -c "import sys; sys.stdout.writelines(line for line in sys.stdin if not line.startswith('DEBUG'))" > output_clean.c

# Method 2: Filter with grep (Linux/Mac/Git Bash)
python -m vcdecomp structure script.scr | grep -v "^DEBUG" > output_clean.c

# Method 3: Post-process existing file
python -c "
with open('output.c', 'r', encoding='utf-8') as f:
    lines = [line for line in f if not line.startswith('DEBUG')]
with open('output_clean.c', 'w', encoding='utf-8') as f:
    f.writelines(lines)
"

# Show script info
python -m vcdecomp info script.scr

# Disassemble to readable assembly
python -m vcdecomp disasm script.scr > output.asm

# Launch GUI
python -m vcdecomp gui [script.scr]

# Export global variable symbols
python -m vcdecomp symbols script.scr -o output.json -f json
```

### Validation System (Recompilation Testing)
```bash
# Validate single file by recompiling and comparing bytecode
python -m vcdecomp validate original.scr decompiled.c
python -m vcdecomp validate original.scr decompiled.c --report-file report.html

# Batch validation with parallelization
python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --jobs 8

# Regression testing - save baseline and detect changes
python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --save-baseline
python -m vcdecomp validate-batch --input-dir decompiled/ --original-dir scripts/ --regression --report-file regression.json
```

### Running Tests
```bash
# Run all tests
PYTHONPATH=. python -m pytest vcdecomp/tests/ -v

# Run specific test suite
PYTHONPATH=. python -m pytest vcdecomp/tests/test_structure_patterns.py -v

# Run with coverage
PYTHONPATH=. python -m pytest vcdecomp/tests/ --cov=vcdecomp.core.ir.structure

# Run integration tests (end-to-end decompilation)
PYTHONPATH=. python -m pytest vcdecomp/tests/test_end_to_end_decompilation.py -v
```

### Compiling Scripts (Original Compiler)
The original SCMP compiler toolchain is in `original-resources/compiler/`. Due to WSL/Windows interop limitations, use the Python wrapper:

```bash
# Compile tt.c (the test file in compiler directory)
py -3 compile_simple.py

# This compiles: original-resources/compiler/tt.c
# Output: original-resources/compiler/tt.scr (60KB)
# Takes: ~2-3 seconds
```

**To compile other files:**
1. Copy your `.c` file to `original-resources/compiler/`
2. Edit `compile.bat` to reference your file:
   ```batch
   "%~dp0scmp" "your_file.c" "your_file.scr" "your_file.h"
   ```
3. Run: `py -3 compile_simple.py`

**Alternative (manual):** Double-click `compile.bat` in Windows Explorer

**See:** [COMPILING.md](COMPILING.md) for detailed documentation

**Compilation pipeline:**
```
.c → [SPP preprocessor] → [SCC compiler] → [SASM assembler] → .scr
```

## Architecture Overview

### Decompilation Pipeline
The decompilation process follows these stages:

1. **Parsing** (`vcdecomp/parsing/`) - Parse `.scr` file format
   - Header, data segment, code segment, XFN table
   - 12-byte instructions: opcode + 2 arguments

2. **Disassembly** (`vcdecomp/core/disasm/`) - Convert bytecode to assembly
   - 150 opcodes (arithmetic, control flow, stack ops)
   - Runtime vs compiler opcode variants

3. **IR Construction** (`vcdecomp/core/ir/`)
   - **CFG** (`cfg.py`) - Control flow graph construction
   - **Stack Lifting** (`stack_lifter.py`) - Stack simulation, value tracking
   - **SSA** (`ssa.py`) - Static single assignment form with phi nodes

4. **Expression Building** (`vcdecomp/core/ir/expr.py`)
   - Convert stack operations to C expressions
   - Type inference from opcodes (IADD vs FADD)

5. **Structure Analysis** (`vcdecomp/core/ir/structure/`)
   - **patterns/** - Detect if/else, switch/case, loops
   - **analysis/** - CFG analysis, condition extraction, value tracing
   - **emit/** - Code generation and formatting

6. **Validation** (`vcdecomp/validation/`)
   - Recompile decompiled code and compare bytecode
   - Bytecode difference categorization (semantic vs non-semantic)
   - Regression testing with baselines

### Structure Module (Recently Refactored)
The `vcdecomp/core/ir/structure/` package was refactored from 3,250 lines into 17 focused modules:

```
structure/
├── orchestrator.py          # Main entry points
├── patterns/                # Pattern detection
│   ├── if_else.py          # If/else, early return, short-circuit
│   ├── switch_case.py      # Switch/case detection
│   └── loops.py            # For-loop detection
├── analysis/               # Control flow analysis
│   ├── flow.py            # CFG traversal and analysis
│   ├── condition.py       # Condition extraction
│   ├── value_trace.py     # Value tracing through CFG
│   └── variables.py       # Variable collection
├── emit/                   # Code generation
│   ├── block_formatter.py # Block-level formatting
│   └── code_emitter.py    # Final code rendering
└── utils/                  # Utilities
    └── helpers.py         # Helper functions
```

## Key Technical Details

### .SCR File Format
```
1. Header        - Entry point, function parameters
2. Data Segment  - Constants, strings (4-byte aligned, little-endian)
3. Global Ptrs   - Offsets to global variables
4. Code Segment  - Instructions (12 bytes: opcode + 2x int32 args)
5. XFN Table     - External functions (28 bytes/entry)
```

### Instruction Set
- **Arithmetic**: ADD, SUB, MUL, DIV, MOD, NEG, INC, DEC
- **Type prefixes**: C=char, S=short, I=int, F=float, D=double
- **Control flow**: JMP, JZ, JNZ, CALL, RET, XCALL (external calls)
- **Stack**: PUSH, POP, ASP, SSP, LCP, GCP, LLD, GLD
- **Conversions**: CTOI, ITOF, FTOD, etc.

### External Functions
Scripts call 700+ engine functions with `SC_*` prefix:
- `SC_P_Create()` - Create player
- `SC_NOD_Get()` - Get object
- `SC_SND_PlaySound3D()` - Play 3D sound
- `SC_message()` - Debug message

Function prototypes are in `original-resources/h/sc_global.h`.

## Important Constraints

### Compilation & Validation
- **Compiler usage:** Use `py -3 compile_simple.py` to compile scripts (see compilation section above)
- **WSL limitation:** Cannot invoke Windows .exe files directly with arguments - use the Python wrapper
- **ALWAYS test decompiled output** by recompiling with the original compiler (SCMP.exe)
- Use `validate` command to compare bytecode differences
- Focus on reducing **semantic differences** (different behavior)
- **Non-semantic differences** (different bytecode, same behavior) are acceptable:
  - Register allocation changes
  - Instruction ordering (if equivalent)
  - Constant representation differences

### Code Quality
- Tests have 100% coverage on core modules - maintain this
- Use type hints (currently 87% coverage)
- Average module size: ~229 lines (was 3,250 before refactoring)
- Zero circular dependencies in structure package

### Pattern Detection Accuracy
When modifying control flow reconstruction:
1. Test on `Compiler-testruns/` scripts (known source + bytecode pairs)
2. Verify switch/case jump tables are correctly identified
3. Ensure for-loop patterns (init, condition, increment) are detected
4. Check early return patterns don't break if/else chains

## Clean Decompilation Output

### Understanding Debug Output
The decompiler outputs DEBUG lines to show its internal analysis process:
- `DEBUG: Entry point = 9054` - Entry point identification
- `DEBUG FieldTracker: ...` - Struct field detection
- `DEBUG PNT: SUCCESS ...` - Pointer-to-field pattern recognition
- `DEBUG SWITCH: ...` - Switch/case detection analysis
- `DEBUG Propagate: ...` - Type propagation iterations

These lines are helpful for debugging the decompiler itself, but clutter the decompiled code.

### Removing Debug Output

**Real-world example from TUNNELS01:**
```bash
# Original decompilation (with debug)
py -3 -m vcdecomp structure level.scr > level_decompiled.c
# Result: 9,825 lines (2,617 DEBUG lines + 7,208 code lines)

py -3 -m vcdecomp structure player.scr > player_decompiled.c
# Result: 4,045 lines (2,017 DEBUG lines + 2,028 code lines)

# Clean decompilation (debug removed)
py -3 -m vcdecomp structure level.scr | python -c "import sys; sys.stdout.writelines(line for line in sys.stdin if not line.startswith('DEBUG'))" > level_clean.c
# Result: 1,845 lines (clean code only)

py -3 -m vcdecomp structure player.scr | python -c "import sys; sys.stdout.writelines(line for line in sys.stdin if not line.startswith('DEBUG'))" > player_clean.c
# Result: 401 lines (clean code only)
```

### Batch Processing Multiple Files

**Python script for batch clean decompilation:**
```python
import os
import subprocess
from pathlib import Path

def clean_decompile(scr_file, output_dir):
    """Decompile .scr file and remove DEBUG lines"""
    scr_path = Path(scr_file)
    output_file = Path(output_dir) / f"{scr_path.stem}_clean.c"

    # Run decompiler
    result = subprocess.run(
        ['python', '-m', 'vcdecomp', 'structure', str(scr_path)],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    # Filter DEBUG lines
    clean_lines = [line for line in result.stdout.splitlines(keepends=True)
                   if not line.startswith('DEBUG')]

    # Write clean output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)

    print(f"Decompiled {scr_path.name} -> {output_file.name}")
    print(f"  Original: {len(result.stdout.splitlines())} lines")
    print(f"  Clean: {len(clean_lines)} lines")

# Example usage:
# clean_decompile('level.scr', 'output/')
# clean_decompile('player.scr', 'output/')
```

### On Windows (PowerShell)
```powershell
# Single file
py -3 -m vcdecomp structure script.scr | Where-Object { -not $_.StartsWith("DEBUG") } > output_clean.c

# Multiple files
Get-ChildItem *.scr | ForEach-Object {
    $output = "$($_.BaseName)_clean.c"
    py -3 -m vcdecomp structure $_.Name | Where-Object { -not $_.StartsWith("DEBUG") } > $output
}
```

### File Size Comparison

From TUNNELS01 analysis:
| File | With DEBUG | Clean | Reduction |
|------|-----------|-------|-----------|
| level.scr | 925 KB | 50 KB | 94.6% smaller |
| player.scr | 317 KB | 15 KB | 95.3% smaller |

**Recommendation:** Always generate clean versions for code analysis, reconstruction, or recompilation. Keep debug versions only when troubleshooting decompiler issues.

## Common Development Tasks

### Adding New Opcode Support
1. Update `vcdecomp/core/disasm/opcodes.py`
2. Add handling in `vcdecomp/core/ir/stack_lifter.py`
3. Update expression formatting in `vcdecomp/core/ir/expr.py`
4. Add test cases in `vcdecomp/tests/`

### Improving Control Flow Detection
1. Modify pattern detection in `vcdecomp/core/ir/structure/patterns/`
2. Update CFG analysis in `vcdecomp/core/ir/structure/analysis/`
3. Test with known scripts in `Compiler-testruns/`
4. Run regression tests: `PYTHONPATH=. python -m pytest vcdecomp/tests/test_regression_baseline.py`
5. Validate output compiles correctly: `python -m vcdecomp validate original.scr decompiled.c`

### Adding New External Function Signatures
1. Update `original-resources/h/sc_global.h` or relevant header
2. Rebuild header database: `vcdecomp/core/headers/database.py`
3. Test function call detection in decompiled output

## Test Data

### Test Scripts
- `Compiler-testruns/` - Original C source + compiled .scr files with debug info
- `script-folders/` - Real game mission scripts (production code)

### Known Good Test Cases
- `testrun1/tdm.c` - Team deathmatch script
- `testrun1/hitable.c` - Object hit detection
- `testrun1/camping_bot.c` - AI camping behavior

## Documentation

### Essential Reading
- `docs/decompilation_guide.md` - Decompilation workflow
- `docs/structure_refactoring.md` - Structure module architecture
- `docs/Scripting_SDK.txt` - Official Vietcong SDK (380KB, definitive reference)

### Technical Analysis
- `docs/SCC_TECHNICAL_ANALYSIS.md` - Compiler analysis
- `docs/SASM_TECHNICAL_ANALYSIS.md` - Assembler analysis
- `docs/SPP_TECHNICAL.md` - Preprocessor analysis

## Common Pitfalls

1. **Don't trust raw constant values** - The decompiler sometimes misinterprets data segment values
2. **Global variable detection is heuristic** - Verify `GADR data[X]` references manually
3. **Type inference is incomplete** - Some variables remain `dword` (unknown type)
4. **Macro expansion** - Original macros are lost (preprocessor expanded them)
5. **Optimization artifacts** - Original compiler generates redundant code

## Git Workflow

- Main branch: `main`
- Recent major work: Validation subsystem, structure refactoring
- Auto-Claude tasks stored in `.auto-claude/worktrees/` (can ignore)
- Don't commit `__pycache__/` or `.pyc` files (already in `.gitignore`)
