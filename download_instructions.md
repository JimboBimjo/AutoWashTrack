# Download Instructions for Carwash Management System

## Desktop Application Download

### Files to Download:
1. **carwash_app.py** - Main desktop application file
2. **README_Desktop.md** - Setup and usage instructions

### How to Download:
1. Right-click on each file in the file browser
2. Select "Download" from the menu
3. Save both files to your computer

### Installation Steps:
1. Install Python 3.6+ on your computer if not already installed
   - Windows: Download from python.org
   - Mac: Use Homebrew or download from python.org
   - Linux: Use your package manager (apt, yum, etc.)

2. Install required package:
   ```bash
   pip install openpyxl
   ```

3. Run the desktop application:
   ```bash
   python carwash_app.py
   ```

### Creating an Executable (Optional):
To create a standalone .exe file that doesn't require Python:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create executable:
   ```bash
   pyinstaller --onefile --windowed carwash_app.py
   ```

3. Find the .exe file in the `dist/` folder

## Mobile Access

### Web Application (Mobile-Friendly):
The original web application is already mobile-optimized and can be accessed on phones and tablets:

1. **Access the web version**: Use your mobile browser to visit the web application
2. **Add to Home Screen**: 
   - iOS: Tap Share → Add to Home Screen
   - Android: Tap Menu → Add to Home Screen
3. **Offline Capability**: The web app works like a native mobile app

### Mobile Features:
- Touch-friendly buttons and interfaces
- Responsive design that adapts to screen size
- Floating action button for quick access
- Mobile navigation menu
- Camera integration for license plate photos

### No Separate Mobile App Download Needed:
The web application IS the mobile version - it automatically adapts to mobile devices and provides a native app-like experience.

## Summary

- **Desktop**: Download `carwash_app.py` and run with Python
- **Mobile**: Use the web application in your mobile browser (already mobile-optimized)
- **Tablets**: Either desktop app or web version works well

Both versions have the same features:
- Employee login
- Car tracking through washing stages
- Payment processing in Philippine Peso
- Excel and CSV export
- Daily reset functionality
- Photo upload support