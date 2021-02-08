from flask import url_for, flash
from flask_login import LoginManager
from werkzeug.utils import redirect

from backend.user.models import UserModel

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return UserModel.query.get(int(user_id))
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('user_api.login'))
