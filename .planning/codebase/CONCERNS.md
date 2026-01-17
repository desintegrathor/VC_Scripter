# Codebase Concerns

**Analysis Date:** 2026-01-17

## Tech Debt

**Expression Formatter Complexity:**
- Issue: `vcdecomp/core/ir/expr.py` is 2,571 lines - single monolithic module handling expression formatting, type inference, global resolution, and struct detection
- Files: `vcdecomp/core/ir/expr.py`
- Impact: Difficult to maintain, test, and extend. High cognitive load for modifications. Contains 20+ commented-out debug print statements indicating active debugging sessions
- Fix approach: Refactor into separate modules: `expression_builder.py`, `type_resolver.py`, `struct_analyzer.py`, `global_name_resolver.py`

**Deprecated Functions Still in Use:**
- Issue: Legacy function `format_structured_function()` marked as deprecated but still present in codebase
- Files: `vcdecomp/core/ir/structure/orchestrator.py` (lines 75-98)
- Impact: Code duplication, maintenance burden, potential for using wrong API
- Fix approach: Remove deprecated function after confirming no external callers exist. Add deprecation warning if removal requires migration period

**Deprecated Method in Type Detector:**
- Issue: `_has_network_functions()` marked DEPRECATED in favor of `_calculate_network_percentage()` but still exists
- Files: `vcdecomp/core/script_type_detector.py` (lines 163-169)
- Impact: Confusing API, maintenance overhead
- Fix approach: Remove deprecated method, ensure all callers use `_calculate_network_percentage()`

**TODO Comments Indicating Incomplete Features:**
- Issue: Multiple TODO comments indicating unfinished work
- Files:
  - `vcdecomp/core/ir/type_inference.py:503` - Field tracker integration incomplete
  - `vcdecomp/core/ir/structure/orchestrator.py:305` - Array declaration logic should be merged into SSA lowering
  - `vcdecomp/tests/test_function_detector.py:241,251,260` - Three test cases not implemented
  - `vcdecomp/core/headers/detector.py:94` - Multiplayer header detection incomplete
- Impact: Incomplete functionality, untested code paths, potential bugs in edge cases
- Fix approach: Prioritize completing field tracker integration and SSA lowering merger. Implement missing test cases with real .scr test files

**Commented Debug Code:**
- Issue: Extensive commented-out debug print statements throughout codebase
- Files:
  - `vcdecomp/core/ir/expr.py:646,1574,1576,1579` - Global resolution and ASGN pattern debugging
  - `vcdecomp/core/ir/structure/emit/block_formatter.py:156` - Early return detection debugging
  - `vcdecomp/core/ir/structure/analysis/value_trace.py:42,44,51` - Value tracing debugging
- Impact: Code clutter, suggests recent stability issues, makes code harder to read
- Fix approach: Remove commented debug code and use proper logging framework at DEBUG level. Keep debug capability but make it toggleable via logging config

**Heuristic-Based Global Variable Detection:**
- Issue: Global variable naming uses heuristics rather than definitive analysis
- Files: `vcdecomp/core/ir/global_resolver.py`, `vcdecomp/core/ir/expr.py:2048-2064`
- Impact: Global variables may be misidentified or unnamed, leading to incorrect decompilation output
- Fix approach: Implement symbol table analysis from debug info when available. Cross-reference with known SaveInfo structures

**Array Size Hardcoding:**
- Issue: Array sizes are hardcoded based on specific variable names rather than analyzed
- Files: `vcdecomp/__main__.py:531-544` - Special cases for `gRec`, `SideFrags`, etc.
- Impact: Brittle code that breaks with unknown variable patterns. Comment notes "SaveInfo is unreliable" suggesting data quality issues
- Fix approach: Implement proper array bound analysis from usage patterns (index accesses, loops). Add fallback to conservative estimates

**Legacy TODO for SSA Lowering Integration:**
- Issue: Variable declaration logic split between old system and new SSA lowering
- Files: `vcdecomp/core/ir/structure/orchestrator.py:305` - "TODO: Merge this logic into SSA lowering"
- Impact: Duplicate logic, potential inconsistencies between array/struct declarations
- Fix approach: Complete SSA lowering refactor to handle all variable declarations uniformly

**Circular Import Risk:**
- Issue: Conditional imports inside functions to avoid circular dependencies
- Files: `vcdecomp/core/ir/expr.py:631` - `from .global_resolver import resolve_globals_with_types` inside function
- Impact: Hidden dependencies, potential import failures in edge cases, difficult to track module relationships
- Fix approach: Restructure module dependencies. Move shared types to separate `types.py` module. Use dependency injection where appropriate

## Known Bugs

