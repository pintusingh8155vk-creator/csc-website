from extensions import db
from datetime import datetime, timedelta

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)  # free, starter, professional, enterprise
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Plan details
    PLANS = {
        'free': {'price': 0, 'days': 0, 'features': ['Basic Dashboard', '5 Customers', 'Basic Reports']},
        'starter': {'price': 499, 'days': 30, 'features': ['All Free features', 'Unlimited Customers', 'Advanced Reports']},
        'professional': {'price': 999, 'days': 30, 'features': ['All Starter features', 'Payment Processing', 'Email Support']},
        'enterprise': {'price': 2999, 'days': 30, 'features': ['All features', 'Priority Support', 'Custom Reports']}
    }
    
    def __repr__(self):
        return f'<Subscription {self.plan_name}>'
    
    def is_expired(self):
        """Check if subscription is expired"""
        if not self.expiry_date:
            return False
        return datetime.utcnow() > self.expiry_date
    
    def days_remaining(self):
        """Get days remaining in subscription"""
        if not self.expiry_date:
            return None
        remaining = self.expiry_date - datetime.utcnow()
        return max(0, remaining.days)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_name': self.plan_name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'is_active': self.is_active,
            'is_expired': self.is_expired(),
            'days_remaining': self.days_remaining(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }