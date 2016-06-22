# coding: utf-8
import pytest
from auth.actions import RoleAction
from auth.exceptions import RoleNotFound, RoleAlreadyExist, InvalidRoleName
from auth.models import Role


def test_create_role_with_success():
    role_action = RoleAction()
    created_role = role_action.create(name='Review', description='Reviewer')
    role = Role.query.filter(Role.name == created_role.name).one()
    assert role.description == created_role.description


@pytest.mark.parametrize('exception, name', [
    (RoleAlreadyExist, 'Admin'),
    (InvalidRoleName, '')
])
def test_should_not_create_role(role, exception, name):
    role_action = RoleAction()
    with pytest.raises(exception):
        role_action.create(name=name)


def test_edit_role_with_sucess(role):
    role_action = RoleAction()
    role_action.edit(role.id, name='User', description='Simple User')
    assert role.name == 'User'


@pytest.mark.parametrize('exception, name', [
    (RoleAlreadyExist, 'Admin'),
    (InvalidRoleName, 'Ad')
])
def test_should_not_edit_role(role, exception, name):
    role = RoleAction().create(name='User', description='Simple User')
    with pytest.raises(exception):
        RoleAction().edit(role.id, name=name)


def test_invalidate_and_validate_role(role):
    role_action = RoleAction()
    role_action.change_status(role.id)
    assert role.is_active is False
    role_action.change_status(role.id)
    assert role.is_active is True


def test_search_role_with_name(role):
    role = RoleAction().search_role(name='Admin', exactly=True)
    assert role.description == 'Administrator'


def test_search_role_with_part_of_name(role):
    role_list = RoleAction().search_role(name='Ad', exactly=False)
    assert role in role_list


def test_search_role_do_not_return_a_role():
    with pytest.raises(RoleNotFound):
        RoleAction().search_role(name='Inexist role', exactly=True)


def test_delete_role_with_success(role):
    role_action = RoleAction()
    role_action.delete(role.id)
    assert Role.query.all() == []
