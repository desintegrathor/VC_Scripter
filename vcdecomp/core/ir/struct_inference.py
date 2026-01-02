"""
Struct Inference Engine for Vietcong Script Decompiler.

Reconstructs structure definitions from access patterns:
1. Tracks all offset-based accesses (DADR, PNT)
2. Detects alignment/stride patterns (4, 8, 16 bytes)
3. Matches against known structs from headers
4. Generates typedef for unknown structs
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from collections import defaultdict

from .ssa import SSAFunction, SSAInstruction


@dataclass
class FieldAccessPattern:
    """Tracked access to a field offset."""

    offset: int
    """Byte offset from structure base"""

    access_count: int = 0
    """Total number of accesses"""

    read_count: int = 0
    """Number of read accesses"""

    write_count: int = 0
    """Number of write accesses"""

    inferred_size: int = 4
    """Inferred field size in bytes (1, 2, 4, 8)"""

    inferred_type: Optional[str] = None
    """Inferred C type (int, float, char*, etc.)"""


@dataclass
class InferredStruct:
    """Reconstructed structure definition."""

    base_global: int
    """Data segment offset of structure base"""

    total_size: int
    """Total structure size in bytes"""

    fields: List[FieldAccessPattern] = field(default_factory=list)
    """List of detected fields"""

    possible_known_match: Optional[str] = None
    """Name of known struct if matched"""

    confidence: float = 0.0
    """Confidence score (0.0-1.0)"""

    def to_typedef(self, name: str = "UnknownStruct") -> str:
        """
        Generate C typedef for this structure.

        Args:
            name: Structure name

        Returns:
            C typedef string
        """
        if not self.fields:
            return f"// Empty struct at 0x{self.base_global:X}\n"

        lines = [f"typedef struct {{"]

        # Sort fields by offset
        sorted_fields = sorted(self.fields, key=lambda f: f.offset)

        for i, fld in enumerate(sorted_fields):
            field_type = fld.inferred_type or "int"
            field_name = f"field_{fld.offset}"

            # Add padding if needed
            if i > 0:
                prev_field = sorted_fields[i - 1]
                expected_offset = prev_field.offset + prev_field.inferred_size
                if fld.offset > expected_offset:
                    padding_size = fld.offset - expected_offset
                    lines.append(f"    char padding_{prev_field.offset}[{padding_size}];")

            lines.append(f"    {field_type} {field_name};  // offset {fld.offset}, size {fld.inferred_size}")

        lines.append(f"}} {name};  // Total size: {self.total_size} bytes")

        return "\n".join(lines)


class StructInferenceEngine:
    """
    Infers struct definitions from access patterns.

    Analyzes DADR/PNT instructions to detect offset-based accesses
    and reconstructs probable structure layouts.
    """

    def __init__(self, ssa_func: SSAFunction):
        """
        Initialize struct inference engine.

        Args:
            ssa_func: SSA function to analyze
        """
        self.ssa = ssa_func
        self.scr = ssa_func.scr

        # global_offset → {field_offset → FieldAccessPattern}
        self.access_tracker: Dict[int, Dict[int, FieldAccessPattern]] = defaultdict(dict)

        # Known structures from headers (for matching)
        from ..headers.database import get_header_database
        self.header_db = get_header_database()

    def analyze_accesses(self):
        """Track all offset-based accesses in the function."""
        for block_id, instrs in self.ssa.instructions.items():
            for instr in instrs:
                if instr.mnemonic in ["DADR", "PNT"]:
                    self._track_offset_access(instr)
                elif instr.mnemonic == "DCP":
                    # DCP after DADR/PNT is a write
                    self._track_dcp_write(instr)

    def _track_offset_access(self, instr: SSAInstruction):
        """
        Track offset-based access from DADR/PNT instruction.

        DADR pattern:
            LADR &global_0   → base address
            DADR 4           → add offset 4
            → accessing global_0.field_at_offset_4
        """
        if not instr.instruction or not instr.instruction.instruction:
            return

        offset = instr.instruction.instruction.arg1

        # Find base global (input to DADR/PNT)
        if not instr.inputs:
            return

        base_value = instr.inputs[0]

        # Check if base comes from LADR or GADR (global address)
        base_global_offset = None

        if base_value.producer_inst:
            prod = base_value.producer_inst

            if prod.mnemonic == "LADR":
                # LADR loads address of local - skip for now
                return

            elif prod.mnemonic == "GADR":
                # GADR loads address of global
                if prod.instruction and prod.instruction.instruction:
                    base_global_offset = prod.instruction.instruction.arg1

            elif prod.mnemonic == "GCP":
                # Pointer loaded from global
                if prod.instruction and prod.instruction.instruction:
                    base_global_offset = prod.instruction.instruction.arg1

        if base_global_offset is None:
            return

        # Track this field access
        if offset not in self.access_tracker[base_global_offset]:
            self.access_tracker[base_global_offset][offset] = FieldAccessPattern(offset=offset)

        field = self.access_tracker[base_global_offset][offset]
        field.access_count += 1
        field.read_count += 1  # DADR/PNT is usually for reading

    def _track_dcp_write(self, instr: SSAInstruction):
        """Track write through DCP (after DADR)."""
        # DCP input should be address from DADR
        if not instr.inputs:
            return

        addr_value = instr.inputs[0]

        # Check if address comes from DADR
        if not addr_value.producer_inst:
            return

        prod = addr_value.producer_inst

        if prod.mnemonic == "DADR":
            # This is a write to a field
            if not prod.instruction or not prod.instruction.instruction:
                return

            offset = prod.instruction.instruction.arg1

            # Find base global
            if not prod.inputs:
                return

            base_value = prod.inputs[0]

            base_global_offset = None

            if base_value.producer_inst:
                base_prod = base_value.producer_inst

                if base_prod.mnemonic == "GADR":
                    if base_prod.instruction and base_prod.instruction.instruction:
                        base_global_offset = base_prod.instruction.instruction.arg1

            if base_global_offset is None:
                return

            # Track write
            if offset not in self.access_tracker[base_global_offset]:
                self.access_tracker[base_global_offset][offset] = FieldAccessPattern(offset=offset)

            field = self.access_tracker[base_global_offset][offset]
            field.write_count += 1

    def infer_structs(self) -> Dict[int, InferredStruct]:
        """
        Reconstruct struct definitions from tracked accesses.

        Returns:
            Dict mapping global_offset → InferredStruct
        """
        structs = {}

        for global_offset, fields_dict in self.access_tracker.items():
            if not fields_dict:
                continue

            # Only consider as struct if multiple field offsets accessed
            if len(fields_dict) < 2:
                continue

            # Calculate total size (max offset + assumed field size)
            max_offset = max(fields_dict.keys())
            total_size = max_offset + 4  # Assume 4-byte field at max offset

            # Detect stride/alignment
            stride = self._detect_alignment_patterns(list(fields_dict.keys()))

            # Create inferred struct
            struct = InferredStruct(
                base_global=global_offset,
                total_size=total_size,
                fields=list(fields_dict.values())
            )

            # Try to match against known structs
            match = self._match_known_struct(struct)
            if match:
                struct.possible_known_match = match
                struct.confidence = 0.85
            else:
                struct.confidence = 0.60

            structs[global_offset] = struct

        return structs

    def _detect_alignment_patterns(self, offsets: List[int]) -> int:
        """
        Detect common stride between field offsets.

        Args:
            offsets: List of field offsets

        Returns:
            Detected stride (4, 8, 16, etc.) or 0 if no pattern
        """
        if len(offsets) < 2:
            return 0

        sorted_offsets = sorted(offsets)
        diffs = [sorted_offsets[i+1] - sorted_offsets[i] for i in range(len(sorted_offsets) - 1)]

        # Check for common stride
        if not diffs:
            return 0

        # Most common difference
        from collections import Counter
        counter = Counter(diffs)
        most_common_stride = counter.most_common(1)[0][0]

        # Validate stride is power of 2 and reasonable
        if most_common_stride in [1, 2, 4, 8, 16, 32, 64]:
            return most_common_stride

        return 0

    def _match_known_struct(self, inferred: InferredStruct) -> Optional[str]:
        """
        Try to match inferred struct against known structs from headers.

        Args:
            inferred: Inferred structure

        Returns:
            Name of known struct if matched, else None
        """
        # Get all known structures
        known_structs = self.header_db.structures

        # Simple matching by size
        for struct_name, struct_data in known_structs.items():
            # Check if size matches
            known_size = struct_data.get('size')
            if known_size and abs(inferred.total_size - known_size) <= 4:
                # Size matches within 4 bytes - possible match
                return struct_name

        return None


def infer_structs_for_function(ssa_func: SSAFunction) -> Dict[int, InferredStruct]:
    """
    Convenience function to infer structures for a function.

    Args:
        ssa_func: SSA function to analyze

    Returns:
        Dict mapping global_offset → InferredStruct
    """
    engine = StructInferenceEngine(ssa_func)
    engine.analyze_accesses()
    return engine.infer_structs()
