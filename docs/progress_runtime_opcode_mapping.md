# Runtime Opcode Mapping – project status

## Overview

- **Runtime reverse engineering:** `logs.dll` (imported by `game.dll` via `SCR_ExecScript`) contains the interpreter loop `sub_100F1380`. Using `idaapi.calc_switch_cases()` we extracted all 150 opcode branches and saved them into `docs/runtime_opcode_map*.json` (basic map plus snippets).
- **Authoritative table:** `vcdecomp/core/disasm/runtime_opcode_table.py` is generated from `docs/SASM_TECHNICAL_ANALYSIS.md` and stores the runtime numbering (opcode → mnemonic pairs).
- **`opcodes.py` integration:** Lookups go through `_INFO_BY_MNEMONIC`, so metadata is keyed by mnemonic rather than numeric opcode. The default resolver now reflects the runtime numbering.

## Current state

- **Variant detection:** `SCRFile.from_bytes()` runs heuristics after loading the code segment (does the supposed `XCALL` hit the XFN table? do CALL/JMP targets stay within the code segment?). It stores the best scoring resolver plus the raw scores in `scr.opcode_detection_scores`, and `scr.info()` prints the decision.
- **Disassembler:** `Disassembler(scr, resolver=None)` pulls the resolver from the `SCRFile`, so labels, jumps, and comments are rendered with the correct opcode map automatically. Comments (`GCP`, `XCALL`, `PCALL`, etc.) switched to mnemonic-based conditions instead of hard coded numbers.
- **Opcode metadata:** Completed coverage for the runtime VM – char/short arithmetic, all `CT*`/`ST*`/`ITOC`/`DTO*` conversions, pointer helpers (`GDM`, `FDM`, `PCALL`, `CFA`, `ITRPT`) and unsigned comparisons now expose stack effects and result types, so `get_opcode_info()` no longer returns `None` for any of the 150 mnemonics.
- **CLI override:** Every CLI subcommand that loads a script (`info`, `disasm`, `strings`, `hex`) now supports `--variant {auto,runtime,compiler}`. `auto` remains default, but manual overrides are handy when validating heuristics or poking at exotic builds. The chosen mode (and whether it was forced) shows up in `SCRFile.info()`.
- **Regeneration tooling:** `docs/runtime_opcode_map_with_snippets.json` now stores snippets plus mnemonics, and `tools/update_runtime_opcode_table.py` rebuilds `runtime_opcode_table.py` directly from that source to keep code and docs in sync.
- **Variant validation:** `docs/runtime_variant_detection.md` captures the current heuristic scores for every sample `.scr` in `Compiler-testruns/`, providing ground truth for future regression testing.
- **CFG + stack lifting:** `vcdecomp/core/ir/cfg.py` builds basic blocks/edges and `stack_lifter.py` simulates the VM stack per block. `python -m vcdecomp cfg …` dumps block ranges, while `python -m vcdecomp lift … [-b block]` prints the lifted stack inputs/outputs—first step toward SSA/Hex-Rays-style IR.
- **IR documentation:** see `docs/runtime_cfg_and_ir.md` for CLI examples (`cfg`, `lift`) and the roadmap toward SSA + structured decompilation.

## Next steps

1. **SSA + structuring:** Extend the stack lifter to carry values across blocks (`phi` nodes) and start type propagation/structured output to move toward Hex-Rays-like decompilation.
2. **Validate heuristics:** Test detection against real runtime `.scr` dumps from the shipped game. Add more signals if needed (e.g. CALL vs. SSP patterns, RET density).
3. **Documentation:** Fold the workflow (how to regenerate `runtime_opcode_table.py`, how auto-detect works, when to use `--variant`) into the main README or developer docs so others can reproduce the extraction.

## Repository changes so far

- `docs/runtime_opcode_map.json` / `_with_snippets.json` – raw exports from IDA.
- `vcdecomp/core/disasm/runtime_opcode_table.py` – runtime opcode table.
- `vcdecomp/core/disasm/opcodes.py` – resolver infrastructure, runtime default, fallback metadata.
- `vcdecomp/core/loader/scr_loader.py` – auto detection plus manual override support.
- `vcdecomp/core/disasm/disassembler.py` – resolver-aware disassembly and mnemonic based helpers.
- `vcdecomp/__main__.py` – CLI entry point with `--variant`.
