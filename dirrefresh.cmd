@echo off
:a
dir /w /b .
timeout /t 15 /nobreak > nul
echo.
goto a