#!/usr/bin/env python3
"""
Test script for difference categorization system.

Verifies that the categorization system correctly identifies:
- Semantic differences (affect behavior)
- Cosmetic differences (no behavioral impact)
- Optimization differences (equivalent implementation)
- Unknown differences (unclear impact)
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from vcdecomp.validation.bytecode_compare import (
    Difference,
    DifferenceType,
    DifferenceSeverity,
)
from vcdecomp.validation.difference_types import (
    DifferenceCategory,
    DifferenceCategorizer,
    CategorizedDifference,
    DifferenceSummary,
    categorize_differences,
    get_summary,
    filter_by_category,
    get_semantic_differences,
    get_cosmetic_differences,
)


def create_semantic_differences() -> list[Difference]:
    """Create example semantic differences."""
    return [
        Difference(
            type=DifferenceType.HEADER,
            severity=DifferenceSeverity.CRITICAL,
            description="Entry point differs",
            location="header.enter_ip",
            original_value=0,
            recompiled_value=100,
            details={
                "impact": "Script execution will start at different location"
            }
        ),
        Difference(
            type=DifferenceType.HEADER,
            severity=DifferenceSeverity.CRITICAL,
            description="Parameter count differs",
            location="header.enter_size",
            original_value=2,
            recompiled_value=3,
            details={
                "impact": "Script expects different number of parameters"
            }
        ),
        Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.CRITICAL,
            description="Different opcode",
            location="instruction[42]",
            original_value="JMP 100",
            recompiled_value="CALL 100",
            details={
                "category": "control_flow",
                "impact": "Different control flow instruction"
            }
        ),
        Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.MAJOR,
            description="Constant missing in recompiled version",
            location="data.constants",
            original_value="42",
            recompiled_value="<missing>",
            details={
                "category": "constant",
                "impact": "Missing constant will cause incorrect behavior"
            }
        ),
        Difference(
            type=DifferenceType.XFN,
            severity=DifferenceSeverity.CRITICAL,
            description="External function missing",
            location="xfn[5]",
            original_value="SC_SND_PlaySound3D",
            recompiled_value="<missing>",
            details={
                "impact": "Missing external function will cause runtime error"
            }
        ),
    ]


def create_cosmetic_differences() -> list[Difference]:
    """Create example cosmetic differences."""
    return [
        Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.MINOR,
            description="3 string(s) at different offsets",
            location="data.strings",
            details={
                "impact": "Strings exist but at different memory locations",
                "category": "reordering"
            }
        ),
        Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.INFO,
            description="Alignment padding differs",
            location="data.padding",
            details={
                "impact": "Different alignment padding - no functional impact",
                "category": "alignment"
            }
        ),
        Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.MINOR,
            description="Constants reordered",
            location="data.constants",
            details={
                "impact": "Constants exist but at different offsets",
                "category": "reordering"
            }
        ),
    ]


def create_optimization_differences() -> list[Difference]:
    """Create example optimization differences."""
    return [
        Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.MINOR,
            description="Equivalent instruction with different encoding",
            location="instruction[10]",
            original_value="INC 5, 0",
            recompiled_value="IADD 5, 1",
            details={
                "category": "optimization",
                "impact": "Optimization/compiler difference - semantically equivalent"
            }
        ),
        Difference(
            type=DifferenceType.CODE,
            severity=DifferenceSeverity.MINOR,
            description="Equivalent instruction with different encoding",
            location="instruction[20]",
            original_value="IMUL 5, 2",
            recompiled_value="ILS 5, 1",
            details={
                "category": "optimization",
                "impact": "Multiply by 2 vs left shift by 1 - equivalent"
            }
        ),
    ]


def create_unknown_differences() -> list[Difference]:
    """Create differences that are hard to categorize."""
    return [
        Difference(
            type=DifferenceType.DATA,
            severity=DifferenceSeverity.MINOR,
            description="Unknown data difference",
            location="data.unknown",
            original_value="0x1234",
            recompiled_value="0x5678",
            details={}
        ),
    ]


def test_categorization():
    """Test that differences are categorized correctly."""
    print("Testing difference categorization...")
    print("=" * 80)

    categorizer = DifferenceCategorizer()

    # Test semantic differences
    print("\n1. Testing SEMANTIC differences:")
    print("-" * 80)
    semantic_diffs = create_semantic_differences()
    for diff in semantic_diffs:
        categorized = categorizer.categorize(diff)
        print(f"\n{categorized}")
        print(f"   Rationale: {categorized.rationale}")
        assert categorized.category == DifferenceCategory.SEMANTIC, \
            f"Expected SEMANTIC, got {categorized.category} for: {diff.description}"
    print(f"\n✓ All {len(semantic_diffs)} semantic differences correctly categorized")

    # Test cosmetic differences
    print("\n2. Testing COSMETIC differences:")
    print("-" * 80)
    cosmetic_diffs = create_cosmetic_differences()
    for diff in cosmetic_diffs:
        categorized = categorizer.categorize(diff)
        print(f"\n{categorized}")
        print(f"   Rationale: {categorized.rationale}")
        assert categorized.category == DifferenceCategory.COSMETIC, \
            f"Expected COSMETIC, got {categorized.category} for: {diff.description}"
    print(f"\n✓ All {len(cosmetic_diffs)} cosmetic differences correctly categorized")

    # Test optimization differences
    print("\n3. Testing OPTIMIZATION differences:")
    print("-" * 80)
    optimization_diffs = create_optimization_differences()
    for diff in optimization_diffs:
        categorized = categorizer.categorize(diff)
        print(f"\n{categorized}")
        print(f"   Rationale: {categorized.rationale}")
        assert categorized.category == DifferenceCategory.OPTIMIZATION, \
            f"Expected OPTIMIZATION, got {categorized.category} for: {diff.description}"
    print(f"\n✓ All {len(optimization_diffs)} optimization differences correctly categorized")

    # Test unknown differences
    print("\n4. Testing UNKNOWN differences:")
    print("-" * 80)
    unknown_diffs = create_unknown_differences()
    for diff in unknown_diffs:
        categorized = categorizer.categorize(diff)
        print(f"\n{categorized}")
        print(f"   Rationale: {categorized.rationale}")
        # Unknown is acceptable for ambiguous cases
        print(f"   Category: {categorized.category}")

    print("\n✓ Unknown differences handled")

    return semantic_diffs + cosmetic_diffs + optimization_diffs + unknown_diffs


def test_summary(all_differences: list[Difference]):
    """Test the summary functionality."""
    print("\n\nTesting difference summary...")
    print("=" * 80)

    summary = get_summary(all_differences)
    print(f"\n{summary}")

    # Verify counts
    assert summary.total_count == len(all_differences), \
        f"Expected {len(all_differences)} total, got {summary.total_count}"

    assert summary.semantic_count == 5, \
        f"Expected 5 semantic, got {summary.semantic_count}"

    assert summary.cosmetic_count == 3, \
        f"Expected 3 cosmetic, got {summary.cosmetic_count}"

    assert summary.optimization_count == 2, \
        f"Expected 2 optimization, got {summary.optimization_count}"

    print("\n✓ Summary counts are correct")

    # Verify severity counts
    print(f"\nSeverity breakdown:")
    print(f"  Critical: {summary.critical_count}")
    print(f"  Major:    {summary.major_count}")
    print(f"  Minor:    {summary.minor_count}")
    print(f"  Info:     {summary.info_count}")

    assert summary.critical_count == 4, \
        f"Expected 4 critical, got {summary.critical_count}"

    print("\n✓ Severity counts are correct")


def test_filtering():
    """Test filtering functions."""
    print("\n\nTesting filtering functions...")
    print("=" * 80)

    all_differences = create_semantic_differences() + \
                      create_cosmetic_differences() + \
                      create_optimization_differences()

    categorized = categorize_differences(all_differences)

    # Test filter by category
    semantic_only = filter_by_category(categorized, DifferenceCategory.SEMANTIC)
    print(f"\nSemantic differences: {len(semantic_only)}")
    assert len(semantic_only) == 5, f"Expected 5 semantic, got {len(semantic_only)}"

    cosmetic_only = filter_by_category(categorized, DifferenceCategory.COSMETIC)
    print(f"Cosmetic differences: {len(cosmetic_only)}")
    assert len(cosmetic_only) == 3, f"Expected 3 cosmetic, got {len(cosmetic_only)}"

    optimization_only = filter_by_category(categorized, DifferenceCategory.OPTIMIZATION)
    print(f"Optimization differences: {len(optimization_only)}")
    assert len(optimization_only) == 2, f"Expected 2 optimization, got {len(optimization_only)}"

    print("\n✓ Filter by category works")

    # Test convenience functions
    semantic_convenience = get_semantic_differences(categorized)
    assert len(semantic_convenience) == 5, \
        f"Expected 5 from get_semantic_differences, got {len(semantic_convenience)}"

    cosmetic_convenience = get_cosmetic_differences(categorized)
    assert len(cosmetic_convenience) == 3, \
        f"Expected 3 from get_cosmetic_differences, got {len(cosmetic_convenience)}"

    print("✓ Convenience functions work")

    # Test filter by severity
    from vcdecomp.validation.difference_types import filter_by_severity

    critical_only = filter_by_severity(categorized, DifferenceSeverity.CRITICAL)
    print(f"\nCritical severity: {len(critical_only)}")
    assert len(critical_only) == 4, f"Expected 4 critical, got {len(critical_only)}"

    minor_only = filter_by_severity(categorized, DifferenceSeverity.MINOR)
    print(f"Minor severity: {len(minor_only)}")
    assert len(minor_only) == 4, f"Expected 4 minor, got {len(minor_only)}"

    print("\n✓ Filter by severity works")


def test_acceptance_criteria():
    """Verify all acceptance criteria are met."""
    print("\n\nVerifying acceptance criteria...")
    print("=" * 80)

    all_differences = create_semantic_differences() + \
                      create_cosmetic_differences() + \
                      create_optimization_differences()

    categorized = categorize_differences(all_differences)

    # 1. All differences have category and severity
    print("\n1. All differences have category and severity:")
    for cat_diff in categorized:
        assert cat_diff.category is not None, "Missing category"
        assert cat_diff.difference.severity is not None, "Missing severity"
    print("   ✓ All differences have category and severity")

    # 2. Semantic differences are clearly distinguished
    print("\n2. Semantic differences are clearly distinguished:")
    semantic = get_semantic_differences(categorized)
    print(f"   Found {len(semantic)} semantic differences:")
    for cat_diff in semantic:
        print(f"   - {cat_diff.difference.description}")
    assert len(semantic) == 5, "Should have 5 semantic differences"
    print("   ✓ Semantic differences clearly distinguished")

    # 3. Cosmetic differences are marked
    print("\n3. Cosmetic differences are marked:")
    cosmetic = get_cosmetic_differences(categorized)
    print(f"   Found {len(cosmetic)} cosmetic differences:")
    for cat_diff in cosmetic:
        print(f"   - {cat_diff.difference.description}")
    assert len(cosmetic) == 3, "Should have 3 cosmetic differences"
    print("   ✓ Cosmetic differences properly marked")

    # 4. Provides human-readable descriptions
    print("\n4. Provides human-readable descriptions:")
    for cat_diff in categorized[:3]:  # Show first 3
        str_repr = str(cat_diff)
        assert len(str_repr) > 0, "Empty string representation"
        print(f"   {str_repr.split(chr(10))[0]}")  # First line only
    print("   ✓ Human-readable descriptions provided")

    print("\n" + "=" * 80)
    print("✅ ALL ACCEPTANCE CRITERIA MET")
    print("=" * 80)


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("DIFFERENCE CATEGORIZATION SYSTEM TESTS")
    print("=" * 80)

    try:
        # Test categorization
        all_differences = test_categorization()

        # Test summary
        test_summary(all_differences)

        # Test filtering
        test_filtering()

        # Verify acceptance criteria
        test_acceptance_criteria()

        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED")
        print("=" * 80)
        print("\nThe difference categorization system is working correctly!")
        print("- Semantic differences (affect behavior) are identified")
        print("- Cosmetic differences (no impact) are identified")
        print("- Optimization differences (equivalent) are identified")
        print("- Summary and filtering functions work as expected")

        return 0

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
