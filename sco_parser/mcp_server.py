"""MCP server for interactive .sco file querying."""

import os
import fnmatch
from typing import Dict, Optional
from mcp.server.fastmcp import FastMCP

from .parser import parse_sco
from .models import ScoFile, SceneNode

mcp = FastMCP("sco-parser", instructions="Vietcong .sco scene file parser. Use sco_open to load a file, then query nodes, waypoints, entities, and metadata.")

# Loaded files keyed by handle (basename without extension)
_files: Dict[str, ScoFile] = {}


def _get_file(handle: str) -> ScoFile:
    if handle not in _files:
        raise ValueError(f"No file loaded with handle '{handle}'. Use sco_open first.")
    return _files[handle]


def _make_handle(path: str) -> str:
    base = os.path.basename(path)
    name = os.path.splitext(base)[0].lower()
    if name in _files:
        i = 2
        while f"{name}_{i}" in _files:
            i += 1
        return f"{name}_{i}"
    return name


def _node_summary(node: SceneNode, path: str = "") -> dict:
    pos = node.position
    return {
        "name": node.name,
        "type": node.node_type_name(),
        "path": path or "/" + node.name,
        "bes_index": node.bes_index,
        "flags": node.flags,
        "child_count": len(node.children),
        "position": list(pos) if pos else None,
        "has_waypoint": node.waypoint is not None,
        "has_scrhelper": node.scrhelper is not None,
        "parse_error": node.parse_error,
    }


def _walk_tree(node: SceneNode, path: str = "", max_depth: int = -1, depth: int = 0):
    """Yield (node, path, depth) for all nodes."""
    current_path = path + "/" + node.name if path else "/" + node.name
    yield node, current_path, depth
    if max_depth >= 0 and depth >= max_depth:
        return
    for child in node.children:
        yield from _walk_tree(child, current_path, max_depth, depth + 1)


@mcp.tool()
def sco_open(path: str) -> dict:
    """Open and parse a .sco file. Returns handle, header summary, and counts.

    Args:
        path: Absolute or relative path to the .sco file
    """
    sco = parse_sco(path)
    handle = _make_handle(path)
    _files[handle] = sco

    h = sco.header
    result = {
        "handle": handle,
        "path": sco.file_path,
        "version": f"{h.version:#x}",
        "timestamp": f"{h.year}-{h.month:02d}-{h.day:02d} {h.hour:02d}:{h.minute:02d}:{h.second:02d}",
        "camera": {"x": h.camera_x, "y": h.camera_y, "z": h.camera_z,
                    "yaw": h.camera_yaw, "pitch": h.camera_pitch},
        "entity_count": len(sco.entities),
        "node_count": sco.node_count,
        "level_name": sco.level_name,
        "camera_fov": sco.camera_fov,
    }
    if sco.trailer:
        result["author"] = sco.trailer.author
        result["comment"] = sco.trailer.comment
        result["sublevel"] = sco.trailer.sublevel
    if sco.parse_warnings:
        result["warnings"] = sco.parse_warnings[:20]  # cap for readability
    return result


@mcp.tool()
def sco_close(handle: str) -> dict:
    """Close a previously opened .sco file.

    Args:
        handle: Handle returned by sco_open
    """
    if handle in _files:
        del _files[handle]
        return {"status": "ok", "handle": handle}
    return {"status": "not_found", "handle": handle}


@mcp.tool()
def sco_list() -> list:
    """List all currently opened .sco files with their handles and paths."""
    return [{"handle": h, "path": f.file_path, "node_count": f.node_count,
             "entity_count": len(f.entities)} for h, f in _files.items()]


@mcp.tool()
def sco_entities(handle: str) -> list:
    """List all BES entity references in the file.

    Args:
        handle: Handle returned by sco_open
    """
    sco = _get_file(handle)
    return [{"index": e.index, "path": e.path} for e in sco.entities]


