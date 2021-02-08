from flask import Flask, request
from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy

from backend.app.admin import admin, UserModelView, LogoutMenuLink
from backend.app.celery import init_celery, celery
from backend.app.database import sqla_db
from backend.app.log_config import configure_logs
from backend.app.login_manager import login_manager
from backend.settings.env_vars import env_db_url
from backend.app.api import user_api, system_api
from backend.user.models import UserModel

import logging

LOG = logging.getLogger(__name__)


def configure_dependency_injections(binder):
    binder.bind(SQLAlchemy, to=sqla_db, scope=request)


def create_app():
    app = Flask(__name__)

    app.config.from_object('backend.settings.env_vars')
    configure_logs(app)

    LOG.info('Initializing MySQL connection (uri=%s)...', env_db_url(scrub=True))
    sqla_db.init_app(app)
    login_manager.init_app(app)
    init_celery(app, celery)

    if not app.testing:
        admin.init_app(app)
        admin.add_link(LogoutMenuLink(name='Logout'))
        admin.add_view(UserModelView(model=UserModel, session=sqla_db.session))

    # Add Blueprints
    app.register_blueprint(system_api)
    app.register_blueprint(user_api)

    # Dependency Injection
    app.injector = FlaskInjector(app=app, modules=[configure_dependency_injections]).injector

    return app
