"""
Unit tests for dead code elimination of temporary variables.

Tests the _is_unused_temporary() and _build_use_count_map() functions
from vcdecomp.core.ir.structure.analysis.variables module.

Phase 5: Dead Code Elimination for Temporary Variables
"""

import pytest
from typing import Dict, List, Set
from unittest.mock import MagicMock
from dataclasses import dataclass, field

from vcdecomp.core.ir.structure.analysis.variables import (
    _is_unused_temporary,
    _build_use_count_map,
)


# ============================================================================
# Mock Classes for Testing
# ============================================================================

@dataclass
class MockSSAValue:
    """Mock SSA value for testing."""
    name: str
    alias: str = None


@dataclass
class MockSSAInstruction:
    """Mock SSA instruction for testing."""
    mnemonic: str
    address: int
    inputs: List[MockSSAValue] = field(default_factory=list)
    outputs: List[MockSSAValue] = field(default_factory=list)


@dataclass
class MockSSAFunction:
    """Mock SSA function for testing."""
    instructions: Dict[int, List[MockSSAInstruction]] = field(default_factory=dict)


# ============================================================================
# _is_unused_temporary Tests
# ============================================================================

class TestIsUnusedTemporary:
    """Tests for the _is_unused_temporary() function."""

    def test_unused_tmp_is_eliminated(self):
        """Unused 'tmp' variable should be eliminated."""
        use_counts = {"tmp": 0, "local_1": 5}
        assert _is_unused_temporary("tmp", use_counts) is True

    def test_unused_tmp1_is_eliminated(self):
        """Unused 'tmp1' variable should be eliminated."""
        use_counts = {"tmp1": 0, "tmp2": 3}
        assert _is_unused_temporary("tmp1", use_counts) is True

    def test_unused_tmp_with_number_is_eliminated(self):
        """Unused 'tmpN' variables should be eliminated."""
        use_counts = {"tmp123": 0}
        assert _is_unused_temporary("tmp123", use_counts) is True

    def test_used_tmp_is_not_eliminated(self):
        """Used 'tmp' variable should NOT be eliminated."""
        use_counts = {"tmp": 1}
        assert _is_unused_temporary("tmp", use_counts) is False

    def test_used_tmp_multiple_uses_not_eliminated(self):
        """Heavily used 'tmp' variable should NOT be eliminated."""
        use_counts = {"tmp": 10}
        assert _is_unused_temporary("tmp", use_counts) is False

    def test_non_tmp_var_not_eliminated(self):
        """Non-tmp variables should never be eliminated even with 0 uses."""
        use_counts = {"local_1": 0}
        assert _is_unused_temporary("local_1", use_counts) is False

    def test_loop_counter_not_eliminated(self):
        """Loop counter 'i' should never be eliminated even with 0 uses."""
        use_counts = {"i": 0}
        assert _is_unused_temporary("i", use_counts) is False

    def test_return_value_temp_not_eliminated(self):
        """Return value temps (t123_ret) should NOT be eliminated."""
        use_counts = {"t123_ret": 0}
        assert _is_unused_temporary("t123_ret", use_counts) is False

    def test_ssa_temp_not_eliminated(self):
        """SSA temps (t100_0) should NOT be eliminated by this function."""
        use_counts = {"t100_0": 0}
        assert _is_unused_temporary("t100_0", use_counts) is False

    def test_missing_var_treated_as_unused(self):
        """Variable not in use_counts should be treated as unused."""
        use_counts = {"other_var": 5}
        assert _is_unused_temporary("tmp", use_counts) is True

    def test_empty_use_counts(self):
        """Empty use_counts should treat all temps as unused."""
        use_counts = {}
        assert _is_unused_temporary("tmp", use_counts) is True
        assert _is_unused_temporary("tmp1", use_counts) is True
        assert _is_unused_temporary("tmp99", use_counts) is True


# ============================================================================
# _build_use_count_map Tests
# ============================================================================

