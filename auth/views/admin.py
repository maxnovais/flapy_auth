# coding: utf-8
"""The views of user administration are here"""
from flask import Blueprint, abort, jsonify
from flask_login import login_required
from auth.models import User, Role
from auth.views import login_permission, dict_list


blueprint = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
@login_required
def home():
    """Admin home"""
    permissions = ['admin']
    if not login_permission(permissions):
        return abort(403)

    users = dict_list(User.query.order_by(User.id.desc()).limit(10).all())
    roles = dict_list(Role.query.order_by(Role.id.desc()).limit(10).all())

    data = {
        'latest_10_users': users,
        'latest_10_roles': roles,
    }

    return jsonify(data), 200
