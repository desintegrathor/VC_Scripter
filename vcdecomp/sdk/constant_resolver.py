"""
Constant resolution - resolve numeric literals to SDK constant names.

Replaces magic numbers with meaningful constant names:
- 0 → SC_P_AI_BATTLEMODE_HOLD
- 1 → SC_LEV_MES_INITSCENE
- etc.
"""

from typing import Optional, Dict
from .sdk_database import SDKDatabase


class ConstantResolver:
    """Resolve numeric literals to SDK constant names."""

    # Context hints to constant prefix mappings
    CONTEXT_PREFIXES = {
        # AI battle modes
        'battle_mode': 'SC_P_AI_BATTLEMODE_',
        'battlemode': 'SC_P_AI_BATTLEMODE_',

        # AI peace modes
        'peace_mode': 'SC_P_AI_PEACEMODE_',
        'peacemode': 'SC_P_AI_PEACEMODE_',

        # AI move modes
        'move_mode': 'SC_P_AI_MOVEMODE_',
        'movemode': 'SC_P_AI_MOVEMODE_',

        # AI move positions
        'move_pos': 'SC_P_AI_MOVEPOS_',
        'movepos': 'SC_P_AI_MOVEPOS_',

        # Level script messages
        'level_message': 'SC_LEV_MES_',
        'lev_message': 'SC_LEV_MES_',
        'message': 'SC_LEV_MES_',  # Generic, may need refinement

        # Player script messages
        'player_message': 'SC_P_MES_',
        'p_message': 'SC_P_MES_',

        # Object event types
        'object_event': 'SC_OBJ_INFO_EVENT_',
        'obj_event': 'SC_OBJ_INFO_EVENT_',

        # Network messages
        'net_message': 'SC_NET_MES_',
        'network_message': 'SC_NET_MES_',

        # Player sides
        'side': 'SC_P_SIDE_',
        'player_side': 'SC_P_SIDE_',
    }

    # Function parameter to context mapping
    # Maps (function_name, param_index) → context hint
    FUNCTION_PARAM_CONTEXTS = {
        # AI battle mode functions
        ('SC_Ai_SetBattleMode', 2): 'battle_mode',
        ('SC_P_Ai_SetBattleMode', 1): 'battle_mode',

        # AI peace mode functions
        ('SC_Ai_SetPeaceMode', 2): 'peace_mode',
        ('SC_P_Ai_SetPeaceMode', 1): 'peace_mode',

        # AI move mode functions
        ('SC_P_Ai_SetMoveMode', 1): 'move_mode',

        # AI move position functions
        ('SC_P_Ai_SetMovePos', 1): 'move_pos',

        # Side parameters
        ('SC_Ai_SetBattleMode', 0): 'side',
        ('SC_Ai_SetPeaceMode', 0): 'side',
        ('SC_MP_EnumPlayers', 2): 'side',
        ('SC_P_Create', 1): 'side',  # Second parameter is side
    }

    # Special handling for callback message parameters
    # These are struct field accesses that indicate message types
    STRUCT_FIELD_CONTEXTS = {
        's_SC_L_info.message': 'level_message',
        's_SC_P_info.message': 'player_message',
        's_SC_OBJ_info.event_type': 'object_event',
    }

    def __init__(self, sdk_db: SDKDatabase):
        """
        Initialize constant resolver.

        Args:
            sdk_db: SDK database with constant definitions
        """
        self.sdk_db = sdk_db

        # Build reverse lookup: value → [names]
        self._value_to_names: Dict[int, list] = {}
        for name, value in sdk_db.constants.items():
            if value not in self._value_to_names:
                self._value_to_names[value] = []
            self._value_to_names[value].append(name)

    def resolve_constant(self, value: int, context: str = "") -> Optional[str]:
        """
        Resolve numeric value to constant name.

        Args:
            value: Numeric value (e.g., 0, 1, 2)
            context: Context hint (e.g., "battle_mode", "message_type")

        Returns:
            Constant name (e.g., "SC_P_AI_BATTLEMODE_HOLD") or None
        """
        candidates = self._value_to_names.get(value, [])
        if not candidates:
            return None

        # If context provided, filter by prefix
        if context:
            prefix = self.CONTEXT_PREFIXES.get(context.lower(), '')
            if prefix:
                filtered = [c for c in candidates if c.startswith(prefix)]
                if filtered:
                    return filtered[0]

        # No context or no match, return first candidate
        return candidates[0] if candidates else None

    def resolve_from_function_param(self, value: int, func_name: str,
                                    param_index: int) -> Optional[str]:
        """
        Resolve constant based on function parameter context.

        Args:
            value: Numeric value
            func_name: Function name (e.g., "SC_Ai_SetBattleMode")
            param_index: Parameter index (0-based)

        Returns:
            Constant name or None
        """
        # Look up context from function parameter mapping
        context = self.FUNCTION_PARAM_CONTEXTS.get((func_name, param_index))
        if context:
            return self.resolve_constant(value, context)

        return None

    def resolve_from_struct_field(self, value: int, struct_type: str,
                                  field_name: str) -> Optional[str]:
        """
        Resolve constant based on struct field access.

        Args:
            value: Numeric value
            struct_type: Structure type (e.g., "s_SC_L_info")
            field_name: Field name (e.g., "message")

        Returns:
            Constant name or None
        """
        # Look up context from struct field mapping
        field_key = f"{struct_type}.{field_name}"
        context = self.STRUCT_FIELD_CONTEXTS.get(field_key)
        if context:
            return self.resolve_constant(value, context)

        return None

    def infer_context_from_variable_name(self, var_name: str) -> Optional[str]:
        """
        Infer constant context from variable name patterns.

        Args:
            var_name: Variable name (e.g., "battle_mode", "side", "msg_type")

        Returns:
            Context hint or None
        """
        var_lower = var_name.lower()

        # Check for common patterns
        if 'battle' in var_lower and 'mode' in var_lower:
            return 'battle_mode'
        elif 'peace' in var_lower and 'mode' in var_lower:
            return 'peace_mode'
        elif 'move' in var_lower and 'mode' in var_lower:
            return 'move_mode'
        elif 'move' in var_lower and 'pos' in var_lower:
            return 'move_pos'
        elif 'side' in var_lower:
            return 'side'
        elif 'message' in var_lower or 'msg' in var_lower:
            return 'message'
        elif 'event' in var_lower:
            return 'object_event'

        return None

    def should_resolve_constant(self, value: int) -> bool:
        """
        Check if this value should be resolved to a constant.

        Small integers (0-20) are good candidates for named constants.
        Large values are likely memory addresses or data offsets.

        Args:
            value: Numeric value

        Returns:
            True if this value should be resolved
        """
        # Only resolve small positive integers that are likely enum values
        # Most SDK constants are in range 0-15
        return 0 <= value <= 20 and value in self._value_to_names

    def get_all_constants_for_value(self, value: int) -> list:
        """
        Get all constant names that have this value.

        Useful for debugging or providing alternatives.

        Args:
            value: Numeric value

        Returns:
            List of constant names (may be empty)
        """
        return self._value_to_names.get(value, [])
