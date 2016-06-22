#coding: utf-8


class BaseException(Exception):
    message = ''


class InvalidCredentials(BaseException):
    pass


class InvalidUsername(InvalidCredentials):
    pass


class InvalidPassword(InvalidCredentials):
    pass


class InvalidEmail(InvalidCredentials):
    pass


class PasswordMismatch(BaseException):
    pass


class UserNotFound(BaseException):
    pass


class UserAlreadyExist(BaseException):
    pass


class ValidationError(BaseException):
    pass


class SessionNotFound(BaseException):
    pass


class RoleAlreadyExist(BaseException):
    pass


class RoleNotFound(BaseException):
    pass