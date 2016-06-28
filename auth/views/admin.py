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
def home():
    """Admin home

    Show last updates in user administration
    ---
    tags:
      - User
      - Role
    definitions:
      - schema:
          id: Role
          properties:
            active:
              type: boolean
            created_at:
              type: string
            description:
              type: string
            id:
              type: number
            name:
              type: string
      - schema:
          id: User
          properties:
            active:
              type: boolean
            created_at:
              type: string
            current_login_at:
              type: string
            email:
              type: string
            id:
              type: number
            last_login_at:
              type: string
            login_count:
              type: number
            password:
              type: string
            username:
              type: string
    responses:
      200:
        description: Last updates
        schema:
          id: last_updates
          properties:
            latest:
              properties:
                roles:
                  type: array
                  items:
                    $ref: "#/definitions/Role"
                users:
                  type: array
                  items:
                    $ref: "#/definitions/User"
            total:
              properties:
                roles:
                  type: number
                users:
                  type: number
    """
    users, total_users = query_object_list(User, paginable=False)
    roles, total_roles = query_object_list(Role, paginable=False)

    data = {
        'latest': {'users': users, 'roles': roles},
        'total': {'users': total_users, 'roles': total_roles}
    }

    return jsonify(data), 200


@blueprint.route('/users', methods=['GET'])
def users():
    """ Get Users

    Show all users in base
    ---
    tags:
      - User
    responses:
      200:
        description: All users
        schema:
          id: all_users
          properties:
            users:
              schema:
                $ref: "#/definitions/User"
            total:
              type: number
    """
    values, total = query_object_list(User)
    data = {'users': values, 'total': total}
    return jsonify(data), 200


@blueprint.route('/users', methods=['POST'])
def create_user():
    """ Create User

    Create a new user
    ---
    tags:
      - User
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: create_edit_user_form
          required:
            - username
            - email
            - password
            - confirm_password
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
            confirm_password:
              type: string
    responses:
      201:
        description: Created User
        schema:
          id: create_edit_user
          properties:
            user:
              schema:
                $ref: "#/definitions/User"
      400:
        description: Invalid json informations
        schema:
          $ref: "#/definitions/generic_error"
      401:
        description: Invalid credentials
        schema:
          $ref: "#/definitions/generic_error"
      409:
        description: Conflict
        schema:
          $ref: "#/definitions/generic_error"
    """
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
    """ Show User

    Show a single user
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
    responses:
      200:
        decription: show user
        schema:
          id: show_user
          properties:
            user:
              schema:
                id: User_with_roles
                properties:
                  active:
                    type: boolean
                  created_at:
                    type: string
                  current_login_at:
                    type: string
                  email:
                    type: string
                  id:
                    type: number
                  last_login_at:
                    type: string
                  login_count:
                    type: number
                  password:
                    type: string
                  username:
                    type: string
                  roles:
                    type: array
                    items:
                      $ref: "#/definitions/Role"
      404:
        description: Not Found
        schema:
          $ref: "#/definitions/generic_error"
    """
    user = User.query.get(user_id)
    if not user:
        abort(404)

    data = {'user': dict_object(user)}
    data['user']['roles'] = dict_list(user.roles)
    return jsonify(data), 200


@blueprint.route('/users/<user_id>/status', methods=['POST'])
def toogle_user_status(user_id):
    """ Toogle User Status

    Change user status **active** = `true` or `false`
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        required: true
    responses:
      202:
        decription: Create User
        schema:
          $ref: "#/definitions/User_with_roles"
      404:
        description: Not Found
        schema:
          $ref: "#/definitions/generic_error"
    """
    user = User.query.get(user_id)
    if not user:
        abort(404)

    user.toggle_status()
    user.refresh()

    data = {'user': dict_object(user)}
    data['user']['roles'] = dict_list(user.roles)
    return jsonify(data), 202


