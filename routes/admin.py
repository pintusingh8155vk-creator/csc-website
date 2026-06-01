from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import User, Subscription, Service, Payment
from functools import wraps
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/secure-admin-panel')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('-login', methods=['GET', 'POST'])
def login():
    """Admin panel login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, is_admin=True).first()
        
        if user and user.check_password(password):
            from flask_login import login_user
            login_user(user, remember=True)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('-dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    total_services = Service.query.count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).scalar() or 0
    
    stats = {
        'total_users': total_users,
        'total_services': total_services,
        'total_revenue': float(total_revenue)
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('-users')
@login_required
@admin_required
def users():
    """List all users"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('-users/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    """View user details"""
    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    
    stats = {
        'total_customers': len(user.customers),
        'total_services': sum(len(c.services) for c in user.customers),
        'total_payments': sum(p.amount for p in Payment.query.filter_by(user_id=user_id).all())
    }
    
    return render_template('admin/view_user.html', user=user, stats=stats)

@admin_bp.route('-subscriptions')
@login_required
@admin_required
def subscriptions():
    """List all subscriptions"""
    subscriptions = Subscription.query.all()
    return render_template('admin/subscriptions.html', subscriptions=subscriptions)
