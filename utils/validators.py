import re
from datetime import datetime

def validate_indian_mobile(mobile):
    """Validate Indian mobile number"""
    pattern = r'^[6-9]\d{9}$'
    return bool(re.match(pattern, str(mobile)))

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_aadhaar(aadhaar):
    """Validate Aadhaar number (12 digits)"""
    return bool(re.match(r'^[0-9]{12}$', str(aadhaar)))

def validate_pan(pan):
    """Validate PAN format"""
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return bool(re.match(pattern, pan.upper()))

def format_currency(amount):
    """Format amount as Indian currency"""
    return f"₹{amount:,.2f}"

def format_date(date, format='%d %b %Y'):
    """Format date"""
    if isinstance(date, str):
        return date
    return date.strftime(format) if date else '-'

def get_days_remaining(expiry_date):
    """Get days remaining till expiry"""
    if not expiry_date:
        return None
    remaining = expiry_date - datetime.utcnow()
    return max(0, remaining.days)

def is_subscription_expiring_soon(expiry_date, days=7):
    """Check if subscription is expiring soon"""
    if not expiry_date:
        return False
    days_left = get_days_remaining(expiry_date)
    return days_left is not None and 0 <= days_left <= days
