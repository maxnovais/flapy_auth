# coding: utf-8
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    config_object = 'auth.config.{}.Config'.format(os.environ.get('AUTH_ENV') or 'local')
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.debug = app.config['DEBUG']

    db.init_app(app)

    lm = LoginManager()
    lm.init_app(app)
    return app
