"""
Parser for sc_global.h to extract struct definitions and function struct parameters.

This parser automatically generates:
1. STRUCT_DEFINITIONS - Structure definitions with fields and byte offsets
2. FUNCTION_STRUCT_PARAMS - Mapping of functions to struct parameter types

This replaces manual maintenance of these mappings in structures.py.
"""

from __future__ import annotations

import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


# ============================================================================
# Type size definitions (32-bit architecture)
# ============================================================================

# Basic type sizes in bytes
TYPE_SIZES: Dict[str, int] = {
    # Standard C types
    'char': 1,
    'short': 2,
    'ushort': 2,
    'int': 4,
    'long': 4,
    'float': 4,
    'double': 8,
    # Vietcong-specific types
    'dword': 4,
    'BOOL': 4,
    'void': 4,  # void* pointers
}

# Known struct sizes for recursive resolution
KNOWN_STRUCT_SIZES: Dict[str, int] = {
    'c_Vector3': 12,  # 3 floats
    's_sphere': 16,   # c_Vector3 + float
}


@dataclass
class ParsedField:
    """Represents a parsed struct field."""
    name: str
    type_name: str
    offset: int
    size: int
    is_pointer: bool = False
    is_array: bool = False
    array_size: int = 1


@dataclass
class ParsedStruct:
    """Represents a parsed struct definition."""
    name: str
    fields: List[ParsedField]
    total_size: int


@dataclass
class ParsedFunction:
    """Represents a parsed function declaration."""
    name: str
    return_type: str
    parameters: List[Tuple[str, str]]  # [(type, name), ...]
    struct_params: Dict[int, str]  # {param_index: struct_type}


