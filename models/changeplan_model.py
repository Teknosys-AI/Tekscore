
from . import db 
from datetime import datetime


class ChangePlan(db.Model):
    __tablename__ = 'Change_Plan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.now())
    time = db.Column(db.Time, default=datetime.now().time)
    userid = db.Column(db.Integer, db.ForeignKey('User.UserId'), nullable=False)
    user_email = db.Column(db.String(255))
    planid = db.Column(db.Integer, db.ForeignKey('Plan.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    
    
    # Define relationships
    user = db.relationship("User", backref="change_requests")
    plan = db.relationship("Plan", backref="change_requests")  # This line fixes the issue

