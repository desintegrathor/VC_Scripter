"""
Symbol database for storing constants, types, structs, and enums from C headers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


@dataclass
class StructField:
    """Represents a field in a C struct."""
    name: str
    type: str
    offset: Optional[int] = None  # Byte offset from struct start
    size: Optional[int] = None    # Size in bytes


@dataclass
class StructDef:
    """Represents a C struct definition."""
    name: str
    fields: List[StructField] = field(default_factory=list)
    size: Optional[int] = None  # Total size in bytes

    def get_field_by_offset(self, offset: int) -> Optional[StructField]:
        """Get field at given byte offset."""
        for f in self.fields:
            if f.offset == offset:
                return f
        return None

    def get_field_by_name(self, name: str) -> Optional[StructField]:
        """Get field by name."""
        for f in self.fields:
            if f.name == name:
                return f
        return None


@dataclass
class EnumDef:
    """Represents a C enum definition."""
    name: Optional[str]  # Can be anonymous
    values: Dict[str, int] = field(default_factory=dict)  # name -> value

    def get_name_for_value(self, value: int) -> Optional[str]:
        """Get enum constant name for given value."""
        for name, val in self.values.items():
            if val == value:
                return name
        return None


class SymbolDatabase:
    """
    Database of symbols extracted from C headers.

    Stores:
    - #define constants (macros)
    - typedef definitions
    - struct definitions with field mappings
    - enum definitions
    """

    def __init__(self):
        # Constants from #define: name -> value (int, float, or string)
        self.constants: Dict[str, Union[int, float, str]] = {}

        # Type definitions: typedef name -> actual type
        self.typedefs: Dict[str, str] = {}

        # Struct definitions: struct name -> StructDef
        self.structs: Dict[str, StructDef] = {}

        # Enum definitions: enum name -> EnumDef (can have None for anonymous)
        self.enums: Dict[Optional[str], EnumDef] = {}

        # Reverse lookup for values: value -> constant names
        self._value_to_constants: Dict[Union[int, float, str], List[str]] = {}

    def add_constant(self, name: str, value: Union[int, float, str]) -> None:
        """Add a constant (#define) to the database."""
        self.constants[name] = value

        # Add to reverse lookup
        if value not in self._value_to_constants:
            self._value_to_constants[value] = []
        self._value_to_constants[value].append(name)

    def add_typedef(self, name: str, actual_type: str) -> None:
        """Add a typedef definition."""
        self.typedefs[name] = actual_type

    def add_struct(self, struct: StructDef) -> None:
        """Add a struct definition."""
        self.structs[struct.name] = struct

    def add_enum(self, enum: EnumDef) -> None:
        """Add an enum definition."""
        self.enums[enum.name] = enum

        # Also add enum values as constants
        for name, value in enum.values.items():
            self.add_constant(name, value)

    def get_constant_name(self, value: Union[int, float, str]) -> Optional[str]:
        """
        Get constant name for a given value.
        Returns the first matching constant if multiple exist.
        """
        constants = self._value_to_constants.get(value, [])
        return constants[0] if constants else None

    def get_all_constant_names(self, value: Union[int, float, str]) -> List[str]:
        """Get all constant names that have the given value."""
        return self._value_to_constants.get(value, [])

    def get_struct(self, name: str) -> Optional[StructDef]:
        """Get struct definition by name."""
        return self.structs.get(name)

    def get_enum(self, name: Optional[str]) -> Optional[EnumDef]:
        """Get enum definition by name."""
        return self.enums.get(name)

    def resolve_typedef(self, typename: str) -> str:
        """Resolve typedef to actual type (may chain through multiple typedefs)."""
        visited = set()
        while typename in self.typedefs and typename not in visited:
            visited.add(typename)
            typename = self.typedefs[typename]
        return typename

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'constants': self.constants,
            'typedefs': self.typedefs,
            'structs': {
                name: {
                    'name': s.name,
                    'size': s.size,
                    'fields': [
                        {
                            'name': f.name,
                            'type': f.type,
                            'offset': f.offset,
                            'size': f.size
                        }
                        for f in s.fields
                    ]
                }
                for name, s in self.structs.items()
            },
            'enums': {
                name: {
                    'name': e.name,
                    'values': e.values
                }
                for name, e in self.enums.items()
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SymbolDatabase:
        """Load from dictionary (deserialization)."""
        db = cls()

        # Load constants
        for name, value in data.get('constants', {}).items():
            db.add_constant(name, value)

        # Load typedefs
        for name, actual_type in data.get('typedefs', {}).items():
            db.add_typedef(name, actual_type)

        # Load structs
        for name, struct_data in data.get('structs', {}).items():
            fields = [
                StructField(
                    name=f['name'],
                    type=f['type'],
                    offset=f.get('offset'),
                    size=f.get('size')
                )
                for f in struct_data.get('fields', [])
            ]
            struct = StructDef(
                name=struct_data['name'],
                fields=fields,
                size=struct_data.get('size')
            )
            db.add_struct(struct)

        # Load enums
        for name, enum_data in data.get('enums', {}).items():
            enum = EnumDef(
                name=enum_data['name'],
                values=enum_data.get('values', {})
            )
            db.add_enum(enum)

        return db

    def save(self, path: Union[str, Path]) -> None:
        """Save symbol database to JSON file."""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Union[str, Path]) -> SymbolDatabase:
        """Load symbol database from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def __repr__(self) -> str:
        return (
            f"SymbolDatabase("
            f"{len(self.constants)} constants, "
            f"{len(self.typedefs)} typedefs, "
            f"{len(self.structs)} structs, "
            f"{len(self.enums)} enums)"
        )
