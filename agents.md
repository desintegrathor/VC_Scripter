# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VC-Script-Decompiler** decompiles Vietcong (2003) game scripts from `.scr` bytecode back to readable C-like source code. The scripts use a proprietary C-like language with external engine functions.

### Project Philosophy & Goals

This is a **one-time-use tool** for reconstructing a finite set of Vietcong game scripts. The decompiled output will later be further refined with AI assistance, so the decompiler's job is to produce the most **correct and accurate** output possible.

**Critical Guidelines:**
- **Evidence-based decisions:** Use hard evidence as extensively as possible before making any inferences
- **Conservative naming:** Do NOT rename functions or variables unless there is **100% confidence** based on hard evidence. Generic names (`func_001`, `var_42`) are far better than incorrect names
- **Acceptable guesses:** Only guess things that are critical for logical function (e.g., data types, control flow structures)
- **Unacceptable guesses:** Never guess semantic meaning (function purposes, variable meanings) without concrete evidence
- **Err on the side of caution:** When uncertain, keep the generic/raw representation

**Evidence hierarchy (strongest to weakest):**
1. String literals used in context (e.g., `SC_message("player created")` near a variable)
2. External function signatures from SDK headers (`sc_global.h`)
3. Consistent usage patterns across multiple call sites
4. Type constraints from opcodes (IADD = int, FADD = float)
5. Structural patterns (loop counters, array indices)

**Inspiration from Ghidra decompiler:**
Look often into the Ghidra decompiler source to find how a state-of-the-art decompiler works. Take what you can from it.

**Local copy (for quick reference):** `ghidra-decompiler-src/` - Contains the C++ decompiler core (~7.3 MB, 236 files)

**Key files for control flow analysis:**
| File | Purpose |
|------|---------|
| `block.hh/cc` | CFG data structures |
| `blockaction.hh/cc` | Loop detection, DAG-based structuring |
| `flow.hh/cc` | Control flow generation from bytecode |
| `jumptable.hh/cc` | Switch/case jump table recovery |
| `heritage.hh/cc` | SSA form generation |
| `printc.hh/cc` | C code emission |

**Full Ghidra repository:** `C:\Users\flori\Documents\GitHub\ghidra`

## Essential Commands

### Running the Decompiler
```bash
# Decompile a script (default: Ghidra-style collapse + incremental heritage SSA)
py -3 -m vcdecomp structure script.scr > output.c

# Decompile with flat mode (disable collapse algorithm)
py -3 -m vcdecomp structure --no-collapse script.scr > output.c

# Decompile with DEBUG output (for development/debugging)
py -3 -m vcdecomp structure --debug script.scr > output.c 2>debug.log

# Decompile with legacy SSA (faster but lower quality)
py -3 -m vcdecomp structure --legacy-ssa script.scr > output.c

# Show script info
py -3 -m vcdecomp info script.scr

# Disassemble to readable assembly
py -3 -m vcdecomp disasm script.scr > output.asm

# Launch GUI
py -3 -m vcdecomp gui [script.scr]

# Export global variable symbols
py -3 -m vcdecomp symbols script.scr -o output.json -f json

# Aggregate external function signatures from multiple .scr files
py -3 -m vcdecomp xfn-aggregate scripts/ --format summary
py -3 -m vcdecomp xfn-aggregate scripts/ --format sdk -o functions.json
```

### Testing Decompiler Output (Visual Comparison)

Testing is done by **visual comparison** of decompiled output against original source code.

**Test 1 - Simple test file (tt.scr):**
```bash
# Decompile
py -3 -m vcdecomp structure decompiler_source_tests\test1\tt.scr > decompiler_source_tests\test1\tt_decompiled.c

# Compare decompiled output to original source
# Original: decompiler_source_tests\test1\tt.c
# Decompiled: decompiler_source_tests\test1\tt_decompiled.c
```

**Test 2 - Full level script (LEVEL.SCR):**
```bash
# Decompile
py -3 -m vcdecomp structure decompiler_source_tests\test3\LEVEL.SCR > decompiler_source_tests\test3\LEVEL_decompiled.c

# Compare decompiled output to original source
# Original: decompiler_source_tests\test3\LEVEL.C
# Decompiled: decompiler_source_tests\test3\LEVEL_decompiled.c
```

**Testing workflow:**
1. Decompile the `.scr` file, saving output to `*_decompiled.c` in the same folder
2. Always overwrite the old decompiled file if one exists
3. Compare the decompiled code to the original source visually
4. Examine differences and identify what went wrong during decompilation
5. Find the root cause in the decompiler code and fix it
6. Check `ghidra-decompiler-src/` for how Ghidra handles similar cases
7. Goal: improve the decompiler to reliably decompile any script

