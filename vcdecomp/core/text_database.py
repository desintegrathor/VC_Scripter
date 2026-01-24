"""Parser for Vietcong INGAME_TEXT.TXT database.

This module parses the game's text database and provides text ID to string mapping.
Used for annotating decompiled code with human-readable text strings.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Path to bundled database
_DATA_DIR = Path(__file__).parent.parent / 'data'
_DEFAULT_TEXT_DB = _DATA_DIR / 'INGAME_TEXT.TXT'

# Cached database singleton
_cached_database: Optional[Dict[int, str]] = None


def parse_ingame_text(path: str | Path) -> Dict[int, str]:
    """Parse INGAME_TEXT.TXT and return {id: text} mapping.

    Format variants:
        #3471: \t#ame Find the pilot
        #8180  : \t#ame Mission name

    Args:
        path: Path to the INGAME_TEXT.TXT file

    Returns:
        Dictionary mapping text ID (int) to text string
    """
    result: Dict[int, str] = {}
    # Pattern handles optional spaces before colon: #ID: or #ID  :
    pattern = re.compile(r'^#(\d+)\s*:\s*#ame\s*(.*)$')

    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            match = pattern.match(line)
            if match:
                text_id = int(match.group(1))
                text = match.group(2).strip()
                if text:  # Only store non-empty texts
                    result[text_id] = text

    return result


def get_text_database() -> Dict[int, str]:
    """Load the bundled INGAME_TEXT.TXT database (cached).

    Returns:
        Dictionary mapping text ID to text string.
        Empty dict if database file not found.
    """
    global _cached_database

    if _cached_database is not None:
        return _cached_database

    if _DEFAULT_TEXT_DB.exists():
        _cached_database = parse_ingame_text(_DEFAULT_TEXT_DB)
    else:
        _cached_database = {}

    return _cached_database


def get_text(text_id: int) -> Optional[str]:
    """Get text string by ID.

    Args:
        text_id: The text ID to look up

    Returns:
        Text string if found, None otherwise
    """
    db = get_text_database()
    return db.get(text_id)


def format_text_annotation(text_ids: list[int], max_length: int = 80) -> Optional[str]:
    """Format text IDs as annotation comment.

    Args:
        text_ids: List of text IDs to include
        max_length: Maximum length of the annotation (truncate if longer)

    Returns:
        Formatted annotation string like "9136: \"Air Recon\" | 9137: \"description\""
        or None if no texts found
    """
    db = get_text_database()
    parts = []

    for tid in text_ids:
        text = db.get(tid)
        if text:
            # Truncate individual text if too long
            if len(text) > 40:
                text = text[:37] + "..."
            parts.append(f'{tid}: "{text}"')

    if not parts:
        return None

    result = " | ".join(parts)

    # Truncate entire annotation if too long
    if len(result) > max_length:
        result = result[:max_length - 3] + "..."

    return result


# Functions that should have text annotations
TEXT_ANNOTATION_FUNCTIONS = frozenset({
    'SC_ShowMovieInfo',
    'SC_MissionSave',
    'SC_SetObjectives',
    'SC_GameInfo',
    'SC_Wtxt',
})


def should_annotate_function(func_name: str) -> bool:
    """Check if function calls should have text annotations.

    Args:
        func_name: Name of the external function

    Returns:
        True if this function uses text IDs that should be annotated
    """
    return func_name in TEXT_ANNOTATION_FUNCTIONS


# Reasonable range for text IDs in Vietcong (based on INGAME_TEXT.TXT)
TEXT_ID_MIN = 100
TEXT_ID_MAX = 100000


@dataclass
class StructTextIDs:
    """Text IDs assigned to a struct before function call."""
    var_name: str
    text_ids: List[int] = field(default_factory=list)
    field_offsets: List[int] = field(default_factory=list)


class StructAssignmentTracker:
    """Tracks constant assignments to struct fields for text annotation.

    This class monitors ASGN instructions that store constants into local
    variables (potential struct fields). When a function like SC_MissionSave
    is called with a struct pointer, we can look up what values were assigned
    to that struct's fields.

    Example:
        local_80.field0 = 9136;  // tracked: local_80 @ offset 0 = 9136
        local_80.field1 = 9137;  // tracked: local_80 @ offset 1 = 9137
        SC_MissionSave(&local_80);  // -> annotation: 9136: "..." | 9137: "..."
    """

    def __init__(self):
        # var_base_name -> {field_offset: constant_value}
        # Example: {"local_80": {0: 9136, 1: 9137}}
        self._assignments: Dict[str, Dict[int, int]] = {}

    def track_assignment(self, target: str, value: int, offset: int = 0) -> None:
        """Track assignment of constant to struct field.

        Args:
            target: Target variable name (e.g., "local_80" or "local_80.field0")
            value: The constant value being assigned
            offset: Field offset (0 if assigning to base variable)
        """
        # Skip values outside reasonable text ID range
        if not (TEXT_ID_MIN <= value <= TEXT_ID_MAX):
            return

        # Parse target to extract base variable name and field offset
        base_name, field_offset = self._parse_target(target)
        if base_name is None:
            return

        # Use explicit offset if provided, otherwise use parsed field offset
        final_offset = offset if offset != 0 else field_offset

        # Store the assignment
        if base_name not in self._assignments:
            self._assignments[base_name] = {}
        self._assignments[base_name][final_offset] = value

    def _parse_target(self, target: str) -> Tuple[Optional[str], int]:
        """Parse target string to extract base name and field offset.

        Args:
            target: Variable name like "local_80", "local_80.field0", "local_80.savename_id",
                   "local_63[0].y", "local_63[0]"

        Returns:
            Tuple of (base_name, field_offset). base_name is None if not parseable.
        """
        if not target:
            return None, 0

        # Handle array indexing: local_63[0].y -> local_63
        array_match = re.match(r'^(local_\d+)\[\d+\]', target)
        if array_match:
            base_name = array_match.group(1)
            # Try to extract field offset from remaining part
            remaining = target[len(array_match.group(0)):]
            if remaining.startswith('.'):
                field_part = remaining[1:]
                return self._parse_field_offset(base_name, field_part)
            # Just array access without field: local_63[0]
            return base_name, 0

        # Handle field access: local_X.fieldN or local_X.name
        if '.' in target:
            parts = target.split('.', 1)
            base_name = parts[0]
            field_part = parts[1]
            return self._parse_field_offset(base_name, field_part)

        # Simple variable name: local_80
        if target.startswith('local_'):
            return target, 0

        return None, 0

    def _parse_field_offset(self, base_name: str, field_part: str) -> Tuple[str, int]:
        """Parse field part to get offset.

        Args:
            base_name: The base variable name (e.g., "local_80")
            field_part: The field name (e.g., "field0", "y", "savename_id")

        Returns:
            Tuple of (base_name, field_offset)
        """
        # Try to extract numeric offset from field name
        # Patterns: field0, field1, field_0, field_1
        match = re.match(r'field_?(\d+)', field_part)
        if match:
            return base_name, int(match.group(1))

        # Common vector/struct fields
        vector_fields = {'x': 0, 'y': 1, 'z': 2, 'w': 3}
        if field_part in vector_fields:
            return base_name, vector_fields[field_part]

        # Known struct field names that contain text IDs
        text_id_fields = {
            'savename_id': 0,
            'description_id': 1,
            'text_id': 0,
            'status': 1,
        }
        if field_part in text_id_fields:
            return base_name, text_id_fields[field_part]

        # Unknown field - use offset 0 as fallback
        return base_name, 0

    def get_text_ids_for_var(self, var_name: str) -> List[int]:
        """Get all numeric values assigned to a variable's fields.

        Args:
            var_name: Variable name (e.g., "local_80" from "&local_80")

        Returns:
            List of text IDs sorted by field offset
        """
        # Strip address-of operator if present
        if var_name.startswith('&'):
            var_name = var_name[1:]

        if var_name not in self._assignments:
            return []

        # Return values sorted by field offset
        field_values = self._assignments[var_name]
        sorted_items = sorted(field_values.items(), key=lambda x: x[0])
        return [value for offset, value in sorted_items]

    def get_struct_text_ids(self, var_name: str) -> Optional[StructTextIDs]:
        """Get structured information about text IDs for a variable.

        Args:
            var_name: Variable name (e.g., "local_80")

        Returns:
            StructTextIDs with all tracked information, or None if no data
        """
        if var_name.startswith('&'):
            var_name = var_name[1:]

        if var_name not in self._assignments:
            return None

        field_values = self._assignments[var_name]
        sorted_items = sorted(field_values.items(), key=lambda x: x[0])

        return StructTextIDs(
            var_name=var_name,
            text_ids=[value for offset, value in sorted_items],
            field_offsets=[offset for offset, value in sorted_items],
        )

    def clear(self) -> None:
        """Clear all tracked assignments."""
        self._assignments.clear()

    def clear_var(self, var_name: str) -> None:
        """Clear assignments for a specific variable."""
        if var_name.startswith('&'):
            var_name = var_name[1:]
        self._assignments.pop(var_name, None)
