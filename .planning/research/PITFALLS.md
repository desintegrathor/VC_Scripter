# Domain Pitfalls: Decompiler Quality Improvement

**Domain:** Decompiler correctness and compilability improvement
**Researched:** 2025-01-17
**Confidence:** HIGH

---

## Critical Pitfalls

Mistakes that cause rewrites, regressions, or project failure.

### Pitfall 1: Fixing Without Validation Infrastructure

**What goes wrong:** Teams fix decompiler bugs by eyeballing output, then discover the fixes broke other scripts or introduced subtle semantic errors.

**Why it happens:**
- Decompilers have 45-55% accuracy even at state-of-the-art (Hex-Rays)
- Manual inspection misses semantic differences that only appear at runtime
- Small changes cascade through expression trees unpredictably

**Consequences:**
- "Whack-a-mole" bug fixing where fixes introduce new bugs
- Silent correctness regressions (output looks fine but behaves differently)
- Loss of confidence in decompiler output
- Inability to measure improvement progress

**Prevention:**
1. **Build validation first, fix second** - Never fix decompiler bugs without automated recompilation testing
2. **Bytecode comparison is mandatory** - Validate that recompiled bytecode matches original
3. **Categorize differences** - Distinguish semantic vs non-semantic bytecode differences
4. **Baseline everything** - Save validation results before each fix to detect regressions

**Detection:**
- Warning sign: "This fix looks good" without recompiling to verify
- Warning sign: No automated way to detect if a fix broke other scripts
- Warning sign: Discovering bugs only when users report them

**Phase mapping:** Phase 1 (Validation Infrastructure) must complete before Phase 2 (Bug Fixing)

---

### Pitfall 2: Testing with Too Few Test Cases

**What goes wrong:** Team has 3 test scripts, fixes bugs until those 3 compile, then discovers the decompiler fails on 90% of real-world scripts.

**Why it happens:**
- Small test suites create massive coverage blind spots
- Decompilers have 15+ distinct error types across different code patterns
- Compiler optimizations create edge cases (optimization level -O0 vs -O3)
- Pattern detection (if/else, switch/case, loops) fails on variants not in test suite

**Consequences:**
- False confidence that decompiler is "fixed"
- Production scripts fail with novel error patterns
- Bug fixes optimized for test cases, not real patterns
- Cannot measure actual improvement (3/3 passing means nothing if 3/200 real scripts pass)

**Prevention:**
1. **Batch validation from day 1** - Test against ALL available scripts, not just 3
2. **Stratified sampling** - Ensure test suite covers: simple/complex, different optimization levels, all control flow patterns
3. **Track pass rate metrics** - "127/200 scripts compile (63.5%)" not "3/3 pass"
4. **Prioritize by frequency** - Fix bugs that affect the most scripts first
5. **Real-world corpus** - Use actual game scripts (production code) not just compiler test runs

**Detection:**
- Warning sign: Test suite smaller than 20-30 scripts
- Warning sign: All test scripts are compiler-generated with debug info (missing real-world patterns)
- Warning sign: Team celebrating "all tests pass" when pass rate is 100% of 3 scripts
- Warning sign: No diversity in test cases (all similar structure/complexity)

**Phase mapping:** Phase 1 should include batch validation setup; Phase 2 should track pass rate across full corpus

---

### Pitfall 3: Chasing Perfect Decompilation Instead of Compilability

**What goes wrong:** Team spends weeks making decompiled code "readable" (nice variable names, beautiful formatting) but it still doesn't compile or has semantic errors.

**Why it happens:**
- Conflating two different goals: readability vs correctness
- Decompilation research focuses on readability metrics (identifier names, typecast correctness)
- "Perfect decompilation" is impossible - original macros are lost, optimizations obscure intent
- Readable code with wrong semantics is worse than ugly code that works

**Consequences:**
- Wasted effort on cosmetic improvements
- Core correctness bugs remain unfixed
- Project timeline explodes chasing diminishing returns
- Users get "pretty" code that doesn't work

