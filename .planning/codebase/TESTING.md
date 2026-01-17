# Testing Patterns

**Analysis Date:** 2026-01-17

## Test Framework

**Runner:**
- pytest (primary framework)
- unittest (used in some test files, compatible with pytest)
- Config: No `pytest.ini` or `setup.cfg` detected in root

**Assertion Library:**
- pytest assertions (implicit with assert statements)
- unittest assertions (in unittest.TestCase subclasses)

**Run Commands:**
```bash
PYTHONPATH=. python -m pytest vcdecomp/tests/ -v              # Run all tests
PYTHONPATH=. python -m pytest vcdecomp/tests/test_structure_patterns.py -v  # Run specific suite
PYTHONPATH=. python -m pytest vcdecomp/tests/ --cov=vcdecomp.core.ir.structure  # Coverage
PYTHONPATH=. python -m pytest vcdecomp/tests/test_end_to_end_decompilation.py -v  # Integration tests
```

## Test File Organization

**Location:**
- Co-located with package: `vcdecomp/tests/` directory
- Validation tests in subdirectory: `vcdecomp/tests/validation/`

**Naming:**
- Test modules: `test_<module_name>.py` pattern
- Examples: `test_structure_patterns.py`, `test_end_to_end_decompilation.py`, `test_validation_workflow.py`

**Structure:**
```
vcdecomp/
├── tests/
│   ├── test_structure_patterns.py       # Unit tests for pattern detection
│   ├── test_structure_analysis.py       # Unit tests for CFG analysis
│   ├── test_structure_emit.py           # Unit tests for code emission
│   ├── test_end_to_end_decompilation.py # Integration tests
│   ├── test_regression_baseline.py      # Regression tests
│   ├── validation/
│   │   ├── test_validation_workflow.py  # Integration tests for validation
│   │   ├── test_compiler_wrapper.py     # Unit tests for compiler wrapper
│   │   └── test_bytecode_compare.py     # Unit tests for bytecode comparison
```

## Test Structure

**Suite Organization:**

**pytest style:**
```python
class TestFunctionDetectorBasic:
    """Basic functionality tests for function detector."""

    def test_detect_boundaries_v2_exists(self):
        """Test that detect_function_boundaries_v2 is callable."""
        assert callable(detect_function_boundaries_v2)
```

**unittest style:**
```python
class TestEndToEndDecompilation(unittest.TestCase):
    """Test complete end-to-end decompilation workflow"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests"""
        cls.test_files = {...}

    def test_hitable_decompilation(self):
        """Test complete decompilation of hitable.scr (simple switch/case)"""
        if 'hitable' not in self.test_files:
            self.skipTest("hitable.scr not found")
        ...
```

**Patterns:**
- One test class per functionality area
- Descriptive test names: `test_<what>_<scenario>`
- Docstrings explaining what is being tested
- Use of `setUpClass` for expensive fixture setup

## Mocking

**Framework:** `unittest.mock`

**Patterns:**

**Patch method calls:**
```python
from unittest.mock import Mock, patch

with patch.object(orchestrator, '_compile_source') as mock_compile:
    mock_result = CompilationResult(
        success=True,
        output_file=original_scr,
        errors=[],
        warnings=[],
    )
    mock_compile.return_value = mock_result
    result = orchestrator.validate(...)
```

**Create mock objects:**
```python
class MockBasicBlock:
    """Mock BasicBlock for testing"""
    def __init__(self, block_id: int, start: int, successors: List[int] = None):
        self.block_id = block_id
        self.start = start
        self.successors = successors or []

class MockCFG:
    """Mock Control Flow Graph"""
    def __init__(self, blocks: Dict[int, MockBasicBlock] = None):
        self.blocks = blocks or {}
```

**What to Mock:**
- External compilation steps (compiler executables)
- File I/O for predictable testing
- Expensive operations (full decompilation pipeline)

**What NOT to Mock:**
- Core business logic under test
- Simple data structures
- Internal function calls within same module

## Fixtures and Factories

**Test Data:**

**pytest fixtures:**
```python
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
```

**unittest setUpClass:**
```python
@classmethod
def setUpClass(cls):
    """Set up test fixtures once for all tests"""
    cls.project_root = Path(__file__).parent.parent.parent.parent
    cls.compiler_dir = cls.project_root / "original-resources" / "compiler"
    cls.test_data_dir = cls.project_root / "Compiler-testruns"

    # Check if compiler tools exist
    cls.compiler_available = (cls.compiler_dir / "SCMP.exe").exists()
```

**Location:**
- Real test data: `Compiler-testruns/` directory (original C source + compiled .scr files)
- Production scripts: `script-folders/` directory
- Mock objects: Defined inline in test files

