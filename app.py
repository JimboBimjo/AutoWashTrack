import os
import csv
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from werkzeug.utils import secure_filename
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "carwash-secret-key-123")

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage
cars_data = {}  # {car_id: {car_name, plate_number, plate_photo, status, washer_name, timestamp, payment_amount, cashier_name, completion_time}}
employees = {}  # {session_id: {name, role}}

# Car statuses
STATUS_WASHING = "washing"
STATUS_AWAITING_PAYMENT = "awaiting_payment" 
STATUS_FINISHED = "finished"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_employee():
    session_id = session.get('session_id')
    return employees.get(session_id) if session_id else None

# Make get_current_employee available in templates
@app.context_processor
def inject_current_employee():
    return dict(get_current_employee=get_current_employee)

def generate_session_id():
    return str(uuid.uuid4())

@app.route('/')
def index():
    employee = get_current_employee()
    if not employee:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        role = request.form.get('role')
        
        if not name or role not in ['washer', 'cashier']:
            flash('Please enter your name and select a valid role.', 'error')
            return render_template('login.html')
        
        # Create session
        session_id = generate_session_id()
        session['session_id'] = session_id
        employees[session_id] = {
            'name': name,
            'role': role,
            'login_time': datetime.now()
        }
        
        flash(f'Welcome, {name}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session_id = session.get('session_id')
    if session_id and session_id in employees:
        del employees[session_id]
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    employee = get_current_employee()
    if not employee:
        return redirect(url_for('login'))
    
    # Filter cars by status for dashboard display
    washing_cars = [car for car in cars_data.values() if car['status'] == STATUS_WASHING]
    awaiting_payment_cars = [car for car in cars_data.values() if car['status'] == STATUS_AWAITING_PAYMENT]
    finished_cars = [car for car in cars_data.values() if car['status'] == STATUS_FINISHED]
    
    return render_template('dashboard.html', 
                         employee=employee,
                         washing_cars=washing_cars,
                         awaiting_payment_cars=awaiting_payment_cars,
                         finished_cars=finished_cars,
                         total_cars=len(cars_data))

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    employee = get_current_employee()
    if not employee or employee['role'] != 'washer':
        flash('Only washers can add new cars.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        car_name = request.form.get('car_name', '').strip()
        plate_number = request.form.get('plate_number', '').strip()
        
        if not car_name or not plate_number:
            flash('Please enter both car name and plate number.', 'error')
            return render_template('add_car.html', employee=employee)
        
        # Handle file upload
        plate_photo = None
        if 'plate_photo' in request.files:
            file = request.files['plate_photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                plate_photo = filename
        
        # Create new car entry
        car_id = str(uuid.uuid4())
        cars_data[car_id] = {
            'car_id': car_id,
            'car_name': car_name,
            'plate_number': plate_number,
            'plate_photo': plate_photo,
            'status': STATUS_WASHING,
            'washer_name': employee['name'],
            'timestamp': datetime.now(),
            'payment_amount': None,
            'cashier_name': None,
            'completion_time': None
        }
        
        flash(f'Car "{car_name}" has been added and is now washing.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_car.html', employee=employee)

@app.route('/update_status/<car_id>', methods=['GET', 'POST'])
def update_status(car_id):
    employee = get_current_employee()
    if not employee:
        return redirect(url_for('login'))
    
    if car_id not in cars_data:
        flash('Car not found.', 'error')
        return redirect(url_for('dashboard'))
    
    car = cars_data[car_id]
    
    if request.method == 'POST':
        new_status = request.form.get('status')
        
        # Validate status transitions
        if employee['role'] == 'washer' and car['status'] == STATUS_WASHING and new_status == STATUS_AWAITING_PAYMENT:
            car['status'] = STATUS_AWAITING_PAYMENT
            flash(f'Car "{car["car_name"]}" is now awaiting payment.', 'success')
        elif employee['role'] == 'washer' and new_status == STATUS_WASHING:
            car['status'] = STATUS_WASHING
            car['washer_name'] = employee['name']
            flash(f'Car "{car["car_name"]}" status updated to washing.', 'success')
        else:
            flash('Invalid status update.', 'error')
            return redirect(url_for('dashboard'))
        
        return redirect(url_for('dashboard'))
    
    return render_template('update_status.html', employee=employee, car=car)

@app.route('/payment/<car_id>', methods=['GET', 'POST'])
def payment(car_id):
    employee = get_current_employee()
    if not employee:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    
    if car_id not in cars_data:
        flash('Car not found.', 'error')
        return redirect(url_for('dashboard'))
    
    car = cars_data[car_id]
    
    if car['status'] != STATUS_AWAITING_PAYMENT:
        flash('This car is not awaiting payment.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            payment_amount = float(request.form.get('payment_amount', 0))
            if payment_amount <= 0:
                flash('Please enter a valid payment amount.', 'error')
                return render_template('payment.html', employee=employee, car=car)
            
            # Update car status to finished
            car['status'] = STATUS_FINISHED
            car['payment_amount'] = payment_amount
            car['cashier_name'] = employee['name']
            car['completion_time'] = datetime.now()
            
            flash(f'Payment of ${payment_amount:.2f} processed for car "{car["car_name"]}".', 'success')
            return redirect(url_for('dashboard'))
            
        except ValueError:
            flash('Please enter a valid payment amount.', 'error')
            return render_template('payment.html', employee=employee, car=car)
    
    return render_template('payment.html', employee=employee, car=car)

@app.route('/export_daily_data')
def export_daily_data():
    employee = get_current_employee()
    if not employee:
        return redirect(url_for('login'))
    
    # Get today's date
    today = datetime.now().date()
    
    # Filter finished cars from today
    finished_today = []
    for car in cars_data.values():
        if (car['status'] == STATUS_FINISHED and 
            car['completion_time'] and 
            car['completion_time'].date() == today):
            finished_today.append(car)
    
    if not finished_today:
        flash('No completed cars found for today.', 'info')
        return redirect(url_for('dashboard'))
    
    # Create CSV file
    csv_filename = f"carwash_daily_report_{today.strftime('%Y-%m-%d')}.csv"
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Car Name', 'Plate Number', 'Washer', 'Cashier', 'Payment Amount', 'Start Time', 'Completion Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for car in finished_today:
            writer.writerow({
                'Car Name': car['car_name'],
                'Plate Number': car['plate_number'],
                'Washer': car['washer_name'],
                'Cashier': car['cashier_name'],
                'Payment Amount': f"${car['payment_amount']:.2f}" if car['payment_amount'] else '',
                'Start Time': car['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                'Completion Time': car['completion_time'].strftime('%Y-%m-%d %H:%M:%S') if car['completion_time'] else ''
            })
    
    return send_file(csv_path, as_attachment=True, download_name=csv_filename)

@app.route('/api/dashboard_data')
def api_dashboard_data():
    """API endpoint for dashboard updates (minimal JavaScript usage)"""
    employee = get_current_employee()
    if not employee:
        return jsonify({'error': 'Not authenticated'}), 401
    
    washing_count = len([car for car in cars_data.values() if car['status'] == STATUS_WASHING])
    awaiting_payment_count = len([car for car in cars_data.values() if car['status'] == STATUS_AWAITING_PAYMENT])
    finished_count = len([car for car in cars_data.values() if car['status'] == STATUS_FINISHED])
    
    return jsonify({
        'washing_count': washing_count,
        'awaiting_payment_count': awaiting_payment_count,
        'finished_count': finished_count,
        'total_count': len(cars_data)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