@blueprint.route('/users/<user_id>/roles', methods=['GET'])
def show_user_roles(user_id):
    """ Show User Roles

    Show all roles of a single user
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        required: true
    responses:
      200:
        description: Create User
        schema:
          id: user_roles
          properties:
            roles:
              type: array
              items:
                $ref: "#/definitions/Role"
      404:
        description: Not Found
        schema:
          $ref: "#/definitions/generic_error"
    """
    user = User.query.get(user_id)
    if not user:
        abort(404)

    data = {'roles': dict_list(user.roles)}
    return jsonify(data), 200


@blueprint.route('/users/<user_id>/roles', methods=['DELETE'])
def delete_user_roles(user_id):
    """ Remove All User's Role

    Remove all roles of a user
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        required: true
    responses:
      202:
        decription: Create User
        schema:
          $ref: "#/definitions/User_with_role"
      404:
        description: Not Found
        schema:
          $ref: "#/definitions/generic_error"
    """
    user = User.query.get(user_id)
    if not user:
        abort(404)

    try:
        user.delete_all_roles()
        user.refresh()
        data = {'user': dict_object(user)}
        data['user']['roles'] = dict_list(user.roles)
        return jsonify(data), 202
    except UserNotHasRole:
        abort(404)


@blueprint.route('/users/<user_id>/roles/<role_id>', methods=['POST'])
def set_user_role(user_id, role_id):
    """ Set User Role

    Set a role to user
    ---
    tags:
      - Permissions
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
      - name: role_id
        in: path
        type: string
        required: true
    responses:
      201:
        description: Create User
        schema:
          $ref: "#/definitions/User_with_role"
      404:
        description: Not Found
        schema:
          $ref: "#/definitions/generic_error"
      409:
        description: Conflict
        schema:
          $ref: "#/definitions/generic_error"
    """
    user = User.query.get(user_id)
    role = Role.query.get(role_id)
    if not user or not role:
        abort(404)

    try:
        UserRole.set_role(user, role)
        user.refresh()
        data = {'user': dict_object(user)}
        data['user']['roles'] = dict_list(user.roles)
        return jsonify(data), 201
    except UserAlreadyInRole:
        abort(409)


@blueprint.route('/users/<user_id>/roles/<role_id>', methods=['DELETE'])
def delete_user_role(user_id, role_id):
    """ Delete User Role

    Delete one role of user
    ---
    tags:
      - Permissions
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
      - name: role_id
        in: path
        type: string
        required: true
    responses:
      201:
        description: Create User
        schema:
          $ref: "#/definitions/User_with_role"
      404:
        description: Not Found
        schema:
          $ref: "#/definitions/generic_error"
      409:
        description: Conflict
        schema:
          $ref: "#/definitions/generic_error"
    """
    user = User.query.get(user_id)
    role = Role.query.get(role_id)
    if not user or not role:
        abort(404)

    try:
        UserRole.delete_role(user, role)
        user.refresh()
        data = {'user': dict_object(user)}
        data['user']['roles'] = dict_list(user.roles)
        return jsonify(data), 202
    except UserRoleNotFound:
        abort(409)


@blueprint.route('/roles', methods=['GET'])
# @login_required
def roles():
    """ Get Roles

    Show all roles in base
    ---
    tags:
      - Role
    responses:
      200:
        description: All roles
        schema:
          id: all_roles
          properties:
            roles:
              schema:
                $ref: "#/definitions/Role"
            total:
              type: number
    """
    login_permission([blueprint.name])

    values, total = query_object_list(Role)
    data = {'roles': values, 'total': total}
    return jsonify(data), 200


