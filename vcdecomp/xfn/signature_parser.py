"""
XFN Signature Parser

Parses function signatures embedded in XFN table name fields.
The compiler embeds type information in the format:
    FunctionName(param1,param2,...)returntype

Examples:
    SC_P_GetPos(unsignedlong,*c_Vector3)void
    SC_InitSide(unsignedlong,*s_SC_initside)void
    SC_Log(unsignedlong,*constchar,...)void
    frnd(float)float
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class ParsedParameter:
    """A parsed function parameter."""
    raw_type: str          # Original XFN type string
    c_type: str            # Normalized C type
    is_pointer: bool       # True if pointer type
    struct_name: Optional[str] = None  # Struct name if struct type


@dataclass
class ParsedSignature:
    """A fully parsed function signature."""
    name: str                          # Function name
    raw_name: str                      # Original XFN name field (with signature)
    return_type: str                   # Normalized C return type
    raw_return_type: str               # Original return type string
    parameters: List[ParsedParameter]  # Parsed parameters
    is_variadic: bool = False          # True if has ... parameter
    parse_error: Optional[str] = None  # Error message if parsing failed

    def to_sdk_format(self) -> dict:
        """Convert to SDK-compatible JSON format."""
        params = []
        for i, param in enumerate(self.parameters):
            params.append({
                "type": param.c_type,
                "name": f"arg{i}"
            })

        return {
            "name": self.name,
            "return_type": self.return_type,
            "parameters": params,
            "is_variadic": self.is_variadic,
        }


class XFNSignatureParser:
    """
    Parser for XFN function signatures.

    XFN entries store function signatures in the format:
        FunctionName(param1,param2,...)returntype

    This parser extracts:
    - Function name
    - Parameter types (mapped to C types)
    - Return type
    - Variadic indicator (...)
    - Struct types referenced in parameters
    """

    # Type mapping from XFN format to C types
    TYPE_MAP = {
        # Basic types
        "void": "void",
        "char": "char",
        "short": "short",
        "int": "int",
        "long": "long",
        "float": "float",
        "double": "double",

        # Unsigned variants (XFN uses "unsignedX" without space)
        "unsignedchar": "unsigned char",
        "unsignedshort": "unsigned short",
        "unsignedint": "unsigned int",
        "unsignedlong": "unsigned long",

        # Signed variants
        "signedchar": "signed char",
        "signedshort": "signed short",
        "signedint": "signed int",
        "signedlong": "signed long",

        # Common typedefs (game engine specific)
        "dword": "dword",
        "word": "word",
        "byte": "byte",
        "bool": "bool",

        # Const variants
        "constchar": "const char",
        "constvoid": "const void",
    }

    # Pattern to match function signature: Name(params)return
    SIGNATURE_PATTERN = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\(([^)]*)\)(.+)$')

    def __init__(self):
        self.struct_types: set = set()  # Track discovered struct types

    def parse(self, xfn_name: str) -> ParsedSignature:
        """
        Parse an XFN name field into a structured signature.

        Args:
            xfn_name: The raw XFN name field (e.g., "SC_P_GetPos(unsignedlong,*c_Vector3)void")

        Returns:
            ParsedSignature with extracted type information
        """
        # Try to match the signature pattern
        match = self.SIGNATURE_PATTERN.match(xfn_name)
        if not match:
            # No signature embedded - just function name
            return ParsedSignature(
                name=xfn_name,
                raw_name=xfn_name,
                return_type="void",
                raw_return_type="",
                parameters=[],
                parse_error="No embedded signature"
            )

        func_name = match.group(1)
        params_str = match.group(2)
        return_str = match.group(3)

        # Parse parameters
        parameters = []
        is_variadic = False

        if params_str.strip():
            param_parts = self._split_parameters(params_str)
            for param in param_parts:
                param = param.strip()
                if param == "...":
                    is_variadic = True
                    continue

                # Skip 'void' as sole parameter (C convention for no params)
                if param.lower() == "void" and len(param_parts) == 1:
                    continue

                parsed_param = self._parse_type(param)
                parameters.append(parsed_param)

        # Parse return type (handle pointer return types like *void)
        return_type = self._parse_return_type(return_str)

        return ParsedSignature(
            name=func_name,
            raw_name=xfn_name,
            return_type=return_type,
            raw_return_type=return_str,
            parameters=parameters,
            is_variadic=is_variadic,
        )

    def _split_parameters(self, params_str: str) -> List[str]:
        """
        Split parameter string by commas, handling nested structures.

        This is straightforward as XFN format doesn't have nested parentheses
        in parameter types.
        """
        return [p.strip() for p in params_str.split(',') if p.strip()]

    def _parse_type(self, type_str: str) -> ParsedParameter:
        """
        Parse a single parameter type.

        Handles:
        - Basic types (int, float, void, etc.)
        - Pointer types (*char, **void)
        - Struct/class pointers (*c_Vector3, *s_SC_initside)
        - Const qualifiers
        """
        original = type_str
        is_pointer = False
        pointer_depth = 0
        struct_name = None

        # Count and strip leading asterisks (pointer markers)
        while type_str.startswith('*'):
            is_pointer = True
            pointer_depth += 1
            type_str = type_str[1:]

        # Check for struct/class prefixes
        if type_str.startswith(('c_', 's_', 'C_', 'S_')):
            struct_name = type_str
            self.struct_types.add(struct_name)
            # Keep struct name as type
            c_type = struct_name
        else:
            # Normalize the type
            c_type = self._normalize_type(type_str)

        # Add pointer suffix
        if is_pointer:
            c_type = c_type + '*' * pointer_depth

        return ParsedParameter(
            raw_type=original,
            c_type=c_type,
            is_pointer=is_pointer,
            struct_name=struct_name
        )

    def _parse_return_type(self, return_str: str) -> str:
        """
        Parse return type, handling leading asterisks for pointer returns.

        XFN format uses *type for pointer returns (e.g., *void, *char)
        while C uses type* format.
        """
        return_str = return_str.strip()

        # Count and strip leading asterisks
        pointer_depth = 0
        while return_str.startswith('*'):
            pointer_depth += 1
            return_str = return_str[1:]

        # Normalize the base type
        base_type = self._normalize_type(return_str)

        # Add pointer suffix (C style: type*)
        if pointer_depth > 0:
            base_type = base_type + '*' * pointer_depth

        return base_type

    def _normalize_type(self, type_str: str) -> str:
        """
        Normalize an XFN type string to C type.

        Handles the XFN convention of no spaces between unsigned/signed and type.
        """
        # Strip any whitespace
        type_str = type_str.strip()

        # Handle pointer suffix (shouldn't be here but just in case)
        pointer_suffix = ""
        while type_str.endswith('*'):
            pointer_suffix += '*'
            type_str = type_str[:-1]

        # Check direct mapping first
        if type_str.lower() in self.TYPE_MAP:
            return self.TYPE_MAP[type_str.lower()] + pointer_suffix

        # Try lowercase lookup
        lower = type_str.lower()
        if lower in self.TYPE_MAP:
            return self.TYPE_MAP[lower] + pointer_suffix

        # Handle "const" prefix
        if lower.startswith("const"):
            rest = lower[5:]  # Strip "const"
            if rest in self.TYPE_MAP:
                return "const " + self.TYPE_MAP[rest] + pointer_suffix
            return "const " + rest + pointer_suffix

        # Check for struct/class types
        if type_str.startswith(('c_', 's_', 'C_', 'S_')):
            self.struct_types.add(type_str)
            return type_str + pointer_suffix

        # Unknown type - return as-is
        return type_str + pointer_suffix

    def get_discovered_structs(self) -> set:
        """Return all struct types discovered during parsing."""
        return self.struct_types.copy()


def parse_xfn_signature(xfn_name: str) -> ParsedSignature:
    """
    Convenience function to parse a single XFN signature.

    Args:
        xfn_name: Raw XFN name field

    Returns:
        ParsedSignature instance
    """
    parser = XFNSignatureParser()
    return parser.parse(xfn_name)
