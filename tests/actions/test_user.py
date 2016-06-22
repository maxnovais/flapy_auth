# coding: utf-8
import pytest
from auth.actions import UserAction
from auth.exceptions import (UserAlreadyExist, InvalidUsername, InvalidEmail, InvalidPassword, PasswordMismatch,
                             UserNotFound)
from auth.models import User


def test_create_user_with_success():
    user_action = UserAction()
    user_action.create(username='testuser', email='test1@gmail.com', password='12345678', confirm_password='12345678')
    user = User.query.filter_by(username='testuser').one()
    assert user.email == 'test1@gmail.com'


@pytest.mark.parametrize('exception, username, email, password, confirm_password', [
    (UserAlreadyExist, 'Darth_Vader', 'mayforce@bewith.you', '12345678', '12345678'),
    (InvalidUsername, '', 'test1@gmail.com', '12345678', '12345678'),
    (InvalidUsername, 'test@user', 'test1@gmail.com', '12345678', '12345678'),
    (InvalidEmail, 'testuser', 'itsnotvalidemail', '12345678', '12345678'),
    (InvalidPassword, 'testuser', 'test1@gmail.com', '', ''),
    (PasswordMismatch, 'testuser', 'test1@gmail.com', '12345678', '87654321'),
])
def test_create_user_raises_error(user, exception, username, email, password, confirm_password):
    user_action = UserAction()
    with pytest.raises(exception):
        user_action.create(username=username, email=email, password=password, confirm_password=confirm_password)


def test_change_user_password_with_success(user):
    user_action = UserAction()
    user_action.change_password(user.username, '12345678', '87654321', '87654321')
    valid = user_action.validate_password(user.username, '87654321')
    assert valid is True


@pytest.mark.parametrize('exception, password, new_password, confirm_new_password', [
    (InvalidPassword, 'password_error', '12345678', '12345678'),
    (InvalidPassword, '12345678', '', ''),
    (PasswordMismatch, '12345678', '1234567890', '0987654321'),
])
def test_change_password_errors(user, exception, password, new_password, confirm_new_password):
    user_action = UserAction()
    with pytest.raises(exception):
        user_action.change_password(login=user.username, old_password=password, new_password=new_password,
                                    confirm_new_password=confirm_new_password)


def test_get_user_with_username(user):
    user_action = UserAction()
    user = user_action.get_user('Darth_Vader')
    assert user.email == 'mayforce@bewith.you'


def test_get_user_with_email(user):
    user_action = UserAction()
    user = user_action.get_user('mayforce@bewith.you')
    assert str(user) == '<User[1] username=\'Darth_Vader\'>'


def test_get_inexistent_user():
    user_action = UserAction()
    with pytest.raises(UserNotFound):
        user_action.get_user('Luke_Skywalker')


def test_return_true_in_validate_password(user):
    user_action = UserAction()
    valid = user_action.validate_password('Darth_Vader', '12345678')
    assert valid is True


def test_invalidate_and_validate_user(user):
    user_action = UserAction()
    user_action.change_status(user.username)
    assert user.is_active is False
    user_action.change_status(user.email)
    assert user.is_active is True


