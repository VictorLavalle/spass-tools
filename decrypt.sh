#!/bin/bash
# Decrypt a Samsung Pass .spass file to CSV (macOS/Linux)
cd "$(dirname "$0")"
echo ""
echo "=== Samsung Pass (.spass) to CSV Converter ==="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "  Error: Python 3 is not installed."
    echo "  Install it from https://www.python.org/downloads/"
    echo ""
    read -p "  Press Enter to exit..."
    exit 1
fi

# Install dependencies if needed
python3 -c "import cryptography" 2>/dev/null || {
    echo "  Installing dependencies..."
    pip3 install -r requirements.txt -q
}

python3 spass_to_csv.py "$@"
echo ""
read -p "  Press Enter to exit..."
