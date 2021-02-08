import logging

from flask import Flask


def configure_logs(app: Flask):
    level = logging.DEBUG if app.debug else logging.INFO
    app_logs = logging.getLogger('backend')
    app_logs.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s %(name)s: %(message)s'))
    app_logs.addHandler(handler)
