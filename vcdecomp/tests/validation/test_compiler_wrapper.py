"""
Unit tests for compiler wrapper classes.

Tests the wrapper classes for Vietcong script compilation tools:
- BaseCompiler: Base functionality (subprocess execution, cleanup)
- SCMPWrapper: Full compilation chain orchestrator
- SPPWrapper: Preprocessor
- SCCWrapper: Compiler (C to assembly)
- SASMWrapper: Assembler (assembly to bytecode)

Uses mocked subprocess calls for fast, deterministic testing.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import tempfile
import shutil
import subprocess
from typing import Optional

from vcdecomp.validation.compiler_wrapper import (
    BaseCompiler,
    SCMPWrapper,
    SPPWrapper,
    SCCWrapper,
    SASMWrapper,
    ProcessResult,
    _parse_error_file,
)
from vcdecomp.validation.compilation_types import (
    CompilationResult,
    CompilationError,
    CompilationStage,
    ErrorSeverity,
)


class TestBaseCompiler(unittest.TestCase):
    """Test BaseCompiler functionality."""

    def setUp(self):
        """Create temporary executable for testing."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_compiler_"))
        self.executable = self.temp_dir / "test_compiler.exe"
        self.executable.touch()

    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_init_with_valid_executable(self):
        """Test initialization with valid executable path."""
        compiler = BaseCompiler(
            executable_path=self.executable,
            timeout=30,
            cleanup_on_success=True,
            cleanup_on_failure=False,
        )

        self.assertEqual(compiler.executable_path, self.executable)
        self.assertEqual(compiler.timeout, 30)
        self.assertTrue(compiler.cleanup_on_success)
        self.assertFalse(compiler.cleanup_on_failure)

    def test_init_with_invalid_executable(self):
        """Test initialization with non-existent executable raises error."""
        non_existent = self.temp_dir / "nonexistent.exe"

        with self.assertRaises(FileNotFoundError) as context:
            BaseCompiler(executable_path=non_existent)

        self.assertIn("not found", str(context.exception).lower())

    def test_working_dir_creation(self):
        """Test automatic working directory creation."""
        compiler = BaseCompiler(
            executable_path=self.executable,
            working_dir=None,
        )

        # Access working_dir to trigger creation
        work_dir = compiler.working_dir

        self.assertTrue(work_dir.exists())
        self.assertTrue(work_dir.is_dir())
        self.assertTrue(compiler._temp_dir_created)

    def test_working_dir_provided(self):
        """Test using provided working directory."""
        work_dir = self.temp_dir / "custom_work"
        work_dir.mkdir()

        compiler = BaseCompiler(
            executable_path=self.executable,
            working_dir=work_dir,
        )

        self.assertEqual(compiler.working_dir, work_dir)
        self.assertFalse(compiler._temp_dir_created)

    @patch('subprocess.run')
    def test_execute_success(self, mock_run):
        """Test successful subprocess execution."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Success output",
            stderr="",
        )

        compiler = BaseCompiler(executable_path=self.executable)
        result = compiler._execute(["arg1", "arg2"])

        self.assertTrue(result.success)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Success output")
        self.assertEqual(result.stderr, "")

    @patch('subprocess.run')
    def test_execute_failure(self, mock_run):
        """Test failed subprocess execution."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error: compilation failed",
        )

        compiler = BaseCompiler(executable_path=self.executable)
        result = compiler._execute(["arg1"])

        self.assertFalse(result.success)
        self.assertEqual(result.returncode, 1)
        self.assertIn("compilation failed", result.stderr)

    @patch('subprocess.run')
    def test_execute_timeout(self, mock_run):
        """Test subprocess timeout handling."""
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["test.exe"],
            timeout=5,
            output=b"partial output",
            stderr=None,
        )

        compiler = BaseCompiler(executable_path=self.executable, timeout=5)
        result = compiler._execute(["arg1"])

        self.assertFalse(result.success)
        self.assertEqual(result.returncode, -1)
        self.assertIn("timed out", result.stderr.lower())

    @patch('subprocess.run')
    def test_execute_exception(self, mock_run):
        """Test subprocess execution exception handling."""
        mock_run.side_effect = OSError("Permission denied")

        compiler = BaseCompiler(executable_path=self.executable)
        result = compiler._execute(["arg1"])

        self.assertFalse(result.success)
        self.assertEqual(result.returncode, -1)
        self.assertIn("Permission denied", result.stderr)

    def test_cleanup_force(self):
        """Test forced cleanup of temporary directory."""
        compiler = BaseCompiler(
            executable_path=self.executable,
            working_dir=None,
            cleanup_on_success=False,
            cleanup_on_failure=False,
        )

        work_dir = compiler.working_dir
        self.assertTrue(work_dir.exists())

        # Force cleanup
        compiler.cleanup(force=True)

        self.assertFalse(work_dir.exists())

    def test_cleanup_on_success(self):
        """Test cleanup on successful compilation."""
        compiler = BaseCompiler(
            executable_path=self.executable,
            working_dir=None,
            cleanup_on_success=True,
        )

        work_dir = compiler.working_dir
        self.assertTrue(work_dir.exists())

        compiler._cleanup_on_result(success=True)

        self.assertFalse(work_dir.exists())

    def test_no_cleanup_on_success(self):
        """Test no cleanup when disabled."""
        compiler = BaseCompiler(
            executable_path=self.executable,
            working_dir=None,
            cleanup_on_success=False,
        )

        work_dir = compiler.working_dir
        self.assertTrue(work_dir.exists())

        compiler._cleanup_on_result(success=True)

        self.assertTrue(work_dir.exists())

    def test_cleanup_on_failure(self):
        """Test cleanup on failed compilation."""
        compiler = BaseCompiler(
            executable_path=self.executable,
            working_dir=None,
            cleanup_on_failure=True,
        )

        work_dir = compiler.working_dir
        self.assertTrue(work_dir.exists())

        compiler._cleanup_on_result(success=False)

        self.assertFalse(work_dir.exists())

    def test_context_manager_success(self):
        """Test context manager with successful operation."""
        with BaseCompiler(
            executable_path=self.executable,
            working_dir=None,
        ) as compiler:
            work_dir = compiler.working_dir
            self.assertTrue(work_dir.exists())

        # After exit, directory should still exist (not auto-cleaned)
        self.assertTrue(work_dir.exists())

    def test_context_manager_exception(self):
        """Test context manager with exception."""
        compiler = BaseCompiler(
            executable_path=self.executable,
            working_dir=None,
            cleanup_on_failure=True,
        )

        work_dir = None
        with self.assertRaises(ValueError):
            with compiler:
                work_dir = compiler.working_dir
                self.assertTrue(work_dir.exists())
                raise ValueError("Test error")

        # After exception, should cleanup if cleanup_on_failure=True
        self.assertFalse(work_dir.exists())


