# coding: utf-8
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from auth.blueprints import register_blueprints
from auth.handler import error_handlers


db = SQLAlchemy()


def create_app():
    config_object = 'auth.config.{}.Config'.format(os.environ.get('AUTH_ENV') or 'local')
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.debug = app.config['DEBUG']

    db.init_app(app)

    lm = LoginManager()
    lm.init_app(app)

    def load_user(user_id):
        try:
            from auth.action import UserAction
            return UserAction().get_by_id(user_id)
        except ValueError:
            pass

    load_user = lm.user_loader(load_user)
    error_handlers(app)
    register_blueprints(app)
    return app
