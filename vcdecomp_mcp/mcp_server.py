"""MCP server for interactive .scr file decompilation and analysis."""

import os
import shutil
import subprocess
from typing import Dict, Optional
from mcp.server.fastmcp import FastMCP

from .session import SCRSession

mcp = FastMCP(
    "vcdecomp-mcp",
    instructions=(
        "Vietcong .scr bytecode decompiler. Use scr_open to load a file, "
        "then query functions, globals, data, XFNs, and decompile individual functions. "
        "Use scr_rename/scr_set_type to mutate analysis — changes propagate on next query."
    ),
)

_sessions: Dict[str, SCRSession] = {}


def _get_session(handle: str) -> SCRSession:
    if handle not in _sessions:
        raise ValueError(f"No file loaded with handle '{handle}'. Use scr_open first.")
    return _sessions[handle]


def _make_handle(path: str) -> str:
    base = os.path.basename(path)
    name = os.path.splitext(base)[0].lower()
    if name in _sessions:
        i = 2
        while f"{name}_{i}" in _sessions:
            i += 1
        return f"{name}_{i}"
    return name


# ============================================================
# Phase 1: Core read-only tools
# ============================================================

@mcp.tool()
def scr_open(path: str) -> dict:
    """Open and analyze a .scr bytecode file. Runs parsing, SSA construction,
    and global variable resolution. Returns handle + metadata summary.

    Args:
        path: Absolute or relative path to the .scr file
    """
    handle = _make_handle(path)
    session = SCRSession.open(path, handle=handle)
    _sessions[handle] = session

    scr = session.scr
    return {
        "handle": handle,
        "path": session.path,
        "entry_point": scr.header.enter_ip,
        "instruction_count": scr.code_segment.code_count,
        "function_count": len(session.func_bounds),
        "xfn_count": scr.xfn_table.xfn_count,
        "data_segment_dwords": scr.data_segment.data_count,
        "data_segment_bytes": len(scr.data_segment.raw_data),
        "globals_resolved": len(session.globals_usage),
        "string_count": len(scr.data_strings),
    }


@mcp.tool()
def scr_close(handle: str) -> dict:
    """Close a previously opened .scr file and free its session.

    Args:
        handle: Handle returned by scr_open
    """
    if handle in _sessions:
        del _sessions[handle]
        return {"status": "ok", "handle": handle}
    return {"status": "not_found", "handle": handle}


@mcp.tool()
def scr_list() -> list:
    """List all currently opened .scr sessions with handles and paths."""
    return [
        {
            "handle": h,
            "path": s.path,
            "function_count": len(s.func_bounds),
        }
        for h, s in _sessions.items()
    ]


@mcp.tool()
def scr_info(handle: str) -> dict:
    """Get detailed file info: header fields, entry point, segment sizes, counts.

    Args:
        handle: Handle returned by scr_open
    """
    s = _get_session(handle)
    scr = s.scr
    h = scr.header
    return {
        "path": s.path,
        "filename": scr.filename,
        "entry_point": h.enter_ip,
        "instruction_count": scr.code_segment.code_count,
        "function_count": len(s.func_bounds),
        "xfn_count": scr.xfn_table.xfn_count,
        "data_segment_dwords": scr.data_segment.data_count,
        "data_segment_bytes": len(scr.data_segment.raw_data),
        "globals_resolved": len(s.globals_usage),
        "string_count": len(scr.data_strings),
        "has_save_info": scr.save_info is not None,
        "opcode_variant": "forced" if scr.opcode_variant_forced else "auto",
    }


@mcp.tool()
def scr_list_funcs(handle: str, filter: Optional[str] = None) -> list:
    """List all detected functions with name, address range, and instruction count.

    Args:
        handle: Handle returned by scr_open
        filter: Optional substring filter on function name
    """
    s = _get_session(handle)
    results = []
    for name, (start, end) in sorted(s.func_bounds.items(), key=lambda x: x[1][0]):
        if filter and filter.lower() not in name.lower():
            continue
        results.append({
            "name": name,
            "start": start,
            "end": end,
            "instruction_count": end - start + 1,
        })
    return results


