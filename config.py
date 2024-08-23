

class Config:
    SECRET_KEY = 'hardsecretkey'
    API_ENDPOINT = 'https://quanticaapi.jazz.com.pk/jscore/Jazz_Score'
    #SqlAlchemy Database Configuration With Mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/jscore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERMANENT_SESSION_LIFETIME = 900  # 900 seconds = 15 minutes