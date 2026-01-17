@echo off
REM Compile script for validation
REM Usage: compile_script.bat source.c output.scr output.h

REM Change to the directory where this bat file is located
cd /d "%~dp0"

REM Call scmp from the current directory
"%~dp0scmp.exe" "%1" "%2" "%3"
