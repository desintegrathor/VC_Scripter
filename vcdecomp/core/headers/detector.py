"""
Header file detection for automatic #include generation.

Analyzes decompiled scripts to determine which header files
should be included based on:
- XFN table function usage
- Script type (level, player, object, multiplayer)
- Constant usage patterns
"""

from typing import List, Set
from pathlib import Path
from ..loader.scr_loader import SCRFile


class HeaderDetector:
    """Detects which header files should be included for a script."""

    def __init__(self, scr_file: SCRFile):
        self.scr = scr_file
        self.headers: Set[str] = set()

    def detect_headers(self) -> List[str]:
        """
        Detect all required headers for this script.

        Returns:
            List of header include paths in order of inclusion
        """
        # Always include base headers
        self.headers.add("<inc\\sc_global.h>")
        self.headers.add("<inc\\sc_def.h>")

        # Detect from XFN table
        self._detect_from_xfn()

        # Detect from script type
        self._detect_from_script_type()

        # Convert to ordered list
        # Order matters: sc_global first, sc_def second, then others
        ordered = []
        if "<inc\\sc_global.h>" in self.headers:
            ordered.append("<inc\\sc_global.h>")
        if "<inc\\sc_def.h>" in self.headers:
            ordered.append("<inc\\sc_def.h>")

        # Add remaining headers in alphabetical order
        for header in sorted(self.headers):
            if header not in ordered:
                ordered.append(header)

        return ordered

    def _detect_from_xfn(self):
        """Detect headers based on XFN table function names."""
        if not self.scr.xfn_table:
            return

        # Collect all function names
        func_names = set()
        # XFNTable has entries attribute
        xfn_entries = getattr(self.scr.xfn_table, 'entries', [])
        for xfn in xfn_entries:
            if xfn.name:
                # Extract function name (before parentheses)
                paren_idx = xfn.name.find('(')
                func_name = xfn.name[:paren_idx] if paren_idx > 0 else xfn.name
                func_names.add(func_name)

        # Multiplayer functions
        mp_functions = {'SC_MP_', 'SC_NET_'}
        if any(any(func.startswith(prefix) for prefix in mp_functions) for func in func_names):
            self.headers.add("<inc\\mplevel.inc>")

        # Equipment functions
        if any('Equip_US_' in func or 'EQUIP_US_' in func for func in func_names):
            self.headers.add("<inc\\us_equips.inc>")
        if any('Equip_VC_' in func or 'EQUIP_VC_' in func for func in func_names):
            self.headers.add("<inc\\vc_equips.inc>")

        # Briefing functions
        briefing_funcs = {'SC_Briefing_', 'SC_BRIEF_'}
        if any(any(func.startswith(prefix) for prefix in briefing_funcs) for func in func_names):
            self.headers.add("<inc\\BRIEFING.H>")

        # Level scripting functions
        level_funcs = {'SC_LevScr_', 'SC_Level_'}
        if any(any(func.startswith(prefix) for prefix in level_funcs) for func in func_names):
            self.headers.add("<inc\\sc_level.h>")

    def _detect_from_script_type(self):
        """Detect headers based on script type (from entry point signature)."""
        # This would require analyzing the entry point to determine parameter types
        # For now, we rely on XFN detection
        # Future enhancement: detect s_SC_L_info vs s_SC_P_info vs s_SC_OBJ_info
        pass

    def generate_include_block(self) -> str:
        """
        Generate the complete #include block for the script.

        Returns:
            Multi-line string with all #include directives
        """
        headers = self.detect_headers()
        lines = [f"#include {header}" for header in headers]
        return "\n".join(lines)


def detect_headers_for_script(scr_file: SCRFile) -> List[str]:
    """
    Convenience function to detect headers for a script.

    Args:
        scr_file: Loaded SCR file

    Returns:
        List of header include paths
    """
    detector = HeaderDetector(scr_file)
    return detector.detect_headers()


def generate_include_block(scr_file: SCRFile) -> str:
    """
    Generate #include block for a script.

    Args:
        scr_file: Loaded SCR file

    Returns:
        Multi-line string with #include directives
    """
    detector = HeaderDetector(scr_file)
    return detector.generate_include_block()
