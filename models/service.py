from extensions import db
from datetime import datetime

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, in-progress, completed, cancelled
    amount = db.Column(db.Float, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='service', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Service {self.service_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'service_type': self.service_type,
            'status': self.status,
            'amount': self.amount,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }