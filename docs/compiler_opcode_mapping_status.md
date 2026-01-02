# Compiler Opcode Mapping – status

## Current coverage

The helper script (`python tools/extract_compiler_opcode_map.py`, temporary inline) walks every `.scr`/`sasm.dbg` pair under `Compiler-testruns/` and records the opcode value that SASM emitted for each mnemonic observed in the debug log. The latest run produced `docs/compiler_opcode_map_partial.json` with **85 / 150** entries populated directly from real compiler output. The remaining **65** opcodes never appear in the current test suites, so their numeric values are still unknown.

```
Missing compiler opcode ids:
3, 6, 9, 11, 13, 16, 21, 23, 28, 30,
33, 34, 38, 41, 42, 46, 48, 50, 52, 53,
57, 60, 62, 64, 67, 69, 70, 71, 73, 75,
76, 77, 78, 80, 82, 85, 86, 87, 89, 95,
98, 100, 101, 102, 107, 108, 109, 112, 113, 115,
118, 120, 122, 123, 124, 131, 132, 134, 135, 137,
139, 143, 144, 145, 149
```

## Next steps

1. **Targeted opcode harness:** auto-generate a synthetic `.sca` (or `.c`) that exercises every missing mnemonic exactly once, compile it with `sasm.exe`, and feed the resulting `.scr` + `.dbg` back into the extractor. Because SASM accepts human‑readable assembly, building a script from the existing template should be faster than trying to hit everything indirectly via C.
2. **Automate extraction:** move the quick-and-dirty extractor into a reusable tool (e.g., `tools/extract_compiler_opcode_map.py`), and wire it into docs so regenerating the full 0‑149 table is a single command.
3. **Publish final table:** once all 150 entries are observed, promote the JSON to a first-class asset (e.g., `vcdecomp/core/disasm/compiler_opcode_table.py`) so the resolver no longer depends on the partial `OPCODE_INFO` set.
