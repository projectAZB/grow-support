from flask import Blueprint, redirect, url_for
from flask_login import current_user

from backend.common.api_utils import create_200_response
from backend.common.constants import ADMIN_PATH, USER_LOGIN_PATH


import logging

LOG = logging.getLogger(__name__)


system_api = Blueprint('system_api', __name__)


@system_api.route('/healthcheck', methods=['GET'])
def healthcheck():
    return create_200_response()


@system_api.route('/', methods=['GET'])
def base():
    if current_user.is_authenticated:
        return redirect(url_for(ADMIN_PATH))
    return redirect(url_for(USER_LOGIN_PATH))
