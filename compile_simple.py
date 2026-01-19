#!/usr/bin/env python3
"""
Simplest possible compilation wrapper.

Uses the existing compile.bat that works when you double-click it.
Monitors for output file creation.
"""
import sys
import time
from pathlib import Path
import subprocess

def compile_tt():
    """Compile tt.c using the existing compile.bat"""

    compiler_dir = Path(__file__).parent / 'original-resources' / 'compiler'
    output_scr = compiler_dir / 'tt.scr'
    output_h = compiler_dir / 'tt.h'
    compile_bat = compiler_dir / 'compile.bat'

    if not compile_bat.exists():
        print(f"ERROR: compile.bat not found: {compile_bat}")
        return False

    # Remove old outputs
    for f in [output_scr, output_h]:
        if f.exists():
            print(f"Removing old {f.name}...")
            f.unlink()

    print(f"\nRunning: {compile_bat.name}")
    print(f"Directory: {compiler_dir}")
    print("\nStarting compilation...")

    # Try to run the bat file using explorer (which definitely works from WSL)
    bat_win = str(compile_bat).replace('/', '\\')

    # Method 1: Use cmd /c
    print("Triggering compile.bat...")
    subprocess.Popen(
        f'cmd.exe /c "{bat_win}"',
        shell=True,
        cwd=str(compiler_dir)
    )

    # Monitor for output
    print("Monitoring for tt.scr", end='', flush=True)
    start_time = time.time()
    timeout = 30

    while time.time() - start_time < timeout:
        time.sleep(1)
        print('.', end='', flush=True)

        if output_scr.exists() and output_scr.stat().st_size > 0:
            time.sleep(0.5)  # Let it finish writing
            print("\n")
            size = output_scr.stat().st_size
            print(f"\n{'='*60}")
            print(f"SUCCESS: tt.scr created ({size:,} bytes)")
            print('='*60)

            if output_h.exists():
                print(f"Header: tt.h ({output_h.stat().st_size:,} bytes)")

            return True

    print("\n")
    print(f"TIMEOUT after {timeout} seconds")

    # Check if files exist now
    if output_scr.exists():
        print(f"Note: tt.scr was created ({output_scr.stat().st_size:,} bytes)")
        return True

    print("\nPlease try running compile.bat manually from Windows Explorer:")
    print(f"  {compiler_dir}\\compile.bat")

    return False


if __name__ == '__main__':
    print("="*60)
    print("Vietcong tt.c Compiler")
    print("="*60)
    success = compile_tt()
    sys.exit(0 if success else 1)
