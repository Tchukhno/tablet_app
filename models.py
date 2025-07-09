from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))  # admin, editor, viewer

class Tablet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True)

class Leader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tablet_id = db.Column(db.Integer, db.ForeignKey('tablet.id'))
    leader_id = db.Column(db.Integer, db.ForeignKey('leader.id'))
    brigade_number = db.Column(db.String(20))
    issue_date = db.Column(db.Date)
    added_by = db.Column(db.String(100))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_invalid = db.Column(db.Boolean, default=False)
