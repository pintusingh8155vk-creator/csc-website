from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Customer, Service

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

@customer_bp.route('/')
@login_required
def list_customers():
    """List all customers"""
    customers = Customer.query.filter_by(user_id=current_user.id).all()
    return render_template('customer/list.html', customers=customers)

@customer_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new customer"""
    if request.method == 'POST':
        try:
            customer = Customer(
                user_id=current_user.id,
                full_name=request.form.get('full_name'),
                mobile_number=request.form.get('mobile_number'),
                aadhaar_last_4=request.form.get('aadhaar_last_4'),
                address=request.form.get('address'),
                village=request.form.get('village'),
                notes=request.form.get('notes')
            )
            db.session.add(customer)
            db.session.commit()
            flash('Customer created successfully', 'success')
            return redirect(url_for('customer.view', customer_id=customer.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('customer/create.html')

@customer_bp.route('/<int:customer_id>')
@login_required
def view(customer_id):
    """View customer details"""
    customer = Customer.query.get(customer_id)
    if not customer or customer.user_id != current_user.id:
        flash('Customer not found', 'danger')
        return redirect(url_for('customer.list_customers'))
    
    services = Service.query.filter_by(customer_id=customer_id).all()
    return render_template('customer/view.html', customer=customer, services=services)

@customer_bp.route('/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(customer_id):
    """Edit customer"""
    customer = Customer.query.get(customer_id)
    if not customer or customer.user_id != current_user.id:
        flash('Customer not found', 'danger')
        return redirect(url_for('customer.list_customers'))
    
    if request.method == 'POST':
        try:
            customer.full_name = request.form.get('full_name')
            customer.mobile_number = request.form.get('mobile_number')
            customer.aadhaar_last_4 = request.form.get('aadhaar_last_4')
            customer.address = request.form.get('address')
            customer.village = request.form.get('village')
            customer.notes = request.form.get('notes')
            db.session.commit()
            flash('Customer updated successfully', 'success')
            return redirect(url_for('customer.view', customer_id=customer_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('customer/edit.html', customer=customer)

@customer_bp.route('/<int:customer_id>/delete', methods=['POST'])
@login_required
def delete(customer_id):
    """Delete customer"""
    customer = Customer.query.get(customer_id)
    if not customer or customer.user_id != current_user.id:
        flash('Customer not found', 'danger')
        return redirect(url_for('customer.list_customers'))
    
    try:
        # Delete related services
        Service.query.filter_by(customer_id=customer_id).delete()
        db.session.delete(customer)
        db.session.commit()
        flash('Customer deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('customer.list_customers'))
