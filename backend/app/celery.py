from celery import Celery
from flask import Flask

from backend.settings.env_vars import RABBIT_URL, REDIS_URL

celery = Celery(__name__, broker=RABBIT_URL, backend=REDIS_URL)


def init_celery(app: Flask, _celery: Celery):
    _celery.conf.update(app.config)
    _celery.autodiscover_tasks(['backend.app.messages'])
    TaskBase = _celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    _celery.Task = ContextTask
