"""
XFN Table Aggregator

Scans directories of .scr files and aggregates function signatures from
XFN tables to build a comprehensive database of engine functions.

The aggregator:
1. Recursively scans for .scr files
2. Extracts XFN entries from each file
3. Parses embedded type signatures
4. Deduplicates functions by name
5. Tracks usage statistics
6. Exports in SDK-compatible format
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict

from .signature_parser import XFNSignatureParser, ParsedSignature


@dataclass
class FunctionUsage:
    """Tracks usage of a function across scripts."""
    signature: ParsedSignature
    source_files: List[str] = field(default_factory=list)
    usage_count: int = 0

    @property
    def name(self) -> str:
        return self.signature.name


@dataclass
class AggregationResult:
    """Results of XFN aggregation."""
    functions: Dict[str, FunctionUsage]    # name -> usage info
    struct_types: Set[str]                  # All discovered struct types
    scripts_scanned: int                    # Total scripts processed
    scripts_failed: int                     # Scripts that failed to parse
    failed_files: List[str]                 # List of failed file paths
    errors: List[Tuple[str, str]]           # (file, error message)

    @property
    def function_count(self) -> int:
        return len(self.functions)

    @property
    def struct_count(self) -> int:
        return len(self.struct_types)

    def get_top_functions(self, n: int = 20) -> List[FunctionUsage]:
        """Get the N most frequently used functions."""
        sorted_funcs = sorted(
            self.functions.values(),
            key=lambda f: f.usage_count,
            reverse=True
        )
        return sorted_funcs[:n]

    def to_sdk_format(self) -> dict:
        """
        Export to SDK-compatible JSON format.

        Returns a dict where keys are function names and values
        match the format in vcdecomp/sdk/data/functions.json
        """
        result = {}
        for name, usage in sorted(self.functions.items()):
            result[name] = usage.signature.to_sdk_format()
        return result

    def to_json(self, include_usage: bool = True) -> dict:
        """
        Export full aggregation data to JSON.

        Args:
            include_usage: If True, include usage statistics

        Returns:
            Full aggregation data as dict
        """
        functions_data = {}
        for name, usage in sorted(self.functions.items()):
            func_data = usage.signature.to_sdk_format()
            if include_usage:
                func_data["usage_count"] = usage.usage_count
                func_data["source_files"] = usage.source_files[:5]  # Limit file list
            functions_data[name] = func_data

        return {
            "metadata": {
                "scripts_scanned": self.scripts_scanned,
                "scripts_failed": self.scripts_failed,
                "function_count": self.function_count,
                "struct_count": self.struct_count,
            },
            "struct_types": sorted(self.struct_types),
            "functions": functions_data,
        }

    def summary(self) -> str:
        """Generate a summary report."""
        lines = [
            "XFN Aggregation Summary",
            "=" * 50,
            f"Scripts scanned:     {self.scripts_scanned}",
            f"Scripts failed:      {self.scripts_failed}",
            f"Functions found:     {self.function_count}",
            f"Struct types found:  {self.struct_count}",
            "",
            "Top 20 Most Used Functions:",
            "-" * 50,
        ]

        for usage in self.get_top_functions(20):
            sig = usage.signature
            param_count = len(sig.parameters)
            variadic = " ..." if sig.is_variadic else ""
            lines.append(
                f"  {usage.usage_count:4d}x  {sig.name}({param_count} params{variadic}) -> {sig.return_type}"
            )

        if self.struct_types:
            lines.extend([
                "",
                "Discovered Struct Types:",
                "-" * 50,
            ])
            for struct_name in sorted(self.struct_types):
                lines.append(f"  {struct_name}")

        return "\n".join(lines)


class XFNAggregator:
    """
    Aggregates XFN function signatures from multiple .scr files.

    Usage:
        aggregator = XFNAggregator()
        result = aggregator.scan_directory("C:\\vc soubory\\LEVELS")
        print(result.summary())
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize the aggregator.

        Args:
            verbose: If True, print progress during scanning
        """
        self.verbose = verbose
        self.parser = XFNSignatureParser()

    def scan_directory(
        self,
        directory: str,
        recursive: bool = True,
        progress_callback=None
    ) -> AggregationResult:
        """
        Scan a directory for .scr files and aggregate XFN entries.

        Args:
            directory: Path to directory to scan
            recursive: If True, scan subdirectories
            progress_callback: Optional callback(current, total, filename)

        Returns:
            AggregationResult with aggregated data
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            raise ValueError(f"Directory not found: {directory}")

        # Find all .scr files
        pattern = "**/*.scr" if recursive else "*.scr"
        scr_files = list(dir_path.glob(pattern))

        if self.verbose:
            print(f"Found {len(scr_files)} .scr files in {directory}")

        # Aggregate functions
        functions: Dict[str, FunctionUsage] = {}
        struct_types: Set[str] = set()
        scripts_scanned = 0
        scripts_failed = 0
        failed_files: List[str] = []
        errors: List[Tuple[str, str]] = []

        for i, scr_path in enumerate(scr_files):
            if progress_callback:
                progress_callback(i + 1, len(scr_files), scr_path.name)

            try:
                xfn_entries = self._extract_xfn_entries(scr_path)
                scripts_scanned += 1

                for entry in xfn_entries:
                    signature = self.parser.parse(entry)

                    # Track struct types
                    struct_types.update(self.parser.struct_types)

                    # Deduplicate by function name
                    if signature.name in functions:
                        # Update usage count
                        functions[signature.name].usage_count += 1
                        # Add source file if not too many
                        if len(functions[signature.name].source_files) < 10:
                            functions[signature.name].source_files.append(str(scr_path))
                    else:
                        # New function
                        functions[signature.name] = FunctionUsage(
                            signature=signature,
                            source_files=[str(scr_path)],
                            usage_count=1
                        )

            except Exception as e:
                scripts_failed += 1
                failed_files.append(str(scr_path))
                errors.append((str(scr_path), str(e)))
                if self.verbose:
                    print(f"Error processing {scr_path.name}: {e}")

        # Collect all struct types from parser
        struct_types.update(self.parser.get_discovered_structs())

        return AggregationResult(
            functions=functions,
            struct_types=struct_types,
            scripts_scanned=scripts_scanned,
            scripts_failed=scripts_failed,
            failed_files=failed_files,
            errors=errors,
        )

    def scan_file(self, filepath: str) -> List[ParsedSignature]:
        """
        Scan a single .scr file and return parsed signatures.

        Args:
            filepath: Path to .scr file

        Returns:
            List of ParsedSignature for all XFN entries
        """
        scr_path = Path(filepath)
        xfn_entries = self._extract_xfn_entries(scr_path)

        signatures = []
        for entry in xfn_entries:
            sig = self.parser.parse(entry)
            signatures.append(sig)

        return signatures

    def _extract_xfn_entries(self, scr_path: Path) -> List[str]:
        """
        Extract XFN name entries from a .scr file.

        This uses the existing SCRFile loader to parse the file
        and extract XFN table entries.
        """
        # Import here to avoid circular imports
        from ..core.loader import SCRFile

        scr = SCRFile.load(str(scr_path))
        return [entry.name for entry in scr.xfn_table.entries]


