# AI Agent Guide

How to use the MCP tools for Vietcong script reverse engineering and development.

## Overview

Two MCP servers are preconfigured in `.mcp.json` and start automatically when an AI agent connects:

- **vcdecomp-mcp** — Analyzes `.scr` bytecode files (decompile, disassemble, inspect)
- **sco-parser** — Analyzes `.sco` scene files (nodes, waypoints, entities, metadata)

Both use a session model: open a file → get a handle → query using the handle → close when done.

## Before you start

**Read the SDK first.** Before working on any script, read `SDK/SC_GLOBAL.H` and `SDK/Scripting_SDK.md` to understand the available engine functions, structs, and constants. This is essential context for understanding what scripts do and writing correct code.

**Decompilation is not 100% reliable.** The decompiler produces best-effort output — some things may be wrong or missing (incorrect types, mangled expressions, lost control flow). Always cross-check decompiled code against the disassembly (`scr_disasm`). The disassembly is a faithful representation of the bytecode and is always correct.

**Override types when needed.** The decompiler's type inference is incomplete. If a decompiled function looks wrong, try overriding variable types with `scr_set_type` and re-decompiling — this often fixes incorrect expressions and casts.

## vcdecomp-mcp — Script Bytecode Analysis

### Session Management

| Tool | What it does |
|-|-|
| `scr_open(path)` | Open a `.scr` file, returns a handle |
| `scr_close(handle)` | Close a session |
| `scr_list()` | List all open sessions |

### Inspection

| Tool | What it does |
|-|-|
| `scr_info(handle)` | Header fields, entry point, segment sizes |
| `scr_list_funcs(handle, filter?)` | All functions with address ranges and instruction counts |
| `scr_list_globals(handle, filter?)` | Global variables with offsets, names, types, initializers |
| `scr_list_xfns(handle, filter?)` | External engine functions (SC_* API calls) |
| `scr_strings(handle, filter?)` | All strings in the data segment |

### Decompilation & Disassembly

| Tool | What it does |
|-|-|
| `scr_decompile(handle, func)` | Decompile a function to C code |
| `scr_disasm(handle, func?, addr?, count?)` | Disassemble a function or address range |
| `scr_ssa(handle, func)` | View SSA (Static Single Assignment) form |
| `scr_basic_blocks(handle, func)` | CFG basic blocks with edges |
| `scr_stack_frame(handle, func)` | Stack frame layout — parameters and locals |

### Analysis

| Tool | What it does |
|-|-|
| `scr_callees(handle, func)` | Functions and XFNs called by a function |
| `scr_callgraph(handle, root?, max_depth?)` | Recursive call graph from a root function |
| `scr_xrefs_to(handle, target)` | Cross-references to a global, function, or `xfn:name` |
| `scr_search(handle, query, search_in?)` | Search for strings, values, or data refs in code/data |

### Mutation

Changes propagate to subsequent `scr_decompile` calls.

| Tool | What it does |
|-|-|
| `scr_rename(handle, target_type, old_name, new_name, func_context?)` | Rename a function, global, or local variable |
| `scr_set_type(handle, target, new_type)` | Override type of a global (`global:name`) or local (`local:func:var`) |
| `scr_set_comment(handle, addr, comment)` | Add/update comment at an instruction address |

### Compilation

| Tool | What it does |
|-|-|
| `scr_compile(source_path, output_name?)` | Compile a `.c` script to `.scr` bytecode using the SCMP compiler |

Copies the source file into the compiler directory, invokes the toolchain (`spp → scc → sasm`), and returns the output `.scr` path on success or compiler error messages on failure.

### Data & Export

| Tool | What it does |
|-|-|
| `scr_get_data(handle, offset, type?, count?)` | Read typed values from data segment (int, float, string, bytes) |
| `scr_read_struct(handle, offset, struct_name)` | Interpret data region as an SDK struct |
| `scr_export(handle, format?)` | Export function prototypes and globals as JSON or C header |

## sco-parser — Scene File Analysis

### Session Management

| Tool | What it does |
|-|-|
| `sco_open(path)` | Open a `.sco` file, returns a handle |
| `sco_close(handle)` | Close a session |
| `sco_list()` | List all open files |

### Scene Graph

| Tool | What it does |
|-|-|
| `sco_node_tree(handle, max_depth?)` | Browse the node hierarchy (default depth 3, use -1 for all) |
| `sco_find_nodes(handle, name_pattern, node_type?)` | Search nodes by name pattern (`*`, `?` wildcards) |
| `sco_node_detail(handle, node_path)` | Full details for a specific node by tree path |
| `sco_positions(handle, node_type?)` | All positioned nodes as a flat list, optionally filtered by type |

### Game Data

