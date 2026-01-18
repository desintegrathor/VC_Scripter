# Pattern 1 Root Cause Analysis: Undefined goto Labels

**Date**: 2026-01-18
**Plan**: 06-06a
**Issue**: Gotos emitted to blocks 3, 46, 48 but labels never rendered

## Executive Summary

**Root Cause Identified**: Blocks 3, 46, 48 pass the orphaned check (have predecessors), so gotos are emitted. However, **the blocks themselves are never rendered** into the output, meaning their labels never appear.

**Hypothesis**: **Option B** - Gotos are emitted but labels are not. The blocks exist in CFG, have predecessors, but are skipped during block rendering phase (likely due to switch/case handling or if/else detection logic).

## Evidence from Debug Output

### 1. Orphaned Check Results

From `pattern1_debug_output.txt`:

```
[PATTERN1_DEBUG] Block 3: NOT ORPHANED (has 1 predecessors: [1])
[PATTERN1_DEBUG] EMITTING UNCONDITIONAL GOTO: block_3

[PATTERN1_DEBUG] Block 46: NOT ORPHANED (has 1 predecessors: [44])
[PATTERN1_DEBUG] EMITTING UNCONDITIONAL GOTO: block_46

[PATTERN1_DEBUG] Block 48: NOT ORPHANED (has 1 predecessors: [46])
[PATTERN1_DEBUG] EMITTING UNCONDITIONAL GOTO: block_48
```

**Finding**: All three blocks pass the orphaned check because they have predecessors:
- Block 3 has predecessor [1]
- Block 46 has predecessor [44]
- Block 48 has predecessor [46]

### 2. Goto Emission Confirmed

From `test1_tt_decompiled.c`:

```c
Line 36:  goto block_3; // @57
Line 165: goto block_46; // @343
Line 166: goto block_48; // @348
```

**Finding**: Gotos ARE emitted to all three blocks.

### 3. Labels Never Emitted

Searched for block labels in decompiled output:

```bash
grep -n "^block_3:\|^block_46:\|^block_48:" test1_tt_decompiled.c
# Result: No matches found
```

**Finding**: None of the three blocks have labels rendered in the output.

### 4. Context Analysis

**Block 3 context (line 36)**:
```c
int func_0050(int param_0, int param_1) {
    int tmp;
    int tmp1;
    // ... variable declarations ...

    goto block_3; // @57    <- GOTO EMITTED
    if (!tmp1) {             <- NO LABEL HERE
        data_ = tmp2;
    } else {
        // ...
    }
    return 0;
}
```

**Block 46/48 context (lines 165-166)**:
```c
int func_0334(int param_0) {
    int tmp;

    goto block_46; // @343   <- GOTO EMITTED
    goto block_48; // @348   <- GOTO EMITTED
    return FALSE;            <- NO LABELS HERE
}
```

**Finding**: The blocks that gotos refer to are completely absent from the output. Not just missing labels - the blocks are never rendered at all.

## Root Cause Analysis

### Hypothesis: Blocks Marked as Emitted but Never Actually Rendered

**Theory**: Blocks 3, 46, 48 are being added to `emitted_blocks` set by switch/case or if/else detection logic, but the actual rendering code that would emit their labels is never reached.

**Evidence**:
1. Blocks have valid predecessors → pass orphaned check → goto emitted
2. Blocks never appear in output → rendering logic skipped them
3. Likely scenarios:
   - **Switch/case detection** marks blocks as part of switch body, adds to `emitted_blocks`, but switch rendering doesn't actually emit them (dead code in switch?)
   - **If/else detection** marks blocks as part of if body, adds to `emitted_blocks`, but recursive rendering skips them
   - **Early termination** - Block rendering stops after return statement before reaching these blocks

### Why This Happens

Looking at `orchestrator.py` structure:

1. **Line 353-388**: Main block iteration loop processes blocks in order
2. **Line 355**: Skips blocks already in `emitted_blocks`
3. **Line 371-386**: Switch pattern detection adds ALL switch blocks to `emitted_blocks`
4. **Line 388-390**: If/else pattern detection

**Problem**: If blocks 3, 46, 48 are detected as part of a switch or if/else pattern but the pattern rendering logic doesn't actually emit them (e.g., they're unreachable dead code after a return), they get marked as emitted but never rendered.

### Specific Control Flow

**For block 3 (in func_0050)**:
- Block 1 (predecessor) emits `goto block_3`
- Block 3 should follow, but:
  - It may be detected as part of if/else pattern (block_to_if)
  - Added to `emitted_blocks` by if/else detection
  - But if/else rendering skips it (e.g., dead code after return)
  - Result: goto emitted, label never emitted

