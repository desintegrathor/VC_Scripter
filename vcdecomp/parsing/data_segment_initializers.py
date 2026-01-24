"""
Helpers for reading and formatting data segment initializers.
"""

from __future__ import annotations

from typing import Optional, Sequence

from ..core.ir.data_resolver import _format_float, _is_likely_float, DataResolver
from ..core.loader.scr_loader import DataSegment


VECTOR3_TYPES = {"c_Vector3", "c_vector3"}


def looks_like_vector3(data_segment: DataSegment, byte_offset: int) -> bool:
    """Return True if three consecutive dwords look like float values."""
    if byte_offset < 0 or byte_offset + 12 > len(data_segment.raw_data):
        return False
    dwords = [
        data_segment.get_dword(byte_offset + i * 4)
        for i in range(3)
    ]
    return all(_is_likely_float(val) for val in dwords)


def _format_vector3(dwords: Sequence[int]) -> str:
    return "{" + ", ".join(_format_float(val) for val in dwords) + "}"


def build_initializer(
    data_segment: DataSegment,
    data_resolver: DataResolver,
    byte_offset: int,
    element_type: str,
    element_size: Optional[int],
    element_count: int,
) -> Optional[str]:
    """
    Build a C initializer string for a global value or array.

    Returns None if no explicit initializer should be emitted.
    """
    if element_count <= 0:
        return None

    if byte_offset < 0 or byte_offset >= len(data_segment.raw_data):
        return None

    element_type = element_type or "int"
    element_size = element_size or 4

    is_vector3 = element_type in VECTOR3_TYPES
    # FIX: Only apply vector3 heuristic for unknown types ("dword")
    # Do NOT apply to explicit "float" or "int" types - those were inferred/specified
    # from SaveInfo or type inference and should not be expanded.
    if element_count == 1 and not is_vector3 and element_type == "dword":
        if looks_like_vector3(data_segment, byte_offset):
            element_type = "c_Vector3"
            is_vector3 = True
            element_size = 12
    if is_vector3 and element_size != 12:
        element_size = 12

    if element_type in {"int", "float", "dword", "BOOL"}:
        element_size = 4

    total_bytes = element_size * element_count
    if byte_offset + total_bytes > len(data_segment.raw_data):
        return None

    total_dwords = total_bytes // 4
    raw_values = [
        data_segment.get_dword(byte_offset + i * 4)
        for i in range(total_dwords)
    ]

    if all(val == 0 for val in raw_values):
        return None

    # FIX: Detect garbage initializers - arrays with uninitialized memory.
    # This handles cases like gRecs[12] and gRec[1536] which have no initializer
    # in the original source but the data segment contains garbage at those offsets.
    #
    # Heuristics:
    # 1. If only the first element is non-zero and looks like garbage (> 65536), skip
    # 2. If non-zeros are only at the END (after 80%+ zeros at start), and look like
    #    garbage/pointers, skip - this is likely adjacent data being read
    if element_count > 1:
        non_zero_indices = [i for i, val in enumerate(raw_values) if val != 0]

        # Case 1: Only first element is non-zero and looks like garbage
        if len(non_zero_indices) == 1 and non_zero_indices[0] == 0:
            first_val = raw_values[0]
            if first_val > 0x10000:  # > 65536
                return None

        # Case 2: Non-zeros are only in the trailing portion (last 20%) of the array
        # and the values look like garbage/pointers
        if non_zero_indices:
            min_non_zero_idx = min(non_zero_indices)
            threshold_idx = int(element_count * 0.8)  # 80% of array must be leading zeros

            if min_non_zero_idx >= threshold_idx:
                # Non-zeros are only at the end - check if they look like garbage
                non_zero_values = [raw_values[i] for i in non_zero_indices]
                # If any value is large (looks like pointer/garbage), skip initializer
                if any(val > 0x10000 for val in non_zero_values):
                    return None

    dword_offset = byte_offset // 4

    if element_count == 1:
        if is_vector3:
            if len(raw_values) < 3 or not all(_is_likely_float(val) for val in raw_values[:3]):
                return None
            return _format_vector3(raw_values[:3])

        return data_resolver.resolve_value(
            offset=dword_offset,
            expected_type=element_type,
            is_address=False,
        )

    if is_vector3:
        values = []
        for idx in range(element_count):
            base = idx * 3
            vec_vals = raw_values[base:base + 3]
            if len(vec_vals) < 3:
                return None
            values.append(_format_vector3(vec_vals))
        return "{" + ", ".join(values) + "}"

    if element_size != 4:
        return None

    values = [
        data_resolver.resolve_value(
            offset=dword_offset + idx,
            expected_type=element_type,
            is_address=False,
        )
        for idx in range(element_count)
    ]
    return "{" + ", ".join(values) + "}"
