from . import db 

class User(db.Model):
    __tablename__ = 'User'
    UserId = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(255), unique = True)
    Username = db.Column(db.String(100), unique = True)
    Password = db.Column(db.String(1000))
    Token = db.Column(db.String(100000), unique = True)
    RoleId = db.Column(db.Integer, db.ForeignKey('Role.RoleId'))
    subscription_type_id  = db.Column(db.Integer, db.ForeignKey('subscriptiontype.Id'))
    

 
 
    def __init__(self, username, password, token,name,roleId, quotaid , subscriptiontype, email):
        self.Username = username
        self.Password = password
        self.Name = name
        self.Token = token
        self.RoleId = roleId
        self.QuotaId = quotaid
        self.subscriptiontype = subscriptiontype
        self.email = email



    def to_dict(self):
            return {
                'UserId': self.UserId,
                'Name': self.Name,
                'Username': self.Username,
                'Token': self.Token,
                'Password' : self.Password
            }