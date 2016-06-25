# coding: utf-8
from flask import make_response
from flask.json import jsonify


def error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return make_response(jsonify({'error_code': 'bad_request'}), 400)

    @app.errorhandler(401)
    def not_authorized(error):
        return make_response(jsonify({'error_code': 'not_authorized'}), 401)

    @app.errorhandler(403)
    def not_authorized(error):
        return make_response(jsonify({'error_code': 'forbidden'}), 403)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error_code': 'not_found'}), 404)

    @app.errorhandler(500)
    def server_error(error):
        return make_response(jsonify({'error_code': 'internal_error'}), 500)

    return app
