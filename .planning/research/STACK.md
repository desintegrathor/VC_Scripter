# Technology Stack

**Project:** VC-Script-Decompiler Quality Improvement
**Researched:** 2026-01-17
**Confidence:** HIGH

## Executive Summary

The stack focuses on three pillars: **test automation** (pytest ecosystem), **code quality enforcement** (Ruff + mypy), and **validation infrastructure** (custom bytecode comparison already in place). Windows-only constraint drives tool selection (native Windows compatibility required).

**Key decision:** Leverage existing validation subsystem (already implemented) and focus stack on testing frameworks, quality gates, and developer workflow tools.

## Recommended Stack

### Core Testing Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pytest | >=9.1.0 | Test runner, test discovery, fixtures | Industry standard, 100% project coverage requirement already met with pytest |
| pytest-cov | >=6.0.0 | Coverage measurement and reporting | Wrapper around coverage.py with pytest integration, requirement: maintain 100% coverage |
| coverage.py | >=7.13.1 | Code coverage analysis | Underlying engine for pytest-cov, supports Python 3.10-3.15 including free-threading |
| pytest-xdist | >=3.6.1 | Parallel test execution | Batch validation needs parallelization (`--jobs 8` already in CLI), 4-8x speedup |
| pytest-timeout | >=2.3.1 | Test timeout handling | Prevent hanging tests during bytecode recompilation (compiler timeout is 30s) |

**Rationale:** pytest already in use with 100% core module coverage. Extensions add parallelization (critical for batch validation of 100+ scripts) and timeout protection (compiler can hang on malformed C code).

**Confidence:** HIGH - All versions verified from official PyPI/GitHub releases (Jan 2026)

### Code Quality & Static Analysis

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| ruff | >=0.14.13 | Linter and formatter | 10-100x faster than Flake8/Black, 800+ rules, replaces 6+ tools (Flake8, Black, isort, pyupgrade, autoflake, pydocstyle) |
| mypy | >=1.19.1 | Static type checker | Project has 87% type hint coverage - mypy enforces this, catches type errors Ruff misses |
| pre-commit | >=4.0.1 | Git hook automation | Auto-run Ruff + mypy before commits, prevent quality regressions |

**Rationale:**
- **Ruff over Pylint:** Pylint has 409 rules, Ruff has 800+ and is orders of magnitude faster. Ruff + mypy covers Pylint's type inference gaps.
- **mypy required:** Ruff is a linter, not a type checker. Complementary, not overlapping.
- **pre-commit framework:** Standard in 2026, actively maintained (updated Jan 2026), prevents "oops forgot to lint" commits.

**Confidence:** HIGH - Versions from official releases, rationale from official Ruff FAQ

### Test Reporting & Visualization

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pytest-html | >=4.1.1 | HTML test reports | Already generating HTML reports for validation (see report_generator.py), pytest-html provides standard format |
| (existing) | N/A | Custom validation HTML reports | Project already has custom ReportGenerator with expandable sections - keep this |

**Rationale:** Dual reporting strategy. pytest-html for unit/integration test runs (developer workflow), existing custom HTML generator for validation reports (stakeholder consumption). Custom reports show bytecode diffs categorized by semantic impact - pytest-html can't do this.

**Confidence:** HIGH - pytest-html is official pytest plugin, custom reports already implemented

### Advanced Testing (Optional - Phase 2+)

| Technology | Version | Purpose | When to Use |
|------------|---------|---------|-------------|
| hypothesis | >=6.150.2 | Property-based testing | Generate random bytecode inputs to find decompiler edge cases, 100k+ downloads/week |
| pytest-benchmark | >=5.1.0 | Performance regression testing | Track decompilation speed regressions (structure refactoring improved speed, keep it) |
| inline-snapshot | >=0.20.0 | Snapshot testing for output | Validate decompiled C output format doesn't regress (alternative to manual diffing) |
| pytest-testmon | >=2.2.0 | Selective test execution | Only re-run tests affected by code changes (smart CI, local dev speedup) |

**Rationale:** Not critical for MVP but high-value later:
- **hypothesis:** Decompilers have edge cases (found bugs in NumPy/Astropy). Property-based testing finds these.
- **inline-snapshot:** Superior to ApprovalTests for decompiled output (Samuel Colvin: "transformative", puts snapshots inline in test code).
- **pytest-testmon:** With 100% coverage, test suite will grow. Testmon keeps it fast.

**Confidence:** MEDIUM - Versions verified, but adoption timing depends on roadmap priorities

### Bytecode Comparison (Existing - Document Only)

