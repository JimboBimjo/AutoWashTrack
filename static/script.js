// Carwash Management System JavaScript

// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered');
            })
            .catch(function(registrationError) {
                console.log('SW registration failed');
            });
    });
}

// PWA Install prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    deferredPrompt = e;
    // Show install button if you want
});

document.addEventListener('DOMContentLoaded', function() {
    // Initialize real-time synchronization if Socket.IO is available
    if (typeof io !== 'undefined') {
        const socket = io();
        
        socket.on('connect', function() {
            console.log('Connected for real-time updates');
            socket.emit('join_dashboard');
        });
        
        socket.on('car_updated', function(carData) {
            console.log('Car updated:', carData);
            if (window.location.pathname === '/dashboard') {
                setTimeout(() => location.reload(), 500);
            }
        });
        
        socket.on('dashboard_refresh', function() {
            if (window.location.pathname === '/dashboard') {
                setTimeout(() => location.reload(), 500);
            }
        });
        
        window.addEventListener('beforeunload', function() {
            socket.emit('leave_dashboard');
        });
    }
    
    // Initialize tooltips if Bootstrap is available
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert.alert-dismissible');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // File upload preview for license plate photos
    var fileInput = document.getElementById('plate_photo');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            var file = e.target.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    // Remove any existing preview
                    var existingPreview = document.getElementById('plate-preview');
                    if (existingPreview) {
                        existingPreview.remove();
                    }
                    
                    // Create new preview
                    var preview = document.createElement('div');
                    preview.id = 'plate-preview';
                    preview.className = 'mt-3';
                    preview.innerHTML = '<strong>Preview:</strong><br><img src="' + e.target.result + '" class="img-thumbnail" style="max-width: 200px;">';
                    
                    fileInput.parentNode.appendChild(preview);
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Confirmation dialogs for important actions
    var confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            var message = button.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-refresh functionality
    function updateDashboardCounters() {
        if (window.location.pathname === '/dashboard') {
            fetch('/api/dashboard_data')
                .then(response => response.json())
                .then(data => {
                    if (!data.error) {
                        // Update counters with animation
                        updateCounterWithAnimation('washing-count', data.washing_count);
                        updateCounterWithAnimation('awaiting-payment-count', data.awaiting_payment_count);
                        updateCounterWithAnimation('finished-count', data.finished_count);
                        updateCounterWithAnimation('total-count', data.total_count);
                    }
                })
                .catch(error => {
                    console.log('Dashboard refresh error:', error);
                });
        }
    }
    
    function updateCounterWithAnimation(elementId, newValue) {
        var element = document.getElementById(elementId);
        if (element && element.textContent !== String(newValue)) {
            element.style.transform = 'scale(1.1)';
            element.textContent = newValue;
            setTimeout(() => {
                element.style.transform = 'scale(1)';
            }, 200);
        }
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + N for new car (washers only)
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            var addCarLink = document.querySelector('a[href*="add_car"]');
            if (addCarLink) {
                e.preventDefault();
                window.location.href = addCarLink.href;
            }
        }
        
        // Escape key to go back to dashboard
        if (e.key === 'Escape' && window.location.pathname !== '/dashboard') {
            var dashboardLink = document.querySelector('a[href*="dashboard"]');
            if (dashboardLink) {
                window.location.href = dashboardLink.href;
            }
        }
    });
    
    // Mobile-friendly touch interactions
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
        
        // Add touch feedback for buttons
        var buttons = document.querySelectorAll('.btn');
        buttons.forEach(function(button) {
            button.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.95)';
            });
            
            button.addEventListener('touchend', function() {
                this.style.transform = 'scale(1)';
            });
        });
    }
    
    // Print functionality for daily reports
    if (window.location.search.includes('print=1')) {
        window.print();
    }
});

// Utility functions
function setAmount(amount) {
    var paymentInput = document.getElementById('payment_amount');
    if (paymentInput) {
        paymentInput.value = amount.toFixed(2);
        paymentInput.focus();
    }
}

function showSuccess(message) {
    showAlert(message, 'success');
}

function showError(message) {
    showAlert(message, 'danger');
}

function showAlert(message, type) {
    var alertsContainer = document.querySelector('main .container');
    if (alertsContainer) {
        var alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        alertsContainer.insertBefore(alert, alertsContainer.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    }
}

// Service worker registration for offline capabilities (optional)
if ('serviceWorker' in navigator && window.location.protocol === 'https:') {
    navigator.serviceWorker.register('/static/sw.js')
        .then(registration => console.log('SW registered'))
        .catch(error => console.log('SW registration failed'));
}
