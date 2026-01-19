@echo off
echo Testing direct compilation...
echo Working directory: %CD%
echo.

echo [Step 1] Running SPP...
"%~dp0spp.exe" tt.c spp.c inc
if errorlevel 1 (
    echo SPP FAILED
    if exist spp.err type spp.err
    pause
    exit /b 1
)
echo SPP OK
echo.

echo [Step 2] Running SCC...
"%~dp0scc.exe" spp.c sasm.sca tt.scr tt.h
if errorlevel 1 (
    echo SCC FAILED
    if exist scc.err type scc.err
    pause
    exit /b 1
)
echo SCC OK
echo.

echo [Step 3] Running SASM...
"%~dp0sasm.exe" sasm.sca tt.scr tt.h
if errorlevel 1 (
    echo SASM FAILED
    if exist sasm.err type sasm.err
    pause
    exit /b 1
)
echo SASM OK
echo.

if exist tt.scr (
    echo SUCCESS! tt.scr created
    dir tt.scr
) else (
    echo FAILED - tt.scr not found
)

pause
