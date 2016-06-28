# coding: utf-8
import json
import pytest
from flask import url_for


def test_home_should_return_latest_values(client, admin_login):
    response = client.get(url_for('admin.home'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['latest']['roles'][0]['description'] == 'Administrator'
    assert data['latest']['users'][0]['username'] == 'Darth_Vader'
    assert response.status_code == 200


def test_user_return_all_users_in_base(client, admin_login, other_user):
    response = client.get(url_for('admin.users'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['total'] == 2
    assert response.status_code == 200


def test_create_new_user_with_success(client, admin_login, header):
    response = client.post(url_for('admin.create_user'),
                           data=json.dumps({'username': 'Anakin', 'email': 'anakin@sw.com', 'password': '123456',
                                            'confirm_password': '123456'}), headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['user']['username'] == 'Anakin'
    assert response.status_code == 201


@pytest.mark.parametrize('status_code, error_code, username, email, password, confirm_password', [
    (400, 'bad_request', '', '', '', ''),
    (400, 'bad_request', 'Darth Vader', 'notvalidemail', '654321', '123456'),
    (409, 'conflict', 'Darth_Vader', 'mayforce@bewith.you', '123456', '123456')])
def test_create_new_user_without_success(client, admin_login, header, status_code, error_code, username, email,
                                        password, confirm_password):
    response = client.post(url_for('admin.create_user'),
                           data=json.dumps({'username': username, 'email': email, 'password': password,
                                            'confirm_password': confirm_password}), headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == error_code
    assert response.status_code == status_code


def test_user_return_a_single_user_in_base(client, admin_login, other_user):
    response = client.get(url_for('admin.show_user', user_id=other_user.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['user']['username'] == other_user.username
    assert response.status_code == 200


def test_should_toggle_status_of_single_user(client, admin_login, other_user):
    response = client.post(url_for('admin.toogle_user_status', user_id=other_user.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['user']['active'] is False
    assert response.status_code == 202


def test_should_return_user_roles_with_success(client, admin_login, user):
    response = client.get(url_for('admin.show_user_roles', user_id=user.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['roles'][0]['name'] == 'admin'
    assert response.status_code == 200


def test_should_delete_all_user_roles_with_success(client, admin_login, other_user, other_user_in_role):
    response = client.get(url_for('admin.show_user_roles', user_id=other_user.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['roles'][0]['name'] == 'admin'
    response = client.delete(url_for('admin.delete_user_roles', user_id=other_user.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['user']['roles'] == []


def test_should_return_error_in_remove_role_of_empty_user(client, admin_login, other_user):
    response = client.delete(url_for('admin.delete_user_roles', user_id=other_user.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


@pytest.mark.parametrize('view', ['admin.show_user', 'admin.show_user_roles'])
def test_do_not_return_inexistent_user_for_get_views(client, admin_login, view):
    response = client.get(url_for(view, user_id=100))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


@pytest.mark.parametrize('view', ['admin.toogle_user_status'])
def test_do_not_return_inexistent_user_for_post_views(client, admin_login, view):
    response = client.post(url_for(view, user_id=100))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


@pytest.mark.parametrize('view', ['admin.delete_user_roles'])
def test_do_not_return_inexistent_user_for_delete_views(client, admin_login, view):
    response = client.delete(url_for(view, user_id=100))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


def test_set_user_role_with_success(client, admin_login, other_user, role_writer):
    response = client.post(url_for('admin.set_user_role', user_id=other_user.id, role_id=role_writer.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['user']['roles'][0]['name'] == 'writer'


def test_set_user_inexistent_role(client, admin_login, other_user):
    response = client.post(url_for('admin.set_user_role', user_id=other_user.id, role_id=100))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


def test_set_user_role_with_conflict(client, admin_login, other_user, other_user_in_role, role):
    response = client.post(url_for('admin.set_user_role', user_id=other_user.id, role_id=role.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'conflict'
    assert response.status_code == 409


def test_delete_user_role_with_success(client, admin_login, other_user, other_user_in_role, role):
    response = client.delete(url_for('admin.delete_user_role', user_id=other_user.id, role_id=role.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['user']['roles'] == []


def test_delete_user_inexistent_role(client, admin_login, other_user):
    response = client.delete(url_for('admin.delete_user_role', user_id=other_user.id, role_id=100))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


def test_delete_user_role_with_conflict(client, admin_login, other_user, role):
    response = client.delete(url_for('admin.delete_user_role', user_id=other_user.id, role_id=role.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'conflict'
    assert response.status_code == 409


def test_user_return_all_roles_in_base(client, admin_login, role, role_writer, role_user):
    response = client.get(url_for('admin.roles'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['total'] == 3
    assert response.status_code == 200


def test_create_new_role_with_success(client, admin_login, header):
    response = client.post(url_for('admin.create_role'),
                           data=json.dumps({'name': 'madmax', 'description': 'Mad'}), headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['role']['name'] == 'madmax'
    assert response.status_code == 201


@pytest.mark.parametrize('status_code, error_code, name, description', [
    (400, 'bad_request', 'a', ''),
    (400, 'bad_request', '', ''),
    (409, 'conflict', 'admin', 'admin')])
def test_create_new_role_without_success(client, admin_login, header, role, status_code, error_code, name, description):
    response = client.post(url_for('admin.create_role'),
                           data=json.dumps({'name': name, 'description': description}), headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == error_code
    assert response.status_code == status_code


def test_should_return_a_single_role_in_base(client, admin_login, role):
    response = client.get(url_for('admin.show_role', role_id=role.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['role']['name'] == role.name
    assert response.status_code == 200


@pytest.mark.parametrize('view', ['admin.show_role', 'admin.show_role_users'])
def test_do_not_return_inexistent_role_for_get_views(client, admin_login, view):
    response = client.get(url_for(view, role_id=100))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


@pytest.mark.parametrize('view', ['admin.edit_role'])
def test_do_not_return_inexistent_role_for_post_views(client, admin_login, view, header):
    response = client.post(url_for(view, role_id=100),
                           data=json.dumps({'name': 'madmax', 'description': 'Mad'}), headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


@pytest.mark.parametrize('view', ['admin.delete_role', 'admin.remove_all_users'])
def test_do_not_return_inexistent_role_for_delete_views(client, admin_login, view):
    response = client.delete(url_for(view, role_id=100))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


def test_edit_role_with_success(client, admin_login, header, role_writer):
    response = client.post(url_for('admin.edit_role', role_id=role_writer.id),
                           data=json.dumps({'name': 'madmax', 'description': 'Mad'}), headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['role']['name'] == 'madmax'
    assert response.status_code == 202


@pytest.mark.parametrize('status_code, error_code, name, description', [
    (400, 'bad_request', 'a', ''),
    (400, 'bad_request', '', ''),
    (409, 'conflict', 'admin', 'admin')])
def test_edit_role_without_success(client, admin_login, header, role, role_writer, status_code, error_code, name, description):
    response = client.post(url_for('admin.edit_role', role_id=role_writer.id),
                           data=json.dumps({'name': name, 'description': description}), headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == error_code
    assert response.status_code == status_code


def test_remove_role_with_success(client, admin_login, role_writer):
    response = client.delete(url_for('admin.delete_role', role_id=role_writer.id))
    data = json.loads(response.data.decode('utf-8'))
    assert role_writer.name not in data
    assert response.status_code == 202


def test_remove_all_users_of_role_with_success(client, admin_login, user, role_user, user_role):
    response = client.get(url_for('admin.show_role', role_id=user_role.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['role']['users'][0]['username'] == user.username

    response = client.delete(url_for('admin.remove_all_users', role_id=role_user.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['role']['users'] == []
    assert response.status_code == 202


def test_should_return_all_users_in_this_role(client, admin_login, user, role, other_user, other_user_in_role):
    response = client.get(url_for('admin.show_role_users', role_id=role.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['users'][0]['username'] == 'Darth_Vader'
    assert response.status_code == 200