from dataclasses import dataclass

from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance


@dataclass(frozen=True)
class TwilioClient:
    client: Client
    service_sid: str

    def send_message(self, message) -> str:
        twilio_message: MessageInstance = self.client.api.account.messages.create(
            to=message.to, body=message.body, messaging_service_sid=self.service_sid
        )
        return twilio_message.sid
