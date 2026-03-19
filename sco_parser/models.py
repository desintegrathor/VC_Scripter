"""Data models for parsed .sco file structures."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ScoHeader:
    """SCO file header (100 bytes at offset 0x00)."""
    version: int
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    milliseconds: int
    day_of_week: int
    camera_x: float
    camera_y: float
    camera_z: float
    camera_yaw: float
    camera_pitch: float


@dataclass
class Entity:
    """BES file reference from the entity list."""
    index: int
    path: str


@dataclass
class Transform:
    """Node transform data (Chunk 2/3)."""
    matrix_count: int
    matrix_data: List[float]
    flags: Optional[int] = None
    bsphere: Optional[float] = None
    bsphere2: Optional[float] = None
    pos_x: Optional[float] = None
    pos_y: Optional[float] = None
    has_marker: bool = False

    @property
    def position(self) -> Optional[tuple]:
        """Extract world position. Returns (x, y, z) or None.

        In the transform payload, position is at floats[4], [5], [6]
        (payload offsets +20, +24, +28). These are stored as pos_x, pos_y,
        and matrix_data[6] (z).
        """
        if self.pos_x is not None and self.pos_y is not None:
            # Z from matrix_data[6] (payload offset +28, 7th float after flags)
            z = self.matrix_data[6] if len(self.matrix_data) > 6 else 0.0
            return (self.pos_x, self.pos_y, z)
        return None


@dataclass
class WaypointData:
    """Waypoint connection data (Chunk 6)."""
    wp_id: int
    wp_param: int
    connections: List[int] = field(default_factory=list)


@dataclass
class DummyBasicData:
    """Basic dummy node properties (Chunk 10)."""
    radius_x: float
    radius_y: float
    radius_z: float
    dummy_type: int
    dummy_flags: int


@dataclass
class ScrHelperData:
    """Script helper data (Chunk 19)."""
    helper_type: int
    param1: int
    param2: int
    pos_x: float
    pos_y: float
    pos_z: float


@dataclass
class SoundData:
    """Sound source properties (Chunk 5)."""
    params: List[float]  # 7 floats


@dataclass
class SoundSwitchData:
    """Sound switch/camera data (Chunk 9)."""
    fields: List[int]  # 7 u32s in non-sequential order


@dataclass
class PortalData:
    """Portal geometry data (Chunk 12)."""
    portal_fields: List[int]  # 7 u32s
    portal_bytes: bytes  # 3 bytes


@dataclass
class LevelItemData:
    """Level item data (Chunk 24)."""
    item_type: int
    item_name: Optional[str] = None


@dataclass
class StringData:
    """Portal/occluder name string (Chunk 8)."""
    value: str


@dataclass
class SectorParam:
    """Sector parameter (Chunk 7)."""
    value: int


@dataclass
class OccluderData:
    """Occluder parameter (Chunk 13)."""
    value: int


@dataclass
class RecoveryData:
    """Recovery point ID (Chunk 20)."""
    recovery_id: int


@dataclass
class SpectatorData:
    """Spectator camera data (Chunk 21)."""
    param1: int
    param2: int


@dataclass
class ScrHelperFlag:
    """Script helper flag (Chunk 23)."""
    flag: int


@dataclass
class FogColorData:
    """Fog color (Chunk 25)."""
    color: int


@dataclass
class SceneNode:
    """A node in the scene tree."""
    node_version: int
    child_count: int
    sector_count: int
    bes_index: int
    flags: int
    data_size: int
    param1: int
    param2: int
    name: str
    node_type: int = 0

    # Parsed chunk data
    transform: Optional[Transform] = None
    mesh_transform: Optional[Transform] = None
    waypoint: Optional[WaypointData] = None
    dummy_basic: Optional[DummyBasicData] = None
    scrhelper: Optional[ScrHelperData] = None
    scrhelper_flag: Optional[ScrHelperFlag] = None
    sound: Optional[SoundData] = None
    sound_switch: Optional[SoundSwitchData] = None
    portal: Optional[PortalData] = None
    level_item: Optional[LevelItemData] = None
    string_data: Optional[StringData] = None
    sector_param: Optional[SectorParam] = None
    occluder: Optional[OccluderData] = None
    recovery: Optional[RecoveryData] = None
    spectator: Optional[SpectatorData] = None
    fog_color: Optional[FogColorData] = None

    # Raw chunk data for unhandled/complex chunks
    raw_chunks: Dict[int, bytes] = field(default_factory=dict)

    # Child nodes
    children: List['SceneNode'] = field(default_factory=list)

    # Error tracking
    parse_error: Optional[str] = None

    @property
    def position(self) -> Optional[tuple]:
        """Get world position from transform."""
        if self.transform:
            return self.transform.position
        return None

    @property
    def total_children(self) -> int:
        return self.child_count + self.sector_count

    def node_type_name(self) -> str:
        """Human-readable node type from node_type field."""
        type_names = {
            0: "Root", 1: "Mesh", 3: "Light(sub)", 6: "Dummy", 7: "Light",
            8: "Event", 9: "Dummy(WP)", 10: "SndSw", 13: "WorldSector",
            14: "Portal", 15: "Occluder", 16: "LevelItem", 17: "FogColor",
            18: "Model", 19: "ScrHelper",
            0x101: "Player", 0x102: "AnimPath", 0x103: "MPHelper",
            0x104: "Recovery", 0x105: "Spectator", 0x106: "Northstar",
        }
        if self.node_type in type_names:
            return type_names[self.node_type]
        return f"Type({self.node_type:#x})"


@dataclass
class SoundArea:
    """Sound area definition."""
    index: int
    name: str
    area_type: int
    param1: int
    param2: int
    param3: int
    param4: Optional[int] = None


@dataclass
class EditorLighting:
    """Editor lighting state."""
    version: int
    ambient_r: float
    ambient_g: float
    ambient_b: float
    light_dir_2: List[float]  # 3 floats
    light_dir_1: List[float]  # 3 floats
    fog_param_1: int
    fog_param_3: int
    fog_param_4: int
    fog_param_5: int
    fog_param_2: int
    fog_param_6: int
    fog_far_clip: float
    fog_near_clip: float
    fog_density: float
    scene_param_1: int
    scene_param_2: int
    extra_param_1: Optional[int] = None
    extra_param_2: Optional[int] = None


@dataclass
class TerrainSector:
    """Terrain sector reference."""
    data: bytes  # 84 bytes raw
    paths: List[str] = field(default_factory=list)


@dataclass
class TerrainData:
    """Terrain section data."""
    heightmap_path: Optional[str] = None
    texture_path: Optional[str] = None
    detail_path: Optional[str] = None
    sectors: List[TerrainSector] = field(default_factory=list)


@dataclass
class ScoTrailer:
    """SCO trailer (last 112 bytes)."""
    magic: int
    thumb_width: int
    thumb_height: int
    thumb_data_size: int
    thumb_offset: int
    creation_time: int  # FILETIME as u64
    modified_time: int  # FILETIME as u64
    author_length: int
    author_offset: int
    comment_length: int
    comment_offset: int
    sector_count: int
    hidden_count: int
    object_count: int
    stats: List[int]  # stat_1 through stat_7
    collision_size: int
    constant_1: int
    level_path_offset: int
    level_path_length: int
    sublevel_offset: int
    # Resolved strings
    author: str = ""
    comment: str = ""
    level_path: str = ""
    sublevel: str = ""


@dataclass
class ScoFile:
    """Top-level container for a parsed .sco file."""
    file_path: str
    header: ScoHeader
    entities: List[Entity]
    root_node: Optional[SceneNode] = None
    lighting: Optional[EditorLighting] = None
    level_name: str = ""
    camera_fov: Optional[float] = None
    layer_visibility: Optional[int] = None
    sound_areas: List[SoundArea] = field(default_factory=list)
    terrain: Optional[TerrainData] = None
    trailer: Optional[ScoTrailer] = None
    # Parse diagnostics
    node_count: int = 0
    parse_warnings: List[str] = field(default_factory=list)
