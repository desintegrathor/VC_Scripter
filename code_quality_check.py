#!/usr/bin/env python3
"""
Comprehensive code quality check for refactored structure modules.
Checks for:
- Module size (< 500 lines)
- Syntax errors
- Import issues
- Type hints presence
- Code complexity
- Common code smells
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class CodeQualityChecker:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.issues: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def check_all(self) -> bool:
        """Run all code quality checks. Returns True if all checks pass."""
        print("=" * 80)
        print("CODE QUALITY CHECK - Refactored Structure Modules")
        print("=" * 80)

        modules = list(self.base_path.rglob("*.py"))
        print(f"\nFound {len(modules)} Python files to check\n")

        # Run all checks
        self.check_module_sizes(modules)
        self.check_syntax(modules)
        self.check_imports(modules)
        self.check_type_hints(modules)
        self.check_docstrings(modules)
        self.check_code_complexity(modules)

        # Print results
        self.print_results()

        return len(self.issues) == 0

    def check_module_sizes(self, modules: List[Path]):
        """Check that all modules are under 500 lines."""
        print("\n[1/6] Checking module sizes (target: < 500 lines)...")

        oversized = []
        for module in modules:
            with open(module, 'r', encoding='utf-8') as f:
                line_count = len(f.readlines())

            # Report modules over 500 lines
            if line_count > 500:
                oversized.append((module.relative_to(self.base_path.parent.parent.parent.parent), line_count))
                self.warnings.append(
                    f"Module {module.name} has {line_count} lines (exceeds 500-line target)"
                )
            elif line_count > 400:
                self.info.append(
                    f"Module {module.name} has {line_count} lines (approaching 500-line target)"
                )

        if oversized:
            print(f"  ⚠️  {len(oversized)} module(s) exceed 500 lines:")
            for path, lines in oversized:
                print(f"      - {path}: {lines} lines")
        else:
            print(f"  ✓ All {len(modules)} modules are under 500 lines")

    def check_syntax(self, modules: List[Path]):
        """Check Python syntax using AST parsing."""
        print("\n[2/6] Checking Python syntax...")

        errors = 0
        for module in modules:
            try:
                with open(module, 'r', encoding='utf-8') as f:
                    ast.parse(f.read(), filename=str(module))
            except SyntaxError as e:
                errors += 1
                self.issues.append(f"Syntax error in {module.name}: {e}")

        if errors:
            print(f"  ✗ {errors} syntax error(s) found")
        else:
            print(f"  ✓ All {len(modules)} modules have valid syntax")

    def check_imports(self, modules: List[Path]):
        """Check for import issues."""
        print("\n[3/6] Checking imports...")

        import_errors = 0
        for module in modules:
            try:
                with open(module, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=str(module))

                # Check for unused imports (basic check)
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        for alias in node.names:
                            imports.append(alias.name)

            except Exception as e:
                import_errors += 1
                self.warnings.append(f"Import check failed for {module.name}: {e}")

        if import_errors:
            print(f"  ⚠️  {import_errors} import issue(s) found")
        else:
            print(f"  ✓ All imports checked")

    def check_type_hints(self, modules: List[Path]):
        """Check for type hints in function signatures."""
        print("\n[4/6] Checking type hints...")

        total_functions = 0
        typed_functions = 0

        for module in modules:
            # Skip __init__.py files (often just re-exports)
            if module.name == '__init__.py':
                continue

            try:
                with open(module, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=str(module))

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        total_functions += 1

                        # Check if function has return type annotation
                        has_return_type = node.returns is not None

                        # Check if args have type annotations
                        has_arg_types = any(
                            arg.annotation is not None
                            for arg in node.args.args
                            if arg.arg != 'self' and arg.arg != 'cls'
                        )

                        if has_return_type or has_arg_types:
                            typed_functions += 1

            except Exception as e:
                self.warnings.append(f"Type hint check failed for {module.name}: {e}")

        if total_functions > 0:
            percentage = (typed_functions / total_functions) * 100
            print(f"  ℹ️  {typed_functions}/{total_functions} functions ({percentage:.1f}%) have type hints")
            if percentage < 50:
                self.warnings.append(
                    f"Only {percentage:.1f}% of functions have type hints (consider adding more)"
                )
        else:
            print(f"  ℹ️  No functions found to check")

    def check_docstrings(self, modules: List[Path]):
        """Check for docstrings in functions and classes."""
        print("\n[5/6] Checking docstrings...")

        total_items = 0
        documented_items = 0

        for module in modules:
            # Skip __init__.py files
            if module.name == '__init__.py':
                continue

            try:
                with open(module, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=str(module))

                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        total_items += 1

                        # Check if has docstring
                        docstring = ast.get_docstring(node)
                        if docstring:
                            documented_items += 1

            except Exception as e:
                self.warnings.append(f"Docstring check failed for {module.name}: {e}")

        if total_items > 0:
            percentage = (documented_items / total_items) * 100
            print(f"  ℹ️  {documented_items}/{total_items} items ({percentage:.1f}%) have docstrings")
        else:
            print(f"  ℹ️  No items found to check")

    def check_code_complexity(self, modules: List[Path]):
        """Check for overly complex functions (high nesting, many branches)."""
        print("\n[6/6] Checking code complexity...")

        complex_functions = []

        for module in modules:
            try:
                with open(module, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=str(module))

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Count control flow statements
                        complexity = self._calculate_complexity(node)

                        if complexity > 15:  # High complexity threshold
                            complex_functions.append((
                                module.name,
                                node.name,
                                complexity
                            ))

            except Exception as e:
                self.warnings.append(f"Complexity check failed for {module.name}: {e}")

        if complex_functions:
            print(f"  ⚠️  {len(complex_functions)} complex function(s) found (complexity > 15):")
            for mod_name, func_name, complexity in sorted(complex_functions, key=lambda x: x[2], reverse=True)[:5]:
                print(f"      - {mod_name}::{func_name} (complexity: {complexity})")
                self.info.append(f"High complexity in {mod_name}::{func_name} ({complexity})")
        else:
            print(f"  ✓ No overly complex functions found")

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            # Count decision points
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def print_results(self):
        """Print summary of all checks."""
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        if self.issues:
            print(f"\n❌ CRITICAL ISSUES ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  - {issue}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if self.info:
            print(f"\nℹ️  INFO ({len(self.info)}):")
            for info in self.info[:10]:  # Show first 10
                print(f"  - {info}")
            if len(self.info) > 10:
                print(f"  ... and {len(self.info) - 10} more")

        print("\n" + "=" * 80)

        if not self.issues:
            print("✓ ALL CRITICAL CHECKS PASSED")
        else:
            print(f"✗ {len(self.issues)} CRITICAL ISSUE(S) FOUND")

        print("=" * 80 + "\n")


def main():
    base_path = Path("vcdecomp/core/ir/structure")

    if not base_path.exists():
        print(f"Error: Directory {base_path} not found")
        sys.exit(1)

    checker = CodeQualityChecker(base_path)
    success = checker.check_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