@mcp.tool()
def scr_decompile(handle: str, func: str) -> dict:
    """Decompile a single function to C code.

    Args:
        handle: Handle returned by scr_open
        func: Function name (as shown by scr_list_funcs)
    """
    s = _get_session(handle)
    try:
        code = s.decompile_func(func)
        return {"func": func, "code": code}
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool()
def scr_disasm(handle: str, func: Optional[str] = None,
               addr: Optional[int] = None, count: int = 50) -> dict:
    """Get disassembly output. Specify either a function name or an address range.

    Args:
        handle: Handle returned by scr_open
        func: Function name to disassemble (mutually exclusive with addr)
        addr: Starting instruction address (mutually exclusive with func)
        count: Number of instructions when using addr (default 50)
    """
    s = _get_session(handle)
    try:
        if func:
            text = s.get_disasm_func(func)
            return {"func": func, "disasm": text}
        elif addr is not None:
            text = s.get_disasm_range(addr, count)
            return {"addr": addr, "count": count, "disasm": text}
        else:
            return {"error": "Specify either func or addr"}
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool()
def scr_list_globals(handle: str, filter: Optional[str] = None) -> list:
    """List resolved global variables with offset, name, type, and initializer.

    Args:
        handle: Handle returned by scr_open
        filter: Optional substring filter on variable name
    """
    s = _get_session(handle)
    return s.get_globals_list(filter or "")


@mcp.tool()
def scr_get_data(handle: str, offset: int, type: str = "int", count: int = 1) -> dict:
    """Read typed value(s) from the data segment.

    Args:
        handle: Handle returned by scr_open
        offset: Byte offset into data segment
        type: Data type: "int", "float", "string", "bytes" (default "int")
        count: Number of values to read (default 1; for "bytes", this is byte count)
    """
    s = _get_session(handle)
    values = s.get_data_value(offset, type, count)
    return {"offset": offset, "type": type, "values": values}


@mcp.tool()
def scr_list_xfns(handle: str, filter: Optional[str] = None) -> list:
    """List external function table entries (engine API calls).

    Args:
        handle: Handle returned by scr_open
        filter: Optional substring filter on function name
    """
    s = _get_session(handle)
    results = []
    for entry in s.scr.xfn_table.entries:
        if filter and filter.lower() not in entry.name.lower():
            continue
        results.append({
            "index": entry.index,
            "name": entry.name,
            "arg_count": entry.arg_count,
            "ret_size": entry.ret_size,
            "returns_float": entry.field4 == 1,
        })
    return results


@mcp.tool()
def scr_strings(handle: str, filter: Optional[str] = None) -> list:
    """List all strings found in the data segment with their offsets.

    Args:
        handle: Handle returned by scr_open
        filter: Optional substring filter on string content
    """
    s = _get_session(handle)
    return s.get_strings(filter or "")


# ============================================================
# Phase 2: Mutation and analysis tools
# ============================================================

@mcp.tool()
def scr_rename(handle: str, target_type: str, old_name: str, new_name: str,
               func_context: Optional[str] = None) -> dict:
    """Rename a function, global variable, or local variable.
    Changes propagate to subsequent scr_decompile calls.

    Args:
        handle: Handle returned by scr_open
        target_type: One of "function", "global", "local"
        old_name: Current name
        new_name: New name
        func_context: Required when target_type is "local" — the function containing the variable
    """
    s = _get_session(handle)
    return s.rename(target_type, old_name, new_name, func_context or "")


@mcp.tool()
def scr_set_type(handle: str, target: str, new_type: str) -> dict:
    """Override the type of a global or local variable.
    Changes propagate to subsequent scr_decompile calls.

    Args:
        handle: Handle returned by scr_open
        target: "global:<name>" or "local:<func_name>:<var_name>"
        new_type: C type string (e.g. "float", "int", "s_SC_NET_info *")
    """
    s = _get_session(handle)
    return s.set_type(target, new_type)


