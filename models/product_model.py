from . import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the product
    description = db.Column(db.Text, nullable=True)   # Description of the product

    # Relationship to APIHit model for easy access to API hits related to this product
    api_hits = db.relationship('APIHit', backref='product', lazy=True)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description