class TestErrorFileParsing(unittest.TestCase):
    """Test error file parsing functionality."""

    def setUp(self):
        """Create temporary directory for error files."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_errors_"))

    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_parse_error_file_format1(self):
        """Test parsing error format: file.c(123): error: message."""
        error_file = self.temp_dir / "test.err"
        error_file.write_text("source.c(42): error: undefined variable 'foo'\n")

        errors = _parse_error_file(error_file, CompilationStage.SCC)

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].stage, CompilationStage.SCC)
        self.assertEqual(errors[0].severity, ErrorSeverity.ERROR)
        self.assertEqual(errors[0].line, 42)
        self.assertIn("undefined variable", errors[0].message)

    def test_parse_error_file_format2(self):
        """Test parsing error format: file.c:123:45: error: message."""
        error_file = self.temp_dir / "test.err"
        error_file.write_text("source.c:42:10: error: syntax error\n")

        errors = _parse_error_file(error_file, CompilationStage.SPP)

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].line, 42)
        self.assertEqual(errors[0].column, 10)
        self.assertIn("syntax error", errors[0].message)

    def test_parse_error_file_warning(self):
        """Test parsing warning messages."""
        error_file = self.temp_dir / "test.err"
        error_file.write_text("source.c(10): warning: unused variable 'x'\n")

        errors = _parse_error_file(error_file, CompilationStage.SCC)

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].severity, ErrorSeverity.WARNING)

    def test_parse_error_file_fatal(self):
        """Test parsing fatal error messages."""
        error_file = self.temp_dir / "test.err"
        error_file.write_text("source.c(1): fatal: cannot open file\n")

        errors = _parse_error_file(error_file, CompilationStage.SPP)

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].severity, ErrorSeverity.FATAL)

    def test_parse_error_file_nonexistent(self):
        """Test parsing non-existent error file."""
        error_file = self.temp_dir / "nonexistent.err"

        errors = _parse_error_file(error_file, CompilationStage.SASM)

        self.assertEqual(len(errors), 0)

    def test_parse_error_file_empty(self):
        """Test parsing empty error file."""
        error_file = self.temp_dir / "empty.err"
        error_file.write_text("")

        errors = _parse_error_file(error_file, CompilationStage.SASM)

        self.assertEqual(len(errors), 0)

    def test_parse_error_file_unstructured(self):
        """Test parsing unstructured error messages."""
        error_file = self.temp_dir / "test.err"
        error_file.write_text("Something went wrong!\nCannot continue.")

        errors = _parse_error_file(error_file, CompilationStage.SCC)

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].severity, ErrorSeverity.ERROR)
        self.assertIn("Something went wrong", errors[0].message)


class TestSCMPWrapper(unittest.TestCase):
    """Test SCMPWrapper functionality."""

    def setUp(self):
        """Create temporary directories and files for testing."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_scmp_"))
        self.compiler_dir = self.temp_dir / "compiler"
        self.compiler_dir.mkdir()

        # Create mock executables
        self.scmp_exe = self.compiler_dir / "scmp.exe"
        self.scmp_exe.touch()

        # Create include directory
        self.inc_dir = self.compiler_dir / "inc"
        self.inc_dir.mkdir()

        # Create test source file
        self.source_file = self.temp_dir / "test.c"
        self.source_file.write_text("void main() { }")

        # Create output path
        self.output_scr = self.temp_dir / "test.scr"

    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    @patch.object(SCMPWrapper, '_execute')
    def test_compile_success(self, mock_execute):
        """Test successful compilation."""
        # Mock successful execution
        mock_execute.return_value = ProcessResult(
            returncode=0,
            stdout="Compilation successful",
            stderr="",
            success=True,
        )

        # Create the output file that would be created by scmp
        work_scr = self.compiler_dir / "test.scr"
        work_scr.write_bytes(b"MOCK_SCR_DATA")

        wrapper = SCMPWrapper(executable_path=self.scmp_exe)
        result = wrapper.compile(self.source_file, self.output_scr)

        self.assertTrue(result.success)
        self.assertEqual(result.stage, CompilationStage.SCMP)
        self.assertIsNotNone(result.output_file)
        self.assertTrue(self.output_scr.exists())

    @patch.object(SCMPWrapper, '_execute')
    def test_compile_missing_source(self, mock_execute):
        """Test compilation with missing source file."""
        non_existent = self.temp_dir / "nonexistent.c"

        wrapper = SCMPWrapper(executable_path=self.scmp_exe)
        result = wrapper.compile(non_existent, self.output_scr)

        self.assertFalse(result.success)
        self.assertEqual(result.stage, CompilationStage.SCMP)
        self.assertTrue(result.has_errors)
        self.assertIn("not found", result.errors[0].message.lower())

    @patch.object(SCMPWrapper, '_execute')
    def test_compile_with_errors(self, mock_execute):
        """Test compilation with errors."""
        # Mock failed execution
        mock_execute.return_value = ProcessResult(
            returncode=-2,
            stdout="",
            stderr="SPP error",
            success=False,
        )

        # Create error file
        error_file = self.compiler_dir / "spp.err"
        error_file.write_text("test.c(10): error: syntax error\n")

        wrapper = SCMPWrapper(executable_path=self.scmp_exe)
        result = wrapper.compile(self.source_file, self.output_scr)

        self.assertFalse(result.success)
        self.assertTrue(result.has_errors)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].stage, CompilationStage.SPP)

    @patch.object(SCMPWrapper, '_execute')
    def test_compile_with_header(self, mock_execute):
        """Test compilation with header file output."""
        mock_execute.return_value = ProcessResult(
            returncode=0,
            stdout="",
            stderr="",
            success=True,
        )

        # Create output files
        work_scr = self.compiler_dir / "test.scr"
        work_scr.write_bytes(b"SCR")
        work_header = self.compiler_dir / "test.h"
        work_header.write_text("// header")

        output_header = self.temp_dir / "test.h"

        wrapper = SCMPWrapper(executable_path=self.scmp_exe)
        result = wrapper.compile(self.source_file, self.output_scr, output_header)

        self.assertTrue(result.success)
        self.assertTrue(output_header.exists())

    @patch.object(SCMPWrapper, '_execute')
    def test_compile_with_includes(self, mock_execute):
        """Test compilation with include directories."""
        mock_execute.return_value = ProcessResult(
            returncode=0,
            stdout="",
            stderr="",
            success=True,
        )

        # Create include files
        include_dir = self.temp_dir / "includes"
        include_dir.mkdir()
        header_file = include_dir / "test_header.h"
        header_file.write_text("#define FOO 42")

        # Create output
        work_scr = self.compiler_dir / "test.scr"
        work_scr.write_bytes(b"SCR")

        wrapper = SCMPWrapper(
            executable_path=self.scmp_exe,
            include_dirs=[include_dir],
        )
        result = wrapper.compile(self.source_file, self.output_scr)

        self.assertTrue(result.success)
        # Check that header was copied to inc directory
        copied_header = self.inc_dir / "test_header.h"
        self.assertTrue(copied_header.exists())


