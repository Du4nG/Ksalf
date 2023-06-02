from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Interger, primary_key=True)
    email = db.Column(db.String(128), uniqe=True)
    password = db.Column(db.String(128))  
    first_name = db.COlumn(db.String(128))