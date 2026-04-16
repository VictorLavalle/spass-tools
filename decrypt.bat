@echo off
REM Decrypt a Samsung Pass .spass file to CSV (Windows)
cd /d "%~dp0"
echo.
echo === Samsung Pass (.spass) to CSV Converter ===
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo   Error: Python is not installed.
    echo   Install it from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python -c "import cryptography" 2>nul
if %errorlevel% neq 0 (
    echo   Installing dependencies...
    pip install -r requirements.txt -q
)

python spass_to_csv.py %*
echo.
pause
