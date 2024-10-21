from . import db
from datetime import datetime
class Agreement(db.Model):
    __tablename__ = 'Agreement'

    AgreementId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'), nullable=False)
    agreement_time = db.Column(db.DateTime, nullable=False)


    def __init__(self, UserId, agreement_time):
        self.UserId = UserId
        self.agreement_time = agreement_time