from typing import Optional

from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy

from backend.user.contracts import UserRequest, UserResponse
from backend.user.errors import UserError
from backend.user.models import UserModel

import logging

LOG = logging.getLogger(__name__)


def create_user_service(sqla_db: SQLAlchemy, request: UserRequest) -> UserResponse:
    user_model: Optional[UserModel] = sqla_db.session.query(UserModel).filter_by(username=request.username).one_or_none()

    if user_model is not None:
        return UserResponse(
            success=False,
            errors=[UserError.ACCOUNT_ALREADY_EXISTS.value.format(username=request.username)]
        )

    user_model = UserModel(username=request.username)
    user_model.set_password(request.password)
    sqla_db.session.add(user_model)
    sqla_db.session.commit()

    return UserResponse(success=True)


def login_user_service(sqla_db: SQLAlchemy, request: UserRequest) -> UserResponse:
    user_model: Optional[UserModel] = sqla_db.session.query(UserModel).filter_by(username=request.username).one_or_none()

    if user_model is None:
        return UserResponse(
            success=False,
            errors=[UserError.USERNAME_NOT_FOUND.value.format(username=request.username)]
        )

    if not user_model.check_password(request.password):
        return UserResponse(
            success=False,
            errors=[UserError.INVALID_USERNAME_PASSWORD.value.format(username=request.username)]
        )

    login_user(user_model)
    return UserResponse(success=True)
