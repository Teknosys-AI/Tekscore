import time
import bleach
import logging
import hashlib
from markupsafe import escape
import datetime
from models.role_model import Role
from models.user_model import User, db
from models.agreement_model import Agreement
from models.usersession_model import UserSession
from ..api_util.api_utils import call_Jscore_api_function
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, flash, session, abort, make_response
from utils.error_handler import ErrorHandler



user_bp = Blueprint("user", __name__, template_folder="templates/users")
logger = logging.getLogger(__name__)






@user_bp.route('/login', methods=['GET'])
def show_login():
    # Clear any old flash messages that might have accumulated from 404 errors
    # This ensures a clean login page
    return render_template('login.html')
    

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        # Check database connection with detailed logging
        from sqlalchemy import text
        logger.info("="*60)
        logger.info("LOGIN ATTEMPT - Database Connection Check")
        logger.info("="*60)
        try:
            logger.info(f"Attempting to connect to database...")
            logger.info(f"Database URI: {db.engine.url}")
            logger.info(f"Database engine: {db.engine}")
            
            with db.engine.connect() as conn:
                logger.info("Database connection established successfully")
                # Use text() for SQLAlchemy 2.0+ compatibility
                result = conn.execute(text("SELECT 1"))
                logger.info(f"Test query executed successfully")
                logger.info("[OK] Database connection successful during login.")
        except Exception as db_err:
            logger.error("="*60)
            logger.error("[ERROR] DATABASE CONNECTION FAILED")
            logger.error("="*60)
            logger.error(f"Error Type: {type(db_err).__name__}")
            logger.error(f"Error Message: {str(db_err)}")
            logger.error(f"Error Details: {repr(db_err)}")
            import traceback
            logger.error(f"Full Traceback:\n{traceback.format_exc()}")
            logger.error(f"Database URI: {db.engine.url if hasattr(db, 'engine') else 'N/A'}")
            logger.error("="*60)
            # Use user-friendly error message
            user_message = ErrorHandler.format_database_error(db_err)
            flash(user_message, 'danger')
            return redirect(url_for('user.show_login'))
        
        # Prevent browser caching for this route
        response = make_response()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'

        # Check if the user is locked out
        if session.get('login_locked'):
            lock_time = session['login_locked']
            current_time = time.time()
            if current_time < lock_time:
                remaining_seconds = int(lock_time - current_time)
                flash(f'Too many login attempts. Your account is temporarily locked. Please try again in {remaining_seconds} seconds.', 'warning')
                return redirect(url_for('user.show_login'))
            else:
                session.pop('login_locked', None)  # Unlock after timeout

        # Get and validate username
        username_raw = request.form.get('username', '').strip()
        if not username_raw:
            flash("Please enter your username.", 'danger')
            return redirect(url_for('user.show_login'))
        
        # Validate username format
        is_valid_username, username_error = ErrorHandler.validate_username(username_raw)
        if not is_valid_username:
            flash(username_error, 'danger')
            return redirect(url_for('user.show_login'))
        
        username = bleach.clean(username_raw)
        
        # Get and validate password
        password_raw = request.form.get('password', '').strip()
        if not password_raw:
            flash("Please enter your password.", 'danger')
            return redirect(url_for('user.show_login'))
        
        # Validate password format
        is_valid_password, password_error = ErrorHandler.validate_password(password_raw)
        if not is_valid_password:
            flash(password_error, 'danger')
            return redirect(url_for('user.show_login'))
        
        password = bleach.clean(password_raw)

        # Query to find the user
        user = User.query.filter_by(
            Username=username,
            Password=hashlib.sha256(password.encode()).hexdigest()
        ).first()
        

        if user:
            logger.info(f"Login attempt: Username={username}, UserId={user.UserId}, RoleId={user.RoleId}")
            
            # Check if user has Business role (RoleId == 5)
            business_role = Role.query.filter_by(Name="Business").first()
            
            if business_role and user.RoleId == business_role.RoleId: 
                session.clear()  # Clear the temporary session data
                session['userId'] = user.UserId
                session['username'] = user.Username
                session['RoleID'] = user.RoleId
                session.permanent = True
                logger.info(f"Business user logged in: {user.Username} (UserId: {user.UserId}, RoleID={user.RoleId})")
                return redirect(url_for('businessusers.pending_changes'))
            
            # Clear any previous session-related flags
            session.pop('failed_attempts', None)

            # Check if user has already agreed to privacy policy
            existing_agreement = Agreement.query.filter_by(UserId=user.UserId).first()
            
            if existing_agreement:
                # User has already agreed, skip privacy policy and go directly to dashboard
                session.clear()  # Clear any old session data first
                session['userId'] = user.UserId
                session['username'] = user.Username
                session['agreementuserid'] = user.UserId
                session['RoleID'] = user.RoleId
                session.permanent = True
                session.modified = True
                logger.info(f"User logged in (already agreed): {user.Username} (UserId: {user.UserId}, RoleId: {user.RoleId})")
                return redirect(url_for('jscore.index'))
            
            # User hasn't agreed yet, temporarily store user details until agreement
            session.clear()  # Clear any old session data first
            session['temp_user_id'] = user.UserId
            session['temp_username'] = user.Username
            session['temp_RoleID'] = user.RoleId
            session.permanent = True
            session.modified = True  # Ensure session is saved
            logger.info(f"User logged in (pending agreement): {user.Username} (UserId: {user.UserId}, RoleId: {user.RoleId}, temp_RoleID={session.get('temp_RoleID')})")

            # Redirect to privacy policy page for agreement
            return redirect(url_for('user.privacy_policy'))

        else:
            # Handle failed login logic...
            failed_attempts = session.get('failed_attempts', 0) + 1
            session['failed_attempts'] = failed_attempts
            session.modified = True
            
            if failed_attempts >= 5:
                session['login_locked'] = time.time() + 60  # Lock for 1 minute
                session.pop('failed_attempts', None)  # Reset failed attempts counter
                flash('Too many failed login attempts. Your account has been temporarily locked for 1 minute. Please try again after the lock period expires.', 'danger')
                return redirect(url_for('user.show_login'))
            else:
                remaining_attempts = 5 - failed_attempts
                if remaining_attempts > 0:
                    flash(f"Invalid username or password. You have {remaining_attempts} attempt(s) remaining before your account is temporarily locked.", 'danger')
                else:
                    flash("Invalid username or password.", 'danger')
                return redirect(url_for('user.show_login'))

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        # Check if it's a database error
        if 'database' in str(e).lower() or 'sql' in str(e).lower() or 'connection' in str(e).lower():
            user_message = ErrorHandler.format_database_error(e)
        else:
            user_message = "An unexpected error occurred during login. Please try again later. If the problem persists, contact support."
        flash(user_message, 'danger')
        return redirect(url_for('user.show_login'))






