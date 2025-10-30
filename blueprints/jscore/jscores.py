import json
import time
import bleach
import random
import logging
import hashlib
import requests 
from config import Config
from sqlalchemy import func
from models.plan_model import Plan
from models.quota_model import Quota
from models.apihit_model import APIHit
from models.user_model import User, db
from datetime import datetime, timedelta
from models.product_model import Product
from models.user_product import UserProducts
from models.changeplan_model import ChangePlan
from blueprints.tasks.tasks import role_required
from models.subscriptiontype_model import SubscriptionType
from ..api_util.api_utils import call_Jscore_api_function, call_JscoreHistory_api_function
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, flash, session, abort

# Create a Blueprint for the JScore-related routes
jscore_bp = Blueprint("jscore", __name__, template_folder="templates/jscore")
logger = logging.getLogger(__name__)


# Will be removed
def request_and_check_consent(msisdn, client_name="HBL"):
    print(f"[Mock] Sending consent request to: {msisdn}")
    time.sleep(10)  # simulate waiting
    consent_status = random.choice([1, 2, 3])
    print(f"[Mock] Consent response: {consent_status}")
    return consent_status



@jscore_bp.route('/test_consent', methods=['GET', 'POST'])
def test_consent():
    consent_result = None
    mobile_number = None

    if request.method == 'POST':
        mobile_number = bleach.clean(request.form.get('mobile_number'))

        if mobile_number.startswith('0'):
            mobile_number = '92' + mobile_number[1:]

        consent_result = request_and_check_consent(mobile_number)

    return render_template(
        'test_consent.html',
        consent_result=consent_result,
        mobile_number=mobile_number,
        page_title='Test Consent Flow'
    )


# Define the main route for JScore, supporting both GET and POST methods
@jscore_bp.route('/', methods=['GET', 'POST'])
@jscore_bp.route('/index', methods=['GET', 'POST'])
@role_required("Jscore")  # 🔥 Role check applied here!
def index():
    try:
        # Check if the user is logged in by verifying the presence of 'userId' in the session
        if 'userId'not in session or 'agreementuserid' not in session:
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
            # Get the current date and extract the month and year
          
           
            current_date = datetime.now()
            current_month = current_date.month
            current_year = current_date.year
            jscore_product = db.session.query(Product).filter_by(name='jscore').first()
            if not jscore_product:
                return "JScore product not found", 404  # Handle case if product is not found
            users = User.query.filter_by(UserId=session['userId']).first()
            # quota = Quota.query.filter_by(UserId=users.UserId).first()
            quota = db.session.query(Quota).filter_by(
                        UserId=users.UserId,
                        ProductId=jscore_product.id,
                        Month=current_month,
                        Year=current_year
                    ).first()
            subscription_type = SubscriptionType.query.filter_by(Id=users.subscription_type_id).first()

            # Check if the user subscription is Prepaid or Postpaid
            if subscription_type.subscriptiontype.lower() == 'prepaid':
                # Check if the user has remaining quota
                if quota.UsedQuota >= quota.MaxQuota:
                    flash('Quota limit reached. You cannot make more requests.')
                    return redirect(url_for('jscore.index', page_title='JScore'))

                
                 # Check if the user is authorized (RoleId == 1)
                if users and users.RoleId == 1: 
                    
                    # Call the external API to retrieve the score and related data
                    api_data, status_code = call_Jscore_api_function(users, mobile_number)

                    print(f" ",status_code, api_data)
                    # If the API call is successful, store relevant data in the session and render the template
                    if status_code == 200:
                        # Log
                        logger.info(f"API call was successful for UserId: {users.UserId}, Username: {users.Username}, for MobileNumber: {mobile_number}")
                        
                        quota.UsedQuota += 1
                        score = api_data.get('JSCORE')
                        if score is not None and score != 0:
                            api_hit = APIHit(
                                user_id=users.UserId,
                                product_id=jscore_product.id,
                                mobile_number=mobile_number,
                                status=True , # Set to True as the score is valid
                                score = score
                            )
                        else:
                            api_hit = APIHit(
                                        user_id=users.UserId,
                                        product_id=jscore_product.id,  # Assuming you have the jscore_product from earlier in your code
                                        mobile_number=mobile_number,
                                        status=False , # Set to True as the API call was successful
                                        score = score
                                    )

                        # Add the APIHit record to the session and commit all changes
                        db.session.add(api_hit)
                        db.session.commit()
                        # Store the mobile number, score, and API data in the session
                        session['mobile_number'] = mobile_number
                        session['api_score'] = api_data.get('JSCORE')

                        session['api_data'] = api_data

                        sim_age = api_data.get('sim_age', 'NA')
                        sim_info = 'PRIMARY NUMBER' if api_data.get('sacendory') == 1 else 'SECONDARY NUMBER'

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
            elif subscription_type.subscriptiontype.lower() == 'postpaid':
                 if users and users.RoleId == 1:
                        api_data, status_code = call_Jscore_api_function(users, mobile_number)
                        if status_code == 200:
                            quota.UsedQuota += 1
                            db.session.commit()
                            session['mobile_number'] = mobile_number
                            session['api_score'] = api_data.get('score')
                            session['api_data'] = api_data

                            sim_age = api_data.get('sim_age', 'NA')
                            sim_info = 'PRIMARY NUMBER' if api_data.get('sacendory') == 1 else 'SECONDARY NUMBER'

                            return render_template(
                                'index1.html', 
                                api_data=api_data, 
                                mobile_number=mobile_number, 
                                sim_age=sim_age, 
                                sim_info=sim_info, 
                                page_title='JScore'
                            )
                        else:
                            flash('An error occurred while calling the API')
                            return redirect(url_for('jscore.index', page_title='JScore'))
        
        # Clear the mobile number in the session if no form is submitted
        session['mobile_number'] = ""
        return render_template('index1.html', page_title='JScore')

    except Exception as e:
        # Handle any unexpected exceptions and render the error page
        print(e)
        return render_template('error.html'), 500


# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------


# Define the route for viewing credit history
@jscore_bp.route('/credithistory', methods=['GET', 'POST'])
def credithistory():
    # Check if the user is logged in by verifying the presence of 'userId' in the session
    if 'userId'not in session or 'agreementuserid' not in session:
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
    sim_info = 'PRIMARY NUMBER' if api_data.get('sacendory') == 1 else 'SECONDARY NUMBER'

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
                                        sim_age = sim_age,
                                        sim_info=sim_info,
                                        chartData=history_api_data,
                                        average_value = average_value,
                                        lowest_value = lowest_value,
                                        highest_value = highest_value,
                                        api_score=api_score,
                                        lowest_month_name = lowest_month_name,
                                        highest_month_name = highest_month_name,
                                        months = months,
                                        mobile_number = mobile_number
                                        )
                else:     
                    flash('Error. Please try again')
                    return redirect(url_for('jscore.index', page_title='JScore'))

    else:
                # Handle unauthorized access
                flash('No access.')
                return redirect(url_for('jscore.index', page_title='JScore'))



@jscore_bp.route('/products')
def products():
    if 'userId'not in session or 'agreementuserid' not in session:
        return redirect(url_for('user.show_login'))
    return render_template('products.html')


@jscore_bp.route('/billingandpayments')
def billingandpayments():
    # Retrieve all plans from the database
    plans = Plan.query.all()

    # Fetch specific plans by name
    basic_plan = Plan.query.filter_by(name="Basic").first()
    professional_plan = Plan.query.filter_by(name="Professional").first()
    enterprise_plan = Plan.query.filter_by(name="Enterprise").first()
    print("Basic Plan id:", basic_plan.id)
    

    return render_template(
        'billingandpayments.html',
        # plans=plans,
        basic_plan_id=basic_plan.id if basic_plan else None,
        professional_plan_id=professional_plan.id if professional_plan else None,
        enterprise_plan_id=enterprise_plan.id if enterprise_plan else None
    )


@jscore_bp.route('/purchase_plan/<int:plan_id>')
def purchase_plan(plan_id):
    if 'userId' not in session or 'agreementuserid' not in session:
        return redirect(url_for('user.show_login'))  # Redirect to login if not logged in
    
    # Retrieve the selected plan details
    plan = Plan.query.get(plan_id)
    if not plan:
        flash("Invalid plan selected!", "danger")
        return redirect(url_for('billingandpayments'))

    return render_template('confirm_purchase.html', plan_id=plan)  # Open confirmation page

