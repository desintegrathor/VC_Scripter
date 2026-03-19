"""Entry point for sco_parser package.

Usage:
    py -3 -m sco_parser              # Run MCP server (stdio transport)
    py -3 -m sco_parser parse FILE   # Parse and print summary
    py -3 -m sco_parser --help       # Show help
"""

import sys
import os
import json

# Fix console encoding on Windows
if sys.platform == 'win32':
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def _print_summary(filepath: str) -> None:
    """Parse a .sco file and print a summary."""
    from .parser import parse_sco

    sco = parse_sco(filepath)
    h = sco.header

    print(f"File: {sco.file_path}")
    print(f"Version: {h.version:#x}")
    print(f"Timestamp: {h.year}-{h.month:02d}-{h.day:02d} {h.hour:02d}:{h.minute:02d}:{h.second:02d}")
    print(f"Camera: ({h.camera_x:.1f}, {h.camera_y:.1f}, {h.camera_z:.1f}) yaw={h.camera_yaw:.2f} pitch={h.camera_pitch:.2f}")
    print(f"Entities: {len(sco.entities)}")
    print(f"Nodes: {sco.node_count}")
    print(f"Level name: {sco.level_name}")

    if sco.camera_fov is not None:
        print(f"Camera FOV: {sco.camera_fov:.1f}")

    if sco.trailer:
        t = sco.trailer
        print(f"\nTrailer:")
        print(f"  Author: {t.author}")
        print(f"  Comment: {t.comment}")
        print(f"  Level path: {t.level_path}")
        print(f"  Sublevel: {t.sublevel}")
        print(f"  Sectors: {t.sector_count}, Hidden: {t.hidden_count}, Objects: {t.object_count}")
        print(f"  Collision size: {t.collision_size} bytes")

    if sco.lighting:
        lt = sco.lighting
        print(f"\nLighting (v{lt.version}):")
        print(f"  Ambient: ({lt.ambient_r:.2f}, {lt.ambient_g:.2f}, {lt.ambient_b:.2f})")
        print(f"  Fog: near={lt.fog_near_clip:.1f} far={lt.fog_far_clip:.1f} density={lt.fog_density:.3f}")

    if sco.sound_areas:
        print(f"\nSound areas: {len(sco.sound_areas)}")
        for sa in sco.sound_areas:
            print(f"  {sa.index}: \"{sa.name}\" type={sa.area_type}")

    if sco.terrain:
        print(f"\nTerrain:")
        if sco.terrain.heightmap_path:
            print(f"  Heightmap: {sco.terrain.heightmap_path}")
        if sco.terrain.texture_path:
            print(f"  Texture: {sco.terrain.texture_path}")
        print(f"  Sectors: {len(sco.terrain.sectors)}")

    # Node tree summary
    if sco.root_node:
        print(f"\nNode tree root: \"{sco.root_node.name}\"")

        # Count by type
        type_counts: dict = {}
        wp_count = 0
        from .mcp_server import _walk_tree
        for node, path, depth in _walk_tree(sco.root_node, max_depth=-1):
            tn = node.node_type_name()
            type_counts[tn] = type_counts.get(tn, 0) + 1
            if node.waypoint:
                wp_count += 1

        print(f"  Node types:")
        for tn, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"    {tn}: {count}")
        if wp_count > 0:
            print(f"  Waypoints with connections: {wp_count}")

    # Entity list (first 10)
    if sco.entities:
        print(f"\nEntities (first {min(10, len(sco.entities))} of {len(sco.entities)}):")
        for e in sco.entities[:10]:
            print(f"  [{e.index}] {e.path}")
        if len(sco.entities) > 10:
            print(f"  ... and {len(sco.entities) - 10} more")

    if sco.parse_warnings:
        print(f"\nWarnings ({len(sco.parse_warnings)}):")
        for w in sco.parse_warnings[:10]:
            print(f"  - {w}")
        if len(sco.parse_warnings) > 10:
            print(f"  ... and {len(sco.parse_warnings) - 10} more")


def main():
    args = sys.argv[1:]

    if args and args[0] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)

    if args and args[0] == "parse":
        if len(args) < 2:
            print("Usage: py -3 -m sco_parser parse <file.sco>")
            sys.exit(1)
        _print_summary(args[1])
    else:
        # Default: run MCP server (stdio transport)
        from .mcp_server import mcp
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
