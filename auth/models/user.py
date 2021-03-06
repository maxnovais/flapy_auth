# coding: utf-8
import re
import random
import string
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from auth.exceptions import (InvalidPassword, InvalidUsername, InvalidEmail, PasswordMismatch, UserAlreadyExist,
                             UserNotFound, UserNotHasRole, InvalidCredentials)
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

    @classmethod
    def by_login(cls, login):
        """Search user by username or email"""
        if cls.verify_email(login):
            user = cls.query.filter(User.email == login).first()
        else:
            user = cls.query.filter(User.username == login).first()
        if not user:
            raise UserNotFound
        return user

    @classmethod
    def create(cls, username, email, password, confirm_password):
        """ Create a new user """
        if not cls.verify_username(username):
            raise InvalidUsername

        if not cls.verify_email(email):
            raise InvalidEmail

        if len(password) < 6:
            raise InvalidPassword

        if password != confirm_password:
            raise PasswordMismatch

        try:
            user = User()
            user.username = username
            user.email = email
            user.password = cls.generate_password(password)
            user.save()
            db.session.commit()
            return user
        except IntegrityError:
            raise UserAlreadyExist

    def change_password(self, old_password, password, confirm_password):
        """Change password of user"""
        if not self.validate_password(old_password):
            raise InvalidCredentials

        if len(password) < 6:
            raise InvalidPassword

        if password != confirm_password:
            raise PasswordMismatch

        self.password = self.generate_password(password)
        self.save()
        db.session.commit()

    def validate_password(self, password):
        """Used for validate hash password"""
        if check_password_hash(self.password, password):
            return True

    @staticmethod
    def random_password(size=12):
        """Create a string for password"""
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    @staticmethod
    def verify_email(email):
        """Check if the email contains valid format"""
        if re.search(r'[\w.-]+@[\w.-]+.\w+', email):
            return True

    @staticmethod
    def verify_username(username):
        """Check length and if the username does not contains invalid chars"""
        if len(username) >= 3 and re.search(r'^[a-zA-Z0-9_.-]+$', username):
            return True

    @classmethod
    def generate_password(cls, password=None):
        """Create hash when password set or create a random password"""
        if not password:
            password = cls.random_password(12)
        return generate_password_hash(password)

    @property
    def roles(self):
        """Return all roles of this user"""
        roles = []
        for user_role in self.user_roles:
            roles.append(user_role.role)
        return roles

    def has_role(self, role):
        """Verify if this user have role"""
        if role in self.roles:
            return True

    def delete_all_roles(self):
        """Remove all roles of this user"""
        if not self.user_roles:
            raise UserNotHasRole

        for user_role in self.user_roles:
            user_role.delete(commit=True)
        db.session.commit()
