# Phase 2: Test Suite Automation - Context

**Gathered:** 2026-01-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Automated validation of all test cases with pytest integration - measuring current decompilation quality across a comprehensive test corpus. This phase establishes the testing infrastructure that enables iterative improvement workflow: decompile → test → identify failures → fix → repeat.

Test scripts are located in `decompiler_source_tests/` (not `Compiler-testruns/`).

</domain>

<decisions>
## Implementation Decisions

### Test Corpus Scope
- Initial corpus: Only scripts from `decompiler_source_tests/` (known original source)
- Focus on scripts with original C source for highest confidence baseline
- Expansion to mission scripts (`script-folders/`) deferred to later phases

### Primary Goal
- **Enable iterative improvement workflow** - fast feedback loop for fixing decompilation issues
- Not just measuring baseline - must support rapid iteration cycles
- Organization decisions deferred until after analyzing actual decompilation quality

### Test Execution Strategy
- **Always fresh decompilation** - every pytest run decompiles from .scr and compiles
- Guarantees testing current decompiler state, no stale cached outputs
- **Sequential execution** - one test at a time for clearer output and easier debugging
- **Continue on failure** - collect all failures in one run, preserve artifacts for each
- No fail-fast mode - want to see complete picture of what's broken

### Claude's Discretion
- Test organization structure (flat vs grouped) - decide after seeing decompilation quality
- Level of failure categorization detail - based on observed error patterns
- What debug information to preserve per test failure
- Pytest output verbosity and formatting
- Artifact preservation strategy (logs, .err files, bytecode diffs)
- Whether to implement test discovery or explicit test list

</decisions>

<specifics>
## Specific Ideas

- User emphasized: "look at decompiled.c and disassembled.asm and original.c files and see how deep in shit it is"
- Organizational decisions should be data-driven based on actual decompiler performance
- Test suite must support debugging workflow, not just pass/fail metrics

</specifics>

<deferred>
## Deferred Ideas

- Parallel test execution (pytest-xdist) - sequential sufficient for now
- Comprehensive test corpus including all mission scripts - start small with known-source only
- Advanced failure categorization system - Phase 4 (Error Analysis System) handles this

</deferred>

---

*Phase: 02-test-suite-automation*
*Context gathered: 2026-01-17*
