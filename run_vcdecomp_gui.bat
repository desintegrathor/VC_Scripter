@echo off
REM Launch the VC Script Decompiler GUI from the repository root.
REM Optional argument: path to a .scr file that should be opened immediately.

setlocal
set SCRIPT_DIR=%~dp0
pushd "%SCRIPT_DIR%"

py -m vcdecomp gui %*

if errorlevel 1 (
    echo.
    echo Failed to launch VC Script Decompiler GUI.
    echo Make sure Python and project dependencies are installed.
    echo.
    echo If 'py' command is not found, you may need to:
    echo 1. Install Python from python.org
    echo 2. Or use: python3 -m vcdecomp gui
)

popd
endlocal