from . import db
from datetime import datetime
class UserSession(db.Model):
    __tablename__ = 'UserSession'
    ID = db.Column(db.Integer, primary_key=True)
    SessionUserId = db.Column(db.Integer, db.ForeignKey('User.UserId'), nullable=False)
    SessionId = db.Column(db.String(255), unique=True, nullable=False)
    Login_Time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, SessionUserId, SessionId):
        self.SessionUserId = SessionUserId
        self.SessionId = SessionId