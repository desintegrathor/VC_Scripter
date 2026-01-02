@echo off
REM Launch the VC Script Decompiler GUI from the repository root.
REM Optional argument: path to a .scr file that should be opened immediately.

setlocal
set SCRIPT_DIR=%~dp0
pushd "%SCRIPT_DIR%"

python -m vcdecomp gui %*

if errorlevel 1 (
    echo.
    echo Failed to launch VC Script Decompiler GUI.
    echo Make sure Python and project dependencies are installed.
)

popd
endlocal
