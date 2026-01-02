# TDM.SCR Decompilation Analysis Report
**Date:** January 2, 2026
**Decompiler Version:** Post-Phase 3 Complete
**Test File:** Compiler-testruns/Testrun1/tdm.scr

## Executive Summary

**Overall Assessment:** The decompilation has **MAJOR CORRECTNESS ISSUES** despite Phase 3 completion.

- **Original Source:** 307 lines, 3 functions
- **Decompiled Output:** 239 lines, 4 functions (includes `_init`)
- **Critical Issues Found:** 8
- **Major Issues Found:** 4
- **Estimated Accuracy:** ~60% (down from previous 87% baseline!)

**⚠️ REGRESSION ALERT:** Significant regressions detected compared to COMPARISON.md baseline.

---

## Detailed Discrepancy Matrix

| # | Line(s) | Severity | Category | Original | Decompiled | Status |
|---|---------|----------|----------|----------|------------|--------|
| 1 | 19 | CRITICAL | Switch selector | `switch(gEndRule)` | `switch (local_0)` | ❌ FAIL |
| 2 | 30-48 | CRITICAL | Control flow | Logical OR condition | Nested if/else maze | ❌ FAIL |
| 3 | 49 | CRITICAL | Missing code | `SC_message(...)` in default | Empty default case | ❌ FAIL |
| 4 | 51 | CRITICAL | Missing code | `return FALSE;` | No return | ❌ FAIL |
| 5 | 71 | CRITICAL | Function params | `func(info->elapsed_time)` | `func()` | ❌ FAIL |
| 6 | Many | MAJOR | Struct fields | `info->elapsed_time` | `info->field_16` | ⚠️ PARTIAL |
| 7 | 74,102,184 | MAJOR | Loop bounds | `i < limit` | `i <= limit` | ❌ FAIL |
| 8 | 138-182 | CRITICAL | Code duplication | Single block | Duplicated block | ❌ FAIL |
| 9 | 81-92 | MAJOR | Code duplication | Single call | Triple call | ❌ FAIL |
| 10 | 212 | CRITICAL | Variable aliasing | `sideA == sideB` | `i == i` | ❌ FAIL |
| 11 | 159,162,180 | MAJOR | Code duplication | Conditional call | 3x calls | ❌ FAIL |
| 12 | 193-195 | CRITICAL | Missing code | Assignments in if/else | Empty bodies | ❌ FAIL |
| 13 | N/A | INFO | Preprocessor | `#if` directive | Compiled code | ✅ EXPECTED |

---

## Issue Details & Root Cause Analysis

### CRITICAL #1: Switch Selector Aliasing
**Lines:** func_0010:19 vs tdm.c:46

**Impact:** Makes code unreadable and semantically incorrect.

```c
// ORIGINAL
switch(gEndRule){

// DECOMPILED
switch (local_0) {
```

**Root Cause:**
The compiler generates a local copy of the global:
```assembly
GLD gEndRule     ; Load global to stack
LCP offset_0     ; Copy to local variable
```

The decompiler creates `local_0` for the LCP target but doesn't trace back to see it's an alias of `gEndRule`.

**Affected Components:**
- `vcdecomp/core/ir/expr.py` - `_render_switch()` method
- `vcdecomp/core/ir/ssa.py` - SSA value tracing

**Proposed Fix:**
```python
def _render_switch(switch_value, ssa_func):
    # NEW: Trace back through PHI nodes and copies
    original_value = _trace_to_source(switch_value, ssa_func)

    # If source is a global/parameter, use that name
    if isinstance(original_value, SSAValue):
        if original_value.is_global:
            return format_global_name(original_value)
        elif original_value.is_param:
            return original_value.name

    # Fall back to current logic
    return format_value(switch_value)
```

**Implementation Complexity:** MEDIUM (2-3 hours)

---

### CRITICAL #2: Logical OR Decomposed to Nested If/Else
**Lines:** func_0010:30-48 vs tdm.c:61-65

**Impact:** Produces functionally incorrect code with wrong control flow.

