"""
Parse Vietcong Scripting SDK documentation to extract structured information.

Extracts:
- Function signatures (734 functions)
- Structure definitions (46 structs)
- Constant definitions (98+ constants)
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from pathlib import Path


@dataclass
class ParsedFunction:
    """Parsed function signature from SDK."""
    name: str
    return_type: str
    parameters: List[Tuple[str, str]]  # [(type, name), ...]


@dataclass
class ParsedStructField:
    """Parsed structure field."""
    name: str
    type: str
    size: int  # Size in bytes
    is_array: bool = False
    array_size: int = 0


@dataclass
class ParsedStruct:
    """Parsed structure definition."""
    name: str
    fields: List[ParsedStructField]


class SDKParser:
    """Parse Vietcong Scripting SDK documentation."""

    # Type sizes (in bytes)
    TYPE_SIZES = {
        'dword': 4,
        'int': 4,
        'BOOL': 4,
        'float': 4,
        'double': 8,
        'char': 1,
        'short': 2,
        'ushort': 2,
        'void*': 4,
        'char*': 4,
        'ushort*': 4,
        'dword*': 4,
        'int*': 4,
        'float*': 4,
        'c_Vector3': 12,  # 3 floats
        'c_Vector3*': 4,  # Pointer
        's_sphere': 16,   # c_Vector3 (12) + float (4)
        's_sphere*': 4,   # Pointer
    }

    def __init__(self, sdk_path: str):
        self.sdk_path = Path(sdk_path)
        if not self.sdk_path.exists():
            raise FileNotFoundError(f"SDK file not found: {sdk_path}")

        with open(self.sdk_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.content = f.read()

    def parse_functions(self) -> List[ParsedFunction]:
        """
        Extract all SC_* function signatures.

        Pattern: return_type SC_FunctionName(param_type param, ...);
        """
        functions = []

        # Pattern to match function signatures
        # Matches: void SC_Something(...); or BOOL SC_Something(...);
        pattern = r'^(void|BOOL|dword|float|int|char\s*\*|ushort\s*\*)\s+(SC_\w+)\s*\((.*?)\)\s*;'

        for match in re.finditer(pattern, self.content, re.MULTILINE | re.DOTALL):
            return_type = match.group(1).strip()
            func_name = match.group(2).strip()
            params_str = match.group(3).strip()

            # Parse parameters
            parameters = self._parse_parameters(params_str)

            functions.append(ParsedFunction(
                name=func_name,
                return_type=return_type,
                parameters=parameters
            ))

        return functions

    def _parse_parameters(self, params_str: str) -> List[Tuple[str, str]]:
        """Parse function parameter list."""
        if not params_str or params_str == 'void':
            return []

        parameters = []

        # Split by comma, but handle nested types (e.g., struct pointers)
        # Simple approach: split by comma and parse each
        param_parts = params_str.split(',')

        for param in param_parts:
            param = param.strip()
            if not param:
                continue

            # Handle parameter format: "type name" or "type *name" or "type name[size]"
            # Examples:
            # - "dword pl_id"
            # - "c_Vector3 *pos"
            # - "float time"
            # - "s_SC_P_Create *info"
            # - "dword weapon[4]"

            # Strategy: The parameter name is the LAST identifier
            # Everything before it is the type
            # Match: <type_part> <name><optional_array>
            #
            # Use a more precise pattern:
            # 1. Type part: everything up to the last space before identifier
            # 2. Name: last identifier (may have array suffix)

            # Match pattern: capture type (greedy up to last whitespace) and name
            # This handles: "type *name", "type name", "s_Struct *name"
            # Note: SDK uses "type *name" format, so we need to handle optional * before parameter name
            param_match = re.match(r'^(.+)\s+(\*?)(\w+)(\[\d+\])?$', param)
            if param_match:
                param_type = param_match.group(1).strip()
                pointer_marker = param_match.group(2)  # "*" or ""
                param_name = param_match.group(3).strip()
                array_suffix = param_match.group(4) or ''

                # Add pointer marker to type if present
                if pointer_marker:
                    param_type += '*'

                # Normalize pointer spacing
                param_type = param_type.replace(' *', '*').replace('* ', '*')

                # Add array suffix to type if present
                if array_suffix:
                    param_type += array_suffix

                parameters.append((param_type, param_name))

        return parameters

    def parse_structures(self) -> List[ParsedStruct]:
        """
        Extract typedef struct definitions.

        Pattern:
        typedef struct {
            type field1;
            type field2;
            ...
        } StructName;
        """
        structures = []

        # Pattern to match struct definitions
        # Matches: typedef struct { ... } name;
        pattern = r'typedef\s+struct\s*\{(.*?)\}\s*(s_\w+|c_\w+)\s*;'

        for match in re.finditer(pattern, self.content, re.MULTILINE | re.DOTALL):
            fields_str = match.group(1).strip()
            struct_name = match.group(2).strip()

            # Parse fields
            fields = self._parse_struct_fields(fields_str)

            if fields:  # Only add if we parsed fields successfully
                structures.append(ParsedStruct(
                    name=struct_name,
                    fields=fields
                ))

        return structures

    def _parse_struct_fields(self, fields_str: str) -> List[ParsedStructField]:
        """Parse structure field definitions."""
        fields = []
        current_offset = 0

        # Split into lines and process each field
        for line in fields_str.split('\n'):
            line = line.strip()
            if not line or line.startswith('//') or line.startswith('/*'):
                continue

            # Remove trailing semicolon and comments
            line = line.rstrip(';')
            if '//' in line:
                line = line[:line.index('//')]
            line = line.strip()

            if not line:
                continue

            # Parse field: "type name" or "type name[size]"
            # Handle comma-separated fields (e.g., "float x,y,z;")
            field_match = re.match(r'(\S+(?:\s+\*)?)\s+(.+)$', line)
            if field_match:
                field_type = field_match.group(1).strip()
                field_names = field_match.group(2).strip()

                # Normalize pointer spacing
                field_type = field_type.replace(' *', '*').replace('* ', '*')

                # Handle comma-separated fields
                for field_name_part in field_names.split(','):
                    field_name_part = field_name_part.strip()

                    # Check for array
                    array_match = re.match(r'(\w+)\[(\d+)\]', field_name_part)
                    if array_match:
                        field_name = array_match.group(1)
                        array_size = int(array_match.group(2))
                        is_array = True
                    else:
                        field_name = field_name_part
                        array_size = 0
                        is_array = False

                    # Calculate field size
                    base_size = self._get_type_size(field_type)
                    if is_array:
                        field_size = base_size * array_size
                    else:
                        field_size = base_size

                    fields.append(ParsedStructField(
                        name=field_name,
                        type=field_type,
                        size=field_size,
                        is_array=is_array,
                        array_size=array_size
                    ))

                    current_offset += field_size

        return fields

    def _get_type_size(self, type_str: str) -> int:
        """Get size of a type in bytes."""
        # Remove pointer/array decorations for lookup
        base_type = type_str.rstrip('*').strip()

        # Check known types
        if base_type in self.TYPE_SIZES:
            return self.TYPE_SIZES[base_type]

        # Check if it's a pointer (any unknown type with *)
        if '*' in type_str:
            return 4  # Pointer size

        # Check if it's a structure (s_* or c_*)
        if base_type.startswith('s_') or base_type.startswith('c_'):
            # Unknown struct size, assume pointer or dword
            return 4

        # Default to dword size
        return 4

    def parse_constants(self) -> Dict[str, int]:
        """
        Extract #define constants.

        Pattern: #define CONST_NAME value
        """
        constants = {}

        # Pattern to match #define constants
        pattern = r'^#define\s+(SC_\w+)\s+(\d+)'

        for match in re.finditer(pattern, self.content, re.MULTILINE):
            const_name = match.group(1).strip()
            const_value = int(match.group(2))

            constants[const_name] = const_value

        return constants

    def infer_message_constants(self) -> Dict[str, int]:
        """
        Infer message type constant values from SDK descriptions.

        The SDK describes message types in order (0, 1, 2, ...) but doesn't
        always provide #define declarations. We infer values from the documentation.
        """
        constants = {}

        # Level script messages (SC_LEV_MES_*)
        lev_messages = [
            'SC_LEV_MES_TIME',              # 0
            'SC_LEV_MES_INITSCENE',         # 1
            'SC_LEV_MES_RELEASESCENE',      # 2
            'SC_LEV_MES_JUSTLOADED',        # 3
            'SC_LEV_MES_RADIOUSED',         # 4
            'SC_LEV_MES_SPEACHDONE',        # 5
            'SC_LEV_MES_VIEWANIMCALLBACK',  # 6
            'SC_LEV_MES_EVENT',             # 7
            'SC_LEV_MES_POINTINTERACT',     # 8
            'SC_LEV_MES_POINTINTERACTINFO', # 9
            'SC_LEV_MES_ARTILLERY',         # 10
            'SC_LEV_MES_MUSICDONE',         # 11
            'SC_LEV_MES_LIGHTSTICK_USED',   # 12
            'SC_LEV_MES_STORYSKIP',         # 13
            'SC_LEV_MES_GETMUSIC',          # 14
        ]

        for i, msg in enumerate(lev_messages):
            constants[msg] = i

        # Player script messages (SC_P_MES_*)
        p_messages = [
            'SC_P_MES_TIME',                # 0
            'SC_P_MES_HIT',                 # 1
            'SC_P_MES_KILLED',              # 2
            'SC_P_MES_EVENT',               # 3
            'SC_P_MES_DOANIMEND',           # 4
            'SC_P_MES_INTERACT_GETTEXT',    # 5
            'SC_P_MES_INTERACT_DO',         # 6
            'SC_P_MES_DROPOUTCAR',          # 7
            'SC_P_MES_SHOTAROUNDCALLBACK',  # 8
            'SC_P_MES_GOTOPC',              # 9
        ]

        for i, msg in enumerate(p_messages):
            constants[msg] = i

        # Object event types (SC_OBJ_INFO_EVENT_*)
        obj_events = [
            'SC_OBJ_INFO_EVENT_INIT',       # 0
            'SC_OBJ_INFO_EVENT_RELEASE',    # 1
            'SC_OBJ_INFO_EVENT_JUSTLOADED', # 2
            'SC_OBJ_INFO_EVENT_DOTICK',     # 3
            'SC_OBJ_INFO_EVENT_HIT',        # 4
            'SC_OBJ_INFO_EVENT_SET',        # 5
            'SC_OBJ_INFO_EVENT_USED',       # 6
            'SC_OBJ_INFO_EVENT_MOUNTEDSHOT', # 7
        ]

        for i, event in enumerate(obj_events):
            constants[event] = i

        # Multiplayer messages (SC_NET_MES_*)
        net_messages = [
            'SC_NET_MES_LEVELINIT',         # 0
            'SC_NET_MES_RENDERHUD',         # 1
            'SC_NET_MES_SERVER_TICK',       # 2
            'SC_NET_MES_CLIENT_TICK',       # 3
            'SC_NET_MES_SERVER_RECOVER_TIME', # 4
            'SC_NET_MES_SERVER_RECOVER_PLACE', # 5
            'SC_NET_MES_SERVER_KILL',       # 6
            'SC_NET_MES_MESSAGE',           # 7
            'SC_NET_MES_LEVELPREINIT',      # 8
            'SC_NET_MES_RESTARTMAP',        # 9
            'SC_NET_MES_RULESCHANGED',      # 10
        ]

        for i, msg in enumerate(net_messages):
            constants[msg] = i

        # Player sides
        constants['SC_P_SIDE_US'] = 0
        constants['SC_P_SIDE_VC'] = 1

        return constants

    def parse_all(self) -> Tuple[List[ParsedFunction], List[ParsedStruct], Dict[str, int]]:
        """Parse all SDK data: functions, structures, and constants."""
        functions = self.parse_functions()
        structures = self.parse_structures()

        # Combine explicit #define constants with inferred message constants
        constants = self.parse_constants()
        inferred = self.infer_message_constants()

        # Inferred constants take precedence (more accurate from documentation)
        constants.update(inferred)

        return functions, structures, constants
