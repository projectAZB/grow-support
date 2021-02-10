from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class IncomingMessageRequest:
    twilio_sid: str
    body: str
    from_: str
    to: str


@dataclass(frozen=True)
class OutgoingMessageRequest:
    to: str
    body: str
    responding_to_id: int


@dataclass(frozen=True)
class OutgoingMessageUpdateRequest:
    twilio_sid: str
    from_: Optional[str]
    message_status_str: str