@blueprint.route('/roles', methods=['POST'])
def create_role():
    """ Create Role

     Create a new role
     ---
     tags:
       - Role
     parameters:
       - in: body
         name: body
         required: true
         schema:
           id: create_edit_role_form
           required:
             - name
           properties:
             name:
               type: string
             description:
               type: string
     responses:
       201:
         description: Created Role
         schema:
           id: create_edit_role
           properties:
             role:
               schema:
                 $ref: "#/definitions/Role"
       400:
         description: Invalid json informations
         schema:
           $ref: "#/definitions/generic_error"
       401:
         description: Invalid credentials
         schema:
           $ref: "#/definitions/generic_error"
       409:
         description: Conflict
         schema:
           $ref: "#/definitions/generic_error"
     """
    name = request.json.get('name')
    description = request.json.get('description')

    if not name:
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
    """ Show Role

    Show a single role
    ---
    tags:
      - Role
    parameters:
      - name: role_id
        in: path
        type: string
        required: true
    responses:
      200:
        decription: show_role
        schema:
          id: show_role
          properties:
            user:
              schema:
                id: Role_with_users
                properties:
                  active:
                    type: boolean
                  created_at:
                    type: string
                  name:
                    type: string
                  description:
                    type: string
                  id:
                    type: number
                  users:
                    type: array
                    items:
                      $ref: "#/definitions/User"
      404:
        description: Not Found
        schema:
          $ref: "#/definitions/generic_error"
    """
    role = Role.query.get(role_id)
    if not role:
        abort(404)

    data = {'role': dict_object(role)}
    data['role']['users'] = dict_list(role.users)
    return jsonify(data), 200


@blueprint.route('/roles/<role_id>/users', methods=['GET'])
def show_role_users(role_id):
    """ Show Role's Users

    Show all users in role
    ---
    tags:
      - Role
    parameters:
      - name: role_id
        in: path
        type: string
        required: true
    responses:
      200:
        decription: show_role
        schema:
          id: show_role
          properties:
            users:
              type: array
              items:
                $ref: "#/definitions/User"
      404:
        description: Not Found
        schema:
          $ref: "#/definitions/generic_error"
    """
    role = Role.query.get(role_id)
    if not role:
        abort(404)

    data = {'users': dict_list(role.users)}
    return jsonify(data), 200


@blueprint.route('/roles/<role_id>', methods=['POST'])
def edit_role(role_id):
    """ Edit Role

     Edit a role
     ---
     tags:
       - Role
     parameters:
       - name: role_id
         in: path
         type: string
         required: true
       - in: body
         name: body
         required: true
         schema:
           $ref: "#/definitions/create_edit_role_form"
     responses:
       202:
         description: Created Role
         schema:
           $ref: "#/definitions/create_edit_role"
       400:
         description: Invalid json informations
         schema:
           $ref: "#/definitions/generic_error"
       401:
         description: Invalid credentials
         schema:
           $ref: "#/definitions/generic_error"
       409:
         description: Conflict
         schema:
           $ref: "#/definitions/generic_error"
     """
    name = request.json.get('name')
    description = request.json.get('description')

    if not name:
        return abort(400)

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
    """ Delete Role

    Show all roles in base
    ---
    tags:
      - Role
    parameters:
      - name: role_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: All roles
        schema:
          $ref: "#/definitions/all_role"
    """
    role = Role.query.get(role_id)
    if not role:
        abort(404)

    role.remove_all_users()
    role.delete(commit=True)

    values, total = query_object_list(Role)
    data = {'roles': values, 'total': total}
    return jsonify(data), 202


@blueprint.route('/roles/<role_id>/users', methods=['DELETE'])
def remove_all_users(role_id):
    """ Remove All Role's User

    Remove all users of a role
    ---
    tags:
      - Role
    parameters:
      - name: role_id
        in: path
        type: string
        required: true
    responses:
      202:
        description: Created Role
        schema:
          $ref: "#/definitions/create_edit_role"
      404:
        description: Not Found
        schema:
          $ref: "#/definitions/generic_error"
    """
    role = Role.query.get(role_id)
    if not role:
        abort(404)

    role.remove_all_users()
    role.refresh()

    data = {'role': dict_object(role)}
    data['role']['users'] = dict_list(role.users)
    return jsonify(data), 202
