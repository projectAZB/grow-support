from flask import url_for, request, flash
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.helpers import get_form_data
from flask_admin.menu import MenuLink
from flask_login import current_user
from markupsafe import Markup
from sqlalchemy import func
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


class OutgoingMessageModelView(AuthenticatedModelView):

    column_exclude_list = ['incoming', 'responded']

    def get_query(self):
        return self.session.query(self.model).filter(self.model.incoming == False)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.incoming == False)


class IncomingMessageModelView(AuthenticatedModelView):

    column_exclude_list = ['incoming']

    def _format_responded(view, context, model, name):
        if model.responded:
            return 'Responded'

        # render a form with a submit button for student, include a hidden field for the student id
        # note how checkout_view method is exposed as a route below
        respond_url = url_for('.respond_view')

        _html = '''
                <form action="{respond_url}" method="POST">
                    <input id="message_id" name="message_id"  type="hidden" value="{message_id}">
                    <button type='submit'>Respond</button>
                </form>
            '''.format(respond_url=respond_url, message_id=model.id)

        return Markup(_html)

    column_formatters = {'responded': _format_responded}

    @expose('respond', methods=['POST'])
    def respond_view(self):
        return_url = self.get_url('incoming_messages.index_view')
        form = get_form_data()
        if not form:
            flash('Could not get form from request.')
            return redirect(return_url)
        message_id = form['message_id']
        return redirect(f'/message/respond/{message_id}')

    def get_query(self):
        return self.session.query(self.model).filter(self.model.incoming == True)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.incoming == True)


admin = Admin(name=env_vars.APP_NAME.lower().capitalize(), template_mode='bootstrap3')
