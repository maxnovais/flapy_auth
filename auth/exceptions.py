#coding: utf-8


class BaseException(Exception):
    message = ''


class InvalidUsername(BaseException):
    pass


class InvalidPassword(BaseException):
    pass


class PasswordMismatch(BaseException):
    pass


class UserNotFound(BaseException):
    pass