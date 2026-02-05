Here is the implementation plan:

---

# Implementation Plan - Iteration 1

## Selected Root-Cause Invariant

**When emitting a switch case body via the structured path (because `_has_structured_children` is true), the emitter assumes the structured `body_block.covered_blocks` contains ALL blocks in `body_block_ids`. This assumption is false when the collapse engine only partially collapses the case body (e.g., collapses a loop header + predecessor but not subsequent blocks). The uncovered blocks are silently dropped from the output.**

## Evidence

### Test 1 (tt.scr) - `info->message` case 1 (SC_NET_MES_LEVELINIT)

**Decompiled (lines 547-561):** Only ~15 lines of init code emitted
```c
case 1:
    g_FPV_UsFlag = SC_MP_FpvMapSign_Load("g\\weapons\\...USflag.BES");
    ...
    for (j = 0; j < 6; j++) {
        SC_MP_SRV_SetClassLimit(j + 1, (*tmp222 + j * 4));
        SC_MP_SRV_SetClassLimit(j + 21, (*tmp225 + j * 4));
    }
    break;
```

**Original (lines 756-933):** ~175 lines of init including flag detection, respawn setup, HUD, etc. - all missing.

**Debug evidence:**
```
MISMATCH: switch=info->message, case=1, covered=[275, 276, 277], 
  body_block_ids=[275-316], MISSING=[278-316] (39 blocks!)
```

### Test 3 (LEVEL.SCR) - `gphase` case 0 (initialization)

**Decompiled (lines 278-307):** Only InitSideGroup + 1 for-loop shown
```c
case 0:
    local_4.MaxHideOutsStatus = 32;
    ...SC_InitSideGroup(&idx);...
    for (i = 0; i < 12; i++) { ... }
    break;
```

**Original (lines 401-526):** ~125 lines including multiple InitSide, SetSideAlly, ShowTrashes, gphase=1, SC_sgi calls, Ai_SetPlFollow loop, GetWp loop, etc. - all missing.

**Debug evidence:**
```
GPHASE case 0: body_block type=BlockList, covered_blocks=[110, 111, 112]
body_block_ids=[110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]
MISSING: blocks 113-122 (10 blocks of critical init code)
```

### Root cause trace:

In `hierarchical_emitter.py` line 1424:
```python
if case.body_block is not None and self._has_structured_children(case.body_block):
    lines.extend(self._emit_block(case.body_block, indent + "    "))
    if case.body_block_ids:
        self.emitted_blocks.update(set(case.body_block_ids) - set(exit_ids))
```

When `body_block.covered_blocks = {110, 111, 112}` but `body_block_ids = {110..122}`:
1. `_emit_block(body_block)` only emits blocks 110-112
2. `emitted_blocks.update(body_block_ids)` marks ALL 110-122 as emitted
3. Blocks 113-122 are never rendered but are marked as done

## Proposed Fix

- **File:** `vcdecomp/core/ir/structure/emit/hierarchical_emitter.py`
- **Function:** `_emit_switch` (the case emission logic around lines 1422-1434)
- **Change:** After emitting the structured body_block, check for uncovered blocks. If `body_block_ids` has blocks not in `body_block.covered_blocks`, emit those remaining blocks via the flat path (`_emit_switch_case_body_flat` or `_emit_flat_block_section`).

Specifically, replace:
```python
if case.body_block is not None and self._has_structured_children(case.body_block):
    lines.extend(self._emit_block(case.body_block, indent + "    "))
    if case.body_block_ids:
        self.emitted_blocks.update(set(case.body_block_ids) - set(exit_ids))
```

With:
```python
if case.body_block is not None and self._has_structured_children(case.body_block):
    lines.extend(self._emit_block(case.body_block, indent + "    "))
    # Emit any blocks NOT covered by the structured body_block
    if case.body_block_ids:
        covered = getattr(case.body_block, 'covered_blocks', set())
        uncovered = sorted(
            set(case.body_block_ids) - covered - set(exit_ids),
            key=lambda bid: self.cfg.blocks[bid].start if bid in self.cfg.blocks else 9999999
        )
        if uncovered:
            # Create a temporary case-like object with just the uncovered blocks
            # and emit them via the flat path
            lines.extend(self._emit_flat_block_section(
                uncovered, 
                set(case.body_block_ids) - set(uncovered),  # stop at already-emitted blocks
                indent + "    ",
                exit_ids
            ))
        self.emitted_blocks.update(set(case.body_block_ids) - set(exit_ids))
```

## Expected Impact

- **tt:** IMPROVED - case 1 (SC_NET_MES_LEVELINIT) will emit all 42 body blocks instead of just 3. This will restore ~160 lines of missing initialization code including flag detection, respawn setup, and HUD configuration.
- **tdm:** UNCHANGED - no mismatch detected; no structured bodies with uncovered blocks.
- **LEVEL:** IMPROVED - gphase case 0 will emit all 13 body blocks instead of 3. This will restore ~100 lines of missing initialization code including InitSide for NEUTRAL, SetSideAlly, ShowTrashes, and multiple setup loops.

## Implementation Steps

1. Read the current `_emit_switch` method in `hierarchical_emitter.py` (lines ~1408-1448)
2. Modify the `has_structured_children` branch (line 1424) to detect uncovered blocks
3. After structured emission, emit remaining blocks via `_emit_flat_block_section`
4. Ensure `emitted_blocks` is only updated AFTER all blocks have been emitted (not before the flat section)
5. Run all three test decompilations and verify regression gate
