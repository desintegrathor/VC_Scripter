"""
Parser for Vietcong script header files.

Extracts:
- Function signatures from extern declarations
- Constants from #define statements
- Structure definitions with field offsets
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class FunctionSignature:
    """Represents a parsed function signature."""
    name: str
    return_type: str
    parameters: List[Tuple[str, str]]  # [(type, name), ...]
    is_variadic: bool = False
    comment: Optional[str] = None


@dataclass
class Constant:
    """Represents a #define constant."""
    name: str
    value: str
    comment: Optional[str] = None
    prefix: Optional[str] = None  # SCM_, SGI_, etc.


@dataclass
class StructField:
    """Represents a structure field."""
    name: str
    type: str
    offset: Optional[int] = None  # Will be computed if possible


@dataclass
class StructDef:
    """Represents a structure definition."""
    name: str
    fields: List[StructField]
    size: Optional[int] = None


class HeaderParser:
    """Parser for C header files."""

    # Regex patterns for parsing
    EXTERN_FUNC_PATTERN = re.compile(
        r'extern\s+'  # extern keyword
        r'(\w+(?:\s+\w+)*\s*\*?)\s+'  # return type (may include pointer)
        r'(\w+)\s*'  # function name
        r'\((.*?)\)\s*'  # parameters
        r';'  # semicolon
        r'(?:\s*//\s*(.+))?',  # optional comment
        re.MULTILINE
    )

    DEFINE_PATTERN = re.compile(
        r'#define\s+'  # #define
        r'(\w+)\s+'  # constant name
        r'(.+?)'  # value (non-greedy)
        r'(?:\s*//\s*(.+))?'  # optional comment
        r'$',  # end of line
        re.MULTILINE
    )

    STRUCT_START_PATTERN = re.compile(r'typedef\s+struct\s*\{')
    STRUCT_END_PATTERN = re.compile(r'\}\s*(\w+)\s*;')
    STRUCT_FIELD_PATTERN = re.compile(r'\s*(\w+(?:\s+\w+)*\s*\*?)\s+(\w+)(?:\[(\d+)\])?\s*;')

    def __init__(self):
        self.functions: Dict[str, FunctionSignature] = {}
        self.constants: Dict[str, Constant] = {}
        self.structures: Dict[str, StructDef] = {}

    def parse_sc_global(self, header_path: Path) -> Dict:
        """
        Parse SC_GLOBAL.H for function signatures and structures.

        Returns:
            Dict with keys: 'functions', 'structures', 'constants'
        """
        with open(header_path, 'r', encoding='latin-1') as f:
            content = f.read()

        # Parse extern function declarations
        self._parse_functions(content)

        # Parse structure definitions
        self._parse_structures(content)

        # Parse #define constants (there are some in SC_GLOBAL.H too)
        self._parse_defines(content)

        return {
            'functions': {name: asdict(func) for name, func in self.functions.items()},
            'structures': {name: asdict(struct) for name, struct in self.structures.items()},
            'constants': {name: asdict(const) for name, const in self.constants.items()},
        }

    def parse_sc_def(self, header_path: Path) -> Dict:
        """
        Parse SC_DEF.H for constant definitions.

        Returns:
            Dict with key: 'constants'
        """
        with open(header_path, 'r', encoding='latin-1') as f:
            content = f.read()

        self._parse_defines(content)

        return {
            'constants': {name: asdict(const) for name, const in self.constants.items()},
        }

    def _parse_functions(self, content: str):
        """Parse all extern function declarations."""
        for match in self.EXTERN_FUNC_PATTERN.finditer(content):
            return_type = match.group(1).strip()
            func_name = match.group(2).strip()
            params_str = match.group(3).strip()
            comment = match.group(4).strip() if match.group(4) else None

            # Parse parameters
            parameters = []
            is_variadic = False

            if params_str and params_str != 'void':
                for param in params_str.split(','):
                    param = param.strip()
                    if param == '...':
                        is_variadic = True
                        continue

                    # Parse parameter type and name
                    # Strategy: Find the rightmost identifier that's not a type keyword
                    # Handle cases like: "char *txt", "dword id", "c_Vector3 *vec"

                    # Remove all * to separate type from name clearly
                    param_no_star = param.replace('*', ' * ')
                    tokens = [t for t in param_no_star.split() if t]

                    if tokens:
                        # Find last identifier (should be param name)
                        # Everything before it is type
                        param_name = tokens[-1] if tokens[-1] != '*' else ''
                        param_type_tokens = tokens[:-1] if param_name else tokens

                        param_type = ' '.join(param_type_tokens)

                        # If we have a name but no type, it's actually unnamed param
                        if param_name and not param_type:
                            param_type = param_name
                            param_name = ''

                        parameters.append((param_type.strip(), param_name.strip()))

            self.functions[func_name] = FunctionSignature(
                name=func_name,
                return_type=return_type,
                parameters=parameters,
                is_variadic=is_variadic,
                comment=comment
            )

    def _parse_defines(self, content: str):
        """Parse all #define constants."""
        for match in self.DEFINE_PATTERN.finditer(content):
            const_name = match.group(1).strip()
            value = match.group(2).strip()
            comment = match.group(3).strip() if match.group(3) else None

            # Extract prefix (SCM_, SGI_, SC_P_, etc.)
            prefix_match = re.match(r'([A-Z_]+?)_', const_name)
            prefix = prefix_match.group(1) if prefix_match else None

            self.constants[const_name] = Constant(
                name=const_name,
                value=value,
                comment=comment,
                prefix=prefix
            )

    def _parse_structures(self, content: str):
        """Parse all typedef struct definitions."""
        # Find all struct blocks
        struct_blocks = []
        start_pos = 0

        while True:
            start_match = self.STRUCT_START_PATTERN.search(content, start_pos)
            if not start_match:
                break

            # Find matching closing brace
            brace_count = 1
            pos = start_match.end()
            struct_start = start_match.start()

            while pos < len(content) and brace_count > 0:
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1

            # Extract struct name
            end_match = self.STRUCT_END_PATTERN.search(content, pos - 1, pos + 50)
            if end_match:
                struct_name = end_match.group(1)
                struct_body = content[start_match.end():pos - 1]
                struct_blocks.append((struct_name, struct_body))

            start_pos = pos

        # Parse each struct
        for struct_name, struct_body in struct_blocks:
            fields = []

            for line in struct_body.split('\n'):
                line = line.strip()
                if not line or line.startswith('//') or line.startswith('/*'):
                    continue

                field_match = self.STRUCT_FIELD_PATTERN.match(line)
                if field_match:
                    field_type = field_match.group(1).strip()
                    field_name = field_match.group(2).strip()
                    array_size = field_match.group(3)

                    if array_size:
                        field_type += f'[{array_size}]'

                    fields.append(StructField(
                        name=field_name,
                        type=field_type
                    ))

            if fields:
                self.structures[struct_name] = StructDef(
                    name=struct_name,
                    fields=fields
                )

    def save_to_json(self, output_path: Path, data: Dict):
        """Save parsed data to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_json(self, input_path: Path) -> Dict:
        """Load parsed data from JSON file."""
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)


def main():
    """Parse headers and save to JSON."""
    parser = HeaderParser()

    # Get paths
    project_root = Path(__file__).parent.parent.parent.parent
    headers_dir = project_root / 'original-resources' / 'h'
    output_dir = project_root / 'vcdecomp' / 'core' / 'headers' / 'data'
    output_dir.mkdir(exist_ok=True)

    # Parse SC_GLOBAL.H
    print("Parsing SC_GLOBAL.H...")
    sc_global_path = headers_dir / 'SC_GLOBAL.H'
    if sc_global_path.exists():
        global_data = parser.parse_sc_global(sc_global_path)
        print(f"  Found {len(global_data['functions'])} functions")
        print(f"  Found {len(global_data['structures'])} structures")
        print(f"  Found {len(global_data['constants'])} constants")
        parser.save_to_json(output_dir / 'sc_global.json', global_data)
    else:
        print(f"  ERROR: File not found: {sc_global_path}")

    # Parse SC_DEF.H
    print("\nParsing SC_DEF.H...")
    sc_def_path = headers_dir / 'SC_DEF.H'
    if sc_def_path.exists():
        # Clear constants from previous parse
        parser.constants.clear()
        def_data = parser.parse_sc_def(sc_def_path)
        print(f"  Found {len(def_data['constants'])} constants")
        parser.save_to_json(output_dir / 'sc_def.json', def_data)
    else:
        print(f"  ERROR: File not found: {sc_def_path}")

    print("\nDone! JSON files saved to:", output_dir)


if __name__ == "__main__":
    main()
