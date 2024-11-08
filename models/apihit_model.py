from . import db
from datetime import datetime


class APIHit(db.Model):
    __tablename__ = 'APIHit'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.UserId'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # New column for product ID
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)  # New column for success status (default: False)
    score = db.Column(db.Integer, nullable=True)


    def __init__(self, user_id, product_id, mobile_number,score, status=False, timestamp=None):
        self.user_id = user_id
        self.product_id = product_id
        self.mobile_number = mobile_number
        self.status = status
        self.timestamp = timestamp if timestamp else datetime.now()
        self.month = self.timestamp.month
        self.day = self.timestamp.day
        self.score = score
