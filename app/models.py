from flask_login import UserMixin
from datetime import datetime
from .app import db 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(32), nullable = False)
    password = db.Column(db.String(32), nullable = False)
    fullname = db.Column(db.String(32), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = False)

class Role(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_role = db.Column(db.String(32), nullable = False)
    name_role = db.Column(db.String(255), nullable = False)


class Book(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), nullable = False)
    author = db.Column(db.String(32), nullable = False)
    year = db.Column(db.Integer, nullable = False)
    quantity = db.Column(db.Integer,nullable = False)

class UsersBook(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Integer, nullable = False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    book = db.Column(db.Integer,  db.ForeignKey('book.id'), nullable = False)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable = False)

class Status(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    condition = db.Column(db.String(32), nullable = False) 