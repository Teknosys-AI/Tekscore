from functools import wraps
from flask import session, redirect, url_for, flash
from models.role_model import Role

def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import logging
            logger = logging.getLogger(__name__)
            
            if 'userId' not in session:
                logger.warning(f"role_required('{role_name}'): No userId in session")
                flash("Please log in to access this page.", "warning")
                return redirect(url_for('user.show_login'))
            
            user_role_id = session.get('RoleID')
            required_role = Role.query.filter_by(Name=role_name).first()
            
            logger.info(f"role_required('{role_name}'): userId={session.get('userId')}, session['RoleID']={user_role_id}, required_role={required_role.RoleId if required_role else None}")

            if not required_role:
                logger.error(f"role_required('{role_name}'): Role '{role_name}' not found in database!")
                flash("System configuration error. Please contact support for assistance.", "danger")
                return redirect(url_for('user.show_login'))
            
            if str(user_role_id) != str(required_role.RoleId):
                logger.warning(f"role_required('{role_name}'): Access denied - User RoleID={user_role_id}, Required RoleID={required_role.RoleId}")
                # Get user's current role name for better error message
                user_role = Role.query.filter_by(RoleId=user_role_id).first()
                user_role_name = user_role.Name if user_role else "Unknown"
                flash(f"Access denied. This page requires '{role_name}' role, but your account has '{user_role_name}' role. Please contact your administrator if you need access.", "danger")
                return redirect(url_for('user.show_login'))
            
            logger.info(f"role_required('{role_name}'): Access granted for userId={session.get('userId')}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
