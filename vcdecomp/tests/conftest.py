"""
Shared pytest fixtures for validation tests.

Provides reusable fixtures for compiler paths and validation orchestrator
to avoid duplication across test modules.
"""

import pytest
from pathlib import Path

from vcdecomp.validation.validator import ValidationOrchestrator


@pytest.fixture
def datadir():
    """
    Override pytest-regressions datadir fixture to use custom baseline directory.

    This tells pytest-regressions to store baselines in .planning/baselines/
    instead of the default vcdecomp/tests/{test_module_name}/ location.
    """
    # Get repository root (conftest.py is in vcdecomp/tests/)
    repo_root = Path(__file__).parent.parent.parent
    baseline_dir = repo_root / '.planning' / 'baselines' / 'test_validation'

    # Create directory if it doesn't exist
    baseline_dir.mkdir(parents=True, exist_ok=True)

    return baseline_dir


@pytest.fixture(scope="session")
def compiler_paths():
    """
    Provide paths to compiler directory and include directories.

    Returns:
        dict: Dictionary with 'compiler_dir' and 'include_dirs' keys
    """
    # Paths relative to project root
    project_root = Path(__file__).parent.parent.parent
    compiler_dir = project_root / "original-resources" / "compiler"

    # Include directories (headers)
    include_dirs = [
        compiler_dir / "inc",
    ]

    return {
        "compiler_dir": compiler_dir,
        "include_dirs": include_dirs,
    }


@pytest.fixture(scope="session")
def validation_orchestrator(compiler_paths):
    """
    Create ValidationOrchestrator instance for testing.

    Configuration:
    - cache_enabled=False: Always fresh decompilation per user requirement
    - timeout=120: Allow longer compilation time for complex scripts

    Args:
        compiler_paths: Fixture providing compiler paths

    Returns:
        ValidationOrchestrator: Configured orchestrator instance
    """
    return ValidationOrchestrator(
        compiler_dir=compiler_paths["compiler_dir"],
        include_dirs=compiler_paths["include_dirs"],
        timeout=120,
        cache_enabled=False,  # Always fresh decompilation
    )
