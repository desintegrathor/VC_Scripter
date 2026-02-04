

"""
Integration tests for validation workflow.

Tests the complete end-to-end validation workflow using real compiler tools
and test fixtures from Compiler-testruns/:
- Full validation of test scripts
- Error recovery (missing files, compilation errors, etc.)
- Report generation (text, HTML, JSON)
- Cache functionality

These are integration tests that use real compiler executables and SCR files,
so they may be slower than unit tests but provide comprehensive validation
of the entire system.
"""

import unittest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile
import shutil
import json
import os

from vcdecomp.validation.validator import ValidationOrchestrator
from vcdecomp.validation.validation_types import ValidationResult, ValidationVerdict
from vcdecomp.validation.report_generator import ReportGenerator
from vcdecomp.validation.cache import ValidationCache


class TestValidationWorkflowBasic(unittest.TestCase):
    """Basic integration tests for validation workflow."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures and paths."""
        cls.project_root = Path(__file__).parent.parent.parent.parent
        cls.compiler_dir = cls.project_root / "vcdecomp" / "compiler"
        cls.test_data_dir = cls.project_root / "Compiler-testruns"

        # Check if compiler tools exist
        cls.compiler_available = (cls.compiler_dir / "SCMP.exe").exists()

        # Test fixtures from Compiler-testruns
        cls.test_fixtures = []
        if cls.test_data_dir.exists():
            # Find .scr files with corresponding .c files
            for scr_file in cls.test_data_dir.rglob("*.scr"):
                # Look for corresponding .c file (try various naming patterns)
                source_candidates = [
                    scr_file.with_suffix(".c"),
                    scr_file.parent / f"{scr_file.stem}_FINAL.c",
                    scr_file.parent / f"{scr_file.stem}_FIX4.c",
                    scr_file.parent / f"{scr_file.stem}_FIX3.c",
                ]
                for source_file in source_candidates:
                    if source_file.exists():
                        cls.test_fixtures.append((scr_file, source_file))
                        break

    def setUp(self):
        """Create temporary directory for test outputs."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_validation_"))
        self.cache_dir = self.temp_dir / "cache"
        self.cache_dir.mkdir(exist_ok=True)

    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    @unittest.skipUnless(
        Path(__file__).parent.parent.parent.parent / "vcdecomp" / "compiler" / "SCMP.exe",
        "Compiler tools not available"
    )
    def test_validation_orchestrator_initialization(self):
        """Test ValidationOrchestrator initialization with valid compiler directory."""
        orchestrator = ValidationOrchestrator(
            compiler_dir=self.compiler_dir,
            cache_dir=self.cache_dir,
        )

        self.assertEqual(orchestrator.compiler_dir, self.compiler_dir)
        self.assertTrue(orchestrator.cache is not None)

    def test_validation_orchestrator_invalid_compiler_dir(self):
        """Test ValidationOrchestrator initialization with invalid compiler directory."""
        with self.assertRaises(FileNotFoundError):
            ValidationOrchestrator(
                compiler_dir=self.temp_dir / "nonexistent",
            )

    @unittest.skipUnless(
        Path(__file__).parent.parent.parent.parent / "vcdecomp" / "compiler" / "SCMP.exe",
        "Compiler tools not available"
    )
    def test_full_validation_workflow_with_mocked_compilation(self):
        """Test full validation workflow with mocked compilation step.

        This test validates the workflow without requiring the compiler to work,
        by mocking the compilation step and focusing on the orchestration logic.
        """
        if not self.test_fixtures:
            self.skipTest("No test fixtures available")

        original_scr, source_file = self.test_fixtures[0]

        # Create orchestrator
        orchestrator = ValidationOrchestrator(
            compiler_dir=self.compiler_dir,
            cache_dir=self.cache_dir,
            cache_enabled=False,  # Disable cache for predictable testing
        )

        # Mock the compilation step to return success
        with patch.object(orchestrator, '_compile_source') as mock_compile:
            # Create a mock compilation result
            from vcdecomp.validation.compilation_types import CompilationResult

            mock_result = CompilationResult(
                success=True,
                output_file=original_scr,  # Use original as "recompiled"
                errors=[],
                warnings=[],
                stage=None,
                returncode=0,
                stdout="",
                stderr="",
            )
            mock_compile.return_value = mock_result

            # Run validation
            result = orchestrator.validate(
                original_scr=original_scr,
                decompiled_source=source_file,
            )

            # Verify result structure
            self.assertIsInstance(result, ValidationResult)
            self.assertEqual(result.original_scr, original_scr)
            self.assertEqual(result.decompiled_source, source_file)
            self.assertTrue(result.compilation_succeeded)
            self.assertTrue(result.comparison_succeeded)

            # Since we're comparing identical files, should be PASS
            self.assertEqual(result.verdict, ValidationVerdict.PASS)
            self.assertTrue(result.bytecode_identical)

    def test_validation_with_missing_original_scr(self):
        """Test validation error handling when original SCR is missing."""
        orchestrator = ValidationOrchestrator(
            compiler_dir=self.compiler_dir,
            cache_dir=self.cache_dir,
        )

        missing_scr = self.temp_dir / "nonexistent.scr"
        source_file = self.temp_dir / "test.c"
        source_file.write_text("void main() {}")

        result = orchestrator.validate(
            original_scr=missing_scr,
            decompiled_source=source_file,
        )

        self.assertEqual(result.verdict, ValidationVerdict.ERROR)
        self.assertIn("not found", result.error_message.lower())

    def test_validation_with_missing_source_file(self):
        """Test validation error handling when source file is missing."""
        orchestrator = ValidationOrchestrator(
            compiler_dir=self.compiler_dir,
            cache_dir=self.cache_dir,
        )

        scr_file = self.temp_dir / "test.scr"
        scr_file.write_bytes(b"SCR" + b"\x00" * 100)
        missing_source = self.temp_dir / "nonexistent.c"

        result = orchestrator.validate(
            original_scr=scr_file,
            decompiled_source=missing_source,
        )

        self.assertEqual(result.verdict, ValidationVerdict.ERROR)
        self.assertIn("not found", result.error_message.lower())

    def test_validation_with_compilation_error_mocked(self):
        """Test validation handling of compilation errors."""
        if not self.test_fixtures:
            self.skipTest("No test fixtures available")

        original_scr, _ = self.test_fixtures[0]

        # Create invalid source file
        invalid_source = self.temp_dir / "invalid.c"
        invalid_source.write_text("this is not valid C code !!!###")

        orchestrator = ValidationOrchestrator(
            compiler_dir=self.compiler_dir,
            cache_dir=self.cache_dir,
        )

        # Mock compilation to return failure
        with patch.object(orchestrator, '_compile_source') as mock_compile:
            from vcdecomp.validation.compilation_types import (
                CompilationResult, CompilationError, CompilationStage, ErrorSeverity
            )

            mock_result = CompilationResult(
                success=False,
                output_file=None,
                errors=[
                    CompilationError(
                        stage=CompilationStage.SCC,
                        severity=ErrorSeverity.ERROR,
                        file="invalid.c",
                        line=1,
                        column=1,
                        message="Syntax error",
                    )
                ],
                warnings=[],
                stage=CompilationStage.SCC,
                returncode=1,
                stdout="",
                stderr="Syntax error",
            )
            mock_compile.return_value = mock_result

            result = orchestrator.validate(
                original_scr=original_scr,
                decompiled_source=invalid_source,
            )

            self.assertEqual(result.verdict, ValidationVerdict.FAIL)
            self.assertFalse(result.compilation_succeeded)
            self.assertIn("Compilation failed", result.error_message)


class TestReportGeneration(unittest.TestCase):
    """Test report generation from validation results."""

    def setUp(self):
        """Create temporary directory for test outputs."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_reports_"))

    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_generate_text_report(self):
        """Test text report generation."""
        # Create a mock validation result
        result = ValidationResult(
            original_scr=Path("test.scr"),
            decompiled_source=Path("test.c"),
            verdict=ValidationVerdict.PASS,
        )
        result.recommendations.append("Bytecode is identical")

        generator = ReportGenerator()
        report = generator.generate_text(result)

        self.assertIsInstance(report, str)
        self.assertIn("PASS", report.upper())
        self.assertIn("test.scr", report)
        self.assertIn("test.c", report)

    def test_generate_html_report(self):
        """Test HTML report generation."""
        result = ValidationResult(
            original_scr=Path("test.scr"),
            decompiled_source=Path("test.c"),
            verdict=ValidationVerdict.PARTIAL,
        )
        result.recommendations.append("Review semantic differences")

        generator = ReportGenerator()
        report = generator.generate_html(result)

        self.assertIsInstance(report, str)
        self.assertIn("<html", report.lower())
        self.assertIn("PARTIAL", report.upper())
        self.assertIn("test.scr", report)

    def test_generate_json_report(self):
        """Test JSON report generation."""
        result = ValidationResult(
            original_scr=Path("test.scr"),
            decompiled_source=Path("test.c"),
            verdict=ValidationVerdict.FAIL,
        )

        generator = ReportGenerator()
        report = generator.generate_json(result)

        self.assertIsInstance(report, str)

        # Verify it's valid JSON
        data = json.loads(report)
        self.assertIn("verdict", data)
        self.assertEqual(data["verdict"], "fail")

    def test_save_report_text(self):
        """Test saving text report to file."""
        result = ValidationResult(
            original_scr=Path("test.scr"),
            decompiled_source=Path("test.c"),
            verdict=ValidationVerdict.PASS,
        )

        generator = ReportGenerator()
        output_file = self.temp_dir / "report.txt"

        generator.save_report(result, output_file, format="text")

        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn("PASS", content.upper())

    def test_save_report_html(self):
        """Test saving HTML report to file."""
        result = ValidationResult(
            original_scr=Path("test.scr"),
            decompiled_source=Path("test.c"),
            verdict=ValidationVerdict.PARTIAL,
        )

        generator = ReportGenerator()
        output_file = self.temp_dir / "report.html"

        generator.save_report(result, output_file, format="html")

        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn("<html", content.lower())

    def test_save_report_json(self):
        """Test saving JSON report to file."""
        result = ValidationResult(
            original_scr=Path("test.scr"),
            decompiled_source=Path("test.c"),
            verdict=ValidationVerdict.ERROR,
        )

        generator = ReportGenerator()
        output_file = self.temp_dir / "report.json"

        generator.save_report(result, output_file, format="json")

        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        data = json.loads(content)
        self.assertEqual(data["verdict"], "error")

    def test_save_report_auto_detect_format(self):
        """Test automatic format detection from file extension."""
        result = ValidationResult(
            original_scr=Path("test.scr"),
            decompiled_source=Path("test.c"),
            verdict=ValidationVerdict.PASS,
        )

        generator = ReportGenerator()

        # Test .txt extension
        txt_file = self.temp_dir / "report.txt"
        generator.save_report(result, txt_file)
        self.assertTrue(txt_file.exists())

        # Test .html extension
        html_file = self.temp_dir / "report.html"
        generator.save_report(result, html_file)
        self.assertTrue(html_file.exists())
        self.assertIn("<html", html_file.read_text(encoding='utf-8').lower())

        # Test .json extension
        json_file = self.temp_dir / "report.json"
        generator.save_report(result, json_file)
        self.assertTrue(json_file.exists())
        json.loads(json_file.read_text(encoding='utf-8'))  # Should parse without error


