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
from models.agreement_model import Agreement
from blueprints.tasks.tasks import role_required
from models.subscriptiontype_model import SubscriptionType
from ..api_util.api_utils import call_Jscore_api_function, call_JscoreHistory_api_function
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, flash, session, abort
from utils.error_handler import ErrorHandler

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
            # Check if we have API data from a previous POST (for Post/Redirect/Get pattern)
            show_results = session.get('show_results', False)
            api_data = None
            mobile_number = ''
            sim_age = 'NA'
            sim_info = 'NA'
            
            # Only use session data if show_results flag is set (from recent POST)
            if show_results:
                api_data = session.get('api_data')
                mobile_number = session.get('mobile_number', '')
                sim_age = session.get('sim_age', 'NA')
                sim_info = session.get('sim_info', 'NA')
                
                # Clear the session data after using it to prevent stale data on refresh
                session.pop('show_results', None)
                # Note: We keep api_data, mobile_number, sim_age, sim_info in session
                # in case user wants to see them again, but they'll be overwritten on next POST
            
            # Get user quota information
            user_id = session.get('userId')
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Initialize variables
            subscription_type_name = None
            subscription_description = None
            max_quota = None
            used_quota = None
            remaining_quota = None
            quota_percentage = 0
            
            # Analytics data
            quota_history = []
            api_stats = {
                'total_calls': 0,
                'monthly_calls': 0,
                'success_rate': 0.0,
                'successful_calls': 0,
                'failed_calls': 0,
                'avg_score': 0.0,
                'recent_calls': [],
                'daily_usage': []
            }
            account_activity = {
                'last_agreement_date': None,
                'total_agreements': 0
            }
            
            # Get jscore product
            jscore_product = db.session.query(Product).filter_by(name='jscore').first()
            
            if user_id and jscore_product:
                # Get user's quota for current month
                quota = Quota.query.filter_by(
                    UserId=user_id,
                    ProductId=jscore_product.id,
                    Month=current_month,
                    Year=current_year
                ).first()
                
                if quota:
                    max_quota = quota.MaxQuota
                    used_quota = quota.UsedQuota
                    remaining_quota = quota.MaxQuota - quota.UsedQuota
                    quota_percentage = round((quota.UsedQuota / quota.MaxQuota * 100), 1) if quota.MaxQuota > 0 else 0
                
                # Get quota history (last 6 months)
                six_months_ago = datetime.now() - timedelta(days=180)
                quota_history_records = Quota.query.filter(
                    Quota.UserId == user_id,
                    Quota.ProductId == jscore_product.id
                ).order_by(Quota.Year.desc(), Quota.Month.desc()).limit(6).all()
                
                for q in quota_history_records:
                    quota_history.append({
                        'month': q.Month,
                        'year': q.Year,
                        'max': q.MaxQuota,
                        'used': q.UsedQuota,
                        'percentage': round((q.UsedQuota / q.MaxQuota * 100), 1) if q.MaxQuota > 0 else 0
                    })
                
                # Get user's subscription type
                user = User.query.filter_by(UserId=user_id).first()
                if user and user.subscription_type_id:
                    subscription = SubscriptionType.query.filter_by(Id=user.subscription_type_id).first()
                    if subscription:
                        subscription_type_name = subscription.subscriptiontype
                        subscription_description = subscription.description
                
                # Get API usage statistics
                all_api_hits = APIHit.query.filter_by(
                    user_id=user_id,
                    product_id=jscore_product.id
                ).order_by(APIHit.timestamp.desc()).all()
                
                if all_api_hits:
                    # Total calls
                    api_stats['total_calls'] = len(all_api_hits)
                    
                    # Monthly calls
                    monthly_hits = [h for h in all_api_hits if h.month == current_month and h.timestamp.year == current_year]
                    api_stats['monthly_calls'] = len(monthly_hits)
                    
                    # Success/failure counts
                    successful_hits = [h for h in all_api_hits if h.status == True]
                    failed_hits = [h for h in all_api_hits if h.status == False]
                    api_stats['successful_calls'] = len(successful_hits)
                    api_stats['failed_calls'] = len(failed_hits)
                    
                    # Success rate
                    if api_stats['total_calls'] > 0:
                        api_stats['success_rate'] = round((api_stats['successful_calls'] / api_stats['total_calls']) * 100, 1)
                    
                    # Average score (from successful calls with scores)
                    scores = [h.score for h in successful_hits if h.score is not None]
                    if scores:
                        api_stats['avg_score'] = round(sum(scores) / len(scores), 1)
                    
                    # Recent calls (last 10)
                    recent_hits = all_api_hits[:10]
                    for hit in recent_hits:
                        # Mask mobile number (show only last 4 digits)
                        mobile = str(hit.mobile_number)
                        if len(mobile) > 4:
                            masked_mobile = '****' + mobile[-4:]
                        else:
                            masked_mobile = mobile
                        
                        api_stats['recent_calls'].append({
                            'timestamp': hit.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                            'mobile': masked_mobile,
                            'status': hit.status,
                            'score': hit.score
                        })
                    
                    # Daily usage (last 7 days)
                    seven_days_ago = datetime.now() - timedelta(days=7)
                    daily_hits = {}
                    for hit in all_api_hits:
                        if hit.timestamp >= seven_days_ago:
                            date_key = hit.timestamp.strftime('%Y-%m-%d')
                            daily_hits[date_key] = daily_hits.get(date_key, 0) + 1
                    
                    # Sort by date
                    for date_key in sorted(daily_hits.keys(), reverse=True)[:7]:
                        api_stats['daily_usage'].append({
                            'date': date_key,
                            'calls': daily_hits[date_key]
                        })
                
                # Get account activity
                agreements = Agreement.query.filter_by(UserId=user_id).order_by(Agreement.agreement_time.desc()).all()
                if agreements:
                    account_activity['total_agreements'] = len(agreements)
                    account_activity['last_agreement_date'] = agreements[0].agreement_time.strftime('%Y-%m-%d %H:%M:%S')

            return render_template(
                        'index1.html', 
                        api_data=api_data,  # Include API data if available from session
                        mobile_number=mobile_number,  # Include mobile number if available
                        sim_age=sim_age, 
                        sim_info=sim_info, 
                        page_title='Dashboard',
                        subscription_type_name=subscription_type_name,
                        subscription_description=subscription_description,
                        max_quota=max_quota,
                        used_quota=used_quota,
                        remaining_quota=remaining_quota,
                        quota_percentage=quota_percentage,
                        quota_history=quota_history,
                        api_stats=api_stats,
                        account_activity=account_activity
                        )
        # Handle form submission with POST request
        if request.method == 'POST':
            # Get mobile number from form
            mobile_number_raw = request.form.get('mobile_number', '').strip()
            
            # Validate mobile number using ErrorHandler
            is_valid, validation_error = ErrorHandler.validate_mobile_number(mobile_number_raw)
            if not is_valid:
                flash(validation_error, 'danger')
                return redirect(url_for('jscore.index', page_title='Dashboard'))
            
            # Clean the mobile number input to prevent XSS attacks
            mobile_number = bleach.clean(mobile_number_raw)
            
            # Standardize the mobile number format (convert '0' prefix to '92')
            if mobile_number.startswith('0'):
                mobile_number = '92' + mobile_number[1:]

            # Fetch the current user from the database using the UserId from the session
            # Get the current date and extract the month and year
          
           
            current_date = datetime.now()
            current_month = current_date.month
            current_year = current_date.year
            
            # Get jscore product
            jscore_product = db.session.query(Product).filter_by(name='jscore').first()
            if not jscore_product:
                flash('JScore product is not configured. Please contact support.', 'danger')
                logger.error("JScore product not found in database")
                return redirect(url_for('jscore.index', page_title='JScore'))
            
            # Get user
            users = User.query.filter_by(UserId=session['userId']).first()
            if not users:
                flash('User not found. Please log in again.', 'danger')
                logger.error(f"User not found for UserId: {session['userId']}")
                return redirect(url_for('user.show_login'))
            
            # Get subscription type
            subscription_type = SubscriptionType.query.filter_by(Id=users.subscription_type_id).first()
            if not subscription_type:
                flash('Your account subscription type is not configured. Please contact support.', 'danger')
                logger.error(f"Subscription type not found for user {users.UserId}")
                return redirect(url_for('jscore.index', page_title='JScore'))
            
            # Get quota for current month
            quota = db.session.query(Quota).filter_by(
                        UserId=users.UserId,
                        ProductId=jscore_product.id,
                        Month=current_month,
                        Year=current_year
                    ).first()

            # Check if the user subscription is Prepaid or Postpaid
            if subscription_type.subscriptiontype.lower() == 'prepaid':
                # Check if quota exists for current month
                if not quota:
                    quota_error_msg = ErrorHandler.get_quota_error_message(None, None, None)
                    flash(quota_error_msg, 'warning')
                    logger.warning(f"No quota found for UserId: {users.UserId}, Month: {current_month}, Year: {current_year}")
                    return redirect(url_for('jscore.index', page_title='Dashboard'))
                
                # Check quota percentage for warning
                quota_percentage = round((quota.UsedQuota / quota.MaxQuota * 100), 1) if quota.MaxQuota > 0 else 0
                quota_warning_msg = ErrorHandler.get_quota_error_message(quota, quota.MaxQuota, quota.UsedQuota, quota_percentage)
                if quota_warning_msg and quota.UsedQuota < quota.MaxQuota:
                    # This is a warning (80%+ but not exhausted), show as warning
                    flash(quota_warning_msg, 'warning')
                
                # Check if the user has remaining quota
                if quota.UsedQuota >= quota.MaxQuota:
                    quota_error_msg = ErrorHandler.get_quota_error_message(quota, quota.MaxQuota, quota.UsedQuota, quota_percentage)
                    flash(quota_error_msg, 'warning')
                    return redirect(url_for('jscore.index', page_title='Dashboard'))
                
                # Check if user has valid token before API call
                if not users.Token or not users.Token.strip():
                    token_error_msg = ErrorHandler.get_token_error_message('missing')
                    flash(token_error_msg, 'danger')
                    logger.error(f"User {users.UserId} ({users.Username}) has no token before API call")
                    return redirect(url_for('jscore.index', page_title='Dashboard'))

                
                 # Check if the user is authorized (RoleId == 1 for Jscore users)
                if users and users.RoleId == 1: 
                    
                    # Call the external API to retrieve the score and related data
                    api_data, status_code = call_Jscore_api_function(users, mobile_number)

                    print(f" ",status_code, api_data)
                    # If the API call is successful, store relevant data in the session and render the template
                    if status_code == 200:
                        # Log
                        logger.info(f"API call was successful for UserId: {users.UserId}, Username: {users.Username}, for MobileNumber: {mobile_number}")
                        
                        # Increment quota only after successful API call
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

                        # Add the APIHit record to the session and commit all changes with error handling
                        try:
                            db.session.add(api_hit)
                            db.session.commit()
                        except Exception as db_error:
                            # Rollback on database error
                            db.session.rollback()
                            error_msg = ErrorHandler.format_database_error(db_error)
                            flash(error_msg, 'danger')
                            logger.error(f"Database error while saving API hit for UserId: {users.UserId}, Error: {str(db_error)}", exc_info=True)
                            # Revert quota increment since commit failed
                            quota.UsedQuota -= 1
                            return redirect(url_for('jscore.index', page_title='Dashboard'))
                        # Store the mobile number, score, and API data in the session
                        session['mobile_number'] = mobile_number
                        session['api_score'] = api_data.get('JSCORE')

                        session['api_data'] = api_data

                        sim_age = api_data.get('sim_age', 'NA')
                        sim_info = 'PRIMARY NUMBER' if api_data.get('sacendory') == 1 else 'SECONDARY NUMBER'

                        # Get user quota information for POST response
                        subscription_type_name = None
                        subscription_description = None
                        max_quota = None
                        used_quota = None
                        remaining_quota = None
                        quota_percentage = 0
                        
                        # Initialize analytics
                        quota_history = []
                        api_stats = {
                            'total_calls': 0,
                            'monthly_calls': 0,
                            'success_rate': 0.0,
                            'successful_calls': 0,
                            'failed_calls': 0,
                            'avg_score': 0.0,
                            'recent_calls': [],
                            'daily_usage': []
                        }
                        account_activity = {
                            'last_agreement_date': None,
                            'total_agreements': 0
                        }
                        
                        if quota:
                            max_quota = quota.MaxQuota
                            used_quota = quota.UsedQuota
                            remaining_quota = quota.MaxQuota - quota.UsedQuota
                            quota_percentage = round((quota.UsedQuota / quota.MaxQuota * 100), 1) if quota.MaxQuota > 0 else 0
                        
                        if subscription_type:
                            subscription_type_name = subscription_type.subscriptiontype
                            subscription_description = subscription_type.description
                        
                        # Fetch analytics data (same as GET method)
                        if users.UserId and jscore_product:
                            # Get quota history (last 6 months)
                            quota_history_records = Quota.query.filter(
                                Quota.UserId == users.UserId,
                                Quota.ProductId == jscore_product.id
                            ).order_by(Quota.Year.desc(), Quota.Month.desc()).limit(6).all()
                            
                            for q in quota_history_records:
                                quota_history.append({
                                    'month': q.Month,
                                    'year': q.Year,
                                    'max': q.MaxQuota,
                                    'used': q.UsedQuota,
                                    'percentage': round((q.UsedQuota / q.MaxQuota * 100), 1) if q.MaxQuota > 0 else 0
                                })
                            
                            # Get API usage statistics
                            all_api_hits = APIHit.query.filter_by(
                                user_id=users.UserId,
                                product_id=jscore_product.id
                            ).order_by(APIHit.timestamp.desc()).all()
                            
                            if all_api_hits:
                                # Total calls
                                api_stats['total_calls'] = len(all_api_hits)
                                
                                # Monthly calls
                                monthly_hits = [h for h in all_api_hits if h.month == current_month and h.timestamp.year == current_year]
                                api_stats['monthly_calls'] = len(monthly_hits)
                                
                                # Success/failure counts
                                successful_hits = [h for h in all_api_hits if h.status == True]
                                failed_hits = [h for h in all_api_hits if h.status == False]
                                api_stats['successful_calls'] = len(successful_hits)
                                api_stats['failed_calls'] = len(failed_hits)
                                
                                # Success rate
                                if api_stats['total_calls'] > 0:
                                    api_stats['success_rate'] = round((api_stats['successful_calls'] / api_stats['total_calls']) * 100, 1)
                                
                                # Average score (from successful calls with scores)
                                scores = [h.score for h in successful_hits if h.score is not None]
                                if scores:
                                    api_stats['avg_score'] = round(sum(scores) / len(scores), 1)
                                
                                # Recent calls (last 10)
                                recent_hits = all_api_hits[:10]
                                for hit in recent_hits:
                                    # Mask mobile number (show only last 4 digits)
                                    mobile = str(hit.mobile_number)
                                    if len(mobile) > 4:
                                        masked_mobile = '****' + mobile[-4:]
                                    else:
                                        masked_mobile = mobile
                                    
                                    api_stats['recent_calls'].append({
                                        'timestamp': hit.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                        'mobile': masked_mobile,
                                        'status': hit.status,
                                        'score': hit.score
                                    })
                                
                                # Daily usage (last 7 days)
                                seven_days_ago = datetime.now() - timedelta(days=7)
                                daily_hits = {}
                                for hit in all_api_hits:
                                    if hit.timestamp >= seven_days_ago:
                                        date_key = hit.timestamp.strftime('%Y-%m-%d')
                                        daily_hits[date_key] = daily_hits.get(date_key, 0) + 1
                                
                                # Sort by date
                                for date_key in sorted(daily_hits.keys(), reverse=True)[:7]:
                                    api_stats['daily_usage'].append({
                                        'date': date_key,
                                        'calls': daily_hits[date_key]
                                    })
                            
                            # Get account activity
                            agreements = Agreement.query.filter_by(UserId=users.UserId).order_by(Agreement.agreement_time.desc()).all()
                            if agreements:
                                account_activity['total_agreements'] = len(agreements)
                                account_activity['last_agreement_date'] = agreements[0].agreement_time.strftime('%Y-%m-%d %H:%M:%S')

                        # Store additional data in session for GET request rendering
                        session['sim_age'] = sim_age
                        session['sim_info'] = sim_info
                        session['show_results'] = True  # Flag to indicate we should show results
                        
                        # Redirect to GET request to prevent "Resubmit form" dialog on refresh
                        # This implements the Post/Redirect/Get (PRG) pattern
                        return redirect(url_for('jscore.index', page_title='Dashboard'))
                    else:
                        # Handle API call failure with user-friendly message
                        # Note: Quota was NOT incremented, so no need to revert
                        user_friendly_msg = ErrorHandler.get_api_error_message(api_data, status_code)
                        flash(user_friendly_msg, 'danger')
                        logger.error(f"API call failed for UserId: {users.UserId}, Status: {status_code}, Error: {api_data}")
                        return redirect(url_for('jscore.index', page_title='Dashboard'))
                else:
                    # Handle unauthorized access
                    flash('You do not have permission to access Tekscore features. Please contact your administrator.', 'danger')
                    logger.warning(f"Unauthorized access attempt - UserId: {users.UserId}, RoleId: {users.RoleId}")
                    return redirect(url_for('jscore.index', page_title='Tekscore'))
            elif subscription_type.subscriptiontype.lower() == 'postpaid':
                 # Check if the user is authorized (RoleId == 1 for Jscore users)
                 if users and users.RoleId == 1:
                        # Check if user has valid token before API call
                        if not users.Token or not users.Token.strip():
                            token_error_msg = ErrorHandler.get_token_error_message('missing')
                            flash(token_error_msg, 'danger')
                            logger.error(f"User {users.UserId} ({users.Username}) has no token before API call")
                            return redirect(url_for('jscore.index', page_title='Dashboard'))
                        
                        api_data, status_code = call_Jscore_api_function(users, mobile_number)
                        if status_code == 200:
                            # Update quota if it exists (for tracking purposes, postpaid users may not have quota)
                            score = api_data.get('JSCORE') or api_data.get('score')
                            
                            # Create APIHit record for postpaid users too
                            if score is not None and score != 0:
                                api_hit = APIHit(
                                    user_id=users.UserId,
                                    product_id=jscore_product.id,
                                    mobile_number=mobile_number,
                                    status=True,
                                    score=score
                                )
                            else:
                                api_hit = APIHit(
                                    user_id=users.UserId,
                                    product_id=jscore_product.id,
                                    mobile_number=mobile_number,
                                    status=False,
                                    score=score
                                )
                            
                            # Update quota and commit with error handling
                            try:
                                if quota:
                                    quota.UsedQuota += 1
                                db.session.add(api_hit)
                                db.session.commit()
                            except Exception as db_error:
                                # Rollback on database error
                                db.session.rollback()
                                error_msg = ErrorHandler.format_database_error(db_error)
                                flash(error_msg, 'danger')
                                logger.error(f"Database error while saving API hit for postpaid UserId: {users.UserId}, Error: {str(db_error)}", exc_info=True)
                                # Revert quota increment if it was incremented
                                if quota:
                                    quota.UsedQuota -= 1
                                return redirect(url_for('jscore.index', page_title='Dashboard'))
                            
                            session['mobile_number'] = mobile_number
                            session['api_score'] = api_data.get('JSCORE') or api_data.get('score')
                            session['api_data'] = api_data

                            sim_age = api_data.get('sim_age', 'NA')
                            sim_info = 'PRIMARY NUMBER' if api_data.get('sacendory') == 1 else 'SECONDARY NUMBER'

                            # Get user quota information for POST response
                            subscription_type_name = None
                            subscription_description = None
                            max_quota = None
                            used_quota = None
                            remaining_quota = None
                            quota_percentage = 0
                            
                            # Initialize analytics
                            quota_history = []
                            api_stats = {
                                'total_calls': 0,
                                'monthly_calls': 0,
                                'success_rate': 0.0,
                                'successful_calls': 0,
                                'failed_calls': 0,
                                'avg_score': 0.0,
                                'recent_calls': [],
                                'daily_usage': []
                            }
                            account_activity = {
                                'last_agreement_date': None,
                                'total_agreements': 0
                            }
                            
                            if quota:
                                max_quota = quota.MaxQuota
                                used_quota = quota.UsedQuota
                                remaining_quota = quota.MaxQuota - quota.UsedQuota
                                quota_percentage = round((quota.UsedQuota / quota.MaxQuota * 100), 1) if quota.MaxQuota > 0 else 0
                            
                            if subscription_type:
                                subscription_type_name = subscription_type.subscriptiontype
                                subscription_description = subscription_type.description
                            
                            # Fetch analytics data (same as GET method)
                            if users.UserId and jscore_product:
                                # Get quota history (last 6 months)
                                quota_history_records = Quota.query.filter(
                                    Quota.UserId == users.UserId,
                                    Quota.ProductId == jscore_product.id
                                ).order_by(Quota.Year.desc(), Quota.Month.desc()).limit(6).all()
                                
                                for q in quota_history_records:
                                    quota_history.append({
                                        'month': q.Month,
                                        'year': q.Year,
                                        'max': q.MaxQuota,
                                        'used': q.UsedQuota,
                                        'percentage': round((q.UsedQuota / q.MaxQuota * 100), 1) if q.MaxQuota > 0 else 0
                                    })
                                
                                # Get API usage statistics
                                all_api_hits = APIHit.query.filter_by(
                                    user_id=users.UserId,
                                    product_id=jscore_product.id
                                ).order_by(APIHit.timestamp.desc()).all()
                                
                                if all_api_hits:
                                    # Total calls
                                    api_stats['total_calls'] = len(all_api_hits)
                                    
                                    # Monthly calls
                                    monthly_hits = [h for h in all_api_hits if h.month == current_month and h.timestamp.year == current_year]
                                    api_stats['monthly_calls'] = len(monthly_hits)
                                    
                                    # Success/failure counts
                                    successful_hits = [h for h in all_api_hits if h.status == True]
                                    failed_hits = [h for h in all_api_hits if h.status == False]
                                    api_stats['successful_calls'] = len(successful_hits)
                                    api_stats['failed_calls'] = len(failed_hits)
                                    
                                    # Success rate
                                    if api_stats['total_calls'] > 0:
                                        api_stats['success_rate'] = round((api_stats['successful_calls'] / api_stats['total_calls']) * 100, 1)
                                    
                                    # Average score (from successful calls with scores)
                                    scores = [h.score for h in successful_hits if h.score is not None]
                                    if scores:
                                        api_stats['avg_score'] = round(sum(scores) / len(scores), 1)
                                    
                                    # Recent calls (last 10)
                                    recent_hits = all_api_hits[:10]
                                    for hit in recent_hits:
                                        # Mask mobile number (show only last 4 digits)
                                        mobile = str(hit.mobile_number)
                                        if len(mobile) > 4:
                                            masked_mobile = '****' + mobile[-4:]
                                        else:
                                            masked_mobile = mobile
                                        
                                        api_stats['recent_calls'].append({
                                            'timestamp': hit.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                            'mobile': masked_mobile,
                                            'status': hit.status,
                                            'score': hit.score
                                        })
                                    
                                    # Daily usage (last 7 days)
                                    seven_days_ago = datetime.now() - timedelta(days=7)
                                    daily_hits = {}
                                    for hit in all_api_hits:
                                        if hit.timestamp >= seven_days_ago:
                                            date_key = hit.timestamp.strftime('%Y-%m-%d')
                                            daily_hits[date_key] = daily_hits.get(date_key, 0) + 1
                                    
                                    # Sort by date
                                    for date_key in sorted(daily_hits.keys(), reverse=True)[:7]:
                                        api_stats['daily_usage'].append({
                                            'date': date_key,
                                            'calls': daily_hits[date_key]
                                        })
                                
                                # Get account activity
                                agreements = Agreement.query.filter_by(UserId=users.UserId).order_by(Agreement.agreement_time.desc()).all()
                                if agreements:
                                    account_activity['total_agreements'] = len(agreements)
                                    account_activity['last_agreement_date'] = agreements[0].agreement_time.strftime('%Y-%m-%d %H:%M:%S')

                            # Store additional data in session for GET request rendering
                            session['sim_age'] = sim_age
                            session['sim_info'] = sim_info
                            session['show_results'] = True  # Flag to indicate we should show results
                            
                            # Redirect to GET request to prevent "Resubmit form" dialog on refresh
                            # This implements the Post/Redirect/Get (PRG) pattern
                            return redirect(url_for('jscore.index', page_title='Dashboard'))
                        else:
                            # Handle API call failure with user-friendly message
                            # Note: Quota was NOT incremented, so no need to revert
                            user_friendly_msg = ErrorHandler.get_api_error_message(api_data, status_code)
                            flash(user_friendly_msg, 'danger')
                            logger.error(f"API call failed for postpaid UserId: {users.UserId}, Status: {status_code}, Error: {api_data}")
                            return redirect(url_for('jscore.index', page_title='Dashboard'))
                 else:
                     flash('You do not have permission to access Tekscore features. Please contact your administrator.', 'danger')
                     logger.warning(f"Unauthorized access attempt - UserId: {users.UserId}, RoleId: {users.RoleId}")
                     return redirect(url_for('jscore.index', page_title='Dashboard'))
            else:
                # Unknown subscription type
                flash(f'Your subscription type ({subscription_type.subscriptiontype}) is not supported. Please contact support.', 'danger')
                logger.error(f"Unsupported subscription type: {subscription_type.subscriptiontype} for UserId: {users.UserId}")
                return redirect(url_for('jscore.index', page_title='JScore'))
        
        # Clear the mobile number in the session if no form is submitted
        session['mobile_number'] = ""
        return render_template('index1.html', page_title='JScore')

    except AttributeError as attr_err:
        # Handle attribute errors (e.g., accessing None object attributes)
        logger.error(f"AttributeError in index: {str(attr_err)}", exc_info=True)
        flash('A data error occurred. Please refresh the page and try again. If the problem persists, contact support.', 'danger')
        return redirect(url_for('jscore.index', page_title='JScore'))
    except Exception as e:
        # Handle any unexpected exceptions
        logger.error(f"Unexpected error in index: {str(e)}", exc_info=True)
        # Check if it's a database error
        if 'database' in str(e).lower() or 'sql' in str(e).lower() or 'connection' in str(e).lower():
            user_message = ErrorHandler.format_database_error(e)
        elif 'network' in str(e).lower() or 'timeout' in str(e).lower():
            user_message = ErrorHandler.format_network_error(e)
        else:
            user_message = "An unexpected error occurred. Please try again later. If the problem persists, contact support."
        flash(user_message, 'danger')
        return redirect(url_for('jscore.index', page_title='JScore'))


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
    
    if not users:
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('user.show_login'))

    # Check if user has Jscore role (RoleId == 1)
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
                                        page_title='Tekscore History',  
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
                    error_msg = history_api_data.get('message', history_api_data.get('error', 'An error occurred while calling the API'))
                    flash(f'API Error: {error_msg}', 'danger')
                    logger.error(f"History API call failed for UserId: {users.UserId}, Status: {status_code}")
                    return redirect(url_for('jscore.index', page_title='Tekscore'))

    else:
        # Handle unauthorized access
        flash('You do not have permission to view credit history. Please contact your administrator.', 'danger')
        logger.warning(f"Unauthorized access to credithistory - UserId: {users.UserId}, RoleId: {users.RoleId}")
        return redirect(url_for('jscore.index', page_title='Tekscore'))



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
    return render_template('myaccount.html', page_title='My Account')


@jscore_bp.route('/help_page')
def show_help_page():
    if 'userId'not in session or 'agreementuserid' not in session:
        return redirect(url_for('user.show_login'))
    return render_template('help.html', page_title='Help')


@jscore_bp.route('/settings')
def settings():
    if 'userId'not in session or 'agreementuserid' not in session:
        return redirect(url_for('user.show_login'))
    return render_template('settings.html', page_title='Settings')


@jscore_bp.route('/activity_log')
def activity_log():
    if 'userId'not in session or 'agreementuserid' not in session:
        return redirect(url_for('user.show_login'))
    return render_template('activity_log.html', page_title='Activity Log')



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
            