@echo off
REM Manual compilation script for testing
echo === Starting compilation ===
echo.

echo [1/3] Preprocessing with SPP...
spp.exe tt.c spp.c inc
if errorlevel 1 (
    echo ERROR in SPP
    if exist spp.err type spp.err
    exit /b 1
)
if not exist spp.c (
    echo ERROR: spp.c not created
    exit /b 1
)
echo SPP OK - spp.c created (%~z1 bytes)

echo.
echo [2/3] Compiling with SCC...
scc.exe spp.c sasm.sca tt.scr tt.h
if errorlevel 1 (
    echo ERROR in SCC
    if exist scc.err type scc.err
    exit /b 1
)
if not exist sasm.sca (
    echo ERROR: sasm.sca not created
    exit /b 1
)
echo SCC OK - sasm.sca created

echo.
echo [3/3] Assembling with SASM...
sasm.exe sasm.sca tt.scr tt.h
if errorlevel 1 (
    echo ERROR in SASM
    if exist sasm.err type sasm.err
    exit /b 1
)

echo.
echo === Compilation complete ===
if exist tt.scr (
    echo SUCCESS: tt.scr created
    dir tt.scr | find "tt.scr"
) else (
    echo ERROR: tt.scr not created
    exit /b 1
)

if exist tt.h (
    echo Header: tt.h created
)

echo.
echo Intermediate files:
dir /b spp.c sasm.sca *.syn *.dbg 2>nul
