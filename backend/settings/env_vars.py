import os

# Extract env variables here

APP_NAME = os.getenv('APP_NAME', 'Grow')


def get_env_variable_bool(var_name, default=None):
    value = os.getenv(var_name, default)
    if isinstance(value, bool):
        return value

    if value and value.lower() == 'true':
        return True
    if value and value.lower() == 'false':
        return False

    raise Exception(f'ImproperlyConfigured {var_name}, value must be True or False')


TESTING = get_env_variable_bool('TESTING', default=False)


def env_db_url(scrub=False):
    host = os.getenv(f'MYSQL_HOST')
    port = int(os.getenv(f'MYSQL_PORT', '3306'))
    dbname = os.getenv(f'MYSQL_DBNAME')
    user = os.getenv(f'MYSQL_USER')
    password = os.getenv(f'MYSQL_PASSWORD') if not scrub else '***'

    if TESTING:
        dbname = os.getenv(f'MYSQL_TEST_DBNAME', f'{dbname}_test')

    return f'mysql://{user}:{password}@{host}:{port}/{dbname}'


def env_redis_url():
    host = os.getenv('REDIS_HOST', 'redis')
    port = int(os.getenv('REDIS_PORT', 6379))
    return f'redis://{host}:{port}'


def env_rabbit_url():
    host = os.getenv('RABBITMQ_HOST', 'rabbit')
    port = int(os.getenv('RABBITMQ_PORT', 5672))
    return f'amqp://{host}:{port}'


SQLALCHEMY_DATABASE_URI = env_db_url()
SQLALCHEMY_TRACK_MODIFICATIONS = get_env_variable_bool('SQLALCHEMY_TRACK_MODIFICATIONS', False)

DEBUG = get_env_variable_bool('DEBUG', 'False')

FLASK_APP = '/backend/app/factory.py'
FLASK_SKIP_DOTENV = 1
PYTHONUNBUFFERED = 1

SECRET_KEY = 'secret_key'

FLASK_ADMIN_SWATCH = 'paper'

REDIS_URL = env_redis_url()
RABBIT_URL = env_rabbit_url()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_API_SID', 'xxx')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_API_TOKEN', 'xxx')
TWILIO_MESSAGING_SERVICE_SID = os.getenv('TWILIO_MESSAGING_SERVICE_SID', 'xxx')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER', '+17172290088')
