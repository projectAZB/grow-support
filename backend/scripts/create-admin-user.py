#!/usr/bin/env python

from flask_sqlalchemy import SQLAlchemy

from backend.app.factory import create_app
from backend.common.errors import string_from_errors
from backend.user.contracts import UserResponse, UserRequest
from backend.user.services import create_user_service

import logging

LOG = logging.getLogger(__name__)

if __name__ == '__main__':

    username = None
    while not username:
        username = input('Choose a Username (alphanumeric only): ')
        if not username.isalnum():
            username = None

    password = None
    while not password:
        password = input('Choose a Password: ')
        if not password.isalnum():
            password = None

    app = create_app()
    sqla_db = app.injector.get(SQLAlchemy)

    with app.app_context():
        user_request: UserRequest = UserRequest(username=username, password=password)
        user_response: UserResponse = create_user_service(sqla_db, user_request)

        if not user_response.success:
            print(string_from_errors(user_response.errors))
            exit(1)

        msg = f'Created user with username: {username}'
        print(msg)
        LOG.info(msg)
