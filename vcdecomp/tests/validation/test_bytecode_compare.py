"""
Unit tests for bytecode comparison engine.

Tests the BytecodeComparator class and related data structures:
- Comparison of identical SCR files
- Detection of cosmetic differences (reordering, padding, etc.)
- Detection of semantic differences (different opcodes, wrong values, etc.)
- Difference categorization (SEMANTIC, COSMETIC, OPTIMIZATION)
- All comparison methods (header, data, code, XFN)

Uses test fixtures from Compiler-testruns/ and mocked SCRFile objects.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
from typing import List
import struct

from vcdecomp.validation.bytecode_compare import (
    BytecodeComparator,
    Difference,
    DifferenceType,
    DifferenceSeverity,
    SectionComparison,
    ComparisonResult,
)
from vcdecomp.validation.difference_types import (
    DifferenceCategory,
    DifferenceCategorizer,
    categorize_differences,
    get_semantic_differences,
    get_cosmetic_differences,
)
from vcdecomp.core.loader.scr_loader import (
    SCRFile,
    SCRHeader,
    DataSegment,
    CodeSegment,
    XFNTable,
    XFNEntry,
    Instruction,
)


class TestDifferenceDataStructures(unittest.TestCase):
    """Test Difference, SectionComparison, and ComparisonResult data structures."""

    def test_difference_creation(self):
        """Test creating a Difference object."""
        diff = Difference(
            type=DifferenceType.HEADER,
            severity=DifferenceSeverity.CRITICAL,
            description="Entry point differs",
            location="header.enter_ip",
            original_value=0,
            recompiled_value=4,
            details={"impact": "Script execution will start at different location"}
        )

        self.assertEqual(diff.type, DifferenceType.HEADER)
        self.assertEqual(diff.severity, DifferenceSeverity.CRITICAL)
        self.assertEqual(diff.description, "Entry point differs")
        self.assertEqual(diff.location, "header.enter_ip")
        self.assertEqual(diff.original_value, 0)
        self.assertEqual(diff.recompiled_value, 4)
        self.assertIn("impact", diff.details)

    def test_difference_str(self):
        """Test Difference string representation."""
        diff = Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.MAJOR,
            description="Different opcode",
            location="instruction[10]",
            original_value="IADD",
            recompiled_value="IMUL"
        )

        str_repr = str(diff)
        self.assertIn("CODE", str_repr)
        self.assertIn("instruction[10]", str_repr)
        self.assertIn("Different opcode", str_repr)
        self.assertIn("IADD", str_repr)
        self.assertIn("IMUL", str_repr)

    def test_section_comparison_identical(self):
        """Test SectionComparison for identical sections."""
        comparison = SectionComparison(
            section_name="header",
            identical=True,
            original_size=20,
            recompiled_size=20
        )

        self.assertTrue(comparison.identical)
        self.assertEqual(comparison.difference_count, 0)
        self.assertEqual(comparison.critical_count, 0)
        self.assertEqual(comparison.major_count, 0)
        self.assertIn("Identical", str(comparison))

    def test_section_comparison_with_differences(self):
        """Test SectionComparison with differences."""
        comparison = SectionComparison(
            section_name="code",
            identical=False,
            original_size=100,
            recompiled_size=100
        )

        comparison.differences.append(Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.CRITICAL,
            description="Wrong opcode",
            location="instruction[5]"
        ))
        comparison.differences.append(Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.MINOR,
            description="Different offset",
            location="instruction[10]"
        ))

        self.assertFalse(comparison.identical)
        self.assertEqual(comparison.difference_count, 2)
        self.assertEqual(comparison.critical_count, 1)
        self.assertEqual(comparison.major_count, 0)

    def test_comparison_result_valid(self):
        """Test ComparisonResult with valid comparison."""
        result = ComparisonResult(
            original_file=Path("original.scr"),
            recompiled_file=Path("recompiled.scr"),
            identical=False
        )

        result.sections["header"] = SectionComparison(
            section_name="header",
            identical=True
        )
        result.sections["code"] = SectionComparison(
            section_name="code",
            identical=False,
            differences=[
                Difference(
                    type=DifferenceType.CODE,
                    severity=DifferenceSeverity.CRITICAL,
                    description="Critical error",
                    location="code[0]"
                )
            ]
        )

        self.assertTrue(result.is_valid)
        self.assertFalse(result.identical)
        self.assertEqual(len(result.all_differences), 1)
        self.assertEqual(len(result.critical_differences), 1)
        self.assertTrue(result.has_critical_differences)

    def test_comparison_result_load_error(self):
        """Test ComparisonResult with load error."""
        result = ComparisonResult(
            original_file=Path("missing.scr"),
            recompiled_file=Path("recompiled.scr"),
            load_error="Failed to load original file: File not found"
        )

        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.load_error)
        self.assertIn("Failed to load", str(result))


class TestBytecodeComparator(unittest.TestCase):
    """Test BytecodeComparator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.comparator = BytecodeComparator()

    def _create_mock_scr_file(
        self,
        enter_ip: int = 0,
        enter_size: int = 0,
        data_count: int = 0,
        data_bytes: bytes = b"",
        instructions: List[Instruction] = None,
        xfn_entries: List[XFNEntry] = None
    ) -> Mock:
        """Create a mock SCRFile object."""
        mock_scr = Mock(spec=SCRFile)

        # Header
        mock_scr.header = Mock(spec=SCRHeader)
        mock_scr.header.enter_ip = enter_ip
        mock_scr.header.enter_size = enter_size
        mock_scr.header.ret_size = 0
        mock_scr.header.enter_array = []
        mock_scr.header.size_bytes = 12 + (4 * enter_size)

        # Data segment
        mock_scr.data = Mock(spec=DataSegment)
        mock_scr.data.data_count = data_count
        mock_scr.data.raw_data = data_bytes
        mock_scr.data.strings = {}
        mock_scr.data.size_bytes = 4 + len(data_bytes)

        # Global pointers
        mock_scr.global_pointers = []

        # Code segment
        mock_scr.code = Mock(spec=CodeSegment)
        mock_scr.code.instructions = instructions or []
        mock_scr.code.instruction_count = len(instructions or [])

        # XFN table
        mock_scr.xfn = Mock(spec=XFNTable)
        mock_scr.xfn.entries = xfn_entries or []
        mock_scr.xfn.count = len(xfn_entries or [])

        # Raw data
        mock_scr.raw_data = b"\x00" * 100

        return mock_scr

    def test_compare_identical_files(self):
        """Test comparison of two identical files."""
        # Create two identical mock files
        orig = self._create_mock_scr_file(enter_ip=0, enter_size=0, data_count=0)
        recomp = self._create_mock_scr_file(enter_ip=0, enter_size=0, data_count=0)

        # Same raw data
        orig.raw_data = b"\x00\x01\x02\x03"
        recomp.raw_data = b"\x00\x01\x02\x03"

        self.comparator.original = orig
        self.comparator.recompiled = recomp

        # Compare sections
        header_comp = self.comparator._compare_headers()
        data_comp = self.comparator._compare_data_segments()
        code_comp = self.comparator._compare_code_segments()
        xfn_comp = self.comparator._compare_xfn_tables()

        # All sections should be identical
        self.assertTrue(header_comp.identical)
        self.assertTrue(data_comp.identical)
        self.assertTrue(code_comp.identical)
        self.assertTrue(xfn_comp.identical)

        self.assertEqual(len(header_comp.differences), 0)
        self.assertEqual(len(data_comp.differences), 0)
        self.assertEqual(len(code_comp.differences), 0)
        self.assertEqual(len(xfn_comp.differences), 0)

    def test_compare_different_entry_points(self):
        """Test detection of different entry points (semantic difference)."""
        orig = self._create_mock_scr_file(enter_ip=0)
        recomp = self._create_mock_scr_file(enter_ip=4)

        self.comparator.original = orig
        self.comparator.recompiled = recomp

        header_comp = self.comparator._compare_headers()

        self.assertFalse(header_comp.identical)
        self.assertEqual(len(header_comp.differences), 1)
        self.assertEqual(header_comp.differences[0].severity, DifferenceSeverity.CRITICAL)
        self.assertIn("Entry point", header_comp.differences[0].description)

    def test_compare_different_parameter_counts(self):
        """Test detection of different parameter counts."""
        orig = self._create_mock_scr_file(enter_size=2)
        orig.header.enter_array = [1, 2]

        recomp = self._create_mock_scr_file(enter_size=3)
        recomp.header.enter_array = [1, 2, 3]

        self.comparator.original = orig
        self.comparator.recompiled = recomp

        header_comp = self.comparator._compare_headers()

        self.assertFalse(header_comp.identical)
        self.assertTrue(any(
            "parameter count" in d.description.lower()
            for d in header_comp.differences
        ))

    def test_compare_different_data_sizes(self):
        """Test detection of different data segment sizes."""
        orig = self._create_mock_scr_file(
            data_count=5,
            data_bytes=b"\x00" * 20
        )
        recomp = self._create_mock_scr_file(
            data_count=10,
            data_bytes=b"\x00" * 40
        )

        self.comparator.original = orig
        self.comparator.recompiled = recomp

        data_comp = self.comparator._compare_data_segments()

        self.assertFalse(data_comp.identical)
        self.assertTrue(any(
            "size" in d.description.lower()
            for d in data_comp.differences
        ))

    def test_compare_different_data_values(self):
        """Test detection of different data values (semantic difference)."""
        orig = self._create_mock_scr_file(
            data_count=4,
            data_bytes=struct.pack('<4I', 1, 2, 3, 4)
        )
        recomp = self._create_mock_scr_file(
            data_count=4,
            data_bytes=struct.pack('<4I', 1, 2, 99, 4)  # Different value at offset 8
        )

        self.comparator.original = orig
        self.comparator.recompiled = recomp

        data_comp = self.comparator._compare_data_segments()

        self.assertFalse(data_comp.identical)
        # Should detect the difference at some offset
        self.assertGreater(len(data_comp.differences), 0)

    def test_compare_different_instruction_counts(self):
        """Test detection of different instruction counts."""
        orig_instructions = [
            Instruction(offset=0, opcode=0x01, arg1=0, arg2=0),
            Instruction(offset=12, opcode=0x02, arg1=0, arg2=0),
        ]
        recomp_instructions = [
            Instruction(offset=0, opcode=0x01, arg1=0, arg2=0),
        ]

        orig = self._create_mock_scr_file(instructions=orig_instructions)
        recomp = self._create_mock_scr_file(instructions=recomp_instructions)

        self.comparator.original = orig
        self.comparator.recompiled = recomp

        code_comp = self.comparator._compare_code_segments()

        self.assertFalse(code_comp.identical)
        self.assertTrue(any(
            "count" in d.description.lower()
            for d in code_comp.differences
        ))

    def test_compare_different_opcodes(self):
        """Test detection of different opcodes (semantic difference)."""
        orig_instructions = [
            Instruction(offset=0, opcode=0x01, arg1=5, arg2=0),  # IADD
        ]
        recomp_instructions = [
            Instruction(offset=0, opcode=0x02, arg1=5, arg2=0),  # IMUL (different!)
        ]

        orig = self._create_mock_scr_file(instructions=orig_instructions)
        recomp = self._create_mock_scr_file(instructions=recomp_instructions)

        self.comparator.original = orig
        self.comparator.recompiled = recomp

        code_comp = self.comparator._compare_code_segments()

        self.assertFalse(code_comp.identical)
        # Should find a critical difference in opcode
        self.assertTrue(any(
            d.severity == DifferenceSeverity.CRITICAL
            for d in code_comp.differences
        ))

    def test_compare_different_xfn_counts(self):
        """Test detection of different XFN table sizes."""
        orig_xfn = [
            XFNEntry(name="SC_message", signature="v1s", offset=0),
            XFNEntry(name="SC_P_Create", signature="v2ss", offset=28),
        ]
        recomp_xfn = [
            XFNEntry(name="SC_message", signature="v1s", offset=0),
        ]

        orig = self._create_mock_scr_file(xfn_entries=orig_xfn)
        recomp = self._create_mock_scr_file(xfn_entries=recomp_xfn)

        self.comparator.original = orig
        self.comparator.recompiled = recomp

        xfn_comp = self.comparator._compare_xfn_tables()

        self.assertFalse(xfn_comp.identical)
        self.assertTrue(any(
            "count" in d.description.lower()
            for d in xfn_comp.differences
        ))

    def test_compare_different_xfn_names(self):
        """Test detection of different XFN function names."""
        orig_xfn = [
            XFNEntry(name="SC_message", signature="v1s", offset=0),
        ]
        recomp_xfn = [
            XFNEntry(name="SC_GameMessage", signature="v1s", offset=0),  # Different!
        ]

        orig = self._create_mock_scr_file(xfn_entries=orig_xfn)
        recomp = self._create_mock_scr_file(xfn_entries=recomp_xfn)

        self.comparator.original = orig
        self.comparator.recompiled = recomp

        xfn_comp = self.comparator._compare_xfn_tables()

        self.assertFalse(xfn_comp.identical)
        # Should detect missing/extra functions
        self.assertGreater(len(xfn_comp.differences), 0)

    def test_compare_different_xfn_signatures(self):
        """Test detection of different XFN signatures."""
        orig_xfn = [
            XFNEntry(name="SC_message", signature="v1s", offset=0),
        ]
        recomp_xfn = [
            XFNEntry(name="SC_message", signature="v2si", offset=0),  # Different signature!
        ]

        orig = self._create_mock_scr_file(xfn_entries=orig_xfn)
        recomp = self._create_mock_scr_file(xfn_entries=recomp_xfn)

        self.comparator.original = orig
        self.comparator.recompiled = recomp

        xfn_comp = self.comparator._compare_xfn_tables()

        self.assertFalse(xfn_comp.identical)
        self.assertTrue(any(
            "signature" in d.description.lower()
            for d in xfn_comp.differences
        ))


