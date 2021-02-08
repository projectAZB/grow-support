from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

from backend.common.api_utils import create_200_response
from backend.forms.login import LoginForm
from backend.user.contracts import UserRequest, UserResponse
from backend.user.services import login_user_service


system_api = Blueprint('system_api', __name__)
user_api = Blueprint('user_api', __name__, url_prefix='/user')

ADMIN_PATH = 'admin.index'
USER_LOGIN_PATH = 'user_api.login'


@system_api.route('/healthcheck', methods=['GET'])
def healthcheck():
    return create_200_response()


@system_api.route('/', methods=['GET'])
def base():
    if current_user.is_authenticated:
        return redirect(url_for(ADMIN_PATH))
    return redirect(url_for(USER_LOGIN_PATH))


@user_api.route('/login', methods=['GET', 'POST'])
def login(sqla_db: SQLAlchemy):

    if current_user.is_authenticated:
        return redirect(url_for(ADMIN_PATH))

    form = LoginForm()
    if form.validate_on_submit():
        login_user_request = UserRequest(username=form.username.data, password=form.password.data)
        login_user_response: UserResponse = login_user_service(sqla_db, login_user_request)

        # handle failure
        if not login_user_response.success:
            flash(login_user_response.errors[0])
            return redirect(url_for(USER_LOGIN_PATH))

        next_page = request.args.get('next')
        return redirect(next_page or url_for(ADMIN_PATH))

    return render_template(
        'login.jinja2',
        form=form,
        title='Log In',
        template='login-page',
        body='Log in for Admin Access'
    )


@user_api.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(USER_LOGIN_PATH))
