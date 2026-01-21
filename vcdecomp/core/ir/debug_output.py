"""
Debug output control for the decompiler.

This module provides a global debug output flag and utility function
that can be controlled via the --debug/--verbose CLI flags.

Note: This is a standalone module with no dependencies on other
vcdecomp modules to avoid circular imports.
"""

import sys

# =============================================================================
# Global debug output control
# =============================================================================
# Set by cmd_structure() based on --debug/--verbose flags:
# - default (no flags): DEBUG_ENABLED = False (clean output)
# - --debug or --verbose: DEBUG_ENABLED = True
DEBUG_ENABLED = False  # Default to disabled (clean output by default)


def set_debug_enabled(enabled: bool):
    """
    Set global debug output state.

    Called by orchestrator based on --style CLI flag.

    Args:
        enabled: True to enable DEBUG output, False to suppress it
    """
    global DEBUG_ENABLED
    DEBUG_ENABLED = enabled


def debug_print(msg: str):
    """
    Print DEBUG message to stderr if debug output is enabled.

    Use this instead of print(f"DEBUG: ...", file=sys.stderr) to allow
    the --style flag to control debug output.

    Args:
        msg: Message to print (will be prefixed with "DEBUG " automatically
             if not already starting with "DEBUG")
    """
    if DEBUG_ENABLED:
        # Normalize message prefix
        if not msg.startswith("DEBUG"):
            msg = f"DEBUG: {msg}"
        print(msg, file=sys.stderr)
