from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    weight = db.Column(db.Integer)
    shoulder = db.Column(db.REAL)
    chest = db.Column(db.REAL)
    arm = db.Column(db.REAL)
    forearm = db.Column(db.REAL)
    waist = db.Column(db.REAL)
    leg = db.Column(db.REAL)
    calf = db.Column(db.REAL)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    measurements = db.relationship('Measurement')
