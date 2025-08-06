# Carwash Management System - Installation Guide

## Quick Start

### Option 1: Automatic Installer (Recommended)
1. Download all files to a folder on your computer
2. Run the installer for your system:

**Windows:**
- Double-click `install.bat`

**Mac/Linux:**
- Open terminal in the folder
- Run: `chmod +x install.sh && ./install.sh`

**Cross-Platform (Python):**
- Run: `python install.py`

### Option 2: Manual Installation
1. Install Python 3.6+ from python.org
2. Run: `pip install openpyxl`
3. Run: `python carwash_app.py`

## Files Included

### Core Application
- **carwash_app.py** - Main desktop application
- **README_Desktop.md** - Detailed usage instructions

### Installers
- **install.bat** - Windows installer script
- **install.sh** - Mac/Linux installer script  
- **install.py** - Cross-platform Python installer
- **INSTALLER_README.md** - This file

### Documentation
- **download_instructions.md** - Download and setup guide

## What the Installers Do

1. **Check Python Installation** - Verifies Python 3.6+ is installed
2. **Install Dependencies** - Automatically installs openpyxl for Excel export
3. **Check GUI Support** - Verifies tkinter is available for the interface
4. **Create Run Scripts** - Makes easy-to-use launcher files
5. **Setup Verification** - Tests that everything works properly

## After Installation

### Windows
- Double-click `run_carwash.bat` to start the application
- Or run `python carwash_app.py` from command prompt

### Mac/Linux
- Run `./run_carwash.sh` from terminal
- Or run `python3 carwash_app.py` from terminal

## Troubleshooting

### Python Not Found
- Download from python.org
- During installation, check "Add Python to PATH"
- Restart your computer after installation

### Permission Denied (Mac/Linux)
```bash
chmod +x install.sh
chmod +x run_carwash.sh
```

### GUI Not Working (Linux)
Install tkinter:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# Arch Linux
sudo pacman -S tk
```

### Package Installation Failed
Try manual installation:
```bash
pip install --user openpyxl
```

## System Requirements

- **Python**: 3.6 or higher
- **Operating System**: Windows 7+, macOS 10.12+, or Linux
- **Memory**: 100MB RAM minimum
- **Storage**: 50MB free space
- **Display**: 1024x768 minimum resolution

## Features After Installation

✓ Complete carwash management system
✓ Employee login (Washer/Cashier roles)
✓ Car tracking through washing stages
✓ Payment processing in Philippine Peso
✓ Excel and CSV export with professional formatting
✓ Photo upload for license plates
✓ Automatic data saving
✓ Daily reset functionality
✓ Mobile-responsive web version also available

## Data Storage

The application creates these files/folders:
- `carwash_data.json` - Stores all car and payment data
- `uploads/` - Stores uploaded license plate photos
- Data persists between application sessions
- Files are created automatically on first run

## Getting Help

1. Check `README_Desktop.md` for detailed usage instructions
2. Check system requirements above
3. Verify Python and package installation
4. For advanced users: Check error messages in terminal/command prompt

## Uninstalling

To remove the application:
1. Delete the folder containing all files
2. Optionally remove Python and packages if not needed for other programs

The application doesn't modify system files or registry, so simple deletion is sufficient.