class TestBuildUseCountMap:
    """Tests for the _build_use_count_map() function."""

    def test_empty_function(self):
        """Empty function should return empty use counts."""
        ssa_func = MockSSAFunction(instructions={})
        func_block_ids = set()

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        assert use_counts == {}

    def test_single_use(self):
        """Single use of a variable should be counted."""
        ssa_func = MockSSAFunction(instructions={
            1: [MockSSAInstruction(
                mnemonic="ADD",
                address=100,
                inputs=[MockSSAValue(name="t100", alias="tmp")],
                outputs=[]
            )]
        })
        func_block_ids = {1}

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        assert use_counts.get("tmp", 0) == 1

    def test_multiple_uses_same_block(self):
        """Multiple uses of same variable in same block should be counted."""
        ssa_func = MockSSAFunction(instructions={
            1: [
                MockSSAInstruction(
                    mnemonic="ADD",
                    address=100,
                    inputs=[MockSSAValue(name="t100", alias="tmp")],
                    outputs=[]
                ),
                MockSSAInstruction(
                    mnemonic="MUL",
                    address=101,
                    inputs=[MockSSAValue(name="t100", alias="tmp")],
                    outputs=[]
                ),
            ]
        })
        func_block_ids = {1}

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        assert use_counts.get("tmp", 0) == 2

    def test_multiple_uses_different_blocks(self):
        """Uses across different blocks should be summed."""
        ssa_func = MockSSAFunction(instructions={
            1: [MockSSAInstruction(
                mnemonic="ADD",
                address=100,
                inputs=[MockSSAValue(name="t100", alias="local_1")],
                outputs=[]
            )],
            2: [MockSSAInstruction(
                mnemonic="SUB",
                address=200,
                inputs=[MockSSAValue(name="t100", alias="local_1")],
                outputs=[]
            )],
        })
        func_block_ids = {1, 2}

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        assert use_counts.get("local_1", 0) == 2

    def test_blocks_outside_function_ignored(self):
        """Blocks not in func_block_ids should be ignored."""
        ssa_func = MockSSAFunction(instructions={
            1: [MockSSAInstruction(
                mnemonic="ADD",
                address=100,
                inputs=[MockSSAValue(name="t100", alias="tmp")],
                outputs=[]
            )],
            2: [MockSSAInstruction(
                mnemonic="SUB",
                address=200,
                inputs=[MockSSAValue(name="t200", alias="other")],
                outputs=[]
            )],
        })
        func_block_ids = {1}  # Only block 1 is in function

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        assert use_counts.get("tmp", 0) == 1
        assert use_counts.get("other", 0) == 0  # Block 2 ignored

    def test_uses_name_when_no_alias(self):
        """Uses SSA name when alias is not set."""
        ssa_func = MockSSAFunction(instructions={
            1: [MockSSAInstruction(
                mnemonic="ADD",
                address=100,
                inputs=[MockSSAValue(name="t100_0", alias=None)],
                outputs=[]
            )]
        })
        func_block_ids = {1}

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        assert use_counts.get("t100_0", 0) == 1

    def test_address_of_prefix_stripped(self):
        """&prefix should be stripped from variable names."""
        ssa_func = MockSSAFunction(instructions={
            1: [MockSSAInstruction(
                mnemonic="CALL",
                address=100,
                inputs=[MockSSAValue(name="t100", alias="&local_1")],
                outputs=[]
            )]
        })
        func_block_ids = {1}

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        assert use_counts.get("local_1", 0) == 1
        assert use_counts.get("&local_1", 0) == 0  # Not counted with prefix

    def test_rename_map_applied(self):
        """Rename map should be applied to get display names."""
        ssa_func = MockSSAFunction(instructions={
            1: [MockSSAInstruction(
                mnemonic="ADD",
                address=100,
                inputs=[MockSSAValue(name="t100_0", alias=None)],
                outputs=[]
            )]
        })
        func_block_ids = {1}
        rename_map = {"t100_0": "result"}

        use_counts = _build_use_count_map(ssa_func, func_block_ids, rename_map)

        assert use_counts.get("result", 0) == 1
        assert use_counts.get("t100_0", 0) == 0  # Original name not counted

    def test_multiple_different_variables(self):
        """Multiple different variables should each be tracked."""
        ssa_func = MockSSAFunction(instructions={
            1: [
                MockSSAInstruction(
                    mnemonic="ADD",
                    address=100,
                    inputs=[
                        MockSSAValue(name="t100", alias="a"),
                        MockSSAValue(name="t200", alias="b"),
                    ],
                    outputs=[]
                ),
                MockSSAInstruction(
                    mnemonic="MUL",
                    address=101,
                    inputs=[MockSSAValue(name="t100", alias="a")],
                    outputs=[]
                ),
            ]
        })
        func_block_ids = {1}

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        assert use_counts.get("a", 0) == 2
        assert use_counts.get("b", 0) == 1