**Loop Condition Off-By-One:**
- Issue: Compiler generates `<=` for `<` in some loop conditions (off-by-one bug)
- Files: `vcdecomp/core/ir/structure/patterns/loops.py:168` - "Problem: Compiler generates <= for < in some cases"
- Symptoms: For-loops may have incorrect boundary conditions after decompilation
- Trigger: Specific loop patterns with backward jumps
- Workaround: Pattern detection analyzes jump direction to correct condition (fix implemented but documented as workaround)

**Global Variable Resolution Failures:**
- Issue: Global name resolution can silently fail with fallback to empty dict
- Files: `vcdecomp/core/ir/expr.py:640-650` - Exception caught but only prints to stderr
- Symptoms: Variables appear as `data_XXX` instead of meaningful names
- Trigger: Unknown - exception handling suggests intermittent failures
- Workaround: Code continues with empty global name map

## Security Considerations

**Windows Binary Dependencies:**
- Risk: Validation system requires Windows executables (SCMP.exe, SCC.exe, SASM.exe, SPP.exe) from 2002-2025
- Files: `original-resources/compiler/*.exe`, `vcdecomp/compiler/*.exe`
- Current mitigation: Executables are original Pterodon tools, stored in repository
- Recommendations:
  - Document provenance and checksums of all .exe files
  - Consider Wine compatibility layer for Linux/Mac development
  - Add virus scan CI step for executable artifacts
  - Store executables in LFS rather than direct commit

**Subprocess Execution:**
- Risk: External process execution with user-controlled paths
- Files: `vcdecomp/validation/compiler_wrapper.py:139-179` - subprocess.run with file paths
- Current mitigation: Paths are validated, timeout enforced, encoding errors handled
- Recommendations: Add path sanitization to prevent directory traversal. Validate executable signatures before running

**Temporary File Cleanup:**
- Risk: Sensitive compilation artifacts may persist if cleanup fails
- Files: `vcdecomp/validation/compiler_wrapper.py:187-238` - Cleanup logic with multiple failure modes
- Current mitigation: Context manager and destructor attempt cleanup, configurable cleanup-on-failure
- Recommendations: Use atexit handlers for final cleanup guarantee. Log cleanup failures to security log

## Performance Bottlenecks

**Large Expression Module Load Time:**
- Problem: `expr.py` at 2,571 lines takes significant time to parse and import
- Files: `vcdecomp/core/ir/expr.py`
- Cause: Monolithic module with all expression formatting logic
- Improvement path: Split into smaller modules with lazy imports. Most decompilation tasks don't need all functionality

**No Caching of Header Database:**
- Problem: Header parsing happens on every run
- Files: `vcdecomp/parsing/header_parser.py`, `vcdecomp/core/headers/database.py`
- Cause: Headers re-parsed from source files each time
- Improvement path: Cache parsed header database to JSON/pickle. Invalidate on header file modification timestamp

**Validation Cache Not Enabled by Default:**
- Problem: Validation recompiles unchanged files
- Files: `vcdecomp/validation/cache.py` - Full caching system exists but requires opt-in
- Cause: Conservative default to avoid stale cache issues
- Improvement path: Enable caching by default with aggressive invalidation. Add `--no-cache` flag for debugging

**Linear Search in Global Resolution:**
- Problem: Data segment offset lookups use dictionary, but pattern matching uses linear iteration
- Files: `vcdecomp/core/ir/global_resolver.py` - Multiple `for offset, usage in globals_usage.items()` loops
- Cause: Need to find array bases by checking if offset falls within array range
- Improvement path: Build interval tree for array ranges. O(log n) lookup instead of O(n)

## Fragile Areas

**Switch Case Detection:**
- Files: `vcdecomp/core/ir/structure/patterns/switch_case.py:469,516` - Multiple "BUG FIX" comments
- Why fragile: Jump table analysis depends on compiler patterns. Three documented bug fixes suggest edge cases
- Safe modification: Always test on `Compiler-testruns/` known-good scripts. Verify jump table boundaries don't cross case bodies
- Test coverage: Good - dedicated test suite in `vcdecomp/tests/test_structure_patterns.py`

**If/Else Pattern Detection:**
- Files: `vcdecomp/core/ir/structure/patterns/if_else.py:347,390,393,412` - Four "CRITICAL FIX" comments
- Why fragile: JZ/JNZ semantics are opposite, merge point detection is complex, blocks can overlap with switch cases
- Safe modification: Run full test suite including compound conditions. Check for proper stop blocks to prevent bleeding into adjacent patterns
- Test coverage: Extensive tests in `vcdecomp/tests/test_structure_patterns.py` and `vcdecomp/tests/test_compound_conditions.py`

**Compound Condition Detection:**
- Files: `vcdecomp/core/ir/structure/orchestrator.py:443-449` - Compound conditions detected before early returns
- Why fragile: Detection order matters - compound patterns must be found before simpler patterns consume their blocks
- Safe modification: Maintain detection priority order. Test with nested && and || expressions
- Test coverage: Dedicated test suite in `vcdecomp/tests/test_compound_conditions.py`

