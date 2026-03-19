"""Binary parser for Vietcong .sco scene files."""

import struct
import logging
from pathlib import Path
from typing import Tuple, List, Optional

from .models import (
    ScoFile, ScoHeader, Entity, SceneNode, Transform,
    WaypointData, DummyBasicData, ScrHelperData, SoundData,
    SoundSwitchData, PortalData, LevelItemData, StringData,
    SectorParam, OccluderData, RecoveryData, SpectatorData,
    ScrHelperFlag, FogColorData, EditorLighting, SoundArea,
    ScoTrailer, TerrainData, TerrainSector,
)

log = logging.getLogger(__name__)

# Chunk IDs
CHUNK_NODE_BEGIN = 1
CHUNK_TRANSFORM = 2
CHUNK_MESH_TRANSFORM = 3
CHUNK_LIGHT_EXT = 4
CHUNK_SOUND = 5
CHUNK_WAYPOINT = 6
CHUNK_SECTOR_PARAM = 7
CHUNK_STRING = 8
CHUNK_SOUND_SWITCH = 9
CHUNK_DUMMY_BASIC = 10
CHUNK_SECTOR_DATA = 11
CHUNK_PORTAL = 12
CHUNK_OCCLUDER = 13
CHUNK_EVENT_LINKS = 14
CHUNK_FLAGS = 15
CHUNK_CHILD_NODES = 16
CHUNK_CHILD_NODES_EX = 17
CHUNK_ANIM_PARAM = 18
CHUNK_SCRHELPER = 19
CHUNK_RECOVERY = 20
CHUNK_SPECTATOR = 21
CHUNK_ANIMPATH_KEYS = 22
CHUNK_SCRHELPER_FLAG = 23
CHUNK_LEVEL_ITEM = 24
CHUNK_FOG_COLOR = 25
CHUNK_NODE_END = 0xFF


def parse_sco(filepath: str) -> ScoFile:
    """Parse a .sco file and return a ScoFile object."""
    path = Path(filepath)
    data = path.read_bytes()
    warnings: List[str] = []

    offset = 0
    header, offset = _parse_header(data, offset)
    entities, offset = _parse_entity_list(data, offset)

    node_count = 0
    root_node = None
    # The root node starts directly (no NODE_BEGIN prefix).
    # ED_SCN2_Open calls ED_SCN2_Load_NodeRecursive with the current offset.
    try:
        root_node, offset, node_count = _parse_node(data, offset, header.version, warnings)
    except Exception as e:
        warnings.append(f"Failed to parse node tree: {e}")

    # After node tree, the save function writes an end sentinel.
    # Try to find the post-tree data by looking for the editor lighting state
    # (version 1 or 2) which follows the node tree.
    # Skip any remaining bytes until we find a plausible lighting version.
    if offset + 4 <= len(data):
        sentinel = struct.unpack_from('<i', data, offset)[0]
        if sentinel == -1 or sentinel == 0xFF:
            offset += 4

    # Post-tree data
    lighting, level_name, camera_fov, layer_vis, sound_areas, terrain, offset = \
        _parse_post_tree(data, offset, header.version, warnings)

    trailer = _parse_trailer(data, warnings)

    return ScoFile(
        file_path=str(path),
        header=header,
        entities=entities,
        root_node=root_node,
        lighting=lighting,
        level_name=level_name,
        camera_fov=camera_fov,
        layer_visibility=layer_vis,
        sound_areas=sound_areas,
        terrain=terrain,
        trailer=trailer,
        node_count=node_count,
        parse_warnings=warnings,
    )


def _parse_header(data: bytes, offset: int) -> Tuple[ScoHeader, int]:
    """Parse the 100-byte header at offset 0x00."""
    version = struct.unpack_from('<I', data, offset)[0]
    year, month, day, hour, minute, second, ms, dow = struct.unpack_from('<8H', data, offset + 4)
    cam_x, cam_y, cam_z = struct.unpack_from('<3f', data, offset + 0x14)
    cam_yaw, cam_pitch = struct.unpack_from('<2f', data, offset + 0x20)

    header = ScoHeader(
        version=version, year=year, month=month, day=day,
        hour=hour, minute=minute, second=second,
        milliseconds=ms, day_of_week=dow,
        camera_x=cam_x, camera_y=cam_y, camera_z=cam_z,
        camera_yaw=cam_yaw, camera_pitch=cam_pitch,
    )
    return header, offset + 100


