"""
Validation result caching system.

Caches validation results to avoid recompiling unchanged code. Uses file hashes
to detect changes and automatically invalidate stale cache entries.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any

from .validation_types import ValidationResult, ValidationVerdict

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """
    A single cache entry.

    Attributes:
        source_hash: SHA256 hash of the source code
        original_scr_hash: SHA256 hash of the original .SCR file
        result_data: Serialized ValidationResult data
        timestamp: Unix timestamp when entry was created
        access_count: Number of times this entry has been accessed
        last_access: Unix timestamp of last access
    """
    source_hash: str
    original_scr_hash: str
    result_data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    access_count: int = 0
    last_access: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "source_hash": self.source_hash,
            "original_scr_hash": self.original_scr_hash,
            "result_data": self.result_data,
            "timestamp": self.timestamp,
            "access_count": self.access_count,
            "last_access": self.last_access,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CacheEntry:
        """Create from dictionary."""
        return cls(
            source_hash=data["source_hash"],
            original_scr_hash=data["original_scr_hash"],
            result_data=data["result_data"],
            timestamp=data.get("timestamp", time.time()),
            access_count=data.get("access_count", 0),
            last_access=data.get("last_access", time.time()),
        )


@dataclass
class CacheStatistics:
    """
    Cache performance statistics.

    Attributes:
        hits: Number of cache hits
        misses: Number of cache misses
        invalidations: Number of cache invalidations
        total_entries: Total number of cached entries
        hit_rate: Cache hit rate (0.0 to 1.0)
    """
    hits: int = 0
    misses: int = 0
    invalidations: int = 0
    total_entries: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    @property
    def total_requests(self) -> int:
        """Total cache lookup requests."""
        return self.hits + self.misses

    def __str__(self) -> str:
        """Human-readable statistics."""
        return (
            f"Cache Statistics:\n"
            f"  Hits: {self.hits}\n"
            f"  Misses: {self.misses}\n"
            f"  Hit Rate: {self.hit_rate:.1%}\n"
            f"  Invalidations: {self.invalidations}\n"
            f"  Total Entries: {self.total_entries}"
        )


class ValidationCache:
    """
    Cache for validation results.

    Stores validation results indexed by source code hash to avoid
    recompiling unchanged code. Automatically invalidates entries
    when source code changes.

    Cache entries are stored in .validation_cache/ directory as JSON files.
    Each entry is named by its cache key (hash of source and original SCR).

    Attributes:
        cache_dir: Directory to store cache files
        max_age_seconds: Maximum age of cache entries (0 = no limit)
        enabled: Whether caching is enabled
        statistics: Cache performance statistics
    """

    def __init__(
        self,
        cache_dir: Path | str = ".validation_cache",
        max_age_seconds: int = 0,
        enabled: bool = True,
    ):
        """
        Initialize the validation cache.

        Args:
            cache_dir: Directory to store cache files
            max_age_seconds: Maximum age of cache entries in seconds (0 = no limit)
            enabled: Whether caching is enabled (can be disabled via config)
        """
        self.cache_dir = Path(cache_dir)
        self.max_age_seconds = max_age_seconds
        self.enabled = enabled
        self.statistics = CacheStatistics()

        # Create cache directory if it doesn't exist
        if self.enabled:
            self.cache_dir.mkdir(exist_ok=True, parents=True)
            logger.info(f"ValidationCache initialized: {self.cache_dir} (enabled={enabled})")
        else:
            logger.info("ValidationCache disabled")

    def _compute_file_hash(self, file_path: Path) -> str:
        """
        Compute SHA256 hash of a file.

        Args:
            file_path: Path to file

        Returns:
            Hex string of SHA256 hash
        """
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            # Read in chunks to handle large files
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _get_cache_key(self, source_hash: str, original_scr_hash: str) -> str:
        """
        Generate cache key from hashes.

        Args:
            source_hash: Hash of source code
            original_scr_hash: Hash of original .SCR file

        Returns:
            Cache key string
        """
        # Combine both hashes to create unique cache key
        combined = f"{source_hash}:{original_scr_hash}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def _get_cache_path(self, cache_key: str) -> Path:
        """
        Get path to cache file.

        Args:
            cache_key: Cache key

        Returns:
            Path to cache file
        """
        return self.cache_dir / f"{cache_key}.json"

    def _is_entry_expired(self, entry: CacheEntry) -> bool:
        """
        Check if cache entry is expired.

        Args:
            entry: Cache entry to check

        Returns:
            True if expired, False otherwise
        """
        if self.max_age_seconds <= 0:
            return False  # No expiration

        age = time.time() - entry.timestamp
        return age > self.max_age_seconds

    def get(
        self,
        original_scr: Path | str,
        decompiled_source: Path | str,
    ) -> Optional[ValidationResult]:
        """
        Get cached validation result.

        Returns cached result if:
        1. Caching is enabled
        2. Cache entry exists
        3. Source code hash matches
        4. Original SCR hash matches
        5. Entry is not expired

        Args:
            original_scr: Path to original .SCR file
            decompiled_source: Path to decompiled source code

        Returns:
            Cached ValidationResult or None if not found or invalid
        """
        if not self.enabled:
            return None

        original_scr = Path(original_scr)
        decompiled_source = Path(decompiled_source)

        # Check files exist
        if not original_scr.exists() or not decompiled_source.exists():
            return None

        try:
            # Compute hashes
            source_hash = self._compute_file_hash(decompiled_source)
            original_scr_hash = self._compute_file_hash(original_scr)

            # Get cache key
            cache_key = self._get_cache_key(source_hash, original_scr_hash)
            cache_path = self._get_cache_path(cache_key)

            # Check if cache file exists
            if not cache_path.exists():
                self.statistics.misses += 1
                logger.debug(f"Cache MISS: {cache_key} (file not found)")
                return None

            # Load cache entry
            with open(cache_path, 'r', encoding='utf-8') as f:
                entry_data = json.load(f)
                entry = CacheEntry.from_dict(entry_data)

            # Verify hashes match
            if entry.source_hash != source_hash or entry.original_scr_hash != original_scr_hash:
                self.statistics.misses += 1
                logger.debug(f"Cache MISS: {cache_key} (hash mismatch)")
                # Invalidate stale entry
                cache_path.unlink(missing_ok=True)
                self.statistics.invalidations += 1
                return None

            # Check expiration
            if self._is_entry_expired(entry):
                self.statistics.misses += 1
                logger.debug(f"Cache MISS: {cache_key} (expired)")
                # Remove expired entry
                cache_path.unlink(missing_ok=True)
                self.statistics.invalidations += 1
                return None

            # Update access statistics
            entry.access_count += 1
            entry.last_access = time.time()

            # Save updated entry
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(entry.to_dict(), f, indent=2)

            # Reconstruct ValidationResult
            result = self._deserialize_result(entry.result_data)

            # Add cache metadata
            result.metadata["cached"] = True
            result.metadata["cache_key"] = cache_key
            result.metadata["cache_timestamp"] = entry.timestamp
            result.metadata["cache_access_count"] = entry.access_count

            self.statistics.hits += 1
            logger.info(f"Cache HIT: {cache_key} (age: {time.time() - entry.timestamp:.1f}s)")
            return result

        except Exception as e:
            logger.warning(f"Cache lookup failed: {e}")
            self.statistics.misses += 1
            return None

    def set(
        self,
        original_scr: Path | str,
        decompiled_source: Path | str,
        result: ValidationResult,
    ) -> bool:
        """
        Store validation result in cache.

        Args:
            original_scr: Path to original .SCR file
            decompiled_source: Path to decompiled source code
            result: ValidationResult to cache

        Returns:
            True if successfully cached, False otherwise
        """
        if not self.enabled:
            return False

        original_scr = Path(original_scr)
        decompiled_source = Path(decompiled_source)

        # Check files exist
        if not original_scr.exists() or not decompiled_source.exists():
            return False

        try:
            # Compute hashes
            source_hash = self._compute_file_hash(decompiled_source)
            original_scr_hash = self._compute_file_hash(original_scr)

            # Create cache entry
            entry = CacheEntry(
                source_hash=source_hash,
                original_scr_hash=original_scr_hash,
                result_data=result.to_dict(),
            )

            # Get cache key and path
            cache_key = self._get_cache_key(source_hash, original_scr_hash)
            cache_path = self._get_cache_path(cache_key)

            # Save to file
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(entry.to_dict(), f, indent=2)

            # Update statistics
            self.statistics.total_entries = len(list(self.cache_dir.glob("*.json")))

            logger.info(f"Cache SET: {cache_key}")
            return True

        except Exception as e:
            logger.warning(f"Cache storage failed: {e}")
            return False

    def invalidate(
        self,
        original_scr: Optional[Path | str] = None,
        decompiled_source: Optional[Path | str] = None,
    ) -> int:
        """
        Invalidate cache entries.

        If both paths are provided, invalidates specific entry.
        If neither is provided, invalidates all entries.

        Args:
            original_scr: Optional path to original .SCR file
            decompiled_source: Optional path to decompiled source code

        Returns:
            Number of entries invalidated
        """
        if not self.enabled:
            return 0

        count = 0

        if original_scr is not None and decompiled_source is not None:
            # Invalidate specific entry
            original_scr = Path(original_scr)
            decompiled_source = Path(decompiled_source)

            if original_scr.exists() and decompiled_source.exists():
                try:
                    source_hash = self._compute_file_hash(decompiled_source)
                    original_scr_hash = self._compute_file_hash(original_scr)
                    cache_key = self._get_cache_key(source_hash, original_scr_hash)
                    cache_path = self._get_cache_path(cache_key)

                    if cache_path.exists():
                        cache_path.unlink()
                        count = 1
                        logger.info(f"Cache invalidated: {cache_key}")
                except Exception as e:
                    logger.warning(f"Cache invalidation failed: {e}")
        else:
            # Invalidate all entries
            try:
                for cache_file in self.cache_dir.glob("*.json"):
                    cache_file.unlink()
                    count += 1
                logger.info(f"Cache cleared: {count} entries removed")
            except Exception as e:
                logger.warning(f"Cache clear failed: {e}")

        self.statistics.invalidations += count
        self.statistics.total_entries = len(list(self.cache_dir.glob("*.json")))

        return count

    def clear(self) -> int:
        """
        Clear all cache entries.

        Returns:
            Number of entries cleared
        """
        return self.invalidate()

    def get_statistics(self) -> CacheStatistics:
        """
        Get cache statistics.

        Returns:
            CacheStatistics object with current statistics
        """
        # Update total entries count
        if self.enabled:
            self.statistics.total_entries = len(list(self.cache_dir.glob("*.json")))
        return self.statistics

    def reset_statistics(self) -> None:
        """Reset cache statistics."""
        self.statistics = CacheStatistics()
        if self.enabled:
            self.statistics.total_entries = len(list(self.cache_dir.glob("*.json")))

    def _deserialize_result(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Deserialize ValidationResult from dictionary.

        Args:
            data: Dictionary representation of ValidationResult

        Returns:
            ValidationResult object
        """
        from .compilation_types import CompilationResult
        from .bytecode_compare import ComparisonResult
        from .difference_types import CategorizedDifference

        # Note: This is a simplified deserialization that reconstructs
        # the basic structure. Full reconstruction would require serializing
        # all nested objects, which is complex. For now, we just preserve
        # the essential information.

        result = ValidationResult(
            original_scr=Path(data["original_scr"]),
            decompiled_source=Path(data["decompiled_source"]),
            verdict=ValidationVerdict(data["verdict"]),
            error_message=data.get("error_message"),
            recommendations=data.get("recommendations", []),
            metadata=data.get("metadata", {}),
        )

        return result