## Coverage

**Requirements:** 100% coverage on core modules maintained (mentioned in CLAUDE.md)

**View Coverage:**
```bash
PYTHONPATH=. python -m pytest vcdecomp/tests/ --cov=vcdecomp.core.ir.structure
```

**Target modules:**
- `vcdecomp/core/ir/structure/` - 100% coverage goal
- Core decompilation pipeline modules

## Test Types

**Unit Tests:**
- Scope: Individual functions and classes in isolation
- Files: `test_structure_patterns.py`, `test_structure_analysis.py`, `test_structure_emit.py`
- Pattern: Mock external dependencies, test single responsibility
- Example: Pattern detection functions (`_detect_if_else_pattern`, `_detect_switch_patterns`)

**Integration Tests:**
- Scope: Complete workflows with real data
- Files: `test_end_to_end_decompilation.py`, `test_integration_pipeline.py`, `test_validation_workflow.py`
- Pattern: Use real SCR files from `Compiler-testruns/`, verify complete pipeline
- Example: Full decompilation from `.scr` to structured C code

**Regression Tests:**
- Scope: Prevent regressions after refactoring
- Files: `test_regression_baseline.py`
- Pattern: Save baseline outputs, compare against new outputs
- Example: Verify structure refactoring didn't change output

**End-to-End Tests:**
- Scope: Complete use cases including external tools
- Files: `test_validation_workflow.py` (validates with real compiler)
- Pattern: Use real compiler executables, compare bytecode
- Example: Decompile → recompile → compare bytecode

## Common Patterns

**Async Testing:**
Not used (synchronous codebase)

**Error Testing:**
```python
def test_validation_orchestrator_invalid_compiler_dir(self):
    """Test ValidationOrchestrator initialization with invalid compiler directory."""
    with self.assertRaises(FileNotFoundError):
        ValidationOrchestrator(
            compiler_dir=self.temp_dir / "nonexistent",
        )
```

**Conditional Skipping:**
```python
@unittest.skipUnless(
    Path(__file__).parent.parent.parent.parent / "original-resources" / "compiler" / "SCMP.exe",
    "Compiler tools not available"
)
def test_validation_orchestrator_initialization(self):
    ...

# pytest style
if 'hitable' not in self.test_files:
    self.skipTest("hitable.scr not found")
```

**Parametrized Tests:**
Not extensively used, but could be with `@pytest.mark.parametrize`

**Setup/Teardown:**
```python
def setUp(self):
    """Create temporary directory for test outputs."""
    self.temp_dir = Path(tempfile.mkdtemp(prefix="test_validation_"))
    self.cache_dir = self.temp_dir / "cache"
    self.cache_dir.mkdir(exist_ok=True)

def tearDown(self):
    """Clean up temporary files."""
    if self.temp_dir.exists():
        shutil.rmtree(self.temp_dir)
```

**Assertions:**
```python
# pytest style (preferred)
assert success_count > 0
assert 25 <= len(boundaries) <= 30
assert "switch" in full_output

# unittest style (in TestCase subclasses)
self.assertEqual(result.verdict, ValidationVerdict.PASS)
self.assertTrue(result.compilation_succeeded)
self.assertIn("case", full_output)
self.assertGreater(success_count, 0)
```

## Test Data Organization

**Known good test cases:**
- `Compiler-testruns/Testrun1/tdm.scr` - Team deathmatch script (medium complexity)
- `Compiler-testruns/Testrun3/hitable.scr` - Object hit detection (switch/case pattern)
- `Compiler-testruns/Testrun2/Gaz_67.scr` - Vehicle script
- `decompilation/TUNNELS01/SCRIPTS/LEVEL.scr` - Complex level script with 28 functions

**Test file discovery:**
```python
cls.test_fixtures = []
if cls.test_data_dir.exists():
    for scr_file in cls.test_data_dir.rglob("*.scr"):
        source_candidates = [
            scr_file.with_suffix(".c"),
            scr_file.parent / f"{scr_file.stem}_FINAL.c",
        ]
        for source_file in source_candidates:
            if source_file.exists():
                cls.test_fixtures.append((scr_file, source_file))
                break
```

## Test Statistics

**Total Tests:** 253+ test functions across 13 test files

**Test Distribution:**
- Unit tests: ~60% (pattern detection, analysis, utilities)
- Integration tests: ~30% (end-to-end decompilation, validation workflow)
- Regression tests: ~10% (baseline comparison)

**Coverage Notes:**
- Core IR modules: 100% coverage maintained
- Structure package: 100% coverage after refactoring
- Type hint coverage: 87% across codebase

---

*Testing analysis: 2026-01-17*
