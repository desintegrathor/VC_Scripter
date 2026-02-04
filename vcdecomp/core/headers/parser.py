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
    # Matches struct field declarations like:
    #   dword action;   char *wpName;   c_Vector3 shoot;   dword ai[4];
    # Group 1: type (everything before the name), Group 2: pointer star, Group 3: name, Group 4: array size
    STRUCT_FIELD_PATTERN = re.compile(r'\s*(\w+(?:\s+\w+)*?)\s+(\*?)(\w+)(?:\[(\d+)\])?\s*;')

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

    # Pattern for named struct: struct name { ... };
    NAMED_STRUCT_START_PATTERN = re.compile(r'struct\s+(\w+)\s*\{')

    # Pattern for function definition with body: ReturnType FuncName(params) {
    FUNC_DEF_PATTERN = re.compile(
        r'^(\w+)\s+\*?\s*'    # return type; optional pointer star after
        r'(\w+)\s*'           # function name
        r'\(([^)]*)\)\s*$',   # parameters
        re.MULTILINE
    )

    # Pattern to match #include directives: #include <path> or #include "path"
    INCLUDE_PATTERN = re.compile(r'#include\s*[<"](.+?)[>"]')

    # Headers already handled by SDK/header database — skip these in include resolution
    SKIP_INCLUDES = {'sc_global.h', 'sc_def.h', 'sc_mpglobal.h', 'mplevel.inc'}

    def _resolve_includes(self, content: str, include_dirs: List[Path],
                          visited: Optional[set] = None) -> str:
        """
        Resolve #include directives and return concatenated content from included files.

        Args:
            content: The header file content to scan for includes
            include_dirs: Directories to search for included files
            visited: Set of already-visited filenames (lowercase) to prevent circular includes

        Returns:
            Concatenated content of all resolved included files
        """
        if visited is None:
            visited = set()

        included_parts = []

        for match in self.INCLUDE_PATTERN.finditer(content):
            inc_path_str = match.group(1)
            # Extract just the filename from paths like inc\gLevel_h.h or inc/gLevel_h.h
            inc_filename = Path(inc_path_str.replace('\\', '/')).name
            inc_filename_lower = inc_filename.lower()

            # Skip headers already handled by SDK/database
            if inc_filename_lower in self.SKIP_INCLUDES:
                continue

            # Skip already-visited files (circular include protection)
            if inc_filename_lower in visited:
                continue

            # Case-insensitive search in include directories
            resolved_path = None
            for inc_dir in include_dirs:
                if not inc_dir.exists():
                    continue
                for candidate in inc_dir.iterdir():
                    if candidate.is_file() and candidate.name.lower() == inc_filename_lower:
                        resolved_path = candidate
                        break
                if resolved_path:
                    break

            if resolved_path:
                visited.add(inc_filename_lower)
                inc_content = resolved_path.read_text(encoding='latin-1')
                # Recursively resolve includes within the included file
                nested = self._resolve_includes(inc_content, include_dirs, visited)
                if nested:
                    included_parts.append(nested)
                included_parts.append(inc_content)

        return '\n'.join(included_parts)

    def parse_mission_header(self, header_path: Path,
                             include_dirs: Optional[List[Path]] = None) -> Dict:
        """
        Parse a mission-specific header file (e.g., LEVEL_H.H).

        Follows #include directives to resolve shared headers (e.g., gLevel_h.h)
        from the provided include directories.

        Extracts:
        - #define constants (reuses _parse_defines)
        - Named struct definitions (struct name { fields };)
        - Function definitions with bodies (extracts signature, skips body)

        Args:
            header_path: Path to the mission header file
            include_dirs: Directories to search for #include'd files

        Returns:
            Dict with keys: 'constants', 'structures', 'functions'
        """
        # Reset state for fresh parse
        self.functions = {}
        self.constants = {}
        self.structures = {}

        with open(header_path, 'r', encoding='latin-1') as f:
            content = f.read()

        # Resolve and prepend included headers
        if include_dirs:
            included_content = self._resolve_includes(content, include_dirs)
            if included_content:
                content = included_content + '\n' + content

        # Parse #define constants
        self._parse_defines(content)

        # Parse typedef struct definitions (existing)
        self._parse_structures(content)

        # Parse named struct definitions (struct name { ... };)
        self._parse_named_structures(content)

        # Parse function definitions with bodies
        self._parse_function_definitions(content)

        return {
            'functions': {name: asdict(func) for name, func in self.functions.items()},
            'structures': {name: asdict(struct) for name, struct in self.structures.items()},
            'constants': {name: asdict(const) for name, const in self.constants.items()},
        }

    def _parse_named_structures(self, content: str):
        """Parse named struct definitions: struct name { fields };"""
        for match in self.NAMED_STRUCT_START_PATTERN.finditer(content):
            struct_name = match.group(1)
            # Skip if already parsed as typedef struct
            if struct_name in self.structures:
                continue

            # Find matching closing brace
            brace_count = 1
            pos = match.end()
            struct_start = match.start()

            while pos < len(content) and brace_count > 0:
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1

            # Verify it ends with };
            rest = content[pos:pos + 20].strip()
            if not rest.startswith(';'):
                continue

            struct_body = content[match.end():pos - 1]

            # Parse fields
            fields = []
            for line in struct_body.split('\n'):
                line = line.strip()
                if not line or line.startswith('//') or line.startswith('/*'):
                    continue

                # Remove inline comments
                if '//' in line:
                    line = line[:line.index('//')]

                field_match = self.STRUCT_FIELD_PATTERN.match(line)
                if field_match:
                    field_type = field_match.group(1).strip()
                    pointer_star = field_match.group(2)
                    if pointer_star:
                        field_type += ' *'
                    field_name = field_match.group(3).strip()
                    array_size = field_match.group(4)

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

    def _parse_function_definitions(self, content: str):
        """
        Parse function definitions with bodies.

        Extracts signature, skips body via brace counting.
        Ignores #define macros, extern declarations, and struct definitions.
        """
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip preprocessor, comments, struct blocks, extern declarations
            if (not line or line.startswith('#') or line.startswith('//')
                    or line.startswith('/*') or line.startswith('extern')
                    or line.startswith('typedef') or line.startswith('struct ')):
                i += 1
                continue

            # Look for function definition: ReturnType FuncName(params)
            # The opening brace may be on same line or next line
            func_match = self.FUNC_DEF_PATTERN.match(line)
            if func_match:
                return_type = func_match.group(1).strip()
                func_name = func_match.group(2).strip()
                params_str = func_match.group(3).strip()

                # Check if next non-empty line is '{'
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1

                if j < len(lines) and lines[j].strip().startswith('{'):
                    # This is a function definition - extract signature
                    # Parse parameters
                    parameters = []
                    is_variadic = False

                    if params_str and params_str != 'void':
                        for param in params_str.split(','):
                            param = param.strip()
                            if param == '...':
                                is_variadic = True
                                continue

                            param_no_star = param.replace('*', ' * ')
                            tokens = [t for t in param_no_star.split() if t]

                            if tokens:
                                param_name = tokens[-1] if tokens[-1] != '*' else ''
                                param_type_tokens = tokens[:-1] if param_name else tokens
                                param_type = ' '.join(param_type_tokens)

                                if param_name and not param_type:
                                    param_type = param_name
                                    param_name = ''

                                parameters.append((param_type.strip(), param_name.strip()))

                    self.functions[func_name] = FunctionSignature(
                        name=func_name,
                        return_type=return_type,
                        parameters=parameters,
                        is_variadic=is_variadic
                    )

                    # Skip the function body by counting braces
                    brace_count = 0
                    k = j
                    while k < len(lines):
                        for ch in lines[k]:
                            if ch == '{':
                                brace_count += 1
                            elif ch == '}':
                                brace_count -= 1
                        if brace_count <= 0:
                            break
                        k += 1
                    i = k + 1
                    continue

            # Also handle: ReturnType FuncName(params) {  (brace on same line)
            # Check if line ends with '{'
            if '{' in line and '(' in line and ')' in line:
                # Try to parse as function def with brace on same line
                brace_idx = line.index('{')
                sig_part = line[:brace_idx].strip()
                sig_match = self.FUNC_DEF_PATTERN.match(sig_part)
                if sig_match:
                    return_type = sig_match.group(1).strip()
                    func_name = sig_match.group(2).strip()
                    params_str = sig_match.group(3).strip()

                    parameters = []
                    is_variadic = False

                    if params_str and params_str != 'void':
                        for param in params_str.split(','):
                            param = param.strip()
                            if param == '...':
                                is_variadic = True
                                continue

                            param_no_star = param.replace('*', ' * ')
                            tokens = [t for t in param_no_star.split() if t]

                            if tokens:
                                param_name = tokens[-1] if tokens[-1] != '*' else ''
                                param_type_tokens = tokens[:-1] if param_name else tokens
                                param_type = ' '.join(param_type_tokens)

                                if param_name and not param_type:
                                    param_type = param_name
                                    param_name = ''

                                parameters.append((param_type.strip(), param_name.strip()))

                    self.functions[func_name] = FunctionSignature(
                        name=func_name,
                        return_type=return_type,
                        parameters=parameters,
                        is_variadic=is_variadic
                    )

                    # Skip body
                    brace_count = line.count('{') - line.count('}')
                    if brace_count > 0:
                        k = i + 1
                        while k < len(lines):
                            brace_count += lines[k].count('{') - lines[k].count('}')
                            if brace_count <= 0:
                                break
                            k += 1
                        i = k + 1
                        continue

            i += 1

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
                    pointer_star = field_match.group(2)
                    if pointer_star:
                        field_type += ' *'
                    field_name = field_match.group(3).strip()
                    array_size = field_match.group(4)

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
    headers_dir = Path(__file__).parent.parent.parent / 'compiler' / 'inc'
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
