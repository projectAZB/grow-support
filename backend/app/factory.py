from flask import Flask, request
from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy
from injector import inject
from twilio.rest import Client

from backend.app.admin import admin, LogoutMenuLink, IncomingMessageModelView, OutgoingMessageModelView
from backend.app.celery import init_celery, celery
from backend.app.database import sqla_db
from backend.app.log_config import configure_logs
from backend.app.login_manager import login_manager
from backend.messages.api import message_api
from backend.messages.clients import TwilioClient
from backend.messages.models import MessageModel
from backend.messages.webhooks.twilio import twilio_webhooks
from backend.settings.env_vars import env_db_url, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_MESSAGING_SERVICE_SID
from backend.app.api import system_api

import logging

from backend.user.api import user_api

LOG = logging.getLogger(__name__)


def configure_dependency_injections(binder):
    binder.bind(SQLAlchemy, to=sqla_db, scope=request)
    binder.bind(Client, to=Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))

    @inject
    def create_twilio_client(client: Client):
        return TwilioClient(client, TWILIO_MESSAGING_SERVICE_SID)

    binder.bind(TwilioClient, to=create_twilio_client)


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
        admin.add_view(IncomingMessageModelView(model=MessageModel, session=sqla_db.session, name='Incoming Messages', endpoint='incoming_messages'))
        admin.add_view(OutgoingMessageModelView(model=MessageModel, session=sqla_db.session, name='Outgoing Messages', endpoint='outgoing_messages'))

    # Add Blueprints
    app.register_blueprint(system_api)
    app.register_blueprint(user_api)
    app.register_blueprint(message_api)
    app.register_blueprint(twilio_webhooks)

    # Dependency Injection
    app.injector = FlaskInjector(app=app, modules=[configure_dependency_injections]).injector

    return app
