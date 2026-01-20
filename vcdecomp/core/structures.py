"""
Structure definitions for Vietcong scripts.

Extracted from sc_global.h and other SDK headers.
Used for field access detection and structure layout analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class StructField:
    """Single field in a structure."""
    offset: int
    name: str
    type_name: str
    size: int
    is_pointer: bool = False
    is_array: bool = False
    array_count: int = 1


@dataclass
class StructDef:
    """Structure definition."""
    name: str
    size: int
    fields: List[StructField]

    def get_field_at_offset(self, offset: int) -> Optional[StructField]:
        """Get field at specific byte offset."""
        for field in self.fields:
            if field.offset == offset:
                return field
            # Check if offset is within array bounds
            if field.is_array:
                field_end = field.offset + (field.size * field.array_count)
                if field.offset <= offset < field_end:
                    return field
        return None

    def get_field_name_at_offset(self, offset: int) -> Optional[str]:
        """Get field name at offset, with array index if applicable."""
        field = self.get_field_at_offset(offset)
        if not field:
            return None
        if field.is_array and offset != field.offset:
            index = (offset - field.offset) // field.size
            return f"{field.name}[{index}]"
        return field.name


# ============================================================================
# Core types
# ============================================================================

STRUCT_C_VECTOR3 = StructDef(
    name="c_Vector3",
    size=12,
    fields=[
        StructField(0, "x", "float", 4),
        StructField(4, "y", "float", 4),
        StructField(8, "z", "float", 4),
    ]
)

STRUCT_S_SPHERE = StructDef(
    name="s_sphere",
    size=16,
    fields=[
        StructField(0, "pos", "c_Vector3", 12),
        StructField(12, "rad", "float", 4),
    ]
)


# ============================================================================
# Player script info structure (passed to ScriptMain)
# ============================================================================

STRUCT_S_SC_P_INFO = StructDef(
    name="s_SC_P_info",
    size=28,
    fields=[
        StructField(0, "message", "dword", 4),
        StructField(4, "param1", "dword", 4),
        StructField(8, "param2", "dword", 4),
        StructField(12, "pl_id", "dword", 4),
        StructField(16, "pos", "void*", 4, is_pointer=True),
        StructField(20, "elapsed_time", "float", 4),
        StructField(24, "next_exe_time", "float", 4),
    ]
)


# ============================================================================
# Player creation structures
# ============================================================================

STRUCT_S_SC_P_CREATEEQP = StructDef(
    name="s_SC_P_CreateEqp",
    size=8,
    fields=[
        StructField(0, "bes", "char*", 4, is_pointer=True),
        StructField(4, "eqp", "char*", 4, is_pointer=True),
    ]
)

STRUCT_S_SC_P_CREATE = StructDef(
    name="s_SC_P_Create",
    size=156,
    fields=[
        StructField(0, "type", "dword", 4),
        StructField(4, "side", "dword", 4),
        StructField(8, "group", "dword", 4),
        StructField(12, "member_id", "dword", 4),
        StructField(16, "name_nr", "dword", 4),
        StructField(20, "debrief_group", "dword", 4),
        StructField(24, "inifile", "char*", 4, is_pointer=True),
        StructField(28, "recover_pos", "void*", 4, is_pointer=True),
        StructField(32, "icon_name", "char*", 4, is_pointer=True),
        StructField(36, "flags", "dword", 4),
        StructField(40, "weap_knife", "dword", 4),
        StructField(44, "weap_pistol", "dword", 4),
        StructField(48, "weap_main1", "dword", 4),
        StructField(52, "weap_main2", "dword", 4),
        StructField(56, "weap_slot1", "dword", 4),
        StructField(60, "weap_slot6", "dword", 4),
        StructField(64, "weap_slot7", "dword", 4),
        StructField(68, "weap_slot8", "dword", 4),
        StructField(72, "weap_slot9", "dword", 4),
        StructField(76, "weap_slot10", "dword", 4),
        StructField(80, "force_sel_slot", "dword", 4),
        StructField(84, "eqps", "dword", 4),
        StructField(88, "eqp", "s_SC_P_CreateEqp*", 4, is_pointer=True),
        StructField(92, "aeg_valid_head_bes", "dword", 4, is_array=True, array_count=8),
        StructField(124, "aeg_valid_body_bes", "dword", 4, is_array=True, array_count=8),
    ]
)


# ============================================================================
# Level script info structure
# ============================================================================

STRUCT_S_SC_L_INFO = StructDef(
    name="s_SC_L_info",
    size=36,
    fields=[
        StructField(0, "message", "dword", 4),
        StructField(4, "param1", "dword", 4),
        StructField(8, "param2", "dword", 4),
        StructField(12, "param3", "dword", 4),
        StructField(16, "elapsed_time", "float", 4),
        StructField(20, "next_exe_time", "float", 4),
        StructField(24, "param4", "c_Vector3", 12),
    ]
)

# ============================================================================
# Multiplayer/Network script info structure (for MP scripts like TDM)
# ============================================================================

STRUCT_S_SC_NET_INFO = StructDef(
    name="s_SC_NET_info",
    size=24,
    fields=[
        StructField(0, "message", "dword", 4),
        StructField(4, "param1", "dword", 4),
        StructField(8, "param2", "dword", 4),
        StructField(12, "param3", "dword", 4),
        StructField(16, "elapsed_time", "float", 4),
        StructField(20, "fval1", "float", 4),
    ]
)


# ============================================================================
# AI properties structure (very large - 128 bytes)
# ============================================================================

STRUCT_S_SC_P_AI_PROPS = StructDef(
    name="s_SC_P_AI_props",
    size=128,
    fields=[
        StructField(0, "max_vis_distance", "float", 4),
        StructField(4, "watchfulness_zerodist", "float", 4),
        StructField(8, "watchfulness_maxdistance", "float", 4),
        StructField(12, "boldness", "float", 4),
        StructField(16, "coveramount", "float", 4),
        StructField(20, "shoot_imprecision", "float", 4),
        StructField(24, "extend_searchway", "BOOL", 4),
        StructField(28, "shortdistance_fight", "float", 4),
        StructField(32, "view_angle", "float", 4),
        StructField(36, "view_angle_near", "float", 4),
        StructField(40, "hear_imprecision", "float", 4),
        StructField(44, "hear_distance_mult", "float", 4),
        StructField(48, "hear_distance_max", "float", 4),
        StructField(52, "grenade_min_distance", "float", 4),
        StructField(56, "grenade_timing_imprecision", "float", 4),
        StructField(60, "grenade_throw_imprecision", "float", 4),
        StructField(64, "grenade_sure_time", "float", 4),
        StructField(68, "forget_enemy_mult", "float", 4),
        StructField(72, "shoot_damage_mult", "float", 4),
        StructField(76, "disable_peace_crouch", "BOOL", 4),
        StructField(80, "peace_fakeenemy_run", "float", 4),
        StructField(84, "peace_fakeenemy_phase", "float", 4),
        StructField(88, "shoot_while_hidding", "float", 4),
        StructField(92, "reaction_time", "float", 4),
        StructField(96, "scout", "float", 4),
        StructField(100, "berserk", "float", 4),
        StructField(104, "aimtime_max", "float", 4),
        StructField(108, "aimtime_canshoot", "float", 4),
        StructField(112, "aimtime_rotmult", "float", 4),
        StructField(116, "wounded_start_perc", "float", 4),
        StructField(120, "wounded_aimtime_mult_max", "float", 4),
        StructField(124, "wounded_shoot_imprec_plus", "float", 4),
    ]
)


# ============================================================================
# Player info (from SC_P_GetInfo)
# ============================================================================

STRUCT_S_SC_P_GETINFO = StructDef(
    name="s_SC_P_getinfo",
    size=20,
    fields=[
        StructField(0, "cur_hp", "float", 4),
        StructField(4, "max_hp", "float", 4),
        StructField(8, "side", "dword", 4),
        StructField(12, "group", "dword", 4),
        StructField(16, "member_id", "dword", 4),
    ]
)


# ============================================================================
# AI Battle Props
# ============================================================================

STRUCT_S_SC_P_AI_BATTLEPROPS = StructDef(
    name="s_SC_P_Ai_BattleProps",
    size=16,
    fields=[
        StructField(0, "Position", "float", 4),
        StructField(4, "Aim", "float", 4),
        StructField(8, "Run", "float", 4),
        # Note: original has only 3 fields = 12 bytes, but aligned to 16
    ]
)


# ============================================================================
# Object info structure (for SC_OBJ scripts)
# ============================================================================

STRUCT_S_SC_OBJ_INFO = StructDef(
    name="s_SC_OBJ_info",
    size=40,
    fields=[
        StructField(0, "event_type", "dword", 4),
        StructField(4, "master_nod", "void*", 4, is_pointer=True),
        StructField(8, "nod", "void*", 4, is_pointer=True),
        StructField(12, "new_hp_obtained", "float", 4),
        StructField(16, "hit_by", "dword", 4),
        StructField(20, "world_pos", "c_Vector3*", 4, is_pointer=True),
        StructField(24, "world_dir", "c_Vector3*", 4, is_pointer=True),
        StructField(28, "time", "float", 4),
    ]
)


# ============================================================================
# Objective structure
# ============================================================================

STRUCT_S_SC_OBJECTIVE = StructDef(
    name="s_SC_Objective",
    size=16,
    fields=[
        StructField(0, "text_nr", "dword", 4),
        StructField(4, "status", "dword", 4),
        StructField(8, "type", "dword", 4),
        StructField(12, "prio", "dword", 4),
    ]
)


# ============================================================================
# Init structures
# ============================================================================

STRUCT_S_SC_INITSIDE = StructDef(
    name="s_SC_initside",
    size=8,
    fields=[
        StructField(0, "MaxHideOutsStatus", "dword", 4),
        StructField(4, "MaxGroups", "dword", 4),
    ]
)

STRUCT_S_SC_INITGROUP = StructDef(
    name="s_SC_initgroup",
    size=20,
    fields=[
        StructField(0, "SideId", "dword", 4),
        StructField(4, "GroupId", "dword", 4),
        StructField(8, "MaxPlayers", "dword", 4),
        StructField(12, "NoHoldFireDistance", "float", 4),
        StructField(16, "follow_point_max_distance", "float", 4),
    ]
)


# ============================================================================
# Multiplayer structures (TDM, CTF, etc.)
# ============================================================================

STRUCT_S_SC_MP_SRV_SETTINGS = StructDef(
    name="s_SC_MP_SRV_settings",
    size=28,  # 4 + 4 + 4 + 6*4 = 28 bytes
    fields=[
        StructField(0, "coop_respawn_time", "dword", 4),
        StructField(4, "coop_respawn_limit", "dword", 4),
        StructField(8, "dm_weap_resp_time", "dword", 4),
        StructField(12, "atg_class_limit", "dword", 4, is_array=True, array_count=6),
    ]
)

STRUCT_S_SC_MP_HUD = StructDef(
    name="s_SC_MP_hud",
    size=60,  # 4 + 4 + 4 + 4 + 8 + 8 + 4 + 4 + 20 = 60 bytes
    fields=[
        StructField(0, "title", "dword", 4),
        StructField(4, "use_sides", "BOOL", 4),
        StructField(8, "disableUSside", "BOOL", 4),
        StructField(12, "disableVCside", "BOOL", 4),
        StructField(16, "side_name", "dword", 4, is_array=True, array_count=2),
        StructField(24, "side_color", "dword", 4, is_array=True, array_count=2),
        StructField(32, "pl_mask", "dword", 4),
        StructField(36, "side_mask", "dword", 4),
        StructField(40, "sort_by", "dword", 4, is_array=True, array_count=5),
    ]
)

STRUCT_S_SC_HUD_MP_ICON = StructDef(
    name="s_SC_HUD_MP_icon",
    size=16,
    fields=[
        StructField(0, "icon_id", "dword", 4),
        StructField(4, "type", "dword", 4),
        StructField(8, "value", "int", 4),
        StructField(12, "color", "dword", 4),
    ]
)

STRUCT_S_SC_MP_ENUMPAYERS = StructDef(
    name="s_SC_MP_EnumPlayers",
    size=16,  # 4 + 4 + 4 + 4 = 16 bytes
    fields=[
        StructField(0, "id", "dword", 4),
        StructField(4, "side", "dword", 4),
        StructField(8, "status", "dword", 4),
        StructField(12, "name", "char*", 4, is_pointer=True),
    ]
)

STRUCT_S_SC_MP_RECOVER = StructDef(
    name="s_SC_MP_Recover",
    size=16,
    fields=[
        StructField(0, "pos", "c_Vector3", 12),
        StructField(12, "rz", "float", 4),
    ]
)


# ============================================================================
# Registry - all structures by name and size
# ============================================================================

# Base hardcoded structures (legacy - will be merged with SDK structures)
_HARDCODED_STRUCTURES: Dict[str, StructDef] = {
    "c_Vector3": STRUCT_C_VECTOR3,
    "s_sphere": STRUCT_S_SPHERE,
    "s_SC_P_info": STRUCT_S_SC_P_INFO,
    "s_SC_P_CreateEqp": STRUCT_S_SC_P_CREATEEQP,
    "s_SC_P_Create": STRUCT_S_SC_P_CREATE,
    "s_SC_L_info": STRUCT_S_SC_L_INFO,
    "s_SC_NET_info": STRUCT_S_SC_NET_INFO,
    "s_SC_P_AI_props": STRUCT_S_SC_P_AI_PROPS,
    "s_SC_P_getinfo": STRUCT_S_SC_P_GETINFO,
    "s_SC_P_Ai_BattleProps": STRUCT_S_SC_P_AI_BATTLEPROPS,
    "s_SC_OBJ_info": STRUCT_S_SC_OBJ_INFO,
    "s_SC_Objective": STRUCT_S_SC_OBJECTIVE,
    "s_SC_initside": STRUCT_S_SC_INITSIDE,
    "s_SC_initgroup": STRUCT_S_SC_INITGROUP,
    "s_SC_MP_SRV_settings": STRUCT_S_SC_MP_SRV_SETTINGS,
    "s_SC_MP_hud": STRUCT_S_SC_MP_HUD,
    "s_SC_HUD_MP_icon": STRUCT_S_SC_HUD_MP_ICON,
    "s_SC_MP_EnumPlayers": STRUCT_S_SC_MP_ENUMPAYERS,
    "s_SC_MP_Recover": STRUCT_S_SC_MP_RECOVER,
}


def _load_sdk_structures() -> Dict[str, StructDef]:
    """
    Load structure definitions from SDK database.

    Returns:
        Dictionary of structure name -> StructDef
    """
    try:
        from ..sdk import SDKDatabase

        sdk_db = SDKDatabase()
        sdk_structs = {}

        for struct_name, sdk_struct in sdk_db.structures.items():
            # Convert SDK StructDefinition to our StructDef format
            fields = []
            for sdk_field in sdk_struct.fields:
                field = StructField(
                    offset=sdk_field.offset,
                    name=sdk_field.name,
                    type_name=sdk_field.type,
                    size=sdk_field.size,
                    is_pointer=sdk_field.type.endswith('*'),
                    is_array=sdk_field.is_array,
                    array_count=sdk_field.array_size if sdk_field.is_array else 1
                )
                fields.append(field)

            sdk_structs[struct_name] = StructDef(
                name=struct_name,
                size=sdk_struct.size,
                fields=fields
            )

        return sdk_structs
    except Exception:
        # SDK not available, return empty dict
        return {}


# Merge hardcoded structures with SDK structures
# SDK structures override hardcoded ones if there's a conflict
ALL_STRUCTURES: Dict[str, StructDef] = _HARDCODED_STRUCTURES.copy()
_sdk_structures = _load_sdk_structures()
ALL_STRUCTURES.update(_sdk_structures)  # SDK takes priority

# Map size -> possible structures (for heuristic detection)
STRUCTURES_BY_SIZE: Dict[int, List[str]] = {}
for name, struct in ALL_STRUCTURES.items():
    if struct.size not in STRUCTURES_BY_SIZE:
        STRUCTURES_BY_SIZE[struct.size] = []
    STRUCTURES_BY_SIZE[struct.size].append(name)


def get_struct_by_name(name: str) -> Optional[StructDef]:
    """Get structure definition by name."""
    return ALL_STRUCTURES.get(name)


def get_struct_by_size(size: int) -> List[StructDef]:
    """Get possible structures matching a given size."""
    names = STRUCTURES_BY_SIZE.get(size, [])
    return [ALL_STRUCTURES[n] for n in names]


def get_field_at_offset(struct_name: str, offset: int) -> Optional[str]:
    """
    Get field name at offset for named structure.

    Tries HeaderDatabase first (dynamic parsing), falls back to hardcoded structures.
    """
    # PRIORITY 1: Try HeaderDatabase (parsed from sc_global.h/sc_def.h)
    from .headers.database import get_header_database

    try:
        db = get_header_database()
        field_name = db.lookup_field_name(struct_name, offset)

        # Only use HeaderDatabase result if it's not a fallback generic name
        if field_name and not field_name.startswith("field_"):
            return field_name
    except Exception:
        pass  # Fallback to hardcoded structures

    # PRIORITY 2: Hardcoded structures (legacy)
    struct = get_struct_by_name(struct_name)
    if struct:
        return struct.get_field_name_at_offset(offset)

    return None


# ============================================================================
# Function parameter type hints
# Used to infer structure types from function calls
# ============================================================================

FUNCTION_STRUCT_PARAMS: Dict[str, Dict[int, str]] = {
    # SC_P_Create takes pointer to s_SC_P_Create
    "SC_P_Create": {0: "s_SC_P_Create"},
    # SC_P_GetInfo takes pointer to s_SC_P_getinfo
    "SC_P_GetInfo": {1: "s_SC_P_getinfo"},
    # SC_P_Ai_GetProps takes pointer to s_SC_P_AI_props
    "SC_P_Ai_GetProps": {1: "s_SC_P_AI_props"},
    "SC_P_Ai_SetProps": {1: "s_SC_P_AI_props"},
    # SC_P_GetPos takes pointer to c_Vector3
    "SC_P_GetPos": {1: "c_Vector3"},
    "SC_P_SetPos": {1: "c_Vector3"},
    # Sphere-based functions
    "SC_GetPls": {0: "s_sphere"},
    "SC_GetRndWp": {0: "s_sphere", 1: "c_Vector3"},
    # Zone functions
    "SC_NOD_GetWorldPos": {1: "c_Vector3"},
    # ZeroMem - need size analysis
    "SC_ZeroMem": {},  # First arg is pointer, second is size
    # FIX #5: Multiplayer/networking functions
    "SC_MP_GetSRVsettings": {0: "s_SC_MP_SRV_settings"},
    "SC_MP_HUD_SetTabInfo": {0: "s_SC_MP_hud"},
    "SC_MP_SetIconHUD": {0: "s_SC_HUD_MP_icon"},
    "SC_MP_EnumPlayers": {0: "s_SC_MP_EnumPlayers"},
    # Phase 2: Missing functions from field_tracker.py
    "SC_MP_SRV_GetAtgSettings": {0: "s_SC_MP_SRV_AtgSettings"},
    "SC_NOD_GetInfo": {0: "s_SC_OBJ_info"},
    "SC_L_GetInfo": {0: "s_SC_L_info"},
}


def infer_struct_from_function(func_name: str, arg_index: int) -> Optional[str]:
    """Infer structure type from function parameter."""
    params = FUNCTION_STRUCT_PARAMS.get(func_name, {})
    return params.get(arg_index)
