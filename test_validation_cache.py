#!/usr/bin/env python3
"""
Comprehensive verification tests for validation caching system.

Tests all acceptance criteria:
1. Caches validation results by source hash
2. Invalidates cache when source changes
3. Provides cache hit/miss statistics
4. Can be disabled via config flag
"""

import sys
import tempfile
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from vcdecomp.validation import (
    ValidationCache,
    CacheEntry,
    CacheStatistics,
    ValidationResult,
    ValidationVerdict,
)


def create_test_files(temp_dir: Path) -> tuple[Path, Path]:
    """Create test files for validation."""
    # Create test source file
    source_file = temp_dir / "test.c"
    source_file.write_text("""
#include "sc_global.h"

void main() {
    SC_message("Hello, World!");
}
""")

    # Create test SCR file (dummy content)
    scr_file = temp_dir / "test.scr"
    scr_file.write_bytes(b"SCR\x00" + b"\x00" * 100)

    return scr_file, source_file


def create_test_result(scr_file: Path, source_file: Path) -> ValidationResult:
    """Create a test ValidationResult."""
    return ValidationResult(
        original_scr=scr_file,
        decompiled_source=source_file,
        verdict=ValidationVerdict.PASS,
        recommendations=["Test result"],
        metadata={"test": True},
    )


def test_cache_basic_functionality():
    """Test 1: Basic cache get/set functionality."""
    print("=" * 80)
    print("Test 1: Basic Cache Functionality")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        cache_dir = temp_path / ".test_cache"

        # Create cache
        cache = ValidationCache(cache_dir=cache_dir, enabled=True)
        print(f"\n✓ Created cache at {cache_dir}")

        # Create test files
        scr_file, source_file = create_test_files(temp_path)
        print(f"✓ Created test files: {scr_file.name}, {source_file.name}")

        # Create test result
        result = create_test_result(scr_file, source_file)
        print(f"✓ Created test result with verdict: {result.verdict.value}")

        # Cache should be empty initially
        cached = cache.get(scr_file, source_file)
        assert cached is None, "Cache should be empty initially"
        print("✓ Initial cache lookup returns None (cache miss)")

        # Store result in cache
        success = cache.set(scr_file, source_file, result)
        assert success, "Cache set should succeed"
        print("✓ Successfully stored result in cache")

        # Retrieve from cache
        cached = cache.get(scr_file, source_file)
        assert cached is not None, "Cache should return stored result"
        assert cached.verdict == result.verdict, "Cached result should match original"
        assert cached.metadata.get("cached") is True, "Cached result should have cached flag"
        print("✓ Successfully retrieved result from cache")
        print(f"  - Verdict matches: {cached.verdict == result.verdict}")
        print(f"  - Cached flag present: {cached.metadata.get('cached')}")

        # Check cache file exists
        cache_files = list(cache_dir.glob("*.json"))
        assert len(cache_files) == 1, "Should have exactly one cache file"
        print(f"✓ Cache file created: {cache_files[0].name}")

    print("\n" + "=" * 80)
    print("Test 1: PASSED - Basic cache functionality working")
    print("=" * 80)
    return True


def test_cache_invalidation_on_source_change():
    """Test 2: Cache invalidates when source changes."""
    print("\n" + "=" * 80)
    print("Test 2: Cache Invalidation on Source Change")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        cache_dir = temp_path / ".test_cache"

        # Create cache
        cache = ValidationCache(cache_dir=cache_dir, enabled=True)
        print(f"\n✓ Created cache at {cache_dir}")

        # Create test files
        scr_file, source_file = create_test_files(temp_path)
        print(f"✓ Created test files")

        # Create and cache result
        result1 = create_test_result(scr_file, source_file)
        cache.set(scr_file, source_file, result1)
        print("✓ Stored initial result in cache")

        # Verify cache hit
        cached1 = cache.get(scr_file, source_file)
        assert cached1 is not None, "Should get cached result"
        print("✓ Cache hit for initial source")

        # Modify source file (change content)
        source_file.write_text("""
#include "sc_global.h"

void main() {
    SC_message("Modified content!");
}
""")
        print("✓ Modified source file content")

        # Cache should miss now (hash changed)
        cached2 = cache.get(scr_file, source_file)
        assert cached2 is None, "Cache should miss after source change"
        print("✓ Cache miss after source modification (hash mismatch)")

        # Store new result
        result2 = create_test_result(scr_file, source_file)
        cache.set(scr_file, source_file, result2)
        print("✓ Stored new result for modified source")

        # Should get the new result now
        cached3 = cache.get(scr_file, source_file)
        assert cached3 is not None, "Should get new cached result"
        print("✓ Cache hit for modified source")

    print("\n" + "=" * 80)
    print("Test 2: PASSED - Cache invalidation on source change")
    print("=" * 80)
    return True


