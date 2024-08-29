import bleach
import logging
import hashlib
import requests 
from config import Config
from datetime import datetime
from models.user_model import User, db
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, flash, session, abort
from ..api_util.api_utils import call_Jscore_api_function



jscore_bp = Blueprint("jscore", __name__, template_folder="templates/jscore")
logger = logging.getLogger(__name__)


@jscore_bp.route('/', methods=['GET', 'POST'])
@jscore_bp.route('/index', methods=['GET', 'POST'])
def index():
    try:
        if 'userId' not in session:
            return redirect(url_for('user.show_login'))

        # Check if the form is being resubmitted with a stored mobile number
        

        if request.method == 'POST':
            mobile_number = bleach.clean(request.form.get('mobile_number'))

            if mobile_number.startswith('0'):
                mobile_number = '92' + mobile_number[1:]

            if (mobile_number.startswith('0') and len(mobile_number) != 11) or (mobile_number.startswith('92') and len(mobile_number) != 12):
                flash('Invalid mobile number length. It must be 11 characters long if starting with 0, or 12 characters long if starting with 92.')
                return redirect(url_for('jscore.index', page_title='JScore'))

            users = User.query.filter_by(UserId=session['userId']).first()
            if users and users.RoleId == 1:
                api_data, status_code = call_Jscore_api_function(users, mobile_number)

                if status_code == 200:
                    logger.info(f"API call was successful for UserId: {users.UserId}, Username: {users.Username}, for MobileNumber: {mobile_number}")
                    
                    session['mobile_number'] = mobile_number
                    session['api_score'] = api_data.get('score')
                    session['api_data'] = api_data

                    return render_template('index1.html', api_data=api_data, mobile_number=mobile_number, page_title='JScore')
                else:
                    flash('An Error occures while calling the API')
                    return redirect(url_for('jscore.index', page_title='JScore'))
            else:
                flash('No access.')
                return redirect(url_for('jscore.index', page_title='JScore'))

        return render_template('index1.html', page_title='JScore')

    except Exception as e:
        return render_template('error.html'), 500




@jscore_bp.route('/credithistory', methods=['GET', 'POST'])
def credithistory():
    if 'userId' not in session:
        # print("redirecting to login by Index")
        return redirect(url_for('user.show_login'))

    if not session.get('mobile_number') or not session.get('api_score') or not session.get('api_data'):
        flash('Please submit the form to view the credit history.')
        return redirect(url_for('jscore.index'))

    current_date = datetime.now().strftime("%Y-%m-%d")  # Format the date as needed
    
    # Retrieve data from the session
    mobile_number = session.get('mobile_number')
    api_score = session.get('api_score')
    api_data = session.get('api_data')
    # session['auto_resubmit'] = True

    return render_template('credithistory.html', 
                           page_title='JScore History', 
                           current_date=current_date, 
                           mobile_number=mobile_number, 
                           api_score=api_score, 
                           api_data=api_data)
