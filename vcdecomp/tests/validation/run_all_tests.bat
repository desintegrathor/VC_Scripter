@echo off
REM Test runner for all validation unit tests (Windows)
REM
REM Usage: run_all_tests.bat

echo Running all validation unit tests...
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

REM Run compiler wrapper tests
echo.
echo ========================================
echo 1. Compiler Wrapper Tests
echo ========================================
%PYTHON% -m unittest vcdecomp.tests.validation.test_compiler_wrapper -v

if %errorlevel% neq 0 (
    echo.
    echo Compiler wrapper tests FAILED!
    set TEST_FAILED=1
)

REM Run bytecode comparison tests
echo.
echo ========================================
echo 2. Bytecode Comparison Tests
echo ========================================
%PYTHON% -m unittest vcdecomp.tests.validation.test_bytecode_compare -v

if %errorlevel% neq 0 (
    echo.
    echo Bytecode comparison tests FAILED!
    set TEST_FAILED=1
)

REM Summary
echo.
echo ========================================
echo Test Summary
echo ========================================

if defined TEST_FAILED (
    echo.
    echo Some tests FAILED!
    echo Please review the output above for details.
    exit /b 1
) else (
    echo.
    echo All tests PASSED!
    echo - Compiler wrapper tests: PASS
    echo - Bytecode comparison tests: PASS
    exit /b 0
)
