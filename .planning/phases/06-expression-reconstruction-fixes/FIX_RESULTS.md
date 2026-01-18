# Expression Reconstruction Fix Results (Plan 06-02)

**Date**: 2026-01-18
**Fixes Applied**: Pattern 1 (Undefined goto labels), Pattern 5 (Undeclared variables)
**Result**: Fixes implemented but compilation still fails - deeper issues identified

## Fixes Applied

### Fix 1: Pattern 1 - Skip goto to orphaned blocks

**Files**: `vcdecomp/core/ir/structure/orchestrator.py` (lines 763-778, 790-805)

**Problem**: Decompiler generates `goto block_X` statements where block_X doesn't exist or is unreachable (orphaned block with no predecessors).

**Fix Implemented**:
```python
# Check if target_block is valid and reachable before generating goto
is_orphaned_target = False
if target_block < 0 or target_block not in cfg.blocks:
    is_orphaned_target = True  # Target doesn't exist
elif target_block not in func_block_ids:
    is_orphaned_target = True  # Target outside function scope
elif target_block != entry_block:
    predecessors = [p for p in target_cfg_block.predecessors if p in func_block_ids]
    if not predecessors:
        is_orphaned_target = True  # Target has no predecessors (orphaned)

# Only generate goto if target is valid and reachable
if not is_switch_header_jump and not is_orphaned_target:
    lines.append(f"{base_indent}goto block_{target_block}; // @{target}")
```

**Applied to**:
- Conditional jumps (JZ/JNZ) - line 763-786
- Unconditional jumps (JMP) - line 790-815

**Example**:
```c
// BEFORE:
if (!tmp) goto block_88; // @1056  // ERROR: block_88 undefined
return;

// AFTER (expected):
// goto removed, block_88 is orphaned
return;
```

---

### Fix 2: Pattern 5 - Collect undeclared variable references

**Files**: `vcdecomp/core/ir/structure/analysis/variables.py` (lines 385-419)

**Problem**: Variables like `vec`, `enum_pl` are used in function calls (via `&vec`) but never declared.

**Fix Implemented**:
```python
# Scan all formatted expressions for &varname patterns
import re
for block_id in func_block_ids:
    block_exprs = format_block_expressions(ssa_func, block_id, formatter=formatter)
    for expr in block_exprs:
        # Extract address-of references
        addr_of_vars = re.findall(r'&(\w+)', expr.text)
        for var_name in addr_of_vars:
            if var_name not in var_types:
                # Infer type from name pattern
                if var_name in ('vec', 'pos', 'rot', 'dir'):
                    var_type = "s_SC_vector"
                elif 'enum' in var_name.lower():
                    var_type = "s_SC_MP_EnumPlayers"
                else:
                    var_type = "int"
                var_types[var_name] = var_type
```

**Example**:
```c
// BEFORE:
SC_ZeroMem(&vec, 12);  // ERROR: 'vec' undeclared
SC_MP_EnumPlayers(&enum_pl, &local_, 1);  // ERROR: 'enum_pl' undeclared

// AFTER (expected):
s_SC_vector vec;
s_SC_MP_EnumPlayers enum_pl;
// ...
SC_ZeroMem(&vec, 12);  // OK
SC_MP_EnumPlayers(&enum_pl, &local_, 1);  // OK
```

---

## Validation Results

### Baseline (Pre-Fix)
- **test1/tt.scr**: Compilation CRASH (0xC0000005), size 4530 bytes
- **test2/tdm.scr**: Compilation CRASH (0xC0000005), size unknown
- **test3/LEVEL.scr**: Compilation CRASH (0xC0000005), size 2520 bytes
- **Success rate**: 0/3 (100% failure)

### After Fixes
- **test1/tt.scr**: Compilation CRASH (0xC0000005), size unknown
- **test2/tdm.scr**: Compilation CRASH (0xC0000005), size 967 bytes
- **test3/LEVEL.scr**: Compilation CRASH (0xC0000005), size 2470 bytes
- **Success rate**: 0/3 (100% failure)

### Metrics Comparison

| Metric | Baseline | After Fixes | Delta |
|--------|----------|-------------|-------|
| Total compilation errors | N/A (crash) | N/A (crash) | - |
| Scripts compiling | 0/3 | 0/3 | 0 |
| Compiler crashes | 3/3 | 3/3 | 0 |
| test3/LEVEL size | 2520 bytes | 2470 bytes | -50 bytes |
| test2/tdm size | Unknown | 967 bytes | - |

