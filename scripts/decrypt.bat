@echo off
REM Decrypt a Samsung Pass .spass file to CSV (Windows)
cd /d "%~dp0\.."

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo   Python is not installed.
    echo   Install it from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python -c "import cryptography" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo   Installing dependencies...
    pip install -r requirements.txt -q
)

python scripts\spass_to_csv.py %*
echo.
pause
