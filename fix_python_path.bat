@echo off
echo ================================================
echo Python Path Fixer for Carwash Management System
echo ================================================
echo.

echo Searching for Python installations...
echo.

REM Try to find Python in common locations
set FOUND_PYTHON=

REM Check if python command works
python --version >nul 2>&1
if not errorlevel 1 (
    echo Found: python command works
    set FOUND_PYTHON=python
    goto :found
)

REM Check if python3 command works
python3 --version >nul 2>&1
if not errorlevel 1 (
    echo Found: python3 command works
    set FOUND_PYTHON=python3
    goto :found
)

REM Check if py launcher works
py --version >nul 2>&1
if not errorlevel 1 (
    echo Found: py launcher works
    set FOUND_PYTHON=py
    goto :found
)

echo Searching in Program Files...
if exist "C:\Program Files\Python*" (
    for /d %%i in ("C:\Program Files\Python*") do (
        if exist "%%i\python.exe" (
            echo Found: %%i\python.exe
            set FOUND_PYTHON="%%i\python.exe"
            goto :found
        )
    )
)

echo Searching in Program Files (x86)...
if exist "C:\Program Files (x86)\Python*" (
    for /d %%i in ("C:\Program Files (x86)\Python*") do (
        if exist "%%i\python.exe" (
            echo Found: %%i\python.exe
            set FOUND_PYTHON="%%i\python.exe"
            goto :found
        )
    )
)

echo Searching in AppData...
if exist "%LOCALAPPDATA%\Programs\Python\Python*" (
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%i\python.exe" (
            echo Found: %%i\python.exe
            set FOUND_PYTHON="%%i\python.exe"
            goto :found
        )
    )
)

echo Searching in User directory...
if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python*" (
    for /d %%i in ("%USERPROFILE%\AppData\Local\Programs\Python\Python*") do (
        if exist "%%i\python.exe" (
            echo Found: %%i\python.exe
            set FOUND_PYTHON="%%i\python.exe"
            goto :found
        )
    )
)

REM Python not found
echo.
echo ============================================
echo Python Not Found
echo ============================================
echo.
echo Solutions:
echo 1. Download Python from https://python.org
echo 2. During installation, CHECK "Add Python to PATH"
echo 3. Or install from Microsoft Store (search "Python")
echo.
echo After installing Python, run install.bat again
echo.
pause
exit /b 1

:found
echo.
echo ============================================
echo Python Found: %FOUND_PYTHON%
echo ============================================
echo.

REM Test Python
echo Testing Python...
%FOUND_PYTHON% --version
if errorlevel 1 (
    echo ERROR: Python found but not working properly
    pause
    exit /b 1
)

echo.
echo Creating fixed installer...

REM Create a fixed install script
echo @echo off > install_fixed.bat
echo echo Carwash Management System - Fixed Installer >> install_fixed.bat
echo echo Using Python: %FOUND_PYTHON% >> install_fixed.bat
echo echo. >> install_fixed.bat
echo echo Installing openpyxl... >> install_fixed.bat
echo %FOUND_PYTHON% -m pip install openpyxl >> install_fixed.bat
echo if errorlevel 1 ( >> install_fixed.bat
echo     echo ERROR: Failed to install openpyxl >> install_fixed.bat
echo     echo Try: %FOUND_PYTHON% -m pip install --user openpyxl >> install_fixed.bat
echo     pause >> install_fixed.bat
echo     exit /b 1 >> install_fixed.bat
echo ^) >> install_fixed.bat
echo echo. >> install_fixed.bat
echo echo Creating run script... >> install_fixed.bat
echo echo @echo off ^> run_carwash_fixed.bat >> install_fixed.bat
echo echo echo Starting Carwash Management System... ^>^> run_carwash_fixed.bat >> install_fixed.bat
echo echo %FOUND_PYTHON% carwash_app.py ^>^> run_carwash_fixed.bat >> install_fixed.bat
echo echo pause ^>^> run_carwash_fixed.bat >> install_fixed.bat
echo echo. >> install_fixed.bat
echo echo Installation completed! >> install_fixed.bat
echo echo Use run_carwash_fixed.bat to start the application >> install_fixed.bat
echo pause >> install_fixed.bat

echo ✓ Created install_fixed.bat
echo.
echo Next steps:
echo 1. Run install_fixed.bat to install dependencies
echo 2. Use run_carwash_fixed.bat to start the application
echo.
pause