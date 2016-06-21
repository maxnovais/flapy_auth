# coding: utf-8
import os

os.environ['AUTH_ENV'] = 'test'

import pytest
from auth.main import db

@pytest.yield_fixture(scope='session')
def app():
    """
    Creates a new Flask application for a test duration.
    Uses application factory `create_app`.
    """
    from auth.main import create_app
    _app = create_app()
    yield _app


@pytest.yield_fixture(scope='function', autouse=True)
def session(app):
    ctx = app.app_context()
    ctx.push()
    yield session
    ctx.pop()


@pytest.fixture(scope='session')
def database(session_app):
    ctx = session_app.test_request_context()
    ctx.push()
    db.create_all()
    ctx.pop()


@pytest.fixture
def user():
    from auth.actions import UserAction
    user = UserAction()
    return user.create(username='Darth Vader',
                       email='mayforce@bewith.you',
                       password='12345678',
                       confirm_password='12345678')
