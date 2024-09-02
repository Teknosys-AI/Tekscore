import time
import bleach
import logging
import hashlib
from markupsafe import escape
from models.user_model import User, db
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
            # Check if the user has an existing session
            session.pop('failed_attempts', None)
            existing_session = UserSession.query.filter_by(SessionUserId=user.UserId).first()

            if existing_session:
                # Log out the user from the previous session
                # print(existing_session.SessionUserId)
                UserSession.query.filter_by(SessionUserId=user.UserId).delete()
                db.session.commit()
                # print(existing_session.SessionUserId)
                session.clear()



            # Clear the current session and log in the user
            session.clear()
            session['userId'] = user.UserId
            session['username'] = user.Username
            session.permanent = False
            session['needs_agreement'] = True
            # print(f"session created  {session['userId']}")

            # Create a new session entry in the database
            session_id = str(time.time())  # Generate a unique session ID (you can use any other method)
            user_session = UserSession(
                SessionUserId=user.UserId,
                SessionId=session_id
            )
            db.session.add(user_session)
            db.session.commit()
            # print(f"DB session created {user_session.SessionUserId}")

            # Store the session ID in Flask session
            session['session_id'] = session_id
            # print("redirecting to index")
            return redirect(url_for('jscore.index'))
        else:
            session['failed_attempts'] = session.get('failed_attempts', 0) + 1
            session.modified = True
            # print ("failed attempt ")
            # print (session['failed_attempts'])

            if session['failed_attempts'] >= 5:
                session['login_locked'] = time.time() + 60  # Lock for 1 minute
                session.pop('failed_attempts', None)  # Reset failed attempts counter
                flash('Too many login attempts. Please try again in 1 minute.')
                return redirect(url_for('user.show_login'))
            else:
                flash("Login failed. Please try again.")
                return redirect(url_for('user.show_login'))
    except Exception as e:
        print (e)
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



@user_bp.route('/agreement', methods=['GET', 'POST'])
def agreement():
    if 'userId' not in session or not session.get('needs_agreement'):
        return redirect(url_for('user.show_login'))

    if request.method == 'POST':
        session.pop('needs_agreement', None)
        return redirect(url_for('jscore.index'))

    return render_template('agreement.html')