@jscore_bp.route('/confirm_change_plan', methods=['POST'])
def confirm_change_plan():
    if 'userId' not in session:
        return redirect(url_for('user.show_login'))  # Redirect if not logged in

    user_id = session['userId']
    user = User.query.get(user_id)

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for('jscore.billingandpayments'))

    plan_id = request.form.get('plan_id')  # Fetch plan ID from the form
    print("plan_id foung from form: ", plan_id)
    

    if not plan_id:
        flash("Invalid request. Please select a plan.", "warning")
        print("plan_id not found")
        return redirect(url_for('jscore.billingandpayments'))

    try:
        plan_id = int(plan_id)  # Convert to integer safely
        plan = Plan.query.get(plan_id)
        print("plan from db", plan)
        
    except ValueError:
        flash("Invalid plan ID format.", "danger")
        return redirect(url_for('jscore.billingandpayments'))

    if not plan:
        flash("Selected plan does not exist.", "danger")
        return redirect(url_for('jscore.billingandpayments'))

    current_month = datetime.now().month

    change_request = ChangePlan(
        userid=user.UserId,
        user_email=user.email,
        planid=plan_id,
        month=current_month,
        date=datetime.now().date(),
        time=datetime.now().time().replace(microsecond=0),
        status="pending"
    )

    print (change_request)
    db.session.add(change_request)
    db.session.commit()

    flash(f"Your request to change the plan to {plan.name} has been submitted for approval.", "success")
    return redirect(url_for('jscore.billingandpayments'))





@jscore_bp.route('/myaccount')
def myaccount():
    if 'userId'not in session or 'agreementuserid' not in session:
        return redirect(url_for('user.show_login'))
    return render_template('myaccount.html')



