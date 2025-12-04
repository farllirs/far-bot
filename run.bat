@echo off
REM Far-Bot Launcher for Windows

echo.
echo ╔════════════════════════════════╗
echo ║       Far-Bot Launcher          │
echo ║  Discord Bot Manager v1.0.0     │
echo ╚════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

REM Run installer if needed
if not exist "data" (
    echo First run detected, running installer...
    python installer.py
)

REM Run launcher
echo.
echo Starting Far-Bot...
echo.
python launcher.py
pause
