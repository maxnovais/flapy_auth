# coding: utf-8
from datetime import datetime
from auth.main import db


class BaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())


from auth.models.user import User
