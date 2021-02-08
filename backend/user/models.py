from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from backend.common.models import BaseModel
from backend.app.database import sqla_db as sqla

import logging

LOG = logging.getLogger(__name__)


class UserModel(UserMixin, BaseModel):
    __tablename__ = 'user'

    username = sqla.Column(sqla.String(40), index=True)
    password = sqla.Column(sqla.String(200))

    def is_active(self):
        """All users are by default active"""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements"""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated"""
        return True

    def is_anonymous(self):
        """Anonymous users aren't supported"""
        return False

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
