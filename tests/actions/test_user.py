# coding: utf-8
from auth.actions import UserAction
from auth.models import User


def test_create_user_with_success():
    user_action = UserAction()
    user_action.create(username='testuser', email='test1@gmail.com', password='12345678', confirm_password='12345678')
    user = User.query.filter_by(username='testuser').one()

    assert user.email == 'test1@gmail.com'
