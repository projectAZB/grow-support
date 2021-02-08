from flask import url_for, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user
from werkzeug.utils import redirect

from backend.settings import env_vars


class LogoutMenuLink(MenuLink):

    def get_url(self):
        return url_for('user_api.logout')

    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user_api.login', next=request.url))


class UserModelView(AuthenticatedModelView):
    column_exclude_list = ['password']


admin = Admin(name=env_vars.APP_NAME.lower().capitalize(), template_mode='bootstrap3')
