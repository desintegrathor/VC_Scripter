"""
Unit tests for function boundary detection using RET instructions.

Tests the improved function detection algorithm that uses RET instructions
to accurately detect function boundaries, preventing unreachable code from
appearing after return statements.
"""

import pytest
from vcdecomp.core.loader.scr_loader import SCRFile
from vcdecomp.core.disasm.opcodes import OpcodeResolver
from vcdecomp.core.ir.function_detector import (
    detect_function_boundaries_v2,
    detect_function_boundaries_call_only,
)


class TestFunctionDetectorBasic:
    """Basic functionality tests for function detector."""

    def test_detect_boundaries_v2_exists(self):
        """Test that detect_function_boundaries_v2 is callable."""
        assert callable(detect_function_boundaries_v2)

    def test_detect_boundaries_call_only_exists(self):
        """Test that detect_function_boundaries_call_only is callable."""
        assert callable(detect_function_boundaries_call_only)


class TestFunctionDetectorLEVEL:
    """
    Tests for LEVEL.scr function boundary detection.

    LEVEL.scr contains the problematic functions 291-353 that were merged
    together in the old implementation, causing unreachable code after returns.

    Expected functions from LEVEL_disasm.asm:
    - Function 1: addresses 291-312 (ends with RET at 312)
    - Function 2: addresses 313-331 (ends with RET at 331)
    - Function 3: addresses 332-353 (ends with RET at 353)
    """

    @pytest.fixture
    def level_scr(self):
        """Load LEVEL.scr for testing."""
        try:
            scr = SCRFile.load("decompilation/TUNNELS01/SCRIPTS/LEVEL.scr")
            return scr
        except FileNotFoundError:
            pytest.skip("LEVEL.scr not found, skipping integration test")

    @pytest.fixture
    def resolver(self, level_scr):
        """Create resolver for LEVEL.scr."""
        return level_scr.opcode_resolver

    def test_separate_functions_after_ret(self, level_scr, resolver):
        """
        Test that CALL-based function detection works correctly.

        LEVEL.SCR has 28 functions according to SaveInfo.
        Functions should be detected based on CALL targets + entry point,
        not every RET instruction (which would create 240+ fragmented functions).

        Address 291 IS a CALL target (func_0291).
        Addresses 313 and 332 are NOT CALL targets (orphan code merged into surrounding functions).
        Address 354 IS a CALL target (func_0354).
        """
        boundaries = detect_function_boundaries_v2(
            level_scr,
            resolver,
            entry_point=level_scr.header.enter_ip
        )

        # Should have ~28 functions (not 240+)
        assert 25 <= len(boundaries) <= 30, \
            f"Expected ~28 functions, got {len(boundaries)}"

        # Check that CALL target functions are detected
        func_291 = None
        func_354 = None

        for func_name, (start, end) in boundaries.items():
            if start == 291:
                func_291 = (func_name, start, end)
            elif start == 354:
                func_354 = (func_name, start, end)

        # CALL targets should be detected
        assert func_291 is not None, "Function at address 291 (CALL target) not detected"
        assert func_354 is not None, "Function at address 354 (CALL target) not detected"

        # Function 291: should end at 312 (first RET after start)
        assert func_291[2] == 312, f"Function 291 should end at 312, got {func_291[2]}"

        # Function 354: should end at 364 (first RET after start)
        assert func_354[2] == 364, f"Function 354 should end at 364, got {func_354[2]}"

    def test_v2_detects_more_functions_than_call_only(self, level_scr, resolver):
        """Test that v2 detects more functions than CALL-only method."""
        boundaries_v2 = detect_function_boundaries_v2(
            level_scr,
            resolver,
            entry_point=level_scr.header.enter_ip
        )

        boundaries_call = detect_function_boundaries_call_only(
            level_scr,
            resolver,
            entry_point=level_scr.header.enter_ip
        )

        # V2 should detect at least as many functions as CALL-only
        # (likely more due to orphan functions)
        assert len(boundaries_v2) >= len(boundaries_call), \
            f"V2 detected {len(boundaries_v2)} functions, " \
            f"CALL-only detected {len(boundaries_call)}"


