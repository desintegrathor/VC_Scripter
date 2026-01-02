# Runtime vs Compiler Variant Detection

The loader now heuristically decides whether a `.scr` file uses the runtime opcode layout (as seen in `logs.dll`) or the original compiler layout (as produced by SASM). Detection works by scanning every instruction and scoring how often jump/call opcodes reference valid code targets vs. how often the supposed `XCALL` opcode points into the XFN table. Manual overrides (`SCRFile.load(..., variant="runtime|compiler")` or `--variant` on the CLI/GUI) are still available.

## Current coverage

Running the loader with `variant="auto"` on all samples in `Compiler-testruns/` yields:

| Script | Instructions | Selected | Compiler Score | Runtime Score | Margin |
| --- | ---:| --- | ---:| ---:| ---:|
| `Compiler-testruns/opcodetest/opcode_test.scr` | 2 381 | compiler | 329.00 | −149.99 | +478.99 |
| `Compiler-testruns/Testrun1/tdm.scr` | 782 | compiler | 556.00 | −114.99 | +670.99 |
| `Compiler-testruns/Testrun2/Gaz_67.scr` | 1 079 | runtime | 358.00 | 622.01 | +264.01 |
| `Compiler-testruns/Testrun3/hitable.scr` | 53 | compiler | 30.00 | −76.99 | +106.99 |
| `Compiler-testruns/Testrun4/tt.scr` | 3 736 | compiler | 2 649.00 | −898.99 | +3 547.99 |
| `Compiler-testruns/Testrun5/realcoop.scr` | 6 184 | compiler | 4 881.00 | 477.01 | +4 403.99 |

Even the closest call (`hitable.scr`, margin +106.99) has a comfortable gap between the two scores, so the existing heuristic is sufficient for all known samples.

## Manual override

If a future script confuses the heuristic (e.g., a hand‑assembled runtime `.scr`), pass `variant="runtime"`/`"compiler"` to `SCRFile.load()` or add `--variant` on the CLI/GUI to force the resolver. `SCRFile.info()` prints the scores and whether the result was forced.
