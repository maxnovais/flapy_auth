# coding: utf-8
import pytest
from auth.exceptions import RoleNotFound, RoleAlreadyExist, InvalidRoleName
from auth.models import Role


def test_create_role_with_success():
    created_role = Role.create(name='review', description='Reviewer')
    role = Role.query.filter(Role.name == created_role.name).one()
    assert role.description == created_role.description


@pytest.mark.parametrize('exception, name', [
    (RoleAlreadyExist, 'admin'),
    (InvalidRoleName, '')
])
def test_should_not_create_role(role, exception, name):
    with pytest.raises(exception):
        Role.create(name=name)


def test_edit_role_with_sucess(role):
    role.edit(name='user', description='Simple User')
    assert role.name == 'user'


@pytest.mark.parametrize('exception, name', [
    (RoleAlreadyExist, 'admin'),
    (InvalidRoleName, 'ad')
])
def test_should_not_edit_role(role, exception, name):
    role = Role.create(name='user', description='Simple User')
    with pytest.raises(exception):
        role.edit(name=name)


def test_invalidate_and_validate_role(role):
    role.toggle_status()
    assert role.is_active is False
    role.toggle_status()
    assert role.is_active is True


def test_search_role_with_name(role):
    role = Role.search_role(name='admin', exactly=True)
    assert role.description == 'Administrator'


def test_search_role_with_part_of_name(role):
    role_list = Role.search_role(name='ad', exactly=False)
    assert role in role_list


def test_search_role_do_not_return_a_role():
    with pytest.raises(RoleNotFound):
        Role.search_role(name='Inexist role', exactly=True)
