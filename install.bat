@echo off
echo ================================================
echo Carwash Management System - Windows Installer
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python detected:
python --version
echo.

echo Installing required packages...
pip install openpyxl
if errorlevel 1 (
    echo ERROR: Failed to install openpyxl
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ================================================
echo Installation completed successfully!
echo ================================================
echo.
echo To run the Carwash Management System:
echo   1. Double-click on 'run_carwash.bat'
echo   OR
echo   2. Open command prompt and run: python carwash_app.py
echo.

REM Create run script
echo @echo off > run_carwash.bat
echo echo Starting Carwash Management System... >> run_carwash.bat
echo python carwash_app.py >> run_carwash.bat
echo pause >> run_carwash.bat

echo Created 'run_carwash.bat' for easy launching
echo.
pause