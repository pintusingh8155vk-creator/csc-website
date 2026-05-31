from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.customer import Customer
from models.service import Service
from extensions import db
from datetime import datetime

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

@customer_bp.route('/')
@login_required
def list_customers():
    """List all customers"""
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    
    query = Customer.query.filter_by(user_id=current_user.id)
    
    if search:
        query = query.filter(
            db.or_(
                Customer.full_name.ilike(f'%{search}%'),
                Customer.mobile_number.ilike(f'%{search}%'),
                Customer.village.ilike(f'%{search}%')
            )
        )
    
    customers = query.paginate(page=page, per_page=10)
    return render_template('customer/list.html', customers=customers, search=search)

@customer_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_customer():
    """Create new customer"""
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        mobile_number = request.form.get('mobile_number', '').strip()
        aadhaar_last_4 = request.form.get('aadhaar_last_4', '').strip()
        address = request.form.get('address', '').strip()
        village = request.form.get('village', '').strip()
        notes = request.form.get('notes', '').strip()
        
        if not full_name:
            flash('Customer name is required!', 'danger')
            return redirect(url_for('customer.create_customer'))
        
        customer = Customer(
            user_id=current_user.id,
            full_name=full_name,
            mobile_number=mobile_number,
            aadhaar_last_4=aadhaar_last_4,
            address=address,
            village=village,
            notes=notes
        )
        
        try:
            db.session.add(customer)
            db.session.commit()
            flash('Customer created successfully!', 'success')
            return redirect(url_for('customer.list_customers'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating customer!', 'danger')
            return redirect(url_for('customer.create_customer'))
    
    return render_template('customer/create.html')

@customer_bp.route('/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def view_customer(customer_id):
    """View/edit customer details"""
    customer = Customer.query.filter_by(id=customer_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        customer.full_name = request.form.get('full_name', customer.full_name)
        customer.mobile_number = request.form.get('mobile_number', customer.mobile_number)
        customer.aadhaar_last_4 = request.form.get('aadhaar_last_4', customer.aadhaar_last_4)
        customer.address = request.form.get('address', customer.address)
        customer.village = request.form.get('village', customer.village)
        customer.notes = request.form.get('notes', customer.notes)
        customer.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Customer updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating customer!', 'danger')
        
        return redirect(url_for('customer.view_customer', customer_id=customer.id))
    
    services = Service.query.filter_by(customer_id=customer_id).order_by(Service.created_at.desc()).all()
    return render_template('customer/view.html', customer=customer, services=services)

@customer_bp.route('/<int:customer_id>/delete', methods=['POST'])
@login_required
def delete_customer(customer_id):
    """Delete customer"""
    customer = Customer.query.filter_by(id=customer_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(customer)
        db.session.commit()
        flash('Customer deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting customer!', 'danger')
    
    return redirect(url_for('customer.list_customers'))

@customer_bp.route('/api/search')
@login_required
def search_customers():
    """Search customers via API"""
    search = request.args.get('q', '').strip()
    limit = request.args.get('limit', 10, type=int)
    
    customers = Customer.query.filter(
        Customer.user_id == current_user.id,
        db.or_(
            Customer.full_name.ilike(f'%{search}%'),
            Customer.mobile_number.ilike(f'%{search}%')
        )
    ).limit(limit).all()
    
    return jsonify([c.to_dict() for c in customers])