from celery import Celery
from flask import Flask

from backend.settings import env_vars

celery = Celery(__name__, broker=env_vars.env_rabbit_url(), backend=env_vars.env_redis_url())


def init_celery(app: Flask, _celery: Celery):
    _celery.conf.update(app.config)
    _celery.autodiscover_tasks(['backend.app.user'])
    TaskBase = _celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    _celery.Task = ContextTask