**For blocks 46/48 (in func_0334)**:
- Sequential gotos suggest these are part of a switch statement or complex if chain
- Blocks marked as emitted by pattern detection
- But pattern rendering doesn't emit them (unreachable code)

## Fix Proposal

### Option 1: Emit Labels for All Goto Targets (RECOMMENDED)

**Location**: `orchestrator.py` lines 788-831 (goto emission code)

**Change**: When emitting a goto, check if the target block will be rendered. If not, emit the label inline.

```python
# After orphaned check, before emitting goto:
if not is_switch_header_jump and not is_orphaned_target:
    # NEW: Check if target block will be rendered
    target_will_be_rendered = (
        target_block in emitted_blocks or  # Already rendered
        target_block in func_block_ids     # Will be rendered later
    )

    # If target won't be rendered, we need to emit its label somewhere
    if target_block not in emitted_blocks:
        # Emit goto normally - label will appear when block is rendered
        lines.append(f"{base_indent}goto block_{target_block}; // @{target}")
    else:
        # Target was marked emitted but never actually rendered
        # This is the bug - we need to force label emission
        logger.warning(f"[PATTERN1_FIX] Block {target_block} marked emitted but not rendered - forcing label emission")
        # Option A: Skip goto (treat as orphaned)
        # Option B: Force block rendering here
        # Option C: Track "needs_label" and emit later
```

### Option 2: Track "Referenced But Not Rendered" Blocks

**Location**: `orchestrator.py` lines 353-390 (main block loop)

**Change**: After main rendering loop, detect blocks that were:
1. Referenced by gotos
2. Marked as emitted
3. But never actually rendered (no label emitted)

Then emit minimal labels for these blocks:

```python
# After main block rendering loop (line 820+)
# NEW: Find blocks that need labels
needs_label = set()
for line in lines:
    if "goto block_" in line:
        # Extract block ID from goto statement
        import re
        match = re.search(r'goto block_(\d+)', line)
        if match:
            block_id = int(match.group(1))
            # Check if label was emitted
            label_exists = any(f"block_{block_id}:" in l for l in lines)
            if not label_exists:
                needs_label.add(block_id)

# Emit missing labels
for block_id in sorted(needs_label):
    # Find where to insert label (before the code that follows the goto)
    # For now, emit at end of function as dead code marker
    lines.append(f"    block_{block_id}:  // UNREACHABLE - dead code")
    lines.append(f"    return 0;  // Should never reach here")
```

### Option 3: Fix Pattern Detection to Not Mark Unreachable Blocks as Emitted

**Location**: Switch/case and if/else detection logic

**Change**: When detecting patterns, don't add blocks to `emitted_blocks` if they're unreachable dead code after returns.

**Complexity**: HIGH - requires understanding all pattern detection logic and reachability analysis

## Recommended Fix: Option 1 (Simplified)

**Simplest fix**: When a goto is emitted to a block, **ensure that block gets rendered** even if it was marked as part of a pattern.

**Implementation**:

1. **Track goto targets**: Maintain a `goto_targets` set of blocks that have gotos pointing to them
2. **Force label emission**: Before marking a block as "emitted", check if it's a goto target. If yes, emit its label even if pattern detection wants to skip it.

**Code change** (~10 lines):

```python
# At start of format_structured_function (line 218+):
goto_targets = set()  # Will be populated during rendering

# In goto emission code (lines 788-831):
if not is_switch_header_jump and not is_orphaned_target:
    goto_targets.add(target_block)  # Track this as a goto target
    lines.append(f"{base_indent}goto block_{target_block}; // @{target}")

# In main block loop (lines 353-390):
for idx, (addr, block_id, block) in enumerate(func_blocks):
    # NEW: Always render blocks that are goto targets, even if "emitted"
    if block_id in emitted_blocks and block_id not in goto_targets:
        continue  # Skip already emitted blocks (unless they're goto targets)

    # If this is a goto target, emit label
    if block_id in goto_targets:
        lines.append(f"    block_{block_id}:")

    # ... rest of block rendering ...
```

## Next Steps (Plan 06-06b)

1. Implement Option 1 fix
2. Remove diagnostic logging
3. Verify blocks 3, 46, 48 now have labels
4. Run validation tests to confirm fix
5. Update documentation

## Verification Strategy

**Before fix**:
```bash
grep "goto block_3" test1_tt_decompiled.c  # Found
grep "^block_3:" test1_tt_decompiled.c     # Not found
```

**After fix**:
```bash
grep "goto block_3" test1_tt_decompiled.c  # Found
grep "^block_3:" test1_tt_decompiled.c     # Found
```

**Success criteria**: All gotos have corresponding labels, no undefined labels.
