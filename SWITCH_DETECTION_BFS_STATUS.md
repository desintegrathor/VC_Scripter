# Switch Detection BFS Implementation Status

**Date**: 2026-01-19
**Task**: Implement graph-based (BFS) switch detection to handle non-linear comparison chains
**Status**: Partially implemented, debugging in progress

---

## Executive Summary

The BFS-based switch detection has been partially implemented to replace the linear chain detection approach. The implementation is syntactically correct and passes all existing unit tests, but **switch detection is still not working** (0 switches detected vs. goal of 7/12).

**Root Cause Discovered**: The issue is NOT just the linear vs. BFS traversal. The deeper problem is that **constant value extraction is failing**, preventing any cases from being added to switches regardless of traversal strategy.

---

## What Was Implemented

### 1. Stage 1: Parameter Offset Tracing ✅ COMPLETE

**File**: `vcdecomp/core/ir/structure/analysis/value_trace.py`

**Changes**:
- Added `_trace_stack_slot_to_parameter()` function (lines 1028-1142)
  - Traces high stack offsets (e.g., `LCP [sp+41]`) back to parameter sources (e.g., `LCP [sp-4]`)
  - Uses BFS through predecessor blocks to find parameter loads
  - Handles compiler optimization where parameters are copied to local stack slots

- Modified `_trace_value_to_parameter()` (lines 962-973)
  - Added branch for offsets >= 20 to use new tracing function
  - Preserves existing logic for standard parameter offsets (< 20)

**Expected Impact**: Should detect switch at line 309 (`switch(attacking_side)`) where parameter is stored at offset 41

**Test Status**: All unit tests pass, no regressions

---

### 2. Stage 2: BFS-Based Switch Detection ⚠️ PARTIAL

**File**: `vcdecomp/core/ir/structure/patterns/switch_case.py`

**Changes**:

#### a) Replaced Linear Loop with BFS (lines 412-458)

**Old approach** (linear chain):
```python
while current_block is not None and current_block in func_block_ids:
    # Process current_block
    # Find next block in linear chain
    current_block = next_block
```

**New approach** (BFS exploration):
```python
visited_blocks = set()
to_visit = [(block_id, 0)]  # (block_id, depth)
max_bfs_depth = 15

while to_visit:
    current_block, depth = to_visit.pop(0)

    # Depth limit
    if depth > max_bfs_depth:
        continue

    # Skip visited blocks
    if current_block in visited_blocks:
        continue
    visited_blocks.add(current_block)

    # Process block...
```

**Rationale**: Handles non-linear patterns where case bodies are interleaved between comparison blocks.

**Example Pattern** (line 670 switch):
```
Block 1757: EQU (test case 0)  ← First comparison
Block 1761: Case 0 body         ← INTERRUPTS CHAIN
Block 1774: EQU (test case 1)  ← Second comparison
```

Linear approach breaks at block 1761 (no EQU). BFS approach explores both paths.

#### b) Changed Break → Continue (lines 437, 442, 458, 684)

**Old**:
```python
if current_block in processed_blocks:
    break  # Abort entire chain
```

**New**:
```python
if current_block in processed_blocks:
    continue  # Skip this block, keep exploring
```

**Impact**: Allows BFS to continue even when encountering:
- Already-processed blocks
- Blocks without instructions
- Blocks without conditional jumps
- Blocks testing different variables

#### c) Added Successor Exploration (lines 454-458, 730-733, 738-742)

**After finding comparison block**:
```python
# Add ALL successors to BFS queue
for succ in curr_block_obj.successors:
    if succ not in visited_blocks and succ in func_block_ids:
        to_visit.append((succ, depth + 1))
```

**After non-comparison block**:
```python
# Might be case body - explore successors
for succ in curr_block_obj.successors:
    if succ not in visited_blocks and succ in func_block_ids:
        to_visit.append((succ, depth + 1))
```

**Impact**: Allows BFS to "jump over" case body blocks to find next comparison block.

---

## Current Issue: Why Switches Still Aren't Detected

### Debugging Timeline

1. ✅ BFS loop executes (confirmed by debug output)
2. ✅ EQU instructions found (confirmed by "First case" messages)
3. ✅ Test variables identified correctly (e.g., `gEndRule`, `SC_ggi(503)`)
4. ❌ **No cases are added** (0 "Added case" messages)
5. ❌ **No "Chain complete" messages** (BFS completes without collecting cases)

