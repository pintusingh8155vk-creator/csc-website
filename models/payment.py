from extensions import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default='cash')  # cash, upi, card, bank_transfer
    payment_status = db.Column(db.String(50), default='completed')  # pending, completed, failed
    transaction_id = db.Column(db.String(100), unique=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'service_id': self.service_id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'transaction_id': self.transaction_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }