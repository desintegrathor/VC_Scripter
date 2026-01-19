#!/usr/bin/env python3
"""
Vietcong Script Compiler - Working WSL/Windows bridge

This script works around the WSL command-line argument passing limitation
by creating a custom batch file and monitoring for output files.

Since WSL cannot pass arguments to Windows executables properly, we:
1. Create a batch file with hardcoded arguments
2. Trigger it via explorer.exe (which works from WSL)
3. Monitor for the output .scr file to appear
"""
import sys
import time
from pathlib import Path
import shutil
import subprocess

def compile_vc_script(source_file, timeout=30):
    """
    Compile a Vietcong .c script to .scr bytecode.

    Args:
        source_file: Path to the .c source file
        timeout: Maximum time to wait for compilation (seconds)

    Returns:
        Path to the generated .scr file, or None if failed
    """
    source_path = Path(source_file).resolve()

    if not source_path.exists():
        print(f"ERROR: Source file not found: {source_path}")
        return None

    # Locate compiler directory
    repo_root = Path(__file__).parent
    compiler_dir = repo_root / 'original-resources' / 'compiler'

    if not (compiler_dir / 'scmp.exe').exists():
        print(f"ERROR: Compiler not found in: {compiler_dir}")
        return None

    # Copy source to compiler directory
    source_in_compiler = compiler_dir / source_path.name

    if source_path != source_in_compiler:
        print(f"Copying {source_path.name} to compiler directory...")
        shutil.copy2(source_path, source_in_compiler)
    else:
        print(f"Source file already in compiler directory: {source_path.name}")

    # Determine output filenames
    base_name = source_path.stem
    output_scr = compiler_dir / f"{base_name}.scr"
    output_h = compiler_dir / f"{base_name}.h"

    # Remove old outputs to detect new compilation
    for f in [output_scr, output_h]:
        if f.exists():
            print(f"Removing old {f.name}...")
            f.unlink()

    # Remove error files
    for err in ['spp.err', 'scc.err', 'sasm.err']:
        err_file = compiler_dir / err
        if err_file.exists():
            err_file.unlink()

    # Create a custom batch file for this compilation
    batch_content = f'''@echo off
cd /d "%~dp0"
scmp "{source_path.name}" "{base_name}.scr" "{base_name}.h"
'''

    batch_file = compiler_dir / "auto_compile.bat"
    batch_file.write_text(batch_content)

    print(f"\nCompiling: {source_path.name}")
    print(f"Expected output: {base_name}.scr, {base_name}.h")
    print(f"Working directory: {compiler_dir}")
    print("\nStarting compilation via Windows...")

    # Execute the batch file using Windows explorer (works from WSL)
    # We use start command which doesn't wait, so we monitor for files
    try:
        # Convert to Windows path
        batch_file_win = str(batch_file).replace('/', '\\')

        # Start the batch file - run it directly without 'start'
        subprocess.Popen(
            ['cmd.exe', '/c', batch_file_win],
            cwd=str(compiler_dir),
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )

        # Monitor for output file creation
        print("Waiting for compilation to complete", end='', flush=True)
        start_time = time.time()

        while time.time() - start_time < timeout:
            time.sleep(0.5)
            print('.', end='', flush=True)

            # Check if output file exists and has content
            if output_scr.exists() and output_scr.stat().st_size > 0:
                # Give it a moment to finish writing
                time.sleep(0.5)
                print("\n")
                break
        else:
            print("\n")
            print(f"TIMEOUT: Compilation did not complete within {timeout} seconds")

            # Check for error files
            errors_found = False
            for err_name in ['spp.err', 'scc.err', 'sasm.err']:
                err_path = compiler_dir / err_name
                if err_path.exists() and err_path.stat().st_size > 0:
                    print(f"\n{'='*60}")
                    print(f"ERROR in {err_name}:")
                    print('='*60)
                    print(err_path.read_text())
                    errors_found = True

            if not errors_found:
                print("\nNo error files found - compilation may still be running.")
                print("Please check the compiler directory manually.")

            return None

        # Check for errors even if file was created
        errors_found = False
        for err_name in ['spp.err', 'scc.err', 'sasm.err']:
            err_path = compiler_dir / err_name
            if err_path.exists() and err_path.stat().st_size > 0:
                print(f"\n{'='*60}")
                print(f"ERROR in {err_name}:")
                print('='*60)
                print(err_path.read_text())
                errors_found = True

        if errors_found:
            return None

        # Verify output file
        if output_scr.exists():
            size = output_scr.stat().st_size
            print('='*60)
            print(f"SUCCESS: {output_scr.name} created ({size:,} bytes)")
            print('='*60)

            if output_h.exists():
                h_size = output_h.stat().st_size
                print(f"Header: {output_h.name} ({h_size:,} bytes)")

            # Show intermediate files
            print(f"\nIntermediate files created:")
            for pattern in ['spp.c', 'sasm.sca', '*.syn', '*.cmp', 'spp.dbg', 'scc.dbg', 'sasm.dbg']:
                for f in compiler_dir.glob(pattern):
                    if f.is_file() and f.stat().st_size > 0:
                        print(f"  {f.name} ({f.stat().st_size:,} bytes)")

            return output_scr
        else:
            print(f"\nERROR: {output_scr.name} was not created")
            return None

    except Exception as e:
        print(f"\nERROR: Compilation failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        # Clean up temporary batch file
        if batch_file.exists():
            try:
                # Wait a moment before deleting
                time.sleep(0.5)
                batch_file.unlink()
            except:
                pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("="*60)
        print("Vietcong Script Compiler")
        print("="*60)
        print("\nCompiles Vietcong .c scripts to .scr bytecode")
        print("\nUsage:")
        print(f"  py -3 {Path(__file__).name} <source.c>")
        print("\nExamples:")
        print(f"  py -3 {Path(__file__).name} original-resources/compiler/tt.c")
        print(f"  py -3 {Path(__file__).name} decompiler_source_tests/test1/tt.c")
        print("\nNote: Output files (.scr and .h) are created in:")
        print("  original-resources/compiler/")
        print("\nThis script works around WSL/Windows command-line limitations")
        print("by creating a temporary batch file and monitoring for output.")
        sys.exit(1)

    source = sys.argv[1]
    result = compile_vc_script(source)

    sys.exit(0 if result else 1)