@user_bp.route('/logout')
def logout():
    try:
        user_id = session.get('userId')
        session_id = session.get('session_id')
        if user_id and session_id:
            # Clear the session from the database
            UserSession.query.filter_by(SessionUserId=user_id, SessionId=session_id).delete()
            db.session.commit()

        session.clear()
        return redirect(url_for('user.show_login'))
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}", exc_info=True)
        # Even if logout fails, clear the session and redirect
        session.clear()
        flash("You have been logged out. If you encountered any issues, please contact support.", 'info')
        return redirect(url_for('user.show_login'))



        
@user_bp.route('/notfound')
def notfound():
    return render_template('404.html'), 404



@user_bp.route('/privacy_policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html')


@user_bp.route('/agree_privacy', methods=['POST'])
def agree_privacy():
    try:
        # Retrieve the temporary user information
        temp_user_id = session.get('temp_user_id')
        temp_username = session.get('temp_username')
        temp_RoleID = session.get('temp_RoleID')
        

        if not temp_user_id or not temp_username:
            flash("Your session has expired. Please log in again to continue.", 'warning')
            return redirect(url_for('user.show_login'))

        
        

        # Create a new session in the database
        session_id = str(time.time())  # Generate a unique session ID

        session['session_id'] = session_id
        current_time = datetime.datetime.now()
        # Store the user's agreement in the Agreement table
        new_agreement = Agreement(UserId=temp_user_id, agreement_time=current_time)
        db.session.add(new_agreement)
        db.session.commit()

        # Now create the full session
        session.clear()  # Clear the temporary session data
        session['userId'] = temp_user_id
        session['username'] = temp_username
        session['agreementuserid'] = temp_user_id
        session['RoleID'] = temp_RoleID
        session.permanent = True  # Changed to True to persist session
        session.modified = True  # Ensure session is saved

        # log the agreement
        logger.info(f"User with UserId: {temp_user_id} agrees with Privacy Policy at {current_time}")
        logger.info(f"Session set: userId={session.get('userId')}, RoleID={session.get('RoleID')}, agreementuserid={session.get('agreementuserid')}")

        # Redirect to the dashboard after agreeing to the privacy policy
        return redirect(url_for('jscore.index'))

    except Exception as e:
        logger.error(f"Error during agreement: {str(e)}", exc_info=True)
        # Check if it's a database error
        if 'database' in str(e).lower() or 'sql' in str(e).lower() or 'connection' in str(e).lower():
            user_message = ErrorHandler.format_database_error(e)
        else:
            user_message = "An error occurred while processing your agreement. Please try again."
        flash(user_message, 'danger')
        return redirect(url_for('user.show_login'))


@user_bp.route('/signup', methods=['GET'])
def signup():
    """Sign up page - placeholder for now"""
    return render_template('signup.html')