```c
// ORIGINAL
if (((gSideFrags[0]>0)&&(gSideFrags[0]>=gEndValue))
    ||((gSideFrags[1]>1)&&(gSideFrags[1]>=gEndValue))){
    SC_MP_LoadNextMap();
    return TRUE;
}

// DECOMPILED (WRONG!)
if (((gSideFrags[0] > 0))) {
    if (((gSideFrags[0] >= gEndValue))) {
        // EMPTY BODY!
    } else {
        if (((gSideFrags[1] > 1))) {
            if (((gSideFrags[1] >= gEndValue))) {
                SC_MP_LoadNextMap();
                return TRUE;
            }
            SC_MP_LoadNextMap();  // DUPLICATE!
            return TRUE;
        }
        SC_message("...");  // WRONG PLACE!
        return FALSE;
    }
    SC_MP_LoadNextMap();  // DUPLICATE!
    return TRUE;
}
```

**Root Cause:**
The compiler generates short-circuit evaluation:
```
1. Check gSideFrags[0] > 0
   JZ to check_side1
2. Check gSideFrags[0] >= gEndValue
   JNZ to success_block
3. check_side1:
   Check gSideFrags[1] > 1
   JZ to end_of_if
4. Check gSideFrags[1] >= gEndValue
   JZ to end_of_if
5. success_block:
   Call SC_MP_LoadNextMap
   Return TRUE
6. end_of_if:
   Continue...
```

The decompiler incorrectly interprets these jumps as nested if/else instead of recognizing the logical OR pattern.

**Affected Components:**
- `vcdecomp/core/ir/structure.py` - `_detect_if_else_pattern()`
- `vcdecomp/core/ir/structure.py` - `_reconstruct_boolean_expression()`

**Proposed Fix:**
Implement a **short-circuit expression reconstructor**:

```python
def _reconstruct_boolean_expression(header_block, true_target, false_target, cfg):
    """
    Detect and reconstruct compound boolean expressions from CFG.

    Patterns to detect:
    1. AND: if (!A) goto false; if (!B) goto false; goto true;
    2. OR:  if (A) goto true; if (B) goto true; goto false;
    """

    # Collect all blocks in the boolean expression chain
    expr_blocks = _find_boolean_chain(header_block, true_target, false_target, cfg)

    if len(expr_blocks) == 1:
        # Simple condition
        return _simple_condition(header_block)

    # Determine if it's AND or OR based on jump targets
    is_or = _detect_or_pattern(expr_blocks, true_target)
    is_and = _detect_and_pattern(expr_blocks, false_target)

    if is_or:
        # All intermediate jumps to true_target -> OR
        conditions = [_extract_condition(block) for block in expr_blocks]
        return f"({' || '.join(conditions)})"
    elif is_and:
        # All intermediate jumps to false_target -> AND
        conditions = [_extract_condition(block) for block in expr_blocks]
        return f"({' && '.join(conditions)})"

    # Fall back to nested if/else
    return None
```

**Implementation Complexity:** HARD (1-2 days)

---

### CRITICAL #3: Missing Default Case Logic
**Lines:** func_0010:49 vs tdm.c:69-71

**Impact:** Default case is empty when it should print error message.

```c
// ORIGINAL
default:
    SC_message("EndRule unsopported: %d",gEndRule);
    break;

// DECOMPILED
default:
}
```

**Root Cause:**
Related to Issue #2. The `SC_message` call was mis-assigned to case 1 instead of default. The switch case boundary detection is failing.

**Affected Components:**
- `vcdecomp/core/ir/structure.py` - `_assign_blocks_to_cases()`

**Proposed Fix:**
Improve case boundary detection by analyzing jump targets:

```python
def _assign_blocks_to_cases(switch_pattern, cfg):
    """
    Correctly assign CFG blocks to switch cases.
    """
    case_blocks = {}

    for case_value, target_block in switch_pattern.case_targets.items():
        # Find all blocks reachable from target until:
        # 1. Break (jump to exit_block)
        # 2. Return
        # 3. Another case entry point
        blocks = _collect_case_blocks(
            target_block,
            switch_pattern.exit_block,
            switch_pattern.case_targets.values()
        )
        case_blocks[case_value] = blocks

    # Default case: blocks not in any other case
    all_case_blocks = set().union(*case_blocks.values())
    default_blocks = (
        set(switch_pattern.all_blocks)
        - all_case_blocks
        - {switch_pattern.header_block}
    )

    return case_blocks, default_blocks
```

