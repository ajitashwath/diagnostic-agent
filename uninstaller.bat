@echo off
echo Windows System Diagnostic Agent Uninstaller
echo ============================================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This uninstaller requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

set INSTALL_DIR=%ProgramFiles%\WindowsSystemDiagnostic

echo Removing application files...
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%"
    if %errorlevel% equ 0 (
        echo [SUCCESS] Application files removed
    ) else (
        echo [ERROR] Failed to remove application files
    )
) else (
    echo [INFO] Application directory not found
)

echo Removing desktop shortcut...
if exist "%PUBLIC%\Desktop\Windows System Diagnostic.lnk" (
    del "%PUBLIC%\Desktop\Windows System Diagnostic.lnk"
    if %errorlevel% equ 0 (
        echo [SUCCESS] Desktop shortcut removed
    ) else (
        echo [ERROR] Failed to remove desktop shortcut
    )
) else (
    echo [INFO] Desktop shortcut not found
)

echo Removing start menu entry...
if exist "%ProgramData%\Microsoft\Windows\Start Menu\Programs\Windows System Diagnostic" (
    rmdir /s /q "%ProgramData%\Microsoft\Windows\Start Menu\Programs\Windows System Diagnostic"
    if %errorlevel% equ 0 (
        echo [SUCCESS] Start menu entry removed
    ) else (
        echo [ERROR] Failed to remove start menu entry
    )
) else (
    echo [INFO] Start menu entry not found
)

echo.
echo [SUCCESS] Uninstallation completed successfully!
echo.
pause