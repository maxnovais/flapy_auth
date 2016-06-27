# coding: utf-8
"""The views of user administration are here"""
from flask import Blueprint, abort, jsonify, request, redirect
from flask_login import login_required
from auth.models import User, Role, UserRole
from auth.views import login_permission, query_object_list, dict_object, dict_list
from auth.exceptions import (InvalidUsername, InvalidEmail, InvalidPassword, PasswordMismatch, UserAlreadyExist,
                             InvalidRoleName, RoleAlreadyExist, UserAlreadyInRole, UserRoleNotFound, UserNotHasRole)


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


@blueprint.route('/users/<user_id>', methods=['GET'])
def show_user(user_id):
    """ Show user """
    user = User.query.get(user_id)
    if not user:
        abort(404)

    data = {'user': dict_object(user)}
    data['user']['roles'] = dict_list(user.roles)
    return jsonify(data), 200


@blueprint.route('/users/<user_id>/status', methods=['POST'])
def toogle_user_status(user_id):
    """ Show user """
    user = User.query.get(user_id)
    if not user:
        abort(404)

    user.toggle_status()
    user.refresh()

    data = {'user': dict_object(user)}
    return jsonify(data), 202


@blueprint.route('/users/<user_id>/roles', methods=['GET'])
def show_user_roles(user_id):
    """ Show user """
    user = User.query.get(user_id)
    if not user:
        abort(404)

    data = {'roles': dict_list(user.roles)}
    return jsonify(data), 200


@blueprint.route('/users/<user_id>/roles', methods=['DELETE'])
def delete_user_roles(user_id):
    """ Show user """
    user = User.query.get(user_id)
    if not user:
        abort(404)

    try:
        user.delete_all_roles()
        user.refresh()
        data = {'user': dict_object(user)}
        return jsonify(data), 202
    except UserNotHasRole:
        abort(404)


@blueprint.route('/users/<user_id>/roles/<role_id>', methods=['POST'])
def set_user_role(user_id, role_id):
    """ Show user """
    user = User.query.get(user_id)
    role = Role.query.get(role_id)
    if not user or not role:
        abort(404)

    try:
        UserRole.set_role(user, role)
        user.refresh()
        data = {'roles': dict_list(user.roles)}
        return jsonify(data), 201
    except UserAlreadyInRole:
        abort(409)


@blueprint.route('/users/<user_id>/roles/<role_id>', methods=['DELETE'])
def delete_user_role(user_id, role_id):
    """ Show user """
    user = User.query.get(user_id)
    role = Role.query.get(role_id)
    if not user or not role:
        abort(404)

    try:
        UserRole.delete_role(user, role)
        user.refresh()
        data = {'roles': dict_list(user.roles)}
        return jsonify(data), 202
    except UserRoleNotFound:
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


@blueprint.route('/roles/<role_id>', methods=['GET'])
def show_role(role_id):
    """ Show user """
    role = Role.query.get(role_id)
    if not role:
        abort(404)

    data = {'role': dict_object(role)}
    data['role']['users'] = dict_list(role.users)
    return jsonify(data), 200


@blueprint.route('/roles/<role_id>', methods=['POST'])
def edit_role(role_id):
    """ Show user """
    required_fields = ('name')
    if all(request.json.get(field) for field in required_fields):
        name = request.json.get('name')
        description = request.json.get('description')
    else:
        abort(400)

    role = Role.query.get(role_id)
    if not role:
        abort(404)

    try:
        role.edit(name=name, description=description)
        role.refresh()
        data = {'role': dict_object(role)}
        return jsonify(data), 202

    except InvalidRoleName:
        abort(400)

    except RoleAlreadyExist:
        abort(409)


@blueprint.route('/roles/<role_id>', methods=['DELETE'])
def delete_role(role_id):
    """ Show user """
    role = Role.query.get(role_id)
    if not role:
        abort(404)

    role.remove_all_users()
    role.delete(commit=True)

    values, total = query_object_list(Role)
    data = {'roles': values, 'total': total}
    return jsonify(data), 202


@blueprint.route('/roles/<role_id>/remove', methods=['DELETE'])
def remove_all_users(role_id):
    """ Show user """
    role = Role.query.get(role_id)
    if not role:
        abort(404)

    role.remove_all_users()
    role.refresh()

    data = {'role': dict_object(role)}
    data['role']['users'] = dict_list(role.users)
    return jsonify(data), 202