def test_cache_statistics():
    """Test 3: Cache provides hit/miss statistics."""
    print("\n" + "=" * 80)
    print("Test 3: Cache Statistics")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        cache_dir = temp_path / ".test_cache"

        # Create cache
        cache = ValidationCache(cache_dir=cache_dir, enabled=True)
        print(f"\n✓ Created cache at {cache_dir}")

        # Create test files
        scr_file, source_file = create_test_files(temp_path)

        # Check initial statistics
        stats = cache.get_statistics()
        assert stats.hits == 0, "Initial hits should be 0"
        assert stats.misses == 0, "Initial misses should be 0"
        assert stats.total_entries == 0, "Initial entries should be 0"
        assert stats.hit_rate == 0.0, "Initial hit rate should be 0"
        print("✓ Initial statistics: hits=0, misses=0, entries=0, hit_rate=0%")

        # Cache miss (file not in cache)
        result = cache.get(scr_file, source_file)
        assert result is None, "Should be cache miss"
        stats = cache.get_statistics()
        assert stats.misses == 1, "Should have 1 miss"
        print(f"✓ After cache miss: hits={stats.hits}, misses={stats.misses}")

        # Store in cache
        test_result = create_test_result(scr_file, source_file)
        cache.set(scr_file, source_file, test_result)
        stats = cache.get_statistics()
        assert stats.total_entries == 1, "Should have 1 entry"
        print(f"✓ After cache set: entries={stats.total_entries}")

        # Cache hit
        result = cache.get(scr_file, source_file)
        assert result is not None, "Should be cache hit"
        stats = cache.get_statistics()
        assert stats.hits == 1, "Should have 1 hit"
        assert stats.misses == 1, "Should still have 1 miss"
        assert stats.hit_rate == 0.5, "Hit rate should be 50%"
        print(f"✓ After cache hit: hits={stats.hits}, misses={stats.misses}, hit_rate={stats.hit_rate:.1%}")

        # Another cache hit
        result = cache.get(scr_file, source_file)
        assert result is not None, "Should be cache hit"
        stats = cache.get_statistics()
        assert stats.hits == 2, "Should have 2 hits"
        assert stats.misses == 1, "Should still have 1 miss"
        assert abs(stats.hit_rate - 2/3) < 0.01, "Hit rate should be ~66.7%"
        print(f"✓ After 2nd cache hit: hits={stats.hits}, misses={stats.misses}, hit_rate={stats.hit_rate:.1%}")

        # Test string representation
        stats_str = str(stats)
        assert "Hits: 2" in stats_str, "String should contain hit count"
        assert "Misses: 1" in stats_str, "String should contain miss count"
        print(f"✓ Statistics string representation:\n{stats_str}")

        # Test invalidation counter
        cache.invalidate(scr_file, source_file)
        stats = cache.get_statistics()
        assert stats.invalidations == 1, "Should have 1 invalidation"
        print(f"✓ After invalidation: invalidations={stats.invalidations}")

    print("\n" + "=" * 80)
    print("Test 3: PASSED - Cache statistics working correctly")
    print("=" * 80)
    return True


def test_cache_disabled():
    """Test 4: Cache can be disabled via config flag."""
    print("\n" + "=" * 80)
    print("Test 4: Cache Can Be Disabled")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        cache_dir = temp_path / ".test_cache"

        # Create cache with disabled flag
        cache = ValidationCache(cache_dir=cache_dir, enabled=False)
        print(f"\n✓ Created cache with enabled=False")

        # Create test files
        scr_file, source_file = create_test_files(temp_path)

        # Try to set cache (should return False)
        result = create_test_result(scr_file, source_file)
        success = cache.set(scr_file, source_file, result)
        assert success is False, "Cache set should return False when disabled"
        print("✓ Cache set returns False when disabled")

        # Try to get from cache (should return None)
        cached = cache.get(scr_file, source_file)
        assert cached is None, "Cache get should return None when disabled"
        print("✓ Cache get returns None when disabled")

        # Cache directory should not be created
        assert not cache_dir.exists(), "Cache directory should not be created when disabled"
        print("✓ Cache directory not created when disabled")

        # Statistics should still work (but show no activity)
        stats = cache.get_statistics()
        assert stats.hits == 0, "Disabled cache should have 0 hits"
        assert stats.misses == 0, "Disabled cache should have 0 misses"
        print(f"✓ Statistics still available: hits={stats.hits}, misses={stats.misses}")

    print("\n" + "=" * 80)
    print("Test 4: PASSED - Cache can be disabled via config")
    print("=" * 80)
    return True