### Root Cause Analysis

**Problem Location**: Lines 705-736 in `switch_case.py`

The case is only added if `case_val is not None`:
```python
case_val = None
if const_value.alias and const_value.alias.startswith("data_"):
    try:
        offset = int(const_value.alias[5:])
        if ssa_func.scr and ssa_func.scr.data_segment:
            case_val = ssa_func.scr.data_segment.get_dword(offset * 4)
    except (ValueError, AttributeError):
        pass

if case_val is not None:  # ← FAILS HERE
    # Add case to switch
    cases.append(CaseInfo(value=case_val, block_id=case_block_id))
```

**Why extraction fails** (hypothesis):
1. `const_value.alias` might not start with `"data_"` (different format)
2. Offset calculation might be wrong
3. Data segment might not contain the expected value
4. Exception might be raised silently

**Evidence**:
- 24 "First case" messages seen in debug output
- 0 "Added case" messages
- This affects ALL switches, not just the ones with non-linear chains

---

## How to Continue Implementation

### Immediate Next Steps

#### Step 1: Debug Constant Value Extraction (HIGH PRIORITY)

Add debug logging to understand why `case_val` remains `None`:

```python
# In switch_case.py, around line 696
case_val = None

# ADD THIS DEBUG
_switch_debug(f"Extracting constant: alias={const_value.alias}, has_alias={hasattr(const_value, 'alias')}")

if const_value.alias and const_value.alias.startswith("data_"):
    try:
        offset = int(const_value.alias[5:])
        _switch_debug(f"  Offset: {offset}")

        if ssa_func.scr and ssa_func.scr.data_segment:
            case_val = ssa_func.scr.data_segment.get_dword(offset * 4)
            _switch_debug(f"  Extracted value: {case_val}")
        else:
            _switch_debug(f"  No data segment available")
    except (ValueError, AttributeError) as e:
        _switch_debug(f"  Exception during extraction: {e}")
else:
    _switch_debug(f"  Constant not in data_ format")

# ADD THIS DEBUG
if case_val is None:
    _switch_debug(f"  FAILED to extract constant value")
    # Try alternative extraction methods
    if hasattr(const_value, 'constant_value'):
        case_val = const_value.constant_value
        _switch_debug(f"  Fallback: Using constant_value attribute: {case_val}")
    elif hasattr(const_value, 'literal'):
        case_val = const_value.literal
        _switch_debug(f"  Fallback: Using literal attribute: {case_val}")
```

**Run**:
```bash
cd "C:\Users\flori\source\repos\VC_Scripter"
py -m vcdecomp structure decompiler_source_tests/test1/tt.scr > debug_constants.c 2>&1
grep "Extracting constant\|Extracted value\|FAILED to extract" debug_constants.c | head -50
```

#### Step 2: Fix Constant Extraction Based on Findings

**Option A**: If `const_value` has a different attribute:
```python
# Try multiple attributes
if hasattr(const_value, 'constant_value') and const_value.constant_value is not None:
    case_val = const_value.constant_value
elif hasattr(const_value, 'literal') and const_value.literal is not None:
    case_val = const_value.literal
elif const_value.alias and const_value.alias.isdigit():
    case_val = int(const_value.alias)
elif const_value.alias and const_value.alias.startswith("data_"):
    # Existing logic...
```

**Option B**: If SSA value representation changed:
```python
# Check SSA value structure
_switch_debug(f"const_value type: {type(const_value)}")
_switch_debug(f"const_value attributes: {dir(const_value)}")

# Use appropriate extraction method based on type
```

#### Step 3: Verify BFS Explores Correct Blocks

After fixing constant extraction, verify BFS is working:

```bash
# Look for BFS traversal messages
grep "Added successor.*to BFS queue" debug_constants.c | head -20

# Check if multiple comparison blocks are found
grep "First case\|Added case" debug_constants.c | head -30

# Verify chain completion
grep "Chain complete:.*cases found" debug_constants.c
```

**Expected output** (after fix):
```
First case - variable: gEndRule, SSA: t53_0
Added case: value=0, block=4
Added successor 5 to BFS queue
Added case: value=1, block=6
Added successor 7 to BFS queue
Chain complete: 2 cases found
Switch detected: gEndRule, type=full
```

