import re

class Config:
    SECRET_KEY = 'hardsecretkey'
    API_ENDPOINT = 'https://quanticaapi.jazz.com.pk/jscore/Jazz_Score'
    #SqlAlchemy Database Configuration With Mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/jscore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERMANENT_SESSION_LIFETIME = 900  # 900 seconds = 15 minutes

    # In your Flask app configuration
    # SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access
    # SESSION_COOKIE_SAMESITE = 'Lax'  # Controls whether cookies are sent with cross-site requests
    # SESSION_COOKIE_SECURE = True  # Cookies only sent over HTTPS
    WHITELIST_PATTERN = re.compile(r'^[a-zA-Z0-9@._-]+$')

    # SESSION_COOKIE_DOMAIN = 'jscores.com'  # Replace with your actual domain
    # SESSION_COOKIE_PATH = '/login'   # Replace with the path you want to restrict to
    
    # # Additional security configurations
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to the cookie
    SESSION_COOKIE_SECURE = True

        