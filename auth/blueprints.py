# coding: utf-8


def register_blueprints(app):
    from auth.views.core import blueprint as core_blueprint
    from auth.views.admin import blueprint as admin_blueprint
    app.register_blueprint(core_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