#### Step 4: Test on Known Switch Patterns

Create minimal test case to verify BFS works:

```python
# In vcdecomp/tests/test_structure_patterns.py

def test_nonlinear_switch_detection(self):
    """Test BFS can handle interleaved case bodies."""
    # Create CFG with pattern:
    # Block 1: EQU(var, 0) → JZ block_3
    # Block 2: Case 0 body → JMP block_exit  (INTERRUPTS)
    # Block 3: EQU(var, 1) → JZ block_exit
    # Block 4: Case 1 body

    cfg = create_test_cfg(...)
    switches = _detect_switch_patterns(...)

    assert len(switches) == 1
    assert len(switches[0].cases) == 2
    assert switches[0].test_var == "test_var"
```

### Medium-Term Improvements

#### 1. Optimize BFS Depth Limit

Current limit is 15 blocks. Adjust based on findings:

```python
# Too restrictive?
max_bfs_depth = 15

# Consider making it configurable or adaptive:
max_bfs_depth = min(len(func_block_ids) // 2, 20)  # Half function size, capped at 20
```

#### 2. Add Early Termination for BFS

Stop exploring when we've found enough cases:

```python
while to_visit:
    current_block, depth = to_visit.pop(0)

    # Early termination if we have enough cases
    if len(cases) > 10:  # Reasonable upper limit for switch
        _switch_debug(f"Found {len(cases)} cases, stopping BFS early")
        break
```

#### 3. Improve Variable Equivalence Checking

The equivalence check (line 668-684) might be too strict:

```python
# Current: Checks SSA value equivalence
values_equivalent = _check_ssa_value_equivalence(
    test_ssa_value, var_value, ssa_func, max_depth=10
)

# Consider relaxing for function calls:
if not values_equivalent:
    # For function calls, check if same function with same args
    if both are XCALL results:
        # Already handled in _check_ssa_value_equivalence
        pass
```

---

## Testing Strategy

### Unit Tests to Add

1. **Test parameter offset tracing**:
```python
def test_parameter_high_offset_detection():
    """Test tracing LCP [sp+41] back to param_0."""
    # Create SSA function with:
    # - Block 1: LCP [sp-4] (param_0 load)
    # - Block 2: LCP [sp+41] (reload from local slot)

    param_name = _trace_value_to_parameter(value_at_41, ...)
    assert param_name == "param_0"
```

2. **Test BFS with interleaved blocks**:
```python
def test_bfs_handles_interleaved_case_bodies():
    """Test BFS doesn't break on case bodies between comparisons."""
    # CFG: Test1 → CaseBody → Test2 → CaseBody
    switches = _detect_switch_patterns(...)
    assert len(switches[0].cases) == 2
```

3. **Test BFS depth limiting**:
```python
def test_bfs_respects_depth_limit():
    """Test BFS doesn't explore infinitely deep."""
    # Create deep CFG (> 15 blocks)
    # Verify BFS stops at depth limit
```

### Integration Tests

```bash
# Test on tt.scr
py -m vcdecomp structure decompiler_source_tests/test1/tt.scr > output.c 2>&1

# Count switches (target: 7/12)
grep -c "switch(" output.c

# Verify specific switches
grep "switch(attacking_side)" output.c  # Line 309
grep "switch(SC_ggi" output.c          # Line 670
grep "switch(gEndRule)" output.c       # Line 110

# Run full test suite
py -m pytest vcdecomp/tests/ -v
```

---

## Expected Results After Fix

### Baseline → Target

| Switch | Line | Expression | Before | After |
|--------|------|-----------|---------|-------|
| 1 | 110 | `switch(gEndRule)` | ❌ (0) | ✅ |
| 2 | 297 | `switch(gMainPhase%2)` | ❌ (0) | ✅ |
| 3 | 309 | `switch(attacking_side)` | ❌ (0) | ✅ (Stage 1) |
| 4 | 323 | `switch(param_0%4)` | ❌ (0) | ✅ |
| 5 | 382 | `switch(gMission_phase)` | ❌ (0) | ✅ |
| 6 | 670 | `switch(SC_ggi(GVAR_GAMEPHASE))` | ❌ (0) | ✅ (Stage 2) |
| 7 | 762 | `switch(local_418)` | ❌ (0) | ✅ |

**Conservative estimate**: 5-7 switches after fixes (vs. current 0)

