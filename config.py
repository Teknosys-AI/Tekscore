import re

class Config:
    SECRET_KEY = 'hardsecretkey'
    API_ENDPOINT = 'https://tsfapi.teknosys.ai/fusionapi/1.0/fusionapi/JScore'
    # HISTORYAPI_ENDPOINT = 'https://quanticaapi.jazz.com.pk/jscore/Jazz_Score_history'
    # CVM_ASK_USER_CONCENT = 'http://10.50.143.61:7044/event/J-score_request_consent'
    # CVM_GET_USER_CONCENT = ' http://10.50.18.78:7046/get_latest_consent'
    #SqlAlchemy Database Configuration With Mysql
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/jscore'

    SQLALCHEMY_DATABASE_URI = 'mysql://jscore_user:CreditScore%40123@192.168.209.38:3306/jscore'

    # SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/jscore'
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

        