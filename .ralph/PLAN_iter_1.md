The plan is complete. To summarize the key points:

**Root-cause:** `_detect_array_indexing()` in `expr.py` handles only single-dimension indexing (`base[i]`), even though `GlobalResolver` already correctly computes `array_dimensions` and `array_strides` metadata. For multi-dim arrays like `gRecTimer[2][6][32]`, the bytecode produces nested `ADD(ADD(GADR, MUL(i, 768)), MUL(j, 128))` chains, but the renderer can only extract one MUL per ADD, falling back to raw pointer arithmetic for the remaining dimensions.

**Fix:** Add a `_decompose_multidim_index()` helper that walks the nested ADD/MUL tree and matches stride constants to the known `array_strides`, producing `base[i][j][k]` notation. This uses metadata already computed and stored - no new analysis needed.

**Impact:** ~40+ expressions fixed in tt.scr, zero regression risk for tdm.scr and LEVEL.SCR since they have no multi-dimensional global arrays.
