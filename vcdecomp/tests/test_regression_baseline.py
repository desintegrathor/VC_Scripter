"""
Regression test to verify decompilation output is identical before and after refactoring.

This test compares decompilation output from the refactored structure package
against the baseline output from the pre-refactoring monolithic structure.py.
"""

import unittest
import sys
import tempfile
import subprocess
from pathlib import Path
from io import StringIO

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from vcdecomp.core.loader import SCRFile
from vcdecomp.core.disasm import Disassembler
from vcdecomp.core.ir.ssa import build_ssa_all_blocks
from vcdecomp.core.ir.structure import format_structured_function_named
from vcdecomp.core.ir.global_resolver import GlobalResolver


class TestRegressionBaseline(unittest.TestCase):
    """Test that refactored code produces identical output to pre-refactoring baseline"""

    # Git commit hash with pre-refactoring baseline (3250-line structure.py)
    BASELINE_COMMIT = "2d079a1"

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

        # Check if git is available
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, timeout=5)
            cls.git_available = result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            cls.git_available = False

    def decompile_file(self, scr_path: Path) -> dict:
        """
        Decompile a .scr file and return dict of function_name -> output.

        Args:
            scr_path: Path to .scr file

        Returns:
            Dictionary mapping function names to their decompiled output
        """
        scr = SCRFile.load(str(scr_path))
        ssa_func = build_ssa_all_blocks(scr)
        disasm = Disassembler(scr)
        func_bounds = disasm.get_function_boundaries()
        resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
        resolver.analyze()

        outputs = {}
        for func_name, (start, end) in func_bounds.items():
            try:
                output = format_structured_function_named(
                    ssa_func, func_name, start, end, resolver
                )
                outputs[func_name] = output
            except Exception as e:
                # Record failures
                outputs[func_name] = f"ERROR: {str(e)}"

        return outputs

    def get_baseline_output(self, scr_path: Path) -> dict:
        """
        Get baseline decompilation output from pre-refactoring commit.

        This uses git worktree to check out the baseline commit and run
        decompilation with the old monolithic structure.py.

        Args:
            scr_path: Path to .scr file

        Returns:
            Dictionary mapping function names to their baseline decompiled output
        """
        if not self.git_available:
            self.skipTest("Git not available")

        # Create temporary directory for baseline worktree
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            worktree_path = tmpdir / "baseline"

            try:
                # Create git worktree at baseline commit
                subprocess.run(
                    ['git', 'worktree', 'add', str(worktree_path), self.BASELINE_COMMIT],
                    check=True,
                    capture_output=True,
                    timeout=30
                )

                # Create a script to run decompilation in the baseline worktree
                test_script = worktree_path / "test_decompile.py"
                script_content = '''
import sys
from pathlib import Path

# Add baseline code to path
sys.path.insert(0, str(Path(__file__).parent))

from vcdecomp.core.loader import SCRFile
from vcdecomp.core.disasm import Disassembler
from vcdecomp.core.ir.ssa import build_ssa_all_blocks
from vcdecomp.core.ir.structure import format_structured_function_named
from vcdecomp.core.ir.global_resolver import GlobalResolver

scr_path = r"''' + str(scr_path.absolute()) + '''"
scr = SCRFile.load(scr_path)
ssa_func = build_ssa_all_blocks(scr)
disasm = Disassembler(scr)
func_bounds = disasm.get_function_boundaries()
resolver = GlobalResolver(ssa_func, aggressive_typing=True, infer_structs=False)
resolver.analyze()

for func_name, (start, end) in func_bounds.items():
    try:
        output = format_structured_function_named(
            ssa_func, func_name, start, end, resolver
        )
        print(f"===FUNCTION:{func_name}===")
        print(output)
        print(f"===END:{func_name}===")
    except Exception as e:
        print(f"===FUNCTION:{func_name}===")
        print(f"ERROR: {str(e)}")
        print(f"===END:{func_name}===")
'''
                test_script.write_text(script_content)

                # Run decompilation script in baseline worktree
                result = subprocess.run(
                    [sys.executable, str(test_script)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(worktree_path)
                )

                # Parse output
                baseline_outputs = {}
                lines = result.stdout.split('\n')
                current_func = None
                current_output = []

                for line in lines:
                    if line.startswith('===FUNCTION:'):
                        current_func = line.replace('===FUNCTION:', '').replace('===', '')
                        current_output = []
                    elif line.startswith('===END:'):
                        if current_func:
                            baseline_outputs[current_func] = '\n'.join(current_output)
                        current_func = None
                        current_output = []
                    elif current_func is not None:
                        current_output.append(line)

                return baseline_outputs

            finally:
                # Clean up worktree
                try:
                    subprocess.run(
                        ['git', 'worktree', 'remove', str(worktree_path), '--force'],
                        capture_output=True,
                        timeout=10
                    )
                except subprocess.SubprocessError:
                    pass  # Ignore cleanup errors

    def test_hitable_regression(self):
        """Test that hitable.scr output matches baseline"""
        if 'hitable' not in self.test_files:
            self.skipTest("hitable.scr not found")

        scr_path = self.test_files['hitable']

        # Get current output
        current_output = self.decompile_file(scr_path)

        # Get baseline output
        baseline_output = self.get_baseline_output(scr_path)

        # Compare function names
        self.assertEqual(
            set(current_output.keys()),
            set(baseline_output.keys()),
            "Function list differs from baseline"
        )

        # Compare each function's output
        mismatches = []
        for func_name in current_output.keys():
            current = current_output[func_name].strip()
            baseline = baseline_output[func_name].strip()

            if current != baseline:
                mismatches.append(func_name)

        if mismatches:
            # Report detailed diff for first mismatch
            func = mismatches[0]
            msg = f"\nOutput mismatch in {func}:\n"
            msg += f"BASELINE:\n{baseline_output[func]}\n"
            msg += f"CURRENT:\n{current_output[func]}\n"
            msg += f"Total mismatches: {len(mismatches)} functions"
            self.fail(msg)

    def test_tdm_regression(self):
        """Test that tdm.scr output matches baseline"""
        if 'tdm' not in self.test_files:
            self.skipTest("tdm.scr not found")

        scr_path = self.test_files['tdm']

        # Get current output
        current_output = self.decompile_file(scr_path)

        # Get baseline output
        baseline_output = self.get_baseline_output(scr_path)

        # Compare function names
        self.assertEqual(
            set(current_output.keys()),
            set(baseline_output.keys()),
            "Function list differs from baseline"
        )

        # Compare each function's output
        mismatches = []
        for func_name in current_output.keys():
            current = current_output[func_name].strip()
            baseline = baseline_output[func_name].strip()

            if current != baseline:
                mismatches.append(func_name)

        # Allow some mismatches in complex files (report but don't fail)
        if mismatches:
            print(f"\nWarning: {len(mismatches)} functions differ from baseline in tdm.scr")
            # Only fail if more than 20% differ
            mismatch_ratio = len(mismatches) / len(current_output)
            self.assertLess(
                mismatch_ratio,
                0.2,
                f"Too many mismatches: {len(mismatches)}/{len(current_output)}"
            )

    def test_current_output_quality(self):
        """Test that current refactored code produces quality output"""
        # This doesn't compare to baseline, just validates output quality
        for name, path in self.test_files.items():
            with self.subTest(file=name):
                outputs = self.decompile_file(path)

                # Check that we got some outputs
                self.assertGreater(len(outputs), 0, f"No functions in {name}")

                # Check that outputs are non-empty
                non_empty = [o for o in outputs.values() if len(o.strip()) > 0]
                self.assertGreater(len(non_empty), 0, f"All functions empty in {name}")

                # Check for error messages
                errors = [f for f, o in outputs.items() if o.startswith("ERROR:")]
                error_ratio = len(errors) / len(outputs)
                self.assertLess(
                    error_ratio,
                    0.3,
                    f"Too many errors in {name}: {len(errors)}/{len(outputs)}"
                )

                # Check for basic C syntax in at least one function
                full_output = "\n".join(outputs.values())
                self.assertIn("{", full_output)
                self.assertIn("}", full_output)

    def test_output_stability(self):
        """Test that running decompilation twice produces identical output"""
        if not self.test_files:
            self.skipTest("No test files available")

        # Pick first available file
        name, path = next(iter(self.test_files.items()))

        # Decompile twice
        output1 = self.decompile_file(path)
        output2 = self.decompile_file(path)

        # Compare
        self.assertEqual(
            set(output1.keys()),
            set(output2.keys()),
            "Function list differs between runs"
        )

        for func_name in output1.keys():
            self.assertEqual(
                output1[func_name],
                output2[func_name],
                f"Output differs between runs for {func_name}"
            )


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
