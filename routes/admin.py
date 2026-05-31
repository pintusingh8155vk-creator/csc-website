from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models.user import User
from models.subscription import Subscription
from extensions import db
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/secure-admin-panel')

def admin_required(f):
    """Decorator to check admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied!', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('-login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        admin_code = request.form.get('admin_code', '').strip()
        
        user = User.query.filter_by(email=email, is_admin=True).first()
        
        if user and user.check_password(password):
            from flask_login import login_user
            login_user(user, remember=True)
            flash('Admin panel access granted!', 'success')
            return redirect(url_for('admin.dashboard'))
        
        flash('Invalid credentials!', 'danger')
        return redirect(url_for('admin.login'))
    
    return render_template('admin/login.html')

@admin_bp.route('-dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    total_users = User.query.filter_by(is_admin=False).count()
    active_users = User.query.filter_by(is_admin=False, is_active=True).count()
    total_subscriptions = Subscription.query.count()
    active_subscriptions = Subscription.query.filter_by(is_active=True).count()
    
    # Get subscription breakdown
    subscription_breakdown = db.session.query(
        Subscription.plan_name,
        db.func.count(Subscription.id)
    ).group_by(Subscription.plan_name).all()
    
    recent_users = User.query.filter_by(is_admin=False).order_by(
        User.created_at.desc()
    ).limit(10).all()
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_subscriptions': total_subscriptions,
        'active_subscriptions': active_subscriptions,
        'subscription_breakdown': subscription_breakdown,
        'recent_users': recent_users
    }
    
    return render_template('admin/dashboard.html', **context)

@admin_bp.route('-users')
@login_required
@admin_required
def users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    
    query = User.query.filter_by(is_admin=False)
    
    if search:
        query = query.filter(
            db.or_(
                User.full_name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
                User.shop_name.ilike(f'%{search}%')
            )
        )
    
    users = query.paginate(page=page, per_page=20)
    return render_template('admin/users.html', users=users, search=search)

@admin_bp.route('-user/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    """View user details"""
    user = User.query.filter_by(id=user_id, is_admin=False).first_or_404()
    subscription = Subscription.query.filter_by(user_id=user_id).first()
    
    stats = {
        'total_customers': len(user.customers),
        'total_payments': sum(p.amount for p in user.payments),
        'total_services': sum(len(c.services) for c in user.customers)
    }
    
    return render_template('admin/view_user.html', user=user, subscription=subscription, stats=stats)

@admin_bp.route('-user/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status"""
    user = User.query.filter_by(id=user_id, is_admin=False).first_or_404()
    user.is_active = not user.is_active
    
    try:
        db.session.commit()
        status = 'activated' if user.is_active else 'deactivated'
        flash(f'User {status} successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating user status!', 'danger')
    
    return redirect(url_for('admin.view_user', user_id=user_id))

@admin_bp.route('-subscriptions')
@login_required
@admin_required
def subscriptions():
    """Manage subscriptions"""
    page = request.args.get('page', 1, type=int)
    plan = request.args.get('plan', 'all')
    
    query = Subscription.query
    
    if plan != 'all':
        query = query.filter_by(plan_name=plan)
    
    subscriptions = query.paginate(page=page, per_page=20)
    plans = [sub[0] for sub in db.session.query(Subscription.plan_name).distinct()]
    
    return render_template('admin/subscriptions.html', subscriptions=subscriptions, plans=plans, current_plan=plan)