class TestSPPWrapper(unittest.TestCase):
    """Test SPPWrapper functionality."""

    def setUp(self):
        """Create temporary directories and files for testing."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_spp_"))
        self.spp_exe = self.temp_dir / "spp.exe"
        self.spp_exe.touch()

        self.source_file = self.temp_dir / "test.c"
        self.source_file.write_text("#define FOO 42\nvoid main() { int x = FOO; }")

        self.output_file = self.temp_dir / "output.c"

    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    @patch.object(SPPWrapper, '_execute')
    def test_preprocess_success(self, mock_execute):
        """Test successful preprocessing."""
        mock_execute.return_value = ProcessResult(
            returncode=0,
            stdout="Preprocessing successful",
            stderr="",
            success=True,
        )

        wrapper = SPPWrapper(executable_path=self.spp_exe)

        # Create the output file that would be created by spp
        work_output = wrapper.working_dir / "spp.c"
        work_output.write_text("void main() { int x = 42; }")

        result = wrapper.preprocess(self.source_file, self.output_file)

        self.assertTrue(result.success)
        self.assertEqual(result.stage, CompilationStage.SPP)
        self.assertTrue(self.output_file.exists())

    @patch.object(SPPWrapper, '_execute')
    def test_preprocess_missing_source(self, mock_execute):
        """Test preprocessing with missing source file."""
        non_existent = self.temp_dir / "nonexistent.c"

        wrapper = SPPWrapper(executable_path=self.spp_exe)
        result = wrapper.preprocess(non_existent, self.output_file)

        self.assertFalse(result.success)
        self.assertTrue(result.has_errors)

    @patch.object(SPPWrapper, '_execute')
    def test_preprocess_with_includes(self, mock_execute):
        """Test preprocessing with include path."""
        mock_execute.return_value = ProcessResult(
            returncode=0,
            stdout="",
            stderr="",
            success=True,
        )

        include_path = self.temp_dir / "includes"
        include_path.mkdir()

        wrapper = SPPWrapper(
            executable_path=self.spp_exe,
            include_path=include_path,
        )

        work_output = wrapper.working_dir / "spp.c"
        work_output.write_text("preprocessed")

        result = wrapper.preprocess(self.source_file, self.output_file)

        self.assertTrue(result.success)
        # Check that include_path was passed in args
        call_args = mock_execute.call_args[0][0]
        self.assertIn(str(include_path.absolute()), call_args)


class TestSCCWrapper(unittest.TestCase):
    """Test SCCWrapper functionality."""

    def setUp(self):
        """Create temporary directories and files for testing."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_scc_"))
        self.scc_exe = self.temp_dir / "scc.exe"
        self.scc_exe.touch()

        self.source_file = self.temp_dir / "preprocessed.c"
        self.source_file.write_text("void main() { }")

        self.output_file = self.temp_dir / "output.sca"

    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    @patch.object(SCCWrapper, '_execute')
    def test_compile_success(self, mock_execute):
        """Test successful compilation to assembly."""
        mock_execute.return_value = ProcessResult(
            returncode=0,
            stdout="Compilation successful",
            stderr="",
            success=True,
        )

        wrapper = SCCWrapper(executable_path=self.scc_exe)

        # Create the output file
        work_output = wrapper.working_dir / "sasm.sca"
        work_output.write_text("ASSEMBLY CODE")

        result = wrapper.compile(self.source_file, self.output_file)

        self.assertTrue(result.success)
        self.assertEqual(result.stage, CompilationStage.SCC)
        self.assertTrue(self.output_file.exists())

    @patch.object(SCCWrapper, '_execute')
    def test_compile_with_debug(self, mock_execute):
        """Test compilation with debug mode enabled."""
        mock_execute.return_value = ProcessResult(
            returncode=0,
            stdout="",
            stderr="",
            success=True,
        )

        wrapper = SCCWrapper(
            executable_path=self.scc_exe,
            debug_mode=True,
        )

        work_output = wrapper.working_dir / "sasm.sca"
        work_output.write_text("ASSEMBLY")

        result = wrapper.compile(self.source_file, self.output_file)

        self.assertTrue(result.success)
        # Check that "dbg" flag was passed
        call_args = mock_execute.call_args[0][0]
        self.assertIn("dbg", call_args)


