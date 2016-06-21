# coding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy(session_options={'expire_on_commit': False, 'autoflush': False})
lm = LoginManager()


def create_app(env):
    config_object = 'elflapy.config.{}.Config'.format(env)
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.debug = app.config['DEBUG']
    db.init_app()
    lm.init_app(app)
    return app

