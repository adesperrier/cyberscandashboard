@echo off
REM ============================================================
REM CyberScan - One Click Installer Builder
REM ============================================================
REM This single file builds everything you need
REM ============================================================

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ============================================================
echo       CYBERSCAN - INSTALLER BUILDER
echo ============================================================
echo.
echo This will create: CyberScan-Setup.exe
echo Installation time: 5-10 minutes
echo.

REM Step 1: Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK
echo.

REM Step 2: Install dependencies
echo [2/5] Installing build tools...
pip install PyInstaller==6.1.0 -q
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo OK
echo.

REM Step 3: Clean old builds
echo [3/5] Cleaning old builds...
if exist build rmdir /s /q build >nul 2>&1
if exist dist rmdir /s /q dist >nul 2>&1
echo OK
echo.

REM Step 4: Build portable EXE
echo [4/5] Building CyberScan.exe (this takes 2-3 min)...
python -m PyInstaller ^
    --name CyberScan ^
    --onefile ^
    --console ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --hidden-import=flask ^
    --hidden-import=nmap ^
    --hidden-import=werkzeug ^
    --clean ^
    main.py >nul 2>&1

if not exist dist\CyberScan.exe (
    echo ERROR: Failed to build EXE
    pause
    exit /b 1
)
echo OK
echo.

REM Step 5: Check Inno Setup
echo [5/5] Checking Inno Setup...
set INNO_PATH=

if exist "C:\Program Files (x86)\Inno Setup 6\iscc.exe" (
    set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\iscc.exe"
) else if exist "C:\Program Files\Inno Setup 6\iscc.exe" (
    set "INNO_PATH=C:\Program Files\Inno Setup 6\iscc.exe"
) else if exist "C:\Program Files (x86)\Inno Setup 5\iscc.exe" (
    set "INNO_PATH=C:\Program Files (x86)\Inno Setup 5\iscc.exe"
) else if exist "C:\Program Files\Inno Setup 5\iscc.exe" (
    set "INNO_PATH=C:\Program Files\Inno Setup 5\iscc.exe"
)

if "!INNO_PATH!"=="" (
    echo.
    echo ============================================================
    echo WARNING: Inno Setup not found
    echo ============================================================
    echo.
    echo Please download and install Inno Setup:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo After installation, run this script again.
    echo.
    echo ============================================================
    echo.
    echo NOTE: Your portable EXE is ready in: dist\CyberScan.exe
    echo You can use it directly without installing!
    echo.
    pause
    exit /b 0
)

echo OK - Building installer...
"!INNO_PATH!" CyberScan.iss >nul 2>&1

if not exist "dist\CyberScan-Setup.exe" (
    echo ERROR: Failed to create installer
    pause
    exit /b 1
)

echo.
echo ============================================================
echo              SUCCESS!
echo ============================================================
echo.
echo Your installer is ready:
echo Location: dist\CyberScan-Setup.exe
echo.
echo Share this file with users!
echo They just need to double-click to install.
echo.
echo ============================================================
echo.
pause
start explorer dist
