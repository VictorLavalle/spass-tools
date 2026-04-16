#!/bin/bash
# Encrypt a CSV file into Samsung Pass .spass format (macOS/Linux)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

if ! command -v python3 &> /dev/null; then
    echo ""
    echo "  Python 3 is not installed."
    echo "  Install it from https://www.python.org/downloads/"
    echo ""
    read -p "  Press Enter to exit..."
    exit 1
fi

python3 -c "import cryptography" 2>/dev/null || {
    echo ""
    echo "  Installing dependencies..."
    pip3 install -r requirements.txt -q
    echo ""
}

python3 scripts/csv_to_spass.py "$@"
read -p "  Press Enter to exit..."
