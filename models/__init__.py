from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import your models so that they are registered with the db instance
from .user_model import User
from .role_model import Role
from .usersession_model import UserSession
from .quota_model import Quota
from .agreement_model import Agreement
from .subscriptiontype_model import SubscriptionType
from .user_product import UserProducts
from .product_model import Product
from .apihit_model import APIHit
from .changeplan_model import ChangePlan
from .plan_model import Plan