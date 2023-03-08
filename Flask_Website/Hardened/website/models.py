"""
Create DB models for users and notes and import db object
"""
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Inherit only from db.model
class Note(db.Model):
    # DB will automatically increment unique ids
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # SQL alchemy will automatically
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Set up relationship between note and user objects via foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Inherit from sqlalchemy obj, db.model and UserMixin
class User(db.Model, UserMixin):
    # Define schema of db
    # ID, is primary key and integer
    id = db.Column(db.Integer, primary_key=True)
    # Unique = True means no user can have same email
    email = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(1000))
    first_name = db.Column(db.String(150))
    # Store all notes
    notes = db.relationship('Note')
