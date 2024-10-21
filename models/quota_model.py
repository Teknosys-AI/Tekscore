from . import db
class Quota(db.Model):
    __tablename__ = 'Quota'

    QuotaId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaxQuota = db.Column(db.Integer)
    UsedQuota = db.Column(db.Integer)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'))


    def __init__(self, MaxQuota=None, UsedQuota=None):
        self.MaxQuota = MaxQuota
        self.UsedQuota = UsedQuota