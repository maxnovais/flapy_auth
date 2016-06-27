# coding: utf-8
"""The views of user administration are here"""
from flask import Blueprint, abort, jsonify, request
from flask_login import login_required
from auth.models import User, Role
from auth.views import login_permission, query_object_list, dict_object
from auth.exceptions import (InvalidUsername, InvalidEmail, InvalidPassword, PasswordMismatch, UserAlreadyExist,
                             InvalidRoleName, RoleAlreadyExist)


blueprint = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
@login_required
def home():
    """Admin home"""
    login_permission([blueprint.name])

    users, total_users = query_object_list(User, paginable=False)
    roles, total_roles = query_object_list(Role, paginable=False)

    data = {
        'latest': {'users': users, 'roles': roles},
        'totals': {'users': total_users, 'roles': total_roles}
    }

    return jsonify(data), 200


@blueprint.route('/users', methods=['GET'])
# @login_required
def users():
    """ Get Users """
    login_permission([blueprint.name])

    values, total = query_object_list(User)
    data = {'users': values, 'total': total}
    return jsonify(data), 200


@blueprint.route('/users', methods=['POST'])
def create_user():
    """ Create new user """
    required_fields = ('username', 'email', 'password', 'confirm_password')
    if all(request.json.get(field) for field in required_fields):
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        confirm_password = request.json.get('confirm_password')
    else:
        return abort(400)

    try:
        user = User.create(username=username, email=email, password=password, confirm_password=confirm_password)
        data = {'user': dict_object(user)}
        return jsonify(data), 201

    except (InvalidUsername, InvalidEmail, InvalidPassword, PasswordMismatch):
        abort(400)

    except UserAlreadyExist:
        abort(409)


@blueprint.route('/roles', methods=['GET'])
# @login_required
def roles():
    """Get Roles"""
    login_permission([blueprint.name])

    values, total = query_object_list(Role)
    data = {'roles': values, 'total': total}
    return jsonify(data), 200


@blueprint.route('/roles', methods=['POST'])
def create_role():
    """ Create new user """
    required_fields = ('name')
    if all(request.json.get(field) for field in required_fields):
        name = request.json.get('name')
        description = request.json.get('description')
    else:
        return abort(400)

    try:
        role = Role.create(name=name, description=description)
        data = {'role': dict_object(role)}
        return jsonify(data), 201

    except InvalidRoleName:
        abort(400)

    except RoleAlreadyExist:
        abort(409)
