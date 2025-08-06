# Carwash Management Desktop Application

A standalone desktop application for managing carwash operations, built with Python and tkinter.

## Features

- **Employee Login**: Simple name and role selection (Washer/Cashier)
- **Car Tracking**: Three-stage workflow (Washing → Awaiting Payment → Finished)
- **Payment Processing**: Philippine Peso (₱) currency support
- **Data Export**: Excel and CSV export with professional formatting
- **Photo Support**: Optional license plate photo upload
- **Auto-Save**: Automatic data saving every 30 seconds
- **Daily Reset**: Clear all data at end of business day

## Requirements

- Python 3.6 or higher
- Required packages:
  - tkinter (usually included with Python)
  - openpyxl (for Excel export)

## Installation

1. Ensure Python 3.6+ is installed on your system
2. Install required package:
   ```bash
   pip install openpyxl
   ```
3. Download the `carwash_app.py` file
4. Run the application:
   ```bash
   python carwash_app.py
   ```

## Usage

### Starting the Application

1. Run `python carwash_app.py`
2. Enter your name and select your role (Washer or Cashier)
3. Click "Start Work" to access the dashboard

### Main Dashboard

The dashboard is organized into three tabs:

- **Washing**: Cars currently being washed
- **Awaiting Payment**: Cars ready for payment processing
- **Finished**: Completed cars with payments processed

### Adding New Cars (Washers Only)

1. Click "Add New Car" button
2. Enter car name and plate number
3. Optionally browse and select a license plate photo
4. Click "Add Car" to add to washing queue

### Processing Workflow

1. **Move to Payment**: Move cars from washing to payment queue
2. **Process Payment**: Enter payment amount and complete transaction
3. **View Reports**: Check finished cars and daily revenue

### Data Export

- **Excel Export**: Professional formatted reports with totals and styling
- **CSV Export**: Simple comma-separated values format
- Both exports include:
  - Car details and payment information
  - Total cars processed
  - Total revenue for the day

### Daily Reset

- Click "Reset Daily Data" to clear all car records
- Confirmation dialog prevents accidental data loss
- Use at end of business day to start fresh

## Data Storage

- Data is automatically saved to `carwash_data.json`
- Photos are stored in `uploads/` directory
- Auto-save occurs every 30 seconds
- Data persists between application sessions

## File Structure

```
carwash_app.py          # Main application file
carwash_data.json       # Data storage file (created automatically)
uploads/                # Photo storage directory (created automatically)
├── 20250806_120000_plate1.jpg
└── 20250806_130000_plate2.png
```

## Features by Role

### Washer
- Add new cars to system
- Move cars from washing to payment queue
- View all car statuses
- Export reports
- Reset daily data

### Cashier
- Process payments for cars
- Move cars from washing to payment queue
- View all car statuses
- Export reports
- Reset daily data

## Keyboard Shortcuts

- **Enter**: Confirm actions in dialogs
- **Tab**: Navigate between form fields

## Technical Details

- Built with Python tkinter for cross-platform compatibility
- JSON-based data storage for simplicity
- Automatic timestamp tracking
- Philippine Peso currency formatting
- Excel export with professional styling using openpyxl

## Troubleshooting

### Application won't start
- Ensure Python 3.6+ is installed
- Install openpyxl: `pip install openpyxl`

### Data not saving
- Check file permissions in application directory
- Ensure sufficient disk space

### Photos not uploading
- Check if `uploads/` directory exists and is writable
- Verify image file format (jpg, jpeg, png, gif, bmp)

## Converting to Executable

To create a standalone executable file:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create executable:
   ```bash
   pyinstaller --onefile --windowed carwash_app.py
   ```

3. Find the executable in `dist/` directory

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.6 or higher
- **Memory**: Minimum 100MB RAM
- **Storage**: 50MB free space
- **Display**: Minimum 1024x768 resolution

## Support

For issues or questions about the desktop application, please refer to this documentation or contact your system administrator.