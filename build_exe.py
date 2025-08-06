#!/usr/bin/env python3
"""
Build script to create standalone executable from carwash_app.py
Uses PyInstaller to create a single .exe file that doesn't require Python installation
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, shell=False):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    print("Installing PyInstaller...")
    success, stdout, stderr = run_command([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    if success:
        print("✓ PyInstaller installed successfully")
        return True
    else:
        print(f"✗ Failed to install PyInstaller: {stderr}")
        return False

def check_files():
    """Check if required files exist"""
    # Prefer compatible version for Python 3.13
    if os.path.exists('carwash_app_compatible.py'):
        print("✓ Using Python 3.13 compatible version")
        return True, 'carwash_app_compatible.py'
    elif os.path.exists('carwash_app.py'):
        print("✓ Using original version (may have Python 3.13 compatibility issues)")
        return True, 'carwash_app.py'
    else:
        print("✗ No carwash application files found")
        print("  Looking for: carwash_app_compatible.py or carwash_app.py")
        return False, None

def create_spec_file(main_file):
    """Create PyInstaller spec file for customization"""
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['{main_file}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['openpyxl', 'tkinter', 'tkinter.ttk'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CarwashManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('carwash.spec', 'w') as f:
        f.write(spec_content)
    
    print("✓ Created carwash.spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable... This may take a few minutes...")
    
    # Use the spec file for better control
    success, stdout, stderr = run_command([
        sys.executable, '-m', 'PyInstaller', 
        '--clean',
        'carwash.spec'
    ])
    
    if success:
        print("✓ Executable built successfully")
        return True
    else:
        print(f"✗ Build failed: {stderr}")
        return False

def create_portable_package():
    """Create a portable package with the executable and instructions"""
    # Create package directory
    package_dir = "CarwashManager_Portable"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    # Copy executable
    exe_path = os.path.join("dist", "CarwashManager.exe")
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, package_dir)
        print(f"✓ Copied executable to {package_dir}")
    else:
        print("✗ Executable not found in dist folder")
        return False
    
    # Create readme for portable version
    readme_content = '''# Carwash Management System - Portable Version

## Quick Start
1. Double-click CarwashManager.exe to start the application
2. No installation required - this is a portable application

## Features
- Complete carwash management system
- Employee login (Washer/Cashier roles)
- Car tracking through washing stages
- Payment processing in Philippine Peso (₱)
- Excel and CSV export capabilities
- Photo upload for license plates
- Automatic data saving
- Daily reset functionality

## Data Storage
- All data is saved in the same folder as the executable
- carwash_data.json - Contains all car and payment data
- uploads/ folder - Contains uploaded photos
- Data persists between sessions

## System Requirements
- Windows 7 or later
- No additional software required
- Minimum 100MB RAM
- 50MB free disk space

## Usage
1. Run CarwashManager.exe
2. Enter employee name and select role (Washer or Cashier)
3. Start managing your carwash operations

## Troubleshooting
- If Windows warns about unknown publisher, click "More info" then "Run anyway"
- For antivirus warnings, add CarwashManager.exe to your antivirus exceptions
- If the program doesn't start, try running as administrator

## Support
This is a standalone version that doesn't require Python or any other software.
All features from the original application are included.
'''
    
    readme_path = os.path.join(package_dir, "README.txt")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✓ Created {readme_path}")
    
    # Create a simple batch file for easier access
    batch_content = '''@echo off
echo Starting Carwash Management System...
CarwashManager.exe
'''
    
    batch_path = os.path.join(package_dir, "Start_Carwash.bat")
    with open(batch_path, 'w') as f:
        f.write(batch_content)
    
    print(f"✓ Created {batch_path}")
    
    return True

def cleanup():
    """Clean up temporary files"""
    temp_dirs = ['build', '__pycache__']
    temp_files = ['carwash.spec']
    
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"✓ Cleaned up {temp_dir}")
    
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"✓ Cleaned up {temp_file}")

def main():
    """Main build function"""
    print("=" * 60)
    print("Carwash Management System - Executable Builder")
    print("=" * 60)
    print()
    
    # Check if required files exist
    if not check_files():
        input("Press Enter to exit...")
        return
    
    # Install PyInstaller
    if not install_pyinstaller():
        input("Press Enter to exit...")
        return
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    if not build_executable():
        input("Press Enter to exit...")
        return
    
    # Create portable package
    if not create_portable_package():
        input("Press Enter to exit...")
        return
    
    # Clean up
    cleanup()
    
    print()
    print("=" * 60)
    print("Build completed successfully!")
    print("=" * 60)
    print()
    print("Your portable Carwash Management System is ready!")
    print()
    print("📁 Package location: CarwashManager_Portable/")
    print("🚀 Executable: CarwashManager_Portable/CarwashManager.exe")
    print("📄 Instructions: CarwashManager_Portable/README.txt")
    print()
    print("Distribution:")
    print("- Copy the entire 'CarwashManager_Portable' folder to any Windows computer")
    print("- No installation required - just run CarwashManager.exe")
    print("- All data is stored locally in the same folder")
    print()
    
    # Check file size
    exe_path = os.path.join("CarwashManager_Portable", "CarwashManager.exe")
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"📊 Executable size: {size_mb:.1f} MB")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()