@mcp.tool()
def scr_xrefs_to(handle: str, target: str) -> dict:
    """Find all references to a global variable, function, or external function.

    Args:
        handle: Handle returned by scr_open
        target: Global variable name, function name, or "xfn:<name>" for external functions
    """
    s = _get_session(handle)
    refs = s.get_xrefs_to(target)
    return {"target": target, "count": len(refs), "refs": refs}


@mcp.tool()
def scr_callees(handle: str, func: str) -> dict:
    """List all functions and external functions called by a function.

    Args:
        handle: Handle returned by scr_open
        func: Function name
    """
    s = _get_session(handle)
    try:
        return s.get_callees(func)
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool()
def scr_basic_blocks(handle: str, func: str) -> dict:
    """Get CFG basic blocks for a function with successor/predecessor edges.

    Args:
        handle: Handle returned by scr_open
        func: Function name
    """
    s = _get_session(handle)
    try:
        blocks = s.get_basic_blocks(func)
        return {"func": func, "block_count": len(blocks), "blocks": blocks}
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool()
def scr_search(handle: str, query: str, search_in: str = "all") -> dict:
    """Search for strings, immediate values, or data references in code/data.

    Args:
        handle: Handle returned by scr_open
        query: Search string (also parsed as integer for immediate search)
        search_in: "code", "data", or "all" (default "all")
    """
    s = _get_session(handle)
    results = s.search(query, search_in)
    return {"query": query, "count": len(results), "results": results}


# ============================================================
# Phase 3: Comments, export, advanced analysis
# ============================================================

@mcp.tool()
def scr_set_comment(handle: str, addr: int, comment: str) -> dict:
    """Add or update a comment at an instruction address.

    Args:
        handle: Handle returned by scr_open
        addr: Instruction index
        comment: Comment text (empty string to remove)
    """
    s = _get_session(handle)
    if comment:
        s.comments[addr] = comment
    else:
        s.comments.pop(addr, None)
    s._auto_save()
    return {"status": "ok", "addr": addr}


@mcp.tool()
def scr_save(handle: str) -> dict:
    """Save session annotations (renames, types, comments) to .vcdb sidecar file.

    Args:
        handle: Handle returned by scr_open
    """
    s = _get_session(handle)
    path = s.save_session()
    return {"status": "ok", "path": path}


@mcp.tool()
def scr_callgraph(handle: str, root: Optional[str] = None,
                  max_depth: int = 10) -> dict:
    """Build recursive call graph from a root function (or all functions).

    Args:
        handle: Handle returned by scr_open
        root: Root function name (default: all functions)
        max_depth: Maximum recursion depth (default 10)
    """
    s = _get_session(handle)
    roots = [root] if root else None
    return s.get_callgraph(roots, max_depth)


@mcp.tool()
def scr_read_struct(handle: str, offset: int, struct_name: str) -> dict:
    """Interpret a data segment region as an SDK struct, showing typed fields.

    Args:
        handle: Handle returned by scr_open
        offset: Byte offset into data segment where the struct starts
        struct_name: SDK struct name (e.g. "s_SC_MP_Recover", "c_Vector3")
    """
    s = _get_session(handle)
    return s.read_struct(offset, struct_name)


