import logging
from config import Config
from models.user_model import db
from datetime import timedelta, datetime
from blueprints.user.users import user_bp
from blueprints.businessusers.businessusers import businessusers_bp
from flask_apscheduler import APScheduler
from blueprints.jscore.jscores import jscore_bp
from blueprints.landing.landing import landing_bp
from tasks.backgroungtasks import reset_quota
from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.error_handler import ErrorHandler

import pymysql
pymysql.install_as_MySQLdb()



#create the object of Flask
app  = Flask(__name__)
scheduler = APScheduler()


# Configure logging - Output to both file and console
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# File handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))

# Console handler (for terminal output)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(log_format))

# Root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Create a logger instance for your application
logger = logging.getLogger(__name__)

app.config.from_object(Config)

_missing = [
    k
    for k in ("SECRET_KEY", "API_ENDPOINT", "HISTORYAPI_ENDPOINT", "SQLALCHEMY_DATABASE_URI")
    if not app.config.get(k)
]
if _missing:
    raise RuntimeError(
        f"Missing required configuration: {', '.join(_missing)}. "
        "Create a .env file next to config.py (see .env.example)."
    )

# Log database configuration on startup
logger.info("="*70)
logger.info("APPLICATION STARTUP")
logger.info("="*70)
logger.info(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')}")
logger.info("="*70)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.after_request
def remove_headers(response):
    response.headers.pop('X-Powered-By', None)  # Remove X-Powered-By header
    response.headers.pop('Server', None)         # Remove Server header
    return response

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=900)


@app.before_request
def check_session_timeout():
    """Check and handle session timeout"""
    last_activity = session.get('last_activity')
    now = datetime.now()

    if last_activity:
        # Handle both naive and timezone-aware datetimes
        if hasattr(last_activity, 'replace'):
            last_activity_naive = last_activity.replace(tzinfo=None) if last_activity.tzinfo else last_activity
        else:
            last_activity_naive = last_activity
        
        elapsed_time = (now - last_activity_naive).total_seconds() if isinstance(last_activity_naive, datetime) else (now - last_activity).total_seconds()
        
        if elapsed_time > 900:  # 15 minutes in seconds
            session.pop('userId', None)  # Log out the user by removing their session data
            flash('Your session has expired due to inactivity. Please log in again to continue.', 'warning')
            return redirect(url_for('user.show_login'))

    session['last_activity'] = now

# app.after_request
# def add_security_headers(response):
#     response.headers['X-Frame-Options'] = 'DENY'
#     return response

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors with user-friendly message"""
    # Don't show 404 errors for static files (CSS, JS, images, etc.)
    if request.path.startswith('/static/'):
        logger.debug(f"404 Error for static file: {request.url}")
        return "Not Found", 404
    
    # Don't show 404 errors for favicon requests
    if request.path.startswith('/favicon'):
        logger.debug(f"404 Error for favicon: {request.url}")
        return "Not Found", 404
    
    logger.warning(f"404 Error: {request.url} - {str(e)}")
    
    # Only show message if not already on an error page or login page
    if not request.path.startswith('/login') and not request.path.startswith('/error'):
        flash('The page you are looking for could not be found. You have been redirected to the home page.', 'warning')
        return redirect(url_for('landing.index'))
    
    # If already on login page, just return 404 without redirect
    return "Page not found", 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors with user-friendly message"""
    logger.error(f"500 Internal Server Error: {str(e)}", exc_info=True)
    # Try to render 500 page, fallback to redirect with message
    try:
        return render_template('users/500.html'), 500
    except:
        flash('An internal server error occurred. Please try again later. If the problem persists, contact support.', 'danger')
        return redirect(url_for('landing.index'))


@app.errorhandler(403)
def forbidden(e):
    """Handle 403 errors with user-friendly message"""
    logger.warning(f"403 Forbidden Error: {request.url} - {str(e)}")
    flash('You do not have permission to access this page. Please contact your administrator if you believe this is an error.', 'danger')
    # If user is logged in, redirect to their dashboard, otherwise to login
    if 'userId' in session:
        return redirect(url_for('jscore.index'))
    return redirect(url_for('user.show_login'))
    
app.register_blueprint(landing_bp)  # Landing page (initial page)
app.register_blueprint(user_bp) 
app.register_blueprint(jscore_bp) 
app.register_blueprint(businessusers_bp) 



db.init_app(app)

# Test database connection on startup
from sqlalchemy import text
try:
    with app.app_context():
        logger.info("Testing database connection on startup...")
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("[OK] Database connection successful on startup!")
        logger.info(f"Database URL: {db.engine.url}")
except Exception as e:
    logger.error("="*70)
    logger.error("[ERROR] DATABASE CONNECTION FAILED ON STARTUP")
    logger.error("="*70)
    logger.error(f"Error Type: {type(e).__name__}")
    logger.error(f"Error Message: {str(e)}")
    import traceback
    logger.error(f"Full Traceback:\n{traceback.format_exc()}")
    logger.error("="*70)

scheduler.init_app(app)

# Schedule the reset_quota job to run daily at 23:59:59
scheduler.add_job(id='reset_quota_job', func=reset_quota, trigger='cron', hour=23, minute=59, second=59)


#run flask app
if __name__ == "__main__":
    scheduler.start()
    app.run(port=5000, debug=False)
