# coding: utf-8
import re
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from auth.exceptions import (InvalidPassword, InvalidUsername, InvalidEmail, PasswordMismatch, UserAlreadyExist,
                             UserNotFound)
from auth.main import db
from auth.models import User


class UserAction(object):
    def create(self, username, email, password=None, confirm_password=None):
        """ Create a new user """
        if len(username) < 5:
            raise InvalidUsername

        if not self.verify_username(username):
            raise InvalidUsername

        if not self.verify_email(email):
            raise InvalidEmail

        if len(password) < 8:
            raise InvalidPassword

        if password != confirm_password:
            raise PasswordMismatch

        try:
            user = User()
            user.username = username
            user.email = email
            user.password = self.generate_password(password)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            raise UserAlreadyExist

    def get_user(self, login):
        try:
            if self.verify_email(login):
                user = User.query.filter_by(email=login).one()
            else:
                user = User.query.filter_by(username=login).one()
        except:
            raise UserNotFound
        return user

    def validate_password(self, login, password):
        user = self.get_user(login)
        if check_password_hash(user.password, password):
            return True

    def change_password(self, login, old_password, new_password, confirm_new_password):
        if not self.validate_password(login, old_password):
            raise InvalidPassword

        if len(new_password) < 8:
            raise InvalidPassword

        if new_password != confirm_new_password:
            raise PasswordMismatch

        user = self.get_user(login)
        user.password = self.generate_password(new_password)
        db.session.add(user)
        db.session.commit()

    def reset_password(self, email):
        pass

    def generate_password(self, password):
        if not password:
            password = self.random_password(12)
        return generate_password_hash(password)

    @staticmethod
    def random_password(size=12):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    @staticmethod
    def verify_email(email):
        if re.search(r'[\w.-]+@[\w.-]+.\w+', email):
            return True

    @staticmethod
    def verify_username(username):
        if re.search(r'^[a-zA-Z0-9_.-]+$', username):
            return True