# ============================================================================
# Integration Tests
# ============================================================================

class TestDeadTempEliminationIntegration:
    """Integration tests combining use count building and elimination check."""

    def test_unused_temp_detected_and_eliminated(self):
        """Full flow: build use counts, then check elimination."""
        # Create a function with an unused temp
        ssa_func = MockSSAFunction(instructions={
            1: [
                # tmp1 is defined but never used
                MockSSAInstruction(
                    mnemonic="PUSH",
                    address=100,
                    inputs=[],
                    outputs=[MockSSAValue(name="t100", alias="tmp1")]
                ),
                # tmp2 is defined and used
                MockSSAInstruction(
                    mnemonic="PUSH",
                    address=101,
                    inputs=[],
                    outputs=[MockSSAValue(name="t200", alias="tmp2")]
                ),
                MockSSAInstruction(
                    mnemonic="ADD",
                    address=102,
                    inputs=[MockSSAValue(name="t200", alias="tmp2")],
                    outputs=[]
                ),
            ]
        })
        func_block_ids = {1}

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        # tmp1 should be unused (0 uses)
        assert _is_unused_temporary("tmp1", use_counts) is True

        # tmp2 should be used (1 use)
        assert _is_unused_temporary("tmp2", use_counts) is False

    def test_local_var_never_eliminated(self):
        """Local variables should never be eliminated regardless of use count."""
        ssa_func = MockSSAFunction(instructions={
            1: [
                # local_1 is defined but never used
                MockSSAInstruction(
                    mnemonic="PUSH",
                    address=100,
                    inputs=[],
                    outputs=[MockSSAValue(name="t100", alias="local_1")]
                ),
            ]
        })
        func_block_ids = {1}

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        # local_1 should NOT be eliminated even with 0 uses
        assert _is_unused_temporary("local_1", use_counts) is False

    def test_semantic_names_preserved(self):
        """Semantic names (i, j, k, side) should never be eliminated."""
        ssa_func = MockSSAFunction(instructions={})
        func_block_ids = set()

        use_counts = _build_use_count_map(ssa_func, func_block_ids)

        # These should never be eliminated
        assert _is_unused_temporary("i", use_counts) is False
        assert _is_unused_temporary("j", use_counts) is False
        assert _is_unused_temporary("side", use_counts) is False
        assert _is_unused_temporary("result", use_counts) is False


# ============================================================================
# Two-Pass DCE Tests (_scan_used_variables_in_code)
# ============================================================================

from vcdecomp.core.ir.structure.analysis.variables import _scan_used_variables_in_code


