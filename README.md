# VC-Script Decompiler

Decompiler for Vietcong (2003) game scripts. Converts compiled `.scr` bytecode files back into readable C-like source code.

## Getting Started

### Launch the GUI

Double-click **`launch.bat`** to start the application. The GUI lets you open `.scr` files, view disassembly, and decompile scripts interactively.

### Command-Line Usage

The decompiler can also be used from the command line:

```bash
# Decompile a script (default: Ghidra-style collapse + incremental heritage SSA)
py -3 -m vcdecomp structure script.scr > output.c

# Show script info
py -3 -m vcdecomp info script.scr

# Disassemble to readable assembly
py -3 -m vcdecomp disasm script.scr > output.asm
```

### Batch Decompilation

**Windows (PowerShell):**
```powershell
Get-ChildItem *.scr | ForEach-Object {
    py -3 -m vcdecomp structure $_.FullName > "$($_.BaseName)_decompiled.c"
}
```

**Bash:**
```bash
for file in *.scr; do
    py -3 -m vcdecomp structure "$file" > "${file%.scr}_decompiled.c"
done
```

## Recommended Workflow for Decompiled Output

The decompiler produces a best-effort reconstruction of the original source. The output should be reviewed and refined before considering it final:

1. **Cross-check against disassembly** — Compare the decompiled C code with the disassembly output (`py -3 -m vcdecomp disasm script.scr`) to verify that nothing is missing, duplicated, or logically incorrect.

2. **Use SDK headers as reference** — Consult `sc_global.h` and `sc_def.h` (in `vcdecomp/compiler/inc/`) and the Scripting SDK documentation (`docs/Scripting_SDK.txt`) to verify function signatures, parameter types, constants, and engine API usage.

3. **Analyze full missions together** — When decompiling an entire mission, process all scripts from the mission folder at once and cross-reference them. Scripts within a mission share global state, call each other's functions, and reference the same entities. Reconstructing them together gives much better results than analyzing each file in isolation.

4. **Use external context** — Game walkthroughs, mission descriptions, and lore can help understand what a script is doing — naming variables, identifying event sequences, and making sense of AI behavior or trigger logic.

If you don't have access to a coding agent (Claude Code, Cursor, etc.), you can use the [Vietcong Game Modder](https://chatgpt.com/g/g-68b42a36825c81919ebd8df8bc6d1478-vietcong-game-modder) chat assistant for the review and refinement steps. It won't be ideal, but it can still help with cross-referencing disassembly, spotting issues, and suggesting corrections through the chat window.

## CLI Options

### Decompilation Modes

```bash
# Ghidra-style hierarchical structuring (default, best quality)
py -3 -m vcdecomp structure script.scr > output.c

# Flat mode (faster, lower quality)
py -3 -m vcdecomp structure --no-collapse script.scr > output.c

# Debug output (for diagnostics)
py -3 -m vcdecomp structure --debug script.scr > output.c 2> debug.log

# Legacy SSA (faster but less accurate)
py -3 -m vcdecomp structure --legacy-ssa script.scr > output.c
```

### Other Commands

```bash
# Script metadata (entry point, size, instruction count)
py -3 -m vcdecomp info script.scr

# Disassembly
py -3 -m vcdecomp disasm script.scr > output.asm

# Export global variable symbols
py -3 -m vcdecomp symbols script.scr -o globals.json -f json

# Aggregate external function signatures from multiple .scr files
py -3 -m vcdecomp xfn-aggregate scripts/ --format summary
```

## SDK Integration

The decompiler automatically uses Vietcong SDK data (external function signatures) stored in `vcdecomp/sdk/data/functions.json`. This provides parameter names, types, and return types for 700+ `SC_*` engine functions.

To update the SDK from new scripts:

```bash
py -3 -m vcdecomp xfn-aggregate scripts/ --format sdk -o new_functions.json --merge-sdk
```

## Technical Details

### .SCR File Format
- **Header:** Entry point, function parameter count
- **Data segment:** Constants, strings (4-byte aligned, little-endian)
- **Code segment:** Instructions (12 bytes each: opcode + 2× int32 args)
- **XFN table:** External function entries (28 bytes each)

### Instruction Set
- ~150 opcodes (arithmetic, control flow, stack operations)
- Type prefixes: `C`=char, `S`=short, `I`=int, `F`=float, `D`=double
- Examples: `IADD`, `FADD`, `PUSH`, `POP`, `JZ`, `XCALL`

### External Functions (SC_*)
Scripts call 700+ engine functions with the `SC_` prefix:
- `SC_P_Create()` — Create player
- `SC_NOD_Get()` — Get scene object
- `SC_SND_PlaySound3D()` — Play 3D sound
- `SC_message()` — Debug message
- Full list in `vcdecomp/sdk/data/functions.json`

## Documentation

- `docs/Scripting_SDK.txt` — Official Vietcong Scripting SDK reference
- `docs/decompilation_guide.md` — Decompilation workflow guide
- `vcdecomp/core/ir/structure/README.md` — Structure module architecture
- `CLAUDE.md` — AI assistant reference (complete technical details)

## Known Limitations

1. **Variable types** — Type inference is incomplete; some variables remain as `dword`
2. **Macros** — Original macros are lost (expanded by the preprocessor before compilation)
3. **Global variables** — Detection is heuristic-based and may be inaccurate
4. **Complex loops** — Loop body detection may be incomplete for complex control flow graphs

## License

Internal tool for Vietcong script reconstruction.