---

## Code Locations Reference

### Files Modified

1. **`vcdecomp/core/ir/structure/analysis/value_trace.py`**
   - Line 1028-1142: `_trace_stack_slot_to_parameter()` (new function)
   - Line 962-973: Modified `_trace_value_to_parameter()` to use tracing

2. **`vcdecomp/core/ir/structure/patterns/switch_case.py`**
   - Line 412-458: BFS loop initialization and structure
   - Line 437: Changed break → continue for processed blocks
   - Line 442: Changed break → continue for blocks without instructions
   - Line 452-458: Added successor exploration for non-comparison blocks
   - Line 684: Changed break → continue for variable mismatch
   - Line 730-733: Added successor exploration after finding case
   - Line 738-742: Added successor exploration when no EQU found

### Critical Code Sections

**Constant extraction** (needs debugging):
- File: `switch_case.py`
- Lines: 696-704
- Function: Extract case value from `const_value.alias`

**Case addition** (blocked by constant extraction):
- File: `switch_case.py`
- Lines: 705-736
- Function: Add case to switch if `case_val is not None`

**BFS queue management**:
- File: `switch_case.py`
- Lines: 413-415 (initialization)
- Lines: 418-458 (main BFS loop)
- Lines: 730-733, 738-742 (successor addition)

---

## Known Issues & Limitations

### Issue 1: No Switches Currently Detected

**Status**: Critical blocker
**Symptom**: 0 switches in output despite 24 potential switches found
**Cause**: Constant value extraction fails (`case_val` remains `None`)
**Fix**: Debug constant extraction (see Step 1 above)

### Issue 2: BFS Not Fully Tested

**Status**: Unknown effectiveness
**Symptom**: Can't test BFS until constant extraction works
**Mitigation**: Unit tests pass, suggesting structure is sound

### Issue 3: Documentation Claims Incorrect

**Status**: Documentation issue
**Files**: `tt_info.txt`, `PHASE8_IMPLEMENTATION_STATUS.md`
**Claim**: "5/12 switches detected (42%)"
**Reality**: 0 switches detected
**Action**: Update documentation after fixes

---

## Success Criteria

### Minimum Viable

- [ ] **At least 1 switch detected** (prove constant extraction works)
- [ ] **No test regressions** (all unit tests pass)
- [ ] **Code compiles** (no Python syntax errors)

### Target Goals

- [ ] **5-7 switches detected** (approaching 50%+ success rate)
- [ ] **Switch at line 309 works** (parameter offset tracing)
- [ ] **Switch at line 670 works** (BFS handles non-linear chain)
- [ ] **New unit tests pass** (BFS behavior validated)

### Stretch Goals

- [ ] **8+ switches detected** (>67% success rate)
- [ ] **All non-nested switches work** (exclude lines 574, 948, 959, 1051, 1076)
- [ ] **Performance acceptable** (BFS doesn't slow down decompilation)

---

## Quick Reference Commands

```bash
# Navigate to project
cd "C:\Users\flori\source\repos\VC_Scripter"

# Run decompiler with debug
py -m vcdecomp structure decompiler_source_tests/test1/tt.scr > output.c 2>&1

# Count switches
grep -c "switch(" output.c

# Check specific switches
grep "switch(attacking_side)\|switch(SC_ggi\|switch(gEndRule)" output.c

# Run tests
py -m pytest vcdecomp/tests/test_structure_patterns.py -v

# Check for debug messages
grep "First case\|Added case\|Chain complete" output.c | head -30

# Debug constant extraction
grep "Extracting constant\|Extracted value\|FAILED" output.c | head -50
```

---

## Contact/Continuation Notes

**Current Blocker**: Constant value extraction (line 696-704 in `switch_case.py`)
**Next Person Should**: Add debug logging per Step 1, identify why `case_val` is `None`
**Time Estimate**: 2-4 hours to debug and fix constant extraction
**Risk Level**: Low (changes are isolated, tests pass)

**Files to Watch**:
- `switch_case.py` (main implementation)
- `value_trace.py` (parameter tracing - completed)
- `test_structure_patterns.py` (add tests here)

**Git Branch**: `main` (changes committed directly, can revert if needed)

---

**Last Updated**: 2026-01-19 15:30 UTC
**Author**: Claude (Sonnet 4.5)
**Status**: Ready for continuation
