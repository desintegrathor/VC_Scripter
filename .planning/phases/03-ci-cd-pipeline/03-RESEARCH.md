# Phase 3: CI/CD Pipeline - Research

**Researched:** 2026-01-17
**Domain:** GitHub Actions CI/CD with pytest integration
**Confidence:** HIGH

## Summary

GitHub Actions provides a complete CI/CD solution for automating pytest validation on self-hosted Windows runners. The standard approach uses workflow YAML files to trigger test execution on push/pull_request events, leverages GitHub's artifact storage for test results and baselines, and integrates status checks to block merges when validation fails.

For this project, the key technical challenge is running a Windows-only compiler (SCMP.exe) in a self-hosted runner environment with proper serialization (already solved via threading.Lock in Phase 2). The standard stack includes GitHub Actions workflows, pytest with plugins for better CI integration (pytest-github-actions-annotate-failures for annotations, pytest-json-report for structured results), and artifact storage for test baselines and regression comparison.

**Primary recommendation:** Use self-hosted Windows runner with pytest integration, store baselines in Git repository (version-controlled), upload test results as artifacts (retention/comparison), and enable required status checks on pull requests for merge protection.

## Standard Stack

The established libraries/tools for GitHub Actions pytest CI/CD:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| GitHub Actions | Native | CI/CD orchestration | Official GitHub CI/CD platform, zero-cost for private repos |
| pytest | 9.0.2 | Test execution | Already used in project, Python standard |
| actions/setup-python@v5 | v5 | Python environment | Official GitHub action, version management |
| actions/upload-artifact@v4 | v4 | Test result storage | Official GitHub artifact storage |
| actions/download-artifact@v5 | v5 | Baseline retrieval | Official GitHub artifact retrieval |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest-github-actions-annotate-failures | 0.2.0+ | Annotate failures in PR | Always - provides inline error annotations |
| pytest-json-report | 1.5.0+ | Structured test results | Optional - enables programmatic result processing |
| pytest-xdist | 3.6.0+ | Parallel test execution | Future optimization - not Phase 3 priority |
| pytest-regressions | 2.5.0+ | Baseline management | Alternative to manual baseline storage |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Self-hosted runner | GitHub-hosted Windows runner | GitHub-hosted doesn't support 32-bit compiler, more expensive |
| Artifact storage | Git LFS for baselines | Git storage simpler for version control, artifacts better for results |
| pytest-regressions | Custom baseline implementation | Custom more flexible but pytest-regressions is proven |

**Installation:**
```bash
# Test execution (already installed)
pip install pytest>=9.0

# GitHub Actions integration plugins
pip install pytest-github-actions-annotate-failures
pip install pytest-json-report

# Optional: regression baseline management
pip install pytest-regressions
```

## Architecture Patterns

### Recommended Project Structure
```
.github/
├── workflows/
│   ├── validation.yml           # Main validation workflow
│   └── regression-report.yml    # Optional: regression summary
.planning/
└── baselines/                    # Git-tracked test baselines
    └── {test-name}.json
vcdecomp/
└── tests/
    ├── conftest.py              # Existing fixtures
    └── test_validation.py       # Existing parametrized tests
```

### Pattern 1: Self-Hosted Windows Runner Workflow
**What:** GitHub Actions workflow that runs pytest validation on Windows self-hosted runner
**When to use:** Every push to main, every pull request
**Example:**
```yaml
# Source: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python
name: Validation Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: [self-hosted, windows, x64]

    steps:
    - uses: actions/checkout@v4

    - uses: actions/setup-python@v5
      with:
        python-version: '3.13'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-github-actions-annotate-failures
        pip install PyQt6

    - name: Run validation tests
      run: |
        py -m pytest vcdecomp/tests/test_validation.py -v --tb=short
```

### Pattern 2: Baseline Storage in Git Repository
**What:** Store expected test outcomes in Git for version control and regression detection
**When to use:** When baselines should be version-controlled alongside code changes
**Example:**
```python
# Source: https://pytest-regressions.readthedocs.io/en/latest/overview.html
# Using pytest-regressions for automatic baseline management
def test_decompilation_validation_with_baseline(data_regression):
    result = decompile_and_validate(script_path)

    # First run: generates baseline YAML
    # Subsequent runs: compares against baseline
    data_regression.check({
        "verdict": result.verdict.value,
        "compilation_succeeded": result.compilation_succeeded,
        "bytecode_identical": result.bytecode_identical,
        "semantic_differences": len(result.get_differences_by_category(DifferenceCategory.SEMANTIC))
    })
```

