# Architecture

**Analysis Date:** 2026-01-17

## Pattern Overview

**Overall:** Multi-stage Decompilation Pipeline with Layered Transformation

**Key Characteristics:**
- Bytecode-to-IR-to-C pipeline architecture
- Stack-based VM simulation with SSA transformation
- Pattern-based control flow reconstruction
- Validation-driven development with round-trip compilation testing

## Layers

**Parsing Layer:**
- Purpose: Parse binary .SCR file format into structured data
- Location: `vcdecomp/parsing/`
- Contains: Header parser, symbol database, binary file readers
- Depends on: Python standard library (struct, pathlib)
- Used by: Loader layer

**Loader Layer:**
- Purpose: Load and structure .SCR file components
- Location: `vcdecomp/core/loader/`
- Contains: SCRFile class, data segment parser, instruction loader
- Depends on: Parsing layer, disasm layer (opcodes)
- Used by: All decompilation stages

**Disassembly Layer:**
- Purpose: Convert bytecode to assembly representation
- Location: `vcdecomp/core/disasm/`
- Contains: Disassembler, opcode tables (runtime/compiler variants), opcode resolver
- Depends on: Loader layer
- Used by: IR construction layer, CLI tools

**IR Construction Layer:**
- Purpose: Build intermediate representations (CFG, SSA)
- Location: `vcdecomp/core/ir/`
- Contains: CFG builder, stack lifter, SSA construction, type inference
- Depends on: Disassembly layer, loader layer
- Used by: Structure analysis, expression formatting

**Structure Analysis Layer:**
- Purpose: Reconstruct high-level control flow patterns
- Location: `vcdecomp/core/ir/structure/`
- Contains: Pattern detection (if/else, switch, loops), control flow analysis, code emission
- Depends on: IR layer, expression formatter
- Used by: Main decompilation pipeline

**Expression Formatting Layer:**
- Purpose: Convert SSA instructions to C expressions
- Location: `vcdecomp/core/ir/expr.py`
- Contains: Expression builder, type-aware formatters, operator mapping
- Depends on: IR layer, header database
- Used by: Structure analysis, code emitter

**Header Database Layer:**
- Purpose: Resolve external function signatures and constants
- Location: `vcdecomp/core/headers/`
- Contains: C header parser, function signature database, constant detector
- Depends on: None (data files in `data/`)
- Used by: Expression formatter, symbol export

**Validation Layer:**
- Purpose: Verify decompiled code by recompiling and comparing bytecode
- Location: `vcdecomp/validation/`
- Contains: Compiler wrapper, bytecode comparator, difference categorizer, regression tester
- Depends on: Loader layer (for bytecode reading)
- Used by: CLI validation commands, testing

**GUI Layer:**
- Purpose: Interactive decompiler frontend
- Location: `vcdecomp/gui/`
- Contains: Main window, validation view, syntax highlighter, hex viewer
- Depends on: All core layers, PyQt6
- Used by: End users

## Data Flow

**Decompilation Flow:**

1. Parse .SCR file → SCRFile object (loader)
2. Disassemble bytecode → Assembly listing (disassembler)
3. Build CFG → BasicBlocks with edges (cfg.py)
4. Lift stack operations → LiftedInstructions with stack values (stack_lifter.py)
5. Construct SSA → SSAFunction with phi nodes (ssa.py)
6. Format expressions → C-like statements (expr.py)
7. Detect patterns → If/else, switch, loops (structure/patterns/)
8. Emit code → Final C source (structure/emit/)

**Validation Flow:**

1. Decompile .SCR → .c source
2. Compile .c → .scr bytecode (SCMP.exe wrapper)
3. Compare bytecode → Difference list (bytecode_compare.py)
4. Categorize differences → Semantic vs non-semantic (difference_types.py)
5. Generate report → HTML/JSON/text (report_generator.py)

**State Management:**
- Immutable data structures (dataclasses) for IR nodes
- CFG maintains block graph and dominator tree
- SSA tracks value definitions and uses
- No global mutable state

## Key Abstractions

**SCRFile:**
- Purpose: Represents parsed .SCR file
- Examples: `vcdecomp/core/loader/scr_loader.py`
- Pattern: Data class with header, data_segment, code_segment, xfn_table

**BasicBlock:**
- Purpose: Represents control flow graph node
- Examples: `vcdecomp/core/ir/cfg.py`
- Pattern: Data class with start/end addresses, successors, predecessors

**SSAValue:**
- Purpose: Represents single-assignment value in SSA form
- Examples: `vcdecomp/core/ir/ssa.py`
- Pattern: Named value with type, producer instruction, use list, phi sources

**Pattern Classes:**
- Purpose: Represent detected control flow patterns
- Examples: `SwitchPattern`, `IfElsePattern`, `ForLoopInfo` in `vcdecomp/core/ir/structure/patterns/models.py`
- Pattern: Data classes capturing pattern structure for code emission

**ExpressionFormatter:**
- Purpose: Converts SSA instructions to C expressions
- Examples: `vcdecomp/core/ir/expr.py`
- Pattern: Visitor-style formatter with type-aware operator selection

## Entry Points

**CLI Entry Point:**
- Location: `vcdecomp/__main__.py`
- Triggers: `python -m vcdecomp <command>`
- Responsibilities: Argument parsing, command dispatch, error handling

**GUI Entry Point:**
- Location: `vcdecomp/gui/main_window.py` (`run_gui()`)
- Triggers: `python -m vcdecomp gui`
- Responsibilities: Initialize PyQt6 application, load file, display views

**Decompilation Pipeline:**
- Location: `vcdecomp/__main__.py` (`cmd_structure()`)
- Triggers: `python -m vcdecomp structure file.scr`
- Responsibilities: Orchestrate full decompilation, output C source

**Validation Pipeline:**
- Location: `vcdecomp/validation/validator.py` (`ValidationOrchestrator.validate()`)
- Triggers: `python -m vcdecomp validate original.scr decompiled.c`
- Responsibilities: Compile, compare, categorize, report

## Error Handling

**Strategy:** Exception-based with graceful degradation

**Patterns:**
- FileNotFoundError raised for missing files, caught at CLI level
- Validation errors wrapped in ValidationResult with verdict (PASS/FAIL/ERROR)
- Decompilation failures fall back to assembly output
- Missing header signatures treated as unknown external calls

## Cross-Cutting Concerns

**Logging:** Python logging module, configured at CLI level
**Validation:** Round-trip compilation testing via validation subsystem
**Authentication:** Not applicable (offline tool)

---

*Architecture analysis: 2026-01-17*
