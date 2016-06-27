#coding: utf-8
import os


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False