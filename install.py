#!/usr/bin/env python3
"""
Cross-platform installer for Carwash Management System
Works on Windows, macOS, and Linux
"""

import sys
import subprocess
import os
import platform

def run_command(command, shell=False):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check if Python version is sufficient"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(f"ERROR: Python 3.6+ required, but found Python {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_packages():
    """Install required Python packages"""
    packages = ['openpyxl']
    
    print("\nInstalling required packages...")
    for package in packages:
        print(f"Installing {package}...")
        success, stdout, stderr = run_command([sys.executable, '-m', 'pip', 'install', package])
        
        if success:
            print(f"✓ {package} installed successfully")
        else:
            print(f"✗ Failed to install {package}")
            print(f"Error: {stderr}")
            return False
    
    return True

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        print("✓ GUI support (tkinter) is available")
        return True
    except ImportError:
        print("✗ tkinter not found")
        system = platform.system().lower()
        
        if system == "linux":
            print("Install tkinter with:")
            print("  Ubuntu/Debian: sudo apt-get install python3-tk")
            print("  CentOS/RHEL:   sudo yum install tkinter")
            print("  Arch Linux:    sudo pacman -S tk")
        elif system == "darwin":  # macOS
            print("Install tkinter with:")
            print("  brew install python-tk")
            print("  Or reinstall Python with tkinter support")
        elif system == "windows":
            print("Tkinter should be included with Python on Windows")
            print("Try reinstalling Python from python.org")
        
        return False

def create_run_scripts():
    """Create platform-specific run scripts"""
    system = platform.system().lower()
    
    if system == "windows":
        # Create Windows batch file
        with open("run_carwash.bat", "w") as f:
            f.write("@echo off\n")
            f.write("echo Starting Carwash Management System...\n")
            f.write("python carwash_app.py\n")
            f.write("pause\n")
        print("✓ Created run_carwash.bat")
        
    else:
        # Create Unix shell script
        with open("run_carwash.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'Starting Carwash Management System...'\n")
            f.write(f"{sys.executable} carwash_app.py\n")
        
        # Make executable
        os.chmod("run_carwash.sh", 0o755)
        print("✓ Created run_carwash.sh")

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only for now)"""
    if platform.system().lower() == "windows":
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Carwash Management.lnk")
            target = os.path.join(os.getcwd(), "run_carwash.bat")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.getcwd()
            shortcut.IconLocation = target
            shortcut.save()
            
            print("✓ Created desktop shortcut")
        except ImportError:
            print("• Desktop shortcut not created (requires pywin32)")
        except Exception as e:
            print(f"• Desktop shortcut creation failed: {e}")

def main():
    """Main installer function"""
    print("=" * 50)
    print("Carwash Management System - Python Installer")
    print("=" * 50)
    print()
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Install packages
    if not install_packages():
        print("\nInstallation failed!")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check GUI support
    tkinter_available = check_tkinter()
    
    # Create run scripts
    print("\nCreating run scripts...")
    create_run_scripts()
    
    # Create desktop shortcut (Windows)
    create_desktop_shortcut()
    
    print("\n" + "=" * 50)
    print("Installation completed!")
    print("=" * 50)
    print()
    
    if tkinter_available:
        print("✓ Everything is ready to go!")
    else:
        print("⚠ GUI support needs to be installed manually (see instructions above)")
    
    print("\nTo run the Carwash Management System:")
    
    system = platform.system().lower()
    if system == "windows":
        print("  • Double-click 'run_carwash.bat'")
        print("  • Or run: python carwash_app.py")
    else:
        print("  • Run: ./run_carwash.sh")
        print("  • Or run: python3 carwash_app.py")
    
    print("\nFiles created:")
    print("  • carwash_data.json (will be created on first run)")
    print("  • uploads/ folder (will be created for photos)")
    
    if system == "windows":
        print("  • run_carwash.bat (launcher script)")
    else:
        print("  • run_carwash.sh (launcher script)")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()