from . import db
from datetime import datetime

class Quota(db.Model):
    __tablename__ = 'Quota'

    QuotaId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaxQuota = db.Column(db.Integer)
    UsedQuota = db.Column(db.Integer)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    ProductId = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    SubscriptionTypeId = db.Column(db.Integer, db.ForeignKey('subscriptiontype.id'), nullable=True)
    Month = db.Column(db.Integer, nullable=False)
    Year = db.Column(db.Integer, nullable=False)

    def __init__(self, MaxQuota=None, UsedQuota=None, UserId=None, ProductId=None, SubscriptionTypeId=None, Month=None, Year=None):
        self.MaxQuota = MaxQuota
        self.UsedQuota = UsedQuota
        self.UserId = UserId
        self.ProductId = ProductId
        self.SubscriptionTypeId = SubscriptionTypeId
        self.Month = Month if Month is not None else datetime.utcnow().month
        self.Year = Year if Year is not None else datetime.utcnow().year
