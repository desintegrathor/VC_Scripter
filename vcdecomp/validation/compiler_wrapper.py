"""
Compiler wrapper for Vietcong script compilation tools.

Provides Python wrappers for the original Pterodon compiler executables:
- SCMP.exe - Orchestrator for full compilation chain
- SPP.exe - Preprocessor
- SCC.exe - Compiler (C to assembly)
- SASM.exe - Assembler (assembly to bytecode)
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import logging

from .compilation_types import (
    CompilationResult,
    CompilationError,
    CompilationStage,
    ErrorSeverity,
)

logger = logging.getLogger(__name__)


@dataclass
class ProcessResult:
    """Result of a subprocess execution."""
    returncode: int
    stdout: str
    stderr: str
    success: bool

    @property
    def output(self) -> str:
        """Combined stdout and stderr."""
        return self.stdout + self.stderr


class BaseCompiler:
    """
    Base class for wrapping Pterodon compiler tools.

    Handles:
    - Subprocess execution with timeout
    - stdout/stderr capture
    - Temporary working directory management
    - Resource cleanup on success or failure

    Attributes:
        executable_path: Path to the compiler executable
        working_dir: Temporary working directory for compilation
        timeout: Maximum execution time in seconds
        cleanup_on_success: Whether to cleanup temp files after success
        cleanup_on_failure: Whether to cleanup temp files after failure
    """

    def __init__(
        self,
        executable_path: Path | str,
        working_dir: Optional[Path | str] = None,
        timeout: int = 30,
        cleanup_on_success: bool = True,
        cleanup_on_failure: bool = False,
    ):
        """
        Initialize the base compiler wrapper.

        Args:
            executable_path: Path to the compiler executable
            working_dir: Working directory for compilation (creates temp if None)
            timeout: Maximum execution time in seconds
            cleanup_on_success: Whether to cleanup temp files after successful compilation
            cleanup_on_failure: Whether to cleanup temp files after failed compilation
        """
        self.executable_path = Path(executable_path)
        self._working_dir: Optional[Path] = Path(working_dir) if working_dir else None
        self._temp_dir_created = False
        self.timeout = timeout
        self.cleanup_on_success = cleanup_on_success
        self.cleanup_on_failure = cleanup_on_failure

        # Validate executable exists
        if not self.executable_path.exists():
            raise FileNotFoundError(f"Compiler executable not found: {self.executable_path}")

        logger.debug(f"Initialized {self.__class__.__name__} with executable: {self.executable_path}")

    @property
    def working_dir(self) -> Path:
        """
        Get or create the working directory.

        Returns:
            Path to the working directory
        """
        if self._working_dir is None:
            self._working_dir = Path(tempfile.mkdtemp(prefix="vcdecomp_compile_"))
            self._temp_dir_created = True
            logger.debug(f"Created temporary working directory: {self._working_dir}")
        return self._working_dir

    def _execute(
        self,
        args: List[str],
        cwd: Optional[Path] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> ProcessResult:
        """
        Execute the compiler process with given arguments.

        Args:
            args: Command line arguments (executable path will be prepended)
            cwd: Working directory for execution (defaults to self.working_dir)
            env: Environment variables (defaults to current environment)
            timeout: Timeout in seconds (defaults to self.timeout)

        Returns:
            ProcessResult with execution details

        Raises:
            subprocess.TimeoutExpired: If execution exceeds timeout
        """
        if cwd is None:
            cwd = self.working_dir

        if timeout is None:
            timeout = self.timeout

        # Build full command
        # On Windows, use just the executable name (not full path) when cwd is set
        # This matches how the .bat files work and avoids path issues
        if cwd and self.executable_path.parent == Path(cwd):
            # Executable is in the working directory, use just the name without .exe
            exe_name = self.executable_path.stem.lower()  # Gets 'scmp' from 'SCMP.exe' or 'scmp.exe'
            cmd = [exe_name] + args
        else:
            # Use full path if executable is elsewhere
            cmd = [str(self.executable_path)] + args

        import sys
        print(f"\n=== COMPILER EXECUTION DEBUG ===", file=sys.stderr)
        print(f"FULL COMMAND: {cmd}", file=sys.stderr)
        print(f"COMMAND STRING: {' '.join(cmd)}", file=sys.stderr)
        print(f"EXECUTABLE: {self.executable_path}", file=sys.stderr)
        print(f"EXECUTABLE EXISTS: {self.executable_path.exists()}", file=sys.stderr)
        print(f"WORKING DIR: {cwd}", file=sys.stderr)
        print(f"ENV: {env}", file=sys.stderr)
        print(f"================================\n", file=sys.stderr)

        logger.debug(f"Executing: {' '.join(cmd)}")
        logger.debug(f"Working directory: {cwd}")

        try:
            # Execute process
            # Use shell=True on Windows to properly handle .exe files
            result = subprocess.run(
                cmd,
                cwd=str(cwd),
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout,
                errors='replace',  # Handle encoding errors gracefully
                shell=True,  # Required for Windows .exe executables
            )

            success = result.returncode == 0

            print(f"\n=== COMPILER EXECUTION RESULT ===", file=sys.stderr)
            print(f"Return code: {result.returncode}", file=sys.stderr)
            print(f"STDOUT: {result.stdout[:200] if result.stdout else '(empty)'}", file=sys.stderr)
            print(f"STDERR: {result.stderr[:200] if result.stderr else '(empty)'}", file=sys.stderr)
            print(f"=================================\n", file=sys.stderr)

            logger.debug(f"Process exited with code: {result.returncode}")
            if not success:
                logger.warning(f"Process failed: {result.stderr}")

            return ProcessResult(
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                success=success,
            )

        except subprocess.TimeoutExpired as e:
            logger.error(f"Process timed out after {timeout} seconds")
            # Return a ProcessResult with timeout information
            return ProcessResult(
                returncode=-1,
                stdout=e.stdout.decode('utf-8', errors='replace') if e.stdout else "",
                stderr=f"Process timed out after {timeout} seconds",
                success=False,
            )
        except Exception as e:
            logger.error(f"Process execution failed: {e}")
            return ProcessResult(
                returncode=-1,
                stdout="",
                stderr=f"Process execution failed: {str(e)}",
                success=False,
            )

    def cleanup(self, force: bool = False) -> None:
        """
        Clean up temporary working directory.

        Args:
            force: If True, cleanup regardless of cleanup settings
        """
        if self._working_dir and self._temp_dir_created:
            if force or self.cleanup_on_success or self.cleanup_on_failure:
                try:
                    if self._working_dir.exists():
                        shutil.rmtree(self._working_dir)
                        logger.debug(f"Cleaned up temporary directory: {self._working_dir}")
                    self._working_dir = None
                    self._temp_dir_created = False
                except Exception as e:
                    logger.warning(f"Failed to cleanup temporary directory: {e}")

    def _cleanup_on_result(self, success: bool) -> None:
        """
        Conditionally cleanup based on compilation result.

        Args:
            success: Whether the compilation was successful
        """
        if success and self.cleanup_on_success:
            self.cleanup(force=True)
        elif not success and self.cleanup_on_failure:
            self.cleanup(force=True)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources."""
        # If an exception occurred, consider it a failure
        if exc_type is not None:
            self._cleanup_on_result(success=False)
        else:
            # Don't auto-cleanup on success, let the caller decide
            # They might need the output files
            pass
        return False

    def __del__(self):
        """Destructor - ensure cleanup."""
        # Final cleanup attempt, but don't force if user wanted to keep files
        if self._temp_dir_created and self._working_dir and self._working_dir.exists():
            logger.warning(
                f"Temporary directory still exists at destruction: {self._working_dir}. "
                "Consider using context manager or calling cleanup() explicitly."
            )


