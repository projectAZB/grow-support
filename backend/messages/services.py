from flask_sqlalchemy import SQLAlchemy

from backend.messages.clients import TwilioClient
from backend.messages.contracts import IncomingMessageRequest, OutgoingMessageRequest, OutgoingMessageUpdateRequest
from backend.messages.entities import Message, MessageStatus
from backend.messages.models import MessageModel
from backend.settings.env_vars import TWILIO_NUMBER


def receive_incoming_message(sqla_db: SQLAlchemy, incoming_message_request: IncomingMessageRequest) -> Message:
    message_model = MessageModel(
        to=incoming_message_request.to,
        from_=incoming_message_request.from_,
        twilio_sid=incoming_message_request.twilio_sid,
        body=incoming_message_request.body,
        status=MessageStatus.RECEIVED_FROM_USER,
        incoming=True
    )

    sqla_db.session.add(message_model)
    sqla_db.session.commit()

    return Message.from_message_model(message_model)


def send_message(
        sqla_db: SQLAlchemy,
        twilio_client: TwilioClient,
        outgoing_message_request: OutgoingMessageRequest
) -> Message:
    message_model = MessageModel(
        to=outgoing_message_request.to,
        from_=TWILIO_NUMBER,
        body=outgoing_message_request.body,
        status=MessageStatus.SEND_PENDING,
        incoming=False
    )

    send_message_sid: str = twilio_client.send_message(Message.from_message_model(message_model))
    message_model.twilio_sid = send_message_sid

    sqla_db.session.add(message_model)
    sqla_db.session.commit()

    return Message.from_message_model(message_model)


def update_outgoing_message(
        sqla_db: SQLAlchemy,
        outgoing_message_update_request: OutgoingMessageUpdateRequest
) -> Message:
    message_model: MessageModel = sqla_db.session.query(MessageModel).filter_by(
        twilio_sid=outgoing_message_update_request.twilio_sid
    ).one()

    message_status_str = outgoing_message_update_request.message_status_str
    if message_status_str == 'ACCEPTED' or message_status_str == 'QUEUED':
        message_status = MessageStatus.SEND_PENDING
    elif message_status_str == 'SENT' or message_status_str == 'DELIVERED':
        message_status = MessageStatus.SENT_TO_USER
    else:
        message_status = MessageStatus.SEND_FAILED

    message_model.status = message_status
    sqla_db.session.commit()

    return Message.from_message_model(message_model)
