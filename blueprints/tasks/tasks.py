from functools import wraps
from flask import session, redirect, url_for, flash
from models.role_model import Role

def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'userId' not in session:
                flash("You need to log in first.", "error")
                return redirect(url_for('user.show_login'))
            
            user_role_id = session.get('RoleID')
            business_role = Role.query.filter_by(Name=role_name).first()

            if not business_role or str(user_role_id) != str(business_role.RoleId):  # Convert both to string for safety
                flash("Unauthorized access!", "error")
                return redirect(url_for('user.show_login'))
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
