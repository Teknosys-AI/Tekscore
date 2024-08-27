import logging
from datetime import timedelta, datetime
from config import Config
from models.user_model import db
from blueprints.user.users import user_bp
from blueprints.jscore.jscores import jscore_bp
from flask import Flask, render_template, request, redirect, url_for, flash, session


#create the object of Flask
app  = Flask(__name__)


# Configure logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='app.log', level=logging.DEBUG, format=log_format)

# Create a logger instance for your application
logger = logging.getLogger(__name__)

app.config.from_object(Config)



@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=900)


@app.before_request
def update_last_activity():
    now = datetime.now()  # This creates a naive datetime object
    last_activity = session.get('last_activity')

    if last_activity:
        # Convert session 'last_activity' to naive datetime (remove timezone info)
        last_activity_naive = last_activity.replace(tzinfo=None)
        elapsed_time = (now - last_activity_naive).total_seconds()

        if elapsed_time > 900:  # 15 minutes in seconds
            session.pop('userId', None)  # Log out the user by removing their session data
            flash('Session timed out due to inactivity.')
            return redirect(url_for('user.show_login'))

    session['last_activity'] = now


@app.before_request
def check_session_timeout():
    last_activity = session.get('last_activity')
    now = datetime.now()

    if last_activity:
        elapsed_time = (now - last_activity).total_seconds()
        if elapsed_time > 900:  # 15 minutes in seconds
            session.pop('userId', None)  # Log out the user by removing their session data
            flash('Session timed out due to inactivity.')
            return redirect(url_for('user.show_login'))

    session['last_activity'] = now

app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    return response

    
app.register_blueprint(user_bp) 
app.register_blueprint(jscore_bp) 


db.init_app(app)

#run flask app
if __name__ == "__main__":
    app.run(debug=True)