| Component | Location | Purpose | Notes |
|-----------|----------|---------|-------|
| BytecodeComparator | vcdecomp/validation/bytecode_compare.py | Compare original vs recompiled .SCR bytecode | Custom implementation, domain-specific |
| DifferenceCategorization | vcdecomp/validation/difference_types.py | Categorize differences (semantic/cosmetic/optimization) | No off-the-shelf tool exists for this |
| ValidationOrchestrator | vcdecomp/validation/validator.py | Workflow: compile → compare → report | Already implemented with caching |

**Rationale:** Python stdlib (difflib, filecmp) insufficient for bytecode comparison. Need domain knowledge:
- SCR file format (12-byte instructions, data segment alignment)
- Semantic vs cosmetic differences (register allocation changes are OK, control flow changes are NOT OK)
- Opcode variant handling (runtime vs compiler opcodes)

**Existing solution is correct approach.** Standard binary diff tools (bindiff, vbindiff) lack domain semantics.

**Confidence:** HIGH - Reviewed existing implementation, fits requirements

### Debugging & Interactive Development

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| ipdb | >=0.13.13 | Interactive debugger | Enhanced pdb with IPython features (syntax highlight, tab complete), better than pdb for interactive debugging |
| pytest --pdb | (builtin) | Drop into debugger on test failure | Drop into ipdb when validation fails, inspect bytecode differences interactively |

**Rationale:**
- **ipdb over pdb:** IPython integration, same commands as pdb but better UX
- **ipdb over pudb:** CLI-based like ipdb but simpler, lower learning curve. Pudb's full-screen UI is overkill.
- **pytest --pdb integration:** Run `pytest --pdb --pdbcls=IPython.terminal.debugger:Pdb` for automatic breakpoint on failure

**Confidence:** MEDIUM - Tool selection solid, but version for ipdb not found in 2026 results (using latest known stable)

### Developer Workflow Automation (Optional)

| Technology | Version | Purpose | When to Use |
|------------|---------|---------|-------------|
| pytest-watcher | >=0.4.3 | Continuous test runner (file watching) | Local dev: auto-rerun tests on save (pytest-watch is unmaintained) |
| tox | >=4.21.2 | Multi-environment testing | Test across Python 3.10, 3.11, 3.12, 3.13 if supporting multiple versions |

**Rationale:**
- **pytest-watcher:** pytest-watch is dead, pytest-watcher is the maintained fork
- **tox:** Only needed if supporting multiple Python versions. Current project uses Python 3.13.7 only.

**Confidence:** MEDIUM - Not critical for single-version project

## Installation

### Core Stack (Phase 1)

```bash
# Testing framework
pip install pytest>=9.1.0
pip install pytest-cov>=6.0.0
pip install pytest-xdist>=3.6.1
pip install pytest-timeout>=2.3.1

# Code quality
pip install ruff>=0.14.13
pip install mypy>=1.19.1
pip install pre-commit>=4.0.1

# Reporting
pip install pytest-html>=4.1.1

# Debugging
pip install ipdb>=0.13.13
```

### Optional Extensions (Phase 2+)

```bash
# Advanced testing
pip install hypothesis>=6.150.2
pip install pytest-benchmark>=5.1.0
pip install inline-snapshot>=0.20.0
pip install pytest-testmon>=2.2.0

# Developer workflow
pip install pytest-watcher>=0.4.3
```

### Pre-commit Setup

