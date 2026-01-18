# Phase 6: Expression Reconstruction Fixes - Research

**Researched:** 2026-01-18
**Domain:** C expression reconstruction from bytecode SSA IR with operator precedence
**Confidence:** HIGH

## Summary

Researched expression reconstruction in a decompiler context where stack-based bytecode instructions are converted to SSA IR, then formatted as C expressions. The domain involves operator precedence management, type inference from opcodes, and parenthesization rules to ensure syntactically valid C code.

Key findings:
- **Current implementation** uses `vcdecomp/core/ir/expr.py` (2400+ lines) for expression formatting with `parenthesization.py` providing precedence rules
- **Error patterns** from Phase 4 show syntax errors dominate compilation failures - many related to malformed expressions
- **Ground truth** exists in `Compiler-testruns/` - original C source files provide exact reference for correct expression syntax
- **Type inference** already implemented via opcode analysis (IADD vs FADD, ITOF casts) but may produce incorrect types
- **Operator precedence** handled by dedicated module with C standard precedence table, but not consistently applied

**Primary recommendation:** Fix expression bugs systematically using validation-driven debugging. Use error categorization from Phase 4 to prioritize fixes. Test each fix against known-good source files in Compiler-testruns/.

## Standard Stack

The established libraries/tools for expression reconstruction:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python AST | stdlib | Not used currently, but standard for expression trees | Could model expressions before rendering |
| Operator precedence table | Custom | C operator precedence from standard | Already implemented in parenthesization.py |
| SSA IR | Custom | Stack lifting to SSA form | Already implemented in vcdecomp/core/ir/ssa.py |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| difflib | stdlib | Compare decompiled vs original expressions | Debugging expression differences |
| Validation system | Existing | SCMP.exe recompilation | Already integrated - use for every fix |
| Error analyzer | Existing (Phase 4) | Categorize syntax errors | Prioritize which expression bugs to fix first |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| String concatenation | AST-based code generation | More complexity, not needed for simple C |
| Manual precedence | Parser generator (PLY, lark) | Over-engineering - C precedence is fixed |
| Ad-hoc testing | Property-based testing (Hypothesis) | Could generate edge cases, but validation system sufficient |

**Installation:**
No new dependencies required - all tools already in project.

## Architecture Patterns

### Recommended Project Structure
```
vcdecomp/core/ir/
├── expr.py                    # Expression formatting (EXISTING - 2400+ lines)
│   ├── ExpressionFormatter    # Main class with expression rendering
│   ├── _render_value()        # Convert SSAValue to string
│   ├── _inline_expression()   # Inline simple expressions
│   ├── _format_binary()       # Binary operator formatting
│   └── _format_unary()        # Unary operator formatting
├── parenthesization.py        # Operator precedence (EXISTING - 315 lines)
│   ├── OPERATOR_PRECEDENCE    # C precedence table
│   ├── needs_parens()         # Determine if parens needed
│   └── wrap_if_needed()       # Add parens conditionally
├── ssa.py                     # SSA IR construction (EXISTING)
└── stack_lifter.py            # Bytecode → SSA (EXISTING)
```

### Pattern 1: Expression Rendering Pipeline
**What:** Convert SSA instruction tree to C expression string with correct precedence
**When to use:** All expression formatting in decompiler
**Example:**
```python
# Source: vcdecomp/core/ir/expr.py (lines 922-1073)
def _render_value(self, value: SSAValue, expected_type_str: str = None,
                  context: ExpressionContext = ExpressionContext.IN_EXPRESSION,
                  parent_operator: Optional[str] = None) -> str:
    # Priority order for rendering:
    # 1. Struct field access (highest - preserves semantic meaning)
    # 2. Variable rename map (for collision resolution)
    # 3. String literals from data segment
    # 4. Function parameters (by stack offset)
    # 5. PHI node resolution (multiple inputs → single value)
    # 6. Array indexing patterns
    # 7. Global variable names
    # 8. Float literal detection
    # 9. Struct field from local variable
    # 10. Semantic names (loop counters, etc.)
    # 11. Data segment literals (last resort)

    # Check field expression first
    field_expr = self._field_tracker.get_field_expression(value)
    if field_expr:
        return field_expr

    # Check rename map for collision resolution
    if self._rename_map and value.name in self._rename_map:
        return self._rename_map[value.name]

    # ... (continue with other checks)

    # Finally, inline if possible
    if self._can_inline(value):
        return self._inline_expression(value, context, parent_operator)
    return value.name
```

