# coding: utf-8
import json
import pytest
from flask import url_for


@pytest.fixture
def header():
    return {'Content-Type': 'application/json; charset=UTF-8'}


def test_access_home(client):
    response = client.get(url_for('core.index'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'hello word!'
    assert response.status_code == 200


def test_login_user_with_success(user, header, client):
    response = client.post(url_for('core.login'),
                           data=json.dumps({
                               'username': 'Darth_Vader',
                               'password': '12345678'
                           }),
                           headers=header)
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'success'
    assert response.status_code == 200


@pytest.mark.parametrize('status_code, message, username, password',[
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
