from dataclasses import asdict

from flask import Blueprint, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

from backend.app.forms.respond import RespondForm
from backend.messages.contracts import OutgoingMessageRequest
from backend.messages.entities import Message
from backend.messages.models import MessageModel
from backend.messages.tasks import send_message_task

import logging

LOG = logging.getLogger(__name__)

message_api = Blueprint('message_api', __name__, url_prefix='/message')


@message_api.route('/respond/<int:message_id>', methods=['POST', 'GET'])
def respond(sqla_db: SQLAlchemy, message_id: int):
    form = RespondForm()

    message_model: MessageModel = sqla_db.session.query(MessageModel).get(message_id)

    if form.validate_on_submit():
        outgoing_message_request = OutgoingMessageRequest(
            to=message_model.from_, body=form.body.data, responding_to_id=message_model.id
        )
        send_message_task.delay(**asdict(outgoing_message_request))
        message_model.responded = True
        sqla_db.session.commit()
        LOG.info(f'Responded to message {message_model.id}')
        return redirect(url_for('incoming_messages.index_view'))

    return render_template('respond.jinja2', form=form, message=Message.from_message_model(message_model))
