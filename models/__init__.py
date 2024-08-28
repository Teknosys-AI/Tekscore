from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import your models so that they are registered with the db instance
from .user_model import User
from .role_model import Role
from .usersession_model import UserSession
