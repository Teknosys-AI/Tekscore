import bleach
import logging
import hashlib
import requests 
from config import Config
from datetime import datetime
from models.user_model import User, db
from ..api_util.api_utils import call_Jscore_api_function, call_JscoreHistory_api_function
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, flash, session, abort

# Create a Blueprint for the JScore-related routes
jscore_bp = Blueprint("jscore", __name__, template_folder="templates/jscore")
logger = logging.getLogger(__name__)

# Define the main route for JScore, supporting both GET and POST methods
@jscore_bp.route('/', methods=['GET', 'POST'])
@jscore_bp.route('/index', methods=['GET', 'POST'])
def index():
    try:
        # Check if the user is logged in by verifying the presence of 'userId' in the session
        if 'userId' not in session:
            return redirect(url_for('user.show_login'))
        if request.method == 'GET':
            sim_age = 'NA'
            sim_info = 'NA'

            return render_template(
                        'index1.html', 
                        sim_age=sim_age, 
                        sim_info=sim_info, 
                        page_title='JScore'
                        )
        # Handle form submission with POST request
        if request.method == 'POST':
            # Clean the mobile number input to prevent XSS attacks
            mobile_number = bleach.clean(request.form.get('mobile_number'))

            # Standardize the mobile number format (convert '0' prefix to '92')
            if mobile_number.startswith('0'):
                mobile_number = '92' + mobile_number[1:]

            # Validate the length of the mobile number based on its prefix
            if (mobile_number.startswith('0') and len(mobile_number) != 11) or (mobile_number.startswith('92') and len(mobile_number) != 12):
                flash('Invalid mobile number length. It must be 11 characters long if starting with 0, or 12 characters long if starting with 92.')
                return redirect(url_for('jscore.index', page_title='JScore'))

            # Fetch the current user from the database using the UserId from the session
            users = User.query.filter_by(UserId=session['userId']).first()

            # Check if the user is authorized (RoleId == 1)
            if users and users.RoleId == 1:
                # Call the external API to retrieve the score and related data
                api_data, status_code = call_Jscore_api_function(users, mobile_number)

                # If the API call is successful, store relevant data in the session and render the template
                if status_code == 200:
                    logger.info(f"API call was successful for UserId: {users.UserId}, Username: {users.Username}, for MobileNumber: {mobile_number}")
                    
                    # Store the mobile number, score, and API data in the session
                    session['mobile_number'] = mobile_number
                    session['api_score'] = api_data.get('score')
                    session['api_data'] = api_data

                    sim_age = api_data.get('sim_age', 'NA')
                    sim_info = 'PRIMARY' if api_data.get('sacendory') == 1 else 'SECONDARY'

                    # Render the template with the obtained data
                    return render_template(
                        'index1.html', 
                        api_data=api_data, 
                        mobile_number=mobile_number, 
                        sim_age=sim_age, 
                        sim_info=sim_info, 
                        page_title='JScore'
                        )
                else:
                    # Handle API call failure
                    flash('An Error occurred while calling the API')
                    return redirect(url_for('jscore.index', page_title='JScore'))
            else:
                # Handle unauthorized access
                flash('No access.')
                return redirect(url_for('jscore.index', page_title='JScore'))
        
        # Clear the mobile number in the session if no form is submitted
        session['mobile_number'] = ""
        return render_template('index1.html', page_title='JScore')

    except Exception as e:
        # Handle any unexpected exceptions and render the error page
        return render_template('error.html'), 500


# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------


# Define the route for viewing credit history
@jscore_bp.route('/credithistory', methods=['GET', 'POST'])
def credithistory():
    # Check if the user is logged in by verifying the presence of 'userId' in the session
    if 'userId' not in session:
        return redirect(url_for('user.show_login'))


    # Ensure that the necessary data is present in the session
    if not session.get('mobile_number') or not session.get('api_score') or not session.get('api_data'):
        flash('Please submit the form to view the credit history.')
        return redirect(url_for('jscore.index'))

    # Get the current date to be displayed on the page
    current_date = datetime.now().strftime("%Y-%m-%d")  # Format the date as needed
    
    # Retrieve the stored mobile number, score, and API data from the session
    mobile_number = session.get('mobile_number')
    api_data = session.get('api_data')
    sim_age = api_data.get('sim_age')
    sim_info = 'PRIMARY' if api_data.get('sacendory') == 1 else 'SECONDARY'

    users = User.query.filter_by(UserId=session['userId']).first()

    if users and users.RoleId == 1:
                # Call the external API to retrieve the score and related data
                history_api_data, status_code = call_JscoreHistory_api_function(users, mobile_number)

                # If the API call is successful, store relevant data in the session and render the template
                if status_code == 200:
                    logger.info(f"History API call was successful for UserId: {users.UserId}, Username: {users.Username}, for MobileNumber: {mobile_number}")
                    month_values = [
                    int(history_api_data.get(f'month_{i}', 0)) for i in range(1, 7)
                    ]

                    current_month = datetime.now().month
                    months = {}
                    for i in range(6):
                        month_key = f"month_{i + 1}"
                        calculated_month = (current_month - i - 1) % 12 or 12
                        months[month_key] = calculated_month
                    # print (months)

                    # Calculate the average, lowest, and highest values
                    if month_values:
                        average_value = round(sum(month_values) / len(month_values), 1)
                        lowest_value = min(month_values)
                        highest_value = max(month_values)

                        # Get the corresponding month names
                        month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                        lowest_month_index = month_values.index(lowest_value)
                        highest_month_index = month_values.index(highest_value)

                        lowest_month_name = month_names[months[f'month_{lowest_month_index + 1}'] - 1]
                        highest_month_name = month_names[months[f'month_{highest_month_index + 1}'] - 1]
                    else:
                        average_value = lowest_value = highest_value = 0
                        lowest_month_name = highest_month_name = "N/A"
                    
                    api_score = session.get('api_score')
                
                    # Render the credit history template with the retrieved data
                    return render_template('credithistory.html', 
                                        page_title='JScore History', 
                                        mobile_number=mobile_number,  
                                        sim_age = sim_age,
                                        sim_info=sim_info,
                                        chartData=history_api_data,
                                        average_value = average_value,
                                        lowest_value = lowest_value,
                                        highest_value = highest_value,
                                        api_score=api_score,
                                        lowest_month_name = lowest_month_name,
                                        highest_month_name = highest_month_name,
                                        months = months
                                        )
                else:     
                    flash('Error. Please try again')
                    return redirect(url_for('jscore.index', page_title='JScore'))

    else:
                # Handle unauthorized access
                flash('No access.')
                return redirect(url_for('jscore.index', page_title='JScore'))



@jscore_bp.route('/products', methods=['GET', 'POST'])
def products():
    if 'userId' not in session:
        return redirect(url_for('user.show_login'))
    return render_template('products.html')