def _parse_error_file(error_file: Path, stage: CompilationStage) -> List[CompilationError]:
    """
    Parse a .err file and extract compilation errors.

    This is a standalone function used by all wrapper classes.
    The error files contain error messages from each compilation stage.
    Format varies but typically includes file names, line numbers, and messages.

    Args:
        error_file: Path to the .err file
        stage: Which compilation stage produced this error

    Returns:
        List of CompilationError objects
    """
    errors = []

    if not error_file.exists():
        return errors

    try:
        with open(error_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        if not content.strip():
            return errors

        # Try to parse structured error messages
        # Common formats:
        # "file.c(123): error: message"
        # "file.c:123: error: message"
        # "Error in file.c at line 123: message"
        # "error: message"

        # Pattern for file(line): severity: message
        pattern1 = re.compile(
            r'^(.+?)\((\d+)\):\s*(error|warning|fatal|info):\s*(.+)$',
            re.MULTILINE | re.IGNORECASE
        )

        # Pattern for file:line:col: severity: message
        pattern2 = re.compile(
            r'^(.+?):(\d+):(\d+):\s*(error|warning|fatal|info):\s*(.+)$',
            re.MULTILINE | re.IGNORECASE
        )

        # Pattern for file:line: severity: message
        pattern3 = re.compile(
            r'^(.+?):(\d+):\s*(error|warning|fatal|info):\s*(.+)$',
            re.MULTILINE | re.IGNORECASE
        )

        # Try each pattern
        matches = []
        for match in pattern1.finditer(content):
            file_path, line, severity, message = match.groups()
            matches.append((file_path, int(line), None, severity, message, match.group(0)))

        if not matches:
            for match in pattern2.finditer(content):
                file_path, line, col, severity, message = match.groups()
                matches.append((file_path, int(line), int(col), severity, message, match.group(0)))

        if not matches:
            for match in pattern3.finditer(content):
                file_path, line, severity, message = match.groups()
                matches.append((file_path, int(line), None, severity, message, match.group(0)))

        # Convert matches to CompilationError objects
        for file_path, line, col, severity_str, message, raw in matches:
            # Map severity string to ErrorSeverity enum
            severity = ErrorSeverity.ERROR  # default
            severity_lower = severity_str.lower()
            if severity_lower == 'warning':
                severity = ErrorSeverity.WARNING
            elif severity_lower == 'fatal':
                severity = ErrorSeverity.FATAL
            elif severity_lower == 'info':
                severity = ErrorSeverity.INFO

            errors.append(CompilationError(
                stage=stage,
                severity=severity,
                message=message.strip(),
                file=Path(file_path) if file_path else None,
                line=line,
                column=col,
                raw_text=raw,
            ))

        # If no structured errors found, treat entire content as one error
        if not errors and content.strip():
            errors.append(CompilationError(
                stage=stage,
                severity=ErrorSeverity.ERROR,
                message=content.strip(),
                raw_text=content,
            ))

    except Exception as e:
        logger.warning(f"Failed to parse error file {error_file}: {e}")
        # Create a generic error
        errors.append(CompilationError(
            stage=stage,
            severity=ErrorSeverity.ERROR,
            message=f"Failed to parse error file: {str(e)}",
        ))

    return errors


class SCMPWrapper(BaseCompiler):
    """
    Wrapper for SCMP.exe - the orchestrator for the full compilation chain.

    SCMP orchestrates the 3-stage compilation pipeline:
    1. SPP.exe - Preprocessor (.c → spp.c + spp.syn)
    2. SCC.exe - Compiler (spp.c → sasm.sca + scc.syn)
    3. SASM.exe - Assembler (sasm.sca → .scr + .h)

    Usage:
        wrapper = SCMPWrapper(
            executable_path="path/to/scmp.exe",
            include_dirs=["path/to/inc"]
        )
        result = wrapper.compile("source.c", "output.scr", "output.h")
    """

    def __init__(
        self,
        executable_path: Path | str,
        include_dirs: Optional[List[Path | str]] = None,
        working_dir: Optional[Path | str] = None,
        timeout: int = 60,
        cleanup_on_success: bool = True,
        cleanup_on_failure: bool = False,
    ):
        """
        Initialize SCMP wrapper.

        Args:
            executable_path: Path to scmp.exe
            include_dirs: List of directories to search for header files
            working_dir: Working directory for compilation
            timeout: Maximum execution time in seconds
            cleanup_on_success: Whether to cleanup temp files after success
            cleanup_on_failure: Whether to cleanup temp files after failure
        """
        super().__init__(
            executable_path=executable_path,
            working_dir=working_dir,
            timeout=timeout,
            cleanup_on_success=cleanup_on_success,
            cleanup_on_failure=cleanup_on_failure,
        )
        self.include_dirs = [Path(d) for d in include_dirs] if include_dirs else []

    def _parse_error_file(self, error_file: Path, stage: CompilationStage) -> List[CompilationError]:
        """Delegate to standalone _parse_error_file function."""
        return _parse_error_file(error_file, stage)

    def _copy_includes_to_working_dir(self) -> None:
        """
        Copy include directories to working directory.

        SCMP expects include files to be in an 'inc' subdirectory.
        """
        if not self.include_dirs:
            return

        inc_dir = self.working_dir / "inc"
        inc_dir.mkdir(exist_ok=True)

        for include_dir in self.include_dirs:
            if not include_dir.exists():
                logger.warning(f"Include directory not found: {include_dir}")
                continue

            # Copy all header files from include_dir to inc_dir
            for header_file in include_dir.glob("*.h"):
                dest = inc_dir / header_file.name
                shutil.copy2(header_file, dest)
                logger.debug(f"Copied include: {header_file.name}")

    def compile(
        self,
        source_file: Path | str,
        output_scr: Path | str,
        output_header: Optional[Path | str] = None,
    ) -> CompilationResult:
        """
        Compile a Vietcong script using the full SCMP compilation chain.

        IMPORTANT: SCMP.exe must be run from its own directory where the other
        compiler executables (spp.exe, scc.exe, sasm.exe) are located. This method
        handles copying files to/from the compiler directory automatically.

        Args:
            source_file: Path to the source .c file
            output_scr: Path to the output .scr file
            output_header: Optional path to output .h file

        Returns:
            CompilationResult with compilation status and any errors

        Example:
            >>> wrapper = SCMPWrapper("path/to/scmp.exe")
            >>> result = wrapper.compile("script.c", "script.scr", "script.h")
            >>> if result.success:
            ...     print(f"Compiled to {result.output_file}")
            >>> else:
            ...     for error in result.errors:
            ...         print(error)
        """
        source_file = Path(source_file).absolute()
        output_scr = Path(output_scr).absolute()
        output_header = Path(output_header).absolute() if output_header else None

        # Validate source file exists
        if not source_file.exists():
            return CompilationResult(
                success=False,
                stage=CompilationStage.SCMP,
                errors=[CompilationError(
                    stage=CompilationStage.SCMP,
                    severity=ErrorSeverity.FATAL,
                    message=f"Source file not found: {source_file}",
                )]
            )

        # SCMP must run from its own directory (where spp.exe, scc.exe, sasm.exe are)
        compiler_dir = self.executable_path.parent

        # Copy include directories to compiler directory
        inc_dir = compiler_dir / "inc"
        if not inc_dir.exists():
            inc_dir.mkdir(exist_ok=True)

        for include_dir in self.include_dirs:
            if not include_dir.exists():
                logger.warning(f"Include directory not found: {include_dir}")
                continue

            for header_file in include_dir.glob("*.h"):
                dest = inc_dir / header_file.name
                if not dest.exists() or dest.stat().st_mtime < header_file.stat().st_mtime:
                    shutil.copy2(header_file, dest)
                    logger.debug(f"Copied include: {header_file.name}")

        # Clean up any leftover files from previous compilation BEFORE starting new one
        logger.debug("Cleaning up previous compilation artifacts")
        intermediate_names_cleanup = {
            'spp.c': 'preprocessed',
            'spp.syn': 'preprocessor_symbols',
            'spp.dbg': 'preprocessor_debug',
            'sasm.sca': 'assembly',
            'scc.syn': 'compiler_symbols',
            'scc.dbg': 'compiler_debug',
            'sasm.syn': 'assembler_symbols',
            'sasm.dbg': 'assembler_debug',
        }

        error_files_cleanup = {
            'spp.err': 'preprocessor',
            'scc.err': 'compiler',
            'sasm.err': 'assembler',
        }

        # Remove old intermediate files
        for filename in intermediate_names_cleanup.keys():
            file_path = compiler_dir / filename
            if file_path.exists():
                try:
                    file_path.unlink()
                    logger.debug(f"Removed old {filename}")
                except Exception as e:
                    logger.debug(f"Could not delete {filename}: {e}")

        # Remove old error files
        for filename in error_files_cleanup.keys():
            file_path = compiler_dir / filename
            if file_path.exists():
                try:
                    file_path.unlink()
                    logger.debug(f"Removed old {filename}")
                except Exception as e:
                    logger.debug(f"Could not delete {filename}: {e}")

        # Copy source file to compiler directory
        source_name = source_file.name
        work_source = compiler_dir / source_name

        import sys
        print(f"\n=== FILE COPY DEBUG ===", file=sys.stderr)
        print(f"Source file: {source_file}", file=sys.stderr)
        print(f"Source exists: {source_file.exists()}", file=sys.stderr)
        print(f"Dest file: {work_source}", file=sys.stderr)
        print(f"Compiler dir: {compiler_dir}", file=sys.stderr)

        shutil.copy2(source_file, work_source)

        print(f"After copy - dest exists: {work_source.exists()}", file=sys.stderr)
        if work_source.exists():
            print(f"Dest file size: {work_source.stat().st_size} bytes", file=sys.stderr)
        print(f"======================\n", file=sys.stderr)

        # Determine output paths in compiler directory
        scr_name = output_scr.name if output_scr.name.endswith('.scr') else f"{output_scr.stem}.scr"
        work_scr = compiler_dir / scr_name

        # Build command line arguments
        args = [source_name, scr_name]

        if output_header:
            header_name = output_header.name if output_header.name.endswith('.h') else f"{output_header.stem}.h"
            work_header = compiler_dir / header_name
            args.append(header_name)
        else:
            work_header = None

        logger.info(f"Compiling {source_file.name} → {scr_name}")
        logger.debug(f"Working directory: {compiler_dir}")

        # Execute SCMP from the compiler directory
        proc_result = self._execute(args, cwd=compiler_dir)

        # Check for error files in the compiler directory
        errors = []
        error_files = {
            CompilationStage.SPP: compiler_dir / "spp.err",
            CompilationStage.SCC: compiler_dir / "scc.err",
            CompilationStage.SASM: compiler_dir / "sasm.err",
        }

        for stage, error_file in error_files.items():
            stage_errors = self._parse_error_file(error_file, stage)
            errors.extend(stage_errors)

        # Determine success
        # SCMP return codes: 0=success, -2=spp error, -3=scc error, -4=sasm error
        success = proc_result.success and work_scr.exists()

        # Collect intermediate files
        intermediate_files = {}
        intermediate_names = {
            'spp.c': 'preprocessed',
            'spp.syn': 'preprocessor_symbols',
            'spp.dbg': 'preprocessor_debug',
            'sasm.sca': 'assembly',
            'scc.syn': 'compiler_symbols',
            'scc.dbg': 'compiler_debug',
            'sasm.syn': 'assembler_symbols',
            'sasm.dbg': 'assembler_debug',
        }

        for filename, key in intermediate_names.items():
            file_path = compiler_dir / filename
            if file_path.exists():
                # Copy to temp location for inspection
                temp_file = self.working_dir / filename
                shutil.copy2(file_path, temp_file)
                intermediate_files[key] = temp_file

        # Copy output files to destination if successful
        final_scr = None
        if success and work_scr.exists():
            shutil.copy2(work_scr, output_scr)
            final_scr = output_scr
            logger.info(f"Compilation successful: {output_scr}")

            if work_header and work_header.exists() and output_header:
                shutil.copy2(work_header, output_header)
                intermediate_files['header'] = output_header

        # Clean up only the source file copy (leave intermediate files for debugging)
        try:
            if work_source.exists():
                work_source.unlink()
                logger.debug(f"Removed source copy: {work_source.name}")
        except Exception as e:
            logger.debug(f"Could not delete source copy: {e}")

        # NOTE: Intermediate files, error files, and output .scr are NOT cleaned up here
        # They will be cleaned up BEFORE the next compilation starts (see cleanup above)

        # Create result
        result = CompilationResult(
            success=success,
            stage=CompilationStage.SCMP,
            output_file=final_scr,
            errors=errors,
            stdout=proc_result.stdout,
            stderr=proc_result.stderr,
            returncode=proc_result.returncode,
            working_dir=compiler_dir,
            intermediate_files=intermediate_files,
        )

        return result


class SPPWrapper(BaseCompiler):
    """
    Wrapper for SPP.exe - the preprocessor.

    SPP handles:
    - Preprocessing directives (#include, #define, #if/ifdef/etc.)
    - Macro expansion
    - File inclusion

    Command line: spp.exe <input.c> <output.c> [include_path] [root_path]

    Outputs:
    - spp.c (preprocessed source)
    - spp.syn (symbol table)
    - spp.dbg (debug log)
    - spp.err (errors if any)

    Usage:
        wrapper = SPPWrapper(
            executable_path="path/to/spp.exe",
            include_path="path/to/headers"
        )
        result = wrapper.preprocess("source.c", "preprocessed.c")
    """

    def __init__(
        self,
        executable_path: Path | str,
        include_path: Optional[Path | str] = None,
        root_path: Optional[Path | str] = None,
        working_dir: Optional[Path | str] = None,
        timeout: int = 30,
        cleanup_on_success: bool = True,
        cleanup_on_failure: bool = False,
    ):
        """
        Initialize SPP wrapper.

        Args:
            executable_path: Path to spp.exe
            include_path: Base path for <...> includes (optional)
            root_path: Root path for __FILE__ macro (optional)
            working_dir: Working directory for preprocessing
            timeout: Maximum execution time in seconds
            cleanup_on_success: Whether to cleanup temp files after success
            cleanup_on_failure: Whether to cleanup temp files after failure
        """
        super().__init__(
            executable_path=executable_path,
            working_dir=working_dir,
            timeout=timeout,
            cleanup_on_success=cleanup_on_success,
            cleanup_on_failure=cleanup_on_failure,
        )
        self.include_path = Path(include_path) if include_path else None
        self.root_path = Path(root_path) if root_path else None

    def preprocess(
        self,
        source_file: Path | str,
        output_file: Path | str,
    ) -> CompilationResult:
        """
        Preprocess a C source file.

        Args:
            source_file: Path to the input .c file
            output_file: Path to the output preprocessed file

        Returns:
            CompilationResult with preprocessing status and any errors

        Example:
            >>> wrapper = SPPWrapper("path/to/spp.exe")
            >>> result = wrapper.preprocess("script.c", "script_preprocessed.c")
            >>> if result.success:
            ...     print(f"Preprocessed to {result.output_file}")
            >>> else:
            ...     for error in result.errors:
            ...         print(error)
        """
        source_file = Path(source_file).absolute()
        output_file = Path(output_file).absolute()

        # Validate source file exists
        if not source_file.exists():
            return CompilationResult(
                success=False,
                stage=CompilationStage.SPP,
                errors=[CompilationError(
                    stage=CompilationStage.SPP,
                    severity=ErrorSeverity.FATAL,
                    message=f"Source file not found: {source_file}",
                )]
            )

        # Copy source file to working directory
        work_source = self.working_dir / source_file.name
        shutil.copy2(source_file, work_source)

        # Determine output path in working directory
        work_output = self.working_dir / "spp.c"

        # Build command line arguments
        args = [str(work_source), str(work_output)]

        # Add optional paths
        if self.include_path:
            args.append(str(self.include_path.absolute()))
        if self.root_path:
            args.append(str(self.root_path.absolute()))

        logger.info(f"Preprocessing {source_file.name}")

        # Execute SPP
        proc_result = self._execute(args)

        # Check for error file
        error_file = self.working_dir / "spp.err"
        errors = _parse_error_file(error_file, CompilationStage.SPP)

        # Determine success
        success = proc_result.success and work_output.exists()

        # Collect intermediate files
        intermediate_files = {}
        for filename, key in [('spp.syn', 'symbols'), ('spp.dbg', 'debug')]:
            file_path = self.working_dir / filename
            if file_path.exists():
                intermediate_files[key] = file_path

        # Copy output file to destination if successful
        final_output = None
        if success and work_output.exists():
            shutil.copy2(work_output, output_file)
            final_output = output_file
            logger.info(f"Preprocessing successful: {output_file}")

        # Cleanup based on result
        self._cleanup_on_result(success)

        return CompilationResult(
            success=success,
            stage=CompilationStage.SPP,
            output_file=final_output,
            errors=errors,
            stdout=proc_result.stdout,
            stderr=proc_result.stderr,
            returncode=proc_result.returncode,
            working_dir=self.working_dir,
            intermediate_files=intermediate_files,
        )


class SCCWrapper(BaseCompiler):
    """
    Wrapper for SCC.exe - the compiler (C to assembly).

    SCC compiles preprocessed C code to assembly.

    Command line: scc.exe <input.spp> <output.sca> <temp.h> [dbg]

    Outputs:
    - sasm.sca (assembly code)
    - scc.syn (symbol table)
    - scc.dbg (debug log)
    - scc.err (errors if any)

    Usage:
        wrapper = SCCWrapper(executable_path="path/to/scc.exe")
        result = wrapper.compile("preprocessed.c", "output.sca")
    """

    def __init__(
        self,
        executable_path: Path | str,
        debug_mode: bool = False,
        working_dir: Optional[Path | str] = None,
        timeout: int = 60,
        cleanup_on_success: bool = True,
        cleanup_on_failure: bool = False,
    ):
        """
        Initialize SCC wrapper.

        Args:
            executable_path: Path to scc.exe
            debug_mode: Enable debug output
            working_dir: Working directory for compilation
            timeout: Maximum execution time in seconds
            cleanup_on_success: Whether to cleanup temp files after success
            cleanup_on_failure: Whether to cleanup temp files after failure
        """
        super().__init__(
            executable_path=executable_path,
            working_dir=working_dir,
            timeout=timeout,
            cleanup_on_success=cleanup_on_success,
            cleanup_on_failure=cleanup_on_failure,
        )
        self.debug_mode = debug_mode

    def compile(
        self,
        source_file: Path | str,
        output_file: Path | str,
    ) -> CompilationResult:
        """
        Compile preprocessed C code to assembly.

        Args:
            source_file: Path to the preprocessed .c or .spp file
            output_file: Path to the output .sca assembly file

        Returns:
            CompilationResult with compilation status and any errors

        Example:
            >>> wrapper = SCCWrapper("path/to/scc.exe")
            >>> result = wrapper.compile("preprocessed.c", "output.sca")
            >>> if result.success:
            ...     print(f"Compiled to {result.output_file}")
            >>> else:
            ...     for error in result.errors:
            ...         print(error)
        """
        source_file = Path(source_file).absolute()
        output_file = Path(output_file).absolute()

        # Validate source file exists
        if not source_file.exists():
            return CompilationResult(
                success=False,
                stage=CompilationStage.SCC,
                errors=[CompilationError(
                    stage=CompilationStage.SCC,
                    severity=ErrorSeverity.FATAL,
                    message=f"Source file not found: {source_file}",
                )]
            )

        # Copy source file to working directory
        work_source = self.working_dir / source_file.name
        shutil.copy2(source_file, work_source)

        # Determine output path in working directory
        work_output = self.working_dir / "sasm.sca"

        # Create temporary header file (required but deleted after compilation)
        temp_header = self.working_dir / "temp.h"
        temp_header.touch()

        # Build command line arguments
        args = [str(work_source), str(work_output), str(temp_header)]

        # Add debug flag if enabled
        if self.debug_mode:
            args.append("dbg")

        logger.info(f"Compiling {source_file.name} to assembly")

        # Execute SCC
        proc_result = self._execute(args)

        # Check for error file
        error_file = self.working_dir / "scc.err"
        errors = _parse_error_file(error_file, CompilationStage.SCC)

        # Determine success
        success = proc_result.success and work_output.exists()

        # Collect intermediate files
        intermediate_files = {}
        for filename, key in [('scc.syn', 'symbols'), ('scc.dbg', 'debug')]:
            file_path = self.working_dir / filename
            if file_path.exists():
                intermediate_files[key] = file_path

        # Copy output file to destination if successful
        final_output = None
        if success and work_output.exists():
            shutil.copy2(work_output, output_file)
            final_output = output_file
            logger.info(f"Compilation successful: {output_file}")

        # Cleanup based on result
        self._cleanup_on_result(success)

        return CompilationResult(
            success=success,
            stage=CompilationStage.SCC,
            output_file=final_output,
            errors=errors,
            stdout=proc_result.stdout,
            stderr=proc_result.stderr,
            returncode=proc_result.returncode,
            working_dir=self.working_dir,
            intermediate_files=intermediate_files,
        )


class SASMWrapper(BaseCompiler):
    """
    Wrapper for SASM.exe - the assembler (assembly to bytecode).

    SASM assembles .sca files into final .scr bytecode.

    Command line: sasm.exe <input.sca> <output.scr> [output.h]

    Outputs:
    - .scr (bytecode)
    - .h (optional header)
    - sasm.syn (symbol table)
    - sasm.dbg (debug log)
    - sasm.err (errors if any)

    Usage:
        wrapper = SASMWrapper(executable_path="path/to/sasm.exe")
        result = wrapper.assemble("input.sca", "output.scr", "output.h")
    """

    def __init__(
        self,
        executable_path: Path | str,
        working_dir: Optional[Path | str] = None,
        timeout: int = 30,
        cleanup_on_success: bool = True,
        cleanup_on_failure: bool = False,
    ):
        """
        Initialize SASM wrapper.

        Args:
            executable_path: Path to sasm.exe
            working_dir: Working directory for assembly
            timeout: Maximum execution time in seconds
            cleanup_on_success: Whether to cleanup temp files after success
            cleanup_on_failure: Whether to cleanup temp files after failure
        """
        super().__init__(
            executable_path=executable_path,
            working_dir=working_dir,
            timeout=timeout,
            cleanup_on_success=cleanup_on_success,
            cleanup_on_failure=cleanup_on_failure,
        )

    def assemble(
        self,
        source_file: Path | str,
        output_scr: Path | str,
        output_header: Optional[Path | str] = None,
    ) -> CompilationResult:
        """
        Assemble .sca file to .scr bytecode.

        Args:
            source_file: Path to the input .sca assembly file
            output_scr: Path to the output .scr bytecode file
            output_header: Optional path to output .h header file

        Returns:
            CompilationResult with assembly status and any errors

        Example:
            >>> wrapper = SASMWrapper("path/to/sasm.exe")
            >>> result = wrapper.assemble("input.sca", "output.scr", "output.h")
            >>> if result.success:
            ...     print(f"Assembled to {result.output_file}")
            >>> else:
            ...     for error in result.errors:
            ...         print(error)
        """
        source_file = Path(source_file).absolute()
        output_scr = Path(output_scr).absolute()
        output_header = Path(output_header).absolute() if output_header else None

        # Validate source file exists
        if not source_file.exists():
            return CompilationResult(
                success=False,
                stage=CompilationStage.SASM,
                errors=[CompilationError(
                    stage=CompilationStage.SASM,
                    severity=ErrorSeverity.FATAL,
                    message=f"Source file not found: {source_file}",
                )]
            )

        # Copy source file to working directory
        work_source = self.working_dir / source_file.name
        shutil.copy2(source_file, work_source)

        # Determine output paths in working directory
        work_scr = self.working_dir / "output.scr"
        work_header = self.working_dir / "output.h" if output_header else None

        # Build command line arguments
        args = [str(work_source), str(work_scr)]

        if output_header:
            args.append(str(work_header))

        logger.info(f"Assembling {source_file.name}")

        # Execute SASM
        proc_result = self._execute(args)

        # Check for error file
        error_file = self.working_dir / "sasm.err"
        errors = _parse_error_file(error_file, CompilationStage.SASM)

        # Determine success
        success = proc_result.success and work_scr.exists()

        # Collect intermediate files
        intermediate_files = {}
        for filename, key in [('sasm.syn', 'symbols'), ('sasm.dbg', 'debug')]:
            file_path = self.working_dir / filename
            if file_path.exists():
                intermediate_files[key] = file_path

        # Copy output files to destination if successful
        final_scr = None
        if success and work_scr.exists():
            shutil.copy2(work_scr, output_scr)
            final_scr = output_scr
            logger.info(f"Assembly successful: {output_scr}")

            if work_header and work_header.exists() and output_header:
                shutil.copy2(work_header, output_header)
                intermediate_files['header'] = output_header

        # Cleanup based on result
        self._cleanup_on_result(success)

        return CompilationResult(
            success=success,
            stage=CompilationStage.SASM,
            output_file=final_scr,
            errors=errors,
            stdout=proc_result.stdout,
            stderr=proc_result.stderr,
            returncode=proc_result.returncode,
            working_dir=self.working_dir,
            intermediate_files=intermediate_files,
        )
