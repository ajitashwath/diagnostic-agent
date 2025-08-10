@echo off
echo Starting Windows System Diagnostic Agent...
echo.

if not exist "dist\WindowsSystemDiagnostic.exe" (
    echo ERROR: WindowsSystemDiagnostic.exe not found in dist folder.
    echo Please make sure the executable has been built properly.
    pause
    exit /b 1
)

start "" "dist\WindowsSystemDiagnostic.exe"