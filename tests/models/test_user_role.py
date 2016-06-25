# coding: utf-8
import pytest
from auth.exceptions import UserAlreadyInRole, RoleAlreadyEmpty, UserNotHasRole
from auth.models import UserRole


def test_create_user_role_with_success(user, role, role_user):
    UserRole.set_role(user, role)
    UserRole.set_role(user, role_user)
    assert user.has_role(role) is True


def test_should_raise_error_in_duplicate_user_role(user, role, admin_role):
    with pytest.raises(UserAlreadyInRole):
        UserRole.set_role(user, role)


def test_should_raise_error_in_remove_users_role_without_roles(user):
    with pytest.raises(UserNotHasRole):
        user.delete_all_roles()


def test_remove_all_roles_for_a_user(user, admin_role, role, role_user, role_writer):
    UserRole.set_role(user, role_writer)
    UserRole.set_role(user, role_user)
    assert len(user.roles) == 3
    user.delete_all_roles()
    user_roles = UserRole.query.filter(UserRole.user == user).all()
    assert len(user_roles) == 0
    # Todo: Review refresh model


def test_remove_all_users_of_a_role(role, user, admin_role, other_user, other_user_in_role):
    assert len(role.users) == 2
    role.remove_all_users()
    role_users = UserRole.query.filter(UserRole.role == role).all()
    assert len(role_users) == 0


