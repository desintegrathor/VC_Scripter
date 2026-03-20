"""SCRSession: cached decompiler pipeline state with lazy per-function decompilation."""

from __future__ import annotations

import json
import os
import re
import struct
from argparse import Namespace
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


def _default_args() -> Namespace:
    """Create a synthetic argparse.Namespace with sensible defaults."""
    return Namespace(
        variant='auto',
        debug=False,
        verbose=False,
        legacy_ssa=False,
        no_simplify=False,
        debug_simplify=False,
        no_array_detection=False,
        debug_array_detection=False,
        no_bidirectional_types=False,
        debug_type_inference=False,
        no_collapse=False,
        header=None,
        ignore_mp=False,
    )


@dataclass
class SCRSession:
    """Holds all cached pipeline state for an open .scr file."""

    handle: str
    path: str
    scr: object  # SCRFile
    disasm: object  # Disassembler
    func_bounds: Dict[str, Tuple[int, int]]
    ssa_func: object  # SSAFunction
    heritage_metadata: Optional[Dict]
    globals_usage: Dict  # offset -> GlobalUsage
    float_globals: Set[int]
    array_strides: Dict[int, Set[int]]
    saveinfo_sizes: Dict[int, int] = field(default_factory=dict)

    # Lazy caches (invalidated on mutation)
    _decompiled: Dict[str, str] = field(default_factory=dict)

    # User overrides
    func_renames: Dict[str, str] = field(default_factory=dict)
    global_renames: Dict[int, str] = field(default_factory=dict)
    local_renames: Dict[str, Dict[str, str]] = field(default_factory=dict)
    type_overrides: Dict[str, str] = field(default_factory=dict)
    comments: Dict[int, str] = field(default_factory=dict)

    @classmethod
    def open(cls, path: str, handle: str = "") -> 'SCRSession':
        """Run the cheap part of the pipeline and cache everything."""
        from vcdecomp.core.loader import SCRFile
        from vcdecomp.core.disasm import Disassembler
        from vcdecomp.core.ir.ssa import build_ssa_incremental
        from vcdecomp.core.ir.global_resolver import GlobalResolver
        from vcdecomp.core.ir.decompile_file import (
            _detect_float_globals, _detect_array_strides, resolve_mission_header,
        )
        from vcdecomp.core.ir.debug_output import set_debug_enabled

        set_debug_enabled(False)

        # Load binary
        scr = SCRFile.load(str(path), variant='auto')
        scr.enable_simplify = True
        scr.debug_simplify = False
        scr.enable_array_detection = True
        scr.debug_array_detection = False
        scr.enable_bidirectional_types = True
        scr.debug_type_inference = False

        # Function detection
        disasm = Disassembler(scr)
        func_bounds = disasm.get_function_boundaries_v2()

        # Mission header auto-detection
        scr_dir = Path(path).parent
        header_path = resolve_mission_header(scr_dir)
        if header_path:
            from vcdecomp.core.headers.database import get_header_database
            from vcdecomp.core.constants import _reset_constants
            hdb = get_header_database()
            hdb.load_mission_header(header_path)
            _reset_constants()

            from vcdecomp.core.ir.function_detector import match_header_functions
            header_source = header_path.read_text(encoding='latin-1')
            rename_map = match_header_functions(
                scr, func_bounds, hdb.mission_functions, header_source
            )
            scr._header_function_signatures = {}
            for old_name, new_info in rename_map.items():
                scr._header_function_signatures[new_info['name']] = new_info
                if old_name in func_bounds:
                    func_bounds[new_info['name']] = func_bounds.pop(old_name)

        # Build SSA
        ssa_func, heritage_metadata = build_ssa_incremental(scr, return_metadata=True)

        # Float/array analysis
        float_globals = _detect_float_globals(ssa_func)
        array_strides = _detect_array_strides(ssa_func, scr)

        # Global resolution
        resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
        globals_usage = resolver.analyze()
        ssa_func._cached_global_type_info_bytes = globals_usage

        # SaveInfo sizes
        saveinfo_sizes = {}
        if scr.save_info:
            for item in scr.save_info.items:
                byte_offset = item['val1'] * 4
                size_dwords = item['val2']
                saveinfo_sizes[byte_offset] = size_dwords

        if not handle:
            handle = _make_handle_from_path(path)

        session = cls(
            handle=handle,
            path=str(path),
            scr=scr,
            disasm=disasm,
            func_bounds=func_bounds,
            ssa_func=ssa_func,
            heritage_metadata=heritage_metadata,
            globals_usage=globals_usage,
            float_globals=float_globals,
            array_strides=array_strides,
            saveinfo_sizes=saveinfo_sizes,
        )

        # Load persisted annotations from .vcdb sidecar if it exists
        session.load_session()

        return session

    def decompile_func(self, func_name: str) -> str:
        """Decompile a single function, with caching and override application."""
        # Resolve renamed functions
        actual_name = func_name
        for old, new in self.func_renames.items():
            if new == func_name:
                actual_name = old
                break

        if actual_name not in self.func_bounds:
            # Try the name as-is (maybe it wasn't renamed)
            if func_name not in self.func_bounds:
                raise ValueError(f"Function '{func_name}' not found")
            actual_name = func_name

        cache_key = func_name
        if cache_key in self._decompiled:
            return self._decompiled[cache_key]

        from vcdecomp.core.ir.structure import format_structured_function_named

        func_start, func_end = self.func_bounds[actual_name]
        text = format_structured_function_named(
            self.ssa_func,
            actual_name,
            func_start,
            func_end,
            function_bounds=self.func_bounds,
            style='quiet',
            heritage_metadata=self.heritage_metadata,
            use_collapse=True,
        )

        # Apply overrides
        text = self._apply_overrides(text, actual_name)

        self._decompiled[cache_key] = text
        return text

    def get_disasm_func(self, func_name: str) -> str:
        """Get disassembly text for a single function."""
        actual_name = self._resolve_func_name(func_name)
        if actual_name not in self.func_bounds:
            raise ValueError(f"Function '{func_name}' not found")

        func_start, func_end = self.func_bounds[actual_name]
        lines = []
        for instr in self.scr.code_segment.instructions[func_start:func_end + 1]:
            dl = self.disasm.disassemble_instruction(instr)
            lines.append(str(dl))
        return "\n".join(lines)

    def get_disasm_range(self, addr: int, count: int = 20) -> str:
        """Get disassembly text for an address range."""
        lines = []
        instrs = self.scr.code_segment.instructions
        end = min(addr + count, len(instrs))
        for instr in instrs[addr:end]:
            dl = self.disasm.disassemble_instruction(instr)
            lines.append(str(dl))
        return "\n".join(lines)

    def get_data_value(self, offset: int, type_name: str = "int", count: int = 1) -> list:
        """Read typed value(s) from data segment."""
        ds = self.scr.data_segment
        results = []
        for i in range(count):
            off = offset + i * _type_size(type_name)
            if type_name == "string":
                s = ds.get_string(off)
                if s is None:
                    # Try to read raw null-terminated string
                    s = _read_cstring(ds.raw_data, off)
                results.append(s)
                break  # strings are variable-length
            elif type_name == "float":
                results.append(ds.get_float(off))
            elif type_name == "bytes":
                end = min(off + count, len(ds.raw_data))
                results.append(list(ds.raw_data[off:end]))
                break
            else:  # int/dword
                results.append(ds.get_dword(off))
        return results

    def get_strings(self, filter_pattern: str = "") -> List[dict]:
        """Get all strings in data segment."""
        strings = []
        for offset, s in sorted(self.scr.data_strings.items()):
            if filter_pattern and filter_pattern.lower() not in s.lower():
                continue
            strings.append({"offset": offset, "value": s})
        return strings

    def get_globals_list(self, filter_pattern: str = "") -> List[dict]:
        """Get resolved global variables."""
        results = []
        for offset in sorted(self.globals_usage.keys()):
            usage = self.globals_usage[offset]
            if usage.is_array_element:
                continue
            if usage.write_count == 0 and not usage.name.startswith("g"):
                continue
            if usage.source in ("SGI_constant", "SGI_runtime"):
                continue

            name = self.global_renames.get(offset, usage.name or f"data_{offset}")
            var_type = self._resolve_global_type(offset, usage)

            info = {
                "offset": offset,
                "name": name,
                "type": var_type,
                "reads": usage.read_count,
                "writes": usage.write_count,
            }

            # Initializer
            if var_type == "float" and self.scr.data_segment:
                raw = self.scr.data_segment.get_dword(offset)
                fval = struct.unpack('<f', struct.pack('<I', raw & 0xFFFFFFFF))[0]
                info["initializer"] = fval
            elif usage.initializer:
                info["initializer"] = usage.initializer

            # Array info
            size_dwords = self.saveinfo_sizes.get(offset, 1)
            if size_dwords > 1 or (usage.is_array_base and usage.array_element_size):
                info["is_array"] = True
                if usage.array_dimensions:
                    info["dimensions"] = usage.array_dimensions
                info["size_dwords"] = size_dwords

            if filter_pattern and filter_pattern.lower() not in name.lower():
                continue
            results.append(info)
        return results

    def rename(self, target_type: str, old_name: str, new_name: str,
               func_context: str = "") -> dict:
        """Rename a function, global, or local variable."""
        if target_type == "function":
            if old_name not in self.func_bounds:
                return {"error": f"Function '{old_name}' not found"}
            self.func_renames[old_name] = new_name
            # Update func_bounds key
            self.func_bounds[new_name] = self.func_bounds.pop(old_name)
            self._decompiled.clear()
            # Invalidate block-to-func cache
            if hasattr(self, '_block_to_func_cache'):
                del self._block_to_func_cache
            self._auto_save()
            return {"status": "ok", "old": old_name, "new": new_name}
        elif target_type == "global":
            # Find by name
            offset = None
            for off, usage in self.globals_usage.items():
                current_name = self.global_renames.get(off, usage.name)
                if current_name == old_name:
                    offset = off
                    break
            if offset is None:
                return {"error": f"Global '{old_name}' not found"}
            self.global_renames[offset] = new_name
            self._decompiled.clear()
            self._auto_save()
            return {"status": "ok", "old": old_name, "new": new_name, "offset": offset}
        elif target_type == "local":
            if not func_context:
                return {"error": "func_context required for local renames"}
            if func_context not in self.local_renames:
                self.local_renames[func_context] = {}
            self.local_renames[func_context][old_name] = new_name
            self._decompiled.pop(func_context, None)
            self._auto_save()
            return {"status": "ok", "func": func_context, "old": old_name, "new": new_name}
        return {"error": f"Unknown target_type '{target_type}'"}

    def set_type(self, target: str, new_type: str) -> dict:
        """Override type of a global or local variable.

        target format: "global:<name>" or "local:<func>:<name>"
        """
        self.type_overrides[target] = new_type
        # Invalidate relevant caches
        if target.startswith("local:"):
            parts = target.split(":", 2)
            if len(parts) >= 2:
                self._decompiled.pop(parts[1], None)
        else:
            # Patch GlobalUsage so decompiler sees the new type
            self._apply_type_overrides_to_globals()
            self._decompiled.clear()
        self._auto_save()
        return {"status": "ok", "target": target, "type": new_type}

    def get_xrefs_to(self, target: str) -> List[dict]:
        """Find all references to a global, function, or XFN.

        target: global name, function name, or "xfn:<name>"
        """
        results = []
        is_xfn = target.startswith("xfn:")
        xfn_name = target[4:] if is_xfn else None

        # Find target offset for globals
        target_offset = None
        if not is_xfn and target not in self.func_bounds:
            for off, usage in self.globals_usage.items():
                name = self.global_renames.get(off, usage.name)
                if name == target:
                    target_offset = off
                    break

        # Build block_id -> func_name mapping
        block_to_func = self._build_block_to_func_map()

        for block_id, instrs in self.ssa_func.instructions.items():
            func_name = block_to_func.get(block_id)
            if not func_name:
                continue
            for inst in instrs:
                matched = False
                if is_xfn and inst.mnemonic == "XCALL":
                    if inst.instruction and inst.instruction.instruction:
                        xfn_idx = inst.instruction.instruction.arg1
                        xfn_entry = self.scr.get_xfn(xfn_idx)
                        if xfn_entry:
                            entry_name = xfn_entry.name.split("(")[0]
                            if xfn_name == entry_name or xfn_name in entry_name:
                                matched = True
                elif target in self.func_bounds and inst.mnemonic == "CALL":
                    if inst.instruction and inst.instruction.instruction:
                        call_target = inst.instruction.instruction.arg1
                        if call_target == self.func_bounds[target][0]:
                            matched = True
                elif target_offset is not None:
                    for val in list(inst.inputs) + list(inst.outputs):
                        if val.alias:
                            if val.alias == f"data_{target_offset // 4}":
                                matched = True
                                break
                            if val.alias == f"&data_{target_offset // 4}":
                                matched = True
                                break
                if matched:
                    results.append({
                        "func": func_name,
                        "addr": inst.address,
                        "mnemonic": inst.mnemonic,
                    })
        return results

    def get_callees(self, func_name: str) -> dict:
        """List functions/XFNs called by a function."""
        actual_name = self._resolve_func_name(func_name)
        if actual_name not in self.func_bounds:
            raise ValueError(f"Function '{func_name}' not found")

        block_to_func = self._build_block_to_func_map()
        calls = []
        xcalls = []

        for block_id, instrs in self.ssa_func.instructions.items():
            if block_to_func.get(block_id) != actual_name:
                continue
            for inst in instrs:
                if inst.mnemonic == "CALL" and inst.instruction and inst.instruction.instruction:
                    target_addr = inst.instruction.instruction.arg1
                    # Find function name by address
                    for fn, (fs, _fe) in self.func_bounds.items():
                        if fs == target_addr:
                            calls.append(fn)
                            break
                elif inst.mnemonic == "XCALL" and inst.instruction and inst.instruction.instruction:
                    xfn_idx = inst.instruction.instruction.arg1
                    xfn_entry = self.scr.get_xfn(xfn_idx)
                    if xfn_entry:
                        # Extract just the function name (before the '(' signature)
                        xfn_name = xfn_entry.name.split("(")[0]
                        xcalls.append(xfn_name)

        return {"calls": sorted(set(calls)), "xcalls": sorted(set(xcalls))}

    def get_basic_blocks(self, func_name: str) -> List[dict]:
        """Get CFG basic blocks for a function."""
        actual_name = self._resolve_func_name(func_name)
        if actual_name not in self.func_bounds:
            raise ValueError(f"Function '{func_name}' not found")

        block_to_func = self._build_block_to_func_map()
        blocks = []
        cfg = self.ssa_func.cfg

        for block_id, block in cfg.blocks.items():
            if block_to_func.get(block_id) != actual_name:
                continue
            blocks.append({
                "id": block.start,
                "start": block.start,
                "end": block.end,
                "successors": [s if isinstance(s, int) else s.start for s in block.successors],
                "predecessors": [p if isinstance(p, int) else p.start for p in block.predecessors],
                "instruction_count": block.end - block.start + 1,
            })

        return sorted(blocks, key=lambda b: b["start"])

    def search(self, query: str, search_in: str = "all") -> List[dict]:
        """Search for strings, immediates, or data refs in code/data.

        search_in: "code", "data", "all"
        """
        results = []

        # Search in strings
        if search_in in ("data", "all"):
            for offset, s in self.scr.data_strings.items():
                if query.lower() in s.lower():
                    results.append({
                        "type": "string",
                        "offset": offset,
                        "value": s,
                    })

        # Search in code (instruction immediates and XFN names)
        if search_in in ("code", "all"):
            # Try to parse as integer
            try:
                int_query = int(query, 0)
                for instr in self.scr.code_segment.instructions:
                    if instr.arg1 == int_query or instr.arg2 == int_query:
                        results.append({
                            "type": "immediate",
                            "addr": instr.address,
                            "mnemonic": self.scr.opcode_resolver.get_mnemonic(instr.opcode),
                        })
            except ValueError:
                pass

            # Search XFN names
            for entry in self.scr.xfn_table.entries:
                if query.lower() in entry.name.lower():
                    results.append({
                        "type": "xfn",
                        "index": entry.index,
                        "name": entry.name,
                    })

        return results

    def get_callgraph(self, root_funcs: Optional[List[str]] = None,
                      max_depth: int = 10) -> dict:
        """Build recursive call graph from root functions."""
        if root_funcs is None:
            # Default: all functions
            root_funcs = list(self.func_bounds.keys())

        nodes = {}
        edges = []
        visited = set()

        def _walk(func_name: str, depth: int):
            if func_name in visited or depth > max_depth:
                return
            visited.add(func_name)
            if func_name not in self.func_bounds:
                return
            fstart = self.func_bounds[func_name][0]
            nodes[func_name] = {"name": func_name, "start": fstart}

            callees = self.get_callees(func_name)
            for callee in callees["calls"]:
                edges.append({"from": func_name, "to": callee, "type": "call"})
                _walk(callee, depth + 1)
            for xcall in callees["xcalls"]:
                edges.append({"from": func_name, "to": xcall, "type": "xcall"})
                nodes.setdefault(xcall, {"name": xcall, "start": -1})

        for root in root_funcs:
            actual = self._resolve_func_name(root)
            _walk(actual, 0)

        return {
            "nodes": list(nodes.values()),
            "edges": edges,
            "node_count": len(nodes),
            "edge_count": len(edges),
        }

    def read_struct(self, offset: int, struct_name: str) -> dict:
        """Interpret a data segment region as an SDK struct."""
        from vcdecomp.core.structures import get_struct_by_name

        struct_def = get_struct_by_name(struct_name)
        if not struct_def:
            return {"error": f"Struct '{struct_name}' not found"}

        ds = self.scr.data_segment
        fields = []
        for f in struct_def.fields:
            field_offset = offset + f.offset
            # Read value based on type
            if "float" in f.type_name:
                value = ds.get_float(field_offset)
            elif "char" in f.type_name and (f.is_array or f.is_pointer):
                value = _read_cstring(ds.raw_data, field_offset)
            elif f.is_array and not f.is_pointer:
                count = f.array_count
                values = []
                elem_size = f.size
                for i in range(min(count, 32)):  # cap at 32 elements
                    values.append(ds.get_dword(field_offset + i * elem_size))
                value = values
            else:
                value = ds.get_dword(field_offset)

            fields.append({
                "name": f.name,
                "type": f.type_name,
                "offset": f.offset,
                "abs_offset": field_offset,
                "value": value,
            })

        return {
            "struct": struct_name,
            "offset": offset,
            "size": struct_def.size,
            "field_count": len(fields),
            "fields": fields,
        }

    def get_ssa_form(self, func_name: str) -> dict:
        """View SSA form for a function."""
        actual_name = self._resolve_func_name(func_name)
        if actual_name not in self.func_bounds:
            raise ValueError(f"Function '{func_name}' not found")

        block_to_func = self._build_block_to_func_map()
        cfg = self.ssa_func.cfg
        blocks = []

        for block_id in sorted(self.ssa_func.instructions.keys()):
            if block_to_func.get(block_id) != actual_name:
                continue
            block = cfg.blocks.get(block_id)
            instrs = self.ssa_func.instructions[block_id]
            formatted_instrs = []
            for inst in instrs:
                inputs = []
                for v in inst.inputs:
                    inputs.append({"name": v.name, "alias": v.alias})
                outputs = []
                for v in inst.outputs:
                    if v is not None:
                        outputs.append({"name": v.name, "alias": v.alias})
                formatted_instrs.append({
                    "addr": inst.address,
                    "mnemonic": inst.mnemonic,
                    "inputs": inputs,
                    "outputs": outputs,
                })
            blocks.append({
                "id": block_id,
                "start": block.start if block else block_id,
                "end": block.end if block else block_id,
                "instructions": formatted_instrs,
            })

        return {"func": func_name, "block_count": len(blocks), "blocks": blocks}

    def get_stack_frame(self, func_name: str) -> dict:
        """View stack frame layout for a function."""
        actual_name = self._resolve_func_name(func_name)
        if actual_name not in self.func_bounds:
            raise ValueError(f"Function '{func_name}' not found")

        block_to_func = self._build_block_to_func_map()
        frame_accesses: Dict[int, dict] = {}  # offset -> info

        for block_id, instrs in self.ssa_func.instructions.items():
            if block_to_func.get(block_id) != actual_name:
                continue
            for inst in instrs:
                if inst.mnemonic not in ("LCP", "SSP", "LADR"):
                    continue
                if not inst.instruction or not inst.instruction.instruction:
                    continue
                offset = inst.instruction.instruction.arg1
                if offset not in frame_accesses:
                    frame_accesses[offset] = {
                        "offset": offset,
                        "reads": 0,
                        "writes": 0,
                        "alias": None,
                    }
                if inst.mnemonic in ("LCP", "LADR"):
                    frame_accesses[offset]["reads"] += 1
                elif inst.mnemonic == "SSP":
                    frame_accesses[offset]["writes"] += 1
                # Capture alias from outputs/inputs
                for v in inst.outputs:
                    if v and v.alias:
                        frame_accesses[offset]["alias"] = v.alias

        # Separate params (negative offsets or first N slots) from locals
        params = []
        locals_list = []
        for offset in sorted(frame_accesses.keys()):
            info = frame_accesses[offset]
            if offset < 0:
                params.append(info)
            else:
                locals_list.append(info)

        return {
            "func": func_name,
            "param_count": len(params),
            "local_count": len(locals_list),
            "params": params,
            "locals": locals_list,
        }

    # --- Private helpers ---

    def _build_block_to_func_map(self) -> Dict[int, str]:
        """Map CFG block IDs to function names using block start addresses."""
        if hasattr(self, '_block_to_func_cache'):
            return self._block_to_func_cache
        import bisect
        # Build sorted list of (func_start, func_end, func_name) for bisect lookup
        sorted_funcs = sorted(
            [(fstart, fend, fname) for fname, (fstart, fend) in self.func_bounds.items()]
        )
        starts = [f[0] for f in sorted_funcs]

        cfg = self.ssa_func.cfg
        result = {}
        for block_id, block in cfg.blocks.items():
            idx = bisect.bisect_right(starts, block.start) - 1
            if idx >= 0:
                fstart, fend, fname = sorted_funcs[idx]
                if fstart <= block.start <= fend:
                    result[block_id] = fname
        self._block_to_func_cache = result
        return result

    # ── Session persistence (.vcdb sidecar) ──────────────────────────

    def _vcdb_path(self) -> Path:
        return Path(self.path).with_suffix('.vcdb')

    def save_session(self) -> str:
        """Persist user annotations to .vcdb sidecar file."""
        data = {
            "version": 1,
            "func_renames": self.func_renames,
            "global_renames": {str(k): v for k, v in self.global_renames.items()},
            "local_renames": self.local_renames,
            "type_overrides": self.type_overrides,
            "comments": {str(k): v for k, v in self.comments.items()},
        }
        p = self._vcdb_path()
        p.write_text(json.dumps(data, indent=2), encoding='utf-8')
        return str(p)

    def load_session(self):
        """Load user annotations from .vcdb sidecar if it exists."""
        p = self._vcdb_path()
        if not p.exists():
            return
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            return

        self.func_renames = data.get("func_renames", {})
        self.global_renames = {int(k): v for k, v in data.get("global_renames", {}).items()}
        self.local_renames = data.get("local_renames", {})
        self.type_overrides = data.get("type_overrides", {})
        self.comments = {int(k): v for k, v in data.get("comments", {}).items()}

        # Apply function renames to func_bounds
        for old, new in self.func_renames.items():
            if old in self.func_bounds:
                self.func_bounds[new] = self.func_bounds.pop(old)

        # Apply type overrides to GlobalUsage objects
        self._apply_type_overrides_to_globals()

    def _auto_save(self):
        """Auto-save session state after mutations."""
        try:
            self.save_session()
        except OSError:
            pass  # Best-effort

    def _resolve_func_name(self, name: str) -> str:
        """Resolve a possibly-renamed function name to the actual name in func_bounds."""
        if name in self.func_bounds:
            return name
        # Check if it's a pre-rename name
        for old, new in self.func_renames.items():
            if new == name and new in self.func_bounds:
                return new
        return name

    def _apply_type_overrides_to_globals(self):
        """Patch GlobalUsage entries with user type overrides so the decompiler sees them."""
        from vcdecomp.core.structures import get_struct_by_name

        for target, new_type in self.type_overrides.items():
            if not target.startswith("global:"):
                continue
            var_name = target[7:]  # strip "global:"

            # Find the GlobalUsage by name (checking renames too)
            for offset, usage in self.globals_usage.items():
                current_name = self.global_renames.get(offset, usage.name)
                if current_name == var_name or usage.name == var_name:
                    # Patch the usage object in-place
                    usage.inferred_type = new_type
                    usage.type_confidence = 1.0

                    struct_def = get_struct_by_name(new_type)
                    if struct_def:
                        usage.is_struct_base = True
                    elif new_type == "float":
                        self.float_globals.add(offset)
                    break

    def _resolve_global_type(self, offset: int, usage) -> str:
        """Determine type for a global variable."""
        # Check user override
        override_key = f"global:{usage.name or f'data_{offset}'}"
        if override_key in self.type_overrides:
            return self.type_overrides[override_key]

        if offset in self.float_globals:
            return "float"
        if usage.inferred_type:
            return usage.inferred_type
        if usage.header_type:
            return usage.header_type
        if usage.is_incremented or usage.is_decremented:
            return "int"
        if usage.possible_types:
            return list(usage.possible_types)[0]
        return "dword"

    def _apply_overrides(self, text: str, func_name: str) -> str:
        """Apply user renames and type overrides to rendered C code."""
        # Global renames
        for offset, new_name in self.global_renames.items():
            usage = self.globals_usage.get(offset)
            if usage and usage.name:
                text = re.sub(r'\b' + re.escape(usage.name) + r'\b', new_name, text)

        # Function renames
        for old_name, new_name in self.func_renames.items():
            text = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, text)

        # Local renames
        local_map = self.local_renames.get(func_name, {})
        for old_name, new_name in local_map.items():
            text = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, text)

        # Type overrides — replace type in declarations
        for target, new_type in self.type_overrides.items():
            if target.startswith("global:"):
                var_name = target[7:]
                # Also check renamed name
                display_name = var_name
                for off, rn in self.global_renames.items():
                    usage = self.globals_usage.get(off)
                    if usage and usage.name == var_name:
                        display_name = rn
                        break
                text = re.sub(
                    r'\b(int|float|dword|char|short|double)\s+' + re.escape(display_name) + r'\b',
                    f'{new_type} {display_name}',
                    text,
                )
            elif target.startswith("local:"):
                parts = target.split(":", 2)
                if len(parts) == 3 and parts[1] == func_name:
                    var_name = parts[2]
                    text = re.sub(
                        r'\b(int|float|dword|char|short|double)\s+' + re.escape(var_name) + r'\b',
                        f'{new_type} {var_name}',
                        text,
                    )

        return text


def _make_handle_from_path(path: str) -> str:
    """Generate a handle from a file path."""
    base = os.path.basename(path)
    return os.path.splitext(base)[0].lower()


def _type_size(type_name: str) -> int:
    """Return byte size for a type name."""
    sizes = {"char": 1, "short": 2, "int": 4, "float": 4, "dword": 4, "double": 8}
    return sizes.get(type_name, 4)


def _read_cstring(data: bytes, offset: int) -> Optional[str]:
    """Read a null-terminated string from bytes."""
    if offset >= len(data):
        return None
    end = data.find(b'\x00', offset)
    if end < 0:
        end = len(data)
    try:
        return data[offset:end].decode('latin-1')
    except Exception:
        return None
