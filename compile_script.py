#!/usr/bin/env python3
"""
Wrapper script to compile Vietcong scripts using the original SCMP compiler.
This handles the Windows/WSL bridge issue by invoking cmd.exe properly.
"""
import subprocess
import sys
import os
from pathlib import Path

def compile_script(source_file, output_scr=None, output_header=None, compiler_dir=None):
    """
    Compile a .c source file to .scr bytecode using SCMP compiler.

    Args:
        source_file: Path to the .c source file
        output_scr: Path to output .scr file (defaults to source_file with .scr extension)
        output_header: Path to output .h file (defaults to source_file with .h extension)
        compiler_dir: Directory containing scmp.exe (defaults to original-resources/compiler)
    """
    source_path = Path(source_file).resolve()

    if not source_path.exists():
        print(f"ERROR: Source file not found: {source_path}")
        return False

    # Set defaults
    if output_scr is None:
        output_scr = source_path.with_suffix('.scr')
    else:
        output_scr = Path(output_scr).resolve()

    if output_header is None:
        output_header = source_path.with_suffix('.h')
    else:
        output_header = Path(output_header).resolve()

    if compiler_dir is None:
        repo_root = Path(__file__).parent
        compiler_dir = repo_root / 'original-resources' / 'compiler'
    else:
        compiler_dir = Path(compiler_dir)

    if not compiler_dir.exists():
        print(f"ERROR: Compiler directory not found: {compiler_dir}")
        return False

    # Copy source file to compiler directory (if not already there)
    source_in_compiler = compiler_dir / source_path.name
    import shutil

    if source_path != source_in_compiler:
        print(f"Copying {source_path.name} to compiler directory...")
        try:
            shutil.copy2(source_path, source_in_compiler)
        except Exception as e:
            print(f"ERROR: Failed to copy source file: {e}")
            return False
    else:
        print(f"Source file already in compiler directory: {source_path.name}")

    # Build the command
    output_scr_name = output_scr.name
    output_header_name = output_header.name

    # Run directly from the compiler directory
    cmd = ['scmp.exe', source_path.name, output_scr_name, output_header_name]

    print(f"\nCompiling: {source_path.name}")
    print(f"Output .scr: {output_scr_name}")
    print(f"Output .h: {output_header_name}")
    print(f"Working directory: {compiler_dir}\n")

    # Run the compiler
    try:
        result = subprocess.run(
            cmd,
            cwd=str(compiler_dir),
            capture_output=True,
            text=True,
            timeout=60,
            shell=True
        )

        # Check for error files
        error_files = ['spp.err', 'scc.err', 'sasm.err']
        errors_found = False

        for err_file in error_files:
            err_path = compiler_dir / err_file
            if err_path.exists():
                print(f"\n{'='*60}")
                print(f"ERROR in {err_file}:")
                print('='*60)
                print(err_path.read_text())
                errors_found = True

        if errors_found:
            return False

        # Check if output files were created
        output_scr_path = compiler_dir / output_scr_name
        output_header_path = compiler_dir / output_header_name

        if output_scr_path.exists():
            print(f"SUCCESS: {output_scr_name} created ({output_scr_path.stat().st_size} bytes)")

            # Copy output files back to desired location
            if output_scr != output_scr_path:
                shutil.copy2(output_scr_path, output_scr)
                print(f"  Copied to: {output_scr}")

            if output_header_path.exists() and output_header != output_header_path:
                shutil.copy2(output_header_path, output_header)
                print(f"Header file: {output_header_name} created")

            # Show intermediate files
            print(f"\nIntermediate files created:")
            for pattern in ['*.syn', '*.cmp', 'spp.c', 'sasm.sca']:
                for f in compiler_dir.glob(pattern):
                    print(f"  - {f.name} ({f.stat().st_size} bytes)")

            return True
        else:
            print(f"ERROR: Compilation failed - {output_scr_name} not created")
            print(f"\nCompiler returned exit code: {result.returncode}")
            if result.stdout:
                print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("ERROR: Compilation timed out (60 seconds)")
        return False
    except Exception as e:
        print(f"ERROR: Compilation failed with exception: {e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python compile_script.py <source.c> [output.scr] [output.h]")
        print("\nExample:")
        print("  python compile_script.py decompiler_source_tests/test1/tt.c")
        print("  python compile_script.py tt.c tt_compiled.scr tt_compiled.h")
        sys.exit(1)

    source = sys.argv[1]
    output_scr = sys.argv[2] if len(sys.argv) > 2 else None
    output_h = sys.argv[3] if len(sys.argv) > 3 else None

    success = compile_script(source, output_scr, output_h)
    sys.exit(0 if success else 1)
