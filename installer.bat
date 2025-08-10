@echo off
echo Windows System Diagnostic Agent Installer
echo ==========================================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This installer requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

:: Create program directory
set INSTALL_DIR=%ProgramFiles%\WindowsSystemDiagnostic
echo Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy executable
echo Copying application files...
copy "dist\WindowsSystemDiagnostic.exe" "%INSTALL_DIR%\" >nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy executable file
    pause
    exit /b 1
)

:: Create desktop shortcut
echo Creating desktop shortcut...
set DESKTOP=%PUBLIC%\Desktop
(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%DESKTOP%\Windows System Diagnostic.lnk"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "%INSTALL_DIR%\WindowsSystemDiagnostic.exe"
echo oLink.WorkingDirectory = "%INSTALL_DIR%"
echo oLink.Description = "Windows System Diagnostic Agent"
echo oLink.Save
) > temp_shortcut.vbs
cscript temp_shortcut.vbs >nul
del temp_shortcut.vbs

:: Create start menu entry
echo Creating start menu entry...
set STARTMENU=%ProgramData%\Microsoft\Windows\Start Menu\Programs
if not exist "%STARTMENU%\Windows System Diagnostic" mkdir "%STARTMENU%\Windows System Diagnostic"
(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%STARTMENU%\Windows System Diagnostic\Windows System Diagnostic.lnk"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "%INSTALL_DIR%\WindowsSystemDiagnostic.exe"
echo oLink.WorkingDirectory = "%INSTALL_DIR%"
echo oLink.Description = "Windows System Diagnostic Agent"
echo oLink.Save
) > temp_shortcut.vbs
cscript temp_shortcut.vbs >nul
del temp_shortcut.vbs

echo.
echo [SUCCESS] Installation completed successfully!
echo.
echo The Windows System Diagnostic Agent has been installed to:
echo %INSTALL_DIR%
echo.
echo You can find shortcuts on your desktop and in the start menu.
echo.
pause