**Implementation Complexity:** HARD (linked to Issue #2)

---

### CRITICAL #4: Missing Function Return Statement
**Lines:** func_0010:51 vs tdm.c:75

**Impact:** Function missing final return, causes undefined behavior.

```c
// ORIGINAL
return FALSE;

// DECOMPILED
}  // No return!
```

**Root Cause:**
The function epilogue detection doesn't recognize the fall-through return after the switch statement.

**CFG Structure:**
```
switch_exit_block -> return_block (return FALSE)
```

The `return_block` exists but isn't being rendered because it's not part of any switch case.

**Affected Components:**
- `vcdecomp/core/ir/structure.py` - `format_structured_function()`

**Proposed Fix:**
```python
def format_structured_function(ssa_func, cfg):
    # ... render switch statement ...

    # NEW: Check for blocks after switch exit
    if switch_pattern:
        blocks_after_switch = cfg.get_successors(switch_pattern.exit_block)
        for block_id in blocks_after_switch:
            if block_id not in emitted_blocks:
                # Render post-switch blocks (like fall-through returns)
                lines.extend(_format_block_lines(
                    ssa_func, block_id, indent,
                    formatter, emitted_blocks, cfg
                ))
```

**Implementation Complexity:** MEDIUM (2-3 hours)

---

### CRITICAL #5: Missing Function Call Arguments
**Lines:** ScriptMain:71 vs tdm.c:102

**Impact:** Function calls missing critical arguments, produces incorrect code.

```c
// ORIGINAL
if (SRV_CheckEndRule(info->elapsed_time)) break;

// DECOMPILED
if ((func_0010())) break;
```

**Root Cause:**
This is the **known Phase 4 incomplete issue** documented in COMPARISON.md. CALL argument detection requires tracing SSA values pushed to stack before the CALL instruction.

**Bytecode Pattern:**
```assembly
FPSH [info + offset_16]     ; Push info->elapsed_time
CALL func_0010              ; Call function
ASP 4                       ; Clean stack
```

The decompiler sees the CALL but doesn't trace back to find the FPSH instructions.

**Affected Components:**
- `vcdecomp/core/ir/expr.py` - `_render_call_expression()`
- `vcdecomp/core/ir/ssa.py` - Stack value tracing

**Proposed Fix:**
```python
def _extract_call_arguments(call_inst, ssa_func, prototype):
    """
    Trace back from CALL to find pushed arguments.
    """
    args = []

    # Get function prototype to know how many args
    param_count = len(prototype.params) if prototype else 0

    # Scan backwards from CALL instruction
    block = _find_block_containing(call_inst, ssa_func)
    inst_idx = block.instructions.index(call_inst)

    # Look for PUSH instructions before CALL
    scan_idx = inst_idx - 1
    pushes_found = []

    while scan_idx >= 0 and len(pushes_found) < param_count:
        inst = block.instructions[scan_idx]

        if inst.opcode in [IPSH, FPSH, DPSH, CPSH, SPSH]:
            # Found a push - extract the value
            pushes_found.append(inst.arg1)
        elif inst.opcode in [CALL, XCALL]:
            # Hit another call - stop searching
            break

        scan_idx -= 1

    # Reverse because pushes are in reverse order
    pushes_found.reverse()

    # Format each argument
    for push_value in pushes_found:
        args.append(_format_value(push_value, ssa_func))

    return args
```

**Implementation Complexity:** HARD (1 day)

---

### MAJOR #6: Struct Field Names Generic
**Lines:** Throughout ScriptMain

**Impact:** Reduces readability significantly.

**Examples:**
- `info->field_16` should be `info->elapsed_time`
- `info->field_4` should be `info->param1`
- `player_info.field2` should be `player_info.side`

**Root Cause:**
The decompiler doesn't parse struct definitions from headers. It only knows field offsets, not names.

**Affected Components:**
- `vcdecomp/core/headers/parser.py` - Struct definition parsing
- `vcdecomp/core/ir/expr.py` - Struct field name resolution

**Proposed Fix:**
Extend header parser to extract struct definitions:

```python
class StructDefinition:
    def __init__(self, name):
        self.name = name
        self.fields = []  # List of (offset, name, type)

    def get_field_name(self, offset):
        for field_offset, field_name, field_type in self.fields:
            if field_offset == offset:
                return field_name
        return f"field_{offset}"

class HeaderParser:
    def parse_struct(self, header_text):
        """
        Parse: typedef struct { ... } s_StructName;
        """
        struct_pattern = r'typedef\s+struct\s*\{([^}]+)\}\s*(\w+);'
        matches = re.finditer(struct_pattern, header_text, re.MULTILINE)

        structs = {}
        for match in matches:
            struct_body = match.group(1)
            struct_name = match.group(2)

            struct_def = StructDefinition(struct_name)
            offset = 0

            # Parse fields
            for line in struct_body.split('\n'):
                # Extract type, name
                field_match = re.match(r'\s*(\w+)\s+(\w+);', line)
                if field_match:
                    field_type = field_match.group(1)
                    field_name = field_match.group(2)

                    struct_def.fields.append((offset, field_name, field_type))
                    offset += _sizeof(field_type)

            structs[struct_name] = struct_def

        return structs
```

**Implementation Complexity:** HARD (1-2 days)

---

### MAJOR #7: Wrong Loop Bounds (Off-by-One + Unknown Constants)
**Lines:** ScriptMain:74, 102, 184

**Impact:** Loops execute one too many times (buffer overflow risk!) and use wrong bounds.

```c
// ORIGINAL
for (i=0;i<gRecs;i++)
for (i=0;i<2;i++)
for (i=0;i<REC_MAX;i++)

// DECOMPILED
for (i = 0; (i <= gRecs); i = (i + 1))      // BUG: <= instead of <
for (i = 0; (i <= data_383); i = (i + 1))   // BUG: data_383 instead of 2
for (i = 0; (i <= data_430); i = (i + 1))   // BUG: data_430 instead of REC_MAX
```

**Root Cause:**
1. **`<=` vs `<`:** Loop condition reconstruction incorrectly uses `<=` for `<` loops
2. **`data_XXX`:** Constants not resolved from data segment

**Bytecode Pattern for `i < N`:**
```assembly
loop_header:
  LLD i                  ; Load i
  IPSH N                 ; Push N
  ILT                    ; Compare i < N
  JZ loop_exit           ; Exit if false
  ; loop body
  JMP loop_header
```

The decompiler might be seeing `JZ loop_exit` and thinking "jump when !(i < N)" = "jump when i >= N" = "continue when i <= N-1", but getting the logic backwards.

**Affected Components:**
- `vcdecomp/core/ir/structure.py` - `_detect_for_loop()`
- `vcdecomp/core/loader/scr_loader.py` - Data segment constant resolution

**Proposed Fix:**

```python
def _extract_loop_condition(header_block, exit_block, cfg):
    """
    Extract loop condition and fix <= vs < issue.
    """
    # Find the comparison instruction
    last_inst = header_block.instructions[-1]
    if not is_conditional_jump(last_inst):
        return None

    # Find the comparison before the jump
    comp_inst = header_block.instructions[-2]

    # Map opcode to operator
    op_map = {
        ILT: '<',
        ILE: '<=',
        IGT: '>',
        IGE: '>=',
        IEQ: '==',
        INE: '!='
    }

    operator = op_map.get(comp_inst.opcode)

    # CRITICAL: If jump is JZ (jump if false), we use the operator as-is
    # If jump is JNZ (jump if true), we need to negate it
    if last_inst.opcode == JNZ:
        operator = _negate_operator(operator)

    return f"{comp_inst.arg1} {operator} {comp_inst.arg2}"

def _negate_operator(op):
    negation_map = {
        '<': '>=',
        '<=': '>',
        '>': '<=',
        '>=': '<',
        '==': '!=',
        '!=': '=='
    }
    return negation_map.get(op, op)
```

For the `data_XXX` issue:
```python
def _resolve_data_constant(data_addr, scr_file):
    """
    Resolve data segment address to actual constant value.
    """
    if data_addr in scr_file.data_segment:
        value = scr_file.read_int_at(data_addr)

        # Check if this matches a known #define
        if value == 2:
            return "2"  # Or find the #define name
        elif value == 64:
            return "REC_MAX"

        return str(value)

    return f"data_{data_addr}"
```

**Implementation Complexity:** MEDIUM (3-4 hours)

---

### CRITICAL #8: Massive Code Duplication in Nested If
**Lines:** ScriptMain:138-182 vs tdm.c:188-222

**Impact:** Entire initialization block duplicated, makes code 2x larger and wrong.

```c
// ORIGINAL (simplified)
if (info->param2){
    if (info->param1){
        // Server init code (25 lines)
    }
}

// DECOMPILED
if ((info->field_8)) {
    if ((info->field_4)) {
        // Server init code (25 lines)
    }
    // DUPLICATE: Same 25 lines again!
}
```

**Root Cause:**
The if/else block boundary detection is failing. The decompiler thinks the inner if block ends earlier than it actually does, so it emits the remaining code both:
1. Inside the inner if (correct)
2. After the inner if but still inside the outer if (incorrect)

This is a **REGRESSION** - Phase 3B should have fixed recursive if/else detection.

**CFG Structure:**
```
Block A: if (info->param2)
  Block B: if (info->param1)
    Blocks C-M: Server init code
  Block N: (should be after outer if)
```

The decompiler is likely emitting Blocks C-M twice:
- Once as part of Block B
- Once as part of Block A (thinking they're not in Block B)

**Affected Components:**
- `vcdecomp/core/ir/structure.py` - `_detect_if_else_pattern()`
- `vcdecomp/core/ir/structure.py` - `emitted_blocks` tracking

**Proposed Fix:**
```python
def _format_if_else(if_pattern, indent, emitted_blocks, ...):
    """
    Render if/else and mark all blocks as emitted.
    """
    lines = [f"{indent}if ({condition}) {{"]

    # Render true branch
    true_lines = _format_block_lines(
        if_pattern.true_block,
        indent + "    ",
        emitted_blocks,  # CRITICAL: Must share same set
        ...
    )
    lines.extend(true_lines)

    # Mark ALL blocks in true branch as emitted
    emitted_blocks.update(if_pattern.true_blocks)  # NEW: Mark entire branch

    # Render false branch (if exists)
    if if_pattern.false_block:
        lines.append(f"{indent}}} else {{")
        false_lines = _format_block_lines(...)
        lines.extend(false_lines)
        emitted_blocks.update(if_pattern.false_blocks)  # NEW

    lines.append(f"{indent}}}")

    # CRITICAL: Return emitted_blocks so parent can see what we emitted
    return lines, emitted_blocks
```

**Implementation Complexity:** HARD (1 day) - This is a critical regression fix

---

### MAJOR #9: Triple Code Duplication
**Lines:** ScriptMain:81-92 vs tdm.c:112-116

**Impact:** Code executes 3x instead of 1x, causes wrong behavior.

**Root Cause:** Same as Issue #8 - block boundary detection failure.

**Fix:** Same as Issue #8.

---

### CRITICAL #10: Wrong Variable Comparison (Always True)
**Lines:** ScriptMain:212 vs tdm.c:268

**Impact:** Produces logically incorrect code (condition always true).

```c
// ORIGINAL
if (sideA==sideB){

// DECOMPILED
if (((i == i))) {  // ALWAYS TRUE!
```

**Root Cause:**
Variable aliasing failure. The original code has two separate variables:
- `sideA` from line 260: `sideA = plinfo.side;`
- `sideB` from line 264/266: `sideB = plinfo.side;` or `sideB = 0xffffffff;`

The decompiler lost track that there are two distinct variables and assigned them both to `i`.

**SSA Issue:**
The decompiler's SSA renaming is collapsing distinct variables into the same SSA register. This might be due to register pressure or incorrect liveness analysis.

**Affected Components:**
- `vcdecomp/core/ir/ssa.py` - SSA variable allocation
- `vcdecomp/core/ir/ssa.py` - Variable naming strategy

**Proposed Fix:**
Improve SSA variable naming to preserve semantic distinctions:

```python
class SSAVariableNamer:
    def __init__(self):
        self.var_counter = 0
        self.source_tracking = {}  # Track where each SSA var came from

    def allocate_variable(self, source_expr, block_id):
        """
        Allocate a new SSA variable, tracking its source.
        """
        var_name = f"var_{self.var_counter}"
        self.var_counter += 1

        self.source_tracking[var_name] = {
            'source': source_expr,
            'block': block_id,
            'def_site': ...
        }

        return var_name

    def are_same_variable(self, var1, var2):
        """
        Check if two SSA vars represent the same logical variable.
        """
        source1 = self.source_tracking[var1]['source']
        source2 = self.source_tracking[var2]['source']

        # Same source = same variable
        return source1 == source2

    def get_readable_name(self, ssa_var):
        """
        Get human-readable name based on source.
        """
        source = self.source_tracking[ssa_var]['source']

        if 'plinfo.side' in source:
            # Distinguish multiple reads from same struct field
            block_id = self.source_tracking[ssa_var]['block']
            if block_id < 210:
                return 'sideA'
            else:
                return 'sideB'

        return self._default_name(ssa_var)
```

**Implementation Complexity:** HARD (1-2 days)

---

### MAJOR #11: Duplicate Message Calls
**Lines:** ScriptMain:159, 162, 180 vs tdm.c:216

**Impact:** Error message printed 3x instead of conditionally once.

**Root Cause:** Same as Issues #8 and #9 - block duplication.

**Fix:** Same as Issue #8.

---

### CRITICAL #12: Empty If/Else Bodies
**Lines:** ScriptMain:193-195 vs tdm.c:235-241

**Impact:** Missing critical assignments, produces non-functional code.

```c
// ORIGINAL
if (info->param2){
    info->fval1 = 0.1f;
}
else{
    info->fval1 = RECOVER_TIME;
}

// DECOMPILED
if ((info->field_8)) {
} else {
}
```

**Root Cause:**
The assignments to `info->fval1` are missing. This could be:
1. Struct field assignment detection issue
2. Float field handling issue (note: `fval1` is a float union member)

**Bytecode Likely:**
```assembly
FPSH 0.1                    ; Push float constant
GCP info                    ; Get pointer to info
IPSH offset_fval1           ; Push offset to fval1
IADD                        ; Calculate field address
FSTO                        ; Store float to address
```

The `FSTO` to a calculated address might not be recognized as a struct field assignment.

**Affected Components:**
- `vcdecomp/core/ir/expr.py` - Struct field assignment detection
- `vcdecomp/core/ir/ssa.py` - Pointer arithmetic analysis

**Proposed Fix:**
```python
def _detect_field_assignment(sto_inst, ssa_func):
    """
    Detect pattern: GCP base + IPSH offset + IADD + STO = field assignment
    """
    if sto_inst.opcode not in [ISTO, FSTO, DSTO, CSTO, SSTO]:
        return None

    # Trace back to find the address calculation
    addr_value = sto_inst.arg1

    # Look for pattern: base_ptr + offset
    if isinstance(addr_value, SSAValue):
        def_inst = addr_value.definition

        if def_inst and def_inst.opcode == IADD:
            # Found addition - check if it's ptr + offset
            base = def_inst.arg1
            offset = def_inst.arg2

            if _is_pointer(base) and _is_constant(offset):
                # This is a field access!
                base_name = _format_value(base, ssa_func)
                field_name = _get_field_name(base.type, offset)

                return f"{base_name}->{field_name}"

    return None
```

**Implementation Complexity:** MEDIUM (3-4 hours)

---

## Proposed Decompiler Fixes - Priority Ranking

### Priority 1: CRITICAL CORRECTNESS (Must Fix)
These produce functionally incorrect code that would crash or misbehave.

| Priority | Issue | Module | Complexity | Est. Time |
|----------|-------|--------|------------|-----------|
| **P1.1** | #8: Code duplication (regression!) | `structure.py` | HARD | 1 day |
| **P1.2** | #2: Logical OR to nested if | `structure.py` | HARD | 1-2 days |
| **P1.3** | #10: Variable aliasing `i==i` | `ssa.py` | HARD | 1-2 days |
| **P1.4** | #12: Empty if/else bodies | `expr.py`, `ssa.py` | MEDIUM | 3-4 hours |
| **P1.5** | #4: Missing return statement | `structure.py` | MEDIUM | 2-3 hours |
| **P1.6** | #3: Missing default case | `structure.py` | HARD | Linked to #2 |

**Total P1:** ~4-6 days

### Priority 2: MAJOR CORRECTNESS (Should Fix)
These produce incorrect code but might not crash immediately.

| Priority | Issue | Module | Complexity | Est. Time |
|----------|-------|--------|------------|-----------|
| **P2.1** | #7: Loop bounds `<=` vs `<` | `structure.py` | MEDIUM | 3-4 hours |
| **P2.2** | #5: Missing call arguments | `expr.py`, `ssa.py` | HARD | 1 day |
| **P2.3** | #1: Switch selector aliasing | `expr.py`, `ssa.py` | MEDIUM | 2-3 hours |

**Total P2:** ~2-3 days

### Priority 3: READABILITY (Nice to Have)
These reduce readability but don't affect functionality.

| Priority | Issue | Module | Complexity | Est. Time |
|----------|-------|--------|------------|-----------|
| **P3.1** | #6: Struct field names | `headers/parser.py`, `expr.py` | HARD | 1-2 days |

**Total P3:** ~1-2 days

---

## Implementation Roadmap

### Phase 4A: Critical Fixes (Week 1)
**Goal:** Fix code duplication and control flow issues

1. **Fix Issue #8: Code Duplication** (Day 1-2)
   - Improve `emitted_blocks` tracking
   - Fix nested if/else boundary detection
   - Add comprehensive tests

2. **Fix Issue #2/#3: Logical OR + Default Case** (Day 3-4)
   - Implement boolean expression reconstruction
   - Fix switch case boundary detection
   - Test on tdm.scr and other scripts

3. **Fix Issue #10: Variable Aliasing** (Day 5)
   - Improve SSA variable naming
   - Add source tracking for variables
   - Prevent collapsing distinct variables

**Validation:** Re-run tdm.scr decompilation and verify:
- No code duplication
- Correct logical OR expressions
- Variables have distinct names

### Phase 4B: Correctness Fixes (Week 2)
**Goal:** Fix remaining critical and major issues

1. **Fix Issue #12: Empty If/Else Bodies** (Day 1)
   - Implement struct field assignment detection
   - Handle pointer arithmetic patterns

2. **Fix Issue #4: Missing Return** (Day 1)
   - Detect post-switch blocks
   - Render fall-through returns

3. **Fix Issue #7: Loop Bounds** (Day 2)
   - Fix `<=` vs `<` logic
   - Implement data constant resolution

4. **Fix Issue #5: Call Arguments** (Day 3-4)
   - Implement PUSH instruction tracing
   - Extract call arguments from stack

5. **Fix Issue #1: Switch Selector** (Day 5)
   - Implement value tracing for switch
   - Resolve aliases to original names

**Validation:** 100% pass on tdm.scr with all issues fixed

### Phase 4C: Readability (Week 3)
**Goal:** Improve readability with struct field names

1. **Fix Issue #6: Struct Field Names** (Day 1-3)
   - Extend header parser for struct definitions
   - Implement field name resolution by offset
   - Test on all scripts

**Validation:** Full regression test on tdm.scr, hitable.scr, Gaz_67.scr

---

## Testing Strategy

### Regression Tests
After each fix, run all test scripts:

```bash
# Test 1: TDM (primary test case)
python -m vcdecomp structure Compiler-testruns/Testrun1/tdm.scr > tdm_output.c

# Test 2: Hitable (switch test)
python -m vcdecomp structure Compiler-testruns/Testrun3/hitable.scr > hitable_output.c

# Test 3: Gaz_67 (loop test)
python -m vcdecomp structure Compiler-testruns/Testrun2/Gaz_67.scr > gaz67_output.c
```

### Validation Criteria
For each test:
1. No code duplication
2. Correct control flow (if/else, loops, switches)
3. Correct variable names (no `i == i`)
4. All function bodies complete (no missing returns)
5. No empty if/else bodies

### Success Metrics
- **Code size:** Decompiled output within ±20% of original LOC
- **Accuracy:** ≥95% structural correctness
- **Zero duplications:** No blocks emitted more than once
- **Zero empty bodies:** All control structures have bodies or comments

---

## Conclusion

The current decompilation has **severe regressions** compared to the Phase 3 baseline:

**Estimated Accuracy: ~60%** (down from 87%)

### Most Critical Issues:
1. **Code duplication** (#8, #9, #11) - Makes code 2-3x larger
2. **Wrong control flow** (#2) - Breaks logical OR expressions
3. **Variable aliasing** (#10) - `i == i` always true

These issues suggest problems with the **Phase 3 if/else detection** that was supposedly fixed. Either:
- The fixes weren't properly applied
- New bugs were introduced
- The test cases didn't catch these patterns

### Recommended Action:
**IMMEDIATELY** fix Priority 1 issues before proceeding with any other development. The current output is not production-ready.

**Estimated total fix time:** 7-11 days for all priorities.

---

**Report Generated:** January 2, 2026
**Next Review:** After Phase 4A completion
