@echo off
REM Encrypt a CSV file into Samsung Pass .spass format (Windows)
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

if not exist ".venv" (
    echo.
    echo   Setting up virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt -q
    echo   Done.
) else (
    call .venv\Scripts\activate.bat
)

python scripts\csv_to_spass.py %*
echo.
pause
