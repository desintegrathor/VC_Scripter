"""
Script Type Detector for Vietcong Scripts.

Automatically detects the type of script (object, player, level, network, etc.)
based on XFN function usage, constant patterns, and other heuristics.

This allows the decompiler to use the correct parameter type:
- s_SC_OBJ_info for object scripts
- s_SC_NET_info for multiplayer/network scripts
- s_SC_P_info for player AI scripts
- s_SC_L_info for level scripts
- etc.
"""

from typing import Set, Optional
from .loader.scr_loader import SCRFile


class ScriptType:
    """Known script types with their info structure names."""

    OBJECT = "s_SC_OBJ_info"           # Object scripts (vehicles, props, etc.)
    NETWORK = "s_SC_NET_info"          # Multiplayer/network scripts
    PLAYER = "s_SC_P_info"             # Player AI scripts
    LEVEL = "s_SC_L_info"              # Level/mission scripts
    WEAPON = "s_SC_WEAP_info"          # Weapon scripts
    WEAPON_3PV = "s_SC_WEAP3pv_info"   # 3rd person weapon scripts
    SOUND = "s_SC_SOUND_info"          # Sound scripts
    HELPER = "s_SC_ScriptHelper_info"  # Script helper
    REMOTE_CAM = "s_SC_RC_info"        # Remote camera scripts


def detect_script_type(scr: SCRFile) -> str:
    """
    Detect the script type based on function usage and patterns.

    Args:
        scr: Loaded SCR file

    Returns:
        Structure type name (e.g., "s_SC_NET_info")
    """
    detector = ScriptTypeDetector(scr)
    return detector.detect()


class ScriptTypeDetector:
    """Detects script type using multiple strategies."""

    def __init__(self, scr: SCRFile):
        self.scr = scr
        self.xfn_functions: Set[str] = set()
        self._load_xfn_functions()

    def _load_xfn_functions(self):
        """Extract all function names from XFN table."""
        if not self.scr.xfn_table:
            return

        xfn_entries = getattr(self.scr.xfn_table, 'entries', [])
        for xfn in xfn_entries:
            if xfn.name:
                # Extract function name (before parentheses)
                paren_idx = xfn.name.find('(')
                func_name = xfn.name[:paren_idx] if paren_idx > 0 else xfn.name
                self.xfn_functions.add(func_name)

    def detect(self) -> str:
        """
        Run detection algorithm with priority-based checks.

        Priority order (with confidence levels):
        1. Level-exclusive functions (99% confidence)
        2. Network function dominance >30% (95% confidence)
        3. Player function dominance >30% (80% confidence)
        4. Weapon/Sound specific patterns (70% confidence)
        5. Object fallback (50% confidence)

        Returns:
            Script type structure name
        """
        # PRIORITY 1: Level-exclusive functions (STRONGEST indicator)
        # These functions are ONLY used by level scripts
        if self._has_level_exclusive_functions():
            return ScriptType.LEVEL

        # PRIORITY 2: Network function dominance (STRONG indicator)
        # Real network scripts have >30% SC_MP_/SC_NET_ functions
        # (tdm.scr has 75.9%, false positives have <10%)
        network_pct = self._calculate_network_percentage()
        if network_pct > 30.0:
            return ScriptType.NETWORK

        # PRIORITY 3: Player function dominance (MODERATE indicator)
        # Player AI scripts have >30% SC_P_* functions
        player_pct = self._calculate_player_percentage()
        if player_pct > 30.0:
            return ScriptType.PLAYER

        # PRIORITY 4: Weapon/Sound specific patterns
        if self._has_weapon_functions():
            return ScriptType.WEAPON

        if self._has_sound_functions():
            return ScriptType.SOUND

        # DEFAULT: Object script (most common type)
        return ScriptType.OBJECT

    def _has_level_exclusive_functions(self) -> bool:
        """
        Check for functions that ONLY level scripts use.

        These are mission control functions that are exclusive to level scripts.
        If ANY of these are present, the script is almost certainly s_SC_L_info.
        """
        level_exclusive = {
            'SC_MissionCompleted',
            'SC_MissionFailed',
            'SC_MissionFailedEx',
            'SC_MissionFailedDeathPlayer',
            'SC_MissionDone',
            'SC_TheEnd',
            'SC_SetObjectives',
            'SC_SetObjectivesNoSound',
            'SC_MissionSave',
            'SC_StorySkipEnable',
        }
        return any(func in level_exclusive for func in self.xfn_functions)

    def _calculate_network_percentage(self) -> float:
        """
        Calculate percentage of SC_MP_/SC_NET_ functions.

        Returns:
            Percentage (0-100) of network functions in XFN table
        """
        if not self.xfn_functions:
            return 0.0

        network_count = sum(
            1 for func in self.xfn_functions
            if func.startswith('SC_MP_') or func.startswith('SC_NET_')
        )
        return (network_count * 100.0) / len(self.xfn_functions)

    def _calculate_player_percentage(self) -> float:
        """
        Calculate percentage of SC_P_* functions.

        Returns:
            Percentage (0-100) of player functions in XFN table
        """
        if not self.xfn_functions:
            return 0.0

        player_count = sum(
            1 for func in self.xfn_functions
            if func.startswith('SC_P_')
        )
        return (player_count * 100.0) / len(self.xfn_functions)

    def _has_network_functions(self) -> bool:
        """
        Check for SC_MP_* or SC_NET_* functions (multiplayer/network).

        DEPRECATED: Use _calculate_network_percentage() instead for better accuracy.
        """
        return self._calculate_network_percentage() > 30.0

    def _has_sound_functions(self) -> bool:
        """Check for sound-specific functions."""
        sound_functions = {
            'SC_SND_PlaySound2D', 'SC_SND_PlaySound3D',
            'SC_SND_SetVolume', 'SC_SND_StopSound',
            'SC_SpeachRadio', 'SC_SpeechRadio2'
        }
        # Sound scripts are usually simple and only use sound functions
        # Check if majority of functions are sound-related
        if not self.xfn_functions:
            return False

        sound_count = sum(1 for f in self.xfn_functions if f in sound_functions)
        return sound_count > len(self.xfn_functions) * 0.5

    def _has_weapon_functions(self) -> bool:
        """Check for weapon-specific functions."""
        weapon_patterns = {
            'SC_Weap_', 'SC_WEAP_',
            'SC_W_', 'Weapon_',
            'SC_P_SetWeap', 'SC_P_GetWeap'
        }
        return any(
            any(func.startswith(prefix) or prefix in func for prefix in weapon_patterns)
            for func in self.xfn_functions
        )


    def get_parameter_type_info(self) -> tuple[str, str]:
        """
        Get both the structure type and a friendly parameter name.

        Returns:
            Tuple of (struct_type, param_name)
            e.g., ("s_SC_NET_info", "net_info")
        """
        script_type = self.detect()

        # Map structure types to friendly parameter names
        param_names = {
            ScriptType.OBJECT: "info",
            ScriptType.NETWORK: "net_info",
            ScriptType.PLAYER: "player_info",
            ScriptType.LEVEL: "level_info",
            ScriptType.WEAPON: "weapon_info",
            ScriptType.WEAPON_3PV: "weapon_info",
            ScriptType.SOUND: "sound_info",
            ScriptType.HELPER: "helper_info",
            ScriptType.REMOTE_CAM: "cam_info",
        }

        param_name = param_names.get(script_type, "info")
        return script_type, param_name
