# coding: utf-8
from flask import Blueprint, request, current_app, render_template
from flask_login import login_required, login_user, logout_user, current_user
from flask_swagger import swagger
from flask.json import jsonify

from auth.actions import UserAction
from auth.exceptions import UserNotFound, InvalidCredentials

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
    return jsonify({'message': 'hello word!'})


@blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    remember = request.json.get('remember')

    if username is None or password is None:
        return jsonify({'error_code': 'empty_credentials'}), 400

    try:
        user_action = UserAction()
        if user_action.validate_password(username, password):
            login_user(username, remember=remember)
            return jsonify({'message': 'success'}), 200

    except UserNotFound:
        return jsonify({'error_code': 'user_not_found'}), 404

    except InvalidCredentials:
        return jsonify({'error_code': 'invalid_credentials'}), 401


@blueprint.route('/home', methods=['GET'])
@login_required
def home():
    user_action = UserAction()
    user = user_action.get_by_id(current_user.get_id())
    return jsonify(user)


@login_required
@blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify({'message': 'success'}), 200


@blueprint.route('/change_password', methods=['POST'])
@login_required
def change_password():
    pass