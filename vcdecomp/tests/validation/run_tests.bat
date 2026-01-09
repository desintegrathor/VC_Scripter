@echo off
REM Test runner for compiler wrapper unit tests (Windows)
REM
REM Usage: run_tests.bat

echo Running compiler wrapper unit tests...
echo ========================================
echo.

REM Try to find Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=python
    goto run_tests
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=py
    goto run_tests
)

echo Error: Python not found in PATH
exit /b 1

:run_tests
echo Using Python: %PYTHON%
%PYTHON% --version
echo.

REM Run tests with unittest
%PYTHON% -m unittest vcdecomp.tests.validation.test_compiler_wrapper -v

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo Tests FAILED!
    exit /b 1
)

echo.
echo ========================================
echo All tests passed!
