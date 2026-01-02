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

    # Special cases: common integer values should NOT be floats
    # 0, 1, -1, small integers are almost never intended as floats
    if val in [0, 1, 2, 3, 4, 5, 0xFFFFFFFF]:  # Common int values
        return False

    # Convert to float and check if it's a reasonable value
    try:
        f = struct.unpack('<f', struct.pack('<I', val))[0]

        # Filter out NaN and Inf
        if f != f or abs(f) > 1e30:  # NaN or Inf
            return False

        # Only consider it a float if:
        # 1. It's a reasonable range (not tiny denormal)
        # 2. It looks like a float value (has decimal or exponent)
        if abs(f) < 1e-10 and f != 0.0:  # Too small (denormal)
            return False

        str_repr = str(f)
        # Must have decimal point AND reasonable magnitude
        if '.' in str_repr and (abs(f) >= 0.1 or f == 0.0):
            return True

    except:
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
    # Format with 'f' suffix for C compatibility
    return f"{f}f"


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

        # Float types
        if 'float' in type_hint.lower():
            val = self.data_segment.get_dword(byte_offset)
            return _format_float(val)

        # Integer types (int, dword, void*, BOOL, etc.)
        val = self.data_segment.get_dword(byte_offset)

        # Heuristic float detection (for 'unknown' type)
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
