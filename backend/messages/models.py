from backend.common.constants import PHONE_NUMBER_FIELD_LENGTH
from backend.common.models import BaseModel

from backend.app.database import sqla_db as sqla
from backend.messages.entities import MessageStatus


class MessageModel(BaseModel):
    __tablename__ = 'message'

    to = sqla.Column(sqla.String(PHONE_NUMBER_FIELD_LENGTH), nullable=False)
    from_ = sqla.Column(sqla.String(PHONE_NUMBER_FIELD_LENGTH), nullable=False)
    body = sqla.Column(sqla.String(255), nullable=False)
    incoming = sqla.Column(sqla.Boolean, nullable=False)
    status = sqla.Column(MessageStatus.sqla_values_enum(), nullable=False)
    twilio_sid = sqla.Column(sqla.String(100))
    responded = sqla.Column(sqla.Boolean, nullable=False, default=False)