class TestCompareFilesIntegration(unittest.TestCase):
    """Test compare_files method with mocked file loading."""

    def setUp(self):
        """Set up test fixtures."""
        self.comparator = BytecodeComparator()

    @patch('vcdecomp.validation.bytecode_compare.SCRFile.load')
    def test_compare_files_success(self, mock_load):
        """Test successful file comparison."""
        # Create mock SCR files
        mock_orig = Mock(spec=SCRFile)
        mock_orig.raw_data = b"\x00\x01\x02"
        mock_orig.header = Mock(spec=SCRHeader)
        mock_orig.header.enter_ip = 0
        mock_orig.header.enter_size = 0
        mock_orig.header.ret_size = 0
        mock_orig.header.enter_array = []
        mock_orig.header.size_bytes = 12
        mock_orig.data = Mock(spec=DataSegment)
        mock_orig.data.data_count = 0
        mock_orig.data.raw_data = b""
        mock_orig.data.size_bytes = 4
        mock_orig.data.strings = {}
        mock_orig.global_pointers = []
        mock_orig.code = Mock(spec=CodeSegment)
        mock_orig.code.instructions = []
        mock_orig.code.instruction_count = 0
        mock_orig.xfn = Mock(spec=XFNTable)
        mock_orig.xfn.entries = []
        mock_orig.xfn.count = 0

        mock_recomp = Mock(spec=SCRFile)
        mock_recomp.raw_data = b"\x00\x01\x02"
        mock_recomp.header = Mock(spec=SCRHeader)
        mock_recomp.header.enter_ip = 0
        mock_recomp.header.enter_size = 0
        mock_recomp.header.ret_size = 0
        mock_recomp.header.enter_array = []
        mock_recomp.header.size_bytes = 12
        mock_recomp.data = Mock(spec=DataSegment)
        mock_recomp.data.data_count = 0
        mock_recomp.data.raw_data = b""
        mock_recomp.data.size_bytes = 4
        mock_recomp.data.strings = {}
        mock_recomp.global_pointers = []
        mock_recomp.code = Mock(spec=CodeSegment)
        mock_recomp.code.instructions = []
        mock_recomp.code.instruction_count = 0
        mock_recomp.xfn = Mock(spec=XFNTable)
        mock_recomp.xfn.entries = []
        mock_recomp.xfn.count = 0

        mock_load.side_effect = [mock_orig, mock_recomp]

        result = self.comparator.compare_files("original.scr", "recompiled.scr")

        self.assertTrue(result.is_valid)
        self.assertIsNone(result.load_error)
        self.assertTrue(result.identical)

    @patch('vcdecomp.validation.bytecode_compare.SCRFile.load')
    def test_compare_files_load_error_original(self, mock_load):
        """Test handling of original file load error."""
        mock_load.side_effect = FileNotFoundError("File not found")

        result = self.comparator.compare_files("missing.scr", "recompiled.scr")

        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.load_error)
        self.assertIn("original", result.load_error.lower())

    @patch('vcdecomp.validation.bytecode_compare.SCRFile.load')
    def test_compare_files_load_error_recompiled(self, mock_load):
        """Test handling of recompiled file load error."""
        mock_orig = Mock(spec=SCRFile)
        mock_load.side_effect = [mock_orig, FileNotFoundError("File not found")]

        result = self.comparator.compare_files("original.scr", "missing.scr")

        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.load_error)
        self.assertIn("recompiled", result.load_error.lower())


