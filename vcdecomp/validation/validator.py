"""
Validation workflow orchestrator.

Coordinates the full validation workflow:
1. Compile decompiled source code using original compiler
2. Compare original and recompiled bytecode
3. Categorize differences
4. Generate validation result with recommendations
"""

from __future__ import annotations

import logging
import tempfile
import threading
import time
from pathlib import Path
from typing import Optional, List

from .compiler_wrapper import SCMPWrapper
from .bytecode_compare import BytecodeComparator
from .difference_types import categorize_differences, get_summary, DifferenceCategory
from .validation_types import ValidationResult, ValidationVerdict
from .cache import ValidationCache

logger = logging.getLogger(__name__)

# Global lock to serialize compiler access across all ValidationOrchestrator instances
# The original SCMP.exe compiler cannot run multiple instances simultaneously
_compiler_lock = threading.Lock()


class ValidationOrchestrator:
    """
    Orchestrates the full validation workflow.

    Manages the complete validation process from compilation through
    comparison and reporting. Handles errors gracefully at each step
    and provides detailed feedback on validation status.

    Attributes:
        compiler_dir: Path to directory containing compiler executables
        include_dir: Path to directory containing header files
        timeout: Compilation timeout in seconds
        opcode_variant: SCR opcode variant to use for comparison
        cache: ValidationCache for caching results
        use_cache: Whether to use caching
    """

    def __init__(
        self,
        compiler_dir: Path | str,
        include_dirs: Optional[List[Path | str]] = None,
        timeout: int = 30,
        opcode_variant: str = "auto",
        cache_dir: Optional[Path | str] = None,
        cache_enabled: bool = True,
        cache_max_age: int = 0,
    ):
        """
        Initialize the validation orchestrator.

        Args:
            compiler_dir: Path to directory containing SCMP.exe and other compiler tools
            include_dirs: List of directories containing header files (e.g., inc/ folder)
            timeout: Compilation timeout in seconds
            opcode_variant: SCR opcode variant to use ("auto", "v1.60", etc.)
            cache_dir: Directory to store cache files (default: .validation_cache)
            cache_enabled: Whether to enable caching (can be disabled via config)
            cache_max_age: Maximum age of cache entries in seconds (0 = no limit)
        """
        self.compiler_dir = Path(compiler_dir)
        self.include_dirs = [Path(d) for d in include_dirs] if include_dirs else []
        self.timeout = timeout
        self.opcode_variant = opcode_variant
        self.use_cache = cache_enabled

        # Initialize cache
        if cache_dir is None:
            cache_dir = Path(".validation_cache")
        self.cache = ValidationCache(
            cache_dir=cache_dir,
            max_age_seconds=cache_max_age,
            enabled=cache_enabled,
        )

        # Validate compiler directory
        if not self.compiler_dir.exists():
            raise FileNotFoundError(f"Compiler directory not found: {self.compiler_dir}")

        scmp_exe = self.compiler_dir / "SCMP.exe"
        if not scmp_exe.exists():
            raise FileNotFoundError(f"SCMP.exe not found in {self.compiler_dir}")

        logger.info(f"Initialized ValidationOrchestrator with compiler_dir={self.compiler_dir}")

    def validate(
        self,
        original_scr: Path | str,
        decompiled_source: Path | str,
        output_scr: Optional[Path | str] = None,
        use_cache: Optional[bool] = None,
    ) -> ValidationResult:
        """
        Validate decompiled source code against original bytecode.

        Performs the complete validation workflow:
        1. Check cache for existing result (if enabled)
        2. Compile decompiled source to .SCR
        3. Compare original and recompiled bytecode
        4. Categorize differences
        5. Generate recommendations
        6. Store result in cache (if enabled)

        Args:
            original_scr: Path to original .SCR file
            decompiled_source: Path to decompiled source code (.c file)
            output_scr: Path to save recompiled .SCR (uses temp file if None)
            use_cache: Whether to use cache for this validation (None = use default)

        Returns:
            ValidationResult with complete validation findings

        Example:
            >>> orchestrator = ValidationOrchestrator("./original-resources/compiler")
            >>> result = orchestrator.validate("original.scr", "decompiled.c")
            >>> print(result.verdict)
            ValidationVerdict.PASS
        """
        original_scr = Path(original_scr)
        decompiled_source = Path(decompiled_source)

        # Determine cache usage
        use_cache = self.use_cache if use_cache is None else use_cache

        # Check cache first
        if use_cache:
            cached_result = self.cache.get(original_scr, decompiled_source)
            if cached_result is not None:
                logger.info(f"Using cached validation result for {decompiled_source.name}")
                return cached_result

        # Initialize result
        result = ValidationResult(
            original_scr=original_scr,
            decompiled_source=decompiled_source,
            metadata={
                "compiler_dir": str(self.compiler_dir),
                "include_dirs": [str(d) for d in self.include_dirs],
                "opcode_variant": self.opcode_variant,
                "timeout": self.timeout,
                "timestamp": time.time(),
            }
        )

        # Validate input files
        if not original_scr.exists():
            result.verdict = ValidationVerdict.ERROR
            result.error_message = f"Original SCR file not found: {original_scr}"
            return result

        if not decompiled_source.exists():
            result.verdict = ValidationVerdict.ERROR
            result.error_message = f"Decompiled source file not found: {decompiled_source}"
            return result

        logger.info(f"Starting validation: {original_scr.name} vs {decompiled_source.name}")

        # Step 1: Compile decompiled source
        try:
            result.compilation_result = self._compile_source(decompiled_source, output_scr)
        except Exception as e:
            logger.exception("Compilation step failed")
            result.verdict = ValidationVerdict.ERROR
            result.error_message = f"Compilation failed with exception: {e}"
            result.recommendations.append("Check that compiler tools are properly installed")
            result.recommendations.append("Verify that source code is syntactically correct")
            return result

        # Check compilation success
        if not result.compilation_succeeded:
            result.verdict = ValidationVerdict.FAIL
            result.error_message = "Compilation failed"
            result.recommendations.append("Review compilation errors above")
            result.recommendations.append("Verify decompiled source code syntax")
            if result.compilation_result and result.compilation_result.errors:
                # Add specific recommendations based on error types
                error_messages = [err.message.lower() for err in result.compilation_result.errors]
                if any("syntax" in msg for msg in error_messages):
                    result.recommendations.append("Check for syntax errors in decompiled code")
                if any("undefined" in msg or "undeclared" in msg for msg in error_messages):
                    result.recommendations.append("Verify all functions and variables are declared")
                if any("include" in msg or "header" in msg for msg in error_messages):
                    result.recommendations.append("Check that all required header files are available")
            return result

        # Step 2: Compare bytecode
        try:
            recompiled_scr = result.compilation_result.output_file
            if not recompiled_scr or not Path(recompiled_scr).exists():
                raise FileNotFoundError("Compiled SCR file not found")

            result.comparison_result = self._compare_bytecode(original_scr, recompiled_scr)
        except Exception as e:
            logger.exception("Comparison step failed")
            result.verdict = ValidationVerdict.ERROR
            result.error_message = f"Bytecode comparison failed with exception: {e}"
            result.recommendations.append("Check that SCR files are valid")
            result.recommendations.append("Try validating with different opcode variant")
            return result

        # Check comparison success
        if not result.comparison_succeeded:
            result.verdict = ValidationVerdict.ERROR
            result.error_message = result.comparison_result.load_error or "Comparison failed"
            result.recommendations.append("Verify SCR files are valid and readable")
            return result

        # Step 3: Categorize differences
        try:
            all_differences = result.comparison_result.all_differences
            result.categorized_differences = categorize_differences(all_differences)
            result.difference_summary = get_summary(all_differences)
        except Exception as e:
            logger.exception("Categorization step failed")
            result.verdict = ValidationVerdict.ERROR
            result.error_message = f"Difference categorization failed: {e}"
            return result

        # Step 4: Determine verdict and generate recommendations
        self._determine_verdict(result)

        # Step 5: Store in cache
        if use_cache:
            self.cache.set(original_scr, decompiled_source, result)

        logger.info(f"Validation complete: {result.verdict.value}")
        return result

    def _compile_source(
        self,
        source_file: Path,
        output_scr: Optional[Path] = None,
    ) -> "CompilationResult":
        """
        Compile decompiled source code.

        Args:
            source_file: Path to source .c file
            output_scr: Path to output .SCR file (uses temp if None)

        Returns:
            CompilationResult
        """
        logger.debug(f"Compiling: {source_file}")

        # Use temp file if no output specified
        if output_scr is None:
            temp_dir = Path(tempfile.gettempdir()) / "vcdecomp_validation"
            temp_dir.mkdir(exist_ok=True)
            output_scr = temp_dir / f"{source_file.stem}_recompiled.scr"

        # Initialize compiler wrapper
        scmp_exe = self.compiler_dir / "SCMP.exe"
        wrapper = SCMPWrapper(
            executable_path=scmp_exe,
            include_dirs=self.include_dirs,
            timeout=self.timeout,
        )

        # CRITICAL: Serialize compiler access with global lock
        # The original SCMP.exe cannot run multiple instances simultaneously
        # This prevents concurrent execution across pytest workers and test cases
        with _compiler_lock:
            logger.debug(f"Acquired compiler lock for {source_file.name}")

            # Compile (with header output like .bat files do)
            output_header = output_scr.parent / f"{source_file.stem}.h"
            result = wrapper.compile(
                source_file=source_file,
                output_scr=output_scr,
                output_header=output_header,
            )

            logger.debug(f"Released compiler lock for {source_file.name}")

        logger.debug(f"Compilation {'succeeded' if result.success else 'failed'}")
        return result

    def _compare_bytecode(
        self,
        original_scr: Path,
        recompiled_scr: Path,
    ) -> "ComparisonResult":
        """
        Compare original and recompiled bytecode.

        Args:
            original_scr: Path to original .SCR file
            recompiled_scr: Path to recompiled .SCR file

        Returns:
            ComparisonResult
        """
        logger.debug(f"Comparing: {original_scr.name} vs {recompiled_scr.name}")

        comparator = BytecodeComparator()
        result = comparator.compare_files(
            original_path=original_scr,
            recompiled_path=recompiled_scr,
            opcode_variant=self.opcode_variant,
        )

        logger.debug(f"Comparison found {len(result.all_differences)} differences")
        return result

    def _determine_verdict(self, result: ValidationResult) -> None:
        """
        Determine overall verdict and generate recommendations.

        Modifies the ValidationResult in place.

        Args:
            result: ValidationResult to update
        """
        # If bytecode is identical, it's a clear pass
        if result.bytecode_identical:
            result.verdict = ValidationVerdict.PASS
            result.recommendations.append("Bytecode is identical - decompilation is perfect!")
            return

        # Check if there are semantic differences
        if result.has_semantic_differences:
            result.verdict = ValidationVerdict.PARTIAL
            semantic_diffs = result.get_differences_by_category(
                DifferenceCategory.SEMANTIC
            )
            result.recommendations.append(
                f"Found {len(semantic_diffs)} semantic differences that affect behavior"
            )
            result.recommendations.append(
                "Review semantic differences carefully before using decompiled code"
            )

            # Provide specific recommendations based on difference types
            diff_types = set(diff.difference.type for diff in semantic_diffs)
            if any(dt.name == "HEADER" for dt in diff_types):
                result.recommendations.append(
                    "Header differences detected - check entry point and parameters"
                )
            if any(dt.name == "CODE" for dt in diff_types):
                result.recommendations.append(
                    "Code differences detected - verify control flow and logic"
                )
            if any(dt.name == "XFN" for dt in diff_types):
                result.recommendations.append(
                    "External function differences detected - check function calls"
                )
        else:
            # Only cosmetic/optimization differences
            result.verdict = ValidationVerdict.PASS
            result.recommendations.append(
                "Only cosmetic or optimization differences found - functionally equivalent"
            )

            if result.has_cosmetic_differences:
                cosmetic_diffs = result.get_differences_by_category(
                    DifferenceCategory.COSMETIC
                )
                result.recommendations.append(
                    f"Found {len(cosmetic_diffs)} cosmetic differences (no behavioral impact)"
                )

    def get_cache_statistics(self) -> "CacheStatistics":
        """
        Get cache performance statistics.

        Returns:
            CacheStatistics object with hit/miss counts and hit rate

        Example:
            >>> orchestrator = ValidationOrchestrator("./compiler")
            >>> stats = orchestrator.get_cache_statistics()
            >>> print(f"Hit rate: {stats.hit_rate:.1%}")
            Hit rate: 75.0%
        """
        return self.cache.get_statistics()

    def clear_cache(self) -> int:
        """
        Clear all cached validation results.

        Returns:
            Number of cache entries cleared

        Example:
            >>> orchestrator = ValidationOrchestrator("./compiler")
            >>> count = orchestrator.clear_cache()
            >>> print(f"Cleared {count} cache entries")
            Cleared 5 cache entries
        """
        return self.cache.clear()

    def invalidate_cache(
        self,
        original_scr: Optional[Path | str] = None,
        decompiled_source: Optional[Path | str] = None,
    ) -> int:
        """
        Invalidate specific cache entry or all entries.

        Args:
            original_scr: Optional path to original .SCR file
            decompiled_source: Optional path to decompiled source code

        Returns:
            Number of cache entries invalidated

        Example:
            >>> orchestrator = ValidationOrchestrator("./compiler")
            >>> # Invalidate specific entry
            >>> count = orchestrator.invalidate_cache("orig.scr", "decomp.c")
            >>> # Invalidate all entries
            >>> count = orchestrator.invalidate_cache()
        """
        return self.cache.invalidate(original_scr, decompiled_source)
