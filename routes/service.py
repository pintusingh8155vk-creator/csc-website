from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Service, Customer, Payment, Notification
from datetime import datetime

service_bp = Blueprint('service', __name__, url_prefix='/services')

@service_bp.route('/')
@login_required
def list_services():
    """List all services"""
    services = Service.query.join(Customer).filter(
        Customer.user_id == current_user.id
    ).all()
    return render_template('service/list.html', services=services)

@service_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new service"""
    if request.method == 'POST':
        try:
            customer_id = request.form.get('customer_id')
            customer = Customer.query.get(customer_id)
            
            if not customer or customer.user_id != current_user.id:
                flash('Customer not found', 'danger')
                return redirect(url_for('service.create'))
            
            service = Service(
                customer_id=customer_id,
                service_type=request.form.get('service_type'),
                status='Pending',
                amount=float(request.form.get('amount', 0)),
                submission_date=datetime.utcnow(),
                notes=request.form.get('notes')
            )
            db.session.add(service)
            db.session.commit()
            
            # Create notification
            notification = Notification(
                user_id=current_user.id,
                type='service',
                title='New Service Created',
                message=f'Service {service.service_type} created for {customer.full_name}'
            )
            db.session.add(notification)
            db.session.commit()
            
            flash('Service created successfully', 'success')
            return redirect(url_for('service.view', service_id=service.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    customers = Customer.query.filter_by(user_id=current_user.id).all()
    return render_template('service/create.html', customers=customers)

@service_bp.route('/<int:service_id>')
@login_required
def view(service_id):
    """View service details"""
    service = Service.query.get(service_id)
    if not service or service.customer.user_id != current_user.id:
        flash('Service not found', 'danger')
        return redirect(url_for('service.list_services'))
    
    payments = Payment.query.filter_by(service_id=service_id).all()
    return render_template('service/view.html', service=service, payments=payments)

@service_bp.route('/<int:service_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(service_id):
    """Edit service"""
    service = Service.query.get(service_id)
    if not service or service.customer.user_id != current_user.id:
        flash('Service not found', 'danger')
        return redirect(url_for('service.list_services'))
    
    if request.method == 'POST':
        try:
            service.service_type = request.form.get('service_type')
            service.status = request.form.get('status')
            service.amount = float(request.form.get('amount', 0))
            service.notes = request.form.get('notes')
            
            if service.status == 'Completed':
                service.completion_date = datetime.utcnow()
            
            db.session.commit()
            flash('Service updated successfully', 'success')
            return redirect(url_for('service.view', service_id=service_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('service/edit.html', service=service)

@service_bp.route('/<int:service_id>/payment', methods=['GET', 'POST'])
@login_required
def record_payment(service_id):
    """Record payment for service"""
    service = Service.query.get(service_id)
    if not service or service.customer.user_id != current_user.id:
        flash('Service not found', 'danger')
        return redirect(url_for('service.list_services'))
    
    if request.method == 'POST':
        try:
            payment = Payment(
                user_id=current_user.id,
                service_id=service_id,
                amount=float(request.form.get('amount', 0)),
                payment_method=request.form.get('payment_method'),
                payment_status='Completed',
                transaction_id=request.form.get('transaction_id'),
                notes=request.form.get('notes')
            )
            db.session.add(payment)
            db.session.commit()
            
            # Create notification
            notification = Notification(
                user_id=current_user.id,
                type='payment',
                title='Payment Received',
                message=f'Payment of ₹{payment.amount} received for {service.service_type}'
            )
            db.session.add(notification)
            db.session.commit()
            
            flash('Payment recorded successfully', 'success')
            return redirect(url_for('service.view', service_id=service_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('service/payment.html', service=service)