**Prevention:**
1. **Core value: Compilability first** - Code must compile with original compiler before worrying about readability
2. **Semantic correctness second** - Recompiled bytecode must match original behavior
3. **Readability third** - Only after code compiles and validates correctly
4. **Accept decompiler limitations** - Variables named `local_X` are fine if code compiles
5. **Use validation verdict hierarchy**:
   - PERFECT (bytecode matches exactly) > ACCEPTABLE (semantic equivalent) > COMPILES (has warnings) > FAILED (doesn't compile)

**Detection:**
- Warning sign: PRs focused on variable naming before fixing syntax errors
- Warning sign: Discussions about "elegant" expression formatting when code doesn't compile
- Warning sign: Implementing type inference before fixing control flow bugs
- Warning sign: No validation of semantic equivalence, only visual inspection

**Phase mapping:** Roadmap should prioritize: Phase 2 (compilation errors) -> Phase 3 (semantic errors) -> Phase 4+ (readability)

---

### Pitfall 4: Refactoring Before Understanding Failure Modes

**What goes wrong:** Team sees 2,571-line expr.py module and immediately refactors it, breaking working code without understanding what was broken vs working.

**Why it happens:**
- Large modules feel like "tech debt" that must be fixed
- Refactoring is more comfortable than debugging
- Lack of systematic bug inventory - don't know what's actually broken
- Assumption that "cleaner code" will magically fix bugs

**Consequences:**
- Working code paths get broken during refactor
- Cannot isolate whether new bugs came from refactor or were pre-existing
- Refactor doesn't actually fix the decompiler bugs (just reorganizes them)
- Test coverage drops because refactored code has different structure

**Prevention:**
1. **Bug inventory first** - Systematically catalog what's broken before refactoring
2. **Test coverage baseline** - Measure coverage before refactor, maintain during refactor
3. **Refactor for purpose** - Only refactor modules that are blocking bug fixes
4. **Incremental refactoring** - Extract one pattern type at a time, validate after each
5. **Keep working code working** - If decompiler produces correct output for some patterns, don't break those

**Detection:**
- Warning sign: "Let's refactor expr.py" without knowing which bugs are in expr.py
- Warning sign: Refactoring PRs that don't fix any specific bug
- Warning sign: Test coverage drops after refactor
- Warning sign: New bugs appear after "cleanup" refactor

**Phase mapping:** Phase 1 should include bug inventory; refactoring should only happen when blocking specific bug fixes

---

### Pitfall 5: Trusting Bytecode Comparison Without Understanding Compiler Behavior

**What goes wrong:** Team sees bytecode differences and assumes decompiler is wrong, when actually the original compiler has non-deterministic behavior or multiple valid encodings.

**Why it happens:**
- Bytecode comparison is necessary but insufficient for validation
- Compilers have optimization variance (different register allocation, instruction ordering)
- Some bytecode differences are semantic (behavior changes), others are non-semantic (equivalent code)
- Without understanding compiler internals, cannot distinguish false positives from real bugs

**Consequences:**
- Wasting time "fixing" decompiler for compiler variance, not actual bugs
- False negatives - thinking code is correct because bytecode matches, missing semantic bugs
- Over-constraining decompiler to match specific compiler artifacts instead of valid C code
- Validation system with high false positive rate (team ignores warnings)

**Prevention:**
1. **Categorize differences** - Build taxonomy: semantic vs non-semantic, acceptable vs critical
2. **Study compiler internals** - Understand SCMP.exe optimization patterns, instruction selection
3. **Multiple validation approaches**:
   - Bytecode comparison (catches most issues)
   - Execution testing (catches semantic bugs bytecode comparison misses)
   - Manual inspection (catches readability/correctness bytecode can't verify)
4. **Accept non-semantic differences** - Register allocation changes are OK if behavior matches
5. **Differential fuzzing** - Test with different inputs to catch semantic divergence

**Prevention (continued):**
6. **Document known compiler quirks** - Track patterns where compiler has multiple valid outputs
7. **Validation confidence levels**:
   - HIGH: Perfect bytecode match
   - MEDIUM: Non-semantic differences only
   - LOW: Semantic differences in non-critical code paths
   - FAIL: Semantic differences affecting behavior

**Detection:**
- Warning sign: Every validation run shows "failures" but code seems to work
- Warning sign: Spending effort to match exact register allocation
- Warning sign: No documentation of what differences are acceptable
- Warning sign: Binary pass/fail validation with no nuance
- Warning sign: Validation failures increasing after fixes (false positive spiral)

**Phase mapping:** Phase 1 must include difference categorization; Phase 2 should track semantic vs non-semantic difference rates

---

## Moderate Pitfalls

Mistakes that cause delays or technical debt.

### Pitfall 6: Not Tracking Regression Baselines

**What goes wrong:** Team fixes Bug A, introduces Bug B, doesn't notice until weeks later when user reports it.

**Why it happens:**
- Decompiler changes have non-local effects (expression formatting affects control flow detection)
- Small test suite doesn't exercise affected code paths
- No "before/after" baseline to compare against
- Focus on fixing new bugs, not preventing regressions

**Consequences:**
- Bugs reappear after being "fixed"
- Cannot track true progress (1 fix + 2 regressions = -1 progress)
- Loss of trust in decompiler stability
- Firefighting mode - always fixing regressions instead of advancing

**Prevention:**
1. **Save validation baseline before every fix** - `validate-batch --save-baseline`
2. **Regression testing in CI** - `validate-batch --regression` fails if any script regresses
3. **Track metrics over time**:
   - Pass rate (how many scripts compile)
   - Semantic accuracy rate (how many match bytecode)
   - Coverage (lines of code tested)
4. **Git bisect for regressions** - When regression found, bisect to exact commit
5. **Require baseline in PRs** - "This PR fixes 3 scripts, regresses 0 scripts"

**Detection:**
- Warning sign: No historical record of which scripts passed before
- Warning sign: Discovering regressions weeks after they were introduced
- Warning sign: Cannot answer "Did this get better or worse?"
- Warning sign: No CI checks for regression prevention

---

### Pitfall 7: Ignoring Control Flow Reconstruction Complexity

**What goes wrong:** Team assumes if/else detection is "simple pattern matching," spends weeks debugging edge cases.

**Why it happens:**
- Control flow reconstruction is one of the hardest decompiler problems
- Compiler optimizations obscure original structure (loop unrolling, branch prediction)
- Jump tables, indirect branches, computed gotos create ambiguity
- Pattern matching approaches fail on 2-5% of code, falling back to goto spaghetti

**Consequences:**
- Underestimated effort for control flow fixes
- Fragile pattern detection that breaks on minor variations
- Decompiled code full of gotos (unreadable, hard to validate)
- Switch/case detection fails on jump table variants

**Prevention:**
1. **Study existing research** - "No More Gotos" (NDSS 2017), pattern-independent structuring
2. **Test on real optimized code** - Not just -O0, but -O2/-O3 with loop unrolling
3. **Robust CFG analysis** - Build dominance trees, identify natural loops properly
4. **Fallback strategies** - When pattern detection fails, emit structured goto (not raw goto mess)
5. **Incremental improvement** - Fix most common patterns first (90% of code), handle edge cases later

**Detection:**
- Warning sign: Assuming "just match if/else pattern" will work
- Warning sign: Pattern detection hardcoded to specific jump instruction sequences
- Warning sign: No testing on compiler-optimized code
- Warning sign: Goto statements appearing in decompiled output frequently

---

### Pitfall 8: Decompiling Without Original Source Examples

**What goes wrong:** Team works only with production .scr files (no source code), cannot verify if decompiler output is correct.

**Why it happens:**
- Production scripts only exist as bytecode
- Lack of ground truth makes validation impossible beyond "does it compile"
- Cannot verify if control flow reconstruction matches original intent
- No way to measure decompiler accuracy

**Consequences:**
- Cannot distinguish correct decompilation from plausible-but-wrong output
- Validation limited to "compiles" instead of "matches original"
- Accuracy measurement impossible
- Fixes may introduce semantic errors undetected

**Prevention:**
1. **Prioritize scripts with source** - Test on Compiler-testruns/* where original C exists
2. **Compare decompiled vs original** - Diff to identify decompiler weaknesses
3. **Use debug builds** - Scripts compiled with debug info reveal function boundaries, variable names
4. **Generate synthetic test cases** - Write C code covering edge cases, compile, decompile, compare
5. **Track accuracy metrics** - When source available, measure how many variables/types/structures match

**Detection:**
- Warning sign: Working only on production scripts without source
- Warning sign: No ground truth for validation
- Warning sign: Cannot measure decompiler accuracy objectively
- Warning sign: Validation only checks compilability, not correctness

---

### Pitfall 9: Expression Tree Refactoring Without Safety Net

**What goes wrong:** Team modifies expression formatting logic, breaks operator precedence, generates code like `a + b * c` instead of `(a + b) * c`, creating silent semantic bugs.

**Why it happens:**
- Expression trees are central to decompiler (every value flows through them)
- Precedence rules are subtle (12 precedence levels in C)
- Stack-based IR to expression tree conversion is error-prone
- Type inference interacts with expression formatting (IADD vs FADD)

**Consequences:**
- Generated code compiles but has wrong semantics
- Operator precedence bugs create subtle calculation errors
- Type confusion (int/float) causes incorrect conversions
- Bytecode validation might pass (compiler optimizes to same result) but source code is wrong

**Prevention:**
1. **Comprehensive precedence tests** - Test all 12 C precedence levels with all operators
2. **Roundtrip validation** - Compile decompiled code, verify bytecode matches
3. **Expression correctness suite** - Unit tests for expression formatting isolated from full decompiler
4. **Parenthesization module** - Separate module (already exists in codebase!) for precedence rules
5. **Type inference testing** - Verify int vs float operations generate correct types

**Detection:**
- Warning sign: Modifying expr.py without expression-specific tests
- Warning sign: No tests for operator precedence edge cases
- Warning sign: Parenthesization logic scattered throughout codebase
- Warning sign: Type casting appearing in unexpected places

---

### Pitfall 10: Not Understanding the Compiler Toolchain

**What goes wrong:** Team treats SCMP.exe as black box, cannot debug why recompiled code differs from original.

**Why it happens:**
- Compiler has multiple stages (preprocessor, compiler, assembler, linker)
- Each stage has quirks and limitations
- Header files define critical constants/macros that affect compilation
- Compiler bugs exist (even in original tools)

**Consequences:**
- Cannot diagnose validation failures
- Blaming decompiler for compiler limitations
- Missing opportunities to workaround compiler quirks
- Wasting time on unfixable differences

**Prevention:**
1. **Study compiler internals** - Read SCC_TECHNICAL_ANALYSIS.md, understand compilation stages
2. **Document compiler quirks** - Track known issues (dead code generation, optimization artifacts)
3. **Test compiler behavior** - Write minimal C programs to test edge cases
4. **Header file management** - Understand which headers define what constants
5. **Compiler version awareness** - Track if multiple SCMP.exe versions exist with different behavior

**Detection:**
- Warning sign: Every validation failure assumed to be decompiler bug
- Warning sign: No documentation of compiler limitations
- Warning sign: Treating compiler as "ground truth" without verification
- Warning sign: Not testing compiler behavior independently

---

## Minor Pitfalls

Mistakes that cause annoyance but are fixable.

### Pitfall 11: Over-Reliance on Automated Decompilation

**What goes wrong:** Team expects `vcdecomp structure` to output production-ready code automatically.

**Why it happens:**
- Decompilers marketed as "one-click" solutions
- Underestimating inherent decompilation limitations
- Unrealistic expectations from AI/LLM hype

**Consequences:**
- Disappointment when output needs manual cleanup
- Wasted effort trying to automate inherently manual tasks
- Ignoring tools that require human judgment

**Prevention:**
1. **Set realistic expectations** - Decompilation is reconstruction, not recovery
2. **Hybrid workflow** - Automated disassembly + manual analysis + assisted reconstruction
3. **Focus automation on tedious tasks** - Let tools handle formatting, not semantic understanding
4. **Leverage disassembly** - `vcdecomp disasm` is more reliable than `vcdecomp structure`

---

### Pitfall 12: Ignoring Data Segment Analysis

**What goes wrong:** Team focuses only on code, misses critical constant/string data that affects correctness.

**Why it happens:**
- Code is "interesting," data is "boring"
- Data segment analysis requires understanding alignment, endianness, type inference
- Global variable detection is heuristic-based (error-prone)

**Consequences:**
- Constants displayed incorrectly (int vs float confusion)
- String references broken
- Global variable accesses misidentified

**Prevention:**
1. **Validate data segment parsing** - Verify constants, strings match expected values
2. **Global variable analysis** - Map GADR data[X] references to meaningful names
3. **Type inference for constants** - Distinguish int vs float vs pointer
4. **Alignment awareness** - Data segment is 4-byte aligned, affects interpretation

---

### Pitfall 13: Not Documenting Decompiler Assumptions

**What goes wrong:** Decompiler makes assumptions (e.g., "all functions return dword"), assumptions violated in real code, no documentation of why.

**Why it happens:**
- Assumptions embedded in code, not documented
- Original developer knowledge lost
- Edge cases discovered later contradict assumptions

**Consequences:**
- Cannot debug why decompiler behaves unexpectedly
- Fixes based on wrong assumptions
- Confusion about intended vs actual behavior

**Prevention:**
1. **Document all heuristics** - "Why do we assume X?" should have written answer
2. **Track assumption violations** - When assumptions fail, document the case
3. **Make assumptions configurable** - Flags for aggressive vs conservative type inference
4. **Code comments for non-obvious logic** - Explain "why," not just "what"

---

### Pitfall 14: Skipping Disassembly Verification

**What goes wrong:** Team jumps straight to structured decompilation, misses that disassembly itself is wrong.

**Why it happens:**
- Structured output is the end goal
- Disassembly seems "boring" (just raw instructions)
- Assuming bytecode parsing is correct

**Consequences:**
- Bugs in instruction decoding propagate to all downstream analysis
- Wasting time debugging structure when real bug is in disassembler
- Cannot trust any decompiler output if disassembly is wrong

**Prevention:**
1. **Verify disassembly first** - Compare `vcdecomp disasm` against known-good scripts
2. **Opcode coverage** - Ensure all 150 opcodes are tested
3. **Instruction format validation** - Verify 12-byte instruction parsing
4. **XFN table parsing** - Validate external function references

---

### Pitfall 15: GUI Before CLI Stability

**What goes wrong:** Team builds GUI visualization before core decompiler works reliably.

**Why it happens:**
- GUI is impressive demo material
- Visual tools are satisfying to build
- Underestimating core decompiler complexity

**Consequences:**
- GUI displays incorrect data (garbage in, garbage out)
- Maintenance burden of GUI when core changes
- Users trust GUI output without validation

**Prevention:**
1. **CLI-first development** - Get `validate` command working before GUI
2. **GUI as visualization** - GUI displays validated output, not primary workflow
3. **Automated tests don't need GUI** - Can validate 200 scripts without clicking buttons

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Validation Infrastructure | Building incomplete validator that only checks compilation, not bytecode equivalence | Implement bytecode comparison + difference categorization from day 1 |
| Bug Identification | Working with only 3 test scripts, missing real-world bug patterns | Use batch validation on full corpus (200+ scripts) immediately |
| Control Flow Fixes | Underestimating if/else/switch complexity, fragile pattern matching | Study academic research, test on optimized code, build robust CFG analysis |
| Expression Formatting | Breaking operator precedence, type inference during refactoring | Use existing parenthesization module, comprehensive expression tests |
| Type Inference | Chasing perfect variable names/types before code compiles | Prioritize: compilability > semantic correctness > readability |
| Regression Prevention | No baseline tracking, regressions discovered weeks later | `validate-batch --save-baseline` before every fix, CI regression checks |
| Production Readiness | Celebrating "all 3 tests pass" when 197 other scripts fail | Track pass rate on full corpus, not just test suite |

---

## Meta-Warning: The Measurement Problem

**Critical insight from research:** State-of-the-art decompiler (Hex-Rays) has ~55% accuracy, contradicting belief among reverse engineers that decompilers are "usually accurate."

**Implication for this project:**
- **You cannot improve what you don't measure**
- Must track objective metrics:
  - Compilation success rate (X% of scripts compile)
  - Semantic accuracy rate (Y% of compiled scripts match bytecode)
  - Error type distribution (which bugs affect most scripts)
  - Coverage (Z% of bytecode patterns tested)
- Subjective assessment ("looks better") is insufficient
- Small test suite creates illusion of progress

**Prevention:**
1. Define success metrics upfront (e.g., "80% of scripts compile correctly")
2. Track metrics in every PR (before: 63% pass, after: 68% pass)
3. Maintain dashboard of progress over time
4. Distinguish:
   - Scripts that compile perfectly (bytecode matches)
   - Scripts that compile acceptably (semantic equivalent)
   - Scripts that compile with warnings (minor issues)
   - Scripts that fail compilation (broken)

---

## Sources

### High Confidence (Academic Research, 2024-2025)

- [Evaluating the Effectiveness of Decompilers](https://dl.acm.org/doi/10.1145/3650212.3652144) (ISSTA 2024) - Decompiler accuracy 55%, goto statement proliferation
- [Understanding and Finding Java Decompiler Bugs](https://dl.acm.org/doi/10.1145/3649860) (OOPSLA 2024) - Bug taxonomy, 69.7% bugs fixed in <100 LOC
- [D-LiFT: Improving LLM-based Decompiler Backend via Code Quality-driven Fine-tuning](https://arxiv.org/html/2506.10125v2) (2025) - Regression categorization, syntax vs semantic errors
- [BIN2WRONG: Systematic Correctness Testing of Decompilers](https://www.usenix.org/system/files/atc25-yang-zao.pdf) (USENIX ATC 2025) - Fuzzing limitations, manual bug discovery prevalence
- [DecompileBench: A Comprehensive Benchmark](https://arxiv.org/html/2505.11340v1) (ACL 2025) - 15 error types, evaluation framework
- [FuzzFlesh: Randomised Testing of Decompilers](http://www.doc.ic.ac.uk/~afd/papers/2025/ECOOP-FuzzFlesh.pdf) (ECOOP 2025) - CFG-based testing, switch/loop bugs
- [PyLingual: Perfect Decompilation Testing](https://kangkookjee.io/wp-content/uploads/2025/09/pylingual-blackhat24-1.pdf) (BlackHat 2024) - Bytecode matching validation

### Medium Confidence (Technical Blogs, Community Resources)

- [No More Gotos: Pattern-Independent Control-Flow Structuring](https://www.ndss-symposium.org/wp-content/uploads/2017/09/11_4_2.pdf) (NDSS 2017) - Control flow reconstruction
- [Recovering control flow structures without CFGs](https://purplesyringa.moe/blog/recovering-control-flow-structures-without-cfgs/) - Modern approaches
- [Ghidra Issue #3733](https://github.com/NationalSecurityAgency/ghidra/issues/3733) - Switch statement decompiler bugs
- [Ghidra Issue #1288](https://github.com/NationalSecurityAgency/ghidra/issues/1288) - Indirect switch statement failures
- [DIRTY: Augmenting Decompiler Output](https://www.usenix.org/conference/usenixsecurity22/presentation/chen-qibin) (USENIX Security 2022) - Variable naming/typing
- [Code Coverage Tool Analysis](https://github.com/matt-kempster/m2c) - Small test suite coverage approaches

### Project-Specific (VC_Scripter Codebase)

- `CLAUDE.md` - Project documentation, current challenges
- `vcdecomp/validation/validator.py` - Validation infrastructure design
- `vcdecomp/core/ir/expr.py` - 2,571-line expression module (tech debt example)
- `vcdecomp/tests/test_end_to_end_decompilation.py` - Current test suite scope
- `docs/decompilation_guide.md` - Known decompiler limitations
