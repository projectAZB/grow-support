from flask import current_app
from flask_sqlalchemy import SQLAlchemy

from backend.app.celery import celery
from backend.messages.clients import TwilioClient
from backend.messages.contracts import OutgoingMessageRequest
from backend.messages.services import send_message


@celery.task()
def send_message_task(**kwargs):
    app = current_app
    sqla_db: SQLAlchemy = app.injector.get(SQLAlchemy)
    twilio_client: TwilioClient = app.injector.get(TwilioClient)
    outgoing_message_request = OutgoingMessageRequest(**kwargs)
    send_message(sqla_db, twilio_client, outgoing_message_request)