### Pattern 2: Operator Precedence Management
**What:** Use precedence table to determine when parentheses are required
**When to use:** Building binary/unary expressions, nested expressions
**Example:**
```python
# Source: vcdecomp/core/ir/parenthesization.py (lines 228-298)
def needs_parens(child_expr: str, child_operator: Optional[str],
                 parent_operator: Optional[str], context: ExpressionContext,
                 is_left_operand: bool = True) -> bool:
    """
    Determine if child expression needs parentheses in parent context.

    Examples:
        (a + b) * c  → parens needed (lower precedence in higher)
        a * (b + c)  → parens needed (right operand of same precedence)
        a + b + c    → no parens (left-associative)
        a = b = c    → (a = b) = c wrong, a = (b = c) correct (right-associative)
    """
    # Simple expressions never need parens
    if is_simple_expression(child_expr):
        return False

    # Get operator info
    child_info = get_operator_info(child_operator)
    parent_info = get_operator_info(parent_operator)

    # Higher precedence = tighter binding = fewer parens needed
    if child_info.precedence < parent_info.precedence:
        return False  # Child binds tighter, no parens

    if child_info.precedence > parent_info.precedence:
        return True   # Parent binds tighter, needs parens

    # Same precedence - check associativity
    if child_info.precedence == parent_info.precedence:
        if parent_info.associativity == Associativity.LEFT:
            return not is_left_operand  # Right needs parens
        elif parent_info.associativity == Associativity.RIGHT:
            return is_left_operand      # Left needs parens

    return False
```

### Pattern 3: Type-Aware Expression Formatting
**What:** Use opcode types to generate correct C type casts and literals
**When to use:** Float literals, type conversions, function arguments
**Example:**
```python
# Source: vcdecomp/core/ir/expr.py (lines 36-101, 1032-1038)
def _is_likely_float(val: int) -> bool:
    """Detect if integer value is actually IEEE 754 float constant."""
    if val == 0 or 0 < val < 1000:
        return False  # Small integers are ints, not floats

    try:
        f = struct.unpack('<f', struct.pack('<I', val & 0xFFFFFFFF))[0]

        # Reject NaN, Inf, extreme values
        if math.isnan(f) or math.isinf(f) or abs(f) > 1e6:
            return False

        # Accept whole numbers and common decimals (0.5, 0.25, 1.5)
        if f == int(f) or round(f, 2) in {0.5, 0.25, 0.75, 1.5, 2.5}:
            return True
    except (struct.error, OverflowError):
        return False

    return False

# Usage in rendering
if expected_type_str and 'float' in expected_type_str.lower():
    return _format_float(val)
if _is_likely_float(val):
    return _format_float(val)
```

### Anti-Patterns to Avoid
- **Over-parenthesization:** Don't add parens everywhere "to be safe" - violates C readability conventions
- **Ignoring operator precedence:** Leads to semantic bugs like `a + b * c` becoming `(a + b) * c`
- **Type guessing from context alone:** Use opcode types (IADD vs FADD) as primary source of truth
- **Mixing inlining and non-inlining unpredictably:** Establish clear rules for when to inline expressions
- **String concatenation without escaping:** String literals must escape `\n`, `\t`, `"`, etc.

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Operator precedence table | Manual precedence values | C standard precedence reference | Already codified in parenthesization.py, matches C spec |
| Expression tree traversal | Recursive string building | Existing SSA IR with producer/consumer links | Already implemented, tested, handles cycles |
| Type inference | Pattern matching on usage | Opcode-based type detection (IADD=int, FADD=float) | Compiler already encodes types in opcodes |
| String escaping | Manual replace() calls | Existing _escape_string() method | Handles all C escape sequences correctly |
| Float literal detection | Regex or simple heuristics | IEEE 754 struct unpacking | Already implemented, handles edge cases |

