from extensions import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    mobile_number = db.Column(db.String(15))
    aadhaar_last_4 = db.Column(db.String(4))
    address = db.Column(db.Text)
    village = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    services = db.relationship('Service', backref='customer', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.full_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'mobile_number': self.mobile_number,
            'aadhaar_last_4': self.aadhaar_last_4,
            'address': self.address,
            'village': self.village,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }