"""
Header database for fast lookup of function signatures and constants.

Now enhanced with SDK integration for improved type inference and constant resolution.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class FieldInfo:
    """Information about a struct field."""
    name: str          # Field name (e.g., "position", "x")
    type: str          # Field type (e.g., "float", "s_SC_vector*")
    offset: int        # Byte offset within struct
    size: int          # Field size in bytes


class HeaderDatabase:
    """
    Database for header information with fast lookup.

    Enhanced with SDK integration to prioritize SDK data over header files.
    Lookup priority:
    1. SDK database (most accurate, from official documentation)
    2. Header files (parsed from C headers)
    """

    def __init__(self, use_sdk: bool = True):
        """
        Initialize header database.

        Args:
            use_sdk: If True, load and use SDK database (default: True)
        """
        self.functions: Dict = {}
        self.constants: Dict = {}
        self.structures: Dict = {}
        self._constant_value_map: Dict[int, List[str]] = {}  # value → [names]
        self.struct_fields: Dict[str, Dict[int, FieldInfo]] = {}  # struct_type → {offset: FieldInfo}

        # SDK integration
        self.use_sdk = use_sdk
        self.sdk_db = None

        if use_sdk:
            try:
                from ...sdk import SDKDatabase
                self.sdk_db = SDKDatabase()
                # Merge SDK constants into constant value map
                self._merge_sdk_constants()
            except Exception:
                # SDK not available, fall back to header-only mode
                self.sdk_db = None

    def load_from_json(self, json_dir: Path):
        """Load parsed header data from JSON files."""
        # Load SC_GLOBAL.H data
        sc_global_path = json_dir / 'sc_global.json'
        if sc_global_path.exists():
            with open(sc_global_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.functions.update(data.get('functions', {}))
                self.structures.update(data.get('structures', {}))
                self.constants.update(data.get('constants', {}))

        # Load SC_DEF.H data
        sc_def_path = json_dir / 'sc_def.json'
        if sc_def_path.exists():
            with open(sc_def_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.constants.update(data.get('constants', {}))

        # Build reverse lookup for constants
        self._build_constant_value_map()

        # Parse struct field definitions from header files
        self._parse_struct_fields()

    def _build_constant_value_map(self):
        """Build reverse lookup: integer value → constant names."""
        for name, const_data in self.constants.items():
            value_str = const_data['value']
            # Try to parse as integer
            try:
                if value_str.startswith('0x'):
                    value = int(value_str, 16)
                else:
                    value = int(value_str)

                if value not in self._constant_value_map:
                    self._constant_value_map[value] = []
                self._constant_value_map[value].append(name)
            except ValueError:
                # Not an integer constant
                pass

    def _merge_sdk_constants(self):
        """Merge SDK constants into reverse lookup map."""
        if not self.sdk_db:
            return

        for const_name, const_value in self.sdk_db.constants.items():
            if const_value not in self._constant_value_map:
                self._constant_value_map[const_value] = []
            # Add to front of list (SDK constants are prioritized)
            if const_name not in self._constant_value_map[const_value]:
                self._constant_value_map[const_value].insert(0, const_name)

    def get_function_signature(self, name: str) -> Optional[Dict]:
        """
        Get function signature by name.

        Lookup priority:
        1. SDK database (if available and enabled)
        2. Header files

        Returns:
            Dict with 'return_type', 'parameters' (list of [type, name] tuples),
            and optionally 'is_variadic' flag
        """
        # PRIORITY 1: SDK database (most accurate)
        if self.sdk_db:
            sdk_sig = self.sdk_db.get_function_signature(name)
            if sdk_sig:
                # Convert SDK signature to header database format
                return {
                    'return_type': sdk_sig.return_type,
                    'parameters': sdk_sig.parameters,
                    'is_variadic': False,  # SDK signatures don't track varargs yet
                    'source': 'SDK'  # Mark source for debugging
                }

        # PRIORITY 2: Header files
        header_sig = self.functions.get(name)
        if header_sig:
            return header_sig

        return None

    def get_constant(self, name: str) -> Optional[Dict]:
        """Get constant by name."""
        return self.constants.get(name)

    def get_constant_names_by_value(self, value: int, prefix: str = None) -> List[str]:
        """
        Get constant name(s) that have this value.

        Args:
            value: Integer value to look up
            prefix: Optional prefix filter (e.g., 'SCM', 'SGI')

        Returns:
            List of matching constant names
        """
        names = self._constant_value_map.get(value, [])

        if prefix:
            names = [n for n in names if n.startswith(f'{prefix}_')]

        return names

    def get_structure(self, name: str) -> Optional[Dict]:
        """Get structure definition by name."""
        return self.structures.get(name)

    def get_constants_by_prefix(self, prefix: str) -> Dict[str, Dict]:
        """Get all constants with given prefix (e.g., 'SCM', 'SGI')."""
        return {
            name: data
            for name, data in self.constants.items()
            if data.get('prefix') == prefix
        }

    def _parse_struct_fields(self):
        """Parse struct field definitions from header files."""
        import logging
        logger = logging.getLogger(__name__)

        # Locate header files relative to this module
        headers_dir = Path(__file__).parent.parent.parent / 'compiler' / 'inc'

        if not headers_dir.exists():
            logger.warning(f"Header directory not found: {headers_dir}")
            return

        # Parse primary struct definition files
        header_files = [
            headers_dir / 'sc_global.h',
            headers_dir / 'sc_def.h'
        ]

        struct_count = 0
        field_count = 0

        for header_path in header_files:
            if not header_path.exists():
                logger.debug(f"Header file not found: {header_path}")
                continue

            try:
                with open(header_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Parse struct definitions
                structs = self._extract_struct_definitions(content)
                struct_count += len(structs)

                for struct_name, fields in structs.items():
                    self.struct_fields[struct_name] = fields
                    field_count += len(fields)

            except Exception as e:
                logger.warning(f"Error parsing {header_path}: {e}")

        logger.info(f"Loaded {struct_count} struct definitions with {field_count} total fields")

    def _extract_struct_definitions(self, content: str) -> Dict[str, Dict[int, FieldInfo]]:
        """Extract struct definitions from C header content."""
        structs = {}

        # Pattern to match typedef struct { ... } struct_name;
        # This handles multi-line struct definitions
        pattern = re.compile(
            r'typedef\s+struct\s*\{([^}]+)\}\s*(\w+)\s*;',
            re.MULTILINE | re.DOTALL
        )

        for match in pattern.finditer(content):
            struct_body = match.group(1)
            struct_name = match.group(2)

            # Parse fields within the struct
            fields = self._parse_struct_fields_from_body(struct_body, struct_name)
            if fields:
                structs[struct_name] = fields

        return structs

    def _parse_struct_fields_from_body(self, body: str, struct_name: str) -> Dict[int, FieldInfo]:
        """Parse field definitions from struct body."""
        fields = {}
        current_offset = 0

        # Split into lines and parse field declarations
        for line in body.split('\n'):
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('//') or line.startswith('/*'):
                continue

            # Remove inline comments
            if '//' in line:
                line = line[:line.index('//')]

            # Parse field declaration: type name; or type name[size];
            # Examples: "float x;", "dword message;", "char *name;", "int array[10];"
            field_match = re.match(r'(\w+(?:\s*\*)?)\s+(\w+)(?:\[(\d+)\])?\s*;', line)
            if field_match:
                field_type = field_match.group(1).strip()
                field_name = field_match.group(2)
                array_size_str = field_match.group(3)

                # Calculate field size
                field_size = self._get_type_size(field_type)

                # Handle arrays
                if array_size_str:
                    array_size = int(array_size_str)
                    field_size *= array_size

                # Create field info
                field_info = FieldInfo(
                    name=field_name,
                    type=field_type,
                    offset=current_offset,
                    size=field_size
                )

                fields[current_offset] = field_info
                current_offset += field_size

                # Apply 4-byte alignment after each field
                if current_offset % 4 != 0:
                    current_offset += (4 - current_offset % 4)

        return fields

    def _get_type_size(self, type_str: str) -> int:
        """Get size in bytes for a C type."""
        # Remove pointer indicator
        is_pointer = '*' in type_str
        if is_pointer:
            return 4  # Pointers are 4 bytes in 32-bit architecture

        base_type = type_str.strip()

        # Basic type sizes (32-bit architecture)
        type_sizes = {
            'char': 1,
            'short': 2,
            'int': 4,
            'long': 4,
            'float': 4,
            'double': 8,
            'dword': 4,
            'void': 0,
            'BOOL': 4,
        }

        # Check if it's a known struct type (recursive case)
        if base_type.startswith('c_') or base_type.startswith('s_SC_'):
            # If we already have this struct, calculate its size
            if base_type in self.struct_fields:
                max_offset = 0
                max_size = 0
                for offset, field in self.struct_fields[base_type].items():
                    if offset >= max_offset:
                        max_offset = offset
                        max_size = field.size
                return max_offset + max_size
            # Unknown struct, assume pointer size or 4-byte alignment
            return 4

        return type_sizes.get(base_type, 4)  # Default to 4 bytes

    def get_struct_fields(self, struct_type: str) -> Dict[int, FieldInfo]:
        """
        Return field definitions for a struct type.

        Args:
            struct_type: Name of struct type (e.g., "s_SC_vector", "c_Vector3")

        Returns:
            Dictionary mapping byte offset to FieldInfo
            Example: {0: FieldInfo("x", "float", 0, 4),
                      4: FieldInfo("y", "float", 4, 4),
                      8: FieldInfo("z", "float", 8, 4)}
        """
        return self.struct_fields.get(struct_type, {})

    def lookup_field_name(self, struct_type: str, offset: int) -> str:
        """
        Get field name for a struct at given byte offset.

        Args:
            struct_type: Name of struct type
            offset: Byte offset within struct

        Returns:
            Field name or "field_{offset}" if not found
        """
        fields = self.struct_fields.get(struct_type, {})
        field = fields.get(offset)

        if field:
            return field.name
        else:
            return f"field_{offset}"


# Global instance
_db_instance: Optional[HeaderDatabase] = None


def get_header_database() -> HeaderDatabase:
    """Get singleton header database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = HeaderDatabase()
        # Try to load data
        json_dir = Path(__file__).parent / 'data'
        if json_dir.exists():
            _db_instance.load_from_json(json_dir)
    return _db_instance
