"""
Cross-File Context for Multi-File Decompilation

Aggregates global variable evidence across multiple .scr files in the same
mission folder. Scripts in a mission share state via SC_ggi/SC_sgi and a
common LEVEL_H.H header, but never call each other's functions directly.

This module collects naming, typing, and array dimension evidence from each
file's analysis pass and resolves the best name/type for each global variable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Set


@dataclass
class GlobalVarEvidence:
    """Aggregated evidence for one global variable across all scripts."""

    offset: int  # Byte offset in data segment

    # Names from different files: filename -> name
    names: Dict[str, str] = field(default_factory=dict)
    # Best resolved name (set by resolve())
    best_name: Optional[str] = None
    # Source of best name (save_info, SGI_constant, etc.)
    name_source: Optional[str] = None

    # Type evidence counters
    float_evidence: int = 0
    int_evidence: int = 0
    # Best resolved type
    best_type: Optional[str] = None
    # Specific inferred types from files: filename -> type
    inferred_types: Dict[str, str] = field(default_factory=dict)

    # Array info (from save_info or detection)
    saveinfo_size_dwords: Optional[int] = None
    array_element_size: Optional[int] = None
    array_dimensions: Optional[list] = None

    # SGI mapping
    sgi_index: Optional[int] = None
    sgi_name: Optional[str] = None

    # Which files read/write this global
    readers: Set[str] = field(default_factory=set)
    writers: Set[str] = field(default_factory=set)


class CrossFileContext:
    """
    Aggregated cross-file context for a mission folder.

    Built during Pass 1 (analysis) by calling add_file_analysis() for each
    .scr file. After all files are added, call resolve() to pick the best
    name and type for each global variable.

    Used during Pass 2 (decompilation) via get_global_name() and
    get_global_type() lookups.
    """

    def __init__(self):
        self.globals: Dict[int, GlobalVarEvidence] = {}  # byte_offset -> evidence
        self.sgi_mappings: Dict[int, str] = {}  # sgi_index -> constant_name
        self._resolved = False

    def _get_or_create(self, byte_offset: int) -> GlobalVarEvidence:
        if byte_offset not in self.globals:
            self.globals[byte_offset] = GlobalVarEvidence(offset=byte_offset)
        return self.globals[byte_offset]

    def add_file_analysis(
        self,
        filename: str,
        scr,
        globals_usage: Dict[int, object],
        float_globals: Set[int],
    ) -> None:
        """
        Merge one file's analysis results into the cross-file context.

        Args:
            filename: Script filename (e.g., "LEVEL.SCR")
            scr: The loaded SCRFile object
            globals_usage: Dict[byte_offset, GlobalUsage] from GlobalResolver
            float_globals: Set of byte offsets known to be float from opcode evidence
        """
        # Merge global variable info
        for byte_offset, usage in globals_usage.items():
            # Skip read-only constants — they are literal values, not variables
            if usage.source == "read_only_constant":
                continue
            ev = self._get_or_create(byte_offset)

            # Track name if this file has one
            if usage.name and usage.source in ("save_info", "SGI_constant", "SGI_runtime"):
                ev.names[filename] = usage.name
                # save_info names are strongest
                if usage.source == "save_info":
                    if ev.name_source != "save_info":
                        ev.best_name = usage.name
                        ev.name_source = "save_info"
                elif ev.best_name is None:
                    ev.best_name = usage.name
                    ev.name_source = usage.source

            # Track type evidence
            if usage.inferred_type:
                ev.inferred_types[filename] = usage.inferred_type
            if usage.header_type:
                ev.inferred_types.setdefault(filename, usage.header_type)

            # Track reads/writes
            if usage.read_count > 0:
                ev.readers.add(filename)
            if usage.write_count > 0:
                ev.writers.add(filename)

            # Merge array info (prefer larger/more specific)
            if usage.saveinfo_size_dwords:
                if ev.saveinfo_size_dwords is None or usage.saveinfo_size_dwords > ev.saveinfo_size_dwords:
                    ev.saveinfo_size_dwords = usage.saveinfo_size_dwords
            if usage.array_element_size:
                ev.array_element_size = usage.array_element_size
            if usage.array_dimensions:
                ev.array_dimensions = usage.array_dimensions

            # SGI info
            if usage.sgi_index is not None:
                ev.sgi_index = usage.sgi_index
            if usage.sgi_name:
                ev.sgi_name = usage.sgi_name

        # Merge float evidence
        for byte_offset in float_globals:
            ev = self._get_or_create(byte_offset)
            ev.float_evidence += 1

        # Merge save_info directly (for globals not in globals_usage)
        if scr.save_info:
            for item in scr.save_info.items:
                byte_offset = item['val1'] * 4
                size_dwords = item['val2']
                var_name = item['name']

                ev = self._get_or_create(byte_offset)
                if var_name and "save_info" not in (ev.name_source or ""):
                    if byte_offset not in globals_usage or not globals_usage.get(byte_offset):
                        ev.names[filename] = var_name
                        if ev.best_name is None:
                            ev.best_name = var_name
                            ev.name_source = "save_info"
                if ev.saveinfo_size_dwords is None or size_dwords > (ev.saveinfo_size_dwords or 0):
                    ev.saveinfo_size_dwords = size_dwords

    def resolve(self) -> None:
        """
        After all files are added, resolve the best name and type for each
        global variable.
        """
        for byte_offset, ev in self.globals.items():
            # Resolve best name: prefer save_info, then SGI, then most common
            if ev.best_name is None and ev.names:
                # Pick the name that appears most often
                from collections import Counter
                name_counts = Counter(ev.names.values())
                ev.best_name = name_counts.most_common(1)[0][0]
                ev.name_source = "cross_file"

            # SGI name override
            if ev.sgi_name and ev.name_source not in ("save_info",):
                ev.best_name = ev.sgi_name
                ev.name_source = "SGI_constant"

            # Resolve best type
            if ev.float_evidence > 0:
                ev.best_type = "float"
            elif ev.inferred_types:
                # Pick most common inferred type
                from collections import Counter
                type_counts = Counter(ev.inferred_types.values())
                ev.best_type = type_counts.most_common(1)[0][0]
            elif ev.int_evidence > 0:
                ev.best_type = "int"

        self._resolved = True

    def get_global_name(self, byte_offset: int) -> Optional[str]:
        """Get the cross-file resolved name for a global at byte_offset."""
        ev = self.globals.get(byte_offset)
        if ev and ev.best_name:
            return ev.best_name
        return None

    def get_global_name_source(self, byte_offset: int) -> Optional[str]:
        """Get the source of the cross-file resolved name."""
        ev = self.globals.get(byte_offset)
        if ev:
            return ev.name_source
        return None

    def get_global_type(self, byte_offset: int) -> Optional[str]:
        """Get the cross-file resolved type for a global at byte_offset."""
        ev = self.globals.get(byte_offset)
        if ev and ev.best_type:
            return ev.best_type
        return None

    def get_saveinfo_size(self, byte_offset: int) -> Optional[int]:
        """Get the cross-file save_info size in dwords."""
        ev = self.globals.get(byte_offset)
        if ev:
            return ev.saveinfo_size_dwords
        return None

    def get_array_dimensions(self, byte_offset: int) -> Optional[list]:
        """Get the cross-file array dimensions."""
        ev = self.globals.get(byte_offset)
        if ev:
            return ev.array_dimensions
        return None

    def get_array_element_size(self, byte_offset: int) -> Optional[int]:
        """Get the cross-file array element size."""
        ev = self.globals.get(byte_offset)
        if ev:
            return ev.array_element_size
        return None

    def summary(self) -> str:
        """Return a human-readable summary of the cross-file context."""
        named = sum(1 for ev in self.globals.values() if ev.best_name)
        typed = sum(1 for ev in self.globals.values() if ev.best_type)
        multi_file = sum(1 for ev in self.globals.values()
                         if len(ev.readers) + len(ev.writers) > 1)
        return (
            f"CrossFileContext: {len(self.globals)} globals, "
            f"{named} named, {typed} typed, {multi_file} used in multiple files"
        )
