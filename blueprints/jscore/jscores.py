import bleach
import logging
import hashlib
import requests 
from models.user_model import User, db
from config import Config
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, flash, session, abort
from ..api_util.api_utils import call_Jscore_api_function



jscore_bp = Blueprint("jscore", __name__, template_folder="templates/jscore")
logger = logging.getLogger(__name__)


@jscore_bp.route('/', methods=['GET', 'POST'])
def index():
    try:
        print(f"Session in index: {session}")
        if 'userId' not in session:
            # print("redirecting to login by Index")
            return redirect(url_for('user.show_login'))

        if request.method == 'POST':
            mobile_number = bleach.clean(request.form.get('mobile_number'))

            if mobile_number.startswith('0'):
                mobile_number = '92' + mobile_number[1:]

            users = User.query.filter_by(UserId=session['userId']).first()
            if users and users.RoleId == 1:
                api_data, status_code = call_Jscore_api_function(users, mobile_number)

                if status_code == 200:
                    # Successfully received data
                    logger.info(f"API call was successful for UserId: {users.UserId}, Username: {users.Username}, for MobileNumber: {mobile_number}")
                    
                    return render_template('index1.html', api_data=api_data,  mobile_number=mobile_number)
                else:
                    # Handle errors from the API
                    flash(f'Error calling the API: {api_data.get("error", "Unknown error")}')
                    return redirect(url_for('jscore.index'))
            else:
                flash('No access.')
                return redirect(url_for('jscore.index'))

        return render_template('index1.html')

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return render_template('error.html'), 500  # Redirect to your custom error page


