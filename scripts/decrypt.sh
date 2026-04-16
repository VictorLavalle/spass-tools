#!/bin/bash
# Decrypt a Samsung Pass .spass file to CSV (macOS/Linux)
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

if [ ! -d ".venv" ]; then
    echo ""
    echo "  Setting up virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt -q
    echo "  Done."
else
    source .venv/bin/activate
fi

python3 scripts/spass_to_csv.py "$@"
read -p "  Press Enter to exit..."
