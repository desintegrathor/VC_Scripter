"""
Build SDK databases from Scripting_SDK.txt.

Generates JSON database files:
- functions.json (734 functions)
- structures.json (46 structs)
- constants.json (98+ constants)
"""

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
        sdk_path: Path to Scripting_SDK.txt
        output_dir: Output directory for JSON files (default: vcdecomp/sdk/data/)
    """
    print(f"Parsing SDK: {sdk_path}")

    # Parse SDK
    parser = SDKParser(sdk_path)
    functions, structures, constants = parser.parse_all()

    print(f"Parsed {len(functions)} functions")
    print(f"Parsed {len(structures)} structures")
    print(f"Parsed {len(constants)} constants")

    # Create database
    if output_dir:
        db = SDKDatabase(data_dir=output_dir)
    else:
        db = SDKDatabase()  # Use default location

    # Populate database
    db.populate_from_parser(functions, structures, constants)

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
    # Default SDK path
    sdk_path = Path(__file__).parent.parent.parent / 'original-resources' / 'Scripting_SDK.txt'

    if not sdk_path.exists():
        print(f"Error: SDK file not found: {sdk_path}")
        print("Please ensure Scripting_SDK.txt is in original-resources/")
        sys.exit(1)

    # Build databases
    build_databases(str(sdk_path))

    print("\nSDK databases built successfully!")


if __name__ == '__main__':
    main()
