# coding: utf-8
import pytest
from werkzeug.exceptions import Forbidden
from auth.views import login_permission



def test_check_login_permission_return_true(user, role, admin_role, login):
    permission = login_permission((role.name,))
    assert permission is True


def test_check_login_permission_return_false_if_user_not_have_role(user, role, login):
    with pytest.raises(Forbidden):
        permission = login_permission((role.name,))


def test_check_login_permission_return_false_if_role_not_exists(user, login):
    with pytest.raises(Forbidden):
        permission = login_permission(('inexistent_role',))