```bash
# Install pre-commit hooks
pre-commit install

# Create .pre-commit-config.yaml:
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.13
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.19.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## Alternatives Considered

| Category | Recommended | Alternative | Why Not Alternative |
|----------|-------------|-------------|---------------------|
| Linter | Ruff | Pylint | Ruff is 10-100x faster, has more rules (800 vs 409), replaces 6 tools. Pylint's type inference covered by mypy. |
| Linter | Ruff | Flake8 + plugins | Ruff reimplements Flake8 plugins natively, single tool vs plugin sprawl |
| Formatter | Ruff | Black | Ruff format mode is Black-compatible, one tool vs two |
| Coverage | pytest-cov | coverage.py alone | pytest-cov is thin wrapper, same engine, better pytest integration |
| Parallelization | pytest-xdist | pytest-parallel | pytest-xdist is official pytest-dev project, more mature (pytest-parallel is community) |
| Continuous testing | pytest-watcher | pytest-watch | pytest-watch unmaintained (last update 2020), doesn't work for many users |
| Snapshot testing | inline-snapshot | snapshottest | inline-snapshot is newer (2023+), snapshots in-code not separate files, Pydantic creator endorsement |
| Snapshot testing | inline-snapshot | ApprovalTests.Python | inline-snapshot: modern, in-code. ApprovalTests: legacy, external files. Inline is 2026 standard. |
| Type checker | mypy | Pyright | mypy is reference implementation (by Python creator Guido van Rossum team), 4x faster with mypyc compilation |
| Binary diff | Custom (existing) | bindiff / vbindiff | Generic tools lack SCR domain knowledge (opcode semantics, segment alignment, semantic vs cosmetic) |
| Debugger | ipdb | pdb | ipdb = pdb + IPython (syntax highlight, tab complete, better REPL). Same commands, better UX. |
| Debugger | ipdb | pudb | pudb is full-screen TUI, steeper learning curve. ipdb is CLI, familiar to pdb users. |

## What NOT to Use

### unittest (use pytest instead)
- Project already uses pytest
- pytest has better fixtures, parameterization, plugins
- unittest is stdlib but less ergonomic

### nose / nose2 (deprecated)
- nose is dead (unmaintained since 2015)
- nose2 exists but pytest won the ecosystem battle

### pytest-runner / setup.py test (deprecated)
- Deprecated by pytest docs (2026)
- Use `pytest` CLI directly or tox

### Black (use Ruff format instead)
- Ruff format is Black-compatible
- One tool vs two
- Ruff is faster

### isort / autoflake / pyupgrade (use Ruff instead)
- Ruff replaces all of these
- Single configuration vs scattered configs

### Generic binary diff tools for validation
- bindiff, vbindiff, bsdiff: No domain semantics
- Can't distinguish semantic vs cosmetic bytecode differences
- Keep custom BytecodeComparator

## Environment Notes

### Windows-Specific Considerations

**Compiler Constraint:** Original SCMP.exe is Windows-only (.exe binary), no Linux/Mac support.

**Tool Compatibility:**
- ✅ pytest, ruff, mypy: Cross-platform, Windows native support
- ✅ pytest-xdist: Works on Windows (uses multiprocessing, not fork-based)
- ✅ pre-commit: Windows support via Git Bash or WSL
- ⚠️ pytest-watcher: File watching on Windows may have latency vs Linux (uses watchdog library, Windows FS events slower)

**CI/CD:** If using GitHub Actions, use `windows-latest` runner, not Linux (compiler requirement).

### Python Version

**Current:** Python 3.13.7 (detected from project)

**Support range:** Pytest 9.1 supports Python 3.10-3.14, Ruff supports 3.7+, mypy supports 3.10+. Full stack compatible with Python 3.10-3.14.

**Recommendation:** Stay on Python 3.13.x (stable, modern, good performance). No need to upgrade to 3.14 alpha.

## Integration Points

### Existing Validation System

**Already implemented (keep these):**

1. **ValidationOrchestrator** (vcdecomp/validation/validator.py)
   - Workflow: compile source → compare bytecode → categorize differences
   - Caching support for batch validation
   - Custom HTML report generation

2. **BytecodeComparator** (vcdecomp/validation/bytecode_compare.py)
   - Domain-specific SCR format knowledge
   - Difference categorization (semantic/cosmetic/optimization)
   - Opcode variant handling

3. **CLI Integration** (vcdecomp/__main__.py)
   - `python -m vcdecomp validate` single file
   - `python -m vcdecomp validate-batch` parallel batch with `--jobs 8`

**Stack integration points:**

- pytest-xdist parallelization: Mirrors existing `--jobs` flag pattern
- pytest-html: Complements custom HTML reports (unit tests vs validation reports)
- pre-commit: Runs before commits, validation runs on-demand

### GUI Integration (Future)

PROJECT.md mentions: "One-click compile integration in GUI"

**Stack considerations:**
- PyQt6 already in requirements.txt
- Validation can be triggered from GUI via ValidationOrchestrator API
- HTML reports can be displayed in QWebEngineView widget

## Configuration Files

### pyproject.toml (recommended)

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "vcdecomp"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "PyQt6>=6.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=9.1.0",
    "pytest-cov>=6.0.0",
    "pytest-xdist>=3.6.1",
    "pytest-timeout>=2.3.1",
    "pytest-html>=4.1.1",
    "ruff>=0.14.13",
    "mypy>=1.19.1",
    "ipdb>=0.13.13",
]
test-advanced = [
    "hypothesis>=6.150.2",
    "pytest-benchmark>=5.1.0",
    "inline-snapshot>=0.20.0",
    "pytest-testmon>=2.2.0",
]

[tool.pytest.ini_options]
testpaths = ["vcdecomp/tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = [
    "-v",
    "--strict-markers",
    "--cov=vcdecomp",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=100",  # Maintain 100% coverage requirement
]
timeout = 60  # Global timeout for hanging tests

[tool.coverage.run]
source = ["vcdecomp"]
omit = [
    "*/tests/*",
    "*/gui/*",  # GUI code excluded from coverage requirement
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
]
ignore = [
    "E501",  # Line too long (handled by formatter)
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",  # Allow assert in tests
]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
strict = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false  # Tests can be less strict
```

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.13
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.19.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--strict]
```

## Quality Gates

### Local Development

```bash
# Before commit (automated by pre-commit)
ruff check --fix .
ruff format .
mypy vcdecomp

