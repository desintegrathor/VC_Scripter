"""
Data Resolver - Type-Aware Data Segment Reading with Caching.

Centralizuje logiku pro čtení hodnot z data segmentu s oh ledem na inferred types.
Poskytuje caching pro opakované přístupy a clean separation of concerns.
"""

from typing import Dict, Optional, Tuple
from ..loader.scr_loader import DataSegment
from .global_resolver import GlobalUsage


def _is_likely_float(val: int) -> bool:
    """
    Heuristika pro detekci float hodnot uložených jako int.

    Args:
        val: 32-bit integer value

    Returns:
        True if value looks like a float
    """
    import struct
    import math

    # FIXED: Allow 0 as 0.0f (valid float constant)
    # Removed exclusion: if val == 0: return False

    # FIXED: Narrowed range exclusion from [0,1,2,3,4,5] to [1,2,3,4,5]
    # This allows 0.0f while still filtering very small integers
    if val in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0xFFFFFFFF]:  # Common small int values
        return False

    # Convert to float and check if it's a reasonable value
    try:
        f = struct.unpack('<f', struct.pack('<I', val))[0]

        # Filter out NaN and Inf
        if math.isnan(f) or math.isinf(f):
            return False

        # Rozumný rozsah pro herní konstanty
        if abs(f) > 1e6 or (abs(f) < 1e-6 and f != 0.0):
            return False

        # Kontrola zda je to "hezká" hodnota
        # Celá čísla nebo hodnoty s max 2 desetinnými místy
        if f == int(f):
            return True

        # Hodnoty jako 0.5, 0.25, 0.75, 1.5, etc.
        rounded = round(f, 2)
        if abs(f - rounded) < 1e-5:
            return True

        # FIXED: Expanded common_floats to include more whole number floats
        # Added: 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, 100.0 explicitly
        common_floats = {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                        1.0, 1.1, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0,
                        10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 100.0,
                        0.05, 0.075, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65}
        if rounded in common_floats or round(f, 3) in common_floats:
            return True

    except (struct.error, OverflowError):
        pass

    return False


def _format_float(val: int) -> str:
    """
    Format 32-bit value as float.

    Args:
        val: Integer representation of float (IEEE 754)

    Returns:
        Formatted float string with 'f' suffix
    """
    import struct
    f = struct.unpack('<f', struct.pack('<I', val))[0]

    # FIXED: Handle 0.0f explicitly
    if f == 0.0:
        return "0.0f"

    if f == int(f):
        return f"{int(f)}.0f"

    # FIXED: Increased precision from default to 6 decimal places
    rounded = round(f, 6)
    if rounded == int(rounded):
        return f"{int(rounded)}.0f"

    # FIXED: Add scientific notation for extreme values
    if abs(f) >= 1e4 or (abs(f) < 1e-3 and f != 0.0):
        return f"{f:.6e}f"

    return f"{rounded}f"


