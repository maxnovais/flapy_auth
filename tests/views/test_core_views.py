# coding: utf-8
import json
import pytest
from flask import url_for


def test_generate_swagger_spec(client):
    response = client.get(url_for('core.spec'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['info']['title'] == 'Flapy Auth-API'
    assert response.status_code == 200


def test_should_execute_swagger_ui_with_spec_url(client):
    response = client.get(url_for('core.swagger_ui'))
    assert '<title>Swagger UI</title>' in response.data.decode('utf8')
    assert response.status_code == 200


def test_access_home(client):
    response = client.get(url_for('core.index'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'hello word!'
    assert response.status_code == 200


def test_login_user_with_success(user, header, client):
    response = client.post(url_for('core.login'),
                           data=json.dumps({'username': 'Darth_Vader', 'password': '12345678'}),
                           headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'success'
    assert response.status_code == 200


@pytest.mark.parametrize('status_code, message, username, password', [
    (400, 'bad_request', '', ''),
    (401, 'not_authorized', 'Darth_Vader', '87654321'),
    (404, 'not_found', 'Luke_Skywalker', '12345678')
])
def test_login_user_without_success(app, user, header, client, status_code, message, username, password):
    response = client.post(url_for('core.login'),
                           data=json.dumps({
                               'username': username,
                               'password': password
                           }),
                           headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == message
    assert response.status_code == status_code


def test_change_password_with_success(app, user, login, header, client):
    from flask_login import current_user
    new_password = '87654321'
    response = client.post(url_for('core.change_password'),
                           data=json.dumps({
                               'old_password': '12345678',
                               'password': new_password,
                               'confirm_password': new_password
                           }),
                           headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'success'
    client.get(url_for('core.logout'))
    assert current_user.is_authenticated is False
    response = client.post(url_for('core.login'),
                           data=json.dumps({'username': user.username, 'password': new_password}),
                           headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'success'
    assert response.status_code == 200


@pytest.mark.parametrize('status_code, message, old_password, password, confirm_password', [
    (400, 'bad_request', '', '', ''),
    (400, 'bad_request', '12345678', '123', '123'),
    (400, 'bad_request', '12345678', '123456', '12345678'),
    (401, 'not_authorized', 'Darth_Vader', '87654321', '87654321'),
])
def test_change_password_without_success(app, user, header, client, login, status_code, message, old_password,
                                         password, confirm_password):
    response = client.post(url_for('core.change_password'),
                           data=json.dumps({
                               'old_password': old_password,
                               'password': password,
                               'confirm_password': confirm_password
                           }),
                           headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == message
    assert response.status_code == status_code



def test_access_a_blocked_page_with_login(login, user, client):
    response = client.get(url_for('core.home'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'I\'m user as all!'
    assert response.status_code == 200


def test_access_a_blocked_page_without_login(user, client):
    response = client.get(url_for('core.home'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'not_authorized'
    assert response.status_code == 401


def test_access_a_blocked_page_by_role_with_success(login, user, client, user_role):
    response = client.get(url_for('core.user_view'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'I\'m user with success!'
    assert response.status_code == 200


def test_access_a_blocked_page_by_role_without_success(login, user, client):
    response = client.get(url_for('core.user_view'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['error_code'] == 'forbidden'
    assert response.status_code == 403


def test_logout_is_a_success(login, user, client):
    from flask_login import current_user
    response = client.get(url_for('core.logout'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'success'
    assert current_user.is_authenticated is False

