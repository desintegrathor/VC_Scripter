# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VC-Script-Decompiler** decompiles Vietcong (2003) game scripts from `.scr` bytecode back to readable C-like source code. The scripts use a proprietary C-like language with external engine functions.

## Essential Commands

### Running the Decompiler
```bash
# Decompile a script (full structured output)
python -m vcdecomp structure script.scr > output.c

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

### Original Compiler (for validation)
```bash
# Located in: original-resources/compiler/
# Compile C source to .scr bytecode
cd original-resources/compiler
./scmp.exe source.c output.scr header.h
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

### Validation System
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
