# coding: utf-8
import json
from flask import url_for


def test_home_should_return_latest_values(app, client, admin_login):
    response = client.get(url_for('admin.home'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['latest_10_roles'][0]['description'] == 'Administrator'
    assert data['latest_10_users'][0]['username'] == 'Darth_Vader'