def aggregate_from_directory(
    directory: str,
    verbose: bool = False
) -> AggregationResult:
    """
    Convenience function to aggregate XFN entries from a directory.

    Args:
        directory: Path to directory containing .scr files
        verbose: If True, print progress

    Returns:
        AggregationResult
    """
    aggregator = XFNAggregator(verbose=verbose)
    return aggregator.scan_directory(directory)


def merge_with_sdk(
    aggregation: AggregationResult,
    sdk_path: str,
    output_path: Optional[str] = None
) -> dict:
    """
    Merge aggregated functions with existing SDK database.

    New functions from aggregation are added; existing functions
    are kept (SDK is considered authoritative for function signatures
    that exist in both).

    Args:
        aggregation: Result from XFN aggregation
        sdk_path: Path to existing SDK functions.json
        output_path: Optional path to write merged result

    Returns:
        Merged function database as dict
    """
    # Load existing SDK
    with open(sdk_path, 'r', encoding='utf-8') as f:
        sdk_functions = json.load(f)

    # Get aggregated functions in SDK format
    xfn_functions = aggregation.to_sdk_format()

    # Count new vs existing
    new_count = 0
    existing_count = 0

    # Merge: add new functions, keep existing ones
    merged = dict(sdk_functions)  # Start with SDK
    for name, func_data in xfn_functions.items():
        if name not in merged:
            merged[name] = func_data
            new_count += 1
        else:
            existing_count += 1

    # Optionally save
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2)

    return merged
