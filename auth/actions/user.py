# coding: utf-8
import re
from auth.exceptions import InvalidPassword, InvalidUsername, PasswordMismatch, UserNotFound
from auth.main import db
from auth.models import User


class UserAction(object):
    def create(self, username, email, password, confirm_password):
        if len(password) < 8:
            raise InvalidPassword

        if password != confirm_password:
            raise PasswordMismatch

        if not username or username < 5:
            raise InvalidUsername

        user = User(username=username, email=email, password=self.hash_password(password))
        db.session.add(user)
        db.session.commit()

    def get_user(self, login):
        try:
            if self.verify_email(login):
                user = User.query.filter_by(email=login).one()
            else:
                user = User.query.filter_by(username=login).one()
        except:
            raise UserNotFound
        return user

    def verify_email(self, login):
        match = re.search(r'[\w.-]+@[\w.-]+.\w+', login)
        if match:
            return True

    def verify_username(self, login):
        match = re.search(r'^[a-zA-Z0-9_.-]+$', login)
        if match:
            return login