| Tool | What it does |
|-|-|
| `sco_entities(handle)` | List all BES model references in the scene |
| `sco_waypoints(handle)` | Extract AI waypoint navigation graph (nodes + connections) |
| `sco_metadata(handle)` | Trailer data, lighting, fog, sound areas, level name |

### Common Queries

```
# Find spawn points
sco_find_nodes(handle, "USSpawn*")
sco_find_nodes(handle, "VCSpawn*")

# Find all waypoints for bot navigation
sco_waypoints(handle)

# Find objects by type
sco_positions(handle, node_type="Dummy")    # Script helpers, markers
sco_positions(handle, node_type="Event")    # Trigger zones
sco_positions(handle, node_type="Mesh")     # 3D objects
sco_positions(handle, node_type="Player")   # Player start positions
```

## Typical Workflows

### Decompile and understand a mission

1. Read `SDK/SC_GLOBAL.H` and `SDK/Scripting_SDK.md` to understand available engine functions
2. `scr_open("path/to/LEVEL.SCR")` — open the script
3. `scr_list_funcs(handle)` — see what functions exist
4. `scr_decompile(handle, "main")` — decompile the entry point
5. `scr_disasm(handle, func="main")` — verify decompiled output against disassembly (disasm is always correct)
6. If something looks wrong, use `scr_set_type` to fix variable types and re-decompile
7. `scr_strings(handle)` — find debug messages, entity names, file paths
8. `sco_open("path/to/level.sco")` — open the corresponding scene
9. `sco_find_nodes(handle, "SomeNodeName")` — cross-reference node names from `SC_NOD_Get()` calls
10. `sco_waypoints(handle)` — understand bot navigation

### Modify an existing script

1. Decompile the script using `scr_decompile` or the CLI (`py -3 -m vcdecomp structure script.scr > output.c`)
2. Edit the decompiled C source
3. Compile: `scr_compile("path/to/script.c")` — returns the output `.scr` path or error messages
4. Replace the original `.scr` in your game folder with the compiled output

### Create a new script

1. Use `SDK/SC_GLOBAL.H` for available engine functions and their signatures
2. Browse `original-resources/c/` for example scripts to use as templates
3. Browse `original-resources/h/` and `original-resources/inc/` for common headers and includes
4. Open a similar mission's `.sco` to understand available nodes, spawn points, waypoints
5. Write your script, compile, and test in-game

## CLI Quick Reference

```bash
# Decompile
py -3 -m vcdecomp structure script.scr > output.c

# Disassemble
py -3 -m vcdecomp disasm script.scr > output.asm

# Script info
py -3 -m vcdecomp info script.scr

# Compile (via MCP or CLI)
# MCP: scr_compile("script.c")
# CLI: copy .c to vcdecomp/compiler/, then: py -3 compile_simple.py

# GUI
py -3 -m vcdecomp gui
```

## SDK & Reference Files

| Path | Contents |
|-|-|
| `SDK/SC_GLOBAL.H` | All 700+ engine function prototypes (`SC_*` API) |
| `SDK/SC_DEF.H` | Constants, enums, defines |
| `SDK/Scripting_SDK.md` | Full SDK documentation |
| `original-resources/c/` | Original game scripts — level, player, vehicle, weapon scripts |
| `original-resources/h/` | Headers — SC_LEVEL.H, SC_LIBRARY.H, GLEVEL.H, etc. |
| `original-resources/inc/` | Include files — equipment, weapon configs, coop helpers |
| `original-resources/bots/` | Bot behavior configs (.CXX) |
| `vcdecomp/compiler/inc/sc_global.h` | Compiler copy of engine function headers |

## Node Types in .sco files

Key types you'll encounter when querying scene nodes:

| Type | What it is |
|-|-|
| Mesh (1) | 3D objects, buildings, terrain features |
| Dummy (6) | Script helper markers, position references |
| Light (7) | Light sources |
| Event (8) | Trigger zones, event areas |
| SndSw (10) | Sound switch areas |
| WorldSector (13) | Level geometry sectors |
| LevelItem (16) | Pickable items |
| ScrHelper (19) | Script-specific helper objects |
| Player (0x101) | Player start positions |
| MPHelper (0x103) | Multiplayer helper objects |
| Recovery (0x104) | Recovery/respawn points |

## Cross-referencing Scripts and Scenes

Scripts reference scene nodes by name using `SC_NOD_Get("NodeName")`. To understand what a script does:

1. Decompile the script and find all `SC_NOD_Get` calls
2. Open the corresponding `.sco` file
3. Use `sco_find_nodes` to locate each referenced node
4. Use `sco_node_detail` to see the node's position, type, and properties
5. Use `sco_waypoints` to understand bot movement paths referenced in the script
