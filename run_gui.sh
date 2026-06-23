#!/bin/bash
# Desktop launcher script for Precious Media Transfer and Aggregator

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the project directory
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv/bin" ]; then
    source venv/bin/activate
fi

# Find Python 3 - try common locations
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    # Fallback to common installation paths
    if [ -f "/usr/local/bin/python3" ]; then
        PYTHON_CMD="/usr/local/bin/python3"
    elif [ -f "/opt/homebrew/bin/python3" ]; then
        PYTHON_CMD="/opt/homebrew/bin/python3"
    else
        echo "Error: Python 3 not found. Please install Python 3 first."
        echo ""
        echo "Install Python 3:"
        echo "  brew install python3"
        echo ""
        echo "Or download from: https://www.python.org"
        exit 1
    fi
fi

# Run the GUI
"$PYTHON_CMD" src/gui.py
