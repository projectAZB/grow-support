import pytest
from flask_sqlalchemy import SQLAlchemy

from backend.app.factory import create_app


@pytest.fixture(scope='function')
def app():
    app = create_app()
    yield app


@pytest.fixture(scope='function')
def database(app):
    db = app.injector.get(SQLAlchemy)
    with app.test_request_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
