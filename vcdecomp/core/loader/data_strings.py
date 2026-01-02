"""
Data segment string extraction for SCR bytecode.

Extracts null-terminated ASCII strings from the data segment.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DataStringExtractor:
    """
    Extracts strings from SCR data segment.

    The data segment contains:
    - Constants (ints, floats)
    - Null-terminated ASCII strings
    - Array data
    - Struct initializers

    This extractor finds null-terminated strings and creates mapping:
    offset → string content
    """

    def __init__(self, min_length: int = 3):
        """
        Initialize extractor.

        Args:
            min_length: Minimum string length to consider valid (default: 3)
        """
        self.min_length = min_length
        self.strings: Dict[int, str] = {}  # offset → string

    def extract_strings(self, data_bytes: bytes) -> Dict[int, str]:
        """
        Extract all null-terminated strings from data segment.

        Args:
            data_bytes: Raw bytes from data segment

        Returns:
            Dictionary mapping offset → string content
        """
        self.strings = {}
        offset = 0
        length = len(data_bytes)

        while offset < length:
            # Try to read a string starting at this offset
            string_data = self._try_read_string(data_bytes, offset)

            if string_data is not None:
                string_value, string_len = string_data
                self.strings[offset] = string_value
                logger.debug(f"String at offset {offset}: \"{string_value}\"")
                # Skip past the string (including null terminator)
                offset += string_len + 1
            else:
                # Not a valid string, move to next byte
                offset += 1

        logger.info(f"Extracted {len(self.strings)} strings from data segment")
        return self.strings

    def _try_read_string(self, data: bytes, offset: int) -> Optional[Tuple[str, int]]:
        """
        Try to read a null-terminated ASCII string at given offset.

        Returns:
            (string_value, length) if valid string found, None otherwise
        """
        if offset >= len(data):
            return None

        # Find null terminator
        end = offset
        chars = []
        printable_count = 0

        while end < len(data) and data[end] != 0:
            byte = data[end]

            # Check if printable ASCII
            if 32 <= byte < 127:  # Printable ASCII range
                chars.append(chr(byte))
                printable_count += 1
            elif byte in (9, 10, 13):  # Tab, LF, CR
                chars.append(chr(byte))
            else:
                # Non-printable character - not a valid string
                return None

            end += 1

            # Safety limit: strings longer than 1024 chars are suspicious
            if end - offset > 1024:
                return None

        # Check if we found a null terminator
        if end >= len(data) or data[end] != 0:
            return None

        string_len = end - offset

        # Check minimum length and printable ratio
        if string_len < self.min_length:
            return None

        # Require at least 80% printable characters
        if printable_count / string_len < 0.8:
            return None

        string_value = ''.join(chars)
        return (string_value, string_len)

    def get_string_at_offset(self, offset: int) -> Optional[str]:
        """Get string at specific offset."""
        return self.strings.get(offset)

    def find_string(self, content: str) -> Optional[int]:
        """Find offset of string with given content."""
        for offset, string in self.strings.items():
            if string == content:
                return offset
        return None

    def get_all_strings(self) -> Dict[int, str]:
        """Get all extracted strings."""
        return self.strings.copy()


def extract_data_strings(data_bytes: bytes, min_length: int = 3) -> Dict[int, str]:
    """
    Convenience function to extract strings from data segment.

    Args:
        data_bytes: Raw data segment bytes
        min_length: Minimum string length (default: 3)

    Returns:
        Dictionary mapping offset → string
    """
    extractor = DataStringExtractor(min_length=min_length)
    return extractor.extract_strings(data_bytes)
