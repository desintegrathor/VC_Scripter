"""
Symbol Table Exporter for Vietcong Script Decompiler.

Exports global variable symbol table to various formats:
- JSON (structured data with all metadata)
- C Header (extern declarations and #define)
- Markdown (human-readable documentation)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from pathlib import Path

from .global_resolver import GlobalUsage
from ..loader.scr_loader import SCRFile


@dataclass
class SymbolTableEntry:
    """Single symbol table entry for export."""

    offset: int
    """Data segment offset"""

    name: str
    """Variable name"""

    type: str
    """Inferred C type"""

    size: Optional[int] = None
    """Size in bytes (if known)"""

    # Usage statistics
    read_count: int = 0
    write_count: int = 0
    functions_used: List[str] = None

    # Classification
    is_array: bool = False
    is_struct: bool = False
    is_pointer: bool = False

    # Header mapping
    sgi_index: Optional[int] = None
    sgi_name: Optional[str] = None

    # Struct info (if applicable)
    struct_typedef: Optional[str] = None
    fields: Optional[List[Dict]] = None

    # Type confidence
    type_confidence: float = 0.0

    def __post_init__(self):
        if self.functions_used is None:
            self.functions_used = []
        if self.fields is None:
            self.fields = []

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            "offset": self.offset,
            "name": self.name,
            "type": self.type,
            "size": self.size,
            "read_count": self.read_count,
            "write_count": self.write_count,
            "functions_used": self.functions_used,
            "is_array": self.is_array,
            "is_struct": self.is_struct,
            "is_pointer": self.is_pointer,
            "sgi_index": self.sgi_index,
            "sgi_name": self.sgi_name,
            "struct_typedef": self.struct_typedef,
            "fields": self.fields,
            "type_confidence": self.type_confidence
        }

    @staticmethod
    def from_global_usage(usage: GlobalUsage) -> "SymbolTableEntry":
        """
        Create SymbolTableEntry from GlobalUsage.

        Args:
            usage: GlobalUsage object from global_resolver

        Returns:
            SymbolTableEntry
        """
        # Determine type
        var_type = usage.inferred_type or "int"

        # Determine size
        size = None
        if usage.inferred_struct and hasattr(usage.inferred_struct, 'total_size'):
            size = usage.inferred_struct.total_size
        elif usage.array_element_size:
            size = usage.array_element_size
        else:
            # Guess from type
            type_sizes = {
                'char': 1, 'short': 2, 'int': 4, 'float': 4,
                'double': 8, 'void*': 4, 'char*': 4
            }
            size = type_sizes.get(var_type, 4)

        # Extract field info if struct
        fields = None
        if usage.inferred_struct and hasattr(usage.inferred_struct, 'fields'):
            fields = []
            for field in usage.inferred_struct.fields:
                fields.append({
                    "offset": field.offset,
                    "type": field.inferred_type or "int",
                    "size": field.inferred_size,
                    "access_count": field.access_count
                })

        return SymbolTableEntry(
            offset=usage.offset,
            name=usage.name or f"global_{usage.offset}",
            type=var_type,
            size=size,
            read_count=usage.read_count,
            write_count=usage.write_count,
            functions_used=list(usage.functions_used),
            is_array=usage.is_array_base,
            is_struct=usage.is_struct_base,
            is_pointer="*" in var_type,
            sgi_index=usage.sgi_index,
            sgi_name=usage.sgi_name,
            struct_typedef=usage.struct_typedef,
            fields=fields,
            type_confidence=usage.type_confidence
        )


class SymbolTableExporter:
    """Exports symbol table to various formats."""

    def __init__(self, globals_usage: Dict[int, GlobalUsage], scr: SCRFile):
        """
        Initialize exporter.

        Args:
            globals_usage: Dict of GlobalUsage from global_resolver
            scr: Loaded SCR file
        """
        self.globals = globals_usage
        self.scr = scr

    def export_to_json(self, output_path: Path) -> None:
        """
        Export to JSON file.

        Args:
            output_path: Path to output JSON file
        """
        # Convert all globals to SymbolTableEntry
        entries = []
        for usage in self.globals.values():
            entry = SymbolTableEntry.from_global_usage(usage)
            entries.append(entry.to_dict())

        # Sort by offset
        entries.sort(key=lambda e: e["offset"])

        # Create output data
        data = {
            "file": str(self.scr.file_path) if hasattr(self.scr, 'file_path') else "unknown",
            "data_segment_size": self.scr.data_segment.size_bytes if self.scr.data_segment else 0,
            "global_count": len(self.globals),
            "symbols": entries,
            "statistics": {
                "total_reads": sum(e["read_count"] for e in entries),
                "total_writes": sum(e["write_count"] for e in entries),
                "sgi_mapped": sum(1 for e in entries if e["sgi_name"]),
                "structs_detected": sum(1 for e in entries if e["is_struct"]),
                "arrays_detected": sum(1 for e in entries if e["is_array"]),
            }
        }

        # Write to file
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def export_to_c_header(self, output_path: Path) -> None:
        """
        Generate C header with extern declarations.

        Args:
            output_path: Path to output .h file
        """
        lines = []

        # Header guard
        guard_name = f"__{output_path.stem.upper()}_H__"
        lines.append(f"#ifndef {guard_name}")
        lines.append(f"#define {guard_name}")
        lines.append("")
        lines.append("// Auto-generated global variable declarations")
        lines.append(f"// Source: {self.scr.file_path if hasattr(self.scr, 'file_path') else 'unknown'}")
        lines.append("")

        # Struct typedefs
        structs_added = set()
        for usage in sorted(self.globals.values(), key=lambda u: u.offset):
            if usage.struct_typedef and usage.struct_typedef not in structs_added:
                lines.append(usage.struct_typedef)
                lines.append("")
                structs_added.add(usage.struct_typedef)

        lines.append("// Global variable declarations")
        lines.append("")

        # Extern declarations
        for usage in sorted(self.globals.values(), key=lambda u: u.offset):
            if not usage.name:
                continue

            var_type = usage.inferred_type or "int"
            var_name = usage.name

            # Add comment with metadata
            comment = f"// Offset 0x{usage.offset:04X}"
            if usage.sgi_index:
                comment += f", SGI index {usage.sgi_index}"
            if usage.read_count or usage.write_count:
                comment += f", R:{usage.read_count} W:{usage.write_count}"

            lines.append(comment)

            # Array declaration
            if usage.array_dimensions:
                dim_suffix = "".join(f"[{dim}]" for dim in usage.array_dimensions)
                lines.append(f"extern {var_type} {var_name}{dim_suffix};")
            elif usage.is_array_base and usage.array_element_size:
                # Try to estimate array size
                array_size = 10  # Default guess
                lines.append(f"extern {var_type} {var_name}[{array_size}];")
            else:
                lines.append(f"extern {var_type} {var_name};")

            lines.append("")

        # Close header guard
        lines.append(f"#endif // {guard_name}")

        # Write to file
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def export_to_markdown(self, output_path: Path) -> None:
        """
        Generate Markdown documentation.

        Args:
            output_path: Path to output .md file
        """
        lines = []
        lines.append("# Global Variable Symbol Table")
        lines.append("")
        lines.append(f"**Source:** `{self.scr.file_path if hasattr(self.scr, 'file_path') else 'unknown'}`")
        lines.append("")

        # Statistics
        total_reads = sum(u.read_count for u in self.globals.values())
        total_writes = sum(u.write_count for u in self.globals.values())
        sgi_mapped = sum(1 for u in self.globals.values() if u.sgi_name)
        structs = sum(1 for u in self.globals.values() if u.is_struct_base)
        arrays = sum(1 for u in self.globals.values() if u.is_array_base)

        lines.append("## Statistics")
        lines.append("")
        lines.append(f"- **Total globals:** {len(self.globals)}")
        lines.append(f"- **Total reads:** {total_reads}")
        lines.append(f"- **Total writes:** {total_writes}")
        lines.append(f"- **SGI mapped:** {sgi_mapped}")
        lines.append(f"- **Structs detected:** {structs}")
        lines.append(f"- **Arrays detected:** {arrays}")
        lines.append("")

        # Table of all globals
        lines.append("## Global Variables")
        lines.append("")
        lines.append("| Offset | Name | Type | Size | R/W | SGI | Notes |")
        lines.append("|--------|------|------|------|-----|-----|-------|")

        for usage in sorted(self.globals.values(), key=lambda u: u.offset):
            if not usage.name:
                continue

            offset_str = f"0x{usage.offset:04X}"
            name_str = usage.name
            type_str = usage.inferred_type or "int"
            size_str = str(usage.inferred_struct.total_size if usage.inferred_struct and hasattr(usage.inferred_struct, 'total_size') else 4)
            rw_str = f"{usage.read_count}/{usage.write_count}"
            sgi_str = str(usage.sgi_index) if usage.sgi_index else "-"

            notes = []
            if usage.is_array_base:
                notes.append("Array")
            if usage.is_struct_base:
                notes.append("Struct")
            if usage.type_confidence > 0.8:
                notes.append(f"Type: {usage.type_confidence:.0%}")

            notes_str = ", ".join(notes) if notes else "-"

            lines.append(f"| {offset_str} | `{name_str}` | {type_str} | {size_str} | {rw_str} | {sgi_str} | {notes_str} |")

        # Struct definitions
        if any(u.struct_typedef for u in self.globals.values()):
            lines.append("")
            lines.append("## Detected Structures")
            lines.append("")

            for usage in sorted(self.globals.values(), key=lambda u: u.offset):
                if usage.struct_typedef:
                    lines.append(f"### {usage.name} (offset 0x{usage.offset:04X})")
                    lines.append("")
                    lines.append("```c")
                    lines.append(usage.struct_typedef)
                    lines.append("```")
                    lines.append("")

        # Write to file
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


def export_symbol_table(
    globals_usage: Dict[int, GlobalUsage],
    scr: SCRFile,
    output_path: Path,
    format: str = 'json'
) -> None:
    """
    Convenience function to export symbol table.

    Args:
        globals_usage: Dict of GlobalUsage from global_resolver
        scr: Loaded SCR file
        output_path: Path to output file
        format: Export format ('json', 'header', 'markdown')
    """
    exporter = SymbolTableExporter(globals_usage, scr)

    if format == 'json':
        exporter.export_to_json(output_path)
    elif format == 'header':
        exporter.export_to_c_header(output_path)
    elif format == 'markdown':
        exporter.export_to_markdown(output_path)
    else:
        raise ValueError(f"Unknown format: {format}")