@jscore_bp.route('/credithithistory')
def credithithistory():
    if 'userId'not in session or 'agreementuserid' not in session:
        return redirect(url_for('user.show_login'))
    
    # Get the current date and extract the month and year
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # Determine last month and year for comparison
    if current_month == 1:  # If it's January
        last_month = 12     # December of the previous year
        last_year = current_year - 1
    else:
        last_month = current_month - 1
        last_year = current_year

 

    # Retrieve the current user's subscription or product data for the jscore product
    user_id = session['userId']

    jscore_product = db.session.query(Product).filter_by(name='jscore').first()
    if not jscore_product:
        return "JScore product not found", 404  # Handle case if product is not found
    
    # Check if the user has this product in their `user_products` table
    user_product = db.session.query(UserProducts).filter_by(
        user_id=user_id,
        product_id=jscore_product.id
    ).first()

    if not user_product:
        return "User does not have access to JScore product", 403  # Handle no access
    
    
    users = User.query.filter_by(UserId=user_id).first()
    subscription_type = SubscriptionType.query.filter_by(id=users.subscription_type_id).first()
        
    # Check if the user subscription is Prepaid
    quota_limit = None
    last_month_quota_limit = None
    percentage_difference = None


            # Check if the user subscription is Prepaid or Postpaid
    if subscription_type.subscriptiontype.lower() == 'prepaid':
        # Fetch the quota limit for the `jscore` product for the current month
        quota = db.session.query(Quota).filter_by(
            UserId=user_id,
            ProductId=jscore_product.id,
            Month=current_month,
            Year=current_year
        ).first()


        # Get the quota limit if it exists, or set to None if not found
        quota_limit = quota.MaxQuota if quota else None

        print (f"limit: {quota_limit}")


        # Fetch the last month's quota limit for the `jscore` product
        last_month_quota = db.session.query(Quota).filter_by(
            UserId=user_id,
            ProductId=jscore_product.id,
            Month= last_month,
            Year=last_year
        ).first()
        
        last_month_quota_limit = last_month_quota.MaxQuota if last_month_quota else None
        last_month_quota_used = last_month_quota.UsedQuota if last_month_quota else None



        # Get MaxQuota and UsedQuota if quota exists
        if quota:
            quota_limit = quota.MaxQuota
            used_quota = quota.UsedQuota if quota.UsedQuota is not None else None
            remaining_quota = quota_limit - used_quota if quota_limit is not None else None


        print (f"last month limit: {last_month_quota_limit}")
        print (f"Remaining: {remaining_quota}")


        # Calculate the percentage difference if both current and last month quotas are available
        if quota_limit is not None and last_month_quota_limit is not None:
            percentage_difference = round(((quota_limit - last_month_quota_limit) / last_month_quota_limit) * 100, 2)
               

        if used_quota is not None and last_month_quota_used is not None:
            last_month_remaining_percentage_difference = round(((used_quota - last_month_quota_used) / last_month_quota_used) * 100, 2)
               
            

            print (f"Percentage: {percentage_difference}")
            print (f"last_month_remaining_percentage_difference: {last_month_remaining_percentage_difference}")


        # Query the unique mobile numbers for the current month
        unique_mobile_numbers = db.session.query(APIHit.mobile_number).filter(
                                APIHit.user_id == user_id,  # Filter by user_id (ensure user_id is provided)
                                func.extract('month', APIHit.timestamp) == current_month,
                                func.extract('year', APIHit.timestamp) == current_year
                            ).distinct().all()

        # Get the count of unique mobile numbers
        unique_mobile_count = len(unique_mobile_numbers)



        # Query the unique mobile numbers for the last month
        last_unique_mobile_numbers = db.session.query(APIHit.mobile_number).filter(
                                APIHit.user_id == user_id,  # Filter by user_id (ensure user_id is provided)
                                func.extract('month', APIHit.timestamp) == last_month,
                                func.extract('year', APIHit.timestamp) == last_month
                            ).distinct().all()
        

        # Get the count of unique mobile numbers
        unique_mobile_count = len(unique_mobile_numbers)
        last_unique_mobile_count = len(last_unique_mobile_numbers)
        difference_unique_numbers = unique_mobile_count - last_unique_mobile_count
        # Calculate the last month's unique mobile number percentage difference
        if last_unique_mobile_count > 0:
            last_month_unique_number_percentage = round(((unique_mobile_count - last_unique_mobile_count) / last_unique_mobile_count) * 100, 2)
        else:
            last_month_unique_number_percentage = 0  # Or any default value you prefer when there's no data


        # Print the result (or return it as needed)
        print(f"Number of unique mobile numbers checked by the user in {current_month}/{current_year}: {unique_mobile_count}")


        # Calculate API hits for the last 7 days, grouped by day
        seven_days_ago = current_date - timedelta(days=7)
        daily_hits = db.session.query(
                        func.date(APIHit.timestamp).label('day'),
                        func.count(APIHit.id).label('hit_count')
                    ).filter(APIHit.timestamp >= seven_days_ago) \
                    .group_by(func.date(APIHit.timestamp)) \
                    .order_by(func.date(APIHit.timestamp)).all()

        # Create a dictionary for daily hit counts
        daily_hits_dict = {hit.day.strftime('%A'): hit.hit_count for hit in daily_hits}

        # If there are any missing days, add them with a count of 0
        for i in range(7):
            date_to_check = (current_date - timedelta(days=i)).strftime('%A')
            if date_to_check not in daily_hits_dict:
                daily_hits_dict[date_to_check] = 0

        # Print all 7 days with their respective hit counts
        print(daily_hits_dict)


        # Fetch the API hits for the current month where status = true
        true_hits = db.session.query(
            func.count(APIHit.id).label('true_hits')
        ).filter(
            APIHit.user_id == user_id,
            func.extract('month', APIHit.timestamp) == current_month,
            func.extract('year', APIHit.timestamp) == current_year,
            APIHit.status == True  # Filter for status = true
        ).scalar()  # Use scalar to directly get the count

        # Fetch the API hits for the current month where status = false
        false_hits = db.session.query(
            func.count(APIHit.id).label('false_hits')
        ).filter(
            APIHit.user_id == user_id,
            func.extract('month', APIHit.timestamp) == current_month,
            func.extract('year', APIHit.timestamp) == current_year,
            APIHit.status == False  # Filter for status = false
        ).scalar()  # Use scalar to directly get the count

        # Print or return the hit counts
        print(f"API hits with status = True: {true_hits}")
        print(f"API hits with status = False: {false_hits}")


        # Return the rendered template with the necessary data
        return render_template(
            'credithithistory.html',
            true_hits = true_hits,
            false_hits = false_hits,
            unique_mobile_count=unique_mobile_count,
            percentage_difference=percentage_difference,
            daily_hits_dict=daily_hits_dict,
            quota_limit=quota_limit,
            last_month_quota_limit=last_month_quota_limit,
            remaining_quota=remaining_quota,
            difference_unique_numbers = difference_unique_numbers,
            last_month_remaining_percentage_difference=last_month_remaining_percentage_difference,
            last_month_unique_number_percentage = last_month_unique_number_percentage
        )




    return render_template('credithithistory.html',
                           unique_mobile_count=0,
            percentage_difference=0,
            daily_hits_dict=0,
            quota_limit=0,
            last_month_quota_limit=0,
            remaining_quota=0,
            last_month_remaining_percentage_difference=0
                           
                           )