@mcp.tool()
def scr_ssa(handle: str, func: str) -> dict:
    """View SSA form for a function: blocks with instructions, inputs, outputs.

    Args:
        handle: Handle returned by scr_open
        func: Function name
    """
    s = _get_session(handle)
    try:
        return s.get_ssa_form(func)
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool()
def scr_stack_frame(handle: str, func: str) -> dict:
    """View stack frame layout for a function: parameters and local variables.

    Args:
        handle: Handle returned by scr_open
        func: Function name
    """
    s = _get_session(handle)
    try:
        return s.get_stack_frame(func)
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool()
def scr_export(handle: str, format: str = "json") -> dict:
    """Export function prototypes and global declarations.
    Applies any renames and type overrides from mutations.

    Args:
        handle: Handle returned by scr_open
        format: "json" or "header" (C header format)
    """
    s = _get_session(handle)

    funcs = []
    for name, (start, end) in sorted(s.func_bounds.items(), key=lambda x: x[1][0]):
        funcs.append({
            "name": name,
            "start": start,
            "end": end,
            "instruction_count": end - start + 1,
        })

    globals_list = s.get_globals_list()

    if format == "header":
        lines = ["// Auto-generated function prototypes", ""]
        for f in funcs:
            lines.append(f"void {f['name']}();  // @ {f['start']}")
        lines.append("")
        lines.append("// Global variables")
        for g in globals_list:
            lines.append(f"{g['type']} {g['name']};  // offset {g['offset']}")
        return {"format": "header", "content": "\n".join(lines)}

    return {
        "format": "json",
        "functions": funcs,
        "globals": globals_list,
    }


# ============================================================
# Phase 4: Compilation
# ============================================================

# Locate compiler directory relative to this package
_COMPILER_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "vcdecomp", "compiler")
)


@mcp.tool()
def scr_compile(source_path: str, output_name: Optional[str] = None) -> dict:
    """Compile a .c script to .scr bytecode using the Vietcong SCMP compiler.

    Args:
        source_path: Path to the .c source file
        output_name: Base name for output files (default: same as source)
    """
    source_path = os.path.abspath(source_path)
    if not os.path.isfile(source_path):
        return {"error": f"Source file not found: {source_path}"}

    compiler_dir = _COMPILER_DIR
    bat_path = os.path.join(compiler_dir, "compile_script.bat")
    if not os.path.isfile(bat_path):
        return {"error": f"compile_script.bat not found in {compiler_dir}"}

    # Determine base name for output
    src_basename = os.path.basename(source_path)
    base = output_name or os.path.splitext(src_basename)[0]
    out_scr = base + ".scr"
    out_h = base + ".h"

    # Copy source into compiler dir if not already there
    compiler_src = os.path.join(compiler_dir, src_basename)
    if os.path.normcase(os.path.abspath(source_path)) != os.path.normcase(compiler_src):
        shutil.copy2(source_path, compiler_src)

    # Clean up old error files and previous output
    for ext in (".err",):
        for prefix in ("spp", "scc", "sasm"):
            err_file = os.path.join(compiler_dir, prefix + ext)
            if os.path.exists(err_file):
                os.remove(err_file)
    scr_out_path = os.path.join(compiler_dir, out_scr)
    if os.path.exists(scr_out_path):
        os.remove(scr_out_path)

    # Run the compiler via cmd.exe /c
    try:
        result = subprocess.run(
            [os.path.join(compiler_dir, "compile_script.bat"),
             src_basename, out_scr, out_h],
            cwd=compiler_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return {"error": "Compilation timed out after 30 seconds"}

    # Check for error files
    errors = {}
    for prefix in ("spp", "scc", "sasm"):
        err_file = os.path.join(compiler_dir, prefix + ".err")
        if os.path.isfile(err_file):
            content = open(err_file, "r", errors="replace").read().strip()
            if content:
                errors[prefix] = content

    if errors:
        return {
            "status": "error",
            "errors": errors,
            "stdout": result.stdout.strip() if result.stdout else "",
            "stderr": result.stderr.strip() if result.stderr else "",
        }

    # Check for output
    if os.path.isfile(scr_out_path):
        size = os.path.getsize(scr_out_path)
        return {
            "status": "ok",
            "output_path": scr_out_path,
            "output_size": size,
            "stdout": result.stdout.strip() if result.stdout else "",
        }

    # Neither errors nor output — generic failure
    return {
        "status": "error",
        "error": "Compilation produced no output and no error files",
        "returncode": result.returncode,
        "stdout": result.stdout.strip() if result.stdout else "",
        "stderr": result.stderr.strip() if result.stderr else "",
    }
