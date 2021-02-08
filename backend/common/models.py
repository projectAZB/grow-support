import logging
from datetime import datetime, timezone
from functools import partial

from backend.app.database import sqla_db as sqla

LOG = logging.getLogger(__name__)


class BaseModel(sqla.Model):
    __abstract__ = True

    id = sqla.Column(sqla.Integer, primary_key=True)
    created = sqla.Column(sqla.DateTime, default=partial(datetime.now, tz=timezone.utc))
    updated = sqla.Column(sqla.DateTime, nullable=True, default=None, onupdate=partial(datetime.now, tz=timezone.utc))
