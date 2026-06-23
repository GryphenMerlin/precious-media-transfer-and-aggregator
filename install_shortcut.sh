#!/bin/bash
# Create desktop shortcut for Precious Media Transfer and Aggregator
# Run this script to install a desktop shortcut

set -e

echo "Installing Precious Media Transfer and Aggregator..."

# Get the directory where the script is run from
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Project directory: $PROJECT_DIR"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS"
    
    # Create an alias/shortcut on Desktop
    DESKTOP="$HOME/Desktop"
    SHORTCUT_NAME="Precious Media Transfer"
    
    # Create a simple launcher app script
    cat > "$DESKTOP/$SHORTCUT_NAME.command" << 'EOF'
#!/bin/bash
cd "PROJECT_DIR_PLACEHOLDER"

# Find Python 3
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    if [ -f "/usr/local/bin/python3" ]; then
        PYTHON_CMD="/usr/local/bin/python3"
    elif [ -f "/opt/homebrew/bin/python3" ]; then
        PYTHON_CMD="/opt/homebrew/bin/python3"
    else
        echo "Error: Python 3 not found. Please install Python 3."
        echo ""
        echo "Install with: brew install python3"
        echo "Or download from: https://www.python.org"
        sleep 5
        exit 1
    fi
fi

# Activate virtual environment if it exists
if [ -d "venv/bin" ]; then
    source venv/bin/activate
fi

"$PYTHON_CMD" src/gui.py
EOF
    
    # Replace placeholder
    sed -i '' "s|PROJECT_DIR_PLACEHOLDER|$PROJECT_DIR|g" "$DESKTOP/$SHORTCUT_NAME.command"
    
    # Make it executable
    chmod +x "$DESKTOP/$SHORTCUT_NAME.command"
    
    # Make it executable from Finder (set as executable)
    xattr -d com.apple.quarantine "$DESKTOP/$SHORTCUT_NAME.command" 2>/dev/null || true
    
    echo "✓ Desktop shortcut created at: $DESKTOP/$SHORTCUT_NAME.command"
    echo ""
    echo "You can now:"
    echo "1. Double-click the shortcut on your Desktop to launch the app"
    echo "2. Or add it to your Dock by dragging it there"
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Detected Linux"
    
    DESKTOP="$HOME/Desktop"
    APPLICATIONS="$HOME/.local/share/applications"
    
    # Create applications directory if it doesn't exist
    mkdir -p "$APPLICATIONS"
    mkdir -p "$DESKTOP"
    
    # Create desktop entry
    DESKTOP_FILE="$APPLICATIONS/precious-media-transfer.desktop"
    
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Precious Media Transfer
Comment=Scan, deduplicate, and transfer media to SSD
Exec=bash $PROJECT_DIR/run_gui.sh
Icon=$PROJECT_DIR/assets/icon.png
Terminal=false
Categories=Utility;Application;
EOF
    
    chmod +x "$DESKTOP_FILE"
    
    # Copy to desktop as well
    cp "$DESKTOP_FILE" "$DESKTOP/precious-media-transfer.desktop"
    chmod +x "$DESKTOP/precious-media-transfer.desktop"
    
    echo "✓ Desktop shortcut created"
    echo "  Applications menu: $APPLICATIONS/precious-media-transfer.desktop"
    echo "  Desktop: $DESKTOP/precious-media-transfer.desktop"
    
else
    echo "✗ Unsupported OS: $OSTYPE"
    echo "Please create a shortcut manually by linking to: python3 $PROJECT_DIR/src/gui.py"
    exit 1
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "First time setup (if needed):"
echo "  1. Install Python 3: brew install python3"
echo "  2. cd $PROJECT_DIR"
echo "  3. pip3 install -r requirements.txt"
echo "  4. Then run the shortcut"
