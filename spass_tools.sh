#!/bin/bash
# Samsung Pass (.spass) Tools (macOS/Linux)
cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo ""
    echo "  Python 3 is not installed."
    echo "  Install it from https://www.python.org/downloads/"
    echo ""
    read -p "  Press Enter to exit..."
    exit 1
fi

# Create and activate virtual environment
if [ ! -d ".venv" ]; then
    echo ""
    echo "  Setting up virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    echo "  Done."
else
    source .venv/bin/activate
fi

python3 spass_tools.py
