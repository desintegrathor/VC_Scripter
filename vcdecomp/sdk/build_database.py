"""
Build SDK databases from Scripting_SDK.md.

Generates JSON database files:
- functions.json
- structures.json
- constants.json
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from vcdecomp.sdk.sdk_parser import SDKParser
from vcdecomp.sdk.sdk_database import SDKDatabase


def build_databases(sdk_path: str, output_dir: str = None) -> None:
    """
    Build JSON databases from SDK.

    Args:
        sdk_path: Path to Scripting_SDK.md
        output_dir: Output directory for JSON files (default: vcdecomp/sdk/data/)
    """
    print(f"Parsing SDK: {sdk_path}")

    # Parse SDK
    parser = SDKParser(sdk_path)
    functions, structures, constants = parser.parse_all()

    print(f"Parsed {len(functions)} functions")
    print(f"Parsed {len(structures)} structures")
    print(f"Parsed {len(constants)} constants")

    # Load existing functions.json to preserve manually-added builtins
    if output_dir:
        data_dir = Path(output_dir)
    else:
        data_dir = Path(__file__).parent / 'data'

    existing_functions = {}
    existing_file = data_dir / 'functions.json'
    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8') as f:
            existing_functions = json.load(f)

    # Create database
    db = SDKDatabase(data_dir=str(data_dir))

    # Populate database from parser
    db.populate_from_parser(functions, structures, constants)

    # Merge manually-added functions (those with is_variadic field)
    # that were not parsed from the SDK (e.g., cos, sin, rand, sprintf)
    parsed_names = {func.name for func in functions}
    merged_count = 0
    for name, func_data in existing_functions.items():
        if name not in parsed_names and 'is_variadic' in func_data:
            # Preserve manually-added entry
            from vcdecomp.sdk.sdk_database import FunctionSignature
            db.functions[name] = FunctionSignature.from_dict(func_data)
            merged_count += 1

    if merged_count:
        print(f"Merged {merged_count} manually-added builtin functions")

    # Save to JSON files
    db.save_databases()

    print(f"\nDatabases saved to: {db.data_dir}")
    print(f"  - functions.json ({len(db.functions)} functions)")
    print(f"  - structures.json ({len(db.structures)} structures)")
    print(f"  - constants.json ({len(db.constants)} constants)")

    # Show some examples
    print("\nExample functions:")
    for func_name in list(db.functions.keys())[:5]:
        func = db.functions[func_name]
        params = ', '.join(f"{t} {n}" for t, n in func.parameters)
        print(f"  {func.return_type} {func.name}({params})")

    print("\nExample structures:")
    for struct_name in list(db.structures.keys())[:3]:
        struct = db.structures[struct_name]
        print(f"  {struct.name} (size={struct.size} bytes, {len(struct.fields)} fields)")
        for field in struct.fields[:3]:
            print(f"    +{field.offset:3d}: {field.type} {field.name}")
        if len(struct.fields) > 3:
            print(f"    ... ({len(struct.fields) - 3} more fields)")

    print("\nExample constants:")
    constant_groups = {
        'SC_LEV_MES_': [],
        'SC_P_MES_': [],
        'SC_P_AI_BATTLEMODE_': [],
        'SC_P_SIDE_': []
    }

    for name, value in db.constants.items():
        for prefix in constant_groups:
            if name.startswith(prefix):
                constant_groups[prefix].append((name, value))
                break

    for prefix, constants_list in constant_groups.items():
        if constants_list:
            print(f"  {prefix}*:")
            for name, value in sorted(constants_list[:3], key=lambda x: x[1]):
                print(f"    {name} = {value}")


def main():
    """Main entry point."""
    # Default SDK path (new clean markdown version)
    sdk_path = Path(__file__).parent.parent / 'data' / 'Scripting_SDK.md'

    if not sdk_path.exists():
        print(f"Error: SDK file not found: {sdk_path}")
        print("Please ensure Scripting_SDK.md is in vcdecomp/data/")
        sys.exit(1)

    # Build databases
    build_databases(str(sdk_path))

    print("\nSDK databases built successfully!")


if __name__ == '__main__':
    main()
