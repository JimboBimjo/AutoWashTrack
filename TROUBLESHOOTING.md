# Troubleshooting Guide - Carwash Management System

## Python Installation Issues

### Problem: "Python not installed or not in PATH"

This means Python is either not installed or not accessible from the command line.

#### Solution 1: Check if Python is Actually Installed
1. Open Command Prompt (Win+R, type `cmd`, press Enter)
2. Try these commands one by one:
   ```
   python --version
   python3 --version
   py --version
   ```
3. If any works, note which one and use the corresponding fix below

#### Solution 2: Use the Python Path Fixer
1. Double-click `fix_python_path.bat`
2. It will automatically find your Python installation
3. Follow the instructions to create fixed installer scripts

#### Solution 3: Reinstall Python with PATH
1. Download Python from [python.org](https://python.org)
2. **Important**: Check "Add Python to PATH" during installation
3. Restart your computer
4. Run `install.bat` again

#### Solution 4: Microsoft Store Python
1. Open Microsoft Store
2. Search for "Python"
3. Install Python 3.11 or newer
4. This automatically adds Python to PATH

#### Solution 5: Manual PATH Addition
1. Find your Python installation folder (usually `C:\Python39` or `C:\Users\YourName\AppData\Local\Programs\Python\Python39`)
2. Copy the folder path
3. Press Win+R, type `sysdm.cpl`, press Enter
4. Click "Environment Variables"
5. Under "System Variables", find "Path" and click "Edit"
6. Click "New" and paste your Python folder path
7. Also add the Scripts folder (add `\Scripts` to the path)
8. Click OK on all windows
9. Restart Command Prompt and try again

## Common Installation Issues

### Issue: "pip is not recognized"
**Solution**: Use `python -m pip` instead of just `pip`

### Issue: "Permission denied" or "Access denied"
**Solutions**:
1. Run Command Prompt as Administrator
2. Or use: `python -m pip install --user openpyxl`

### Issue: "No module named tkinter"
This happens on some Linux systems.
**Solution**: Install tkinter:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# Arch Linux  
sudo pacman -S tk
```

### Issue: Excel export not working
**Solutions**:
1. Make sure openpyxl is installed:
   ```
   python -m pip install openpyxl
   ```
2. If you get "bad option -initialname" error (Python 3.13):
   - This is automatically fixed in the latest version
   - Download the updated carwash_app.py or carwash_app_compatible.py

## Application Issues

### Issue: Application window doesn't appear
**Solutions**:
1. Check if there are error messages in the command prompt
2. Try running as administrator
3. Check Windows Defender/antivirus - add exception for the app
4. Make sure you have minimum system requirements:
   - Windows 7 or later
   - 100MB RAM
   - 50MB disk space

### Issue: "CarwashManager.exe is not recognized as trusted"
**Solution**:
1. Right-click on CarwashManager.exe
2. Select "Properties"
3. Click "Unblock" if available
4. Or click "More info" → "Run anyway" when Windows warns

### Issue: Data not saving
**Solutions**:
1. Make sure the application folder is writable
2. Run as administrator if needed
3. Check available disk space

### Issue: Photos not uploading
**Solutions**:
1. Check if `uploads` folder exists and is writable
2. Verify image file formats (jpg, png, gif, bmp)
3. Check file size (must be under 16MB)

## Mobile/PWA Issues

### Issue: "Add to Home Screen" option not showing
**Solutions**:
1. Make sure you're using Chrome, Safari, or Edge
2. Visit the site via HTTPS (required for PWA)
3. Use the site for a few minutes first
4. Check if it's already installed

### Issue: PWA not working offline
**Solutions**:
1. Load the app fully while online first
2. Check browser settings allow offline storage
3. Clear browser cache and reload

## Getting Help

### Step-by-Step Diagnosis
1. **Run `fix_python_path.bat`** - This solves 90% of installation issues
2. **Check the error message** - The specific error tells you what's wrong
3. **Try the manual commands**:
   ```
   python --version
   python -m pip install openpyxl
   python carwash_app.py
   ```
4. **Check system requirements** - Make sure your system is compatible

### Still Having Issues?
1. Note the exact error message
2. Check which operating system you're using
3. Verify Python version with `python --version`
4. Try the alternative installation methods above

### Quick Fixes
- **Can't install**: Use `fix_python_path.bat`
- **Permission errors**: Run as administrator
- **Path errors**: Reinstall Python with "Add to PATH" checked
- **Module errors**: Use `python -m pip install openpyxl`
- **GUI errors**: Install tkinter for your system

Most installation issues are caused by Python not being in the system PATH. The `fix_python_path.bat` script will automatically detect and fix this for you.