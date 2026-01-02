"""
C header file parser for extracting symbols, types, and constants.

Uses pycparser if available, falls back to regex-based parsing for #define.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Union, Dict, Any
import logging

from .symbol_db import SymbolDatabase, StructDef, StructField, EnumDef

logger = logging.getLogger(__name__)

# Try to import pycparser
try:
    from pycparser import c_parser, c_ast, parse_file
    from pycparser.c_generator import CGenerator
    HAS_PYCPARSER = True
except ImportError:
    HAS_PYCPARSER = False
    logger.warning("pycparser not available, using regex fallback for parsing")


class HeaderParser:
    """
    Parser for C header files.

    Extracts:
    - #define constants (always uses regex, as pycparser skips preprocessor)
    - typedef definitions (pycparser or regex)
    - struct definitions with field offsets (pycparser or limited regex)
    - enum definitions (pycparser or regex)
    """

    def __init__(self):
        self.symbol_db = SymbolDatabase()

    def parse_file(self, file_path: Union[str, Path]) -> SymbolDatabase:
        """
        Parse a C header file and return symbol database.

        Args:
            file_path: Path to .h or .inc file

        Returns:
            SymbolDatabase with extracted symbols
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"Header file not found: {file_path}")
            return self.symbol_db

        logger.info(f"Parsing header: {file_path}")

        # Read file content
        content = file_path.read_text(encoding='utf-8', errors='ignore')

        # Always parse #define with regex (pycparser skips preprocessor directives)
        self._parse_defines_regex(content)

        # Try pycparser for structs/enums/typedefs, fallback to regex
        if HAS_PYCPARSER:
            try:
                self._parse_with_pycparser(file_path, content)
            except Exception as e:
                logger.warning(f"pycparser failed: {e}, using regex fallback")
                self._parse_with_regex(content)
        else:
            self._parse_with_regex(content)

        return self.symbol_db

    def _parse_defines_regex(self, content: str) -> None:
        """
        Parse #define directives using regex.

        Handles:
        - #define NAME VALUE
        - #define NAME "string"
        - #define NAME 0x123
        - #define NAME 1.5f
        """
        # Pattern: #define NAME VALUE
        define_pattern = r'^\s*#define\s+([A-Z_][A-Z0-9_]*)\s+(.+?)(?://.*)?$'

        for line in content.split('\n'):
            match = re.match(define_pattern, line, re.IGNORECASE)
            if not match:
                continue

            name = match.group(1)
            value_str = match.group(2).strip()

            # Try to parse value
            value = self._parse_constant_value(value_str)
            if value is not None:
                self.symbol_db.add_constant(name, value)
                logger.debug(f"Define: {name} = {value}")

    def _parse_constant_value(self, value_str: str) -> Optional[Union[int, float, str]]:
        """Parse constant value from #define."""
        value_str = value_str.strip()

        # String literal
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]  # Remove quotes

        # Hex integer
        if value_str.startswith('0x') or value_str.startswith('0X'):
            try:
                return int(value_str, 16)
            except ValueError:
                pass

        # Float literal
        if 'f' in value_str.lower() or '.' in value_str:
            try:
                return float(value_str.rstrip('fF'))
            except ValueError:
                pass

        # Integer literal
        try:
            return int(value_str)
        except ValueError:
            pass

        # Give up, might be a macro or expression
        return None

    def _parse_with_pycparser(self, file_path: Path, content: str) -> None:
        """
        Parse using pycparser for structs, enums, typedefs.

        Note: Requires preprocessing to resolve includes/macros.
        """
        try:
            # pycparser requires preprocessed input
            # For now, try to parse directly (may fail on complex headers)
            parser = c_parser.CParser()
            ast = parser.parse(content, filename=str(file_path))

            # Visit AST nodes
            for ext in ast.ext:
                self._visit_ast_node(ext)

        except Exception as e:
            logger.warning(f"pycparser AST parsing failed: {e}")
            raise

    def _visit_ast_node(self, node) -> None:
        """Visit pycparser AST node and extract symbols."""
        if isinstance(node, c_ast.Typedef):
            self._handle_typedef(node)
        elif isinstance(node, c_ast.Decl):
            if isinstance(node.type, c_ast.Struct):
                self._handle_struct(node.type)
            elif isinstance(node.type, c_ast.Enum):
                self._handle_enum(node.type)

    def _handle_typedef(self, node: c_ast.Typedef) -> None:
        """Handle typedef node."""
        name = node.name
        # Get actual type (simplified)
        if isinstance(node.type, c_ast.TypeDecl):
            actual_type = node.type.type
            if isinstance(actual_type, c_ast.IdentifierType):
                type_name = ' '.join(actual_type.names)
                self.symbol_db.add_typedef(name, type_name)
                logger.debug(f"Typedef: {name} = {type_name}")

    def _handle_struct(self, node: c_ast.Struct) -> None:
        """Handle struct node."""
        if not node.name:
            return  # Anonymous struct

        fields = []
        offset = 0

        if node.decls:
            for decl in node.decls:
                if isinstance(decl, c_ast.Decl):
                    field_name = decl.name
                    # Get type (simplified)
                    field_type = self._get_type_name(decl.type)

                    # Estimate size (very rough, doesn't handle alignment)
                    field_size = self._estimate_type_size(field_type)

                    fields.append(StructField(
                        name=field_name,
                        type=field_type,
                        offset=offset,
                        size=field_size
                    ))

                    offset += field_size

        struct = StructDef(name=node.name, fields=fields, size=offset)
        self.symbol_db.add_struct(struct)
        logger.debug(f"Struct: {node.name} ({len(fields)} fields)")

    def _handle_enum(self, node: c_ast.Enum) -> None:
        """Handle enum node."""
        values = {}
        current_value = 0

        if node.values:
            for enumerator in node.values.enumerators:
                name = enumerator.name
                if enumerator.value:
                    # Has explicit value
                    current_value = self._evaluate_const_expr(enumerator.value)
                values[name] = current_value
                current_value += 1

        enum = EnumDef(name=node.name, values=values)
        self.symbol_db.add_enum(enum)
        logger.debug(f"Enum: {node.name or '(anonymous)'} ({len(values)} values)")

    def _get_type_name(self, type_node) -> str:
        """Extract type name from AST node (simplified)."""
        if isinstance(type_node, c_ast.TypeDecl):
            return self._get_type_name(type_node.type)
        elif isinstance(type_node, c_ast.IdentifierType):
            return ' '.join(type_node.names)
        elif isinstance(type_node, c_ast.PtrDecl):
            return self._get_type_name(type_node.type) + '*'
        elif isinstance(type_node, c_ast.ArrayDecl):
            return self._get_type_name(type_node.type) + '[]'
        else:
            return 'unknown'

    def _estimate_type_size(self, type_name: str) -> int:
        """Estimate size of type in bytes (very rough)."""
        type_sizes = {
            'char': 1,
            'short': 2,
            'int': 4,
            'long': 4,
            'float': 4,
            'double': 8,
            'dword': 4,
            'DWORD': 4,
            'word': 2,
            'WORD': 2,
            'byte': 1,
            'BYTE': 1,
        }

        # Pointer types
        if '*' in type_name:
            return 4  # 32-bit pointer

        # Look up base type
        for base_type, size in type_sizes.items():
            if base_type in type_name:
                return size

        # Default to 4 bytes (int)
        return 4

    def _evaluate_const_expr(self, node) -> int:
        """Evaluate constant expression (simplified)."""
        if isinstance(node, c_ast.Constant):
            try:
                return int(node.value, 0)  # Auto-detect base
            except ValueError:
                return 0
        # Complex expressions not supported
        return 0

    def _parse_with_regex(self, content: str) -> None:
        """
        Fallback regex-based parsing for structs and enums.

        Limited but doesn't require pycparser.
        """
        self._parse_structs_regex(content)
        self._parse_enums_regex(content)
        self._parse_typedefs_regex(content)

    def _parse_structs_regex(self, content: str) -> None:
        """Parse struct definitions using regex."""
        # Pattern: struct NAME { ... };
        struct_pattern = r'struct\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{([^}]+)\}'

        for match in re.finditer(struct_pattern, content, re.DOTALL):
            struct_name = match.group(1)
            body = match.group(2)

            fields = []
            offset = 0

            # Parse fields: type name;
            field_pattern = r'([A-Za-z_][A-Za-z0-9_\s\*]+)\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[([0-9]+)\])?\s*;'

            for field_match in re.finditer(field_pattern, body):
                field_type = field_match.group(1).strip()
                field_name = field_match.group(2)
                array_size = field_match.group(3)

                if array_size:
                    field_type += f'[{array_size}]'

                field_size = self._estimate_type_size(field_type)

                fields.append(StructField(
                    name=field_name,
                    type=field_type,
                    offset=offset,
                    size=field_size
                ))

                offset += field_size

            struct = StructDef(name=struct_name, fields=fields, size=offset)
            self.symbol_db.add_struct(struct)
            logger.debug(f"Struct (regex): {struct_name} ({len(fields)} fields)")

    def _parse_enums_regex(self, content: str) -> None:
        """Parse enum definitions using regex."""
        # Pattern: enum NAME { ... };
        enum_pattern = r'enum\s+([A-Za-z_][A-Za-z0-9_]*)?\s*\{([^}]+)\}'

        for match in re.finditer(enum_pattern, content, re.DOTALL):
            enum_name = match.group(1)  # Can be None for anonymous
            body = match.group(2)

            values = {}
            current_value = 0

            # Parse enumerators: NAME = VALUE or just NAME
            for line in body.split(','):
                line = line.strip()
                if not line or line.startswith('//'):
                    continue

                # Remove trailing comment
                line = re.sub(r'//.*$', '', line).strip()

                if '=' in line:
                    parts = line.split('=')
                    name = parts[0].strip()
                    value_str = parts[1].strip()
                    try:
                        current_value = int(value_str, 0)  # Auto-detect base
                    except ValueError:
                        pass  # Keep current_value
                else:
                    name = line

                if name:
                    values[name] = current_value
                    current_value += 1

            enum = EnumDef(name=enum_name, values=values)
            self.symbol_db.add_enum(enum)
            logger.debug(f"Enum (regex): {enum_name or '(anonymous)'} ({len(values)} values)")

    def _parse_typedefs_regex(self, content: str) -> None:
        """Parse typedef definitions using regex."""
        # Pattern: typedef TYPE NAME;
        typedef_pattern = r'typedef\s+([A-Za-z_][A-Za-z0-9_\s\*]+)\s+([A-Za-z_][A-Za-z0-9_]*)\s*;'

        for match in re.finditer(typedef_pattern, content):
            actual_type = match.group(1).strip()
            typedef_name = match.group(2)

            self.symbol_db.add_typedef(typedef_name, actual_type)
            logger.debug(f"Typedef (regex): {typedef_name} = {actual_type}")


def parse_headers(header_paths: List[Union[str, Path]]) -> SymbolDatabase:
    """
    Parse multiple C header files and merge into single symbol database.

    Args:
        header_paths: List of paths to header files

    Returns:
        Combined SymbolDatabase
    """
    parser = HeaderParser()

    for header_path in header_paths:
        try:
            parser.parse_file(header_path)
        except Exception as e:
            logger.error(f"Failed to parse {header_path}: {e}")

    return parser.symbol_db
