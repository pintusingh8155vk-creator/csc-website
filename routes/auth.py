from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from extensions import db
from models import User, Subscription
from utils.validators import validate_email, validate_indian_mobile
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        try:
            full_name = request.form.get('full_name', '').strip()
            shop_name = request.form.get('shop_name', '').strip()
            mobile_number = request.form.get('mobile_number', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Validation
            if not all([full_name, shop_name, mobile_number, email, password]):
                flash('All fields are required', 'danger')
                return redirect(url_for('auth.register'))
            
            if not validate_email(email):
                flash('Invalid email format', 'danger')
                return redirect(url_for('auth.register'))
            
            if not validate_indian_mobile(mobile_number):
                flash('Invalid mobile number (10 digits, starts with 6-9)', 'danger')
                return redirect(url_for('auth.register'))
            
            if password != confirm_password:
                flash('Passwords do not match', 'danger')
                return redirect(url_for('auth.register'))
            
            if len(password) < 6:
                flash('Password must be at least 6 characters', 'danger')
                return redirect(url_for('auth.register'))
            
            # Check if user exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'warning')
                return redirect(url_for('auth.login'))
            
            # Create user
            user = User(
                full_name=full_name,
                shop_name=shop_name,
                mobile_number=mobile_number,
                email=email,
                is_active=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Create free subscription
            subscription = Subscription(
                user_id=user.id,
                plan_name='Free',
                start_date=datetime.utcnow(),
                expiry_date=datetime.utcnow() + timedelta(days=365),
                is_active=True
            )
            db.session.add(subscription)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Registration error: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                if not user.is_active:
                    flash('Your account is deactivated', 'warning')
                    return redirect(url_for('auth.login'))
                
                login_user(user, remember=True)
                flash(f'Welcome back, {user.full_name}!', 'success')
                return redirect(url_for('dashboard.index'))
            else:
                flash('Invalid email or password', 'danger')
        
        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile"""
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    return render_template('auth/profile.html', user=current_user, subscription=subscription)

@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    try:
        current_user.full_name = request.form.get('full_name', current_user.full_name)
        current_user.shop_name = request.form.get('shop_name', current_user.shop_name)
        current_user.mobile_number = request.form.get('mobile_number', current_user.mobile_number)
        current_user.district = request.form.get('district', current_user.district)
        current_user.address = request.form.get('address', current_user.address)
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Update error: {str(e)}', 'danger')
    
    return redirect(url_for('auth.profile'))
