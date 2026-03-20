"""Entry point for vcdecomp_mcp package.

Usage:
    py -3 -m vcdecomp_mcp              # Run MCP server (stdio transport)
    py -3 -m vcdecomp_mcp open FILE    # Quick test: open and print summary
    py -3 -m vcdecomp_mcp --help       # Show help
"""

import sys
import os

# Fix console encoding on Windows
if sys.platform == 'win32':
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def _print_summary(filepath: str) -> None:
    """Open a .scr file and print session summary."""
    from .session import SCRSession

    session = SCRSession.open(filepath)
    print(f"Handle: {session.handle}")
    print(f"Path: {session.path}")
    print(f"Functions: {len(session.func_bounds)}")
    print(f"Instructions: {session.scr.code_segment.code_count}")
    print(f"XFN count: {session.scr.xfn_table.xfn_count}")
    print(f"Data segment: {session.scr.data_segment.data_count} dwords")
    print(f"Globals resolved: {len(session.globals_usage)}")

    print("\nFunctions:")
    for name, (start, end) in sorted(session.func_bounds.items(), key=lambda x: x[1][0]):
        print(f"  {name}: {start}-{end}")


def main():
    args = sys.argv[1:]

    if args and args[0] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)

    if args and args[0] == "open":
        if len(args) < 2:
            print("Usage: py -3 -m vcdecomp_mcp open <file.scr>")
            sys.exit(1)
        _print_summary(args[1])
    else:
        # Default: run MCP server (stdio transport)
        from .mcp_server import mcp
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
