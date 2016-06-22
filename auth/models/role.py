# coding: utf-8
from datetime import datetime
from auth.models import Model, db


class Role(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())

    @property
    def is_active(self):
        return self.active
