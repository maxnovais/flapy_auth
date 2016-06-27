# coding: utf-8
import json
import pytest
from flask import url_for


def test_home_should_return_latest_values(app, client, admin_login):
    response = client.get(url_for('admin.home'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['latest']['roles'][0]['description'] == 'Administrator'
    assert data['latest']['users'][0]['username'] == 'Darth_Vader'


def test_user_return_all_users_in_base(app, client, admin_login, other_user):
    response = client.get(url_for('admin.users'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['total'] == 2


def test_create_new_user_with_success(app, client, admin_login, header):
    response = client.post(url_for('admin.create_user'),
                           data=json.dumps({'username': 'Anakin', 'email': 'anakin@sw.com', 'password': '123456',
                                            'confirm_password': '123456'}), headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['user']['username'] == 'Anakin'


@pytest.mark.parametrize('status_code, error_code, username, email, password, confirm_password', [
    (400, 'bad_request', '', '', '', ''),
    (400, 'bad_request', 'Darth Vader', 'notvalidemail', '654321', '123456'),
    (409, 'conflict', 'Darth_Vader', 'mayforce@bewith.you', '123456', '123456')])
def test_create_new_user_without_success(app, client, admin_login, header, status_code, error_code, username, email,
                                        password, confirm_password):
    response = client.post(url_for('admin.create_user'),
                           data=json.dumps({'username': username, 'email': email, 'password': password,
                                            'confirm_password': confirm_password}), headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == error_code
    assert response.status_code == status_code


def test_user_return_a_single_user_in_base(app, client, admin_login, other_user):
    response = client.get(url_for('admin.show_user', user_id=other_user.id))
    data = json.loads(response.data.decode('utf-8'))
    assert data['user']['username'] == other_user.username



@pytest.mark.parametrize('view', [('admin.show_user'), ('admin.show_user_roles')])
def test_do_not_return_inexistent_user_for_get_views(app, client, admin_login, view):
    response = client.get(url_for(view, user_id=100))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


@pytest.mark.parametrize('view', [('admin.toogle_user_status')])
def test_do_not_return_inexistent_user_for_post_views(app, client, admin_login, view):
    response = client.post(url_for(view, user_id=100))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404


@pytest.mark.parametrize('view', [('admin.delete_user_roles')])
def test_do_not_return_inexistent_user_for_delete_views(app, client, admin_login, view):
    response = client.delete(url_for(view, user_id=100))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_found'
    assert response.status_code == 404