@mcp.tool()
def sco_node_tree(handle: str, max_depth: int = 3) -> dict:
    """Get a truncated view of the scene node tree.

    Args:
        handle: Handle returned by sco_open
        max_depth: Maximum depth to traverse (default 3). Use -1 for unlimited.
    """
    sco = _get_file(handle)
    if not sco.root_node:
        return {"error": "No node tree parsed"}

    def _build(node: SceneNode, path: str, depth: int) -> dict:
        pos = node.position
        entry = {
            "name": node.name,
            "type": node.node_type_name(),
            "child_count": len(node.children),
        }
        if pos:
            entry["position"] = [round(p, 2) for p in pos]
        if max_depth < 0 or depth < max_depth:
            if node.children:
                entry["children"] = [
                    _build(c, path + "/" + c.name, depth + 1)
                    for c in node.children
                ]
        elif node.children:
            entry["children_truncated"] = len(node.children)
        return entry

    return _build(sco.root_node, "", 0)


@mcp.tool()
def sco_find_nodes(handle: str, name_pattern: str, node_type: Optional[str] = None) -> list:
    """Find nodes matching a name pattern (supports * and ? wildcards).

    Args:
        handle: Handle returned by sco_open
        name_pattern: Glob pattern to match node names (e.g., "USSpawn*", "WayPoint*")
        node_type: Optional type filter (e.g., "Dummy", "Event", "Mesh")
    """
    sco = _get_file(handle)
    if not sco.root_node:
        return []

    results = []
    for node, path, depth in _walk_tree(sco.root_node):
        if not fnmatch.fnmatch(node.name, name_pattern):
            continue
        if node_type and node_type.lower() not in node.node_type_name().lower():
            continue
        results.append(_node_summary(node, path))

    return results


@mcp.tool()
def sco_node_detail(handle: str, node_path: str) -> dict:
    """Get full details for a specific node by its tree path.

    Args:
        handle: Handle returned by sco_open
        node_path: Tree path like "/root_name/child_name" from sco_find_nodes or sco_node_tree
    """
    sco = _get_file(handle)
    if not sco.root_node:
        return {"error": "No node tree parsed"}

    # Find node by path
    target = None
    for node, path, depth in _walk_tree(sco.root_node, max_depth=-1):
        if path == node_path:
            target = node
            break

    if not target:
        return {"error": f"Node not found at path: {node_path}"}

    result = _node_summary(target, node_path)
    result["node_version"] = target.node_version
    result["data_size"] = target.data_size
    result["param1"] = target.param1
    result["param2"] = target.param2
    result["sector_count"] = target.sector_count

    if target.transform:
        t = target.transform
        result["transform"] = {
            "matrix_count": t.matrix_count,
            "has_marker": t.has_marker,
            "flags": t.flags,
            "bsphere": t.bsphere,
            "bsphere2": t.bsphere2,
            "pos_x": t.pos_x,
            "pos_y": t.pos_y,
            "position": list(t.position) if t.position else None,
        }
    if target.waypoint:
        w = target.waypoint
        result["waypoint"] = {
            "wp_id": w.wp_id, "wp_param": w.wp_param,
            "connections": w.connections,
        }
    if target.dummy_basic:
        d = target.dummy_basic
        result["dummy_basic"] = {
            "radius_x": d.radius_x, "radius_y": d.radius_y, "radius_z": d.radius_z,
            "dummy_type": d.dummy_type, "dummy_flags": d.dummy_flags,
        }
    if target.scrhelper:
        s = target.scrhelper
        result["scrhelper"] = {
            "helper_type": s.helper_type, "param1": s.param1, "param2": s.param2,
            "pos_x": s.pos_x, "pos_y": s.pos_y, "pos_z": s.pos_z,
        }
    if target.scrhelper_flag:
        result["scrhelper_flag"] = target.scrhelper_flag.flag
    if target.sound:
        result["sound"] = {"params": target.sound.params}
    if target.sound_switch:
        result["sound_switch"] = {"fields": target.sound_switch.fields}
    if target.portal:
        result["portal"] = {
            "fields": target.portal.portal_fields,
            "bytes": list(target.portal.portal_bytes),
        }
    if target.level_item:
        result["level_item"] = {
            "item_type": target.level_item.item_type,
            "item_name": target.level_item.item_name,
        }
    if target.string_data:
        result["string_data"] = target.string_data.value
    if target.sector_param:
        result["sector_param"] = target.sector_param.value
    if target.occluder:
        result["occluder"] = target.occluder.value
    if target.recovery:
        result["recovery_id"] = target.recovery.recovery_id
    if target.spectator:
        result["spectator"] = {"param1": target.spectator.param1, "param2": target.spectator.param2}
    if target.fog_color:
        result["fog_color"] = f"{target.fog_color.color:#010x}"
    if target.raw_chunks:
        result["raw_chunk_ids"] = list(target.raw_chunks.keys())

    # List children names
    if target.children:
        result["children"] = [{"name": c.name, "type": c.node_type_name()} for c in target.children]

    return result