**Key insight:** Expression reconstruction is not a greenfield problem - 90% already implemented. Phase 6 fixes bugs in existing implementation, not rewrite.

## Common Pitfalls

### Pitfall 1: Incorrect Operator Precedence
**What goes wrong:** Expression `a + b * c` decompiles as `(a + b) * c` changing semantics
**Why it happens:** Bytecode is stack-based, order of operations not explicit. SSA IR may not preserve precedence hints.
**How to avoid:**
- Always consult OPERATOR_PRECEDENCE table in parenthesization.py
- Test precedence with known expressions from Compiler-testruns/
- Use needs_parens() function, don't manually add parentheses
**Warning signs:** Validation shows bytecode differences in arithmetic operations

### Pitfall 2: Type Confusion (Int vs Float)
**What goes wrong:** `1.0f` renders as `1`, causing type mismatch in function calls
**Why it happens:** Stack slots hold raw 32-bit values. Type lost unless inferred from opcode.
**How to avoid:**
- Check opcode: FADD/FSUB/FMUL → float, IADD/ISUB/IMUL → int
- Use expected_type_str from function signatures (XFN table has types)
- Call _is_likely_float() for data segment constants
**Warning signs:** Compiler errors like "incompatible types: expected float, got int"

### Pitfall 3: Over-Inlining Complex Expressions
**What goes wrong:** Single statement becomes unreadable: `x = ((a + b) * (c - d)) / ((e + f) * (g - h));`
**Why it happens:** _can_inline() allows inlining of multi-use values if "simple enough"
**How to avoid:**
- Limit inlining depth (track nesting level in _inline_expression)
- Don't inline if expression exceeds 80 characters
- Preserve intermediate variables for complex expressions
**Warning signs:** Decompiled code harder to read than necessary, long lines

### Pitfall 4: Missing Type Casts
**What goes wrong:** `int x = SC_FloatFunction();` compiles but has wrong semantics
**Why it happens:** SCMP.exe compiler sometimes allows implicit conversions, but semantics differ
**How to avoid:**
- Emit explicit casts when opcode shows conversion: ITOF → (float), FTOI → (int)
- Check function return types from XFN table
- Test bytecode equivalence, not just compilation success
**Warning signs:** Validation shows semantic differences (non-matching bytecode) despite compiling

### Pitfall 5: Parenthesization in Conditions
**What goes wrong:** `if (a && b || c)` parsed as `if (a && (b || c))` instead of `if ((a && b) || c)`
**Why it happens:** Condition context has different precedence rules than expressions
**How to avoid:**
- Use ExpressionContext.IN_CONDITION when rendering condition expressions
- Check needs_parens_in_condition() separately from general needs_parens()
- Test with original switch/case statements (jump table conditions)
**Warning signs:** Control flow differs between original and decompiled (wrong branches taken)

## Code Examples

Verified patterns from existing codebase:

### Binary Expression Formatting
```python
# Source: vcdecomp/core/ir/expr.py (lines 2301-2311)
def _format_binary(self, inst: SSAInstruction, operator: str) -> str:
    """
    Format binary operator instruction with correct precedence.

    Example:
        ADD instruction: inputs=[a, b], output=c
        Renders as: c = a + b;
    """
    if len(inst.inputs) != 2 or not inst.outputs:
        return self._format_call(inst)

    lhs, rhs = inst.inputs
    dst = self._format_target(inst.outputs[0])

    # NOTE: Parenthesization should be handled in _render_value()
    # with parent_operator parameter, not here
    return f"{dst} = {self._render_value(lhs)} {operator} {self._render_value(rhs)};"
```