**Variable Name Collision Resolution:**
- Files: `vcdecomp/core/ir/variable_renaming.py:177,324` - Pattern matching for tXXX_X, local_X, data_X
- Why fragile: String pattern matching with multiple underscore splits. Comment says "CRITICAL FIX: Distinguish between LOAD and STORE"
- Safe modification: Add test case for every new pattern. Verify no regex injection possible
- Test coverage: Coverage exists but not comprehensive for all edge cases

**Function Boundary Detection:**
- Files: `vcdecomp/core/ir/function_detector.py:59-141` - RET-based and CALL-based function detection
- Why fragile: Relies on heuristics (orphan code, entry point). Recent fixes mentioned in commit history
- Safe modification: Test with scripts that have multiple functions. Verify no overlap or gaps in address ranges
- Test coverage: Basic tests exist but marked with "TODO: Implement when we have test SCR files" for edge cases

## Scaling Limits

**Structure Module Complexity:**
- Current capacity: Handles typical game scripts (500-1500 instructions)
- Limit: Very large scripts (>5000 instructions) may have O(n²) behavior in BFS pattern detection
- Scaling path: Implement incremental pattern detection. Cache CFG analysis results. Add depth limits to BFS

**Bytecode Comparison Memory:**
- Current capacity: Full bytecode loaded into memory for comparison
- Limit: Large mission scripts with extensive data segments may consume significant memory
- Scaling path: Stream-based comparison for data/code segments. Only load headers fully into memory

**Parallel Validation:**
- Current capacity: Configurable job count for batch validation
- Limit: No built-in scheduling - all jobs start simultaneously
- Scaling path: Implement worker pool with queue. Add progress tracking and cancellation support

## Dependencies at Risk

**Windows-Only Compiler Tools:**
- Risk: SCMP.exe, SCC.exe, SASM.exe, SPP.exe are Windows 32-bit executables from 2002-2025
- Impact: Validation system completely broken on non-Windows platforms without Wine
- Migration plan:
  - Document Wine setup for Linux/Mac
  - Consider implementing Python-based compiler if specs reverse-engineered
  - Alternative: Server-based validation service running Windows

**No Dependency Version Pinning:**
- Risk: No requirements.txt or pyproject.toml with version constraints visible
- Impact: Uncontrolled dependency upgrades may break compatibility
- Migration plan: Add requirements.txt with pinned versions. Use dependabot for security updates

## Missing Critical Features

**No Symbol Table Preservation:**
- Problem: Debug symbols from .dbg files not integrated into decompiler
- Blocks: Accurate variable naming, function parameter names, local variable types
- Impact: Decompiled code uses generic names (local_0, param_1) instead of original names

**No Type Inference from Usage:**
- Problem: Type inference incomplete - field tracker integration incomplete (TODO comment)
- Blocks: Accurate struct type detection, pointer vs value disambiguation
- Impact: Many variables remain as `dword` (unknown type) in output

**No Cross-Function Analysis:**
- Problem: Each function analyzed independently
- Blocks: Global variable usage patterns, call graph analysis, unused function detection
- Impact: Incomplete optimization, redundant variable declarations

## Test Coverage Gaps

**Function Detector Edge Cases:**
- What's not tested: Empty functions, nested functions (if possible), entry point variations
- Files: `vcdecomp/tests/test_function_detector.py:241-260` - Three TODO test stubs
- Risk: Function boundary detection may fail on unusual script structures
- Priority: Medium - core functionality but heuristic-based

**Real Script End-to-End Tests:**
- What's not tested: Full decompilation + recompilation cycle on production game scripts
- Files: `vcdecomp/tests/test_end_to_end_decompilation.py` exists but limited coverage
- Risk: Integration issues between pipeline stages may not surface until production use
- Priority: High - validation is core feature

**Multiplayer Script Types:**
- What's not tested: Multiplayer level scripts with SC_MP_* functions
- Files: Header detection disabled (TODO at `vcdecomp/core/headers/detector.py:94`)
- Risk: Multiplayer scripts may have incorrect headers or missing function signatures
- Priority: Low - niche use case but documented in SDK

**Circular Import Edge Cases:**
- What's not tested: Import order variations when global_resolver imported conditionally
- Files: `vcdecomp/core/ir/expr.py:631` - Conditional import inside function
- Risk: Refactoring may trigger circular import errors not caught by current tests
- Priority: Medium - structural issue that could block development

**Platform-Specific Validation:**
- What's not tested: Validation on Wine/Linux/Mac
- Files: `vcdecomp/validation/compiler_wrapper.py` - Windows subprocess execution
- Risk: Cross-platform users cannot validate decompiled output
- Priority: Medium - limits contributor base

---

*Concerns audit: 2026-01-17*
