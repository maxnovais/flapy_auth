#coding: utf-8
import os
from auth.config.base import BaseConfig


class Config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
