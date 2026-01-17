# VC-Script-Decompiler Quality Improvement

## What This Is

A systematic effort to fix the Vietcong game script decompiler to produce high-quality, recompilable C code from .scr bytecode files. The decompiler currently produces output that won't compile due to syntax errors, malformed code, and missing declarations. This project focuses on identifying and fixing these bugs through automated testing and validation until decompiled scripts compile successfully and produce bytecode matching the original.

## Core Value

Decompiled C code must compile successfully with the original SCMP.exe compiler. Until code compiles, nothing else matters - bytecode matching, readability, and optimization are secondary goals that come after achieving compilable output.

## Requirements

### Validated

Current working capabilities of the decompiler:

- ✓ Parse .scr bytecode format (header, data segment, code segment, XFN table) — existing
- ✓ Disassemble bytecode to assembly (.asm output) — existing
- ✓ Build control flow graph (CFG) from bytecode — existing
- ✓ Convert stack operations to SSA form — existing
- ✓ Detect basic control flow patterns (if/else, switch, loops) — existing
- ✓ CLI interface for decompilation commands — existing
- ✓ GUI with syntax highlighting and hex viewer — existing
- ✓ Validation system (recompile and compare bytecode) — existing

### Active

Improvements needed to achieve compilable output:

- [ ] Systematically identify all syntax errors preventing compilation
- [ ] Fix expression reconstruction to produce valid C syntax
- [ ] Fix variable declaration generation (locals, globals, arrays, structs)
- [ ] Fix type inference to use correct C types instead of generic `dword`
- [ ] Fix function signature detection and parameter naming
- [ ] Integrate one-click compile button into GUI (reads from decompiler, not file)
- [ ] Build automated test suite that runs decompilation on test cases and validates compilation
- [ ] Expand test coverage beyond current 3 test cases to cover all control flow patterns
- [ ] Create interactive analysis workflow (AI-assisted review of decompilation errors)
- [ ] Implement regression testing to prevent fixed bugs from returning

### Out of Scope

- Rebuilding decompiler from scratch — Fix existing architecture, don't replace it
- Optimization of decompiled code — Compilable first, readable later
- Cross-platform validation on Linux/Mac — Windows-only for now (original compiler is Windows .exe)
- Symbol table integration from .dbg files — Deferred to future work
- Advanced type inference from usage patterns — Basic types first

## Context

**Current State:**
- Decompiler has complete pipeline: parsing → disassembly → CFG → SSA → pattern detection → code emission
- Validation system exists with bytecode comparison and difference categorization
- Three test cases available in `decompiler_source_tests/` with original C source and compiled .scr files
- Codebase recently refactored (structure module split into 17 focused modules)
- Known issues documented in CONCERNS.md: expression formatter complexity, heuristic-based detection, incomplete type inference

**Test Data Available:**
- `decompiler_source_tests/` - 3 test cases with .scr and .c files
- `Compiler-testruns/` - Additional scripts with known source
- `script-folders/` - Real game mission scripts (production code)

**Original Compiler:**
- SCMP.exe (Windows 32-bit) located in `original-resources/compiler/`
- Produces .err files on compilation failure (indicates failure stage)
- Current validation system uses this compiler but reads from files, not decompiler output directly

**User Workflow Goal:**
1. Load .scr file in GUI
2. Click "Compile" button
3. Decompiler generates C code → feeds directly to SCMP.exe
4. If compilation fails, show .err file content
5. If compilation succeeds, compare bytecode and show match/diff report

## Constraints

- **Platform**: Windows-only (original compiler is Windows .exe, Wine support deferred)
- **Language**: Python 3.x (existing codebase)
- **Compiler**: Must use original SCMP.exe (no reimplementation - it's the validation oracle)
- **Test Coverage**: Must maintain 100% coverage on core modules during fixes
- **Architecture**: Work within existing pipeline structure (no full rewrite)
- **Validation**: Every fix must be validated by recompilation test (no "looks good" - must compile)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Fix existing decompiler vs rebuild | Existing architecture is sound (pipeline works), bugs are in individual stages | — Pending |
| Validation via bytecode comparison | Original compiler is authoritative source of correct behavior | — Pending |
| Start with 3 test cases | Known good sources provide ground truth for error identification | — Pending |

---
*Last updated: 2026-01-17 after initialization*
