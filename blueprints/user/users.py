import time
import bleach
import logging
import hashlib
from models.user_model import User, db
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, flash, session, abort



user_bp = Blueprint("user", __name__, template_folder="templates/users")
logger = logging.getLogger(__name__)






@user_bp.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        if request.method == 'POST':
            # Check if the user is locked out
            if session.get('login_locked'):
                if time.time() < session['login_locked']:
                    flash('Too many login attempts. Please try again in 1 minute.')
                    return redirect(url_for('user.show_login'))
                else:
                    session.pop('login_locked', None)  # Unlock after timeout

            username = bleach.clean(request.form.get('username'))
            password = bleach.clean(request.form.get('password'))

            users = User.query.filter_by(
                Username=username,
                Password=hashlib.sha256(password.encode()).hexdigest()
            ).first()

            if users:
                session.clear()
                session['userId'] = users.UserId
                session['username'] = users.Username
                session.permanent = False
                return redirect(url_for('jscore.index'))
            else:
                session['failed_attempts'] = session.get('failed_attempts', 0) + 1

                if session['failed_attempts'] >= 5:
                    session['login_locked'] = time.time() + 60  # Lock for 1 minute
                    session.pop('failed_attempts', None)  # Reset failed attempts counter
                    flash('Too many login attempts. Please try again in 1 minute.')
                    return redirect(url_for('user.show_login'))
                else:
                    flash("Login failed. Please try again.")
                    return redirect(url_for('user.show_login'))
        else:
            return render_template('login.html')
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return render_template('error.html'), 500

@user_bp.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('user.show_login'))
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return render_template('error.html'), 500




@user_bp.route('/error')
def error():
    return render_template('error.html'), 500