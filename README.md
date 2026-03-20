# VC Scripter

AI-powered reverse engineering and scripting environment for Vietcong (2003).

## What is this?

A development environment for working with Vietcong game scripts. Clone this repo, run an AI coding agent inside it, and the agent automatically connects to MCP servers that let it read and analyze game files directly.

The repo includes a decompiler (`.scr` bytecode → C source), a compiler (C source → `.scr` bytecode), scene file parser (`.sco`), SDK headers, and original reference scripts. Together, these give an AI agent everything it needs to reverse engineer, modify, and create Vietcong game scripts.

## What you can do with it

> "Here is my unpacked game LEVELS folder. Open the AMBUSH level, decompile the scripts, and reimplement the code so I can compile it and run it in the game."

> "Reverse engineer the NVA_BASE mission and add a new objective to it."

> "I'm creating a multiplayer coop map. The game can hold only 64 players, so I need bots to respawn at different locations when killed to pack more into the level. Here's a script that does something similar — implement it in my script."

> "I'm making a coop map. Create a bot script where bots follow the human players and help them fight."

You provide your unpacked game files (`.scr` scripts, `.sco` scene files) and any reference scripts you have. The AI agent handles the rest — decompiling, analyzing, writing code, and compiling.

## Prerequisites

- **Python 3** (tested on 3.10+)
- **An AI coding agent** — [Claude Code](https://claude.ai/code) recommended (MCP auto-detected via `.mcp.json`). Cursor, Windsurf, and other MCP-capable agents also work.
- **Unpacked Vietcong game files** — you need the `.scr` and `.sco` files from your game installation

## Getting Started

```bash
# Clone the repo
git clone https://github.com/pocketrice/VC_Scripter.git
cd VC_Scripter

# Install Python dependencies
pip install -r requirements.txt

# Launch your AI agent in this directory
# Claude Code example:
claude

# Then just ask:
# "Open the LEVEL.SCR from my_game_folder/ and decompile it"
# "What functions does this script have?"
# "Rewrite the respawn logic to use these new spawn points"
```

The `.mcp.json` file is preconfigured — Claude Code and other MCP-aware agents will automatically start the tool servers.

## What's included

| Directory | What it is |
|-|-|
| `vcdecomp/` | Decompiler — converts `.scr` bytecode to readable C source |
| `vcdecomp/compiler/` | Original SCMP compiler toolchain (SPP → SCC → SASM) for compiling C back to `.scr` |
| `vcdecomp_mcp/` | MCP server exposing decompiler tools to AI agents |
| `sco_parser/` | `.sco` scene file parser + MCP server for AI agents |
| `SDK/` | Vietcong Scripting SDK — `SC_GLOBAL.H`, `SC_DEF.H`, full SDK docs |
| `original-resources/` | Example scripts (`.c`), headers (`.h`), includes (`.inc`), bot configs (`.CXX`) |
| `.mcp.json` | Preconfigured MCP server definitions (auto-detected by Claude Code) |

## MCP Tools

Two MCP servers give AI agents direct access to game file internals. See [agents.md](agents.md) for full tool reference.

**vcdecomp-mcp** — Script bytecode analysis:
- Open `.scr` files and list functions, globals, strings, external API calls
- Decompile individual functions to C code
- View disassembly, SSA form, basic blocks, call graphs
- Rename variables/functions, override types, add comments
- Cross-reference who calls what

**sco-parser** — Scene file analysis:
- Open `.sco` files and browse the node hierarchy
- Find spawn points, waypoints, objects by name or type
- Extract AI navigation graphs
- Get entity references, lighting, metadata
- Cross-reference node names with `SC_NOD_Get()` calls in scripts

## CLI Usage

```bash
# Decompile a script to C source
py -3 -m vcdecomp structure script.scr > output.c

# Show script info (entry point, sizes, counts)
py -3 -m vcdecomp info script.scr

# Disassemble to readable assembly
py -3 -m vcdecomp disasm script.scr > output.asm

# Compile C source back to .scr bytecode
# Copy your .c file to vcdecomp/compiler/, then:
py -3 compile_simple.py

# Launch the GUI
py -3 -m vcdecomp gui
```

## Batch Decompilation

```bash
# PowerShell
Get-ChildItem *.scr | ForEach-Object {
    py -3 -m vcdecomp structure $_.FullName > "$($_.BaseName)_decompiled.c"
}

# Bash
for file in *.scr; do
    py -3 -m vcdecomp structure "$file" > "${file%.scr}_decompiled.c"
done
```

## Important: Decompilation is not 100% reliable

The decompiler produces a best-effort reconstruction. Some things may be wrong or missing — incorrect variable types, mangled expressions, lost control flow. **Always review decompiled output against the disassembly.** The disassembly (`scr_disasm` or `py -3 -m vcdecomp disasm`) is a faithful representation of the bytecode and is always correct.

You may also need to override variable types using `scr_set_type` to get proper decompiled output — the decompiler's type inference is incomplete and sometimes guesses wrong.

## Known Limitations

- **Type inference** is incomplete — some variables remain as `dword` (unknown type), override with `scr_set_type`
- **Macros** are lost — the preprocessor expands them before compilation
- **Global variable detection** is heuristic-based and may be inaccurate
- **Complex control flow** — some nested loops or switch statements may not reconstruct perfectly
- **Compiler** requires Windows (uses original Win32 executables via WSL or native)
