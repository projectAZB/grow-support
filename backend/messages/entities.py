from dataclasses import dataclass

from backend.common.entities import Entity
from backend.common.enums import ValueEnum


class MessageStatus(ValueEnum):
    SEND_PENDING = 'SEND_PENDING'
    SENT_TO_USER = 'SENT_TO_USER'
    SEND_FAILED = 'SEND_FAILED'
    RECEIVED_FROM_USER = 'RECEIVED_FROM_USER'


@dataclass(frozen=True)
class Message(Entity):
    to: str
    from_: str
    body: str
    status: MessageStatus

    @staticmethod
    def from_message_model(sms_message):
        return Message(
            id=sms_message.id,
            to=sms_message.to,
            from_=sms_message.from_,
            body=sms_message.body,
            status=sms_message.status
        )
