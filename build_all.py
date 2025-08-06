#!/usr/bin/env python3
"""
Complete build script for Carwash Management System
Creates both desktop executable and mobile PWA package
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path

def run_command(command, shell=False):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_required_packages():
    """Install all required packages for building"""
    packages = ['pyinstaller', 'openpyxl']
    
    print("Installing required packages...")
    for package in packages:
        print(f"Installing {package}...")
        success, stdout, stderr = run_command([sys.executable, '-m', 'pip', 'install', package])
        
        if success:
            print(f"✓ {package} installed successfully")
        else:
            print(f"✗ Failed to install {package}: {stderr}")
            return False
    
    return True

def build_desktop_executable():
    """Build the desktop executable"""
    print("\n" + "="*60)
    print("Building Desktop Executable (.exe)")
    print("="*60)
    
    # Check if carwash_app.py exists
    if not os.path.exists('carwash_app.py'):
        print("✗ carwash_app.py not found")
        return False
    
    # Create PyInstaller spec file
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['carwash_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['openpyxl', 'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox'],
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
    
    print("✓ Created PyInstaller spec file")
    
    # Build executable
    print("Building executable... This may take several minutes...")
    success, stdout, stderr = run_command([
        sys.executable, '-m', 'PyInstaller', 
        '--clean',
        'carwash.spec'
    ])
    
    if not success:
        print(f"✗ Build failed: {stderr}")
        return False
    
    print("✓ Executable built successfully")
    
    # Create portable package
    package_dir = "CarwashManager_Desktop"
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
    
    # Create instructions
    readme_content = '''# Carwash Management System - Desktop Version

## Quick Start
1. Double-click CarwashManager.exe to start
2. No installation required - this is portable!

## Features
- Complete carwash management system
- Employee login (Washer/Cashier roles)
- Car tracking through washing stages
- Payment processing in Philippine Peso (₱)
- Excel and CSV export with professional formatting
- Photo upload for license plates
- Automatic data saving
- Daily reset functionality

## System Requirements
- Windows 7 or later
- No additional software needed
- 100MB RAM minimum
- 50MB free disk space

## Data Storage
- carwash_data.json - All car and payment data
- uploads/ folder - License plate photos
- Data persists between sessions

## Troubleshooting
- If Windows warns about unknown publisher: Click "More info" → "Run anyway"
- For antivirus warnings: Add CarwashManager.exe to exceptions
- If program doesn't start: Try running as administrator

This standalone version includes everything needed to run the carwash management system.
'''
    
    readme_path = os.path.join(package_dir, "README.txt")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✓ Created {readme_path}")
    
    # Create launcher batch file
    batch_content = '''@echo off
title Carwash Management System
echo Starting Carwash Management System...
echo.
echo If you see this window, the application is starting.
echo The main window should appear shortly.
echo.
CarwashManager.exe
if errorlevel 1 (
    echo.
    echo Error: Application failed to start
    echo Please check README.txt for troubleshooting
    pause
)
'''
    
    batch_path = os.path.join(package_dir, "Start_Carwash.bat")
    with open(batch_path, 'w') as f:
        f.write(batch_content)
    
    print(f"✓ Created {batch_path}")
    
    # Clean up build files
    temp_dirs = ['build', 'dist', '__pycache__']
    temp_files = ['carwash.spec']
    
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print("✓ Cleaned up temporary files")
    
    return True

def build_mobile_pwa():
    """Build the mobile PWA package"""
    print("\n" + "="*60)
    print("Building Mobile PWA Package")
    print("="*60)
    
    # Create mobile package directory
    mobile_dir = "CarwashManager_Mobile"
    if os.path.exists(mobile_dir):
        shutil.rmtree(mobile_dir)
    
    os.makedirs(mobile_dir)
    
    # Files to include in mobile package
    web_files = [
        'app.py',
        'main.py',
        'templates/',
        'static/',
        'pyproject.toml',
        'uv.lock'
    ]
    
    # Copy web application files
    for file_path in web_files:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.copytree(file_path, os.path.join(mobile_dir, file_path))
            else:
                shutil.copy2(file_path, mobile_dir)
            print(f"✓ Copied {file_path}")
    
    # Create mobile-specific instructions
    mobile_readme = '''# Carwash Management System - Mobile PWA

## What is a PWA?
A Progressive Web App (PWA) is a web application that works like a native mobile app. It can be installed on your phone's home screen and works offline.

## Installation on Mobile Device

### Method 1: Direct Access (Recommended)
1. Open your mobile browser (Chrome, Safari, Edge)
2. Navigate to your deployed carwash application URL
3. The app will automatically work on mobile with touch-friendly interface

### Method 2: Install as Native App
**On iPhone/iPad:**
1. Open the web app in Safari
2. Tap the Share button (square with arrow)
3. Scroll down and tap "Add to Home Screen"
4. Tap "Add" to install

**On Android:**
1. Open the web app in Chrome
2. Tap the menu (three dots)
3. Tap "Add to Home screen" or "Install app"
4. Tap "Add" or "Install"

### Method 3: Deploy This Package
If you want to host your own version:

**On Replit:**
1. Upload all files to a new Replit project
2. Run the project
3. Access via the provided URL
4. Follow Method 1 or 2 above

**On Other Platforms:**
1. Deploy the Flask application to your hosting service
2. Ensure all files are uploaded
3. Configure environment variables if needed
4. Access via your domain

## Mobile Features
- Touch-friendly interface with large buttons
- Responsive design that adapts to screen size
- Floating action button for quick access
- Mobile navigation menu
- Camera integration for license plate photos
- Offline capability (with PWA installation)
- Native app-like experience

## PWA Capabilities
✓ Install on home screen like native app
✓ Works offline (cached data)
✓ Push notifications (if configured)
✓ Native app appearance
✓ Fast loading with service worker
✓ Cross-platform (iOS, Android)

## System Requirements
- Modern mobile browser (Chrome, Safari, Edge)
- iOS 11.3+ or Android 5.0+
- Internet connection for initial load
- 10MB storage space

## Features
Same as desktop version:
- Employee login system
- Car tracking through washing stages
- Payment processing in Philippine Peso
- Excel and CSV export
- Photo upload
- Daily reset functionality

The mobile version provides the same powerful features as the desktop app, optimized for touch interaction and mobile workflows.
'''
    
    mobile_readme_path = os.path.join(mobile_dir, "README_Mobile.txt")
    with open(mobile_readme_path, 'w') as f:
        f.write(mobile_readme)
    
    print(f"✓ Created {mobile_readme_path}")
    
    # Create deployment script
    deploy_script = '''#!/bin/bash
# Quick deployment script for Carwash Mobile PWA

echo "Carwash Management System - Mobile Deployment"
echo "============================================="
echo

# Check if Python is installed
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found. Please install Python 3.6+"
    exit 1
fi

echo "Python detected: $($PYTHON_CMD --version)"

# Install dependencies
echo "Installing dependencies..."
$PYTHON_CMD -m pip install flask flask-sqlalchemy openpyxl gunicorn

# Check if files exist
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found"
    exit 1
fi

echo
echo "Starting Carwash Management System..."
echo "Mobile-optimized version with PWA capabilities"
echo
echo "Access your app at: http://localhost:5000"
echo "For mobile testing, use your computer's IP address"
echo
echo "Press Ctrl+C to stop the server"
echo

# Start the application
$PYTHON_CMD -m gunicorn --bind 0.0.0.0:5000 --reload main:app
'''
    
    deploy_script_path = os.path.join(mobile_dir, "deploy.sh")
    with open(deploy_script_path, 'w') as f:
        f.write(deploy_script)
    
    # Make script executable on Unix systems
    try:
        os.chmod(deploy_script_path, 0o755)
    except:
        pass  # Windows doesn't support chmod
    
    print(f"✓ Created {deploy_script_path}")
    
    return True

def create_distribution_packages():
    """Create ZIP packages for distribution"""
    print("\n" + "="*60)
    print("Creating Distribution Packages")
    print("="*60)
    
    # Create desktop ZIP
    desktop_dir = "CarwashManager_Desktop"
    if os.path.exists(desktop_dir):
        desktop_zip = f"{desktop_dir}.zip"
        with zipfile.ZipFile(desktop_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(desktop_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, '.')
                    zipf.write(file_path, arc_path)
        
        desktop_size = os.path.getsize(desktop_zip) / (1024 * 1024)
        print(f"✓ Created {desktop_zip} ({desktop_size:.1f} MB)")
    
    # Create mobile ZIP
    mobile_dir = "CarwashManager_Mobile"
    if os.path.exists(mobile_dir):
        mobile_zip = f"{mobile_dir}.zip"
        with zipfile.ZipFile(mobile_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(mobile_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, '.')
                    zipf.write(file_path, arc_path)
        
        mobile_size = os.path.getsize(mobile_zip) / (1024 * 1024)
        print(f"✓ Created {mobile_zip} ({mobile_size:.1f} MB)")
    
    return True

def main():
    """Main build function"""
    print("="*80)
    print("Carwash Management System - Complete Build Script")
    print("="*80)
    print()
    print("This script will create both desktop and mobile versions:")
    print("1. Desktop: Standalone .exe file (Windows)")
    print("2. Mobile: PWA package for web deployment")
    print()
    
    # Install required packages
    if not install_required_packages():
        input("Press Enter to exit...")
        return
    
    # Build desktop version
    desktop_success = build_desktop_executable()
    
    # Build mobile version
    mobile_success = build_mobile_pwa()
    
    # Create distribution packages
    if desktop_success or mobile_success:
        create_distribution_packages()
    
    # Final summary
    print("\n" + "="*80)
    print("Build Summary")
    print("="*80)
    
    if desktop_success:
        print("✓ Desktop Version: CarwashManager_Desktop/")
        print("  - CarwashManager.exe (standalone executable)")
        print("  - Start_Carwash.bat (easy launcher)")
        print("  - README.txt (instructions)")
        print("  - CarwashManager_Desktop.zip (distribution package)")
    else:
        print("✗ Desktop Version: Build failed")
    
    if mobile_success:
        print("✓ Mobile Version: CarwashManager_Mobile/")
        print("  - Complete PWA web application")
        print("  - Can be installed as native mobile app")
        print("  - README_Mobile.txt (deployment instructions)")
        print("  - deploy.sh (quick deployment script)")
        print("  - CarwashManager_Mobile.zip (distribution package)")
    else:
        print("✗ Mobile Version: Build failed")
    
    print()
    print("Distribution:")
    if desktop_success:
        print("🖥️  Desktop: Share CarwashManager_Desktop.zip")
        print("   Recipients extract and run CarwashManager.exe")
    
    if mobile_success:
        print("📱 Mobile: Deploy CarwashManager_Mobile/ to web server")
        print("   Users access via browser and can install as PWA")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()