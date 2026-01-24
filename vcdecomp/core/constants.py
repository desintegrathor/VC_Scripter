"""
Konstanty z Vietcong SDK hlaviček.

Použití:
    from .constants import get_constant_name, SCM_CONSTANTS, SGI_CONSTANTS

    # Nahrazení magic numbers symbolickými názvy
    name = get_constant_name("SCM", 6)  # -> "SCM_CREATE"
    name = get_constant_name("SGI", 10) # -> "SGI_DIFFICULTY"
"""

from typing import Optional, Dict

# Flag to track if constants have been loaded from headers
_CONSTANTS_LOADED = False

# =============================================================================
# Script Messages (SCM_*)
# Zprávy mezi skripty - používané v S_Mes() a info->message
# =============================================================================
SCM_CONSTANTS: Dict[int, str] = {
    1: "SCM_FEELDANGER",
    2: "SCM_RUN",
    3: "SCM_WARNABOUTENEMY",
    4: "SCM_BOOBYTRAPFOUND",
    5: "SCM_TAUNTRUNNER",
    6: "SCM_CREATE",
    7: "SCM_HEARDSOMETHING",
    8: "SCM_SETGPHASE",
    9: "SCM_ONWAYPOINT",
    10: "SCM_DISABLE",
    11: "SCM_ENABLE",
    12: "SCM_TELEPORT",
    13: "SCM_REMOVE",
    14: "SCM_CONFIRM",
    15: "SCM_TIMEDRUN",
    16: "SCM_WALK",
    17: "SCM_BATTLEWALK",
    18: "SCM_INITTRAP",
    19: "SCM_EXPLODETRAP",
    20: "SCM_DISARMTRAP",
    21: "SCM_TEAMKIA",
    22: "SCM_BATTLERUN",
    23: "SCM_RETREAT",
    24: "SCM_PANICRUN",
    25: "SCM_STARTWALK",
    26: "SCM_CHECKBODY",
    27: "SCM_GETBACK",
    28: "SCM_HUNTER",
    29: "SCM_RUNANDKILL",
    30: "SCM_PLAYANIM",
    31: "SCM_STARTPATROL",
    32: "SCM_MORTARLAND",
    33: "SCM_STARTMORTARFIRE",
    34: "SCM_STARTASSAULT",
    35: "SCM_WALK",
    36: "SCM_RUNATWP",
    37: "SCM_WALKATWP",
    38: "SCM_SHOOTING",
    39: "SCM_PATHWALK",
    40: "SCM_WPPATH_BEGIN",
    41: "SCM_WPPATH_CONTINUE",
    42: "SCM_WPPATH_END",
    43: "SCM_RUNWITHMORTAR",
    44: "SCM_SAPPERATTACK",
    45: "SCM_EXPLOSIVEPLANTED",
    46: "SCM_SUPPORTSAPPER",
    47: "SCM_EXITCAR",
    48: "SCM_MORTARPLACED",
    49: "SCM_CHANGETARGET",
    50: "SCM_CAREFULLASSAULT",
    51: "SCM_OBJECTUSED",
    52: "SCM_OBJECTDESTROYED",
    53: "SCM_DONE",
    54: "SCM_ENTERCAR",
    55: "SCM_THROWSMOKE",
    56: "SCM_SMOKETHROWED",
    57: "SCM_KAMIKADZE",
    58: "SCM_ENABLEINTERACTION",
    59: "SCM_DISABLEINTERACTION",
    60: "SCM_PLAYERINTERACTION",
    61: "SCM_TRAPACTIVATED",
    62: "SCM_EXITHELI",
    63: "SCM_RADIOCOM",
    64: "SCM_YOUARECOMMANDER",
    65: "SCM_GROUPRETREAT",
    66: "SCM_NEWCOMMANDER",
    70: "SCM_GOTO",
    71: "SCM_CANUSEMAP",
    72: "SCM_DO",
    73: "SCM_SETPHASE",
    74: "SCM_HELIIN",
    75: "SCM_HELIOUT",
    76: "SCM_FIRE",
    77: "SCM_RECOVER",
    78: "SCM_HELILOADED",
    79: "SCM_HELIEMPTY",
    80: "SCM_INFO",
    777: "SCM_MP_REINIT",
}

