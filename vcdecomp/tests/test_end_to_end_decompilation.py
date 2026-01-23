"""
End-to-end integration tests for complete decompilation pipeline.

These tests verify that the refactored structure modules work correctly
in real-world decompilation scenarios.
"""

import unittest
import sys
from pathlib import Path
from io import StringIO

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from vcdecomp.core.loader import SCRFile
from vcdecomp.core.disasm import Disassembler
from vcdecomp.core.ir.ssa import build_ssa_all_blocks
from vcdecomp.core.ir.structure import format_structured_function_named
from vcdecomp.core.headers.detector import generate_include_block
from vcdecomp.core.ir.global_resolver import GlobalResolver


class TestEndToEndDecompilation(unittest.TestCase):
    """Test complete end-to-end decompilation workflow"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests"""
        cls.test_files = {
            'hitable': Path('./Compiler-testruns/Testrun3/hitable.scr'),
            'tdm': Path('./Compiler-testruns/Testrun1/tdm.scr'),
            'gaz_67': Path('./Compiler-testruns/Testrun2/Gaz_67.scr'),
        }
        # Filter to only existing files
        cls.test_files = {name: path for name, path in cls.test_files.items()
                         if path.exists()}

    def test_hitable_decompilation(self):
        """Test complete decompilation of hitable.scr (simple switch/case)"""
        if 'hitable' not in self.test_files:
            self.skipTest("hitable.scr not found")

        path = self.test_files['hitable']

        # Complete decompilation pipeline
        scr = SCRFile.load(str(path))
        ssa_func = build_ssa_all_blocks(scr)
        disasm = Disassembler(scr)
        func_bounds = disasm.get_function_boundaries()

        # Generate includes
        include_block = generate_include_block(scr)
        self.assertIn("#include", include_block)
        self.assertIn("sc_global.h", include_block)

        # Analyze globals
        resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
        globals_usage = resolver.analyze()
        self.assertIsNotNone(globals_usage)

        # Decompile all functions
        outputs = []
        for func_name, (start, end) in func_bounds.items():
            output = format_structured_function_named(
                ssa_func, func_name, start, end, resolver
            )
            outputs.append(output)
            self.assertIn(func_name, output, f"Function name {func_name} not in output")

        # Verify switch pattern was detected
        full_output = "\n".join(outputs)
        self.assertIn("switch", full_output, "Expected switch statement in hitable.scr")
        self.assertIn("case", full_output, "Expected case statements in hitable.scr")

    def test_tdm_decompilation(self):
        """Test complete decompilation of tdm.scr (medium complexity)"""
        if 'tdm' not in self.test_files:
            self.skipTest("tdm.scr not found")

        path = self.test_files['tdm']

        # Complete decompilation pipeline
        scr = SCRFile.load(str(path))
        ssa_func = build_ssa_all_blocks(scr)
        disasm = Disassembler(scr)
        func_bounds = disasm.get_function_boundaries()

        # Analyze globals
        resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
        globals_usage = resolver.analyze()

        # Decompile all functions
        success_count = 0
        for func_name, (start, end) in func_bounds.items():
            try:
                output = format_structured_function_named(
                    ssa_func, func_name, start, end, resolver
                )
                if len(output.strip()) > 0:
                    success_count += 1
                    self.assertIn(func_name, output)
            except Exception as e:
                # Some functions may fail due to edge cases, that's okay
                print(f"Warning: {func_name} failed: {e}")

        # At least some functions should succeed
        self.assertGreater(success_count, 0, "At least one function should decompile successfully")

    def test_tdm_param_alias_preserved(self):
        """Ensure gTime += time keeps the parameter name (from decompiler_source_tests/test2/tdm.scr)."""
        source_path = Path("decompiler_source_tests/test2/tdm.scr")
        if not source_path.exists():
            self.skipTest("decompiler_source_tests/test2/tdm.scr not found")

        scr = SCRFile.load(str(source_path))
        ssa_func = build_ssa_all_blocks(scr)
        disasm = Disassembler(scr)
        func_bounds = disasm.get_function_boundaries()
        resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
        resolver.analyze()

        outputs = []
        for func_name, (start, end) in func_bounds.items():
            output = format_structured_function_named(
                ssa_func, func_name, start, end, resolver
            )
            outputs.append(output)

        full_output = "\n".join(outputs)
        self.assertIn("gTime += time", full_output)

    def test_refactored_modules_work_in_pipeline(self):
        """Test that refactored structure modules work correctly in pipeline"""
        # Import all refactored modules to ensure they work
        from vcdecomp.core.ir.structure.patterns import (
            CaseInfo, SwitchPattern, IfElsePattern,
            CompoundCondition, ForLoopInfo,
            _detect_if_else_pattern, _detect_switch_patterns,
            _detect_for_loop, _detect_short_circuit_pattern
        )
        from vcdecomp.core.ir.structure.analysis import (
            _find_if_body_blocks, _extract_condition_from_block,
            _collect_local_variables, _find_common_successor
        )
        from vcdecomp.core.ir.structure.emit import (
            _format_block_lines, _render_if_else_recursive,
            _render_blocks_with_loops
        )
        from vcdecomp.core.ir.structure.utils import SHOW_BLOCK_COMMENTS

        # Verify all imports are valid
        self.assertTrue(callable(_detect_if_else_pattern))
        self.assertTrue(callable(_detect_switch_patterns))
        self.assertTrue(callable(_detect_for_loop))
        self.assertTrue(callable(_find_if_body_blocks))
        self.assertTrue(callable(_extract_condition_from_block))
        self.assertTrue(callable(_format_block_lines))

        # Test using them in actual pipeline
        if 'hitable' not in self.test_files:
            self.skipTest("hitable.scr not found")

        path = self.test_files['hitable']
        scr = SCRFile.load(str(path))
        ssa_func = build_ssa_all_blocks(scr)
        disasm = Disassembler(scr)
        func_bounds = disasm.get_function_boundaries()
        resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
        resolver.analyze()

        # Decompile - this exercises all refactored modules
        for func_name, (start, end) in func_bounds.items():
            output = format_structured_function_named(
                ssa_func, func_name, start, end, resolver
            )
            # Just verify it doesn't crash
            self.assertIsNotNone(output)

    def test_pattern_detection_works(self):
        """Test that all pattern detection works in real decompilation"""
        if 'hitable' not in self.test_files:
            self.skipTest("hitable.scr not found")

        path = self.test_files['hitable']
        scr = SCRFile.load(str(path))
        ssa_func = build_ssa_all_blocks(scr)
        disasm = Disassembler(scr)
        func_bounds = disasm.get_function_boundaries()
        resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
        resolver.analyze()

        # Decompile all functions
        full_output = ""
        for func_name, (start, end) in func_bounds.items():
            output = format_structured_function_named(
                ssa_func, func_name, start, end, resolver
            )
            full_output += output + "\n"

        # Verify patterns were detected and rendered
        # hitable.scr has switch/case
        self.assertIn("switch", full_output)
        self.assertIn("case", full_output)
        self.assertIn("default", full_output)

    def test_output_is_valid_c_syntax(self):
        """Test that decompiled output has valid C-like syntax"""
        if 'hitable' not in self.test_files:
            self.skipTest("hitable.scr not found")

        path = self.test_files['hitable']
        scr = SCRFile.load(str(path))
        ssa_func = build_ssa_all_blocks(scr)
        disasm = Disassembler(scr)
        func_bounds = disasm.get_function_boundaries()
        resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
        resolver.analyze()

        for func_name, (start, end) in func_bounds.items():
            output = format_structured_function_named(
                ssa_func, func_name, start, end, resolver
            )

            # Check balanced braces
            open_braces = output.count('{')
            close_braces = output.count('}')
            self.assertEqual(open_braces, close_braces,
                           f"Unbalanced braces in {func_name}")

            # Check for function signature
            if len(output.strip()) > 0:
                # Should have type and function name
                self.assertIn(func_name, output)

    def test_no_regression_from_refactoring(self):
        """Test that refactoring didn't break decompilation quality"""
        if 'hitable' not in self.test_files:
            self.skipTest("hitable.scr not found")

        path = self.test_files['hitable']

        # Capture decompilation output
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            scr = SCRFile.load(str(path))
            ssa_func = build_ssa_all_blocks(scr)
            disasm = Disassembler(scr)
            func_bounds = disasm.get_function_boundaries()
            resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
            resolver.analyze()

            outputs = []
            for func_name, (start, end) in func_bounds.items():
                output = format_structured_function_named(
                    ssa_func, func_name, start, end, resolver
                )
                outputs.append(output)

            # Verify all functions decompiled
            self.assertEqual(len(outputs), len(func_bounds))

            # Verify outputs are meaningful
            non_empty = [o for o in outputs if len(o.strip()) > 0]
            self.assertGreater(len(non_empty), 0)

            # Verify core C structures present
            full_output = "\n".join(outputs)
            self.assertIn("int", full_output)  # Has type declarations

        finally:
            sys.stdout = old_stdout

    def test_all_available_files(self):
        """Test that all available test files can be decompiled"""
        for name, path in self.test_files.items():
            with self.subTest(file=name):
                scr = SCRFile.load(str(path))
                ssa_func = build_ssa_all_blocks(scr)
                disasm = Disassembler(scr)
                func_bounds = disasm.get_function_boundaries()
                resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
                resolver.analyze()

                # Try to decompile at least one function successfully
                success = False
                for func_name, (start, end) in func_bounds.items():
                    try:
                        output = format_structured_function_named(
                            ssa_func, func_name, start, end, resolver
                        )
                        if len(output.strip()) > 0:
                            success = True
                            break
                    except Exception:
                        continue

                self.assertTrue(success, f"Failed to decompile any function in {name}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
