# coding: utf-8
"""The views of login, change password and common views are here"""
from flask import Blueprint, request, current_app, render_template, abort
from flask_login import login_required, login_user, logout_user, current_user
from flask_swagger import swagger
from flask.json import jsonify

from auth.exceptions import UserNotFound, InvalidPassword, InvalidCredentials, PasswordMismatch
from auth.views import login_permission
from auth.models import User


blueprint = Blueprint('core', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/spec')
def spec():
    """View that exposes a JSON spec from API to use in swagger-ui"""
    swag = swagger(current_app)

    swag['info'] = {
        'version': '2.0',
        'title': 'Flapy Auth-API',
        'description': 'All content of web application in API for Apps',
    }

    swag['swagger'] = '2.0'
    swag['produces'] = ['application/json; charset=utf-8']
    swag['consumes'] = ['application/json; charset=utf-8']

    return jsonify(swag)


@blueprint.route('/swagger-ui', methods=['GET'])
def swagger_ui():
    """Simple view to return swagger-ui in all enviroments, except production"""
    spec_url = '{}spec'.format(request.host_url)
    return render_template('swagger-ui.html', spec_url=spec_url)


@blueprint.route('/', methods=['GET'])
def index():
    """Template index page"""
    return jsonify({'message': 'hello word!'})


@blueprint.route('/login', methods=['POST'])
def login():
    """Login

    **Authenticate user using json params.**
    ---
    tags:
      - Core
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: login_form
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
            remember:
              type: boolean
    responses:
      200:
        description: Login with success
        schema:
          id: generic_success
          properties:
            message:
              type: string
      400:
        description: Invalid json informations
        schema:
          id: generic_error
          properties:
            error_code:
              type: string
      401:
        description: Invalid credentials
        schema:
          $ref: "#/definitions/generic_error"
      404:
        description: User not found
        schema:
          $ref: "#/definitions/generic_error"
    """
    required_fields = ('username', 'password')
    if all(request.json.get(field) for field in required_fields):
        username = request.json.get('username')
        password = request.json.get('password')
        remember = request.json.get('remember')
    else:
        return abort(400)

    try:
        user = User.by_login(username)
        if user.validate_password(password):
            login_user(user, remember)
            return jsonify({'message': 'success'}), 200
        else:
            return abort(401)

    except UserNotFound:
        return abort(404)


@blueprint.route('/home', methods=['GET'])
@login_required
def home():
    """Home

    **Authenticated home for all**
    ---
    tags:
      - Core
    responses:
      200:
        description: Return user with success
        schema:
          $ref: "#/definitions/generic_success"
      401:
        description: Invalid credentials
        schema:
          $ref: "#/definitions/generic_error"
    """
    return jsonify({'message': 'I\'m user as all!'}), 200


@blueprint.route('/user', methods=['GET'])
@login_required
@login_permission('user')
def user_view():
    """User_view

    **Authenticated home for usergroup**
    ---
    tags:
      - Core
    responses:
      200:
        description: Return user with success
        schema:
          $ref: "#/definitions/generic_success"
      401:
        description: Invalid credentials
        schema:
          $ref: "#/definitions/generic_error"
      403:
        description: User not have permission
        schema:
          $ref: "#/definitions/generic_error"
    """
    return jsonify({'message': 'I\'m user with success!'}), 200


@login_required
@blueprint.route('/logout', methods=['GET'])
def logout():
    """Logout

    **Logout user**
    ---
    tags:
      - Core
    responses:
      200:
        description: Logout with success
        schema:
          $ref: "#/definitions/generic_success"
    """
    logout_user()
    return jsonify({'message': 'success'}), 200


@blueprint.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """Change password

    **Change user password using json params.**
    ---
    tags:
      - Core
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: change_password_form
          required:
            - old_password
            - password
            - confirm_password
          properties:
            old_password:
              type: string
            password:
              type: string
            confirm_password:
              type: string
    responses:
      200:
        description: Change with success
        schema:
          id: generic_success
          properties:
            message:
              type: string
      400:
        description: Invalid json informations
        schema:
          $ref: "#/definitions/generic_error"
      401:
        description: Invalid credentials
        schema:
          $ref: "#/definitions/generic_error"
    """
    required_fields = ('old_password', 'password', 'confirm_password')
    if all(request.json.get(field) for field in required_fields):
        old_password = request.json.get('old_password')
        password = request.json.get('password')
        confirm_password = request.json.get('confirm_password')
    else:
        return abort(400)

    try:
        user = User.by_login(current_user.username)
        user.change_password(old_password=old_password, password=password, confirm_password=confirm_password)
        return jsonify({'message': 'success'}), 200

    except (InvalidPassword, PasswordMismatch):
        return abort(400)

    except InvalidCredentials:
        return abort(401)
