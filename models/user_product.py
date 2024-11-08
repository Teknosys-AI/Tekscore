from . import db

class UserProducts(db.Model):
    __tablename__ = 'user_products'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    # Define composite primary key
    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'product_id'),
    )

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

       
