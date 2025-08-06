@echo off
echo ================================================
echo Carwash Management System - Windows Installer
echo ================================================
echo.

REM Check if Python is installed - try multiple common locations
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_found
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :python_found
)

py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_found
)

REM Try common installation paths
if exist "C:\Python*\python.exe" (
    for /d %%i in ("C:\Python*") do (
        if exist "%%i\python.exe" (
            set PYTHON_CMD="%%i\python.exe"
            goto :python_found
        )
    )
)

REM Try AppData local installation
if exist "%LOCALAPPDATA%\Programs\Python\Python*\python.exe" (
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%i\python.exe" (
            set PYTHON_CMD="%%i\python.exe"
            goto :python_found
        )
    )
)

echo ERROR: Python is not found
echo.
echo Python installation options:
echo 1. Download from https://python.org
echo 2. During installation, CHECK "Add Python to PATH"
echo 3. Or use Microsoft Store version (search "Python" in Store)
echo.
echo If Python is already installed, try these commands manually:
echo   python --version
echo   python3 --version  
echo   py --version
echo.
pause
exit /b 1

:python_found

echo Python detected:
%PYTHON_CMD% --version
echo.

echo Installing required packages...
%PYTHON_CMD% -m pip install openpyxl
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
echo %PYTHON_CMD% carwash_app.py >> run_carwash.bat
echo if errorlevel 1 ( >> run_carwash.bat
echo     echo. >> run_carwash.bat
echo     echo Error: Application failed to start >> run_carwash.bat
echo     echo Please check that Python and openpyxl are installed >> run_carwash.bat
echo     echo. >> run_carwash.bat
echo ^) >> run_carwash.bat
echo pause >> run_carwash.bat

echo Created 'run_carwash.bat' for easy launching
echo.
pause