### Running Tests
```bash
# Run all tests (Windows)
py -3 -m pytest vcdecomp/tests/ -v

# Run specific test suite
py -3 -m pytest vcdecomp/tests/test_structure_patterns.py -v

# Run a single test
py -3 -m pytest vcdecomp/tests/test_structure_patterns.py::TestDetectForLoop::test_simple_for_loop -v

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
# Output: original-resources/compiler/tt.scr
```

**To compile other files:**
1. Copy your `.c` file to `original-resources/compiler/`
2. Edit `compile.bat` to reference your file
3. Run: `py -3 compile_simple.py`

**See:** [COMPILING.md](COMPILING.md) for detailed documentation

**Compilation pipeline:**
```
.c → [SPP preprocessor] → [SCC compiler] → [SASM assembler] → .scr
```

## Architecture Overview

### Decompilation Pipeline
The decompilation process follows these stages:

1. **Parsing** (`vcdecomp/core/loader/`) - Parse `.scr` file format
   - Header, data segment, code segment, XFN table
   - 12-byte instructions: opcode + 2 arguments

2. **Disassembly** (`vcdecomp/core/disasm/`) - Convert bytecode to assembly
   - 150 opcodes (arithmetic, control flow, stack ops)
   - Runtime vs compiler opcode variants

3. **IR Construction** (`vcdecomp/core/ir/`)
   - **CFG** (`cfg.py`) - Control flow graph construction with natural loop detection
   - **Stack Lifting** (`stack_lifter.py`) - Stack simulation, value tracking
   - **SSA** (`ssa.py`) - Static single assignment form with phi nodes

4. **Expression Building** (`vcdecomp/core/ir/expr.py`)
   - Convert stack operations to C expressions
   - Type inference from opcodes (IADD vs FADD)

