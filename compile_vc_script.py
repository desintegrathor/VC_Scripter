#!/usr/bin/env python3
"""
Vietcong Script Compiler - WSL-compatible wrapper

This works around WSL/Windows command-line argument passing issues
by using SCMP.exe directly, which handles the compilation pipeline.
"""
import subprocess
import sys
import time
from pathlib import Path
import shutil

def compile_script(source_file, output_scr=None, output_h=None):
    """
    Compile a Vietcong .c script using SCMP.exe

    Args:
        source_file: Path to source .c file
        output_scr: Optional output .scr filename (default: same as source)
        output_h: Optional output .h filename (default: same as source)

    Returns:
        True if compilation succeeded, False otherwise
    """
    source_path = Path(source_file).resolve()

    if not source_path.exists():
        print(f"ERROR: Source file not found: {source_path}")
        return False

    # Find compiler directory
    repo_root = Path(__file__).parent
    compiler_dir = repo_root / 'original-resources' / 'compiler'

    if not (compiler_dir / 'scmp.exe').exists():
        print(f"ERROR: SCMP compiler not found in: {compiler_dir}")
        return False

    # Determine output filenames
    base_name = source_path.stem
    if output_scr is None:
        output_scr = f"{base_name}.scr"
    if output_h is None:
        output_h = f"{base_name}.h"

    # Copy source to compiler directory
    source_in_compiler = compiler_dir / source_path.name
    if source_path != source_in_compiler:
        print(f"Copying {source_path.name} to compiler directory...")
        shutil.copy2(source_path, source_in_compiler)

    # Clean up old output files
    for f in [compiler_dir / output_scr, compiler_dir / output_h]:
        if f.exists():
            f.unlink()

    # Clean up error files
    for err in ['spp.err', 'scc.err', 'sasm.err']:
        err_file = compiler_dir / err
        if err_file.exists():
            err_file.unlink()

    print(f"\nCompiling: {source_path.name}")
    print(f"Output: {output_scr}, {output_h}")
    print(f"Compiler directory: {compiler_dir}\n")

    # Create a response file to pass arguments (workaround for WSL)
    # SCMP syntax: scmp.exe source.c output.scr output.h
    response_file = compiler_dir / "compile_args.txt"
    response_file.write_text(f"{source_path.name}\n{output_scr}\n{output_h}\n")

    # Try calling SCMP through a batch file that reads the response file
    batch_content = f"""@echo off
cd /d "%~dp0"
set /p SRC=<compile_args.txt
for /f "skip=1 tokens=*" %%a in (compile_args.txt) do (
    set SCR=%%a
    goto :got_scr
)
:got_scr
for /f "skip=2 tokens=*" %%a in (compile_args.txt) do (
    set HDR=%%a
    goto :got_hdr
)
:got_hdr
scmp.exe %SRC% %SCR% %HDR%
exit /b %ERRORLEVEL%
"""

    batch_file = compiler_dir / "do_compile.bat"
    batch_file.write_text(batch_content)

    try:
        # Run the batch file
        result = subprocess.run(
            ['cmd.exe', '/c', str(batch_file)],
            cwd=str(compiler_dir),
            timeout=30,
            capture_output=True,
            text=True
        )

        # Wait for filesystem sync
        time.sleep(0.5)

        # Check for errors
        errors = []
        for err_name in ['spp.err', 'scc.err', 'sasm.err']:
            err_path = compiler_dir / err_name
            if err_path.exists() and err_path.stat().st_size > 0:
                errors.append(f"\n{'='*60}\nERROR in {err_name}:\n{'='*60}\n{err_path.read_text()}")

        if errors:
            for err in errors:
                print(err)
            return False

        # Check if output was created
        output_path = compiler_dir / output_scr
        if output_path.exists():
            size = output_path.stat().st_size
            print(f"\n{'='*60}")
            print(f"SUCCESS: {output_scr} created ({size:,} bytes)")
            print('='*60)

            h_path = compiler_dir / output_h
            if h_path.exists():
                h_size = h_path.stat().st_size
                print(f"Header: {output_h} ({h_size:,} bytes)")

            # Show intermediate files
            print(f"\nIntermediate files:")
            for pattern in ['spp.c', 'sasm.sca', '*.syn', '*.cmp']:
                for f in compiler_dir.glob(pattern):
                    if f.is_file() and f.stat().st_size > 0:
                        print(f"  {f.name} ({f.stat().st_size:,} bytes)")

            return True
        else:
            print(f"\nERROR: Compilation failed - {output_scr} not created")
            if result.stdout:
                print(f"STDOUT: {result.stdout}")
            if result.stderr:
                print(f"STDERR: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("ERROR: Compilation timed out (30 seconds)")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        for f in [response_file, batch_file]:
            if f.exists():
                try:
                    f.unlink()
                except:
                    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Vietcong Script Compiler")
        print("=" * 60)
        print("\nUsage: py -3 compile_vc_script.py <source.c> [output.scr] [output.h]")
        print("\nExamples:")
        print("  py -3 compile_vc_script.py decompiler_source_tests/test1/tt.c")
        print("  py -3 compile_vc_script.py original-resources/compiler/tt.c tt_out.scr tt_out.h")
        sys.exit(1)

    source = sys.argv[1]
    out_scr = sys.argv[2] if len(sys.argv) > 2 else None
    out_h = sys.argv[3] if len(sys.argv) > 3 else None

    success = compile_script(source, out_scr, out_h)
    sys.exit(0 if success else 1)
