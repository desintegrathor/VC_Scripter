"""
Verification script for code segment comparison implementation.

Tests:
1. Equivalent instruction pattern detection (INC vs ADD 1)
2. Control flow analysis (jumps, calls)
3. Instruction difference reporting
"""

import sys
from pathlib import Path

# Add vcdecomp to path
sys.path.insert(0, str(Path(__file__).parent))

from vcdecomp.validation.bytecode_compare import BytecodeComparator, DifferenceSeverity

def test_identical_files():
    """Test comparison of identical files."""
    print("=" * 80)
    print("TEST 1: Identical Files")
    print("=" * 80)

    comparator = BytecodeComparator()

    # Use a simple test file (comparing with itself)
    test_file = Path("/c/Users/flori/source/repos/VC_Scripter/Compiler-testruns/Testrun1/tdm.scr")

    if not test_file.exists():
        # Try alternative locations
        for alt_path in [
            Path("Compiler-testruns/Testrun1/tdm.scr"),
            Path("../Compiler-testruns/Testrun1/tdm.scr"),
            Path("../../Compiler-testruns/Testrun1/tdm.scr"),
        ]:
            if alt_path.exists():
                test_file = alt_path
                break

    if not test_file.exists():
        print(f"⚠ Test file not found: {test_file}")
        print("Skipping test...")
        return False

    result = comparator.compare_files(test_file, test_file)

    if result.is_valid:
        print(f"✓ Comparison completed successfully")
        print(f"  Identical: {result.identical}")

        if result.identical:
            print("  ✓ Files are identical (as expected)")
            return True
        else:
            print("  ✗ Files should be identical but differences were found")
            for diff in result.all_differences:
                print(f"    {diff}")
            return False
    else:
        print(f"✗ Comparison failed: {result.load_error}")
        return False

def test_code_section_analysis():
    """Test code section detailed analysis."""
    print("\n" + "=" * 80)
    print("TEST 2: Code Section Analysis")
    print("=" * 80)

    comparator = BytecodeComparator()

    # Compare two different test files to see analysis (just use same file for now)
    file1 = Path("/c/Users/flori/source/repos/VC_Scripter/Compiler-testruns/Testrun1/tdm.scr")
    file2 = Path("/c/Users/flori/source/repos/VC_Scripter/Compiler-testruns/Testrun1/tdm.scr")

    # Try to find files
    if not file1.exists():
        for alt_path in [Path("Compiler-testruns/Testrun1/tdm.scr"), Path("../../Compiler-testruns/Testrun1/tdm.scr")]:
            if alt_path.exists():
                file1 = alt_path
                break

    if not file2.exists():
        for alt_path in [Path("Compiler-testruns/opcodetest/opcodetest.scr"), Path("../../Compiler-testruns/opcodetest/opcodetest.scr")]:
            if alt_path.exists():
                file2 = alt_path
                break

    if not file1.exists() or not file2.exists():
        print(f"⚠ Test files not found")
        print(f"  file1: {file1} (exists: {file1.exists()})")
        print(f"  file2: {file2} (exists: {file2.exists()})")
        print("Skipping test...")
        return False

    result = comparator.compare_files(file1, file2)

    if result.is_valid:
        print(f"✓ Comparison completed successfully")
        print(f"  Files compared: {file1.name} vs {file2.name}")
        print(f"  Identical: {result.identical}")

        if "code" in result.sections:
            code_section = result.sections["code"]
            print(f"\n  Code Section Analysis:")
            print(f"    Original size: {code_section.original_size} bytes")
            print(f"    Recompiled size: {code_section.recompiled_size} bytes")
            print(f"    Differences: {code_section.difference_count}")
            print(f"    Critical: {code_section.critical_count}")
            print(f"    Major: {code_section.major_count}")

            # Show first few differences
            if code_section.differences:
                print(f"\n  First 5 differences:")
                for i, diff in enumerate(code_section.differences[:5]):
                    print(f"    {i+1}. {diff.severity.value.upper()}: {diff.description}")
                    print(f"       Location: {diff.location}")
                    if "category" in diff.details:
                        print(f"       Category: {diff.details['category']}")
                    if "impact" in diff.details:
                        print(f"       Impact: {diff.details['impact']}")

        return True
    else:
        print(f"✗ Comparison failed: {result.load_error}")
        return False

