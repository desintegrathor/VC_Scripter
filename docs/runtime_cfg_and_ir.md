# Runtime CFG & Stack Lifting

We now have the first IR layer on top of the opcode mapping. This is the foundation for SSA/type propagation and, ultimately, Hex-Rays-style structured output.

## Tools

- `python -m vcdecomp cfg file.scr [--variant auto|runtime|compiler]`
  - Builds the control-flow graph (`vcdecomp/core/ir/cfg.py`), prints each basic block, its instruction range, and successors.
  - Useful for spotting entry blocks, fan-out, and verifying jump normalization.
- `python -m vcdecomp lift file.scr [--variant …] [-b block_id]`
  - Runs the stack lifter (`vcdecomp/core/ir/stack_lifter.py`) on the requested block (defaults to CFG entry).
  - Shows stack values entering/exiting the block plus per-instruction inputs/outputs (`t<addr>_<idx>` pseudo-registers). Incoming phi-like slots appear as `phi_<block>_<depth>` when predecessors disagree.
- `python -m vcdecomp ssa file.scr [--variant …] [-b block_id]`
  - Builds SSA metadata (`vcdecomp/core/ir/ssa.py`) so each temporary knows its uses/producer.
  - Output mirrors `lift` but uses SSA names/types; phi placeholders are included, making it easier to spot where values merge.

Example (runtime script block 2):

```
python -m vcdecomp lift Compiler-testruns/Testrun2/Gaz_67.scr --variant runtime -b 2
```

Output:

```
Lifted block 2 [0002-0002] in Compiler-testruns/Testrun2/Gaz_67.scr
Stack before block: t0_0, t1_0

0002: LADR     | in: - -> out: t2_0

Stack after block: t0_0, t1_0, t2_0
```

## Next steps

1. **Full SSA:** replace the placeholder `phi_*` values with actual SSA nodes referencing predecessor blocks (dominance frontier placement, renaming). The current `ssa` command already aggregates values, but renaming still mirrors stack indices.
2. **Type propagation:** use `OpcodeInfo.result_type`/`arg*_type` to infer types for each SSA value, intersect with XFN signatures.
3. **Structuring:** once SSA + types exist, begin reconstructing high-level control structures (if/loops/switch) for pretty-printing.
4. **Documentation:** when SSA stabilizes, move these notes into the main README and add regression tests covering `cfg`/`lift`.