### Pattern 3: Artifact Upload for Test Results
**What:** Upload pytest results and compilation artifacts for debugging and historical tracking
**When to use:** Always - enables debugging failures without local reproduction
**Example:**
```yaml
# Source: https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts
- name: Run validation tests
  run: |
    py -m pytest vcdecomp/tests/test_validation.py -v \
      --junit-xml=test-results.xml \
      --json-report --json-report-file=test-report.json
  continue-on-error: true  # Always upload artifacts even on failure

- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: |
      test-results.xml
      test-report.json
    retention-days: 30
```

### Pattern 4: Required Status Checks
**What:** Configure branch protection to require validation passing before merge
**When to use:** Always - prevents merging broken code
**Configuration:**
```
Repository Settings → Branches → Branch protection rules → Add rule
- Branch name pattern: main
- ✓ Require status checks to pass before merging
  - ✓ Require branches to be up to date before merging
  - Required checks: "validate" (job name from workflow)
```

### Anti-Patterns to Avoid
- **Using pull_request_target**: Security risk - executes code from forks with write permissions ([source](https://securitylab.github.com/resources/github-actions-new-patterns-and-mitigations/))
- **Not using continue-on-error for artifact upload**: Artifacts won't upload if tests fail
- **Hardcoding paths**: Use relative paths from repository root, not absolute
- **Using @main for actions in production**: Pin to commit SHA or version tag ([source](https://www.datree.io/resources/github-actions-best-practices))
- **Default token permissions**: Set to read-only, elevate only where needed

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Baseline comparison | Custom JSON diff logic | pytest-regressions | Handles parametrization, auto-updates, proven |
| Test failure annotations | Parse pytest output, call GitHub API | pytest-github-actions-annotate-failures | Handles line numbers, file paths, auto-detection |
| Test result reporting | Custom HTML/Markdown generator | pytest --junit-xml + Test Reporter action | Standard format, many tools support |
| Parallel test execution | Custom multiprocessing | pytest-xdist | Handles fixtures, proper isolation, battle-tested |
| Self-hosted runner service | Custom Windows service wrapper | GitHub's config.cmd --runasservice | Official, handles auto-updates, logs |

**Key insight:** GitHub Actions ecosystem is mature with proven plugins. Custom solutions add maintenance burden for marginal benefit. Use official actions (@actions/\*) and popular pytest plugins (pytest-dev org).

## Common Pitfalls

### Pitfall 1: Workflow Doesn't Appear in Status Checks
**What goes wrong:** Branch protection settings don't show workflow job as available required check
**Why it happens:** GitHub only shows checks that have run on the target branch (main) within last 7 days. Workflows triggered only by `pull_request` won't appear.
**How to avoid:** Include `push: branches: [main]` trigger in workflow, run once on main branch
**Warning signs:** Branch protection dropdown is empty or missing expected check name
**Source:** [GitHub Docs - Troubleshooting required status checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks)

### Pitfall 2: Path Filtering Causes "Waiting for status" Block
**What goes wrong:** PR stuck "waiting for status to be reported" because workflow was skipped
**Why it happens:** Using `paths:` or `paths-ignore:` can skip workflow, but required status check still expects it
**How to avoid:** Don't use path filtering for required status check workflows, or use `if:` conditionals inside jobs to skip steps
**Warning signs:** PR shows "Expected — Waiting for status to be reported" indefinitely
**Source:** [GitHub Community Discussion #26698](https://github.com/orgs/community/discussions/26698)

### Pitfall 3: Self-Hosted Runner Can't Access SCMP.exe
**What goes wrong:** Workflow fails with "SCMP.exe not found" or permission denied
**Why it happens:** Runner service account doesn't have access to compiler directory, or path is incorrect
**How to avoid:**
- Install runner in `C:\actions-runner` (Windows system account access)
- Ensure compiler directory (`original-resources/compiler`) is in repository
- Use relative paths from repository root in conftest.py fixture
**Warning signs:** Works locally but fails in CI with path/permission errors
**Source:** [GitHub Docs - Adding self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners)

### Pitfall 4: Concurrent Test Execution Deadlocks SCMP.exe
**What goes wrong:** Tests hang or fail intermittently with compiler errors
**Why it happens:** DOS-era compiler doesn't support concurrent execution
**How to avoid:** Already solved in Phase 2 - threading.Lock in validator.py serializes compiler access. Don't use pytest-xdist without accounting for this.
**Warning signs:** Tests pass individually but fail when run together
**Source:** Project's validation/validator.py line 30 (existing solution)

### Pitfall 5: Artifact Upload Fails When Tests Fail
**What goes wrong:** Test artifacts (JUnit XML, JSON reports) aren't uploaded when tests fail
**Why it happens:** pytest exits with non-zero status, workflow stops before artifact upload
**How to avoid:** Use `continue-on-error: true` on pytest step and `if: always()` on artifact upload
**Warning signs:** No artifacts available for failed workflow runs
**Source:** [GitHub Docs - Storing workflow data as artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)

### Pitfall 6: Baseline Files Not Committed After Regeneration
**What goes wrong:** pytest-regressions regenerates baselines but they're not persisted, tests fail on next run
**Why it happens:** Running pytest with `--regen-all` locally but not committing generated YAML files
**How to avoid:**
- Commit baseline files to Git after regeneration
- Add `.pytest_cache/` to .gitignore (not baseline files)
- Document baseline regeneration workflow for team
**Warning signs:** Tests pass locally after `--regen-all` but fail in CI
**Source:** [pytest-regressions docs](https://pytest-regressions.readthedocs.io/en/latest/overview.html)

## Code Examples

Verified patterns from official sources:

### Complete Validation Workflow
```yaml
# Source: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python
# Adapted for Windows self-hosted runner with SCMP.exe validation
name: Decompilation Validation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read
  pull-requests: write  # For pytest-coverage-comment if used

jobs:
  validate:
    runs-on: [self-hosted, windows, x64]
    timeout-minutes: 30

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Setup Python 3.13
      uses: actions/setup-python@v5
      with:
        python-version: '3.13'
        cache: 'pip'  # Cache pip dependencies for faster runs

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-github-actions-annotate-failures pytest-json-report
        pip install -r vcdecomp/requirements.txt

    - name: Run validation tests
      run: |
        py -m pytest vcdecomp/tests/test_validation.py -v `
          --tb=short `
          --junit-xml=test-results.xml `
          --json-report --json-report-file=test-report.json
      continue-on-error: true

    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-results-${{ github.run_number }}
        path: |
          test-results.xml
          test-report.json
        retention-days: 30

    - name: Publish test results
      if: always()
      uses: EnricoMi/publish-unit-test-result-action/windows@v2
      with:
        files: test-results.xml
        check_name: Validation Test Results
```

### Baseline Storage with pytest-regressions
```python
# Source: https://pytest-regressions.readthedocs.io/en/latest/overview.html
# Add to vcdecomp/tests/test_validation.py

@pytest.mark.parametrize("test_id,scr_path,original_c", TEST_SCRIPTS)
def test_decompilation_validation_with_baseline(
    test_id, scr_path, original_c, validation_orchestrator, tmp_path, data_regression
):
    """
    Test decompilation with baseline regression detection.

    On first run: Generates baseline YAML with test outcomes
    On subsequent runs: Compares against baseline, fails if regression detected
    """
    # ... existing decompilation logic ...

    result = validation_orchestrator.validate(scr_path, decompiled_path)

    # Store regression-relevant metrics
    baseline_data = {
        "verdict": result.verdict.value,
        "compilation_succeeded": result.compilation_succeeded,
        "bytecode_identical": result.bytecode_identical,
        "error_count": len(result.compilation_result.errors) if not result.compilation_succeeded else 0,
        "semantic_diffs": len(result.get_differences_by_category(DifferenceCategory.SEMANTIC)),
    }

    # Compare against baseline (fails if regression detected)
    data_regression.check(baseline_data)
```

### Runner Configuration Script
```powershell
# Source: https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners
# Run in Administrator PowerShell on Windows runner machine

# Download runner
mkdir C:\actions-runner ; cd C:\actions-runner
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.321.0/actions-runner-win-x64-2.321.0.zip -OutFile actions-runner-win-x64-2.321.0.zip
Expand-Archive -Path .\actions-runner-win-x64-2.321.0.zip -DestinationPath .

# Configure runner
# Get token from: Repository Settings → Actions → Runners → New self-hosted runner
.\config.cmd --url https://github.com/USER/REPO --token YOUR_TOKEN --labels windows,x64 --runasservice

# Start runner service
.\run.cmd
```

### Regression Detection with Baseline Download
```yaml
# Source: https://docs.github.com/en/actions/managing-workflow-runs/downloading-workflow-artifacts
# Advanced: Compare current results against baseline from previous successful run

- name: Download baseline results
  uses: actions/download-artifact@v5
  with:
    name: baseline-test-results
    path: baseline/
  continue-on-error: true  # First run won't have baseline

- name: Compare against baseline
  if: always()
  run: |
    if (Test-Path baseline/test-report.json) {
      py -m vcdecomp.validation.compare_baselines `
        baseline/test-report.json test-report.json
    } else {
      Write-Host "No baseline found - this run becomes new baseline"
    }
  shell: powershell

- name: Save as new baseline if success
  if: success()
  uses: actions/upload-artifact@v4
  with:
    name: baseline-test-results
    path: test-report.json
    retention-days: 90
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| actions/upload-artifact@v3 | @v4 (immutable artifacts) | 2024 | Must use unique names for each upload, can't overwrite |
| actions/download-artifact@v4 | @v5 | 2025 | Better multi-artifact handling, wildcard support |
| setup-python@v4 | @v5 | 2025 | Improved caching, better version resolution |
| pytest-json plugin (unmaintained) | pytest-json-report | 2023+ | Active maintenance, better xdist support |
| Jenkins/Travis CI | GitHub Actions | 2019+ | Native GitHub integration, simpler YAML, free for private repos |

**Deprecated/outdated:**
- **save-state/set-output commands**: Use environment files instead (`echo "name=value" >> $GITHUB_OUTPUT`)
- **Node.js 12/16 actions**: GitHub deprecating, use Node.js 20 actions
- **pull_request_target for forks**: Security risk, use pull_request with appropriate permissions

## Open Questions

Things that couldn't be fully resolved:

1. **Baseline storage longevity for artifacts**
   - What we know: GitHub stores artifacts 90 days default, configurable retention
   - What's unclear: Whether 90 days sufficient for long-term regression tracking vs Git storage
   - Recommendation: Use Git repository for long-term baselines (pytest-regressions pattern), artifacts for ephemeral test results

2. **Optimal parallelization strategy with SCMP.exe lock**
   - What we know: Threading.Lock prevents concurrent SCMP.exe execution, pytest-xdist can parallelize test collection/setup
   - What's unclear: Whether parallelization gains worth complexity given compiler serialization bottleneck
   - Recommendation: Defer to Phase 4/5 - measure actual test duration before optimizing

3. **Self-hosted runner scaling for multiple PRs**
   - What we know: Single runner processes jobs sequentially, can add more runners with same labels
   - What's unclear: Whether single runner sufficient for expected PR volume
   - Recommendation: Start with one runner, monitor queue times, add runners if CI becomes bottleneck

## Sources

### Primary (HIGH confidence)
- [GitHub Docs - Adding self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners) - Official setup instructions
- [GitHub Docs - Building and testing Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python) - Official pytest workflow patterns
- [GitHub Docs - Storing workflow data as artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts) - Artifact upload/download patterns
- [pytest-regressions documentation](https://pytest-regressions.readthedocs.io/en/latest/overview.html) - Baseline management patterns
- [GitHub Docs - Using self-hosted runners in workflow](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow) - Labels and runs-on syntax
- [GitHub Docs - About status checks](https://docs.github.com/articles/about-status-checks) - Branch protection configuration

### Secondary (MEDIUM confidence)
- [pytest-github-actions-annotate-failures GitHub](https://github.com/pytest-dev/pytest-github-actions-annotate-failures) - Official pytest plugin for annotations
- [GitHub Actions Security Guide - Wiz Blog](https://www.wiz.io/blog/github-actions-security-guide) - Security best practices (2025+)
- [GitHub Actions Best Practices - Datree.io](https://www.datree.io/resources/github-actions-best-practices) - Community best practices
- [Exercism GitHub Actions Best Practices](https://exercism.org/docs/building/github/gha-best-practices) - Practical patterns

### Tertiary (LOW confidence)
- Community discussions on status check issues - anecdotal troubleshooting
- Third-party test reporter actions - functionality verified but not official

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Official GitHub documentation, pytest is Python standard, plugins widely used
- Architecture: HIGH - Patterns from official docs, proven in production use
- Pitfalls: MEDIUM-HIGH - Mix of official documentation (HIGH) and community reports (MEDIUM)

**Research date:** 2026-01-17
**Valid until:** 2026-04-17 (90 days - GitHub Actions is mature, changes are incremental)
