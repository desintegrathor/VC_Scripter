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
        """Detect headers based on XFN functions that are ACTUALLY CALLED in the code."""
        if not self.scr.xfn_table or not self.scr.code_segment:
            return

        # Get XCALL opcode for the current resolver
        xcall_opcode = None
        for opcode, mnemonic in self.scr.opcode_resolver.opcode_map.items():
            if mnemonic == "XCALL":
                xcall_opcode = opcode
                break
        
        if xcall_opcode is None:
            return

        # Scan code segment to find which XFN functions are actually called
        called_xfn_indices = set()
        for instr in self.scr.code_segment.instructions:
            if instr.opcode == xcall_opcode:
                # arg1 contains the XFN index
                xfn_index = instr.arg1
                # Handle signed integers (shouldn't be negative, but be safe)
                if xfn_index < 0x80000000:
                    called_xfn_indices.add(xfn_index)

        # Collect function names that are ACTUALLY called
        func_names = set()
        xfn_entries = getattr(self.scr.xfn_table, 'entries', [])
        for xfn in xfn_entries:
            if xfn.index in called_xfn_indices and xfn.name:
                # Extract function name (before parentheses)
                paren_idx = xfn.name.find('(')
                func_name = xfn.name[:paren_idx] if paren_idx > 0 else xfn.name
                func_names.add(func_name)

        # Now detect headers based on ACTUALLY CALLED functions
        # Note: SC_MP_* functions like SC_MP_EnumPlayers are in sc_global.h, not mplevel.inc
        # Only add mplevel.inc for truly multiplayer-specific level functions
        # For now, disable this detection to avoid false positives
        # TODO: Add detection for specific multiplayer level functions if needed

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