# Run tests with coverage
pytest --cov=vcdecomp --cov-report=html

# Run validation on test scripts
python -m vcdecomp validate-batch \
    --input-dir Compiler-testruns/ \
    --original-dir Compiler-testruns/ \
    --jobs 8
```

### CI/CD Pipeline (Recommended)

```yaml
# GitHub Actions example (.github/workflows/test.yml)
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest  # Required for SCMP.exe compiler

    steps:
    - uses: actions/checkout@v4

    - uses: actions/setup-python@v5
      with:
        python-version: '3.13'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Lint with ruff
      run: |
        ruff check .
        ruff format --check .

    - name: Type check with mypy
      run: mypy vcdecomp

    - name: Test with pytest
      run: |
        pytest --cov=vcdecomp \
               --cov-report=html \
               --cov-report=xml \
               --html=test-report.html \
               --self-contained-html \
               -n auto  # Parallel execution

    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        files: ./coverage.xml

    - name: Upload test report
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: test-report
        path: test-report.html

    - name: Validate decompilation
      run: |
        python -m vcdecomp validate-batch \
          --input-dir Compiler-testruns/ \
          --original-dir Compiler-testruns/ \
          --jobs 8 \
          --report-file validation-report.html

    - name: Upload validation report
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: validation-report
        path: validation-report.html
```

## Success Metrics

### Code Quality Metrics

- **100% test coverage** on core modules (vcdecomp/core/ir/structure/*)
- **Type hint coverage:** Maintain current 87%, target 95%+
- **Ruff violations:** Zero (enforced by pre-commit)
- **mypy errors:** Zero (strict mode)

### Validation Metrics

- **Bytecode match rate:** % of decompiled scripts that recompile to identical bytecode
- **Semantic difference rate:** % with behavioral differences (target: <5%)
- **Compilation success rate:** % that compile without errors (current baseline: establish, then track)

### Performance Metrics

- **Test suite runtime:** Baseline with pytest-xdist, track regressions
- **Validation batch time:** 100 scripts in <5 minutes (8 parallel jobs)
- **Decompilation speed:** Track with pytest-benchmark if adopted

## Sources

### Testing & Coverage
- [pytest 9.1 Documentation](https://docs.pytest.org/en/stable/changelog.html) (Latest version: 9.1, Jan 2026)
- [pytest-cov PyPI](https://pypi.org/project/pytest-cov/) (Latest: 6.0.0)
- [coverage.py 7.13.1 Documentation](https://coverage.readthedocs.io/) (Released Dec 2025)
- [Good Integration Practices - pytest documentation](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/) (Parallel execution)
- [pytest-timeout PyPI](https://pypi.org/project/pytest-timeout/)

### Code Quality Tools
- [Ruff 0.14.13 Documentation](https://docs.astral.sh/ruff/) (Released Jan 15, 2026)
- [Ruff FAQ](https://docs.astral.sh/ruff/faq/) (Comparison with Pylint)
- [mypy 1.19.1 Documentation](https://mypy.readthedocs.io/) (Released Dec 15, 2025)
- [How do Ruff and Pylint compare?](https://pydevtools.com/handbook/explanation/how-do-ruff-and-pylint-compare/)
- [Top 10 Python Code Analysis Tools in 2026](https://www.jit.io/resources/appsec-tools/top-python-code-analysis-tools-to-improve-code-quality)

### Advanced Testing
- [Hypothesis 6.150.2 Documentation](https://hypothesis.readthedocs.io/) (Released Jan 13, 2026)
- [inline-snapshot PyPI](https://pypi.org/project/inline-snapshot/)
- [pytest-testmon GitHub](https://github.com/tarpas/pytest-testmon)

### Reporting
- [pytest-html Documentation](https://pytest-html.readthedocs.io/)
- [pytest-html-reporter PyPI](https://pypi.org/project/pytest-html-reporter/)

### Developer Workflow
- [pre-commit Framework](https://pre-commit.com/) (Updated Jan 3, 2026)
- [pytest-watcher PyPI](https://pypi.org/project/pytest-watcher/)

### Binary/Bytecode Comparison
- [Google BinDiff](https://github.com/google/bindiff) (Not suitable - lacks domain semantics)
- [Python difflib Documentation](https://docs.python.org/3/library/difflib.html)
- [Python filecmp Documentation](https://docs.python.org/3/library/filecmp.html)

### Debugging
- [ipdb PyPI](https://pypi.org/project/ipdb/)
- [Better Python Debugging With IPDB](https://hasil-sharma.github.io/2017-05-13-python-ipdb/)
- [A Guide to Debugging Python Code with ipdb](https://betterstack.com/community/guides/scaling-python/python-debugging/)
