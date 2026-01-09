"""
Bytecode comparison engine for SCR files.

Compares two .SCR files at the bytecode level to identify semantic and
cosmetic differences in headers, data segments, code segments, and XFN tables.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Any

from ..core.loader.scr_loader import SCRFile, SCRHeader, DataSegment, CodeSegment, XFNTable, Instruction, XFNEntry


class DifferenceType(Enum):
    """Type of difference found between two SCR files."""
    HEADER = "header"
    DATA = "data"
    CODE = "code"
    XFN = "xfn"
    STRUCTURE = "structure"  # Major structural differences


class DifferenceSeverity(Enum):
    """Severity level of a difference."""
    INFO = "info"           # Informational, no impact
    MINOR = "minor"         # Minor difference, likely cosmetic
    MAJOR = "major"         # Significant difference, may affect behavior
    CRITICAL = "critical"   # Critical difference, definitely affects behavior


@dataclass
class Difference:
    """
    Represents a single difference between two SCR files.

    Attributes:
        type: The type of difference (header, data, code, xfn)
        severity: How severe the difference is
        description: Human-readable description
        location: Where the difference occurs (e.g., "instruction 42", "xfn[3]")
        original_value: Value from original file
        recompiled_value: Value from recompiled file
        details: Additional context-specific details
    """
    type: DifferenceType
    severity: DifferenceSeverity
    description: str
    location: str
    original_value: Any = None
    recompiled_value: Any = None
    details: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """Human-readable difference representation."""
        severity_symbol = {
            DifferenceSeverity.INFO: "ℹ",
            DifferenceSeverity.MINOR: "⚠",
            DifferenceSeverity.MAJOR: "⚠",
            DifferenceSeverity.CRITICAL: "✗",
        }
        symbol = severity_symbol.get(self.severity, "•")

        result = f"{symbol} [{self.type.value}] {self.location}: {self.description}"

        if self.original_value is not None and self.recompiled_value is not None:
            result += f"\n  Original:    {self.original_value}"
            result += f"\n  Recompiled:  {self.recompiled_value}"

        return result


@dataclass
class SectionComparison:
    """
    Results of comparing a specific section of two SCR files.

    Attributes:
        section_name: Name of the section (e.g., "header", "code", "data")
        identical: Whether the sections are identical
        differences: List of differences found
        original_size: Size of original section in bytes
        recompiled_size: Size of recompiled section in bytes
    """
    section_name: str
    identical: bool
    differences: List[Difference] = field(default_factory=list)
    original_size: int = 0
    recompiled_size: int = 0

    @property
    def difference_count(self) -> int:
        """Total number of differences."""
        return len(self.differences)

    @property
    def critical_count(self) -> int:
        """Number of critical differences."""
        return sum(1 for d in self.differences if d.severity == DifferenceSeverity.CRITICAL)

    @property
    def major_count(self) -> int:
        """Number of major differences."""
        return sum(1 for d in self.differences if d.severity == DifferenceSeverity.MAJOR)

    def __str__(self) -> str:
        """Human-readable section comparison."""
        if self.identical:
            return f"✓ {self.section_name}: Identical"

        result = f"✗ {self.section_name}: {self.difference_count} difference(s)"
        if self.critical_count > 0:
            result += f" ({self.critical_count} critical)"
        elif self.major_count > 0:
            result += f" ({self.major_count} major)"

        return result


@dataclass
class ComparisonResult:
    """
    Complete comparison result for two SCR files.

    Attributes:
        original_file: Path to original .SCR file
        recompiled_file: Path to recompiled .SCR file
        identical: Whether files are bytewise identical
        sections: Dictionary of section comparisons by name
        load_error: Error message if files couldn't be loaded
    """
    original_file: Path
    recompiled_file: Path
    identical: bool = False
    sections: Dict[str, SectionComparison] = field(default_factory=dict)
    load_error: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        """Whether comparison completed successfully."""
        return self.load_error is None

    @property
    def all_differences(self) -> List[Difference]:
        """All differences across all sections."""
        diffs = []
        for section in self.sections.values():
            diffs.extend(section.differences)
        return diffs

    @property
    def critical_differences(self) -> List[Difference]:
        """All critical differences."""
        return [d for d in self.all_differences if d.severity == DifferenceSeverity.CRITICAL]

    @property
    def has_critical_differences(self) -> bool:
        """Whether there are any critical differences."""
        return len(self.critical_differences) > 0

    def __str__(self) -> str:
        """Human-readable comparison result."""
        if not self.is_valid:
            return f"✗ Comparison failed: {self.load_error}"

        if self.identical:
            return f"✓ Files are identical"

        result = f"Comparison: {self.original_file.name} vs {self.recompiled_file.name}\n"

        for section_name in ["header", "data", "global_pointers", "code", "xfn"]:
            if section_name in self.sections:
                result += f"\n  {self.sections[section_name]}"

        total_diffs = len(self.all_differences)
        critical = len(self.critical_differences)

        result += f"\n\nTotal differences: {total_diffs}"
        if critical > 0:
            result += f" ({critical} critical)"

        return result


class BytecodeComparator:
    """
    Compares two .SCR files at the bytecode level.

    Extracts and compares:
    - Headers (entry point, parameters, return values)
    - Data segments (constants, strings)
    - Global pointers
    - Code segments (instructions)
    - XFN tables (external functions)

    Identifies semantic differences (different behavior) vs cosmetic differences
    (different formatting, ordering, etc.).
    """

    def __init__(self):
        """Initialize the bytecode comparator."""
        self.original: Optional[SCRFile] = None
        self.recompiled: Optional[SCRFile] = None

    def compare_files(
        self,
        original_path: Path | str,
        recompiled_path: Path | str,
        opcode_variant: str = "auto"
    ) -> ComparisonResult:
        """
        Compare two SCR files.

        Args:
            original_path: Path to original .SCR file
            recompiled_path: Path to recompiled .SCR file
            opcode_variant: Opcode variant to use ("auto", "v1.60", etc.)

        Returns:
            ComparisonResult with all findings
        """
        original_path = Path(original_path)
        recompiled_path = Path(recompiled_path)

        result = ComparisonResult(
            original_file=original_path,
            recompiled_file=recompiled_path
        )

        # Load both files
        try:
            self.original = SCRFile.load(str(original_path), variant=opcode_variant)
        except Exception as e:
            result.load_error = f"Failed to load original file: {e}"
            return result

        try:
            self.recompiled = SCRFile.load(str(recompiled_path), variant=opcode_variant)
        except Exception as e:
            result.load_error = f"Failed to load recompiled file: {e}"
            return result

        # Quick check: are they bytewise identical?
        bytewise_identical = self.original.raw_data == self.recompiled.raw_data

        # Always compare sections to provide detailed information
        result.sections["header"] = self._compare_headers()
        result.sections["data"] = self._compare_data_segments()
        result.sections["global_pointers"] = self._compare_global_pointers()
        result.sections["code"] = self._compare_code_segments()
        result.sections["xfn"] = self._compare_xfn_tables()

        # Check if all sections are identical
        all_identical = all(section.identical for section in result.sections.values())
        result.identical = all_identical or bytewise_identical

        return result

    def _compare_headers(self) -> SectionComparison:
        """
        Compare header sections.

        Compares:
        - Entry point offset (enter_ip)
        - Parameter count (enter_size)
        - Return value count (ret_size)
        - Parameter types (enter_array)
        - Script attributes (save_info, opcode variant)
        """
        comparison = SectionComparison(
            section_name="header",
            identical=True,
            original_size=self.original.header.size_bytes,
            recompiled_size=self.recompiled.header.size_bytes
        )

        orig_h = self.original.header
        recomp_h = self.recompiled.header

        # Compare entry point
        if orig_h.enter_ip != recomp_h.enter_ip:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.HEADER,
                severity=DifferenceSeverity.CRITICAL,
                description="Entry point differs",
                location="header.enter_ip",
                original_value=orig_h.enter_ip,
                recompiled_value=recomp_h.enter_ip,
                details={
                    "impact": "Script execution will start at different location",
                    "is_scriptmain": (orig_h.enter_ip == -2, recomp_h.enter_ip == -2)
                }
            ))

        # Compare parameter count
        if orig_h.enter_size != recomp_h.enter_size:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.HEADER,
                severity=DifferenceSeverity.CRITICAL,
                description="Parameter count differs",
                location="header.enter_size",
                original_value=orig_h.enter_size,
                recompiled_value=recomp_h.enter_size,
                details={
                    "impact": "Script expects different number of parameters"
                }
            ))

        # Compare return value count
        if orig_h.ret_size != recomp_h.ret_size:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.HEADER,
                severity=DifferenceSeverity.CRITICAL,
                description="Return value count differs",
                location="header.ret_size",
                original_value=orig_h.ret_size,
                recompiled_value=recomp_h.ret_size,
                details={
                    "impact": "Script returns different number of values"
                }
            ))

        # Compare parameter types
        if orig_h.enter_array != recomp_h.enter_array:
            comparison.identical = False

            # Provide detailed type mismatch information
            type_diffs = []
            for i in range(max(len(orig_h.enter_array), len(recomp_h.enter_array))):
                orig_type = orig_h.enter_array[i] if i < len(orig_h.enter_array) else None
                recomp_type = recomp_h.enter_array[i] if i < len(recomp_h.enter_array) else None
                if orig_type != recomp_type:
                    type_diffs.append(f"param[{i}]: {orig_type} -> {recomp_type}")

            comparison.differences.append(Difference(
                type=DifferenceType.HEADER,
                severity=DifferenceSeverity.CRITICAL,
                description="Parameter types differ",
                location="header.enter_array",
                original_value=orig_h.enter_array,
                recompiled_value=recomp_h.enter_array,
                details={
                    "impact": "Script expects different parameter types",
                    "type_differences": type_diffs
                }
            ))

        # Compare header size (redundant check but useful for debugging)
        if self.original.header.size_bytes != self.recompiled.header.size_bytes:
            # This should already be caught by parameter count, but check explicitly
            if comparison.identical:  # Only report if we haven't already found differences
                comparison.identical = False
                comparison.differences.append(Difference(
                    type=DifferenceType.HEADER,
                    severity=DifferenceSeverity.MAJOR,
                    description="Header size differs",
                    location="header.size_bytes",
                    original_value=self.original.header.size_bytes,
                    recompiled_value=self.recompiled.header.size_bytes
                ))

        # Compare script attributes (file-level metadata)
        # These are informational and don't affect bytecode semantics

        # Save info presence
        orig_has_save = self.original.save_info is not None
        recomp_has_save = self.recompiled.save_info is not None
        if orig_has_save != recomp_has_save:
            comparison.differences.append(Difference(
                type=DifferenceType.STRUCTURE,
                severity=DifferenceSeverity.MINOR,
                description="Save info section presence differs",
                location="file.save_info",
                original_value="present" if orig_has_save else "absent",
                recompiled_value="present" if recomp_has_save else "absent",
                details={
                    "impact": "Cosmetic - save info is optional metadata",
                    "orig_save_count": self.original.save_info.count if orig_has_save else 0,
                    "recomp_save_count": self.recompiled.save_info.count if recomp_has_save else 0
                }
            ))

        # Opcode variant detection (informational)
        if hasattr(self.original, 'opcode_detection_scores') and hasattr(self.recompiled, 'opcode_detection_scores'):
            orig_variant = self.original.opcode_resolver.name
            recomp_variant = self.recompiled.opcode_resolver.name

            if orig_variant != recomp_variant:
                comparison.differences.append(Difference(
                    type=DifferenceType.STRUCTURE,
                    severity=DifferenceSeverity.INFO,
                    description="Detected opcode variant differs",
                    location="file.opcode_variant",
                    original_value=orig_variant,
                    recompiled_value=recomp_variant,
                    details={
                        "impact": "Informational - may indicate different compiler version",
                        "orig_forced": self.original.opcode_variant_forced,
                        "recomp_forced": self.recompiled.opcode_variant_forced
                    }
                ))

        return comparison

    def _compare_data_segments(self) -> SectionComparison:
        """
        Compare data segments.

        Performs comprehensive comparison including:
        - String differences (missing, extra, reordered)
        - Constant differences (numeric values)
        - Alignment padding differences
        - Reordering detection (same content, different order)
        """
        comparison = SectionComparison(
            section_name="data",
            identical=True,
            original_size=self.original.data_segment.size_bytes,
            recompiled_size=self.recompiled.data_segment.size_bytes
        )

        orig_data = self.original.data_segment
        recomp_data = self.recompiled.data_segment

        # Compare data count
        if orig_data.data_count != recomp_data.data_count:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.DATA,
                severity=DifferenceSeverity.MAJOR,
                description="Data segment size differs",
                location="data.data_count",
                original_value=orig_data.data_count,
                recompiled_value=recomp_data.data_count,
                details={
                    "impact": "Data segment has different number of 32-bit words",
                    "orig_bytes": orig_data.data_count * 4,
                    "recomp_bytes": recomp_data.data_count * 4
                }
            ))

        # Compare extracted strings (semantic comparison)
        self._compare_strings(orig_data, recomp_data, comparison)

        # Compare constants (numeric values)
        self._compare_constants(orig_data, recomp_data, comparison)

        # Compare alignment and padding
        self._compare_alignment(orig_data, recomp_data, comparison)

        # If strings and constants are the same but bytes differ, it's likely reordering
        if (len(comparison.differences) == 0 and
            orig_data.raw_data != recomp_data.raw_data):
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.DATA,
                severity=DifferenceSeverity.INFO,
                description="Data segment reordered (same content, different layout)",
                location="data",
                details={
                    "impact": "Cosmetic - data values are identical but in different order"
                }
            ))

        return comparison

    def _compare_strings(
        self,
        orig_data: DataSegment,
        recomp_data: DataSegment,
        comparison: SectionComparison
    ) -> None:
        """
        Compare string contents between data segments.

        Detects:
        - Missing strings (present in original, absent in recompiled)
        - Extra strings (absent in original, present in recompiled)
        - Reordered strings (same strings, different offsets)
        """
        # Compare by value (set comparison) for missing/extra detection
        orig_strings_set = set(orig_data.strings.values())
        recomp_strings_set = set(recomp_data.strings.values())

        missing_strings = orig_strings_set - recomp_strings_set
        extra_strings = recomp_strings_set - orig_strings_set

        # Missing strings are MAJOR - they may be referenced by code
        for s in missing_strings:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.DATA,
                severity=DifferenceSeverity.MAJOR,
                description="String missing in recompiled version",
                location="data.strings",
                original_value=repr(s),
                recompiled_value="<missing>",
                details={
                    "impact": "Code may reference this string by offset",
                    "string_length": len(s)
                }
            ))

        # Extra strings are MINOR - they may be dead code or debug strings
        for s in extra_strings:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.DATA,
                severity=DifferenceSeverity.MINOR,
                description="Extra string in recompiled version",
                location="data.strings",
                original_value="<not present>",
                recompiled_value=repr(s),
                details={
                    "impact": "May be unused or debug string",
                    "string_length": len(s)
                }
            ))

        # Check for string reordering (same strings, different offsets)
        if len(missing_strings) == 0 and len(extra_strings) == 0:
            # Same strings exist, but check if they're at different offsets
            orig_offset_map = {v: k for k, v in orig_data.strings.items()}
            recomp_offset_map = {v: k for k, v in recomp_data.strings.items()}

            reordered_count = 0
            for string_val in orig_strings_set:
                orig_offset = orig_offset_map[string_val]
                recomp_offset = recomp_offset_map.get(string_val)

                if recomp_offset is not None and orig_offset != recomp_offset:
                    reordered_count += 1

            if reordered_count > 0:
                comparison.identical = False
                comparison.differences.append(Difference(
                    type=DifferenceType.DATA,
                    severity=DifferenceSeverity.MINOR,
                    description=f"{reordered_count} string(s) at different offsets",
                    location="data.strings",
                    details={
                        "impact": "Strings exist but at different memory locations - code must use correct offsets",
                        "reordered_count": reordered_count,
                        "category": "reordering"
                    }
                ))

    def _compare_constants(
        self,
        orig_data: DataSegment,
        recomp_data: DataSegment,
        comparison: SectionComparison
    ) -> None:
        """
        Compare numeric constants in data segments.

        Extracts 32-bit integers and floats from non-string regions
        and compares them for differences.
        """
        import struct

        # Extract constants from both segments (excluding string regions)
        orig_constants = self._extract_constants(orig_data)
        recomp_constants = self._extract_constants(recomp_data)

        # Compare constant values (as sets for unordered comparison)
        orig_const_values = set(orig_constants.values())
        recomp_const_values = set(recomp_constants.values())

        missing_constants = orig_const_values - recomp_const_values
        extra_constants = recomp_const_values - orig_const_values

        # Missing constants are MAJOR
        for const in missing_constants:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.DATA,
                severity=DifferenceSeverity.MAJOR,
                description="Constant missing in recompiled version",
                location="data.constants",
                original_value=self._format_constant(const),
                recompiled_value="<missing>",
                details={
                    "impact": "Code may reference this constant by offset",
                    "category": "constant"
                }
            ))

        # Extra constants are MINOR
        for const in extra_constants:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.DATA,
                severity=DifferenceSeverity.MINOR,
                description="Extra constant in recompiled version",
                location="data.constants",
                original_value="<not present>",
                recompiled_value=self._format_constant(const),
                details={
                    "impact": "May be unused constant",
                    "category": "constant"
                }
            ))

        # Check for constant reordering
        if len(missing_constants) == 0 and len(extra_constants) == 0:
            orig_offset_map = {v: k for k, v in orig_constants.items()}
            recomp_offset_map = {v: k for k, v in recomp_constants.items()}

            reordered_count = 0
            for const_val in orig_const_values:
                orig_offset = orig_offset_map[const_val]
                recomp_offset = recomp_offset_map.get(const_val)

                if recomp_offset is not None and orig_offset != recomp_offset:
                    reordered_count += 1

            if reordered_count > 0:
                comparison.differences.append(Difference(
                    type=DifferenceType.DATA,
                    severity=DifferenceSeverity.MINOR,
                    description=f"{reordered_count} constant(s) at different offsets",
                    location="data.constants",
                    details={
                        "impact": "Constants exist but at different memory locations",
                        "reordered_count": reordered_count,
                        "category": "reordering"
                    }
                ))

    def _extract_constants(self, data_seg: DataSegment) -> Dict[int, Any]:
        """
        Extract numeric constants from data segment.

        Returns dict of {offset: value} for 32-bit integers and floats
        found outside of string regions.
        """
        import struct

        constants = {}

        # Build set of string regions to exclude
        string_regions = set()
        for offset, string_val in data_seg.strings.items():
            # String region includes the string bytes plus null terminator
            string_len = len(string_val) + 1  # +1 for null terminator
            for i in range(offset, offset + string_len):
                string_regions.add(i)

        # Scan 32-bit aligned offsets
        i = 0
        while i < len(data_seg.raw_data) - 3:
            # Skip if this is part of a string
            if i in string_regions:
                i += 1
                continue

            # Try to extract 32-bit value (ensure 4-byte alignment)
            if i % 4 == 0:
                try:
                    # Try as integer
                    int_val = struct.unpack('<I', data_seg.raw_data[i:i+4])[0]

                    # Try as float
                    float_val = struct.unpack('<f', data_seg.raw_data[i:i+4])[0]

                    # Store both representations
                    # Use a tuple to represent the raw bytes
                    raw_bytes = data_seg.raw_data[i:i+4]
                    constants[i] = raw_bytes

                except struct.error:
                    pass

            i += 4

        return constants

    def _format_constant(self, raw_bytes: bytes) -> str:
        """
        Format a constant value for display.

        Shows both integer and float interpretations.
        """
        import struct

        if len(raw_bytes) != 4:
            return f"0x{raw_bytes.hex()}"

        int_val = struct.unpack('<I', raw_bytes)[0]

        try:
            float_val = struct.unpack('<f', raw_bytes)[0]
            # Check if float representation makes sense
            if abs(float_val) < 1e6 and abs(float_val) > 1e-6 and float_val == float_val:  # NaN check
                return f"0x{int_val:08X} (int: {int_val}, float: {float_val:.6f})"
            else:
                return f"0x{int_val:08X} (int: {int_val})"
        except:
            return f"0x{int_val:08X} (int: {int_val})"

    def _compare_alignment(
        self,
        orig_data: DataSegment,
        recomp_data: DataSegment,
        comparison: SectionComparison
    ) -> None:
        """
        Compare alignment and padding between data segments.

        Detects differences in padding bytes (typically zeros) used for 4-byte alignment.
        """
        # Padding is typically at the end of strings or between data
        # Look for sequences of null bytes
        orig_padding = self._find_padding_regions(orig_data)
        recomp_padding = self._find_padding_regions(recomp_data)

        # Calculate total padding
        orig_padding_bytes = sum(end - start for start, end in orig_padding)
        recomp_padding_bytes = sum(end - start for start, end in recomp_padding)

        if orig_padding_bytes != recomp_padding_bytes:
            comparison.differences.append(Difference(
                type=DifferenceType.DATA,
                severity=DifferenceSeverity.INFO,
                description="Different amount of alignment padding",
                location="data.padding",
                original_value=f"{orig_padding_bytes} bytes",
                recompiled_value=f"{recomp_padding_bytes} bytes",
                details={
                    "impact": "Cosmetic - padding doesn't affect functionality",
                    "orig_padding_regions": len(orig_padding),
                    "recomp_padding_regions": len(recomp_padding),
                    "category": "alignment"
                }
            ))

    def _find_padding_regions(self, data_seg: DataSegment) -> List[tuple]:
        """
        Find regions of padding (null bytes) in data segment.

        Returns list of (start_offset, end_offset) tuples for padding regions.
        """
        padding_regions = []

        # Build set of string regions to exclude
        string_regions = set()
        for offset, string_val in data_seg.strings.items():
            string_len = len(string_val) + 1  # +1 for null terminator
            for i in range(offset, offset + string_len):
                string_regions.add(i)

        # Find sequences of null bytes outside of strings
        i = 0
        while i < len(data_seg.raw_data):
            # Skip string regions
            if i in string_regions:
                i += 1
                continue

            # Start of potential padding region
            if data_seg.raw_data[i] == 0:
                start = i
                while i < len(data_seg.raw_data) and data_seg.raw_data[i] == 0:
                    if i in string_regions:
                        break
                    i += 1
                end = i

                # Only consider padding if it's at least 2 bytes (1 byte might be part of a value)
                if end - start >= 2:
                    padding_regions.append((start, end))
            else:
                i += 1

        return padding_regions

    def _compare_global_pointers(self) -> SectionComparison:
        """Compare global pointer tables."""
        comparison = SectionComparison(
            section_name="global_pointers",
            identical=True,
            original_size=self.original.global_pointers.size_bytes,
            recompiled_size=self.recompiled.global_pointers.size_bytes
        )

        orig_gp = self.original.global_pointers
        recomp_gp = self.recompiled.global_pointers

        # Compare count
        if orig_gp.gptr_count != recomp_gp.gptr_count:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.DATA,
                severity=DifferenceSeverity.CRITICAL,
                description="Global pointer count differs",
                location="global_pointers.gptr_count",
                original_value=orig_gp.gptr_count,
                recompiled_value=recomp_gp.gptr_count
            ))

        # Compare offsets
        min_count = min(orig_gp.gptr_count, recomp_gp.gptr_count)
        for i in range(min_count):
            if orig_gp.offsets[i] != recomp_gp.offsets[i]:
                comparison.identical = False
                comparison.differences.append(Difference(
                    type=DifferenceType.DATA,
                    severity=DifferenceSeverity.MAJOR,
                    description="Global pointer offset differs",
                    location=f"global_pointers[{i}]",
                    original_value=orig_gp.offsets[i],
                    recompiled_value=recomp_gp.offsets[i]
                ))

        return comparison

    def _compare_code_segments(self) -> SectionComparison:
        """
        Compare code segments instruction by instruction.

        Performs comprehensive comparison including:
        - Instruction-by-instruction bytecode comparison
        - Equivalent instruction pattern detection (e.g., INC vs ADD 1)
        - Control flow analysis (jumps, calls, returns)
        - Optimization difference detection
        """
        comparison = SectionComparison(
            section_name="code",
            identical=True,
            original_size=self.original.code_segment.size_bytes,
            recompiled_size=self.recompiled.code_segment.size_bytes
        )

        orig_code = self.original.code_segment
        recomp_code = self.recompiled.code_segment

        # Compare instruction count
        if orig_code.code_count != recomp_code.code_count:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.CODE,
                severity=DifferenceSeverity.CRITICAL,
                description="Instruction count differs",
                location="code.code_count",
                original_value=orig_code.code_count,
                recompiled_value=recomp_code.code_count,
                details={
                    "impact": "Code has different number of instructions - major structural difference",
                    "orig_bytes": orig_code.code_count * 12,
                    "recomp_bytes": recomp_code.code_count * 12
                }
            ))
            # If counts differ, can't do instruction-by-instruction comparison
            return comparison

        # Compare instructions
        for i in range(orig_code.code_count):
            orig_instr = orig_code.instructions[i]
            recomp_instr = recomp_code.instructions[i]

            if not self._instructions_equal(orig_instr, recomp_instr):
                # Check if instructions are semantically equivalent
                if self._instructions_equivalent(orig_instr, recomp_instr, i):
                    comparison.identical = False
                    self._add_equivalent_instruction_difference(
                        comparison, i, orig_instr, recomp_instr
                    )
                else:
                    comparison.identical = False
                    self._add_instruction_difference(
                        comparison, i, orig_instr, recomp_instr
                    )

        # Analyze control flow differences
        self._analyze_control_flow(orig_code, recomp_code, comparison)

        return comparison

    def _instructions_equivalent(
        self,
        instr1: Instruction,
        instr2: Instruction,
        address: int
    ) -> bool:
        """
        Check if two instructions are semantically equivalent.

        Detects patterns like:
        - INC vs ADD 1
        - DEC vs SUB 1
        - Different representations of the same operation
        """
        # Get mnemonics
        mnem1 = self.original.opcode_resolver.opcode_map.get(
            instr1.opcode, ""
        )
        mnem2 = self.recompiled.opcode_resolver.opcode_map.get(
            instr2.opcode, ""
        )

        # INC vs ADD 1 pattern
        if mnem1 == "INC" and mnem2 == "ADD":
            # ADD with immediate value 1
            return instr2.arg1 == 1 or instr2.arg2 == 1

        if mnem1 == "ADD" and mnem2 == "INC":
            return instr1.arg1 == 1 or instr1.arg2 == 1

        # DEC vs SUB 1 pattern
        if mnem1 == "DEC" and mnem2 == "SUB":
            return instr2.arg1 == 1 or instr2.arg2 == 1

        if mnem1 == "SUB" and mnem2 == "DEC":
            return instr1.arg1 == 1 or instr1.arg2 == 1

        # MUL 2 vs LS 1 (left shift by 1 is multiply by 2)
        if mnem1 == "MUL" and mnem2 == "LS":
            if (instr1.arg1 == 2 or instr1.arg2 == 2) and (instr2.arg1 == 1 or instr2.arg2 == 1):
                return True

        if mnem1 == "LS" and mnem2 == "MUL":
            if (instr1.arg1 == 1 or instr1.arg2 == 1) and (instr2.arg1 == 2 or instr2.arg2 == 2):
                return True

        # Similar patterns for typed operations (CINC/CADD, SINC/SADD, etc.)
        type_prefixes = ["C", "S", "F", "D"]
        for prefix in type_prefixes:
            if mnem1 == f"{prefix}INC" and mnem2 == f"{prefix}ADD":
                return instr2.arg1 == 1 or instr2.arg2 == 1
            if mnem1 == f"{prefix}ADD" and mnem2 == f"{prefix}INC":
                return instr1.arg1 == 1 or instr1.arg2 == 1
            if mnem1 == f"{prefix}DEC" and mnem2 == f"{prefix}SUB":
                return instr2.arg1 == 1 or instr2.arg2 == 1
            if mnem1 == f"{prefix}SUB" and mnem2 == f"{prefix}DEC":
                return instr1.arg1 == 1 or instr1.arg2 == 1

        return False

    def _add_equivalent_instruction_difference(
        self,
        comparison: SectionComparison,
        address: int,
        orig_instr: Instruction,
        recomp_instr: Instruction
    ) -> None:
        """
        Add a difference for equivalent instructions.

        These are marked as MINOR severity since they're semantically equivalent.
        """
        orig_mnemonic = self.original.opcode_resolver.opcode_map.get(
            orig_instr.opcode, f"OP_{orig_instr.opcode}"
        )
        recomp_mnemonic = self.recompiled.opcode_resolver.opcode_map.get(
            recomp_instr.opcode, f"OP_{recomp_instr.opcode}"
        )

        comparison.differences.append(Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.MINOR,
            description="Equivalent instruction with different encoding",
            location=f"instruction[{address}]",
            original_value=f"{orig_mnemonic} {orig_instr.arg1}, {orig_instr.arg2}",
            recompiled_value=f"{recomp_mnemonic} {recomp_instr.arg1}, {recomp_instr.arg2}",
            details={
                "address": address,
                "impact": "Optimization/compiler difference - semantically equivalent",
                "category": "optimization",
                "orig_opcode": orig_instr.opcode,
                "recomp_opcode": recomp_instr.opcode,
                "orig_arg1": orig_instr.arg1,
                "recomp_arg1": recomp_instr.arg1,
                "orig_arg2": orig_instr.arg2,
                "recomp_arg2": recomp_instr.arg2,
            }
        ))

    def _add_instruction_difference(
        self,
        comparison: SectionComparison,
        address: int,
        orig_instr: Instruction,
        recomp_instr: Instruction
    ) -> None:
        """
        Add a difference for non-equivalent instructions.

        These are marked as CRITICAL severity since they may behave differently.
        """
        orig_mnemonic = self.original.opcode_resolver.opcode_map.get(
            orig_instr.opcode, f"OP_{orig_instr.opcode}"
        )
        recomp_mnemonic = self.recompiled.opcode_resolver.opcode_map.get(
            recomp_instr.opcode, f"OP_{recomp_instr.opcode}"
        )

        # Determine if this is a control flow instruction
        control_flow_ops = {"JMP", "JZ", "JNZ", "CALL", "RET", "XCALL"}
        is_control_flow = orig_mnemonic in control_flow_ops or recomp_mnemonic in control_flow_ops

        comparison.differences.append(Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.CRITICAL,
            description="Instruction differs" + (" (control flow)" if is_control_flow else ""),
            location=f"instruction[{address}]",
            original_value=f"{orig_mnemonic} {orig_instr.arg1}, {orig_instr.arg2}",
            recompiled_value=f"{recomp_mnemonic} {recomp_instr.arg1}, {recomp_instr.arg2}",
            details={
                "address": address,
                "impact": "Different instruction - behavior may differ",
                "is_control_flow": is_control_flow,
                "orig_opcode": orig_instr.opcode,
                "recomp_opcode": recomp_instr.opcode,
                "orig_arg1": orig_instr.arg1,
                "recomp_arg1": recomp_instr.arg1,
                "orig_arg2": orig_instr.arg2,
                "recomp_arg2": recomp_instr.arg2,
            }
        ))

    def _analyze_control_flow(
        self,
        orig_code: CodeSegment,
        recomp_code: CodeSegment,
        comparison: SectionComparison
    ) -> None:
        """
        Analyze control flow differences between code segments.

        Examines:
        - Jump targets and control flow graph
        - Function calls (internal and external)
        - Return points
        """
        # Extract control flow instructions from both
        orig_cf = self._extract_control_flow(orig_code, self.original)
        recomp_cf = self._extract_control_flow(recomp_code, self.recompiled)

        # Compare jump targets
        orig_jumps = orig_cf.get("jumps", {})
        recomp_jumps = recomp_cf.get("jumps", {})

        # Check for different jump targets at same address
        for addr in orig_jumps.keys() & recomp_jumps.keys():
            if orig_jumps[addr] != recomp_jumps[addr]:
                comparison.identical = False
                comparison.differences.append(Difference(
                    type=DifferenceType.CODE,
                    severity=DifferenceSeverity.CRITICAL,
                    description="Jump target differs",
                    location=f"instruction[{addr}]",
                    original_value=f"jumps to {orig_jumps[addr]}",
                    recompiled_value=f"jumps to {recomp_jumps[addr]}",
                    details={
                        "impact": "Control flow diverges - code will execute differently",
                        "category": "control_flow",
                        "orig_target": orig_jumps[addr],
                        "recomp_target": recomp_jumps[addr]
                    }
                ))

        # Compare function calls
        orig_calls = orig_cf.get("calls", set())
        recomp_calls = recomp_cf.get("calls", set())

        missing_calls = orig_calls - recomp_calls
        extra_calls = recomp_calls - orig_calls

        for call_addr in missing_calls:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.CODE,
                severity=DifferenceSeverity.MAJOR,
                description="Function call missing in recompiled version",
                location=f"instruction[{call_addr}]",
                original_value="CALL instruction present",
                recompiled_value="CALL instruction missing",
                details={
                    "impact": "Function call removed - behavior will differ",
                    "category": "control_flow"
                }
            ))

        for call_addr in extra_calls:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.CODE,
                severity=DifferenceSeverity.MAJOR,
                description="Extra function call in recompiled version",
                location=f"instruction[{call_addr}]",
                original_value="No CALL instruction",
                recompiled_value="CALL instruction added",
                details={
                    "impact": "Function call added - behavior will differ",
                    "category": "control_flow"
                }
            ))

        # Compare external function calls
        orig_xcalls = orig_cf.get("xcalls", {})
        recomp_xcalls = recomp_cf.get("xcalls", {})

        for addr in orig_xcalls.keys() & recomp_xcalls.keys():
            if orig_xcalls[addr] != recomp_xcalls[addr]:
                comparison.identical = False
                comparison.differences.append(Difference(
                    type=DifferenceType.CODE,
                    severity=DifferenceSeverity.CRITICAL,
                    description="External function call differs",
                    location=f"instruction[{addr}]",
                    original_value=f"calls XFN[{orig_xcalls[addr]}]",
                    recompiled_value=f"calls XFN[{recomp_xcalls[addr]}]",
                    details={
                        "impact": "Calls different external function",
                        "category": "control_flow",
                        "orig_xfn_index": orig_xcalls[addr],
                        "recomp_xfn_index": recomp_xcalls[addr]
                    }
                ))

    def _extract_control_flow(
        self,
        code_seg: CodeSegment,
        scr_file: SCRFile
    ) -> Dict[str, Any]:
        """
        Extract control flow information from code segment.

        Returns dict with:
        - jumps: {address: target_address}
        - calls: {address}
        - xcalls: {address: xfn_index}
        - returns: {address}
        """
        result = {
            "jumps": {},
            "calls": set(),
            "xcalls": {},
            "returns": set()
        }

        for i, instr in enumerate(code_seg.instructions):
            mnemonic = scr_file.opcode_resolver.opcode_map.get(
                instr.opcode, ""
            )

            if mnemonic in ("JMP", "JZ", "JNZ"):
                # arg1 is the target address
                result["jumps"][i] = instr.arg1

            elif mnemonic == "CALL":
                # arg1 is the target function address
                result["calls"].add(i)
                result["jumps"][i] = instr.arg1

            elif mnemonic == "XCALL":
                # arg1 is the XFN table index
                result["xcalls"][i] = instr.arg1

            elif mnemonic == "RET":
                result["returns"].add(i)

        return result

    def _compare_xfn_tables(self) -> SectionComparison:
        """Compare external function tables."""
        comparison = SectionComparison(
            section_name="xfn",
            identical=True
        )

        orig_xfn = self.original.xfn_table
        recomp_xfn = self.recompiled.xfn_table

        # Compare count
        if orig_xfn.xfn_count != recomp_xfn.xfn_count:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.XFN,
                severity=DifferenceSeverity.CRITICAL,
                description="External function count differs",
                location="xfn.xfn_count",
                original_value=orig_xfn.xfn_count,
                recompiled_value=recomp_xfn.xfn_count
            ))
            # If counts differ, we can still compare what's common

        # Create name-based lookup for semantic comparison
        orig_by_name = {entry.name: entry for entry in orig_xfn.entries}
        recomp_by_name = {entry.name: entry for entry in recomp_xfn.entries}

        # Check for missing functions
        missing = set(orig_by_name.keys()) - set(recomp_by_name.keys())
        for name in missing:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.XFN,
                severity=DifferenceSeverity.CRITICAL,
                description="External function missing in recompiled version",
                location="xfn",
                original_value=name,
                recompiled_value="<missing>"
            ))

        # Check for extra functions
        extra = set(recomp_by_name.keys()) - set(orig_by_name.keys())
        for name in extra:
            comparison.identical = False
            comparison.differences.append(Difference(
                type=DifferenceType.XFN,
                severity=DifferenceSeverity.MAJOR,
                description="Extra external function in recompiled version",
                location="xfn",
                original_value="<not present>",
                recompiled_value=name
            ))

        # Compare common functions
        common = set(orig_by_name.keys()) & set(recomp_by_name.keys())
        for name in common:
            orig_entry = orig_by_name[name]
            recomp_entry = recomp_by_name[name]

            if not self._xfn_entries_equal(orig_entry, recomp_entry):
                comparison.identical = False
                comparison.differences.append(Difference(
                    type=DifferenceType.XFN,
                    severity=DifferenceSeverity.MAJOR,
                    description=f"External function signature differs: {name}",
                    location=f"xfn[{name}]",
                    original_value=f"args={orig_entry.arg_count}, ret={orig_entry.ret_size}",
                    recompiled_value=f"args={recomp_entry.arg_count}, ret={recomp_entry.ret_size}",
                    details={
                        "orig_arg_count": orig_entry.arg_count,
                        "recomp_arg_count": recomp_entry.arg_count,
                        "orig_ret_size": orig_entry.ret_size,
                        "recomp_ret_size": recomp_entry.ret_size,
                    }
                ))

        return comparison

    def _instructions_equal(self, instr1: Instruction, instr2: Instruction) -> bool:
        """Check if two instructions are equal."""
        return (
            instr1.opcode == instr2.opcode and
            instr1.arg1 == instr2.arg1 and
            instr1.arg2 == instr2.arg2
        )

    def _xfn_entries_equal(self, entry1: XFNEntry, entry2: XFNEntry) -> bool:
        """Check if two XFN entries are equal (ignoring index and name_ptr)."""
        return (
            entry1.name == entry2.name and
            entry1.arg_count == entry2.arg_count and
            entry1.ret_size == entry2.ret_size and
            entry1.arg_types == entry2.arg_types
        )
