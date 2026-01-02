@echo off
echo ========================================
echo Compiling all 12 bot scripts...
echo ========================================

REM US Bots
echo.
echo Compiling US bots...
scmp USBOT0.c USBOT0.scr USBOT0.h
if exist spp.err goto error
scmp USBOT1.c USBOT1.scr USBOT1.h
if exist spp.err goto error
scmp USBOT2.c USBOT2.scr USBOT2.h
if exist spp.err goto error
scmp USBOT3.c USBOT3.scr USBOT3.h
if exist spp.err goto error
scmp USBOT4.c USBOT4.scr USBOT4.h
if exist spp.err goto error
scmp USBOT5.c USBOT5.scr USBOT5.h
if exist spp.err goto error

REM VC Bots
echo.
echo Compiling VC bots...
scmp VCBOT0.c VCBOT0.scr VCBOT0.h
if exist spp.err goto error
scmp VCBOT1.c VCBOT1.scr VCBOT1.h
if exist spp.err goto error
scmp VCBOT2.c VCBOT2.scr VCBOT2.h
if exist spp.err goto error
scmp VCBOT3.c VCBOT3.scr VCBOT3.h
if exist spp.err goto error
scmp VCBOT4.c VCBOT4.scr VCBOT4.h
if exist spp.err goto error
scmp VCBOT5.c VCBOT5.scr VCBOT5.h
if exist spp.err goto error

echo.
echo ========================================
echo All 12 bot scripts compiled successfully!
echo ========================================
goto end

:error
echo.
echo ========================================
echo ERROR: Compilation failed!
echo ========================================
if exist spp.err type spp.err
if exist scc.err type scc.err
if exist sasm.err type sasm.err
pause

:end
