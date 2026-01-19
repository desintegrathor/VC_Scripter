# Phase 8: Switch Detection Enhancement - Implementation Status

## Current Status: 5/12 switches detected (42%)

### Completed Work

#### Phase 8A: Binary Search Pattern Detection ✓
**Status**: Infrastructure implemented, integrated into detection pipeline

**Files Created**:
- `vcdecomp/core/ir/structure/patterns/jump_table.py` (370 lines)
  - `_detect_binary_search_switch()` - Main detection function
  - `_build_decision_tree()` - Recursive tree building
  - `_find_comparison_for_jump()` - Comparison instruction finder
  - Helper functions for constant extraction, comparison reversal

**Files Modified**:
- `vcdecomp/core/ir/structure/patterns/switch_case.py`
  - Added binary search detection priority (lines 339-347)
  - Integrated before linear chain detection

**Result**: Binary search detector runs successfully but finds no matches in tt.scr
- Likely because tt.scr uses linear chains or other patterns
- Infrastructure ready for files that do use binary search

### Remaining Work

#### Phase 8B: Enhanced Variable Tracing (HIGH PRIORITY)
**Target**: +3 switches (lines 670, 232, 309)

**Missing Switches Requiring Enhanced Tracing**:
1. **Line 670**: `switch(SC_ggi(GVAR_GAMEPHASE))`
   - Needs: Better function call result tracing
   - Current: `_trace_value_to_function_call()` exists but may need cross-block search

2. **Line 232**: `switch(main_phase%4)`
   - Needs: Modulo expression detection
   - Implementation: Add `_trace_modulo_expression()` to value_trace.py

3. **Line 309**: `switch(attacking_side)`
   - Needs: Better parameter tracing
   - Current: `_trace_value_to_parameter()` exists, may need negative offset handling

**Recommended Implementation**:

```python
# In vcdecomp/core/ir/structure/analysis/value_trace.py

def _trace_modulo_expression(
    value,
    formatter,
    ssa_func,
    max_depth=5
):
    """
    Trace value to modulo expression (base_var % constant).

    Pattern:
        t123 = LCP [sp+8]         # Load variable
        t124 = GCP data_456       # Load constant
        t125 = IMOD               # Modulo operation
    """
    if not value.producer_inst or max_depth <= 0:
        return None

    producer = value.producer_inst

    if producer.mnemonic == "IMOD" and len(producer.inputs) >= 2:
        base_var = producer.inputs[0]
        const_val = producer.inputs[1]

        # Format as "var % const"
        base_name = _format_variable_name(base_var, formatter, ssa_func, max_depth-1)
        const_value = _extract_constant(const_val, ssa_func)

        if base_name and const_value is not None:
            return f"{base_name}%{const_value}"

    return None

# Integrate in switch_case.py::_resolve_variable_name()
# Add after function call tracing:
if not var_name:
    var_name = _trace_modulo_expression(var_value, formatter, ssa_func)
```

#### Phase 8C: Nested Switch Handling (MEDIUM PRIORITY)
**Target**: +1-2 switches (lines 574, 948, 959, 1051, 1076)

**Problem**: Nested switches interfere with outer switch detection
- Outer switch detection includes inner switch blocks in case body
- Both detected separately but outer incomplete

**Recommended Approach**:
Use dominator tree ordering to detect outer switches first:
1. Sort potential switch headers by dominance (outer first)
2. Process each, claiming blocks
3. Inner switches only use unclaimed blocks

```python
def _detect_switches_hierarchical(
    ssa_func,
    func_block_ids,
    formatter,
    start_to_block
):
    """
    Detect switches in dominator order (outer before inner).
    """
    cfg = ssa_func.cfg

    # Find all potential switch headers
    headers = _find_switch_headers(cfg, func_block_ids)

    # Sort by domination (blocks earlier in dom_order dominate more)
    headers.sort(key=lambda h: cfg.dom_order.index(h) if h in cfg.dom_order else 999)

    switches = []
    claimed_blocks = set()

    for header in headers:
        if header in claimed_blocks:
            continue

        # Try to build switch using unclaimed blocks
        switch = _try_build_switch(
            header, func_block_ids - claimed_blocks, ...
        )

        if switch:
            switches.append(switch)
            claimed_blocks.update(switch.all_blocks)

    return switches
```

### Testing & Verification

**Test Command**:
```bash
# Run with switch debug enabled
set VCDECOMP_SWITCH_DEBUG=1
py -m vcdecomp structure decompiler_source_tests/test1/tt.scr > output.c 2>debug.log

# Count switches
grep -c "switch (" output.c
# Expected after Phase 8B: 8-9/12
# Expected after Phase 8C: 12/12

# Compare with original
diff decompiler_source_tests/test1/tt.c output.c | grep "switch"
```

**Expected Results by Phase**:
- **Current**: 5/12 (42%) - gEndRule, gSteps, n, gMission_phase, gCLN_ShowInfo
- **After Phase 8B**: 8-9/12 (67-75%) - adds function call, modulo, parameter switches
- **After Phase 8C**: 12/12 (100%) - adds nested switches

### Implementation Priority

1. **Phase 8B.1: Modulo Expression** (HIGHEST)
   - Line 232 is straightforward - just IMOD detection
   - Quick win, ~50 lines of code

2. **Phase 8B.2: Function Call Enhancement** (HIGH)
   - Line 670 - extend existing function call tracer
   - Cross-block search for XCALL

3. **Phase 8B.3: Parameter Tracing** (MEDIUM)
   - Line 309 - extend existing parameter tracer
   - Handle negative offsets

4. **Phase 8C: Hierarchical Detection** (LOWER)
   - More complex refactoring (~200 lines)
   - Can defer if time-constrained

### Files Requiring Changes

**Phase 8B**:
- `vcdecomp/core/ir/structure/analysis/value_trace.py`
  - Add `_trace_modulo_expression()` (~30 lines)
  - Enhance `_trace_value_to_function_call()` for cross-block (~20 lines)
  - Enhance `_trace_value_to_parameter()` for negative offsets (~10 lines)

- `vcdecomp/core/ir/structure/patterns/switch_case.py`
  - Update variable resolution priority (~10 lines at line ~470)
  - Add modulo/enhanced call/param tracing

**Phase 8C**:
- `vcdecomp/core/ir/structure/patterns/switch_case.py`
  - Add `_detect_switches_hierarchical()` (~150 lines)
  - Add `_find_switch_headers()` (~50 lines)
  - Modify `_detect_switch_patterns()` to use hierarchical (~20 lines)

### Next Developer Actions

1. Start with Phase 8B.1 (modulo) - quickest win
2. Run tests after each sub-phase
3. Keep debug logging enabled
4. Compare output incrementally with original tt.c
5. If reaching 10+/12 switches, Phase 8C may not be needed

### Notes

- Binary search detection (Phase 8A) is ready but not finding matches
  - Keep in codebase - useful for other scripts
  - May trigger on different mission scripts

- Existing tests pass (224 tests)
  - No regressions from Phase 8A addition

- Token usage efficient design:
  - Reuse existing infrastructure where possible
  - Small, focused functions
  - Clear integration points
