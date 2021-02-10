from flask_sqlalchemy import SQLAlchemy

sqla_db = SQLAlchemy()


# Weird workaround to get alembic to recognize the models
def load_models():
    from backend.user import models
    from backend.messages import models


load_models()
