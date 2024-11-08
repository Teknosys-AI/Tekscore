from . import db

class SubscriptionType(db.Model):
    __tablename__ = 'subscriptiontype'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subscriptiontype = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

    def __init__(self, subscriptiontype, description=None):
        self.subscriptiontype = subscriptiontype
        self.description = description
        
