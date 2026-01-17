# Phase 3: CI/CD Pipeline - Context

**Gathered:** 2026-01-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Establish automated validation on every commit through GitHub Actions. The CI pipeline runs the pytest validation suite (from Phase 2) automatically, detects regressions when previously-passing scripts fail, persists test baselines for comparison, and shows validation status on pull requests. This enables continuous quality monitoring without manual testing.

</domain>

<decisions>
## Implementation Decisions

### Windows Runner Setup
- **Self-hosted runner** on existing Windows machine (not GitHub-hosted)
- Run as regular user account (not isolated service account)
- Simpler setup, direct access to SCMP.exe and existing tooling
- Machine must remain online to process CI jobs

### Test Execution Strategy
- **Run all tests** even after failures (not fail-fast)
- Complete test suite execution shows full picture of what's broken
- Longer CI runs, but comprehensive failure visibility

### Claude's Discretion
- Baseline storage location (Git repo, artifacts, or external storage)
- Regression reporting format (PR comments, status checks, issues, notifications)
- Runner installation and registration process
- Workflow trigger configuration (push, PR, scheduled)
- Artifact retention policies
- Test parallelization within CI environment

</decisions>

<specifics>
## Specific Ideas

- Existing Windows machine is available and can stay online for CI
- User prefers seeing all test results at once rather than stopping at first failure
- SCMP.exe is already accessible on the runner machine

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 03-ci-cd-pipeline*
*Context gathered: 2026-01-17*
