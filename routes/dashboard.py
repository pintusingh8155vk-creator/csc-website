from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models.customer import Customer
from models.service import Service
from models.payment import Payment
from models.notification import Notification
from models.subscription import Subscription
from extensions import db
from datetime import datetime, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard home"""
    # Get statistics
    total_customers = Customer.query.filter_by(user_id=current_user.id).count()
    
    services = Service.query.join(Customer).filter(
        Customer.user_id == current_user.id
    )
    pending_services = services.filter_by(status='pending').count()
    completed_services = services.filter_by(status='completed').count()
    
    # Today's earnings
    today = datetime.utcnow().date()
    today_payments = Payment.query.filter(
        Payment.user_id == current_user.id,
        func.date(Payment.created_at) == today,
        Payment.payment_status == 'completed'
    ).all()
    today_earnings = sum(p.amount for p in today_payments)
    
    # Get subscription
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    
    # Get notifications
    notifications = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    # Chart data - last 7 days revenue
    revenue_data = []
    for i in range(6, -1, -1):
        date = (datetime.utcnow() - timedelta(days=i)).date()
        daily_revenue = db.session.query(func.sum(Payment.amount)).filter(
            Payment.user_id == current_user.id,
            func.date(Payment.created_at) == date,
            Payment.payment_status == 'completed'
        ).scalar() or 0
        revenue_data.append({
            'date': date.strftime('%a'),
            'revenue': float(daily_revenue)
        })
    
    context = {
        'total_customers': total_customers,
        'pending_services': pending_services,
        'completed_services': completed_services,
        'today_earnings': today_earnings,
        'subscription': subscription,
        'notifications': notifications,
        'revenue_data': revenue_data
    }
    
    return render_template('dashboard/index.html', **context)

@dashboard_bp.route('/api/chart-data')
@login_required
def chart_data():
    """Get chart data as JSON"""
    # Revenue data
    revenue_data = []
    for i in range(6, -1, -1):
        date = (datetime.utcnow() - timedelta(days=i)).date()
        daily_revenue = db.session.query(func.sum(Payment.amount)).filter(
            Payment.user_id == current_user.id,
            func.date(Payment.created_at) == date,
            Payment.payment_status == 'completed'
        ).scalar() or 0
        revenue_data.append({
            'date': date.strftime('%b %d'),
            'revenue': float(daily_revenue)
        })
    
    # Service breakdown
    services = Service.query.join(Customer).filter(
        Customer.user_id == current_user.id
    ).all()
    
    service_types = {}
    for service in services:
        if service.service_type not in service_types:
            service_types[service.service_type] = 0
        service_types[service.service_type] += 1
    
    return jsonify({
        'revenue': revenue_data,
        'services': service_types
    })