5. **Structure Analysis** (`vcdecomp/core/ir/structure/`)
   - **patterns/** - Detect if/else, switch/case, loops
   - **analysis/** - CFG analysis, condition extraction, value tracing
   - **blocks/** - Hierarchical block structure (Ghidra-style)
   - **collapse/** - Iterative structure collapse engine
   - **emit/** - Code generation and formatting

### Structure Module Architecture

The `vcdecomp/core/ir/structure/` package has two code generation paths:

**Flat Mode (Default)** - Pattern-based detection with linear block iteration:
```
structure/
├── orchestrator.py          # Main entry points, coordinates both modes
├── patterns/                # Pattern detection
│   ├── if_else.py          # If/else, early return, short-circuit
│   ├── switch_case.py      # Switch/case detection
│   └── loops.py            # For-loop detection
├── analysis/               # Control flow analysis
│   ├── flow.py            # CFG traversal, natural loop detection
│   ├── condition.py       # Condition extraction
│   ├── value_trace.py     # Value tracing through CFG
│   └── variables.py       # Variable collection
└── emit/
    ├── block_formatter.py # Block-level formatting
    └── code_emitter.py    # Final code rendering
```

**Collapse Mode** (`--use-collapse`) - Ghidra-style hierarchical block collapse:
```
structure/
├── blocks/
│   └── hierarchy.py       # BlockGraph, StructuredBlock types
├── collapse/
│   ├── engine.py         # CollapseStructure iterative algorithm
│   └── rules.py          # Collapse rules (BlockCat, ProperIf, etc.)
└── emit/
    └── hierarchical_emitter.py  # Emits from collapsed hierarchy
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

### Compiling Scripts
- **Compiler usage:** Use `py -3 compile_simple.py` to compile scripts
- **WSL limitation:** Cannot invoke Windows .exe files directly with arguments - use the Python wrapper

### Pattern Detection Accuracy
When modifying control flow reconstruction:
1. Test on `decompiler_source_tests/` scripts (known source + bytecode pairs)
2. Verify switch/case jump tables are correctly identified
3. Ensure for-loop patterns (init, condition, increment) are detected
4. Check early return patterns don't break if/else chains
5. Run: `py -3 -m pytest vcdecomp/tests/test_structure_patterns.py -v`
6. Visually compare decompiled output against original source files

## Command-Line Flags Reference

### Global Flags (all commands)
| Flag | Description |
|------|-------------|
| `--variant {auto,runtime,compiler}` | Opcode map selection (default: auto-detect) |
| `--ignore-mp` | Ignore multiplayer-only functions (SC_MP_*); SP-only mode |

### Structure Command Flags (`structure`)

**Output Control:**
| Flag | Description | Default |
|------|-------------|---------|
| `--debug` / `-d` | Enable DEBUG output to stderr | Off |
| `--verbose` / `-v` | Same as --debug (for future expansion) | Off |
| `--dump-type-evidence [FILE]` | Dump type inference evidence as JSON (stdout with "-") | Off |

**Algorithm Selection:**
| Flag | Description | Default |
|------|-------------|---------|
| `--no-collapse` | Disable Ghidra-style hierarchical collapse (use flat mode) | Off (collapse enabled) |
| `--legacy-ssa` | Use legacy single-pass SSA (faster but lower quality) | Off (uses incremental heritage SSA) |

**Feature Toggles (disable features):**
| Flag | Description | Default |
|------|-------------|---------|
| `--no-simplify` | Disable expression simplification (constant folding, algebraic identities) | Enabled |
| `--no-array-detection` | Disable array detection (LoadGuard system) | Enabled |
| `--no-bidirectional-types` | Disable bidirectional type inference | Enabled |

**Debug Output for Subsystems:**
| Flag | Description |
|------|-------------|
| `--debug-simplify` | Debug output for simplification rules |
| `--debug-array-detection` | Debug output for array detection |
| `--debug-type-inference` | Debug output for type inference |

### XFN-Aggregate Command Flags (`xfn-aggregate`)
| Flag | Description | Default |
|------|-------------|---------|
| `-f/--format {summary,sdk,json}` | Output format | summary |
| `-o/--output FILE` | Output file path (required for sdk/json) | - |
| `--no-recursive` | Do not scan subdirectories | Recursive |
| `--merge-sdk` | Merge with existing SDK functions.json | - |
| `--sdk-path FILE` | Path to SDK functions.json | vcdecomp/sdk/data/functions.json |

### Symbols Command Flags (`symbols`)
| Flag | Description |
|------|-------------|
| `-o/--output FILE` | Output file path (required) |
| `-f/--format {json,header,markdown}` | Export format (default: json) |

### Understanding Debug Output
When `--debug` is enabled, DEBUG lines (written to stderr) show internal analysis:
- `DEBUG: Entry point = 9054` - Entry point identification
- `DEBUG FieldTracker: ...` - Struct field detection
- `DEBUG SWITCH: ...` - Switch/case detection analysis
- `DEBUG COLLAPSE: ...` - Hierarchical collapse iterations

## Common Development Tasks

### Code Organization & Module Size
- **Avoid large monolithic modules**: Keep individual Python modules under **1500 lines** for better maintainability
- When a module grows too large, split it into smaller, focused modules with clear responsibilities
- Prefer multiple small modules over one large file

### Adding New Opcode Support
1. Update `vcdecomp/core/disasm/opcodes.py`
2. Add handling in `vcdecomp/core/ir/stack_lifter.py`
3. Update expression formatting in `vcdecomp/core/ir/expr.py`
4. Add test cases in `vcdecomp/tests/`

### Improving Control Flow Detection
1. Modify pattern detection in `vcdecomp/core/ir/structure/patterns/`
2. Update CFG analysis in `vcdecomp/core/ir/structure/analysis/`
3. Test with known scripts in `decompiler_source_tests/`
4. Run: `py -3 -m pytest vcdecomp/tests/test_structure_patterns.py -v`

### Adding Collapse Rules (Ghidra-style)
1. Add rule class in `vcdecomp/core/ir/structure/collapse/rules.py`
2. Implement `matches()` and `apply()` methods
3. Register in `DEFAULT_RULES` list
4. Test with `vcdecomp/tests/test_collapse_rules.py`

## Test Data

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
- `vcdecomp/core/ir/structure/README.md` - Detailed structure package docs

### Technical Analysis
- `docs/SCC_TECHNICAL_ANALYSIS.md` - Compiler analysis
- `docs/SASM_TECHNICAL_ANALYSIS.md` - Assembler analysis
- `docs/SPP_TECHNICAL.md` - Preprocessor analysis

## Common Pitfalls

1. **Don't trust raw constant values** - The decompiler sometimes misinterprets data segment values
2. **Global variable detection is heuristic** - Verify `GADR data[X]` references manually
3. **Type inference is incomplete** - Some variables remain `dword` (unknown type)
4. **Macro expansion** - Original macros are lost (preprocessor expanded them)
5. **Loop body detection** - Natural loops may have incomplete body sets for complex CFGs

## Git Workflow

- Main branch: `main`
- Recent major work: Structure refactoring, collapse mode
- Auto-Claude tasks stored in `.auto-claude/worktrees/` (can ignore)
