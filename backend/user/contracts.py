from dataclasses import dataclass

from backend.common.contracts import BaseRequest, BaseResponse


@dataclass(frozen=True)
class UserRequest(BaseRequest):
    username: str
    password: str


@dataclass(frozen=True)
class UserResponse(BaseResponse):
    pass