class TestSASMWrapper(unittest.TestCase):
    """Test SASMWrapper functionality."""

    def setUp(self):
        """Create temporary directories and files for testing."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_sasm_"))
        self.sasm_exe = self.temp_dir / "sasm.exe"
        self.sasm_exe.touch()

        self.source_file = self.temp_dir / "input.sca"
        self.source_file.write_text("ASSEMBLY CODE")

        self.output_scr = self.temp_dir / "output.scr"

    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    @patch.object(SASMWrapper, '_execute')
    def test_assemble_success(self, mock_execute):
        """Test successful assembly to bytecode."""
        mock_execute.return_value = ProcessResult(
            returncode=0,
            stdout="Assembly successful",
            stderr="",
            success=True,
        )

        wrapper = SASMWrapper(executable_path=self.sasm_exe)

        # Create the output file
        work_scr = wrapper.working_dir / "output.scr"
        work_scr.write_bytes(b"BYTECODE")

        result = wrapper.assemble(self.source_file, self.output_scr)

        self.assertTrue(result.success)
        self.assertEqual(result.stage, CompilationStage.SASM)
        self.assertTrue(self.output_scr.exists())

    @patch.object(SASMWrapper, '_execute')
    def test_assemble_with_header(self, mock_execute):
        """Test assembly with header file output."""
        mock_execute.return_value = ProcessResult(
            returncode=0,
            stdout="",
            stderr="",
            success=True,
        )

        wrapper = SASMWrapper(executable_path=self.sasm_exe)

        # Create output files
        work_scr = wrapper.working_dir / "output.scr"
        work_scr.write_bytes(b"BYTECODE")
        work_header = wrapper.working_dir / "output.h"
        work_header.write_text("// header")

        output_header = self.temp_dir / "output.h"

        result = wrapper.assemble(self.source_file, self.output_scr, output_header)

        self.assertTrue(result.success)
        self.assertTrue(output_header.exists())

    @patch.object(SASMWrapper, '_execute')
    def test_assemble_missing_source(self, mock_execute):
        """Test assembly with missing source file."""
        non_existent = self.temp_dir / "nonexistent.sca"

        wrapper = SASMWrapper(executable_path=self.sasm_exe)
        result = wrapper.assemble(non_existent, self.output_scr)

        self.assertFalse(result.success)
        self.assertTrue(result.has_errors)


if __name__ == '__main__':
    unittest.main()