class TestFunctionDetectorOutput:
    """
    Tests for decompiled output quality.

    Ensures that the new function detector produces output without
    unreachable code after return statements.
    """

    @pytest.fixture
    def level_scr(self):
        """Load LEVEL.scr for testing."""
        try:
            scr = SCRFile.load("decompilation/TUNNELS01/SCRIPTS/LEVEL.scr")
            return scr
        except FileNotFoundError:
            pytest.skip("LEVEL.scr not found, skipping integration test")

    def test_no_unreachable_code_after_return(self, level_scr):
        """
        Test that decompiled output doesn't have unreachable statements.

        This is an integration test that decompiles LEVEL.scr and checks
        that there's no code after return statements within if/else branches.

        The dead code elimination should filter out unreachable blocks,
        but some valid patterns like "if {...return} else {...return}" followed
        by an unreachable return are acceptable (the unreachable return will be
        at the end of the function).
        """
        from vcdecomp.core.disasm.disassembler import Disassembler
        from vcdecomp.core.ir.ssa import build_ssa_all_blocks
        from vcdecomp.core.ir.structure import format_structured_function_named

        # Setup
        disasm = Disassembler(level_scr)
        func_bounds = disasm.get_function_boundaries_v2()
        ssa_func = build_ssa_all_blocks(level_scr)

        # Decompile all functions
        all_output = []
        for func_name, (start, end) in sorted(func_bounds.items(), key=lambda x: x[1][0]):
            output = format_structured_function_named(
                ssa_func,
                func_name,
                start,
                end,
                function_bounds=func_bounds
            )
            all_output.append(output)

        full_output = "\n".join(all_output)
        lines = full_output.split('\n')

        # Check for unreachable code after return
        # We use a more sophisticated approach: track brace depth to properly
        # identify function boundaries and nested blocks
        current_function = None
        brace_depth = 0
        return_seen_at_depth = {}

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()

            # Track function start
            if any(stripped.startswith(t) for t in ["int ", "void ", "float ", "double "]):
                if "(" in stripped and ")" in stripped and "{" not in stripped:
                    current_function = stripped
                    brace_depth = 0
                    return_seen_at_depth = {}
                    continue

            if not current_function:
                continue

            # Track braces
            brace_depth += stripped.count("{")
            brace_depth -= stripped.count("}")

            # Function ended
            if brace_depth == 0 and "}" in stripped:
                current_function = None
                return_seen_at_depth = {}
                continue

            # Detect return statements
            if "return" in stripped and not stripped.startswith("//"):
                if "return " in stripped or stripped == "return;":
                    return_seen_at_depth[brace_depth] = line_num

            # Check for unreachable code: statement after return at SAME depth
            # (but allow closing braces and opening new blocks)
            if brace_depth > 0 and brace_depth in return_seen_at_depth:
                # Check if this is actual code (not brace, not comment)
                is_code = (stripped and
                          stripped != "}" and
                          stripped != "{" and
                          not stripped.startswith("//") and
                          not stripped.startswith("if ") and
                          not stripped.startswith("else") and
                          not stripped.startswith("while ") and
                          not stripped.startswith("for ") and
                          not "return" in stripped)  # Allow multiple returns

                if is_code:
                    pytest.fail(
                        f"Unreachable code in {current_function} at line {line_num}:\n"
                        f"  {stripped}\n"
                        f"  Previous return was at line {return_seen_at_depth[brace_depth]}"
                    )


class TestFunctionDetectorEdgeCases:
    """Tests for edge cases in function detection."""

    def test_function_without_ret(self):
        """
        Test handling of functions without RET (e.g., infinite loops).

        Note: This is a synthetic test - we'd need to create a test SCR file
        or mock the data structures to properly test this.
        """
        # TODO: Implement when we have test SCR files
        pass

    def test_empty_function(self):
        """
        Test handling of empty functions (only RET instruction).

        Note: This is a synthetic test - we'd need to create a test SCR file
        or mock the data structures to properly test this.
        """
        # TODO: Implement when we have test SCR files
        pass

    def test_entry_point_handling(self):
        """
        Test that entry point (ScriptMain) is correctly identified.

        Note: This requires a real SCR file with known entry point.
        """
        # TODO: Implement with known test case
        pass


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