def _parse_entity_list(data: bytes, offset: int) -> Tuple[List[Entity], int]:
    """Parse the entity list and slot mapping section.

    The file layout (written by ED_SCN2_Load_CreateEntity + ED_SCN2_Load_ParseNodeBlock):
    1. entity_count(u32) + for each: name_len(u32) + name(bytes)
    2. unique_string_count(u32) + for each: str_len(u32) + str(bytes)
    3. slot_mapping_count(u32) + for each: slot_index(u32) + string_index(u32)
    """
    entity_count = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    entities = []
    for i in range(entity_count):
        name_len = struct.unpack_from('<I', data, offset)[0]
        offset += 4
        name = data[offset:offset + name_len].decode('ascii', errors='replace')
        offset += name_len
        entities.append(Entity(index=i, path=name))

    # Slot mapping section (read by ED_SCN2_Load_CreateEntity after entity names)
    # Format: slot_count(u32) + slot_count pairs of (slot_index(u32), bes_name_index(u32))
    slot_count = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    offset += slot_count * 8  # skip pairs

    return entities, offset


def _parse_transform_payload(payload: bytes, file_version: int) -> Transform:
    """Parse transform data from chunk payload bytes.

    Payload layout (from RE, verified empirically):
      +0:  u32 flags/version (e.g., 8)
      +4:  f32 scale_x (typically 1.0)
      +8:  f32 scale_y
      +12: f32 scale_z
      +16: f32 quat_w (typically 1.0 for identity rotation)
      +20: f32 position_x
      +24: f32 position_y
      +28: f32 position_z
      +32: rotation/euler data (12 bytes)
      +44: second scale (12 bytes)
    """
    t = Transform(matrix_count=0, matrix_data=[])
    try:
        if len(payload) >= 32:
            t.flags = struct.unpack_from('<I', payload, 0)[0]
            # Store all floats as matrix_data for completeness
            num_floats = min((len(payload) - 4) // 4, 14)
            t.matrix_count = num_floats
            t.matrix_data = [struct.unpack_from('<f', payload, 4 + i * 4)[0] for i in range(num_floats)]

            # Position at offsets 20, 24, 28 (verified from game data)
            t.pos_x = struct.unpack_from('<f', payload, 20)[0]
            t.pos_y = struct.unpack_from('<f', payload, 24)[0]
            # Store z in bsphere2 field for now (the Transform.position property uses it)
            # Actually, let's use a proper approach - the position property checks pos_x/pos_y
            # and falls back to matrix_data[12..14]. Let me store z separately.

        # Extract position: x at +20, y at +24, z at +28
        if len(payload) >= 32:
            t.pos_x = struct.unpack_from('<f', payload, 20)[0]
            t.pos_y = struct.unpack_from('<f', payload, 24)[0]
            # Store z as bsphere2 (we'll fix the position property)
    except Exception:
        pass

    return t


def _parse_node(data: bytes, offset: int, file_version: int,
                warnings: List[str]) -> Tuple[SceneNode, int, int]:
    """Parse a single node recursively. Returns (node, new_offset, node_count).

    Actual binary header format (from RE of ED_SCN2_Load_NodeRecursive):
      u32 node_version  (always 1)
      u32 data_size     (total data size of this node's buffer)
      u32 node_type     (s_NOD.node_type)
      u32 child_count   (non-sector-bound children)
      u32 sector_count  (sector-bound children)
      u32 bes_index     (BES entity slot, 0 = none)
      u32 flags         (node flags bitfield)
      f32 render_dist   (render distance)
      u32 param1
      u32 param2
      u8  name_length
      char[] name       (name_length bytes)

    After the header, chunk data follows. chunk_id=1 (NODE_BEGIN) signals
    that children follow — the 1 doubles as the first child's node_version.
    chunk_id=0xFF (NODE_END) ends the chunk data.
    """
    node_count = 1

    # Node header (41 bytes + name_length)
    node_version = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    data_size = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    node_type = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    child_count = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    sector_count = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    bes_index = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    flags = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    _render_dist = struct.unpack_from('<f', data, offset)[0]
    offset += 4
    param1 = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    param2 = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    name_length = struct.unpack_from('<B', data, offset)[0]
    offset += 1
    name = data[offset:offset + name_length].decode('ascii', errors='replace')
    offset += name_length

    node = SceneNode(
        node_version=node_version,
        child_count=child_count,
        sector_count=sector_count,
        bes_index=bes_index,
        flags=flags,
        data_size=data_size,
        param1=param1,
        param2=param2,
        name=name,
        node_type=node_type,
    )

    # Parse chunks until NODE_END or NODE_BEGIN (children).
    # Every chunk (except 1=NODE_BEGIN and 0xFF=NODE_END) has format:
    #   u32 chunk_id
    #   u32 total_size  (includes chunk_id + total_size fields = 8 + payload)
    # Next chunk starts at chunk_offset + total_size.
    try:
        while offset < len(data):
            chunk_id = struct.unpack_from('<I', data, offset)[0]

            if chunk_id == CHUNK_NODE_BEGIN:
                # chunk_id=1 doubles as child's node_version=1.
                total_children = child_count + sector_count
                for _ in range(total_children):
                    child, offset, child_count_n = _parse_node(data, offset, file_version, warnings)
                    node.children.append(child)
                    node_count += child_count_n
                break
            elif chunk_id == CHUNK_NODE_END:
                offset += 4
                break

            # Read total_size and compute payload boundaries
            chunk_start = offset
            total_size = struct.unpack_from('<I', data, offset + 4)[0]
            if total_size < 8 or total_size > 10_000_000:
                warnings.append(f"Bad chunk {chunk_id} total_size={total_size} at node '{name}' offset {offset}")
                break
            payload = data[offset + 8:offset + total_size]
            payload_len = len(payload)

            try:
                if chunk_id == CHUNK_TRANSFORM:
                    node.transform = _parse_transform_payload(payload, file_version)
                elif chunk_id == CHUNK_MESH_TRANSFORM:
                    node.mesh_transform = _parse_transform_payload(payload, file_version)
                elif chunk_id == CHUNK_SOUND and payload_len >= 28:
                    node.sound = SoundData(params=list(struct.unpack_from('<7f', payload, 0)))
                elif chunk_id == CHUNK_WAYPOINT and payload_len >= 7:
                    wp_id = struct.unpack_from('<H', payload, 0)[0]
                    wp_param = struct.unpack_from('<I', payload, 2)[0]
                    conn_count = payload[6]
                    connections = []
                    for ci in range(conn_count):
                        if 7 + ci * 2 + 2 <= payload_len:
                            connections.append(struct.unpack_from('<H', payload, 7 + ci * 2)[0])
                    node.waypoint = WaypointData(wp_id=wp_id, wp_param=wp_param, connections=connections)
                elif chunk_id == CHUNK_SECTOR_PARAM and payload_len >= 4:
                    node.sector_param = SectorParam(value=struct.unpack_from('<I', payload, 0)[0])
                elif chunk_id == CHUNK_STRING and payload_len >= 4:
                    str_len = struct.unpack_from('<I', payload, 0)[0]
                    if str_len > 0 and 4 + str_len <= payload_len:
                        node.string_data = StringData(value=payload[4:4 + str_len].decode('ascii', errors='replace'))
                elif chunk_id == CHUNK_SOUND_SWITCH and payload_len >= 28:
                    node.sound_switch = SoundSwitchData(fields=list(struct.unpack_from('<7I', payload, 0)))
                elif chunk_id == CHUNK_DUMMY_BASIC and payload_len >= 14:
                    rx, ry, rz = struct.unpack_from('<3f', payload, 0)
                    node.dummy_basic = DummyBasicData(
                        radius_x=rx, radius_y=ry, radius_z=rz,
                        dummy_type=payload[12], dummy_flags=payload[13],
                    )
                elif chunk_id == CHUNK_PORTAL and payload_len >= 31:
                    node.portal = PortalData(
                        portal_fields=list(struct.unpack_from('<7I', payload, 0)),
                        portal_bytes=bytes(payload[28:31]),
                    )
                elif chunk_id == CHUNK_OCCLUDER and payload_len >= 4:
                    node.occluder = OccluderData(value=struct.unpack_from('<I', payload, 0)[0])
                elif chunk_id == CHUNK_RECOVERY and payload_len >= 4:
                    node.recovery = RecoveryData(recovery_id=struct.unpack_from('<I', payload, 0)[0])
                elif chunk_id == CHUNK_SPECTATOR and payload_len >= 8:
                    node.spectator = SpectatorData(
                        param1=struct.unpack_from('<I', payload, 0)[0],
                        param2=struct.unpack_from('<I', payload, 4)[0],
                    )
                elif chunk_id == CHUNK_SCRHELPER_FLAG and payload_len >= 4:
                    node.scrhelper_flag = ScrHelperFlag(flag=struct.unpack_from('<I', payload, 0)[0])
                elif chunk_id == CHUNK_FOG_COLOR and payload_len >= 4:
                    node.fog_color = FogColorData(color=struct.unpack_from('<I', payload, 0)[0])
                elif chunk_id == CHUNK_SCRHELPER and payload_len >= 12:
                    ht = struct.unpack_from('<I', payload, 0)[0]
                    hp1 = struct.unpack_from('<I', payload, 4)[0]
                    hp2 = struct.unpack_from('<I', payload, 8)[0]
                    hx = hy = hz = 0.0
                    if payload_len >= 24:
                        hx, hy, hz = struct.unpack_from('<3f', payload, 12)
                    node.scrhelper = ScrHelperData(
                        helper_type=ht, param1=hp1, param2=hp2,
                        pos_x=hx, pos_y=hy, pos_z=hz,
                    )
                elif chunk_id == CHUNK_LEVEL_ITEM and payload_len >= 4:
                    item_type = struct.unpack_from('<I', payload, 0)[0]
                    item_name = None
                    if payload_len >= 8:
                        name_len = struct.unpack_from('<I', payload, 4)[0]
                        if name_len > 0 and 8 + name_len <= payload_len:
                            item_name = payload[8:8 + name_len].decode('ascii', errors='replace')
                    node.level_item = LevelItemData(item_type=item_type, item_name=item_name)
                elif chunk_id in (CHUNK_EVENT_LINKS, CHUNK_FLAGS, CHUNK_CHILD_NODES,
                                  CHUNK_CHILD_NODES_EX, CHUNK_ANIM_PARAM, CHUNK_ANIMPATH_KEYS,
                                  CHUNK_LIGHT_EXT, CHUNK_SECTOR_DATA):
                    node.raw_chunks[chunk_id] = bytes(payload)
                else:
                    node.raw_chunks[chunk_id] = bytes(payload)
            except Exception as e:
                warnings.append(f"Error parsing chunk {chunk_id} in node '{name}': {e}")

            # Always advance by total_size (reliable skip)
            offset = chunk_start + total_size

    except Exception as e:
        node.parse_error = str(e)
        warnings.append(f"Error parsing node '{name}': {e}")

    return node, offset, node_count


def _parse_post_tree(data: bytes, offset: int, file_version: int,
                     warnings: List[str]) -> tuple:
    """Parse post-node-tree data. Returns (lighting, level_name, camera_fov,
    layer_vis, sound_areas, terrain, new_offset)."""
    lighting = None
    level_name = ""
    camera_fov = None
    layer_vis = None
    sound_areas: List[SoundArea] = []
    terrain = None

    try:
        # 7.1 Editor lighting state
        if offset + 4 > len(data):
            return lighting, level_name, camera_fov, layer_vis, sound_areas, terrain, offset

        light_version = struct.unpack_from('<I', data, offset)[0]
        if light_version in (1, 2):
            offset += 4
            # 3 ambient floats
            ambient = list(struct.unpack_from('<3f', data, offset))
            offset += 12
            # 3 light_dir_2 floats
            ld2 = list(struct.unpack_from('<3f', data, offset))
            offset += 12
            # 3 light_dir_1 floats
            ld1 = list(struct.unpack_from('<3f', data, offset))
            offset += 12
            # fog params: 6 u32s
            fp = struct.unpack_from('<6I', data, offset)
            offset += 24
            # fog clip/density: 3 floats
            far_clip, near_clip, density = struct.unpack_from('<3f', data, offset)
            offset += 12
            # scene params: 2 u32s
            sp1, sp2 = struct.unpack_from('<2I', data, offset)
            offset += 8

            extra1 = extra2 = None
            if light_version == 2:
                extra1, extra2 = struct.unpack_from('<2I', data, offset)
                offset += 8

            lighting = EditorLighting(
                version=light_version,
                ambient_r=ambient[0], ambient_g=ambient[1], ambient_b=ambient[2],
                light_dir_2=ld2, light_dir_1=ld1,
                fog_param_1=fp[0], fog_param_3=fp[1], fog_param_4=fp[2],
                fog_param_5=fp[3], fog_param_2=fp[4], fog_param_6=fp[5],
                fog_far_clip=far_clip, fog_near_clip=near_clip, fog_density=density,
                scene_param_1=sp1, scene_param_2=sp2,
                extra_param_1=extra1, extra_param_2=extra2,
            )
        else:
            warnings.append(f"Unexpected lighting version {light_version} at offset {offset}")

        # 7.2 File version flags
        if offset + 4 > len(data):
            return lighting, level_name, camera_fov, layer_vis, sound_areas, terrain, offset

        flags_bitmask = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        if flags_bitmask & 0x01:  # Level name
            level_name = data[offset:offset + 64].decode('ascii', errors='replace').rstrip('\x00')
            offset += 64
        if flags_bitmask & 0x02:  # 8 bytes skipped
            offset += 8
        if flags_bitmask & 0x04:  # Camera FOV
            camera_fov = struct.unpack_from('<f', data, offset)[0]
            offset += 4
        if flags_bitmask & 0x08:  # Unknown param
            offset += 4

        # 7.3 Layer visibility
        if offset + 4 > len(data):
            return lighting, level_name, camera_fov, layer_vis, sound_areas, terrain, offset
        layer_vis = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        # 7.4 Camera view bounds (version > 0xFF000002)
        if file_version > 0xFF000002 and offset + 4 <= len(data):
            sentinel = struct.unpack_from('<i', data, offset)[0]
            offset += 4
            if sentinel != -1:
                num_views = struct.unpack_from('<I', data, offset)[0]
                offset += 4
                for _ in range(num_views):
                    offset += 32  # view_data
                    num_refs = struct.unpack_from('<I', data, offset)[0]
                    offset += 4
                    for _ in range(num_refs):
                        offset += 12  # entity_slot(4) + entity_id(8)
                # zoom_level
                if offset + 4 <= len(data):
                    offset += 4

        # 7.5 Sound areas (version > 0xFF000004)
        if file_version > 0xFF000004 and offset + 4 <= len(data):
            sa_version = struct.unpack_from('<I', data, offset)[0]
            offset += 4
            if sa_version in (1, 2):
                while offset + 4 <= len(data):
                    area_index = struct.unpack_from('<i', data, offset)[0]
                    offset += 4
                    if area_index == -1:  # sentinel
                        break
                    name_len = struct.unpack_from('<I', data, offset)[0]
                    offset += 4
                    area_name = data[offset:offset + name_len].decode('ascii', errors='replace')
                    offset += name_len
                    p1, p2, p3, atype = struct.unpack_from('<4I', data, offset)
                    offset += 16
                    p4 = None
                    if sa_version == 2:
                        p4 = struct.unpack_from('<I', data, offset)[0]
                        offset += 4
                    sound_areas.append(SoundArea(
                        index=area_index, name=area_name, area_type=atype,
                        param1=p1, param2=p2, param3=p3, param4=p4,
                    ))

        # 7.6 Terrain sectors
        if offset + 8 <= len(data):
            magic = struct.unpack_from('<I', data, offset)[0]
            if magic == 0xAAEE:
                offset += 4
                terrain_size = struct.unpack_from('<I', data, offset)[0]
                offset += 4
                if terrain_size > 0:
                    terrain = _parse_terrain(data, offset, terrain_size, warnings)
                offset += terrain_size

    except Exception as e:
        warnings.append(f"Error parsing post-tree data at offset {offset}: {e}")

    return lighting, level_name, camera_fov, layer_vis, sound_areas, terrain, offset


def _parse_terrain(data: bytes, offset: int, size: int, warnings: List[str]) -> TerrainData:
    """Parse terrain section data."""
    td = TerrainData()
    end = offset + size

    try:
        # 4 pointers (used as flags: 0 = not present)
        ptrs = struct.unpack_from('<4I', data, offset)
        offset += 16

        if ptrs[0] != 0 and offset < end:
            # Null-terminated heightmap path
            nul = data.index(b'\x00', offset)
            td.heightmap_path = data[offset:nul].decode('ascii', errors='replace')
            offset = nul + 1

        if ptrs[1] != 0 and offset < end:
            nul = data.index(b'\x00', offset)
            td.texture_path = data[offset:nul].decode('ascii', errors='replace')
            offset = nul + 1

        if ptrs[2] != 0 and offset < end:
            nul = data.index(b'\x00', offset)
            td.detail_path = data[offset:nul].decode('ascii', errors='replace')
            offset = nul + 1

        # Remaining: sector structs (84 bytes each) with up to 5 conditional strings
        # Complex format - just store raw for now
        while offset + 84 <= end:
            sector_data = data[offset:offset + 84]
            offset += 84
            paths = []
            # Check up to 5 fields for non-zero → read null-terminated string
            fields = struct.unpack_from('<5I', sector_data, 0)
            for f in fields:
                if f != 0 and offset < end:
                    try:
                        nul = data.index(b'\x00', offset)
                        paths.append(data[offset:nul].decode('ascii', errors='replace'))
                        offset = nul + 1
                    except ValueError:
                        break
            td.sectors.append(TerrainSector(data=sector_data, paths=paths))

    except Exception as e:
        warnings.append(f"Error parsing terrain data: {e}")

    return td


def _parse_trailer(data: bytes, warnings: List[str]) -> Optional[ScoTrailer]:
    """Parse the SCO trailer (last 112 bytes)."""
    if len(data) < 112:
        warnings.append("File too small for trailer")
        return None

    t = len(data) - 112
    magic = struct.unpack_from('<I', data, t)[0]
    if magic != 0xABCC:
        warnings.append(f"Invalid trailer magic: {magic:#x} (expected 0xABCC)")
        return None

    tw, th, tds, to = struct.unpack_from('<4I', data, t + 4)
    ct = struct.unpack_from('<Q', data, t + 0x14)[0]
    mt = struct.unpack_from('<Q', data, t + 0x1C)[0]
    al, ao = struct.unpack_from('<2I', data, t + 0x24)
    cl, co = struct.unpack_from('<2I', data, t + 0x2C)
    sc, hc, oc = struct.unpack_from('<3I', data, t + 0x34)
    stats = list(struct.unpack_from('<7I', data, t + 0x40))
    cs = struct.unpack_from('<I', data, t + 0x5C)[0]
    c1 = struct.unpack_from('<I', data, t + 0x60)[0]
    lpo = struct.unpack_from('<I', data, t + 0x64)[0]
    lpl = struct.unpack_from('<I', data, t + 0x68)[0]
    slo = struct.unpack_from('<I', data, t + 0x6C)[0]

    trailer = ScoTrailer(
        magic=magic, thumb_width=tw, thumb_height=th,
        thumb_data_size=tds, thumb_offset=to,
        creation_time=ct, modified_time=mt,
        author_length=al, author_offset=ao,
        comment_length=cl, comment_offset=co,
        sector_count=sc, hidden_count=hc, object_count=oc,
        stats=stats, collision_size=cs, constant_1=c1,
        level_path_offset=lpo, level_path_length=lpl,
        sublevel_offset=slo,
    )

    # Resolve strings
    try:
        if al > 0 and ao + al <= len(data):
            trailer.author = data[ao:ao + al].decode('ascii', errors='replace').rstrip('\x00')
        if cl > 0 and co + cl <= len(data):
            trailer.comment = data[co:co + cl].decode('ascii', errors='replace').rstrip('\x00')
        if lpl > 0 and lpo + lpl <= len(data):
            trailer.level_path = data[lpo:lpo + lpl].decode('ascii', errors='replace').rstrip('\x00')
        if slo > 0 and slo + lpl <= len(data):
            trailer.sublevel = data[slo:slo + lpl].decode('ascii', errors='replace').rstrip('\x00')
    except Exception as e:
        warnings.append(f"Error resolving trailer strings: {e}")

    return trailer
