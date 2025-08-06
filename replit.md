# Overview

A Flask-based carwash management system that tracks vehicles through the washing process from arrival to payment completion. The system supports two types of employees (washers and cashiers) and manages car statuses through a simple workflow: washing → awaiting payment → finished. Features include license plate photo capture, dashboard views, daily data export functionality (Excel and CSV), PostgreSQL database storage, and daily reset capabilities. Uses Philippine Peso (₱) currency and is accessible on both desktop and mobile devices through responsive web design.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework
- **Flask**: Chosen for its simplicity and rapid development capabilities
- **Session-based authentication**: Simple role-based access without complex user management
- **In-memory storage**: All data stored in Python dictionaries for simplicity and real-time updates

## Frontend Architecture
- **Server-side rendering**: Flask templates with Jinja2 for dynamic content
- **Bootstrap 5**: Dark theme UI framework with mobile-first responsive design
- **Font Awesome**: Icon library for visual consistency
- **Vanilla JavaScript**: Basic client-side functionality for form validation and file previews
- **Mobile-optimized**: Responsive navigation, touch-friendly buttons, floating action button for quick access

## Data Storage
- **PostgreSQL Database**: Persistent storage with two main tables:
  - `cars`: Stores car information, status, timestamps, and payment details
  - `employees`: Stores active employee sessions with names and roles
- **File system**: License plate photos stored in `uploads/` directory
- **Cross-device access**: Responsive web design for desktop and mobile access

## Authentication & Authorization
- **UUID-based sessions**: Each employee gets a unique session ID
- **Role-based access**: Two roles (washer, cashier) with different permissions
- **No password authentication**: Simple name + role selection for quick employee access

## File Upload System
- **Image handling**: License plate photo upload with file type validation
- **Security**: Secure filename generation and file size limits (16MB max)
- **Preview functionality**: Client-side image preview before upload

## Business Logic Flow
- **Three-state workflow**: washing → awaiting_payment → finished
- **Role permissions**: Both washers and cashiers can add cars, update status, and process payments
- **Data export**: Excel (.xlsx) and CSV export functionality for daily reporting with totals and revenue
- **Daily reset**: Clear all car data at end of business day
- **Currency**: Philippine Peso (₱) with appropriate pricing for carwash services

## External Dependencies
- **Bootstrap 5**: UI framework via CDN
- **Font Awesome 6**: Icon library via CDN  
- **Flask**: Core web framework
- **Flask**: Core web framework with session management
- **PostgreSQL**: Database for persistent storage
- **SQLAlchemy**: Database ORM and migrations
- **Werkzeug**: File upload utilities and security helpers
- **openpyxl**: Excel file generation and formatting
- **Responsive design**: Mobile-optimized interface with Bootstrap framework
- **Python standard library**: CSV, datetime, UUID, logging, and OS modules