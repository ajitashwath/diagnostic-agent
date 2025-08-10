"""
Fixed build script to create executable files for the Windows System Diagnostic Agent.
This version handles Unicode characters properly.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")

def create_spec_file():
    """Create PyInstaller spec file for better control over the build."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/laptop_repair/config/*.yaml', 'src/laptop_repair/config/'),
        ('src/laptop_repair/tools/*.py', 'src/laptop_repair/tools/'),
        ('src/laptop_repair/*.py', 'src/laptop_repair/'),
    ],
    hiddenimports=[
        'crewai',
        'yaml',
        'pydantic',
        'subprocess',
        'threading',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WindowsSystemDiagnostic',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('diagnostic_app.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content.strip())
    
    print("✓ Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    
    # Create the spec file
    create_spec_file()
    
    # Build using the spec file
    try:
        subprocess.check_call([
            'pyinstaller',
            '--clean',
            '--noconfirm',
            'diagnostic_app.spec'
        ])
        print("✓ Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False
    
    return True

def create_installer_script():
    """Create a simple batch installer script without Unicode characters."""
    installer_content = '''@echo off
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
set INSTALL_DIR=%ProgramFiles%\\WindowsSystemDiagnostic
echo Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy executable
echo Copying application files...
copy "dist\\WindowsSystemDiagnostic.exe" "%INSTALL_DIR%\\" >nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy executable file
    pause
    exit /b 1
)

:: Create desktop shortcut
echo Creating desktop shortcut...
set DESKTOP=%PUBLIC%\\Desktop
(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%DESKTOP%\\Windows System Diagnostic.lnk"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "%INSTALL_DIR%\\WindowsSystemDiagnostic.exe"
echo oLink.WorkingDirectory = "%INSTALL_DIR%"
echo oLink.Description = "Windows System Diagnostic Agent"
echo oLink.Save
) > temp_shortcut.vbs
cscript temp_shortcut.vbs >nul
del temp_shortcut.vbs

:: Create start menu entry
echo Creating start menu entry...
set STARTMENU=%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs
if not exist "%STARTMENU%\\Windows System Diagnostic" mkdir "%STARTMENU%\\Windows System Diagnostic"
(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%STARTMENU%\\Windows System Diagnostic\\Windows System Diagnostic.lnk"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "%INSTALL_DIR%\\WindowsSystemDiagnostic.exe"
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
'''
    
    try:
        with open('installer.bat', 'w', encoding='ascii', errors='replace') as f:
            f.write(installer_content.strip())
        print("✓ Created installer script")
    except Exception as e:
        print(f"✗ Error creating installer script: {e}")

def create_uninstaller_script():
    """Create an uninstaller script without Unicode characters."""
    uninstaller_content = '''@echo off
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

set INSTALL_DIR=%ProgramFiles%\\WindowsSystemDiagnostic

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
if exist "%PUBLIC%\\Desktop\\Windows System Diagnostic.lnk" (
    del "%PUBLIC%\\Desktop\\Windows System Diagnostic.lnk"
    if %errorlevel% equ 0 (
        echo [SUCCESS] Desktop shortcut removed
    ) else (
        echo [ERROR] Failed to remove desktop shortcut
    )
) else (
    echo [INFO] Desktop shortcut not found
)

echo Removing start menu entry...
if exist "%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\Windows System Diagnostic" (
    rmdir /s /q "%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\Windows System Diagnostic"
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
'''
    
    try:
        with open('uninstaller.bat', 'w', encoding='ascii', errors='replace') as f:
            f.write(uninstaller_content.strip())
        print("✓ Created uninstaller script")
    except Exception as e:
        print(f"✗ Error creating uninstaller script: {e}")


def create_launch_script():
    """Create a simple launch script for the portable version."""
    launch_content = '''@echo off
echo Starting Windows System Diagnostic Agent...
echo.

if not exist "dist\\WindowsSystemDiagnostic.exe" (
    echo ERROR: WindowsSystemDiagnostic.exe not found in dist folder.
    echo Please make sure the executable has been built properly.
    pause
    exit /b 1
)

start "" "dist\\WindowsSystemDiagnostic.exe"
'''
    
    try:
        with open('launch.bat', 'w', encoding='ascii') as f:
            f.write(launch_content.strip())
        print("✓ Created launch script")
    except Exception as e:
        print(f"✗ Error creating launch script: {e}")

def main():
    print("    Windows System Diagnostic Agent - Build Script")
    print("=" * 60)
    
    # Check if main_gui.py exists
    if not os.path.exists('main_gui.py'):
        print("✗ main_gui.py not found. Please ensure the GUI file exists.")
        return
    
    # Check if src directory exists
    if not os.path.exists('src'):
        print("✗ src directory not found. Please ensure the source files exist.")
        return
    
    # Check dependencies
    print("\n[1/7] Checking dependencies...")
    check_dependencies()
    

    
    # Build executable
    print("\n[3/7] Building executable...")
    if build_executable():
        print("\n[4/7] Creating installer script...")
        create_installer_script()
        
        print("\n[5/7] Creating uninstaller script...")
        create_uninstaller_script()
        
        
        print("\n[7/7] Creating launch script...")
        create_launch_script()
        
        print("\n" + "=" * 60)
        print("    BUILD PROCESS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print("\nFiles created:")
        print("  - dist/WindowsSystemDiagnostic.exe (Main executable)")
        print("  - installer.bat (Installation script)")
        print("  - uninstaller.bat (Uninstallation script)")
        print("  - launch.bat (Quick launch script)")
        print("  - README.md (Usage instructions)")
        print("  - requirements.txt (Python dependencies)")
        
        print("\nDistribution options:")
        print("  1. Use installer.bat for full system installation")
        print("  2. Use launch.bat for portable execution")
        print("  3. Distribute WindowsSystemDiagnostic.exe standalone")
        
        print("\nNext steps:")
        print("  1. Test the executable: dist\\WindowsSystemDiagnostic.exe")
        print("  2. Test the installer: Right-click installer.bat -> Run as administrator")
        print("  3. Create distribution package (ZIP all files)")
        
    else:
        print("\n✗ Build process failed!")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()