@mcp.tool()
def sco_waypoints(handle: str) -> dict:
    """Extract the waypoint navigation graph.

    Args:
        handle: Handle returned by sco_open

    Returns:
        Graph with nodes (id, name, position, wp_param, connections) and edges.
    """
    sco = _get_file(handle)
    if not sco.root_node:
        return {"error": "No node tree parsed"}

    nodes = []
    edges = []
    id_to_name = {}

    for node, path, depth in _walk_tree(sco.root_node, max_depth=-1):
        if node.waypoint:
            wp = node.waypoint
            pos = node.position
            id_to_name[wp.wp_id] = node.name
            entry = {
                "wp_id": wp.wp_id,
                "name": node.name,
                "position": [round(p, 2) for p in pos] if pos else None,
                "wp_param": wp.wp_param,
                "connections": wp.connections,
                "path": path,
            }
            nodes.append(entry)
            for conn in wp.connections:
                edges.append([wp.wp_id, conn])

    return {
        "waypoint_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }


@mcp.tool()
def sco_metadata(handle: str) -> dict:
    """Get file metadata: trailer, lighting, sound areas, level name, fog params.

    Args:
        handle: Handle returned by sco_open
    """
    sco = _get_file(handle)
    result: dict = {
        "level_name": sco.level_name,
        "camera_fov": sco.camera_fov,
        "layer_visibility": sco.layer_visibility,
    }

    if sco.trailer:
        t = sco.trailer
        result["trailer"] = {
            "author": t.author,
            "comment": t.comment,
            "level_path": t.level_path,
            "sublevel": t.sublevel,
            "sector_count": t.sector_count,
            "hidden_count": t.hidden_count,
            "object_count": t.object_count,
            "collision_size": t.collision_size,
            "stats": t.stats,
            "thumb_size": f"{t.thumb_width}x{t.thumb_height}",
        }

    if sco.lighting:
        lt = sco.lighting
        result["lighting"] = {
            "version": lt.version,
            "ambient": [round(lt.ambient_r, 3), round(lt.ambient_g, 3), round(lt.ambient_b, 3)],
            "light_dir_1": [round(v, 3) for v in lt.light_dir_1],
            "light_dir_2": [round(v, 3) for v in lt.light_dir_2],
            "fog_far_clip": lt.fog_far_clip,
            "fog_near_clip": lt.fog_near_clip,
            "fog_density": lt.fog_density,
        }

    if sco.sound_areas:
        result["sound_areas"] = [
            {"index": sa.index, "name": sa.name, "type": sa.area_type,
             "params": [sa.param1, sa.param2, sa.param3, sa.param4]}
            for sa in sco.sound_areas
        ]

    if sco.terrain:
        td = sco.terrain
        result["terrain"] = {
            "heightmap": td.heightmap_path,
            "texture": td.texture_path,
            "detail": td.detail_path,
            "sector_count": len(td.sectors),
        }

    return result


@mcp.tool()
def sco_positions(handle: str, node_type: Optional[str] = None) -> list:
    """Get a flat list of all nodes with positions for spatial queries.

    Args:
        handle: Handle returned by sco_open
        node_type: Optional type filter (e.g., "Dummy", "Event", "Mesh", "Player")
    """
    sco = _get_file(handle)
    if not sco.root_node:
        return []

    results = []
    for node, path, depth in _walk_tree(sco.root_node, max_depth=-1):
        pos = node.position
        if pos is None:
            continue
        type_name = node.node_type_name()
        if node_type and node_type.lower() not in type_name.lower():
            continue
        results.append({
            "name": node.name,
            "type": type_name,
            "x": round(pos[0], 2),
            "y": round(pos[1], 2),
            "z": round(pos[2], 2),
            "path": path,
        })

    return results
