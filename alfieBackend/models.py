from .app import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class Expenses(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    dateOcurred=db.Column(db.DateTime(timezone=True), default=func.now())
    itemName=db.Column(db.String(200), nullable=False)
    price=db.Column(db.Integer, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
class Goals(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    goal=db.Column(db.String(500), nullable=False)
    dueDate=db.Column(db.DateTime(timezone=True), nullable=False)
    completed=db.Column(db.Boolean, default=False, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    expenses=db.relationship('Expenses')
    goals=db.relationship('Goals')
  