@jscore_bp.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
        if 'userId'not in session or 'agreementuserid' not in session:
            return redirect(url_for('user.show_login'))
        
        if request.method == 'POST':
        # Get form data
            users = User.query.filter_by(UserId=session['userId']).first()

            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            # Validate form data
            if not current_password or not new_password or not confirm_password:
                flash('All fields are required!', 'danger')
            elif new_password != confirm_password:
                flash('New password and confirm password do not match!', 'danger')
            else:
                # Example: Check current password (replace this with your logic)
                # user = get_current_user()  # Replace with your user session logic
                user = User.query.filter_by(UserId=session['userId']).first()
                check_pass = 0
                if user.Password ==  hashlib.sha256(current_password.encode()).hexdigest() :
                    check_pass = 1

                # if user and verify_password(current_password, user.password):  # Replace with your password verification
                if user and check_pass == 1:  # Replace with your password verification
                
                    # Update the password (replace with your update logic)
                    user.Password = hashlib.sha256(new_password.encode()).hexdigest()  # Hash the new password 
                    # save_user(user)  # Save the user to the database
                    db.session.commit()
                    flash('Password changed successfully!', 'success')
                    return redirect(url_for('jscore.changepassword'))
                else:
                    flash('Current password is incorrect!', 'danger')

        return render_template('changepassword.html') 


@jscore_bp.route('/contactus', methods=['GET', 'POST'])
def contactus():
     return render_template('contactus.html') 

@jscore_bp.route('/help')
def help_page():
    return render_template('help.html')




# # Define the route for viewing credit history
# @jscore_bp.route('/credithistory', methods=['GET', 'POST'])
# def credithistory():
#     # Check if the user is logged in by verifying the presence of 'userId' in the session
#     if 'userId' not in session:
#         return redirect(url_for('user.show_login'))


#     # Ensure that the necessary data is present in the session
#     # if not session.get('mobile_number') or not session.get('api_score') or not session.get('api_data'):
#     #     flash('Please submit the form to view the credit history.')
#     #     return redirect(url_for('jscore.index'))

#     # Get the current date to be displayed on the page
#     current_date = datetime.now().strftime("%Y-%m-%d")  # Format the date as needed
    
#     # Retrieve the stored mobile number, score, and API data from the session
#     mobile_number = '923034605404'
#     api_data = session.get('api_data')
#     sim_age = '+12 MONTHS'
#     sim_info = 'SECONDARY NUMBER'

#     users = User.query.filter_by(UserId=session['userId']).first()

#     if users and users.RoleId == 1:
#                 # Call the external API to retrieve the score and related data
#                 #history_api_data, status_code = call_JscoreHistory_api_function(users, mobile_number)

#                 # If the API call is successful, store relevant data in the session and render the template
#                     history_api_data = {'month_1': 5,'month_2': 3,'month_3': 7,'month_4': 2,'month_5': 8,'month_6': 7}
#                     #logger.info(f"History API call was successful for UserId: {users.UserId}, Username: {users.Username}, for MobileNumber: {mobile_number}")
#                     month_values = [
#                     int(history_api_data.get(f'month_{i}', 0)) for i in range(1, 7)
#                     ]

#                     current_month = datetime.now().month
#                     months = {}
#                     for i in range(6):
#                         month_key = f"month_{i + 1}"
#                         calculated_month = (current_month - i - 1) % 12 or 12
#                         months[month_key] = calculated_month
#                     # print (months)

#                     # Calculate the average, lowest, and highest values
#                     if month_values:
#                         average_value = round(sum(month_values) / len(month_values), 1)
#                         lowest_value = min(month_values)
#                         highest_value = max(month_values)

#                         # Get the corresponding month names
#                         month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#                         lowest_month_index = month_values.index(lowest_value)
#                         highest_month_index = month_values.index(highest_value)

#                         lowest_month_name = month_names[months[f'month_{lowest_month_index + 1}'] - 1]
#                         highest_month_name = month_names[months[f'month_{highest_month_index + 1}'] - 1]
#                     else:
#                         average_value = lowest_value = highest_value = 0
#                         lowest_month_name = highest_month_name = "N/A"
                    
#                     api_score = 4
                
#                     # Render the credit history template with the retrieved data
#                     return render_template('credithistory.html', 
#                                         page_title='JScore History',  
#                                         sim_age = sim_age,
#                                         sim_info=sim_info,
#                                         chartData=history_api_data,
#                                         average_value = average_value,
#                                         lowest_value = lowest_value,
#                                         highest_value = highest_value,
#                                         api_score=api_score,
#                                         lowest_month_name = lowest_month_name,
#                                         highest_month_name = highest_month_name,
#                                         months = months,
#                                         mobile_number = mobile_number
#                                         )
            