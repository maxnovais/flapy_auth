# coding: utf-8
import json
from flask import url_for


def test_home_should_return_latest_values(app, client, admin_login):
    response = client.get(url_for('admin.home'))
    data = json.loads(response.data.decode('utf-8'))
    assert data['latest']['roles'][0]['description'] == 'Administrator'
    assert data['latest']['users'][0]['username'] == 'Darth_Vader'
