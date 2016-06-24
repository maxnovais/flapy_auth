# coding: utf-8
from datetime import datetime
from flask_login import UserMixin
from auth.models import Model, db


class User(Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user'

    username =db.Column(db.String(30), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer())
