from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Car(db.Model):
    __tablename__ = 'cars'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    car_name = db.Column(db.String(100), nullable=False)
    plate_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='washing')  # washing, awaiting_payment, finished
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completion_time = db.Column(db.DateTime)
    
    # Employee tracking
    washer_name = db.Column(db.String(100))
    cashier_name = db.Column(db.String(100))
    
    # Payment info
    payment_amount = db.Column(db.Float)
    
    # Photo
    photo_filename = db.Column(db.String(255))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'car_name': self.car_name,
            'plate_number': self.plate_number,
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'completion_time': self.completion_time.isoformat() if self.completion_time else None,
            'washer_name': self.washer_name,
            'cashier_name': self.cashier_name,
            'payment_amount': self.payment_amount,
            'photo_filename': self.photo_filename,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # washer, cashier
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'name': self.name,
            'role': self.role,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None
        }