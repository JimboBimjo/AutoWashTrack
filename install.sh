#!/bin/bash

echo "================================================"
echo "Carwash Management System - Cross-Platform Installer"
echo "================================================"
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if command_exists python3; then
    PYTHON_CMD="python3"
    echo "Python 3 detected:"
    python3 --version
elif command_exists python; then
    PYTHON_VERSION=$(python --version 2>&1)
    if [[ $PYTHON_VERSION == *"Python 3"* ]]; then
        PYTHON_CMD="python"
        echo "Python 3 detected:"
        python --version
    else
        echo "ERROR: Python 3 is required but only Python 2 was found"
        echo "Please install Python 3.6+ from https://python.org"
        exit 1
    fi
else
    echo "ERROR: Python is not installed"
    echo "Please install Python 3.6+ from https://python.org"
    echo
    echo "Installation commands by OS:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
    echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
    echo "  macOS:         brew install python3"
    exit 1
fi

echo

# Check if pip is available
if command_exists pip3; then
    PIP_CMD="pip3"
elif command_exists pip; then
    PIP_CMD="pip"
else
    echo "ERROR: pip is not installed"
    echo "Please install pip for Python package management"
    exit 1
fi

echo "Installing required packages..."
$PIP_CMD install openpyxl

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install openpyxl"
    echo "Please check your internet connection and try again"
    echo "You may need to run: sudo $PIP_CMD install openpyxl"
    exit 1
fi

echo
echo "================================================"
echo "Installation completed successfully!"
echo "================================================"
echo

# Create run script
cat > run_carwash.sh << EOF
#!/bin/bash
echo "Starting Carwash Management System..."
$PYTHON_CMD carwash_app.py
EOF

chmod +x run_carwash.sh

echo "To run the Carwash Management System:"
echo "  1. Run: ./run_carwash.sh"
echo "  OR"
echo "  2. Run: $PYTHON_CMD carwash_app.py"
echo
echo "Created 'run_carwash.sh' for easy launching"
echo

# Check for tkinter
echo "Checking GUI support..."
$PYTHON_CMD -c "import tkinter" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "WARNING: tkinter not found. Installing GUI support..."
    
    # Detect OS and install tkinter
    if command_exists apt-get; then
        echo "Detected Debian/Ubuntu system"
        echo "Please run: sudo apt-get install python3-tk"
    elif command_exists yum; then
        echo "Detected Red Hat/CentOS system"
        echo "Please run: sudo yum install tkinter"
    elif command_exists pacman; then
        echo "Detected Arch Linux system"
        echo "Please run: sudo pacman -S tk"
    else
        echo "Please install tkinter for your system manually"
    fi
    echo
else
    echo "GUI support (tkinter) is available ✓"
fi

echo "Setup complete! You can now run the application."