**File size reduction** in test3/LEVEL (-50 bytes) suggests some code was removed, potentially the orphaned goto statements.

---

## Regression Check

**No new errors introduced**: Compilation still crashes with same error code (0xC0000005 - access violation).

**No regressions detected**: All tests fail in the same way as baseline.

---

## Root Cause Analysis

The fixes were correctly implemented but **did not resolve the compiler crashes**. Inspection of the decompiled files reveals the fixes were only partially effective:

### Fix 1 Status: PARTIALLY EFFECTIVE
- Code inspection shows `goto block_88` still present in `test3/LEVEL_decompiled.c` line 147
- The orphaned block check logic is correct but may not catch all cases
- Possible issues:
  1. **Timing problem**: Block hasn't been marked orphaned yet when goto is generated
  2. **ScriptMain failure**: The function containing the problematic goto (func_1021) may be part of ScriptMain which failed to decompile
  3. **Different code path**: The goto might be generated through a code path not covered by the fix

### Fix 2 Status: NOT EFFECTIVE
- Variables `vec` and `enum_pl` still undeclared in test3/LEVEL_decompiled.c
- The regex-based extraction should have worked
- Possible issues:
  1. **Expression formatting not called**: The fix runs after format_block_expressions, but maybe those variables appear before this pass runs
  2. **Filtering too aggressive**: The skip conditions might be removing these variables
  3. **Timing**: Variables needed before declarations are generated

---

## Deeper Issues Identified

The compiler crashes (0xC0000005) indicate the generated C code is **so malformed** that SCMP.exe crashes during parsing. The baseline identified 6 error patterns, but Patterns 1 and 5 alone aren't sufficient to make code compileable.

**Additional patterns that likely contribute to crashes**:

1. **Pattern 2 (Type mismatches)**: Variables declared as `s_SC_MP_EnumPlayers` but assigned `float` values
   - Example: `*tmp = -20000.0f;` where `tmp` is declared as `int`
   - This requires fixing type inference in `vcdecomp/core/ir/stack_lifter.py`

2. **Pattern 3 (Missing return values)**: Functions with `int` return type ending with `return;`
   - Example: `int func_0292(void) { ...; return; }`
   - This requires control flow analysis to synthesize return values

3. **Decompilation failures**: 2/10 functions in LEVEL.scr fail with AttributeError
   - func_0612 and ScriptMain both fail during structure analysis
   - These failures might be generating invalid code that crashes the compiler

---

## Next Steps

### Immediate (Plan 06-03)
The current fixes should be refined:

1. **Debug Fix 1**: Add logging to determine why `goto block_88` is still generated
   - Check if block_88 is in func_block_ids when goto is generated
   - Verify the orphaned check logic executes for this specific case

2. **Debug Fix 2**: Add logging to see which variables are found by regex
   - Print var_types after the regex pass to verify `vec` and `enum_pl` are added
   - Check if they're being filtered out during declaration generation

### Medium-term (Plan 06-03 or 06-04)
Address the other high-priority patterns:

3. **Fix Pattern 3 (Missing return values)**:
   - Detect when function signature requires return value
   - Synthesize `return 0;` or appropriate placeholder when missing

4. **Fix Pattern 2 (Type mismatches)**:
   - Improve type inference in stack lifter
   - Propagate type information through SSA correctly

### Long-term
5. **Fix AttributeError failures**: Investigate why 2/10 functions fail structure analysis
6. **Fix Pattern 4 (Multiple assignments)**: Optimize SSA-to-AST conversion
7. **Fix Pattern 6 (Unreachable code)**: Prune unreachable blocks before emission

---

## Conclusion

**Fixes Applied**: 2 patterns addressed (Patterns 1 & 5)
**Fixes Effective**: 0 patterns fully resolved
**Compilation Success**: 0/3 tests pass
**Recommendation**: Proceed to Plan 06-03 with debugging and additional pattern fixes

The two highest-priority patterns were addressed with theoretically sound fixes, but the compiler still crashes. This indicates:
1. The fixes have bugs that prevent them from working correctly
2. OR the fixes work but other patterns (2, 3, or AttributeErrors) are severe enough to crash the compiler

Debugging and addressing additional patterns is required to achieve compilation success.
