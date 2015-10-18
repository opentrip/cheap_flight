# coding: UTF-8
import os

from werkzeug.utils import import_string
from flask import Flask, url_for

from cheapflight.ext import db

__all__ = ['create_app']

blueprints = [
    'home',
]


def create_app(config=None):
    if os.environ.get('PRODUCTION_CONFIG'):
        app = Flask(__name__, static_url_path='/')
    else:
        app = Flask(__name__)

    config_app(app, config)
    config_hook(app)
    config_blueprints(app, blueprints)
    config_extensions(app)
    config_templates(app)
    return app


def config_app(app, config):
    app.config.from_object('cheapflight.config.DevelopmentConfig')
    app.config.from_envvar('PRODUCTION_CONFIG', silent=True)

    if config:
        app.config.from_object(config)

    if app.debug:
        config_app_for_debug(app)


def config_app_for_debug(app):

    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            nodated = values.pop('nodated', False)
            filename = values.get('filename', None)
            if filename and not nodated:
                file_path = os.path.join(app.root_path,
                                         endpoint, filename)
                values['_t'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)


def config_extensions(app):
    db.init_app(app)


def config_blueprints(app, blueprints):
    for bp in blueprints:
        import_name = '%s.views.%s:bp' % (__package__, bp)
        app.register_blueprint(import_string(import_name))


def config_hook(app):

    @app.before_request
    def before_request():
        pass


def config_templates(app):
    app.jinja_env.globals['DEBUG'] = app.debug
