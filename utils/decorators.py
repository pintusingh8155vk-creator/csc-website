from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def login_required_custom(f):
    """Custom login required decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Admin required decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def subscription_required(f):
    """Subscription required decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        from models.subscription import Subscription
        subscription = Subscription.query.filter_by(user_id=current_user.id).first()
        
        if not subscription or not subscription.is_active:
            flash('Your subscription is inactive. Please renew your subscription.', 'warning')
            return redirect(url_for('pricing'))
        
        if subscription.is_expired():
            flash('Your subscription has expired. Please renew.', 'warning')
            return redirect(url_for('pricing'))
        
        return f(*args, **kwargs)
    return decorated_function