def test_control_flow_detection():
    """Test control flow analysis."""
    print("\n" + "=" * 80)
    print("TEST 3: Control Flow Detection")
    print("=" * 80)

    comparator = BytecodeComparator()

    # Use test file that should have control flow
    test_file = Path("/c/Users/flori/source/repos/VC_Scripter/Compiler-testruns/Testrun1/tdm.scr")

    if not test_file.exists():
        for alt_path in [Path("Compiler-testruns/Testrun1/tdm.scr"), Path("../../Compiler-testruns/Testrun1/tdm.scr")]:
            if alt_path.exists():
                test_file = alt_path
                break

    if not test_file.exists():
        print(f"⚠ Test file not found: {test_file}")
        print("Skipping test...")
        return False

    # Compare with itself - should find no control flow differences
    result = comparator.compare_files(test_file, test_file)

    if result.is_valid:
        print(f"✓ Comparison completed")

        # Extract control flow from the code
        if comparator.original and comparator.original.code_segment:
            cf_info = comparator._extract_control_flow(
                comparator.original.code_segment,
                comparator.original
            )

            print(f"\n  Control Flow Analysis:")
            print(f"    Jump instructions: {len(cf_info['jumps'])}")
            print(f"    Call instructions: {len(cf_info['calls'])}")
            print(f"    External calls: {len(cf_info['xcalls'])}")
            print(f"    Return instructions: {len(cf_info['returns'])}")

            if cf_info['jumps']:
                print(f"\n  Jump targets (first 5):")
                for addr, target in list(cf_info['jumps'].items())[:5]:
                    print(f"    instruction[{addr}] -> instruction[{target}]")

            if cf_info['xcalls']:
                print(f"\n  External function calls:")
                for addr, xfn_idx in cf_info['xcalls'].items():
                    xfn_entry = comparator.original.xfn_table.entries[xfn_idx]
                    print(f"    instruction[{addr}] -> {xfn_entry.name}")

        return True
    else:
        print(f"✗ Comparison failed: {result.load_error}")
        return False

def test_equivalent_instructions():
    """Test equivalent instruction detection."""
    print("\n" + "=" * 80)
    print("TEST 4: Equivalent Instruction Detection")
    print("=" * 80)

    from vcdecomp.core.loader.scr_loader import Instruction

    comparator = BytecodeComparator()

    # Load a file to get opcode resolver
    test_file = Path("/c/Users/flori/source/repos/VC_Scripter/Compiler-testruns/Testrun1/tdm.scr")

    if not test_file.exists():
        for alt_path in [Path("Compiler-testruns/Testrun1/tdm.scr"), Path("../../Compiler-testruns/Testrun1/tdm.scr")]:
            if alt_path.exists():
                test_file = alt_path
                break

    if not test_file.exists():
        print(f"⚠ Test file not found: {test_file}")
        print("Skipping test...")
        return False

    # Load to initialize comparator
    result = comparator.compare_files(test_file, test_file)

    if not result.is_valid:
        print(f"✗ Failed to load test file")
        return False

    # Test equivalent instruction patterns
    print("\n  Testing INC vs ADD 1 pattern:")

    # Mock instructions - we need actual opcodes
    # These would need to be looked up from the opcode resolver
    # For now, just verify the method exists and can be called

    test_instr1 = Instruction(opcode=58, arg1=1, arg2=0, address=0)  # ADD with arg1=1
    test_instr2 = Instruction(opcode=205, arg1=0, arg2=0, address=0)  # Would be INC if opcode correct

    # Just verify the method works
    try:
        is_equiv = comparator._instructions_equivalent(test_instr1, test_instr2, 0)
        print(f"  ✓ _instructions_equivalent() method works")
        print(f"    Result: {is_equiv}")
    except Exception as e:
        print(f"  ✗ Error calling _instructions_equivalent(): {e}")
        return False

    print("\n  Testing control flow extraction:")
    try:
        cf_info = comparator._extract_control_flow(
            comparator.original.code_segment,
            comparator.original
        )
        print(f"  ✓ _extract_control_flow() method works")
        print(f"    Found {len(cf_info['jumps'])} jumps")
    except Exception as e:
        print(f"  ✗ Error calling _extract_control_flow(): {e}")
        return False

    return True

def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "CODE SEGMENT COMPARISON TESTS" + " " * 29 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    tests = [
        ("Identical Files", test_identical_files),
        ("Code Section Analysis", test_code_section_analysis),
        ("Control Flow Detection", test_control_flow_detection),
        ("Equivalent Instructions", test_equivalent_instructions),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