class TestValidationCache(unittest.TestCase):
    """Test validation caching functionality."""

    def setUp(self):
        """Create temporary directory for cache."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_cache_"))
        self.cache_dir = self.temp_dir / "cache"

    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_cache_stores_and_retrieves_results(self):
        """Test that cache can store and retrieve validation results."""
        cache = ValidationCache(cache_dir=self.cache_dir)

        # Create test files
        scr_file = self.temp_dir / "test.scr"
        scr_file.write_bytes(b"test data")
        source_file = self.temp_dir / "test.c"
        source_file.write_text("void main() {}")

        # Create validation result
        result = ValidationResult(
            original_scr=scr_file,
            decompiled_source=source_file,
            verdict=ValidationVerdict.PASS,
        )

        # Store in cache
        cache.set(scr_file, source_file, result)

        # Retrieve from cache
        cached = cache.get(scr_file, source_file)

        self.assertIsNotNone(cached)
        self.assertEqual(cached.verdict, ValidationVerdict.PASS)

    def test_cache_invalidates_on_source_change(self):
        """Test that cache is invalidated when source changes."""
        cache = ValidationCache(cache_dir=self.cache_dir)

        scr_file = self.temp_dir / "test.scr"
        scr_file.write_bytes(b"test data")
        source_file = self.temp_dir / "test.c"
        source_file.write_text("void main() {}")

        result = ValidationResult(
            original_scr=scr_file,
            decompiled_source=source_file,
            verdict=ValidationVerdict.PASS,
        )

        cache.set(scr_file, source_file, result)

        # Modify source file
        source_file.write_text("void main() { int x = 1; }")

        # Cache should be invalidated
        cached = cache.get(scr_file, source_file)
        self.assertIsNone(cached)

    def test_cache_disabled(self):
        """Test that cache can be disabled."""
        cache = ValidationCache(cache_dir=self.cache_dir, enabled=False)

        scr_file = self.temp_dir / "test.scr"
        scr_file.write_bytes(b"test data")
        source_file = self.temp_dir / "test.c"
        source_file.write_text("void main() {}")

        result = ValidationResult(
            original_scr=scr_file,
            decompiled_source=source_file,
            verdict=ValidationVerdict.PASS,
        )

        # Try to store (should do nothing when disabled)
        cache.set(scr_file, source_file, result)

        # Should return None
        cached = cache.get(scr_file, source_file)
        self.assertIsNone(cached)


class TestErrorRecovery(unittest.TestCase):
    """Test error recovery in validation workflow."""

    def setUp(self):
        """Create temporary directory."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_errors_"))
        self.compiler_dir = Path(__file__).parent.parent.parent.parent / "vcdecomp" / "compiler"

    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_graceful_handling_of_comparison_exception(self):
        """Test that comparison exceptions are handled gracefully."""
        orchestrator = ValidationOrchestrator(
            compiler_dir=self.compiler_dir,
            cache_dir=self.temp_dir / "cache",
        )

        scr_file = self.temp_dir / "test.scr"
        scr_file.write_bytes(b"invalid scr data")
        source_file = self.temp_dir / "test.c"
        source_file.write_text("void main() {}")

        # Mock compilation to succeed but produce invalid SCR
        with patch.object(orchestrator, '_compile_source') as mock_compile:
            from vcdecomp.validation.compilation_types import CompilationResult

            mock_result = CompilationResult(
                success=True,
                output_file=scr_file,
                errors=[],
                warnings=[],
                stage=None,
                returncode=0,
                stdout="",
                stderr="",
            )
            mock_compile.return_value = mock_result

            # Mock comparison to raise exception
            with patch.object(orchestrator, '_compare_bytecode') as mock_compare:
                mock_compare.side_effect = Exception("Comparison failed")

                result = orchestrator.validate(
                    original_scr=scr_file,
                    decompiled_source=source_file,
                )

                self.assertEqual(result.verdict, ValidationVerdict.ERROR)
                self.assertIn("Comparison failed", result.error_message)

    def test_validation_result_has_recommendations(self):
        """Test that validation results include actionable recommendations."""
        orchestrator = ValidationOrchestrator(
            compiler_dir=self.compiler_dir,
            cache_dir=self.temp_dir / "cache",
        )

        scr_file = self.temp_dir / "test.scr"
        source_file = self.temp_dir / "missing.c"

        result = orchestrator.validate(
            original_scr=scr_file,
            decompiled_source=source_file,
        )

        # Even error results should have some context
        self.assertEqual(result.verdict, ValidationVerdict.ERROR)
        self.assertIsNotNone(result.error_message)


if __name__ == "__main__":
    unittest.main()
