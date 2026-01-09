"""
Data structures for compilation results and errors.

Defines types used throughout the validation system for representing
compilation outcomes, errors, and stages.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional


class CompilationStage(Enum):
    """Stages in the Vietcong script compilation pipeline."""
    SPP = "spp"      # Preprocessor
    SCC = "scc"      # Compiler (C to assembly)
    SASM = "sasm"    # Assembler (assembly to bytecode)
    SCMP = "scmp"    # Orchestrator (full chain)


class ErrorSeverity(Enum):
    """Severity levels for compilation errors."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"


@dataclass
class CompilationError:
    """
    Represents a single compilation error or warning.

    Attributes:
        stage: Which compilation stage produced this error
        severity: Error severity level
        message: The error message
        file: Source file where error occurred (if applicable)
        line: Line number in source file (if applicable)
        column: Column number in source file (if applicable)
        raw_text: Original error text from .err file
    """
    stage: CompilationStage
    severity: ErrorSeverity
    message: str
    file: Optional[Path] = None
    line: Optional[int] = None
    column: Optional[int] = None
    raw_text: Optional[str] = None

    def __str__(self) -> str:
        """Human-readable error representation."""
        location = ""
        if self.file:
            location = f"{self.file}"
            if self.line is not None:
                location += f":{self.line}"
                if self.column is not None:
                    location += f":{self.column}"
            location += ": "

        return f"[{self.stage.value}] {location}{self.severity.value}: {self.message}"


@dataclass
class CompilationResult:
    """
    Result of a compilation operation.

    Attributes:
        success: Whether compilation completed successfully
        stage: The compilation stage that was run
        output_file: Path to the output file (if successful)
        errors: List of errors and warnings encountered
        stdout: Standard output from the compiler
        stderr: Standard error from the compiler
        returncode: Process return code
        working_dir: Working directory where compilation occurred
        intermediate_files: Dictionary of intermediate files produced
    """
    success: bool
    stage: CompilationStage
    output_file: Optional[Path] = None
    errors: List[CompilationError] = field(default_factory=list)
    stdout: str = ""
    stderr: str = ""
    returncode: int = 0
    working_dir: Optional[Path] = None
    intermediate_files: dict[str, Path] = field(default_factory=dict)

    @property
    def has_errors(self) -> bool:
        """Check if there are any errors (not just warnings)."""
        return any(
            err.severity in (ErrorSeverity.ERROR, ErrorSeverity.FATAL)
            for err in self.errors
        )

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return any(
            err.severity == ErrorSeverity.WARNING
            for err in self.errors
        )

    @property
    def error_count(self) -> int:
        """Count of errors (not warnings)."""
        return sum(
            1 for err in self.errors
            if err.severity in (ErrorSeverity.ERROR, ErrorSeverity.FATAL)
        )

    @property
    def warning_count(self) -> int:
        """Count of warnings."""
        return sum(
            1 for err in self.errors
            if err.severity == ErrorSeverity.WARNING
        )

    def get_errors_by_stage(self, stage: CompilationStage) -> List[CompilationError]:
        """Get all errors from a specific compilation stage."""
        return [err for err in self.errors if err.stage == stage]

    def __str__(self) -> str:
        """Human-readable compilation result."""
        if self.success:
            result = f"✓ Compilation successful ({self.stage.value})"
            if self.output_file:
                result += f"\n  Output: {self.output_file}"
            if self.has_warnings:
                result += f"\n  Warnings: {self.warning_count}"
        else:
            result = f"✗ Compilation failed ({self.stage.value})"
            if self.has_errors:
                result += f"\n  Errors: {self.error_count}"
            if self.has_warnings:
                result += f"\n  Warnings: {self.warning_count}"

            # Show first few errors
            for err in self.errors[:3]:
                result += f"\n  {err}"

            if len(self.errors) > 3:
                result += f"\n  ... and {len(self.errors) - 3} more"

        return result
