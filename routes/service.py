from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.service import Service
from models.customer import Customer
from models.payment import Payment
from extensions import db
from datetime import datetime

service_bp = Blueprint('service', __name__, url_prefix='/services')

@service_bp.route('/')
@login_required
def list_services():
    """List all services"""
    status = request.args.get('status', 'all')
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    
    query = Service.query.join(Customer).filter(Customer.user_id == current_user.id)
    
    if status != 'all':
        query = query.filter(Service.status == status)
    
    if search:
        query = query.filter(
            db.or_(
                Customer.full_name.ilike(f'%{search}%'),
                Service.service_type.ilike(f'%{search}%')
            )
        )
    
    services = query.paginate(page=page, per_page=10)
    return render_template('service/list.html', services=services, status=status, search=search)

@service_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_service():
    """Create new service"""
    if request.method == 'POST':
        customer_id = request.form.get('customer_id', type=int)
        service_type = request.form.get('service_type', '').strip()
        amount = request.form.get('amount', type=float)
        notes = request.form.get('notes', '').strip()
        
        if not all([customer_id, service_type, amount]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('service.create_service'))
        
        # Verify customer ownership
        customer = Customer.query.filter_by(id=customer_id, user_id=current_user.id).first()
        if not customer:
            flash('Invalid customer!', 'danger')
            return redirect(url_for('service.create_service'))
        
        service = Service(
            customer_id=customer_id,
            service_type=service_type,
            status='pending',
            amount=amount,
            notes=notes
        )
        
        try:
            db.session.add(service)
            db.session.commit()
            flash('Service created successfully!', 'success')
            return redirect(url_for('service.list_services'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating service!', 'danger')
            return redirect(url_for('service.create_service'))
    
    customers = Customer.query.filter_by(user_id=current_user.id).all()
    return render_template('service/create.html', customers=customers)

@service_bp.route('/<int:service_id>', methods=['GET', 'POST'])
@login_required
def view_service(service_id):
    """View/edit service"""
    service = Service.query.filter(
        Service.id == service_id,
        Service.customer.has(user_id=current_user.id)
    ).first_or_404()
    
    if request.method == 'POST':
        service.service_type = request.form.get('service_type', service.service_type)
        service.status = request.form.get('status', service.status)
        service.amount = request.form.get('amount', service.amount, type=float)
        service.notes = request.form.get('notes', service.notes)
        
        if service.status == 'completed':
            service.completion_date = datetime.utcnow()
        
        service.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Service updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating service!', 'danger')
        
        return redirect(url_for('service.view_service', service_id=service.id))
    
    payments = Payment.query.filter_by(service_id=service_id).all()
    return render_template('service/view.html', service=service, payments=payments)

@service_bp.route('/<int:service_id>/delete', methods=['POST'])
@login_required
def delete_service(service_id):
    """Delete service"""
    service = Service.query.filter(
        Service.id == service_id,
        Service.customer.has(user_id=current_user.id)
    ).first_or_404()
    
    try:
        db.session.delete(service)
        db.session.commit()
        flash('Service deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting service!', 'danger')
    
    return redirect(url_for('service.list_services'))

@service_bp.route('/<int:service_id>/payment', methods=['POST'])
@login_required
def record_payment(service_id):
    """Record payment for service"""
    service = Service.query.filter(
        Service.id == service_id,
        Service.customer.has(user_id=current_user.id)
    ).first_or_404()
    
    amount = request.form.get('amount', type=float)
    payment_method = request.form.get('payment_method', 'cash')
    transaction_id = request.form.get('transaction_id', '').strip()
    
    if not amount or amount <= 0:
        flash('Invalid amount!', 'danger')
        return redirect(url_for('service.view_service', service_id=service_id))
    
    payment = Payment(
        user_id=current_user.id,
        service_id=service_id,
        amount=amount,
        payment_method=payment_method,
        payment_status='completed',
        transaction_id=transaction_id
    )
    
    try:
        db.session.add(payment)
        db.session.commit()
        flash('Payment recorded successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error recording payment!', 'danger')
    
    return redirect(url_for('service.view_service', service_id=service_id))