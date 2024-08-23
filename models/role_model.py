from . import db
class Role(db.Model):
    __tablename__ = 'Role'

    RoleId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)
    SeniorityLevel = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.String(250), nullable=False)

    def __init__(self, Name=None, Description=None, SeniorityLevel=None):
        self.Name = Name
        self.Description = Description
        self.SeniorityLevel = SeniorityLevel