class SCGlobalParser:
    """Parser for sc_global.h header file."""

    # Regex patterns
    STRUCT_PATTERN = re.compile(
        r'typedef\s+struct\s*\{([^}]+)\}\s*(\w+)\s*;',
        re.MULTILINE | re.DOTALL
    )

    FIELD_PATTERN = re.compile(
        r'^\s*'
        r'([\w\s]+?)\s*'  # Type (may have spaces like "unsigned int")
        r'(\*?)\s*'       # Optional pointer
        r'(\w+)'          # Field name
        r'(?:\s*\[([^\]]+)\])?'  # Optional array size
        r'\s*;',
        re.MULTILINE
    )

    EXTERN_FUNC_PATTERN = re.compile(
        r'extern\s+'
        r'([\w\s*]+?)\s+'  # Return type
        r'(SC_\w+)\s*'     # Function name (SC_ prefix)
        r'\(([^)]*)\)\s*;',  # Parameters
        re.MULTILINE
    )

    PARAM_PATTERN = re.compile(
        r'^\s*'
        r'([\w\s]+)'   # Type
        r'(\*?)\s*'    # Optional pointer
        r'(\w+)?'      # Optional parameter name
        r'\s*$'
    )

    def __init__(self):
        self.structs: Dict[str, ParsedStruct] = {}
        self.functions: Dict[str, ParsedFunction] = {}
        self.defines: Dict[str, int] = {}

    def parse_file(self, header_path: str) -> Tuple[Dict[str, List[Tuple[int, str, str]]], Dict[str, Dict[int, str]]]:
        """
        Parse sc_global.h and extract struct definitions and function struct params.

        Args:
            header_path: Path to sc_global.h

        Returns:
            Tuple of:
                - struct_definitions: {struct_name: [(offset, field_name, field_type), ...]}
                - function_struct_params: {func_name: {param_index: struct_type}}
        """
        path = Path(header_path)
        if not path.exists():
            logger.error(f"Header file not found: {header_path}")
            return {}, {}

        with open(path, 'r', encoding='latin-1') as f:
            content = f.read()

        # Remove comments
        content = self._remove_comments(content)

        # Parse #define constants (for array sizes)
        self._parse_defines(content)

        # Parse struct definitions
        self._parse_structs(content)

        # Parse function declarations
        self._parse_functions(content)

        # Convert to output format
        struct_defs = self._convert_structs()
        func_params = self._convert_functions()

        return struct_defs, func_params

    def _remove_comments(self, content: str) -> str:
        """Remove C-style comments from content."""
        # Remove multi-line comments /* ... */
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # Remove single-line comments // ...
        content = re.sub(r'//[^\n]*', '', content)
        return content

    def _parse_defines(self, content: str) -> None:
        """Parse #define constants for use in array sizes."""
        pattern = re.compile(r'#define\s+(\w+)\s+(\d+)')
        for match in pattern.finditer(content):
            name = match.group(1)
            try:
                value = int(match.group(2))
                self.defines[name] = value
            except ValueError:
                pass

    def _parse_structs(self, content: str) -> None:
        """Parse all typedef struct definitions."""
        for match in self.STRUCT_PATTERN.finditer(content):
            struct_body = match.group(1)
            struct_name = match.group(2)

            fields = self._parse_struct_body(struct_body, struct_name)
            if fields:
                total_size = 0
                if fields:
                    last_field = fields[-1]
                    total_size = last_field.offset + last_field.size * (
                        last_field.array_size if last_field.is_array else 1
                    )
                    # Apply 4-byte alignment to total size
                    if total_size % 4 != 0:
                        total_size += (4 - total_size % 4)

                self.structs[struct_name] = ParsedStruct(
                    name=struct_name,
                    fields=fields,
                    total_size=total_size
                )

                # Update known struct sizes for recursive resolution
                KNOWN_STRUCT_SIZES[struct_name] = total_size

    def _parse_struct_body(self, body: str, struct_name: str) -> List[ParsedField]:
        """Parse fields from a struct body."""
        fields = []
        current_offset = 0

        for line in body.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Skip preprocessor directives inside structs
            if line.startswith('#'):
                continue

            # Try to match a field declaration
            match = self.FIELD_PATTERN.match(line)
            if match:
                type_str = match.group(1).strip()
                is_pointer = bool(match.group(2))
                field_name = match.group(3)
                array_size_str = match.group(4)

                # Determine field size
                if is_pointer:
                    field_size = 4  # Pointer size
                else:
                    field_size = self._get_type_size(type_str)

                # Handle arrays
                is_array = array_size_str is not None
                array_size = 1
                if is_array:
                    array_size = self._resolve_array_size(array_size_str)

                # Store field
                fields.append(ParsedField(
                    name=field_name,
                    type_name=type_str + ('*' if is_pointer else ''),
                    offset=current_offset,
                    size=field_size,
                    is_pointer=is_pointer,
                    is_array=is_array,
                    array_size=array_size
                ))

                # Advance offset
                total_field_size = field_size * array_size
                current_offset += total_field_size

                # Apply 4-byte alignment
                if current_offset % 4 != 0:
                    current_offset += (4 - current_offset % 4)
            else:
                # Try handling multiple fields on one line: "float x,y,z;"
                multi_match = re.match(r'^\s*([\w\s*]+)\s+(\w+(?:\s*,\s*\w+)+)\s*;', line)
                if multi_match:
                    type_str = multi_match.group(1).strip()
                    names_str = multi_match.group(2)

                    is_pointer = '*' in type_str
                    base_type = type_str.replace('*', '').strip()
                    field_size = 4 if is_pointer else self._get_type_size(base_type)

                    for name in names_str.split(','):
                        name = name.strip()
                        fields.append(ParsedField(
                            name=name,
                            type_name=type_str,
                            offset=current_offset,
                            size=field_size,
                            is_pointer=is_pointer
                        ))
                        current_offset += field_size

        return fields

    def _get_type_size(self, type_str: str) -> int:
        """Get size in bytes for a type."""
        # Remove any whitespace
        type_str = type_str.strip()

        # Check basic types
        if type_str in TYPE_SIZES:
            return TYPE_SIZES[type_str]

        # Check known struct sizes
        if type_str in KNOWN_STRUCT_SIZES:
            return KNOWN_STRUCT_SIZES[type_str]

        # Check if it's already parsed
        if type_str in self.structs:
            return self.structs[type_str].total_size

        # Default to 4 bytes (dword size)
        logger.debug(f"Unknown type '{type_str}', assuming 4 bytes")
        return 4

    def _resolve_array_size(self, size_str: str) -> int:
        """Resolve array size from string (may be a #define constant)."""
        size_str = size_str.strip()

        # Try as integer literal
        try:
            return int(size_str)
        except ValueError:
            pass

        # Try as defined constant
        if size_str in self.defines:
            return self.defines[size_str]

        # Default
        logger.warning(f"Could not resolve array size '{size_str}', defaulting to 1")
        return 1

    def _parse_functions(self, content: str) -> None:
        """Parse extern function declarations."""
        for match in self.EXTERN_FUNC_PATTERN.finditer(content):
            return_type = match.group(1).strip()
            func_name = match.group(2).strip()
            params_str = match.group(3).strip()

            # Parse parameters
            parameters = []
            struct_params: Dict[int, str] = {}

            if params_str and params_str != 'void':
                param_list = params_str.split(',')
                for idx, param in enumerate(param_list):
                    param = param.strip()
                    if param == '...':
                        continue

                    param_match = self.PARAM_PATTERN.match(param)
                    if param_match:
                        param_type = param_match.group(1).strip()
                        is_pointer = bool(param_match.group(2))
                        param_name = param_match.group(3) or ''

                        full_type = param_type + ('*' if is_pointer else '')
                        parameters.append((full_type, param_name))

                        # Check if this is a struct pointer parameter
                        if is_pointer:
                            struct_type = self._extract_struct_type(param_type)
                            if struct_type:
                                struct_params[idx] = struct_type
                    else:
                        # Fallback parsing
                        parameters.append((param, ''))

            self.functions[func_name] = ParsedFunction(
                name=func_name,
                return_type=return_type,
                parameters=parameters,
                struct_params=struct_params
            )

    def _extract_struct_type(self, type_str: str) -> Optional[str]:
        """Extract struct type name if the type is a known struct."""
        type_str = type_str.strip()

        # Check for s_SC_* or c_* prefixes (Vietcong struct naming convention)
        if type_str.startswith('s_SC_') or type_str.startswith('c_'):
            return type_str
        if type_str.startswith('s_') and '_' in type_str:
            return type_str

        # Check if it's in our parsed structs
        if type_str in self.structs:
            return type_str

        return None

    def _convert_structs(self) -> Dict[str, List[Tuple[int, str, str]]]:
        """Convert parsed structs to output format."""
        result = {}
        for struct_name, struct in self.structs.items():
            fields = []
            for field in struct.fields:
                fields.append((field.offset, field.name, field.type_name))
            result[struct_name] = fields
        return result

    def _convert_functions(self) -> Dict[str, Dict[int, str]]:
        """Convert parsed functions to function_struct_params format."""
        result = {}
        for func_name, func in self.functions.items():
            if func.struct_params:
                result[func_name] = func.struct_params
        return result


