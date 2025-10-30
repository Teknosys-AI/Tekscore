from . import db

class UserProducts(db.Model):
    __tablename__ = 'user_products'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    # change_plan_id = db.Column(db.Integer, db.ForeignKey('change_plan.id'), nullable=True) 

    # Define composite primary key
    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'product_id'),
    )

    # change_plan = db.relationship("ChangePlan", backref="user_products")

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id
        # self.change_plan_id = change_plan_id  # Optional, can be None
        

       
