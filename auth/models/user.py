# coding: utf-8
from datetime import datetime
from auth.models import Model, db


class User(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user'

    username =db.Column(db.String(30), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(default=True))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer())

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False


class Role(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return '<Roles {}>'.format(self.name)


class UserRole(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user_role'

    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))

    __table_args__ = (db.UniqueConstraint('user_id', 'role_id', name='un_user_role'),)