class TestScanUsedVariablesInCode:
    """Tests for the _scan_used_variables_in_code() function (Phase 5.5 Two-Pass DCE)."""

    def test_empty_lines(self):
        """Empty lines should return empty set."""
        code_lines = []
        used = _scan_used_variables_in_code(code_lines)
        assert used == set()

    def test_finds_simple_variables(self):
        """Simple variable names in expressions should be found."""
        code_lines = [
            "    x = y + z;",
            "    result = a * b;",
        ]
        used = _scan_used_variables_in_code(code_lines)
        assert "x" in used
        assert "y" in used
        assert "z" in used
        assert "result" in used
        assert "a" in used
        assert "b" in used

    def test_skips_declaration_only_lines(self):
        """Declaration-only lines should not count as variable usage."""
        code_lines = [
            "    int tmp;",
            "    float x;",
            "    dword result;",
        ]
        used = _scan_used_variables_in_code(code_lines)
        # These are just declarations, not usages
        assert "tmp" not in used
        assert "x" not in used
        assert "result" not in used

    def test_includes_assignment_with_declarations(self):
        """Variables in assignment declarations should be found."""
        code_lines = [
            "    int x = 5;",  # Has = so not pure declaration
            "    float y = x + 1;",
        ]
        used = _scan_used_variables_in_code(code_lines)
        # These have assignments, so identifiers should be found
        assert "x" in used
        assert "y" in used

    def test_finds_function_call_arguments(self):
        """Variables in function call arguments should be found."""
        code_lines = [
            "    SC_message(foo, bar);",
            "    result = SC_P_GetPos(player, &pos);",
        ]
        used = _scan_used_variables_in_code(code_lines)
        assert "foo" in used
        assert "bar" in used
        assert "result" in used
        assert "player" in used
        assert "pos" in used

    def test_finds_condition_variables(self):
        """Variables in conditions should be found."""
        code_lines = [
            "    if (x > 0) {",
            "        y = 5;",
            "    }",
        ]
        used = _scan_used_variables_in_code(code_lines)
        assert "x" in used
        assert "y" in used

    def test_finds_loop_variables(self):
        """Variables in loop constructs should be found."""
        code_lines = [
            "    for (i = 0; i < count; i++) {",
            "        total = total + arr[i];",
            "    }",
        ]
        used = _scan_used_variables_in_code(code_lines)
        assert "i" in used
        assert "count" in used
        assert "total" in used
        assert "arr" in used

    def test_excludes_keywords(self):
        """C keywords should be excluded."""
        code_lines = [
            "    if (x) return;",
            "    while (y) break;",
            "    for (;;) continue;",
        ]
        used = _scan_used_variables_in_code(code_lines)
        # Keywords should be excluded
        assert "if" not in used
        assert "return" not in used
        assert "while" not in used
        assert "break" not in used
        assert "for" not in used
        assert "continue" not in used
        # Variables should be found
        assert "x" in used
        assert "y" in used

    def test_excludes_type_names(self):
        """Type names should be excluded."""
        code_lines = [
            "    int foo;",  # Declaration, skipped
            "    float bar = int_val;",  # int is type, not variable
        ]
        used = _scan_used_variables_in_code(code_lines)
        assert "int" not in used
        assert "float" not in used
        assert "int_val" in used  # This is a variable name, not a type

    def test_excludes_struct_type_prefixes(self):
        """Struct type prefixes (s_SC_*, c_*) should be excluded."""
        code_lines = [
            "    s_SC_P_info info;",  # Declaration
            "    c_Vector3 pos;",  # Declaration
            "    player = s_SC_P_Create();",  # Function call, player found
        ]
        used = _scan_used_variables_in_code(code_lines)
        assert "s_SC_P_info" not in used
        assert "c_Vector3" not in used
        assert "s_SC_P_Create" not in used  # Also excluded
        assert "player" in used

    def test_inlined_temp_not_declared(self):
        """Temp that gets inlined should not appear in declarations."""
        # This simulates the case where tmp was inlined into the condition
        code_lines = [
            "    if (x > 0) {",  # tmp was inlined, x is the actual variable
            "        y = 5;",
            "    }",
        ]
        used = _scan_used_variables_in_code(code_lines)
        # tmp should not be in used set (it was inlined - doesn't appear at all)
        assert "tmp" not in used
        assert "x" in used
        assert "y" in used

    def test_used_temp_is_found(self):
        """Temp that appears in output should be found."""
        code_lines = [
            "    tmp = x + y;",
            "    result = tmp * 2;",
        ]
        used = _scan_used_variables_in_code(code_lines)
        assert "tmp" in used
        assert "result" in used
        assert "x" in used
        assert "y" in used

    def test_complex_expression_variables(self):
        """Variables in complex expressions should be found."""
        code_lines = [
            "    result = ((a + b) * c) / (d - e);",
            "    flag = (x > y) && (z != 0);",
        ]
        used = _scan_used_variables_in_code(code_lines)
        assert "result" in used
        assert "a" in used
        assert "b" in used
        assert "c" in used
        assert "d" in used
        assert "e" in used
        assert "flag" in used
        assert "x" in used
        assert "y" in used
        assert "z" in used

    def test_array_access_variables(self):
        """Variables in array access should be found."""
        code_lines = [
            "    arr[i] = value;",
            "    result = matrix[row][col];",
        ]
        used = _scan_used_variables_in_code(code_lines)
        assert "arr" in used
        assert "i" in used
        assert "value" in used
        assert "result" in used
        assert "matrix" in used
        assert "row" in used
        assert "col" in used

    def test_struct_field_access(self):
        """Variables with struct field access should be found."""
        code_lines = [
            "    player.health = 100;",
            "    x = obj->position;",
        ]
        used = _scan_used_variables_in_code(code_lines)
        assert "player" in used
        assert "health" in used  # Field name is also an identifier
        assert "x" in used
        assert "obj" in used
        assert "position" in used


