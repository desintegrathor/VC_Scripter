# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VC-Script-Decompiler** decompiles Vietcong (2003) game scripts from `.scr` bytecode back to readable C-like source code. The scripts use a proprietary C-like language with external engine functions.

## Essential Commands

### Running the Decompiler
```bash
# Decompile a script (default: clean output with best quality SSA)
python -m vcdecomp structure script.scr > output.c

# Decompile with DEBUG output (for development/debugging)
python -m vcdecomp structure --debug script.scr > output.c 2>debug.log

# Decompile with legacy SSA (faster but lower quality)
python -m vcdecomp structure --legacy-ssa script.scr > output.c

# Show script info
python -m vcdecomp info script.scr

# Disassemble to readable assembly
python -m vcdecomp disasm script.scr > output.asm

# Launch GUI
python -m vcdecomp gui [script.scr]

# Export global variable symbols
python -m vcdecomp symbols script.scr -o output.json -f json

# Aggregate external function signatures from multiple .scr files
python -m vcdecomp xfn-aggregate scripts/ --format summary
python -m vcdecomp xfn-aggregate scripts/ --format sdk -o functions.json
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
# Run all tests (Windows)
py -3 -m pytest vcdecomp/tests/ -v

# Run specific test suite
py -3 -m pytest vcdecomp/tests/test_structure_patterns.py -v

# Run with coverage
py -3 -m pytest vcdecomp/tests/ --cov=vcdecomp.core.ir.structure

# Run integration tests (end-to-end decompilation)
py -3 -m pytest vcdecomp/tests/test_end_to_end_decompilation.py -v
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
1. Test on `decompiler_source_tests/` scripts (known source + bytecode pairs)
2. Verify switch/case jump tables are correctly identified
3. Ensure for-loop patterns (init, condition, increment) are detected
4. Check early return patterns don't break if/else chains

## Output Verbosity

The `structure` command produces **clean output by default** with the best quality SSA analysis.

| Flag | Description | Use Case |
|------|-------------|----------|
| (none) | Clean output, best SSA | **Default - recommended for recompilation** |
| `--debug` / `-d` | Enable DEBUG to stderr | Debugging decompiler issues |
| `--verbose` / `-v` | Same as --debug | Future: extended diagnostics |
| `--legacy-ssa` | Use old SSA algorithm | Faster, but lower quality output |

### Quick Examples
```bash
# Default: clean output with best quality (RECOMMENDED)
py -3 -m vcdecomp structure script.scr > output.c

# Debug output for development
py -3 -m vcdecomp structure --debug script.scr > output.c 2>debug.log

# Legacy mode (faster but lower quality)
py -3 -m vcdecomp structure --legacy-ssa script.scr > output.c
```

### Understanding Debug Output
When `--debug` is enabled, DEBUG lines (written to stderr) show internal analysis:
- `DEBUG: Entry point = 9054` - Entry point identification
- `DEBUG FieldTracker: ...` - Struct field detection
- `DEBUG PNT: SUCCESS ...` - Pointer-to-field pattern recognition
- `DEBUG SWITCH: ...` - Switch/case detection analysis
- `DEBUG Propagate: ...` - Type propagation iterations

### Batch Processing
```bash
# Batch decompile all .scr files (default is already clean)
for f in *.scr; do
    py -3 -m vcdecomp structure "$f" > "${f%.scr}.c"
done
```

```powershell
# PowerShell batch
Get-ChildItem *.scr | ForEach-Object {
    py -3 -m vcdecomp structure $_.Name > "$($_.BaseName).c"
}
```

## Common Development Tasks

### Adding New Opcode Support
1. Update `vcdecomp/core/disasm/opcodes.py`
2. Add handling in `vcdecomp/core/ir/stack_lifter.py`
3. Update expression formatting in `vcdecomp/core/ir/expr.py`
4. Add test cases in `vcdecomp/tests/`

### Improving Control Flow Detection
1. Modify pattern detection in `vcdecomp/core/ir/structure/patterns/`
2. Update CFG analysis in `vcdecomp/core/ir/structure/analysis/`
3. Test with known scripts in `decompiler_source_tests/`
4. Run regression tests: `py -3 -m pytest vcdecomp/tests/test_regression_baseline.py`
5. Validate output compiles correctly: `py -3 -m vcdecomp validate original.scr decompiled.c`

### Adding New External Function Signatures
1. Update `original-resources/h/sc_global.h` or relevant header
2. Rebuild header database: `vcdecomp/core/headers/database.py`
3. Test function call detection in decompiled output

## Test Data

### Test Scripts
- `decompiler_source_tests/` - Original C source + compiled .scr files for validation:
  - `test1/tt.c` - General test file used by `compile_simple.py`
  - `test2/tdm.c` - Team deathmatch script
  - `test3/LEVEL.C` - Full level script
- `script-folders/` - Real game mission scripts (production code)

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