# =============================================================================
# Global Variable Indices (SGI_*)
# Pro SC_sgi() a SC_ggi() funkce
# =============================================================================
SGI_CONSTANTS: Dict[int, str] = {
    1: "SGI_MISSIONDEATHCOUNT",
    2: "SGI_MISSIONALARM",
    3: "SGI_TEAMDEATHCOUNT",
    4: "SGI_ALLYDEATHCOUNT",
    5: "SGI_GROUPDEATHCOUNT",
    6: "SGI_LEVELPHASE",
    7: "SGI_CHOPPER",
    8: "SGI_TEAMWIA",
    10: "SGI_DIFFICULTY",
    11: "SGI_GAMETYPE",
    12: "SGI_C4COUNT",
    13: "SGF_C4TIMER",
    200: "SGI_CURRENTMISSION",
    201: "SGF_MISSIONTIMER",
    2000: "SGI_INTELBASE",
    2081: "SGI_INTELCOUNT",
    2222: "SGI_PHASE",

    # Note: Values 499-503+ are game-mode-specific (GVAR_*) defined per-script.
    # Different game modes use these indices for different variables:
    # - ATG mode: 500=GVAR_SIDE0POINTS, 502=GVAR_MAINPHASE
    # - DM mode: may use different mappings
    # We intentionally do NOT map these to avoid incorrect symbolic names.
    # Let numeric values pass through - they're defined in the game script headers.
}

# =============================================================================
# Mission IDs (MISSION_*)
# =============================================================================
MISSION_CONSTANTS: Dict[int, str] = {
    0: "MISSION_BASECAMPARRIVAL",
    1: "MISSION_MEDPATROL",
    2: "MISSION_3CANYONSFIRST",
    3: "MISSION_3CANYONSA",
    4: "MISSION_3CANYONSB",
    5: "MISSION_BAHNARFIRST",
    6: "MISSION_BASECAMPFIRST",
    7: "MISSION_FRENCHROUTEA",
    8: "MISSION_FRENCHROUTEB",
    9: "MISSION_TUNNELS",
    10: "MISSION_ARROYO",
    11: "MISSION_TUNNELS2",
    12: "MISSION_BIGRIVER",
    13: "MISSION_NIGHT",
    14: "MISSION_NIGHT_B",
    15: "MISSION_AMBUSH",
    16: "MISSION_BIGVALLEY",
    17: "MISSION_OUTPOST",
    18: "MISSION_RADIORELAY",
    19: "MISSION_CRASHFLIGHT",
    20: "MISSION_CRASH",
    21: "MISSION_CONQUEST",
    22: "MISSION_NVABASE",
    23: "MISSION_UNDERGROUND",
    24: "MISSION_ESCAPE",
    25: "MISSION_PILOT",
    26: "MISSION_STREAM",
    27: "MISSION_BAHNARRAZEDA",
    28: "MISSION_BAHNARRAZEDB",
    29: "MISSION_BIGVALLEYCHOPPER",
    30: "MISSION_BASECAMPDEFEAT",
    31: "MISSION_BASECAMPDEFEAT2",
    32: "MISSION_BASECAMPDEFEAT3",
    # Addon missions
    50: "MISSION_BOMBERPILOT",
    51: "MISSION_PLEIKU",
    52: "MISSION_JARAI",
    53: "MISSION_HANGINGBRIDGE",
    54: "MISSION_NUIPEK",
    55: "MISSION_MINEFACTORY",
    56: "MISSION_NUIPEK2",
    57: "MISSION_BASEATTACK",
    58: "MISSION_NUIPEK3",
    59: "MISSION_DEATHVALLEYA",
    60: "MISSION_DEATHVALLEYB",
    61: "MISSION_NVACAMP",
}

