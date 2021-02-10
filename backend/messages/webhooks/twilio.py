import logging
from typing import Dict, Optional

from flask import Blueprint, request, Response
from flask_sqlalchemy import SQLAlchemy

from backend.messages.contracts import IncomingMessageRequest, OutgoingMessageUpdateRequest
from backend.messages.entities import Message
from backend.messages.services import receive_incoming_message, update_outgoing_message

LOG = logging.getLogger(__name__)

twilio_webhooks = Blueprint('twilio', __name__, url_prefix='/twilio')


@twilio_webhooks.route('/incoming_sms', methods=['GET', 'POST'])
def incoming_sms_webhook(sqla_db: SQLAlchemy):
    request_data: Dict = request.form
    message_sid: str = request_data['MessageSid']
    body: str = request_data['Body']
    from_: str = request_data['From']
    to: str = request_data['To']
    incoming_message_request = IncomingMessageRequest(twilio_sid=message_sid, body=body, from_=from_, to=to)
    message: Message = receive_incoming_message(sqla_db, incoming_message_request)
    LOG.info(f'Saved message from {message.from_} with id {message.id} to database')
    return Response(status=204)


@twilio_webhooks.route('/outgoing_sms_status', methods=['POST'])
def outgoing_sms_status_webhook(sqla_db: SQLAlchemy):
    request_data: Dict = request.form
    message_sid: str = request_data['MessageSid']
    status_str: str = request_data['MessageStatus'].upper()
    from_: Optional[str] = request_data.get('From', None)
    update_request = OutgoingMessageUpdateRequest(twilio_sid=message_sid, from_=from_, message_status_str=status_str)
    update_outgoing_message(sqla_db, update_request)
    return Response(status=204)
