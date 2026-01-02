"""
Header database for fast lookup of function signatures and constants.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class HeaderDatabase:
    """Database for header information with fast lookup."""

    def __init__(self):
        self.functions: Dict = {}
        self.constants: Dict = {}
        self.structures: Dict = {}
        self._constant_value_map: Dict[int, List[str]] = {}  # value → [names]

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

    def get_function_signature(self, name: str) -> Optional[Dict]:
        """Get function signature by name."""
        return self.functions.get(name)

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
