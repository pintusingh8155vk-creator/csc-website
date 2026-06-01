from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Customer, Service, Payment, Notification
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard home"""
    # Get statistics
    total_customers = Customer.query.filter_by(user_id=current_user.id).count()
    total_services = Service.query.join(Customer).filter(Customer.user_id == current_user.id).count()
    
    # Calculate total revenue
    total_payments = db.session.query(func.sum(Payment.amount)).join(Service).join(Customer).filter(
        Customer.user_id == current_user.id,
        Payment.payment_status == 'Completed'
    ).scalar() or 0
    
    # Recent services
    recent_services = Service.query.join(Customer).filter(
        Customer.user_id == current_user.id
    ).order_by(Service.created_at.desc()).limit(5).all()
    
    # Recent notifications
    notifications = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).limit(5).all()
    
    stats = {
        'total_customers': total_customers,
        'total_services': total_services,
        'total_payments': float(total_payments)
    }
    
    return render_template('dashboard/index.html', 
                         stats=stats,
                         recent_services=recent_services,
                         notifications=notifications)

@dashboard_bp.route('/api/chart-data')
@login_required
def chart_data():
    """Get chart data for dashboard"""
    try:
        # Get last 7 days revenue
        today = datetime.utcnow().date()
        data = []
        
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            revenue = db.session.query(func.sum(Payment.amount)).join(Service).join(Customer).filter(
                Customer.user_id == current_user.id,
                func.date(Payment.created_at) == date,
                Payment.payment_status == 'Completed'
            ).scalar() or 0
            data.append({'date': date.strftime('%Y-%m-%d'), 'revenue': float(revenue)})
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/mark-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_read(notification_id):
    """Mark notification as read"""
    try:
        notification = Notification.query.get(notification_id)
        if notification and notification.user_id == current_user.id:
            notification.is_read = True
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