class TestTwoPassDCEIntegration:
    """Integration tests for two-pass dead code elimination."""

    def test_inlined_temps_excluded_from_declarations(self):
        """
        Integration test: temps that get inlined during expression formatting
        should not appear in declarations after two-pass filtering.
        """
        # Simulate candidate declarations (from SSA lowering)
        candidates = [
            ("tmp", "int tmp"),  # Should be eliminated (not in output)
            ("tmp1", "int tmp1"),  # Should be eliminated (not in output)
            ("local_1", "int local_1"),  # Should be kept (non-temp)
            ("i", "int i"),  # Should be kept (non-temp)
        ]

        # Simulate generated code (temps were inlined)
        code_lines = [
            "    if (x > 0) {",  # tmp was inlined as comparison
            "        local_1 = 5;",  # local_1 used
            "    }",
            "    for (i = 0; i < 10; i++) {",  # i used
            "    }",
        ]

        # Scan for used variables
        used_in_output = _scan_used_variables_in_code(code_lines)

        # Filter declarations
        filtered = []
        for var_name, formatted_decl in candidates:
            base_name = var_name.split('[')[0]
            if not base_name.startswith('tmp'):
                filtered.append(formatted_decl)
            elif base_name in used_in_output:
                filtered.append(formatted_decl)

        # Verify filtering
        assert "int tmp" not in filtered  # Eliminated
        assert "int tmp1" not in filtered  # Eliminated
        assert "int local_1" in filtered  # Kept (non-temp)
        assert "int i" in filtered  # Kept (non-temp)

    def test_used_temps_kept_in_declarations(self):
        """
        Integration test: temps that ARE used in output should be kept.
        """
        candidates = [
            ("tmp", "int tmp"),  # Should be kept (used in output)
            ("tmp1", "int tmp1"),  # Should be eliminated (not used)
        ]

        code_lines = [
            "    tmp = SC_P_Get();",  # tmp is assigned
            "    SC_message(tmp);",  # tmp is used
        ]

        used_in_output = _scan_used_variables_in_code(code_lines)

        filtered = []
        for var_name, formatted_decl in candidates:
            base_name = var_name.split('[')[0]
            if not base_name.startswith('tmp'):
                filtered.append(formatted_decl)
            elif base_name in used_in_output:
                filtered.append(formatted_decl)

        assert "int tmp" in filtered  # Kept (used)
        assert "int tmp1" not in filtered  # Eliminated (not used)