class DataResolver:
    """
    Type-aware data segment value resolver with caching.

    Provides clean interface for reading data segment values with automatic
    type detection based on:
    1. Explicit expected_type (from function signatures)
    2. Inferred types (from TypeInferenceEngine via GlobalResolver)
    3. Heuristic fallback (float detection, string extraction)

    Features:
    - Type-aware reading (int, float, char*, void*)
    - Confidence-based type selection
    - Value caching for performance
    - Clean separation from ExpressionFormatter
    """

    def __init__(self,
                 data_segment: DataSegment,
                 global_type_info: Dict[int, GlobalUsage],
                 confidence_threshold: float = 0.70):
        """
        Initialize DataResolver.

        Args:
            data_segment: Data segment from SCR file
            global_type_info: GlobalUsage dict from GlobalResolver
            confidence_threshold: Minimum confidence to use inferred type (default: 0.70)
        """
        self.data_segment = data_segment
        self.type_info = global_type_info
        self.threshold = confidence_threshold
        # Cache: (offset, expected_type, is_address) → formatted value
        self._cache: Dict[Tuple[int, Optional[str], bool], str] = {}

    def resolve_value(self,
                     offset: int,
                     expected_type: Optional[str] = None,
                     is_address: bool = False) -> str:
        """
        Resolve data segment value with type awareness.

        Args:
            offset: Word offset (NOT byte offset!)
            expected_type: Explicit type hint (e.g., from function signature)
            is_address: Whether this is a pointer to data (affects string rendering)

        Returns:
            Formatted value string ready for C output
        """
        # Check cache
        cache_key = (offset, expected_type, is_address)
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Determine type
        resolved_type = self._determine_type(offset, expected_type)

        # Read value based on type
        value = self._read_typed_value(offset, resolved_type, is_address)

        # Cache and return
        self._cache[cache_key] = value
        return value

    def _determine_type(self, offset: int, expected_type: Optional[str] = None) -> str:
        """
        Determine type for data value.

        Priority order:
        1. Explicit expected_type (from caller, e.g., function signature)
        2. Inferred type (from TypeInferenceEngine if confidence >= threshold)
        3. Fallback to 'unknown' (will use heuristics)

        Args:
            offset: Word offset
            expected_type: Explicit type hint

        Returns:
            Type string (e.g., 'int', 'float', 'char*', 'unknown')
        """
        # Priority 1: Explicit expected type
        if expected_type:
            return expected_type

        # Priority 2: Inferred type (if confidence high enough)
        if offset in self.type_info:
            usage = self.type_info[offset]
            if usage.inferred_type and usage.type_confidence >= self.threshold:
                return usage.inferred_type

        # Priority 3: Unknown (will use heuristics)
        return 'unknown'

    def _read_typed_value(self, offset: int, type_hint: str, is_address: bool) -> str:
        """
        Read value from data segment based on type hint.

        Args:
            offset: Word offset
            type_hint: Type string ('int', 'float', 'char*', 'unknown')
            is_address: Pointer to data

        Returns:
            Formatted value string
        """
        byte_offset = offset * 4  # Convert word offset to byte offset

        # String types (char*, string)
        if 'char*' in type_hint or 'string' in type_hint.lower():
            s = self.data_segment.get_string(byte_offset)
            if s:
                escaped = self._escape_string(s)
                return f'&"{escaped}"' if is_address else f'"{escaped}"'
            # Fallback: if no string found, treat as int

        # Float types (but NOT float pointers!)
        # '*float' is a pointer to float, NOT a float value - check for non-pointer first
        if 'float' in type_hint.lower() and '*' not in type_hint:
            val = self.data_segment.get_dword(byte_offset)
            return _format_float(val)

        # Pointer types (void*, float*, char* for data, etc.) - pass through as integers
        # A value of 0 for a pointer type is NULL
        if '*' in type_hint:
            val = self.data_segment.get_dword(byte_offset)
            if val > 0x7FFFFFFF:
                val = val - 0x100000000
            return str(val)  # Return as integer (NULL is 0)

        # Integer types (int, dword, void*, BOOL, etc.)
        val = self.data_segment.get_dword(byte_offset)

        # FIXED (Phase 3): Heuristic float detection for 'unknown' type ONLY
        # When type_hint is explicitly 'int', 'dword', etc. (from context or function signature),
        # we must respect that and NOT override with float heuristic.
        # Only apply float heuristic when type is truly unknown.
        if type_hint == 'unknown' and _is_likely_float(val):
            return _format_float(val)

        # Signed conversion for negative integers
        if val > 0x7FFFFFFF:
            val = val - 0x100000000

        return str(val)

    def _escape_string(self, s: str) -> str:
        """
        Escape string for C output.

        Args:
            s: Raw string

        Returns:
            Escaped string with proper C escapes
        """
        escaped = (s.replace("\\", "\\\\")    # Backslash first!
                   .replace('"', '\\"')        # Double quote
                   .replace("\n", "\\n")       # Newline
                   .replace("\r", "\\r")       # Carriage return
                   .replace("\t", "\\t"))      # Tab

        # Limit string length for readability
        if len(escaped) > 60:
            escaped = escaped[:57] + "..."

        return escaped

    def clear_cache(self):
        """
        Clear value cache.

        Call this between functions or when re-analyzing to free memory.
        """
        self._cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics for debugging.

        Returns:
            Dict with 'size' and 'hits' (approximation)
        """
        return {
            'size': len(self._cache),
            'entries': len(self._cache)
        }
