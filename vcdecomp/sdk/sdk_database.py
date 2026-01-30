"""
Runtime database of SDK information for decompiler use.

Provides fast access to:
- Function signatures (734 functions)
- Structure definitions (46 structs)
- Constant definitions (98+ constants)
"""

import json
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
from pathlib import Path


def _is_out_param(type_str: str, name: str) -> bool:
    """Detect out parameters from pointer types or explicit out names."""
    type_normalized = type_str.replace(" ", "")
    if "*" in type_normalized:
        return True

    name = name.strip()
    if not name:
        return False
    name_lower = name.lower()
    if name_lower == "out" or name_lower.startswith("out_"):
        return True
    if name_lower.startswith("out") and len(name) > 3 and name[3].isalpha():
        return True
    if name_lower.startswith("pout"):
        return True
    return False


def _derive_out_params(parameters: List[Tuple[str, str]]) -> List[int]:
    """Return parameter indices that look like out params."""
    return [idx for idx, (param_type, param_name) in enumerate(parameters)
            if _is_out_param(param_type or "", param_name or "")]


@dataclass
class FunctionSignature:
    """Function signature from SDK."""
    name: str
    return_type: str
    parameters: List[Tuple[str, str]]  # [(type, name), ...]
    out_params: List[int] = field(default_factory=list)

    is_variadic: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        d = {
            'name': self.name,
            'return_type': self.return_type,
            'parameters': [{'type': t, 'name': n} for t, n in self.parameters],
            'out_params': list(self.out_params),
        }
        if self.is_variadic:
            d['is_variadic'] = True
        return d

    @classmethod
    def from_dict(cls, data: dict) -> 'FunctionSignature':
        """Create from dictionary (JSON deserialization)."""
        parameters = [(p['type'], p['name']) for p in data['parameters']]
        out_params = data.get('out_params')
        if out_params is None:
            out_params = _derive_out_params(parameters)
        return cls(
            name=data['name'],
            return_type=data['return_type'],
            parameters=parameters,
            out_params=out_params,
            is_variadic=data.get('is_variadic', False)
        )


@dataclass
class StructField:
    """Structure field definition."""
    name: str
    type: str
    offset: int
    size: int
    is_array: bool = False
    array_size: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'StructField':
        """Create from dictionary (JSON deserialization)."""
        return cls(**data)


@dataclass
class StructDefinition:
    """Structure definition from SDK."""
    name: str
    fields: List[StructField]
    size: int

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'size': self.size,
            'fields': [f.to_dict() for f in self.fields]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'StructDefinition':
        """Create from dictionary (JSON deserialization)."""
        return cls(
            name=data['name'],
            size=data['size'],
            fields=[StructField.from_dict(f) for f in data['fields']]
        )


