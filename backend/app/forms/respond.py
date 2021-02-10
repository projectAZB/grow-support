from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class RespondForm(FlaskForm):
    body = StringField('Body', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Send Response')