def test_cache_expiration():
    """Test 5: Cache respects max_age setting."""
    print("\n" + "=" * 80)
    print("Test 5: Cache Expiration")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        cache_dir = temp_path / ".test_cache"

        # Create cache with 2-second expiration
        cache = ValidationCache(cache_dir=cache_dir, enabled=True, max_age_seconds=2)
        print(f"\n✓ Created cache with max_age=2 seconds")

        # Create test files
        scr_file, source_file = create_test_files(temp_path)

        # Store result in cache
        result = create_test_result(scr_file, source_file)
        cache.set(scr_file, source_file, result)
        print("✓ Stored result in cache")

        # Immediately retrieve (should hit)
        cached = cache.get(scr_file, source_file)
        assert cached is not None, "Cache should hit immediately"
        print("✓ Cache hit immediately after storage")

        # Wait for expiration
        print("⏳ Waiting 3 seconds for cache to expire...")
        time.sleep(3)

        # Try to retrieve (should miss due to expiration)
        cached = cache.get(scr_file, source_file)
        assert cached is None, "Cache should miss after expiration"
        print("✓ Cache miss after expiration")

        # Check that expired entry was removed
        cache_files = list(cache_dir.glob("*.json"))
        assert len(cache_files) == 0, "Expired cache file should be removed"
        print("✓ Expired cache file was removed")

    print("\n" + "=" * 80)
    print("Test 5: PASSED - Cache expiration working")
    print("=" * 80)
    return True


def test_cache_clear():
    """Test 6: Cache can be cleared."""
    print("\n" + "=" * 80)
    print("Test 6: Cache Clear")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        cache_dir = temp_path / ".test_cache"

        # Create cache
        cache = ValidationCache(cache_dir=cache_dir, enabled=True)
        print(f"\n✓ Created cache at {cache_dir}")

        # Create multiple test files and cache them
        num_files = 3
        for i in range(num_files):
            scr_file = temp_path / f"test{i}.scr"
            source_file = temp_path / f"test{i}.c"

            scr_file.write_bytes(b"SCR\x00" + bytes([i]) * 100)
            source_file.write_text(f"void main_{i}() {{ }}")

            result = create_test_result(scr_file, source_file)
            cache.set(scr_file, source_file, result)

        print(f"✓ Cached {num_files} validation results")

        # Check cache has entries
        stats = cache.get_statistics()
        assert stats.total_entries == num_files, f"Should have {num_files} entries"
        print(f"✓ Cache has {stats.total_entries} entries")

        # Clear cache
        count = cache.clear()
        assert count == num_files, f"Should clear {num_files} entries"
        print(f"✓ Cleared {count} cache entries")

        # Check cache is empty
        stats = cache.get_statistics()
        assert stats.total_entries == 0, "Cache should be empty after clear"
        print("✓ Cache is now empty")

        # Check invalidation counter
        assert stats.invalidations == num_files, "Should count invalidations"
        print(f"✓ Invalidation counter updated: {stats.invalidations}")

    print("\n" + "=" * 80)
    print("Test 6: PASSED - Cache clear working")
    print("=" * 80)
    return True


def test_acceptance_criteria_summary():
    """Summary of all acceptance criteria."""
    print("\n" + "=" * 80)
    print("ACCEPTANCE CRITERIA SUMMARY")
    print("=" * 80)

    criteria = [
        ("Caches validation results by source hash", "Test 1", True),
        ("Invalidates cache when source changes", "Test 2", True),
        ("Provides cache hit/miss statistics", "Test 3", True),
        ("Can be disabled via config flag", "Test 4", True),
    ]

    print("\nAll Acceptance Criteria:")
    for criterion, test, passed in criteria:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} - {criterion} ({test})")

    print("\nAdditional Features Verified:")
    print("  ✓ Cache expiration (max_age setting)")
    print("  ✓ Cache clearing (clear/invalidate methods)")
    print("  ✓ Cache statistics tracking (hits, misses, hit_rate)")
    print("  ✓ Multiple file support")
    print("  ✓ Automatic hash-based invalidation")

    print("\n" + "=" * 80)
    print("ALL TESTS PASSED")
    print("=" * 80)


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("VALIDATION CACHE COMPREHENSIVE TESTS")
    print("=" * 80)

    tests = [
        ("Basic Functionality", test_cache_basic_functionality),
        ("Source Change Invalidation", test_cache_invalidation_on_source_change),
        ("Cache Statistics", test_cache_statistics),
        ("Cache Disabled", test_cache_disabled),
        ("Cache Expiration", test_cache_expiration),
        ("Cache Clear", test_cache_clear),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except AssertionError as e:
            print(f"\n✗ Test failed: {e}")
            results.append((name, False))
        except Exception as e:
            print(f"\n✗ Test error: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {name}")

    all_passed = all(passed for _, passed in results)
    if all_passed:
        test_acceptance_criteria_summary()
        return 0
    else:
        print("\n" + "=" * 80)
        print("SOME TESTS FAILED")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
