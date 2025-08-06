# Overview

A Flask-based carwash management system that tracks vehicles through the washing process from arrival to payment completion. The system supports two types of employees (washers and cashiers) and manages car statuses through a simple workflow: washing → awaiting payment → finished. Features include license plate photo capture, real-time dashboard views, and daily data export functionality.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework
- **Flask**: Chosen for its simplicity and rapid development capabilities
- **Session-based authentication**: Simple role-based access without complex user management
- **In-memory storage**: All data stored in Python dictionaries for simplicity and real-time updates

## Frontend Architecture
- **Server-side rendering**: Flask templates with Jinja2 for dynamic content
- **Bootstrap 5**: Dark theme UI framework for responsive design
- **Font Awesome**: Icon library for visual consistency
- **Vanilla JavaScript**: Basic client-side functionality for form validation and file previews

## Data Storage
- **In-memory dictionaries**: Two main data structures:
  - `cars_data`: Stores car information, status, timestamps, and payment details
  - `employees`: Stores active employee sessions with names and roles
- **File system**: License plate photos stored in `uploads/` directory
- **No persistent database**: Data resets on application restart (suitable for daily operations)

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
- **Role permissions**: Washers can add cars and update status, cashiers can process payments
- **Data export**: CSV export functionality for daily reporting

## External Dependencies
- **Bootstrap 5**: UI framework via CDN
- **Font Awesome 6**: Icon library via CDN  
- **Flask**: Core web framework
- **Werkzeug**: File upload utilities and security helpers
- **Python standard library**: CSV, datetime, UUID, logging, and OS modules