class TestDifferenceCategorization(unittest.TestCase):
    """Test difference categorization system."""

    def test_categorize_semantic_difference(self):
        """Test categorization of semantic differences."""
        diff = Difference(
            type=DifferenceType.HEADER,
            severity=DifferenceSeverity.CRITICAL,
            description="Entry point differs",
            location="header.enter_ip",
            original_value=0,
            recompiled_value=4
        )

        categorized = categorize_differences([diff])
        self.assertEqual(len(categorized), 1)
        self.assertEqual(categorized[0].category, DifferenceCategory.SEMANTIC)

    def test_categorize_cosmetic_difference(self):
        """Test categorization of cosmetic differences."""
        diff = Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.MINOR,
            description="Data reordering detected",
            location="data[0x10]",
            details={"category": "reordering"}
        )

        categorized = categorize_differences([diff])
        self.assertEqual(len(categorized), 1)
        self.assertEqual(categorized[0].category, DifferenceCategory.COSMETIC)

    def test_categorize_optimization_difference(self):
        """Test categorization of optimization differences."""
        diff = Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.INFO,
            description="Equivalent instruction pattern: INC vs ADD 1",
            location="instruction[5]",
            details={"equivalent": True}
        )

        categorized = categorize_differences([diff])
        self.assertEqual(len(categorized), 1)
        self.assertEqual(categorized[0].category, DifferenceCategory.OPTIMIZATION)

    def test_get_semantic_differences(self):
        """Test filtering semantic differences."""
        diffs = [
            Difference(
                type=DifferenceType.HEADER,
                severity=DifferenceSeverity.CRITICAL,
                description="Entry point differs",
                location="header"
            ),
            Difference(
                type=DifferenceType.DATA,
                severity=DifferenceSeverity.MINOR,
                description="Padding difference",
                location="data",
                details={"category": "alignment"}
            ),
        ]

        categorized = categorize_differences(diffs)
        semantic = get_semantic_differences(categorized)

        self.assertEqual(len(semantic), 1)
        self.assertEqual(semantic[0].difference.type, DifferenceType.HEADER)

    def test_get_cosmetic_differences(self):
        """Test filtering cosmetic differences."""
        diffs = [
            Difference(
                type=DifferenceType.HEADER,
                severity=DifferenceSeverity.CRITICAL,
                description="Entry point differs",
                location="header"
            ),
            Difference(
                type=DifferenceType.DATA,
                severity=DifferenceSeverity.MINOR,
                description="Padding difference",
                location="data",
                details={"category": "alignment"}
            ),
        ]

        categorized = categorize_differences(diffs)
        cosmetic = get_cosmetic_differences(categorized)

        self.assertEqual(len(cosmetic), 1)
        self.assertEqual(cosmetic[0].difference.type, DifferenceType.DATA)


