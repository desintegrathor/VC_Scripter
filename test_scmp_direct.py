#!/usr/bin/env python3
"""Direct test of SCMP executable to diagnose issues."""

import subprocess
import shutil
from pathlib import Path

def test_direct_call():
    """Test calling SCMP directly like the batch file does."""
    compiler_dir = Path("./original-resources/compiler").absolute()
    test_source = Path("./Compiler-testruns/Testrun1/tdm.c").absolute()

    if not compiler_dir.exists():
        print(f"Compiler directory not found: {compiler_dir}")
        return

    if not test_source.exists():
        print(f"Test source not found: {test_source}")
        return

    # Copy source to compiler directory
    work_source = compiler_dir / "test_tdm.c"
    shutil.copy2(test_source, work_source)

    print(f"Compiler directory: {compiler_dir}")
    print(f"Source file: {work_source}")
    print(f"Executables present:")
    print(f"  scmp.exe: {(compiler_dir / 'scmp.exe').exists()}")
    print(f"  spp.exe: {(compiler_dir / 'spp.exe').exists()}")
    print(f"  scc.exe: {(compiler_dir / 'scc.exe').exists()}")
    print(f"  sasm.exe: {(compiler_dir / 'sasm.exe').exists()}")
    print(f"  inc/ directory: {(compiler_dir / 'inc').exists()}")

    # Try running SCMP
    print("\nAttempting to run SCMP...")
    cmd = [str(compiler_dir / "scmp.exe"), "test_tdm.c", "test_output.scr", "test_output.h"]
    print(f"Command: {' '.join(cmd)}")
    print(f"Working directory: {compiler_dir}")

    try:
        result = subprocess.run(
            cmd,
            cwd=str(compiler_dir),
            capture_output=True,
            text=True,
            timeout=30,
        )

        print(f"\nReturn code: {result.returncode}")
        print(f"Return code (hex): {hex(result.returncode & 0xFFFFFFFF)}")
        print(f"stdout: {result.stdout if result.stdout else '(empty)'}")
        print(f"stderr: {result.stderr if result.stderr else '(empty)'}")

        # Check for output files
        output_scr = compiler_dir / "test_output.scr"
        if output_scr.exists():
            print(f"\n✓ Output file created: {output_scr}")
            print(f"  Size: {output_scr.stat().st_size} bytes")
        else:
            print(f"\n✗ Output file not created")

        # Check for error files
        for err_file in ["spp.err", "scc.err", "sasm.err"]:
            err_path = compiler_dir / err_file
            if err_path.exists():
                print(f"\nError file {err_file}:")
                print(err_path.read_text(errors='replace'))

    except subprocess.TimeoutExpired:
        print("\n✗ Process timed out")
    except Exception as e:
        print(f"\n✗ Exception: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if work_source.exists():
            work_source.unlink()
        output_scr = compiler_dir / "test_output.scr"
        if output_scr.exists():
            output_scr.unlink()
        output_h = compiler_dir / "test_output.h"
        if output_h.exists():
            output_h.unlink()

if __name__ == "__main__":
    test_direct_call()
