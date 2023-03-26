from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(20), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(200))
    notes = db.relationship('Note')

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(5000))
    #category examples: plates, wheels, other, holders & adapters for: sensors, microcontrollers & SBCs, motors, cameras 
    category = db.Column(db.Integer)
    file_name = db.Column(db.String(20), unique=True)
    picture = db.Column(db.String(20), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    verified = db.Column(db.Boolean, default=False)
    featured = db.Column(db.Boolean, default=False)
    public = db.Column(db.Boolean, default=False)
    rejected = db.Column(db.Boolean, default=False)
    downloads = db.Column(db.Integer, default=0)
    
    
     