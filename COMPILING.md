# How to Compile Vietcong Scripts

This document explains how to compile Vietcong `.c` scripts to `.scr` bytecode using the original SCMP compiler.

## Quick Start

To compile `tt.c` (the test file in `original-resources/compiler`):

```bash
py -3 compile_simple.py
```

This will compile `tt.c` and create `tt.scr` and `tt.h` in the compiler directory.

## The Problem: WSL/Windows Compatibility

The original Vietcong compiler tools (scmp.exe, spp.exe, scc.exe, sasm.exe) are Windows executables from 2003. When invoked from WSL (Windows Subsystem for Linux), they have issues receiving command-line arguments properly. This is a known WSL interop limitation.

**What works:**
- Double-clicking `compile.bat` in Windows Explorer ✓
- Running batch files that use `%~dp0` for paths ✓

**What doesn't work:**
- Direct invocation: `./scmp.exe source.c output.scr output.h` ✗
- PowerShell from WSL with arguments ✗
- Python subprocess with arguments to .exe files ✗

## The Solution

We use a Python wrapper (`compile_simple.py`) that:
1. Triggers the batch file using `cmd.exe /c`
2. Monitors for the output `.scr` file to appear
3. Reports success when the file is created

### Key Fix

The `compile.bat` file was updated to use `%~dp0` to reference executables:

```batch
"%~dp0scmp" "tt.c" "tt.scr" "tt.h"
```

This ensures `scmp.exe` is found even when the batch file is invoked from a different context.

## Compilation Pipeline

The SCMP compiler runs a 3-stage pipeline:

```
.c → [SPP] → [SCC] → [SASM] → .scr
```

1. **SPP.exe** (Preprocessor)
   - Expands `#include`, `#define`, macros
   - Input: `source.c`
   - Output: `spp.c` (preprocessed C code)

2. **SCC.exe** (Compiler)
   - Compiles C to assembly
   - Input: `spp.c`
   - Output: `sasm.sca` (assembly code)

3. **SASM.exe** (Assembler)
   - Assembles to bytecode
   - Input: `sasm.sca`
   - Output: `output.scr` (bytecode), `output.h` (header)

### Intermediate Files Created

After compilation, you'll see:
- `spp.c` - Preprocessed source (includes expanded)
- `sasm.sca` - Assembly code
- `*.syn` - Symbol maps
- `*.dbg` - Debug information
- `*.cmp` - Compilation metadata
- `sav_file.scc` - Compiler state

### Error Files

If compilation fails, check:
- `spp.err` - Preprocessor errors
- `scc.err` - Compiler errors
- `sasm.err` - Assembler errors

## Manual Compilation (Alternative)

If the Python script doesn't work, you can always compile manually:

1. Open Windows Explorer
2. Navigate to: `C:\Users\flori\source\repos\VC_Scripter\original-resources\compiler`
3. Double-click `compile.bat`
4. The output files (`tt.scr`, `tt.h`) will be created in the same directory

## Compiling Other Files

To compile a different script:

### Option 1: Modify compile.bat

Edit `original-resources/compiler/compile.bat`:

```batch
"%~dp0scmp" "your_file.c" "your_file.scr" "your_file.h"
```

Then run:
```bash
py -3 compile_simple.py
```

### Option 2: Copy to compiler directory

1. Copy your `.c` file to `original-resources/compiler/`
2. Update `compile.bat` to reference it
3. Run the compilation script

## Requirements

- Windows with WSL
- Python 3
- Original compiler tools in `original-resources/compiler/`:
  - `scmp.exe`
  - `spp.exe`
  - `scc.exe`
  - `sasm.exe`
- Header files in `original-resources/compiler/inc/`:
  - `sc_global.h`
  - `sc_def.h`
  - `sc_MPglobal.h`
  - etc.

## Verifying Output

After compilation, verify the output with the decompiler:

```bash
# Show script info
py -3 -m vcdecomp info original-resources/compiler/tt.scr

# Decompile to check output
py -3 -m vcdecomp structure original-resources/compiler/tt.scr > tt_decompiled.c

# Validate (requires original source)
py -3 -m vcdecomp validate original-resources/compiler/tt.scr decompiler_source_tests/test1/tt.c
```

## Troubleshooting

### "scmp is not recognized"

**Problem:** The batch file cannot find scmp.exe

**Solution:** Make sure `compile.bat` uses `%~dp0`:
```batch
"%~dp0scmp" "source.c" "output.scr" "output.h"
```

### "bad parameter count sent to program"

**Problem:** SPP.exe is not receiving arguments correctly

**Solution:** This happens when executables are invoked directly from WSL. Use the batch file wrapper instead.

### Compilation hangs/times out

**Problem:** The compiler is still running in the background

**Solutions:**
- Wait longer (compilation can take 10-15 seconds)
- Check Task Manager for `scmp.exe`, `spp.exe`, `scc.exe`, or `sasm.exe` processes
- Try running `compile.bat` directly from Windows Explorer

### No output file created

**Problem:** Compilation failed silently

**Solutions:**
1. Check for error files: `spp.err`, `scc.err`, `sasm.err`
2. Check intermediate files exist: `spp.c`, `sasm.sca`
3. Run manually from Windows Explorer to see error messages

## Technical Details

### Why %~dp0?

`%~dp0` is a batch file variable that expands to the directory path of the batch file itself. This ensures executables are found regardless of the current working directory or how the batch file is invoked.

### WSL Argument Passing Issue

When WSL invokes Windows executables, command-line arguments containing special characters or spaces can be corrupted. The executables see `argc==2` but `argv[1]==''` (empty string).

This is logged in `spp.dbg`:
```
GetArgcArgv(): cmdln=='"C:\...\spp.exe" tt.c spp.c inc'
GetArgcArgv(): argc==2
GetArgcArgv(): argv[0]=='C:\...\spp.exe'
GetArgcArgv(): argv[1]==''  ← Arguments lost!
```

### Why Monitoring Works

Since we can't capture stdout/stderr from WSL-launched Windows processes reliably, we instead:
1. Delete the old output file
2. Trigger the batch file
3. Poll the filesystem for the new output file
4. Report success when it appears

This "file-watching" approach works around all the WSL interop issues.

## See Also

- [CLAUDE.md](CLAUDE.md) - Main project documentation
- [docs/SCMP_TECHNICAL.md](docs/SCMP_TECHNICAL.md) - Detailed compiler analysis
- [docs/SPP_TECHNICAL.md](docs/SPP_TECHNICAL.md) - Preprocessor internals
- [docs/SCC_TECHNICAL_ANALYSIS.md](docs/SCC_TECHNICAL_ANALYSIS.md) - Compiler internals
- [docs/SASM_TECHNICAL_ANALYSIS.md](docs/SASM_TECHNICAL_ANALYSIS.md) - Assembler internals
