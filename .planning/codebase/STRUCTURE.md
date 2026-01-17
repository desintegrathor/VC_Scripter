# Codebase Structure

**Analysis Date:** 2026-01-17

## Directory Layout

```
VC_Scripter/
├── vcdecomp/                    # Main Python package
│   ├── core/                    # Core decompilation logic
│   ├── parsing/                 # Binary file parsing
│   ├── validation/              # Validation subsystem
│   ├── gui/                     # PyQt6 GUI
│   └── tests/                   # Test suite
├── original-resources/          # Vietcong SDK resources
│   ├── compiler/                # Original compiler (SCMP.exe)
│   ├── h/                       # C header files (700+ functions)
│   └── level scripts/           # Example game scripts
├── script-folders/              # Real game mission scripts
├── docs/                        # Documentation
├── .planning/                   # GSD planning workspace
├── .validation_cache/           # Validation cache
└── test_*.py                    # Root-level validation tests
```

## Directory Purposes

**vcdecomp/**
- Purpose: Main Python package for decompiler
- Contains: Core modules, CLI entry point, tests
- Key files: `__main__.py` (CLI), `__init__.py` (version)

**vcdecomp/core/**
- Purpose: Core decompilation pipeline
- Contains: Loaders, disassemblers, IR builders, headers
- Key files: `constants.py`, `structures.py`, `script_type_detector.py`

**vcdecomp/core/loader/**
- Purpose: Binary .SCR file loading and parsing
- Contains: SCRFile class, data segment parser, instruction loader
- Key files: `scr_loader.py` (362 lines), `data_strings.py`

**vcdecomp/core/disasm/**
- Purpose: Bytecode disassembly
- Contains: Disassembler, opcode tables (runtime/compiler variants)
- Key files: `disassembler.py`, `opcodes.py`, `runtime_opcode_table.py`

**vcdecomp/core/headers/**
- Purpose: External function signature database
- Contains: C header parser, function database, constant detector
- Key files: `database.py`, `parser.py`, `detector.py`, `data/` (JSON databases)

**vcdecomp/core/ir/**
- Purpose: Intermediate representation construction
- Contains: CFG builder, stack lifter, SSA builder, expression formatter
- Key files: `cfg.py`, `stack_lifter.py`, `ssa.py`, `expr.py` (2571 lines)

**vcdecomp/core/ir/structure/**
- Purpose: Structured control flow reconstruction (refactored package)
- Contains: Pattern detection, control flow analysis, code emission
- Key files: `orchestrator.py` (1058 lines), `patterns/`, `analysis/`, `emit/`

**vcdecomp/core/ir/structure/patterns/**
- Purpose: Detect high-level control flow patterns
- Contains: If/else, switch/case, loop detection
- Key files: `if_else.py`, `switch_case.py`, `loops.py`, `models.py`

**vcdecomp/core/ir/structure/analysis/**
- Purpose: Control flow graph analysis utilities
- Contains: Flow analysis, condition extraction, value tracing, variable collection
- Key files: `flow.py`, `condition.py`, `value_trace.py`, `variables.py`

**vcdecomp/core/ir/structure/emit/**
- Purpose: Code generation and formatting
- Contains: Block formatter, code emitter
- Key files: `block_formatter.py`, `code_emitter.py`

**vcdecomp/parsing/**
- Purpose: Binary file format parsing
- Contains: Header parser, symbol database
- Key files: `header_parser.py`, `symbol_db.py`

**vcdecomp/validation/**
- Purpose: Round-trip validation system
- Contains: Compiler wrapper, bytecode comparator, cache, regression tester
- Key files: `validator.py`, `compiler_wrapper.py`, `bytecode_compare.py`, `cache.py`, `regression.py`

**vcdecomp/gui/**
- Purpose: PyQt6 graphical interface
- Contains: Main window, validation view, widgets
- Key files: `main_window.py`, `views/validation_view.py`, `widgets/difference_widgets.py`

**vcdecomp/tests/**
- Purpose: Unit and integration tests
- Contains: Pattern tests, analysis tests, validation tests, end-to-end tests
- Key files: `test_structure_patterns.py`, `test_validation_workflow.py`, `test_end_to_end_decompilation.py`

**original-resources/**
- Purpose: Vietcong SDK and compiler
- Contains: Original compiler binaries, headers, example scripts
- Key files: `compiler/SCMP.exe`, `h/sc_global.h`, `Scripting_SDK.txt` (380KB)

**docs/**
- Purpose: Project documentation
- Contains: Technical analysis, guides, architecture docs
- Key files: `decompilation_guide.md`, `structure_refactoring.md`, `validation_system.md`

**.planning/**
- Purpose: GSD planning and codebase mapping
- Contains: Codebase analysis documents
- Key files: `codebase/ARCHITECTURE.md`, `codebase/STRUCTURE.md`

## Key File Locations

**Entry Points:**
- `vcdecomp/__main__.py`: CLI entry point with argparse commands
- `vcdecomp/gui/main_window.py`: GUI entry point with PyQt6

**Configuration:**
- `.gitignore`: Excludes __pycache__, .pyc, Auto Claude files
- `CLAUDE.md`: Project instructions for Claude Code
- `vcdecomp/core/constants.py`: Game constant definitions

**Core Logic:**
- `vcdecomp/core/loader/scr_loader.py`: .SCR file format parser
- `vcdecomp/core/ir/cfg.py`: Control flow graph builder
- `vcdecomp/core/ir/ssa.py`: SSA construction
- `vcdecomp/core/ir/expr.py`: Expression formatter (2571 lines)
- `vcdecomp/core/ir/structure/orchestrator.py`: Main decompilation orchestrator

**Testing:**
- `vcdecomp/tests/test_*.py`: 10+ test modules
- `test_*.py` (root): 20+ validation test files
- `.pytest_cache/`: Pytest cache

## Naming Conventions

**Files:**
- `snake_case.py`: Python modules
- `UPPERCASE.md`: Documentation files
- `.scr`: Vietcong bytecode files
- `.c`: C source files

**Directories:**
- `lowercase/`: Package directories
- `PascalCase/` or `CamelCase/`: Not used

**Classes:**
- `PascalCase`: SCRFile, BasicBlock, SSAFunction

**Functions:**
- `snake_case`: build_cfg(), lift_function(), format_structured_function_named()
- `_leading_underscore`: Private/internal functions

## Where to Add New Code

**New Opcode Support:**
- Primary code: `vcdecomp/core/disasm/opcodes.py` (add opcode definition)
- Stack handling: `vcdecomp/core/ir/stack_lifter.py` (add lifting logic)
- Expression formatting: `vcdecomp/core/ir/expr.py` (add formatting)
- Tests: `vcdecomp/tests/test_integration_pipeline.py`

**New Control Flow Pattern:**
- Pattern model: `vcdecomp/core/ir/structure/patterns/models.py`
- Detection logic: New file in `vcdecomp/core/ir/structure/patterns/`
- Emission: `vcdecomp/core/ir/structure/emit/code_emitter.py`
- Tests: `vcdecomp/tests/test_structure_patterns.py`

**New Analysis Pass:**
- Implementation: New file in `vcdecomp/core/ir/structure/analysis/`
- Export: `vcdecomp/core/ir/structure/analysis/__init__.py`
- Tests: `vcdecomp/tests/test_structure_analysis.py`

**New External Function Signatures:**
- Headers: `original-resources/h/sc_global.h` (add prototypes)
- Database rebuild: `vcdecomp/core/headers/database.py`
- Tests: Verify XCALL resolution in decompiled output

**New CLI Command:**
- Implementation: `vcdecomp/__main__.py` (add subparser and cmd_* function)
- Help text: Update argparse epilog

**New GUI Feature:**
- Widget: `vcdecomp/gui/widgets/`
- View: `vcdecomp/gui/views/`
- Main window: `vcdecomp/gui/main_window.py`

**New Validation Feature:**
- Core logic: `vcdecomp/validation/`
- Integration: `vcdecomp/validation/validator.py`
- Tests: `vcdecomp/tests/validation/`

## Special Directories

**vcdecomp/core/ir/archive/**
- Purpose: Archived old monolithic modules
- Generated: No
- Committed: Yes (for reference)

**vcdecomp/core/headers/data/**
- Purpose: JSON databases of function signatures
- Generated: Yes (from C headers)
- Committed: Yes

**.validation_cache/**
- Purpose: Cache validation results
- Generated: Yes (by validation system)
- Committed: No (.gitignore)

**.pytest_cache/**
- Purpose: Pytest cache files
- Generated: Yes
- Committed: No (.gitignore)

**__pycache__/**
- Purpose: Python bytecode cache
- Generated: Yes
- Committed: No (.gitignore)

**.auto-claude/**
- Purpose: Auto Claude task management
- Generated: Yes (by Auto Claude extension)
- Committed: No (.gitignore)

**decompilation_work_folder/**
- Purpose: Temporary decompilation outputs
- Generated: Yes (manual)
- Committed: No (.gitignore)

**original-resources/compiler/inc/**
- Purpose: Include files for compiler (headers)
- Generated: No
- Committed: Yes

---

*Structure analysis: 2026-01-17*
