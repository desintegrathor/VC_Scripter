# Phase 6: Expression Reconstruction Fixes - Context

**Gathered:** 2026-01-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix the decompiler's expression reconstruction to produce syntactically valid C code that compiles successfully with SCMP.exe. This phase addresses syntax errors in expression generation - semantic correctness (bytecode equivalence) is verified by existing validation infrastructure but not fixed here.

Scope includes: operator precedence, type casts, complex expressions with multiple operators.
Out of scope: variable declaration fixes (Phase 7), control flow fixes (Phase 8).

</domain>

<decisions>
## Implementation Decisions

### Reference Standard
- **Ground truth:** Original C source files in `Compiler-testruns/` directory
- **Style guide:** `original-resources/Scripting_SDK.txt` (official Vietcong SDK)
- Decompiler output must match the coding patterns visible in these references

### Approach
- Analyze expression patterns in known-good original source code
- Fix expression reconstruction bugs to match original style
- Use validation system (`python -m vcdecomp validate`) to verify output compiles
- No subjective style choices - match what the original developers wrote

### Claude's Discretion
- How to categorize and prioritize different expression bug types
- Implementation strategy for fixes (order of operations, refactoring approach)
- Test case selection and coverage strategy
- Code organization within the expression reconstruction module

</decisions>

<specifics>
## Specific Ideas

- Original source files provide exact reference: `Compiler-testruns/Testrun1/tdm.c`, `hitable.c`, etc.
- Validation system already exists - use it to verify each fix compiles correctly
- Error Analysis System (Phase 4) can categorize syntax errors to guide prioritization
- This is reverse engineering with ground truth, not greenfield development

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope

</deferred>

---

*Phase: 06-expression-reconstruction-fixes*
*Context gathered: 2026-01-18*
