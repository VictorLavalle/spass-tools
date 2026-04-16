@echo off
REM Encrypt a CSV file into Samsung Pass .spass format (Windows)
cd /d "%~dp0"
echo.
echo === CSV to Samsung Pass (.spass) Converter ===
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

python csv_to_spass.py %*
echo.
pause