class SDKDatabase:
    """Runtime database of SDK information."""

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize SDK database.

        Args:
            data_dir: Path to directory containing JSON database files.
                     If None, uses default location (vcdecomp/sdk/data/)
        """
        if data_dir is None:
            # Default to vcdecomp/sdk/data/
            self.data_dir = Path(__file__).parent / 'data'
        else:
            self.data_dir = Path(data_dir)

        # Initialize empty databases
        self.functions: Dict[str, FunctionSignature] = {}
        self.structures: Dict[str, StructDefinition] = {}
        self.constants: Dict[str, int] = {}

        # Load databases if they exist
        self._load_databases()

    def _load_databases(self) -> None:
        """Load JSON databases from disk."""
        # Load functions
        functions_file = self.data_dir / 'functions.json'
        if functions_file.exists():
            with open(functions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.functions = {
                    name: FunctionSignature.from_dict(func_data)
                    for name, func_data in data.items()
                }

        # Load structures
        structures_file = self.data_dir / 'structures.json'
        if structures_file.exists():
            with open(structures_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.structures = {
                    name: StructDefinition.from_dict(struct_data)
                    for name, struct_data in data.items()
                }

        # Load constants
        constants_file = self.data_dir / 'constants.json'
        if constants_file.exists():
            with open(constants_file, 'r', encoding='utf-8') as f:
                self.constants = json.load(f)

    def save_databases(self) -> None:
        """Save databases to JSON files."""
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Save functions
        functions_file = self.data_dir / 'functions.json'
        with open(functions_file, 'w', encoding='utf-8') as f:
            data = {name: func.to_dict() for name, func in self.functions.items()}
            json.dump(data, f, indent=2)

        # Save structures
        structures_file = self.data_dir / 'structures.json'
        with open(structures_file, 'w', encoding='utf-8') as f:
            data = {name: struct.to_dict() for name, struct in self.structures.items()}
            json.dump(data, f, indent=2)

        # Save constants
        constants_file = self.data_dir / 'constants.json'
        with open(constants_file, 'w', encoding='utf-8') as f:
            json.dump(self.constants, f, indent=2)

    def get_function_signature(self, name: str) -> Optional[FunctionSignature]:
        """
        Get function signature by name.

        Args:
            name: Function name (e.g., "SC_P_GetPos")

        Returns:
            FunctionSignature or None if not found
        """
        return self.functions.get(name)

    def get_structure(self, name: str) -> Optional[StructDefinition]:
        """
        Get structure definition by name.

        Args:
            name: Structure name (e.g., "s_SC_P_info")

        Returns:
            StructDefinition or None if not found
        """
        return self.structures.get(name)

    def get_constant_value(self, name: str) -> Optional[int]:
        """
        Get constant value by name.

        Args:
            name: Constant name (e.g., "SC_LEV_MES_TIME")

        Returns:
            Integer value or None if not found
        """
        return self.constants.get(name)

    def get_constant_name(self, value: int, prefix: str = "") -> Optional[str]:
        """
        Reverse lookup: value → constant name.

        Args:
            value: Numeric value (e.g., 0, 1, 2)
            prefix: Optional prefix filter (e.g., "SC_LEV_MES_")

        Returns:
            Constant name or None if not found
        """
        candidates = []

        for name, const_value in self.constants.items():
            if const_value == value:
                if not prefix or name.startswith(prefix):
                    candidates.append(name)

        # Return first match (or None if no matches)
        return candidates[0] if candidates else None

    def get_constant_names(self, value: int, prefix: str = "") -> List[str]:
        """
        Reverse lookup: value → all matching constant names.

        Args:
            value: Numeric value
            prefix: Optional prefix filter

        Returns:
            List of constant names (may be empty)
        """
        candidates = []

        for name, const_value in self.constants.items():
            if const_value == value:
                if not prefix or name.startswith(prefix):
                    candidates.append(name)

        return candidates

    def get_struct_field_at_offset(self, struct_name: str, offset: int) -> Optional[StructField]:
        """
        Get struct field by byte offset.

        Args:
            struct_name: Structure name (e.g., "s_SC_P_info")
            offset: Byte offset into structure

        Returns:
            StructField or None if not found
        """
        struct = self.structures.get(struct_name)
        if not struct:
            return None

        for field in struct.fields:
            if field.offset == offset:
                return field

        return None

    def get_parameter_type(self, func_name: str, param_index: int) -> Optional[str]:
        """
        Get parameter type for a function by index.

        Args:
            func_name: Function name
            param_index: Parameter index (0-based)

        Returns:
            Parameter type string or None
        """
        sig = self.get_function_signature(func_name)
        if not sig or param_index >= len(sig.parameters):
            return None

        return sig.parameters[param_index][0]

    def get_parameter_name(self, func_name: str, param_index: int) -> Optional[str]:
        """
        Get parameter name for a function by index.

        Args:
            func_name: Function name
            param_index: Parameter index (0-based)

        Returns:
            Parameter name string or None
        """
        sig = self.get_function_signature(func_name)
        if not sig or param_index >= len(sig.parameters):
            return None

        return sig.parameters[param_index][1]

    def populate_from_parser(self, functions: list, structures: list, constants: dict) -> None:
        """
        Populate database from parser output.

        Args:
            functions: List of ParsedFunction objects
            structures: List of ParsedStruct objects
            constants: Dictionary of constant name → value
        """
        # Convert parsed functions to FunctionSignature objects
        for func in functions:
            self.functions[func.name] = FunctionSignature(
                name=func.name,
                return_type=func.return_type,
                parameters=func.parameters,
                is_variadic=getattr(func, 'is_variadic', False)
            )

        # Convert parsed structures to StructDefinition objects
        for struct in structures:
            # Calculate field offsets
            offset = 0
            fields = []

            for parsed_field in struct.fields:
                field = StructField(
                    name=parsed_field.name,
                    type=parsed_field.type,
                    offset=offset,
                    size=parsed_field.size,
                    is_array=parsed_field.is_array,
                    array_size=parsed_field.array_size
                )
                fields.append(field)
                offset += parsed_field.size

            self.structures[struct.name] = StructDefinition(
                name=struct.name,
                fields=fields,
                size=offset  # Total size
            )

        # Store constants directly
        self.constants = constants.copy()

    def get_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        return {
            'functions': len(self.functions),
            'structures': len(self.structures),
            'constants': len(self.constants)
        }
