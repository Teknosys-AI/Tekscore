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



user_bp = Blueprint("user", __name__, template_folder="templates/users")
logger = logging.getLogger(__name__)






@user_bp.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')
    

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        with db.engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("✅ Database connection successful during login.")
    except Exception as db_err:
        logger.error(f"❌ Database connection failed during login: {db_err}")
        flash("Database connection error. Please try again later.")
        #return render_template('error.html'), 500
        
        # Prevent browser caching for this route
        response = make_response()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'

        # Check if the user is locked out
        if session.get('login_locked'):
            if time.time() < session['login_locked']:
                flash('Too many login attempts. Please try again in 1 minute.')
                return redirect(url_for('user.show_login'))
            else:
                session.pop('login_locked', None)  # Unlock after timeout

        username = bleach.clean(request.form.get('username'))
        password = bleach.clean(request.form.get('password'))

        # Query to find the user
        user = User.query.filter_by(
            Username=username,
            Password=hashlib.sha256(password.encode()).hexdigest()
        ).first()
        

        if user:
            business_role = Role.query.filter_by(Name="Business").first()
            
            if user.RoleId == business_role.RoleId: 
                    session.clear()  # Clear the temporary session data
                    session['userId'] = user.UserId
                    session['username'] = user.Username
                    session['RoleID'] = user.RoleId
                    return redirect(url_for('businessusers.pending_changes')) 
            # Clear any previous session-related flags
            session.pop('failed_attempts', None)

            # Temporarily store user details until agreement
            session['temp_user_id'] = user.UserId
            session['temp_username'] = user.Username
            session['temp_RoleID'] = user.RoleId
            session.permanent = True
            # print(session['RoleID'])

            # Redirect to privacy policy page for agreement
            return redirect(url_for('user.privacy_policy'))

        else:
            # Handle failed login logic...
            session['failed_attempts'] = session.get('failed_attempts', 0) + 1
            session.modified = True
            if session['failed_attempts'] >= 5:
                session['login_locked'] = time.time() + 60  # Lock for 1 minute
                session.pop('failed_attempts', None)  # Reset failed attempts counter
                flash('Too many login attempts. Please try again in 1 minute.')
                return redirect(url_for('user.show_login'))
            else:
                flash("Login failed. Please try again.")
                return redirect(url_for('user.show_login'))

    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return render_template('error.html'), 500






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
        logger.error(f"Error during logout: {str(e)}")
        return render_template('error.html'), 500



        
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
            flash("Session expired or invalid. Please log in again.")
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
        session.permanent = False

        # log the agreement
        logger.info(f"User with UserId: {temp_user_id} agrees with Privacy Policy at {current_time}")


        # Redirect to the products page after agreeing to the privacy policy
        return redirect(url_for('jscore.index'))

    except Exception as e:
        logger.error(f"Error during agreement: {str(e)}")
        return render_template('error.html'), 500