### Unary Expression Formatting
```python
# Source: vcdecomp/core/ir/expr.py (lines 2313-2318)
def _format_unary(self, inst: SSAInstruction, prefix: str) -> str:
    """
    Format unary operator instruction.

    Example:
        NEG instruction: input=a, output=b
        Renders as: b = -a;
    """
    if len(inst.inputs) != 1 or not inst.outputs:
        return self._format_call(inst)

    operand = inst.inputs[0]
    dst = self._format_target(inst.outputs[0])

    return f"{dst} = {prefix}{self._render_value(operand)};"
```

### Type Cast Insertion
```python
# Source: vcdecomp/core/ir/expr.py (inferred from CAST_OPS at line 196)
# Pattern for type conversion instructions

CAST_OPS = {"ITOF", "FTOI", "ITOD", "DTOI", "DTOF", "FTOD", "SCI", "SSI", "UCI", "USI"}

def _format_cast(self, inst: SSAInstruction) -> str:
    """
    Format type cast instruction explicitly.

    Examples:
        ITOF: int → float
        FTOI: float → int
        ITOD: int → double
    """
    if inst.mnemonic == "ITOF":
        return f"{dst} = (float){self._render_value(operand)};"
    elif inst.mnemonic == "FTOI":
        return f"{dst} = (int){self._render_value(operand)};"
    # ... etc
```

