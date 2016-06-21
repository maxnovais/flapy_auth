# coding: utf-8
from flask import Flask
from flask_login import LoginManager


def create_app(env):
    config_object = 'elflapy.config.{}.Config'.format(env)
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.debug = app.config['DEBUG']

    lm = LoginManager()
    lm.init_app(app)

    return app