# ============================================================================
# Module-level caching
# ============================================================================

_cached_result: Optional[Tuple[Dict, Dict]] = None


def parse_sc_global_header(
    header_path: Optional[str] = None
) -> Tuple[Dict[str, List[Tuple[int, str, str]]], Dict[str, Dict[int, str]]]:
    """
    Parse sc_global.h and return struct definitions and function struct params.

    Args:
        header_path: Path to sc_global.h. If None, uses default location.

    Returns:
        Tuple of:
            - struct_definitions: {struct_name: [(offset, field_name, field_type), ...]}
            - function_struct_params: {func_name: {param_index: struct_type}}
    """
    global _cached_result

    if header_path is None:
        # Default path relative to this file
        header_path = str(Path(__file__).parent.parent.parent / 'compiler' / 'inc' / 'sc_global.h')

    # Return cached result if available
    if _cached_result is not None:
        return _cached_result

    parser = SCGlobalParser()
    _cached_result = parser.parse_file(header_path)

    logger.info(
        f"Parsed sc_global.h: {len(_cached_result[0])} structs, "
        f"{len(_cached_result[1])} functions with struct params"
    )

    return _cached_result


def get_struct_definitions() -> Dict[str, List[Tuple[int, str, str]]]:
    """Get parsed struct definitions."""
    return parse_sc_global_header()[0]


def get_function_struct_params() -> Dict[str, Dict[int, str]]:
    """Get parsed function struct parameter mappings."""
    return parse_sc_global_header()[1]


# ============================================================================
# CLI for testing
# ============================================================================

if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = str(Path(__file__).parent.parent.parent / 'compiler' / 'inc' / 'sc_global.h')

    print(f"Parsing: {path}")
    structs, funcs = parse_sc_global_header(path)

    print(f"\n=== Struct Definitions ({len(structs)}) ===")
    for name, fields in sorted(structs.items()):
        print(f"\n{name}:")
        for offset, field_name, field_type in fields:
            print(f"  {offset:4d}: {field_name} ({field_type})")

    print(f"\n=== Function Struct Params ({len(funcs)}) ===")
    for name, params in sorted(funcs.items()):
        param_strs = [f"{idx}: {typ}" for idx, typ in params.items()]
        print(f"  {name}: {{{', '.join(param_strs)}}}")
