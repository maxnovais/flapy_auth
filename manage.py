# coding: utf-8
import os
from flask_script import Manager
from auth.main import create_app

env = os.environ.get('AUTH_ENV') or 'local'
manager = Manager(create_app(env))

if __name__ == '__main__':
    manager.run()