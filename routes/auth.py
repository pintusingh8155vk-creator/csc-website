from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User
from models.subscription import Subscription
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def validate_mobile(mobile):
    """Validate Indian mobile number"""
    return bool(re.match(r'^[6-9]\d{9}$', mobile))

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        # Validate form data
        full_name = request.form.get('full_name', '').strip()
        shop_name = request.form.get('shop_name', '').strip()
        mobile_number = request.form.get('mobile_number', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        district = request.form.get('district', '').strip()
        address = request.form.get('address', '').strip()
        
        # Validation
        if not all([full_name, shop_name, mobile_number, email, password]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('auth.register'))
        
        if not validate_mobile(mobile_number):
            flash('Invalid mobile number. Use 10 digit Indian mobile number.', 'danger')
            return redirect(url_for('auth.register'))
        
        if not validate_email(email):
            flash('Invalid email format!', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(mobile_number=mobile_number).first():
            flash('Mobile number already registered!', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(shop_name=shop_name).first():
            flash('Shop name already taken!', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(
            full_name=full_name,
            shop_name=shop_name,
            mobile_number=mobile_number,
            email=email,
            district=district,
            address=address,
            is_admin=False,
            is_active=True
        )
        user.set_password(password)
        
        # Create free subscription
        subscription = Subscription(
            user=user,
            plan_name='free',
            is_active=True
        )
        
        try:
            db.session.add(user)
            db.session.add(subscription)
            db.session.commit()
            
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration!', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Email and password are required!', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Your account has been deactivated!', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        flash(f'Welcome back, {user.full_name}!', 'success')
        
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management"""
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name', current_user.full_name)
        current_user.district = request.form.get('district', current_user.district)
        current_user.address = request.form.get('address', current_user.address)
        current_user.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile!', 'danger')
        
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', user=current_user)