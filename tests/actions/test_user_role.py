# coding: utf-8
import pytest
from auth.action import UserRoleAction
from auth.exceptions import UserAlreadyInRole, RoleAlreadyEmpty, UserNotHasRole


@pytest.fixture
def role_writer():
    from auth.models import Role
    role = Role()
    role.name = 'Writer'
    role.description = 'Writer'
    role.save(commit=True)
    return role

@pytest.fixture
def other_user():
    from auth.models import User
    from auth.action import UserAction
    user = User()
    user.username = 'Luke_Skywalker'
    user.email = 'mayforce@bewith.me'
    user.password = UserAction().generate_password(password='12345678')
    user.save(commit=True)
    return user


@pytest.fixture
def other_user_in_role(other_user, role):
    from auth.models import UserRole
    user_role = UserRole()
    user_role.user = other_user
    user_role.role = role
    user_role.save(commit=True)
    return user_role


def test_create_user_role_with_success(user, role, role_user):
    user_role_action = UserRoleAction()
    user_role_action.set_role(user, role)
    user_role_action.set_role(user, role_user)

    assert user_role_action.user_has_role(user, role) is True
    assert user_role_action.user_has_role(user, role_user) is True


def test_should_raise_error_in_duplicate_user_role(user, role, admin_role):
    user_role_action = UserRoleAction()
    with pytest.raises(UserAlreadyInRole):
        user_role_action.set_role(user, role)


def test_remove_all_users_of_a_role(role, user, admin_role, other_user, other_user_in_role):
    user_role_action = UserRoleAction()
    assert len(user_role_action.get_users(role)) == 2
    user_role_action.empty_role(role)
    assert len(user_role_action.get_users_in_role(role)) == 0


def test_should_raise_error_in_remove_users_from_empty_role(role):
    user_role_action = UserRoleAction()
    with pytest.raises(RoleAlreadyEmpty):
        user_role_action.empty_role(role)


def test_remove_all_roles_for_a_user(user, admin_role, role, role_user, role_writer):
    user_role_action = UserRoleAction()
    user_role_action.set_role(user, role_writer)
    user_role_action.set_role(user, role_user)
    assert len(user_role_action.get_roles(user)) == 3
    user_role_action.remove_user_roles(user)
    assert len(user_role_action.get_roles(user)) == 0


def test_should_raise_error_in_remove_users_role_without_roles(user):
    user_role_action = UserRoleAction()
    with pytest.raises(UserNotHasRole):
        user_role_action.remove_user_roles(user)
