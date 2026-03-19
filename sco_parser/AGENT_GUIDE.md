# SCO Parser - Agent Guide

MCP server for parsing Vietcong `.sco` scene files. Provides tools to query scene nodes, waypoints, entities, and metadata.

## Quick Start

1. **Open a file**: `sco_open(path="path/to/level.sco")` → returns a `handle`
2. **Query data** using the handle
3. **Close when done**: `sco_close(handle="...")`

## Tools

| Tool | Purpose |
|-|-|
| `sco_open` | Load and parse a .sco file |
| `sco_close` | Unload a file |
| `sco_list` | List open files |
| `sco_entities` | List all BES model references |
| `sco_node_tree` | Browse the node hierarchy (use `max_depth` to control) |
| `sco_find_nodes` | Search nodes by name pattern (`*`, `?` wildcards) |
| `sco_node_detail` | Full details for a node (by tree path) |
| `sco_waypoints` | Extract AI navigation graph |
| `sco_metadata` | Trailer, lighting, fog, sound areas |
| `sco_positions` | All positioned nodes as flat list |

## Common Patterns

**Find spawn points**: `sco_find_nodes(handle, "USSpawn*")` or `sco_find_nodes(handle, "VCSpawn*")`

**Find waypoints**: `sco_waypoints(handle)` returns full graph with connections

**Find objects by type**: `sco_positions(handle, node_type="Dummy")` or `"Event"`, `"Mesh"`, `"Player"`

**Cross-reference with scripts**: Node names match `SC_NOD_Get("name")` calls in decompiled .scr files

## Node Types

Key types: Mesh (1), Dummy (6), Light (7), Event (8), SndSw (10), WorldSector (13), LevelItem (16), ScrHelper (19), Player (0x101), MPHelper (0x103), Recovery (0x104)