# =============================================================================
# Player Types and Sides (SC_P_*)
# =============================================================================
SC_P_CONSTANTS: Dict[str, Dict[int, str]] = {
    "TYPE": {
        0: "SC_P_TYPE_PC",
        1: "SC_P_TYPE_AI",
    },
    "SIDE": {
        0: "SC_P_SIDE_US",
        1: "SC_P_SIDE_VC",
        2: "SC_P_SIDE_NEUTRAL",
    },
    "AI_MODE": {
        0: "SC_P_AI_MODE_PEACE",
        1: "SC_P_AI_MODE_BATTLE",
        2: "SC_P_AI_MODE_SCRIPT",
    },
    "AI_BATTLEMODE": {
        0: "SC_P_AI_BATTLEMODE_HOLD",
        1: "SC_P_AI_BATTLEMODE_ATTACK",
        2: "SC_P_AI_BATTLEMODE_RETREAT",
    },
    "AI_MOVEMODE": {
        # Values from sc_global.h
        0: "SC_P_AI_MOVEMODE_WALK",
        1: "SC_P_AI_MOVEMODE_AIM",
        2: "SC_P_AI_MOVEMODE_RUN",
    },
    "AI_MOVEPOS": {
        0: "SC_P_AI_MOVEPOS_STAND",
        1: "SC_P_AI_MOVEPOS_CROUCH",
        2: "SC_P_AI_MOVEPOS_PRONE",
    },
    "MESSAGE": {
        0: "SC_P_MES_TIME",
        1: "SC_P_MES_EVENT",
        2: "SC_P_MES_KILLED",
        3: "SC_P_MES_HIT",
    },
}

# =============================================================================
# Equipment IDs (BESID_*)
# =============================================================================
BESID_CONSTANTS: Dict[int, str] = {
    1: "BESID_KNIFE",
    2: "BESID_CLACKER",
    3: "BESID_SMOKE3PV",
    4: "BESID_SMOKEFPV",
    5: "BESID_C4FPV",
    6: "BESID_C4STG",
    7: "BESID_HANDAXE",
    8: "BESID_PICKAXE",
    9: "BESID_PIPE",
    10: "BESID_BEERS",
    11: "BESID_RADIOEAR",
    12: "BESID_BINOCULAR",
    13: "BESID_STIRRER",
    14: "BESID_WINE",
    15: "BESID_SHOVEL",
    16: "BESID_HAMMER",
    17: "BESID_MACHETTE",
    18: "BESID_NAILS",
    19: "BESID_CANTEEN",
    20: "BESID_WOOD",
    21: "BESID_NOTEBOOK",
    22: "BESID_GUITAR",
    23: "BESID_PENCIL",
    24: "BESID_HARMONY",
}

# =============================================================================
# Boolean values
# =============================================================================
BOOL_CONSTANTS: Dict[int, str] = {
    0: "FALSE",
    1: "TRUE",
}


def load_constants_from_headers() -> None:
    """
    Load constants dynamically from parsed header files.

    This supplements the hardcoded constants with all definitions from
    SC_GLOBAL.H and SC_DEF.H, providing 80+ SGI constants instead of ~20.

    Called automatically on first use of get_constant_name().
    """
    global _CONSTANTS_LOADED

    if _CONSTANTS_LOADED:
        return

    try:
        from .headers.database import get_header_database
        db = get_header_database()

        # Load all SGI_ constants (global variable indices)
        sgi_constants = db.get_constants_by_prefix('SGI')
        for name, data in sgi_constants.items():
            try:
                value_str = data.get('value', '')
                # Parse hex (0x...) or decimal
                if value_str.startswith('0x'):
                    value = int(value_str, 16)
                else:
                    value = int(value_str)

                # Only add if not already in hardcoded table
                # (hardcoded takes precedence for backwards compat)
                if value not in SGI_CONSTANTS:
                    SGI_CONSTANTS[value] = name
            except (ValueError, TypeError):
                pass

        # Load all SGF_ constants (float globals - same as SGI)
        sgf_constants = db.get_constants_by_prefix('SGF')
        for name, data in sgf_constants.items():
            try:
                value_str = data.get('value', '')
                if value_str.startswith('0x'):
                    value = int(value_str, 16)
                else:
                    value = int(value_str)

                if value not in SGI_CONSTANTS:
                    SGI_CONSTANTS[value] = name
            except (ValueError, TypeError):
                pass

        # Load all GVAR_ constants (documented global indices)
        gvar_constants = db.get_constants_by_prefix('GVAR')
        for name, data in gvar_constants.items():
            try:
                value_str = data.get('value', '')
                if value_str.startswith('0x'):
                    value = int(value_str, 16)
                else:
                    value = int(value_str)

                if value not in SGI_CONSTANTS:
                    SGI_CONSTANTS[value] = name
            except (ValueError, TypeError):
                pass

        # Load additional SCM_ constants from headers
        scm_constants = db.get_constants_by_prefix('SCM')
        for name, data in scm_constants.items():
            try:
                value_str = data.get('value', '')
                if value_str.startswith('0x'):
                    value = int(value_str, 16)
                else:
                    value = int(value_str)

                if value not in SCM_CONSTANTS:
                    SCM_CONSTANTS[value] = name
            except (ValueError, TypeError):
                pass

        _CONSTANTS_LOADED = True

    except Exception as e:
        # Gracefully handle missing headers - use hardcoded fallback
        import warnings
        warnings.warn(f"Could not load constants from headers: {e}")
        _CONSTANTS_LOADED = True  # Don't retry