### Operator Precedence Lookup
```python
# Source: vcdecomp/core/ir/parenthesization.py (lines 45-124)
# C Operator Precedence Table (from C standard)

OPERATOR_PRECEDENCE = {
    # Precedence 1 (highest) - Postfix
    '[]': OperatorInfo(1, Associativity.LEFT, 2),
    '.': OperatorInfo(1, Associativity.LEFT, 2),
    '->': OperatorInfo(1, Associativity.LEFT, 2),

    # Precedence 2 - Unary prefix
    '!': OperatorInfo(2, Associativity.RIGHT, 1, is_logical=True),
    '~': OperatorInfo(2, Associativity.RIGHT, 1),
    '-unary': OperatorInfo(2, Associativity.RIGHT, 1),
    '&addr': OperatorInfo(2, Associativity.RIGHT, 1),

    # Precedence 4 - Multiplicative
    '*': OperatorInfo(4, Associativity.LEFT, 2, is_arithmetic=True),
    '/': OperatorInfo(4, Associativity.LEFT, 2, is_arithmetic=True),
    '%': OperatorInfo(4, Associativity.LEFT, 2, is_arithmetic=True),

    # Precedence 5 - Additive
    '+': OperatorInfo(5, Associativity.LEFT, 2, is_arithmetic=True),
    '-': OperatorInfo(5, Associativity.LEFT, 2, is_arithmetic=True),

    # Precedence 7 - Relational
    '<': OperatorInfo(7, Associativity.LEFT, 2, is_comparison=True),
    '<=': OperatorInfo(7, Associativity.LEFT, 2, is_comparison=True),

    # Precedence 8 - Equality
    '==': OperatorInfo(8, Associativity.LEFT, 2, is_comparison=True),
    '!=': OperatorInfo(8, Associativity.LEFT, 2, is_comparison=True),

    # Precedence 12 - Logical AND
    '&&': OperatorInfo(12, Associativity.LEFT, 2, is_logical=True),

    # Precedence 13 - Logical OR
    '||': OperatorInfo(13, Associativity.LEFT, 2, is_logical=True),

    # Precedence 15 - Assignment (lowest precedence)
    '=': OperatorInfo(15, Associativity.RIGHT, 2),
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| No parenthesization module | Dedicated parenthesization.py with C precedence table | Unknown (pre-project) | Correct precedence handling |
| Manual type guessing | Opcode-based type inference (IADD=int, FADD=float) | Pre-project | Mostly correct types |
| No float literal detection | IEEE 754 unpacking with heuristics | Pre-project | Correct float constants |
| No validation | SCMP.exe recompilation and bytecode comparison | Phase 1-3 (2026-01-18) | Systematic bug detection |
| Manual error inspection | Error categorization and pattern detection | Phase 4 (2026-01-18) | Prioritized fixes |

**Deprecated/outdated:**
- String concatenation without precedence checks: Now uses needs_parens()
- Type-agnostic rendering: Now uses expected_type_str and opcode types
- Inline everything approach: Now has _can_inline() heuristics

## Open Questions

1. **Should complex expressions be broken into multiple statements?**
   - What we know: Current implementation inlines aggressively (up to 10 uses for some ops)
   - What's unclear: Readability vs compilability tradeoff - does over-inlining cause compiler errors?
   - Recommendation: Measure in validation - if no compilation errors, prioritize correctness over readability for now

2. **How to handle ambiguous type situations (int vs float from data segment)?**
   - What we know: _is_likely_float() uses heuristics (0.5, 1.0, etc. are floats)
   - What's unclear: Edge cases like value=1072693248 (1.0f in IEEE 754) but looks like int
   - Recommendation: Use expected_type_str from XFN signatures as ground truth when available. Add test cases for ambiguous values.

3. **Should parenthesization be conservative or minimal?**
   - What we know: needs_parens() follows C standard strictly
   - What's unclear: Does SCMP.exe accept all valid C precedence, or does it have quirks?
   - Recommendation: Start minimal (follow C standard), add conservative parens only if validation fails

4. **How to handle floating point precision in literals?**
   - What we know: _format_float() rounds to 4 decimal places
   - What's unclear: Does this cause precision loss that affects bytecode equivalence?
   - Recommendation: Test with validation - if bytecode matches, precision is sufficient

## Sources

### Primary (HIGH confidence)
- Existing codebase analysis:
  - `vcdecomp/core/ir/expr.py` - 2400+ lines of expression formatting logic
  - `vcdecomp/core/ir/parenthesization.py` - C operator precedence table and precedence checking
  - `vcdecomp/core/ir/ssa.py` - SSA IR construction from bytecode
  - `vcdecomp/validation/error_analyzer.py` - Error categorization (Phase 4)
- Ground truth reference:
  - `Compiler-testruns/Testrun*/` - Original C source files for known scripts
  - `original-resources/h/sc_global.h` - Function signatures with parameter types
- C language specification:
  - https://en.cppreference.com/w/c/language/operator_precedence (referenced in parenthesization.py)

### Secondary (MEDIUM confidence)
- SCMP.exe compiler behavior (observed):
  - Accepts standard C precedence
  - Type inference from opcodes matches compiler's internal representation
  - Validation system (Phases 1-3) confirms bytecode equivalence testing works
- IEEE 754 floating point:
  - Standard representation for float constants in data segment
  - Python struct module for encoding/decoding

### Tertiary (LOW confidence)
- Decompiler design patterns (general, not VC-specific):
  - Expression tree construction before rendering
  - AST-based code generation (not used in this project, string-based instead)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All tools already in codebase, no external dependencies
- Architecture: HIGH - Patterns extracted directly from working code
- Pitfalls: MEDIUM - Based on common decompiler issues, not all project-specific

**Research date:** 2026-01-18
**Valid until:** 30 days (stable domain - C expression syntax doesn't change, implementation is mature)

---

## Key Takeaways for Planning

1. **Expression reconstruction is 90% implemented** - Phase 6 fixes bugs, not rewrites. Focus on validation-driven debugging.

2. **Ground truth exists** - Use Compiler-testruns/ original C files to verify correct expression syntax. Every fix should compile and match bytecode.

3. **Error categorization guides priorities** - Phase 4's error analyzer shows which expression bugs are most common. Start with highest-frequency errors.

4. **Type inference is mostly correct** - Opcode-based typing (IADD vs FADD) works. Fix edge cases in float literal detection and expected_type_str usage.

5. **Parenthesization module is solid** - Don't reinvent operator precedence. Use needs_parens() correctly with parent_operator parameter.

6. **Validation is the test oracle** - Every expression fix must pass validation (compile + bytecode match). No manual inspection needed.

7. **Systematic approach beats ad-hoc fixes** - Categorize errors, fix one category at a time, run validation suite after each fix.
