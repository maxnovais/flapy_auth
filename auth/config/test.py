#coding: utf-8
import os
from auth.config.base import BaseConfig


class Config(BaseConfig):
    """ Specific config used in test environment """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