def get_constant_name(prefix: str, value: int) -> Optional[str]:
    """
    Získá symbolický název konstanty podle prefixu a hodnoty.

    Automatically loads constants from headers on first call.

    Args:
        prefix: Prefix konstanty ("SCM", "SGI", "MISSION", "BESID", "BOOL")
        value: Numerická hodnota

    Returns:
        Symbolický název nebo None

    Examples:
        get_constant_name("SCM", 6) -> "SCM_CREATE"
        get_constant_name("SGI", 10) -> "SGI_DIFFICULTY"
        get_constant_name("BOOL", 1) -> "TRUE"
    """
    # Load from headers on first use
    load_constants_from_headers()

    tables = {
        "SCM": SCM_CONSTANTS,
        "SGI": SGI_CONSTANTS,
        "SGF": SGI_CONSTANTS,  # Float globals use same table
        "MISSION": MISSION_CONSTANTS,
        "BESID": BESID_CONSTANTS,
        "BOOL": BOOL_CONSTANTS,
    }

    table = tables.get(prefix.upper())
    if table:
        name = table.get(value)
        # If GVAR_* is used outside SGI/SGF contexts, fall back to literal
        if name and name.startswith("GVAR_") and prefix.upper() not in ("SGI", "SGF"):
            return None
        return name
    return None


def get_player_constant(category: str, value: int) -> Optional[str]:
    """
    Získá symbolický název pro player-related konstanty.

    Args:
        category: Kategorie ("TYPE", "SIDE", "AI_MODE", "AI_BATTLEMODE", "AI_MOVEMODE", "AI_MOVEPOS", "MESSAGE")
        value: Numerická hodnota

    Returns:
        Symbolický název nebo None

    Examples:
        get_player_constant("SIDE", 0) -> "SC_P_SIDE_US"
        get_player_constant("AI_MODE", 1) -> "SC_P_AI_MODE_BATTLE"
    """
    category_table = SC_P_CONSTANTS.get(category.upper())
    if category_table:
        return category_table.get(value)
    return None


# Kontextové nahrazení - které funkce používají které konstanty
FUNCTION_CONSTANT_CONTEXT: Dict[str, str] = {
    # Funkce -> typ konstanty pro první argument
    "SC_sgi": "SGI",
    "SC_ggi": "SGI",
    "SC_sgf": "SGF",
    "SC_ggf": "SGF",
    "SC_P_Ai_SetMode": "AI_MODE",
    "SC_P_Ai_SetBattleMode": "AI_BATTLEMODE",
    "SC_P_Ai_SetMoveMode": "AI_MOVEMODE",
    "SC_P_Ai_SetMovePos": "AI_MOVEPOS",
    "S_Mes": "SCM",  # Druhý argument je message type
}