class TestDifferenceCategorizer(unittest.TestCase):
    """Test DifferenceCategorizer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.categorizer = DifferenceCategorizer()

    def test_categorize_by_explicit_category(self):
        """Test categorization using explicit category in details."""
        diff = Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.INFO,
            description="Some difference",
            location="data[0]",
            details={"category": "alignment"}
        )

        categorized = self.categorizer.categorize(diff)
        self.assertEqual(categorized.category, DifferenceCategory.COSMETIC)

    def test_categorize_critical_semantic(self):
        """Test that critical differences are categorized as semantic."""
        diff = Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.CRITICAL,
            description="Wrong opcode",
            location="code[0]"
        )

        categorized = self.categorizer.categorize(diff)
        self.assertEqual(categorized.category, DifferenceCategory.SEMANTIC)

    def test_categorize_equivalent_optimization(self):
        """Test that equivalent patterns are categorized as optimization."""
        diff = Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.INFO,
            description="Equivalent instruction",
            location="code[0]",
            details={"equivalent": True}
        )

        categorized = self.categorizer.categorize(diff)
        self.assertEqual(categorized.category, DifferenceCategory.OPTIMIZATION)

    def test_categorize_alignment_cosmetic(self):
        """Test that alignment differences are cosmetic."""
        diff = Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.INFO,
            description="Alignment padding",
            location="data[0]"
        )

        categorized = self.categorizer.categorize(diff)
        self.assertEqual(categorized.category, DifferenceCategory.COSMETIC)


if __name__ == '__main__':
    unittest.main()
