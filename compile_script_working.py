#!/usr/bin/env python3
"""
Working compilation script that handles WSL/Windows compatibility issues.
Creates a batch file and monitors for output files.
"""
import subprocess
import time
import sys
from pathlib import Path
import shutil

def compile_vietcong_script(source_file, output_dir=None):
    """
    Compile a Vietcong .c script to .scr bytecode.

    Args:
        source_file: Path to .c source file
        output_dir: Optional output directory (defaults to compiler directory)

    Returns:
        Path to the generated .scr file, or None if compilation failed
    """
    source_path = Path(source_file).resolve()

    if not source_path.exists():
        print(f"ERROR: Source file not found: {source_path}")
        return None

    # Determine compiler directory
    repo_root = Path(__file__).parent
    compiler_dir = repo_root / 'original-resources' / 'compiler'

    if not compiler_dir.exists():
        print(f"ERROR: Compiler directory not found: {compiler_dir}")
        return None

    # Copy source to compiler directory
    source_name = source_path.name
    source_in_compiler = compiler_dir / source_name

    if source_path != source_in_compiler:
        print(f"Copying {source_name} to compiler directory...")
        shutil.copy2(source_path, source_in_compiler)

    # Generate output filenames
    base_name = source_path.stem
    scr_file = compiler_dir / f"{base_name}.scr"
    h_file = compiler_dir / f"{base_name}.h"

    # Remove old output files
    for f in [scr_file, h_file]:
        if f.exists():
            f.unlink()

    # Create a temporary batch file with full paths
    compiler_dir_win = str(compiler_dir).replace('/', '\\')
    bat_content = f"""@echo off
cd /d "{compiler_dir_win}"
"%~dp0spp.exe" {source_name} spp.c inc
if errorlevel 1 exit /b 1
"%~dp0scc.exe" spp.c sasm.sca {scr_file.name} {h_file.name}
if errorlevel 1 exit /b 1
"%~dp0sasm.exe" sasm.sca {scr_file.name} {h_file.name}
exit /b %ERRORLEVEL%
"""

    bat_file = compiler_dir / "temp_compile.bat"
    bat_file.write_text(bat_content)

    print(f"\nCompiling {source_name}...")
    print(f"Working directory: {compiler_dir}")

    # Execute the batch file using Windows cmd
    try:
        # Use subprocess with Windows paths
        result = subprocess.run(
            ['cmd.exe', '/c', str(bat_file)],
            cwd=str(compiler_dir),
            timeout=30,
            capture_output=False  # Don't capture - WSL can't get output properly
        )

        # Wait a moment for file system to sync
        time.sleep(1)

        # Check for error files
        error_files = {
            'spp.err': 'Preprocessor',
            'scc.err': 'Compiler',
            'sasm.err': 'Assembler'
        }

        errors_found = False
        for err_name, stage in error_files.items():
            err_path = compiler_dir / err_name
            if err_path.exists() and err_path.stat().st_size > 0:
                print(f"\n{'='*60}")
                print(f"ERROR in {stage} ({err_name}):")
                print('='*60)
                print(err_path.read_text())
                errors_found = True

        if errors_found:
            return None

        # Check if output was created
        if scr_file.exists():
            size = scr_file.stat().st_size
            print(f"\nSUCCESS: {scr_file.name} created ({size:,} bytes)")

            if h_file.exists():
                h_size = h_file.stat().st_size
                print(f"Header: {h_file.name} created ({h_size:,} bytes)")

            # Show intermediate files
            print(f"\nIntermediate files:")
            for pattern in ['spp.c', 'sasm.sca', '*.syn', '*.cmp', '*.dbg']:
                for f in compiler_dir.glob(pattern):
                    if f.is_file():
                        print(f"  - {f.name} ({f.stat().st_size:,} bytes)")

            # Copy to output directory if specified
            if output_dir:
                output_dir = Path(output_dir)
                output_dir.mkdir(parents=True, exist_ok=True)
                out_scr = output_dir / scr_file.name
                shutil.copy2(scr_file, out_scr)
                print(f"\nCopied to: {out_scr}")
                if h_file.exists():
                    shutil.copy2(h_file, output_dir / h_file.name)

            return scr_file
        else:
            print(f"\nERROR: Compilation failed - {scr_file.name} not created")
            print(f"Exit code: {result.returncode}")
            return None

    except subprocess.TimeoutExpired:
        print("ERROR: Compilation timed out (30 seconds)")
        return None
    except Exception as e:
        print(f"ERROR: Compilation failed: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        # Clean up temp batch file
        if bat_file.exists():
            try:
                bat_file.unlink()
            except:
                pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: py -3 compile_script_working.py <source.c> [output_dir]")
        print("\nExamples:")
        print("  py -3 compile_script_working.py original-resources/compiler/tt.c")
        print("  py -3 compile_script_working.py decompiler_source_tests/test1/tt.c test_output/")
        sys.exit(1)

    source = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    result = compile_vietcong_script(source, output_dir)
    sys.exit(0 if result else 1)
